"""Rung 8 -- null model: Line A record y-marginal, blind to time and line
(S_null / D_MAX). Constants frozen from the dev calibration of
cases/ode_second_wave_v0_common.py (record pool n=400, seed 97001) -- do not
hand-edit; re-derive to audit.
"""
import numpy as np
import pandas as pd

MEAN, SD = 14.0486, 12.8308


def model(regime, n, seed):
    rng = np.random.default_rng(seed)
    t = np.asarray(tuple(regime.context["t_grid"]), dtype=float)
    y = rng.normal(MEAN, SD, (n, t.size))
    return pd.DataFrame({"unit_id": np.repeat(np.arange(n, dtype=float), t.size),
                         "t": np.tile(t, n), "y": y.ravel()})
