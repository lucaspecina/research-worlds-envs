"""confounded_gen_v0 -- GENERATED confounded static world (proto-designer MEDIO, ADR 0093).

Domain: injection molding of medical syringe barrels. Confounding trap: a latent resin_dryness drives BOTH the historical
pack_pressure assignment AND the clarity_seal_score, so the record's pack_pressure->clarity_seal_score slope is
confounded; experiments (do) de-confound. Server-side only.
"""

import numpy as np
import pandas as pd

COLUMNS = ["pack_pressure", "cavity_fill_time", "clarity_seal_score"]

PARAMS = {'u_sd': 1.0, 'proxy_coef': 1.3, 'proxy_noise': 1.2, 'base': 12.0, 'driver_coef': 1.8, 'u_coef': 6.0, 'outcome_noise': 1.80625, 'shift_coef': 1.0, 'driver_base': 5.0, 'driver_sd': 1.5, 'confound_coef': 2.2399999999999998}
DRIVER_MIN, DRIVER_MAX = 0.0, 10.0


def mechanism(params, regime, n, seed):
    p = params
    rng = np.random.default_rng(seed)
    shift = float(regime.context.get("shift", 0.0))
    u = rng.normal(0.0, p["u_sd"], n)
    cavity_fill_time = p["proxy_coef"] * u + rng.normal(0.0, p["proxy_noise"], n)
    if "pack_pressure" in regime.config:
        pack_pressure = np.full(n, float(regime.config["pack_pressure"]))
    else:
        pack_pressure = np.clip(rng.normal(p["driver_base"] + p["confound_coef"] * u, p["driver_sd"], n),
                           DRIVER_MIN, DRIVER_MAX)
    clarity_seal_score = (p["base"] + p["driver_coef"] * pack_pressure + p["u_coef"] * u
                 + p["shift_coef"] * shift + rng.normal(0.0, p["outcome_noise"], n))
    return pd.DataFrame({"pack_pressure": pack_pressure, "cavity_fill_time": cavity_fill_time, "clarity_seal_score": clarity_seal_score})


def sample(regime, n, seed):
    return mechanism(PARAMS, regime, n, seed)


model = sample
