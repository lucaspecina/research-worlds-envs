import numpy as np
import pandas as pd
COEFFS = [5.927148461074059, 1.2539091472759525, 1.7826993218733893]


def model(regime, n, seed):
    config = regime.config or {}
    speed = float(config.get("speed", 1.0))
    speed = min(max(speed, 0.8), 1.4)
    lam = float(np.exp(np.polyval(np.asarray(COEFFS), np.log(speed))))
    rng = np.random.default_rng(np.random.SeedSequence([int(seed), 2]))
    y = rng.poisson(lam, int(n)).astype(float)
    return pd.DataFrame({"unit_id": np.arange(int(n), dtype=float), "y": y})
