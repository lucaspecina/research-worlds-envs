"""Shared physics for the four-pole South-to-North topology probe.

The deliverable predicts only ``feedstock`` and ``outcome``.  ``batch_class``
is an extra, agent-facing view column and an optional evaluation context.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

P_HUMIDITY = 0.75
SITES = frozenset({"south", "north"})
POLES = frozenset({"retain", "revise", "local", "latent"})
_SELECTOR_STREAM = 0x544F504F
_PERMUTATION_STREAM = 0x4C4142454C


def _draw_exogenous(n: int, seed: int) -> tuple[np.ndarray, ...]:
    rng = np.random.default_rng(seed)
    era = rng.uniform(0.0, 1.0, n)
    eps_h = rng.normal(0.0, 0.5, n)
    eps_f = rng.normal(0.0, 0.9, n)
    eps_y = rng.normal(0.0, 2.0, n)
    return era, eps_h, eps_f, eps_y


def _humidity_selector(n: int, seed: int) -> np.ndarray:
    rng = np.random.default_rng(
        np.random.SeedSequence([int(seed), _SELECTOR_STREAM])
    )
    return rng.random(n) < P_HUMIDITY


def _permuted_selector(selector: np.ndarray, seed: int) -> np.ndarray:
    """Break association while preserving the selector's exact finite count."""
    rng = np.random.default_rng(
        np.random.SeedSequence([int(seed), _PERMUTATION_STREAM])
    )
    return selector[rng.permutation(len(selector))]


def _site(regime) -> str:
    site = str(regime.context.get("site", "south")).lower()
    if site not in SITES:
        raise ValueError("regime.context['site'] must be 'south' or 'north'")
    return site


def _fixed_batch_class(regime) -> str | None:
    value = regime.context.get("batch_class")
    if value is None:
        return None
    value = str(value).upper()
    if value not in {"A", "B"}:
        raise ValueError("regime.context['batch_class'] must be 'A' or 'B'")
    return value


def latent_sample(pole: str, regime, n: int, seed: int) -> pd.DataFrame:
    """Return the audit view, including the visible class and hidden mechanism."""
    if pole not in POLES:
        raise ValueError(f"unknown topology pole: {pole!r}")
    era, eps_h, eps_f, eps_y = _draw_exogenous(n, seed)
    cfg = regime.config
    site = _site(regime)
    fixed_class = _fixed_batch_class(regime)
    humidity_is_set = "humidity" in cfg
    grade_is_set = "feedstock_grade" in cfg

    humidity = (
        np.full(n, float(cfg["humidity"]))
        if humidity_is_set
        else 2.0 + 6.0 * era + eps_h
    )
    grade = (
        np.full(n, float(cfg["feedstock_grade"]))
        if grade_is_set
        else 10.0 - humidity
    )
    feedstock = grade + eps_f
    selector = _humidity_selector(n, seed)

    if fixed_class is not None:
        class_is_a = np.full(n, fixed_class == "A", dtype=bool)
    elif pole == "latent" and site == "north" and grade_is_set:
        # Same mechanisms/outcomes as LOCAL, but their visible labels carry no
        # information.  Permutation preserves the exact A/B count.
        class_is_a = _permuted_selector(selector, seed)
    else:
        # This makes the complete South prefix and every non-diagnostic view
        # byte-identical across all four poles.
        class_is_a = selector.copy()

    mu_grade = 20.0 + 2.0 * grade
    mu_humidity = 40.0 - 2.0 * humidity
    if site == "south":
        use_humidity = np.zeros(n, dtype=bool)
        outcome_mean = mu_grade
    elif not grade_is_set:
        # On G=10-H the laws coincide.  Canonicalization preserves exact twins.
        use_humidity = selector
        outcome_mean = mu_humidity
    elif pole == "retain":
        use_humidity = np.zeros(n, dtype=bool)
        outcome_mean = mu_grade
    elif pole == "revise":
        use_humidity = np.ones(n, dtype=bool)
        outcome_mean = mu_humidity
    elif pole == "local":
        use_humidity = class_is_a if fixed_class is not None else selector
        outcome_mean = np.where(use_humidity, mu_humidity, mu_grade)
    else:
        use_humidity = selector
        outcome_mean = np.where(use_humidity, mu_humidity, mu_grade)

    return pd.DataFrame(
        {
            "era": era,
            "humidity": humidity,
            "grade": grade,
            "use_humidity": use_humidity,
            "batch_class": np.where(class_is_a, "A", "B"),
            "feedstock": feedstock,
            "outcome": outcome_mean + eps_y,
        }
    )


def sample(pole: str, regime, n: int, seed: int) -> pd.DataFrame:
    hidden = latent_sample(pole, regime, n, seed)
    return hidden[["batch_class", "feedstock", "outcome"]].copy()
