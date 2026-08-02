"""Executable ceiling: South grade response; 75/25 North mechanism mixture."""

import numpy as np
import pandas as pd


def model(regime, n, seed):
    rng = np.random.default_rng(seed)
    t = rng.uniform(0.0, 1.0, n)
    eh = rng.normal(0.0, 0.5, n)
    ef = rng.normal(0.0, 0.9, n)
    ey = rng.normal(0.0, 2.0, n)
    selector_rng = np.random.default_rng(
        np.random.SeedSequence([int(seed), 0x4D49584544])
    )
    use_humidity = selector_rng.random(n) < 0.75
    h = np.full(n, float(regime.config["humidity"])) if "humidity" in regime.config else 2.0 + 6.0 * t + eh
    g = np.full(n, float(regime.config["feedstock_grade"])) if "feedstock_grade" in regime.config else 10.0 - h
    mu_g = 20.0 + 2.0 * g
    mu_h = 40.0 - 2.0 * h
    south = str(regime.context.get("site", "south")).lower() == "south"
    if south:
        mu = mu_g
    elif "feedstock_grade" not in regime.config:
        mu = mu_h
    else:
        mu = np.where(use_humidity, mu_h, mu_g)
    return pd.DataFrame({"feedstock": g + ef, "outcome": mu + ey})
