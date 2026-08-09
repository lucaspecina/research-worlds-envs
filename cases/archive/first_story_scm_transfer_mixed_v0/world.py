"""Mixed pole of the paired South-to-North hidden-SCM transfer probe.

South always uses the feedstock-grade response.  In North, 75% of units use
the humidity response and 25% retain the grade response.  The latent selector
has its own deterministic RNG stream, so introducing it cannot perturb any of
the exogenous draws shared with the two pure poles.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

POLE = "mixed"
P_HUMIDITY = 0.75
SITES = frozenset({"south", "north"})
_SELECTOR_STREAM = 0x4D49584544


def _draw_exogenous(n: int, seed: int) -> tuple[np.ndarray, ...]:
    """Draw the exogenous variables exactly as in both pure twins."""
    rng = np.random.default_rng(seed)
    era = rng.uniform(0.0, 1.0, n)
    eps_h = rng.normal(0.0, 0.5, n)
    eps_f = rng.normal(0.0, 0.9, n)
    eps_y = rng.normal(0.0, 2.0, n)
    return era, eps_h, eps_f, eps_y


def _humidity_selector(n: int, seed: int) -> np.ndarray:
    """Independent, reproducible server-side mechanism assignment."""
    rng = np.random.default_rng(
        np.random.SeedSequence([int(seed), _SELECTOR_STREAM])
    )
    return rng.random(n) < P_HUMIDITY


def _site(regime) -> str:
    site = str(regime.context.get("site", "south")).lower()
    if site not in SITES:
        raise ValueError("regime.context['site'] must be 'south' or 'north'")
    return site


def _latent_sample(regime, n: int, seed: int) -> pd.DataFrame:
    """Server-side audit view; agents receive only ``sample`` below."""
    era, eps_h, eps_f, eps_y = _draw_exogenous(n, seed)
    cfg = regime.config
    site = _site(regime)
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
    use_humidity = _humidity_selector(n, seed)

    mu_grade = 20.0 + 2.0 * grade
    mu_humidity = 40.0 - 2.0 * humidity
    if site == "south":
        outcome_mean = mu_grade
    elif not grade_is_set:
        # On the natural manifold G=10-H both formulas are identical.  Use the
        # canonical expression so samples are byte-identical across all poles.
        outcome_mean = mu_humidity
    else:
        outcome_mean = np.where(use_humidity, mu_humidity, mu_grade)
    outcome = outcome_mean + eps_y
    return pd.DataFrame(
        {
            "era": era,
            "humidity": humidity,
            "grade": grade,
            "use_humidity": use_humidity,
            "feedstock": feedstock,
            "outcome": outcome,
        }
    )


def sample(regime, n: int, seed: int) -> pd.DataFrame:
    hidden = _latent_sample(regime, n, seed)
    return hidden[["feedstock", "outcome"]].copy()


model = sample
