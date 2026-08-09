"""Rung 7 -- naive fit of the truncated noisy Line A record (S_naive anchor).

Believes the ramp-up story on every line: exponential growth, no ceiling,
dispersion real. Constants frozen from the dev calibration of
cases/ode_second_wave_v0_common.py (record pool n=400, seed 97001) -- do not
hand-edit; re-derive to audit.
"""
import numpy as np
import pandas as pd

A, B, S_UNIT, S_READ = 0.541662, 0.521145, 0.314923, 0.570542


def model(regime, n, seed):
    rng = np.random.default_rng(seed)
    t = np.asarray(tuple(regime.context["t_grid"]), dtype=float)
    u = rng.normal(0.0, S_UNIT, n)[:, None]
    e = rng.normal(0.0, S_READ, (n, t.size))
    y = np.exp(A + B * t[None, :] + u + e)
    return pd.DataFrame({"unit_id": np.repeat(np.arange(n, dtype=float), t.size),
                         "t": np.tile(t, n), "y": y.ravel()})
