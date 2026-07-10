"""Rung 8 -- null: independent record marginals (S_null / D_MAX). GENERATED."""
import numpy as np
import pandas as pd

MARG = {'dryer_speed_bias': (5.131856234327379, 2.6329202751640643), 'wet_end_drain_index': (-0.0009872386674790814, 1.6967404190787208), 'roll_quality_score': (28.24999507067803, 3.073752699904976)}
DEC = 'dryer_speed_bias'


def model(regime, n, seed):
    rng = np.random.default_rng(seed)
    out = {}
    for c, (mu, sd) in MARG.items():
        v = rng.normal(mu, sd, n)
        out[c] = np.clip(v, 0.0, 10.0) if c == DEC else v
    return pd.DataFrame(out)
