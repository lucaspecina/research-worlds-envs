"""Rung 8 -- null: independent record marginals (S_null / D_MAX). GENERATED."""
import numpy as np
import pandas as pd

MARG = {'soak_intensity': (5.131856234327379, 2.6329202751640643), 'dryer_exit_signature': (-0.0009872386674790814, 1.6967404190787208), 'glaze_finish_score': (27.65269165013876, 3.191925379910048)}
DEC = 'soak_intensity'


def model(regime, n, seed):
    rng = np.random.default_rng(seed)
    out = {}
    for c, (mu, sd) in MARG.items():
        v = rng.normal(mu, sd, n)
        out[c] = np.clip(v, 0.0, 10.0) if c == DEC else v
    return pd.DataFrame(out)
