"""Per-batch meter offsets (#9, ADR 0078): the record carries the drift+ramp
confound; experiments keep the meter's batch structure WITHOUT the confound.

Should-pass / should-fail pairs (ADR 0057 rule).
"""

import numpy as np
import pandas as pd

from wager.contracts.episode import BatchEffect, MeasurementChannel, SourceConfig
from wager.harness.source_view import experiment_view, source_view

SLOPE = 2.5


def _world(regime, n, seed):
    rng = np.random.default_rng(seed)
    d = rng.uniform(0, 10, n)
    y = 8.0 + SLOPE * d + rng.normal(0.0, 2.0, n)
    return pd.DataFrame({"driver": d, "outcome": y})


BATCH = BatchEffect(column="outcome", batch_size=25, offset_sd=2.0,
                    drift_per_batch=0.1, assign="driver_ramp",
                    sort_key="driver", sort_noise=1.5)
SOURCE = SourceConfig(cost_per_row=1.0,
                      channel=MeasurementChannel(column="outcome", noise_sd=1.0),
                      batch=BATCH)


def _slope(df):
    return float(np.polyfit(df["driver"], df["outcome"], 1)[0])


def test_record_slope_is_confounded_and_batch_id_exposed():
    df = source_view(_world, SOURCE, 4000, seed=7)
    assert "batch_id" in df.columns                       # the run id is visible
    # should-fail-for-naive: the pooled slope absorbs the drift+ramp
    assert _slope(df) > SLOPE + 0.3
    # within-batch slopes stay clean (offset constant inside a batch): the
    # de-confounding move EXISTS in the record itself
    within = [ _slope(g) for _, g in df.groupby("batch_id") if len(g) >= 10 ]
    assert abs(float(np.median(within)) - SLOPE) < 0.4


def test_experiment_keeps_batch_noise_but_not_the_confound():
    from types import SimpleNamespace
    ns = SimpleNamespace(config={}, context={}, horizon=None)
    df = experiment_view(_world, ns, SOURCE.channel, 4000, seed=7, source_batch=BATCH)
    assert "batch_id" in df.columns
    # should-pass: randomized-arrival batches -> the pooled slope is CLEAN
    assert abs(_slope(df) - SLOPE) < 0.3
    # ...but the meter's batch offsets are still there (between-batch variance
    # of the batch means exceeds what within-batch noise explains)
    means = df.groupby("batch_id")["outcome"].mean()
    resid = df["outcome"] - np.polyval(np.polyfit(df["driver"], df["outcome"], 1), df["driver"])
    between = float(df.assign(r=resid).groupby("batch_id")["r"].mean().std())
    assert between > 1.0  # ~offset_sd 2.0 against sem ~0.45
