"""selection_bias_v0 - collider selection + measurement error (sampling/channel).

The truth of the case. Server-side only: the agent never sees this file.

FIRST world whose traps live in the SOURCES, not the mechanism (ARCHITECTURE
§1/§2.2, implemented v0.52; plan v0.49-2 + closures v0.50-v0.53). The mechanism
below is CLEAN: `signal` correlates with `outcome` ONLY through `driver` (no
direct edge). The spurious signal<->outcome association the agent sees in the
cheap records is manufactured entirely by the source's declared selection
filter (f(signal, outcome) > threshold: value-based selection, filter on TRUE values --
v0.53-1); the measured `outcome` carries declared zero-mean instrument noise
(sigma_med; v0.50-1 bias=0), identifiable via the replicated source (v0.51).

Domain skin: a batch conditioning line. An operator sets a CONDITIONING
INTENSITY (`driver`, 0-10); an inline GAUGE reads during conditioning
(`signal`); each unit gets a final QUALITY score (`outcome`, higher = better;
below 2 = rejected). `ambient` is a logged hall reading (decoy: plausible and
irrelevant, ARCHITECTURE §4).

Mechanism (all clean):

    driver  ~ U(0, 10) observational (replaced by regime.config["driver"] under do())
    signal  := signal_coef * driver + N(0, signal_noise)     # gauge tracks intensity
    outcome := outcome_coef * driver + shift_coef * shift + N(0, outcome_noise)
    ambient ~ N(0, ambient_noise)                             # decoy

Operators (declared in meta.json; both live in the SOURCES):
  - collider_seleccion (sampling): the historical record keeps rows with
    signal + outcome above a threshold -> spurious negative partial
    correlation signal<->outcome given driver, inside the record only.
    Ablation = filter off (threshold -> -inf).
  - error_de_medicion (channel): recorded outcome = true + N(0, noise_sd);
    experiments NEVER bypass it (v0.9). Ablation = noise_sd 0.

sample() = mechanism(PARAMS, ...): the S_truth anchor and the scorer's truth.
"""

import numpy as np
import pandas as pd

COLUMNS = ["driver", "signal", "outcome", "ambient"]

PARAMS = {
    "signal_coef": 0.8,     # gauge gain on intensity (signal's ONLY link to outcome)
    "signal_noise": 1.0,
    "outcome_coef": 1.2,    # true effect of conditioning intensity on quality
    "outcome_noise": 1.0,   # PROCESS dispersion (the meter's sigma_med lives in the source)
    "shift_coef": 0.5,      # hall/period baseline effect on quality (context)
    "ambient_noise": 1.0,   # decoy column scale
}
DRIVER_MIN, DRIVER_MAX = 0.0, 10.0


def mechanism(params, regime, n, seed):
    p = params
    rng = np.random.default_rng(seed)
    shift = float(regime.context.get("shift", 0.0))

    if "driver" in regime.config:
        driver = np.full(n, float(regime.config["driver"]))
    else:
        driver = rng.uniform(DRIVER_MIN, DRIVER_MAX, n)

    signal = p["signal_coef"] * driver + rng.normal(0.0, p["signal_noise"], n)
    outcome = (
        p["outcome_coef"] * driver
        + p["shift_coef"] * shift
        + rng.normal(0.0, p["outcome_noise"], n)
    )
    ambient = rng.normal(0.0, p["ambient_noise"], n)
    return pd.DataFrame(
        {"driver": driver, "signal": signal, "outcome": outcome, "ambient": ambient}
    )


def sample(regime, n, seed):
    return mechanism(PARAMS, regime, n, seed)


model = sample
