"""Wiring tests for the count-regime jump pair (ficha 2026-08-07).

Zero-LLM. Run AFTER scripts/build_certify_count_regime_v0.py froze
instance.json (the certifier is the rule; these tests pin the contract)."""

import json
from pathlib import Path

import numpy as np
import pytest

from cases.count_regime_v0_common import (
    ALPHA_RANGE, DELTA0_RANGE, DELTA1_RANGE, INSTANCE_PATH, LAM0_RANGE,
    SSTAR_RANGE, TWIN_PAIRING_TOL, WITNESS_DBIC_BRK, _DictRegime,
    _sample_counts, buyable_design, exam_grid, lam_truth, lam_twin,
    load_instance, s_clean, s_quiebre, smooth_rival_program,
    spurious_break_flag, forced_break_program, witness,
)

ROOT = Path(__file__).resolve().parents[1]

pytestmark = pytest.mark.skipif(
    not INSTANCE_PATH.exists(),
    reason="instance not frozen: run build_certify_count_regime_v0.py",
)


@pytest.fixture(scope="module")
def inst():
    return load_instance()


@pytest.fixture(scope="module")
def progs(inst):
    def make(pole):
        return lambda regime, n, seed: _sample_counts(pole, inst["params"], regime, n, seed)
    return {"brk": make("brk"), "smooth": make("smooth")}


def test_instance_within_ficha_ranges(inst):
    p = inst["params"]
    assert LAM0_RANGE[0] <= p["lam0"] <= LAM0_RANGE[1]
    assert ALPHA_RANGE[0] <= p["alpha"] <= ALPHA_RANGE[1]
    assert SSTAR_RANGE[0] <= p["s_star"] <= SSTAR_RANGE[1]
    assert DELTA0_RANGE[0] <= p["delta0"] <= DELTA0_RANGE[1]
    assert DELTA1_RANGE[0] <= p["delta1"] <= DELTA1_RANGE[1]
    assert 99400 <= p["world_seed"] < 99450
    assert p["s_star"] > 1.0     # gate 1: invisible from the archive


def test_determinism_and_schema(progs):
    r = _DictRegime({"speed": 1.15})
    a = progs["brk"](r, 120, 999)
    b = progs["brk"](r, 120, 999)
    assert a.equals(b)
    assert list(a.columns) == ["unit_id", "y"]
    assert len(a) == 120
    assert a["unit_id"].nunique() == 120      # one measurement per lot
    assert (a["y"] >= 0).all() and (a["y"] == a["y"].round()).all()


def test_break_lives_only_above_sstar(inst):
    p = inst["params"]
    s_lo = p["s_star"] - 0.02
    s_hi = p["s_star"] + 0.02
    smooth_extrap = p["lam0"] * s_hi ** p["alpha"]
    assert abs(lam_truth(p, s_lo) - p["lam0"] * s_lo ** p["alpha"]) < 1e-9
    assert lam_truth(p, s_hi) - smooth_extrap >= p["delta0"]


def test_twin_is_level_paired_and_smooth(inst):
    p = inst["params"]
    grid = np.asarray(exam_grid(p), float)
    assert abs(float(np.mean(lam_twin(p, grid))) - float(np.mean(lam_truth(p, grid)))) <= TWIN_PAIRING_TOL
    dense = np.linspace(0.8, 1.2, 41)
    diffs = np.diff(lam_twin(p, dense))
    assert np.all(np.abs(np.diff(diffs)) < 0.05)   # no step anywhere


def test_witness_selects_piecewise_in_brk_and_smooth_in_twin(inst):
    p = inst["params"]
    wit_brk = witness(buyable_design("brk", p))
    wit_twin = witness(buyable_design("smooth", p))
    assert wit_brk["selected"] == "piecewise"
    assert wit_brk["dbic_pw_vs_smooth"] >= WITNESS_DBIC_BRK
    assert wit_twin["selected"] == "smooth"


def test_s_anchors(inst, progs):
    p = inst["params"]
    assert s_quiebre(progs["brk"], p)["S_quiebre_fuerte"] >= 0.9          # truth ~ 1
    assert s_quiebre(smooth_rival_program(p), p)["S_quiebre_fuerte"] <= 0.1  # rival ~ 0
    assert s_clean(progs["smooth"], p)["S_clean"] >= 0.9
    assert s_clean(forced_break_program(p), p)["S_clean"] <= 0.1


def test_espurio_flag_bilateral(inst, progs):
    p = inst["params"]
    assert not spurious_break_flag(progs["smooth"], p)["spurious"]
    assert spurious_break_flag(forced_break_program(p), p)["spurious"]


def test_briefs_byte_identical_and_leak_free():
    a = (ROOT / "cases/count_regime_v0/brief.md").read_bytes()
    b = (ROOT / "cases/count_regime_twin_v0/brief.md").read_bytes()
    assert a == b
    text = a.decode().lower()
    for forbidden in ("umbral", "quiebre", "fase", "vibra", "tramo", "crítica",
                      "dos leyes", "cambio de comportamiento", "escalón", "salta"):
        assert forbidden not in text


def test_reward_path_stays_zero_llm():
    import cases.count_regime_v0_common as mod
    src = Path(mod.__file__).read_text().lower()
    for token in ("openai", "anthropic", "llm_client", "foundrychat"):
        assert token not in src
