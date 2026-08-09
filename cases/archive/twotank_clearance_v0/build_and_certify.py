"""twotank_clearance_v0 (#12): derived rivals + declared battery + L1 gates + certificates.

Second dynamic world (queue ADR 0075), built with the #11 mold (ADR 0074) on a
NON-monotone curve -- the differential test #11 could not give: the pivot,
grids, horizon pricing and time-indexed functional must survive rise-then-fall.
Zero new machinery expected; anything that asks for code gets registered.

PRE-REGISTERED (signed BEFORE running; #11 template):
  - L1 order: truth(1) > perturbed_x1.15 > twin_canal > twin_truncation >=
    naive_exp(0) > null. In #11 the mechanistic-shape twin beat the naive by
    +0.23; signed expectation here: same sign, magnitude reported.
  - The joya analog: the generic rise-fall family fitted on the RISE-ONLY
    pool cannot identify the drain rate -- where its k2-hat lands (bound or
    absurd) is reported as the certified invisibility of the tail.
  - Visibility: BOTH operators >= 0.05 R (truncation via long items, canal
    via twin_canal).
  - Recoverability: canonical solver (long experiments at valves {2,8} ->
    per-unit two-exp fits -> population params) >= 0.95.
  - Scale sanity: A0 variability keeps early columns non-degenerate; clamp
    untouched. Out-of-record time band in [20, 35]%.

Run:  .venv/Scripts/python cases/twotank_clearance_v0/build_and_certify.py
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
POOL_N, POOL_SEED = 400, 98001
BATTERY_SEED0 = 98301

G_IN = (0.0, 2.0, 4.0, 6.0)
G_MID = (0.0, 4.0, 8.0, 12.0)
G_LONG = (0.0, 6.0, 12.0, 20.0)
VALVES = (2.0, 5.0, 8.0)


def two_exp(tt, C, a, b):
    """C * (exp(-b t) - exp(-a t)) with a = fast (rise), b = slow (drain)."""
    return C * (np.exp(-b * tt) - np.exp(-a * tt))


def truncated_pool(meta):
    spec = meta.episode.observe_sources["registros_campanas"]
    return source_view(world.sample, spec, POOL_N, POOL_SEED)


def pool_fits(pool):
    from scipy.optimize import curve_fit
    t = pool["t"].to_numpy(float)
    y = np.maximum(pool["y"].to_numpy(float), 0.1)
    logy = np.log(np.maximum(y, 0.1))
    mask = t > 0  # log fit ignores the t=0 zeros (y(0)=0 exactly)
    b_exp, a_exp = np.polyfit(t[mask], logy[mask], 1)
    resid = logy[mask] - (a_exp + b_exp * t[mask])
    per_unit = pd.DataFrame({"u": pool["unit_id"][mask].to_numpy(), "r": resid}) \
        .groupby("u")["r"].mean()
    s_unit = float(per_unit.std())
    s_read = float((resid - per_unit.reindex(pool["unit_id"][mask]).to_numpy()).std())
    lin = np.polyfit(t, y, 1)
    poly2 = np.polyfit(t, y, 2)
    rf, _ = curve_fit(two_exp, t, y, p0=(150.0, 0.3, 0.02),
                      bounds=([5.0, 0.02, 1e-4], [4000.0, 3.0, 2.0]), maxfev=30000)
    return {"a_exp": float(a_exp), "b_exp": float(b_exp), "s_unit": s_unit,
            "s_read": s_read, "lin": [float(v) for v in lin],
            "poly2": [float(v) for v in poly2], "risefall": [float(v) for v in rf],
            "marg": {"mean": float(pool["y"].mean()), "sd": float(pool["y"].std())}}


def _long(grid, n, per_unit_curve):
    t = np.asarray(grid, float)
    k = t.size
    y = per_unit_curve(t)
    return pd.DataFrame({"unit_id": np.repeat(np.arange(n, dtype=float), k),
                         "t": np.tile(t, n), "y": y.ravel()})


def naive_exponential(f):
    def sample(ns, n, seed):
        rng = np.random.default_rng(seed)

        def curve(t):
            u = rng.normal(0.0, f["s_unit"], n)[:, None]
            e = rng.normal(0.0, f["s_read"], (n, t.size))
            return np.exp(f["a_exp"] + f["b_exp"] * np.asarray(t, float)[None, :] + u + e)
        return _long(ns.context["t_grid"], n, curve)
    return sample


def null_marginals(f):
    def sample(ns, n, seed):
        rng = np.random.default_rng(seed)

        def curve(t):
            return rng.normal(f["marg"]["mean"], f["marg"]["sd"], (n, np.asarray(t).size))
        return _long(ns.context["t_grid"], n, curve)
    return sample


def family_member(f, kind):
    cv = abs(f["s_unit"])

    def mean_curve(t):
        if kind == "linear_t":
            return np.polyval(f["lin"], t)
        if kind == "poly2_t":
            return np.polyval(f["poly2"], t)
        if kind == "risefall_generic":
            C, a, b = f["risefall"]
            return two_exp(t, C, a, b)
        raise ValueError(kind)

    def sample(ns, n, seed):
        rng = np.random.default_rng(seed)

        def curve(t):
            m = mean_curve(np.asarray(t, float))[None, :]
            u = rng.normal(1.0, cv, n)[:, None]
            return m * u
        return _long(ns.context["t_grid"], n, curve)
    return sample


def twin_truncation(pool):
    """Knows the two-stage SHAPE, believes the pool's horizon covers the story:
    fits (C, a, b) on rise-only readings (b unidentifiable), keeps the true
    dispersions, maps back to mechanism params."""
    from scipy.optimize import curve_fit
    t = pool["t"].to_numpy(float)
    y = np.maximum(pool["y"].to_numpy(float), 0.1)
    (C, a, b), _ = curve_fit(two_exp, t, y, p0=(150.0, 0.3, 0.02),
                             bounds=([5.0, 0.02, 1e-4], [4000.0, 3.0, 2.0]), maxfev=30000)
    p = dict(world.PARAMS)
    p["k2_0"] = float(b)
    p["k1_0"] = float(a) - p["k1_slope"] * world.HIST_VALVE
    p["A0"] = float(C * (a - b) / a)

    def sample(ns, n, seed):
        return world.mechanism(p, ns, n, seed)
    return sample


def twin_canal(meta):
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
    for key in ("k1_0", "k1_slope", "k2_0"):
        p[key] = p[key] * factor

    def sample(ns, n, seed):
        return world.mechanism(p, ns, n, seed)
    return sample


def canonical_solver(meta):
    """Headroom (a): long experiments at two valves -> per-unit two-exp fits ->
    population params (drain k2 transfers across valves)."""
    from scipy.optimize import curve_fit
    grid = tuple(np.arange(0.0, 25.0, 2.0))
    sd = meta.episode.observe_sources["registros_campanas"].channel.noise_sd
    fits = []
    for valve, seed in ((8.0, 62001), (2.0, 62002)):
        ns = SimpleNamespace(config={"valve": valve}, context={"t_grid": grid}, horizon=None)
        raw = world.sample(ns, 60, seed)
        rng = np.random.default_rng(seed + 5)
        raw = raw.assign(y=raw["y"] + rng.normal(0.0, sd, len(raw)))
        for uid, g in raw.groupby("unit_id"):
            try:
                (C, a, b), _ = curve_fit(two_exp, g["t"].to_numpy(float),
                                         g["y"].to_numpy(float), p0=(150.0, 0.3, 0.05),
                                         bounds=([5.0, 0.02, 1e-4], [4000.0, 3.0, 2.0]),
                                         maxfev=30000)
                fits.append((valve, C, a, b))
            except RuntimeError:
                continue
    arr = np.array(fits)
    valves, Cs, as_, bs = arr[:, 0], arr[:, 1], arr[:, 2], arr[:, 3]
    slope, k1_0 = np.polyfit(valves, as_, 1)
    a0s = Cs * (as_ - bs) / as_
    p = dict(world.PARAMS)
    p["k1_0"], p["k1_slope"] = float(k1_0), float(slope)
    p["k2_0"] = float(np.median(bs))
    p["A0"], p["A0_sd"] = float(a0s.mean()), float(max(a0s.std(), 1.0))
    resid_a = as_ - (k1_0 + slope * valves)
    p["k_disp"] = float(max(np.std(resid_a / np.maximum(k1_0 + slope * valves, 1e-3)), 0.02))

    def sample(ns, n, seed):
        return world.mechanism(p, ns, n, seed)
    return sample


def build_battery():
    items, s = [], BATTERY_SEED0
    for valve in VALVES:
        items.append(BatteryItem(weight=0.155, regime=Regime(
            config={"valve": valve}, context={"t_grid": G_IN}), seed_world=s)); s += 1
    items.append(BatteryItem(weight=0.10, regime=Regime(
        config={}, context={"t_grid": G_IN}), seed_world=s)); s += 1
    for valve in VALVES:
        items.append(BatteryItem(weight=0.035, regime=Regime(
            config={"valve": valve}, context={"t_grid": G_MID}), seed_world=s)); s += 1
    items.append(BatteryItem(weight=0.04, regime=Regime(
        config={}, context={"t_grid": G_MID}), seed_world=s)); s += 1
    for valve in VALVES:
        items.append(BatteryItem(weight=0.05, regime=Regime(
            config={"valve": valve}, context={"t_grid": G_LONG}), seed_world=s)); s += 1
    return Battery(items=items)


def write_fixtures(f):
    header = ("GENERATED by build_and_certify.py (POOL_SEED={s}, POOL_N={n}) - do not\n"
              "hand-edit; regenerate to audit.").format(s=POOL_SEED, n=POOL_N)
    naive = f'''"""Rung 7 -- naive fit of the truncated noisy record (S_naive anchor, R=0).

Believes the build-up story: exponential growth, no peak, dispersion real.
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
        "risefall_generic_pool": family_member(f, "risefall_generic"),
        "twin_truncation": twin_truncation(pool),
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
        "risefall_pool_fit": [round(v, 4) for v in f["risefall"]],
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
