"""Null rival: historical marginals, independent and control-insensitive."""

import numpy as np
import pandas as pd


def model(regime, n, seed):
    rng = np.random.default_rng(seed)
    return pd.DataFrame({
        "feedstock": rng.normal(5.0, 2.015, n),
        "outcome": rng.normal(30.0, 4.123, n),
    })
