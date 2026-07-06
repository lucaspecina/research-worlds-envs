"""Contracts for cases: battery, declared operators, stakes, scoring params.

battery.json holds one world-side seed per item (Decision Log v0.10): the
model-side seeds are derived as derive_seed(seed_world, rep), never persisted.
"""

import json
from pathlib import Path

from pydantic import BaseModel, ConfigDict, Field
from typing import Literal

from wager.contracts.episode import EpisodeConfig
from wager.contracts.world import ColumnSpec, Regime


class BatteryItem(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    weight: float = Field(gt=0)
    regime: Regime
    seed_world: int


# Context keys that only ever exist as runtime enrichment derived from the
# item's seed (window protocols' context_key). DECLARED tuple context (e.g. a
# trajectory battery's t_grid) is item identity and persists fine (v0.68-R2).
RUNTIME_DERIVED_CONTEXT_KEYS = frozenset({"cal_window"})


class Battery(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    items: list[BatteryItem] = Field(min_length=1)

    @classmethod
    def from_json_file(cls, path: str | Path) -> "Battery":
        return cls.model_validate(json.loads(Path(path).read_text(encoding="utf-8")))

    def to_json_file(self, path: str | Path) -> None:
        # Persistence PRINCIPLE (Decision Log v0.68-R2, amending v0.63-4):
        # what persists is what is DECLARED as part of the item (a trajectory
        # world's t_grid); what is blocked is what is DERIVED from the seed at
        # runtime (the calibration window, materialized at the WorldSide choke
        # point from the persisted scalar n_cal). Derived keys are the ones the
        # versioned window protocols name (context_key); blocking them here
        # keeps "never persisted" structural for every consumer.
        for i, item in enumerate(self.items):
            for key, value in item.regime.context.items():
                if isinstance(value, tuple) and key in RUNTIME_DERIVED_CONTEXT_KEYS:
                    raise ValueError(
                        f"battery item {i}: context[{key!r}] is runtime-DERIVED "
                        "enrichment (window protocol); batteries persist only "
                        "declared context (v0.68-R2 / v0.63-4)"
                    )
        Path(path).write_text(
            json.dumps(self.model_dump(), indent=2) + "\n", encoding="utf-8"
        )


class OperatorInstance(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    name: str
    # archival (#7, ADR 0077): record-keeping corruption (censoring at the old
    # bench's limit) -- distinct from sampling (who enters the record) and from
    # channel (the meter): experiments bypass it, the meter they never bypass.
    layer: Literal["mechanism", "channel", "sampling", "archival", "meta"]
    knobs: dict[str, float] = Field(default_factory=dict)
    # mechanism-layer operators declare param overrides that ABLATE them, so the
    # factory can render the world with this operator off (derived twins / ladder)
    ablation: dict[str, float] = Field(default_factory=dict)


class FunctionalSpec(BaseModel):
    """A decision functional scored ON TOP of energy distance (ARCHITECTURE §9.3,
    Decision Log v0.26/v0.27). Each instance MUST cite the verbatim brief clause
    that promises it (traceability rule: the brief promises -> the functional
    encodes; if the brief is silent the CASE is fixed, the functional is never
    invented to fabricate a gap). Computed from samples, server-side, zero-LLM."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    name: Literal["exceedance", "quantile", "subgroup_mean", "expected_loss"]
    column: str = "outcome"
    threshold: float | None = None  # exceedance / expected_loss failure threshold
    direction: Literal["below", "above"] = "below"
    tau: float | None = None  # quantile level in (0,1)
    subgroup: dict[str, float] | None = None  # subgroup_mean: regime/context filter
    brief_clause: str  # verbatim clause from the brief that promises this (traceability)


class StakesSpec(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    narrative: str
    decision_variables: list[str]
    # decision functionals (ARCHITECTURE §9.3): the score is energy + Σ c_F·|F(pred)
    # − F(real)|. Prefer ONE expected_loss when the decision is sharp (v0.27 Q6).
    # Empty -> combined score ≡ energy score (identity by construction; the dummy).
    functionals: list[FunctionalSpec] = Field(default_factory=list)
    # decision-relevant population mix declared from the brief: per context var,
    # {"center", "sd"} of the populations the decision cares about. The battery's
    # stakes_relevance MUST modulate context with this (not be flat); a flat
    # relevance lets off-support extremes dominate (Decision Log v0.22).
    context_relevance: dict[str, dict[str, float]] = Field(default_factory=dict)
    # decision-VARIABLE value relevance declared from the brief: which values of a
    # decision variable the decision cares about, beyond merely setting it. The
    # dummy brief explicitly wants "doses outside the historical record" and the
    # saturating region -> meta must encode that, or it tells a different story
    # than the brief (Decision Log v0.23). Per var: {"out_of_record_above",
    # "out_of_record_weight"} elevates the under-explored / costly region.
    decision_relevance: dict[str, dict[str, float]] = Field(default_factory=dict)


class ScoringParams(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    lambda_mdl: float = Field(ge=0)
    # lambda calibrated so the MDL term is ~5% of (S_truth - S_null) on this
    # case; provisional until calibrated over the E1 suite (Decision Log v0.11)
    lambda_provisional: bool = True
    # c_F: weight of the stakes-functional term (ARCHITECTURE §9.3). Frozen ONCE
    # per suite at the minimum-sufficient value under the visibility gate
    # max(3 x own std, 5% resolution floor) -- Decision Log v0.38; identical
    # across the suite's cases (suite lint enforces). 1.0 = historical default,
    # inert for cases with no declared functionals (identity by construction).
    c_f: float | dict[str, float] = 1.0
    n_samples: int = 1000
    m_reps: int = 2  # v0 default (Decision Log v0.12 item 2): CV(R)~1.2% on the
    # dummy, world-side noise dominates so m>2 buys little; raise per case if the
    # L2 protocol shows model-side noise matters
    model_call_timeout_s: float = 10.0


class CaseMeta(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    case_id: str
    suite: str
    columns: list[ColumnSpec] = Field(min_length=1)
    operators: list[OperatorInstance]
    stakes: StakesSpec
    scoring: ScoringParams
    episode: EpisodeConfig | None = None
    prior_reliability: float | None = None
    # window worlds (ARCHITECTURE §10.1 / Decision Log v0.63): versioned
    # protocol for the per-item calibration window -- context/n_cal keys,
    # posterior grid and prior DECLARED here (no hidden constants). None for
    # every non-window world (the whole machinery is inert then).
    window_protocol: dict | None = None
    # trajectory worlds (v0.68-R1): versioned protocol for the long->wide pivot
    # -- the deliverable is LONG format (unit_id, t, y), n counts UNITS, the
    # item's grid travels as DECLARED context under grid_key. None for every
    # static world (pivot machinery inert).
    trajectory_protocol: dict | None = None

    @classmethod
    def from_json_file(cls, path: str | Path) -> "CaseMeta":
        return cls.model_validate(json.loads(Path(path).read_text(encoding="utf-8")))

    @property
    def column_names(self) -> list[str]:
        return [c.name for c in self.columns]
