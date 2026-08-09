"""Rung 7 -- naive joint Gaussian of the record (S_naive anchor, R=0). GENERATED."""
import numpy as np
import pandas as pd

COLS = ['steam_profile_bias', 'wet_end_fluorescence', 'final_brightness_score']
MU = np.array([5.19753018781641, -0.0009872386674790814, 30.3315003943256])
COV = np.array([[4.15393354387084, 1.8187102100749322, 11.434954794417923], [1.8187102100749322, 2.8789280497354324, 8.18544176619921], [11.434954794417923, 8.18544176619921, 46.72702498069055]])
DEC = 'steam_profile_bias'


def model(regime, n, seed):
    rng = np.random.default_rng(seed)
    di = COLS.index(DEC)
    if DEC in regime.config:
        dv = float(regime.config[DEC]); keep = [i for i in range(len(COLS)) if i != di]
        mu_c = MU[keep] + COV[np.ix_(keep, [di])][:, 0] / COV[di, di] * (dv - MU[di])
        cov_c = COV[np.ix_(keep, keep)] - np.outer(COV[keep, di], COV[di, keep]) / COV[di, di]
        draw = rng.multivariate_normal(mu_c, cov_c, n)
        out = {DEC: np.full(n, dv)}
        for j, i in enumerate(keep):
            out[COLS[i]] = draw[:, j]
        return pd.DataFrame(out)[COLS]
    draw = rng.multivariate_normal(MU, COV, n)
    out = {c: draw[:, i] for i, c in enumerate(COLS)}
    out[DEC] = np.clip(out[DEC], 0.0, 10.0)
    return pd.DataFrame(out)[COLS]
