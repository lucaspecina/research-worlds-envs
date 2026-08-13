import numpy as np
import pandas as pd

COLUMNS = ['response_01', 'response_02', 'response_03', 'response_04', 'response_05', 'response_06', 'response_07', 'response_08', 'response_09', 'response_10', 'response_11', 'response_12']
SIGNATURE = np.array([1.0, 1.0, 1.0, 1.0, 1.0, 1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0], dtype=float)
DIRECTION = SIGNATURE / np.sqrt(len(SIGNATURE))
RESIDUAL_SD = 0.5
LEVEL_SD = 0.8660254037844386

MARGINAL_SD = 1.2806248474865698


def model(regime, n, seed):
    rng = np.random.default_rng(seed)
    return pd.DataFrame(rng.normal(0.0, MARGINAL_SD, size=(n, len(COLUMNS))), columns=COLUMNS)
