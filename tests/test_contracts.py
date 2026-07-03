"""L0 - contract tests: schemas, regime semantics, anchors, round-trips."""

import json

import pytest
from pydantic import ValidationError

from wager.contracts import (
    AnchorSet,
    Battery,
    BatteryItem,
    CaseMeta,
    Regime,
)


def test_regime_frozen_and_defaults():
    r = Regime(config={"dose": 3.0})
    assert r.context == {} and r.horizon is None
    with pytest.raises(ValidationError):
        r.config = {"dose": 4.0}  # frozen


def test_regime_rejects_extra_keys():
    with pytest.raises(ValidationError):
        Regime(confg={"dose": 3.0})  # typo => extra=forbid catches it


def test_battery_roundtrip(tmp_path, battery):
    path = tmp_path / "battery.json"
    battery.to_json_file(path)
    again = Battery.from_json_file(path)
    assert again == battery


def test_battery_item_weight_must_be_positive():
    with pytest.raises(ValidationError):
        BatteryItem(weight=0.0, regime=Regime(), seed_world=1)


def test_meta_loads_and_declares_mechanism_operator(meta):
    assert meta.case_id == "dummy_dose_v0"
    names = {op.name: op.layer for op in meta.operators}
    # Decision Log v0.11: confounding-by-indication is mechanism here
    assert names["confounding_por_asignacion"] == "mechanism"


def test_meta_columns_match_battery_world(meta):
    assert meta.column_names == ["dose", "marker", "outcome"]


def test_anchor_r_is_one_at_truth_zero_below_naive():
    anchors = AnchorSet(s_truth=-1.0, s_naive=-3.0, s_null=-5.0)
    r_truth, _ = anchors.r_of(-1.0)
    r_naive, _ = anchors.r_of(-3.0)
    r_below, unclipped = anchors.r_of(-4.0)
    assert r_truth == pytest.approx(1.0)
    assert r_naive == pytest.approx(0.0)
    assert r_below == 0.0 and unclipped < 0.0  # clip floor, Decision Log v0.10


def test_anchor_rejects_nondiscriminating_world():
    anchors = AnchorSet(s_truth=-2.0, s_naive=-2.0, s_null=-5.0)
    with pytest.raises(ValueError):
        anchors.r_of(-2.0)


def test_case_meta_extra_forbidden(case_dir):
    raw = json.loads((case_dir / "meta.json").read_text(encoding="utf-8"))
    raw["bogus_field"] = 1
    with pytest.raises(ValidationError):
        CaseMeta.model_validate(raw)


def test_suite_c_f_is_frozen_identically_across_cases():
    """Suite lint (Decision Log v0.31-e / v0.38, same commit as the freeze):
    within a suite, every case that declares functionals must freeze the SAME
    c_f -- calibrating per case would be authorship."""
    import json
    from pathlib import Path

    root = Path(__file__).resolve().parents[1]
    by_suite = {}
    for meta_path in sorted((root / "cases").glob("*/meta.json")):
        meta = json.loads(meta_path.read_text(encoding="utf-8"))
        if (meta.get("stakes") or {}).get("functionals"):
            c_f = meta.get("scoring", {}).get("c_f")
            assert c_f is not None, f"{meta_path.parent.name}: declares functionals but no frozen c_f"
            by_suite.setdefault(meta["suite"], {})[meta_path.parent.name] = c_f
    for suite, vals in by_suite.items():
        assert len(set(map(str, vals.values()))) == 1, (
            f"suite '{suite}' declares different c_f across cases: {vals}"
        )
