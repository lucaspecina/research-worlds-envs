"""Rung 8 -- null: independent record marginals (S_null / D_MAX). GENERATED."""
import numpy as np
import pandas as pd

MARG = {'dryer_balance_index': (5.19753018781641, 2.038120100453072), 'wet_end_response_signal': (-0.0009872386674790814, 1.6967404190787208), 'sheet_finish_score': (30.328803814864866, 6.717476222641793)}
DEC = 'dryer_balance_index'


def model(regime, n, seed):
    rng = np.random.default_rng(seed)
    out = {}
    for c, (mu, sd) in MARG.items():
        v = rng.normal(mu, sd, n)
        out[c] = np.clip(v, 0.0, 10.0) if c == DEC else v
    return pd.DataFrame(out)
