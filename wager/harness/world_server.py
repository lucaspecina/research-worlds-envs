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
from typing import Callable

import pandas as pd

from wager.contracts import (
    Battery,
    EpisodeConfig,
    ExperimentDesign,
    ScoringParams,
    SubmitResult,
)
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
        cols = list(self.columns)
        ch = spec.channel
        if ch is not None and ch.replicates > 1:
            i = cols.index(ch.column)
            cols[i : i + 1] = [f"{ch.column}__rep{r + 1}" for r in range(ch.replicates)]
        return cols

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
                for name, s in self.config.observe_sources.items()
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
        if source not in self.config.observe_sources:
            raise KeyError(f"unknown source {source!r}; available: {list(self.config.observe_sources)}")
        if n <= 0 or n > 5000:
            raise ValueError("n must be in 1..5000")
        spec = self.config.observe_sources[source]
        cost = spec.cost_per_row * n
        self._charge(cost, f"observe({source!r}, {n})")
        # the agent receives the SOURCE VIEW (selection + channel per the
        # declared pipeline), never the clean mechanism (v0.55/v0.56)
        df = source_view(self.world_sample, spec, n, self._next_seed(700_000))
        self._log("observe", {"source": source, "n": n}, cost)
        return df

    def experiment(self, design: ExperimentDesign) -> pd.DataFrame:
        self._guard_open()
        cost = self.config.experiment.cost_fixed + self.config.experiment.cost_per_row * design.n
        self._charge(cost, f"experiment(n={design.n})")
        # The experiment runs the MECHANISM fresh under the chosen assignment --
        # randomization bypasses the historical SELECTION, but NEVER the
        # measurement channel (v0.9): the same imperfect meter reads the result.
        df = experiment_view(
            self.world_sample, _ns(design.to_regime()), self._meter,
            design.n, self._next_seed(800_000),
        )
        self._log("experiment", {"config": dict(design.config), "context": dict(design.context), "n": design.n}, cost)
        return df

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
                        # representative seeds (same magnitude as scoring) so a
                        # seed-range crash is caught here, not silently at scoring
                        sb.run(regime, SMOKE_N, derive_seed(99991, i))
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
