"""P2 2x2 table (pre-registered: Decision Log v0.29/v0.31/v0.38/v0.39).

Reads EVERYTHING from the v0.39 pre-registration: fresh shared probe grid
(seeds 95001+, uniform weights, mix out to +-2.5 -- beyond experimentable),
standardized (d-exp) access (fixed factorial 6 doses x 5 experimentable mixes,
n=250/cell, seeds 60001+, 18,000 budget units <= the agent's 20,000, RivalAccess
standardized=true), (d-obs) = observational pool n=4000 seed 50001, frozen
c_F=0.25 from each meta, gaps in BOTH units (R and |dP|), energy/functional
decomposition, mechanistic gap in both worlds, x2 band. The interpretation tree
is SIGNED in v0.39 -- the numbers only choose the branch.

Run:  .venv/Scripts/python cases/mendel_subtypes_v1/p2_table.py
"""

import json
import sys
from pathlib import Path
from types import SimpleNamespace

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from wager.contracts import Battery, BatteryItem, RivalAccess  # noqa: E402
from wager.contracts.world import Regime  # noqa: E402
from wager.factory.case_loader import load_meta, load_world_sample  # noqa: E402
from wager.factory.derive_rivals import (  # noqa: E402
    build_standard_rivals, capacity_ladder, case_schema, experimental_grid,
    observational_pool, rival_naive,
)
from wager.reward.functionals import functional_value  # noqa: E402
from wager.reward.scorer import WorldSide, regime_to_namespace, score_callable  # noqa: E402
from wager.reward.seeds import derive_seed  # noqa: E402

DEXP_LEVELS = [0.0, 2.0, 4.0, 6.0, 8.0, 10.0]   # v0.39 standard
DEXP_N, DEXP_SEED0 = 250, 60001
DOBS_N, DOBS_SEED = 4000, 50001


def null_model(pool, schema):
    """Null MODEL (independent pool marginals) for the D_MAX reference -- the
    v0.12 rule: NEVER the permutation fallback (it conserves marginals and
    shrinks D_MAX until everything caps; that exact pathology produced the
    all-capped collapse of P2 runs 1-2, Decision Log v0.42)."""
    stats = {c: (float(pool[c].mean()), float(pool[c].std())) for c in schema.columns}

    def sample(regime, n, seed):
        rng = np.random.default_rng(seed)
        out = {}
        for c, (mu, sd) in stats.items():
            v = rng.normal(mu, sd, n)
            out[c] = np.clip(v, schema.lo, schema.hi) if c == schema.decision else v
        import pandas as pd
        return pd.DataFrame(out)

    return sample


def p2_grid(schema) -> Battery:
    items, s = [], 95001
    for d in (0.0, 2.0, 4.0, 6.0, 8.0, 10.0):
        for m in (-2.5, -1.5, 0.0, 1.5, 2.5):
            items.append(BatteryItem(weight=1.0, regime=Regime(
                config={schema.decision: d}, context={schema.context: m}), seed_world=s))
            s += 1
    for m in (-1.0, 0.0, 1.0):
        items.append(BatteryItem(weight=1.0, regime=Regime(
            config={}, context={schema.context: m}), seed_world=s))
        s += 1
    return Battery(items=items)


def delta_p(fn, world_sample, battery, spec, n, base_seed=97001):
    """|dP| of the declared exceedance functional, rival vs truth, per item."""
    ds = []
    for i, it in enumerate(battery.items):
        ns = regime_to_namespace(it.regime)
        pt = functional_value(spec, world_sample(ns, n, it.seed_world))
        pr = functional_value(spec, fn(ns, n, derive_seed(it.seed_world, 3)))
        ds.append(abs(pr - pt))
    return float(np.mean(ds)), float(np.max(ds))


def run_case(case_dir):
    meta = load_meta(case_dir)
    schema = case_schema(meta)
    world_sample = load_world_sample(case_dir)
    source = list(meta.episode.observe_sources.values())[0]
    pool = observational_pool(world_sample, source, DOBS_N, DOBS_SEED)
    train = experimental_grid(world_sample, schema, DEXP_LEVELS, DEXP_N, DEXP_SEED0)
    dexp = capacity_ladder(train, pool, schema)                 # (d-exp) ladder
    pool_train = pool.copy()
    pool_train[schema.context] = float(source.context[schema.context])
    dobs = capacity_ladder(pool_train, pool, schema)            # (d-obs) ladder
    naive = rival_naive(pool, schema)

    battery = p2_grid(schema)
    null_fn = null_model(pool, schema)
    out = {}
    for c_f, tag in ((meta.scoring.c_f, "frozen"), (meta.scoring.c_f * 2, "x2")):
        ws = WorldSide(world_sample, battery, meta.column_names, meta.scoring.n_samples,
                       null_sample=null_fn, functionals=meta.stakes.functionals, c_f=c_f)
        s_truth = score_callable(world_sample, ws, meta.scoring)
        s_naive = score_callable(naive, ws, meta.scoring)
        den = s_truth - s_naive

        def R(fn):
            return (score_callable(fn, ws, meta.scoring) - s_naive) / den

        r_dexp = {k: R(fn) for k, fn in dexp}
        r_dobs = {k: R(fn) for k, fn in dobs}
        best_dexp = max(r_dexp, key=r_dexp.get)
        best_dobs_r = max(max(r_dobs.values()), 0.0)  # (a) naive anchors 0
        # energy/functional decomposition for the best (d-exp) member at this c_F
        ws_e = WorldSide(world_sample, battery, meta.column_names, meta.scoring.n_samples,
                         null_sample=null_fn, functionals=meta.stakes.functionals, c_f=0.0)
        s_truth_e = score_callable(world_sample, ws_e, meta.scoring)
        s_naive_e = score_callable(naive, ws_e, meta.scoring)
        fn_best = dict(dexp)[best_dexp]
        gap_energy = 1.0 - (score_callable(fn_best, ws_e, meta.scoring) - s_naive_e) / (s_truth_e - s_naive_e)
        gap_comb = 1.0 - r_dexp[best_dexp]
        out[tag] = {
            "c_f": c_f, "denom": den,
            "R_dexp": r_dexp, "best_dexp": best_dexp,
            "theory_gap": gap_comb,
            "gap_energy_only": gap_energy,
            "functional_share": (gap_comb - gap_energy) / gap_comb if gap_comb else None,
            "R_dobs": r_dobs,
            "mechanistic_gap": 1.0 - best_dobs_r,
        }
    spec = meta.stakes.functionals[0]
    dp_mean, dp_max = delta_p(dict(dexp)[out["frozen"]["best_dexp"]], world_sample,
                              battery, spec, meta.scoring.n_samples)
    out["delta_p"] = {"mean": dp_mean, "max": dp_max}
    out["access"] = {
        "theory": RivalAccess(mode="experimental", n_rows=len(train), seed0=DEXP_SEED0,
                              grid=f"do({schema.decision}) x {len(DEXP_LEVELS)} x {len(schema.ctx_levels)} (standard v0.39)",
                              standardized=True).model_dump(),
        "mechanistic": RivalAccess(mode="observational", n_rows=DOBS_N, seed0=DOBS_SEED,
                                   standardized=True).model_dump(),
    }
    return out


def main():
    res = {}
    for case in ("mendel_subtypes_v0", "mendel_subtypes_v1"):
        res[case] = run_case(ROOT / "cases" / case)
        f = res[case]["frozen"]
        print(f"[{case}] theory_gap={f['theory_gap']:.3f} (energy-only {f['gap_energy_only']:.3f}, "
              f"functional share {f['functional_share'] if f['functional_share'] is None else round(f['functional_share'], 2)})  "
              f"mechanistic_gap={f['mechanistic_gap']:.3f}  best_dexp={f['best_dexp']}")
        print(f"    R_dexp={ {k: round(v, 3) for k, v in f['R_dexp'].items()} }")
        print(f"    |dP| mean={res[case]['delta_p']['mean']:.3f} max={res[case]['delta_p']['max']:.3f}   "
              f"x2: theory={res[case]['x2']['theory_gap']:.3f} mech={res[case]['x2']['mechanistic_gap']:.3f}")
    tg0 = res["mendel_subtypes_v0"]["frozen"]["theory_gap"]
    tg1 = res["mendel_subtypes_v1"]["frozen"]["theory_gap"]
    print(f"\n2x2: v0={tg0:.3f}  v1={tg1:.3f}  ratio={tg1 / tg0 if tg0 else float('inf'):.1f}x  "
          f"(tree: expected v0 SMALL / v1 LARGE >=3x and >= 0.05 floor)")
    (ROOT / "cases" / "mendel_subtypes_v1" / "p2_report.json").write_text(
        json.dumps(res, indent=2, default=str) + "\n", encoding="utf-8")
    print("report -> cases/mendel_subtypes_v1/p2_report.json")


if __name__ == "__main__":
    main()
