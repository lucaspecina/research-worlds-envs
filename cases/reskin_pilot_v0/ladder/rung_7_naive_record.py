"""Rung 7 -- naive joint Gaussian of the record (S_naive anchor, R=0). GENERATED."""
import numpy as np
import pandas as pd

COLS = ['dryer_setting', 'moisture_probe', 'shelf_life']
MU = np.array([4.563327518098527, -0.013583500331767919, 26.925252867420568])
COV = np.array([[1.4415136449709745, 0.025873207660224253, 3.5254533888423496], [0.025873207660224253, 3.2314594632648195, 3.925720403436418], [3.5254533888423496, 3.925720403436418, 34.1690470508788]])
DEC = 'dryer_setting'


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
