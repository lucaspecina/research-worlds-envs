"""c_F calibration sweep -- registered DO-OVER (Decision Log v0.31 + v0.34 + v0.36).

Factory-side measurement tooling (NOT the reward path; it CONSUMES wager.reward).
Run 1 (v0.35) halted on the pre-registered guard; this do-over integrates the
three approved decisions and RETIRES run 1's gates (its numbers stand as
measurements; `calibration_report.json` history preserves them).

Protocol (v0.36):
  1. FIXED grid (v0.34-A, verbatim): 27 items, seeds 91001+i, weights =
     battery_builder.stakes_relevance. Disqualified as validity evidence.
  2. Thresholds in ABSOLUTE R units -- 3 x std(R), NEVER relative CV (v0.36-1,
     fifth scale pathology; convention pinned in wager/factory/calibration.py
     and guarded by the scale-sanity suite). Fixed BEFORE the sweep via mini-L2
     (B=10) at the c_F extremes {0, 8}:
       thr_global = 3 x max std(R_mid)        [mid degradation rung, full grid]
       thr_local  = 3 x max std(R_obs(conf))  [confounding ablation, obs sub-battery]
     std(R_oracle) is also measured and REPORTED (investigation data, not a gate).
  3. Gates (conjoint) per candidate c_F, D_MAX recomputed per candidate:
     (i)   NO INVERSIONS: no measurement rung above truth beyond 1 x std_global;
           null strictly below the naive anchor (floor). Margins-vs-truth of
           non-visibility rungs are REPORTED as instrument resolution, not gated
           (v0.36-3: "cannot distinguish a 15% perturbation at current K/n/m" is
           an honest datum, not a failure).
     (ii)  VISIBILITY per operator, measured where its signature lives (v0.36-2,
           instrument-vs-stakes principle): heterogeneidad_latente -> the
           MOMENT-MATCHED ORACLE on the full grid >= thr_global;
           confounding_por_clase -> its PURE ABLATION on the OBSERVATIONAL
           sub-battery >= thr_local (the twin's local separation is reported --
           it measures what the (b) refit buys, it is a rival, not the probe).
     (iii) instrument diagnostic: oracle strictly below world.py >= thr_global.
  4. Sub-battery R is FIDELITY-ONLY (MDL is global and cancels; helper
     sub_battery_r) with anchors recomputed on the same sub-battery.
  5. Baseline at c_F=0 reports all gates per rung. c_F* = MINIMUM candidate
     passing all gates (if 0 passes, the anti-collapse guard fires ->
     investigate). Band x2 / /2; winner confirmation at B=20 (absolute std).
     The functional's binomial noise bounds c_F from above: if the minimum sits
     near that ceiling, report the SANDWICH.

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
from wager.factory.calibration import gate_threshold, sub_battery_r  # noqa: E402
from wager.reward.sandbox import SandboxedSubmission  # noqa: E402
from wager.reward.scorer import WorldSide, sandboxed_null_sample, score_submission  # noqa: E402
from wager.reward.seeds import derive_world_seed  # noqa: E402

C_F_GRID = [0.0, 0.25, 0.5, 1.0, 2.0, 4.0, 8.0]
GRID_SEED0 = 91001
B_SWEEP = 10   # std estimation at the c_F extremes (pre-fixed thresholds)
B_WINNER = 20  # confirmation at the winner
MID_RUNG = "rung_5_ablate_heterogeneity"   # middle of the 7 degradation rungs
ORACLE = "rung_6_oracle_moments"
CONF_ABL = "rung_3_ablate_confounding"
CONF_TWIN = "rung_4_twin_confounding"
NAIVE = "rung_7_naive_fit"
NULL = "rung_8_null"


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


def score_set(world_sample, battery, meta, params, c_f, sandboxes, null_code, which=None):
    """Score a set of rungs on one battery seed-set at one c_F.

    Returns (R_full per rung, reports per rung, denom)."""
    with sandboxed_null_sample(null_code, meta.column_names, params.model_call_timeout_s) as null_sample:
        ws = WorldSide(world_sample, battery, meta.column_names, params.n_samples,
                       null_sample=null_sample, functionals=meta.stakes.functionals, c_f=c_f)
        reports = {}
        for name, sb in sandboxes.items():
            if which is not None and name not in which:
                continue
            reports[name] = score_submission(sb.code, ws, params, sandbox=sb)
    s_truth, s_naive = reports["world"].raw_score, reports[NAIVE].raw_score
    denom = s_truth - s_naive
    r = {name: (rep.raw_score - s_naive) / denom for name, rep in reports.items()}
    return r, reports, denom


def stds_at(world_sample, battery, meta, params, c_f, sandboxes, null_code, obs_idx, b_total):
    """Absolute std over B resampled seed-sets of: R(mid) full, R(oracle) full,
    R_obs(confounding ablation) on the observational sub-battery."""
    which = ("world", NAIVE, MID_RUNG, ORACLE, CONF_ABL)
    r_mid, r_ora, r_loc = [], [], []
    for b in range(1, b_total + 1):
        r, reports, _ = score_set(world_sample, resampled(battery, b), meta, params, c_f,
                                  sandboxes, null_code, which=which)
        r_mid.append(r[MID_RUNG])
        r_ora.append(r[ORACLE])
        r_loc.append(sub_battery_r(reports[CONF_ABL], reports["world"], reports[NAIVE], obs_idx))
    def sd(v):
        return float(np.std(v, ddof=1))
    return {"mid": (sd(r_mid), float(np.mean(r_mid))),
            "oracle": (sd(r_ora), float(np.mean(r_ora))),
            "conf_local": (sd(r_loc), float(np.mean(r_loc)))}


def evaluate_gates(r_full, r_obs_abl, thr_global, thr_local, std_global):
    meas = [k for k in r_full if k not in ("world", NAIVE, NULL)]
    inversions = {k: r_full[k] > 1.0 + std_global for k in meas}
    gate_i = (not any(inversions.values())) and (r_full[NULL] < 0.0)
    vis_het = (1.0 - r_full[ORACLE]) >= thr_global
    vis_conf = (1.0 - r_obs_abl) >= thr_local
    gate_ii = vis_het and vis_conf
    gate_iii = (1.0 - r_full[ORACLE]) >= thr_global
    return {"i": gate_i, "inversions": inversions, "null_floor": r_full[NULL] < 0.0,
            "ii": gate_ii, "ii_hetero_oracle": vis_het, "ii_conf_local": vis_conf,
            "iii": gate_iii, "all": gate_i and gate_ii and gate_iii}


def main():
    t0 = time.perf_counter()
    meta, world_source, rungs, params = load_case()
    battery = calibration_grid()
    null_code = rungs[NULL]
    obs_idx = [i for i, it in enumerate(battery.items) if "dose" not in it.regime.config]

    import importlib.util
    spec = importlib.util.spec_from_file_location("world_v1", CASE_DIR / "world.py")
    world_mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(world_mod)
    world_sample = world_mod.sample

    codes = {"world": world_source, **rungs}
    print(f"grid: {len(battery.items)} items (obs sub-battery: {len(obs_idx)}), seeds {GRID_SEED0}..")

    sandboxes = {}
    try:
        for name, code in codes.items():
            sb = SandboxedSubmission(code, meta.column_names, timeout_s=params.model_call_timeout_s)
            sb.__enter__()
            sb.code = code
            sandboxes[name] = sb

        # --- thresholds fixed BEFORE the sweep (absolute std, both extremes) ----
        s_lo = stds_at(world_sample, battery, meta, params, C_F_GRID[0], sandboxes, null_code, obs_idx, B_SWEEP)
        s_hi = stds_at(world_sample, battery, meta, params, C_F_GRID[-1], sandboxes, null_code, obs_idx, B_SWEEP)
        thr_global = gate_threshold([s_lo["mid"][0], s_hi["mid"][0]])
        thr_local = gate_threshold([s_lo["conf_local"][0], s_hi["conf_local"][0]])
        print(f"\nabsolute stds (B={B_SWEEP}):")
        for lbl, s in (("c_F=0", s_lo), ("c_F=8", s_hi)):
            print(f"  {lbl}: std(R_mid)={s['mid'][0]:.4f} (mean {s['mid'][1]:.3f})  "
                  f"std(R_oracle)={s['oracle'][0]:.4f} (mean {s['oracle'][1]:.3f})  "
                  f"std(R_obs conf)={s['conf_local'][0]:.4f} (mean {s['conf_local'][1]:.3f})")
        print(f"  thr_global = {thr_global:.4f}   thr_local = {thr_local:.4f}   "
              f"[std(R_oracle) reported as investigation data, not a gate]")

        # --- sweep ---------------------------------------------------------------
        results = {}
        for c_f in C_F_GRID:
            r, reports, denom = score_set(world_sample, battery, meta, params, c_f, sandboxes, null_code)
            r_obs_abl = sub_battery_r(reports[CONF_ABL], reports["world"], reports[NAIVE], obs_idx)
            r_obs_twin = sub_battery_r(reports[CONF_TWIN], reports["world"], reports[NAIVE], obs_idx)
            g = evaluate_gates(r, r_obs_abl, thr_global, thr_local, s_lo["mid"][0])
            results[c_f] = {"R": r, "R_obs_conf_abl": r_obs_abl, "R_obs_conf_twin": r_obs_twin,
                            "denom": denom, "gates": g}
            flag = "PASS" if g["all"] else "fail"
            print(f"\nc_F={c_f:<5} denom={denom:.4f}  i={g['i']} ii={g['ii']} "
                  f"(het/oracle={g['ii_hetero_oracle']} conf/local={g['ii_conf_local']}) "
                  f"iii={g['iii']}  -> {flag}")
            for name in codes:
                sep = 1.0 - r[name]
                print(f"    R({name}) = {r[name]:+.3f}   sep={sep:+.3f}")
            print(f"    R_obs(conf ablation) = {r_obs_abl:+.3f} (local sep {1 - r_obs_abl:+.3f} vs thr {thr_local:.3f})"
                  f"   R_obs(conf twin) = {r_obs_twin:+.3f} [reported]")

        # --- baseline + resolution report ---------------------------------------
        base = results[0.0]
        print("\nBASELINE c_F=0 (v0.36 gates):")
        print(f"  oracle: sep={1 - base['R'][ORACLE]:.4f} vs thr_global={thr_global:.4f} -> "
              f"{'separates (guard: investigate if c_F*=0)' if (1 - base['R'][ORACLE]) >= thr_global else 'does NOT separate (as designed)'}")
        print(f"  conf ablation (obs sub-battery): sep={1 - base['R_obs_conf_abl']:.4f} vs thr_local={thr_local:.4f} -> "
              f"{'separates' if (1 - base['R_obs_conf_abl']) >= thr_local else 'does NOT separate'}")
        print("\nINSTRUMENT RESOLUTION (margins vs truth, reported not gated):")
        for name in (f"rung_2_perturbed", CONF_ABL, CONF_TWIN):
            print(f"  {name}: {1 - base['R'][name]:.4f} (K/n/m = {len(battery.items)}/{params.n_samples}/{params.m_reps})")

        # --- c_F* ----------------------------------------------------------------
        passing = [c for c in C_F_GRID if results[c]["gates"]["all"]]
        report = {"thr_global": thr_global, "thr_local": thr_local,
                  "stds": {"c_f_0": s_lo, "c_f_8": s_hi},
                  "results": {str(c): {"R": results[c]["R"],
                                       "R_obs_conf_abl": results[c]["R_obs_conf_abl"],
                                       "R_obs_conf_twin": results[c]["R_obs_conf_twin"],
                                       "denom": results[c]["denom"],
                                       "gates": {k: v for k, v in results[c]["gates"].items() if k != "inversions"}}
                              for c in C_F_GRID}}
        if not passing:
            print("\nNO candidate passes all gates -> investigate (do NOT retune the grid).")
        else:
            c_star = min(passing)
            print(f"\nc_F* = {c_star} (minimum passing; passing set: {passing})")
            if c_star == 0.0:
                print("  ANTI-COLLAPSE GUARD: c_F*=0 -> the functional would be unnecessary on this "
                      "grid; pre-registered response: INVESTIGATE (std(R_oracle) above is the first datum).")
            for lbl, cb in (("x2", c_star * 2), ("/2", c_star / 2)):
                if cb in results:
                    print(f"  band {lbl} (c_F={cb}): all gates = {results[cb]['gates']['all']}")
                elif cb > 0:
                    r, reports, _ = score_set(world_sample, battery, meta, params, cb, sandboxes, null_code)
                    ro = sub_battery_r(reports[CONF_ABL], reports["world"], reports[NAIVE], obs_idx)
                    gb = evaluate_gates(r, ro, thr_global, thr_local, s_lo["mid"][0])
                    print(f"  band {lbl} (c_F={cb}): all gates = {gb['all']}")
            s_win = stds_at(world_sample, battery, meta, params, c_star, sandboxes, null_code, obs_idx, B_WINNER)
            print(f"  winner confirmation (B={B_WINNER}): std(R_mid)={s_win['mid'][0]:.4f}  "
                  f"std(R_oracle)={s_win['oracle'][0]:.4f}  std(R_obs conf)={s_win['conf_local'][0]:.4f}")
            if 3 * s_win["mid"][0] > thr_global:
                print("  SANDWICH check: winner std exceeds the pre-fixed threshold basis -> report as finding.")
            report.update({"c_star": c_star, "stds_winner": s_win})
        out = CASE_DIR / "calibration_report.json"
        out.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
        print(f"\nreport -> {out}  ({time.perf_counter() - t0:.1f}s)")
    finally:
        for sb in sandboxes.values():
            sb.__exit__(None, None, None)


if __name__ == "__main__":
    main()
