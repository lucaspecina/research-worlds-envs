"""Instance scan for count_regime_v1 (el episodio del impasse).

Runs EVERY gate of the ficha + ADDENDUM RATIFICADO over the assigned world
seeds and reports which instances (if any) can host the episode. This is the
NO-GO test Codex ordered BEFORE any harness work or agent spend: if no instance
satisfies non-flagrancy AND visible failure AND patch-survival AND
no-dictation AND teleological necessity simultaneously, the host is abandoned.

Usage:  python scripts/scan_count_regime_v1.py [--verbose]
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from cases import count_regime_v1_common as C  # noqa: E402


def evaluate_seed(seed: int) -> dict:
    p = C.params_from_seed(seed)
    grid = np.asarray(C.exam_grid(p), float)
    res: dict = {"seed": seed, "params": p, "gates": {}}

    # --- gate 1: continuity at s* (no level jump) ---------------------------
    eps = 1e-6
    lo = float(C.lam_truth(p, p["s_star"] - eps))
    hi = float(C.lam_truth(p, p["s_star"] + eps))
    res["gates"]["continuous_at_sstar"] = abs(hi - lo) < 1e-3

    # --- prefix + reference M0 ---------------------------------------------
    design = C.prefix_design("brk", p)
    m0 = C.m0_reference(design)
    sp, mn, nn = C.design_cells(design)
    z_prefix = [C.z_of_cell(m0, s, m, n) for s, m, n in zip(sp, mn, nn)]
    res["max_abs_z_prefix"] = float(np.max(np.abs(z_prefix)))
    res["gates"]["non_flagrant"] = res["max_abs_z_prefix"] < C.NONFLAGRANT_MAX_Z

    # --- gate 3: control 1 fails M0 visibly ---------------------------------
    cell1 = C.control_cell("brk", p, C.CONTROL_1, C.WITNESS_SAMPLE_SEED + 100)
    z1 = C.z_of_cell(m0, cell1["speed"], cell1["mean"], cell1["n"])
    res["z_control1"] = z1
    res["gates"]["control1_fails_M0"] = abs(z1) >= C.FAIL_MIN_Z

    # --- gate B: every peripheral patch still misses control 2 --------------
    cell2 = C.control_cell("brk", p, C.CONTROL_2, C.WITNESS_SAMPLE_SEED + 200)
    patches = C.patch_library(design, cell1)
    z_patch = {name: C.z_of_cell(mod, cell2["speed"], cell2["mean"], cell2["n"])
               for name, mod in patches.items()}
    res["z_control2_by_patch"] = {k: float(v) for k, v in z_patch.items()}
    res["min_abs_z_patch"] = float(min(abs(v) for v in z_patch.values()))
    res["gates"]["patches_still_fail"] = res["min_abs_z_patch"] >= C.PATCH_MIN_Z

    # --- gate 6: no-dictation at the moment of the first failure ------------
    gap1 = C.discrimination_gap(design, [{"speed": cell1["speed"], "mean": cell1["mean"],
                                          "n": cell1["n"]}])
    res["dbic_gap_after_control1"] = gap1
    res["gates"]["no_dictation"] = gap1 < C.NODICT_MAX_DBIC

    # --- fairness (alcanzabilidad): the evidence DOES discriminate once the
    # agent zooms above the envelope after the failure -----------------------
    extra = [{"speed": cell1["speed"], "mean": cell1["mean"], "n": cell1["n"]},
             {"speed": cell2["speed"], "mean": cell2["mean"], "n": cell2["n"]}]
    zoom = C.zoom_design("brk", p)
    zsp, zmn, znn = C.design_cells(zoom)
    extra += [{"speed": float(s), "mean": float(m), "n": float(n)}
              for s, m, n in zip(zsp, zmn, znn)]
    gap2 = C.discrimination_gap(design, extra)
    res["dbic_gap_after_zoom"] = gap2
    res["gates"]["discriminable_eventually"] = gap2 >= C.NODICT_MAX_DBIC

    # --- gate 7: teleological necessity on the DECISION band ----------------
    band = np.asarray(C.decision_band(p), float)
    d_rival = C.curve_distance(C.lam_smooth_rival(p, band), C.lam_truth(p, band))
    res["D_rival"] = d_rival
    res["gates"]["teleological_necessity"] = d_rival >= C.NECESSITY_D_RIVAL_MIN

    # --- twin pairing on the HISTORY surface (what the agent can see) -------
    hist = np.asarray(C.history_grid(), float)
    pairing = C.curve_distance(C.lam_twin(p, hist), C.lam_truth(p, hist))
    res["twin_pairing"] = pairing
    res["gates"]["twin_paired"] = pairing <= C.TWIN_PAIRING_TOL

    res["PASS"] = all(res["gates"].values())
    return res


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--verbose", action="store_true")
    args = ap.parse_args()

    rows = [evaluate_seed(s) for s in C.WORLD_SEEDS]
    passing = [r for r in rows if r["PASS"]]

    gate_names = list(rows[0]["gates"].keys())
    print(f"scan count_regime_v1 — {len(rows)} seeds, gates: {', '.join(gate_names)}\n")
    hdr = f"{'seed':>6} {'maxZpre':>8} {'zC1':>7} {'minZpatch':>10} {'dBIC1':>7} {'dBIC2':>7} {'Driv':>6} {'pair':>6}  gates"
    print(hdr)
    for r in rows:
        failed = [g for g, ok in r["gates"].items() if not ok]
        mark = "PASS" if r["PASS"] else "fail:" + ",".join(failed)
        print(f"{r['seed']:>6} {r['max_abs_z_prefix']:>8.2f} {r['z_control1']:>7.2f} "
              f"{r['min_abs_z_patch']:>10.2f} {r['dbic_gap_after_control1']:>7.1f} "
              f"{r['dbic_gap_after_zoom']:>7.1f} {r['D_rival']:>6.2f} "
              f"{r['twin_pairing']:>6.2f}  {mark}")

    print(f"\nPASS: {len(passing)}/{len(rows)}")
    counts = {g: sum(1 for r in rows if not r["gates"][g]) for g in gate_names}
    print("failures by gate: " + ", ".join(f"{g}={c}" for g, c in counts.items() if c))

    if passing and args.verbose:
        r = passing[0]
        print("\nfirst passing instance:")
        print(json.dumps({k: v for k, v in r.items() if k != "params"}, indent=2, default=float))
        print("params:", json.dumps(r["params"], indent=2, default=float))
    return 0 if passing else 1


if __name__ == "__main__":
    raise SystemExit(main())
