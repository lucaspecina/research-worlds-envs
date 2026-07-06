"""Contracts for the interactive episode: verbs, costs, submit result.

ExperimentDesign is agent-supplied, so it is the data-only boundary (Decision
Log v0.14, precision 3): typed scalar dicts with extra="forbid" reject callables
and stray objects at validation time.
"""

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

from wager.contracts.world import Regime


class ExperimentDesign(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    config: dict[str, float] = Field(default_factory=dict)  # do(): fixed knobs
    # trajectory worlds (v0.68-R3): the measurement SCHEDULE travels here as a
    # declared tuple (t_grid) -- same typed union as Regime.context; n then
    # counts UNITS (trajectories), readings = n x len(t_grid).
    context: dict[str, float | tuple[float, ...]] = Field(default_factory=dict)
    n: int = Field(gt=0, le=5000)  # bounded: runaway guard on a single draw
    horizon: int | None = None

    def to_regime(self) -> Regime:
        return Regime(config=dict(self.config), context=dict(self.context), horizon=self.horizon)


class SelectionFilter(BaseModel):
    """Collider selection into a source's records (sampling layer, ARCHITECTURE
    §1/§3; first implemented for world 3, Decision Log v0.49-2). Rows enter the
    record iff score(row) = sum(weights[c] * row[c]) is on the `keep` side of
    the threshold. The corruption lives in the SOURCE; world.sample() stays
    clean for the scorer."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    weights: dict[str, float]
    threshold: float
    keep: Literal["above", "below"] = "above"


class MeasurementChannel(BaseModel):
    """Zero-mean measurement noise on ONE observed column (channel layer;
    bias = 0 by decision v0.50-1 -- an all-views bias is undiscoverable).
    replicates=2 emits `<column>__rep1/__rep2` (two readings per unit, the
    v0.51 identifiability source: sigma_med via Var(rep1-rep2)/2)."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    column: str
    noise_sd: float = Field(ge=0)
    replicates: int = Field(default=1, ge=1, le=2)


class CensoringRule(BaseModel):
    """ARCHIVAL censoring of a source's recorded values (sampling layer, #7 --
    ADR 0077): the historical record format clips one column at a limit (the
    old bench's range), producing the classic pile-up at the limit. It is a
    property of how records were KEPT, not of the meter: experiments (fresh
    logging) bypass it exactly like they bypass selection, and the v0.9 rule
    keeps protecting only the CHANNEL. Applied AFTER the channel (the recorded
    value is what gets clipped; with replicates, every rep)."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    column: str
    limit: float
    side: Literal["above", "below"] = "above"  # above: values > limit recorded AS limit


class BatchEffect(BaseModel):
    """Per-BATCH meter offsets on one measured column (channel layer, #9 --
    ADR 0078): readings are taken in runs/batches sharing a calibration state.
    The view exposes the batch id as an EXTRA column (id_column, like __rep
    columns -- view schema != deliverable schema, v0.53). Two declared parts:

    - offset_sd: idiosyncratic per-batch offset (property of the METER'S runs
      -- applies to experiments too, v0.9: same instrument, fresh batches).
    - drift_per_batch + assign="driver_ramp": the HISTORICAL confound -- the
      record's batches follow the era's driver ramp (rows sorted by the
      decision variable + sort_noise before chunking) while calibration
      drifted -> the pooled slope absorbs the drift. History-only:
      experiments chunk by arrival and carry no drift (bypassed like
      selection; the offsets they keep are the meter's).
    """

    model_config = ConfigDict(frozen=True, extra="forbid")

    column: str
    id_column: str = "batch_id"
    batch_size: int = Field(default=25, ge=2)
    offset_sd: float = Field(ge=0)
    drift_per_batch: float = 0.0
    assign: Literal["arrival", "driver_ramp"] = "arrival"
    sort_key: str | None = None      # decision column for driver_ramp
    sort_noise: float = Field(default=0.0, ge=0)


class SourceConfig(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    cost_per_row: float = Field(ge=0)
    config: dict[str, float] = Field(default_factory=dict)
    # a source may DECLARE its historical sampling grid (t_grid) here (v0.68-R3)
    context: dict[str, float | tuple[float, ...]] = Field(default_factory=dict)
    # declared corruption pipeline (applied by the harness/factory VIEW, never
    # by the scorer): selection filter (sampling) + measurement channel.
    # pipeline_order (Decision Log v0.53-1): select_then_measure = survivorship
    # (the filter sees TRUE values; v0 default, chosen consciously);
    # measure_then_select = admission-by-recorded-symptom (the filter sees
    # MEASURED values; with replicates, the FIRST reading) -- changes the
    # de-biasing structure, future worlds declare it.
    selection: SelectionFilter | None = None
    channel: MeasurementChannel | None = None
    # archival censoring (#7, ADR 0077): records-only, experiments bypass it
    censoring: CensoringRule | None = None
    # per-batch meter offsets (#9, ADR 0078): offsets apply to experiments too
    # (the meter's runs); the drift+ramp confound is history-only
    batch: BatchEffect | None = None
    pipeline_order: Literal["select_then_measure", "measure_then_select"] = "select_then_measure"


class ExperimentCost(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    cost_fixed: float = Field(ge=0)
    cost_per_row: float = Field(ge=0)  # per READING (unit x timestamp) in trajectory worlds
    # trajectory worlds (v0.68-R3): price of leaving the run going -- charged on
    # max(t_grid). THE knob that makes knowing K expensive and knowing r cheap;
    # declared difficulty dial of the world. 0.0 = inert (every static world).
    cost_per_horizon: float = Field(default=0.0, ge=0)


class EpisodeConfig(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    budget: float = Field(gt=0)
    observe_sources: dict[str, SourceConfig]
    experiment: ExperimentCost
    # the DECLARED instrument experiments read (v0.58-2: positional conventions
    # are dummy-ism seeds -- two sources with different channels would bite
    # silently). Names the source whose channel is the case's meter; None only
    # when no source declares a channel.
    experiment_meter: str | None = None
    smoke_regimes: list[Regime] = Field(min_length=1)
    control_surface: dict = Field(default_factory=dict)  # what describe() shows


class SubmitResult(BaseModel):
    """What the AGENT sees on submit. R (the battery score) is server-side and
    NOT included here -- the battery is secret."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    accepted: bool
    error: str | None = None  # actionable smoke error when not accepted
