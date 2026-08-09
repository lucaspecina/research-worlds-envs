"""|dP| quadrant with per-regime localization (pre-registered, Decision Log v0.43-2).

Completes the 2x2 in the CLIENT's unit: per-regime |P_rival(scrap) - P_truth(scrap)|
for the BEST no-latent member of each world (run-3 report: v0 = marker_conditional,
v1 = hetero), on the SAME P2 grid (seeds 95001+). n=4000 per estimate (binomial
noise ~0.8pp; run-3 used n=1000 -- this is the precision pass, same seed base).

Pre-registered predictions (branches signed in v0.43-2):
  - v0-|dP| small EVERYWHERE;
  - v1-|dP| concentrated at |mix| > experimentable range (the 0.48 lives in deep
    shifts); the best member uses mix as covariate (true by construction).
If confirmed -> the v0-small/v1-large pattern HOLDS in the client's currency ->
world vindicated, branch (c) kappa-do-over activated. If v0-|dP| is also large
outside clamped deep shifts -> branches (a)/(b) activate and kappa WAITS.

Run:  .venv/Scripts/python cases/latent_mix_v1/p2_dp_quadrant.py
"""

import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "cases" / "latent_mix_v1"))

from wager.factory.case_loader import load_meta, load_world_sample  # noqa: E402
from wager.factory.derive_rivals import (  # noqa: E402
    capacity_ladder, case_schema, experimental_grid, observational_pool,
)
from wager.reward.functionals import functional_value  # noqa: E402
from wager.reward.scorer import regime_to_namespace  # noqa: E402
from wager.reward.seeds import derive_seed  # noqa: E402

from p2_table import DEXP_LEVELS, DEXP_N, DEXP_SEED0, DOBS_N, DOBS_SEED, p2_grid  # noqa: E402

N_DP = 4000
BEST = {"latent_mix_v0": "marker_conditional_no_latent",
        "latent_mix_v1": "hetero_no_latent"}


def main():
    out = {}
    for case, member in BEST.items():
        case_dir = ROOT / "cases" / case
        meta = load_meta(case_dir)
        schema = case_schema(meta)
        world_sample = load_world_sample(case_dir)
        source = list(meta.episode.observe_sources.values())[0]
        pool = observational_pool(world_sample, source, DOBS_N, DOBS_SEED)
        train = experimental_grid(world_sample, schema, DEXP_LEVELS, DEXP_N, DEXP_SEED0)
        fn = dict(capacity_ladder(train, pool, schema))[member]
        spec = meta.stakes.functionals[0]
        battery = p2_grid(schema)
        c_hi = max(abs(v) for v in schema.ctx_levels)  # experimentable boundary

        rows = []
        for it in battery.items:
            ns = regime_to_namespace(it.regime)
            pt = functional_value(spec, world_sample(ns, N_DP, it.seed_world))
            pr = functional_value(spec, fn(ns, N_DP, derive_seed(it.seed_world, 3)))
            m = ns.context.get(schema.context, 0.0)
            band = ("obs" if schema.decision not in ns.config
                    else "beyond-exp" if abs(m) > c_hi else "in-exp")
            rows.append({"dec": ns.config.get(schema.decision), "mix": m,
                         "band": band, "dP": abs(pr - pt), "P_truth": pt})
        by_band = {}
        for b in ("in-exp", "beyond-exp", "obs"):
            v = [r["dP"] for r in rows if r["band"] == b]
            by_band[b] = {"mean": float(np.mean(v)), "max": float(np.max(v)), "n": len(v)}
        worst = sorted(rows, key=lambda r: -r["dP"])[:6]
        out[case] = {"member": member, "by_band": by_band, "rows": rows}

        print(f"\n[{case}] best member = {member}")
        for b, s in by_band.items():
            print(f"   {b:10s} (n={s['n']:2d}): |dP| mean={s['mean']:.3f}  max={s['max']:.3f}")
        print("   worst regimes:")
        for r in worst:
            d = "obs" if r["dec"] is None else f"{r['dec']:.0f}"
            print(f"     dec={d:>3} mix={r['mix']:+.1f} [{r['band']:10s}]  |dP|={r['dP']:.3f}  (P_truth={r['P_truth']:.3f})")

    (ROOT / "cases" / "latent_mix_v1" / "p2_dp_quadrant.json").write_text(
        json.dumps(out, indent=2) + "\n", encoding="utf-8")
    print("\nreport -> cases/latent_mix_v1/p2_dp_quadrant.json")


if __name__ == "__main__":
    main()
