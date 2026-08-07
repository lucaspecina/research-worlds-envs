"""Certifier G1/G4/G5-mecanica for the count-mixture pair (ficha 2026-08-06).

Steps (all zero-LLM, deterministic):
  1. Scan world seeds 99200..99249 in order; for each, apply the FROZEN
     acceptance gates on candidate instance parameters:
       G1a  witness on a purchasable-size MIX sample (n=300, world noise):
            BIC selects mix2 with margin >= 10 over best single AND CV: mix
            wins >= 4/5 folds  [ficha: "todos los folds" relaxed NEVER — we
            require 5/5; recorded here explicitly]
       G1b  witness on the SINGLE twin sample: BIC selects a one-component
            model (poisson/negbin/zip) over mix2, majority of CV folds
       AP   anti-poster: marginal is bimodal and valley pmf >= 20% of the
            smaller peak (the jump must not be a cartoon)
  2. Freeze the FIRST accepted instance to cases/count_mix_v0/instance.json
     (params + valley geometry + tail threshold + witness numbers + rejected
     seeds with causes).
  3. Mechanical checks on the frozen instance: determinism, schema, mean
     pairing MIX~SINGLE at three speeds, repeats wiring (ICC gap), necessity
     anchor (single-baseline functionals differ; S_struct(truth)~1, ~0 for
     the baseline), huella vs latent_mix (different formalism: counts+ICC).
  4. Write cases/count_mix_v0/certificates.json (+ twin copy) and print a
     PASS/FAIL report. Behavioral reading stays forbidden until all PASS.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from cases.count_mix_v0_common import (  # noqa: E402
    ANTI_POSTER_FLOOR, INSTANCE_PATH, WITNESS_DBIC, WITNESS_N, WORLD_SEEDS,
    _DictRegime, _sample_counts, params_from_seed, program_functionals,
    s_struct, single_baseline_program, truth_pmf_mix, valley_geometry, witness,
)

CV_REQUIRED_MIX = 5      # 5/5 folds (ficha: "todos los folds")
CV_REQUIRED_SINGLE = 3   # majority for the twin
SAMPLE_SEED = 99299      # frozen witness-sample seed (outside episode seeds)


def _witness_sample(pole: str, params: dict, seed: int) -> np.ndarray:
    df = _sample_counts(pole, params, _DictRegime({"speed": 1.0}), WITNESS_N, seed)
    return df["y"].to_numpy(float)


def scan_instances() -> tuple[dict | None, list[dict]]:
    rejected = []
    for ws in WORLD_SEEDS:
        params = params_from_seed(ws)
        geo = valley_geometry(params)
        if geo is None:
            rejected.append({"world_seed": ws, "cause": "not bimodal"})
            continue
        if geo["valley_ratio"] < ANTI_POSTER_FLOOR:
            rejected.append({"world_seed": ws, "cause": f"cartoon valley (ratio {geo['valley_ratio']:.3f} < {ANTI_POSTER_FLOOR})"})
            continue
        w_mix = witness(_witness_sample("mix", params, SAMPLE_SEED))
        if not (w_mix["selected"] == "mix2"
                and w_mix["dbic_mix_vs_best_single"] >= WITNESS_DBIC
                and w_mix["cv_mix_wins"] >= CV_REQUIRED_MIX):
            rejected.append({"world_seed": ws, "cause": "G1a witness on MIX",
                             "detail": {k: w_mix[k] for k in ("selected", "dbic_mix_vs_best_single", "cv_mix_wins")}})
            continue
        w_single = witness(_witness_sample("single", params, SAMPLE_SEED))
        if not (w_single["selected"] != "mix2"
                and w_single["cv_mix_wins"] <= 5 - CV_REQUIRED_SINGLE):
            rejected.append({"world_seed": ws, "cause": "G1b witness on SINGLE",
                             "detail": {k: w_single[k] for k in ("selected", "dbic_mix_vs_best_single", "cv_mix_wins")}})
            continue
        pmf = truth_pmf_mix(params)
        tail_at = int(np.argmax(np.cumsum(pmf) >= 0.98))
        return ({"params": params, "geometry": geo, "tail_at": tail_at,
                 "witness_mix": w_mix, "witness_single": w_single,
                 "witness_n": WITNESS_N, "witness_sample_seed": SAMPLE_SEED},
                rejected)
    return None, rejected


def mechanical_checks(inst: dict) -> dict:
    params, geo, tail_at = inst["params"], inst["geometry"], inst["tail_at"]
    checks = {}

    def prog(pole):
        return lambda regime, n, seed: _sample_counts(pole, params, regime, n, seed)

    # determinism + schema
    a = prog("mix")(_DictRegime({"speed": 1.0, "repeats_per_unit": 2}), 100, 12345)
    b = prog("mix")(_DictRegime({"speed": 1.0, "repeats_per_unit": 2}), 100, 12345)
    checks["determinism"] = bool(a.equals(b))
    checks["schema"] = (list(a.columns) == ["unit_id", "y"] and len(a) == 100
                        and a["unit_id"].nunique() == 50)

    # mean pairing at three speeds (MIX vs SINGLE, big-sample)
    diffs = []
    for s in (0.8, 1.0, 1.2):
        ym = prog("mix")(_DictRegime({"speed": s}), 20000, 777)["y"].mean()
        ys = prog("single")(_DictRegime({"speed": s}), 20000, 778)["y"].mean()
        diffs.append(abs(ym - ys) / max(ys, 1e-9))
    checks["mean_pairing_reldiff_max"] = float(max(diffs))
    checks["mean_pairing"] = bool(max(diffs) < 0.03)

    # functionals: truth vs single-baseline anchor
    truth_f = program_functionals(prog("mix"), geo, tail_at)
    twin_f = program_functionals(prog("single"), geo, tail_at)
    y_train = _witness_sample("mix", params, inst["witness_sample_seed"])
    base_prog, base_fit = single_baseline_program(y_train)
    base_f = program_functionals(base_prog, geo, tail_at)
    s_truth = s_struct(truth_f, truth_f, base_f)
    s_base = s_struct(base_f, truth_f, base_f)
    s_twin_as_model = s_struct(twin_f, truth_f, base_f)
    checks["necessity_anchor"] = {
        "baseline": base_fit["name"], "baseline_params": base_fit["params"],
        "truth_functionals": truth_f, "twin_functionals": twin_f,
        "baseline_functionals": base_f,
        "S_truth": s_truth["S_struct"], "S_baseline": s_base["S_struct"],
        "S_twin_program": s_twin_as_model["S_struct"],
        "components_used": s_base["components_used"],
    }
    checks["necessity_gap"] = bool(s_truth["S_struct"] >= 0.9 and s_base["S_struct"] <= 0.1)

    # ICC gap: repeats separate the poles mechanically
    checks["icc_mix"] = truth_f["icc"]
    checks["icc_single"] = twin_f["icc"]
    checks["icc_gap"] = bool(truth_f["icc"] >= 0.4 and twin_f["icc"] <= 0.1)

    # huella vs latent_mix family: distinct formalism fingerprint (counts + ICC
    # channel; latent_mix is continuous outcome, no unit persistence)
    checks["huella"] = {"formalism": "integer counts + repeated measures (ICC)",
                        "latent_mix_v2": "continuous outcome, no unit persistence",
                        "distinct": True}
    return checks


def main() -> int:
    inst, rejected = scan_instances()
    report = {"rejected_seeds": rejected}
    if inst is None:
        report["verdict"] = "FAIL: no instance in 99200-99249 passed G1/AP"
        print(json.dumps(report, indent=2))
        return 1

    INSTANCE_PATH.parent.mkdir(parents=True, exist_ok=True)
    INSTANCE_PATH.write_text(json.dumps(
        {"params": inst["params"], "geometry": inst["geometry"],
         "tail_at": inst["tail_at"], "witness_n": inst["witness_n"],
         "witness_sample_seed": inst["witness_sample_seed"]}, indent=2))

    checks = mechanical_checks(inst)
    gates = {
        "G1a_witness_mix": True, "G1b_witness_single": True,
        "AP_anti_poster": True,
        "determinism": checks["determinism"], "schema": checks["schema"],
        "mean_pairing": checks["mean_pairing"],
        "necessity_gap": checks["necessity_gap"], "icc_gap": checks["icc_gap"],
    }
    verdict = "PASS" if all(gates.values()) else "FAIL"
    cert = {"ficha": "docs/research/2026-08-06-ficha-mundo-count-mix-v0.md",
            "world_seed": inst["params"]["world_seed"], "gates": gates,
            "witness_mix": inst["witness_mix"], "witness_single": inst["witness_single"],
            "checks": checks, "rejected_seeds": rejected, "verdict": verdict,
            "pending_gates": ["G2 robots + menu/prices", "G3 value map",
                              "G5 interface smoke (needs server wiring)"]}
    for pole in ("count_mix_v0", "count_mix_twin_v0"):
        (ROOT / "cases" / pole / "certificates.json").write_text(json.dumps(cert, indent=2))

    print(f"world_seed elegido: {inst['params']['world_seed']}")
    print(f"params: {json.dumps(inst['params'], indent=2)}")
    print(f"geometry: {inst['geometry']}")
    print(f"witness MIX: {inst['witness_mix']['selected']} dBIC={inst['witness_mix']['dbic_mix_vs_best_single']:.1f} cv={inst['witness_mix']['cv_mix_wins']}/5")
    print(f"witness SINGLE: {inst['witness_single']['selected']} cv_mix={inst['witness_single']['cv_mix_wins']}/5")
    print(f"rechazadas: {len(rejected)}")
    print(json.dumps({k: v for k, v in checks.items() if k != 'necessity_anchor'}, indent=2))
    print(f"S_truth={checks['necessity_anchor']['S_truth']:.3f}  S_baseline={checks['necessity_anchor']['S_baseline']:.3f}  S_twin={checks['necessity_anchor']['S_twin_program']:.3f}")
    print(f"componentes de S usados: {checks['necessity_anchor']['components_used']}")
    print(f"VEREDICTO (G1+AP+mecanica): {verdict}")
    return 0 if verdict == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
