"""Wiring tests for the count_regime_v1 IMPASSE pair (ficha 2026-08-09 +
addendum ratificado). Zero-LLM; cheap; guard the frozen physics and protocol."""

import json
from pathlib import Path

import numpy as np
import pytest

from cases import count_regime_v1_common as C

ROOT = Path(__file__).resolve().parents[1]
BRK = ROOT / "cases" / "count_regime_v1"
TWIN = ROOT / "cases" / "count_regime_twin_v1"

pytestmark = pytest.mark.skipif(
    not (BRK / "instance.json").exists(), reason="instance not frozen yet")


@pytest.fixture(scope="module")
def params():
    return json.loads((BRK / "instance.json").read_text())["params"]


def test_sampling_deterministic(params):
    a = C.pole_sample("brk", C._DictRegime({"speed": 1.1}), 40, 7)
    b = C.pole_sample("brk", C._DictRegime({"speed": 1.1}), 40, 7)
    assert a.equals(b)
    assert list(a.columns) == ["unit_id", "y"]


def test_mean_continuous_at_threshold(params):
    eps = 1e-6
    lo = float(C.lam_truth(params, params["s_star"] - eps))
    hi = float(C.lam_truth(params, params["s_star"] + eps))
    assert abs(hi - lo) < 1e-3, "v1 must have NO level jump (delta0=0)"


def test_break_only_above_threshold(params):
    s_lo = np.array([0.85, 1.0, 1.15])
    assert np.allclose(C.lam_truth(params, s_lo),
                       params["lam0"] * s_lo ** params["alpha"])
    s_hi = 1.35
    base = params["lam0"] * s_hi ** params["alpha"]
    assert float(C.lam_truth(params, s_hi)) > base + 1.0


def test_threshold_above_history(params):
    assert params["s_star"] > C.HISTORY_MAX, \
        "the regime pays OUTSIDE the historical envelope by design"


def test_twin_paired_on_history_surface(params):
    hist = np.asarray(C.history_grid(), float)
    gap = C.curve_distance(C.lam_twin(params, hist), C.lam_truth(params, hist))
    assert gap <= C.TWIN_PAIRING_TOL
    band = np.asarray(C.decision_band(params), float)
    gap_band = C.curve_distance(C.lam_twin(params, band), C.lam_truth(params, band))
    assert gap_band > 1.0, "poles must DIFFER in the decision band"


def test_briefs_byte_identical_and_leak_free():
    b1 = (BRK / "brief.md").read_bytes()
    b2 = (TWIN / "brief.md").read_bytes()
    assert b1 == b2
    text = b1.decode().lower()
    for banned in ("quiebre", "régimen", "regimen", "umbral", "piecewise",
                   "threshold", "break", "dos leyes", "two laws", "anomal"):
        assert banned not in text, f"brief leaks the concept: {banned!r}"


def test_control1_fails_reference_m0(params):
    design = C.prefix_design("brk", params)
    m0 = C.m0_reference(design)
    cell1 = C.control_cell("brk", params, C.CONTROL_1, C.WITNESS_SAMPLE_SEED + 100)
    assert abs(C.z_of_cell(m0, cell1["speed"], cell1["mean"], cell1["n"])) >= C.FAIL_MIN_Z


def test_every_patch_still_fails_control2(params):
    """Compuerta B (tripwire mayor): the frozen patch library cannot absorb
    the second pilot lot."""
    design = C.prefix_design("brk", params)
    cell1 = C.control_cell("brk", params, C.CONTROL_1, C.WITNESS_SAMPLE_SEED + 100)
    cell2 = C.control_cell("brk", params, C.CONTROL_2, C.WITNESS_SAMPLE_SEED + 200)
    for name, mod in C.patch_library(design, cell1).items():
        z = C.z_of_cell(mod, cell2["speed"], cell2["mean"], cell2["n"])
        assert abs(z) >= C.PATCH_MIN_Z, f"patch {name} absorbed control 2 (z={z:.2f})"


def test_no_dictation_then_discrimination(params):
    design = C.prefix_design("brk", params)
    cell1 = C.control_cell("brk", params, C.CONTROL_1, C.WITNESS_SAMPLE_SEED + 100)
    e1 = [{"speed": cell1["speed"], "mean": cell1["mean"], "n": cell1["n"]}]
    assert C.discrimination_gap(design, e1) < C.NODICT_MAX_DBIC, \
        "at first failure NO candidate may dominate (else we measure acceptance)"
    cell2 = C.control_cell("brk", params, C.CONTROL_2, C.WITNESS_SAMPLE_SEED + 200)
    zoom = C.zoom_design("brk", params)
    zsp, zmn, znn = C.design_cells(zoom)
    extra = e1 + [{"speed": cell2["speed"], "mean": cell2["mean"], "n": cell2["n"]}] + [
        {"speed": float(s), "mean": float(m), "n": float(n)}
        for s, m, n in zip(zsp, zmn, znn)]
    assert C.discrimination_gap(design, extra) >= C.NODICT_MAX_DBIC, \
        "after the zoom the evidence MUST discriminate (alcanzabilidad)"


def test_espurio_bilateral(params):
    forced = C.forced_break_program(params)
    assert C.spurious_break_flag(forced, params)["spurious"]

    tw = C.twin_coeffs(params)

    def clean_prog(regime, n, seed, tw=tw):
        import pandas as pd
        lam = tw["c"] * C._speed_of(regime) ** tw["beta"]
        rng = np.random.default_rng(np.random.SeedSequence([int(seed), 9]))
        return pd.DataFrame({"unit_id": np.arange(int(n), dtype=float),
                             "y": rng.poisson(lam, int(n)).astype(float)})

    assert not C.spurious_break_flag(clean_prog, params)["spurious"]


def test_certificates_green():
    for case in (BRK, TWIN):
        cert = json.loads((case / "certificates.json").read_text())
        assert cert["all_pass"] is True, f"{case.name}: certification not green"


def test_episode_protocol_frozen():
    proto = json.loads((BRK / "episode_protocol.json").read_text())
    assert [c["name"] for c in proto["controls"]] == ["control_1", "control_2"]
    assert set(proto["arms"]) == {"RAW", "VISIBLE_GLOBAL", "VISIBLE_ESTRUCTURADO"}
    assert proto["outcomes"]["primary"].startswith("expansion generativa BINARIA")
    twin_proto = json.loads((TWIN / "episode_protocol.json").read_text())
    assert twin_proto["controls"] == proto["controls"], "controls must match across poles"


def test_zero_llm_in_reward_module():
    """The reward path imports nothing that could reach an LLM (the docstring
    may SAY 'zero-LLM'; what matters is what the module imports)."""
    import ast
    tree = ast.parse((ROOT / "cases" / "count_regime_v1_common.py").read_text())
    allowed = {"json", "pathlib", "numpy", "pandas", "scipy", "__future__"}
    for node in ast.walk(tree):
        mods = ([a.name for a in node.names] if isinstance(node, ast.Import)
                else [node.module] if isinstance(node, ast.ImportFrom) else [])
        for m in mods:
            root = (m or "").split(".")[0]
            assert root in allowed, f"import prohibido en el reward path: {m!r}"
