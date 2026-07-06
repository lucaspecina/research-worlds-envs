"""Generic certification -- the verifier the proto-designer needs (ADR 0093).

Derives ALL rivals from meta + world module (no per-case hand-tooling) and runs
the standard gates, for any single-decision / single-context SCM world composed
from the operator library. Generalizes the per-case build_and_certify scripts
(selection/survivorship/batch/...). Zero-LLM (factory side).

certify(case_dir) -> report dict; writes battery.json + certificates.json +
ladder/rung_7_naive + rung_8_null.
"""

import json
from pathlib import Path
from types import SimpleNamespace

import numpy as np
import pandas as pd

from wager.contracts import Battery
from wager.factory.battery_builder import build_battery
from wager.factory.case_loader import load_meta, load_world_module
from wager.factory.derive_rivals import (
    capacity_ladder, case_schema, experimental_grid, free_knobs, observational_pool,
    rival_naive, rival_twin, source_layer_twins,
)
from wager.harness.source_view import source_view
from wager.reward.functionals import functional_value
from wager.reward.scorer import WorldSide, score_callable

FLOOR = 0.05


def _null_model(pool, schema):
    stats = {c: (float(pool[c].mean()), float(pool[c].std())) for c in schema.columns}

    def sample(regime, n, seed):
        rng = np.random.default_rng(seed)
        out = {}
        for c, (mu, sd) in stats.items():
            v = rng.normal(mu, sd, n)
            out[c] = np.clip(v, schema.lo, schema.hi) if c == schema.decision else v
        return pd.DataFrame(out)[list(schema.columns)]

    return sample


def _perturbed(wmod, meta, factor=1.15):
    keys = set()
    for op in meta.operators:
        keys |= set(op.knobs)
    p = dict(wmod.PARAMS)
    for k in keys:
        if k in p:
            p[k] = p[k] * factor

    def sample(regime, n, seed):
        return wmod.mechanism(p, regime, n, seed)

    return sample


def _canonical(meta, schema, world_sample):
    """Linear-joint recoverability solver: outputs ~ linear(decision, context),
    joint residual covariance, meter sigma deconvolved if a replicas source
    exists. The achievable ceiling for a de-confounding investigator."""
    reps_src = next((s for s in meta.episode.observe_sources.values()
                     if s.channel is not None and s.channel.replicates == 2), None)
    levels = list(range(int(schema.lo), int(schema.hi) + 1))
    src0 = list(meta.episode.observe_sources.values())[0]
    train = experimental_grid(world_sample, schema, levels, 400, 60001, channel=src0.channel)
    outputs = [c for c in schema.columns if c != schema.decision]
    # degree-2 in the decision (handles both linear confounding AND sweet-spot
    # curvature worlds; the quadratic term takes ~0 coef when unneeded)
    d_tr = train[schema.decision].to_numpy()
    X = np.column_stack([d_tr, d_tr ** 2, train[schema.context].to_numpy()])
    from sklearn.linear_model import LinearRegression
    fits, resid = {}, {}
    for c in outputs:
        m = LinearRegression().fit(X, train[c].to_numpy())
        fits[c] = m
        resid[c] = train[c].to_numpy() - m.predict(X)
    cov = np.cov(np.column_stack([resid[c] for c in outputs]), rowvar=False)
    cov = np.atleast_2d(cov)
    sigma_hat = 0.0
    if reps_src is not None:
        reps = source_view(world_sample, reps_src, 3000, 61001)
        ch = reps_src.channel.column
        sigma_hat = float(np.sqrt(max((reps[f"{ch}__rep1"] - reps[f"{ch}__rep2"]).var() / 2.0, 1e-6)))
        if ch in outputs:
            i = outputs.index(ch)
            cov[i, i] = max(cov[i, i] - sigma_hat ** 2, 1e-4)

    def sample(regime, n, seed):
        rng = np.random.default_rng(seed)
        c = float(regime.context.get(schema.context, 0.0))
        dd = (np.full(n, float(regime.config[schema.decision]))
              if schema.decision in regime.config
              else np.clip(rng.normal(5.0, 1.5, n), schema.lo, schema.hi))
        Xq = np.column_stack([dd, dd ** 2, np.full(n, c)])
        eps = rng.multivariate_normal(np.zeros(len(outputs)), cov, n)
        out = {schema.decision: dd}
        for j, col in enumerate(outputs):
            out[col] = fits[col].predict(Xq) + eps[:, j]
        return pd.DataFrame(out)[list(schema.columns)]

    sample.sigma_hat = sigma_hat
    return sample


def _write_fixtures(case_dir, pool, schema):
    cols = list(schema.columns)
    mu = [float(v) for v in pool[cols].mean().to_numpy()]
    cov = [[float(v) for v in row] for row in pool[cols].cov().to_numpy()]
    marg = {c: (float(pool[c].mean()), float(pool[c].std())) for c in cols}
    d = schema.decision
    naive = f'''"""Rung 7 -- naive joint Gaussian of the record (S_naive anchor, R=0). GENERATED."""
import numpy as np
import pandas as pd

COLS = {cols!r}
MU = np.array({mu!r})
COV = np.array({cov!r})
DEC = {d!r}


def model(regime, n, seed):
    rng = np.random.default_rng(seed)
    di = COLS.index(DEC)
    if DEC in regime.config:
        dv = float(regime.config[DEC]); keep = [i for i in range(len(COLS)) if i != di]
        mu_c = MU[keep] + COV[np.ix_(keep, [di])][:, 0] / COV[di, di] * (dv - MU[di])
        cov_c = COV[np.ix_(keep, keep)] - np.outer(COV[keep, di], COV[di, keep]) / COV[di, di]
        draw = rng.multivariate_normal(mu_c, cov_c, n)
        out = {{DEC: np.full(n, dv)}}
        for j, i in enumerate(keep):
            out[COLS[i]] = draw[:, j]
        return pd.DataFrame(out)[COLS]
    draw = rng.multivariate_normal(MU, COV, n)
    out = {{c: draw[:, i] for i, c in enumerate(COLS)}}
    out[DEC] = np.clip(out[DEC], 0.0, 10.0)
    return pd.DataFrame(out)[COLS]
'''
    null = f'''"""Rung 8 -- null: independent record marginals (S_null / D_MAX). GENERATED."""
import numpy as np
import pandas as pd

MARG = {marg!r}
DEC = {d!r}


def model(regime, n, seed):
    rng = np.random.default_rng(seed)
    out = {{}}
    for c, (mu, sd) in MARG.items():
        v = rng.normal(mu, sd, n)
        out[c] = np.clip(v, 0.0, 10.0) if c == DEC else v
    return pd.DataFrame(out)
'''
    ladder = case_dir / "ladder"
    ladder.mkdir(exist_ok=True)
    (ladder / "rung_7_naive_record.py").write_text(naive, encoding="utf-8", newline="\n")
    (ladder / "rung_8_null.py").write_text(null, encoding="utf-8", newline="\n")


def certify(case_dir) -> dict:
    case_dir = Path(case_dir)
    meta = load_meta(case_dir)
    wmod = load_world_module(case_dir)
    schema = case_schema(meta)
    world_sample = wmod.sample
    source = list(meta.episode.observe_sources.values())[0]

    pool = observational_pool(world_sample, source, 4000, 50001)
    levels = list(range(int(schema.lo), int(schema.hi) + 1))
    train = experimental_grid(world_sample, schema, levels, 400, 60001, channel=source.channel)
    naive = rival_naive(pool, schema)
    ladder = capacity_ladder(train, pool, schema)
    twins = []
    for op in meta.operators:
        if op.layer == "mechanism" and op.ablation:
            twins.append((f"twin_{op.name}", rival_twin(wmod.mechanism, wmod.PARAMS, meta, op, pool, schema)))
    twins += source_layer_twins(world_sample, meta, pool, schema)
    twins = dict(twins)
    null_fn = _null_model(pool, schema)

    rivals = [naive] + [fn for _, fn in ladder] + [fn for _, fn in twins.items()]
    battery = build_battery(world_sample, rivals, null_fn, list(schema.columns),
                            meta.stakes, seed=314159)
    # OBSERVATIONAL QUOTA (v0.36 / latent_mix doctrine): a MECHANISM-confounding
    # trap only shows on observational items (under do() truth==twin); the derived
    # battery can under-sample them. Guarantee a quota so the trap is measurable
    # where its signature lives.
    from wager.contracts import BatteryItem
    from wager.contracts.world import Regime
    has_mech = any(op.layer == "mechanism" and op.ablation for op in meta.operators)
    obs_n = sum(1 for it in battery.items if schema.decision not in it.regime.config)
    if has_mech and obs_n < 8:
        ctx = schema.context
        w = float(np.mean([it.weight for it in battery.items]))
        extra = []
        for j in range(8 - obs_n):
            shift = [-1.0, -0.5, 0.0, 0.5, 1.0, -1.5, 1.5, 0.0][j % 8]
            extra.append(BatteryItem(weight=w, regime=Regime(config={}, context={ctx: shift}),
                                     seed_world=880001 + j))
        battery = Battery(items=list(battery.items) + extra)
    Battery.model_validate(battery.model_dump()).to_json_file(case_dir / "battery.json")
    _write_fixtures(case_dir, pool, schema)

    ws = WorldSide(world_sample, battery, meta.column_names, meta.scoring.n_samples,
                   null_sample=null_fn, functionals=meta.stakes.functionals, c_f=meta.scoring.c_f)
    s_truth = score_callable(world_sample, ws, meta.scoring)
    s_naive = score_callable(naive, ws, meta.scoring)
    den = s_truth - s_naive

    def R(fn):
        return (score_callable(fn, ws, meta.scoring) - s_naive) / den if den else float("nan")

    r = {k: round(R(fn), 4) for k, fn in {**dict(ladder), **twins}.items()}
    r["perturbed_x1.15"] = round(R(_perturbed(wmod, meta)), 4)
    r["null"] = round(R(null_fn), 4)
    canon = _canonical(meta, schema, world_sample)
    r_canon = round(R(canon), 4)

    # Visibility is measured WHERE the operator's signature lives (v0.36 /
    # ADR 0077): MECHANISM-layer traps (confounding of the assignment) only show
    # on OBSERVATIONAL items (under do() truth==twin), so their visibility uses
    # the observational sub-battery; SOURCE-layer traps show in every regime
    # (v0.59) and use the full battery. r above is the full-battery R (reported);
    # r_vis is the visibility R per operator.
    mech_ops = {f"twin_{op.name}" for op in meta.operators if op.layer == "mechanism"}
    obs_idx = [i for i, it in enumerate(battery.items) if schema.decision not in it.regime.config]
    r_vis = dict(r)
    if mech_ops & set(twins) and len(obs_idx) >= 3:
        obs_bat = Battery(items=[battery.items[i] for i in obs_idx])
        ws_o = WorldSide(world_sample, obs_bat, meta.column_names, meta.scoring.n_samples,
                         null_sample=null_fn, functionals=meta.stakes.functionals, c_f=meta.scoring.c_f)
        st_o = score_callable(world_sample, ws_o, meta.scoring)
        sn_o = score_callable(naive, ws_o, meta.scoring)
        for k in mech_ops & set(twins):
            r_vis[k] = round((score_callable(twins[k], ws_o, meta.scoring) - sn_o) / (st_o - sn_o), 4)

    g = {}
    g["denom_positive"] = den > 0
    g["naive_far"] = den > 0 and all(r_vis[k] < 1.0 - FLOOR for k in twins)
    g["no_inversions"] = all(v <= 1.0 + 0.02 for v in r.values())
    g["null_floor"] = r["null"] < 0.0
    for k in twins:
        g[f"vis_{k}"] = (1.0 - r_vis[k]) >= FLOOR
    g["recoverability"] = r_canon >= 1.0 - FLOOR
    g["differential_load"] = len(twins) >= 1  # >=1 certified trap coordinate (>=2 for [T])
    g["all"] = all(g.values())

    report = {"denom_raw": round(den, 4), "R": r, "R_visibility": r_vis, "R_canonical": r_canon,
              "obs_items": len(obs_idx), "battery_k": len(battery.items),
              "twins": list(twins), "gates": g}
    (case_dir / "certificates.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    return report


if __name__ == "__main__":
    import sys
    print(json.dumps(certify(Path(sys.argv[1])), indent=2))
