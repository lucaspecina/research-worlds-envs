"""Build + certify the count_regime_v1 IMPASSE pair (ficha 2026-08-09 + addendum ratificado).

One pass, all zero-LLM:
  1. verify the FROZEN instance (cases/count_regime_v1/instance.json, seed 99457)
     still passes every scan gate (no silent drift)
  2. write both case dirs (world/brief/truth_code/meta/ladder/battery/metrics
     + episode_protocol.json, the server-side protocol the runner reads)
  3. robots through the REAL WorldServer + directional R check
  4. certificates.json per pole -> VERDE o ROJA (ROJA = NO-GO al host, regla de Codex)

Run: .venv/bin/python scripts/build_certify_count_regime_v1.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))

from cases import count_regime_v1_common as C  # noqa: E402
from scan_count_regime_v1 import evaluate_seed  # noqa: E402
from wager.harness.case_episode import build_world_server  # noqa: E402

BRK_DIR = ROOT / "cases" / "count_regime_v1"
TWIN_DIR = ROOT / "cases" / "count_regime_twin_v1"
BATTERY_SEED_BASE = 99513          # ficha: bateria 99513-99519
ROBOT_SEED_BASE = 99560            # libres de la familia tras las asignaciones de ficha

TRUTH_BRK = '''"""Self-contained truth program (sandbox-safe; frozen from instance.json).
Server-side artifact: the scorer runs THIS through the sandbox as S_truth."""
import numpy as np
import pandas as pd

LAM0, ALPHA, SSTAR, D1 = {lam0!r}, {alpha!r}, {s_star!r}, {delta1!r}


def model(regime, n, seed):
    config = regime.config or {{}}
    speed = float(config.get("speed", 1.0))
    speed = min(max(speed, 0.8), 1.4)
    lam = LAM0 * speed ** ALPHA + D1 * max(0.0, speed - SSTAR)
    rng = np.random.default_rng(np.random.SeedSequence([int(seed), 0x5631]))
    y = rng.poisson(lam, int(n)).astype(float)
    return pd.DataFrame({{"unit_id": np.arange(int(n), dtype=float), "y": y}})
'''

TRUTH_TWIN = '''"""Self-contained truth program (sandbox-safe; frozen from instance.json).
Server-side artifact: the scorer runs THIS through the sandbox as S_truth."""
import numpy as np
import pandas as pd

CC, BETA = {c!r}, {beta!r}


def model(regime, n, seed):
    config = regime.config or {{}}
    speed = float(config.get("speed", 1.0))
    speed = min(max(speed, 0.8), 1.4)
    lam = CC * speed ** BETA
    rng = np.random.default_rng(np.random.SeedSequence([int(seed), 0x5631]))
    y = rng.poisson(lam, int(n)).astype(float)
    return pd.DataFrame({{"unit_id": np.arange(int(n), dtype=float), "y": y}})
'''

SMOOTH_CODE = '''import numpy as np
import pandas as pd
COEFFS = {coeffs!r}


def model(regime, n, seed):
    config = regime.config or {{}}
    speed = float(config.get("speed", 1.0))
    speed = min(max(speed, 0.8), 1.4)
    lam = float(np.exp(np.polyval(np.asarray(COEFFS), np.log(speed))))
    rng = np.random.default_rng(np.random.SeedSequence([int(seed), 2]))
    y = rng.poisson(lam, int(n)).astype(float)
    return pd.DataFrame({{"unit_id": np.arange(int(n), dtype=float), "y": y}})
'''

NULL_CODE = '''import numpy as np
import pandas as pd
LAM = {lam!r}


def model(regime, n, seed):
    rng = np.random.default_rng(np.random.SeedSequence([int(seed), 3]))
    y = rng.poisson(LAM, int(n)).astype(float)
    return pd.DataFrame({{"unit_id": np.arange(int(n), dtype=float), "y": y}})
'''

FORCED_CODE = '''import numpy as np
import pandas as pd
CC, BETA, D0, AT = {c!r}, {beta!r}, {d0!r}, {at!r}


def model(regime, n, seed):
    config = regime.config or {{}}
    speed = float(config.get("speed", 1.0))
    speed = min(max(speed, 0.8), 1.4)
    lam = CC * speed ** BETA + (D0 if speed >= AT else 0.0)
    rng = np.random.default_rng(np.random.SeedSequence([int(seed), 4]))
    y = rng.poisson(lam, int(n)).astype(float)
    return pd.DataFrame({{"unit_id": np.arange(int(n), dtype=float), "y": y}})
'''


def meta_json(case_id: str, pole: str, params: dict) -> dict:
    if pole == "brk":
        op = {"name": "latent_regime_slope_break", "layer": "mechanism",
              "knobs": {k: params[k] for k in ("lam0", "alpha", "s_star", "delta1")},
              "ablation": {}}
    else:
        op = {"name": "smooth_power_law", "layer": "mechanism",
              "knobs": C.twin_coeffs(params), "ablation": {}}
    return {
        "case_id": case_id,
        "suite": "count_regime_impasse",
        "columns": [
            {"name": "unit_id", "dtype": "float", "unit": None,
             "description": "lot identifier within the returned batch (sequential)"},
            {"name": "y", "dtype": "int", "unit": "defects",
             "description": "defect count of the lot"},
        ],
        "operators": [op],
        "stakes": {
            "narrative": ("The plant has run inside its historical envelope; management is "
                          "evaluating operating ABOVE it and will decide with this generative "
                          "defect model. It must hold across the whole declared range, "
                          "including speeds the line never ran."),
            "decision_variables": [], "context_relevance": {},
            "decision_relevance": {}, "functionals": [],
        },
        "scoring": {"lambda_mdl": 0.0, "lambda_provisional": True,
                    "n_samples": 400, "m_reps": 2, "model_call_timeout_s": 10.0},
        "episode": {
            "budget": 1000.0,
            "observe_sources": {"archivo": {"cost_per_row": 0.5, "config": {},
                                            "context": {}, "max_rows": 400}},
            "experiment": {"cost_fixed": 40.0, "cost_per_row": 1.0, "cost_per_horizon": 0.0},
            "experiment_meter": None, "events": [], "submit_requires_all_events": False,
            "register": None,
            "smoke_regimes": [
                {"config": {}, "context": {}, "horizon": None},
                {"config": {"speed": 1.3}, "context": {}, "horizon": None},
                {"config": {"speed": 0.9}, "context": {}, "horizon": None},
            ],
            "control_surface": {
                "settable": {"speed": {"low": 0.8, "high": 1.4,
                                       "description": "line speed of the runs you launch. The line is CERTIFIED up to 1.2: your own runs may not exceed it unless plant engineering authorizes it during the evaluation (premium per-row cost). The evaluation itself may use any value in the declared range."}},
                "context": {}, "instruments": {},
                "experiment_note": "each experiment call produces n LOTS at your chosen speed; cost = fixed + per ROW. Runs above the certified limit 1.2 are unavailable until plant engineering authorizes them (then premium per-row).",
                "deliverable_note": "model(regime, n, seed) -> DataFrame with columns exactly [unit_id, y]; n counts LOTS (one measurement per lot, unit_id sequential); honor regime.config speed. Model the PROCESS.",
            },
        },
        "prior_reliability": None,
    }


def battery_json(params: dict) -> dict:
    speeds = list(C.exam_grid(params))
    w = round(1.0 / len(speeds), 6)
    items = [{"weight": w, "regime": {"config": {"speed": s}, "context": {}, "horizon": None},
              "seed_world": BATTERY_SEED_BASE + i} for i, s in enumerate(speeds)]
    return {"items": items}


def metrics_json(pole: str) -> dict:
    metricas = [
        {"key": "S_quiebre_fuerte", "nombre": "Captura del cambio de ley (vara del salto)",
         "que_mide": "Qué fracción de la firma que SOLO un modelo con dos leyes puede producir (el cambio de pendiente arriba del rango histórico) capturó la entrega.",
         "anclas": "0 = igual a la mejor curva suave posible · 1 = igual a la verdad",
         "aplica": "count_regime_v1"},
        {"key": "S_clean", "nombre": "Limpieza (en el gemelo)",
         "que_mide": "Si entregó la curva suave correcta donde NO hay cambio de ley.",
         "anclas": "1 = curva suave correcta · 0 = inventó un quiebre grande",
         "aplica": "count_regime_twin_v1"},
        {"key": "F_mean", "nombre": "Nivel capturado",
         "que_mide": "Qué tan bien clavó el promedio de defectos a velocidad 1.0.",
         "anclas": "1 = promedio exacto · 0 = errado en el 100%",
         "aplica": "count_regime_v1"},
        {"key": "espurio", "nombre": "¿Inventó un quiebre falso?",
         "que_mide": "Si la entrega en el gemelo contiene un quiebre sustantivo donde el mundo es suave.",
         "anclas": "SÍ = fantaseó estructura · no = correcto", "aplica": "count_regime_twin_v1"},
    ]
    funcionales = {
        "mean": "promedio de defectos por lote a velocidad 1.0",
        "lam_090": "tasa a velocidad 0.90 (zona histórica baja)",
        "lam_118": "tasa a velocidad 1.18 (tope histórico)",
        "lam_126": "tasa a 1.26 (banda de decisión, pasado el umbral oculto)",
        "lam_140": "tasa a 1.40 (extremo de la banda de decisión)",
    }
    variante = ({"titulo": "Mundo principal — la ley CAMBIA arriba del rango histórico",
                 "rol": "principal",
                 "descripcion": "Dentro del rango histórico la tasa sigue una ley suave; apenas arriba del tope histórico se activa un modo nuevo de defectos (la pendiente cambia, sin salto de nivel). Descubrir que son DOS LEYES — con la evidencia llegando por los pilotos de producción — es el desafío. El agente no sabe que está acá."}
                if pole == "brk" else
                {"titulo": "Mundo control — UNA sola ley en todo el rango (gemelo)",
                 "rol": "control",
                 "descripcion": "La tasa sigue una única ley suave hasta 1.4. Indistinguible del principal en TODO lo comprable dentro del rango histórico. Castiga inventar regímenes que no existen. Mismo encargo, mismos costos, mismos pilotos."})
    return {"metricas": metricas, "funcionales": funcionales,
            "R": "Nota estándar del examen (0 a 1) sobre la grilla que incluye la banda de decisión: el cambio de ley afecta la media arriba del rango histórico, así que R lo cobra (chequeo direccional certificado).",
            "variante": variante}


def episode_protocol(params: dict) -> dict:
    """Server-side protocol for the IMPASSE episode (the runner reads this; the
    agent NEVER sees it). Frozen per ficha + addendum ratificado."""
    return {
        "ficha": "docs/research/2026-08-09-ficha-mundo-count-regime-v1-impasse.md",
        "chain": ["M0", "control_1", "Mpatch", "control_2_vs_Mpatch", "M1", "submit"],
        "register_note": ("brief exposes register(code); production runs the FIXED control "
                          "lots against the LAST registered model and returns prediction vs "
                          "raw outcome per the arm's format. If nothing new is registered, "
                          "Mpatch = M0 (addendum B)."),
        "controls": [
            {"name": "control_1", "speed": C.CONTROL_1["speed"], "n": C.CONTROL_1["n"],
             "seed": C.WITNESS_SAMPLE_SEED + 100},
            {"name": "control_2", "speed": C.CONTROL_2["speed"], "n": C.CONTROL_2["n"],
             "seed": C.WITNESS_SAMPLE_SEED + 200},
        ],
        "controls_fixed_note": "identical lots (speed, n, seed) across arms and poles; never adaptive",
        "arms": {
            "RAW": {"payload": ["rows"],
                    "desc": "las filas crudas del lote piloto, nada mas"},
            "VISIBLE_GLOBAL": {"payload": ["rows", "global_fit_stat"],
                               "desc": "filas + un estadistico GLOBAL de desajuste del modelo registrado (deviance total y su umbral chi2), sin detalle por punto"},
            "VISIBLE_ESTRUCTURADO": {"payload": ["rows", "global_fit_stat", "residual_table"],
                                     "desc": "filas + global + residuos deviance FIRMADOS por celda de velocidad, EN ORDEN DE VELOCIDAD, sin ranking, sin colores, sin etiquetas de patron, sin interpretacion (compuerta C)"},
        },
        "outcomes": {
            "primary": "expansion generativa BINARIA: candidata de familia estructural nueva registrada ANTES del punto de discriminacion (dBIC>=6 sostenido)",
            "secondary_ordinal": ["monster_bar", "tweak", "specialize", "split", "delete", "add_family"],
            "exits": ["perseverar", "rerank_misma_familia", "familia_nueva_correcta",
                      "familia_nueva_incorrecta", "abandono"],
        },
        "persistence_budget": {"turns_after_control_1": 8,
                               "note": "igual entre brazos; se registra cuanto usa (addendum E)"},
        "eligibility_gate": ("compuerta A (elegibilidad unwarranted) por modelo, en sesion "
                             "aparte, ANTES de contar sus nulos: implementa la familia si se "
                             "la nombra + la reconoce en dominio isomorfo entre >=3 rivales"),
    }


def write_artifacts(params: dict) -> None:
    tw = C.twin_coeffs(params)
    brief = (BRK_DIR / "brief.md").read_text()

    for case_dir, pole, truth in (
        (BRK_DIR, "brk", TRUTH_BRK.format(**{k: params[k] for k in ("lam0", "alpha", "s_star", "delta1")})),
        (TWIN_DIR, "smooth", TRUTH_TWIN.format(c=tw["c"], beta=tw["beta"])),
    ):
        (case_dir / "ladder").mkdir(parents=True, exist_ok=True)
        (case_dir / "brief.md").write_text(brief)      # byte-identical by construction
        (case_dir / "truth_code.py").write_text(truth)
        (case_dir / "meta.json").write_text(json.dumps(
            meta_json(case_dir.name, pole, params), indent=2, ensure_ascii=False))
        (case_dir / "battery.json").write_text(json.dumps(battery_json(params), indent=2))
        (case_dir / "metrics.json").write_text(json.dumps(
            metrics_json(pole), indent=2, ensure_ascii=False))
        (case_dir / "episode_protocol.json").write_text(json.dumps(
            episode_protocol(params), indent=2, ensure_ascii=False))

    cf = C.smooth_rival_coeffs(params)
    (BRK_DIR / "ladder" / "rung_3_smooth_rival.py").write_text(
        SMOOTH_CODE.format(coeffs=[float(v) for v in cf["coeffs"]]))
    null_lam = float(np.mean(C.lam_truth(params, np.asarray(C.DENSE_GRID))))
    (BRK_DIR / "ladder" / "rung_4_null.py").write_text(NULL_CODE.format(lam=null_lam))
    (TWIN_DIR / "ladder" / "rung_3_forced_break.py").write_text(
        FORCED_CODE.format(c=tw["c"], beta=tw["beta"],
                           d0=C.FORCED_BREAK_DELTA, at=C.FORCED_BREAK_AT))
    null_twin = float(np.mean(C.lam_twin(params, np.asarray(C.DENSE_GRID))))
    (TWIN_DIR / "ladder" / "rung_4_null.py").write_text(NULL_CODE.format(lam=null_twin))
    print("artifacts written for both poles (brief re-written byte-identical)")


def _exec_model(code: str):
    ns: dict = {}
    exec(compile(code, "<delivery>", "exec"), ns)
    return ns["model"]


def run_robots(params: dict) -> dict:
    cf = C.smooth_rival_coeffs(params)
    tw = C.twin_coeffs(params)
    null_lam = float(np.mean(C.lam_truth(params, np.asarray(C.DENSE_GRID))))
    deliveries = {
        "brk": {
            "oracle_regime": TRUTH_BRK.format(**{k: params[k] for k in ("lam0", "alpha", "s_star", "delta1")}),
            "suave_generosa": SMOOTH_CODE.format(coeffs=[float(v) for v in cf["coeffs"]]),
            "null_plano": NULL_CODE.format(lam=null_lam),
        },
        "smooth": {
            "oracle_suave": TRUTH_TWIN.format(c=tw["c"], beta=tw["beta"]),
            "suave_generosa": SMOOTH_CODE.format(coeffs=[float(v) for v in cf["coeffs"]]),
            "quiebre_forzado": FORCED_CODE.format(c=tw["c"], beta=tw["beta"],
                                                  d0=C.FORCED_BREAK_DELTA, at=C.FORCED_BREAK_AT),
        },
    }
    dirs = {"brk": BRK_DIR, "smooth": TWIN_DIR}
    out: dict = {}
    seed = ROBOT_SEED_BASE
    for pole, robots in deliveries.items():
        out[pole] = {}
        for name, code in robots.items():
            srv = build_world_server(dirs[pole], seed_offset=seed)
            seed += 1
            srv.observe("archivo", 50)
            res = srv.submit(code)
            prog = _exec_model(code)
            r_val = float((srv.result or {}).get("R") or 0.0)
            row = {"accepted": bool(res.accepted), "R": r_val}
            if pole == "brk":
                row.update(C.s_quiebre(prog, params))
                row["F_mean"] = C.f_mean(prog, params, "brk")
            else:
                row.update(C.s_clean(prog, params))
                row["espurio"] = C.spurious_break_flag(prog, params)
            out[pole][name] = row
            extra = (f"S_quiebre={row.get('S_quiebre_fuerte', 0):.3f}" if pole == "brk"
                     else f"S_clean={row.get('S_clean', 0):.3f} espurio={row['espurio']['spurious']}")
            print(f"[{pole}] {name}: accepted={row['accepted']} R={row['R']:.3f} {extra}")
    return out


def main() -> int:
    inst = json.loads((BRK_DIR / "instance.json").read_text())
    params = inst["params"]
    print(f"=== re-verificacion de la instancia congelada (seed {params['world_seed']}) ===")
    res = evaluate_seed(params["world_seed"])
    for g, ok in res["gates"].items():
        print(f"  {g}: {'PASS' if ok else 'FAIL'}")
    if not res["PASS"]:
        print("\nLA INSTANCIA CONGELADA YA NO PASA -> NO-GO (no se escriben artefactos)")
        return 1

    write_artifacts(params)

    print("\n=== robots por el server real ===")
    robots = run_robots(params)

    r_gap = robots["brk"]["oracle_regime"]["R"] - robots["brk"]["suave_generosa"]["R"]
    checks = {
        "oracle_s_high": robots["brk"]["oracle_regime"]["S_quiebre_fuerte"] >= 0.9,
        "smooth_s_low": robots["brk"]["suave_generosa"]["S_quiebre_fuerte"] <= 0.1,
        "twin_oracle_clean": robots["smooth"]["oracle_suave"]["S_clean"] >= 0.9,
        "twin_oracle_no_espurio": not robots["smooth"]["oracle_suave"]["espurio"]["spurious"],
        "twin_forced_espurio": robots["smooth"]["quiebre_forzado"]["espurio"]["spurious"],
        "twin_forced_dirty": robots["smooth"]["quiebre_forzado"]["S_clean"] <= 0.2,
        "r_directional": r_gap >= 0.03,
        "all_accepted": all(r["accepted"] for pole in robots.values() for r in pole.values()),
    }
    print(f"\nR directional gap (oracle - suave, brk): {r_gap:+.3f}")
    all_pass = all(checks.values()) and res["PASS"]
    for case_dir in (BRK_DIR, TWIN_DIR):
        (case_dir / "certificates.json").write_text(json.dumps(
            {"ficha": "docs/research/2026-08-09-ficha-mundo-count-regime-v1-impasse.md",
             "scan_gates": res["gates"],
             "scan_evidence": {k: res[k] for k in
                               ("max_abs_z_prefix", "z_control1", "min_abs_z_patch",
                                "dbic_gap_after_control1", "dbic_gap_after_zoom",
                                "D_rival", "twin_pairing")},
             "robot_checks": checks, "robots": robots, "r_directional_gap": r_gap,
             "all_pass": bool(all_pass)}, indent=2, default=str))
    print("\n=== checks ===")
    for k, v in checks.items():
        print(f"  {k}: {'PASS' if v else 'FAIL'}")
    print(f"\nCERTIFICACION: {'VERDE' if all_pass else 'ROJA (NO-GO al host)'}")
    return 0 if all_pass else 1


if __name__ == "__main__":
    raise SystemExit(main())
