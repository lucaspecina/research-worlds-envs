"""Zero-LLM episode robots for the paired hidden-SCM probe."""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from wager.contracts import ExperimentDesign  # noqa: E402


def _pole_code(pole: str) -> str:
    outcome = (
        "mu = 40.0 - 2.0*h"
        if pole == "revise"
        else "mu = 20.0 + 2.0*g if g_set else 40.0 - 2.0*h"
    )
    return f'''\
import numpy as np
import pandas as pd

def model(regime, n, seed):
    rng = np.random.default_rng(seed)
    t = rng.uniform(0.0, 1.0, n)
    eh = rng.normal(0.0, 0.5, n)
    ef = rng.normal(0.0, 0.9, n)
    ey = rng.normal(0.0, 2.0, n)
    h = np.full(n, float(regime.config["humidity"])) if "humidity" in regime.config else 2.0 + 6.0*t + eh
    g_set = "feedstock_grade" in regime.config
    g = np.full(n, float(regime.config["feedstock_grade"])) if g_set else 10.0 - h
    {outcome}
    return pd.DataFrame({{"feedstock": g + ef, "outcome": mu + ey}})
'''


def _prior_code() -> str:
    return '''\
import numpy as np
import pandas as pd

def model(regime, n, seed):
    rng = np.random.default_rng(seed)
    t = rng.uniform(0.0, 1.0, n)
    eh = rng.normal(0.0, 0.5, n)
    ef = rng.normal(0.0, 0.9, n)
    ey = rng.normal(0.0, 2.0, n)
    choose_g = rng.random(n) < 0.5
    h = np.full(n, float(regime.config["humidity"])) if "humidity" in regime.config else 2.0 + 6.0*t + eh
    g_set = "feedstock_grade" in regime.config
    g = np.full(n, float(regime.config["feedstock_grade"])) if g_set else 10.0 - h
    mu_h = 40.0 - 2.0*h
    mu_g = 20.0 + 2.0*g if g_set else mu_h
    return pd.DataFrame({"feedstock": g + ef, "outcome": np.where(choose_g, mu_g, mu_h) + ey})
'''


def run_never_update(server) -> dict:
    server.observe("production_history", 400)
    result = server.submit(_pole_code("retain"))
    return {"accepted": result.accepted, "chosen_pole": "retain"}


def run_change_always(server) -> dict:
    server.observe("production_history", 400)
    result = server.submit(_pole_code("revise"))
    return {"accepted": result.accepted, "chosen_pole": "revise"}


def run_adaptive(server) -> dict:
    server.observe("production_history", 400)
    low = server.experiment(
        ExperimentDesign(config={"humidity": 5.0, "feedstock_grade": 3.0}, n=120)
    )
    high = server.experiment(
        ExperimentDesign(config={"humidity": 5.0, "feedstock_grade": 7.0}, n=120)
    )
    delta = float(high["outcome"].mean() - low["outcome"].mean())
    pole = "retain" if abs(delta) > 4.0 else "revise"
    result = server.submit(_pole_code(pole))
    return {"accepted": result.accepted, "chosen_pole": pole, "delta_y": delta}


def run_humidity_only(server) -> dict:
    server.observe("production_history", 400)
    low = server.experiment(ExperimentDesign(config={"humidity": 3.0}, n=120))
    high = server.experiment(ExperimentDesign(config={"humidity": 7.0}, n=120))
    delta = float(high["outcome"].mean() - low["outcome"].mean())
    result = server.submit(_prior_code())
    return {"accepted": result.accepted, "chosen_pole": "prior", "delta_y": delta}


def run_associational(server) -> dict:
    history = server.observe("production_history", 500)
    f = history["feedstock"].to_numpy(float)
    y = history["outcome"].to_numpy(float)
    slope, intercept = np.polyfit(f, y, 1)
    resid_sd = float(np.std(y - (intercept + slope * f)))
    code = f'''\
import numpy as np
import pandas as pd

def model(regime, n, seed):
    rng = np.random.default_rng(seed)
    if "feedstock_grade" in regime.config:
        center = float(regime.config["feedstock_grade"])
    elif "humidity" in regime.config:
        center = 10.0 - float(regime.config["humidity"])
    else:
        center = 5.0
    f = center + rng.normal(0.0, 2.015 if not regime.config else 0.9, n)
    y = {float(intercept)!r} + {float(slope)!r}*f + rng.normal(0.0, {resid_sd!r}, n)
    return pd.DataFrame({{"feedstock": f, "outcome": y}})
'''
    result = server.submit(code)
    return {
        "accepted": result.accepted,
        "chosen_pole": "associational_grade",
        "historical_slope": float(slope),
    }


ROBOTS = {
    "never_update": run_never_update,
    "change_always": run_change_always,
    "adaptive": run_adaptive,
    "humidity_only": run_humidity_only,
    "associational": run_associational,
}


def run_robot(case_dir, robot: str, seed_offset: int = 0) -> dict:
    from wager.harness.case_episode import build_world_server

    server = build_world_server(case_dir, seed_offset=seed_offset)
    audit = ROBOTS[robot](server)
    if server.result is None:
        raise RuntimeError(f"robot {robot!r} did not produce a scored submission")
    return audit | {
        "robot": robot,
        "R": float(server.result["R"]),
        "R_unclipped": float(server.result["R_unclipped"]),
        "budget_remaining": float(server.budget_remaining),
    }
