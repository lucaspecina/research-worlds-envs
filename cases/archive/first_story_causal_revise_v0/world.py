"""Paired causal probe, humidity-response pole.

The agent never sees this file. Observational draws are byte-identical to the
retain pole; interventions distinguish which member of the historical pair is
causal for outcome.
"""

import numpy as np
import pandas as pd

POLE = "revise"
HISTORICAL_HUMIDITY_SD = 0.30
AMBIENT_SD = 0.70
FEEDSTOCK_SD = 0.50
OUTCOME_SD = 1.50


def sample(regime, n, seed):
    rng = np.random.default_rng(seed)
    cfg = regime.config
    intervention = "feedstock_grade" in cfg or "humidity" in cfg

    if not intervention:
        era = rng.uniform(0.0, 1.0, n)
        humidity = 2.0 + 6.0 * era + rng.normal(0.0, HISTORICAL_HUMIDITY_SD, n)
        grade = 10.0 - humidity
    else:
        humidity = (
            np.full(n, float(cfg["humidity"]))
            if "humidity" in cfg
            else rng.normal(5.0, AMBIENT_SD, n)
        )
        grade = (
            np.full(n, float(cfg["feedstock_grade"]))
            if "feedstock_grade" in cfg
            else rng.normal(5.0, AMBIENT_SD, n)
        )

    feedstock = grade + rng.normal(0.0, FEEDSTOCK_SD, n)
    outcome_noise = rng.normal(0.0, OUTCOME_SD, n)
    if not intervention:
        # This common expression is deliberately identical in both files.
        outcome = 40.0 - 2.0 * humidity + outcome_noise
    elif POLE == "revise":
        outcome = 40.0 - 2.0 * humidity + outcome_noise
    else:
        outcome = 20.0 + 2.0 * grade + outcome_noise
    return pd.DataFrame({"feedstock": feedstock, "outcome": outcome})


model = sample
