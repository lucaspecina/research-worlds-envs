"""Truth program autocontenido (sandbox-safe; congelado de instance.json)."""
import numpy as np
import pandas as pd

MU0, BETA, T0, SQ, SEX, DSH, PI = 92.29664480335553, -1.6350957618127575, 1.0, 1.0, 0.8306623862918076, 3.59619159825807, 0.2
POLE = 'instrumento'


def model(regime, n, seed):
    config = regime.config or {}
    T = min(max(float(config.get("T", 1.0)), 0.6), 1.4)
    rng = np.random.default_rng(np.random.SeedSequence([int(seed), 0xD1]))
    out = []
    for _ in range(int(n)):
        q = rng.normal(0, SQ)
        affected = rng.random() < PI
        fault = -DSH + rng.normal(0, SEX)
        y = MU0 + BETA * (T - T0) + q
        if POLE == "proceso" and affected:
            y += fault
        out.append(y)
    return pd.DataFrame({"unit_id": np.arange(int(n), dtype=float), "y": np.asarray(out)})
