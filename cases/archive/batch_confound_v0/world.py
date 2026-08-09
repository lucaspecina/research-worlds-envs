"""batch_confound_v0 -- calibration drift confounded with the historical ramp.

The truth of the case. Server-side only: the agent never sees this file.

E1-matrix slot #9 (queue ADR 0075). Static SCM, world-3 family: traps in the
SOURCES, world.sample() clean. Composition (2 certified coordinates):

  - deriva_calibracion (channel/batch, ADR 0078): the record's readings come
    in batches whose meter offset DRIFTED over the era, while the operators
    ramped the driver over the same era -> the pooled driver->outcome slope
    absorbs the drift (inflated ~1.5x). The de-confounding move exists in the
    record itself (within-batch slopes are clean) or via experiments (fresh
    batches, no ramp).
  - offsets_por_tanda (channel/batch): idiosyncratic per-batch meter offsets
    -- present in experiments too (same instrument, v0.9): believing the
    between-batch scatter is real process variability is the second lie.

Meter noise sigma=1.5 stays declared AMBIENT (no visibility claim -- the #7
lesson: economically invisible against unit heterogeneity); the replicas
source still identifies it.

Mechanism per unit (latent quality u -- never a column):

    u       ~ N(0, 1)
    signal  = 1.2*u + N(0, 1.5)                    # inline reading (weak proxy)
    driver  = clip(N(5, 1.5), 0, 10) historically   (settable 0-10 under do())
    outcome = 8 + 2.5*driver + 5*u + 1.2*shift + N(0, 2)
"""

import numpy as np
import pandas as pd

COLUMNS = ["driver", "signal", "outcome"]

PARAMS = {
    "u_sd": 1.0,
    "signal_coef": 1.2,
    "signal_noise": 1.5,
    "base": 8.0,
    "driver_coef": 2.5,
    "u_coef": 5.0,
    "shift_coef": 1.2,
    "outcome_noise": 2.0,
    "driver_base": 5.0,
    "driver_sd": 1.5,
}
DRIVER_MIN, DRIVER_MAX = 0.0, 10.0


def mechanism(params, regime, n, seed):
    p = params
    rng = np.random.default_rng(seed)
    shift = float(regime.context.get("shift", 0.0))
    u = rng.normal(0.0, p["u_sd"], n)
    signal = p["signal_coef"] * u + rng.normal(0.0, p["signal_noise"], n)
    if "driver" in regime.config:
        driver = np.full(n, float(regime.config["driver"]))
    else:
        driver = np.clip(rng.normal(p["driver_base"], p["driver_sd"], n),
                         DRIVER_MIN, DRIVER_MAX)
    outcome = (p["base"] + p["driver_coef"] * driver + p["u_coef"] * u
               + p["shift_coef"] * shift + rng.normal(0.0, p["outcome_noise"], n))
    return pd.DataFrame({"driver": driver, "signal": signal, "outcome": outcome})


def sample(regime, n, seed):
    return mechanism(PARAMS, regime, n, seed)


model = sample
