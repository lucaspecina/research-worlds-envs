"""Null anchor: independent historical marginals, insensitive to controls."""

import numpy as np
import pandas as pd


def model(regime, n, seed):
    rng = np.random.default_rng(seed)
    feedstock = rng.normal(5.0, 1.83, n)
    outcome = rng.normal(30.0, 3.82, n)
    return pd.DataFrame({"feedstock": feedstock, "outcome": outcome})
