"""BRK pole of the count-regime IMPASSE pair (mundo 2, v1).

Server-side truth -- the agent never sees this file. Defects follow law A below
a hidden threshold s* and law B above it; the mean is CONTINUOUS at s* (only the
slope changes), and s* sits just ABOVE the plant's historical envelope, so the
prefix is pure law A and the payoff lives in the proposed new operating band.
Physics shared via cases/count_regime_v1_common.py.
"""

from cases.count_regime_v1_common import pole_sample

POLE = "brk"


def sample(regime, n, seed):
    return pole_sample(POLE, regime, n, seed)


model = sample
