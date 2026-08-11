"""Wiring del par D2 (ficha 2026-08-11): apareo byte-exacto con pi(T), anti-leak,
ancla congelada, certificados, cero-LLM en el reward path."""

from __future__ import annotations

import ast
import json
from pathlib import Path

import numpy as np
import pytest

ROOT = Path(__file__).resolve().parents[1]
PROC = ROOT / "cases" / "d2_proceso"
INST = ROOT / "cases" / "d2_instrumento"

pytestmark = pytest.mark.skipif(not (PROC / "instance.json").exists(),
                                reason="instancia D2 no congelada")


def _inst():
    return json.loads((PROC / "instance.json").read_text())


def test_instancia_hereda_d1_mas_eleccion_d2():
    from cases import d1_calibracion_common as C
    p = _inst()["params"]
    base = C.params_from_seed(p["world_seed"])
    for k, v in base.items():
        assert p[k] == v, f"param D1 alterado: {k}"
    assert p["pi_slope"] == 0.5 and p["d_shift_d2"] is None and p["s_extra_d2"] is None


def test_briefs_byte_identicos_y_sin_leaks():
    a, b = (PROC / "brief.md").read_bytes(), (INST / "brief.md").read_bytes()
    assert a == b
    texto = a.decode("utf-8").lower()
    for palabra in ("calibr", "falla", "roto", "aver", "anomal", "deriva",
                    "mezcla", "subpoblac", "bimodal", "degrada", "intermitente",
                    "autosampler", "sospech", "gemelo", "polo", "rival"):
        assert palabra not in texto, f"leak en brief: {palabra!r}"


def test_apareo_byte_exacto_lotes_piT():
    from cases import d1_calibracion_common as C
    from cases import d2_decision_common as D2
    p = _inst()["params"]
    C.refresh_cache(p)
    lots = [D2.lot_d2(p, "new", i, 1.3) for i in range(50)]
    ra, rb = np.random.default_rng(7), np.random.default_rng(7)
    xs = [C.sensor_reading(l, "proceso", 1.3, ra) for l in lots]
    ys = [C.sensor_reading(l, "instrumento", 1.3, rb) for l in lots]
    assert xs == ys


def test_pi_T_efectivo_y_monotono():
    from cases import d2_decision_common as D2
    p = _inst()["params"]
    assert D2.pi_T(0.7, p) < D2.pi_T(1.0, p) < D2.pi_T(1.3, p)
    frac = np.mean([D2.lot_d2(p, "new", i, 1.3)["affected"] for i in range(3000)])
    assert abs(frac - D2.pi_T(1.3, p)) < 0.04


def test_ancla_congelada_puntua_cero_y_verdad_uno():
    from cases import d1_calibracion_common as C
    from cases import d2_decision_common as D2
    import pandas as pd
    inst = _inst()
    p = inst["params"]
    cm, cs = inst["ancla_cm"], inst["ancla_cs"]

    def anchor(regime, n, seed):
        T = C._speed_T(regime)
        mu = cm[0] + cm[1] * (T - 1.0) + cm[2] * (T - 1.0) ** 2
        sd = min(max(float(np.exp(cs[0] + cs[1] * (T - 1.0) + cs[2] * (T - 1.0) ** 2)),
                     0.3), 6.0)
        rng = np.random.default_rng(seed)
        return pd.DataFrame({"unit_id": np.arange(int(n), dtype=float),
                             "y": mu + rng.normal(0, sd, int(n))})

    tA = D2.pole_truth_program_d2("proceso", p)
    grid = (0.9, 1.3)      # subgrilla para que el test sea rápido
    sT = D2.s_metric_log(tA, "proceso", p, grid=grid, anchor_zero=anchor)
    s0 = D2.s_metric_log(anchor, "proceso", p, grid=grid, anchor_zero=anchor)
    assert sT["S"] >= 0.95
    assert s0["S"] <= 0.05
    assert sT["nats_anchor"] >= 0.08     # la paga existe también en la subgrilla


def test_certificados_verdes():
    for d in (PROC, INST):
        cert = json.loads((d / "certificates.json").read_text())
        assert cert["all_pass"] is True
        assert cert["vara"]["pass"] is True
        assert cert["extra"]["apareo_exacto_piT"] is True


def test_protocolo_congela_decision_y_brazos():
    proto = json.loads((PROC / "episode_protocol.json").read_text())
    assert proto["brazos"] == ["SILENCIO", "REBOTE"]
    cal = proto["calendario"]
    assert cal["decision_turno"] == 8 and cal["piloto_T"] == 1.3
    assert "AUDITADO" in cal["debito"]["formula"]
    assert proto["outcome"]["endpoint_primario"].startswith("has_mixture")


def test_reward_path_cero_llm():
    permitidos = {"numpy", "pandas", "json", "pathlib", "sys", "math", "types",
                  "cases", "__future__", "scipy"}
    archivos = [ROOT / "cases" / "d2_decision_common.py",
                PROC / "world.py", INST / "world.py",
                PROC / "truth_code.py", INST / "truth_code.py"]
    for f in archivos:
        tree = ast.parse(f.read_text())
        for node in ast.walk(tree):
            mods = ([a.name for a in node.names] if isinstance(node, ast.Import)
                    else [node.module] if isinstance(node, ast.ImportFrom) else [])
            for m in mods:
                base = (m or "").split(".")[0]
                assert base in permitidos, f"import no permitido en {f.name}: {m}"
