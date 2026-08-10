import numpy as np
import pandas as pd
CC, BETA, D0, AT = 6.519087186420435, 0.9583494927842326, 3.0, 1.1


def model(regime, n, seed):
    config = regime.config or {}
    speed = float(config.get("speed", 1.0))
    speed = min(max(speed, 0.8), 1.4)
    lam = CC * speed ** BETA + (D0 if speed >= AT else 0.0)
    rng = np.random.default_rng(np.random.SeedSequence([int(seed), 4]))
    y = rng.poisson(lam, int(n)).astype(float)
    return pd.DataFrame({"unit_id": np.arange(int(n), dtype=float), "y": y})
