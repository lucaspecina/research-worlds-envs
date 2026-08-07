"""Self-contained truth program (sandbox-safe; frozen from instance.json)."""
import numpy as np
import pandas as pd

LAM0 = 6.347909043612207


def model(regime, n, seed):
    config = regime.config or {}
    speed = float(config.get("speed", 1.0))
    speed = min(max(speed, 0.8), 1.2)
    repeats = int(round(float(config.get("repeats_per_unit", 1))))
    repeats = min(max(repeats, 1), 4)
    rng = np.random.default_rng(np.random.SeedSequence([int(seed), 0xC0117]))
    full, rem = divmod(n, repeats)
    ids = np.repeat(np.arange(full, dtype=float), repeats)
    if rem:
        ids = np.concatenate([ids, np.full(rem, float(full))])
    n_units = int(ids[-1]) + 1 if n else 0
    lam_unit = np.full(n_units, LAM0) * speed
    y = rng.poisson(lam_unit[ids.astype(int)]).astype(float)
    return pd.DataFrame({"unit_id": ids, "y": y})
