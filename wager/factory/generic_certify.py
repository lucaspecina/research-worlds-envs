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
from wager.harness.source_view import experiment_view, source_view
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


CANONICAL_CLASS = "regime_factored_additive_context_v0"  # ADR 0120


def _partition_gate(vals, den_s, den_full):
    """Per-partition recoverability gate (ADR 0120): a partition is held to the
    0.95 bar only where it can MEASURE it. R on a ~zero denominator is noise,
    not measurement (observed live on confounded_gen_v0's obs cut: naive~truth
    there, den_obs = 1.3% of den_full, and the canonical's R_obs swung
    0.30->0.45 across acquisition seeds while its ABSOLUTE obs distance had
    collapsed). Where the partition denominator is uninformative (<10% of the
    full one) the claim shrinks to "no worse than the naive on that partition"
    -- which the OLD (pre-0120) canonical still fails (its obs R was deeply
    negative). vals = R values across acquisition seeds; the MIN governs."""
    if not vals or den_s is None:
        return None
    if abs(den_s) >= 0.10 * abs(den_full):
        return min(vals) >= 1.0 - FLOOR
    return min(vals) >= -FLOOR


def _source_is_identity(src) -> bool:
    """Positive ALLOWLIST (ADR 0120, ronda 3): the observational view equals the
    true joint ONLY if the source declares no corruption of any kind. Anything
    undeclared-but-corrupting is a contract violation, not a canonical problem."""
    return (src.channel is None and src.selection is None and src.censoring is None
            and src.batch is None and not src.hidden_columns)


def _legal_plan_v0(meta, *, want_pool: bool, reps_src) -> dict | None:
    """legal_plan_v0 -- explicit, VERSIONED shopping policy for the canonical
    (a policy, not a generic optimum). Recoverability is defined WITH the
    declared access/budget (certificates.md par.7), so the ceiling player must
    BUY every row it fits on. Preference: replicas (meter deconvolution, if the
    world sells a replicated channel) -> experimental grid -> observational
    pool. FAIL-CLOSED: returns None when even the minimum viable design
    (3 decision levels x 2 contexts x 50 rows) exceeds the budget."""
    budget = float(meta.episode.budget)
    src0 = list(meta.episode.observe_sources.values())[0]
    c_fix = float(meta.episode.experiment.cost_fixed)
    c_row = float(meta.episode.experiment.cost_per_row)
    remaining = budget
    reps_n, reps_cost = 0, 0.0
    if reps_src is not None:
        reps_n = min(1500, int(budget * 0.25 / float(reps_src.cost_per_row)))
        if reps_n < 200:
            reps_n = 0
        reps_cost = reps_n * float(reps_src.cost_per_row)
        remaining -= reps_cost
    for kd, kc in ((5, 3), (4, 2), (3, 2)):
        exp_money = remaining * (0.7 if want_pool else 0.95)
        rows = min(400, int((exp_money / (kd * kc) - c_fix) / c_row))
        if rows < 50:
            continue
        cost_exp = kd * kc * (c_fix + c_row * rows)
        pool_n = 0
        if want_pool:
            pool_n = min(2000, int((remaining - cost_exp) / float(src0.cost_per_row)))
            if pool_n < 300:
                continue
        cost = reps_cost + cost_exp + pool_n * float(src0.cost_per_row)
        if cost <= budget:
            return {"version": "legal_plan_v0", "d_levels": kd, "ctx_levels": kc,
                    "rows_per_cell": rows, "pool_n": pool_n, "reps_n": reps_n,
                    "cost": round(cost, 2), "budget": budget}
    return None


def _canonical_legal(meta, schema, world_sample, plan, obs_half, src0, reps_src,
                     seed_grid, seed_pool, seed_reps):
    """Recoverability ceiling under legal_plan_v0 (ADR 0120): the best BEHAVIORAL
    predictor a legal investigator could assemble -- NOT a unified causal model,
    and the certified claim is exactly that narrow.

    do() items: degree-2 fit in the decision + ADDITIVE context, on the bought
    grid (the quadratic term takes ~0 coef when unneeded). Observational items,
    ONLY for worlds with a mechanism-layer ablatable operator AND an identity
    source (`obs_half`): MVN joint of the BOUGHT pool over ALL columns -- which
    keeps the confounded assignment's coupling and the true decision width --
    plus the experimentally-identified additive context effect grafted onto the
    outputs (the pool is single-context; the battery's obs items are not).

    Declared class assumptions (ledgered; violations are
    `unsupported_by_canonical`, NEVER "the world is irrecoverable"): additive
    context on output means, no decision-x-context interaction (both guarded by
    the lack-of-fit check on bought data), obs decision/marker marginals
    context-invariant, residual covariance regime-invariant (unverifiable from
    legal access -- they are the TEMPLATE's contract)."""
    levels = np.linspace(schema.lo, schema.hi, plan["d_levels"])
    k_idx = np.unique(np.linspace(0, len(schema.ctx_levels) - 1,
                                  plan["ctx_levels"]).round().astype(int))
    ctx_levels = [schema.ctx_levels[i] for i in k_idx]
    frames = []
    s = seed_grid
    for lv in levels:
        for c in ctx_levels:
            ns = SimpleNamespace(config={schema.decision: float(lv)},
                                 context={schema.context: float(c)}, horizon=None)
            df = experiment_view(world_sample, ns, src0.channel,
                                 plan["rows_per_cell"], s).copy()
            df[schema.context] = c
            frames.append(df)
            s += 1
    train = pd.concat(frames, ignore_index=True)

    outputs = [c for c in schema.columns if c != schema.decision]
    d_tr = train[schema.decision].to_numpy()
    X = np.column_stack([d_tr, d_tr ** 2, train[schema.context].to_numpy()])
    from sklearn.linear_model import LinearRegression
    fits, resid = {}, {}
    for c in outputs:
        m = LinearRegression().fit(X, train[c].to_numpy())
        fits[c] = m
        resid[c] = train[c].to_numpy() - m.predict(X)
    cov = np.atleast_2d(np.cov(np.column_stack([resid[c] for c in outputs]), rowvar=False))

    # lack-of-fit of the declared class on the BOUGHT grid: max standardized
    # per-cell mean residual across cells x outputs. Loose bound by design
    # (30-ish tests -> null max-z ~3; 6.0 only catches gross class violations).
    lof_stat = 0.0
    cells = train.groupby([train[schema.decision].round(6),
                           train[schema.context]]).indices
    for idx in cells.values():
        n_c = len(idx)
        for c in outputs:
            sd = float(np.std(resid[c])) or 1e-9
            z = abs(float(np.mean(resid[c][idx]))) / (sd / np.sqrt(n_c))
            lof_stat = max(lof_stat, z)
    supported = bool(lof_stat < 6.0)

    sigma_hat = 0.0
    if reps_src is not None and plan["reps_n"]:
        reps = source_view(world_sample, reps_src, plan["reps_n"], seed_reps)
        ch = reps_src.channel.column
        sigma_hat = float(np.sqrt(max((reps[f"{ch}__rep1"] - reps[f"{ch}__rep2"]).var() / 2.0, 1e-6)))
        if ch in outputs:
            i = outputs.index(ch)
            cov[i, i] = max(cov[i, i] - sigma_hat ** 2, 1e-4)

    pool = None
    if obs_half and plan["pool_n"]:
        pool = observational_pool(world_sample, src0, plan["pool_n"], seed_pool)
        cols = list(schema.columns)
        mu_pool = pool[cols].mean().to_numpy()
        cov_pool = pool[cols].cov().to_numpy()
        pool_ctx = float(src0.context.get(schema.context, 0.0))
        gamma = np.array([0.0 if c == schema.decision else float(fits[c].coef_[2])
                          for c in cols])

    def sample(regime, n, seed):
        rng = np.random.default_rng(seed)
        c = float(regime.context.get(schema.context, 0.0))
        if schema.decision in regime.config:
            dd = np.full(n, float(regime.config[schema.decision]))
        elif pool is not None:
            draw = rng.multivariate_normal(mu_pool + gamma * (c - pool_ctx), cov_pool, n)
            out = {}
            for j, col in enumerate(schema.columns):
                v = draw[:, j]
                out[col] = np.clip(v, schema.lo, schema.hi) if col == schema.decision else v
            return pd.DataFrame(out)[list(schema.columns)]
        else:
            # legacy_v0 obs draw (pre-ADR-0120), kept ONLY for worlds outside
            # the identity-source confounding class; their own legal obs class
            # is open debt (D10). Regression-guarded by reskin_pilot_v0.
            dd = np.clip(rng.normal(5.0, 1.5, n), schema.lo, schema.hi)
        Xq = np.column_stack([dd, dd ** 2, np.full(n, c)])
        eps = rng.multivariate_normal(np.zeros(len(outputs)), cov, n)
        out = {schema.decision: dd}
        for j, col in enumerate(outputs):
            out[col] = fits[col].predict(Xq) + eps[:, j]
        return pd.DataFrame(out)[list(schema.columns)]

    diag = {"sigma_hat": round(sigma_hat, 4), "lack_of_fit_z": round(lof_stat, 2),
            "supported": supported}
    return sample, diag


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

    # sub-batteries (obs / do): consumed by BOTH the visibility measurement and
    # the per-partition recoverability gates (ADR 0120 -- full+obs alone can
    # hide an obs-easy/do-broken canonical, so do() gets its own gate).
    obs_idx = [i for i, it in enumerate(battery.items) if schema.decision not in it.regime.config]
    do_idx = [i for i in range(len(battery.items)) if i not in obs_idx]

    def _sub_ws(idx):
        sub = Battery(items=[battery.items[i] for i in idx])
        ws_s = WorldSide(world_sample, sub, meta.column_names, meta.scoring.n_samples,
                         null_sample=null_fn, functionals=meta.stakes.functionals, c_f=meta.scoring.c_f)
        st = score_callable(world_sample, ws_s, meta.scoring)
        sn = score_callable(naive, ws_s, meta.scoring)
        return ws_s, st, sn

    sub_obs = _sub_ws(obs_idx) if len(obs_idx) >= 3 else None
    sub_do = _sub_ws(do_idx) if len(do_idx) >= 3 else None

    def R_sub(fn, sub):
        ws_s, st, sn = sub
        return (score_callable(fn, ws_s, meta.scoring) - sn) / (st - sn) if st != sn else float("nan")

    # ---- canonical under legal_plan_v0 (ADR 0120) ------------------------------
    reps_src = next((s for s in meta.episode.observe_sources.values()
                     if s.channel is not None and s.channel.replicates == 2), None)
    has_mech_abl = any(op.layer == "mechanism" and op.ablation for op in meta.operators)
    obs_half = has_mech_abl and _source_is_identity(source)
    plan = _legal_plan_v0(meta, want_pool=obs_half, reps_src=reps_src)
    canon_ledger = {"class": CANONICAL_CLASS, "obs_half": obs_half, "plan": plan}
    rec_obs = rec_do = None
    if plan is None:
        r_canon = None
        supported = False
        rec_full = False
        canon_ledger["note"] = ("no_legal_plan: minimum viable design exceeds the "
                                "declared budget (fail-closed)")
    else:
        acq_seeds = [(62001, 52001, 63001), (62501, 52501, 63501)]
        per_seed = {"full": [], "obs": [], "do": []}
        diags = []
        for sg, sp, sr in acq_seeds:
            canon, diag = _canonical_legal(meta, schema, world_sample, plan, obs_half,
                                           source, reps_src, sg, sp, sr)
            per_seed["full"].append(round(R(canon), 4))
            if sub_obs:
                per_seed["obs"].append(round(R_sub(canon, sub_obs), 4))
            if sub_do:
                per_seed["do"].append(round(R_sub(canon, sub_do), 4))
            diags.append(diag)
        r_canon = min(per_seed["full"])  # seed-robustness: the MIN governs
        supported = all(d["supported"] for d in diags)
        rec_full = supported and r_canon >= 1.0 - FLOOR

        if obs_half and per_seed["obs"]:
            rec_obs = supported and bool(_partition_gate(
                per_seed["obs"], sub_obs[1] - sub_obs[2], den))
        if per_seed["do"]:
            rec_do = supported and bool(_partition_gate(
                per_seed["do"], sub_do[1] - sub_do[2], den))
        canon_ledger.update({
            "acq_seeds": acq_seeds, "r_per_seed": per_seed, "diag_per_seed": diags,
            "partition_denoms": {
                "full": round(den, 6),
                "obs": round(sub_obs[1] - sub_obs[2], 6) if sub_obs else None,
                "do": round(sub_do[1] - sub_do[2], 6) if sub_do else None,
            },
            "note": None if supported else (
                "unsupported_by_canonical: lack-of-fit of the declared class on "
                "bought data (NOT proof the world is irrecoverable)"),
        })

    # Visibility is measured WHERE the operator's signature lives (v0.36 /
    # ADR 0077): MECHANISM-layer traps (confounding of the assignment) only show
    # on OBSERVATIONAL items (under do() truth==twin), so their visibility uses
    # the observational sub-battery; SOURCE-layer traps show in every regime
    # (v0.59) and use the full battery. r above is the full-battery R (reported);
    # r_vis is the visibility R per operator.
    mech_ops = {f"twin_{op.name}" for op in meta.operators if op.layer == "mechanism"}
    r_vis = dict(r)
    if mech_ops & set(twins) and sub_obs:
        ws_o, st_o, sn_o = sub_obs
        for k in mech_ops & set(twins):
            r_vis[k] = round((score_callable(twins[k], ws_o, meta.scoring) - sn_o) / (st_o - sn_o), 4)

    g = {}
    g["denom_positive"] = den > 0
    g["naive_far"] = den > 0 and all(r_vis[k] < 1.0 - FLOOR for k in twins)
    g["no_inversions"] = all(v <= 1.0 + 0.02 for v in r.values())
    g["null_floor"] = r["null"] < 0.0
    for k in twins:
        g[f"vis_{k}"] = (1.0 - r_vis[k]) >= FLOOR
    g["recoverability"] = bool(rec_full)
    if rec_do is not None:
        g["recoverability_do"] = bool(rec_do)
    if rec_obs is not None:
        g["recoverability_obs"] = bool(rec_obs)
    g["differential_load"] = len(twins) >= 1  # >=1 certified trap coordinate (>=2 for [T])
    g["all"] = all(g.values())

    report = {"denom_raw": round(den, 4), "R": r, "R_visibility": r_vis, "R_canonical": r_canon,
              "canonical": canon_ledger,
              "obs_items": len(obs_idx), "battery_k": len(battery.items),
              "twins": list(twins), "gates": g}
    (case_dir / "certificates.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    return report


if __name__ == "__main__":
    import sys
    print(json.dumps(certify(Path(sys.argv[1])), indent=2))
