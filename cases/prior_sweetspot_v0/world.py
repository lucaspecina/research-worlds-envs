"""prior_sweetspot_v0 -- the trustworthy-prior control: a real sweet spot.

The truth of the case. Server-side only: the agent never sees this file.

E1-matrix slot #16 (queue ADR 0075): first world of the Prior suite, CONTROL
bucket. The brief evokes the most textbook process prior there is -- "too
little cures poorly, too much scorches; the veterans say there is a sweet
spot" -- and the world REALLY behaves that way (the treacherous sibling is
slot #17, design pile). Its E1 job: the baseline where invoking a correct
prior helps and distrusting everything merely costs budget; paired with #17
it measures prior-vs-evidence discrimination.

No source traps (control isolates judgment-vs-execution): clean sources with
ambient meter noise (replicas identify sigma). ONE mechanism operator -- the
curvature itself; its innocent twin (the linear believer) extrapolates the
record's local slope straight past the optimum.

Mechanism per unit (latent quality u -- never a column):

    u       ~ N(0, 1)
    signal  = 1.0*u + N(0, 1.5)
    driver  = clip(N(4.5, 1.2), 0, 10) historically   (settable 0-10; optimum at 6)
    outcome = 30 - 0.9*(driver - 6)^2 + 4*u + 1.0*shift + N(0, 2)
"""

import numpy as np
import pandas as pd

COLUMNS = ["driver", "signal", "outcome"]

PARAMS = {
    "u_sd": 1.0,
    "signal_coef": 1.0,
    "signal_noise": 1.5,
    "peak": 30.0,
    "curvature": 0.9,
    "d_opt": 6.0,
    "u_coef": 4.0,
    "shift_coef": 1.0,
    "outcome_noise": 2.0,
    "driver_base": 4.5,
    "driver_sd": 1.2,
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
    outcome = (p["peak"] - p["curvature"] * (driver - p["d_opt"]) ** 2 + p["u_coef"] * u
               + p["shift_coef"] * shift + rng.normal(0.0, p["outcome_noise"], n))
    return pd.DataFrame({"driver": driver, "signal": signal, "outcome": outcome})


def sample(regime, n, seed):
    return mechanism(PARAMS, regime, n, seed)


model = sample
