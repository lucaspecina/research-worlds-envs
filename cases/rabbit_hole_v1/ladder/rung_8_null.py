"""Rung 8 -- null: collapsed variance (S_null / D_MAX)."""
import numpy as np
import pandas as pd


def model(regime, n, seed):
    rng = np.random.default_rng(seed)
    return pd.DataFrame({'gas_yield': rng.normal(21.78032778515842, 0.01, n)})
