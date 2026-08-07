"""Self-contained truth program (sandbox-safe; frozen from instance.json).
Server-side artifact: the scorer runs THIS through the sandbox as S_truth."""
import numpy as np
import pandas as pd

LAM0, ALPHA, SSTAR, D0, D1 = 5.545384223916012, 1.0731758921476697, 1.0710747808373247, 4.812416524321619, 19.761352545854095


def model(regime, n, seed):
    config = regime.config or {}
    speed = float(config.get("speed", 1.0))
    speed = min(max(speed, 0.8), 1.2)
    lam = LAM0 * speed ** ALPHA
    if speed >= SSTAR:
        lam += D0 + D1 * (speed - SSTAR)
    rng = np.random.default_rng(np.random.SeedSequence([int(seed), 0x4E61]))
    y = rng.poisson(lam, int(n)).astype(float)
    return pd.DataFrame({"unit_id": np.arange(int(n), dtype=float), "y": y})
