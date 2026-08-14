import numpy as np
import pandas as pd

PHASE = 0.37
LEVEL_SD = 1.0
ORTHOGONAL_SD = 0.25
READING_SD = 0.3
GAUSSIAN_SD = 1.8189045215513904

def draw_projection(rng, n):
    return rng.normal(0.0, GAUSSIAN_SD, n)


def model(regime, n, seed):
    theta = np.asarray(tuple(regime.context["t_grid"]), dtype=float)
    direction = np.cos(theta - PHASE)
    direction = direction / np.linalg.norm(direction)
    sine = np.sin(theta - PHASE)
    rng = np.random.default_rng(seed)
    level = rng.normal(0.0, LEVEL_SD, n)
    orthogonal = rng.normal(0.0, ORTHOGONAL_SD, n)
    residual = rng.normal(0.0, READING_SD, size=(n, theta.size))
    residual = residual - np.outer(residual @ direction, direction)
    projected = draw_projection(rng, n)
    y = (level[:, None] + orthogonal[:, None] * sine[None, :]
         + projected[:, None] * direction[None, :] + residual)
    return pd.DataFrame({"unit_id": np.repeat(np.arange(n, dtype=float), theta.size),
                         "t": np.tile(theta, n), "y": y.ravel()})
