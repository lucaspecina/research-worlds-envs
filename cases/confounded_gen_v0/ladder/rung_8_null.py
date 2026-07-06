"""Rung 8 -- null: independent record marginals (S_null / D_MAX). GENERATED."""
import numpy as np
import pandas as pd

MARG = {'pack_pressure': (5.10212304906193, 2.557824372022222), 'cavity_fill_time': (-0.0029485694632225084, 1.7629059121251762), 'clarity_seal_score': (21.29894261567435, 10.269307237244687)}
DEC = 'pack_pressure'


def model(regime, n, seed):
    rng = np.random.default_rng(seed)
    out = {}
    for c, (mu, sd) in MARG.items():
        v = rng.normal(mu, sd, n)
        out[c] = np.clip(v, 0.0, 10.0) if c == DEC else v
    return pd.DataFrame(out)
