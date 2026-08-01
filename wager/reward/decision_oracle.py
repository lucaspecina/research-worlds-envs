"""Zero-LLM decision oracles for distributional operational policies.

This module is deliberately generic: a policy chooses one action from a
finite grid, and each action induces a predictive distribution over one
outcome.  The first consumer is the belief-revision plan probe, but none of
the code below knows about worlds, prompts, or agents.

The scientific split is important:

* an exact/reference posterior is represented as a finite Normal mixture;
* an arbitrary submitted model is evaluated through a fixed Monte Carlo
  protocol;
* utility uses the same declared downside penalty in both paths;
* reconfiguration cost is handled by the reopen decision, not hidden inside
  the utility of a replacement action.

Only numpy/scipy are imported, preserving the reward path's zero-LLM gate.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Iterable

import numpy as np
from scipy.optimize import brentq
from scipy.stats import norm


@dataclass(frozen=True)
class DecisionInstrument:
    """Fixed, public decision rule shared by every probe instance."""

    actions: tuple[float, ...]
    safety_threshold: float
    risk_penalty: float
    reopen_cost_low: float
    reopen_cost_high: float
    quantile_tau: float = 0.10

    def __post_init__(self) -> None:
        if len(self.actions) < 2:
            raise ValueError("actions must contain at least two choices")
        if tuple(sorted(set(self.actions))) != self.actions:
            raise ValueError("actions must be unique and sorted increasingly")
        if not 0.0 < self.quantile_tau < 1.0:
            raise ValueError("quantile_tau must lie in (0, 1)")
        if self.risk_penalty < 0.0:
            raise ValueError("risk_penalty must be non-negative")
        if not 0.0 <= self.reopen_cost_low < self.reopen_cost_high:
            raise ValueError("reopen costs must satisfy 0 <= low < high")


@dataclass(frozen=True)
class NormalMixture:
    """A normalized finite mixture of univariate Normal components."""

    weights: np.ndarray
    means: np.ndarray
    stds: np.ndarray

    def __post_init__(self) -> None:
        weights = np.asarray(self.weights, dtype=float)
        means = np.asarray(self.means, dtype=float)
        stds = np.asarray(self.stds, dtype=float)
        if weights.ndim != 1 or means.ndim != 1 or stds.ndim != 1:
            raise ValueError("mixture arrays must be one-dimensional")
        if not (weights.size == means.size == stds.size) or not weights.size:
            raise ValueError("mixture arrays must have the same non-zero length")
        if not np.isfinite(weights).all() or not np.isfinite(means).all():
            raise ValueError("mixture weights and means must be finite")
        if not np.isfinite(stds).all() or np.any(stds <= 0.0):
            raise ValueError("mixture standard deviations must be finite and positive")
        if np.any(weights < 0.0) or float(weights.sum()) <= 0.0:
            raise ValueError("mixture weights must be non-negative with positive mass")
        weights = weights / weights.sum()
        object.__setattr__(self, "weights", weights)
        object.__setattr__(self, "means", means)
        object.__setattr__(self, "stds", stds)

    @property
    def mean(self) -> float:
        return float(np.dot(self.weights, self.means))

    @property
    def variance(self) -> float:
        second = np.dot(self.weights, self.stds**2 + self.means**2)
        return float(max(second - self.mean**2, 0.0))

    def cdf(self, value: float) -> float:
        z = (float(value) - self.means) / self.stds
        return float(np.dot(self.weights, norm.cdf(z)))

    def quantile(self, tau: float) -> float:
        if not 0.0 < tau < 1.0:
            raise ValueError("tau must lie in (0, 1)")
        lo = float(np.min(self.means - 12.0 * self.stds))
        hi = float(np.max(self.means + 12.0 * self.stds))
        return float(brentq(lambda x: self.cdf(x) - tau, lo, hi, xtol=1e-11))

    def sample(self, n: int, seed: int) -> np.ndarray:
        if n <= 0:
            raise ValueError("n must be positive")
        rng = np.random.default_rng(seed)
        component = rng.choice(self.weights.size, size=n, p=self.weights)
        return rng.normal(self.means[component], self.stds[component])


def distribution_utility(
    distribution: NormalMixture,
    instrument: DecisionInstrument,
) -> float:
    """Expected outcome minus the declared linear downside penalty."""

    downside = max(
        0.0,
        instrument.safety_threshold - distribution.quantile(instrument.quantile_tau),
    )
    return distribution.mean - instrument.risk_penalty * downside


def _expected_abs_normal(mean: np.ndarray, std: np.ndarray) -> np.ndarray:
    """E|Z| for vectorized univariate Normal variables."""

    z = mean / std
    return (
        std * np.sqrt(2.0 / np.pi) * np.exp(-0.5 * z**2)
        + mean * (2.0 * norm.cdf(z) - 1.0)
    )


def normal_mixture_energy_distance(
    left: NormalMixture,
    right: NormalMixture,
    *,
    scale: float = 1.0,
) -> float:
    """Exact one-dimensional energy statistic between Normal mixtures.

    This is ``2 E|X-Y| - E|X-X'| - E|Y-Y'|`` evaluated by finite sums,
    avoiding a Monte Carlo gate whose pass/fail could change with a seed.
    The statistic is homogeneous, so truth-side standardization is an exact
    division by ``scale``.
    """

    if not np.isfinite(scale) or scale <= 0.0:
        raise ValueError("scale must be finite and positive")

    def cross(a: NormalMixture, b: NormalMixture) -> float:
        mean = a.means[:, None] - b.means[None, :]
        std = np.sqrt(a.stds[:, None] ** 2 + b.stds[None, :] ** 2)
        weights = a.weights[:, None] * b.weights[None, :]
        return float(np.sum(weights * _expected_abs_normal(mean, std)))

    value = 2.0 * cross(left, right) - cross(left, left) - cross(right, right)
    # Roundoff can make two identical mixtures a few ulps negative.
    return float(max(value / scale, 0.0))


def sample_utility(samples: np.ndarray, instrument: DecisionInstrument) -> float:
    """Monte Carlo analogue of :func:`distribution_utility`."""

    values = np.asarray(samples, dtype=float)
    if values.ndim != 1 or not values.size or not np.isfinite(values).all():
        raise ValueError("samples must be a non-empty finite one-dimensional array")
    downside = max(
        0.0,
        instrument.safety_threshold
        - float(np.quantile(values, instrument.quantile_tau)),
    )
    return float(values.mean() - instrument.risk_penalty * downside)


@dataclass(frozen=True)
class ExactDecision:
    action: float
    utility: float
    utilities: dict[float, float]


def exact_optimal_action(
    predict: Callable[[float], NormalMixture],
    instrument: DecisionInstrument,
) -> ExactDecision:
    """Enumerate the finite action grid; exact ties choose the safer action."""

    utilities = {
        action: distribution_utility(predict(action), instrument)
        for action in instrument.actions
    }
    best_value = max(utilities.values())
    tied = [
        a for a, value in utilities.items()
        if np.isclose(value, best_value, atol=1e-12, rtol=0.0)
    ]
    action = min(tied)
    return ExactDecision(action=action, utility=utilities[action], utilities=utilities)


@dataclass(frozen=True)
class MonteCarloDecision:
    action: float
    utility: float
    utilities: dict[float, float]
    standard_errors: dict[float, float]
    top_gap: float
    top_gap_error: float
    indeterminate: bool


def monte_carlo_optimal_action(
    sample_action: Callable[[float, int, int], np.ndarray],
    instrument: DecisionInstrument,
    *,
    n: int = 400,
    bootstrap_reps: int = 200,
    seed: int = 0,
) -> MonteCarloDecision:
    """Reference optimum for an arbitrary black-box predictive model.

    The samples and bootstrap are fully deterministic in ``seed``.  If the
    top-two gap is below twice its bootstrap error, the reference is marked
    indeterminate rather than manufacturing a crisp self-belief optimum.
    """

    if n <= 1:
        raise ValueError("n must be greater than one")
    if bootstrap_reps <= 1:
        raise ValueError("bootstrap_reps must be greater than one")

    rng = np.random.default_rng(seed)
    utilities: dict[float, float] = {}
    ses: dict[float, float] = {}
    for index, action in enumerate(instrument.actions):
        action_seed = int(rng.integers(0, 2**32 - 1, dtype=np.uint32))
        values = np.asarray(sample_action(action, n, action_seed), dtype=float)
        if values.shape != (n,) or not np.isfinite(values).all():
            raise ValueError(f"action {action:g} returned invalid samples")
        utilities[action] = sample_utility(values, instrument)
        boot = np.empty(bootstrap_reps, dtype=float)
        for b in range(bootstrap_reps):
            draw = values[rng.integers(0, n, size=n)]
            boot[b] = sample_utility(draw, instrument)
        ses[action] = float(np.std(boot, ddof=1))

    order = sorted(instrument.actions, key=lambda a: (-utilities[a], a))
    first, second = order[:2]
    gap = float(utilities[first] - utilities[second])
    gap_error = float(np.hypot(ses[first], ses[second]))
    return MonteCarloDecision(
        action=first,
        utility=utilities[first],
        utilities=utilities,
        standard_errors=ses,
        top_gap=gap,
        top_gap_error=gap_error,
        indeterminate=bool(gap < 2.0 * gap_error),
    )


@dataclass(frozen=True)
class PropagationResult:
    fraction: float | None
    own_gain: float
    sterile: bool
    incoherent_reopen: bool
    indeterminate: bool = False


def propagation_fraction(
    *,
    committed_action: float,
    final_action: float,
    own_decision: ExactDecision | MonteCarloDecision,
    epsilon: float,
    sterile_threshold: float = 0.20,
) -> PropagationResult:
    """Fraction of the improvement licensed by the agent's own belief.

    Reconfiguration cost is already sunk conditional on reopening, hence it
    cancels from numerator and denominator exactly as specified by probe v0.
    """

    if epsilon < 0.0:
        raise ValueError("epsilon must be non-negative")
    if isinstance(own_decision, MonteCarloDecision) and own_decision.indeterminate:
        return PropagationResult(
            fraction=None,
            own_gain=float("nan"),
            sterile=False,
            incoherent_reopen=False,
            indeterminate=True,
        )
    utilities = own_decision.utilities
    if committed_action not in utilities or final_action not in utilities:
        raise ValueError("committed and final actions must lie on the action grid")
    own_gain = float(own_decision.utility - utilities[committed_action])
    if own_gain < epsilon:
        return PropagationResult(
            fraction=None,
            own_gain=own_gain,
            sterile=False,
            incoherent_reopen=True,
        )
    fraction = float(
        (utilities[final_action] - utilities[committed_action]) / own_gain
    )
    return PropagationResult(
        fraction=fraction,
        own_gain=own_gain,
        sterile=bool(fraction < sterile_threshold),
        incoherent_reopen=False,
    )


def reopen_is_optimal(gross_gain: float, cost: float, *, tolerance: float = 1e-12) -> bool:
    """Whether paying the real reconfiguration cost has positive net value."""

    return bool(float(gross_gain) - float(cost) > tolerance)


def normalize_weights(log_weights: Iterable[float]) -> np.ndarray:
    """Stable normalization helper kept here to avoid duplicate oracle math."""

    values = np.asarray(tuple(log_weights), dtype=float)
    if values.ndim != 1 or not values.size or not np.isfinite(values).any():
        raise ValueError("log_weights must contain at least one finite value")
    shifted = values - np.nanmax(values)
    weights = np.exp(shifted)
    total = float(weights.sum())
    if not np.isfinite(total) or total <= 0.0:
        raise ValueError("posterior weights could not be normalized")
    return weights / total
