"""Self-contained truth program (sandbox-safe; frozen from instance.json).
Server-side artifact: the scorer runs THIS through the sandbox as S_truth."""
import numpy as np
import pandas as pd

CC, BETA = 6.519087186420435, 0.9583494927842326


def model(regime, n, seed):
    config = regime.config or {}
    speed = float(config.get("speed", 1.0))
    speed = min(max(speed, 0.8), 1.4)
    lam = CC * speed ** BETA
    rng = np.random.default_rng(np.random.SeedSequence([int(seed), 0x5631]))
    y = rng.poisson(lam, int(n)).astype(float)
    return pd.DataFrame({"unit_id": np.arange(int(n), dtype=float), "y": y})
