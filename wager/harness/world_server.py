"""WorldServer -- the authority of an episode (server side).

Owns the world, the budget ledger, the source/experiment costs, smoke
validation and battery scoring; logs the trajectory. The agent reaches it only
through verbs that take and return DATA (Decision Log v0.14): describe/observe/
experiment return dicts/DataFrames; submit returns a SubmitResult. R (the battery
score) is computed here and kept server-side -- never handed back to the agent.

The same server backs both paths: scripted solvers call it in-process (C2);
the LLM reaches it across a process boundary via a data-only proxy (C3).
"""

from dataclasses import dataclass, field
from types import SimpleNamespace
from typing import Callable

import numpy as np
import pandas as pd

from wager.contracts import (
    Battery,
    EpisodeConfig,
    ExperimentDesign,
    ScoringParams,
    SubmitResult,
)
from wager.contracts.episode import SourceConfig
from wager.contracts.world import Regime
from wager.harness.source_view import experiment_view, source_view
from wager.reward.episode_score import score_episode_submission
from wager.reward.sandbox import SandboxedSubmission, SandboxError, lint_submission
from wager.reward.seeds import derive_seed

SMOKE_N = 200


class BudgetError(RuntimeError):
    pass


@dataclass
class VerbEvent:
    verb: str
    args: dict
    cost: float
    budget_remaining: float
    note: str = ""


@dataclass
class ScoringArtifacts:
    """Server-side artifacts for scoring a submission (never seen by the agent)."""

    world_source: str
    naive_code: str
    null_code: str
    battery: Battery
    params: ScoringParams
    functionals: list = field(default_factory=list)  # declared stakes functionals (v0.60)
    # window worlds (Decision Log v0.63): the LEGAL bayes-ceiling fixture that
    # anchors S_truth (world.py is the ILLEGAL player there), plus the ONE
    # choke point that materializes runtime-only context (cal_window) from the
    # persisted scalar. Both None for every non-window world (inert).
    truth_code: str | None = None
    enrich_regime: Callable | None = None
    # trajectory worlds (v0.68-R1): long->wide pivot for every scored sample;
    # None (inert) for every static world.
    sample_transform: Callable | None = None


@dataclass
class WorldServer:
    world_sample: Callable
    columns: list[str]
    brief: str
    config: EpisodeConfig
    scoring: ScoringArtifacts
    control_surface: dict = field(default_factory=dict)
    case_id: str = ""
    seed_offset: int = 0  # shifts observe/experiment draws across episodes (E0.5)

    def __post_init__(self) -> None:
        self._spent = 0.0
        self._seq = 0
        self.trajectory: list[VerbEvent] = []
        self.terminal = False
        self.result: dict | None = None  # server-side: includes R
        self._unlocked: dict = {}        # sources revealed by fired events (D4)
        self._fired_events: set = set()
        self._rows_bought: dict = {}     # per-source totals (max_rows/unlock_after)
        self._turn = 0                   # last begin_turn index (register latency)
        self._register_jobs: list = []   # queued own-model diagnostics (lab largo)
        self._register_versions: dict = {}  # line -> artifact version counter

    # --- sealed mid-episode events (D4, ADR 0081) -----------------------
    def begin_turn(self, turn_idx: int) -> list[str]:
        """Called by the episode loop (and scripted robots) at the START of
        each turn. Fires every pending event whose trigger is met -- turn
        reached OR spend fraction reached, whichever FIRST -- unlocking its
        source and returning the sealed notices to prepend to the prompt."""
        notices = []
        self._turn = turn_idx
        frac = self._spent / self.config.budget if self.config.budget else 0.0
        for i, ev in enumerate(self.config.events):
            if i in self._fired_events or self.terminal:
                continue
            if turn_idx >= ev.trigger_turn or frac >= ev.trigger_spend_frac:
                self._fired_events.add(i)
                self._unlocked[ev.source_name] = ev.source
                notices.append(ev.notice)
                self._log("event", {"source": ev.source_name, "turn": turn_idx}, 0.0,
                          note=ev.notice[:120])
        # own-model diagnostics due this turn (lab largo): evaluated at delivery
        due = [j for j in self._register_jobs if j["due"] <= turn_idx and not j["done"]]
        for job in due:
            job["done"] = True
            notices.append(self._eval_register(job))
        return notices

    @property
    def _sources(self) -> dict:
        return {**self.config.observe_sources, **self._unlocked}

    # --- ledger --------------------------------------------------------
    @property
    def budget_remaining(self) -> float:
        return self.config.budget - self._spent

    def _charge(self, cost: float, verb: str) -> None:
        if cost > self.budget_remaining + 1e-9:
            raise BudgetError(
                f"{verb} costs {cost:.1f} but only {self.budget_remaining:.1f} budget remains"
            )
        self._spent += cost

    def _next_seed(self, base: int) -> int:
        self._seq += 1
        return base + self.seed_offset * 100_000 + self._seq

    # --- source views (v0.54-2/v0.56: the agent sees VIEWS, the exam grades
    # the PROCESS; first implemented for source-trap worlds) ----------------
    def _source_view_columns(self, spec) -> list[str]:
        # EMPIRICAL view schema (D2/D4 worlds broke the reconstruct-from-
        # deliverable logic: views may carry extra world columns like the era
        # timestamp, hide others, or belong to an unlocked event source): draw
        # a tiny fixed-seed sample through the REAL view and report its
        # columns -- always truthful by construction.
        tiny = source_view(self.world_sample, spec, 5, 424242)
        return list(tiny.columns)

    @property
    def _meter(self):
        """The case's DECLARED measurement channel (meta.episode.experiment_meter,
        v0.58-2 -- never positional): experiments bypass historical SELECTION,
        never the meter (v0.9). Raises if a source declares a channel but the
        meter is undeclared (a positional guess would bite silently)."""
        if self.config.experiment_meter is not None:
            return self.config.observe_sources[self.config.experiment_meter].channel
        if any(s.channel is not None for s in self.config.observe_sources.values()):
            raise ValueError(
                "a source declares a measurement channel but meta.episode."
                "experiment_meter is undeclared (v0.58-2: declared, not positional)"
            )
        return None

    @property
    def _meter_batch(self):
        """The meter's per-batch offset structure (#9, ADR 0078): applies to
        experiments too (same instrument, fresh runs) -- the historical
        drift/ramp confound is what randomization buys off."""
        if self.config.experiment_meter is not None:
            return self.config.observe_sources[self.config.experiment_meter].batch
        return None

    # --- verbs ---------------------------------------------------------
    def describe(self) -> dict:
        return {
            "brief": self.brief,
            # the DELIVERABLE schema: what model(regime, n, seed) must return
            # (the system's true behavior -- family #19, v0.54-2)
            "schema": list(self.columns),
            # per-source VIEW schemas: what observe(source) actually returns
            # (measured columns, incl. __rep1/__rep2). Costs yes; the filter's
            # acceptance rate NEVER (discovering selection IS the investigation).
            "sources": {
                name: {
                    "cost_per_row": s.cost_per_row,
                    "columns": self._source_view_columns(s),
                }
                for name, s in self._sources.items()
            },
            "experiment_cost": {
                "cost_fixed": self.config.experiment.cost_fixed,
                "cost_per_row": self.config.experiment.cost_per_row,
            },
            "control_surface": self.control_surface,
            "budget_total": self.config.budget,
            "budget_remaining": self.budget_remaining,
        }

    def observe(self, source: str, n: int) -> pd.DataFrame:
        self._guard_open()
        if source not in self._sources:
            raise KeyError(f"unknown source {source!r}; available: {list(self._sources)}")
        if n <= 0 or n > 5000:
            raise ValueError("n must be in 1..5000")
        spec = self._sources[source]
        # sequential-access guards (rabbit_hole_v1): escalation is one commit
        # at a time, and an archive layer is a FINITE object.
        if spec.unlock_after is not None:
            prev = self._sources.get(spec.unlock_after)
            need = prev.max_rows if (prev is not None and prev.max_rows) else 1
            if self._rows_bought.get(spec.unlock_after, 0) < need:
                raise ValueError(
                    f"source {source!r} is locked: it opens after {spec.unlock_after!r} "
                    f"has been fully read ({need} rows)"
                )
        if spec.max_rows is not None:
            left = spec.max_rows - self._rows_bought.get(source, 0)
            if n > left:
                raise ValueError(
                    f"source {source!r} has {left} rows left this episode "
                    f"(cap {spec.max_rows}); requested {n}"
                )
        cost = spec.cost_per_row * n
        self._charge(cost, f"observe({source!r}, {n})")
        self._rows_bought[source] = self._rows_bought.get(source, 0) + n
        # the agent receives the SOURCE VIEW (selection + channel per the
        # declared pipeline), never the clean mechanism (v0.55/v0.56)
        df = source_view(self.world_sample, spec, n, self._next_seed(700_000))
        self._log("observe", {"source": source, "n": n}, cost)
        return df

    def experiment(self, design: ExperimentDesign) -> pd.DataFrame:
        self._guard_open()
        # trajectory pricing (v0.68-R3): n counts UNITS; every (unit, timestamp)
        # reading is a row, and leaving the run going costs per horizon -- THE
        # knob that makes knowing K expensive. Static worlds: grid absent,
        # cost_per_horizon 0.0 -> byte-identical to the old formula.
        grid = design.context.get("t_grid")
        if (self.config.experiment.n_exact is not None
                and design.n != self.config.experiment.n_exact):
            raise ValueError(
                f"experiments run as indivisible lots of n={self.config.experiment.n_exact} "
                f"(requested n={design.n})"
            )
        n_readings = design.n * (len(grid) if isinstance(grid, tuple) and grid else 1)
        horizon_span = max(grid) if isinstance(grid, tuple) and grid else 0.0
        cost = (self.config.experiment.cost_fixed
                + self.config.experiment.cost_per_row * n_readings
                + self.config.experiment.cost_per_horizon * horizon_span)
        self._charge(cost, f"experiment(n={design.n})")
        # The experiment runs the MECHANISM fresh under the chosen assignment --
        # randomization bypasses the historical SELECTION, but NEVER the
        # measurement channel (v0.9): the same imperfect meter reads the result.
        meter_hidden = (self.config.observe_sources[self.config.experiment_meter].hidden_columns
                        if self.config.experiment_meter is not None else ())
        df = experiment_view(
            self.world_sample, _ns(design.to_regime()), self._meter,
            design.n, self._next_seed(800_000), source_batch=self._meter_batch,
            hidden_columns=meter_hidden,
        )
        self._log("experiment", {"config": dict(design.config), "context": dict(design.context), "n": design.n}, cost)
        return df

    def register(self, line: int, code: str) -> dict:
        """Own-work worlds (lab largo, r21): register a provisional model for
        ONE line. Free in money; the diagnostic arrives with latency through
        the next begin_turn notices (coarse: RMSE +- SE + dominant residual
        band -- never an exact spectrum). One registration per turn; at most
        max_pending in flight."""
        self._guard_open()
        rc = self.config.register
        if rc is None:
            raise ValueError("this world has no registration service")
        line = int(line)
        if line not in rc.lines:
            raise ValueError(f"register: line must be one of {list(rc.lines)}")
        pending = [j for j in self._register_jobs if not j["done"]]
        if any(j["turn"] == self._turn for j in pending):
            raise ValueError("the QC desk processes ONE registration per round")
        if len(pending) >= rc.max_pending:
            raise ValueError(f"at most {rc.max_pending} diagnostics may be in flight")
        v = self._register_versions.get(line, 0) + 1
        self._register_versions[line] = v
        due = max(self._turn, 1) + rc.diag_latency
        self._register_jobs.append({"line": line, "version": v, "code": code,
                                    "turn": self._turn, "due": due, "done": False})
        self._log("register", {"line": line, "version": v}, 0.0,
                  note=f"diagnostic due turn {due}")
        return {"queued": True, "line": line, "version": v, "diagnostic_turn": due}

    def _eval_register(self, job) -> str:
        """Evaluate the agent's artifact on a rotating private panel (seeded by
        line x version, disjoint from the battery by seed family). Zero-LLM."""
        rc = self.config.register
        k, v = job["line"], job["version"]
        rng = np.random.default_rng(derive_seed(910_000 + 97 * k, v))
        drivers = rng.uniform(rc.driver_lo, rc.driver_hi, rc.panel_n)
        tag = f"[QC own-model] line {k} v{v}"
        try:
            resid = np.zeros(rc.panel_n)
            with SandboxedSubmission(job["code"], self.columns,
                                     timeout_s=20.0) as sb:
                for i, d in enumerate(drivers):
                    ns = SimpleNamespace(
                        config={rc.line_key: k, rc.driver_key: float(d)},
                        context={}, horizon=None)
                    truth = self.world_sample(ns, rc.panel_reps,
                                              derive_seed(920_000 + 97 * k + v, i))
                    pred = sb.run(ns, rc.panel_reps,
                                  derive_seed(930_000 + 97 * k + v, i))
                    resid[i] = (float(pred[self.columns[0]].mean())
                                - float(truth[self.columns[0]].mean()))
        except (SandboxError, Exception) as e:  # noqa: BLE001
            self._log("register_diag", {"line": k, "version": v}, 0.0,
                      note=f"failed: {e}")
            return f"{tag}: diagnostic FAILED ({str(e)[:120]})"
        rmse = float(np.sqrt(np.mean(resid ** 2)))
        boots = [float(np.sqrt(np.mean(rng.choice(resid, resid.size) ** 2)))
                 for _ in range(100)]
        se = float(np.std(boots))
        band_vals = []
        for lo, hi in rc.bands:
            m = (drivers >= lo) & (drivers < hi)
            band_vals.append(float(np.sqrt(np.mean(resid[m] ** 2))) if m.any() else 0.0)
        j = int(np.argmax(band_vals))
        lo, hi = rc.bands[j]
        flagged = band_vals[j] > max(rc.flag_se_mult * se, rc.flag_abs_floor)
        msg = (f"{tag}: RMSE {rmse:.3f} +- {se:.3f}; dominant residual band "
               f"driver {lo:g}-{hi:g}")
        if flagged:
            name = f"mini_line_{k}"
            self._unlocked[name] = SourceConfig(
                cost_per_row=rc.mini_cost_per_row,
                config={"__mini_line": k, "__band_lo": lo, "__band_hi": hi},
                max_rows=rc.mini_rows)
            self._rows_bought[name] = 0  # a fresh focused lot
            msg += (f" -- FLAGGED (> {rc.flag_se_mult:g}x SE): focused lot "
                    f"'{name}' available ({rc.mini_rows} rows, "
                    f"{rc.mini_cost_per_row:g}/row)")
        self._log("register_diag", {"line": k, "version": v,
                                    "rmse": round(rmse, 4)}, 0.0, note=msg[:150])
        return msg

    def submit(self, code: str) -> SubmitResult:
        self._guard_open()
        error = self._smoke(code)
        if error is not None:
            self._log("submit", {"accepted": False}, 0.0, note=error)
            return SubmitResult(accepted=False, error=error)
        # passed smoke -> terminal, score server-side
        self.result = score_episode_submission(
            code=code,
            world_sample=self.world_sample,
            world_source=self.scoring.world_source,
            naive_code=self.scoring.naive_code,
            null_code=self.scoring.null_code,
            battery=self.scoring.battery,
            columns=self.columns,
            params=self.scoring.params,
            functionals=self.scoring.functionals,
            truth_code=self.scoring.truth_code,
            enrich_regime=self.scoring.enrich_regime,
            sample_transform=self.scoring.sample_transform,
        )
        self.result["code"] = code
        self.terminal = True
        self._log("submit", {"accepted": True}, 0.0, note=f"R={self.result['R']:.3f} (server-side)")
        return SubmitResult(accepted=True)

    # --- smoke ---------------------------------------------------------
    def _smoke(self, code: str) -> str | None:
        """Return an actionable error string, or None if the submission passes.
        Error messages are the agent's UX (Decision Log v0.14, precision 3)."""
        try:
            lint_submission(code)
        except SandboxError as exc:
            return f"import/lint rejected: {exc}"
        try:
            with SandboxedSubmission(code, self.columns, timeout_s=self.scoring.params.model_call_timeout_s) as sb:
                for i, regime in enumerate(self.config.smoke_regimes):
                    try:
                        # window worlds: smoke regimes cross the SAME choke
                        # point as scoring (v0.63-4) -- a submission that reads
                        # cal_window must see one here, not crash at scoring
                        run_regime = regime
                        if self.scoring.enrich_regime is not None:
                            run_regime = self.scoring.enrich_regime(_ns(regime), derive_seed(99991, i))
                        # representative seeds (same magnitude as scoring) so a
                        # seed-range crash is caught here, not silently at scoring
                        sb.run(run_regime, SMOKE_N, derive_seed(99991, i))
                    except SandboxError as exc:
                        return (
                            f"smoke regime {i} (config={regime.config}) failed: {exc}. "
                            f"model(regime, n, seed) must return a DataFrame with columns "
                            f"exactly {self.columns}, n rows, finite numeric values."
                        )
        except SandboxError as exc:
            return f"submission could not be loaded: {exc}. Define model(regime, n, seed)."
        return None

    # --- internals -----------------------------------------------------
    def _guard_open(self) -> None:
        if self.terminal:
            raise RuntimeError("episode is terminal (already submitted)")

    def _log(self, verb: str, args: dict, cost: float, note: str = "") -> None:
        self.trajectory.append(
            VerbEvent(verb=verb, args=args, cost=cost, budget_remaining=self.budget_remaining, note=note)
        )


class _ns:
    """Plain regime view (config/context/horizon) for world.sample()."""

    def __init__(self, regime: Regime) -> None:
        self.config = dict(regime.config)
        self.context = dict(regime.context)
        self.horizon = regime.horizon
