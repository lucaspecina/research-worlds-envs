"""kiln_glaze_firing_bias_gen_v0 -- GENERATED confounded static world (proto-designer MEDIO pilot, ADR 0128).

Domain: Industrial ceramic tile firing where operators tune kiln soak intensity to maximize post-fire glaze appearance. Confounding trap: a latent green_body_moisture_balance drives BOTH the historical
soak_intensity assignment AND the glaze_finish_score, so the record's soak_intensity->glaze_finish_score slope is
confounded; experiments (do) de-confound. Server-side only.
"""

import numpy as np
import pandas as pd

COLUMNS = ["soak_intensity", "dryer_exit_signature", "glaze_finish_score"]

PARAMS = {'u_sd': 1.0, 'proxy_coef': 1.3, 'proxy_noise': 1.1, 'base': 21.4, 'driver_coef': 1.2, 'u_coef': 4.7, 'outcome_noise': 1.8, 'shift_coef': 1.0, 'driver_base': 5.1, 'driver_sd': 1.5, 'confound_coef': -2.4}
DRIVER_MIN, DRIVER_MAX = 0.0, 10.0


def mechanism(params, regime, n, seed):
    p = params
    rng = np.random.default_rng(seed)
    shift = float(regime.context.get("shift", 0.0))
    u = rng.normal(0.0, p["u_sd"], n)
    dryer_exit_signature = p["proxy_coef"] * u + rng.normal(0.0, p["proxy_noise"], n)
    if "soak_intensity" in regime.config:
        soak_intensity = np.full(n, float(regime.config["soak_intensity"]))
    else:
        soak_intensity = np.clip(rng.normal(p["driver_base"] + p["confound_coef"] * u, p["driver_sd"], n),
                           DRIVER_MIN, DRIVER_MAX)
    glaze_finish_score = (p["base"] + p["driver_coef"] * soak_intensity + p["u_coef"] * u
                 + p["shift_coef"] * shift + rng.normal(0.0, p["outcome_noise"], n))
    return pd.DataFrame({"soak_intensity": soak_intensity, "dryer_exit_signature": dryer_exit_signature, "glaze_finish_score": glaze_finish_score})


def sample(regime, n, seed):
    return mechanism(PARAMS, regime, n, seed)


model = sample
