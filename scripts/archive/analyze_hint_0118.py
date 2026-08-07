"""ADR 0118 + ADR 0119 SEALED analysis for the corrected hint experiment.

Written BLIND: this script was authored while the run was still in progress
(~11/46 episodes), coding the sealed rules BEFORE seeing the full data, so the
analysis cannot bend to the results. It implements EXACTLY:

  - ADR 0118: predictions P0..P4 on cell MEDIANS.
  - ADR 0119 (seal, supersedes 0118 where they clash):
      * PRIMARY analysis = intent-to-treat (every row with error==null,
        exec-zeros included with their recorded R); judge-only = SECONDARY.
      * P2 is TWO-SIDED (|gap| <= 0.10); a large NEGATIVE control effect
        (< -0.10) is a FAIL, and in that case P4 is NOT read as success.
      * Also report: acceptance rate per cell with Wilson 95% CI, the full
        R distribution per cell, and PAIRED per-seed differences (same seeds
        across arms by design).
      * If P0 fails: NO specificity inference from this run (the latent_mix_v2
        fallback of 0118 is DEGRADED to exploratory -- not run here).
      * Max allowed reading if everything passes (sealed, printed verbatim).

Run:  .venv/Scripts/python scripts/analyze_hint_0118.py
Input: scripts/out/exp_hint_0118_results.json  (48 rows when complete)
Output: stdout verdict + scripts/out/analysis_0118.json
"""

import json
import math
import sys
from pathlib import Path
from statistics import median

ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "scripts" / "out" / "exp_hint_0118_results.json"
OUT = ROOT / "scripts" / "out" / "analysis_0118.json"

WORLD_TRAP = "first_story_scarce_v0"
WORLD_CTRL = "first_story_v0"
CONDS = ("libre", "hint_T", "placebo")
N_EXPECTED = 48

# sealed thresholds (ADR 0118 letter + ADR 0119 seal)
P0_CEILING = 0.75      # control/libre median must be BELOW this (headroom)
P1_MIN_GAP = 0.30      # trap: hint_T - libre >= this
P2_ABS_MAX = 0.10      # control: |hint_T - libre| <= this (TWO-SIDED, seal)
P3_ABS_MAX = 0.10      # placebo: |placebo - libre| <= this, both worlds
P4_MIN_DIFF = 0.15     # (trap gap) - (control gap) >= this

MAX_READING = (
    "LECTURA MAXIMA SELLADA (ADR 0119): 'En DeepSeek, una instruccion "
    "contextualmente congruente sobre integracion final muestra una interaccion "
    "grande con una manipulacion CONJUNTA de presupuesto y precios de evidencia.' "
    "NO es 'senal de validez de constructo'. Proximo peldano si paso: replica con "
    "texto contextualmente NEUTRO + control con precios emparejados."
)


def wilson_ci(k: int, n: int, z: float = 1.96) -> tuple[float, float]:
    if n == 0:
        return (0.0, 1.0)
    p = k / n
    denom = 1 + z * z / n
    center = (p + z * z / (2 * n)) / denom
    half = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / denom
    return (max(0.0, center - half), min(1.0, center + half))


def load_rows() -> list[dict]:
    rows = json.loads(RESULTS.read_text(encoding="utf-8"))
    return rows


def cell(rows, world, cond):
    return [r for r in rows if r["world"] == world and r["cond"] == cond]


def analyze() -> dict:
    all_rows = load_rows()
    errored = [r for r in all_rows if r.get("error") is not None]
    rows = [r for r in all_rows if r.get("error") is None]

    if len(rows) < N_EXPECTED:
        print(f"WARNING: only {len(rows)}/{N_EXPECTED} clean episodes present "
              f"({len(errored)} errored). Analysis below is PARTIAL -- the sealed "
              f"verdict only counts on the complete run.")

    report = {"n_clean": len(rows), "n_errored": len(errored), "cells": {}}

    # ---- per-cell stats: ITT primary, judge-only secondary --------------------
    for world in (WORLD_TRAP, WORLD_CTRL):
        for cond in CONDS:
            c = cell(rows, world, cond)
            itt = sorted(r["R"] for r in c)
            judge = sorted(r["R"] for r in c if r["klass"] == "judge")
            acc = sum(1 for r in c if r["accepted"])
            lo, hi = wilson_ci(acc, len(c))
            report["cells"][f"{world}/{cond}"] = {
                "n": len(c),
                "median_ITT": median(itt) if itt else None,
                "median_judge_only": median(judge) if judge else None,
                "n_judge": len(judge),
                "acceptance_rate": acc / len(c) if c else None,
                "acceptance_wilson95": [round(lo, 3), round(hi, 3)],
                "R_sorted_ITT": [round(x, 3) for x in itt],
            }

    def med(world, cond):
        return report["cells"][f"{world}/{cond}"]["median_ITT"]

    # ---- paired per-seed differences (sealed supplementary) -------------------
    paired = {}
    for world in (WORLD_TRAP, WORLD_CTRL):
        libre_by_seed = {r["seed"]: r["R"] for r in cell(rows, world, "libre")}
        for cond in ("hint_T", "placebo"):
            diffs = []
            for r in cell(rows, world, cond):
                if r["seed"] in libre_by_seed:
                    diffs.append(round(r["R"] - libre_by_seed[r["seed"]], 3))
            paired[f"{world}/{cond}-libre"] = {
                "per_seed_diffs_sorted": sorted(diffs),
                "median_paired_diff": median(diffs) if diffs else None,
            }
    report["paired_by_seed"] = paired

    # ---- gaps on cell medians (ADR 0118 letter) --------------------------------
    gap_trap_hint = med(WORLD_TRAP, "hint_T") - med(WORLD_TRAP, "libre")
    gap_ctrl_hint = med(WORLD_CTRL, "hint_T") - med(WORLD_CTRL, "libre")
    gap_trap_plac = med(WORLD_TRAP, "placebo") - med(WORLD_TRAP, "libre")
    gap_ctrl_plac = med(WORLD_CTRL, "placebo") - med(WORLD_CTRL, "libre")
    report["gaps_on_medians"] = {
        "trap_hint": round(gap_trap_hint, 3),
        "ctrl_hint": round(gap_ctrl_hint, 3),
        "trap_placebo": round(gap_trap_plac, 3),
        "ctrl_placebo": round(gap_ctrl_plac, 3),
        "diff_of_diffs": round(gap_trap_hint - gap_ctrl_hint, 3),
    }

    # ---- sealed predictions ----------------------------------------------------
    p0 = med(WORLD_CTRL, "libre") < P0_CEILING
    p1 = gap_trap_hint >= P1_MIN_GAP
    p2_abs_ok = abs(gap_ctrl_hint) <= P2_ABS_MAX
    p2_negative_fail = gap_ctrl_hint < -P2_ABS_MAX
    p2 = p2_abs_ok  # two-sided per seal
    p3 = (abs(gap_trap_plac) <= P3_ABS_MAX) and (abs(gap_ctrl_plac) <= P3_ABS_MAX)
    p4_raw = (gap_trap_hint - gap_ctrl_hint) >= P4_MIN_DIFF
    p4 = p4_raw and not p2_negative_fail  # seal: not read as success on negative fail

    report["predictions"] = {
        "P0_headroom_ctrl_libre_lt_0.75": {"pass": p0, "value": med(WORLD_CTRL, "libre")},
        "P1_trap_hint_gap_ge_0.30": {"pass": p1, "value": round(gap_trap_hint, 3)},
        "P2_ctrl_hint_absgap_le_0.10_twosided": {
            "pass": p2, "value": round(gap_ctrl_hint, 3),
            "negative_fail": p2_negative_fail,
        },
        "P3_placebo_inert_both": {
            "pass": p3,
            "trap": round(gap_trap_plac, 3), "ctrl": round(gap_ctrl_plac, 3),
        },
        "P4_diff_of_diffs_ge_0.15": {
            "pass": p4, "raw_pass": p4_raw,
            "value": round(gap_trap_hint - gap_ctrl_hint, 3),
        },
    }

    # ---- sealed verdict text ---------------------------------------------------
    lines = []
    if not p0:
        lines.append(
            "P0 FALLO (control sin headroom): SIN inferencia de especificidad en esta "
            "corrida (sello 0119; el fallback v2 queda solo exploratorio, no corre aca)."
        )
    if not p1:
        lines.append(
            "P1 FALLO: el efecto de la pista NO se sostiene ni en su propio mundo -> "
            "fragilidad seria del efecto original; el claim baja otro escalon."
        )
    if p2_negative_fail:
        lines.append(
            "P2 FALLO NEGATIVO (la pista HUNDE el control mas alla de -0.10): fallo de "
            "especificidad; P4 no se lee como exito (sello 0119)."
        )
    elif not p2_abs_ok:
        lines.append(
            "P2 FALLO POSITIVO (la pista tambien levanta el control > +0.10): objecion "
            "operacion/checklist de Codex CONFIRMADA -> el metodo de pistas se retira "
            "como evidencia de constructo; la validacion migra a manipulaciones "
            "no-instruccionales (presupuesto/presion) y robots."
        )
    if not p3:
        lines.append(
            "P3 FALLO (placebo movio el score): lectura acotada -- esa instruccion de "
            "estilo tambien tuvo efecto; debilita el metodo de pistas como evidencia."
        )
    if p0 and p1 and p2 and p3 and p4:
        lines.append("TODAS LAS PREDICCIONES PASAN.")
        lines.append(MAX_READING)
    elif not lines:
        lines.append("Resultado mixto sin rama sellada especifica: reportar tal cual, "
                     "sin lectura de exito.")
    report["verdict_lines"] = lines
    return report


def main() -> None:
    if not RESULTS.exists():
        print(f"no results file at {RESULTS}")
        sys.exit(1)
    report = analyze()
    OUT.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")

    print("=" * 78)
    print("ANALISIS SELLADO 0118+0119 (primario = intencion-de-tratar)")
    print("=" * 78)
    for key, c in report["cells"].items():
        print(f"{key:38s} n={c['n']}  medITT={c['median_ITT']}  "
              f"medJudge={c['median_judge_only']} (nJ={c['n_judge']})  "
              f"acc={c['acceptance_rate']}  CI95={c['acceptance_wilson95']}")
        print(f"{'':38s} R: {c['R_sorted_ITT']}")
    print("-" * 78)
    for k, v in report["gaps_on_medians"].items():
        print(f"  gap {k}: {v}")
    print("-" * 78)
    for k, v in report["paired_by_seed"].items():
        print(f"  paired {k}: med={v['median_paired_diff']}  {v['per_seed_diffs_sorted']}")
    print("-" * 78)
    for k, v in report["predictions"].items():
        print(f"  {'PASS' if v['pass'] else 'FAIL':4s}  {k}  -> {v}")
    print("=" * 78)
    for line in report["verdict_lines"]:
        print("VEREDICTO:", line)
    print(f"\n(json -> {OUT})")


if __name__ == "__main__":
    main()
