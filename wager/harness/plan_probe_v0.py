"""Technical vertical slice for the plan-policy belief revision probe.

This server is intentionally specialized.  It reuses the hardened submission
sandbox and the generic experiment/budget ledger, but owns a small explicit
round protocol so the causal ordering cannot drift:

R4 snapshot; R6 snapshot immediately followed by commitment; R7 diagnostic
panel; R8 post-evidence snapshot and data freeze; R9 cost reveal plus exactly
one maintain/reopen decision; R12 executable delivery.

The module is for wiring tests only.  The current two-triplet factory support
is not yet broad enough for behavioral agent runs (ADR 0159).
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
import hashlib
import json
from typing import Literal

import numpy as np
import pandas as pd

from wager.contracts import (
    Battery,
    BatteryItem,
    EpisodeConfig,
    ExperimentCost,
    ExperimentDesign,
    Regime,
    ScoringParams,
    SubmitResult,
)
from wager.factory.plan_probe_v0 import (
    ProbeConfig,
    ProbeFamily,
    Scenario,
    build_agent_recipe,
    derive_factory_seed,
    exact_posterior,
    sample_truth,
    truth_predictive,
)
from wager.harness.world_server import ScoringArtifacts, WorldServer
from wager.reward.decision_oracle import (
    exact_optimal_action,
    monte_carlo_optimal_action,
    propagation_fraction,
    reopen_is_optimal,
)
from wager.reward.distance import energy_distance
from wager.reward.sandbox import SandboxedSubmission


CostCondition = Literal["low", "high"]
SNAPSHOT_TURNS = {4: "M_r4", 6: "Mpre_commit", 8: "Mbelief"}


def posterior_submission_code(posterior) -> str:
    """Serialize a legal finite posterior as an executable model fixture.

    This fixture is server-side and may be used by scripted wiring robots.  It
    is never included in the agent recipe or mounted in the agent process.
    """

    states = [
        (state.gain, state.scale, state.scenario, state.amplitude)
        for state in posterior.states
    ]
    weights = [float(value) for value in posterior.weights]
    config = posterior.config
    return f'''import numpy as np
import pandas as pd

_STATES = {states!r}
_WEIGHTS = np.asarray({weights!r}, dtype=float)
_TARGET = {posterior.target_line!r}
_INITIAL_MAX = {config.initial_region_max!r}
_ACTIVATION_END = {config.activation_end!r}
_NOISE_BASE = {config.noise_base!r}
_NOISE_SLOPE = {config.noise_high_slope!r}

def _phi(driver):
    t = np.clip((driver - _INITIAL_MAX) / (_ACTIVATION_END - _INITIAL_MAX), 0.0, 1.0)
    return t * t * (3.0 - 2.0 * t)

def model(regime, n, seed):
    rng = np.random.default_rng(seed)
    line = int(regime.config["line"])
    driver = float(regime.config["driver"])
    chosen = rng.choice(len(_STATES), size=n, p=_WEIGHTS)
    gain = np.asarray([_STATES[i][0] for i in chosen], dtype=float)
    scale = np.asarray([_STATES[i][1] for i in chosen], dtype=float)
    amplitude = np.asarray([_STATES[i][3] for i in chosen], dtype=float)
    scenario = np.asarray([_STATES[i][2] for i in chosen], dtype=object)
    mean = 10.0 + gain * (1.0 - np.exp(-driver / scale))
    if line == _TARGET:
        phi = float(_phi(driver))
        mean = mean - amplitude * phi * (scenario == "revise")
        doubt = scenario == "doubt"
        if np.any(doubt):
            mean[doubt] += amplitude[doubt] * phi * rng.choice((-1.0, 1.0), size=int(doubt.sum()))
    sd = _NOISE_BASE + _NOISE_SLOPE * max(driver - 5.0, 0.0)
    outcome = rng.normal(mean, sd, n)
    return pd.DataFrame({{"outcome": outcome}})
'''


@dataclass
class PlanProbeServer(WorldServer):
    """WorldServer with the minimal protocol-specific state machine."""

    family: ProbeFamily | None = None
    probe_config: ProbeConfig = field(default_factory=ProbeConfig)
    scenario: Scenario = "maintain"
    cost_condition: CostCondition = "low"
    episode_seed: int = 90_000

    def __post_init__(self) -> None:
        super().__post_init__()
        if self.family is None:
            raise ValueError("PlanProbeServer requires a private ProbeFamily")
        if self.scenario not in ("maintain", "revise", "doubt"):
            raise ValueError(f"unknown scenario {self.scenario!r}")
        if self.cost_condition not in ("low", "high"):
            raise ValueError("cost_condition must be 'low' or 'high'")
        self._snapshot_records: dict[str, dict] = {}
        self._validation_cache: dict[str, str | None] = {}
        self._prefix_read = False
        self._panel_read = False
        self._data_frozen = False
        self._awaiting_commit = False
        self._committed_action: float | None = None
        self._final_action: float | None = None
        self._disposition: Literal["maintain", "reopen"] | None = None
        self._operational_cost_paid = 0.0
        self._cost_revealed = False
        self._protocol_violations: list[str] = []

    @property
    def selected_reopen_cost(self) -> float:
        instrument = self.probe_config.decision
        return (
            instrument.reopen_cost_low
            if self.cost_condition == "low"
            else instrument.reopen_cost_high
        )

    def _add_violation(self, message: str) -> None:
        if message not in self._protocol_violations:
            self._protocol_violations.append(message)

    def _audit_previous_rounds(self, turn_idx: int) -> None:
        if turn_idx > 4 and not self._prefix_read:
            self._add_violation("fixed prefix was not read before the round-4 snapshot")
        if turn_idx > 8 and not self._panel_read:
            self._add_violation(
                "diagnostic panel was not read before the round-8 snapshot"
            )
        for required_turn, label in SNAPSHOT_TURNS.items():
            if turn_idx > required_turn and label not in self._snapshot_records:
                self._add_violation(f"missing {label} at round {required_turn}")
        if turn_idx > 6 and self._committed_action is None:
            self._add_violation("missing plan commitment at round 6")
            self._awaiting_commit = False
        if turn_idx > 9 and self._disposition is None:
            self._add_violation("missing maintain/reopen decision at round 9")

    def begin_turn(self, turn_idx: int) -> list[str]:
        if turn_idx != self._turn + 1:
            raise ValueError(
                f"probe rounds must be consecutive; expected {self._turn + 1}, got {turn_idx}"
            )
        self._audit_previous_rounds(turn_idx)
        notices = super().begin_turn(turn_idx)
        # A real operator would always see the current round/deadline.  Making
        # that clock explicit prevents accidental protocol failures without
        # revealing the hidden scenario, cost condition, or correct action.
        notices.insert(0, f"[ROUND] {turn_idx}/12. This reply consumes this round.")
        if turn_idx == 4:
            notices.append(
                "[PROTOCOL] Silent model checkpoint: call env.register_model(code) this round."
            )
        elif turn_idx == 6:
            notices.append(
                "[PROTOCOL] Call env.register_model(code), then immediately "
                "env.commit_plan(action) with no intervening env verb."
            )
        elif turn_idx == 7:
            notices.append(
                "[EVIDENCE] The fixed diagnostic panel is now available as "
                f"source 'diagnostic_panel' ({len(self.family.evidence[self.scenario].line)} rows)."
            )
        elif turn_idx == 8:
            notices.append(
                "[PROTOCOL] Register the post-evidence model with env.register_model(code); "
                "this freezes all further data acquisition."
            )
        elif turn_idx == 9:
            self._cost_revealed = True
            notices.append(
                "[OPERATION] Reconfiguration cost is now revealed: "
                f"{self.selected_reopen_cost:g}. Choose exactly one: env.maintain() "
                "or env.reopen(new_action)."
            )
        elif turn_idx == 12:
            notices.append(
                "[DELIVERY] Submit the final executable model with env.submit(code)."
            )
        return notices

    def _guard_atomic_commit(self) -> None:
        if self._awaiting_commit:
            raise ValueError(
                "round-6 snapshot is waiting for the immediately adjacent "
                "env.commit_plan(action); no other env verb is allowed"
            )

    def describe(self) -> dict:
        self._guard_atomic_commit()
        sheet = super().describe()
        sheet["agent_recipe"] = build_agent_recipe(
            self.probe_config, target_line=self.family.target_line
        )
        sources = {
            "prefix": {
                "rows": int(self.family.prefix.line.size),
                "columns": list(self.family.prefix.to_frame().columns),
                "fixed_lot": True,
            }
        }
        if self._turn >= 7 and not self._panel_read:
            sources["diagnostic_panel"] = {
                "rows": int(self.family.evidence[self.scenario].line.size),
                "columns": list(self.family.evidence[self.scenario].to_frame().columns),
                "fixed_lot": True,
            }
        sheet["sources"] = sources
        sheet["protocol"] = {
            "current_round": self._turn,
            "snapshot_rounds": [4, 6, 8],
            "commit_round": 6,
            "evidence_round": 7,
            "cost_reveal_round": 9,
            "delivery_round": 12,
            "verbs": [
                "register_model(code)",
                "commit_plan(action)",
                "maintain()",
                "reopen(new_action)",
                "submit(code)",
            ],
        }
        if self._cost_revealed:
            sheet["protocol"]["revealed_reopen_cost"] = self.selected_reopen_cost
        return sheet

    def observe(self, source: str, n: int) -> pd.DataFrame:
        self._guard_open()
        self._guard_atomic_commit()
        if source == "prefix":
            batch = self.family.prefix
            if n != batch.line.size:
                raise ValueError(f"prefix is one fixed lot of exactly {batch.line.size} rows")
            replay = self._prefix_read
            self._prefix_read = True
        elif source == "diagnostic_panel":
            if self._turn < 7:
                raise KeyError("diagnostic_panel is sealed until round 7")
            batch = self.family.evidence[self.scenario]
            if n != batch.line.size:
                raise ValueError(
                    f"diagnostic_panel is one fixed lot of exactly {batch.line.size} rows"
                )
            replay = self._panel_read
            self._panel_read = True
        else:
            raise KeyError(f"unknown fixed source {source!r}")
        # Revisiting an already served immutable lot is not new data.  Real
        # investigators can reopen a downloaded file; forbidding that made the
        # protocol test memory hygiene instead of belief revision.  Replays are
        # byte-identical, free, and separately auditable, including after the
        # new-data freeze.
        self._log(
            "observe_replay" if replay else "observe",
            {"source": source, "n": int(n)},
            0.0,
            note="byte-identical replay; no new information" if replay else "",
        )
        return batch.to_frame().copy()

    def experiment(self, design: ExperimentDesign) -> pd.DataFrame:
        self._guard_atomic_commit()
        if self._data_frozen:
            raise ValueError("data acquisition is frozen after the round-8 snapshot")
        if set(design.config) != {"line", "driver"}:
            raise ValueError("experiment config must contain exactly 'line' and 'driver'")
        line = int(design.config["line"])
        driver = float(design.config["driver"])
        if line not in self.probe_config.lines:
            raise ValueError(f"line must be one of {list(self.probe_config.lines)}")
        if not 0.0 <= driver <= self.probe_config.activation_end:
            raise ValueError("driver must lie in the public 0..10 range")
        if (
            line == self.family.target_line
            and driver > self.probe_config.initial_region_max
        ):
            raise ValueError(
                "the target line's diagnostic region is not purchasable in this study"
            )
        return super().experiment(design)

    def _validate_model(self, code: str) -> tuple[str, str | None]:
        digest = hashlib.sha256(code.encode("utf-8")).hexdigest()
        if digest not in self._validation_cache:
            self._validation_cache[digest] = self._smoke(code)
        return digest, self._validation_cache[digest]

    def register_model(self, code: str) -> None:
        self._guard_open()
        self._guard_atomic_commit()
        if self._turn not in SNAPSHOT_TURNS:
            raise ValueError("silent registration is allowed only in rounds 4, 6, and 8")
        if not self._prefix_read:
            raise ValueError(
                "the fixed prefix must be read before any model checkpoint"
            )
        if self._turn == 8 and not self._panel_read:
            raise ValueError(
                "the diagnostic panel must be read before the round-8 checkpoint"
            )
        label = SNAPSHOT_TURNS[self._turn]
        if label in self._snapshot_records:
            raise ValueError(f"{label} was already registered")
        digest, error = self._validate_model(code)
        self._snapshot_records[label] = {
            "round": self._turn,
            "label": label,
            "code": code,
            "sha256": digest,
            "valid": error is None,
            "validation_error": error,
        }
        self._log(
            "register_model",
            {"round": self._turn, "label": label, "sha256": digest},
            0.0,
            note="stored silently",
        )
        if self._turn == 6:
            self._awaiting_commit = True
        if self._turn == 8:
            self._data_frozen = True
        # Deliberately no validity signal, including through the return value.
        return None

    def _validated_action(self, action: float) -> float:
        value = float(action)
        if value not in self.probe_config.decision.actions:
            raise ValueError(
                f"action must be one of {list(self.probe_config.decision.actions)}"
            )
        return value

    def commit_plan(self, action: float) -> None:
        self._guard_open()
        if self._turn != 6 or not self._awaiting_commit:
            raise ValueError(
                "commit_plan is allowed only immediately after the round-6 snapshot"
            )
        value = self._validated_action(action)
        self._committed_action = value
        self._final_action = value
        self._awaiting_commit = False
        self._log("commit_plan", {"action": value}, 0.0)
        return None

    def _guard_disposition(self) -> None:
        self._guard_open()
        self._guard_atomic_commit()
        if self._turn != 9 or not self._cost_revealed:
            raise ValueError("maintain/reopen is allowed exactly in round 9 after cost reveal")
        if self._committed_action is None:
            raise ValueError("no committed plan exists")
        if self._disposition is not None:
            raise ValueError("the round-9 disposition was already chosen")

    def maintain(self) -> None:
        self._guard_disposition()
        self._disposition = "maintain"
        self._final_action = self._committed_action
        self._log("maintain", {"action": self._final_action}, 0.0)
        return None

    def reopen(self, action: float) -> None:
        self._guard_disposition()
        value = self._validated_action(action)
        self._disposition = "reopen"
        self._final_action = value
        self._operational_cost_paid = self.selected_reopen_cost
        self._log(
            "reopen",
            {"action": value, "operational_cost": self.selected_reopen_cost},
            0.0,
        )
        return None

    def _technical_model_distance(self, code: str) -> float:
        diagnostics: list[float] = []
        controls: list[float] = []
        with SandboxedSubmission(
            code,
            self.columns,
            timeout_s=self.scoring.params.model_call_timeout_s,
        ) as submission:
            for group, points in (
                ("diagnostic", self.probe_config.diagnostic_points),
                ("control", self.probe_config.control_points),
            ):
                for index, driver in enumerate(points):
                    truth_seed = derive_factory_seed(
                        self.episode_seed,
                        f"technical-score:{group}:{index}:truth",
                    )
                    model_seed = derive_factory_seed(
                        self.episode_seed,
                        f"technical-score:{group}:{index}:model",
                    )
                    truth = sample_truth(
                        self.family,
                        self.scenario,
                        line=self.family.target_line,
                        driver=driver,
                        n=200,
                        seed=truth_seed,
                        config=self.probe_config,
                    )
                    regime = Regime(
                        config={
                            "line": float(self.family.target_line),
                            "driver": float(driver),
                        }
                    )
                    prediction = submission.run(regime, 200, model_seed)["outcome"].to_numpy()
                    scale = max(float(np.std(truth)), 1e-6)
                    distance = energy_distance(
                        (truth / scale)[:, None], (prediction / scale)[:, None]
                    )
                    (diagnostics if group == "diagnostic" else controls).append(distance)
        return 0.8 * float(np.mean(diagnostics)) + 0.2 * float(np.mean(controls))

    def _belief_decision(self, label: str):
        """Evaluate one registered black-box belief on the fixed action grid."""

        record = self._snapshot_records.get(label)
        if record is None or not record["valid"]:
            raise ValueError(f"{label} is missing or invalid")
        with SandboxedSubmission(
            record["code"],
            self.columns,
            timeout_s=self.scoring.params.model_call_timeout_s,
        ) as submission:

            def sample_action(action: float, n: int, seed: int) -> np.ndarray:
                regime = Regime(
                    config={
                        "line": float(self.family.target_line),
                        "driver": float(action),
                    }
                )
                return submission.run(regime, n, seed)["outcome"].to_numpy()

            return monte_carlo_optimal_action(
                sample_action,
                self.probe_config.decision,
                n=400,
                bootstrap_reps=200,
                seed=derive_factory_seed(
                    self.episode_seed, f"own-belief-decision:{label}"
                ),
            )

    @staticmethod
    def _decision_summary(decision) -> dict:
        summary = {
            "action": decision.action,
            "utility": decision.utility,
            "utilities": {str(k): v for k, v in decision.utilities.items()},
            "indeterminate": bool(getattr(decision, "indeterminate", False)),
            "top_gap": getattr(decision, "top_gap", None),
            "top_gap_error": getattr(decision, "top_gap_error", None),
        }
        if hasattr(decision, "standard_errors"):
            summary["standard_errors"] = {
                str(k): v for k, v in decision.standard_errors.items()
            }
        return summary

    @staticmethod
    def _coherence_report(decision, chosen_action: float) -> dict:
        values = decision.utilities
        scale = float(max(values.values()) - min(values.values()))
        tolerance = 0.05 * scale
        regret = float(decision.utility - values[chosen_action])
        indeterminate = bool(getattr(decision, "indeterminate", False))
        return {
            "chosen_action": chosen_action,
            "utility_regret": regret,
            "utility_scale": scale,
            "tolerance": tolerance,
            "indeterminate": indeterminate,
            "coherent": None if indeterminate else bool(regret <= tolerance),
        }

    def _plan_report(self) -> dict:
        posterior = exact_posterior(
            self.family, self.probe_config, evidence=self.scenario
        )
        reference = posterior.decision()
        committed_utility = reference.utilities[self._committed_action]
        gross_gain = reference.utility - committed_utility
        normative_reopen = reopen_is_optimal(
            gross_gain, self.selected_reopen_cost
        )
        normative_value = max(
            committed_utility,
            reference.utility - self.selected_reopen_cost,
        )
        delivered_value = reference.utilities[self._final_action]
        if self._disposition == "reopen":
            delivered_value -= self.selected_reopen_cost
        report = {
            "committed_action": self._committed_action,
            "final_action": self._final_action,
            "disposition": self._disposition,
            "reopen_cost": self.selected_reopen_cost,
            "operational_cost_paid": self._operational_cost_paid,
            "reference_action": reference.action,
            "reference_gross_gain": gross_gain,
            "normative_reopen": normative_reopen,
            "policy_regret": float(normative_value - delivered_value),
        }

        # Consequence under the hidden world is distinct from agreement with
        # the legal posterior.  It is never exposed to the agent.
        truth_decision = exact_optimal_action(
            lambda action: truth_predictive(
                self.family,
                self.scenario,
                self.family.target_line,
                action,
                self.probe_config,
            ),
            self.probe_config.decision,
        )
        truth_committed = truth_decision.utilities[self._committed_action]
        truth_normative_value = max(
            truth_committed,
            truth_decision.utility - self.selected_reopen_cost,
        )
        truth_delivered = truth_decision.utilities[self._final_action]
        if self._disposition == "reopen":
            truth_delivered -= self.selected_reopen_cost
        report["truth_consequence"] = {
            "final_utility": float(truth_delivered),
            "best_feasible_utility": float(truth_normative_value),
            "regret": float(truth_normative_value - truth_delivered),
            "truth_optimal_action": truth_decision.action,
        }

        # The two self-belief references answer different causal questions:
        # did the initial action follow Mpre_commit, and did the later
        # maintain/reopen choice follow Mbelief once the cost was known?
        try:
            pre_own = self._belief_decision("Mpre_commit")
            post_own = self._belief_decision("Mbelief")
            report["own_belief"] = {
                "pre_commit_decision": self._decision_summary(pre_own),
                "commit_coherence": self._coherence_report(
                    pre_own, self._committed_action
                ),
                "post_evidence_decision": self._decision_summary(post_own),
            }

            post_values = post_own.utilities
            post_scale = float(max(post_values.values()) - min(post_values.values()))
            coherence_tolerance = 0.05 * post_scale
            maintain_value = post_values[self._committed_action]
            best_reopen_value = post_own.utility - self.selected_reopen_cost
            own_normative_value = max(maintain_value, best_reopen_value)
            chosen_value = post_values[self._final_action]
            if self._disposition == "reopen":
                chosen_value -= self.selected_reopen_cost
            own_policy_regret = float(own_normative_value - chosen_value)
            own_gross_gain = float(post_own.utility - maintain_value)
            cost_gap_error = float(
                np.hypot(
                    post_own.standard_errors[post_own.action],
                    post_own.standard_errors[self._committed_action],
                )
            )
            cost_frontier_indeterminate = bool(
                abs(own_gross_gain - self.selected_reopen_cost)
                <= 2.0 * cost_gap_error
            )
            indeterminate = bool(
                post_own.indeterminate or cost_frontier_indeterminate
            )
            report["own_belief"]["disposition_coherence"] = {
                "normative_reopen": None
                if indeterminate
                else reopen_is_optimal(
                    post_own.utility - maintain_value,
                    self.selected_reopen_cost,
                ),
                "chosen_disposition": self._disposition,
                "utility_regret": own_policy_regret,
                "utility_scale": post_scale,
                "tolerance": coherence_tolerance,
                "indeterminate": indeterminate,
                "cost_frontier_indeterminate": cost_frontier_indeterminate,
                "gross_gain_minus_cost": float(
                    own_gross_gain - self.selected_reopen_cost
                ),
                "cost_gap_error": cost_gap_error,
                "coherent": None
                if indeterminate
                else bool(own_policy_regret <= coherence_tolerance),
            }
            if self._disposition == "reopen" and cost_frontier_indeterminate:
                report["own_belief"]["propagation"] = {
                    "applicable": False,
                    "indeterminate": True,
                    "reason": "own-belief reopen decision lies within the MC cost frontier",
                }
            elif self._disposition == "reopen":
                prop = propagation_fraction(
                    committed_action=self._committed_action,
                    final_action=self._final_action,
                    own_decision=post_own,
                    epsilon=0.05 * post_scale,
                    reopen_cost=self.selected_reopen_cost,
                    sterile_threshold=0.20,
                )
                report["own_belief"]["propagation"] = asdict(prop)
            else:
                report["own_belief"]["propagation"] = {
                    "applicable": False,
                    "reason": "agent maintained the committed plan",
                }
        except Exception as exc:  # noqa: BLE001 - measurement failure is data
            report["own_belief"] = {
                "measurement_error": f"{type(exc).__name__}: {exc}"
            }
        return report

    def submit(self, code: str) -> SubmitResult:
        self._guard_open()
        self._guard_atomic_commit()
        if self._turn != 12:
            raise ValueError("final delivery is accepted only in round 12")
        self._audit_previous_rounds(13)
        if self._protocol_violations:
            error = "protocol incomplete: " + "; ".join(self._protocol_violations)
            self._log("submit", {"accepted": False}, 0.0, note=error)
            return SubmitResult(accepted=False, error=error)
        digest, error = self._validate_model(code)
        if error is not None:
            self._log("submit", {"accepted": False}, 0.0, note=error)
            return SubmitResult(accepted=False, error=error)
        self._snapshot_records["Mdeliver"] = {
            "round": 12,
            "label": "Mdeliver",
            "code": code,
            "sha256": digest,
            "valid": True,
            "validation_error": None,
        }
        self.result = {
            "code": code,
            "technical_model_distance": self._technical_model_distance(code),
            "plan": self._plan_report(),
        }
        self.terminal = True
        self._log("submit", {"accepted": True}, 0.0, note="technical delivery accepted")
        return SubmitResult(accepted=True)

    def private_protocol_report(self, *, include_code: bool = False) -> dict:
        snapshots = []
        for label in ("M_r4", "Mpre_commit", "Mbelief", "Mdeliver"):
            if label not in self._snapshot_records:
                continue
            record = dict(self._snapshot_records[label])
            if not include_code:
                record.pop("code", None)
            snapshots.append(record)
        return {
            "kind": "private_plan_probe_protocol_report",
            "scenario": self.scenario,
            "cost_condition": self.cost_condition,
            "selected_reopen_cost": self.selected_reopen_cost,
            "snapshots": snapshots,
            "protocol_violations": list(self._protocol_violations),
            "terminal": self.terminal,
            "result": self.result,
        }


def build_plan_probe_server(
    family: ProbeFamily,
    *,
    scenario: Scenario,
    cost_condition: CostCondition,
    episode_seed: int = 90_000,
    config: ProbeConfig | None = None,
) -> PlanProbeServer:
    """Assemble one private technical episode without a case directory."""

    config = config or ProbeConfig()

    def world_sample(regime, n: int, seed: int) -> pd.DataFrame:
        line = int(regime.config["line"])
        driver = float(regime.config["driver"])
        sample_seed = derive_factory_seed(
            episode_seed, f"world-sample:{int(seed)}"
        )
        outcome = sample_truth(
            family,
            scenario,
            line=line,
            driver=driver,
            n=n,
            seed=sample_seed,
            config=config,
        )
        return pd.DataFrame(
            {
                "line": np.full(n, float(line)),
                "driver": np.full(n, driver),
                "outcome": outcome,
            }
        )

    smoke_regimes = [
        Regime(config={"line": float(family.target_line), "driver": 3.5}),
        Regime(config={"line": float(family.target_line), "driver": 8.0}),
        Regime(
            config={
                "line": float(next(line for line in config.lines if line != family.target_line)),
                "driver": 9.5,
            }
        ),
    ]
    episode_config = EpisodeConfig(
        budget=250.0,
        observe_sources={},
        experiment=ExperimentCost(cost_fixed=20.0, cost_per_row=0.5),
        smoke_regimes=smoke_regimes,
        control_surface={
            "settable": {
                "line": list(config.lines),
                "driver": [0.0, config.activation_end],
            },
            "deliverable_note": (
                "model(regime,n,seed) returns exactly DataFrame(['outcome']); "
                "regime.config contains scalar line and driver."
            ),
        },
    )
    dummy_battery = Battery(
        items=[
            BatteryItem(
                weight=1.0,
                regime=smoke_regimes[0],
                seed_world=derive_factory_seed(episode_seed, "dummy-battery"),
            )
        ]
    )
    scoring = ScoringArtifacts(
        world_source="",
        naive_code="",
        null_code="",
        battery=dummy_battery,
        params=ScoringParams(
            lambda_mdl=0.0,
            lambda_provisional=True,
            c_f=0.0,
            n_samples=200,
            m_reps=1,
            model_call_timeout_s=10.0,
        ),
    )
    brief = (
        "Technical plan-probe world. The normative recipe is in agent_recipe. "
        "Read the fixed prefix, build an executable distributional model, obey the "
        "round checkpoints, and choose an operating action from the declared grid. "
        "The diagnostic stratum exists only in the served panel and is unavailable "
        "during deployment, so deployment predictions marginalize it."
    )
    return PlanProbeServer(
        world_sample=world_sample,
        columns=["outcome"],
        brief=brief,
        config=episode_config,
        scoring=scoring,
        control_surface=episode_config.control_surface,
        case_id="plan_probe_v0_technical",
        family=family,
        probe_config=config,
        scenario=scenario,
        cost_condition=cost_condition,
        episode_seed=episode_seed,
    )
