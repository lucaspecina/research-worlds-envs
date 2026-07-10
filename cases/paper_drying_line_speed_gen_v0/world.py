"""paper_drying_line_speed_gen_v0 -- GENERATED confounded static world (proto-designer MEDIO pilot, ADR 0128).

Domain: Industrial paper mill drying section control for final sheet quality. Confounding trap: a latent incoming_pulp_drainability drives BOTH the historical
dryer_speed_bias assignment AND the roll_quality_score, so the record's dryer_speed_bias->roll_quality_score slope is
confounded; experiments (do) de-confound. Server-side only.
"""

import numpy as np
import pandas as pd

COLUMNS = ["dryer_speed_bias", "wet_end_drain_index", "roll_quality_score"]

PARAMS = {'u_sd': 1.0, 'proxy_coef': 1.3, 'proxy_noise': 1.1, 'base': 22.0, 'driver_coef': 1.2, 'u_coef': 4.6, 'outcome_noise': 1.7, 'shift_coef': 1.0, 'driver_base': 5.1, 'driver_sd': 1.5, 'confound_coef': -2.4}
DRIVER_MIN, DRIVER_MAX = 0.0, 10.0


def mechanism(params, regime, n, seed):
    p = params
    rng = np.random.default_rng(seed)
    shift = float(regime.context.get("shift", 0.0))
    u = rng.normal(0.0, p["u_sd"], n)
    wet_end_drain_index = p["proxy_coef"] * u + rng.normal(0.0, p["proxy_noise"], n)
    if "dryer_speed_bias" in regime.config:
        dryer_speed_bias = np.full(n, float(regime.config["dryer_speed_bias"]))
    else:
        dryer_speed_bias = np.clip(rng.normal(p["driver_base"] + p["confound_coef"] * u, p["driver_sd"], n),
                           DRIVER_MIN, DRIVER_MAX)
    roll_quality_score = (p["base"] + p["driver_coef"] * dryer_speed_bias + p["u_coef"] * u
                 + p["shift_coef"] * shift + rng.normal(0.0, p["outcome_noise"], n))
    return pd.DataFrame({"dryer_speed_bias": dryer_speed_bias, "wet_end_drain_index": wet_end_drain_index, "roll_quality_score": roll_quality_score})


def sample(regime, n, seed):
    return mechanism(PARAMS, regime, n, seed)


model = sample
