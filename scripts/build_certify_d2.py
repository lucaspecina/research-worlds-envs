"""Build + certify del par D2 "El turno de decisión" (paso 3a; GO de Lucas 2026-08-11).

Hereda la instancia congelada de D1 (seed 99600) + la física D2 elegida en el scan
(pi(T), pendiente 0.5 — única desviación). Vara log-score con ancla rung-0 (el mejor
rival sin salto, momento-matcheado, CONGELADO acá como fixture de ladder).

Compuertas: las 6 de design_d2_vara (V1-V5) + apareo byte-exacto con lotes pi(T)
+ los 5 robots A3 heredados de D1 (la horquilla diagnóstica no cambió).

Run: .venv/bin/python scripts/build_certify_d2.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from cases import d1_calibracion_common as C  # noqa: E402
from cases import d2_decision_common as D2  # noqa: E402
from scripts.design_d2_vara import (  # noqa: E402
    D2_CHOICE, gates_for as vara_gates, lazy_opt_log, mid_structure, tuned_lazy_d1,
)

PROC_DIR = ROOT / "cases" / "d2_proceso"
INST_DIR = ROOT / "cases" / "d2_instrumento"
BUDGET = 800.0

# Calendario y evento de decisión (CONGELADOS acá; van al protocolo)
NOTICE_TURN = 2
MONITOR_TURN = 5
DECISION_TURN = 8
PILOT_T = 1.3
PILOT_N = 60
DEBIT_SCALE = 600.0     # débito = round(DEBIT_SCALE * |p_pred - p_real|), cap abajo
DEBIT_CAP = 150.0
NO_MODEL_DEBIT = 100.0
MAX_TURNS = 14

BRIEF = """# Encargo — analista de proceso, planta de síntesis

La planta produce LOTES de un compuesto; lo que importa es la PUREZA (`y`, % en
escala 0-100). La pureza de cada lote se mide con el espectrómetro de línea. La
gerencia está evaluando operar la línea a mayor temperatura y va a tomar
decisiones operativas con tu modelo. Necesita un modelo generativo del PROCESO.

## Qué entregás

`model(regime, n, seed) -> DataFrame` con columnas exactas `[unit_id, y]`:
`n` cuenta LOTES (una pureza por lote; `unit_id` correlativo desde 0). Honrá
`regime.config["T"]` (temperatura del reactor, en [0.6, 1.4]). Se evaluará en
condiciones que podés no haber visto. El sandbox de evaluación ejecuta tu código
con un lint estricto: usá acceso directo (`regime.config`) — nombres dinámicos
como `getattr`/`eval`/`exec` y atributos dunder están prohibidos.

## Acciones y costos (presupuesto finito, sin reembolso)

- `observe("archivo", n)`: lecturas históricas del espectrómetro (operación
  normal, T=1.0), baratas.
- `experiment(T=..., n_lotes=..., reps=...)`: produce lotes NUEVOS a la
  temperatura que elijas y los mide (costo fijo + por medición). La línea está
  CERTIFICADA para corridas propias en T ∈ [0.8, 1.2]; fuera de esa banda solo
  corre producción según su calendario.
- `measure(material, reps)`: mide con el espectrómetro cualquier material que
  indiques: un lote ya existente (por `lot_id`, mismo vial), un lote
  re-preparado en vial nuevo (`revial:<lot_id>`), o un insumo del catálogo —
  incluye solventes, blancos y un estándar de referencia certificado (pureza
  nominal en la etiqueta del catálogo).
- `lab_extern([lot_ids])`: re-análisis del MISMO material por un laboratorio
  externo certificado (hasta 6 lotes por pedido; el resultado llega al turno
  siguiente). Caro.
- `register(code)`: dejás asentado tu modelo provisional. El calendario de la
  planta usa tu ÚLTIMO modelo registrado: el monitoreo de rutina reporta contra
  él, y las decisiones operativas programadas se toman con él. Los costos
  operativos que resulten de esas decisiones se debitan de tu presupuesto.
- `submit(code)`: entrega final.

## Cómo se evalúa

Tu entrega es el modelo ejecutable: tu mejor reconstrucción del proceso
generador, lo más fiel posible. El servidor genera lotes con tu modelo y
con el proceso real bajo las mismas condiciones — incluidas algunas que podés
no haber visto — y los compara de distintas maneras. El objetivo es un
sustituto fiel del PROCESO.
"""

WORLD_PY = '''"""{title} — polo del par D2 (server-side; el agente jamás lo ve).
{desc}
Física: cases/d2_decision_common.py (pi(T)) sobre cases/d1_calibracion_common.py."""

import json
from pathlib import Path

from cases.d1_calibracion_common import refresh_cache
from cases.d2_decision_common import pole_truth_program_d2

POLE = "{pole}"
_params = json.loads((Path(__file__).resolve().parents[1] / "d2_proceso"
                      / "instance.json").read_text())["params"]
refresh_cache(_params)
_prog = pole_truth_program_d2(POLE, _params)


def sample(regime, n, seed):
    return _prog(regime, n, seed)


model = sample
'''

TRUTH_PY = '''"""Truth program autocontenido D2 (sandbox-safe; congelado de instance.json)."""
import numpy as np
import pandas as pd

MU0, BETA, SQ, SEX, DSH = {mu0!r}, {beta!r}, 1.0, {sex!r}, {d_shift!r}
PI0, SLOPE = {pi!r}, {slope!r}
POLE = {pole!r}


def model(regime, n, seed):
    config = getattr(regime, "config", None) or {{}}
    T = min(max(float(config.get("T", 1.0)), 0.6), 1.4)
    p = min(max(PI0 + SLOPE * (T - 1.0), 0.02), 0.65)
    rng = np.random.default_rng(np.random.SeedSequence([int(seed), 0xD2]))
    q = rng.normal(0, SQ, int(n))
    affected = rng.random(int(n)) < p
    fault = -DSH + rng.normal(0, SEX, int(n))
    y = MU0 + BETA * (T - 1.0) + q
    if POLE == "proceso":
        y = y + np.where(affected, fault, 0.0)
    return pd.DataFrame({{"unit_id": np.arange(int(n), dtype=float), "y": y}})
'''

NULL_PY = '''"""Anchor nulo: media plana del archivo, sin T ni estructura."""
import numpy as np
import pandas as pd

MU, SD = {mu!r}, 1.6


def model(regime, n, seed):
    rng = np.random.default_rng(np.random.SeedSequence([int(seed), 0xD2F]))
    return pd.DataFrame({{"unit_id": np.arange(int(n), dtype=float),
                          "y": MU + rng.normal(0, SD, int(n))}})
'''

LAZY_PY = '''"""EL ANCLA CERO (rung-0 pattern, ADR 0175): el mejor rival SIN el salto —
gaussiana momento-matcheada por T, coeficientes CONGELADOS en certificación."""
import numpy as np
import pandas as pd

CM = {cm!r}    # mu(T)      = CM[0] + CM[1]*(T-1) + CM[2]*(T-1)**2
CS = {cs!r}    # log sd(T)  = CS[0] + CS[1]*(T-1) + CS[2]*(T-1)**2


def model(regime, n, seed):
    config = getattr(regime, "config", None) or {{}}
    T = min(max(float(config.get("T", 1.0)), 0.6), 1.4)
    mu = CM[0] + CM[1] * (T - 1.0) + CM[2] * (T - 1.0) ** 2
    sd = min(max(float(np.exp(CS[0] + CS[1] * (T - 1.0) + CS[2] * (T - 1.0) ** 2)),
                 0.3), 6.0)
    rng = np.random.default_rng(seed)
    return pd.DataFrame({{"unit_id": np.arange(int(n), dtype=float),
                          "y": mu + rng.normal(0, sd, int(n))}})
'''


def frozen_lazy_coeffs(params: dict) -> tuple[list, list]:
    """Los coeficientes del ancla, calculados UNA vez y congelados (reproducible)."""
    truth = D2.pole_truth_program_d2("proceso", params)
    Ts = np.asarray(D2.EXAM_GRID, float)
    mus, sds = [], []
    for k, T in enumerate(Ts):
        y = np.asarray(truth(C._regime(T), 30000, 611 + k)["y"], float)
        mus.append(np.mean(y))
        sds.append(np.std(y))
    X = np.column_stack([np.ones_like(Ts), Ts - 1.0, (Ts - 1.0) ** 2])
    cm, *_ = np.linalg.lstsq(X, np.asarray(mus), rcond=None)
    cs, *_ = np.linalg.lstsq(X, np.log(np.asarray(sds)), rcond=None)
    return [float(v) for v in cm], [float(v) for v in cs]


def extra_gates(params: dict) -> dict:
    g: dict = {}
    # apareo byte-exacto con lotes pi(T): mismo stream, umbral por T
    C.refresh_cache(params)
    lots_hi = [D2.lot_d2(params, "new", i, 1.2) for i in range(60)]
    ra, rb = np.random.default_rng(3), np.random.default_rng(3)
    xs = [C.sensor_reading(l, "proceso", 1.2, ra) for l in lots_hi]
    ys = [C.sensor_reading(l, "instrumento", 1.2, rb) for l in lots_hi]
    g["apareo_exacto_piT"] = xs == ys
    # pi(T) efectivo en los lotes (sanity de la física)
    frac = np.mean([l["affected"] for l in
                    [D2.lot_d2(params, "new", i, 1.3) for i in range(4000)]])
    g["pi_efectivo_T13"] = float(frac)
    g["pi_T13_ok"] = abs(frac - D2.pi_T(1.3, params)) < 0.03
    return g


def meta_json(case_id: str, pole: str, params: dict) -> dict:
    op = ({"name": "lot_subpopulation_mixture_T", "layer": "mechanism",
           "knobs": {"mu0": params["mu0"], "beta": params["beta"],
                     "d_shift": params["d_shift"], "pi": params["pi"],
                     "pi_slope": params["pi_slope"]}, "ablation": {}}
          if pole == "proceso" else
          {"name": "clean_process_vial_fault_channel_T", "layer": "channel",
           "knobs": {"mu0": params["mu0"], "beta": params["beta"],
                     "d_shift": params["d_shift"], "pi": params["pi"],
                     "pi_slope": params["pi_slope"]}, "ablation": {}})
    return {
        "case_id": case_id, "suite": "d2_decision",
        "columns": [
            {"name": "unit_id", "dtype": "float", "unit": None,
             "description": "lot identifier within the returned batch (sequential)"},
            {"name": "y", "dtype": "float", "unit": "% purity",
             "description": "purity of the lot"}],
        "operators": [op],
        "stakes": {"narrative": ("Management is evaluating operating the line at higher "
                                 "temperature and will take operating decisions with this "
                                 "generative model; it must reflect the REAL process, at "
                                 "temperatures possibly not seen."),
                   "decision_variables": [], "context_relevance": {},
                   "decision_relevance": {}, "functionals": []},
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
                {"config": {"T": 0.8}, "context": {}, "horizon": None}],
            "control_surface": {
                "settable": {"T": {"low": 0.6, "high": 1.4,
                                   "description": "reactor temperature; your OWN runs are certified for T in [0.8, 1.2] — outside that band only production runs on its own calendar. The evaluation may use any value in the declared range."}},
                "context": {}, "instruments": {},
                "experiment_note": ("each experiment call produces n LOTS at your chosen T "
                                    "(certified band [0.8,1.2]), measured by the in-line "
                                    "spectrometer; cost = fixed + per measurement. Other verbs "
                                    "(see brief): env.measure(material, reps) re-measures lots, "
                                    "new vials ('revial:<lot_id>') or catalog items "
                                    "('estandar[:k]','solvente','blanco'); env.lab_extern([ids]) "
                                    "sends lots to the external lab (<=6, next turn); "
                                    "env.register_model(code) files your provisional model — "
                                    "the plant's calendar USES your latest filed model for its "
                                    "routine monitoring and scheduled operating decisions "
                                    "(resulting operating costs are debited)."),
                "deliverable_note": ("model(regime, n, seed) -> DataFrame with columns exactly "
                                     "[unit_id, y]; n counts LOTS; honor regime.config T. "
                                     "Model the PROCESS.")}},
        "prior_reliability": None,
    }


def battery_json() -> dict:
    grid = D2.EXAM_GRID
    w = round(1.0 / len(grid), 6)
    return {"items": [{"weight": w,
                       "regime": {"config": {"T": t}, "context": {}, "horizon": None},
                       "seed_world": 872000 + i} for i, t in enumerate(grid)]}


def main() -> int:
    base = C.load_instance()["params"]
    params = dict(base, **D2_CHOICE)

    print("=== compuertas de vara (design_d2_vara, física elegida) ===")
    vg = vara_gates(params)
    print(f"nats={vg['nats']:.3f} S_mid={vg['s_mid']:.2f} dDec13={vg['ddec_T13']:.3f} "
          f"-> {'PASS' if vg['pass'] else 'FAIL'}")
    eg = extra_gates(params)
    print(f"apareo byte-exacto pi(T): {eg['apareo_exacto_piT']} | "
          f"pi efectivo T=1.3: {eg['pi_efectivo_T13']:.3f} (ok={eg['pi_T13_ok']})")
    ok = vg["pass"] and eg["apareo_exacto_piT"] and eg["pi_T13_ok"]
    if not ok:
        print("CERTIFICACION D2: ROJA")
        return 1

    cm, cs = frozen_lazy_coeffs(params)
    print(f"ancla congelada: mu(T)={[round(v,4) for v in cm]} "
          f"log sd(T)={[round(v,4) for v in cs]}")

    for case_dir, pole, title, desc in (
        (PROC_DIR, "proceso", "PROCESO (A)",
         "La reaccion lateral degrada una fraccion de lotes que CRECE con T (pi(T)); el espectrometro esta sano."),
        (INST_DIR, "instrumento", "INSTRUMENTO (B)",
         "El proceso esta limpio a toda T; el autosampler falla por vial con la MISMA tasa pi(T): rutina byte-identica."),
    ):
        case_dir.mkdir(parents=True, exist_ok=True)
        (case_dir / "brief.md").write_text(BRIEF)
        (case_dir / "world.py").write_text(WORLD_PY.format(title=title, desc=desc, pole=pole))
        (case_dir / "truth_code.py").write_text(TRUTH_PY.format(
            mu0=params["mu0"], beta=params["beta"], sex=C.S_EXTRA,
            d_shift=params["d_shift"], pi=params["pi"], slope=params["pi_slope"],
            pole=pole))
        (case_dir / "meta.json").write_text(json.dumps(
            meta_json(case_dir.name, pole, params), indent=2, ensure_ascii=False))
        (case_dir / "battery.json").write_text(json.dumps(battery_json(), indent=2))
        ladder = case_dir / "ladder"
        ladder.mkdir(exist_ok=True)
        if pole == "proceso":
            (ladder / "rung_3_rival_vago_optimo.py").write_text(
                LAZY_PY.format(cm=cm, cs=cs))
        else:
            (ladder / "rung_3_mezcla_horneada.py").write_text(TRUTH_PY.format(
                mu0=params["mu0"], beta=params["beta"], sex=C.S_EXTRA,
                d_shift=params["d_shift"], pi=params["pi"], slope=params["pi_slope"],
                pole="proceso"))
        (ladder / "rung_4_null.py").write_text(NULL_PY.format(
            mu=params["mu0"] - params["pi"] * params["d_shift"]))
        (case_dir / "metrics.json").write_text(json.dumps({
            "metricas": [
                {"key": "S_log", "nombre": "Fraccion del valor del descubrimiento capturada",
                 "que_mide": "Log-score anclado: 0 = el mejor rival SIN el salto (congelado), 1 = la verdad del polo. En B: 0 = mezcla horneada, 1 = limpio correcto.",
                 "aplica": case_dir.name},
                {"key": "has_mixture", "nombre": "¿La entrega contiene mezcla?",
                 "que_mide": "Flag mecanico (masa baja + gap + asimetria <= -0.4). ENDPOINT PRIMARIO del experimento por brazo.",
                 "aplica": case_dir.name}],
            "outcome_secundario": "Y = 1[D_pre >= 0.25] * 1[S_log >= 0.5 y flag del polo]",
            "variante": {"rol": "principal" if pole == "proceso" else "gemelo",
                         "titulo": title}}, indent=2, ensure_ascii=False))
        (case_dir / "episode_protocol.json").write_text(json.dumps({
            "ficha": "docs/research/2026-08-11-ficha-mundo-d2-decision.md",
            "budget": BUDGET,
            "costos": {"archivo_por_fila": 0.5, "experiment_fijo": 40,
                       "experiment_por_medicion": 1, "measure_fijo": 15,
                       "measure_por_medicion": 1, "revial_prep_por_lote": 12,
                       "lab_fijo": 60, "lab_por_lote": 25, "lab_max_lotes": 6,
                       "lab_latencia_turnos": 1},
            "banda_certificada_T": list(D2.OPER_BAND),
            "calendario": {"aviso_calendario_turno": NOTICE_TURN,
                           "monitoreo_rutina_turno": MONITOR_TURN,
                           "monitoreo_n_lotes": 40,
                           "decision_turno": DECISION_TURN,
                           "piloto_T": PILOT_T, "piloto_n": PILOT_N,
                           "debito": {"escala": DEBIT_SCALE, "cap": DEBIT_CAP,
                                      "sin_modelo": NO_MODEL_DEBIT,
                                      "formula": "round(escala*|p_pred - p_real|), cap; p = P(y < L | T=1.3), L = mu0 - 2.0; p_real AUDITADO contra laboratorio externo (pureza verdadera) — el debito queda alineado con la verdad del polo en A y B (fix del dry-run 2026-08-11)"},
                           "max_turnos": MAX_TURNS,
                           "submit_gate": "entregas finales desde que corre el evento de decision (turno 8)",
                           "nota": "ambos brazos reciben las FILAS del piloto y el debito (dQ/dU fijas); el brazo REBOTE ademas recibe la confrontacion mecanica (p_pred vs p_real, tabla vs p05 del modelo) — solo V varia"},
            "brazos": ["SILENCIO", "REBOTE"],
            "outcome": {"endpoint_primario": "has_mixture (escribe estructura) por brazo x polo",
                        "D_pre": "igual que D1 (horquilla en el contexto del monitoreo T=1.0)",
                        "tau_bits": C.TAU,
                        "gate_secundario": "S_log >= 0.5 y flag del polo"},
            "seeds": {"instancia": params["world_seed"], "pistas_P2": [99700, 99701, 99702],
                      "tecnico": 99703, "tanda": "99704-99743"},
        }, indent=2, ensure_ascii=False))

    (PROC_DIR / "instance.json").write_text(json.dumps(
        {"case_id": "d2_decision", "frozen_at": "2026-08-11",
         "params": params, "ancla_cm": cm, "ancla_cs": cs}, indent=2))
    assert (PROC_DIR / "brief.md").read_bytes() == (INST_DIR / "brief.md").read_bytes()

    for d in (PROC_DIR, INST_DIR):
        (d / "certificates.json").write_text(json.dumps(
            {"ficha": "docs/research/2026-08-11-ficha-mundo-d2-decision.md",
             "vara": {k: (round(v, 4) if isinstance(v, float) else v)
                      for k, v in vg.items()},
             "extra": {k: (round(v, 4) if isinstance(v, float) else v)
                       for k, v in eg.items()},
             "all_pass": True}, indent=2, default=str))
    print("\nCERTIFICACION D2: VERDE (artefactos escritos; briefs byte-identicos)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
