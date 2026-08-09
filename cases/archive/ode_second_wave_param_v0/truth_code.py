"""Legal scoreable ceiling for the PARAM arm (sandbox-safe)."""
import numpy as np
import pandas as pd


def _logistic(K, x0, r, t):
    return K / (1.0 + ((K - x0) / x0) * np.exp(-r * t))


def model(regime, n, seed):
    t = np.asarray(tuple(regime.context["t_grid"]), dtype=float)[None, :]
    line = str(regime.context.get("line", "A")).upper()
    stream = 0x0DEA01 if line == "A" else 0x0DEB02
    width = 3 if line == "A" else 5
    rng = np.random.default_rng(np.random.SeedSequence([int(seed), stream]))
    z = rng.standard_normal((n, width))
    x0 = np.clip(2.0 + 0.4 * z[:, 2:3], 0.5, None)
    if line == "A":
        K = np.clip(100.0 + 8.0 * z[:, 0:1], 20.0, None)
        r = 0.55 * np.exp(0.10 * z[:, 1:2])
    else:
        K = np.clip(170.0 + 8.0 * z[:, 0:1] + 4.0 * z[:, 3:4], 20.0, None)
        r = 0.368 * np.exp(0.10 * z[:, 1:2])
    y = _logistic(K, x0, r, t)
    return pd.DataFrame({
        "unit_id": np.repeat(np.arange(n, dtype=float), t.size),
        "t": np.tile(t.ravel(), n),
        "y": y.ravel(),
    })
