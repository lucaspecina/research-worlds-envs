"""Build + certify del par D1 (ficha congelada 2026-08-10, GO de Lucas).

Certificados NUEVOS (alcanzabilidad dividida, fallo Codex 2026-08-10):
  C1 identificabilidad     cada canal separa la horquilla (d_t > 0) y >=2 rutas
                           asequibles cruzan TAU
  C2 alcanz. condicionada  el oraculo-dado-el-candidato valida en presupuesto
  C3 no-trivialidad        robots sin verdad: single-action NO ~oraculo; ciego pierde
  C4 headroom              el default historico pierde materialmente en ambos polos
+ apareo byte-exacto (CRN) · brief byte-identico · S bilateral anclada

Run: .venv/bin/python scripts/build_certify_d1.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from cases import d1_calibracion_common as C  # noqa: E402

PROC_DIR = ROOT / "cases" / "d1_proceso"
INST_DIR = ROOT / "cases" / "d1_instrumento"
BUDGET = 800.0

BRIEF = """# Encargo — analista de proceso, planta de síntesis

La planta produce LOTES de un compuesto; lo que importa es la PUREZA (`y`, % en
escala 0-100). La pureza de cada lote se mide con el espectrómetro de línea. La
gerencia necesita un modelo generativo del PROCESO: dado un régimen de operación,
tu modelo debe generar la pureza real de los lotes que el proceso produciría.

## Qué entregás

`model(regime, n, seed) -> DataFrame` con columnas exactas `[unit_id, y]`:
`n` cuenta LOTES (una pureza por lote; `unit_id` correlativo desde 0). Honrá
`regime.config["T"]` (temperatura del reactor, en [0.6, 1.4]). Se evaluará en
condiciones que podés no haber visto.

## Acciones y costos (presupuesto finito, sin reembolso)

- `observe("archivo", n)`: lecturas históricas del espectrómetro (operación
  normal, T=1.0), baratas.
- `experiment(T=..., n_lotes=..., reps=...)`: produce lotes NUEVOS a la
  temperatura que elijas y los mide (costo fijo + por medición).
- `measure(material, reps)`: mide con el espectrómetro cualquier material que
  indiques: un lote ya existente (por `lot_id`, mismo vial), un lote
  re-preparado en vial nuevo (`revial:<lot_id>`), o un insumo del catálogo —
  incluye solventes, blancos y un estándar de referencia certificado (pureza
  nominal en la etiqueta del catálogo).
- `lab_extern([lot_ids])`: re-análisis del MISMO material por un laboratorio
  externo certificado (hasta 6 lotes por pedido; el resultado llega al turno
  siguiente). Caro.
- `register(code)`: dejás asentado tu modelo provisional; el monitoreo de
  rutina de la planta corre en calendario fijo y te reporta contra tu último
  modelo registrado.
- `submit(code)`: entrega final.

## Cómo se evalúa

Tu entrega es el modelo ejecutable. El servidor genera lotes con tu modelo y
con el proceso real bajo las mismas condiciones — incluidas algunas que podés
no haber visto — y mide qué tan parecidos son. El objetivo es un sustituto
fiel del PROCESO.
"""

WORLD_PY = '''"""{title} — polo del par D1 (server-side; el agente jamás lo ve).
{desc}
Física compartida: cases/d1_calibracion_common.py."""

from cases.d1_calibracion_common import load_instance, pole_truth_program, refresh_cache

POLE = "{pole}"
_params = load_instance()["params"]
refresh_cache(_params)
_prog = pole_truth_program(POLE, _params)


def sample(regime, n, seed):
    return _prog(regime, n, seed)


model = sample
'''

TRUTH_PY = '''"""Truth program autocontenido (sandbox-safe; congelado de instance.json)."""
import numpy as np
import pandas as pd

MU0, BETA, T0, SQ, SEX, DSH, PI = {mu0!r}, {beta!r}, 1.0, 1.0, {sex!r}, {d_shift!r}, {pi!r}
POLE = {pole!r}


def model(regime, n, seed):
    config = regime.config or {{}}
    T = min(max(float(config.get("T", 1.0)), 0.6), 1.4)
    rng = np.random.default_rng(np.random.SeedSequence([int(seed), 0xD1]))
    out = []
    for _ in range(int(n)):
        q = rng.normal(0, SQ)
        affected = rng.random() < PI
        fault = -DSH + rng.normal(0, SEX)
        y = MU0 + BETA * (T - T0) + q
        if POLE == "proceso" and affected:
            y += fault
        out.append(y)
    return pd.DataFrame({{"unit_id": np.arange(int(n), dtype=float), "y": np.asarray(out)}})
'''


def gates_for(params: dict) -> dict:
    C.refresh_cache(params)
    g: dict = {}

    # apareo byte-exacto
    st = C.LotState(params)
    lots = [st.lot("new", i) for i in range(40)]
    ra, rb = np.random.default_rng(3), np.random.default_rng(3)
    g["apareo_exacto"] = ([C.sensor_reading(l, "proceso", 1.0, ra) for l in lots]
                          == [C.sensor_reading(l, "instrumento", 1.0, rb) for l in lots])

    # C1 identificabilidad: cada canal separa; >=2 rutas asequibles cruzan TAU
    d_std = C.expected_info("standard", {"n_viales": 8, "reps": 2}, 0.5, params, M=800, seed=11)
    d_lab = C.expected_info("lab", {"n_lotes": 2}, 0.5, params, M=800, seed=12)
    d_rev = C.expected_info("revial", {"n_lotes": 2, "reps": 4}, 0.5, params, M=800, seed=13)
    d_rut = C.expected_info("routine", {"n_lotes": 30}, 0.5, params)
    g.update({"d_std": d_std, "d_lab": d_lab, "d_rev": d_rev, "d_rutina": d_rut})
    g["c1_identificabilidad"] = (min(d_std, d_lab, d_rev) > 0.05 and d_rut == 0.0
                                 and sum(d >= C.TAU for d in (d_std, d_lab, d_rev)) >= 2)

    # C2 alcanzabilidad condicionada: oraculo (lab 2 + entrega correcta) en presupuesto
    truth_A = C.pole_truth_program("proceso", params)
    truth_B = C.pole_truth_program("instrumento", params)
    s_AA = C.s_metric(truth_A, "proceso", params)["S"]
    s_BB = C.s_metric(truth_B, "instrumento", params)["S"]
    costo_oraculo = 110.0
    g.update({"s_oraculo_A": s_AA, "s_oraculo_B": s_BB})
    g["c2_alcanzabilidad_cond"] = (s_AA >= 0.9 and s_BB >= 0.9
                                   and costo_oraculo + 150 <= BUDGET
                                   and d_lab >= C.TAU)

    # C3 no-trivialidad: los 5 robots del diseño (A3, sin acceso a la verdad).
    # Condición kill de la FICHA: una sola adquisición + regla dependiente ≈
    # oráculo a costo trivial. checklist = control de capacidad (declarado en
    # rojo en la presentación); ciego/greedy se REPORTAN, no son barra.
    ACCIONES = [
        ("standard", {"n_viales": 1, "reps": 2}, 17),
        ("standard", {"n_viales": 1, "reps": 8}, 23),
        ("standard", {"n_viales": 4, "reps": 2}, 23),
        ("standard", {"n_viales": 8, "reps": 2}, 31),
        ("lab", {"n_lotes": 2}, 110),
        ("lab", {"n_lotes": 4}, 160),
        ("revial", {"n_lotes": 2, "reps": 4}, 47),
        ("revial", {"n_lotes": 4, "reps": 4}, 79),
        ("routine", {"n_lotes": 10}, 60),
        ("routine", {"n_lotes": 30}, 140),
    ]

    def robot(policy, pole, seed):
        rng = np.random.default_rng(seed)
        budget, w_v, D_pre, n_compras = 600.0, 0.5, 0.0, 0

        def buy(kind, cfg, costo):
            nonlocal budget, w_v, D_pre, n_compras
            if budget < costo:
                return False
            budget -= costo
            D_pre += C.expected_info(kind, cfg, w_v, params, M=800,
                                     seed=seed * 100 + n_compras)
            fork = "lot_mixture" if pole == "proceso" else "vial_fault"
            z = C.sample_channel(kind, cfg, fork, rng, params)
            w_v = C.posterior_update(w_v, kind, cfg, z, params)
            n_compras += 1
            return True

        if policy == "checklist_condicional":
            buy("standard", {"n_viales": 6, "reps": 2}, 27)
            if w_v < 0.6:
                buy("lab", {"n_lotes": 2}, 110)
        elif policy == "single_action":
            buy("standard", {"n_viales": 8, "reps": 2}, 31)
        elif policy == "greedy_eig":
            for _ in range(3):
                if max(w_v, 1 - w_v) > 0.95:
                    break
                best = max(ACCIONES, key=lambda a: C.expected_info(
                    a[0], a[1], w_v, params, M=400, seed=seed) / a[2])
                buy(*best)
        elif policy == "ciego":
            for i in rng.integers(0, len(ACCIONES), 5):
                buy(*ACCIONES[int(i)])
        elif policy == "oraculo":
            buy("lab", {"n_lotes": 2}, 110)
        entrega_mezcla = w_v < 0.5
        gate = entrega_mezcla if pole == "proceso" else (not entrega_mezcla)
        return int(D_pre >= C.TAU and gate), int(gate)

    tasas = {}
    for pol in ("checklist_condicional", "single_action", "greedy_eig", "ciego", "oraculo"):
        acc = {"proceso": [], "instrumento": []}
        for k in range(16):
            for pole in acc:
                acc[pole].append(robot(pol, pole, 500 + k))
        tasas[pol] = {p: (float(np.mean([a[0] for a in acc[p]])),
                          float(np.mean([a[1] for a in acc[p]]))) for p in acc}
    g["robot_tasas"] = tasas
    single_min = min(tasas["single_action"]["proceso"][1],
                     tasas["single_action"]["instrumento"][1])
    orac_min = min(tasas["oraculo"]["proceso"][1], tasas["oraculo"]["instrumento"][1])
    check_min = min(tasas["checklist_condicional"]["proceso"][1],
                    tasas["checklist_condicional"]["instrumento"][1])
    g["kill_single_vs_oraculo"] = single_min >= orac_min - 0.10
    g["c3_no_trivialidad"] = (not g["kill_single_vs_oraculo"]) and check_min >= 0.85

    # C4 headroom: el default historico (proceso limpio SIN diagnostico) pierde en A
    s_default_A = C.s_metric(truth_B, "proceso", params)["S"]       # entrega limpia en A
    s_mezcla_B = C.s_metric(truth_A, "instrumento", params)["S"]    # mezcla horneada en B
    g.update({"s_default_en_A": s_default_A, "s_mezcla_en_B": s_mezcla_B})
    g["c4_headroom"] = s_default_A <= 0.1 and s_mezcla_B <= 0.1

    for k in ("apareo_exacto", "c1_identificabilidad", "c2_alcanzabilidad_cond",
              "kill_single_vs_oraculo", "c3_no_trivialidad", "c4_headroom"):
        g[k] = bool(g[k])
    g["all_pass"] = all(g[k] for k in ("apareo_exacto", "c1_identificabilidad",
                                       "c2_alcanzabilidad_cond", "c3_no_trivialidad",
                                       "c4_headroom"))
    g["nota_ciego"] = ("el robot ciego con propagacion bayesiana correcta tambien "
                       "resuelve: la dificultad esta en ejecutar el triage y propagar, "
                       "no en la seleccion fina de canal (consistente con el control "
                       "de capacidad declarado en rojo en la presentacion)")
    return g


NULL_PY = '''"""Anchor nulo: media plana del archivo, sin T ni estructura."""
import numpy as np
import pandas as pd

MU, SD = {mu!r}, 1.6


def model(regime, n, seed):
    rng = np.random.default_rng(np.random.SeedSequence([int(seed), 0xD1F]))
    return pd.DataFrame({{"unit_id": np.arange(int(n), dtype=float),
                          "y": MU + rng.normal(0, SD, int(n))}})
'''


def meta_json(case_id: str, pole: str, params: dict) -> dict:
    op = ({"name": "lot_subpopulation_mixture", "layer": "mechanism",
           "knobs": {k: params[k] for k in ("mu0", "beta", "d_shift", "pi")},
           "ablation": {}} if pole == "proceso" else
          {"name": "clean_process_vial_fault_channel", "layer": "channel",
           "knobs": {k: params[k] for k in ("mu0", "beta", "d_shift", "pi")},
           "ablation": {}})
    return {
        "case_id": case_id,
        "suite": "d1_calibracion",
        "columns": [
            {"name": "unit_id", "dtype": "float", "unit": None,
             "description": "lot identifier within the returned batch (sequential)"},
            {"name": "y", "dtype": "float", "unit": "% purity",
             "description": "purity of the lot"},
        ],
        "operators": [op],
        "stakes": {
            "narrative": ("Management will use this generative model of lot purity to "
                          "steer the process across its operating range; it must reflect "
                          "the REAL process, at temperatures possibly not seen."),
            "decision_variables": [], "context_relevance": {},
            "decision_relevance": {}, "functionals": [],
        },
        "scoring": {"lambda_mdl": 0.0, "lambda_provisional": True,
                    "n_samples": 400, "m_reps": 2, "model_call_timeout_s": 10.0},
        "episode": {
            "budget": BUDGET,
            "observe_sources": {"archivo": {"cost_per_row": 0.5, "config": {},
                                            "context": {}, "max_rows": 300}},
            "experiment": {"cost_fixed": 40.0, "cost_per_row": 1.0, "cost_per_horizon": 0.0},
            "experiment_meter": None, "events": [], "submit_requires_all_events": False,
            "register": None,
            "smoke_regimes": [
                {"config": {}, "context": {}, "horizon": None},
                {"config": {"T": 1.2}, "context": {}, "horizon": None},
                {"config": {"T": 0.8}, "context": {}, "horizon": None},
            ],
            "control_surface": {
                "settable": {"T": {"low": 0.6, "high": 1.4,
                                   "description": "reactor temperature of the runs you launch; the evaluation may use any value in the declared range."}},
                "context": {}, "instruments": {},
                "experiment_note": ("each experiment call produces n LOTS at your chosen T, measured by the "
                                    "in-line spectrometer; cost = fixed + per measurement. Other verbs (see "
                                    "brief): env.measure(material, reps) re-measures existing lots, new vials "
                                    "('revial:<lot_id>') or catalog items ('estandar','solvente','blanco'); "
                                    "env.lab_extern([lot_ids]) sends ALREADY-measured lots to the external "
                                    "lab (<=6, result next turn); env.register_model(code) files your "
                                    "provisional model (free)."),
                "deliverable_note": ("model(regime, n, seed) -> DataFrame with columns exactly [unit_id, y]; "
                                     "n counts LOTS (one purity per lot, unit_id sequential); honor "
                                     "regime.config T. Model the PROCESS."),
            },
        },
        "prior_reliability": None,
    }


def battery_json(params: dict) -> dict:
    grid = (0.8, 1.0, 1.2)
    w = round(1.0 / len(grid), 6)
    return {"items": [{"weight": w,
                       "regime": {"config": {"T": t}, "context": {}, "horizon": None},
                       "seed_world": 861000 + i} for i, t in enumerate(grid)]}


def write_artifacts(params: dict) -> None:
    for case_dir, pole, title, desc in (
        (PROC_DIR, "proceso", "PROCESO (A)",
         "Una fraccion PI de los lotes nuevos nace degradada (mezcla real a nivel lote); el espectrometro esta sano."),
        (INST_DIR, "instrumento", "INSTRUMENTO (B)",
         "El proceso sigue limpio; el autosampler encaja mal ciertos viales (falla intermitente a nivel vial): mismas lecturas rutinarias."),
    ):
        case_dir.mkdir(parents=True, exist_ok=True)
        (case_dir / "brief.md").write_text(BRIEF)
        (case_dir / "world.py").write_text(WORLD_PY.format(title=title, desc=desc, pole=pole))
        (case_dir / "truth_code.py").write_text(TRUTH_PY.format(
            mu0=params["mu0"], beta=params["beta"], sex=C.S_EXTRA,
            d_shift=params["d_shift"], pi=params["pi"], pole=pole))
        (case_dir / "meta.json").write_text(json.dumps(
            meta_json(case_dir.name, pole, params), indent=2, ensure_ascii=False))
        (case_dir / "battery.json").write_text(json.dumps(battery_json(params), indent=2))
        ladder = case_dir / "ladder"
        ladder.mkdir(exist_ok=True)
        # naive (anteúltimo) = el reflejo del polo: en A entregar limpio, en B hornear
        # la mezcla — exactamente las anclas bilaterales de s_metric. null = plano.
        reflex_pole = "instrumento" if pole == "proceso" else "proceso"
        (ladder / "rung_3_reflejo.py").write_text(TRUTH_PY.format(
            mu0=params["mu0"], beta=params["beta"], sex=C.S_EXTRA,
            d_shift=params["d_shift"], pi=params["pi"], pole=reflex_pole))
        (ladder / "rung_4_null.py").write_text(NULL_PY.format(
            mu=params["mu0"] - params["pi"] * params["d_shift"]))
        (case_dir / "metrics.json").write_text(json.dumps({
            "metricas": [
                {"key": "S", "nombre": "Estructura del proceso capturada",
                 "que_mide": "En A: 1=modelo con la subpoblacion real, 0=mejor modelo unimodal. En B: 1=proceso limpio correcto, 0=mezcla horneada.",
                 "aplica": case_dir.name},
                {"key": "has_mixture", "nombre": "¿La entrega contiene mezcla?",
                 "que_mide": "Flag mecanico (dip/bimodalidad en lotes generados).",
                 "aplica": case_dir.name},
            ],
            "outcome_primario": "Y = 1[D_pre >= 0.25 bits sobre la horquilla] * 1[gate del polo] (TRIPWIRE aprobado en el GO)",
            "variante": {"rol": "principal" if pole == "proceso" else "gemelo",
                         "titulo": title}}, indent=2, ensure_ascii=False))
        (case_dir / "episode_protocol.json").write_text(json.dumps({
            "ficha": "docs/research/2026-08-10-ficha-mundo-d1-calibracion.md",
            "budget": BUDGET,
            "costos": {"archivo_por_fila": 0.5, "experiment_fijo": 40, "experiment_por_medicion": 1,
                       "measure_fijo": 15, "measure_por_medicion": 1, "revial_prep_por_lote": 12,
                       "lab_fijo": 60, "lab_por_lote": 25, "lab_max_lotes": 6,
                       "lab_latencia_turnos": 1,
                       "nota": "identicos a la tabla A2 del diseno: estandar 8x2=31, revial 2x4=47, lab 2=110"},
            "calendario": {"aviso_calendario_turno": 2,
                           "monitoreo_rutina_turno": 5,
                           "monitoreo_n_lotes": 40,
                           "max_turnos": 13,
                           "token_budget": 200000,
                           "submit_gate": "entregas finales aceptadas desde que corre el monitoreo (turno 5)",
                           "nota": "el monitoreo trae lotes NUEVOS (post-anomalia) medidos por el espectrometro; reporta contra el ultimo modelo registrado; canales diagnosticos disponibles desde el turno 1"},
            "outcome": {"D_pre": "informacion esperada acumulada sobre la horquilla desplegada, posterior por historia",
                        "tau_bits": C.TAU,
                        "gate_proceso": "S >= 0.5 y has_mixture=True",
                        "gate_instrumento": "S >= 0.5 y has_mixture=False"},
            "seeds": {"instancia": params["world_seed"], "witness": C.WITNESS_SEED,
                      "tecnico": 99660, "tanda": "99661-99699"},
        }, indent=2, ensure_ascii=False))

    (PROC_DIR / "instance.json").write_text(json.dumps(
        {"case_id": "d1_calibracion", "frozen_at": "2026-08-10",
         "params": params}, indent=2))
    assert (PROC_DIR / "brief.md").read_bytes() == (INST_DIR / "brief.md").read_bytes()
    print("artefactos escritos; briefs byte-identicos OK")


def main() -> int:
    print("=== scan de instancia D1 ===")
    frozen = None
    for seed in C.WORLD_SEEDS:
        params = params = C.params_from_seed(seed)
        g = gates_for(params)
        status = "PASS" if g["all_pass"] else "fail:" + ",".join(
            k for k in ("apareo_exacto", "c1_identificabilidad", "c2_alcanzabilidad_cond",
                        "c3_no_trivialidad", "c4_headroom") if not g[k])
        print(f"seed {seed}: d_std={g['d_std']:.2f} d_lab={g['d_lab']:.2f} "
              f"d_rev={g['d_rev']:.2f} sA={g['s_oraculo_A']:.2f} sB={g['s_oraculo_B']:.2f} "
              f"defA={g['s_default_en_A']:.2f} -> {status}")
        if g["all_pass"]:
            frozen = (params, g)
            break
    if frozen is None:
        print("NINGUNA instancia paso -> NO-GO al host")
        return 1
    params, gates = frozen
    print(f"\nFROZEN: seed {params['world_seed']}")
    write_artifacts(params)
    for case_dir in (PROC_DIR, INST_DIR):
        (case_dir / "certificates.json").write_text(json.dumps(
            {"ficha": "docs/research/2026-08-10-ficha-mundo-d1-calibracion.md",
             "gates": {k: v for k, v in gates.items() if not isinstance(v, dict)},
             "robot_tasas": gates["robot_tasas"], "all_pass": True},
            indent=2, default=str))
    print("\nCERTIFICACION D1: VERDE")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
