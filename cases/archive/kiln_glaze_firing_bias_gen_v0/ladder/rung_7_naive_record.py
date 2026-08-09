"""Rung 7 -- naive joint Gaussian of the record (S_naive anchor, R=0). GENERATED."""
import numpy as np
import pandas as pd

COLS = ['soak_intensity', 'dryer_exit_signature', 'glaze_finish_score']
MU = np.array([5.131856234327379, -0.0009872386674790814, 27.65269165013876])
COV = np.array([[6.932269175370013, -2.8518096107942084, -2.1224760557561764], [-2.8518096107942084, 2.8789280497354324, 2.5808179811562413], [-2.1224760557561764, 2.5808179811562413, 10.188387630913907]])
DEC = 'soak_intensity'


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
