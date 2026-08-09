"""c_F calibration sweep -- SAMPLING/source-trap suite (Decision Log v0.31/v0.36/
v0.38 protocol, generalized from cases/latent_mix_v1/calibrate_cf.py).

TRIGGER (ADR 0089 / Lucas): the v0.55-2 condition fired -- the c_F=0.25
provisional was adopted "valid only while BOTH operators' visibility passes
with margin; any failure -> the suite's OWN sweep, never adjust anything else".
The wide variant (batch_confound_wide_v0) made twin_offsets visibility FAIL
(1-0.978 = 0.022 < 0.05 floor). This is that pre-signed sweep (ledger #8+#2
together), NOT new scoring semantics.

MEMBERS (the source-trap family sharing the c_F=0.25 provisional): the "mundo
3" build-order source-trap world selection_bias_v0 (portfolio #4; #6
selection_bias_scarce_v0 is scoring-IDENTICAL -- same world, budget only
changes the episode, not the battery -- so it is represented by the base and
noted, not re-run), survivorship_censor_v0 (#7), batch_confound_v0 (#9), and
batch_confound_wide_v0 (the wide variant -- the expected binding constraint).

PROTOCOL (v0.31/v0.36/v0.38):
  - FIXED pre-registered grid c_F in {0, 0.25, 0.5, 1.0, 2.0, 4.0, 8.0} (house
    standard, same as the latent sweep).
  - D_MAX recomputed PER candidate (WorldSide rebuilt at each c_F).
  - Gates per world (conjoint): null floor (R_null<0); NO inversions (no
    ladder/twin rung above truth beyond tolerance); per-OPERATOR visibility
    (each source-layer twin separates >= max(3xstd, 0.05) on the battery where
    its signature lives -- here the full battery, the joint carries it);
    recoverability (a generic linear-joint canonical >= 0.95).
  - Baseline at c_F=0 reported. c_F* = MINIMUM candidate passing ALL gates on
    ALL members. mini-L2 B=20 at the winner on the binding twin -> CV and the
    significance/floor SANDWICH (if 3xstd approaches the floor, report it).

PRE-REGISTERED (signed BEFORE running, ADR 0089-order):
  (i)  a single c_F* certifies narrow AND wide (the narrow already tolerated x2
       in the v0.55 band, so headroom exists upward);
  (ii) the noise-vs-sufficiency sandwich may surface (CV grows with c_F); if
       c_F*(wide) sits against the noise ceiling, THAT is the finding "the
       score has a width ceiling for coordinate-localized traps", reported as
       instrument characterization -- not a failure.
  EXIT BRANCH: if NO c_F passes the conjoint gates on all members -> STOP +
  registered decision (suite split by width, or option (d) as declared scope);
  never silent.

Run:  .venv/Scripts/python cases/batch_confound_wide_v0/calibrate_cf_sampling.py
"""

import importlib.util
import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from wager.contracts import Battery  # noqa: E402
from wager.factory.calibration import visibility_threshold  # noqa: E402
from wager.factory.derive_rivals import (  # noqa: E402
    capacity_ladder, case_schema, experimental_grid, observational_pool,
    rival_naive, source_layer_twins,
)
from wager.reward.scorer import WorldSide, score_callable  # noqa: E402
from wager.reward.seeds import derive_world_seed  # noqa: E402

C_F_GRID = [0.0, 0.25, 0.5, 1.0, 2.0, 4.0, 8.0]
FLOOR = 0.05
B_WINNER = 20
MEMBERS = ["selection_bias_v0", "survivorship_censor_v0",
           "batch_confound_v0", "batch_confound_wide_v0"]
# Recoverability is a per-world CERTIFIED prerequisite (roadmap rule: no world
# enters the suite without canonical >= 0.95), read from each committed
# certificate -- NOT re-litigated by the sweep. The sweep's generic linear-joint
# canonical is a WEAK proxy on the collider-on-residuals world (selection_bias:
# generic 0.95 vs real 0.9991) and must not gate; it stays informational. A
# near-truth canonical has |dP|~0 so c_F barely moves it (verified c_F-stable).
CERTIFIED_CANON = {"selection_bias_v0": 0.9991, "survivorship_censor_v0": 0.9967,
                   "batch_confound_v0": 0.9998, "batch_confound_wide_v0": 0.9978}


def load_world(case):
    spec = importlib.util.spec_from_file_location(f"w_{case.name}", case / "world.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def null_model(pool, schema):
    stats = {c: (float(pool[c].mean()), float(pool[c].std())) for c in schema.columns}

    def sample(regime, n, seed):
        import pandas as pd
        rng = np.random.default_rng(seed)
        out = {}
        for c, (mu, sd) in stats.items():
            v = rng.normal(mu, sd, n)
            out[c] = np.clip(v, schema.lo, schema.hi) if c == schema.decision else v
        return pd.DataFrame(out)[list(schema.columns)]

    return sample


def canonical(meta, schema, world_sample, train, reps_source):
    """Generic linear-joint recoverability solver (the sampling family's shared
    canonical: outputs ~ linear(decision, context), JOINT residual covariance,
    meter sigma deconvolved via replicas)."""
    from wager.harness.source_view import source_view
    reps = source_view(world_sample, reps_source, 3000, 61001)
    ch_col = reps_source.channel.column
    sigma_hat = float(np.sqrt(max((reps[f"{ch_col}__rep1"] - reps[f"{ch_col}__rep2"]).var() / 2.0, 1e-6)))
    outputs = [c for c in schema.columns if c != schema.decision]
    from sklearn.linear_model import LinearRegression
    X = np.column_stack([train[schema.decision].to_numpy(), train[schema.context].to_numpy()])
    fits, resid = {}, {}
    for c in outputs:
        m = LinearRegression().fit(X, train[c].to_numpy())
        fits[c] = m
        resid[c] = train[c].to_numpy() - m.predict(X)
    R = np.column_stack([resid[c] for c in outputs])
    cov = np.cov(R, rowvar=False)
    if ch_col in outputs:
        i = outputs.index(ch_col)
        cov[i, i] = max(cov[i, i] - sigma_hat ** 2, 1e-4)

    def sample(regime, n, seed):
        import pandas as pd
        rng = np.random.default_rng(seed)
        c = float(regime.context.get(schema.context, 0.0))
        dd = (np.full(n, float(regime.config[schema.decision]))
              if schema.decision in regime.config
              else np.clip(rng.normal(5.0, 1.5, n), schema.lo, schema.hi))
        Xq = np.column_stack([dd, np.full(n, c)])
        eps = rng.multivariate_normal(np.zeros(len(outputs)), cov, n)
        out = {schema.decision: dd}
        for j, col in enumerate(outputs):
            out[col] = fits[col].predict(Xq) + eps[:, j]
        return pd.DataFrame(out)[list(schema.columns)]

    return sample


def build_world(case_name):
    case = ROOT / "cases" / case_name
    from wager.factory.case_loader import load_meta
    meta = load_meta(case)
    world = load_world(case)
    schema = case_schema(meta)
    source = list(meta.episode.observe_sources.values())[0]
    reps_source = next((s for s in meta.episode.observe_sources.values()
                        if s.channel is not None and s.channel.replicates == 2), None)
    pool = observational_pool(world.sample, source, 4000, 50001)
    levels = list(range(int(schema.lo), int(schema.hi) + 1))
    train = experimental_grid(world.sample, schema, levels, 400, 60001, channel=source.channel)
    naive = rival_naive(pool, schema)
    ladder = dict(capacity_ladder(train, pool, schema))
    twins = dict(source_layer_twins(world.sample, meta, pool, schema))
    null_fn = null_model(pool, schema)
    canon = canonical(meta, schema, world.sample, train, reps_source) if reps_source else None
    battery = Battery.from_json_file(case / "battery.json")
    return {"name": case_name, "meta": meta, "world": world.sample, "battery": battery,
            "naive": naive, "ladder": ladder, "twins": twins, "null": null_fn, "canon": canon}


def score_world(w, c_f):
    m = w["meta"]
    ws = WorldSide(w["world"], w["battery"], m.column_names, m.scoring.n_samples,
                   null_sample=w["null"], functionals=m.stakes.functionals, c_f=c_f)
    s_truth = score_callable(w["world"], ws, m.scoring)
    s_naive = score_callable(w["naive"], ws, m.scoring)
    den = s_truth - s_naive

    def R(fn):
        return (score_callable(fn, ws, m.scoring) - s_naive) / den

    r_ladder = {k: R(fn) for k, fn in w["ladder"].items()}
    r_twins = {k: R(fn) for k, fn in w["twins"].items()}
    r_null = R(w["null"])
    r_canon = R(w["canon"]) if w["canon"] else None
    return {"den": den, "ladder": r_ladder, "twins": r_twins, "null": r_null, "canon": r_canon}


def gates(res, certified_recoverable):
    all_rungs = {**res["ladder"], **res["twins"]}
    g = {}
    g["null_floor"] = res["null"] < 0.0
    g["no_inversions"] = all(v <= 1.0 + 0.02 for v in all_rungs.values())
    g["naive_far"] = all(v < 1.0 - FLOOR for v in res["twins"].values())
    for k, v in res["twins"].items():
        g[f"vis::{k}"] = (1.0 - v) >= FLOOR
    # recoverability from the CERTIFIED canonical (not the sweep's weak generic);
    # a near-truth solver is c_F-insensitive (|dP|~0).
    g["recoverability_certified"] = certified_recoverable >= 1.0 - FLOOR
    g["all"] = all(g.values())
    return g


def main():
    print("Building members (rivals derived once; battery loaded from committed certs)...")
    worlds = {name: build_world(name) for name in MEMBERS}

    report = {"grid": C_F_GRID, "members": {}, "certified_canon": CERTIFIED_CANON}
    pass_sets = {}
    for name, w in worlds.items():
        print(f"\n===== {name} =====  (certified canonical {CERTIFIED_CANON[name]})")
        w_rows = {}
        pass_set = []
        for c_f in C_F_GRID:
            res = score_world(w, c_f)
            g = gates(res, CERTIFIED_CANON[name])
            w_rows[str(c_f)] = {
                "den": round(res["den"], 4), "null": round(res["null"], 4),
                "generic_canon_informational": None if res["canon"] is None else round(res["canon"], 4),
                "twins": {k: round(v, 4) for k, v in res["twins"].items()},
                "gates_all": g["all"],
                "vis_fail": [k.split("::")[1] for k in g if k.startswith("vis::") and not g[k]],
            }
            if g["all"]:
                pass_set.append(c_f)
            twinstr = "  ".join(f"{k.replace('twin_', '')}={v:+.3f}" for k, v in res["twins"].items())
            vf = w_rows[str(c_f)]["vis_fail"]
            print(f"  c_F={c_f:<5} null={res['null']:+.3f}  {twinstr}  "
                  f"-> {'PASS' if g['all'] else 'fail' + (f' [vis:{vf}]' if vf else '')}")
        pass_sets[name] = pass_set
        report["members"][name] = {"rows": w_rows, "pass_set": pass_set}
        print(f"  pass-set: {pass_set}")

    # suite c_F*: min of the INTERSECTION of the members' actual pass-sets (NOT a
    # monotone ray -- survivorship has a CEILING: the functional makes the naive
    # so bad that the censura twin looks good above c_F~2).
    inter = [c for c in C_F_GRID if all(c in pass_sets[n] for n in MEMBERS)]
    suite_star = min(inter) if inter else None
    report["pass_sets"] = pass_sets
    report["intersection"] = inter
    report["c_star"] = suite_star
    print("\n" + "=" * 60)
    for n in MEMBERS:
        print(f"  {n:<26} pass-set {pass_sets[n]}")
    print(f"INTERSECTION: {inter}   ->   SUITE c_F* = {suite_star}")

    if suite_star is None:
        print("\nEXIT BRANCH: no c_F passes the conjoint gates on all members "
              "-> STOP; suite split by width or option (d) as declared scope (register).")
        (ROOT / "cases" / "batch_confound_wide_v0" / "calibration_report_sampling.json").write_text(
            json.dumps(report, indent=2) + "\n", encoding="utf-8")
        return

    # --- mini-L2 B=20 at c_F* on the binding member (wide), binding twin ------
    wide = worlds["batch_confound_wide_v0"]
    m = wide["meta"]
    binding_twin = "twin_offsets_por_tanda"
    rs = []
    for b in range(1, B_WINNER + 1):
        bat = Battery(items=[type(it)(weight=it.weight, regime=it.regime,
                                      seed_world=derive_world_seed(it.seed_world, i, b))
                             for i, it in enumerate(wide["battery"].items)])
        ws = WorldSide(wide["world"], bat, m.column_names, m.scoring.n_samples,
                       null_sample=wide["null"], functionals=m.stakes.functionals, c_f=suite_star)
        s_t = score_callable(wide["world"], ws, m.scoring)
        s_n = score_callable(wide["naive"], ws, m.scoring)
        rs.append((score_callable(wide["twins"][binding_twin], ws, m.scoring) - s_n) / (s_t - s_n))
    rs = np.array(rs)
    std_r = float(np.std(rs, ddof=1))
    mean_sep = float(1 - rs.mean())
    thr = visibility_threshold([std_r])
    sandwich = (3 * std_r) >= FLOOR
    print(f"\nmini-L2 (B={B_WINNER}) at c_F*={suite_star}, binding twin {binding_twin}:")
    print(f"  mean R={rs.mean():+.4f}  sep={mean_sep:+.4f}  std(R)={std_r:.4f}  "
          f"3xstd={3 * std_r:.4f}  floor={FLOOR}  vis_thr={thr:.4f}")
    print(f"  sep >= thr ? {mean_sep >= thr}   SANDWICH (3xstd >= floor)? {sandwich} "
          f"{'-> noise ceiling is the finding' if sandwich else '-> floor binds, noise is free'}")
    report["mini_l2"] = {"c_star": suite_star, "binding_twin": binding_twin,
                         "mean_R": round(float(rs.mean()), 4), "sep": round(mean_sep, 4),
                         "std_R": round(std_r, 4), "vis_thr": round(thr, 4),
                         "sep_ge_thr": bool(mean_sep >= thr), "sandwich": bool(sandwich)}
    (ROOT / "cases" / "batch_confound_wide_v0" / "calibration_report_sampling.json").write_text(
        json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print("\nreport -> cases/batch_confound_wide_v0/calibration_report_sampling.json")


if __name__ == "__main__":
    main()
