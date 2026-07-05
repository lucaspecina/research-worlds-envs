"""Property tests for the trajectory pivot (v0.68-R1) -- NEW reward-path code,
verified BEFORE anything is scored with it (the treatment that class demands).

Properties: pivot(long) == wide by construction; row order / t order in the
long table is irrelevant; n = UNITS; grid violations (missing, duplicate,
off-grid, wrong columns) raise ValueError (priced as crash at scoring); the
scale-sanity clamp covers pivoted early-time low-variance columns (the
pre-registered 6th member of the scale-pathology family).
"""

import numpy as np
import pandas as pd
import pytest

from wager.reward.distance import TruthSide
from wager.reward.trajectory import pivot_trajectories, wide_columns

GRID = (0.0, 2.0, 5.0, 12.5)


def make_wide(n_units=40, seed=7):
    rng = np.random.default_rng(seed)
    return pd.DataFrame(
        {name: rng.normal(10 * i, 1.0 + i, n_units) for i, name in enumerate(wide_columns(GRID))}
    )


def wide_to_long(wide, grid=GRID, shuffle_seed=None):
    rows = []
    for unit, row in wide.iterrows():
        for j, t in enumerate(grid):
            rows.append({"unit_id": float(unit), "t": float(t), "y": float(row.iloc[j])})
    long = pd.DataFrame(rows)
    if shuffle_seed is not None:
        long = long.sample(frac=1.0, random_state=shuffle_seed).reset_index(drop=True)
    return long


def test_roundtrip_identity_and_order_invariance():
    wide = make_wide()
    for shuffle in (None, 1, 2):
        out = pivot_trajectories(wide_to_long(wide, shuffle_seed=shuffle), GRID)
        assert list(out.columns) == wide_columns(GRID)
        assert np.allclose(out.to_numpy(), wide.to_numpy())


def test_n_counts_units():
    wide = make_wide(n_units=17)
    long = wide_to_long(wide)
    assert len(long) == 17 * len(GRID)
    assert len(pivot_trajectories(long, GRID)) == 17


def test_missing_reading_raises():
    long = wide_to_long(make_wide()).drop(index=2)
    with pytest.raises(ValueError, match="exactly once"):
        pivot_trajectories(long, GRID)


def test_duplicate_reading_raises():
    long = wide_to_long(make_wide())
    with pytest.raises(ValueError, match="duplicate"):
        pivot_trajectories(pd.concat([long, long.iloc[[0]]], ignore_index=True), GRID)


def test_off_grid_time_raises():
    long = wide_to_long(make_wide())
    long.loc[0, "t"] = 3.7
    with pytest.raises(ValueError, match="not on the item's t_grid"):
        pivot_trajectories(long, GRID)


def test_wrong_columns_raise():
    with pytest.raises(ValueError, match="long format"):
        pivot_trajectories(pd.DataFrame({"unit": [1.0], "t": [0.0], "y": [1.0]}), GRID)


def test_scale_sanity_on_pivoted_early_columns():
    """The 6th scale pathology, pre-registered (MUNDOS_DINAMICOS_CONTEXT 4.3):
    an early-t column with near-zero truth variance must NOT blow distances up
    -- the relative std clamp has to cover pivoted columns without retuning."""
    rng = np.random.default_rng(11)
    n = 300
    # truth: t=0 column nearly degenerate (x0 ~ constant), later columns wide
    truth = pd.DataFrame({
        "y@0": 1.0 + rng.normal(0.0, 1e-9, n),
        "y@10": rng.normal(50.0, 8.0, n),
    })
    ts = TruthSide(truth, ["y@0", "y@10"])
    # a prediction that is EXACT on the wide column and off by an absolute
    # hair (1e-6) on the degenerate one: distance must stay tiny, not explode
    pred = truth.copy()
    pred["y@0"] = pred["y@0"] + 1e-6
    d = ts.distance_to(pred)
    assert d < 0.05, f"degenerate early-t column inflated distance to {d}"
