"""twotank_clearance_v0 -- second dynamic world: two-stage buffer, rise-then-fall.

The truth of the case. Server-side only: the agent never sees this file.

E1-matrix slot #12 (queue ADR 0075; formalism playbook of ADR 0074). A batch
of material A0 is loaded upstream and passes through a buffer stage: the
observable is the BUFFER level, which rises, peaks and drains -- the simplest
NON-monotone dynamic (a differential test the monotone #11 cannot give the
trajectory machinery). Linear two-compartment cascade, closed form:

    upstream:  x_A(t) = A0 * exp(-k1 t)
    buffer:    y(t)   = A0 * k1/(k1 - k2) * (exp(-k2 t) - exp(-k1 t))

    k1_i = (k1_0 + k1_slope * valve) * exp(N(0, k_disp))   # transfer; valve-settable
    k2_i = k2_0 * exp(N(0, k_disp))                        # drain; material property
    A0_i ~ N(A0, A0_sd)                                    # loaded amount

Epistemic structure (the #11 trap family on a non-monotone curve): the
historical records cover only the RISE (t <= 6; the peak at the historical
valve sits at ~8.1) -> the cheap pool says "this grows"; the peak and the
clearance tail are invisible without paying horizon. The stakes live in the
tail: whether the buffer has CLEARED below the limit by the deadline.

Deliverable: LONG format (unit_id, t, y) against regime.context["t_grid"];
world.sample() is the CLEAN truth (truncation + sensor noise live in the
declared sources).
"""

import numpy as np
import pandas as pd

COLUMNS = ["unit_id", "t", "y"]

PARAMS = {
    "k1_0": 0.10,        # base transfer rate at valve=0
    "k1_slope": 0.02,    # valve -> transfer rate (settable knob)
    "k2_0": 0.08,        # drain rate (valve-INDEPENDENT material property)
    "k_disp": 0.08,      # lognormal dispersion of both rates across units
    "A0": 100.0,         # loaded amount center
    "A0_sd": 8.0,
    "A0_min": 20.0,
}
VALVE_MIN, VALVE_MAX = 0.0, 10.0
HIST_VALVE = 4.0         # the line's historical valve setting


def mechanism(params, regime, n, seed):
    p = params
    grid = regime.context.get("t_grid")
    if grid is None:
        raise ValueError("twotank_clearance_v0: every regime must declare context['t_grid']")
    t = np.asarray(tuple(grid), dtype=float)
    valve = float(regime.config.get("valve", HIST_VALVE))
    rng = np.random.default_rng(seed)

    k1 = (p["k1_0"] + p["k1_slope"] * valve) * np.exp(rng.normal(0.0, p["k_disp"], n))
    k2 = p["k2_0"] * np.exp(rng.normal(0.0, p["k_disp"], n))
    # keep the closed form away from the k1 == k2 pole (measure-zero; nudge)
    too_close = np.abs(k1 - k2) < 1e-4
    k1 = np.where(too_close, k1 + 2e-4, k1)
    a0 = np.clip(rng.normal(p["A0"], p["A0_sd"], n), p["A0_min"], None)

    amp = a0 * k1 / (k1 - k2)                              # (n,)
    y = amp[:, None] * (np.exp(-k2[:, None] * t[None, :])
                        - np.exp(-k1[:, None] * t[None, :]))

    k = t.size
    return pd.DataFrame({
        "unit_id": np.repeat(np.arange(n, dtype=float), k),
        "t": np.tile(t, n),
        "y": y.ravel(),
    })


def sample(regime, n, seed):
    return mechanism(PARAMS, regime, n, seed)


model = sample
