"""Rung -- naive single Poisson at the archive mean (S_naive anchor)."""
import numpy as np
import pandas as pd

LAM = 6.86


def model(regime, n, seed):
    config = regime.config or {}
    speed = float(config.get("speed", 1.0))
    repeats = int(round(float(config.get("repeats_per_unit", 1))))
    rng = np.random.default_rng(np.random.SeedSequence([int(seed), 0xAA02]))
    full, rem = divmod(n, repeats)
    ids = np.repeat(np.arange(full, dtype=float), repeats)
    if rem:
        ids = np.concatenate([ids, np.full(rem, float(full))])
    y = rng.poisson(LAM * speed, n).astype(float)
    return pd.DataFrame({"unit_id": ids, "y": y})
