"""MIX pole of the count-mixture jump pair (slice 1 de saltos).

Server-side truth -- the agent never sees this file. Lots carry a hidden type
(A/B) with component rates frozen in instance.json (chosen by rule, not hand);
defects per measurement are Poisson(rate * speed). Physics shared with the
twin via cases/count_mix_v0_common.py; the marginal MEAN is paired across
poles at every speed by construction.
"""

from cases.count_mix_v0_common import pole_sample

POLE = "mix"


def sample(regime, n, seed):
    return pole_sample(POLE, regime, n, seed)


model = sample
