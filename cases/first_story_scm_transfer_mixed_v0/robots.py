"""Zero-LLM episode robots for the mixed South-to-North transfer pole."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from wager.contracts import ExperimentDesign  # noqa: E402


def _model_code(north: str) -> str:
    if north not in {"retain", "revise", "mixed", "moment_matched"}:
        raise ValueError(north)
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
    mu_g = 20.0 + 2.0*g
    mu_h = 40.0 - 2.0*h
    south = str(regime.context.get("site", "south")).lower() == "south"
    if south:
        mu = mu_g
    elif "feedstock_grade" not in regime.config:
        mu = mu_h
    else:
        north_model = {north!r}
        if north_model == "retain":
            mu = mu_g
        elif north_model == "revise":
            mu = mu_h
        elif north_model == "mixed":
            selector_rng = np.random.default_rng(
                np.random.SeedSequence([int(seed), 0x4D49584544])
            )
            mu = np.where(selector_rng.random(n) < 0.75, mu_h, mu_g)
        else:
            mu = 0.75 * mu_h + 0.25 * mu_g
            component_gap = mu_h - mu_g
            ey = rng.normal(
                0.0, np.sqrt(4.0 + 0.75 * 0.25 * component_gap**2), n
            )
    return pd.DataFrame({{"feedstock": g + ef, "outcome": mu + ey}})
'''


def _south_history(server) -> None:
    server.observe("south_production_history", 400)


def _submit(server, model_name: str) -> dict:
    _south_history(server)
    result = server.submit(_model_code(model_name))
    return {"accepted": result.accepted, "chosen_model": model_name}


def run_never_update(server) -> dict:
    return _submit(server, "retain")


def run_change_always(server) -> dict:
    return _submit(server, "revise")


def run_moment_matched(server) -> dict:
    return _submit(server, "moment_matched")


def run_adaptive(server) -> dict:
    _south_history(server)
    low = server.experiment(
        ExperimentDesign(
            config={"humidity": 5.0, "feedstock_grade": 3.0},
            context={"site": "north"},
            n=180,
        )
    )
    high = server.experiment(
        ExperimentDesign(
            config={"humidity": 5.0, "feedstock_grade": 7.0},
            context={"site": "north"},
            n=180,
        )
    )
    delta = float(high["outcome"].mean() - low["outcome"].mean())
    if delta > 5.0:
        model_name = "retain"
    elif delta < 1.0:
        model_name = "revise"
    else:
        model_name = "mixed"
    result = server.submit(_model_code(model_name))
    return {
        "accepted": result.accepted,
        "chosen_model": model_name,
        "north_delta_y": delta,
    }


ROBOTS = {
    "never_update": run_never_update,
    "change_always": run_change_always,
    "moment_matched": run_moment_matched,
    "adaptive": run_adaptive,
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


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("robot", choices=sorted(ROBOTS), default="adaptive")
    parser.add_argument("--seed-offset", type=int, default=84_000)
    args = parser.parse_args()
    print(
        json.dumps(
            run_robot(Path(__file__).resolve().parent, args.robot, args.seed_offset),
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
