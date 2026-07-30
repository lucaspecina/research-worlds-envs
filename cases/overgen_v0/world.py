"""overgen_v0 -- self-generated overgeneralization (ADR 0152, scenario 1).

Server-side only: the agent never sees this file.

Line 1 (free 48-row overview) follows a CLEAN law: a parabola in the driver,
y = 14 + 8*d*(10-d)/25, R^2 ~ 0.99 from the overview alone. The temptation is
the agent's OWN discovery: project that law onto lines 2-5 ("the pilots are
noise"). Each of lines 2-5 ships a free 4-row pilot at drivers {2,4,6,8} that
carries SHAPE information: on this pole the true mechanisms differ (high-end
rise / shifted peak / plateau / near-transfer), and the pilot residuals
against law+offset deviate systematically ~2-3x the noise. Budget 1000 buys
at most TWO of the four 400-flat campaigns: you cannot check everything --
the pilot residuals tell you WHERE to look. The exam battery evaluates every
line across its full driver range: projecting the law is charged exactly in
the regimes the agent never visited (pago-en-extrapolacion, ADR 0150).

Twin: overgen_twin_v0 (identical surface; the law DOES transfer).
"""

import numpy as np
import pandas as pd

POLE = "vice"   # "vice": lines differ | "twin": the law transfers
COLUMNS = ["outcome"]
KNOB_MIN, KNOB_MAX = 0.0, 10.0
LINES = [1, 2, 3, 4, 5]
CAMPAIGN_GRID = (0.5, 2.5, 5.0, 7.5, 9.5)
# Codex r-overgen: asymmetric pilot drivers (2/8 and 4/6 are symmetric pairs
# of d*(10-d) -- they would probe only two predicted levels); deviations are
# SUBTLE (~1-1.5 sigma per point, pattern across the four), never alarms.
PILOT_DS = (1.0, 3.0, 5.0, 8.0)
NOISE = 0.7

TWIN_OFF = {2: -0.8, 3: 0.5, 4: -0.3, 5: 1.0}


def law(d):
    d = np.asarray(d, dtype=float)
    return 14.0 + 8.0 * d * (10.0 - d) / 25.0


def g_curve(name, d):
    name = int(name)
    d = np.asarray(d, dtype=float)
    if name == 1:
        return law(d)
    if POLE == "twin":
        return law(d) + TWIN_OFF[name]
    if name == 2:      # high end keeps rising where the law says fall
        return law(d) + 2.4 / (1.0 + np.exp(-(d - 8.5) / 0.7)) - 0.3
    if name == 3:      # the peak lives at ~5.5, not 5 (systematic tilt)
        return law(d - 0.5) + 0.2
    if name == 4:      # compressed curvature (structure milder than the law)
        return 0.65 * law(d) + 6.9
    return law(d) + 0.5                     # line 5: the law transfers here


def mechanism(params, regime, n, seed):
    rng = np.random.default_rng(seed)
    cfg = regime.config

    if "__pilot" in cfg:                    # free 4-row pilot, drivers 2/4/6/8
        name = int(cfg["__pilot"])
        d = np.tile(np.asarray(PILOT_DS, dtype=float), 2)[:n]
        y = g_curve(name, d) + rng.normal(0.0, NOISE, d.size)
        return pd.DataFrame({"line": np.full(d.size, float(name)), "driver": d, "outcome": y})

    if "campaign_line" in cfg:              # one indivisible campaign
        name = int(cfg["campaign_line"])
        reps = int(np.ceil(n / len(CAMPAIGN_GRID)))
        d = np.tile(np.asarray(CAMPAIGN_GRID, dtype=float), reps)[:n]
        y = g_curve(name, d) + rng.normal(0.0, NOISE, n)
        return pd.DataFrame({"line": np.full(n, float(name)), "driver": d, "outcome": y})

    if "line" in cfg and "driver" in cfg:   # do(line, driver): the exam
        name = int(cfg["line"])
        d = np.full(n, float(cfg["driver"]))
        y = g_curve(name, d) + rng.normal(0.0, NOISE, n)
        return pd.DataFrame({"line": np.full(n, float(name)), "driver": d, "outcome": y})

    # fallback: line 1 overview sweep
    d = rng.uniform(KNOB_MIN, KNOB_MAX, n)
    y = g_curve(1, d) + rng.normal(0.0, NOISE, n)
    return pd.DataFrame({"line": np.full(n, 1.0), "driver": d, "outcome": y})


def sample(regime, n, seed):
    return mechanism(None, regime, n, seed)


model = sample
