"""paper_drying_line_brightness_control_gen_v0 -- GENERATED confounded static world (proto-designer MEDIO pilot, ADR 0128).

Domain: Industrial paper drying line where steam profile settings affect final sheet brightness score. Confounding trap: a latent incoming_pulp_bleachability drives BOTH the historical
steam_profile_bias assignment AND the final_brightness_score, so the record's steam_profile_bias->final_brightness_score slope is
confounded; experiments (do) de-confound. Server-side only.
"""

import numpy as np
import pandas as pd

COLUMNS = ["steam_profile_bias", "wet_end_fluorescence", "final_brightness_score"]

PARAMS = {'u_sd': 1.0, 'proxy_coef': 1.3, 'proxy_noise': 1.1, 'base': 24.0, 'driver_coef': 1.2, 'u_coef': 4.7, 'outcome_noise': 1.8, 'shift_coef': 1.0, 'driver_base': 5.1, 'driver_sd': 1.5, 'confound_coef': 1.4}
DRIVER_MIN, DRIVER_MAX = 0.0, 10.0


def mechanism(params, regime, n, seed):
    p = params
    rng = np.random.default_rng(seed)
    shift = float(regime.context.get("shift", 0.0))
    u = rng.normal(0.0, p["u_sd"], n)
    wet_end_fluorescence = p["proxy_coef"] * u + rng.normal(0.0, p["proxy_noise"], n)
    if "steam_profile_bias" in regime.config:
        steam_profile_bias = np.full(n, float(regime.config["steam_profile_bias"]))
    else:
        steam_profile_bias = np.clip(rng.normal(p["driver_base"] + p["confound_coef"] * u, p["driver_sd"], n),
                           DRIVER_MIN, DRIVER_MAX)
    final_brightness_score = (p["base"] + p["driver_coef"] * steam_profile_bias + p["u_coef"] * u
                 + p["shift_coef"] * shift + rng.normal(0.0, p["outcome_noise"], n))
    return pd.DataFrame({"steam_profile_bias": steam_profile_bias, "wet_end_fluorescence": wet_end_fluorescence, "final_brightness_score": final_brightness_score})


def sample(regime, n, seed):
    return mechanism(PARAMS, regime, n, seed)


model = sample
