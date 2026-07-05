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


def test_pipeline_order_knob_changes_what_the_filter_sees():
    # v0.53-1: select_then_measure (survivorship, filter on TRUE values) vs
    # measure_then_select (admission by recorded symptom, filter on MEASURED
    # values -- with replicates, the FIRST reading). Same knobs, different bias.
    sel = SelectionFilter(weights={"outcome": 1.0}, threshold=6.0, keep="above")
    ch = MeasurementChannel(column="outcome", noise_sd=3.0)
    stm = source_view(toy_world, _src(selection=sel, channel=ch), 4000, 31)
    mts = source_view(toy_world, _src(selection=sel, channel=ch,
                                      pipeline_order="measure_then_select"), 4000, 31)
    # survivorship: TRUE outcome > 6 for every kept row (noise added after) ->
    # measured values can dip below 6 only via noise, but the noisy-admission
    # view keeps rows whose TRUE outcome is well below 6 (admitted on a lucky
    # reading) -> its MEASURED floor is exactly 6 while its true tail is fatter
    assert (mts["outcome"] > 6.0).all()          # admission on the measured value
    assert not (stm["outcome"] > 6.0).all()      # survivorship: measured dips below
    # replicates + measure_then_select: filter used rep1 (all rep1 above), rep2 free
    ch2 = MeasurementChannel(column="outcome", noise_sd=3.0, replicates=2)
    mts2 = source_view(toy_world, _src(selection=sel, channel=ch2,
                                       pipeline_order="measure_then_select"), 2000, 33)
    assert (mts2["outcome__rep1"] > 6.0).all()
    assert not (mts2["outcome__rep2"] > 6.0).all()


def test_sigma_med_identification_is_ordering_dependent():
    """v0.54-2: Var(rep1-rep2)/2 = sigma_med^2 holds ONLY when selection does
    not touch the readings (survivorship / true-values, the v0 case). Under
    admission ordering the gate saw rep1 (the admission measurement decides;
    the follow-up stays free) -> rep1 is truncation-contaminated and the
    estimator inherits the selection: biased LOW on the selected sample."""
    sel = SelectionFilter(weights={"outcome": 1.0}, threshold=10.0, keep="above")
    ch2 = MeasurementChannel(column="outcome", noise_sd=3.0, replicates=2)

    surv = source_view(toy_world, _src(selection=sel, channel=ch2), 6000, 41)
    s_surv = np.sqrt((surv["outcome__rep1"] - surv["outcome__rep2"]).var() / 2.0)
    assert s_surv == pytest.approx(ch2.noise_sd, rel=0.1)   # clean identification

    adm = source_view(toy_world, _src(selection=sel, channel=ch2,
                                      pipeline_order="measure_then_select"), 6000, 41)
    s_adm = np.sqrt((adm["outcome__rep1"] - adm["outcome__rep2"]).var() / 2.0)
    assert s_adm < ch2.noise_sd * 0.95  # inherits the truncation: NOT sigma_med


def test_v2_window_protocol_crn_smoke():
    """v2 FIRST milestone (v0.48 gate sequence): the calibration window is
    deterministic in (world-seed, n_cal) and IDENTICAL for every consumer
    (submission / anchors / rivals share it -- CRN intact); different lots
    (seeds) get different windows; the window reflects the lot (its mean
    tracks the hidden mix through the marker law). Pre-anchor-gate: no
    scorer wiring here."""
    import sys
    from pathlib import Path

    case = Path(__file__).resolve().parents[1] / "cases" / "latent_mix_v2"
    sys.path.insert(0, str(case))
    import importlib.util

    spec = importlib.util.spec_from_file_location("world_v2", case / "world.py")
    w = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(w)

    w1 = w.make_window(91001, 8)
    w2 = w.make_window(91001, 8)
    assert w1 == w2 and len(w1) == 8              # deterministic, n_cal respected
    assert w.make_window(91002, 8) != w1          # another lot, another window
    assert w.make_window(91001, 3) == w1[:0] or len(w.make_window(91001, 3)) == 3
    # the window tracks the hidden lot: big-window mean correlates with mix sign
    mixes = [w.lot_mix(s) for s in range(5000, 5040)]
    means = [np.mean(w.make_window(s, 64)) for s in range(5000, 5040)]
    assert np.corrcoef(mixes, means)[0, 1] > 0.8
    # and the truth side sees the SAME lot the window came from
    ns = SimpleNamespace(config={"dose": 6.0}, context={}, horizon=None)
    hi = max(range(5000, 5040), key=lambda s: w.lot_mix(s))
    lo = min(range(5000, 5040), key=lambda s: w.lot_mix(s))
    assert w.sample(ns, 4000, hi)["marker"].mean() > w.sample(ns, 4000, lo)["marker"].mean()
