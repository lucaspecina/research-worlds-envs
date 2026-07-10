"""paper_mill_dryer_balance_gen_v0 -- GENERATED confounded static world (proto-designer MEDIO pilot, ADR 0128).

Domain: Fine-paper mill dryer balance tuning for sheet finish quality. Confounding trap: a latent incoming_pulp_drainability drives BOTH the historical
dryer_balance_index assignment AND the sheet_finish_score, so the record's dryer_balance_index->sheet_finish_score slope is
confounded; experiments (do) de-confound. Server-side only.
"""

import numpy as np
import pandas as pd

COLUMNS = ["dryer_balance_index", "wet_end_response_signal", "sheet_finish_score"]

PARAMS = {'u_sd': 1.0, 'proxy_coef': 1.3, 'proxy_noise': 1.1, 'base': 24.0, 'driver_coef': 1.2, 'u_coef': 4.6, 'outcome_noise': 1.7, 'shift_coef': 1.0, 'driver_base': 5.1, 'driver_sd': 1.5, 'confound_coef': 1.4}
DRIVER_MIN, DRIVER_MAX = 0.0, 10.0


def mechanism(params, regime, n, seed):
    p = params
    rng = np.random.default_rng(seed)
    shift = float(regime.context.get("shift", 0.0))
    u = rng.normal(0.0, p["u_sd"], n)
    wet_end_response_signal = p["proxy_coef"] * u + rng.normal(0.0, p["proxy_noise"], n)
    if "dryer_balance_index" in regime.config:
        dryer_balance_index = np.full(n, float(regime.config["dryer_balance_index"]))
    else:
        dryer_balance_index = np.clip(rng.normal(p["driver_base"] + p["confound_coef"] * u, p["driver_sd"], n),
                           DRIVER_MIN, DRIVER_MAX)
    sheet_finish_score = (p["base"] + p["driver_coef"] * dryer_balance_index + p["u_coef"] * u
                 + p["shift_coef"] * shift + rng.normal(0.0, p["outcome_noise"], n))
    return pd.DataFrame({"dryer_balance_index": dryer_balance_index, "wet_end_response_signal": wet_end_response_signal, "sheet_finish_score": sheet_finish_score})


def sample(regime, n, seed):
    return mechanism(PARAMS, regime, n, seed)


model = sample
