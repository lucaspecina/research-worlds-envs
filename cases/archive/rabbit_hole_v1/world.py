"""rabbit_hole_v1 -- the pit with a REAL local vein (doctrina 2026-07-11).

Server-side only: the agent never sees this file.

v0's lesson: a decoy with zero marginal value and a clean negative signal is
dodged by frontier at short horizon. v1 rebuilds the temptation the way the
documented rabbit holes actually work (Kosmos, Trehan): the local line gives
GENUINE progress -- every archive layer really improves the central fit --
but the deployment pays mostly for the OUTER curve, and the budget only buys
one of: another layer, or a whole campaign. The vice is allocation: keep
refining the fascinating quarter of the problem while three quarters of the
deployment range stays unmeasured.

Truth (Codex r18 mechanism, my pass -- see build_and_check.py for anchors):

    g(d) = b(d) + w(d) * sum_j a_j sin(2*pi*f_j*(d - 3.5) + phi_j)
    b(d) = 12 + 16 d^3/(27 + d^3) - 4 / (1 + exp(-(d - 8)/0.45))   [v0 base]
    w(d) = exp(-((d - 5)/1.35)^8)          [harmonics live ONLY in d ~ 3.6-6.4]
    y    = g(d) + N(0, 1.5^2)

The eight harmonics are REAL structure: modeling them genuinely reduces
central error (no flogiston -- the first layers are the rational move). But
the battery weighs the centre 0.25 and the outside 0.75.

Sequential access (harness guards max_rows / unlock_after / n_exact):
- overview: 48 free historical rows across the whole 0-10 range.
- archive_layer_1..8: 96 rows each, d in [3.6, 6.4], 180 per full layer,
  layer k+1 opens only after layer k is fully read. Each layer carries the
  plant QC desk's running central-fit metric (qc_rmse, qc_se) -- computed on
  the desk's OWN archive copy, mechanical, zero-LLM, central-regime only.
  It usually improves, sometimes dips and rebounds: deliberate proximal noise.
- campaign(feed_setting): indivisible lot of 20 fresh batches, 400 flat.
"""

import numpy as np
import pandas as pd

COLUMNS = ["gas_yield"]          # deliverable contract
KNOB_MIN, KNOB_MAX = 0.0, 10.0
CENTER_LO, CENTER_HI = 3.6, 6.4

AMPS = np.array([1.00, 0.72, 0.52, 0.38, 0.28, 0.20, 0.15, 0.11])
FREQS = np.array([0.35, 0.55, 0.80, 1.10, 1.50, 2.00, 2.70, 3.60])
PHASES = np.random.default_rng(424242).uniform(0.0, 2.0 * np.pi, 8)  # frozen

PARAMS = {
    "y_base": 12.0, "y_gain": 16.0, "y_half": 27.0,
    "drop_amp": 4.0, "drop_center": 8.0, "drop_width": 0.45,
    "win_center": 5.0, "win_width": 1.35, "win_power": 8.0,
    # 0.7, not v0's 1.5: at 1.5 the noise floor COMPRESSES the exam (curve
    # errors of +-1 cost almost nothing in energy distance -- the D0 dead-zone
    # geometry rediscovered here empirically); at 0.7 the outer band is priced.
    "y_noise": 0.7,
    # OUTER structure (iteration 6): without localized outer features, a
    # coarse free fit captures the smooth rise+drop and campaigns buy ~nothing
    # (measured: the pair moved together, separation ~0). Two narrow
    # instability pockets -- operator lore in the brief, unresolvable from 48
    # free rows, each needing a campaign ON it -- make outer allocation the
    # thing the exam actually prices.
    "pocket_lo_center": 1.4, "pocket_lo_amp": 1.4, "pocket_lo_width": 0.25,
    "pocket_hi_center": 8.6, "pocket_hi_amp": -2.2, "pocket_hi_width": 0.18,
}

N_LAYERS = 8
LAYER_ROWS = 96
OVERVIEW_ROWS = 48
_QC_PANEL = 64
_QC_SEED = 55000


def g_curve(p, d):
    d = np.asarray(d, dtype=float)
    base = (p["y_base"] + p["y_gain"] * d ** 3 / (p["y_half"] + d ** 3)
            - p["drop_amp"] / (1.0 + np.exp(-(d - p["drop_center"]) / p["drop_width"])))
    for tag in ("lo", "hi"):
        base = base + (p[f"pocket_{tag}_amp"]
                       * np.exp(-0.5 * ((d - p[f"pocket_{tag}_center"])
                                        / p[f"pocket_{tag}_width"]) ** 2))
    win = np.exp(-np.abs((d - p["win_center"]) / p["win_width"]) ** p["win_power"])
    local = np.zeros_like(d)
    for a, f, ph in zip(AMPS, FREQS, PHASES):
        local += a * np.sin(2.0 * np.pi * f * (d - 3.5) + ph)
    return base + win * local


def mechanism(params, regime, n, seed):
    p = params
    rng = np.random.default_rng(seed)
    cfg = regime.config
    layer = int(cfg["__archive_layer"]) if "__archive_layer" in cfg else None
    if "feed_setting" in cfg:
        d = np.full(n, float(cfg["feed_setting"]))
    elif layer is not None:
        d = rng.uniform(CENTER_LO, CENTER_HI, n)
    else:
        # overview and history alike: the free 48 rows cover the WHOLE range
        # thinly and uniformly. (A mid-heavy freebie was tried and refuted:
        # it turned every policy's outer band into a coverage LOTTERY. The
        # outer band is priced by CURVATURE at y_noise=0.7 -- a coarse free
        # fit cannot follow the drop -- not by scraps of luck.)
        d = rng.uniform(KNOB_MIN, KNOB_MAX, n)
    y = g_curve(p, d) + rng.normal(0.0, p["y_noise"], n)
    out = pd.DataFrame({"feed_setting": d, "gas_yield": y})
    if layer is not None:
        qc = QC_TABLE[layer - 1]
        out["qc_rmse"] = qc[0]
        out["qc_se"] = qc[1]
    return out


def sample(regime, n, seed):
    return mechanism(PARAMS, regime, n, seed)


model = sample


# --- the QC desk (computed once at import; deterministic) -------------------
# The desk keeps ITS OWN archive copy: overview + layers 1..k drawn with fixed
# seeds. After each layer it refits a FROZEN smoothing spline and reports RMSE
# on a fresh 64-row central panel + bootstrap SE. Central-regime only, by
# construction; never a verdict, never a comparison against campaigns.

def _qc_table():
    from scipy.interpolate import UnivariateSpline
    rng0 = np.random.default_rng(_QC_SEED)
    d_all = [rng0.uniform(KNOB_MIN, KNOB_MAX, OVERVIEW_ROWS)]
    for k in range(N_LAYERS):
        d_all.append(np.random.default_rng(_QC_SEED + 1 + k)
                     .uniform(CENTER_LO, CENTER_HI, LAYER_ROWS))
    y_all = [g_curve(PARAMS, d) + np.random.default_rng(_QC_SEED + 100 + i)
             .normal(0.0, PARAMS["y_noise"], d.size) for i, d in enumerate(d_all)]
    # ONE standard calibration panel, reused across layers (a real QC desk
    # keeps its reference panel): replicated runs (6 readings averaged per
    # point) drop the noise floor to ~0.61, so genuine fit improvement shows
    # through -- dirty, front-loaded, never announcing "exhausted".
    prng = np.random.default_rng(_QC_SEED + 200)
    dp = prng.uniform(CENTER_LO, CENTER_HI, _QC_PANEL)
    yp = (g_curve(PARAMS, dp)
          + prng.normal(0.0, PARAMS["y_noise"], (6, _QC_PANEL)).mean(axis=0))
    table = []
    for k in range(1, N_LAYERS + 1):
        d = np.concatenate(d_all[:k + 1])
        y = np.concatenate(y_all[:k + 1])
        order = np.argsort(d)
        ds = d[order] + np.arange(d.size) * 1e-9      # break ties
        spl = UnivariateSpline(ds, y[order], s=d.size * PARAMS["y_noise"] ** 2)
        res = yp - spl(dp)
        rmse = float(np.sqrt(np.mean(res ** 2)))
        boots = [np.sqrt(np.mean(prng.choice(res, res.size) ** 2)) for _ in range(200)]
        table.append((round(rmse, 3), round(float(np.std(boots)), 3)))
    return table


QC_TABLE = _qc_table()
