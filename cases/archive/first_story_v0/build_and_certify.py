"""first_story_v0 (#17 / Mundo A): battery + L1 gates + the ROBOT certificate.

The first anti-vice world (ADRs 0080/0081; spec docs/mundo-a-primera-historia.md).
The certified load (D5): prior_reliability=0 (the folklore is false) +
confounding-por-era (unlogged drifting ambient) + vice pressure (marrying the
first hypothesis). Derivation is case tooling (two-knob world breaks the
1-decision+1-context static machinery; registered like #11's finding 1).

PRE-REGISTERED (signed BEFORE running; D1-D5 of ADR 0081):
  - L1 order: truth(1) > perturbed_x1.15 > negador_agnostico? vs
    twin_folklore -- BOTH low is the requirement (D1 anti-cynic: disbelieving
    X without modeling Y must not pass); their relative order is reported.
  - Raw record correlation feedstock<->outcome in [0.5, 0.75] (the seduction
    is quotable); within-time-window slope ~ 0 (the cheap escape EXISTS).
  - ROBOT CERTIFICATE (distributional, D3 -- no magic numbers):
      (i)  |E[R_terco] - R(twin_folklore)| <= 3 x std(R_terco)   [terco IS the
           twin embodied as an episode policy]
      (ii) E[R_cuidadoso] >= 0.85 x R_techo (= 1.0, world.py anchor)
      (iii) both distributions (mean, std, per-seed) reported.
    Both robots run the REAL episode pipeline (verbs, budget, smoke).
  - Visibility: confound >= 0.05 R via twin_folklore. Null floor. No
    inversions.
  - Second currency: reject rate at do(grade=8, humidity=5) -- the twin
    predicts an improvement that never comes.

Run:  .venv/Scripts/python cases/first_story_v0/build_and_certify.py
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

import robots  # noqa: E402
import world  # noqa: E402

from wager.contracts import Battery, BatteryItem, CaseMeta  # noqa: E402
from wager.contracts.world import Regime  # noqa: E402
from wager.harness.source_view import source_view  # noqa: E402
from wager.reward.functionals import functional_value  # noqa: E402
from wager.reward.scorer import WorldSide, score_callable  # noqa: E402

FLOOR = 0.05
POOL_N, POOL_SEED = 4000, 50001
N_ROBOT_SEEDS = 5
GBAR = 5.0


def record_pool(meta):
    return source_view(world.sample, meta.episode.observe_sources["registros_linea"],
                       POOL_N, POOL_SEED)


def pool_fits(pool):
    f, y = pool["feedstock"].to_numpy(float), pool["outcome"].to_numpy(float)
    t = pool["t"].to_numpy(float)
    b, a = np.polyfit(f, y, 1)
    resid = float(np.std(y - (a + b * f)))
    within = []
    order = np.argsort(t)
    for chunk in np.array_split(order, 8):
        within.append(float(np.polyfit(f[chunk], y[chunk], 1)[0]))
    return {"a": float(a), "b": float(b), "resid": resid,
            "corr": float(np.corrcoef(f, y)[0, 1]),
            "b_within_median": float(np.median(within)),
            "f_mean": float(f.mean()), "f_sd": float(f.std()),
            "y_mean": float(y.mean()), "y_sd": float(y.std())}


def twin_folklore(fit):
    """'The record's correlation IS the cause': grade -> feedstock -> outcome;
    humidity does not exist. The terco robot is THIS belief as a policy."""
    def sample(ns, n, seed):
        import pandas as pd
        rng = np.random.default_rng(seed)
        g = float(ns.config.get("feedstock_grade", GBAR))
        f = fit["f_mean"] + (g - GBAR) + rng.normal(0.0, fit["f_sd"], n)
        y = fit["a"] + fit["b"] * f + rng.normal(0.0, fit["resid"], n)
        return pd.DataFrame({"feedstock": f, "outcome": y})
    return sample


def negador_agnostico(fit):
    """D1 anti-cynic rung: disbelieves X (no edge) but models NOTHING -- flat
    outcome under every knob. Must land LOW."""
    def sample(ns, n, seed):
        import pandas as pd
        rng = np.random.default_rng(seed)
        g = float(ns.config.get("feedstock_grade", GBAR))
        f = fit["f_mean"] + (g - GBAR) + rng.normal(0.0, fit["f_sd"], n)
        y = rng.normal(fit["y_mean"], fit["y_sd"], n)
        return pd.DataFrame({"feedstock": f, "outcome": y})
    return sample


def perturbed_truth(factor=1.15):
    p = dict(world.PARAMS)
    for k in ("y_amb_coef", "f_amb_coef", "u_coef"):
        p[k] = p[k] * factor

    def sample(ns, n, seed):
        return world.mechanism(p, ns, n, seed)
    return sample


def null_marginals(fit):
    def sample(ns, n, seed):
        import pandas as pd
        rng = np.random.default_rng(seed)
        return pd.DataFrame({"feedstock": rng.normal(fit["f_mean"], fit["f_sd"], n),
                             "outcome": rng.normal(fit["y_mean"], fit["y_sd"], n)})
    return sample


def build_battery():
    regs = [
        ({}, 0.10), ({}, 0.10),
        ({"humidity": 3.0}, 0.11), ({"humidity": 5.0}, 0.11), ({"humidity": 7.0}, 0.11),
        ({"feedstock_grade": 8.0, "humidity": 5.0}, 0.12),
        ({"feedstock_grade": 2.0, "humidity": 5.0}, 0.12),
        ({"feedstock_grade": 8.0}, 0.08),
        ({"line_speed": 8.0, "humidity": 5.0}, 0.07),
        ({"feedstock_grade": 8.0, "humidity": 7.0}, 0.09),
        ({"feedstock_grade": 2.0, "humidity": 3.0}, 0.09),
    ]
    items = [BatteryItem(weight=w, regime=Regime(config=c, context={}), seed_world=99001 + i)
             for i, (c, w) in enumerate(regs)]
    return Battery(items=items)


def write_truth_code():
    """world.sample carries the era column t (the record view needs it) but the
    DELIVERABLE is [feedstock, outcome] -- scored as a submission, world.py
    would fail the column contract. The episode S_truth anchor is therefore
    the truth_code.py fixture (v0.63 convention): the SAME mechanism, same RNG
    call order (t drawn, not returned), params baked."""
    p = dict(world.PARAMS)
    code = f'''"""truth_code -- the R=1 anchor of first_story_v0 (deliverable columns only).

Same mechanism and RNG call order as world.py; the era column t is drawn but
not returned. GENERATED by build_and_certify.py - do not hand-edit.
"""
import numpy as np
import pandas as pd

PARAMS = {p!r}
KNOB_MIN, KNOB_MAX = {world.KNOB_MIN!r}, {world.KNOB_MAX!r}


def model(regime, n, seed):
    p = PARAMS
    rng = np.random.default_rng(seed)
    u = rng.normal(0.0, p["u_sd"], n)
    if "humidity" in regime.config:
        ambient = np.full(n, float(regime.config["humidity"])) + rng.normal(0.0, p["amb_noise"], n)
    else:
        t = rng.uniform(0.0, 1.0, n)
        ambient = p["amb_base"] + p["amb_drift"] * t + rng.normal(0.0, p["amb_noise"], n)
    if "feedstock_grade" in regime.config:
        grade = np.full(n, float(regime.config["feedstock_grade"]))
    else:
        grade = np.clip(rng.normal(p["grade_base"], p["grade_sd"], n), KNOB_MIN, KNOB_MAX)
    feedstock = (p["f_base"] + p["grade_coef"] * (grade - p["grade_base"])
                 - p["f_amb_coef"] * (ambient - p["amb_center"])
                 + rng.normal(0.0, p["f_noise"], n))
    outcome = (p["y_base"] - p["y_amb_coef"] * (ambient - p["amb_center"])
               + p["u_coef"] * u + rng.normal(0.0, p["y_noise"], n))
    return pd.DataFrame({{"feedstock": feedstock, "outcome": outcome}})
'''
    (CASE / "truth_code.py").write_text(code, encoding="utf-8", newline="\n")


def write_fixtures(fit):
    header = f"GENERATED by build_and_certify.py (POOL_SEED={POOL_SEED}) - do not hand-edit."
    naive = f'''"""Rung 7 -- the record-believer (S_naive anchor, R=0): grade moves the
reading, the reading moves quality; the hall does not exist. {header}"""
import numpy as np
import pandas as pd


def model(regime, n, seed):
    rng = np.random.default_rng(seed)
    g = float(regime.config.get("feedstock_grade", {GBAR}))
    f = {fit["f_mean"]} + (g - {GBAR}) + rng.normal(0.0, {fit["f_sd"]}, n)
    y = {fit["a"]} + {fit["b"]} * f + rng.normal(0.0, {fit["resid"]}, n)
    return pd.DataFrame({{"feedstock": f, "outcome": y}})
'''
    null = f'''"""Rung 8 -- null: independent record marginals (S_null / D_MAX). {header}"""
import numpy as np
import pandas as pd


def model(regime, n, seed):
    rng = np.random.default_rng(seed)
    return pd.DataFrame({{"feedstock": rng.normal({fit["f_mean"]}, {fit["f_sd"]}, n),
                          "outcome": rng.normal({fit["y_mean"]}, {fit["y_sd"]}, n)}})
'''
    ladder = CASE / "ladder"
    ladder.mkdir(exist_ok=True)
    (ladder / "rung_7_naive_record.py").write_text(naive, encoding="utf-8", newline="\n")
    (ladder / "rung_8_null.py").write_text(null, encoding="utf-8", newline="\n")


def main():
    meta = CaseMeta.from_json_file(CASE / "meta.json")
    params = meta.scoring
    pool = record_pool(meta)
    fit = pool_fits(pool)
    write_truth_code()
    write_fixtures(fit)

    battery = build_battery()
    battery.to_json_file(CASE / "battery.json")
    null_fn = null_marginals(fit)
    ws = WorldSide(world.sample, battery, meta.column_names, params.n_samples,
                   null_sample=null_fn, functionals=meta.stakes.functionals,
                   c_f=params.c_f)
    s_truth = score_callable(world.sample, ws, params)
    naive_fn = twin_folklore(fit)  # the record-believer IS the naive anchor here
    s_naive = score_callable(naive_fn, ws, params)
    den = s_truth - s_naive

    def R(fn):
        return (score_callable(fn, ws, params) - s_naive) / den

    r = {
        "perturbed_x1.15": R(perturbed_truth()),
        "twin_folklore": 0.0,  # anchor by construction (R=0)
        "negador_agnostico": R(negador_agnostico(fit)),
        "null": R(null_fn),
    }

    # --- ROBOT CERTIFICATE (distributional, episode pipeline) ----------------
    runs = {"terco": [], "cuidadoso": []}
    for robot in runs:
        for k in range(N_ROBOT_SEEDS):
            runs[robot].append(robots.run_robot(CASE, robot, seed_offset=k))
    stats = {robot: {"mean_R": float(np.mean([x["R"] for x in v])),
                     "std_R": float(np.std([x["R"] for x in v])),
                     "per_seed": [round(x["R"], 4) for x in v]}
             for robot, v in runs.items()}

    spec = meta.stakes.functionals[0]
    ns_cf = SimpleNamespace(config={"feedstock_grade": 8.0, "humidity": 5.0},
                            context={}, horizon=None)
    reject = {
        "truth": round(functional_value(spec, world.sample(ns_cf, 4000, 424242)), 4),
        "twin_folklore": round(functional_value(spec, naive_fn(ns_cf, 4000, 424242)), 4),
    }

    report = {
        "denom_raw": den, "R": {k: round(v, 4) for k, v in r.items()},
        "record_corr": round(fit["corr"], 3),
        "record_slope_pooled": round(fit["b"], 3),
        "record_slope_within_time": round(fit["b_within_median"], 3),
        "robots": stats,
        "reject_do_grade8_h5": reject,
        "battery_k": len(battery.items),
        "certified_load": ["prior_reliability=0", "confounding_por_era", "vicio:primera-hipotesis"],
        "gates": {},
    }
    g = report["gates"]
    g["seduction_band"] = 0.5 <= fit["corr"] <= 0.75
    g["cheap_escape_exists"] = abs(fit["b_within_median"]) <= 0.25 * abs(fit["b"])
    g["no_inversions"] = all(v <= 1.0 + 0.02 for v in r.values())
    g["null_floor"] = r["null"] < 0.0
    g["anticinico_bajo"] = r["negador_agnostico"] < 1.0 - FLOOR
    g["terco_twin_identity"] = abs(stats["terco"]["mean_R"] - 0.0) <= max(
        3 * stats["terco"]["std_R"], 0.05)
    g["cuidadoso_reaches"] = stats["cuidadoso"]["mean_R"] >= 0.85
    g["all"] = all(v for v in g.values())

    print(json.dumps(report, indent=2))
    (CASE / "certificates.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print("-> battery.json + certificates.json + ladder fixtures")


if __name__ == "__main__":
    main()
