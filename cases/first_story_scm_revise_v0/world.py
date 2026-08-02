"""One pole of the paired hidden-SCM first-story probe.

Only ``feedstock`` and ``outcome`` cross the server boundary.  Both worlds use
the same observational equation and exogenous draw order; they separate only
when ``feedstock_grade`` is intervened on away from its natural relation with
humidity.  The files are identical except for ``POLE``.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

POLE = "revise"


def _draw_exogenous(n: int, seed: int) -> tuple[np.ndarray, ...]:
    """Draw every exogenous variable before any intervention branch."""
    rng = np.random.default_rng(seed)
    era = rng.uniform(0.0, 1.0, n)
    eps_h = rng.normal(0.0, 0.5, n)
    eps_f = rng.normal(0.0, 0.9, n)
    eps_y = rng.normal(0.0, 2.0, n)
    return era, eps_h, eps_f, eps_y


def _latent_sample(regime, n: int, seed: int) -> pd.DataFrame:
    """Server-side audit view; agents receive only ``sample`` below."""
    era, eps_h, eps_f, eps_y = _draw_exogenous(n, seed)
    cfg = regime.config
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

    # Canonical observational path: both twins evaluate this exact expression
    # whenever G was not intervened on.  This avoids 1e-14 float drift from the
    # algebraically equivalent 20 + 2*G expression.
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
