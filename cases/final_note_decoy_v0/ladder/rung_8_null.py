"""Rung 8 -- null: collapsed variance at the pooled mean."""
import numpy as np
import pandas as pd


def model(regime, n, seed):
    rng = np.random.default_rng(seed)
    return pd.DataFrame({'outcome': rng.normal(19.82211517893761, 0.01, n)})
