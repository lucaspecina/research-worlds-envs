"""logistic_yield_v0 (#11): derived rivals + declared battery + L1 gates + certificates.

THE FORMALISM TEST (spec docs/mundos-dinamicos.md): first dynamic world; its job
is to validate that the exam machinery survives photos -> movies with minor
changes. Findings about machinery that does NOT generalize are part of the
result and get registered (per ADR 0068: zero new code expected outside R1;
whatever asks for more, gets logged):

  - REGISTERED FINDING 1: derive_rivals.capacity_ladder / build_battery are
    static-only (fit tabular (decision, context) -> columns); the trajectory
    ladder and battery grid are built HERE as case tooling (precedent: v1's
    make_ladder_fixtures bootstrap exception). Factory generalization debt.
  - REGISTERED FINDING 2: FunctionalScorer needed the (declared-trivial,
    spec 4.2) extension "a time-indexed functional prices only the items whose
    grid carries its timestamp" -- shipped with its test in the same commit.

PRE-REGISTERED (signed BEFORE running, spec section 5):
  - L1 order: truth(1) > perturbed_x1.15 > twin_canal > twin_truncation >=
    naive_exp(0) > null. twin_truncation ~ naive near-tie is EXPECTED (they
    believe almost the same thing); a tie is reported, never retuned.
  - Theory gap ~ 0 DECLARED: a generic saturating family fitted on full data
    is nearly the mechanism; this world loads on biased-channel (truncation +
    noise) and expensive-probes (time costs), NOT representation. Where
    saturating_generic lands fitted on the TRUNCATED pool is reported as data
    (K is unidentifiable from ramp-up readings).
  - Visibility: BOTH operators separate at the resolution floor (0.05 R) --
    truncation via long-horizon items, channel via twin_canal.
  - Recoverability/headroom (a): canonical solver (high-feed long experiment
    -> per-unit logistic fits -> population params; sigma_med from replicas)
    lands R >= 0.95.
  - Scale sanity (the pre-named 6th of the scale family, spec 4.3): x0
    population variability keeps every pivoted column non-degenerate; the
    existing relative clamp must suffice WITHOUT touching it. If it needs
    touching -> investigate, never retune.
  - Battery band: out-of-record TIME items (grid beyond the historical
    horizon t=6) carry ~34% of the weight (canonized 20-35% band; traceable
    to the brief's promise "long-run outcomes are explicitly part of what you
    are paid to predict").

Run:  .venv/Scripts/python cases/logistic_yield_v0/build_and_certify.py
"""

import json
import sys
from pathlib import Path
from types import SimpleNamespace

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
CASE = Path(__file__).parent
sys.path.insert(0, str(CASE))

import world  # noqa: E402

from wager.contracts import Battery, BatteryItem, CaseMeta  # noqa: E402
from wager.contracts.world import Regime  # noqa: E402
from wager.factory.case_loader import make_sample_transform  # noqa: E402
from wager.harness.source_view import source_view  # noqa: E402
from wager.reward.scorer import WorldSide, score_callable  # noqa: E402

FLOOR = 0.05
POOL_N, POOL_SEED = 400, 97001
BATTERY_SEED0 = 97301

G_IN = (0.0, 2.0, 4.0, 6.0)
G_MID = (0.0, 4.0, 8.0, 12.0, 16.0)
G_LONG = (0.0, 6.0, 12.0, 18.0, 24.0)
FEEDS = (2.0, 5.0, 8.0)


# --- the d-obs pool: truncated + noisy (what every rival believes) -----------

def truncated_pool(meta):
    spec = meta.episode.observe_sources["registros_campanas"]
    return source_view(world.sample, spec, POOL_N, POOL_SEED)


def pool_fits(pool):
    """Population-level fits every ladder member shares (uniform recipe)."""
    t = pool["t"].to_numpy(float)
    y = np.maximum(pool["y"].to_numpy(float), 0.1)
    logy = np.log(y)
    b_exp, a_exp = np.polyfit(t, logy, 1)              # exp family: log-linear
    # per-unit multiplicative dispersion (naive believes it is real structure)
    resid = logy - (a_exp + b_exp * t)
    per_unit = pd.DataFrame({"u": pool["unit_id"], "r": resid}).groupby("u")["r"].mean()
    s_unit = float(per_unit.std())
    s_read = float((resid - per_unit.reindex(pool["unit_id"]).to_numpy()).std())
    lin = np.polyfit(t, y, 1)                          # linear family
    poly2 = np.polyfit(t, y, 2)                        # quadratic family
    # generic saturating family on the TRUNCATED pool (K unidentifiable: data)
    from scipy.optimize import curve_fit

    def logistic3(tt, K, r, x0):
        return K / (1.0 + ((K - x0) / x0) * np.exp(-r * tt))

    p0 = (50.0, 0.3, 2.0)
    sat, _ = curve_fit(logistic3, t, y, p0=p0,
                       bounds=([5.0, 0.01, 0.2], [2000.0, 3.0, 20.0]), maxfev=20000)
    stats = {"mean": float(pool["y"].mean()), "sd": float(pool["y"].std())}
    return {"a_exp": float(a_exp), "b_exp": float(b_exp), "s_unit": s_unit,
            "s_read": s_read, "lin": [float(v) for v in lin],
            "poly2": [float(v) for v in poly2], "sat": [float(v) for v in sat],
            "marg": stats}


# --- rivals (all produce LONG format on the requested grid) -------------------

def _long(grid, n, per_unit_curve):
    t = np.asarray(grid, float)
    k = t.size
    y = per_unit_curve(t)                              # (n, k)
    return pd.DataFrame({"unit_id": np.repeat(np.arange(n, dtype=float), k),
                         "t": np.tile(t, n), "y": y.ravel()})


def naive_exponential(f):
    """R=0 anchor: believes the truncated noisy pool -- growth without ceiling."""
    def sample(ns, n, seed):
        rng = np.random.default_rng(seed)
        grid = ns.context["t_grid"]

        def curve(t):
            u = rng.normal(0.0, f["s_unit"], n)[:, None]
            e = rng.normal(0.0, f["s_read"], (n, t.size))
            return np.exp(f["a_exp"] + f["b_exp"] * t[None, :] + u + e)
        return _long(grid, n, curve)
    return sample


def null_marginals(f):
    """Knows nothing: pool y-marginal per reading, blind to t and feed."""
    def sample(ns, n, seed):
        rng = np.random.default_rng(seed)
        grid = ns.context["t_grid"]

        def curve(t):
            return rng.normal(f["marg"]["mean"], f["marg"]["sd"], (n, t.size))
        return _long(grid, n, curve)
    return sample


def family_member(f, kind):
    """Uniform ladder recipe: population mean curve + per-unit factor N(1, cv)."""
    cv = abs(f["s_unit"])

    def mean_curve(t):
        if kind == "linear_t":
            return np.polyval(f["lin"], t)
        if kind == "poly2_t":
            return np.polyval(f["poly2"], t)
        if kind == "saturating_generic":
            K, r, x0 = f["sat"]
            return K / (1.0 + ((K - x0) / x0) * np.exp(-r * t))
        raise ValueError(kind)

    def sample(ns, n, seed):
        rng = np.random.default_rng(seed)
        grid = ns.context["t_grid"]

        def curve(t):
            m = mean_curve(np.asarray(t, float))[None, :]
            u = rng.normal(1.0, cv, n)[:, None]
            return m * u
        return _long(grid, n, curve)
    return sample


def twin_truncation(meta, pool):
    """Recipe (b) twin: knows the mechanism SHAPE, believes the pool's horizon
    covers the whole story -> fits (r, K, x0) centers on truncated readings,
    keeps the true dispersions. K is unidentifiable there; wherever the fit
    lands is the lie it believes."""
    from scipy.optimize import curve_fit
    t = pool["t"].to_numpy(float)
    y = np.maximum(pool["y"].to_numpy(float), 0.1)

    def logistic3(tt, K, r, x0):
        return K / (1.0 + ((K - x0) / x0) * np.exp(-r * tt))

    (K, r, x0), _ = curve_fit(logistic3, t, y, p0=(50.0, 0.3, 2.0),
                              bounds=([5.0, 0.01, 0.2], [2000.0, 3.0, 20.0]), maxfev=20000)
    p = dict(world.PARAMS)
    p["K0"], p["x0"] = float(K), float(x0)
    p["r0"] = float(r) - p["r_slope"] * world.HIST_FEED   # keeps feed response

    def sample(ns, n, seed):
        return world.mechanism(p, ns, n, seed)
    return sample


def twin_canal(meta):
    """'The dispersion I see is real': true mechanism + sensor noise baked into
    what it believes the process is."""
    sd = meta.episode.observe_sources["registros_campanas"].channel.noise_sd

    def sample(ns, n, seed):
        df = world.mechanism(world.PARAMS, ns, n, seed)
        rng = np.random.default_rng(seed + 17)
        out = df.copy()
        out["y"] = out["y"] + rng.normal(0.0, sd, len(out))
        return out
    return sample


def perturbed_truth(factor=1.15):
    p = dict(world.PARAMS)
    for key in ("r0", "r_slope", "K0"):
        p[key] = p[key] * factor

    def sample(ns, n, seed):
        return world.mechanism(p, ns, n, seed)
    return sample


def canonical_solver(meta):
    """Headroom (a): the manual moves with d-exp access -- high-feed LONG runs
    (saturation arrives sooner: cheap horizon), per-unit logistic fits ->
    population params; K transfers across feeds because it does not depend on
    feed (the judgment move this world prices). sigma_med via replicas."""
    from scipy.optimize import curve_fit
    grid = tuple(np.arange(0.0, 25.0, 2.0))
    fits = []
    for feed, seed in ((8.0, 61001), (2.0, 61002)):
        ns = SimpleNamespace(config={"feed": feed}, context={"t_grid": grid}, horizon=None)
        # experiment access (v0.9): mechanism fresh + the SAME meter as the record
        raw = world.sample(ns, 60, seed)
        rng = np.random.default_rng(seed + 5)
        raw = raw.assign(y=raw["y"] + rng.normal(
            0.0, meta.episode.observe_sources["registros_campanas"].channel.noise_sd, len(raw)))
        for uid, g in raw.groupby("unit_id"):
            try:
                (K, r, x0), _ = curve_fit(
                    lambda tt, K, r, x0: K / (1.0 + ((K - x0) / x0) * np.exp(-r * tt)),
                    g["t"].to_numpy(float), g["y"].to_numpy(float),
                    p0=(100.0, 0.3, 2.0),
                    bounds=([5.0, 0.01, 0.2], [2000.0, 3.0, 20.0]), maxfev=20000)
                fits.append((feed, K, r, x0))
            except RuntimeError:
                continue
    arr = np.array([(f, K, r, x0) for f, K, r, x0 in fits])
    feeds, Ks, rs, x0s = arr[:, 0], arr[:, 1], arr[:, 2], arr[:, 3]
    slope, r0 = np.polyfit(feeds, rs, 1)
    p = dict(world.PARAMS)
    p["K0"], p["K_sd"] = float(Ks.mean()), float(max(Ks.std(), 1.0))
    p["x0"], p["x0_sd"] = float(np.median(x0s)), float(max(x0s.std(), 0.05))
    p["r0"], p["r_slope"] = float(r0), float(slope)
    resid = rs - (r0 + slope * feeds)
    p["r_disp"] = float(max(np.std(resid / np.maximum(r0 + slope * feeds, 1e-3)), 0.02))

    def sample(ns, n, seed):
        return world.mechanism(p, ns, n, seed)
    return sample


# --- the declared battery (pre-registered grid; band traceable) --------------

def build_battery():
    items, s = [], BATTERY_SEED0
    for feed in FEEDS:                       # in-record grids
        items.append(BatteryItem(weight=0.155, regime=Regime(
            config={"feed": feed}, context={"t_grid": G_IN}), seed_world=s)); s += 1
    items.append(BatteryItem(weight=0.10, regime=Regime(
        config={}, context={"t_grid": G_IN}), seed_world=s)); s += 1
    for feed in FEEDS:                       # deadline grids (functional lives here)
        items.append(BatteryItem(weight=0.035, regime=Regime(
            config={"feed": feed}, context={"t_grid": G_MID}), seed_world=s)); s += 1
    items.append(BatteryItem(weight=0.04, regime=Regime(
        config={}, context={"t_grid": G_MID}), seed_world=s)); s += 1
    for feed in FEEDS:                       # plateau grids
        items.append(BatteryItem(weight=0.05, regime=Regime(
            config={"feed": feed}, context={"t_grid": G_LONG}), seed_world=s)); s += 1
    return Battery(items=items)


# --- episode anchor fixtures (naive + null as CODE, baked numbers) ------------

def write_fixtures(f):
    header = ("GENERATED by build_and_certify.py (POOL_SEED={s}, POOL_N={n}) - do not\n"
              "hand-edit; regenerate to audit.").format(s=POOL_SEED, n=POOL_N)
    naive = f'''"""Rung 7 -- naive fit of the truncated noisy record (S_naive anchor, R=0).

Believes the ramp-up story: exponential growth, no ceiling, dispersion real.
{header}
"""
import numpy as np
import pandas as pd

A, B, S_UNIT, S_READ = {f["a_exp"]!r}, {f["b_exp"]!r}, {f["s_unit"]!r}, {f["s_read"]!r}


def model(regime, n, seed):
    rng = np.random.default_rng(seed)
    t = np.asarray(tuple(regime.context["t_grid"]), dtype=float)
    u = rng.normal(0.0, S_UNIT, n)[:, None]
    e = rng.normal(0.0, S_READ, (n, t.size))
    y = np.exp(A + B * t[None, :] + u + e)
    return pd.DataFrame({{"unit_id": np.repeat(np.arange(n, dtype=float), t.size),
                          "t": np.tile(t, n), "y": y.ravel()}})
'''
    null = f'''"""Rung 8 -- null model: record y-marginal, blind to time (S_null / D_MAX).

{header}
"""
import numpy as np
import pandas as pd

MEAN, SD = {f["marg"]["mean"]!r}, {f["marg"]["sd"]!r}


def model(regime, n, seed):
    rng = np.random.default_rng(seed)
    t = np.asarray(tuple(regime.context["t_grid"]), dtype=float)
    y = rng.normal(MEAN, SD, (n, t.size))
    return pd.DataFrame({{"unit_id": np.repeat(np.arange(n, dtype=float), t.size),
                          "t": np.tile(t, n), "y": y.ravel()}})
'''
    ladder = CASE / "ladder"
    ladder.mkdir(exist_ok=True)
    (ladder / "rung_7_naive_exp.py").write_text(naive, encoding="utf-8", newline="\n")
    (ladder / "rung_8_null.py").write_text(null, encoding="utf-8", newline="\n")


def main():
    meta = CaseMeta.from_json_file(CASE / "meta.json")
    params = meta.scoring
    pool = truncated_pool(meta)
    f = pool_fits(pool)
    write_fixtures(f)

    naive = naive_exponential(f)
    null_fn = null_marginals(f)
    rungs = {
        "perturbed_x1.15": perturbed_truth(),
        "linear_t": family_member(f, "linear_t"),
        "poly2_t": family_member(f, "poly2_t"),
        "saturating_generic_pool": family_member(f, "saturating_generic"),
        "twin_truncation": twin_truncation(meta, pool),
        "twin_canal": twin_canal(meta),
    }

    battery = build_battery()
    battery.to_json_file(CASE / "battery.json")
    ws = WorldSide(world.sample, battery, meta.column_names, params.n_samples,
                   null_sample=null_fn, functionals=meta.stakes.functionals,
                   c_f=params.c_f, sample_transform=make_sample_transform(meta))

    s_truth = score_callable(world.sample, ws, params)
    s_naive = score_callable(naive, ws, params)
    den = s_truth - s_naive

    def R(fn):
        return (score_callable(fn, ws, params) - s_naive) / den

    r = {k: R(fn) for k, fn in rungs.items()}
    r["null"] = R(null_fn)
    r_canon = R(canonical_solver(meta))

    out_w = sum(it.weight for it in battery.items
                if max(it.regime.context["t_grid"]) > 6.0)
    tot_w = sum(it.weight for it in battery.items)

    report = {
        "denom_raw": den,
        "R": {k: round(v, 4) for k, v in r.items()},
        "R_canonical": round(r_canon, 4),
        "battery_k": len(battery.items),
        "out_of_record_time_share": round(out_w / tot_w, 3),
        "sat_pool_fit_K": round(f["sat"][0], 2),
        "gates": {},
    }
    g = report["gates"]
    g["naive_far"] = den > 0 and all(v < 1.0 - FLOOR for k, v in r.items()
                                     if k != "perturbed_x1.15")
    g["no_inversions"] = all(v <= 1.0 + 0.02 for v in r.values())
    g["null_floor"] = r["null"] < 0.0
    g["vis_truncation"] = (1.0 - r["twin_truncation"]) >= FLOOR
    g["vis_canal"] = (1.0 - r["twin_canal"]) >= FLOOR
    g["recoverability"] = r_canon >= 1.0 - FLOOR
    g["band_out_of_record"] = 0.20 <= report["out_of_record_time_share"] <= 0.35
    g["l1_signed_order"] = (1.0 > r["perturbed_x1.15"] > r["twin_canal"]
                            and r["twin_truncation"] >= -0.05 and r["null"] < 0.0)
    g["all"] = all(v for v in g.values())

    print(json.dumps(report, indent=2))
    (CASE / "certificates.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print("-> battery.json + certificates.json + ladder fixtures")


if __name__ == "__main__":
    main()
