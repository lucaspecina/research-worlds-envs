"""Wiring tests for the count-mixture jump pair (ficha 2026-08-06).

Zero-LLM. Run AFTER scripts/certify_count_mix_v0.py froze instance.json
(the certifier is the rule; these tests pin the frozen instance's contract).
"""

import json
from pathlib import Path

import numpy as np
import pytest

from cases.count_mix_v0_common import (
    ANTI_POSTER_FLOOR, INSTANCE_PATH, LAM_A_RANGE, RATIO_RANGE, W_RANGE,
    WITNESS_DBIC, WITNESS_N, _DictRegime, _sample_counts, load_instance,
    program_functionals, s_struct, single_baseline_program, valley_geometry,
    witness,
)

ROOT = Path(__file__).resolve().parents[1]

pytestmark = pytest.mark.skipif(
    not INSTANCE_PATH.exists(), reason="instance not frozen: run certify_count_mix_v0.py"
)


@pytest.fixture(scope="module")
def inst():
    return load_instance()


@pytest.fixture(scope="module")
def progs(inst):
    def make(pole):
        return lambda regime, n, seed: _sample_counts(pole, inst["params"], regime, n, seed)
    return {"mix": make("mix"), "single": make("single")}


def test_instance_within_ficha_ranges(inst):
    p = inst["params"]
    assert W_RANGE[0] <= p["w"] <= W_RANGE[1]
    assert LAM_A_RANGE[0] <= p["lam_a"] <= LAM_A_RANGE[1]
    assert RATIO_RANGE[0] <= p["lam_b"] / p["lam_a"] <= RATIO_RANGE[1]
    assert 99200 <= p["world_seed"] < 99250


def test_determinism_and_schema(progs):
    r = _DictRegime({"speed": 1.1, "repeats_per_unit": 3})
    a = progs["mix"](r, 120, 999)
    b = progs["mix"](r, 120, 999)
    assert a.equals(b)
    assert list(a.columns) == ["unit_id", "y"]
    assert len(a) == 120                      # n = FILAS (contrato del server)
    assert a["unit_id"].nunique() == 40       # 120 filas / 3 repeats
    assert (a["y"] >= 0).all() and (a["y"] == a["y"].round()).all()


def test_mean_pairing_across_speeds(progs):
    for s in (0.8, 1.0, 1.2):
        ym = progs["mix"](_DictRegime({"speed": s}), 20000, 11)["y"].mean()
        ys = progs["single"](_DictRegime({"speed": s}), 20000, 12)["y"].mean()
        assert abs(ym - ys) / ys < 0.03


def test_anti_poster_and_bimodality(inst):
    geo = valley_geometry(inst["params"])
    assert geo is not None
    assert geo["valley_ratio"] >= ANTI_POSTER_FLOOR
    assert geo == inst["geometry"] or geo["valley_band"] == inst["geometry"]["valley_band"]


def test_witness_selects_correctly_on_frozen_instance(inst, progs):
    seed = inst["witness_sample_seed"]
    y_mix = progs["mix"](_DictRegime({"speed": 1.0}), WITNESS_N, seed)["y"].to_numpy(float)
    w_mix = witness(y_mix)
    assert w_mix["selected"] == "mix2"
    assert w_mix["dbic_mix_vs_best_single"] >= WITNESS_DBIC
    assert w_mix["cv_mix_wins"] == 5
    y_single = progs["single"](_DictRegime({"speed": 1.0}), WITNESS_N, seed)["y"].to_numpy(float)
    w_single = witness(y_single)
    assert w_single["selected"] != "mix2"


def test_s_struct_anchors(inst, progs):
    geo, tail_at = inst["geometry"], inst["tail_at"]
    truth_f = program_functionals(progs["mix"], geo, tail_at)
    y_train = progs["mix"](_DictRegime({"speed": 1.0}), WITNESS_N,
                           inst["witness_sample_seed"])["y"].to_numpy(float)
    base_prog, _ = single_baseline_program(y_train)
    base_f = program_functionals(base_prog, geo, tail_at)
    assert s_struct(truth_f, truth_f, base_f)["S_struct"] >= 0.9
    assert s_struct(base_f, truth_f, base_f)["S_struct"] <= 0.1
    # a mixture-shaped program with roughly right structure scores high
    assert truth_f["icc"] >= 0.4


def test_icc_separates_poles(inst, progs):
    geo, tail_at = inst["geometry"], inst["tail_at"]
    f_mix = program_functionals(progs["mix"], geo, tail_at)
    f_single = program_functionals(progs["single"], geo, tail_at)
    assert f_mix["icc"] >= 0.4
    assert f_single["icc"] <= 0.1


def test_briefs_byte_identical():
    a = (ROOT / "cases/count_mix_v0/brief.md").read_bytes()
    b = (ROOT / "cases/count_mix_twin_v0/brief.md").read_bytes()
    assert a == b
    text = a.decode()
    for forbidden in ("subpoblac", "mezcla", "bimodal", "dos proveedores", "dos tipos"):
        assert forbidden not in text.lower()


def test_reward_path_stays_zero_llm():
    import cases.count_mix_v0_common as mod
    src = Path(mod.__file__).read_text().lower()
    for token in ("openai", "anthropic", "llm_client", "foundrychat"):
        assert token not in src
