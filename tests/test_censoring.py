"""Archival censoring (#7, ADR 0077): records clip at the old bench's limit;
experiments bypass it (fresh logging) while the channel still applies (v0.9).

Should-pass / should-fail pair (ADR 0057 rule).
"""

import numpy as np
import pandas as pd

from wager.contracts.episode import CensoringRule, MeasurementChannel, SourceConfig
from wager.harness.source_view import experiment_view, source_view

LIMIT = 45.0


def _world(regime, n, seed):
    rng = np.random.default_rng(seed)
    y = rng.normal(40.0, 10.0, n)          # ~30% of true mass above the limit
    return pd.DataFrame({"driver": rng.uniform(0, 10, n), "outcome": y})


CHANNEL = MeasurementChannel(column="outcome", noise_sd=1.0, replicates=1)
SOURCE = SourceConfig(cost_per_row=1.0, channel=CHANNEL,
                      censoring=CensoringRule(column="outcome", limit=LIMIT, side="above"))


def test_records_pile_up_at_the_limit():
    df = source_view(_world, SOURCE, 2000, seed=7)
    assert float(df["outcome"].max()) <= LIMIT                    # hard cap
    pile = float((df["outcome"] == LIMIT).mean())
    assert pile > 0.15, f"expected a visible pile-up at the limit, got {pile:.3f}"


def test_experiments_bypass_censoring_never_the_channel():
    from types import SimpleNamespace
    ns = SimpleNamespace(config={}, context={}, horizon=None)
    df = experiment_view(_world, ns, CHANNEL, 2000, seed=7)
    # should-fail-for-censoring: fresh logging sees the true upper tail...
    assert float((df["outcome"] > LIMIT).mean()) > 0.15
    # ...through the SAME meter (noise still applied: exact equality would be
    # a channel bypass, which v0.9 forbids)
    clean = _world(ns, 2000, 7)
    assert not np.allclose(df["outcome"].to_numpy(), clean["outcome"].to_numpy())


def test_censoring_clips_every_replicate():
    src = SourceConfig(cost_per_row=1.0,
                       channel=MeasurementChannel(column="outcome", noise_sd=1.0, replicates=2),
                       censoring=CensoringRule(column="outcome", limit=LIMIT, side="above"))
    df = source_view(_world, src, 500, seed=11)
    assert float(df["outcome__rep1"].max()) <= LIMIT
    assert float(df["outcome__rep2"].max()) <= LIMIT
