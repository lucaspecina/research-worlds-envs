"""Rung -- DOGMATIC forced two-component split (the apophenia rival):
always claims two well-separated groups, w=0.5, regardless of the data."""
import numpy as np
import pandas as pd

LAM_LO, LAM_HI = 3.5764527580520733, 9.11936532917234


def model(regime, n, seed):
    config = regime.config or {}
    speed = float(config.get("speed", 1.0))
    repeats = int(round(float(config.get("repeats_per_unit", 1))))
    rng = np.random.default_rng(np.random.SeedSequence([int(seed), 0xAA03]))
    full, rem = divmod(n, repeats)
    ids = np.repeat(np.arange(full, dtype=float), repeats)
    if rem:
        ids = np.concatenate([ids, np.full(rem, float(full))])
    n_units = int(ids[-1]) + 1 if n else 0
    hi = rng.random(n_units) < 0.5
    lam_unit = np.where(hi, LAM_HI, LAM_LO) * speed
    y = rng.poisson(lam_unit[ids.astype(int)]).astype(float)
    return pd.DataFrame({"unit_id": ids, "y": y})
