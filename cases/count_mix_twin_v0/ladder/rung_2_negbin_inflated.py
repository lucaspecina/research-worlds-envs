"""Rung -- single NegBin (best one-component; frozen from certifier fit)."""
import numpy as np
import pandas as pd

M, R = 6.289999526583073, 39.740836544524946


def model(regime, n, seed):
    config = regime.config or {}
    speed = float(config.get("speed", 1.0))
    repeats = int(round(float(config.get("repeats_per_unit", 1))))
    rng = np.random.default_rng(np.random.SeedSequence([int(seed), 0xAA01]))
    p = R / (R + M * speed)
    full, rem = divmod(n, repeats)
    ids = np.repeat(np.arange(full, dtype=float), repeats)
    if rem:
        ids = np.concatenate([ids, np.full(rem, float(full))])
    y = rng.negative_binomial(R, p, n).astype(float)
    return pd.DataFrame({"unit_id": ids, "y": y})
