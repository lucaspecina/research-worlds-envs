"""Time-indexed functionals on trajectory worlds (spec docs/mundos-dinamicos.md 4.2).

The declared-trivial extension shipped with #11: a functional whose column is a
pivoted timestamp ("y@16") prices exactly the items whose DECLARED grid carries
that timestamp; on any other item it is inert -- never a KeyError priced as a
crash. Should-pass / should-fail pair (ADR 0057 rule).
"""

import numpy as np
import pandas as pd

from wager.contracts import FunctionalSpec
from wager.reward.functionals import FunctionalScorer

SPEC = FunctionalSpec(name="exceedance", column="y@16", threshold=80.0,
                      direction="below", brief_clause="test clause")


def _wide(cols, n=200, seed=0):
    rng = np.random.default_rng(seed)
    return pd.DataFrame({c: rng.normal(90.0, 5.0, n) for c in cols})


def test_functional_prices_items_whose_grid_has_the_timestamp():
    cols = ["y@0", "y@8", "y@16"]
    truth = _wide(cols)
    scorer = FunctionalScorer([SPEC], truth, cols, truth[cols].std().to_numpy(), c_f=0.25)
    bad = truth.copy()
    bad["y@16"] = bad["y@16"] - 15.0          # shifts mass below the threshold
    assert scorer.extra_distance(truth.copy()) < 1e-6   # same tail -> ~0
    assert scorer.extra_distance(bad) > 0.01            # mispriced tail -> pays


def test_functional_inert_on_items_without_the_timestamp():
    cols = ["y@0", "y@2", "y@4", "y@6"]       # in-record grid: no y@16
    truth = _wide(cols)
    scorer = FunctionalScorer([SPEC], truth, cols, truth[cols].std().to_numpy(), c_f=0.25)
    assert scorer.specs == []                 # pruned, not crashed
    assert scorer.extra_distance(truth.copy()) == 0.0
