"""Shared truth + witness + metrics for the regime-break jump pair (mundo 2).

Two poles share one surface (byte-identical brief, single knob `speed`):

    count_regime_v0       BRK     y ~ Poisson(lam(speed)) with a LEVEL+SLOPE
                                  break at hidden s* (law A below, law B above)
    count_regime_twin_v0  SMOOTH  y ~ Poisson(c * speed**beta), single smooth
                                  power law level-paired to BRK on the exam grid

One measurement per lot (unit_id sequential); the jump lives in the SHAPE of
the mean curve lam(speed) — a smooth family cannot produce the discontinuity,
so the payoff is extrapolation across the threshold (ficha 2026-08-07; A2 fix
by construction).

Instance parameters are NOT hand-picked: the certify script scans world seeds
99400..99449 and freezes the first instance passing ALL ficha gates into
cases/count_regime_v0/instance.json; this module loads it from disk.

Zero-LLM zone: numpy/pandas only, deterministic everywhere.
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd

CASES_DIR = Path(__file__).resolve().parent
INSTANCE_PATH = CASES_DIR / "count_regime_v0" / "instance.json"

# --- ficha constants (frozen 2026-08-07) ------------------------------------
WORLD_SEEDS = range(99400, 99450)
LAM0_RANGE = (5.0, 7.0)
ALPHA_RANGE = (0.8, 1.2)
SSTAR_RANGE = (1.06, 1.14)
DELTA0_RANGE = (3.0, 5.0)
DELTA1_RANGE = (15.0, 30.0)
SPEED_RANGE = (0.8, 1.2)

NECESSITY_D_RIVAL_MIN = 1.2     # gate 2: strong smooth rival gap on exam grid
WITNESS_DBIC_BRK = 10.0         # gate 3: piecewise beats smooth in BRK
WITNESS_DBIC_SMOOTH = 6.0       # gate 4: smooth beats piecewise in twin
TWIN_PAIRING_TOL = 0.35         # gate 4: exam-grid level pairing

WITNESS_SAMPLE_SEED = 99499
WITNESS_ARCHIVE_N = 200         # buyable design (ficha): archive rows at 1.0
WITNESS_EXP_SPEEDS = (0.8, 0.95, 1.05, 1.12, 1.2)
WITNESS_EXP_N = 70              # lots per experiment in the buyable design

CURVE_N = 1500                  # samples per grid speed when estimating lam-hat
CURVE_SEED = 424242
DENSE_GRID = tuple(np.round(np.arange(0.80, 1.2001, 0.025), 3))

ESPURIO_SSE_GAIN = 0.40         # twin flag: piecewise SSE improvement >= 40%
ESPURIO_JUMP_MIN = 1.5          # ...and implied level jump >= 1.5 defects
FORCED_BREAK_DELTA = 4.0        # S_clean zero-anchor: injected break size
FORCED_BREAK_AT = 1.10


# --- instance parameters -----------------------------------------------------

def params_from_seed(world_seed: int) -> dict:
    rng = np.random.default_rng(world_seed)
    lam0 = rng.uniform(*LAM0_RANGE)
    alpha = rng.uniform(*ALPHA_RANGE)
    s_star = rng.uniform(*SSTAR_RANGE)
    delta0 = rng.uniform(*DELTA0_RANGE)
    delta1 = rng.uniform(*DELTA1_RANGE)
    return {"world_seed": world_seed, "lam0": lam0, "alpha": alpha,
            "s_star": s_star, "delta0": delta0, "delta1": delta1}


def exam_grid(params: dict) -> tuple[float, ...]:
    return (0.85, 0.95, 1.05, 1.10, round(params["s_star"] + 0.01, 4), 1.18)


def load_instance() -> dict:
    if not INSTANCE_PATH.exists():
        raise RuntimeError(
            "count_regime instance not frozen yet: run scripts/build_certify_count_regime_v0.py"
        )
    return json.loads(INSTANCE_PATH.read_text())


# --- generative truth --------------------------------------------------------

def lam_truth(params: dict, s) -> np.ndarray:
    s = np.asarray(s, float)
    base = params["lam0"] * s ** params["alpha"]
    extra = np.where(s >= params["s_star"],
                     params["delta0"] + params["delta1"] * (s - params["s_star"]), 0.0)
    return base + extra


def twin_coeffs(params: dict) -> dict:
    """Smooth power law c*s^beta level-paired to the BRK curve on the exam
    grid (LS on logs). Deterministic from params."""
    grid = np.asarray(exam_grid(params), float)
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
    speed = float(config.get("speed", 1.0))
    return min(max(speed, SPEED_RANGE[0]), SPEED_RANGE[1])


def _sample_counts(pole: str, params: dict, regime, n: int, seed: int) -> pd.DataFrame:
    """n = number of LOTS (one measurement per lot)."""
    speed = _speed_of(regime)
    rng = np.random.default_rng(np.random.SeedSequence([int(seed), 0x4E61]))
    if pole == "brk":
        lam = float(lam_truth(params, speed))
    elif pole == "smooth":
        lam = float(lam_twin(params, speed))
    else:  # pragma: no cover
        raise ValueError(f"unknown pole {pole!r}")
    y = rng.poisson(lam, int(n)).astype(float)
    ids = np.arange(int(n), dtype=float)
    return pd.DataFrame({"unit_id": ids, "y": y}, columns=["unit_id", "y"])


def pole_sample(pole: str, regime, n: int, seed: int) -> pd.DataFrame:
    return _sample_counts(pole, load_instance()["params"], regime, n, seed)


# --- curve estimation of any program -----------------------------------------

class _DictRegime:
    def __init__(self, config):
        self.config = config


def program_curve(program, speeds, n: int = CURVE_N, seed: int = CURVE_SEED) -> np.ndarray:
    """lam-hat(s) = mean of the program's counts at each speed (deterministic)."""
    out = []
    for i, s in enumerate(speeds):
        df = program(_DictRegime({"speed": float(s)}), n, seed + i)
        out.append(float(np.asarray(df["y"], float).mean()))
    return np.asarray(out, float)


def program_functionals(program, params: dict) -> dict:
    """Descriptive vector: level at 1.0 + curve landmarks + implied jump."""
    s_star = params["s_star"]
    speeds = (0.85, 1.0, round(s_star - 0.01, 4), round(s_star + 0.01, 4), 1.18)
    lam = program_curve(program, speeds)
    return {"mean": lam[1], "lam_085": lam[0], "lam_pre": lam[2],
            "lam_post": lam[3], "lam_118": lam[4],
            "jump": float(lam[3] - lam[2])}


# --- strong smooth rival (the honest zero-anchor) ----------------------------

def smooth_rival_coeffs(params: dict) -> dict:
    """Log-quadratic fit to the TRUE curve on the dense grid — the strongest
    3-parameter smooth family given GENEROUS information (ficha gate 2)."""
    grid = np.asarray(DENSE_GRID, float)
    lam = lam_truth(params, grid)
    x = np.log(grid)
    c2, c1, c0 = np.polyfit(x, np.log(lam), 2)
    return {"c0": float(c0), "c1": float(c1), "c2": float(c2)}


def lam_smooth_rival(params: dict, s) -> np.ndarray:
    cf = smooth_rival_coeffs(params)
    x = np.log(np.asarray(s, float))
    return np.exp(cf["c0"] + cf["c1"] * x + cf["c2"] * x * x)


def smooth_rival_program(params: dict):
    cf = smooth_rival_coeffs(params)

    def prog(regime, n, seed, cf=cf):
        speed = _speed_of(regime)
        x = np.log(speed)
        lam = float(np.exp(cf["c0"] + cf["c1"] * x + cf["c2"] * x * x))
        rng = np.random.default_rng(np.random.SeedSequence([int(seed), 0x51710]))
        y = rng.poisson(lam, int(n)).astype(float)
        return pd.DataFrame({"unit_id": np.arange(int(n), dtype=float), "y": y})

    return prog


# --- S metrics ----------------------------------------------------------------

def curve_distance(lam_a: np.ndarray, lam_b: np.ndarray) -> float:
    return float(np.mean(np.abs(np.asarray(lam_a) - np.asarray(lam_b))))


def s_quiebre(program, params: dict) -> dict:
    """Break capture vs the STRONG smooth rival: 0 = rival, 1 = truth."""
    grid = np.asarray(exam_grid(params), float)
    lam_t = lam_truth(params, grid)
    d_rival = curve_distance(lam_smooth_rival(params, grid), lam_t)
    d_model = curve_distance(program_curve(program, grid), lam_t)
    s = 0.0 if d_rival < 1e-9 else float(np.clip(1.0 - d_model / d_rival, 0.0, 1.0))
    return {"S_quiebre_fuerte": s, "D_model": d_model, "D_rival": d_rival}


def f_mean(program, params: dict, pole: str) -> float:
    lam_t = float(lam_truth(params, 1.0) if pole == "brk" else lam_twin(params, 1.0))
    lam_m = program_curve(program, (1.0,))[0]
    denom = max(lam_t, 1e-9)
    return float(np.clip(1.0 - abs(lam_m - lam_t) / denom, 0.0, 1.0))


# --- twin instruments ---------------------------------------------------------

def _piecewise_fit(grid: np.ndarray, lam: np.ndarray) -> dict:
    """Best 2-segment power-law fit with split on interior grid points."""
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
            jump = float(np.exp(a2 + b2 * xs) - np.exp(a1 + b1 * xs))
            best = {"sse": sse, "split": float(grid[k]), "jump": jump}
    gain = 0.0 if smooth_sse < 1e-12 else float(1.0 - best["sse"] / smooth_sse)
    return {"smooth_sse": smooth_sse, "pw_sse": float(best["sse"]),
            "gain": gain, "split": best["split"], "jump": best["jump"]}


def spurious_break_flag(program, params: dict) -> dict:
    """Twin 'espurio': the delivered program's curve exhibits a substantive
    break where the world has none (ficha thresholds)."""
    grid = np.asarray(DENSE_GRID[::2], float)     # 9 speeds, cheap
    lam = program_curve(program, grid)
    fit = _piecewise_fit(grid, lam)
    flag = (fit["gain"] >= ESPURIO_SSE_GAIN) and (abs(fit["jump"]) >= ESPURIO_JUMP_MIN)
    return {"spurious": bool(flag), **{k: fit[k] for k in ("gain", "split", "jump")}}


def forced_break_program(params: dict):
    """Apophenia zero-anchor for the twin: the twin curve with an injected
    level break of FORCED_BREAK_DELTA at FORCED_BREAK_AT."""
    tw = twin_coeffs(params)

    def prog(regime, n, seed, tw=tw):
        speed = _speed_of(regime)
        lam = tw["c"] * speed ** tw["beta"]
        if speed >= FORCED_BREAK_AT:
            lam += FORCED_BREAK_DELTA
        rng = np.random.default_rng(np.random.SeedSequence([int(seed), 0xF02CE]))
        y = rng.poisson(lam, int(n)).astype(float)
        return pd.DataFrame({"unit_id": np.arange(int(n), dtype=float), "y": y})

    return prog


def s_clean(program, params: dict) -> dict:
    """Twin cleanliness: 1 = smooth truth, 0 = forced-break program."""
    grid = np.asarray(exam_grid(params), float)
    lam_t = lam_twin(params, grid)
    d_forced = curve_distance(program_curve(forced_break_program(params), grid), lam_t)
    d_model = curve_distance(program_curve(program, grid), lam_t)
    s = 0.0 if d_forced < 1e-9 else float(np.clip(1.0 - d_model / d_forced, 0.0, 1.0))
    return {"S_clean": s, "D_model": d_model, "D_forced": d_forced}


# --- witness (alcanzabilidad, gates 3/4) --------------------------------------

def buyable_design(pole: str, params: dict, seed: int = WITNESS_SAMPLE_SEED):
    """The ficha's affordable shopping set: archive at 1.0 + five experiments."""
    frames = [(1.0, _sample_counts(pole, params, _DictRegime({"speed": 1.0}),
                                   WITNESS_ARCHIVE_N, seed))]
    for i, s in enumerate(WITNESS_EXP_SPEEDS):
        frames.append((s, _sample_counts(pole, params, _DictRegime({"speed": s}),
                                         WITNESS_EXP_N, seed + 10 + i)))
    return frames


def _poisson_ll(y: np.ndarray, lam: float) -> float:
    lam = max(lam, 1e-9)
    from scipy.special import gammaln
    return float(np.sum(y * np.log(lam) - lam - gammaln(y + 1.0)))


def witness(design) -> dict:
    """Piecewise-vs-smooth selection by BIC on the buyable design. Smooth =
    log-quadratic on (speed, mean) via Poisson MLE per speed cell; piecewise =
    2-segment log-linear with split scanned on the sampled speeds."""
    speeds = np.array([s for s, _ in design], float)
    ys = [np.asarray(df["y"], float) for _, df in design]
    order = np.argsort(speeds)
    speeds, ys = speeds[order], [ys[i] for i in order]
    x = np.log(speeds)
    means = np.array([max(y.mean(), 1e-9) for y in ys])
    n_total = int(sum(len(y) for y in ys))

    def ll_curve(pred_lam):
        return sum(_poisson_ll(y, lam) for y, lam in zip(ys, pred_lam))

    c2, c1, c0 = np.polyfit(x, np.log(means), 2)
    ll_smooth = ll_curve(np.exp(c0 + c1 * x + c2 * x * x))
    bic_smooth = 3 * np.log(n_total) - 2.0 * ll_smooth

    best_pw = {"bic": np.inf, "split": None}
    for k in range(2, len(speeds) - 1):
        fits = []
        for xs, seg in ((x[:k], ys[:k]), (x[k:], ys[k:])):
            m = np.array([max(y.mean(), 1e-9) for y in seg])
            b, a = np.polyfit(xs, np.log(m), 1) if len(xs) >= 2 else (0.0, np.log(m[0]))
            fits.append(np.exp(a + b * xs))
        ll_pw = ll_curve(np.concatenate(fits))
        bic_pw = 5 * np.log(n_total) - 2.0 * ll_pw
        if bic_pw < best_pw["bic"]:
            best_pw = {"bic": float(bic_pw), "split": float(speeds[k])}

    dbic = float(bic_smooth - best_pw["bic"])   # >0 => piecewise wins
    return {"bic_smooth": float(bic_smooth), "bic_piecewise": best_pw["bic"],
            "dbic_pw_vs_smooth": dbic, "split": best_pw["split"],
            "selected": "piecewise" if dbic > 0 else "smooth"}
