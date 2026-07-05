"""Derive rivals from the declared case (factory side) -- the rival is DERIVED,
not authored (NORTH_STAR §4.4, ARCHITECTURE §5).

GENERALIZATION PASS (Decision Log v0.39): everything the derivation reads comes
from the case's DECLARED meta/schema -- decision variable from
stakes.decision_variables, context variable from the cheap source's declared
context, columns from meta.columns, bounds from the control surface, free
structural params from the operators' declared knobs. NEVER from name lists:
the "recites the dummy's schema" class (hardcoded `cohort` context + the twin
refit touching `effect_dose`, a key v1 does not have -> silently inert rival,
family #13) is killed as a class, not per symptom. The structural test runs the
full derivation on a world whose schema differs from the dummy's (v1).

Rivals are returned as in-process callables sample(regime_ns, n, seed) for the
battery builder and certificates (scored via score_callable; trusted, no sandbox).
v0 covers:
  (a) naive joint  -- believe the corrupted observational data
  (b) innocent twin -- the mechanism with one operator ABLATED + a one-step
      Gauss-Newton moment refit over the DECLARED knobs of the non-ablated
      operators (fixes-only-strengthen, v0.19; declared approximate)
  (d) capacity ladder -- models of OBSERVABLES only (no mixture head): linear,
      flexible polynomial, and the SMOOTH-IN-CONTEXT member (logistic features,
      v0.29 ladder equity: a polynomial explodes beyond the experimentable
      context range and would inflate the theory gap for the dumb reason).
Rival (c) prior-evoked (LLM panel) lives in rival_c_panel.py (LLM-first).

LLMs are allowed here (factory); these particular rivals use none.
"""

from dataclasses import dataclass
from types import SimpleNamespace
from typing import Callable

import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import PolynomialFeatures


@dataclass(frozen=True)
class CaseSchema:
    """What the derivation is allowed to know, all read from meta (v0.39)."""

    columns: tuple          # meta.columns order (the submission contract)
    decision: str           # stakes.decision_variables[0]
    context: str            # the cheap source's declared context variable
    lo: float               # declared settable bounds of the decision var
    hi: float
    ctx_levels: tuple       # experimentable range -> training grid levels


def case_schema(meta) -> CaseSchema:
    decision = meta.stakes.decision_variables[0]
    source = list(meta.episode.observe_sources.values())[0]
    ctx_keys = sorted(source.context.keys())
    if len(ctx_keys) != 1:
        raise ValueError(f"v0 derivation expects ONE declared context var, got {ctx_keys}")
    context = ctx_keys[0]
    surface = meta.episode.control_surface or {}
    settable = (surface.get("settable") or {}).get(decision) or {}
    lo, hi = float(settable.get("low", 0.0)), float(settable.get("high", 10.0))
    ctx_decl = (surface.get("context") or {}).get(context)
    if isinstance(ctx_decl, dict) and "experimentable_range" in ctx_decl:
        c_lo, c_hi = ctx_decl["experimentable_range"]
        ctx_levels = tuple(float(v) for v in np.linspace(float(c_lo), float(c_hi), 5))
    else:
        ctx_levels = (-1.5, 0.0, 1.5)  # pre-declaration fallback (dummy)
    return CaseSchema(
        columns=tuple(meta.column_names), decision=decision, context=context,
        lo=lo, hi=hi, ctx_levels=ctx_levels,
    )


def _ns(config=None, context=None):
    return SimpleNamespace(config=config or {}, context=context or {}, horizon=None)


def observational_pool(world_sample: Callable, source, n: int, seed: int) -> pd.DataFrame:
    """The pool every factory-side fit consumes -- routed through the SOURCE
    VIEW (Decision Log v0.55-1, the predicted class): until world 3, traps
    lived in the mechanism so world_sample WAS the observational view; with
    source-layer traps the rival (a), the (d-obs) ladder and the twin refits
    must fit the FILTERED+NOISY view or the naive anchor becomes the truth in
    disguise (collapsed L1 denominator). This is not weakening the rival to
    inflate gaps -- it RESTORES its defined semantics (anchor = believe the
    data at face value). The battery stays on world.sample (full population,
    contract v0.50-3)."""
    from wager.harness.source_view import source_view

    return source_view(world_sample, source, n, seed)


def experimental_grid(world_sample: Callable, schema: CaseSchema, levels, n: int, seed0: int,
                      channel=None) -> pd.DataFrame:
    """Interventional data do(decision=level) across declared context levels --
    the access a capable rival would buy. Randomization bypasses the source's
    SELECTION, never its measurement channel (v0.9): pass the source's declared
    channel so the rival's experiments read the same imperfect meter."""
    from wager.harness.source_view import experiment_view

    frames = []
    s = seed0
    for lv in levels:
        for c in schema.ctx_levels:
            ns = _ns({schema.decision: float(lv)}, {schema.context: float(c)})
            df = experiment_view(world_sample, ns, channel, n, s).copy()
            df[schema.context] = c
            frames.append(df)
            s += 1
    return pd.concat(frames, ignore_index=True)


# ---- (a) naive joint -------------------------------------------------------
def rival_naive(pool: pd.DataFrame, schema: CaseSchema) -> Callable:
    cols = list(schema.columns)
    d_idx = cols.index(schema.decision)
    o_idx = [i for i in range(len(cols)) if i != d_idx]
    mu = pool[cols].mean().to_numpy()
    cov = pool[cols].cov().to_numpy()

    def sample(regime, n, seed):
        rng = np.random.default_rng(seed)
        if schema.decision in regime.config:
            d = float(regime.config[schema.decision])
            mu_c = mu[o_idx] + cov[o_idx, d_idx] / cov[d_idx, d_idx] * (d - mu[d_idx])
            cov_c = cov[np.ix_(o_idx, o_idx)] - np.outer(cov[o_idx, d_idx], cov[d_idx, o_idx]) / cov[d_idx, d_idx]
            draw = rng.multivariate_normal(mu_c, cov_c, n)
            out = {schema.decision: np.full(n, d)}
            out.update({cols[j]: draw[:, k] for k, j in enumerate(o_idx)})
        else:
            draw = rng.multivariate_normal(mu, cov, n)
            out = {c: draw[:, i] for i, c in enumerate(cols)}
            out[schema.decision] = np.clip(out[schema.decision], schema.lo, schema.hi)
        return pd.DataFrame(out)[cols]

    return sample


# ---- (b) innocent twin: ablate one operator, refit DECLARED free knobs ------
def free_knobs(meta, ablated_op) -> list[str]:
    """The declared structural free params: knobs of the NON-ablated operators
    (v0.39: read from the meta schema, never a name list)."""
    keys: list[str] = []
    for op in meta.operators:
        if op.name == ablated_op.name:
            continue
        keys.extend(k for k in op.knobs if k not in keys)
    return keys


def rival_twin(mechanism: Callable, base_params: dict, meta, ablated_op,
               pool: pd.DataFrame, schema: CaseSchema, refit_seed: int = 90001) -> Callable:
    """The mechanism with the operator's declared ablation applied (operator
    off), then ONE Gauss-Newton step over the DECLARED knobs of the non-ablated
    operators, matching the observational per-column means and stds of the
    corrupted pool (the 'didn't see the trap' model reproduces the records).
    Deterministic (fixed seed), declared approximate, fixes-only-strengthen:
    with no free knobs declared there is no refit -- visible in the twin's
    `refit_knobs` attribute, never silently absorbed (the v0.34-D bug was a
    refit over a hardcoded name that v1 lacked: an inert rival nobody saw)."""
    p = dict(base_params)
    p.update(dict(ablated_op.ablation))
    knobs = [k for k in free_knobs(meta, ablated_op) if k in p]
    obs = _ns({}, {schema.context: 0.0})
    cols = list(schema.columns)

    def moments(params) -> np.ndarray:
        sim = mechanism(params, obs, len(pool), refit_seed)
        return np.concatenate([sim[cols].mean().to_numpy(), sim[cols].std().to_numpy()])

    target = np.concatenate([pool[cols].mean().to_numpy(), pool[cols].std().to_numpy()])
    if knobs:
        m0 = moments(p)
        jac = np.zeros((len(target), len(knobs)))
        for j, k in enumerate(knobs):
            step = 0.05 * (abs(p[k]) or 1.0)
            hi_p, lo_p = dict(p), dict(p)
            hi_p[k] = p[k] + step
            lo_p[k] = p[k] - step
            jac[:, j] = (moments(hi_p) - moments(lo_p)) / (2 * step)
        delta, *_ = np.linalg.lstsq(jac, target - m0, rcond=None)
        for j, k in enumerate(knobs):
            bound = 0.5 * (abs(p[k]) or 1.0)  # one conservative step, clipped
            p[k] = p[k] + float(np.clip(delta[j], -bound, bound))

    def sample(regime, n, seed):
        return mechanism(p, regime, n, seed)

    sample.refit_knobs = list(knobs)  # self-describing (audit surface)
    sample.params = dict(p)
    return sample


# ---- (d) capacity ladder: models of OBSERVABLES only (no mixture head) ------
def _sigmoid(x):
    return 1.0 / (1.0 + np.exp(-x))


def _fit_no_latent(train: pd.DataFrame, pool: pd.DataFrame, schema: CaseSchema,
                   kind: str) -> Callable:
    """Best generative model restricted to functions of OBSERVABLES (no latent,
    no mixture head). Output-column means via a smooth regressor on (decision,
    context); joint dependence via the fitted residual covariance (NOT by
    chaining through a generated column, which amplifies variance -- v0.18).

    kind: 'linear' | 'poly' (degree-4 flexible) | 'logistic_ctx' (v0.29 equity
    member: features [d, sig(ctx), d*sig(ctx)] -- extrapolates SMOOTHLY in the
    context beyond the experimentable range, where a polynomial explodes and a
    tree plateaus, both killing the gap for the dumb reason)."""
    outputs = [c for c in schema.columns if c != schema.decision]

    def features(d, c):
        if kind == "logistic_ctx":
            s = _sigmoid(c)
            return np.column_stack([d, s, d * s])
        return np.column_stack([d, c])

    def _mk():
        return make_pipeline(PolynomialFeatures(4 if kind == "poly" else 1), LinearRegression())

    X = features(train[schema.decision].to_numpy(), train[schema.context].to_numpy())
    models = {c: _mk().fit(X, train[c].to_numpy()) for c in outputs}
    resid = np.vstack([train[c].to_numpy() - models[c].predict(X) for c in outputs])
    resid_cov = np.atleast_2d(np.cov(resid))
    dec_pool = pool[schema.decision].to_numpy()

    def sample(regime, n, seed):
        rng = np.random.default_rng(seed)
        c = float(regime.context.get(schema.context, 0.0))
        if schema.decision in regime.config:
            d = np.full(n, float(regime.config[schema.decision]))
        else:
            d = rng.choice(dec_pool, n, replace=True)
        Xq = features(d, np.full(n, c))
        draw = rng.multivariate_normal(np.zeros(len(outputs)), resid_cov, n)
        out = {schema.decision: d}
        for k, col in enumerate(outputs):
            out[col] = models[col].predict(Xq) + draw[:, k]
        return pd.DataFrame(out)[list(schema.columns)]

    return sample


def _fit_hetero_no_latent(train: pd.DataFrame, pool: pd.DataFrame, schema: CaseSchema) -> Callable:
    """No-latent with CONDITIONAL residual scale (Decision Log v0.41-3): poly
    means + per-row std fitted on |residual| over (decision, sig(ctx)) features.
    Unimodal per regime -- no mixture head; kills the global-residual explosion
    at low decision values (the all-capped collapse of P2 run 1)."""
    outputs = [c for c in schema.columns if c != schema.decision]

    def feats(d, c):
        s = _sigmoid(c)
        return np.column_stack([d, s, d * s, d * d])

    X = feats(train[schema.decision].to_numpy(), train[schema.context].to_numpy())
    mean_m = {c: make_pipeline(PolynomialFeatures(2), LinearRegression()).fit(X, train[c].to_numpy())
              for c in outputs}
    resid = {c: train[c].to_numpy() - mean_m[c].predict(X) for c in outputs}
    std_m = {c: make_pipeline(PolynomialFeatures(2), LinearRegression()).fit(X, np.abs(resid[c]))
             for c in outputs}
    z = np.vstack([resid[c] / np.maximum(std_m[c].predict(X), 1e-3) for c in outputs])
    z_corr = np.atleast_2d(np.corrcoef(z))
    dec_pool = pool[schema.decision].to_numpy()

    def sample(regime, n, seed):
        rng = np.random.default_rng(seed)
        c = float(regime.context.get(schema.context, 0.0))
        d = (np.full(n, float(regime.config[schema.decision]))
             if schema.decision in regime.config else rng.choice(dec_pool, n, replace=True))
        Xq = feats(d, np.full(n, c))
        draw = rng.multivariate_normal(np.zeros(len(outputs)), z_corr, n)
        out = {schema.decision: d}
        for k, col in enumerate(outputs):
            sd = np.maximum(std_m[col].predict(Xq), 1e-3) * np.sqrt(np.pi / 2.0)
            out[col] = mean_m[col].predict(Xq) + draw[:, k] * sd
        return pd.DataFrame(out)[list(schema.columns)]

    return sample


def _fit_marker_conditional(train: pd.DataFrame, pool: pd.DataFrame, schema: CaseSchema) -> Callable:
    """No-latent that USES the observed channel (Decision Log v0.41-2 doctrine):
    resamples the OBSERVED marker empirically per context cell (population memory
    of an observable's marginal -- no per-sample component inference anywhere),
    then outcome | (decision, marker, ctx) with interaction + conditional scale.
    Empirical/quantile machinery only; the null hypothesis of the theory-gap test."""
    outputs = [c for c in schema.columns if c != schema.decision]
    marker_col = next((c for c in outputs if c != "outcome"), outputs[0])
    other = [c for c in outputs if c != marker_col]
    levels = np.array(schema.ctx_levels)
    bank = {lv: train.loc[np.isclose(train[schema.context], lv), marker_col].to_numpy()
            for lv in levels}

    def feats(d, m, c):
        s = _sigmoid(c)
        return np.column_stack([d, m, d * m, s, d * s])

    X = feats(train[schema.decision].to_numpy(), train[marker_col].to_numpy(),
              train[schema.context].to_numpy())
    mean_m = {c: make_pipeline(PolynomialFeatures(2), LinearRegression()).fit(X, train[c].to_numpy())
              for c in other}
    std_m = {c: make_pipeline(PolynomialFeatures(2), LinearRegression()).fit(
        X, np.abs(train[c].to_numpy() - mean_m[c].predict(X))) for c in other}
    dec_pool = pool[schema.decision].to_numpy()

    def sample(regime, n, seed):
        rng = np.random.default_rng(seed)
        c = float(regime.context.get(schema.context, 0.0))
        d = (np.full(n, float(regime.config[schema.decision]))
             if schema.decision in regime.config else rng.choice(dec_pool, n, replace=True))
        # smooth dependence on the declared knob: interpolate between the two
        # nearest context cells' EMPIRICAL banks (clamped beyond the range)
        cc = float(np.clip(c, levels[0], levels[-1]))
        hi = int(np.searchsorted(levels, cc, side="left").clip(1, len(levels) - 1))
        lo = hi - 1
        w_hi = 0.0 if levels[hi] == levels[lo] else (cc - levels[lo]) / (levels[hi] - levels[lo])
        pick_hi = rng.random(n) < w_hi
        m = np.where(pick_hi, rng.choice(bank[levels[hi]], n, replace=True),
                     rng.choice(bank[levels[lo]], n, replace=True))
        Xq = feats(d, m, np.full(n, c))
        out = {schema.decision: d, marker_col: m}
        for col in other:
            sd = np.maximum(std_m[col].predict(Xq), 1e-3) * np.sqrt(np.pi / 2.0)
            out[col] = mean_m[col].predict(Xq) + rng.normal(0.0, 1.0, n) * sd
        return pd.DataFrame(out)[list(schema.columns)]

    return sample


def _fit_empirical_residual(train: pd.DataFrame, pool: pd.DataFrame, schema: CaseSchema) -> Callable:
    """Practical SUPREMUM of the admissible no-latent class (Decision Log v0.45-2):
    conditional mean on (decision, marker, ctx) + EMPIRICAL residual bank keyed by
    DECLARED bins (decision level, ctx cell, marker quartile within the cell) --
    population memory of observable residual SHAPES (quantile machinery; zero
    per-sample component inference). The ctx dial: interpolation between the two
    nearest cells WITHIN the experimentable range; BEYOND it the bank FREEZES
    (clamp to the boundary cell, declared) -- that is where v1 must bite."""
    outputs = [c for c in schema.columns if c != schema.decision]
    marker_col = next((c for c in outputs if c != "outcome"), outputs[0])
    other = [c for c in outputs if c != marker_col]
    levels_c = np.array(schema.ctx_levels)
    levels_d = np.array(sorted(train[schema.decision].unique()))
    m_bank = {lv: train.loc[np.isclose(train[schema.context], lv), marker_col].to_numpy()
              for lv in levels_c}

    def feats(d, m, c):
        s = _sigmoid(c)
        return np.column_stack([d, m, d * m, s, d * s])

    X = feats(train[schema.decision].to_numpy(), train[marker_col].to_numpy(),
              train[schema.context].to_numpy())
    mean_m = {c: make_pipeline(PolynomialFeatures(2), LinearRegression()).fit(X, train[c].to_numpy())
              for c in other}

    # residual banks: (d level, ctx cell, marker quartile) -> empirical residuals
    q_edges: dict = {}
    r_bank: dict = {}
    for id_, dl in enumerate(levels_d):
        for ic, cl in enumerate(levels_c):
            cell = train[np.isclose(train[schema.decision], dl) & np.isclose(train[schema.context], cl)]
            if len(cell) == 0:
                continue
            m = cell[marker_col].to_numpy()
            edges = np.quantile(m, [0.25, 0.5, 0.75])
            q_edges[(id_, ic)] = edges
            iq = np.searchsorted(edges, m)
            Xc = feats(cell[schema.decision].to_numpy(), m, cell[schema.context].to_numpy())
            for col in other:
                res = cell[col].to_numpy() - mean_m[col].predict(Xc)
                for q in range(4):
                    r_bank[(col, id_, ic, q)] = res[iq == q]
    dec_pool = pool[schema.decision].to_numpy()

    def sample(regime, n, seed):
        rng = np.random.default_rng(seed)
        c = float(regime.context.get(schema.context, 0.0))
        d = (np.full(n, float(regime.config[schema.decision]))
             if schema.decision in regime.config else rng.choice(dec_pool, n, replace=True))
        cc = float(np.clip(c, levels_c[0], levels_c[-1]))   # FREEZE beyond range (declared)
        hi = int(np.searchsorted(levels_c, cc, side="left").clip(1, len(levels_c) - 1))
        lo = hi - 1
        w_hi = 0.0 if levels_c[hi] == levels_c[lo] else (cc - levels_c[lo]) / (levels_c[hi] - levels_c[lo])
        ic_row = np.where(rng.random(n) < w_hi, hi, lo)
        m = np.empty(n)
        for ic in np.unique(ic_row):
            mask = ic_row == ic
            m[mask] = rng.choice(m_bank[levels_c[ic]], int(mask.sum()), replace=True)
        id_row = np.abs(d[:, None] - levels_d[None, :]).argmin(axis=1)
        Xq = feats(d, m, np.full(n, c))
        out = {schema.decision: d, marker_col: m}
        for col in other:
            base = mean_m[col].predict(Xq)
            res = np.empty(n)
            for id_ in np.unique(id_row):
                for ic in np.unique(ic_row):
                    mask = (id_row == id_) & (ic_row == ic)
                    if not mask.any():
                        continue
                    edges = q_edges[(int(id_), int(ic))]
                    iq = np.searchsorted(edges, m[mask])
                    res_m = np.empty(int(mask.sum()))
                    for q in range(4):
                        qmask = iq == q
                        if qmask.any():
                            bank = r_bank[(col, int(id_), int(ic), q)]
                            res_m[qmask] = rng.choice(bank, int(qmask.sum()), replace=True)
                    res[mask] = res_m
            out[col] = base + res
        return pd.DataFrame(out)[list(schema.columns)]

    return sample


def capacity_ladder(train: pd.DataFrame, pool: pd.DataFrame, schema: CaseSchema) -> list[tuple[str, Callable]]:
    return [
        ("linear_no_latent", _fit_no_latent(train, pool, schema, "linear")),
        ("gbm_no_latent", _fit_no_latent(train, pool, schema, "poly")),
        ("logistic_ctx_no_latent", _fit_no_latent(train, pool, schema, "logistic_ctx")),
        ("hetero_no_latent", _fit_hetero_no_latent(train, pool, schema)),
        ("marker_conditional_no_latent", _fit_marker_conditional(train, pool, schema)),
        ("empirical_residual_no_latent", _fit_empirical_residual(train, pool, schema)),
    ]


def best_no_latent(train: pd.DataFrame, pool: pd.DataFrame, schema: CaseSchema) -> Callable:
    """The flexible no-latent -- the THEORY-GAP single reference for callers
    that need one (the certificate itself takes the BEST ladder member)."""
    return _fit_no_latent(train, pool, schema, "poly")


def build_standard_rivals(case_dir, world_sample: Callable, meta, n_pool=4000, n_train=300):
    """The disagreement rival set the battery_builder weighs (Decision Log v0.24):
    naive (a) + the FULL capacity ladder (d: linear + poly + logistic-ctx) + an
    innocent twin (b) per declared mechanism operator. Everything schema-driven
    (v0.39). Returns (rivals, pool, train)."""
    from wager.factory.case_loader import load_world_module

    schema = case_schema(meta)
    source = list(meta.episode.observe_sources.values())[0]
    pool = observational_pool(world_sample, source, n_pool, 50001)
    levels = list(range(int(schema.lo), int(schema.hi) + 1))
    train = experimental_grid(world_sample, schema, levels, n_train, 60001,
                              channel=source.channel)
    wmod = load_world_module(case_dir)
    rivals = [rival_naive(pool, schema)]
    rivals += [fn for _, fn in capacity_ladder(train, pool, schema)]
    for op in meta.operators:
        if op.layer == "mechanism" and op.ablation:
            rivals.append(rival_twin(wmod.mechanism, wmod.PARAMS, meta, op, pool, schema))
    return rivals, pool, train
