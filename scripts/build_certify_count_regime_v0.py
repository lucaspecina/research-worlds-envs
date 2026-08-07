"""Build + certify the count_regime pair (mundo 2, ficha 2026-08-07).

One pass, all zero-LLM:
  1. scan WORLD_SEEDS, freeze the first instance passing ALL ficha gates
  2. write both case dirs (world/brief/truth_code/meta/ladder/battery/metrics)
  3. re-run the gates on the frozen instance -> gates report
  4. robots through the REAL WorldServer (G2/G5) + directional R check
  5. certificates.json per pole

Run: .venv/bin/python scripts/build_certify_count_regime_v0.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from cases.count_regime_v0_common import (  # noqa: E402
    DENSE_GRID, NECESSITY_D_RIVAL_MIN, TWIN_PAIRING_TOL, WITNESS_DBIC_BRK,
    WITNESS_DBIC_SMOOTH, WORLD_SEEDS, buyable_design, curve_distance,
    exam_grid, f_mean, forced_break_program, lam_smooth_rival, lam_truth,
    lam_twin, params_from_seed, s_clean, s_quiebre, smooth_rival_coeffs,
    smooth_rival_program, spurious_break_flag, twin_coeffs, witness,
)
from wager.harness.case_episode import build_world_server  # noqa: E402

BRK_DIR = ROOT / "cases" / "count_regime_v0"
TWIN_DIR = ROOT / "cases" / "count_regime_twin_v0"
BATTERY_SEED_BASE = 99460
ROBOT_SEED_BASE = 99470

BRIEF = """# Encargo — asesoría de calidad de línea

Sos el analista de calidad de una línea de proceso que produce LOTES. Cada
lote registra su cantidad de DEFECTOS (`y`, entero >= 0). La gerencia está
evaluando SUBIR la velocidad de la línea y va a tomar esa decisión con tu
modelo: necesita un modelo generativo de defectos que reproduzca el proceso
en TODO el rango de velocidades declarado.

## Qué entregás

`model(regime, n, seed) -> DataFrame` con columnas exactas `[unit_id, y]`:
`n` cuenta LOTES (una medición por lote; `unit_id` correlativo desde 0). Tu
modelo debe reproducir el PROCESO bajo cualquier `speed` dentro del rango
declarado — se lo evaluará en condiciones que podés no haber visto.

## Perillas del experimento (`regime.config`)

- `speed` en [0.8, 1.2]: velocidad de línea (afecta la tasa de defectos).

## Acciones y costos

- `observe("archivo", n)`: filas históricas (speed=1.0), baratas, tope de archivo.
- `experiment(design)`: corridas nuevas a la velocidad que elijas (costo fijo
  + por fila). Elegís `speed` en cada corrida.
- `submit(code)`: entrega tu modelo. El presupuesto es finito y no se reembolsa.

## Cómo se evalúa

No hay respuestas de texto: tu entrega es el modelo ejecutable. El servidor
genera datos con tu modelo y con el proceso real bajo las mismas condiciones
— incluidas algunas que podés no haber visto — y mide qué tan parecidos son
los datos que producen uno y otro. El objetivo es un sustituto fiel del
sistema: idealmente, los datos generados por tu modelo no deberían poder
distinguirse de los del proceso real.
"""

WORLD_PY = '''"""{title} pole of the count-regime jump pair (mundo 2 de saltos).

Server-side truth -- the agent never sees this file. {desc}
Physics shared via cases/count_regime_v0_common.py; the level is paired
across poles on the exam grid by construction.
"""

from cases.count_regime_v0_common import pole_sample

POLE = "{pole}"


def sample(regime, n, seed):
    return pole_sample(POLE, regime, n, seed)


model = sample
'''

TRUTH_BRK = '''"""Self-contained truth program (sandbox-safe; frozen from instance.json).
Server-side artifact: the scorer runs THIS through the sandbox as S_truth."""
import numpy as np
import pandas as pd

LAM0, ALPHA, SSTAR, D0, D1 = {lam0!r}, {alpha!r}, {s_star!r}, {delta0!r}, {delta1!r}


def model(regime, n, seed):
    config = regime.config or {{}}
    speed = float(config.get("speed", 1.0))
    speed = min(max(speed, 0.8), 1.2)
    lam = LAM0 * speed ** ALPHA
    if speed >= SSTAR:
        lam += D0 + D1 * (speed - SSTAR)
    rng = np.random.default_rng(np.random.SeedSequence([int(seed), 0x4E61]))
    y = rng.poisson(lam, int(n)).astype(float)
    return pd.DataFrame({{"unit_id": np.arange(int(n), dtype=float), "y": y}})
'''

TRUTH_TWIN = '''"""Self-contained truth program (sandbox-safe; frozen from instance.json).
Server-side artifact: the scorer runs THIS through the sandbox as S_truth."""
import numpy as np
import pandas as pd

C, BETA = {c!r}, {beta!r}


def model(regime, n, seed):
    config = regime.config or {{}}
    speed = float(config.get("speed", 1.0))
    speed = min(max(speed, 0.8), 1.2)
    lam = C * speed ** BETA
    rng = np.random.default_rng(np.random.SeedSequence([int(seed), 0x4E61]))
    y = rng.poisson(lam, int(n)).astype(float)
    return pd.DataFrame({{"unit_id": np.arange(int(n), dtype=float), "y": y}})
'''

SMOOTH_CODE = '''import numpy as np
import pandas as pd
C0, C1, C2 = {c0!r}, {c1!r}, {c2!r}


def model(regime, n, seed):
    config = regime.config or {{}}
    speed = float(config.get("speed", 1.0))
    speed = min(max(speed, 0.8), 1.2)
    x = np.log(speed)
    lam = float(np.exp(C0 + C1 * x + C2 * x * x))
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
C, BETA, D0, AT = {c!r}, {beta!r}, 4.0, 1.10


def model(regime, n, seed):
    config = regime.config or {{}}
    speed = float(config.get("speed", 1.0))
    speed = min(max(speed, 0.8), 1.2)
    lam = C * speed ** BETA
    if speed >= AT:
        lam += D0
    rng = np.random.default_rng(np.random.SeedSequence([int(seed), 4]))
    y = rng.poisson(lam, int(n)).astype(float)
    return pd.DataFrame({{"unit_id": np.arange(int(n), dtype=float), "y": y}})
'''


def check_gates(params: dict) -> dict:
    grid = np.asarray(exam_grid(params), float)
    d_rival = curve_distance(lam_smooth_rival(params, grid), lam_truth(params, grid))
    wit_brk = witness(buyable_design("brk", params))
    wit_twin = witness(buyable_design("smooth", params))
    pairing = abs(float(np.mean(lam_twin(params, grid))) - float(np.mean(lam_truth(params, grid))))
    gates = {
        "g1_invisible_archivo": params["s_star"] > 1.0,
        "g2_necesidad_d_rival": d_rival,
        "g2_pass": d_rival >= NECESSITY_D_RIVAL_MIN,
        "g3_dbic_brk": wit_brk["dbic_pw_vs_smooth"],
        "g3_pass": wit_brk["selected"] == "piecewise"
                   and wit_brk["dbic_pw_vs_smooth"] >= WITNESS_DBIC_BRK,
        "g4_dbic_twin": wit_twin["dbic_pw_vs_smooth"],
        "g4_smooth_pass": wit_twin["selected"] == "smooth"
                          and -wit_twin["dbic_pw_vs_smooth"] >= WITNESS_DBIC_SMOOTH,
        "g4_pairing": pairing,
        "g4_pairing_pass": pairing <= TWIN_PAIRING_TOL,
        "witness_brk": wit_brk, "witness_twin": wit_twin,
    }
    gates["all_pass"] = all(gates[k] for k in
                            ("g1_invisible_archivo", "g2_pass", "g3_pass",
                             "g4_smooth_pass", "g4_pairing_pass"))
    return gates


def find_instance() -> tuple[dict, dict]:
    for seed in WORLD_SEEDS:
        params = params_from_seed(seed)
        gates = check_gates(params)
        status = "PASS" if gates["all_pass"] else "fail"
        print(f"seed {seed}: s*={params['s_star']:.3f} d_rival={gates['g2_necesidad_d_rival']:.2f} "
              f"dbic_brk={gates['g3_dbic_brk']:.1f} dbic_twin={gates['g4_dbic_twin']:.1f} "
              f"pair={gates['g4_pairing']:.3f} -> {status}")
        if gates["all_pass"]:
            return params, gates
    raise RuntimeError("no instance passed the ficha gates in WORLD_SEEDS")


def meta_json(case_id: str, pole: str, params: dict) -> dict:
    if pole == "brk":
        op = {"name": "latent_regime_break", "layer": "mechanism",
              "knobs": {k: params[k] for k in ("lam0", "alpha", "s_star", "delta0", "delta1")},
              "ablation": {}}
    else:
        op = {"name": "smooth_power_law", "layer": "mechanism",
              "knobs": twin_coeffs(params), "ablation": {}}
    return {
        "case_id": case_id,
        "suite": "count_regime_jump",
        "columns": [
            {"name": "unit_id", "dtype": "float", "unit": None,
             "description": "lot identifier within the returned batch (sequential)"},
            {"name": "y", "dtype": "int", "unit": "defects",
             "description": "defect count of the lot"},
        ],
        "operators": [op],
        "stakes": {
            "narrative": ("Management is evaluating a LINE SPEED INCREASE and will decide "
                          "with this generative defect model; it must hold across the whole "
                          "declared speed range, including speeds not present in history."),
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
                {"config": {"speed": 1.15}, "context": {}, "horizon": None},
                {"config": {"speed": 0.9}, "context": {}, "horizon": None},
            ],
            "control_surface": {
                "settable": {"speed": {"low": 0.8, "high": 1.2,
                                       "description": "line speed of the runs you launch; the evaluation may use any value in range"}},
                "context": {}, "instruments": {},
                "experiment_note": "each experiment call produces n LOTS at your chosen speed; cost = fixed + per ROW",
                "deliverable_note": "model(regime, n, seed) -> DataFrame with columns exactly [unit_id, y]; n counts LOTS (one measurement per lot, unit_id sequential); honor regime.config speed. Model the PROCESS.",
            },
        },
        "prior_reliability": None,
    }


def battery_json(params: dict) -> dict:
    speeds = [0.85, 0.95, 1.0, 1.05, 1.10, round(params["s_star"] + 0.01, 4), 1.18]
    w = round(1.0 / len(speeds), 6)
    items = [{"weight": w, "regime": {"config": {"speed": s}, "context": {}, "horizon": None},
              "seed_world": BATTERY_SEED_BASE + i} for i, s in enumerate(speeds)]
    return {"items": items}


def metrics_json(pole: str) -> dict:
    metricas = [
        {"key": "S_quiebre_fuerte", "nombre": "Captura del quiebre (vara del salto)",
         "que_mide": "Qué fracción de la firma que SOLO un modelo con dos leyes puede producir (el escalón en la curva defectos-vs-velocidad) capturó la entrega.",
         "anclas": "0 = igual a la mejor curva suave posible · 1 = igual a la verdad",
         "aplica": "count_regime_v0"},
        {"key": "S_clean", "nombre": "Limpieza (en el gemelo)",
         "que_mide": "Si entregó la curva suave correcta donde NO hay quiebre.",
         "anclas": "1 = curva suave correcta · 0 = inventó un escalón grande",
         "aplica": "count_regime_twin_v0"},
        {"key": "F_mean", "nombre": "Nivel capturado",
         "que_mide": "Qué tan bien clavó el promedio de defectos a velocidad 1.0.",
         "anclas": "1 = promedio exacto · 0 = errado en el 100%",
         "aplica": "count_regime_v0"},
        {"key": "espurio", "nombre": "¿Inventó un quiebre falso?",
         "que_mide": "Si la entrega en el gemelo contiene un escalón sustantivo donde el mundo es suave.",
         "anclas": "SÍ = fantaseó estructura · no = correcto", "aplica": "count_regime_twin_v0"},
    ]
    funcionales = {
        "mean": "promedio de defectos por lote a velocidad 1.0",
        "lam_085": "tasa a velocidad 0.85 (zona baja)",
        "lam_pre": "tasa justo ANTES del punto donde la verdad cambia de ley",
        "lam_post": "tasa justo DESPUÉS de ese punto",
        "lam_118": "tasa a velocidad 1.18 (zona alta)",
        "jump": "salto de nivel implícito entre pre y post (verdad ≈ delta0; suave ≈ 0)",
    }
    variante = ({"titulo": "Mundo principal — CON quiebre de ley oculto", "rol": "principal",
                 "descripcion": "La tasa de defectos sigue una ley suave hasta una velocidad oculta y salta a otra ley de ahí en más. Descubrir que son DOS LEYES es el desafío. El agente no sabe que está acá."}
                if pole == "brk" else
                {"titulo": "Mundo control — SIN quiebre (gemelo)", "rol": "control",
                 "descripcion": "La tasa sigue UNA sola ley suave en todo el rango. Castiga inventar quiebres que no existen. Mismo encargo, mismos costos."})
    return {"metricas": metricas, "funcionales": funcionales,
            "R": "Nota estándar del examen (0 a 1): el servidor genera datos con la entrega y con el proceso real bajo varias velocidades y mide qué tan parecidas son las pilas. En ESTE mundo el quiebre afecta la media a velocidades altas, así que R también lo cobra (chequeo direccional certificado).",
            "variante": variante}


def write_artifacts(params: dict) -> None:
    tw = twin_coeffs(params)
    for case_dir, pole, title, desc, truth in (
        (BRK_DIR, "brk", "BRK",
         "The defect rate follows law A below a hidden speed s* and law B (level+slope break) above it.",
         TRUTH_BRK.format(**params)),
        (TWIN_DIR, "smooth", "SMOOTH (twin)",
         "One smooth power law across the whole range; level-paired to the BRK pole.",
         TRUTH_TWIN.format(c=tw["c"], beta=tw["beta"])),
    ):
        (case_dir / "ladder").mkdir(parents=True, exist_ok=True)
        (case_dir / "world.py").write_text(WORLD_PY.format(title=title, desc=desc, pole=pole))
        (case_dir / "brief.md").write_text(BRIEF)
        (case_dir / "truth_code.py").write_text(truth)
        (case_dir / "meta.json").write_text(json.dumps(
            meta_json(case_dir.name, pole, params), indent=2, ensure_ascii=False))
        (case_dir / "battery.json").write_text(json.dumps(battery_json(params), indent=2))
        (case_dir / "metrics.json").write_text(json.dumps(
            metrics_json(pole), indent=2, ensure_ascii=False))

    cf = smooth_rival_coeffs(params)
    smooth_rung = SMOOTH_CODE.format(**cf)
    null_lam = float(np.mean(lam_truth(params, np.asarray(DENSE_GRID))))
    null_rung = NULL_CODE.format(lam=null_lam)
    (BRK_DIR / "ladder" / "rung_3_smooth_rival.py").write_text(smooth_rung)
    (BRK_DIR / "ladder" / "rung_4_null.py").write_text(null_rung)
    forced_rung = FORCED_CODE.format(c=tw["c"], beta=tw["beta"])
    null_twin = NULL_CODE.format(lam=float(np.mean(lam_twin(params, np.asarray(DENSE_GRID)))))
    (TWIN_DIR / "ladder" / "rung_3_forced_break.py").write_text(forced_rung)
    (TWIN_DIR / "ladder" / "rung_4_null.py").write_text(null_twin)

    (BRK_DIR / "instance.json").write_text(json.dumps(
        {"params": params, "twin": tw, "smooth_rival": cf,
         "exam_grid": list(exam_grid(params))}, indent=2))
    print("artifacts written for both poles")


def _exec_model(code: str):
    ns: dict = {}
    exec(compile(code, "<delivery>", "exec"), ns)
    return ns["model"]


def run_robots(params: dict) -> dict:
    """Every robot plays through the REAL server (submit path); instruments
    recomputed locally from the delivered code."""
    cf = smooth_rival_coeffs(params)
    tw = twin_coeffs(params)
    null_lam = float(np.mean(lam_truth(params, np.asarray(DENSE_GRID))))
    oracle_brk = TRUTH_BRK.format(**params).replace('"""', '"', 2)
    oracle_twin = TRUTH_TWIN.format(c=tw["c"], beta=tw["beta"])
    deliveries = {
        "brk": {
            "oracle_piecewise": TRUTH_BRK.format(**params),
            "suave_generosa": SMOOTH_CODE.format(**cf),
            "null_plano": NULL_CODE.format(lam=null_lam),
        },
        "smooth": {
            "oracle_suave": oracle_twin,
            "suave_generosa": SMOOTH_CODE.format(**cf),
            "quiebre_forzado": FORCED_CODE.format(c=tw["c"], beta=tw["beta"]),
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
                row.update(s_quiebre(prog, params))
                row["F_mean"] = f_mean(prog, params, "brk")
            else:
                row.update(s_clean(prog, params))
                row["espurio"] = spurious_break_flag(prog, params)
            out[pole][name] = row
            extra = (f"S_quiebre={row.get('S_quiebre_fuerte', 0):.3f}" if pole == "brk"
                     else f"S_clean={row.get('S_clean', 0):.3f} espurio={row['espurio']['spurious']}")
            print(f"[{pole}] {name}: accepted={row['accepted']} R={row['R']:.3f} {extra}")
    return out


def main() -> int:
    print("=== scan de instancia (compuertas de ficha) ===")
    params, gates = find_instance()
    print(f"\nFROZEN: seed {params['world_seed']} -> {params}")
    write_artifacts(params)

    print("\n=== robots por el server real ===")
    robots = run_robots(params)

    r_gap = robots["brk"]["oracle_piecewise"]["R"] - robots["brk"]["suave_generosa"]["R"]
    checks = {
        "oracle_s_high": robots["brk"]["oracle_piecewise"]["S_quiebre_fuerte"] >= 0.9,
        "smooth_s_low": robots["brk"]["suave_generosa"]["S_quiebre_fuerte"] <= 0.1,
        "twin_oracle_clean": robots["smooth"]["oracle_suave"]["S_clean"] >= 0.9,
        "twin_oracle_no_espurio": not robots["smooth"]["oracle_suave"]["espurio"]["spurious"],
        "twin_forced_espurio": robots["smooth"]["quiebre_forzado"]["espurio"]["spurious"],
        "twin_forced_dirty": robots["smooth"]["quiebre_forzado"]["S_clean"] <= 0.1,
        "r_directional": r_gap >= 0.03,
        "all_accepted": all(r["accepted"] for pole in robots.values() for r in pole.values()),
    }
    print(f"\nR directional gap (oracle - suave, brk): {r_gap:+.3f}")
    all_pass = all(checks.values()) and gates["all_pass"]
    for case_dir in (BRK_DIR, TWIN_DIR):
        (case_dir / "certificates.json").write_text(json.dumps(
            {"ficha": "docs/research/2026-08-07-ficha-mundo-count-regime-v0.md",
             "gates": {k: v for k, v in gates.items() if not isinstance(v, dict)},
             "robot_checks": checks, "robots": robots, "r_directional_gap": r_gap,
             "all_pass": bool(all_pass)}, indent=2, default=str))
    print("\n=== checks ===")
    for k, v in checks.items():
        print(f"  {k}: {'PASS' if v else 'FAIL'}")
    print(f"\nCERTIFICACION: {'VERDE' if all_pass else 'ROJA'}")
    return 0 if all_pass else 1


if __name__ == "__main__":
    raise SystemExit(main())
