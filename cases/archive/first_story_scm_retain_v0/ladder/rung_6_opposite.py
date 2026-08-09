"""Structural rival: the humidity-response SCM (wrong in RETAIN)."""

import numpy as np
import pandas as pd


def model(regime, n, seed):
    rng = np.random.default_rng(seed)
    t = rng.uniform(0.0, 1.0, n)
    eh = rng.normal(0.0, 0.5, n)
    ef = rng.normal(0.0, 0.9, n)
    ey = rng.normal(0.0, 2.0, n)
    h = np.full(n, float(regime.config["humidity"])) if "humidity" in regime.config else 2.0 + 6.0 * t + eh
    g = np.full(n, float(regime.config["feedstock_grade"])) if "feedstock_grade" in regime.config else 10.0 - h
    return pd.DataFrame({"feedstock": g + ef, "outcome": 40.0 - 2.0 * h + ey})
