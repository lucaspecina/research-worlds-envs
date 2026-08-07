"""Self-contained truth program (sandbox-safe; frozen from instance.json).
Server-side artifact: the scorer runs THIS through the sandbox as S_truth."""
import numpy as np
import pandas as pd

W, LAM_A, LAM_B = 0.5243037622611395, 1.9323069270444901, 10.354146391870687


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
    z = rng.random(n_units) < W
    lam_unit = np.where(z, LAM_B, LAM_A) * speed
    y = rng.poisson(lam_unit[ids.astype(int)]).astype(float)
    return pd.DataFrame({"unit_id": ids, "y": y})
