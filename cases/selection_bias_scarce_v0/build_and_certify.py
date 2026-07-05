"""selection_bias_scarce_v0: derived battery + L1 gates + certificates.

E1-matrix slot #6 (Decision Log v0.61/v0.63): the SAME world as
selection_bias_v0 recomposed as a budget-scarcity SIBLING -- episode budget
/4 (20000 -> 5000) and replicated source x3 price (5 -> 15/row). A NEW case
with its own re-derived certificates (variant, never a post-certification
knob); the scoring surface is identical by construction (same world, same
operators, same c_f) -- what changes is the EPISODE economy. The case tests
"difficulty-by-budget vs difficulty-by-composition" on a world the frontier
already saturated at full budget (v0.60: R=0.974/0.993).

Everything derives from meta/schema; pre-registered signatures checked:
  - L1: the naive anchors FAR (routed pool; without routing it would collapse).
  - Visibility (c_f=0.25 condition, v0.55-2): BOTH operators separate at the
    resolution floor (0.05 R). Collider note (registered deviation v0.59): the
    signed sub-battery said observational + do(signal), but `signal` is not
    settable in the authored world -- the edge-twin's signature lives in the
    signal<->outcome JOINT, visible in every regime, so its sub-battery is the
    full battery (v0.36 principle: measured where the signature CAN show).
  - Recoverability/headroom (a): canonical-with-replicas solver ~ world.py
    (sigma_med from Var(rep1-rep2)/2, deconvolved residual scale).

Run:  .venv/Scripts/python cases/selection_bias_v0/build_and_certify.py
"""

import json
import sys
from pathlib import Path
from types import SimpleNamespace

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
CASE = Path(__file__).parent

from wager.contracts import Battery  # noqa: E402
from wager.factory.battery_builder import build_battery  # noqa: E402
from wager.factory.case_loader import load_meta, load_world_module, load_world_sample  # noqa: E402
from wager.factory.derive_rivals import (  # noqa: E402
    capacity_ladder, case_schema, experimental_grid, observational_pool,
    rival_naive, source_layer_twins,
)
from wager.harness.source_view import source_view  # noqa: E402
from wager.reward.scorer import WorldSide, score_callable  # noqa: E402

FLOOR = 0.05  # resolution floor (v0.38); std measured only if a gate lands near it


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


def perturbed_truth(wmod, factor=1.15):
    p = dict(wmod.PARAMS)
    for k in ("signal_coef", "outcome_coef", "shift_coef"):
        p[k] = p[k] * factor

    def sample(regime, n, seed):
        return wmod.mechanism(p, regime, n, seed)

    return sample


def canonical_with_replicas(meta, schema, world_sample, train):
    """The achievable ceiling solver (headroom slot (a), v0.57-3a): fits smooth
    means on the metered experimental grid, estimates sigma_med from the
    replicated source (Var(rep1-rep2)/2), DECONVOLVES it from the outcome
    residual scale, and models the remaining outputs' clean structure."""
    reps_name = next(n for n, s in meta.episode.observe_sources.items()
                     if s.channel is not None and s.channel.replicates == 2)
    reps = source_view(world_sample, meta.episode.observe_sources[reps_name], 3000, 61001)
    ch_col = meta.episode.observe_sources[reps_name].channel.column
    sigma_hat = float(np.sqrt((reps[f"{ch_col}__rep1"] - reps[f"{ch_col}__rep2"]).var() / 2.0))

    outputs = [c for c in schema.columns if c != schema.decision]
    d = train[schema.decision].to_numpy()
    ctx = train[schema.context].to_numpy()
    X = np.column_stack([d, ctx])
    fits, resid = {}, {}
    from sklearn.linear_model import LinearRegression
    for c in outputs:
        m = LinearRegression().fit(X, train[c].to_numpy())
        fits[c] = m
        resid[c] = train[c].to_numpy() - m.predict(X)
    scales = {c: float(np.std(resid[c])) for c in outputs}
    scales[ch_col] = float(np.sqrt(max(scales[ch_col] ** 2 - sigma_hat ** 2, 1e-4)))
    dec_pool = train[schema.decision].to_numpy()

    def sample(regime, n, seed):
        rng = np.random.default_rng(seed)
        c = float(regime.context.get(schema.context, 0.0))
        dd = (np.full(n, float(regime.config[schema.decision]))
              if schema.decision in regime.config else rng.uniform(schema.lo, schema.hi, n))
        Xq = np.column_stack([dd, np.full(n, c)])
        import pandas as pd
        out = {schema.decision: dd}
        for col in outputs:
            out[col] = fits[col].predict(Xq) + rng.normal(0.0, scales[col], n)
        return pd.DataFrame(out)[list(schema.columns)]

    sample.sigma_hat = sigma_hat
    return sample


def main():
    meta = load_meta(CASE)
    schema = case_schema(meta)
    world_sample = load_world_sample(CASE)
    wmod = load_world_module(CASE)
    source = list(meta.episode.observe_sources.values())[0]

    pool = observational_pool(world_sample, source, 4000, 50001)
    levels = list(range(int(schema.lo), int(schema.hi) + 1))
    train = experimental_grid(world_sample, schema, levels, 400, 60001, channel=source.channel)
    naive = rival_naive(pool, schema)
    ladder = capacity_ladder(train, pool, schema)
    twins = source_layer_twins(world_sample, meta, pool, schema)
    null_fn = null_model(pool, schema)

    rivals = [naive] + [fn for _, fn in ladder] + [fn for _, fn in twins]
    battery = build_battery(world_sample, rivals, null_fn, list(schema.columns),
                            meta.stakes, seed=314159)
    Battery.model_validate(battery.model_dump()).to_json_file(CASE / "battery.json")
    obs_idx = [i for i, it in enumerate(battery.items) if schema.decision not in it.regime.config]

    ws = WorldSide(world_sample, battery, meta.column_names, meta.scoring.n_samples,
                   null_sample=null_fn, functionals=meta.stakes.functionals,
                   c_f=meta.scoring.c_f)
    s_truth = score_callable(world_sample, ws, meta.scoring)
    s_naive = score_callable(naive, ws, meta.scoring)
    den = s_truth - s_naive

    def R(fn):
        return (score_callable(fn, ws, meta.scoring) - s_naive) / den

    rungs = {"perturbed_x1.15": perturbed_truth(wmod)}
    rungs.update(dict(ladder))
    rungs.update(dict(twins))
    r = {k: R(fn) for k, fn in rungs.items()}
    r["null"] = R(null_fn)
    canonical = canonical_with_replicas(meta, schema, world_sample, train)
    r_canon = R(canonical)

    report = {
        "denom_raw": den, "R": {k: round(v, 4) for k, v in r.items()},
        "R_canonical": round(r_canon, 4), "sigma_hat": round(canonical.sigma_hat, 4),
        "battery_k": len(battery.items), "obs_items": len(obs_idx),
        "gates": {},
    }
    # L1 production gates: extremes + naive-far signature + no rung above truth
    report["gates"]["naive_far"] = den > 0 and all(v < 1.0 - FLOOR for k, v in r.items()
                                                   if k != "perturbed_x1.15")
    report["gates"]["no_inversions"] = all(v <= 1.0 + 0.02 for v in r.values())
    report["gates"]["null_floor"] = r["null"] < 0.0
    # visibility (c_f condition, v0.55-2): both operators at the FLOOR
    report["gates"]["vis_collider"] = (1.0 - r["twin_collider_seleccion"]) >= FLOOR
    report["gates"]["vis_medicion"] = (1.0 - r["twin_error_de_medicion"]) >= FLOOR
    # recoverability / headroom (a): canonical within a floor of the ceiling
    report["gates"]["recoverability"] = r_canon >= 1.0 - FLOOR
    report["gates"]["all"] = all(v for k, v in report["gates"].items())

    print(json.dumps(report, indent=2))
    (CASE / "certificates.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print("-> battery.json + certificates.json")


if __name__ == "__main__":
    main()
