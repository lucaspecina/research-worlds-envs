"""Rung 8 -- null: independent record marginals (S_null / D_MAX). GENERATED."""
import numpy as np
import pandas as pd

MARG = {'dryer_setting': (4.563327518098527, 1.2006305197565874), 'moisture_probe': (-0.013583500331767919, 1.7976260632469752), 'shelf_life': (26.925252867420568, 5.845429586512766)}
DEC = 'dryer_setting'


def model(regime, n, seed):
    rng = np.random.default_rng(seed)
    out = {}
    for c, (mu, sd) in MARG.items():
        v = rng.normal(mu, sd, n)
        out[c] = np.clip(v, 0.0, 10.0) if c == DEC else v
    return pd.DataFrame(out)
