"""prior_sweetspot_v0 (#16): derived battery + L1 gates + certificates.

Queue ADR 0075, slot #16: the trustworthy-prior CONTROL (suite Prior). No
source traps; ONE mechanism operator (the curvature) whose innocent twin --
the linear believer, via the EXISTING rival_twin machinery -- extrapolates the
record's local slope straight past the optimum. Theory ~ 0 declared (the
d-exp ladder's poly member IS nearly the mechanism; standard).

PRE-REGISTERED (signed BEFORE running):
  - L1 order: truth(1) > perturbed_x1.15 > twin_optimo_no_lineal >= naive(0)
    > null (twin keeps the true joint structure, naive does not; both believe
    a line -- a near-tie is plausible and gets reported).
  - Visibility: the curvature separates >= 0.05 R via its twin (the battery's
    out-of-record band is where a line and a parabola disagree).
  - Recoverability: canonical (quadratic means + replicas deconvolution +
    joint residual covariance) >= 0.95.
  - Second currency: the record-believer OVERESTIMATES quality past the
    optimum (underprices rework exactly where the optimistic move goes) --
    reported at do(2)/do(6)/do(9).

Run:  .venv/Scripts/python cases/prior_sweetspot_v0/build_and_certify.py
"""

import json
import sys
from pathlib import Path
from types import SimpleNamespace

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
CASE = Path(__file__).parent
sys.path.insert(0, str(CASE))

import world  # noqa: E402

from wager.contracts import Battery  # noqa: E402
from wager.factory.battery_builder import build_battery  # noqa: E402
from wager.factory.case_loader import load_meta, load_world_sample  # noqa: E402
from wager.factory.derive_rivals import (  # noqa: E402
    capacity_ladder, case_schema, experimental_grid, observational_pool,
    rival_naive, rival_twin,
)
from wager.harness.source_view import source_view  # noqa: E402
from wager.reward.functionals import functional_value  # noqa: E402
from wager.reward.scorer import WorldSide, score_callable  # noqa: E402

FLOOR = 0.05


def null_model(pool, schema):
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


def perturbed_truth(factor=1.15):
    p = dict(world.PARAMS)
    for k in ("curvature", "u_coef", "signal_coef"):
        p[k] = p[k] * factor

    def sample(regime, n, seed):
        return world.mechanism(p, regime, n, seed)

    return sample


def canonical_with_replicas(meta, schema, world_sample, train):
    """Headroom (a): QUADRATIC means on the decision + context, replicas
    sigma deconvolution, joint residual covariance (#7/#9 pattern)."""
    reps_name = next(n for n, s in meta.episode.observe_sources.items()
                     if s.channel is not None and s.channel.replicates == 2)
    reps = source_view(world_sample, meta.episode.observe_sources[reps_name], 3000, 61001)
    ch_col = meta.episode.observe_sources[reps_name].channel.column
    sigma_hat = float(np.sqrt((reps[f"{ch_col}__rep1"] - reps[f"{ch_col}__rep2"]).var() / 2.0))

    outputs = [c for c in schema.columns if c != schema.decision]
    d = train[schema.decision].to_numpy()
    X = np.column_stack([d, d ** 2, train[schema.context].to_numpy()])
    from sklearn.linear_model import LinearRegression
    fits, resid = {}, {}
    for c in outputs:
        m = LinearRegression().fit(X, train[c].to_numpy())
        fits[c] = m
        resid[c] = train[c].to_numpy() - m.predict(X)
    R = np.column_stack([resid[c] for c in outputs])
    cov = np.cov(R, rowvar=False)
    i_ch = outputs.index(ch_col)
    cov[i_ch, i_ch] = max(cov[i_ch, i_ch] - sigma_hat ** 2, 1e-4)

    def sample(regime, n, seed):
        rng = np.random.default_rng(seed)
        c = float(regime.context.get(schema.context, 0.0))
        dd = (np.full(n, float(regime.config[schema.decision]))
              if schema.decision in regime.config
              else np.clip(rng.normal(world.PARAMS["driver_base"], world.PARAMS["driver_sd"], n),
                           schema.lo, schema.hi))
        Xq = np.column_stack([dd, dd ** 2, np.full(n, c)])
        eps = rng.multivariate_normal(np.zeros(len(outputs)), cov, n)
        import pandas as pd
        out = {schema.decision: dd}
        for j, col in enumerate(outputs):
            out[col] = fits[col].predict(Xq) + eps[:, j]
        return pd.DataFrame(out)[list(schema.columns)]

    sample.sigma_hat = sigma_hat
    return sample


def main():
    meta = load_meta(CASE)
    schema = case_schema(meta)
    world_sample = load_world_sample(CASE)
    source = list(meta.episode.observe_sources.values())[0]

    pool = observational_pool(world_sample, source, 4000, 50001)
    levels = list(range(int(schema.lo), int(schema.hi) + 1))
    train = experimental_grid(world_sample, schema, levels, 400, 60001, channel=source.channel)
    naive = rival_naive(pool, schema)
    ladder = capacity_ladder(train, pool, schema)
    op = meta.operators[0]
    twin = rival_twin(world.mechanism, world.PARAMS, meta, op, pool, schema)
    null_fn = null_model(pool, schema)

    rivals = [naive] + [fn for _, fn in ladder] + [twin]
    battery = build_battery(world_sample, rivals, null_fn, list(schema.columns),
                            meta.stakes, seed=314159)
    Battery.model_validate(battery.model_dump()).to_json_file(CASE / "battery.json")

    ws = WorldSide(world_sample, battery, meta.column_names, meta.scoring.n_samples,
                   null_sample=null_fn, functionals=meta.stakes.functionals,
                   c_f=meta.scoring.c_f)
    s_truth = score_callable(world_sample, ws, meta.scoring)
    s_naive = score_callable(naive, ws, meta.scoring)
    den = s_truth - s_naive

    def R(fn):
        return (score_callable(fn, ws, meta.scoring) - s_naive) / den

    rungs = {"perturbed_x1.15": perturbed_truth()}
    rungs.update(dict(ladder))
    rungs[f"twin_{op.name}"] = twin
    r = {k: R(fn) for k, fn in rungs.items()}
    r["null"] = R(null_fn)
    canonical = canonical_with_replicas(meta, schema, world_sample, train)
    r_canon = R(canonical)

    spec = meta.stakes.functionals[0]
    rework = {}
    for d in (2.0, 6.0, 9.0):
        ns = SimpleNamespace(config={schema.decision: d}, context={schema.context: 0.0}, horizon=None)
        rework[f"do{d:g}"] = {
            "truth": round(functional_value(spec, world_sample(ns, 4000, 424242)), 4),
            "naive": round(functional_value(spec, naive(ns, 4000, 424242)), 4),
        }

    report = {
        "denom_raw": den, "R": {k: round(v, 4) for k, v in r.items()},
        "R_canonical": round(r_canon, 4), "sigma_hat": round(canonical.sigma_hat, 4),
        "battery_k": len(battery.items),
        "rework_rate": rework,
        "gates": {},
    }
    g = report["gates"]
    believers = {k: v for k, v in r.items() if k.startswith("twin_")}
    g["naive_far"] = den > 0 and all(v < 1.0 - FLOOR for v in believers.values())
    g["no_inversions"] = all(v <= 1.0 + 0.02 for v in r.values())
    g["null_floor"] = r["null"] < 0.0
    g["vis_optimo"] = (1.0 - r[f"twin_{op.name}"]) >= FLOOR
    g["recoverability"] = r_canon >= 1.0 - FLOOR
    g["all"] = all(v for v in g.values())

    print(json.dumps(report, indent=2))
    (CASE / "certificates.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print("-> battery.json + certificates.json")


if __name__ == "__main__":
    main()
