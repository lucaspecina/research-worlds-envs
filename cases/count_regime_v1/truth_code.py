"""Self-contained truth program (sandbox-safe; frozen from instance.json).
Server-side artifact: the scorer runs THIS through the sandbox as S_truth."""
import numpy as np
import pandas as pd

LAM0, ALPHA, SSTAR, D1 = 6.519087186420433, 0.9583494927842311, 1.2372228889576284, 66.74009365942116


def model(regime, n, seed):
    config = regime.config or {}
    speed = float(config.get("speed", 1.0))
    speed = min(max(speed, 0.8), 1.4)
    lam = LAM0 * speed ** ALPHA + D1 * max(0.0, speed - SSTAR)
    rng = np.random.default_rng(np.random.SeedSequence([int(seed), 0x5631]))
    y = rng.poisson(lam, int(n)).astype(float)
    return pd.DataFrame({"unit_id": np.arange(int(n), dtype=float), "y": y})
