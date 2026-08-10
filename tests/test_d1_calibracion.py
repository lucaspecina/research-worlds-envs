"""Wiring del par D1 (ficha 2026-08-10): apareo byte-exacto, anti-leak del
brief, S bilateral anclada, rutina = 0 bits, cero-LLM en el reward path."""

from __future__ import annotations

import ast
import json
from pathlib import Path
from types import SimpleNamespace

import numpy as np
import pytest

ROOT = Path(__file__).resolve().parents[1]
PROC = ROOT / "cases" / "d1_proceso"
INST = ROOT / "cases" / "d1_instrumento"

pytestmark = pytest.mark.skipif(not (PROC / "instance.json").exists(),
                                reason="instancia D1 no congelada")


def _params():
    return json.loads((PROC / "instance.json").read_text())["params"]


def test_instancia_congelada_reproducible():
    from cases import d1_calibracion_common as C
    params = _params()
    assert params == C.params_from_seed(params["world_seed"])
    assert params["world_seed"] in C.WORLD_SEEDS


def test_briefs_byte_identicos_y_sin_leaks():
    a, b = (PROC / "brief.md").read_bytes(), (INST / "brief.md").read_bytes()
    assert a == b
    texto = a.decode("utf-8").lower()
    for palabra in ("calibr", "falla", "roto", "aver", "anomal", "deriva",
                    "mezcla", "subpoblac", "bimodal", "degrada", "intermitente",
                    "autosampler", "sospech", "gemelo", "polo", "rival"):
        assert palabra not in texto, f"leak en brief: {palabra!r}"


def test_apareo_byte_exacto_en_rutina():
    from cases import d1_calibracion_common as C
    params = _params()
    C.refresh_cache(params)
    st = C.LotState(params)
    lots = [st.lot("new", i) for i in range(60)]
    ra, rb = np.random.default_rng(7), np.random.default_rng(7)
    xs = [C.sensor_reading(l, "proceso", 1.0, ra) for l in lots]
    ys = [C.sensor_reading(l, "instrumento", 1.0, rb) for l in lots]
    assert xs == ys  # igualdad EXACTA, no allclose


def test_rutina_vale_cero_bits():
    from cases import d1_calibracion_common as C
    params = _params()
    assert C.expected_info("routine", {"n_lotes": 500}, 0.5, params) == 0.0
    assert C.loglik_channel("routine", {}, np.zeros(5), "vial_fault", params) == 0.0


def test_s_metric_bilateral_anclada():
    from cases import d1_calibracion_common as C
    params = _params()
    tA = C.pole_truth_program("proceso", params)
    tB = C.pole_truth_program("instrumento", params)
    assert C.s_metric(tA, "proceso", params)["S"] == pytest.approx(1.0)
    assert C.s_metric(tB, "instrumento", params)["S"] == pytest.approx(1.0)
    assert C.s_metric(tB, "proceso", params)["S"] <= 0.1      # default limpio pierde en A
    assert C.s_metric(tA, "instrumento", params)["S"] <= 0.1  # mezcla horneada pierde en B


def test_worlds_delegan_a_polos_correctos():
    import importlib
    regime = SimpleNamespace(config={"T": 1.2})
    wa = importlib.import_module("cases.d1_proceso.world")
    wb = importlib.import_module("cases.d1_instrumento.world")
    da, db = wa.sample(regime, 400, seed=5), wb.sample(regime, 400, seed=5)
    assert list(da.columns) == list(db.columns) == ["unit_id", "y"]
    assert da["y"].mean() < db["y"].mean() - 0.3   # A arrastra la subpoblacion real


def test_truth_code_espeja_polos():
    import importlib
    regime = SimpleNamespace(config={"T": 1.0})
    ta = importlib.import_module("cases.d1_proceso.truth_code")
    tb = importlib.import_module("cases.d1_instrumento.truth_code")
    ya = ta.model(regime, 3000, seed=9)["y"]
    yb = tb.model(regime, 3000, seed=9)["y"]
    params = _params()
    assert abs(yb.mean() - params["mu0"]) < 0.1
    assert ya.mean() < yb.mean() - 0.4
    frac_low = float((ya < params["mu0"] - 2.0).mean())
    assert 0.10 < frac_low < 0.35                  # subpoblacion PI visible solo en A


def test_structural_flag_no_confunde_varianza_inflada():
    """Fix del técnico 99660: una gaussiana ancha unimodal (la jugada 'hornear
    la varianza') NO es estructura de mezcla; la mezcla real sí."""
    import pandas as pd
    from cases import d1_calibracion_common as C
    params = _params()

    def fat(regime, n, seed):
        rng = np.random.default_rng(seed)
        return pd.DataFrame({"unit_id": np.arange(int(n), dtype=float),
                             "y": params["mu0"] + rng.normal(0, 2.2, int(n))})

    assert C.structural_flag(fat, params)["has_mixture"] is False
    tA = C.pole_truth_program("proceso", params)
    tB = C.pole_truth_program("instrumento", params)
    assert C.structural_flag(tA, params)["has_mixture"] is True
    assert C.structural_flag(tB, params)["has_mixture"] is False


def test_certificados_verdes():
    for d in (PROC, INST):
        cert = json.loads((d / "certificates.json").read_text())
        assert cert["all_pass"] is True
        assert cert["gates"]["kill_single_vs_oraculo"] is False
        assert cert["gates"]["d_rutina"] == 0.0


def test_reward_path_cero_llm():
    permitidos = {"numpy", "pandas", "json", "pathlib", "sys", "math", "types",
                  "cases", "cases.d1_calibracion_common", "__future__", "scipy"}
    archivos = [ROOT / "cases" / "d1_calibracion_common.py",
                PROC / "world.py", INST / "world.py",
                PROC / "truth_code.py", INST / "truth_code.py"]
    for f in archivos:
        tree = ast.parse(f.read_text())
        for node in ast.walk(tree):
            mods = ([a.name for a in node.names] if isinstance(node, ast.Import)
                    else [node.module] if isinstance(node, ast.ImportFrom) else [])
            for m in mods:
                base = (m or "").split(".")[0]
                assert base in {p.split(".")[0] for p in permitidos}, \
                    f"import no permitido en {f.name}: {m}"
