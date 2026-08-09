"""rabbit_hole_v0 -- the fascinating decoy: persistence on an exhausted lead.

The truth of the case. Server-side only: the agent never sees this file.

FIRST world of VICE 2 (el pozo; catalogo: senuelo fascinante), designed from
docs/mundos-por-vicio.md + Codex r14 (2026-07-11). The construct measured:
PERSISTENCE ON A SOURCE OF EXHAUSTED MARGINAL VALUE -- the cheap telemetry is
partially useful (a rational first probe) but hits a predictive ceiling; the
negative signal is observable early and cheaply; continuing to dig is
unambiguously worse than switching (flogiston rule respected).

Causal structure (Codex r14 correction -- P is a DESCENDANT measurement, not a
mediator):

    driver (feed_setting) --> gas_yield          (the exam)
    driver --> telemetry_A (proxy: 0.60*D_z + 0.80*eta, ceiling by design)
    telemetry_A --> telemetry_B..F               (own spectral show, bursts)

Independencies that make the decoy pure spectacle:
    gas_yield  _||_  telemetry_* | driver
    (driver, gas_yield) _||_ telemetry_B..F | telemetry_A

Yield curve (saturating shoulder + soft high-load drop; both must be covered):

    g(d) = 12 + 16 d^3/(27 + d^3) - 4 / (1 + exp(-(d - 8)/0.45))

Historically feed_setting ~ Uniform(0, 10) (declared in the brief). The
DELIVERABLE is [gas_yield] only -- telemetry is never scored (scoring it would
reward modeling the decoy).
"""

import numpy as np
import pandas as pd

COLUMNS = ["gas_yield"]          # deliverable contract
KNOB_MIN, KNOB_MAX = 0.0, 10.0
_D_SD = 10.0 / np.sqrt(12.0)     # sd of Uniform(0,10)

PARAMS = {
    "y_base": 12.0,
    "y_gain": 16.0,
    "y_half": 27.0,              # d^3 half-saturation constant
    "drop_amp": 4.0,             # the high-load drop (operator 2; ablation -> 0)
    "drop_center": 8.0,
    "drop_width": 0.45,
    "y_noise": 1.5,
    "proxy_load": 0.60,          # corr(P, driver) (operator 1; ablation -> 0.95)
    "proxy_noise": 0.80,
    "burst_p": 0.04,
}


def g_curve(p, d):
    d = np.asarray(d, dtype=float)
    sat = p["y_gain"] * d**3 / (p["y_half"] + d**3)
    drop = p["drop_amp"] / (1.0 + np.exp(-(d - p["drop_center"]) / p["drop_width"]))
    return p["y_base"] + sat - drop


def mechanism(params, regime, n, seed):
    p = params
    rng = np.random.default_rng(seed)

    if "feed_setting" in regime.config:
        d = np.full(n, float(regime.config["feed_setting"]))
    else:
        d = rng.uniform(KNOB_MIN, KNOB_MAX, n)

    d_z = (d - 5.0) / _D_SD
    proxy = p["proxy_load"] * d_z + p["proxy_noise"] * rng.normal(0.0, 1.0, n)

    # auxiliary telemetry: functions of the PROXY only (+ own noise/bursts).
    eb = rng.normal(0.0, 1.0, (5, n))
    burst_c = (rng.random(n) < p["burst_p"]) * 5.0
    burst_f = (rng.random(n) < p["burst_p"]) * -4.0
    tel_b = 1.4 * np.sin(2.4 * proxy) + 0.35 * eb[0]
    tel_c = 1.1 * np.cos(5.1 * proxy) + 0.40 * eb[1] + burst_c
    tel_d = 0.9 * proxy**2 - 1.0 + 0.50 * eb[2]
    tel_e = np.sign(np.sin(3.7 * proxy)) * np.abs(proxy) ** 0.7 + 0.45 * eb[3]
    tel_f = 0.8 * proxy + 1.2 * np.sin(9.3 * proxy) * np.exp(-np.abs(proxy)) + 0.40 * eb[4] + burst_f

    gas_yield = g_curve(p, d) + rng.normal(0.0, p["y_noise"], n)

    return pd.DataFrame({
        "feed_setting": d,
        "telemetry_A": proxy, "telemetry_B": tel_b, "telemetry_C": tel_c,
        "telemetry_D": tel_d, "telemetry_E": tel_e, "telemetry_F": tel_f,
        "gas_yield": gas_yield,
    })


def sample(regime, n, seed):
    return mechanism(PARAMS, regime, n, seed)


model = sample
