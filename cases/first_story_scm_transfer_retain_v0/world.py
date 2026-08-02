"""One pole of the paired South-to-North hidden-SCM transfer probe.

South uses the feedstock-grade response in both twins. North preserves the
same observational distribution while the hidden response may or may not
transfer. Exogenous draws are configuration- and site-invariant so every
comparison uses common random numbers. The twin world differs only in
``POLE``.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

POLE = "retain"
SITES = frozenset({"south", "north"})


def _draw_exogenous(n: int, seed: int) -> tuple[np.ndarray, ...]:
    """Draw every exogenous variable before any site/intervention branch."""
    rng = np.random.default_rng(seed)
    era = rng.uniform(0.0, 1.0, n)
    eps_h = rng.normal(0.0, 0.5, n)
    eps_f = rng.normal(0.0, 0.9, n)
    eps_y = rng.normal(0.0, 2.0, n)
    return era, eps_h, eps_f, eps_y


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

    if site == "south":
        # Both twins evaluate the same RETAIN mechanism in South.
        outcome_mean = 20.0 + 2.0 * grade
    else:
        # In North the observational path is canonicalized identically across
        # twins.  Only off-manifold grade interventions distinguish the poles.
        outcome_mean = (
            40.0 - 2.0 * humidity
            if POLE == "revise" or not grade_is_set
            else 20.0 + 2.0 * grade
        )
    outcome = outcome_mean + eps_y
    return pd.DataFrame(
        {
            "era": era,
            "humidity": humidity,
            "grade": grade,
            "feedstock": feedstock,
            "outcome": outcome,
        }
    )


def sample(regime, n: int, seed: int) -> pd.DataFrame:
    hidden = _latent_sample(regime, n, seed)
    return hidden[["feedstock", "outcome"]].copy()


model = sample
