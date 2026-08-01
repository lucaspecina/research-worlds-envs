"""Design-time generator and certificates for the plan-policy probe v0.

The module implements only step 1 of the frozen exploratory design:

* one five-line prefix shared byte-for-byte by three hidden continuations;
* a closed, declared finite prior with an exact posterior;
* fixed operational actions, risk penalty, and low/high reopen costs;
* server-side oracles and fail-closed certification of the four target cases.

It intentionally does *not* add episode verbs, prompts, silent registration,
or agent calls.  Those are only worth building if this factory gate passes.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from functools import lru_cache
import hashlib
import json
from pathlib import Path
from typing import Literal

import numpy as np
import pandas as pd
from scipy.stats import norm

from wager.reward.decision_oracle import (
    DecisionInstrument,
    ExactDecision,
    NormalMixture,
    distribution_utility,
    exact_optimal_action,
    normal_mixture_energy_distance,
    normalize_weights,
    reopen_is_optimal,
)


Scenario = Literal["maintain", "revise", "doubt"]
SCENARIOS: tuple[Scenario, ...] = ("maintain", "revise", "doubt")
SCHEMA_VERSION = "wager.plan_probe_v0.factory.3"
FROZEN_DESIGN_COMMIT = "585033e"
INSTRUMENT_REVISION = "stratified-diagnostic-panel-r8-metricfix-v2"


def derive_factory_seed(base_seed: int, tag: str) -> int:
    """Namespaced uint32 seed; factory streams never reuse episode seeds."""

    payload = f"wager:plan-probe-v0:{int(base_seed)}:{tag}".encode("utf-8")
    return int.from_bytes(hashlib.sha256(payload).digest()[:4], "big")


# Fixed before inspecting the validation cohort.  The source string is the
# commit that froze the probe-v0 design; calibration used only 731000-731499.
VALIDATION_SEED_START = derive_factory_seed(
    int(FROZEN_DESIGN_COMMIT, 16),
    f"fixed-validation-cohort:{INSTRUMENT_REVISION}",
)


@dataclass(frozen=True)
class ProbeConfig:
    """The fixed public recipe and fixed measurement instrument."""

    decision: DecisionInstrument = field(
        default_factory=lambda: DecisionInstrument(
            actions=(3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0),
            safety_threshold=17.30,
            risk_penalty=8.0,
            reopen_cost_low=0.20,
            reopen_cost_high=12.00,
            quantile_tau=0.10,
        )
    )
    lines: tuple[int, ...] = (1, 2, 3, 4, 5)
    initial_region_max: float = 6.0
    activation_end: float = 10.0
    diagnostic_points: tuple[float, ...] = (6.5, 7.25, 8.0, 8.75, 9.5)
    control_points: tuple[float, ...] = (1.5, 3.5, 5.5)
    target_prefix_points: tuple[float, ...] = (0.5, 1.75, 3.0, 4.5, 5.75)
    other_prefix_points: tuple[float, ...] = (0.5, 2.0, 3.5, 5.0, 6.5, 8.0, 9.5)
    prefix_reps_target: int = 6
    prefix_reps_other: int = 3
    evidence_reps: int = 8
    base_gain_grid: tuple[float, ...] = (8.5, 9.25, 10.0, 10.75, 11.5)
    base_scale_grid: tuple[float, ...] = (2.6, 3.0, 3.4, 3.8, 4.2)
    amplitude_grid: tuple[float, ...] = (2.0, 2.25, 2.5)
    scenario_prior: tuple[float, ...] = (0.84, 0.08, 0.08)
    noise_base: float = 0.65
    noise_high_slope: float = 0.22
    posterior_mass_min: float = 0.72
    assimilation_change_min: float = 0.01
    assimilation_maintain_max: float = 0.08
    doubt_width_ratio_min: float = 1.12
    cost_margin_low_mult: float = 1.30
    cost_margin_high_mult: float = 0.70
    propagation_epsilon_fraction: float = 0.05

    def __post_init__(self) -> None:
        if len(self.scenario_prior) != len(SCENARIOS):
            raise ValueError("scenario_prior must have one mass per scenario")
        if not np.isclose(sum(self.scenario_prior), 1.0):
            raise ValueError("scenario_prior must sum to one")
        if any(v <= 0.0 for v in self.scenario_prior):
            raise ValueError("scenario priors must be positive")
        if max(self.target_prefix_points) > self.initial_region_max:
            raise ValueError("target prefix leaks into the diagnostic region")
        if min(self.diagnostic_points) <= self.initial_region_max:
            raise ValueError("diagnostic points must lie beyond the initial region")
        if self.prefix_reps_target <= 0 or self.prefix_reps_other <= 0:
            raise ValueError("prefix repetitions must be positive")
        if self.evidence_reps <= 0:
            raise ValueError("evidence_reps must be positive")

    def public_recipe(self) -> dict:
        """Everything needed to define the legal posterior; no realized truth."""

        triplets, triplet_weights = _triplet_prior(self)
        return {
            "schema_version": SCHEMA_VERSION,
            "instrument_revision": INSTRUMENT_REVISION,
            "lines": list(self.lines),
            "initial_region_max": self.initial_region_max,
            "activation_end": self.activation_end,
            "diagnostic_points": list(self.diagnostic_points),
            "control_points": list(self.control_points),
            "target_prefix_points": list(self.target_prefix_points),
            "other_prefix_points": list(self.other_prefix_points),
            "prefix_reps_target": self.prefix_reps_target,
            "prefix_reps_other": self.prefix_reps_other,
            "evidence_reps": self.evidence_reps,
            "diagnostic_panel": {
                "strata": [-1, 1],
                "repetitions_per_stratum_and_point": self.evidence_reps,
                "stratum_observed_only_in_diagnostic_panel": True,
                "deployment_stratum_unobserved_and_balanced": True,
            },
            "base_gain_grid": list(self.base_gain_grid),
            "base_scale_grid": list(self.base_scale_grid),
            "amplitude_grid": list(self.amplitude_grid),
            "admissible_triplet_rule": "truth_geometry_v0",
            "admissible_triplets": [list(values) for values in triplets],
            "admissible_triplet_weights": list(triplet_weights),
            "scenario_prior": dict(zip(SCENARIOS, self.scenario_prior)),
            "noise_base": self.noise_base,
            "noise_high_slope": self.noise_high_slope,
            "decision": asdict(self.decision),
            "propagation_epsilon_fraction": self.propagation_epsilon_fraction,
            "generative_contract": {
                "independence": (
                    "Conditional on one latent state, observation rows are "
                    "independent except for the declared balanced panel design."
                ),
                "base_mean": "10 + gain * (1 - exp(-driver / scale))",
                "base_sd": (
                    "noise_base + noise_high_slope * max(driver - 5, 0)"
                ),
                "activation": {
                    "below_initial_region": "phi(driver) = 0",
                    "transition": (
                        "t=(driver-initial_region_max)/(activation_end-"
                        "initial_region_max); phi=t^2*(3-2*t) for 0<t<1"
                    ),
                    "above_activation_end": "phi(driver) = 1",
                },
                "deployment_laws_for_target_line": {
                    "maintain": "Normal(base_mean, base_sd)",
                    "revise": (
                        "Normal(base_mean - amplitude*phi, base_sd)"
                    ),
                    "doubt": (
                        "0.5*Normal(base_mean-amplitude*phi, base_sd) + "
                        "0.5*Normal(base_mean+amplitude*phi, base_sd)"
                    ),
                },
                "non_target_lines": (
                    "Normal(base_mean, base_sd) in every scenario"
                ),
                "diagnostic_panel_laws_for_target_line": {
                    "maintain": (
                        "both strata: Normal(base_mean, base_sd)"
                    ),
                    "revise": (
                        "both strata: Normal(base_mean-amplitude*phi, base_sd)"
                    ),
                    "doubt": (
                        "stratum s in {-1,+1}: Normal(base_mean + "
                        "s*amplitude*phi, base_sd)"
                    ),
                },
                "utility": (
                    "mean(outcome) - risk_penalty * max(0, safety_threshold "
                    "- q_quantile_tau(outcome))"
                ),
                "reopen_rule": (
                    "reopen iff best post-evidence utility minus committed-action "
                    "utility exceeds the revealed reopen cost"
                ),
            },
        }


@dataclass(frozen=True)
class ObservationBatch:
    line: np.ndarray
    driver: np.ndarray
    outcome: np.ndarray
    diagnostic_stratum: np.ndarray | None = None

    def __post_init__(self) -> None:
        line = np.asarray(self.line, dtype=np.int64)
        driver = np.asarray(self.driver, dtype=np.float64)
        outcome = np.asarray(self.outcome, dtype=np.float64)
        diagnostic_stratum = (
            np.zeros(line.size, dtype=np.int8)
            if self.diagnostic_stratum is None
            else np.asarray(self.diagnostic_stratum, dtype=np.int8)
        )
        if line.ndim != 1 or driver.ndim != 1 or outcome.ndim != 1:
            raise ValueError("observation arrays must be one-dimensional")
        if not (
            line.size == driver.size == outcome.size == diagnostic_stratum.size
        ):
            raise ValueError("observation arrays must have equal length")
        if not line.size or not np.isfinite(driver).all() or not np.isfinite(outcome).all():
            raise ValueError("observation batch must be non-empty and finite")
        object.__setattr__(self, "line", line)
        object.__setattr__(self, "driver", driver)
        object.__setattr__(self, "outcome", outcome)
        object.__setattr__(self, "diagnostic_stratum", diagnostic_stratum)

    def to_frame(self) -> pd.DataFrame:
        return pd.DataFrame(
            {
                "line": self.line,
                "driver": self.driver,
                "diagnostic_stratum": self.diagnostic_stratum,
                "outcome": self.outcome,
            }
        )

    def digest(self) -> str:
        payload = np.column_stack(
            [
                self.line.astype(np.float64),
                self.driver,
                self.diagnostic_stratum.astype(np.float64),
                self.outcome,
            ]
        ).astype("<f8", copy=False)
        return hashlib.sha256(payload.tobytes(order="C")).hexdigest()


@dataclass(frozen=True)
class ProbeFamily:
    candidate_seed: int
    target_line: int
    true_gain: float
    true_scale: float
    true_amplitude: float
    prefix: ObservationBatch
    evidence: dict[Scenario, ObservationBatch]
    seed_manifest: dict[str, int]

    def __post_init__(self) -> None:
        if set(self.evidence) != set(SCENARIOS):
            raise ValueError("a family must contain all three twin continuations")

    @property
    def prefix_sha256(self) -> str:
        return self.prefix.digest()

    def hidden_manifest(self) -> dict:
        return {
            "candidate_seed": self.candidate_seed,
            "target_line": self.target_line,
            "true_gain": self.true_gain,
            "true_scale": self.true_scale,
            "true_amplitude": self.true_amplitude,
            "prefix_sha256": self.prefix_sha256,
            "evidence_sha256": {
                scenario: batch.digest() for scenario, batch in self.evidence.items()
            },
            "seed_manifest": dict(self.seed_manifest),
        }


@dataclass(frozen=True)
class _State:
    gain: float
    scale: float
    scenario: Scenario
    amplitude: float


@dataclass(frozen=True)
class ExactPosterior:
    """Finite exact posterior over the fully declared world recipe."""

    config: ProbeConfig
    target_line: int
    states: tuple[_State, ...]
    weights: np.ndarray

    def __post_init__(self) -> None:
        weights = np.asarray(self.weights, dtype=float)
        if weights.shape != (len(self.states),):
            raise ValueError("posterior weights do not match state grid")
        if np.any(weights < 0.0) or not np.isclose(weights.sum(), 1.0):
            raise ValueError("posterior weights must be normalized")
        object.__setattr__(self, "weights", weights)

    def scenario_probability(self, scenario: Scenario) -> float:
        return float(sum(w for state, w in zip(self.states, self.weights)
                         if state.scenario == scenario))

    def predictive(self, line: int, driver: float) -> NormalMixture:
        weights: list[float] = []
        means: list[float] = []
        stds: list[float] = []
        phi = float(_activation(driver, self.config)) if line == self.target_line else 0.0
        sigma = float(_base_std(driver, self.config))
        for state, weight in zip(self.states, self.weights):
            mu = float(_base_mean(driver, state.gain, state.scale))
            if state.scenario == "revise" and phi:
                weights.append(float(weight))
                means.append(mu - state.amplitude * phi)
                stds.append(sigma)
            elif state.scenario == "doubt" and phi:
                weights.extend((float(weight) * 0.5, float(weight) * 0.5))
                means.extend((mu - state.amplitude * phi, mu + state.amplitude * phi))
                stds.extend((sigma, sigma))
            else:
                weights.append(float(weight))
                means.append(mu)
                stds.append(sigma)
        return NormalMixture(np.asarray(weights), np.asarray(means), np.asarray(stds))

    def decision(self) -> ExactDecision:
        return exact_optimal_action(
            lambda action: self.predictive(self.target_line, action),
            self.config.decision,
        )


def _activation(driver: float | np.ndarray, config: ProbeConfig) -> np.ndarray:
    """C1 smoothstep that is *exactly* zero throughout the initial region."""

    x = np.asarray(driver, dtype=float)
    t = np.clip(
        (x - config.initial_region_max)
        / (config.activation_end - config.initial_region_max),
        0.0,
        1.0,
    )
    return t * t * (3.0 - 2.0 * t)


def _base_mean(driver: float | np.ndarray, gain: float, scale: float) -> np.ndarray:
    x = np.asarray(driver, dtype=float)
    return 10.0 + gain * (1.0 - np.exp(-x / scale))


def _base_std(driver: float | np.ndarray, config: ProbeConfig) -> np.ndarray:
    x = np.asarray(driver, dtype=float)
    return config.noise_base + config.noise_high_slope * np.maximum(x - 5.0, 0.0)


def truth_predictive(
    family: ProbeFamily,
    scenario: Scenario,
    line: int,
    driver: float,
    config: ProbeConfig,
) -> NormalMixture:
    return _truth_mixture_from_params(
        gain=family.true_gain,
        scale=family.true_scale,
        amplitude=family.true_amplitude,
        scenario=scenario,
        driver=driver,
        active=int(line) == family.target_line,
        config=config,
    )


def _truth_mixture_from_params(
    *,
    gain: float,
    scale: float,
    amplitude: float,
    scenario: Scenario,
    driver: float,
    active: bool,
    config: ProbeConfig,
) -> NormalMixture:
    mu = float(_base_mean(driver, gain, scale))
    sigma = float(_base_std(driver, config))
    phi = float(_activation(driver, config)) if active else 0.0
    if scenario == "revise" and phi:
        return NormalMixture(
            np.array([1.0]), np.array([mu - amplitude * phi]), np.array([sigma])
        )
    if scenario == "doubt" and phi:
        return NormalMixture(
            np.array([0.5, 0.5]),
            np.array([mu - amplitude * phi, mu + amplitude * phi]),
            np.array([sigma, sigma]),
        )
    return NormalMixture(np.array([1.0]), np.array([mu]), np.array([sigma]))


def sample_truth(
    family: ProbeFamily,
    scenario: Scenario,
    *,
    line: int,
    driver: float,
    n: int,
    seed: int,
    config: ProbeConfig,
) -> np.ndarray:
    """Hidden world sampler with exact common-prefix behavior."""

    return truth_predictive(family, scenario, line, driver, config).sample(n, seed)


def _raw_parameter_weights(config: ProbeConfig) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    gains = np.asarray(config.base_gain_grid)
    scales = np.asarray(config.base_scale_grid)
    amplitudes = np.asarray(config.amplitude_grid)
    gain_w = np.exp(-0.5 * ((gains - gains.mean()) / 1.05) ** 2)
    scale_w = np.exp(-0.5 * ((scales - scales.mean()) / 0.55) ** 2)
    amp_w = np.exp(-0.5 * ((amplitudes - amplitudes.mean()) / 0.48) ** 2)
    gain_w /= gain_w.sum()
    scale_w /= scale_w.sum()
    amp_w /= amp_w.sum()
    return gain_w, scale_w, amp_w


@lru_cache(maxsize=None)
def _admissible_triplets(config: ProbeConfig) -> tuple[tuple[float, float, float], ...]:
    """Public, evidence-independent support of the probe's world family.

    The rule uses true predictive distributions only, never realized evidence.
    It fixes the causal geometry the probe needs: stable operation has one
    optimum, both legitimate revisions have a more prudent optimum, and their
    gross gains lie clearly between the two *fixed* reopen costs.
    """

    admitted: list[tuple[float, float, float]] = []
    low = config.decision.reopen_cost_low
    high = config.decision.reopen_cost_high
    for gain in config.base_gain_grid:
        for scale in config.base_scale_grid:
            for amplitude in config.amplitude_grid:
                decisions: dict[Scenario, ExactDecision] = {}
                for scenario in SCENARIOS:
                    decisions[scenario] = exact_optimal_action(
                        lambda action, scenario=scenario: _truth_mixture_from_params(
                            gain=gain,
                            scale=scale,
                            amplitude=amplitude,
                            scenario=scenario,
                            driver=action,
                            active=True,
                            config=config,
                        ),
                        config.decision,
                    )
                committed = decisions["maintain"].action
                revise_gain = (
                    decisions["revise"].utility
                    - decisions["revise"].utilities[committed]
                )
                doubt_gain = (
                    decisions["doubt"].utility
                    - decisions["doubt"].utilities[committed]
                )
                safe = all(
                    _truth_mixture_from_params(
                        gain=gain,
                        scale=scale,
                        amplitude=amplitude,
                        scenario=scenario,
                        driver=decision.action,
                        active=True,
                        config=config,
                    ).quantile(config.decision.quantile_tau)
                    >= config.decision.safety_threshold
                    for scenario, decision in decisions.items()
                )
                if (
                    decisions["revise"].action < committed
                    and decisions["doubt"].action < committed
                    and revise_gain >= config.cost_margin_low_mult * low
                    and revise_gain <= config.cost_margin_high_mult * high
                    and doubt_gain >= config.cost_margin_low_mult * low
                    and doubt_gain <= config.cost_margin_high_mult * high
                    and safe
                ):
                    admitted.append((float(gain), float(scale), float(amplitude)))
    if not admitted:
        raise ValueError("fixed probe instrument admits no parameter triplets")
    return tuple(admitted)


@lru_cache(maxsize=None)
def _triplet_prior(config: ProbeConfig) -> tuple[tuple[tuple[float, float, float], ...], tuple[float, ...]]:
    triplets = _admissible_triplets(config)
    gain_w, scale_w, amp_w = _raw_parameter_weights(config)
    gi = {value: i for i, value in enumerate(config.base_gain_grid)}
    si = {value: i for i, value in enumerate(config.base_scale_grid)}
    ai = {value: i for i, value in enumerate(config.amplitude_grid)}
    weights = np.asarray([
        gain_w[gi[gain]] * scale_w[si[scale]] * amp_w[ai[amplitude]]
        for gain, scale, amplitude in triplets
    ])
    weights /= weights.sum()
    return triplets, tuple(float(value) for value in weights)


@lru_cache(maxsize=None)
def _prior_grid(config: ProbeConfig) -> tuple[tuple[_State, ...], np.ndarray]:
    triplets, triplet_w = _triplet_prior(config)
    scenario_w = dict(zip(SCENARIOS, config.scenario_prior))

    states: list[_State] = []
    log_prior: list[float] = []
    for (gain, scale, amplitude), family_weight in zip(triplets, triplet_w):
        for scenario in SCENARIOS:
            states.append(_State(gain, scale, scenario, amplitude))
            log_prior.append(float(np.log(family_weight) + np.log(scenario_w[scenario])))
    return tuple(states), np.asarray(log_prior)


def _log_likelihood(state: _State, data: ObservationBatch, target_line: int,
                    config: ProbeConfig) -> float:
    mu = _base_mean(data.driver, state.gain, state.scale)
    sigma = _base_std(data.driver, config)
    phi = np.where(data.line == target_line, _activation(data.driver, config), 0.0)
    if state.scenario == "maintain":
        return float(np.sum(norm.logpdf(data.outcome, loc=mu, scale=sigma)))
    if state.scenario == "revise":
        return float(np.sum(norm.logpdf(
            data.outcome, loc=mu - state.amplitude * phi, scale=sigma
        )))
    # The clean diagnostic panel observes a temporary balanced stratum.  In
    # ordinary deployment (stratum == 0), that stratum is unavailable and the
    # predictive is the 50/50 mixture scored by the world.
    observed = data.diagnostic_stratum != 0
    values = np.empty(data.outcome.size, dtype=float)
    if np.any(observed):
        loc = (
            mu[observed]
            + state.amplitude * phi[observed] * data.diagnostic_stratum[observed]
        )
        values[observed] = norm.logpdf(
            data.outcome[observed], loc=loc, scale=sigma[observed]
        )
    if np.any(~observed):
        left = norm.logpdf(
            data.outcome[~observed],
            loc=mu[~observed] - state.amplitude * phi[~observed],
            scale=sigma[~observed],
        )
        right = norm.logpdf(
            data.outcome[~observed],
            loc=mu[~observed] + state.amplitude * phi[~observed],
            scale=sigma[~observed],
        )
        values[~observed] = np.logaddexp(left, right) - np.log(2.0)
    return float(np.sum(values))


def exact_posterior(
    family: ProbeFamily,
    config: ProbeConfig,
    *,
    evidence: Scenario | None = None,
) -> ExactPosterior:
    states, log_prior = _prior_grid(config)
    log_weights = np.empty(len(states), dtype=float)
    batch = family.prefix
    extra = family.evidence[evidence] if evidence is not None else None
    for i, state in enumerate(states):
        value = log_prior[i] + _log_likelihood(state, batch, family.target_line, config)
        if extra is not None:
            value += _log_likelihood(state, extra, family.target_line, config)
        log_weights[i] = value
    return ExactPosterior(
        config=config,
        target_line=family.target_line,
        states=states,
        weights=normalize_weights(log_weights),
    )


def _restrict_posterior_scenario(
    posterior: ExactPosterior,
    scenario: Scenario,
) -> ExactPosterior:
    """Counterfactual robot that insists on one mechanism regardless of data."""

    weights = np.asarray([
        weight if state.scenario == scenario else 0.0
        for state, weight in zip(posterior.states, posterior.weights)
    ])
    total = float(weights.sum())
    if total <= 0.0:
        raise ValueError(f"posterior has no mass for scenario {scenario!r}")
    return ExactPosterior(
        config=posterior.config,
        target_line=posterior.target_line,
        states=posterior.states,
        weights=weights / total,
    )


def _draw_batch(
    *,
    family_stub: ProbeFamily,
    scenario: Scenario,
    lines: list[int],
    drivers: list[float],
    diagnostic_strata: list[int] | None = None,
    seed: int,
    config: ProbeConfig,
) -> ObservationBatch:
    if len(lines) != len(drivers):
        raise ValueError("lines and drivers must have equal length")
    if diagnostic_strata is None:
        diagnostic_strata = [0] * len(lines)
    if len(diagnostic_strata) != len(lines):
        raise ValueError("diagnostic strata must match the observation rows")
    outcomes = np.empty(len(lines), dtype=float)
    for i, (line, driver, stratum) in enumerate(
        zip(lines, drivers, diagnostic_strata)
    ):
        cell_seed = derive_factory_seed(seed, f"row:{i}:line:{line}:driver:{driver:.8f}")
        distribution = truth_predictive(
            family_stub, scenario, line, driver, config
        )
        if scenario == "doubt" and stratum:
            mu = float(_base_mean(
                driver, family_stub.true_gain, family_stub.true_scale
            ))
            sigma = float(_base_std(driver, config))
            phi = (
                float(_activation(driver, config))
                if line == family_stub.target_line
                else 0.0
            )
            distribution = NormalMixture(
                np.array([1.0]),
                np.array([mu + family_stub.true_amplitude * phi * stratum]),
                np.array([sigma]),
            )
        outcomes[i] = distribution.sample(1, cell_seed)[0]
    return ObservationBatch(
        np.asarray(lines),
        np.asarray(drivers),
        outcomes,
        np.asarray(diagnostic_strata),
    )


def generate_candidate(candidate_seed: int, config: ProbeConfig | None = None) -> ProbeFamily:
    """Generate one donor prefix and all three continuations deterministically."""

    config = config or ProbeConfig()
    rng = np.random.default_rng(derive_factory_seed(candidate_seed, "truth-parameters"))
    target_line = int(rng.choice(config.lines))
    # Draw truth base/amplitude from the same declared marginal grids.  State
    # duplication across scenarios would bias a direct state draw, so use the
    # explicit marginal weights below.
    triplets, triplet_weights = _triplet_prior(config)
    triplet_index = int(rng.choice(len(triplets), p=np.asarray(triplet_weights)))
    true_gain, true_scale, true_amplitude = triplets[triplet_index]

    empty = ObservationBatch(np.array([target_line]), np.array([0.0]), np.array([0.0]))
    seed_manifest = {
        "truth_parameters": derive_factory_seed(candidate_seed, "truth-parameters"),
        "prefix": derive_factory_seed(candidate_seed, "prefix"),
        **{
            f"evidence_{scenario}": derive_factory_seed(candidate_seed, f"evidence:{scenario}")
            for scenario in SCENARIOS
        },
        "oracle": derive_factory_seed(candidate_seed, "oracle"),
    }
    stub = ProbeFamily(
        candidate_seed=candidate_seed,
        target_line=target_line,
        true_gain=true_gain,
        true_scale=true_scale,
        true_amplitude=true_amplitude,
        prefix=empty,
        evidence={scenario: empty for scenario in SCENARIOS},
        seed_manifest=seed_manifest,
    )

    lines: list[int] = []
    drivers: list[float] = []
    for line in config.lines:
        points = (config.target_prefix_points if line == target_line
                  else config.other_prefix_points)
        reps = (config.prefix_reps_target if line == target_line
                else config.prefix_reps_other)
        for driver in points:
            lines.extend([line] * reps)
            drivers.extend([driver] * reps)
    prefix = _draw_batch(
        family_stub=stub,
        scenario="maintain",
        lines=lines,
        drivers=drivers,
        seed=seed_manifest["prefix"],
        config=config,
    )

    ev_lines: list[int] = []
    ev_drivers: list[float] = []
    ev_strata: list[int] = []
    for driver in config.diagnostic_points:
        for stratum in (-1, 1):
            ev_lines.extend([target_line] * config.evidence_reps)
            ev_drivers.extend([driver] * config.evidence_reps)
            ev_strata.extend([stratum] * config.evidence_reps)
    evidence = {
        scenario: _draw_batch(
            family_stub=stub,
            scenario=scenario,
            lines=ev_lines,
            drivers=ev_drivers,
            diagnostic_strata=ev_strata,
            seed=seed_manifest[f"evidence_{scenario}"],
            config=config,
        )
        for scenario in SCENARIOS
    }
    return ProbeFamily(
        candidate_seed=candidate_seed,
        target_line=target_line,
        true_gain=true_gain,
        true_scale=true_scale,
        true_amplitude=true_amplitude,
        prefix=prefix,
        evidence=evidence,
        seed_manifest=seed_manifest,
    )


def _predictive_distance(
    left: ExactPosterior,
    right: ExactPosterior,
    family: ProbeFamily,
    config: ProbeConfig,
) -> tuple[float, dict[str, float]]:
    diagnostics: list[float] = []
    controls: list[float] = []
    width_ratios: list[float] = []
    for group, points in (("diagnostic", config.diagnostic_points),
                          ("control", config.control_points)):
        for i, driver in enumerate(points):
            p = left.predictive(family.target_line, driver)
            q = right.predictive(family.target_line, driver)
            scale = max(float(np.sqrt(q.variance)), 1e-6)
            distance = normal_mixture_energy_distance(p, q, scale=scale)
            (diagnostics if group == "diagnostic" else controls).append(distance)
            if group == "diagnostic":
                pre_width = p.quantile(0.9) - p.quantile(0.1)
                post_width = q.quantile(0.9) - q.quantile(0.1)
                width_ratios.append(post_width / max(pre_width, 1e-9))
    weighted = 0.8 * float(np.mean(diagnostics)) + 0.2 * float(np.mean(controls))
    return weighted, {
        "diagnostic": float(np.mean(diagnostics)),
        "control": float(np.mean(controls)),
        "width_ratio": float(np.mean(width_ratios)),
    }


def _assimilation_distance(
    pre: ExactPosterior,
    post: ExactPosterior,
    family: ProbeFamily,
    config: ProbeConfig,
) -> tuple[float, dict[str, float]]:
    return _predictive_distance(pre, post, family, config)


def _gate(value, op: str, threshold) -> dict:
    operations = {
        "eq": lambda a, b: a == b,
        "ne": lambda a, b: a != b,
        "ge": lambda a, b: a >= b,
        "le": lambda a, b: a <= b,
        "gt": lambda a, b: a > b,
        "lt": lambda a, b: a < b,
    }
    if op not in operations:
        raise ValueError(f"unknown gate operation {op!r}")
    return {
        "passed": bool(operations[op](value, threshold)),
        "value": value,
        "op": op,
        "threshold": threshold,
    }


def certify_family(family: ProbeFamily, config: ProbeConfig | None = None) -> dict:
    """Certify the whole triplet together; never select a scenario alone."""

    config = config or ProbeConfig()
    pre = exact_posterior(family, config)
    pre_decision = pre.decision()
    utility_scale = float(
        max(pre_decision.utilities.values()) - min(pre_decision.utilities.values())
    )
    epsilon_prop = config.propagation_epsilon_fraction * utility_scale
    scenario_reports: dict[str, dict] = {}
    posteriors: dict[Scenario, ExactPosterior] = {}
    all_gates: dict[str, dict] = {}

    # Structural byte identity over every pre-checkpoint query allowed by v0.
    common = True
    for line in config.lines:
        points = (config.control_points if line == family.target_line
                  else config.other_prefix_points)
        for i, driver in enumerate(points):
            seed = derive_factory_seed(family.candidate_seed, f"common:{line}:{i}")
            draws = [sample_truth(
                family, scenario, line=line, driver=driver, n=32, seed=seed, config=config
            ) for scenario in SCENARIOS]
            common &= np.array_equal(draws[0], draws[1]) and np.array_equal(draws[0], draws[2])
    all_gates["common_prefix_all_legal_queries"] = _gate(common, "eq", True)

    low = config.decision.reopen_cost_low
    high = config.decision.reopen_cost_high
    for scenario in SCENARIOS:
        post = exact_posterior(family, config, evidence=scenario)
        posteriors[scenario] = post
        decision = post.decision()
        gross_gain = float(decision.utility - decision.utilities[pre_decision.action])
        assimilation, detail = _assimilation_distance(
            pre, post, family, config,
        )
        p_scenario = post.scenario_probability(scenario)
        truth_dist = truth_predictive(
            family, scenario, family.target_line, decision.action, config
        )
        truth_utility = distribution_utility(truth_dist, config.decision)
        q10_opt = post.predictive(family.target_line, decision.action).quantile(
            config.decision.quantile_tau
        )
        report = {
            "posterior_scenario_probability": p_scenario,
            "assimilation_distance": assimilation,
            "assimilation_detail": detail,
            "pre_action": pre_decision.action,
            "post_action": decision.action,
            "gross_gain": gross_gain,
            "propagation_epsilon": epsilon_prop,
            "propagation_denominator_resolved": gross_gain >= epsilon_prop,
            "reopen_low": reopen_is_optimal(gross_gain, low),
            "reopen_high": reopen_is_optimal(gross_gain, high),
            "posterior_q10_at_optimum": q10_opt,
            "truth_utility_at_reference_action": truth_utility,
            "action_utilities": {str(k): v for k, v in decision.utilities.items()},
        }
        gates: dict[str, dict] = {
            "optimum_safe": _gate(
                q10_opt, "ge", config.decision.safety_threshold
            ),
        }
        if scenario == "maintain":
            gates.update({
                "action_maintained": _gate(decision.action, "eq", pre_decision.action),
                "change_below_low_margin": _gate(
                    gross_gain, "le", config.cost_margin_high_mult * low
                ),
                "model_materially_stable": _gate(
                    assimilation, "le", config.assimilation_maintain_max
                ),
            })
        else:
            gates.update({
                "scenario_identified": _gate(
                    p_scenario, "ge", config.posterior_mass_min
                ),
                "action_changes": _gate(decision.action, "ne", pre_decision.action),
                "action_more_prudent": _gate(decision.action, "lt", pre_decision.action),
                "low_cost_reopen_margin": _gate(
                    gross_gain, "ge", config.cost_margin_low_mult * low
                ),
                "high_cost_keep_margin": _gate(
                    gross_gain, "le", config.cost_margin_high_mult * high
                ),
                "model_change_visible": _gate(
                    assimilation, "ge", config.assimilation_change_min
                ),
            })
            if scenario == "doubt":
                gates["uncertainty_increases"] = _gate(
                    detail["width_ratio"], "ge", config.doubt_width_ratio_min
                )
        report["gates"] = gates
        report["all"] = all(g["passed"] for g in gates.values())
        scenario_reports[scenario] = report
        for name, gate in gates.items():
            all_gates[f"{scenario}.{name}"] = gate

    # Fixed policies must lose somewhere in the balanced 3 x 2 design.
    policy_matrix = {
        scenario: {
            "low": scenario_reports[scenario]["reopen_low"],
            "high": scenario_reports[scenario]["reopen_high"],
        }
        for scenario in SCENARIOS
    }
    always_reopen_wrong = sum(
        not correct for row in policy_matrix.values() for correct in row.values()
    )
    never_reopen_wrong = sum(
        correct for row in policy_matrix.values() for correct in row.values()
    )
    all_gates["always_reopen_loses"] = _gate(always_reopen_wrong, "ge", 1)
    all_gates["never_reopen_loses"] = _gate(never_reopen_wrong, "ge", 1)

    # Model-side reflexes: force the same explanation after every batch and
    # compare it against the unrestricted legal posterior.  These are actual
    # predictive distances, not labels inferred from the prompt.
    robot_models: dict[str, dict] = {}
    for robot_name, forced_scenario, incompatible in (
        ("always_revise", "revise", ("maintain", "doubt")),
        ("always_widen", "doubt", ("maintain", "revise")),
    ):
        distances: dict[str, float] = {}
        for actual in SCENARIOS:
            forced = _restrict_posterior_scenario(posteriors[actual], forced_scenario)
            distance, _ = _predictive_distance(
                forced, posteriors[actual], family, config
            )
            distances[actual] = distance
        worst_incompatible = max(distances[name] for name in incompatible)
        robot_models[robot_name] = {
            "forced_scenario": forced_scenario,
            "distance_from_legal_posterior": distances,
            "worst_incompatible_distance": worst_incompatible,
        }
        all_gates[f"{robot_name}_loses"] = _gate(
            worst_incompatible, "ge", config.assimilation_change_min
        )

    all_gates["never_update_model_loses"] = _gate(
        min(
            scenario_reports["revise"]["assimilation_distance"],
            scenario_reports["doubt"]["assimilation_distance"],
        ),
        "ge",
        config.assimilation_change_min,
    )

    # Action-side reflex: always pay to move just one grid point downward.
    # Its regret is evaluated against the exact best maintain/reopen policy.
    pre_index = config.decision.actions.index(pre_decision.action)
    little_action = config.decision.actions[max(pre_index - 1, 0)]
    little_reports: dict[str, dict] = {}
    reopened_regrets: list[float] = []
    for scenario in SCENARIOS:
        decision = posteriors[scenario].decision()
        committed_utility = decision.utilities[pre_decision.action]
        gross_gain = decision.utility - committed_utility
        rows: dict[str, dict] = {}
        for cost_name, cost in (
            ("low", config.decision.reopen_cost_low),
            ("high", config.decision.reopen_cost_high),
        ):
            normative_value = max(committed_utility, decision.utility - cost)
            robot_value = decision.utilities[little_action] - cost
            regret = float(normative_value - robot_value)
            normative_reopen = reopen_is_optimal(gross_gain, cost)
            if normative_reopen:
                reopened_regrets.append(regret)
            denominator = gross_gain
            fraction = (
                None
                if denominator < epsilon_prop
                else float(
                    (decision.utilities[little_action] - committed_utility)
                    / denominator
                )
            )
            rows[cost_name] = {
                "normative_reopen": normative_reopen,
                "regret": regret,
                "propagation_fraction": fraction,
            }
        little_reports[scenario] = rows
    all_gates["change_a_bit_loses"] = _gate(
        max(reopened_regrets, default=0.0),
        "ge",
        epsilon_prop,
    )

    return {
        "schema_version": SCHEMA_VERSION,
        "family": family.hidden_manifest(),
        "instrument": config.public_recipe(),
        "pre": {
            "action": pre_decision.action,
            "utility_scale": utility_scale,
            "propagation_epsilon": epsilon_prop,
            "action_utilities": {str(k): v for k, v in pre_decision.utilities.items()},
            "scenario_probabilities": {
                scenario: pre.scenario_probability(scenario) for scenario in SCENARIOS
            },
        },
        "scenarios": scenario_reports,
        "policy_matrix": policy_matrix,
        "robot_models": robot_models,
        "change_a_bit_robot": {
            "action": little_action,
            "branches": little_reports,
        },
        "deferred_to_harness": {
            "vague_or_invalid_registration": (
                "Requires the silent full-model REGISTER interface; invalid "
                "submissions will remain failures in the denominator."
            ),
            "text_only_strategy": (
                "Requires the episode prompt and executable-model validator."
            ),
        },
        "gates": all_gates,
        "all": all(gate["passed"] for gate in all_gates.values()),
    }


def evaluate_fixed_cohort(
    *,
    count: int,
    candidate_seed_start: int = VALIDATION_SEED_START,
    config: ProbeConfig | None = None,
) -> list[tuple[ProbeFamily, dict]]:
    """Evaluate consecutive precommitted seeds without skipping failures."""

    if count <= 0:
        raise ValueError("count must be positive")
    config = config or ProbeConfig()
    cohort: list[tuple[ProbeFamily, dict]] = []
    for offset in range(count):
        candidate_seed = candidate_seed_start + offset
        family = generate_candidate(candidate_seed, config)
        certificate = certify_family(family, config)
        cohort.append((family, certificate))
    return cohort


def _balanced_episode_manifest(
    cohort: list[tuple[ProbeFamily, dict]],
) -> tuple[list[dict], dict]:
    """Materialize the exact scenario x cost crossing and audit independence."""

    cells: list[dict] = []
    for family_index, (family, _) in enumerate(cohort):
        for scenario in SCENARIOS:
            for cost in ("low", "high"):
                cells.append({
                    "family_index": family_index,
                    "candidate_seed": family.candidate_seed,
                    "scenario": scenario,
                    "cost": cost,
                })

    counts = {
        cost: {scenario: 0 for scenario in SCENARIOS}
        for cost in ("low", "high")
    }
    for cell in cells:
        counts[cell["cost"]][cell["scenario"]] += 1
    total = len(cells)
    accuracy = 0.0
    mutual_information = 0.0
    for cost, row in counts.items():
        cost_total = sum(row.values())
        accuracy += (cost_total / total) * max(row.values()) / cost_total
        for scenario, count in row.items():
            if count:
                joint = count / total
                p_cost = cost_total / total
                p_scenario = sum(
                    counts[c][scenario] for c in counts
                ) / total
                mutual_information += joint * np.log(joint / (p_cost * p_scenario))
    audit = {
        "counts": counts,
        "best_cost_only_scenario_accuracy": float(accuracy),
        "scenario_cost_mutual_information_nats": float(mutual_information),
    }
    return cells, audit


def _public_family_id(prefix_sha256: str, recipe_sha256: str) -> str:
    payload = f"{SCHEMA_VERSION}:{recipe_sha256}:{prefix_sha256}".encode("utf-8")
    return "family_" + hashlib.sha256(payload).hexdigest()[:16]


def build_agent_recipe(
    config: ProbeConfig | None = None,
    *,
    target_line: int | None = None,
) -> dict:
    """Return only normative information safe for one agent episode.

    Cohort layout, seed rules, prefix hashes, certification outcomes and the
    researcher-side balancing scheme are intentionally absent.  A harness may
    add the current public target line, but never a ``ProbeFamily`` or report.
    """

    config = config or ProbeConfig()
    if target_line is not None and target_line not in config.lines:
        raise ValueError(f"target_line must be one of {list(config.lines)}")
    recipe = {
        "schema_version": SCHEMA_VERSION,
        "kind": "agent_normative_recipe",
        "instrument": config.public_recipe(),
    }
    if target_line is not None:
        recipe["current_episode"] = {"target_line": int(target_line)}
    return recipe


def write_factory_report(
    output_dir: str | Path,
    *,
    count: int = 8,
    candidate_seed_start: int = VALIDATION_SEED_START,
    config: ProbeConfig | None = None,
) -> dict:
    """Write isolated private certification and agent-safe public manifest."""

    config = config or ProbeConfig()
    cohort = evaluate_fixed_cohort(
        count=count,
        candidate_seed_start=candidate_seed_start,
        config=config,
    )
    recipe = config.public_recipe()
    recipe_sha256 = hashlib.sha256(
        json.dumps(recipe, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()
    target_lines = [family.target_line for family, _ in cohort]
    episode_cells, independence = _balanced_episode_manifest(cohort)
    cell_counts = [
        independence["counts"][cost][scenario]
        for cost in ("low", "high")
        for scenario in SCENARIOS
    ]
    batch_gates = {
        "fixed_family_count": _gate(len(cohort), "eq", count),
        "every_fixed_family_certifies": _gate(
            sum(certificate["all"] for _, certificate in cohort), "eq", count
        ),
        "target_line_diversity": _gate(
            len(set(target_lines)), "ge", min(3, count)
        ),
        "single_fixed_instrument": _gate(
            len({recipe_sha256 for _ in cohort}), "eq", 1
        ),
        "balanced_scenario_x_cost_cells": _gate(
            len(set(cell_counts)), "eq", 1
        ),
        "cost_only_accuracy_is_chance": _gate(
            independence["best_cost_only_scenario_accuracy"], "eq", 1.0 / 3.0
        ),
        "scenario_cost_mutual_information_zero": _gate(
            abs(independence["scenario_cost_mutual_information_nats"]),
            "le",
            1e-12,
        ),
    }
    report = {
        "schema_version": SCHEMA_VERSION,
        "kind": "private_factory_certification_only_no_agents",
        "frozen_design_commit": FROZEN_DESIGN_COMMIT,
        "instrument_revision": INSTRUMENT_REVISION,
        "instrument": recipe,
        "instrument_sha256": recipe_sha256,
        "seed_separation": {
            "factory_calibration_burned": [731_000, 731_499],
            "factory_validation_fixed_range": [
                candidate_seed_start, candidate_seed_start + count - 1
            ],
            "future_episode_seeds_reserved": [90_000, 90_999],
            "future_episode_seeds_used_here": False,
        },
        "fixed_cohort": {
            "candidate_seed_start": candidate_seed_start,
            "count": count,
            "consecutive_no_skips": True,
            "selection_on_realized_evidence": False,
        },
        "families": [certificate for _, certificate in cohort],
        "episode_cells_private": episode_cells,
        "scenario_cost_independence": independence,
        "batch_gates": batch_gates,
        "all": (
            all(gate["passed"] for gate in batch_gates.values())
            and all(c["all"] for _, c in cohort)
        ),
    }
    researcher_manifest = {
        "schema_version": SCHEMA_VERSION,
        "kind": "researcher_public_factory_manifest_not_agent_facing",
        "frozen_design_commit": FROZEN_DESIGN_COMMIT,
        "instrument_revision": INSTRUMENT_REVISION,
        "instrument": recipe,
        "instrument_sha256": recipe_sha256,
        "cohort": {
            "count": count,
            "families": [
                {
                    "family_id": _public_family_id(
                        family.prefix_sha256, recipe_sha256
                    ),
                    "target_line": family.target_line,
                    "prefix_sha256": family.prefix_sha256,
                }
                for family, _ in cohort
            ],
        },
        "design": {
            "scenarios_crossed_with_both_costs": True,
            "scenario_assignment_hidden_from_agent": True,
            "private_truth_and_correct_actions_excluded": True,
        },
        "factory_gate_passed": report["all"],
    }
    output = Path(output_dir)
    private_dir = output / "private"
    public_dir = output / "public"
    private_dir.mkdir(parents=True, exist_ok=True)
    public_dir.mkdir(parents=True, exist_ok=True)
    (private_dir / "factory_certification.json").write_text(
        json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    (public_dir / "researcher_manifest.json").write_text(
        json.dumps(researcher_manifest, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    (public_dir / "agent_recipe.json").write_text(
        json.dumps(build_agent_recipe(config), indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return {
        "all": report["all"],
        "fixed_cohort_count": count,
        "failed_families": sum(not certificate["all"] for _, certificate in cohort),
        "private_report_path": str(private_dir / "factory_certification.json"),
        "researcher_manifest_path": str(public_dir / "researcher_manifest.json"),
        "agent_recipe_path": str(public_dir / "agent_recipe.json"),
    }
