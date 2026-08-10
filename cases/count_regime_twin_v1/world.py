"""SMOOTH pole (twin) of the count-regime IMPASSE pair (mundo 2, v1).

Server-side truth -- the agent never sees this file. Here there is NO regime
change: a single smooth power law over the whole range, level-paired to the BRK
pole on the HISTORY surface (<= 1.20) so both poles are indistinguishable in
everything the agent can buy from history. Whoever "sees a regime" here loses.
Physics shared via cases/count_regime_v1_common.py.
"""

from cases.count_regime_v1_common import pole_sample

POLE = "smooth"


def sample(regime, n, seed):
    return pole_sample(POLE, regime, n, seed)


model = sample
