"""Executable ceiling: grade response in South and both North classes."""

import numpy as np
import pandas as pd

POLE = "retain"
_SELECTOR_STREAM = 0x544F504F


def _selector(n, seed):
    rng = np.random.default_rng(
        np.random.SeedSequence([int(seed), _SELECTOR_STREAM])
    )
    return rng.random(n) < 0.75


def model(regime, n, seed):
    rng = np.random.default_rng(seed)
    era = rng.uniform(0.0, 1.0, n)
    eps_h = rng.normal(0.0, 0.5, n)
    eps_f = rng.normal(0.0, 0.9, n)
    eps_y = rng.normal(0.0, 2.0, n)
    cfg = regime.config
    site = str(regime.context.get("site", "south")).lower()
    fixed_class = regime.context.get("batch_class")
    if fixed_class is not None:
        fixed_class = str(fixed_class).upper()
        if fixed_class not in {"A", "B"}:
            raise ValueError("batch_class must be A or B")
    humidity = (
        np.full(n, float(cfg["humidity"]))
        if "humidity" in cfg
        else 2.0 + 6.0 * era + eps_h
    )
    grade = (
        np.full(n, float(cfg["feedstock_grade"]))
        if "feedstock_grade" in cfg
        else 10.0 - humidity
    )
    mu_grade = 20.0 + 2.0 * grade
    mu_humidity = 40.0 - 2.0 * humidity
    if site == "south":
        mu = mu_grade
    elif "feedstock_grade" not in cfg:
        mu = mu_humidity
    elif POLE == "retain":
        mu = mu_grade
    elif POLE == "revise":
        mu = mu_humidity
    elif POLE == "local":
        use_humidity = (
            np.full(n, fixed_class == "A", dtype=bool)
            if fixed_class is not None
            else _selector(n, seed)
        )
        mu = np.where(use_humidity, mu_humidity, mu_grade)
    else:
        mu = np.where(_selector(n, seed), mu_humidity, mu_grade)
    return pd.DataFrame(
        {"feedstock": grade + eps_f, "outcome": mu + eps_y}
    )
