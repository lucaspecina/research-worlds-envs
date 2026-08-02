"""Shared ODE physics for the second-wave structural-opening probe (v0).

Three arms share one plant. Line A is a single logistic everywhere and is
byte-identical across arms (its unit draws come from a stream keyed only by
the seed). Line B differs ONLY in its law:

    retain: B follows A's law (fresh units, same distribution);
    param:  B is ONE logistic with new parameters (higher plateau, new rate);
    struct: B keeps A's first logistic and adds a SECOND, delayed wave.

Line-B unit heterogeneity is drawn once from a shared stream and reused by
every arm, so for the same (n, seed) the reports differ across arms only
through the law: struct - retain equals the second wave exactly (no noise
term), and param's per-unit plateau equals struct's K1+K2 realization.

PARAM and STRUCT are dose-calibrated: the mean absolute displacement of the
B mean curve from the A law over the commissioning grid is comparable (the
difference between the arms is temporal topology, not update size). The
frozen constants below were selected by `calibrate_doses()`; the certifier
re-derives the doses and fails if the gap drifts.

Zero-LLM zone: numpy/pandas/scipy only, deterministic everywhere.
"""

from __future__ import annotations

import numpy as np
import pandas as pd
from scipy.optimize import least_squares

ARMS = ("retain", "param", "struct")
LINES = ("A", "B")
LONG_COLUMNS = ["unit_id", "t", "y"]

_A_STREAM = 0x0DEA01
_B_STREAM = 0x0DEB02

# --- line A (identical in every arm) ---------------------------------------
K0 = 100.0
K_SD = 8.0
K_MIN = 20.0
X0 = 2.0
X0_SD = 0.4
X0_MIN = 0.5
R_A = 0.55
R_DISP = 0.10

# --- line B laws ------------------------------------------------------------
# struct: first wave = A's law (same z-draws as retain); second delayed wave.
K2_0 = 70.0
K2_SD = 4.0
K2_MIN = 5.0
R2 = 1.80
R2_DISP = 0.10
T2_MID = 14.0          # midpoint of the delayed wave (calibrated)
# param: one logistic, same total plateau as struct (per unit: 140 + 8z0 + 4z3),
# rate chosen so its dose from the A law matches struct's dose (calibrated).
KP_0 = K0 + K2_0
R_P = 0.368            # frozen by calibrate_doses(); certifier re-checks

# --- commissioning report (identical form in every arm) ---------------------
REPORT_GRID = (0.0, 2.0, 4.0, 6.0, 8.0, 10.0, 12.0, 14.0, 16.0, 18.0, 20.0, 22.0, 24.0)
REPORT_UNITS = 24
NOISE_SD = 3.0         # the plant's one meter (same channel as line A sources)
HISTORY_GRID = (0.0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0)

DOSE_GRID = REPORT_GRID          # dose is measured where the report looks
_MC_N = 20_000
_MC_SEED = 424243


def _logistic(K, x0, r, t):
    """K/(1 + a e^{-rt}) with a=(K-x0)/x0; K,x0,r shape (n,1), t shape (1,k)."""
    a = (K - x0) / x0
    return K / (1.0 + a * np.exp(-r * t))


def _second_wave(K2, r2, t):
    return K2 / (1.0 + np.exp(-r2 * (t - T2_MID)))


def _draws_a(n: int, seed: int) -> tuple[np.ndarray, ...]:
    rng = np.random.default_rng(np.random.SeedSequence([int(seed), _A_STREAM]))
    z = rng.standard_normal((n, 3))
    K = np.clip(K0 + K_SD * z[:, 0:1], K_MIN, None)
    x0 = np.clip(X0 + X0_SD * z[:, 2:3], X0_MIN, None)
    r = R_A * np.exp(R_DISP * z[:, 1:2])
    return K, x0, r


def _draws_b(n: int, seed: int) -> np.ndarray:
    """Shared line-B unit randomness: one (n, 5) block for every arm."""
    rng = np.random.default_rng(np.random.SeedSequence([int(seed), _B_STREAM]))
    return rng.standard_normal((n, 5))


def _b_components(arm: str, z: np.ndarray):
    """Per-unit curve parameters of line B under each arm's law."""
    z0, z1, z2, z3, z4 = (z[:, i : i + 1] for i in range(5))
    x0 = np.clip(X0 + X0_SD * z2, X0_MIN, None)
    if arm == "retain":
        return {"K": np.clip(K0 + K_SD * z0, K_MIN, None),
                "x0": x0, "r": R_A * np.exp(R_DISP * z1)}
    if arm == "param":
        return {"K": np.clip(KP_0 + K_SD * z0 + K2_SD * z3, K_MIN, None),
                "x0": x0, "r": R_P * np.exp(R_DISP * z1)}
    if arm == "struct":
        return {"K1": np.clip(K0 + K_SD * z0, K_MIN, None),
                "x0": x0, "r1": R_A * np.exp(R_DISP * z1),
                "K2": np.clip(K2_0 + K2_SD * z3, K2_MIN, None),
                "r2": R2 * np.exp(R2_DISP * z4)}
    raise ValueError(f"unknown arm {arm!r}")


def struct_second_wave_component(n: int, seed: int, t_grid) -> np.ndarray:
    """The exact (n, k) second-wave contribution struct adds over retain."""
    t = np.asarray(tuple(t_grid), dtype=float)[None, :]
    p = _b_components("struct", _draws_b(n, seed))
    return _second_wave(p["K2"], p["r2"], t)


def _grid(regime) -> np.ndarray:
    grid = regime.context.get("t_grid")
    if grid is None:
        raise ValueError("ode_second_wave: every regime must declare context['t_grid']")
    return np.asarray(tuple(grid), dtype=float)


def _line(regime) -> str:
    line = str(regime.context.get("line", "A")).upper()
    if line not in LINES:
        raise ValueError("regime.context['line'] must be 'A' or 'B'")
    return line


def arm_sample(arm: str, regime, n: int, seed: int) -> pd.DataFrame:
    """Clean truth draw (LONG format). Sensor noise lives in the sources."""
    if arm not in ARMS:
        raise ValueError(f"unknown arm {arm!r}")
    t = _grid(regime)[None, :]
    if _line(regime) == "A":
        K, x0, r = _draws_a(n, seed)
        y = _logistic(K, x0, r, t)
    else:
        p = _b_components(arm, _draws_b(n, seed))
        if arm == "struct":
            y = _logistic(p["K1"], p["x0"], p["r1"], t) + _second_wave(p["K2"], p["r2"], t)
        else:
            y = _logistic(p["K"], p["x0"], p["r"], t)
    k = t.size
    return pd.DataFrame({
        "unit_id": np.repeat(np.arange(n, dtype=float), k),
        "t": np.tile(t.ravel(), n),
        "y": y.ravel(),
    })


class _FrozenRegime:
    def __init__(self, line: str, t_grid) -> None:
        self.config = {}
        self.context = {"line": line, "t_grid": tuple(float(v) for v in t_grid)}
        self.horizon = None


def mean_curve(arm: str, line: str, t_grid, n: int = _MC_N, seed: int = _MC_SEED) -> np.ndarray:
    """Deterministic Monte-Carlo population mean of the clean truth."""
    frame = arm_sample(arm, _FrozenRegime(line, t_grid), n, seed)
    wide = frame.pivot(index="unit_id", columns="t", values="y")
    grid = [float(v) for v in t_grid]
    return wide[grid].to_numpy(dtype=float).mean(axis=0)


def transfer_mean_curve(t_grid, n: int = _MC_N, seed: int = _MC_SEED) -> np.ndarray:
    """The A-law forecast for line B (the mechanical M_pre reference)."""
    return mean_curve("retain", "B", t_grid, n=n, seed=seed)


def dose_from_transfer(arm: str, t_grid=None) -> float:
    """Mean |B mean curve - A-law forecast| over the commissioning grid."""
    if t_grid is None:
        t_grid = DOSE_GRID
    return float(np.mean(np.abs(
        mean_curve(arm, "B", t_grid) - transfer_mean_curve(t_grid)
    )))


def calibrate_doses(rate_grid=None) -> dict:
    """Re-derive the dose match that froze R_P (audit tool, not a runtime knob)."""
    rates = rate_grid if rate_grid is not None else np.round(np.arange(0.30, 0.70, 0.002), 3)
    target = dose_from_transfer("struct")
    best, best_gap = None, np.inf
    global R_P
    frozen = R_P
    try:
        for rate in rates:
            R_P = float(rate)
            gap = abs(dose_from_transfer("param") - target)
            if gap < best_gap:
                best, best_gap = float(rate), gap
    finally:
        R_P = frozen
    return {"struct_dose": target, "best_rate": best, "best_gap": best_gap,
            "frozen_rate": frozen, "frozen_gap": abs(dose_from_transfer("param") - target)}


# --- one-vs-two phase fitter (BIC + unit CV + unit holdout) -----------------

def _predict_1p(theta, t):
    K, x0, r = theta
    a = (K - x0) / x0
    return K / (1.0 + a * np.exp(-r * t))


def _predict_2p(theta, t):
    K1, x0, r1, K2, r2, tmid = theta
    a = (K1 - x0) / x0
    return K1 / (1.0 + a * np.exp(-r1 * t)) + K2 / (1.0 + np.exp(-r2 * (t - tmid)))


_BOUNDS_1P = ([5.0, 0.2, 0.05], [400.0, 20.0, 2.5])
_BOUNDS_2P = ([5.0, 0.2, 0.05, 1.0, 0.05, 2.0], [400.0, 20.0, 2.5, 300.0, 3.0, 30.0])


def _fit(predict, starts, bounds, t, y):
    best = None
    for theta0 in starts:
        theta0 = np.clip(np.asarray(theta0, dtype=float), bounds[0], bounds[1])
        try:
            res = least_squares(
                lambda th: predict(th, t) - y, theta0, bounds=bounds,
                method="trf", max_nfev=4000,
            )
        except ValueError:
            continue
        sse = float(np.sum(res.fun ** 2))
        if best is None or sse < best[1]:
            best = (res.x, sse)
    if best is None:
        raise RuntimeError("curve fit failed from every start")
    return best


def _starts_1p(y):
    top = max(float(np.max(y)), 10.0)
    return [(top, 2.0, 0.3), (top, 2.0, 0.6), (120.0, 2.0, 0.5), (80.0, 2.0, 0.9)]


def _starts_2p(theta1, y):
    K, x0, r = theta1
    top = max(float(np.max(y)), 10.0)
    return [
        # Generic starts only: the fitter is an instrument, not a truth-aware
        # oracle.  The midpoint grid deliberately does not read world constants.
        (0.55 * top, 2.0, 0.5, 0.45 * top, 1.0, 16.0),
        (0.7 * K, x0, r, 0.35 * K, 0.8, 12.0),
        (0.75 * top, 2.0, 0.5, 0.35 * top, 0.6, 10.0),
        (K, x0, r, 2.0, 0.5, 8.0),
    ]


def _fit_both(t, y):
    theta1, sse1 = _fit(_predict_1p, _starts_1p(y), _BOUNDS_1P, t, y)
    theta2, sse2 = _fit(_predict_2p, _starts_2p(theta1, y), _BOUNDS_2P, t, y)
    return (theta1, sse1), (theta2, sse2)


def _bic(sse, n, k):
    return n * np.log(max(sse, 1e-12) / n) + k * np.log(n)


def _unit_folds(unit_ids, n_folds):
    units = np.unique(unit_ids)
    return [(units[fold::n_folds]) for fold in range(n_folds)]


def fit_phase_selection(frame: pd.DataFrame, n_folds: int = 5,
                        holdout_frac: float = 0.30, bic_margin: float = 6.0) -> dict:
    """Deterministic 1-vs-2 phase selection on exactly the served rows.

    two_phase is selected only when BIC prefers it by `bic_margin` AND the
    unit-level cross-validated RMSE AND the held-out-units RMSE both agree.
    """
    t = frame["t"].to_numpy(dtype=float)
    y = frame["y"].to_numpy(dtype=float)
    unit = frame["unit_id"].to_numpy(dtype=float)
    n = t.size

    (theta1, sse1), (theta2, sse2) = _fit_both(t, y)
    bic1, bic2 = _bic(sse1, n, 4), _bic(sse2, n, 7)

    def _cv(predict, starts_of, bounds):
        errors = []
        for val_units in _unit_folds(unit, n_folds):
            mask = np.isin(unit, val_units)
            th, _ = _fit(
                predict,
                starts_of(t[~mask], y[~mask]),
                bounds,
                t[~mask],
                y[~mask],
            )
            errors.append(np.sqrt(np.mean((predict(th, t[mask]) - y[mask]) ** 2)))
        return float(np.mean(errors)), None

    def _starts1(_t_train, y_train):
        return _starts_1p(y_train)

    def _starts2(t_train, y_train):
        th1, _ = _fit(
            _predict_1p,
            _starts_1p(y_train),
            _BOUNDS_1P,
            t_train,
            y_train,
        )
        return _starts_2p(th1, y_train)

    cv1, _ = _cv(_predict_1p, _starts1, _BOUNDS_1P)
    cv2, _ = _cv(_predict_2p, _starts2, _BOUNDS_2P)

    units = np.unique(unit)
    cut = units[int(np.ceil(len(units) * (1.0 - holdout_frac)))]
    train, test = unit < cut, unit >= cut
    th1_h, _ = _fit(_predict_1p, _starts_1p(y[train]), _BOUNDS_1P, t[train], y[train])
    th2_h, _ = _fit(_predict_2p, _starts_2p(th1_h, y[train]), _BOUNDS_2P, t[train], y[train])
    ho1 = float(np.sqrt(np.mean((_predict_1p(th1_h, t[test]) - y[test]) ** 2)))
    ho2 = float(np.sqrt(np.mean((_predict_2p(th2_h, t[test]) - y[test]) ** 2)))

    two_phase = bool((bic2 < bic1 - bic_margin) and (cv2 <= cv1) and (ho2 <= ho1))
    K1, _, _, K2, _, tmid2 = theta2
    return {
        "phases_selected": 2 if two_phase else 1,
        "bic_1p": float(bic1), "bic_2p": float(bic2),
        "delta_bic_2p_minus_1p": float(bic2 - bic1),
        "cv_rmse_1p": cv1, "cv_rmse_2p": cv2,
        "holdout_rmse_1p": ho1, "holdout_rmse_2p": ho2,
        "single_phase_holdout_ratio": float(ho1 / max(ho2, 1e-9)),
        "theta_1p": [float(v) for v in theta1],
        "theta_2p": [float(v) for v in theta2],
        "second_wave_share_2p": float(K2 / max(K1 + K2, 1e-9)),
        "second_wave_midpoint_2p": float(tmid2),
        "bic_margin": bic_margin,
    }


def model_phase_signature(sample_frame: pd.DataFrame) -> dict:
    """Phase signature of an ARTIFACT from its own samples (never its code)."""
    return fit_phase_selection(sample_frame)
