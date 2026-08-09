"""Naive anchor: retain the feedstock-response explanation."""

import numpy as np
import pandas as pd


def model(regime, n, seed):
    rng = np.random.default_rng(seed)
    cfg = regime.config
    intervention = "feedstock_grade" in cfg or "humidity" in cfg
    if not intervention:
        era = rng.uniform(0.0, 1.0, n)
        humidity = 2.0 + 6.0 * era + rng.normal(0.0, 0.30, n)
        grade = 10.0 - humidity
    else:
        humidity = (np.full(n, float(cfg["humidity"])) if "humidity" in cfg
                    else rng.normal(5.0, 0.70, n))
        grade = (np.full(n, float(cfg["feedstock_grade"]))
                 if "feedstock_grade" in cfg else rng.normal(5.0, 0.70, n))
    feedstock = grade + rng.normal(0.0, 0.50, n)
    noise = rng.normal(0.0, 1.50, n)
    outcome = (40.0 - 2.0 * humidity + noise if not intervention
               else 20.0 + 2.0 * grade + noise)
    return pd.DataFrame({"feedstock": feedstock, "outcome": outcome})
