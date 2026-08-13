import numpy as np
import pandas as pd

COLUMNS = ['response_01', 'response_02', 'response_03', 'response_04', 'response_05', 'response_06', 'response_07', 'response_08', 'response_09', 'response_10', 'response_11', 'response_12']
SIGNATURE = np.array([1.0, 1.0, 1.0, 1.0, 1.0, 1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0], dtype=float)
DIRECTION = SIGNATURE / np.sqrt(len(SIGNATURE))
RESIDUAL_SD = 0.5
LEVEL_SD = 0.8660254037844386
GAUSSIAN_SD = 6.7295849271341694


def draw_t(rng, n):
    return rng.normal(0.0, GAUSSIAN_SD, size=n)


def model(regime, n, seed):
    rng = np.random.default_rng(seed)
    t = draw_t(rng, n)
    level = rng.normal(0.0, LEVEL_SD, size=(n, 1))
    residual = rng.normal(0.0, RESIDUAL_SD, size=(n, len(COLUMNS)))
    residual = residual - np.outer(residual @ DIRECTION, DIRECTION)
    values = level + RESIDUAL_SD * t[:, None] * DIRECTION[None, :] + residual
    return pd.DataFrame(values, columns=COLUMNS)
