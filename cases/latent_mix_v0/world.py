"""latent_mix_v0 - latent-class heterogeneity with opposite input effects.

The truth of the case. Server-side only: the agent never sees this file.

Suite Latent (latent constructs). CONTRAST with dummy_dose_v0: the dummy is a
CONFOUNDING trap (a no-latent model with interventional data recovers R~=0.94 --
the latent factor only biases assignment). This case is a LATENT-HETEROGENEITY
trap: two material grades whose input effect has OPPOSITE SIGN, so the correct
setting depends on the grade composition of the lot, and a model restricted to
unimodal generation over observables cannot reproduce the two-cluster joint.

Domain skin: an industrial process line. An operator sets an INPUT LEVEL (`dose`,
0-10); a sensor gives a READING (`marker`); each unit gets an output QUALITY score
(`outcome`). Two hidden material GRADES (a latent class Z) respond to the input
with OPPOSITE SIGN; the lot COMPOSITION (`mix_logit`) sets how many of each.

Mechanism (all mechanism layer):

    Z        ~ Bernoulli(sigmoid(mix_logit))      # latent grade, never observed
    marker   := marker_sep * Z + Normal(0, marker_noise)   # bimodal: REVEALS Z
    dose     := clip(dose_base + class_coef_dose*Z + Normal(0,dose_noise), 0, 10)
                (replaced by the constant regime.config["dose"] under do())
    effect   := slope_a if Z==0 else slope_b       # OPPOSITE SIGNS
    base     := base_a   if Z==0 else base_b
    outcome  := base + effect * dose + Normal(0, outcome_noise)

Two operators (declared in meta.json with their ablation = "off" value):
  - heterogeneidad_latente: the sign flip (slope_b<0). Ablated -> both grades
    share the type-A slope (homogeneous world; the innocent twin that "never
    saw the heterogeneity").
  - confounding_por_clase: Z drives the observed input assignment (the type-B
    grade, reading differently, historically got MORE input). Ablated ->
    assignment independent of Z.

The investigative insight rewarded: discover that the reading is BIMODAL, that it
indexes two grades with opposite input-response, and condition the setting on it.
An operator who averages over grades (no-latent) misprices the input badly.

sample() = mechanism(PARAMS, ...): the S_truth anchor (R(world.py) == 1 by
construction -- it runs through the same pipeline as any submission).
"""

import numpy as np
import pandas as pd

COLUMNS = ["dose", "marker", "outcome"]

# Structured mechanism (Decision Log v0.18 pattern): truth = mechanism(PARAMS,...);
# the factory derives ladder rungs / innocent twins by perturbing or ablating
# these params (operator -> param mapping in meta.json), without reading this file.
# Constants chosen so the heterogeneity is IRREDUCIBLE to a unimodal model (the
# theory-gap probe's symmetric reading, Decision Log v0.25, showed an earlier
# draft -- base_b=3 + slopes +-1 -- made the two grades CROSS near dose 2,
# collapsing the separation; the residual gap was then dominated by HETEROSCEDAS-
# TICITY, which a stronger no-latent rival could fix = a weak-rival artifact, the
# v0.18 trap). Fix: base_b=base_a=0 + strong opposite slopes + tight noise, so at
# any dose>0 the two outcome clusters are cleanly SEPARATED (two modes a unimodal
# model cannot make, however well it fits mean+variance), and the reading is
# cleanly bimodal at all doses. The decisive control is a moment-matched Gaussian
# oracle (theory_gap_probe.py): if it fails, the gap is the modes.
PARAMS = {
    "marker_sep": 5.0,        # heterogeneidad_latente: grade separation in the reading
    "marker_noise": 1.0,      # within-grade reading spread (5-sigma clusters: clean, discoverable)
    "slope_a": 1.5,           # heterogeneidad_latente: type-A input slope (+)
    "slope_b": -1.5,          # heterogeneidad_latente: type-B input slope (-); ablation -> +1.5
    "base_a": 0.0,
    "base_b": 0.0,            # no baseline offset -> no mid-input cross-over; separation grows with dose
    "outcome_noise": 0.5,
    "dose_base": 4.0,         # confounding_por_clase: natural assignment center
    "dose_noise": 1.2,
    "class_coef_dose": 2.5,   # confounding_por_clase: Z -> dose; ablation -> 0.0
}
DOSE_MIN, DOSE_MAX = 0.0, 10.0


def _sigmoid(x):
    return 1.0 / (1.0 + np.exp(-x))


def mechanism(params, regime, n, seed):
    p = params
    rng = np.random.default_rng(seed)
    mix_logit = float(regime.context.get("mix_logit", 0.0))
    z = rng.binomial(1, _sigmoid(mix_logit), n).astype(float)  # latent grade

    marker = p["marker_sep"] * z + rng.normal(0.0, p["marker_noise"], n)

    if "dose" in regime.config:
        dose = np.full(n, float(regime.config["dose"]))
    else:
        raw = p["dose_base"] + p["class_coef_dose"] * z + rng.normal(0.0, p["dose_noise"], n)
        dose = np.clip(raw, DOSE_MIN, DOSE_MAX)

    effect = np.where(z > 0.5, p["slope_b"], p["slope_a"])
    base = np.where(z > 0.5, p["base_b"], p["base_a"])
    outcome = base + effect * dose + rng.normal(0.0, p["outcome_noise"], n)

    return pd.DataFrame({"dose": dose, "marker": marker, "outcome": outcome})


def sample(regime, n, seed):
    return mechanism(PARAMS, regime, n, seed)


model = sample
