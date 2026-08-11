"""Truth program autocontenido D2 (sandbox-safe; congelado de instance.json)."""
import numpy as np
import pandas as pd

MU0, BETA, SQ, SEX, DSH = 92.29664480335553, -1.6350957618127575, 1.0, 0.8306623862918076, 3.59619159825807
PI0, SLOPE = 0.2, 0.5
POLE = 'instrumento'


def model(regime, n, seed):
    config = regime.config or {}
    T = min(max(float(config.get("T", 1.0)), 0.6), 1.4)
    p = min(max(PI0 + SLOPE * (T - 1.0), 0.02), 0.65)
    rng = np.random.default_rng(np.random.SeedSequence([int(seed), 0xD2]))
    q = rng.normal(0, SQ, int(n))
    affected = rng.random(int(n)) < p
    fault = -DSH + rng.normal(0, SEX, int(n))
    y = MU0 + BETA * (T - 1.0) + q
    if POLE == "proceso":
        y = y + np.where(affected, fault, 0.0)
    return pd.DataFrame({"unit_id": np.arange(int(n), dtype=float), "y": y})
