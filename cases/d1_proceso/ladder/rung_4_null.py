"""Anchor nulo: media plana del archivo, sin T ni estructura."""
import numpy as np
import pandas as pd

MU, SD = 91.57740648370392, 1.6


def model(regime, n, seed):
    rng = np.random.default_rng(np.random.SeedSequence([int(seed), 0xD1F]))
    return pd.DataFrame({"unit_id": np.arange(int(n), dtype=float),
                          "y": MU + rng.normal(0, SD, int(n))})
