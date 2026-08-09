"""Zero-LLM episode robots for the South-to-North SCM transfer probe."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from wager.contracts import ExperimentDesign  # noqa: E402


def _pole_code(pole: str) -> str:
    north_mu = "40.0 - 2.0*h" if pole == "revise" else "20.0 + 2.0*g"
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
    g = np.full(n, float(regime.config["feedstock_grade"])) if "feedstock_grade" in regime.config else 10.0 - h
    south = str(regime.context.get("site", "south")).lower() == "south"
    mu = 20.0 + 2.0*g if south else {north_mu}
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
    g = np.full(n, float(regime.config["feedstock_grade"])) if "feedstock_grade" in regime.config else 10.0 - h
    mu_g = 20.0 + 2.0*g
    mu_h = 40.0 - 2.0*h
    south = str(regime.context.get("site", "south")).lower() == "south"
    mu = mu_g if south else np.where(choose_g, mu_g, mu_h)
    return pd.DataFrame({"feedstock": g + ef, "outcome": mu + ey})
'''


def _south_history(server) -> None:
    server.observe("south_production_history", 400)


def run_never_update(server) -> dict:
    _south_history(server)
    result = server.submit(_pole_code("retain"))
    return {"accepted": result.accepted, "chosen_pole": "retain"}


def run_change_always(server) -> dict:
    _south_history(server)
    result = server.submit(_pole_code("revise"))
    return {"accepted": result.accepted, "chosen_pole": "revise"}


def run_adaptive(server) -> dict:
    _south_history(server)
    # The first campaign is genuinely lived work that establishes the South
    # grade response before the same investigator transfers to North.
    server.experiment(
        ExperimentDesign(
            config={"humidity": 5.0, "feedstock_grade": 3.0},
            context={"site": "south"},
            n=120,
        )
    )
    server.experiment(
        ExperimentDesign(
            config={"humidity": 5.0, "feedstock_grade": 7.0},
            context={"site": "south"},
            n=120,
        )
    )
    low = server.experiment(
        ExperimentDesign(
            config={"humidity": 5.0, "feedstock_grade": 3.0},
            context={"site": "north"},
            n=120,
        )
    )
    high = server.experiment(
        ExperimentDesign(
            config={"humidity": 5.0, "feedstock_grade": 7.0},
            context={"site": "north"},
            n=120,
        )
    )
    delta = float(high["outcome"].mean() - low["outcome"].mean())
    pole = "retain" if abs(delta) > 4.0 else "revise"
    result = server.submit(_pole_code(pole))
    return {"accepted": result.accepted, "chosen_pole": pole, "north_delta_y": delta}


def run_humidity_only(server) -> dict:
    _south_history(server)
    low = server.experiment(
        ExperimentDesign(config={"humidity": 3.0}, context={"site": "north"}, n=120)
    )
    high = server.experiment(
        ExperimentDesign(config={"humidity": 7.0}, context={"site": "north"}, n=120)
    )
    delta = float(high["outcome"].mean() - low["outcome"].mean())
    result = server.submit(_prior_code())
    return {"accepted": result.accepted, "chosen_pole": "prior", "north_delta_y": delta}


def run_associational(server) -> dict:
    _south_history(server)
    result = server.submit(_pole_code("retain"))
    return {"accepted": result.accepted, "chosen_pole": "south_extension"}


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
