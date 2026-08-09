"""RETAIN pole of the four-way topology probe."""

from cases.first_story_scm_transfer_topology_v1_common import latent_sample, sample as _sample

POLE = "retain"


def _latent_sample(regime, n, seed):
    return latent_sample(POLE, regime, n, seed)


def sample(regime, n, seed):
    return _sample(POLE, regime, n, seed)


model = sample
