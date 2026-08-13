"""hidden_profiles_v0 -- two persistent profiles hidden by a continuous level.

Each row is one new specimen measured under twelve standardized tests. A specimen keeps one
unobserved type across all tests. A large continuous specimen-level offset makes every test in
isolation look like one broad population; the offset cancels when the within-specimen profile is
compared across the two test blocks.

ZERO-LLM truth. The agent never sees this file.
"""

import numpy as np
import pandas as pd

K = 12
COLUMNS = [f"response_{j:02d}" for j in range(1, K + 1)]
SIGNATURE = np.r_[np.ones(K // 2), -np.ones(K // 2)]

TYPE_SIGNAL = 0.8
RESIDUAL_SD = 0.5
LEVEL_SD = float(np.sqrt(1.0 - RESIDUAL_SD**2))


def sample(regime, n, seed):
    rng = np.random.default_rng(seed)
    hidden_type = rng.choice((-1.0, 1.0), size=n)
    continuous_level = rng.normal(0.0, LEVEL_SD, size=(n, 1))
    residual = rng.normal(0.0, RESIDUAL_SD, size=(n, K))
    values = (
        continuous_level
        + TYPE_SIGNAL * hidden_type[:, None] * SIGNATURE[None, :]
        + residual
    )
    return pd.DataFrame(values, columns=COLUMNS)


model = sample
