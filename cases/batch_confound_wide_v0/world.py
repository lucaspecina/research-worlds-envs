"""batch_confound_wide_v0 -- THE WIDE PILOT (ADR 0085/0086): width alone.

The truth of the case. Server-side only: the agent never sees this file.

Hand-built (NOT the designer -- clean attribution, ADR 0086-1). Exactly #9's
world (same trap: calibration drift confounded with the era's driver ramp on
`outcome`; same params, same sources) WIDENED to 19 columns: 16 plausible,
CORRELATED distractors in four clusters, each with a declared story, NONE
entering the outcome. The pilot question (pre-registered): does width ALONE
re-open frontier headroom (attention / rabbit-hole / wide-joint delivery
pressure) on a world the frontier already saturated at 3 columns?

Distractor clusters (all correlated with REAL latents -> plausible stories,
never white noise; per ADR 0085-2):
  - driver-linked (co-adjusted settings): pressure, flow_rate, torque, rpm
  - u-linked (co-readings of unit quality): surface_gloss, density, weight, grain
  - shift-linked (hall co-readings): hall_temp, hall_rh, vibration, noise_db
  - w-linked ("maintenance state" latent, its own cluster): wear_index,
    feed_counter, supply_age, op_tenure

Mechanism (outcome IDENTICAL to #9):

    u, w    ~ N(0,1) latents (never columns)
    signal  = 1.2*u + N(0, 1.5)
    driver  = clip(N(5, 1.5), 0, 10) historically   (settable 0-10)
    outcome = 8 + 2.5*driver + 5*u + 1.2*shift + N(0, 2)
"""

import numpy as np
import pandas as pd

COLUMNS = [
    "driver", "signal", "outcome",
    "pressure", "flow_rate", "torque", "rpm",
    "surface_gloss", "density", "weight", "grain",
    "hall_temp", "hall_rh", "vibration", "noise_db",
    "wear_index", "feed_counter", "supply_age", "op_tenure",
]

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
    w = rng.normal(0.0, 1.0, n)                      # maintenance-state latent
    signal = p["signal_coef"] * u + rng.normal(0.0, p["signal_noise"], n)
    if "driver" in regime.config:
        driver = np.full(n, float(regime.config["driver"]))
    else:
        driver = np.clip(rng.normal(p["driver_base"], p["driver_sd"], n),
                         DRIVER_MIN, DRIVER_MAX)
    outcome = (p["base"] + p["driver_coef"] * driver + p["u_coef"] * u
               + p["shift_coef"] * shift + rng.normal(0.0, p["outcome_noise"], n))

    d = {"driver": driver, "signal": signal, "outcome": outcome}
    # driver-linked co-settings (the line adjusts them together; no causal role)
    d["pressure"] = 3.0 + 0.5 * driver + rng.normal(0.0, 0.8, n)
    d["flow_rate"] = 10.0 + 0.9 * driver + rng.normal(0.0, 1.2, n)
    d["torque"] = 5.0 + 0.4 * driver + 0.3 * w + rng.normal(0.0, 1.0, n)
    d["rpm"] = 50.0 + 3.0 * driver + rng.normal(0.0, 5.0, n)
    # u-linked co-readings (quality shows everywhere; only via u)
    d["surface_gloss"] = 2.0 + 1.2 * u + rng.normal(0.0, 1.0, n)
    d["density"] = 8.0 + 0.8 * u + rng.normal(0.0, 0.9, n)
    d["weight"] = 20.0 + 1.5 * u + rng.normal(0.0, 1.5, n)
    d["grain"] = 0.6 * u + 0.4 * w + rng.normal(0.0, 1.0, n)
    # shift-linked hall co-readings
    d["hall_temp"] = 22.0 + 1.5 * shift + rng.normal(0.0, 0.7, n)
    d["hall_rh"] = 45.0 + 4.0 * shift + rng.normal(0.0, 2.0, n)
    d["vibration"] = 1.0 + 0.3 * shift + 0.5 * w + rng.normal(0.0, 0.6, n)
    d["noise_db"] = 60.0 + 2.0 * shift + rng.normal(0.0, 1.5, n)
    # maintenance cluster (its own latent w; correlated junk with a story)
    d["wear_index"] = 5.0 + 1.8 * w + rng.normal(0.0, 0.8, n)
    d["feed_counter"] = 100.0 + 6.0 * w + rng.normal(0.0, 4.0, n)
    d["supply_age"] = 30.0 + 3.0 * w + rng.normal(0.0, 2.0, n)
    d["op_tenure"] = 4.0 + 1.0 * w + rng.normal(0.0, 1.2, n)
    return pd.DataFrame(d)[COLUMNS]


def sample(regime, n, seed):
    return mechanism(PARAMS, regime, n, seed)


model = sample
