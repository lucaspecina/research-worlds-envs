"""Longitudinal over-generalization world (ADR 0162), transfer pole.

The agent never sees this file.  Every legal pre-commissioning sample is
identical to the twin.  Lines diverge only above the initially available range.
"""

import numpy as np
import pandas as pd

POLE = "transfer"
NOISE = 0.7
LINES = (1, 2, 3, 4, 5)
LOW_MAX = 4.0
CAMPAIGN_GRID = (0.5, 2.5, 5.0, 7.5, 9.5)
REPORT_DS = (1.0, 3.0, 5.0, 6.2, 7.4, 8.6, 9.6, 7.9)


def law(d):
    d = np.asarray(d, dtype=float)
    return 14.0 + 8.0 * d * (10.0 - d) / 25.0


def _gate(d):
    d = np.asarray(d, dtype=float)
    x = np.clip((d - LOW_MAX) / (10.0 - LOW_MAX), 0.0, 1.0)
    return x * x * (3.0 - 2.0 * x)


def curve(line, d):
    line = int(line)
    d = np.asarray(d, dtype=float)
    base = law(d)
    return base


def _qualification(n, rng):
    # Interleaved 1/2 share: line 1 across the full range; each other line in
    # the commissioned low range. The cycle keeps partial reads representative.
    pattern = np.array((1, 2, 1, 3, 1, 4, 1, 5), dtype=int)
    lines = np.resize(pattern, n)
    driver = np.empty(n, dtype=float)
    low_count = {line: 0 for line in (2, 3, 4, 5)}
    for i, line in enumerate(lines):
        if line == 1:
            driver[i] = rng.uniform(0.0, 10.0)
        else:
            j = low_count[int(line)]
            driver[i] = (0.5, 1.5, 2.5, 3.5)[j % 4]
            low_count[int(line)] += 1
    outcome = np.array([curve(line, d) for line, d in zip(lines, driver)])
    outcome += rng.normal(0.0, NOISE, n)
    return pd.DataFrame({"line": lines.astype(float), "driver": driver, "outcome": outcome})


def _commissioning(n, rng):
    lines = np.resize(np.array((2, 3, 4, 5), dtype=int), n)
    counts = {line: 0 for line in (2, 3, 4, 5)}
    driver = np.empty(n, dtype=float)
    for i, line in enumerate(lines):
        j = counts[int(line)]
        driver[i] = REPORT_DS[j % len(REPORT_DS)]
        counts[int(line)] += 1
    outcome = np.array([curve(line, d) for line, d in zip(lines, driver)])
    outcome += rng.normal(0.0, NOISE, n)
    return pd.DataFrame({"line": lines.astype(float), "driver": driver, "outcome": outcome})


def sample(regime, n, seed):
    rng = np.random.default_rng(seed)
    cfg = regime.config
    if "__qualification" in cfg:
        return _qualification(n, rng)
    if "__commissioning" in cfg:
        return _commissioning(n, rng)
    if "campaign_line" in cfg:
        line = int(cfg["campaign_line"])
        d = np.resize(np.asarray(CAMPAIGN_GRID, dtype=float), n)
    elif "line" in cfg and "driver" in cfg:
        line = int(cfg["line"])
        d = np.full(n, float(cfg["driver"]))
    else:
        line = 1
        d = rng.uniform(0.0, 10.0, n)
    outcome = curve(line, d) + rng.normal(0.0, NOISE, n)
    return pd.DataFrame({"line": np.full(n, float(line)), "driver": d, "outcome": outcome})


def experiment_guard(design, turn, fired_events):
    if 0 in fired_events:
        return
    cfg = design.config
    line = int(cfg.get("campaign_line", cfg.get("line", 1)))
    if line == 1:
        return
    if "campaign_line" in cfg or float(cfg.get("driver", 0.0)) > LOW_MAX:
        raise ValueError(
            "the full range of lines 2-5 is not commissioned yet; before the scheduled "
            "extension only fixed settings at driver <= 4 are operational"
        )


model = sample

