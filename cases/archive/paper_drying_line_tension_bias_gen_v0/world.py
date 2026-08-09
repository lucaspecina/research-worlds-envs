"""paper_drying_line_tension_bias_gen_v0 -- GENERATED confounded static world (proto-designer MEDIO pilot, ADR 0128).

Domain: Industrial paper web drying line with operator-set felt tension affecting sheet quality. Confounding trap: a latent incoming_pulp_drainability drives BOTH the historical
felt_tension_setting assignment AND the sheet_quality_score, so the record's felt_tension_setting->sheet_quality_score slope is
confounded; experiments (do) de-confound. Server-side only.
"""

import numpy as np
import pandas as pd

COLUMNS = ["felt_tension_setting", "vacuum_box_signal", "sheet_quality_score"]

PARAMS = {'u_sd': 1.0, 'proxy_coef': 1.3, 'proxy_noise': 1.1, 'base': 21.4, 'driver_coef': 1.2, 'u_coef': 4.6, 'outcome_noise': 1.7, 'shift_coef': 1.0, 'driver_base': 5.1, 'driver_sd': 1.5, 'confound_coef': -2.4}
DRIVER_MIN, DRIVER_MAX = 0.0, 10.0


def mechanism(params, regime, n, seed):
    p = params
    rng = np.random.default_rng(seed)
    shift = float(regime.context.get("shift", 0.0))
    u = rng.normal(0.0, p["u_sd"], n)
    vacuum_box_signal = p["proxy_coef"] * u + rng.normal(0.0, p["proxy_noise"], n)
    if "felt_tension_setting" in regime.config:
        felt_tension_setting = np.full(n, float(regime.config["felt_tension_setting"]))
    else:
        felt_tension_setting = np.clip(rng.normal(p["driver_base"] + p["confound_coef"] * u, p["driver_sd"], n),
                           DRIVER_MIN, DRIVER_MAX)
    sheet_quality_score = (p["base"] + p["driver_coef"] * felt_tension_setting + p["u_coef"] * u
                 + p["shift_coef"] * shift + rng.normal(0.0, p["outcome_noise"], n))
    return pd.DataFrame({"felt_tension_setting": felt_tension_setting, "vacuum_box_signal": vacuum_box_signal, "sheet_quality_score": sheet_quality_score})


def sample(regime, n, seed):
    return mechanism(PARAMS, regime, n, seed)


model = sample
