"""Common 50/50 posterior-predictive rival over the two hidden SCMs."""

import numpy as np
import pandas as pd


def model(regime, n, seed):
    rng = np.random.default_rng(seed)
    t = rng.uniform(0.0, 1.0, n)
    eh = rng.normal(0.0, 0.5, n)
    ef = rng.normal(0.0, 0.9, n)
    ey = rng.normal(0.0, 2.0, n)
    choose_grade = rng.random(n) < 0.5
    h = np.full(n, float(regime.config["humidity"])) if "humidity" in regime.config else 2.0 + 6.0 * t + eh
    g_set = "feedstock_grade" in regime.config
    g = np.full(n, float(regime.config["feedstock_grade"])) if g_set else 10.0 - h
    mu_h = 40.0 - 2.0 * h
    mu_g = 20.0 + 2.0 * g if g_set else mu_h
    y = np.where(choose_grade, mu_g, mu_h) + ey
    return pd.DataFrame({"feedstock": g + ef, "outcome": y})
