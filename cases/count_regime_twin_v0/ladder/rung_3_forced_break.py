import numpy as np
import pandas as pd
C, BETA, D0, AT = 7.150857751157603, 3.5319607405732034, 4.0, 1.10


def model(regime, n, seed):
    config = regime.config or {}
    speed = float(config.get("speed", 1.0))
    speed = min(max(speed, 0.8), 1.2)
    lam = C * speed ** BETA
    if speed >= AT:
        lam += D0
    rng = np.random.default_rng(np.random.SeedSequence([int(seed), 4]))
    y = rng.poisson(lam, int(n)).astype(float)
    return pd.DataFrame({"unit_id": np.arange(int(n), dtype=float), "y": y})
