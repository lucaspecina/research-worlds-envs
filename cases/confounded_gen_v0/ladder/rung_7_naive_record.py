"""Rung 7 -- naive joint Gaussian of the record (S_naive anchor, R=0). GENERATED."""
import numpy as np
import pandas as pd

COLS = ['pack_pressure', 'cavity_fill_time', 'clarity_seal_score']
MU = np.array([5.10212304906193, -0.0029485694632225084, 21.29894261567435])
COV = np.array([[6.542465518110874, 2.7447226253273524, 24.317472974561802], [2.7447226253273524, 3.1078372550059, 12.611372440743885], [24.317472974561802, 12.611372440743885, 105.45867113292611]])
DEC = 'pack_pressure'


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
