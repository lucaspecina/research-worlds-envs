"""v2 window-world wiring: persistence guard, choke point, anchor parity.

The signed contract (Decision Log v0.63, ARCHITECTURE 10.1):
  (3) anchor parity -- the committed truth_code fixture (bayes ceiling as CODE,
      scored through the SANDBOXED submission path) reproduces the in-process
      ceiling callable exactly (same seeds => identical draws), so the episode
      R=1 anchor IS the certification ceiling;
  (4) the window is NEVER persisted (structural guard in Battery.to_json_file)
      and is materialized at ONE choke point (WorldSide.enrich_regime) --
      bypassing it must break the ceiling loudly, not silently succeed.

Guards ship with should-pass/should-fail pairs (Decision Log v0.57-1).
"""

import sys
from pathlib import Path

import numpy as np
import pytest

ROOT = Path(__file__).resolve().parents[1]
CASE = ROOT / "cases" / "mendel_subtypes_v2"
sys.path.insert(0, str(CASE))

import anchors  # noqa: E402
import world  # noqa: E402

from wager.contracts import Battery, BatteryItem, CaseMeta  # noqa: E402
from wager.contracts.world import Regime  # noqa: E402
from wager.reward.scorer import WorldSide, score_callable, score_submission  # noqa: E402

META = CaseMeta.from_json_file(CASE / "meta.json")


def small_battery(seed0: int = 96101) -> Battery:
    items = [
        BatteryItem(weight=1.0, regime=Regime(config={"dose": d}, context={"n_cal": nc}),
                    seed_world=seed0 + i)
        for i, (d, nc) in enumerate([(3.0, 2.0), (7.0, 2.0), (3.0, 8.0), (7.0, 8.0)])
    ]
    return Battery(items=items)


# --- (4) persistence principle (v0.68-R2): DECLARED persists, DERIVED blocks --

def test_battery_persists_scalar_ncal(tmp_path):
    path = tmp_path / "battery.json"
    small_battery().to_json_file(path)  # should-pass: scalar context only
    text = path.read_text(encoding="utf-8")
    assert "n_cal" in text and "cal_window" not in text


def test_battery_persists_declared_tuple_grid(tmp_path):
    # should-pass: a trajectory world's t_grid is DECLARED item identity
    battery = Battery(items=[BatteryItem(
        weight=1.0,
        regime=Regime(config={}, context={"t_grid": (0.0, 2.0, 8.0)}),
        seed_world=1,
    )])
    path = tmp_path / "battery.json"
    battery.to_json_file(path)
    assert Battery.from_json_file(path).items[0].regime.context["t_grid"] == (0.0, 2.0, 8.0)


def test_battery_refuses_runtime_window(tmp_path):
    enriched = Battery(items=[BatteryItem(
        weight=1.0,
        regime=Regime(config={}, context={"n_cal": 4.0, "cal_window": (0.1, 0.2)}),
        seed_world=1,
    )])
    with pytest.raises(ValueError, match="runtime-DERIVED"):
        enriched.to_json_file(tmp_path / "battery.json")  # should-fail


# --- choke point: enrich determinism ------------------------------------------

def test_enrich_materializes_deterministic_window():
    ns1 = anchors.enrich(_ns({"n_cal": 8.0}), seed_world=96101)
    ns2 = anchors.enrich(_ns({"n_cal": 8.0}), seed_world=96101)
    other = anchors.enrich(_ns({"n_cal": 8.0}), seed_world=96102)
    assert ns1.context["cal_window"] == ns2.context["cal_window"]
    assert len(ns1.context["cal_window"]) == 8
    assert ns1.context["cal_window"] != other.context["cal_window"]


def _ns(context):
    from types import SimpleNamespace
    return SimpleNamespace(config={}, context=dict(context), horizon=None)


# --- (3) anchor parity + (4) bypass-fails pair --------------------------------

def test_truth_code_parity_and_bypass_breaks_ceiling():
    battery = small_battery()
    params = META.scoring
    null_fn = anchors.null_marginals()
    bayes = anchors.bayes_ceiling(META)
    truth_code = (CASE / "truth_code.py").read_text(encoding="utf-8")

    ws = WorldSide(world.sample, battery, META.column_names, params.n_samples,
                   null_sample=null_fn, functionals=META.stakes.functionals,
                   c_f=params.c_f, enrich_regime=anchors.enrich)
    fid_callable = score_callable(bayes, ws, params)
    report = score_submission(truth_code, ws, params)
    # should-pass: the committed fixture IS the certification ceiling (same
    # seeds, same RNG call order => identical draws => identical fidelity)
    assert report.fidelity == pytest.approx(fid_callable, abs=1e-9)
    assert all(item.sandbox_errors == 0 for item in report.items)

    # should-fail: WITHOUT the choke point the window never exists; the
    # ceiling player crashes on every rep (KeyError -> D_MAX) and the "R=1
    # anchor" collapses to the cap -- bypass is loud, never a silent success.
    ws_bypass = WorldSide(world.sample, battery, META.column_names, params.n_samples,
                          null_sample=null_fn, functionals=META.stakes.functionals,
                          c_f=params.c_f, enrich_regime=None)
    report_bypass = score_submission(truth_code, ws_bypass, params)
    assert all(item.sandbox_errors == params.m_reps for item in report_bypass.items)
    assert report_bypass.fidelity < fid_callable - 1.0


def test_window_battery_on_disk_has_no_window():
    text = (CASE / "battery.json").read_text(encoding="utf-8")
    assert "cal_window" not in text and "n_cal" in text
