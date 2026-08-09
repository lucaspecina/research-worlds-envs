"""Rung 8 -- null: independent record marginals (S_null / D_MAX). GENERATED."""
import numpy as np
import pandas as pd

MARG = {'steam_profile_bias': (5.19753018781641, 2.038120100453072), 'wet_end_fluorescence': (-0.0009872386674790814, 1.6967404190787208), 'final_brightness_score': (30.3315003943256, 6.835716859312603)}
DEC = 'steam_profile_bias'


def model(regime, n, seed):
    rng = np.random.default_rng(seed)
    out = {}
    for c, (mu, sd) in MARG.items():
        v = rng.normal(mu, sd, n)
        out[c] = np.clip(v, 0.0, 10.0) if c == DEC else v
    return pd.DataFrame(out)
