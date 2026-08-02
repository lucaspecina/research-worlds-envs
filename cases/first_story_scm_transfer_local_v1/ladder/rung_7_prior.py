"""Common prior: South grade law; 50/50 class-insensitive North mixture."""

import numpy as np
import pandas as pd


def model(regime, n, seed):
    rng = np.random.default_rng(seed)
    era = rng.uniform(0.0, 1.0, n)
    eps_h = rng.normal(0.0, 0.5, n)
    eps_f = rng.normal(0.0, 0.9, n)
    eps_y = rng.normal(0.0, 2.0, n)
    choose_humidity = rng.random(n) < 0.5
    cfg = regime.config
    humidity = (
        np.full(n, float(cfg["humidity"]))
        if "humidity" in cfg
        else 2.0 + 6.0 * era + eps_h
    )
    grade = (
        np.full(n, float(cfg["feedstock_grade"]))
        if "feedstock_grade" in cfg
        else 10.0 - humidity
    )
    mu_grade = 20.0 + 2.0 * grade
    mu_humidity = 40.0 - 2.0 * humidity
    south = str(regime.context.get("site", "south")).lower() == "south"
    mu = (
        mu_grade
        if south
        else np.where(choose_humidity, mu_humidity, mu_grade)
    )
    return pd.DataFrame(
        {"feedstock": grade + eps_f, "outcome": mu + eps_y}
    )
