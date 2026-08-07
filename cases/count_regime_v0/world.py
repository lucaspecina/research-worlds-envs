"""BRK pole of the count-regime jump pair (mundo 2 de saltos).

Server-side truth -- the agent never sees this file. The defect rate follows law A below a hidden speed s* and law B (level+slope break) above it.
Physics shared via cases/count_regime_v0_common.py; the level is paired
across poles on the exam grid by construction.
"""

from cases.count_regime_v0_common import pole_sample

POLE = "brk"


def sample(regime, n, seed):
    return pole_sample(POLE, regime, n, seed)


model = sample
