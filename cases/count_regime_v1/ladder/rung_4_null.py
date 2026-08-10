import numpy as np
import pandas as pd
LAM = 8.779033861418675


def model(regime, n, seed):
    rng = np.random.default_rng(np.random.SeedSequence([int(seed), 3]))
    y = rng.poisson(LAM, int(n)).astype(float)
    return pd.DataFrame({"unit_id": np.arange(int(n), dtype=float), "y": y})
