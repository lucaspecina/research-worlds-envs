"""v2 certification: anchor parity, gap(n_cal) curve, unknowable tax, L1-small.

Pre-registered (v0.63, signed in autonomy): grid = dose {2,4,6,8} x n_cal
{2,4,8,16,32,64}, uniform weights, seeds 96001+; ceiling = Bayes posterior
predictive (R must be exactly 1 by anchor construction, scored via the SAME
pipeline); plug-in = the mandatory rival the TRUE theory gap is measured
against, expected to lose most at SMALL n_cal and EXTREME hidden mixes; the
oracle-with-mix (illegal player) is diagnostic-only, R_uncl > 1 expected --
ceiling<->oracle distance = the tax of the unknowable, reported per n_cal.
L1-v2 at n_cal = 4 (signed): order bayes(1) > plugin > pooled(0) > null; the
convergence of plugin -> ceiling at LARGE n_cal is design, not failure.

Run:  .venv/Scripts/python cases/latent_mix_v2/certify_v2.py
"""

import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
CASE = Path(__file__).parent
sys.path.insert(0, str(CASE))

import anchors  # noqa: E402
import world  # noqa: E402

from wager.contracts import Battery, BatteryItem, CaseMeta  # noqa: E402
from wager.contracts.world import Regime  # noqa: E402
from wager.factory.calibration import sub_battery_r  # noqa: E402
from wager.reward.functionals import functional_value  # noqa: E402
from wager.reward.scorer import WorldSide, score_callable  # noqa: E402
from wager.reward.seeds import derive_seed  # noqa: E402

N_CALS = [2, 4, 8, 16, 32, 64]
DOSES = [2.0, 4.0, 6.0, 8.0]
SEED0 = 96001
L1_NCAL = 4


def grid_battery() -> Battery:
    items, s = [], SEED0
    for nc in N_CALS:
        for d in DOSES:
            items.append(BatteryItem(weight=1.0, regime=Regime(
                config={"dose": d}, context={"n_cal": float(nc)}), seed_world=s))
            s += 1
    return Battery(items=items)


def raw_score_via_pipeline(fn, ws, params, seed_of_item=None):
    """Same per-item semantics as score_callable, but allows a DIAGNOSTIC
    player that receives the item's WORLD seed (the illegal oracle)."""
    weights = np.array([it.weight for it in ws.battery.items], dtype=float)
    weights = weights / weights.sum()
    fid = 0.0
    for idx, item in enumerate(ws.battery.items):
        ts, fs, dmax = ws.truth_sides[idx], ws.func_scorers[idx], ws.d_maxes[idx]
        ns = ws.regimes[idx]
        d = 0.0
        for j in range(params.m_reps):
            seed_m = derive_seed(item.seed_world, j)
            arg_seed = item.seed_world if seed_of_item else seed_m
            pred = fn(ns, params.n_samples, arg_seed) if seed_of_item else fn(ns, params.n_samples, seed_m)
            dist = min(ts.distance_to(pred) + fs.extra_distance(pred), dmax)
            d += dist / params.m_reps
        fid -= float(weights[idx]) * d
    return fid


def main():
    meta = CaseMeta.from_json_file(CASE / "meta.json")
    params = meta.scoring
    battery = grid_battery()
    bayes = anchors.bayes_ceiling(meta)
    plugin = anchors.plugin_player(meta)
    pooled = anchors.pooled_naive()
    null_fn = anchors.null_marginals()

    def oracle(ns, n, seed_world):  # ILLEGAL player: reads the lot's true mix
        return world.mechanism_given_mix(world.PARAMS, world.lot_mix(seed_world), ns, n,
                                         derive_seed(seed_world, 0))

    ws = WorldSide(world.sample, battery, meta.column_names, params.n_samples,
                   null_sample=null_fn, functionals=meta.stakes.functionals,
                   c_f=params.c_f, enrich_regime=anchors.enrich)
    s_bayes = score_callable(bayes, ws, params)
    s_pooled = score_callable(pooled, ws, params)
    s_null = score_callable(null_fn, ws, params)
    s_plugin = score_callable(plugin, ws, params)
    s_oracle = raw_score_via_pipeline(oracle, ws, params, seed_of_item=True)
    den = s_bayes - s_pooled

    def R(s):
        return (s - s_pooled) / den

    print(f"PARIDAD (v0.63-3): R(techo Bayes) = {R(s_bayes):.6f}  (debe ser 1.000000)")
    print(f"R(plugin)={R(s_plugin):+.4f}  R(pooled)=0  R(null)={R(s_null):+.4f}  "
          f"R_uncl(oracle ILEGAL)={R(s_oracle):+.4f}  denom={den:.4f}")

    # --- gap(n_cal) curve + tax, per slice (local fidelity-only R) -----------
    from wager.reward.scorer import score_submission  # noqa: F401 (parity of imports)
    per = {}
    spec = meta.stakes.functionals[0]
    for nc in N_CALS:
        idxs = [i for i, it in enumerate(battery.items) if it.regime.context["n_cal"] == nc]
        rows = {}
        for name, fn, item_seed in (("bayes", bayes, False), ("plugin", plugin, False),
                                    ("pooled", pooled, False), ("oracle", oracle, True)):
            fid = 0.0
            for i in idxs:
                it = battery.items[i]
                ns, ts, fs, dmax = ws.regimes[i], ws.truth_sides[i], ws.func_scorers[i], ws.d_maxes[i]
                d = 0.0
                for j in range(params.m_reps):
                    sm = it.seed_world if item_seed else derive_seed(it.seed_world, j)
                    pred = fn(ns, params.n_samples, sm)
                    d += min(ts.distance_to(pred) + fs.extra_distance(pred), dmax) / params.m_reps
                fid -= d / len(idxs)
            rows[name] = fid
        den_l = rows["bayes"] - rows["pooled"]
        gap = (rows["bayes"] - rows["plugin"]) / den_l
        tax = (rows["oracle"] - rows["bayes"]) / den_l
        # client currency at this n_cal: plugin |dP| vs truth
        dps = []
        for i in idxs:
            it = battery.items[i]
            ns = ws.regimes[i]
            pt = functional_value(spec, world.sample(ns, 4000, it.seed_world))
            pp = functional_value(spec, plugin(ns, 4000, derive_seed(it.seed_world, 5)))
            dps.append(abs(pp - pt))
        per[nc] = {"gap_plugin": round(float(gap), 4), "tax_unknowable": round(float(tax), 4),
                   "dP_plugin_mean": round(float(np.mean(dps)), 4),
                   "dP_plugin_max": round(float(np.max(dps)), 4)}
        print(f"n_cal={nc:>3}: gap(plugin)={gap:+.4f}  tax={tax:+.4f}  "
              f"|dP|plugin mean={np.mean(dps):.3f} max={np.max(dps):.3f}")

    # --- L1-v2 at n_cal=4 (signed): local R for the four LEGAL players --------
    def local_fid(fn, idxs):
        fid = 0.0
        for i in idxs:
            it = battery.items[i]
            ns, ts, fs, dmax = ws.regimes[i], ws.truth_sides[i], ws.func_scorers[i], ws.d_maxes[i]
            d = 0.0
            for j in range(params.m_reps):
                pred = fn(ns, params.n_samples, derive_seed(it.seed_world, j))
                d += min(ts.distance_to(pred) + fs.extra_distance(pred), dmax) / params.m_reps
            fid -= d / len(idxs)
        return fid

    idxs4 = [i for i, it in enumerate(battery.items) if it.regime.context["n_cal"] == L1_NCAL]
    f4 = {name: local_fid(fn, idxs4) for name, fn in
          (("bayes", bayes), ("plugin", plugin), ("pooled", pooled), ("null", null_fn))}
    den4 = f4["bayes"] - f4["pooled"]
    r4 = {k: (v - f4["pooled"]) / den4 for k, v in f4.items()}
    order_ok = r4["bayes"] > r4["plugin"] > r4["pooled"] > r4["null"]
    print(f"\nL1-v2 (n_cal={L1_NCAL}): bayes={r4['bayes']:+.4f} plugin={r4['plugin']:+.4f} "
          f"pooled={r4['pooled']:+.4f} null={r4['null']:+.4f}  orden firmado "
          f"{'CUMPLIDO' if order_ok else 'VIOLADO'}")

    # --- DIAGNOSTIC robustness probe (NOT the signed battery; seeds 98001+) ---
    # gap(n_cal) above rides on 4 lots/slice; here 16 lots/slice x dose 5.0 to
    # separate signal from lot-luck. Reported as diagnostic-only.
    diag = {}
    print("\nSonda diagnostica (16 lotes/slice, seeds 98001+, dose=5):")
    for k, nc in enumerate(N_CALS):
        items_d = [BatteryItem(weight=1.0, regime=Regime(
            config={"dose": 5.0}, context={"n_cal": float(nc)}), seed_world=98001 + 100 * k + i)
            for i in range(16)]
        ws_d = WorldSide(world.sample, Battery(items=items_d), meta.column_names,
                         params.n_samples, null_sample=null_fn,
                         functionals=meta.stakes.functionals, c_f=params.c_f,
                         enrich_regime=anchors.enrich)
        fids = {}
        for name, fn in (("bayes", bayes), ("plugin", plugin), ("pooled", pooled)):
            fid = 0.0
            for i, it in enumerate(items_d):
                ns, ts, fs, dmax = ws_d.regimes[i], ws_d.truth_sides[i], ws_d.func_scorers[i], ws_d.d_maxes[i]
                d = 0.0
                for j in range(params.m_reps):
                    pred = fn(ns, params.n_samples, derive_seed(it.seed_world, j))
                    d += min(ts.distance_to(pred) + fs.extra_distance(pred), dmax) / params.m_reps
                fid -= d / len(items_d)
            fids[name] = fid
        gd = (fids["bayes"] - fids["plugin"]) / (fids["bayes"] - fids["pooled"])
        diag[nc] = round(float(gd), 4)
        print(f"  n_cal={nc:>3}: gap(plugin) diagnostico = {gd:+.4f}")

    report = {"R_global": {"bayes": R(s_bayes), "plugin": R(s_plugin), "null": R(s_null),
                           "oracle_uncl": R(s_oracle)}, "denom": den, "per_n_cal": per,
              "L1_ncal4": {"R": {k: round(float(v), 4) for k, v in r4.items()},
                           "order_ok": bool(order_ok)},
              "diagnostic_gap_16lots": diag}
    (CASE / "certificates.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    battery.to_json_file(CASE / "battery.json")
    txt = (CASE / "battery.json").read_text(encoding="utf-8")
    assert "cal_window" not in txt, "VENTANA PERSISTIDA (violacion v0.63-4)"
    print("battery.json sin ventana OK ; certificates.json escrito")


if __name__ == "__main__":
    main()
