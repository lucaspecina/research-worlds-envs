"""Rung -- null reference (degenerate: no defects ever)."""
import numpy as np
import pandas as pd


def model(regime, n, seed):
    config = regime.config or {}
    repeats = int(round(float(config.get("repeats_per_unit", 1))))
    full, rem = divmod(n, repeats)
    ids = np.repeat(np.arange(full, dtype=float), repeats)
    if rem:
        ids = np.concatenate([ids, np.full(rem, float(full))])
    return pd.DataFrame({"unit_id": ids, "y": np.zeros(n)})
