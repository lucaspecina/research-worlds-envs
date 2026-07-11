
import numpy as np
import pandas as pd

def model(regime, n, seed):
    rng = np.random.default_rng(seed)
    cfg = regime.config
    u = rng.normal(0.0, 1.0, n)
    if "humidity" in cfg:
        ambient = float(cfg["humidity"]) + rng.normal(0.0, 0.5, n)
    else:
        t = rng.uniform(0.0, 1.0, n)
        ambient = 2.0 + 6.0 * t + rng.normal(0.0, 0.5, n)
    if "feedstock_grade" in cfg:
        grade = np.full(n, float(cfg["feedstock_grade"]))
    else:
        grade = np.clip(rng.normal(5.0, 1.0, n), 0.0, 10.0)
    feedstock = 6.0 + 1.0 * (grade - 5.0) - 0.9 * (ambient - 5.0) + rng.normal(0.0, 0.9, n)
    outcome = 30.0 - 2.5 * (ambient - 5.0) + 3.0 * u + rng.normal(0.0, 2.0, n)
    return pd.DataFrame({"feedstock": feedstock, "outcome": outcome})
