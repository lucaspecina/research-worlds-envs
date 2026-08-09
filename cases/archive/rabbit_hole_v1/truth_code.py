"""truth_code -- R=1 anchor of rabbit_hole_v1 (deliverable column only).
Same mechanism and RNG call order as world.py. GENERATED - do not hand-edit."""
import numpy as np
import pandas as pd

AMPS = np.array([1.00, 0.72, 0.52, 0.38, 0.28, 0.20, 0.15, 0.11])
FREQS = np.array([0.35, 0.55, 0.80, 1.10, 1.50, 2.00, 2.70, 3.60])
PHASES = np.array([np.float64(2.981979982482674), np.float64(0.6602849868220143), np.float64(1.8108977599308578), np.float64(1.5114135892855078), np.float64(4.474063129570011), np.float64(3.356354845673419), np.float64(0.8001962294045084), np.float64(5.780280880697888)])


def _g(d):
    base = 12.0 + 16.0 * d ** 3 / (27.0 + d ** 3) - 4.0 / (1.0 + np.exp(-(d - 8.0) / 0.45))
    base = base + 1.4 * np.exp(-0.5 * ((d - 1.4) / 0.25) ** 2)
    base = base - 2.2 * np.exp(-0.5 * ((d - 8.6) / 0.18) ** 2)
    win = np.exp(-np.abs((d - 5.0) / 1.35) ** 8.0)
    local = np.zeros_like(d)
    for a, f, ph in zip(AMPS, FREQS, PHASES):
        local += a * np.sin(2.0 * np.pi * f * (d - 3.5) + ph)
    return base + win * local


def model(regime, n, seed):
    rng = np.random.default_rng(seed)
    if "feed_setting" in regime.config:
        d = np.full(n, float(regime.config["feed_setting"]))
    else:
        d = rng.uniform(0.0, 10.0, n)
    return pd.DataFrame({"gas_yield": _g(d) + rng.normal(0.0, 0.7, n)})
