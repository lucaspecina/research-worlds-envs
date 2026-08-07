import numpy as np
import pandas as pd
C0, C1, C2 = 1.817822791022585, 3.539981072434123, 9.795487714129989


def model(regime, n, seed):
    config = regime.config or {}
    speed = float(config.get("speed", 1.0))
    speed = min(max(speed, 0.8), 1.2)
    x = np.log(speed)
    lam = float(np.exp(C0 + C1 * x + C2 * x * x))
    rng = np.random.default_rng(np.random.SeedSequence([int(seed), 2]))
    y = rng.poisson(lam, int(n)).astype(float)
    return pd.DataFrame({"unit_id": np.arange(int(n), dtype=float), "y": y})
