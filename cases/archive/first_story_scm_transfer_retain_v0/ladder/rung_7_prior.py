"""Common prior: learned grade response in South; 50/50 transfer in North."""

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
    g = np.full(n, float(regime.config["feedstock_grade"])) if "feedstock_grade" in regime.config else 10.0 - h
    mu_g = 20.0 + 2.0 * g
    mu_h = 40.0 - 2.0 * h
    south = str(regime.context.get("site", "south")).lower() == "south"
    mu = mu_g if south else np.where(choose_grade, mu_g, mu_h)
    return pd.DataFrame({"feedstock": g + ef, "outcome": mu + ey})
