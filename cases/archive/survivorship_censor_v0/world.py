"""survivorship_censor_v0 -- intake-screened, bench-capped endurance records.

The truth of the case. Server-side only: the agent never sees this file.

E1-matrix slot #7 (queue ADR 0075). Static SCM, world-3 family: the traps live
in the SOURCES, world.sample() is clean. Composition (3 declared corruptions,
>=2 coordinate load):

  - seleccion_supervivencia (sampling): the record only contains units that
    passed the intake screen (stress reading above a bar). Robust units pass
    more often -> the record's endurance distribution is OPTIMISTIC: the low
    tail -- where the stakes live -- was never written down.
  - censura_archivo (archival, NEW layer ADR 0077): the old bench topped out
    at 45; anything better was recorded AS 45 (pile-up). Records-only:
    experiments (fresh logging) bypass it.
  - error_de_medicion (channel): zero-mean meter noise on endurance; sigma
    identifiable via the replicated source (v0.51). Never bypassed (v0.9).

Mechanism per unit (latent robustness u -- never a column):

    u       ~ N(0, 1)
    stress  = 2*u + N(0, 1)                       # intake reading (observable)
    driver  = clip(N(5, 1.5), 0, 10) historically  (settable 0-10 under do())
    outcome = 20 + 3*driver + 8*u + 1.5*shift + N(0, 3)

The client is REMOVING the intake screen to cut cost: the decision population
is ALL units (battery = full population, contract v0.50-3) -- pricing the
low tail the record never showed is exactly the job.
"""

import numpy as np
import pandas as pd

COLUMNS = ["driver", "stress", "outcome"]

# Parameterization note (single pre-certification iteration, ADR 0077 --
# bright line: declared + registered, world-3 precedent v0.55): first build
# had sigma_med=2.0 economically invisible vs intrinsic noise (v0.38 doctrine),
# cap=45 touching too little battery mass, and stress so informative that the
# no-latent ladder sat at 0.99 (the v0.42 lesson). This world DECLARES theory
# gap ~ 0 (it loads on sampling+archival+channel, not representation).
PARAMS = {
    "u_sd": 1.0,
    "stress_coef": 1.5,
    "stress_noise": 1.2,
    "base": 20.0,
    "driver_coef": 3.0,
    "u_coef": 8.0,
    "shift_coef": 1.5,
    "outcome_noise": 3.0,
    "driver_base": 5.0,
    "driver_sd": 1.5,
}
DRIVER_MIN, DRIVER_MAX = 0.0, 10.0


def mechanism(params, regime, n, seed):
    p = params
    rng = np.random.default_rng(seed)
    shift = float(regime.context.get("shift", 0.0))
    u = rng.normal(0.0, p["u_sd"], n)
    stress = p["stress_coef"] * u + rng.normal(0.0, p["stress_noise"], n)
    if "driver" in regime.config:
        driver = np.full(n, float(regime.config["driver"]))
    else:
        driver = np.clip(rng.normal(p["driver_base"], p["driver_sd"], n),
                         DRIVER_MIN, DRIVER_MAX)
    outcome = (p["base"] + p["driver_coef"] * driver + p["u_coef"] * u
               + p["shift_coef"] * shift + rng.normal(0.0, p["outcome_noise"], n))
    return pd.DataFrame({"driver": driver, "stress": stress, "outcome": outcome})


def sample(regime, n, seed):
    return mechanism(PARAMS, regime, n, seed)


model = sample
