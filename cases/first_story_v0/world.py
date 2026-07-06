"""first_story_v0 -- the treacherous prior: the plant blames the supplier.

The truth of the case. Server-side only: the agent never sees this file.

E1-matrix slot #17 = MUNDO A of the anti-vice line (ADRs 0080/0081; spec
docs/mundo-a-primera-historia.md). Vice under pressure: MARRYING THE FIRST
HYPOTHESIS. The cheap record shows a strong, quotable feedstock<->outcome
correlation (~0.6) and the plant folklore blames the supplier -- Historia X,
seductive and FALSE. The truth (Historia Y): hall humidity DRIFTED over the
era the records cover, pushing BOTH the feedstock reading and the outcome;
the material is innocent. Humidity was never logged (D2) -- only timestamps.

Escapes (both must exist; certificate proves them):
  - cheap: stratify the record by TIME -- within a narrow window the
    feedstock effect evaporates (the #9 within-batch pattern);
  - dear:  experiment over the declared menu of environment knobs (humidity
    + decoys temp/line_speed -- a one-item menu would telegraph, D2): only
    humidity moves the outcome (~5% of budget).

The exam (D1): counterfactual do(feedstock_grade) -- the client's literal
question ("do we switch supplier?") -- where the seduced predicts an
improvement that never comes; PLUS humidity-varying regimes (anti-cynic
guard: disbelieving X is not enough, you must model Y).

Mechanism per unit (latent u -- never a column; t = era position, exposed to
the record view only; the deliverable is [feedstock, outcome]):

    t        ~ U(0,1) historically (record spans the era);  0 under set regimes
    ambient  = 2 + 6*t + N(0, 0.5)   historically;  = humidity when set
    feedstock = 6 + 1.0*(grade-5) - 0.9*(ambient-5) + N(0, 0.9)
    outcome   = 30 - 2.5*(ambient-5) + 3*u + N(0, 2)      # grade NEVER enters
    grade     = N(5, 1) clipped historically; settable 0-10 (the supplier knob)

Decoy knobs temp / line_speed: settable, do NOTHING (declared decoys).
"""

import numpy as np
import pandas as pd

COLUMNS = ["feedstock", "outcome"]

PARAMS = {
    "u_sd": 1.0,
    "amb_base": 2.0,
    "amb_drift": 6.0,
    "amb_noise": 0.5,
    "amb_center": 5.0,
    "f_base": 6.0,
    "grade_coef": 1.0,
    "f_amb_coef": 0.9,
    "f_noise": 0.9,
    "y_base": 30.0,
    "y_amb_coef": 2.5,
    "u_coef": 3.0,
    "y_noise": 2.0,
    "grade_base": 5.0,
    "grade_sd": 1.0,
}
KNOB_MIN, KNOB_MAX = 0.0, 10.0


def mechanism(params, regime, n, seed):
    p = params
    rng = np.random.default_rng(seed)
    u = rng.normal(0.0, p["u_sd"], n)

    if "humidity" in regime.config:
        t = np.zeros(n)
        ambient = np.full(n, float(regime.config["humidity"]))
        ambient = ambient + rng.normal(0.0, p["amb_noise"], n)
    else:
        t = rng.uniform(0.0, 1.0, n)
        ambient = p["amb_base"] + p["amb_drift"] * t + rng.normal(0.0, p["amb_noise"], n)

    if "feedstock_grade" in regime.config:
        grade = np.full(n, float(regime.config["feedstock_grade"]))
    else:
        grade = np.clip(rng.normal(p["grade_base"], p["grade_sd"], n), KNOB_MIN, KNOB_MAX)

    # temp / line_speed are DECLARED DECOYS: settable, never read.
    feedstock = (p["f_base"] + p["grade_coef"] * (grade - p["grade_base"])
                 - p["f_amb_coef"] * (ambient - p["amb_center"])
                 + rng.normal(0.0, p["f_noise"], n))
    outcome = (p["y_base"] - p["y_amb_coef"] * (ambient - p["amb_center"])
               + p["u_coef"] * u + rng.normal(0.0, p["y_noise"], n))
    return pd.DataFrame({"t": t, "feedstock": feedstock, "outcome": outcome})


def sample(regime, n, seed):
    return mechanism(PARAMS, regime, n, seed)


model = sample
