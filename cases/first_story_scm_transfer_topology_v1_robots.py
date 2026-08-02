"""Zero-LLM reflex robots shared by the four topology poles."""

from __future__ import annotations

import numpy as np

from wager.harness.case_episode import build_world_server


def model_code(north: str) -> str:
    """Return one of the four fixed structural policies as executable code."""
    if north not in {"retain", "revise", "local", "latent"}:
        raise ValueError(north)
    return f'''\
import numpy as np
import pandas as pd

NORTH = {north!r}
SELECTOR_STREAM = 0x544F504F

def model(regime, n, seed):
    rng = np.random.default_rng(seed)
    era = rng.uniform(0.0, 1.0, n)
    eps_h = rng.normal(0.0, 0.5, n)
    eps_f = rng.normal(0.0, 0.9, n)
    eps_y = rng.normal(0.0, 2.0, n)
    cfg = regime.config
    h = np.full(n, float(cfg["humidity"])) if "humidity" in cfg else 2.0 + 6.0*era + eps_h
    g = np.full(n, float(cfg["feedstock_grade"])) if "feedstock_grade" in cfg else 10.0 - h
    mu_g = 20.0 + 2.0*g
    mu_h = 40.0 - 2.0*h
    south = str(regime.context.get("site", "south")).lower() == "south"
    batch_class = regime.context.get("batch_class")
    if south:
        mu = mu_g
    elif "feedstock_grade" not in cfg:
        mu = mu_h
    elif NORTH == "retain":
        mu = mu_g
    elif NORTH == "revise":
        mu = mu_h
    elif NORTH == "local":
        if batch_class is None:
            srng = np.random.default_rng(np.random.SeedSequence([int(seed), SELECTOR_STREAM]))
            use_h = srng.random(n) < 0.75
        else:
            use_h = np.full(n, str(batch_class).upper() == "A", dtype=bool)
        mu = np.where(use_h, mu_h, mu_g)
    else:
        srng = np.random.default_rng(np.random.SeedSequence([int(seed), SELECTOR_STREAM]))
        mu = np.where(srng.random(n) < 0.75, mu_h, mu_g)
    return pd.DataFrame({{"feedstock": g + eps_f, "outcome": mu + eps_y}})
'''


ROBOT_MODELS = {
    "always_retain": "retain",
    "always_revise": "revise",
    "always_split_by_class": "local",
    "always_mix": "latent",
}


def run_robot(case_dir, robot: str, seed_offset: int = 0) -> dict:
    if robot not in ROBOT_MODELS:
        raise ValueError(robot)
    server = build_world_server(case_dir, seed_offset=seed_offset)
    observed = server.observe("south_production_history", 400)
    choice = ROBOT_MODELS[robot]
    result = server.submit(model_code(choice))
    return {
        "robot": robot,
        "chosen_model": choice,
        "south_rows": len(observed),
        "south_class_A_fraction": float(
            np.mean(observed["batch_class"].to_numpy() == "A")
        ),
        "accepted": result.accepted,
        "R": float(server.result["R"]),
        "R_unclipped": float(server.result["R_unclipped"]),
    }
