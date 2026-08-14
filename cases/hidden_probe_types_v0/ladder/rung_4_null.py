import numpy as np
import pandas as pd

PHASE = 0.37
LEVEL_SD = 1.0
ORTHOGONAL_SD = 0.25
READING_SD = 0.3
TYPE_AMPLITUDE = 0.75

def model(regime, n, seed):
    theta = np.asarray(tuple(regime.context["t_grid"]), dtype=float)
    cosine = np.cos(theta - PHASE)
    sine = np.sin(theta - PHASE)
    sd = np.sqrt(LEVEL_SD**2 + TYPE_AMPLITUDE**2 * cosine**2
                 + ORTHOGONAL_SD**2 * sine**2 + READING_SD**2)
    rng = np.random.default_rng(seed)
    y = rng.normal(0.0, sd[None, :], size=(n, theta.size))
    return pd.DataFrame({"unit_id": np.repeat(np.arange(n, dtype=float), theta.size),
                         "t": np.tile(theta, n), "y": y.ravel()})
