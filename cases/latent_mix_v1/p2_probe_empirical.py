"""Empirical-residual probe -- the CLOSING round of the strengthen-rivals arc
(pre-registered: Decision Log v0.45-2; three signed outcomes A/B/C).

Runs the practical SUPREMUM of the admissible no-latent class
(`empirical_residual_no_latent`) through: R on the P2 grid (both worlds, frozen
c_F, full ladder -- order re-check), per-regime |dP| by band (the quadrant lens),
and the LOCALIZATION of v0's worst cell (dec=4, mix=0):
  (c1) is the TRUE conditional given FINE marker unimodal? -> min excess
       kurtosis across marker deciles (Gaussian ~0; two-point bimodal ~ -2)
  (c2) is the Gaussian member's dP there sigma-misallocation or tail shape?
       -> dP_shape = |P_gaussfine - P_truth| (best possible Gaussian residual
          given fine marker) vs dP_sigma = dP_member_gaussian - dP_shape.

Run:  .venv/Scripts/python cases/latent_mix_v1/p2_probe_empirical.py
"""

import json
import sys
from pathlib import Path
from types import SimpleNamespace

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "cases" / "latent_mix_v1"))

from scipy import stats  # noqa: E402

from wager.factory.case_loader import load_meta, load_world_sample  # noqa: E402
from wager.factory.derive_rivals import (  # noqa: E402
    capacity_ladder, case_schema, experimental_grid, observational_pool, rival_naive,
)
from wager.reward.functionals import functional_value  # noqa: E402
from wager.reward.scorer import WorldSide, regime_to_namespace, score_callable  # noqa: E402
from wager.reward.seeds import derive_seed  # noqa: E402

from p2_table import DEXP_LEVELS, DEXP_N, DEXP_SEED0, DOBS_N, DOBS_SEED, null_model, p2_grid  # noqa: E402

MEMBER = "empirical_residual_no_latent"
N_DP = 4000


def run_case(case):
    case_dir = ROOT / "cases" / case
    meta = load_meta(case_dir)
    schema = case_schema(meta)
    world_sample = load_world_sample(case_dir)
    source = list(meta.episode.observe_sources.values())[0]
    pool = observational_pool(world_sample, source, DOBS_N, DOBS_SEED)
    train = experimental_grid(world_sample, schema, DEXP_LEVELS, DEXP_N, DEXP_SEED0)
    ladder = capacity_ladder(train, pool, schema)
    battery = p2_grid(schema)
    ws = WorldSide(world_sample, battery, meta.column_names, meta.scoring.n_samples,
                   null_sample=null_model(pool, schema),
                   functionals=meta.stakes.functionals, c_f=meta.scoring.c_f)
    s_truth = score_callable(world_sample, ws, meta.scoring)
    s_naive = score_callable(rival_naive(pool, schema), ws, meta.scoring)
    den = s_truth - s_naive
    r_all = {k: (score_callable(fn, ws, meta.scoring) - s_naive) / den for k, fn in ladder}

    fn = dict(ladder)[MEMBER]
    spec = meta.stakes.functionals[0]
    c_hi = max(abs(v) for v in schema.ctx_levels)
    rows = []
    for it in battery.items:
        ns = regime_to_namespace(it.regime)
        pt = functional_value(spec, world_sample(ns, N_DP, it.seed_world))
        pr = functional_value(spec, fn(ns, N_DP, derive_seed(it.seed_world, 3)))
        m = ns.context.get(schema.context, 0.0)
        band = ("obs" if schema.decision not in ns.config
                else "beyond-exp" if abs(m) > c_hi else "in-exp")
        rows.append({"dec": ns.config.get(schema.decision), "mix": m, "band": band,
                     "dP": abs(pr - pt), "P_truth": pt})
    by_band = {b: {"mean": float(np.mean([r["dP"] for r in rows if r["band"] == b])),
                   "max": float(np.max([r["dP"] for r in rows if r["band"] == b]))}
               for b in ("in-exp", "beyond-exp", "obs")}
    print(f"\n[{case}] R({MEMBER}) = {r_all[MEMBER]:+.3f}   (ladder R: "
          + ", ".join(f"{k.split('_no_latent')[0]}={v:.3f}" for k, v in r_all.items()) + ")")
    for b, s in by_band.items():
        print(f"   {b:10s}: |dP| mean={s['mean']:.3f}  max={s['max']:.3f}")
    worst = sorted(rows, key=lambda r: -r["dP"])[:4]
    for r in worst:
        d = "obs" if r["dec"] is None else f"{r['dec']:.0f}"
        print(f"     worst: dec={d:>3} mix={r['mix']:+.1f} [{r['band']}]  |dP|={r['dP']:.3f}")
    return {"R": r_all, "by_band": by_band, "rows": rows,
            "ladder_fns": ladder, "meta": meta, "schema": schema, "world": world_sample}


def localization_v0(res0):
    """(c1)/(c2) at v0's worst cell dec=4, mix=0 (Decision Log v0.45-2c)."""
    meta, schema, world_sample = res0["meta"], res0["schema"], res0["world"]
    spec = meta.stakes.functionals[0]
    ns = SimpleNamespace(config={schema.decision: 4.0}, context={schema.context: 0.0}, horizon=None)
    t = world_sample(ns, 40000, 424242)
    thr = spec.threshold
    p_t = float((t["outcome"] < thr).mean())
    deciles = np.quantile(t["marker"], np.linspace(0, 1, 11))
    idx = np.clip(np.searchsorted(deciles, t["marker"].to_numpy()) - 1, 0, 9)
    kurts, p_gauss_fine = [], 0.0
    for i in range(10):
        o = t["outcome"].to_numpy()[idx == i]
        kurts.append(float(stats.kurtosis(o)))  # excess: Gaussian ~0, 2-point ~ -2
        p_gauss_fine += stats.norm.cdf((thr - o.mean()) / (o.std() or 1e-9)) / 10.0
    dp_shape = abs(float(p_gauss_fine) - p_t)
    mc = dict(res0["ladder_fns"])["marker_conditional_no_latent"]
    p_mc = float((mc(ns, 40000, 515151)["outcome"] < thr).mean())
    dp_member_gauss = abs(p_mc - p_t)
    print(f"\n[LOCALIZACION v0 dec=4 mix=0]  P_truth={p_t:.3f}")
    print(f"  (c1) min excess kurtosis across fine-marker deciles = {min(kurts):.2f} "
          f"(Gaussian ~0; two-point bimodal ~ -2)")
    print(f"  (c2) dP_shape (best Gaussian residual given fine marker) = {dp_shape:.3f}")
    print(f"       dP_member_gaussian (marker_conditional) = {dp_member_gauss:.3f} "
          f"-> sigma/conditioning part = {dp_member_gauss - dp_shape:+.3f}")
    return {"P_truth": p_t, "min_kurt": min(kurts), "dP_shape": dp_shape,
            "dP_member_gauss": dp_member_gauss}


def main():
    out = {}
    res = {}
    for case in ("latent_mix_v0", "latent_mix_v1"):
        res[case] = run_case(case)
        out[case] = {k: res[case][k] for k in ("R", "by_band", "rows")}
    out["localizacion_v0"] = localization_v0(res["latent_mix_v0"])
    (ROOT / "cases" / "latent_mix_v1" / "p2_probe_empirical.json").write_text(
        json.dumps(out, indent=2, default=str) + "\n", encoding="utf-8")
    print("\nreport -> cases/latent_mix_v1/p2_probe_empirical.json")
    print("Salidas firmadas (v0.45-2b): A = v0 cierra + v1 falla beyond-exp -> kappa re-abre;")
    print("B = v0 no cierra -> mundo/funcional; C = ambos cierran -> clase agotada -> v2 ACTIVO.")


if __name__ == "__main__":
    main()
