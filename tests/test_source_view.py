"""Wiring of the corrupted source views (world 3 contract; Decision Log
v0.49-v0.52). Includes the PRE-REGISTERED test: experiment never bypasses the
measurement channel (v0.9 rule, biting for the first time)."""

from types import SimpleNamespace

import numpy as np
import pandas as pd
import pytest

from wager.contracts.episode import MeasurementChannel, SelectionFilter, SourceConfig
from wager.harness.source_view import experiment_view, source_view


def toy_world(regime, n, seed):
    """signal correlates with outcome ONLY through driver (no direct edge)."""
    rng = np.random.default_rng(seed)
    driver = rng.uniform(0, 10, n)
    signal = 0.8 * driver + rng.normal(0, 1, n)
    outcome = 1.2 * driver + rng.normal(0, 1, n)
    return pd.DataFrame({"driver": driver, "signal": signal, "outcome": outcome})


def _partial_corr_given_driver(df):
    """corr(signal, outcome | driver) -- the collider's spurious signature."""
    rs = df["signal"] - np.polyval(np.polyfit(df["driver"], df["signal"], 1), df["driver"])
    ro = df["outcome"] - np.polyval(np.polyfit(df["driver"], df["outcome"], 1), df["driver"])
    return float(np.corrcoef(rs, ro)[0, 1])


SEL = SelectionFilter(weights={"signal": 1.0, "outcome": 1.0}, threshold=18.0, keep="above")
CH = MeasurementChannel(column="outcome", noise_sd=1.5)
CH_REP = MeasurementChannel(column="outcome", noise_sd=1.5, replicates=2)


def _src(**kw):
    return SourceConfig(cost_per_row=1.0, **kw)


def test_selection_induces_spurious_partial_correlation():
    clean = toy_world(SimpleNamespace(config={}, context={}, horizon=None), 4000, 7)
    view = source_view(toy_world, _src(selection=SEL), 4000, 7)
    assert abs(_partial_corr_given_driver(clean)) < 0.08   # none in the mechanism
    assert _partial_corr_given_driver(view) < -0.25        # collider: strongly negative


def test_channel_adds_declared_variance_and_experiment_never_bypasses_it():
    ns = SimpleNamespace(config={"driver": 5.0}, context={}, horizon=None)
    clean = toy_world(ns, 6000, 11)
    exp = experiment_view(toy_world, ns, CH, 6000, 11)
    # v0.9 rule (PRE-REGISTERED, v0.48): the experiment bypasses selection, NEVER
    # the meter -- measured outcome variance = process variance + sigma_med^2
    assert exp["outcome"].var() == pytest.approx(clean["outcome"].var() + CH.noise_sd**2, rel=0.15)


def test_replicates_identify_sigma_med_and_hide_the_true_column():
    view = source_view(toy_world, _src(channel=CH_REP), 6000, 13)
    assert "outcome" not in view.columns  # the meter never shows the truth
    diff = view["outcome__rep1"] - view["outcome__rep2"]
    sigma_hat = np.sqrt(diff.var() / 2.0)  # the v0.51 identifiability move
    assert sigma_hat == pytest.approx(CH_REP.noise_sd, rel=0.1)


def test_views_are_deterministic_per_seed():
    a = source_view(toy_world, _src(selection=SEL, channel=CH), 500, 21)
    b = source_view(toy_world, _src(selection=SEL, channel=CH), 500, 21)
    pd.testing.assert_frame_equal(a, b)
    c = source_view(toy_world, _src(selection=SEL, channel=CH), 500, 22)
    assert not a.equals(c)
