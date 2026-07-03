"""c_F calibration sweep -- pre-registered protocol (Decision Log v0.31 + v0.34).

Factory-side measurement tooling (NOT the reward path; it CONSUMES wager.reward).

Protocol implemented verbatim:
  1. FIXED calibration grid (v0.34-A, 27 items, seeds 91001+i, weights =
     battery_builder.stakes_relevance) -- NOT the derived battery (circularity,
     v0.31 refinement 3). The grid is DISQUALIFIED as validity evidence.
  2. CV fixed BEFORE the sweep (v0.34-A4): CV_sweep = max(CV at c_F=0, c_F=8),
     B=10 resampled seed-sets on the MIDDLE degradation rung (rung_5, the 4th of
     7); that threshold applies to the gates of ALL candidates.
  3. Log-grid sweep c_F in {0, 0.25, 0.5, 1, 2, 4, 8}; per candidate the
     WorldSide recomputes D_MAX_item = 1.5 x D_combined(truth, null) (v0.28
     amendment 4 -- the cap is a FUNCTION of c_F).
  4. Gates (conjoint, all >= 3 x CV_sweep in R units; v0.31 + v0.34 amendments):
     (i)   extremes + per-axis monotonicity: every measurement rung strictly
           below truth AND strictly above the null (no total order between
           heterogeneous rungs; the ladder rationales are pre-registered
           expectations, reported not gated);
     (ii)  visibility per operator: confounding -> its PARAM ablation (and twin)
           lose >= 3xCV; heterogeneity -> the MOMENT-MATCHED oracle loses
           >= 3xCV (v0.34-C: the param ablation shifts moments and is visible
           for the wrong reason; it is reported as an intermediate rung);
     (iii) instrument diagnostic: oracle strictly below world.py >= 3xCV.
  5. Baseline at c_F=0 reports ALL gates per rung (v0.31-a; v0.34-B expectations:
     confounding rungs PASS via observational items and are c_F-INSENSITIVE --
     their failure means FIX THE GRID, not sweep; pure heterogeneity ablation
     PASSES via energy; the oracle FAILS and is THE gate that fixes c_F*).
  6. c_F* = MINIMUM candidate passing all gates; sensitivity band x2 / /2;
     confirmation CV at the winner with B=20 + extremes B=10. The binomial
     noise of the functional bounds c_F from above -- if the minimum sits near
     that ceiling, the SANDWICH is reported as a finding.

Run:  .venv/Scripts/python cases/mendel_subtypes_v1/calibrate_cf.py
"""

import json
import sys
import time
from pathlib import Path

import numpy as np

CASE_DIR = Path(__file__).parent
sys.path.insert(0, str(CASE_DIR))

from wager.contracts import Battery, BatteryItem, CaseMeta, ScoringParams  # noqa: E402
from wager.contracts.world import Regime  # noqa: E402
from wager.factory.battery_builder import stakes_relevance  # noqa: E402
from wager.reward.sandbox import SandboxedSubmission  # noqa: E402
from wager.reward.scorer import WorldSide, sandboxed_null_sample, score_submission  # noqa: E402
from wager.reward.seeds import derive_world_seed  # noqa: E402

C_F_GRID = [0.0, 0.25, 0.5, 1.0, 2.0, 4.0, 8.0]
GRID_SEED0 = 91001
B_SWEEP = 10   # CV estimation at the c_F extremes (pre-fixed threshold)
B_WINNER = 20  # confirmation at the winner
MID_RUNG = "rung_5_ablate_heterogeneity"  # middle of the 7 degradation rungs

# gate (ii) assignment per operator (Decision Log v0.34-C)
VISIBILITY_RUNG = {
    "confounding_por_clase": ["rung_3_ablate_confounding", "rung_4_twin_confounding"],
    "heterogeneidad_latente": ["rung_6_oracle_moments"],  # moment-matched, NOT the param ablation
}


def calibration_grid() -> Battery:
    """The pre-registered grid, verbatim from Decision Log v0.34-A."""
    meta = CaseMeta.from_json_file(CASE_DIR / "meta.json")
    regimes: list[Regime] = []
    for d in (2.0, 4.0, 6.0, 8.0):                      # in-record interventional (12)
        for m in (-0.75, 0.0, 0.75):
            regimes.append(Regime(config={"dose": d}, context={"mix_logit": m}))
    for d in (4.0, 8.0):                                 # out-of-record in mix (8)
        for m in (-1.5, 1.5, -2.5, 2.5):                 # +-2.5 = beyond experimentable
            regimes.append(Regime(config={"dose": d}, context={"mix_logit": m}))
    for d in (0.0, 10.0):                                # out-of-record in dose (2)
        regimes.append(Regime(config={"dose": d}, context={"mix_logit": 0.0}))
    for m in (-1.0, -0.5, 0.0, 0.5, 1.0):                # observational quota (5)
        regimes.append(Regime(config={}, context={"mix_logit": m}))
    items = [
        BatteryItem(weight=stakes_relevance(r, meta.stakes), regime=r, seed_world=GRID_SEED0 + i)
        for i, r in enumerate(regimes)
    ]
    return Battery(items=items)


def load_case():
    meta = CaseMeta.from_json_file(CASE_DIR / "meta.json")
    world_source = (CASE_DIR / "world.py").read_text(encoding="utf-8")
    rungs = {p.stem: p.read_text(encoding="utf-8") for p in sorted((CASE_DIR / "ladder").glob("rung_*.py"))}
    params = ScoringParams(
        lambda_mdl=meta.scoring.lambda_mdl,
        n_samples=meta.scoring.n_samples,
        m_reps=meta.scoring.m_reps,
        model_call_timeout_s=meta.scoring.model_call_timeout_s,
    )
    return meta, world_source, rungs, params


def resampled(battery: Battery, b: int) -> Battery:
    return Battery(items=[
        BatteryItem(weight=it.weight, regime=it.regime,
                    seed_world=derive_world_seed(it.seed_world, idx, b))
        for idx, it in enumerate(battery.items)
    ])


def score_rungs(world_sample, battery, meta, params, c_f, sandboxes, null_code, which=None):
    """R per rung on one battery seed-set at one c_F. Returns dict name -> R."""
    with sandboxed_null_sample(null_code, meta.column_names, params.model_call_timeout_s) as null_sample:
        ws = WorldSide(world_sample, battery, meta.column_names, params.n_samples,
                       null_sample=null_sample, functionals=meta.stakes.functionals, c_f=c_f)
        raw = {}
        for name, sb in sandboxes.items():
            if which is not None and name not in which:
                continue
            raw[name] = score_submission(sb.code, ws, params, sandbox=sb).raw_score
    s_truth, s_naive = raw["world"], raw["rung_7_naive_fit"]
    denom = s_truth - s_naive
    return {name: (s - s_naive) / denom for name, s in raw.items()}, denom


def cv_of_mid_rung(world_sample, battery, meta, params, c_f, sandboxes, null_code, b_total):
    rs = []
    for b in range(1, b_total + 1):
        r, _ = score_rungs(world_sample, resampled(battery, b), meta, params, c_f,
                           sandboxes, null_code, which=("world", "rung_7_naive_fit", MID_RUNG))
        rs.append(r[MID_RUNG])
    rs = np.array(rs)
    return float(rs.std(ddof=1) / abs(rs.mean())), float(rs.mean())


def gates(r: dict, cv: float, operators) -> dict:
    """Evaluate the three conjoint gates at threshold 3xCV. Returns per-gate detail."""
    thr = 3.0 * cv
    meas = [k for k in r if k not in ("world", "rung_7_naive_fit", "rung_8_null")]
    g1 = {k: {"below_truth": (1.0 - r[k]) >= thr, "above_null": (r[k] - r["rung_8_null"]) >= thr}
          for k in meas}
    gate_i = all(v["below_truth"] and v["above_null"] for v in g1.values())
    g2 = {}
    for op in operators:
        rungs = VISIBILITY_RUNG[op.name]
        g2[op.name] = {rk: (1.0 - r[rk]) >= thr for rk in rungs}
    gate_ii = all(all(d.values()) for d in g2.values())
    gate_iii = (1.0 - r["rung_6_oracle_moments"]) >= thr
    return {"i": gate_i, "i_detail": g1, "ii": gate_ii, "ii_detail": g2,
            "iii": gate_iii, "all": gate_i and gate_ii and gate_iii, "threshold": thr}


def main():
    t0 = time.perf_counter()
    meta, world_source, rungs, params = load_case()
    battery = calibration_grid()
    null_code = rungs["rung_8_null"]

    import importlib.util
    spec = importlib.util.spec_from_file_location("world_v1", CASE_DIR / "world.py")
    world_mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(world_mod)
    world_sample = world_mod.sample

    codes = {"world": world_source, **rungs}
    print(f"grid: {len(battery.items)} items, seeds {GRID_SEED0}..{GRID_SEED0 + len(battery.items) - 1}")
    print(f"rungs: {list(codes)}")

    sandboxes = {}
    try:
        for name, code in codes.items():
            sb = SandboxedSubmission(code, meta.column_names, timeout_s=params.model_call_timeout_s)
            sb.__enter__()
            sb.code = code
            sandboxes[name] = sb

        # --- (2) CV fixed BEFORE the sweep: max over the c_F extremes ----------
        cv_lo, mid_lo = cv_of_mid_rung(world_sample, battery, meta, params, C_F_GRID[0],
                                       sandboxes, null_code, B_SWEEP)
        cv_hi, mid_hi = cv_of_mid_rung(world_sample, battery, meta, params, C_F_GRID[-1],
                                       sandboxes, null_code, B_SWEEP)
        cv_sweep = max(cv_lo, cv_hi)
        print(f"\nCV (B={B_SWEEP}, mid rung {MID_RUNG}):")
        print(f"  c_F=0: CV={cv_lo:.4f} (mean R={mid_lo:.3f})   c_F=8: CV={cv_hi:.4f} (mean R={mid_hi:.3f})")
        print(f"  CV_sweep = {cv_sweep:.4f}  -> gate threshold 3xCV = {3 * cv_sweep:.4f} (R units)")

        # --- (3-5) sweep ------------------------------------------------------
        results = {}
        for c_f in C_F_GRID:
            r, denom = score_rungs(world_sample, battery, meta, params, c_f, sandboxes, null_code)
            g = gates(r, cv_sweep, meta.operators)
            results[c_f] = {"R": r, "denom": denom, "gates": g}
            flag = "PASS" if g["all"] else "fail"
            print(f"\nc_F={c_f:<5} denom={denom:.4f}  gates: i={g['i']} ii={g['ii']} iii={g['iii']}  -> {flag}")
            for name in codes:
                print(f"    R({name}) = {r[name]:+.3f}")

        # --- baseline report (v0.34-B) ----------------------------------------
        base = results[0.0]
        print("\nBASELINE c_F=0 (pre-registered expectations, v0.34-B):")
        b_thr = base["gates"]["threshold"]
        for name, expect in [("rung_3_ablate_confounding", "PASS (observational items; c_F-insensitive)"),
                             ("rung_4_twin_confounding", "PASS (idem)"),
                             ("rung_5_ablate_heterogeneity", "PASS via energy (moments, the wrong reason)"),
                             ("rung_6_oracle_moments", "FAIL (THE gate that must fix c_F*)")]:
            sep = 1.0 - base["R"][name]
            print(f"  {name}: separation={sep:.4f} vs thr={b_thr:.4f} -> "
                  f"{'separates' if sep >= b_thr else 'DOES NOT separate'}   [expected: {expect}]")

        # --- (6) c_F* = minimum passing all gates ------------------------------
        passing = [c for c in C_F_GRID if results[c]["gates"]["all"]]
        report = {"cv_sweep": cv_sweep, "cv_lo": cv_lo, "cv_hi": cv_hi,
                  "grid_items": len(battery.items), "results": {
                      str(c): {"R": results[c]["R"], "denom": results[c]["denom"],
                               "gates": {k: results[c]["gates"][k] for k in ("i", "ii", "iii", "all", "threshold")}}
                      for c in C_F_GRID}}
        if not passing:
            print("\nNO candidate passes all gates -> investigate (do NOT retune the grid).")
        else:
            c_star = min(passing)
            print(f"\nc_F* = {c_star} (minimum passing; candidates passing: {passing})")
            if c_star == 0.0:
                print("  WARNING: c_F*=0 -> the functional is NOT needed on this grid; "
                      "the anti-collapse guard expected the oracle to fail at 0. INVESTIGATE.")
            # which gate binds: the gate that fails at the largest c_F below c_star
            below = [c for c in C_F_GRID if c < c_star]
            if below:
                g = results[max(below)]["gates"]
                binding = [k for k in ("i", "ii", "iii") if not g[k]]
                print(f"  binding gate(s) just below c_F*: {binding}")
            # sensitivity band x2 / /2
            for lbl, cb in (("x2", c_star * 2), ("/2", c_star / 2)):
                if cb in results:
                    print(f"  band {lbl} (c_F={cb}): all gates = {results[cb]['gates']['all']}")
                elif cb > 0:
                    r, _ = score_rungs(world_sample, battery, meta, params, cb, sandboxes, null_code)
                    gb = gates(r, cv_sweep, meta.operators)
                    print(f"  band {lbl} (c_F={cb}): all gates = {gb['all']}")
            # confirmation CV at winner (B=20); extremes already at B=10
            cv_win, mid_win = cv_of_mid_rung(world_sample, battery, meta, params, c_star,
                                             sandboxes, null_code, B_WINNER)
            print(f"  CV at winner (B={B_WINNER}): {cv_win:.4f} (mean R mid rung={mid_win:.3f})")
            if 3 * cv_win > 3 * cv_sweep:
                print("  NOTE: winner CV exceeds the pre-fixed sweep CV -> report; "
                      "if gates fail under it, that is the noise-vs-sufficiency SANDWICH.")
            report.update({"c_star": c_star, "cv_winner": cv_win})
        out = CASE_DIR / "calibration_report.json"
        out.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
        print(f"\nreport -> {out}  ({time.perf_counter() - t0:.1f}s)")
    finally:
        for sb in sandboxes.values():
            sb.__exit__(None, None, None)


if __name__ == "__main__":
    main()
