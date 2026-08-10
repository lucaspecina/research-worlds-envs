"""Shared truth + patch library + gates for the IMPASSE episode (mundo 2, v1).

Ficha: docs/research/2026-08-09-ficha-mundo-count-regime-v1-impasse.md
(+ ADDENDUM RATIFICADO 2026-08-09: compuertas A-E, tres brazos, claim reescrito).

Difference from v0 -- v0 SHOUTED (level jump 5.5 -> 11.5 in anyone's table) and
therefore measured ACCEPTANCE. Here:

  * the mean is CONTINUOUS at the hidden threshold s* (no level jump); only the
    SLOPE changes, so a smooth power law absorbs it inside the prefix design;
  * the same bias is buried by noise at prefix sample sizes and UNMISTAKABLE in
    the routine control lot (n large) -- non-flagrancy and visible failure are
    the same physics seen at two sample sizes, not two different worlds;
  * TWO fixed control lots at different speeds: the second one is the one that
    must survive the agent's PATCH (compuerta B), so a level/refit patch that
    absorbs control 1 still misses control 2.

Poles:
    count_regime_v1        BRK     lam(s) = lam0*s^alpha + delta1*max(0, s-s*)
    count_regime_twin_v1   SMOOTH  lam(s) = c*s^beta, level-paired on the exam grid

Zero-LLM zone: numpy/pandas/scipy only, deterministic everywhere.
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.special import gammaln

CASES_DIR = Path(__file__).resolve().parent
INSTANCE_PATH = CASES_DIR / "count_regime_v1" / "instance.json"

# --- ficha constants (frozen 2026-08-09; seeds per the ficha's assignment) ----
WORLD_SEEDS = tuple(list(range(99450, 99460)) + list(range(99468, 99490)))
LAM0_RANGE = (5.0, 7.0)
ALPHA_RANGE = (0.8, 1.2)
SSTAR_RANGE = (1.21, 1.25)          # JUST ABOVE the buyable envelope
DELTA1_RANGE = (45.0, 75.0)         # slope-only break; NO level jump (delta0=0)
SPEED_RANGE = (0.8, 1.40)           # settable range: experiments allowed anywhere
HISTORY_MAX = 1.20                  # the plant's historical envelope (archive +
                                    # the speeds a first sweep naturally samples);
                                    # NOT a fence — an agent may probe higher from
                                    # turn one, and if it does and catches the
                                    # regime, that is SPONTANEOUS generation.

# The prefix the agent can afford (archive + a typical spread of experiments).
PREFIX_ARCHIVE_SPEED = 1.0
PREFIX_ARCHIVE_N = 400
PREFIX_EXP_SPEEDS = (0.85, 0.95, 1.05, 1.12, 1.18)
PREFIX_EXP_N = 60

# The two ROUTINE control lots: PILOT runs at the proposed new speeds, launched
# by the plant on a fixed calendar (the agent neither chooses nor pays them).
# They sit ABOVE the buyable envelope -- that is where the regime pays, and it
# is the same place the decision lives (fidelity: you only meet the new defect
# mode when you actually run the line faster than history ever did).
CONTROL_1 = {"speed": 1.28, "n": 320}
CONTROL_2 = {"speed": 1.36, "n": 320}

# Gates (addendum ratificado). NOTE on the two thresholds that were re-specified
# on 2026-08-10 after the first scan (documented so this is not gate-loosening):
#   * NONFLAGRANT: with s* ABOVE the historical envelope the prefix contains ZERO
#     break — non-flagrancy is now STRUCTURAL, by construction. What the gate
#     still measures is noise: over 6 cells, max|z| under the pure-noise null
#     exceeds 2.0 by chance often, and exceeding 3.0 has p ~ 1.6% — so 3.0 is the
#     value that flags a real pattern instead of flagging luck.
#   * NECESSITY: measured on the DECISION band (speeds above the envelope, where
#     the stakes live) instead of averaged over the whole exam grid, where
#     in-range accuracy dilutes the very gap the decision depends on.
NONFLAGRANT_MAX_Z = 3.0             # gate 2: prefix must show no PATTERN (noise null)
FAIL_MIN_Z = 4.0                    # gate 3: control 1 must fail M0 visibly
PATCH_MIN_Z = 3.0                   # gate B: every patched model still fails control 2
NODICT_MAX_DBIC = 6.0               # gate 6: no candidate dominates at first failure
NODICT_MIN_RIVALS = 3
NECESSITY_D_RIVAL_MIN = 1.2         # gate 7: on the decision band (as v0)
TWIN_PAIRING_TOL = 0.35             # measured on the HISTORY surface, not the exam

CURVE_N = 1500
CURVE_SEED = 515151
DENSE_GRID = tuple(np.round(np.arange(0.80, 1.4001, 0.025), 3))
WITNESS_SAMPLE_SEED = 99512         # testigo seed (ficha)

ESPURIO_SSE_GAIN = 0.40
ESPURIO_JUMP_MIN = 1.0
FORCED_BREAK_DELTA = 3.0
FORCED_BREAK_AT = 1.10


# --- instance parameters ------------------------------------------------------

def params_from_seed(world_seed: int) -> dict:
    rng = np.random.default_rng(world_seed)
    return {"world_seed": int(world_seed),
            "lam0": rng.uniform(*LAM0_RANGE),
            "alpha": rng.uniform(*ALPHA_RANGE),
            "s_star": rng.uniform(*SSTAR_RANGE),
            "delta1": rng.uniform(*DELTA1_RANGE)}


def exam_grid(params: dict) -> tuple[float, ...]:
    """Exam speeds = the DECISION envelope: some inside history (so a model that
    only extrapolates wildly is punished too) and the proposed new operating band
    above it, where the two-law structure pays and a smooth extrapolation dies."""
    return (0.90, 1.05, 1.18, 1.26, 1.33, 1.40)


def decision_band(params: dict) -> tuple[float, ...]:
    """The exam speeds ABOVE the historical envelope — where the stakes live and
    where teleological necessity is measured."""
    return tuple(s for s in exam_grid(params) if s > HISTORY_MAX)


def history_grid() -> tuple[float, ...]:
    return tuple(s for s in DENSE_GRID if s <= HISTORY_MAX)


def zoom_design(pole: str, params: dict, seed: int = WITNESS_SAMPLE_SEED + 300):
    """What a competent agent buys AFTER the pilot lot fails: a fine sweep across
    the suspected threshold, now that higher speeds are worth probing. Used to
    certify that the evidence CAN discriminate (alcanzabilidad)."""
    frames = []
    for i, s in enumerate((1.22, 1.26, 1.31, 1.37)):
        frames.append((s, _sample_counts(pole, params, _DictRegime({"speed": s}),
                                         PREFIX_EXP_N, seed + i)))
    return frames


def load_instance() -> dict:
    if not INSTANCE_PATH.exists():
        raise RuntimeError("count_regime_v1 instance not frozen: run "
                           "scripts/build_certify_count_regime_v1.py")
    return json.loads(INSTANCE_PATH.read_text())


# --- generative truth ---------------------------------------------------------

def lam_truth(params: dict, s) -> np.ndarray:
    s = np.asarray(s, float)
    base = params["lam0"] * s ** params["alpha"]
    extra = params["delta1"] * np.maximum(0.0, s - params["s_star"])
    return base + extra


def twin_coeffs(params: dict) -> dict:
    """The twin is paired on the BUYABLE surface (<= BUYABLE_MAX), not on the
    exam grid: the two poles must be indistinguishable in everything the agent
    can purchase, and differ only in the band above the envelope — where one
    world changes law and the other does not."""
    grid = np.asarray([s for s in DENSE_GRID if s <= HISTORY_MAX], float)
    lam = lam_truth(params, grid)
    b, a = np.polyfit(np.log(grid), np.log(lam), 1)
    return {"c": float(np.exp(a)), "beta": float(b)}


def lam_twin(params: dict, s) -> np.ndarray:
    tw = twin_coeffs(params)
    return tw["c"] * np.asarray(s, float) ** tw["beta"]


def _speed_of(regime) -> float:
    config = getattr(regime, "config", None)
    if config is None and isinstance(regime, dict):
        config = regime.get("config", {})
    config = config or {}
    return min(max(float((config or {}).get("speed", 1.0)), SPEED_RANGE[0]), SPEED_RANGE[1])


class _DictRegime:
    def __init__(self, config):
        self.config = config


def _sample_counts(pole: str, params: dict, regime, n: int, seed: int) -> pd.DataFrame:
    speed = _speed_of(regime)
    rng = np.random.default_rng(np.random.SeedSequence([int(seed), 0x5631]))
    if pole == "brk":
        lam = float(lam_truth(params, speed))
    elif pole == "smooth":
        lam = float(lam_twin(params, speed))
    else:  # pragma: no cover
        raise ValueError(f"unknown pole {pole!r}")
    y = rng.poisson(lam, int(n)).astype(float)
    return pd.DataFrame({"unit_id": np.arange(int(n), dtype=float), "y": y},
                        columns=["unit_id", "y"])


def pole_sample(pole: str, regime, n: int, seed: int) -> pd.DataFrame:
    return _sample_counts(pole, load_instance()["params"], regime, n, seed)


# --- curve estimation of any delivered program --------------------------------

def program_curve(program, speeds, n: int = CURVE_N, seed: int = CURVE_SEED) -> np.ndarray:
    out = []
    for i, s in enumerate(speeds):
        df = program(_DictRegime({"speed": float(s)}), n, seed + i)
        out.append(float(np.asarray(df["y"], float).mean()))
    return np.asarray(out, float)


# --- smooth families: the strong rival and the patch library -------------------

def _fit_logpoly(speeds: np.ndarray, means: np.ndarray, deg: int) -> np.ndarray:
    """Least squares in (log s, log mean); returns numpy poly coefficients."""
    deg = min(deg, max(1, len(speeds) - 1))
    return np.polyfit(np.log(speeds), np.log(np.maximum(means, 1e-9)), deg)


def _predict_logpoly(coeffs: np.ndarray, s) -> np.ndarray:
    return np.exp(np.polyval(coeffs, np.log(np.asarray(s, float))))


def smooth_rival_coeffs(params: dict) -> dict:
    """Log-quadratic fit to the TRUE curve on the dense grid: the strongest
    3-parameter smooth family GIVEN GENEROUS information (gate 7 anchor)."""
    grid = np.asarray(DENSE_GRID, float)
    c = _fit_logpoly(grid, lam_truth(params, grid), 2)
    return {"coeffs": [float(v) for v in c]}


def lam_smooth_rival(params: dict, s) -> np.ndarray:
    return _predict_logpoly(np.asarray(smooth_rival_coeffs(params)["coeffs"], float), s)


def smooth_rival_program(params: dict):
    coeffs = np.asarray(smooth_rival_coeffs(params)["coeffs"], float)

    def prog(regime, n, seed, coeffs=coeffs):
        lam = float(_predict_logpoly(coeffs, _speed_of(regime)))
        rng = np.random.default_rng(np.random.SeedSequence([int(seed), 0x51711]))
        return pd.DataFrame({"unit_id": np.arange(int(n), dtype=float),
                             "y": rng.poisson(lam, int(n)).astype(float)})

    return prog


def prefix_design(pole: str, params: dict, seed: int = WITNESS_SAMPLE_SEED):
    """The affordable prefix: archive at 1.0 + the typical experiment spread."""
    frames = [(PREFIX_ARCHIVE_SPEED,
               _sample_counts(pole, params, _DictRegime({"speed": PREFIX_ARCHIVE_SPEED}),
                              PREFIX_ARCHIVE_N, seed))]
    for i, s in enumerate(PREFIX_EXP_SPEEDS):
        frames.append((s, _sample_counts(pole, params, _DictRegime({"speed": s}),
                                         PREFIX_EXP_N, seed + 10 + i)))
    return frames


def design_cells(design) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """(speeds, means, counts) sorted by speed."""
    sp = np.array([s for s, _ in design], float)
    mn = np.array([float(np.asarray(df["y"], float).mean()) for _, df in design])
    nn = np.array([len(df) for _, df in design], float)
    o = np.argsort(sp)
    return sp[o], mn[o], nn[o]


def m0_reference(design) -> dict:
    """The reference M0 a competent agent fits on the prefix: the best smooth
    (log-quadratic) power law. Used ONLY for certification -- the real M0 comes
    from the agent."""
    sp, mn, _ = design_cells(design)
    return {"family": "logquad", "coeffs": [float(v) for v in _fit_logpoly(sp, mn, 2)]}


def model_predict(model: dict, s) -> np.ndarray:
    fam = model["family"]
    if fam in ("logquad", "loglin", "logcubic", "spline"):
        return _predict_logpoly(np.asarray(model["coeffs"], float), s)
    if fam == "rescaled":
        base = np.asarray(model["coeffs"], float)
        return model["scale"] * _predict_logpoly(base, s)
    raise ValueError(f"unknown model family {fam!r}")  # pragma: no cover


def z_of_cell(model: dict, speed: float, obs_mean: float, n: float) -> float:
    """Standardized deviation of an observed cell mean from the model's
    prediction (Poisson SE). Signed."""
    pred = float(model_predict(model, speed))
    se = np.sqrt(max(pred, 1e-9) / max(n, 1.0))
    return float((obs_mean - pred) / se)


def control_cell(pole: str, params: dict, control: dict, seed: int) -> dict:
    df = _sample_counts(pole, params, _DictRegime({"speed": control["speed"]}),
                        control["n"], seed)
    return {"speed": control["speed"], "n": float(control["n"]),
            "mean": float(np.asarray(df["y"], float).mean()), "rows": df}


# --- the PATCH LIBRARY (compuerta B, ratificada) -------------------------------
# Peripheral repairs a competent agent reaches for after control 1 fails. Frozen
# here BEFORE any agent runs; every one of them must still miss control 2.

def patch_library(design, cell1: dict) -> dict[str, dict]:
    """Fit each peripheral patch to prefix + control-1 (except the outlier patch,
    which DISCARDS control 1 -- the 'es un outlier' move we want to catch)."""
    sp, mn, nn = design_cells(design)
    sp_a = np.append(sp, cell1["speed"])
    mn_a = np.append(mn, cell1["mean"])

    out: dict[str, dict] = {}
    # 1. refit the same smooth family including the new lot
    out["refit_logquad"] = {"family": "logquad",
                            "coeffs": [float(v) for v in _fit_logpoly(sp_a, mn_a, 2)]}
    # 2. drop the offending lot as an outlier and keep the old fit
    out["drop_outlier"] = {"family": "logquad",
                           "coeffs": [float(v) for v in _fit_logpoly(sp, mn, 2)]}
    # 3. heteroscedasticity: same mean curve, "extra dispersion" -- mean unchanged
    out["heteroscedastic"] = {"family": "logquad",
                              "coeffs": [float(v) for v in _fit_logpoly(sp_a, mn_a, 2)]}
    # 4. more flexible smooth: log-cubic through everything seen
    out["logcubic"] = {"family": "logcubic",
                       "coeffs": [float(v) for v in _fit_logpoly(sp_a, mn_a, 3)]}
    # 5. recalibration: multiplicative offset so the old fit matches control 1
    base = _fit_logpoly(sp, mn, 2)
    scale = float(cell1["mean"] / max(float(_predict_logpoly(base, cell1["speed"])), 1e-9))
    out["recalibrated"] = {"family": "rescaled",
                           "coeffs": [float(v) for v in base], "scale": scale}
    return out


# --- witness / BIC selection ---------------------------------------------------

def _poisson_ll_cells(means: np.ndarray, ns: np.ndarray, pred: np.ndarray) -> float:
    """Poisson log-likelihood of cell means (sufficient statistics)."""
    pred = np.maximum(pred, 1e-9)
    tot = means * ns
    return float(np.sum(tot * np.log(pred) - ns * pred - gammaln(tot + 1.0)))


def fit_regime_family(sp, mn, nn) -> dict:
    """Fit the STRUCTURAL rival — the two-law family itself:
        lam(s) = lam0 * s^alpha + delta1 * max(0, s - s*)
    by scanning the threshold and least-squares on the rest. Four parameters.
    This is the candidate a regime-positing agent delivers, so the BIC
    comparison must use IT (not a proxy of two log-linear segments, which
    approximates the truth badly and would lose for the wrong reason)."""
    best = {"sse": np.inf}
    logs, logm = np.log(sp), np.log(np.maximum(mn, 1e-9))
    for s_star in np.arange(1.00, 1.351, 0.01):
        ramp = np.maximum(0.0, sp - s_star)
        if not np.any(ramp > 0):
            continue
        # profile over (lam0, alpha) with a coarse alpha scan, delta1 by LS
        for alpha in np.arange(0.5, 1.81, 0.05):
            base = sp ** alpha
            A = np.column_stack([base, ramp])
            coef, *_ = np.linalg.lstsq(A, mn, rcond=None)
            if coef[0] <= 0 or coef[1] < 0:
                continue
            pred = A @ coef
            sse = float(np.sum(nn * (mn - pred) ** 2 / np.maximum(pred, 1e-9)))
            if sse < best["sse"]:
                best = {"sse": sse, "s_star": float(s_star), "alpha": float(alpha),
                        "lam0": float(coef[0]), "delta1": float(coef[1])}
    return best


def _regime_bic(sp, mn, nn, n_total) -> dict:
    fit = fit_regime_family(sp, mn, nn)
    if not np.isfinite(fit.get("sse", np.inf)):
        return {"bic": np.inf, "split": None}
    pred = fit["lam0"] * sp ** fit["alpha"] + fit["delta1"] * np.maximum(0.0, sp - fit["s_star"])
    ll = _poisson_ll_cells(mn, nn, pred)
    return {"bic": float(4 * np.log(n_total) - 2.0 * ll), "split": fit["s_star"]}


def _piecewise_bic(sp, mn, nn, n_total) -> dict:
    best = {"bic": np.inf, "split": None}
    x = np.log(sp)
    for k in range(2, len(sp) - 1):
        preds = []
        for xs, ms in ((x[:k], mn[:k]), (x[k:], mn[k:])):
            if len(xs) >= 2:
                b, a = np.polyfit(xs, np.log(np.maximum(ms, 1e-9)), 1)
            else:
                a, b = float(np.log(max(ms[0], 1e-9))), 0.0
            preds.append(np.exp(a + b * xs))
        ll = _poisson_ll_cells(mn, nn, np.concatenate(preds))
        bic = 5 * np.log(n_total) - 2.0 * ll
        if bic < best["bic"]:
            best = {"bic": float(bic), "split": float(sp[k])}
    return best


def candidate_bics(design, extra_cells: list[dict] | None = None) -> dict:
    """BIC of the structurally distinct explanations alive on the evidence.
    Used by gate 6 (no-dictation) and by the discrimination-point rule."""
    sp, mn, nn = design_cells(design)
    for c in (extra_cells or []):
        sp, mn, nn = np.append(sp, c["speed"]), np.append(mn, c["mean"]), np.append(nn, c["n"])
    o = np.argsort(sp)
    sp, mn, nn = sp[o], mn[o], nn[o]
    n_total = float(np.sum(nn))

    out = {}
    for name, deg, k in (("smooth_loglin", 1, 2), ("smooth_logquad", 2, 3),
                         ("smooth_logcubic", 3, 4)):
        pred = _predict_logpoly(_fit_logpoly(sp, mn, deg), sp)
        out[name] = float(k * np.log(n_total) - 2.0 * _poisson_ll_cells(mn, nn, pred))
    pw = _piecewise_bic(sp, mn, nn, n_total)
    rg = _regime_bic(sp, mn, nn, n_total)
    # "regime" = the structural candidate; piecewise-in-log is kept as a second,
    # cruder structural option (an agent may deliver either).
    out["regime"] = rg["bic"]
    out["piecewise_log"] = pw["bic"]
    out["_split"] = rg["split"]
    return out


def discrimination_gap(design, extra_cells=None) -> float:
    """dBIC of the best SMOOTH candidate minus the best STRUCTURAL one
    (>0 = structure wins). The discrimination point is where this crosses +6
    and stays there with the next purchase."""
    b = candidate_bics(design, extra_cells)
    smooth = [v for k, v in b.items() if k.startswith("smooth_")]
    structural = [b["regime"], b["piecewise_log"]]
    return float(min(smooth) - min(structural))


# --- S metrics -----------------------------------------------------------------

def curve_distance(a, b) -> float:
    return float(np.mean(np.abs(np.asarray(a) - np.asarray(b))))


def s_quiebre(program, params: dict) -> dict:
    grid = np.asarray(exam_grid(params), float)
    lam_t = lam_truth(params, grid)
    d_rival = curve_distance(lam_smooth_rival(params, grid), lam_t)
    d_model = curve_distance(program_curve(program, grid), lam_t)
    s = 0.0 if d_rival < 1e-9 else float(np.clip(1.0 - d_model / d_rival, 0.0, 1.0))
    return {"S_quiebre_fuerte": s, "D_model": d_model, "D_rival": d_rival}


def f_mean(program, params: dict, pole: str) -> float:
    lam_t = float(lam_truth(params, 1.0) if pole == "brk" else lam_twin(params, 1.0))
    lam_m = program_curve(program, (1.0,))[0]
    return float(np.clip(1.0 - abs(lam_m - lam_t) / max(lam_t, 1e-9), 0.0, 1.0))


def forced_break_program(params: dict):
    tw = twin_coeffs(params)

    def prog(regime, n, seed, tw=tw):
        speed = _speed_of(regime)
        lam = tw["c"] * speed ** tw["beta"] + (FORCED_BREAK_DELTA if speed >= FORCED_BREAK_AT else 0.0)
        rng = np.random.default_rng(np.random.SeedSequence([int(seed), 0xF02CF]))
        return pd.DataFrame({"unit_id": np.arange(int(n), dtype=float),
                             "y": rng.poisson(lam, int(n)).astype(float)})

    return prog


def s_clean(program, params: dict) -> dict:
    grid = np.asarray(exam_grid(params), float)
    lam_t = lam_twin(params, grid)
    d_forced = curve_distance(program_curve(forced_break_program(params), grid), lam_t)
    d_model = curve_distance(program_curve(program, grid), lam_t)
    s = 0.0 if d_forced < 1e-9 else float(np.clip(1.0 - d_model / d_forced, 0.0, 1.0))
    return {"S_clean": s, "D_model": d_model, "D_forced": d_forced}


def _piecewise_fit_curve(grid: np.ndarray, lam: np.ndarray) -> dict:
    x, ly = np.log(grid), np.log(np.maximum(lam, 1e-9))

    def sse_lin(xs, ys):
        if len(xs) < 2:
            return 0.0, (float(ys.mean()) if len(ys) else 0.0, 0.0)
        b, a = np.polyfit(xs, ys, 1)
        return float(np.sum((ys - (a + b * xs)) ** 2)), (a, b)

    smooth_sse, _ = sse_lin(x, ly)
    best = {"sse": np.inf, "split": None, "jump": 0.0}
    for k in range(2, len(grid) - 1):
        sse_lo, (a1, b1) = sse_lin(x[:k], ly[:k])
        sse_hi, (a2, b2) = sse_lin(x[k:], ly[k:])
        sse = sse_lo + sse_hi
        if sse < best["sse"]:
            xs = x[k]
            best = {"sse": sse, "split": float(grid[k]),
                    "jump": float(np.exp(a2 + b2 * xs) - np.exp(a1 + b1 * xs))}
    gain = 0.0 if smooth_sse < 1e-12 else float(1.0 - best["sse"] / smooth_sse)
    return {"gain": gain, "split": best["split"], "jump": best["jump"]}


def spurious_break_flag(program, params: dict) -> dict:
    grid = np.asarray(DENSE_GRID[::2], float)
    fit = _piecewise_fit_curve(grid, program_curve(program, grid))
    flag = (fit["gain"] >= ESPURIO_SSE_GAIN) and (abs(fit["jump"]) >= ESPURIO_JUMP_MIN)
    return {"spurious": bool(flag), **fit}
