"""Shared truth + witness + functionals for the count-mixture jump pair (slice 1).

Two poles share one surface (byte-identical brief, menu, control knobs):

    count_mix_v0       MIX    y ~ Poisson(lam[Z_i] * speed), Z_i ~ Bern(w) per LOT
    count_mix_twin_v0  SINGLE y ~ Poisson(lam0 * speed),     lam0 = mean-paired

The difference lives ONLY in shape (Fano, zeros, valley, tails, ICC under
repeated measures); the mean is paired by construction at every speed.

Instance parameters are NOT hand-picked: `find_instance()` scans world seeds
99200..99249 (ficha 2026-08-06) and accepts the first that passes the frozen
gates (witness margin + anti-poster). The accepted instance is written to
cases/count_mix_v0/instance.json by scripts/certify_count_mix_v0.py and loaded
from disk here — the rule chooses, the file records.

Zero-LLM zone: numpy/pandas/scipy only, deterministic everywhere.
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.optimize import minimize
from scipy.special import gammaln, logsumexp
from scipy.stats import poisson

CASES_DIR = Path(__file__).resolve().parent
INSTANCE_PATH = CASES_DIR / "count_mix_v0" / "instance.json"

# --- ficha constants (frozen 2026-08-06) ------------------------------------
WORLD_SEEDS = range(99200, 99250)
W_RANGE = (0.35, 0.65)
LAM_A_RANGE = (0.8, 2.5)
RATIO_RANGE = (3.5, 6.0)
SPEED_RANGE = (0.8, 1.2)
REPEATS_RANGE = (1, 4)
WITNESS_N = 300           # purchasable-size sample the witness runs on
WITNESS_DBIC = 10.0       # G1 margin in MIX
ANTI_POSTER_FLOOR = 0.20  # valley pmf >= 20% of the smaller peak's pmf
CV_FOLDS = 5

FUNCTIONAL_N = 4000       # marginal-functional sampling size (per program)
ICC_UNITS = 200
ICC_REPEATS = 3
FUNCTIONAL_SEED = 424242  # fixed: functionals are deterministic per program


# --- instance parameters -----------------------------------------------------

def params_from_seed(world_seed: int) -> dict:
    rng = np.random.default_rng(world_seed)
    w = rng.uniform(*W_RANGE)
    lam_a = rng.uniform(*LAM_A_RANGE)
    lam_b = lam_a * rng.uniform(*RATIO_RANGE)
    return {"world_seed": world_seed, "w": w, "lam_a": lam_a, "lam_b": lam_b,
            "lam0": w * lam_b + (1.0 - w) * lam_a}


def load_instance() -> dict:
    if not INSTANCE_PATH.exists():
        raise RuntimeError(
            "count_mix instance not frozen yet: run scripts/certify_count_mix_v0.py"
        )
    return json.loads(INSTANCE_PATH.read_text())


# --- generative truth --------------------------------------------------------

def _regime_knobs(regime) -> tuple[float, int]:
    config = getattr(regime, "config", None)
    if config is None and isinstance(regime, dict):
        config = regime.get("config", {})
    config = config or {}
    speed = float(config.get("speed", 1.0))
    repeats = int(round(float(config.get("repeats_per_unit", 1))))
    speed = min(max(speed, SPEED_RANGE[0]), SPEED_RANGE[1])
    repeats = min(max(repeats, REPEATS_RANGE[0]), REPEATS_RANGE[1])
    return speed, repeats


def _unit_ids_for(n: int, repeats: int) -> np.ndarray:
    """n counts MEASUREMENT ROWS (platform contract: model returns exactly n
    rows). Lots = ceil(n/repeats); the last lot may carry fewer repeats."""
    full, rem = divmod(n, repeats)
    ids = np.repeat(np.arange(full, dtype=float), repeats)
    if rem:
        ids = np.concatenate([ids, np.full(rem, float(full))])
    return ids


def _sample_counts(pole: str, params: dict, regime, n: int, seed: int) -> pd.DataFrame:
    """n = number of MEASUREMENT ROWS; unit_id groups repeats of one lot."""
    speed, repeats = _regime_knobs(regime)
    rng = np.random.default_rng(np.random.SeedSequence([int(seed), 0xC0117]))
    ids = _unit_ids_for(n, repeats)
    n_units = int(ids[-1]) + 1 if n else 0
    if pole == "mix":
        z = rng.random(n_units) < params["w"]
        lam_by_unit = np.where(z, params["lam_b"], params["lam_a"]) * speed
    elif pole == "single":
        lam_by_unit = np.full(n_units, params["lam0"]) * speed
    else:  # pragma: no cover
        raise ValueError(f"unknown pole {pole!r}")
    y = rng.poisson(lam_by_unit[ids.astype(int)]).astype(float)
    return pd.DataFrame({"unit_id": ids, "y": y}, columns=["unit_id", "y"])


def pole_sample(pole: str, regime, n: int, seed: int) -> pd.DataFrame:
    return _sample_counts(pole, load_instance()["params"], regime, n, seed)


# --- count-model fitters (the witness lattice) -------------------------------
# All return dict(loglik=..., k=..., pmf=callable) on integer support.

def _fit_poisson(y: np.ndarray) -> dict:
    lam = max(float(y.mean()), 1e-9)
    ll = float(poisson.logpmf(y, lam).sum())
    return {"name": "poisson", "k": 1, "loglik": ll, "params": {"lam": lam},
            "logpmf": lambda x, lam=lam: poisson.logpmf(x, lam)}


def _negbin_logpmf(y, m, alpha):
    # var = m (1 + alpha m); r = 1/alpha, p = 1/(1 + alpha m)
    r = 1.0 / alpha
    logp = -np.log1p(alpha * m)
    log1mp = np.log(alpha * m) + logp
    return (gammaln(y + r) - gammaln(r) - gammaln(y + 1.0)
            + r * logp + y * log1mp)


def _fit_negbin(y: np.ndarray) -> dict:
    m0 = max(float(y.mean()), 1e-6)
    v0 = max(float(y.var()), m0 + 1e-6)
    a0 = max((v0 - m0) / (m0 ** 2), 1e-4)

    def nll(theta):
        m, alpha = np.exp(theta)
        return -float(_negbin_logpmf(y, m, alpha).sum())

    res = minimize(nll, x0=np.log([m0, a0]), method="Nelder-Mead",
                   options={"xatol": 1e-6, "fatol": 1e-8, "maxiter": 2000})
    m, alpha = np.exp(res.x)
    return {"name": "negbin", "k": 2, "loglik": -float(res.fun),
            "params": {"mean": float(m), "alpha": float(alpha)},
            "logpmf": lambda x, m=m, a=alpha: _negbin_logpmf(np.asarray(x, float), m, a)}


def _zip_logpmf(y, pi, lam):
    y = np.asarray(y, float)
    base = poisson.logpmf(y, lam) + np.log1p(-pi)
    zero = np.logaddexp(np.log(pi + 1e-300), np.log1p(-pi) - lam)
    return np.where(y == 0, zero, base)


def _fit_zip(y: np.ndarray) -> dict:
    p0_obs = float((y == 0).mean())
    lam0 = max(float(y[y > 0].mean()) if (y > 0).any() else 1.0, 1e-6)

    def nll(theta):
        pi = 1.0 / (1.0 + np.exp(-theta[0]))
        lam = np.exp(theta[1])
        return -float(_zip_logpmf(y, pi, lam).sum())

    x0 = [np.log(max(p0_obs, 1e-3) / max(1 - p0_obs, 1e-3)), np.log(lam0)]
    res = minimize(nll, x0=x0, method="Nelder-Mead",
                   options={"xatol": 1e-6, "fatol": 1e-8, "maxiter": 2000})
    pi = 1.0 / (1.0 + np.exp(-res.x[0]))
    lam = float(np.exp(res.x[1]))
    return {"name": "zip", "k": 2, "loglik": -float(res.fun),
            "params": {"pi": float(pi), "lam": lam},
            "logpmf": lambda x, p=pi, l=lam: _zip_logpmf(x, p, l)}


def _fit_mix2(y: np.ndarray, iters: int = 300, tol: float = 1e-9) -> dict:
    lo, hi = np.quantile(y, [0.25, 0.75])
    lam = np.array([max(lo, 0.05), max(hi, lo + 0.5)])
    w = np.array([0.5, 0.5])
    ll_old = -np.inf
    for _ in range(iters):
        logp = np.stack([np.log(w[j] + 1e-300) + poisson.logpmf(y, lam[j])
                         for j in range(2)])
        norm = logsumexp(logp, axis=0)
        resp = np.exp(logp - norm)
        w = resp.mean(axis=1)
        lam = np.maximum((resp * y).sum(axis=1) / np.maximum(resp.sum(axis=1), 1e-12), 1e-6)
        ll = float(norm.sum())
        if abs(ll - ll_old) < tol:
            break
        ll_old = ll
    order = np.argsort(lam)
    lam, w = lam[order], w[order]

    def logpmf(x, w=w, lam=lam):
        x = np.asarray(x, float)
        comp = np.stack([np.log(w[j] + 1e-300) + poisson.logpmf(x, lam[j])
                         for j in range(2)])
        return logsumexp(comp, axis=0)

    return {"name": "mix2", "k": 3, "loglik": float(ll),
            "params": {"w_low": float(w[0]), "lam_low": float(lam[0]),
                       "w_high": float(w[1]), "lam_high": float(lam[1])},
            "logpmf": logpmf}


FITTERS = (_fit_poisson, _fit_negbin, _fit_zip, _fit_mix2)


def witness(y: np.ndarray, cv_seed: int = 7) -> dict:
    """BIC + k-fold CV model selection over the frozen lattice. Zero-LLM."""
    y = np.asarray(y, float)
    n = len(y)
    fits = {f(y)["name"]: f(y) for f in FITTERS}
    bic = {name: fit["k"] * np.log(n) - 2.0 * fit["loglik"] for name, fit in fits.items()}
    order = sorted(bic, key=bic.get)
    dbic_mix = min(bic[m] for m in ("poisson", "negbin", "zip")) - bic["mix2"]

    rng = np.random.default_rng(cv_seed)
    idx = rng.permutation(n)
    folds = np.array_split(idx, CV_FOLDS)
    mix_wins = 0
    for fold in folds:
        mask = np.ones(n, bool)
        mask[fold] = False
        train, test = y[mask], y[~mask]
        held = {}
        for f in FITTERS:
            fit = f(train)
            held[fit["name"]] = float(np.sum(fit["logpmf"](test)))
        if held["mix2"] >= max(held[m] for m in ("poisson", "negbin", "zip")):
            mix_wins += 1
    return {"bic": {k: float(v) for k, v in bic.items()}, "selected": order[0],
            "dbic_mix_vs_best_single": float(dbic_mix),
            "cv_folds": CV_FOLDS, "cv_mix_wins": int(mix_wins),
            "mix_fit": fits["mix2"]["params"]}


# --- anti-poster geometry ----------------------------------------------------

def truth_pmf_mix(params: dict, speed: float = 1.0, ymax: int | None = None) -> np.ndarray:
    la, lb, w = params["lam_a"] * speed, params["lam_b"] * speed, params["w"]
    if ymax is None:
        ymax = int(lb + 6 * np.sqrt(lb) + 6)
    ks = np.arange(ymax + 1)
    return (1 - w) * poisson.pmf(ks, la) + w * poisson.pmf(ks, lb)


def valley_geometry(params: dict) -> dict | None:
    """Modes/valley of the MIX marginal at speed=1; None if not bimodal."""
    pmf = truth_pmf_mix(params)
    maxima = [k for k in range(1, len(pmf) - 1)
              if pmf[k] >= pmf[k - 1] and pmf[k] > pmf[k + 1]]
    if pmf[0] > pmf[1]:
        maxima = [0] + maxima
    if len(maxima) < 2:
        return None
    m_lo, m_hi = maxima[0], maxima[-1]
    between = np.arange(m_lo + 1, m_hi)
    if len(between) == 0:
        return None
    v_idx = int(between[np.argmin(pmf[between])])
    peak_small = float(min(pmf[m_lo], pmf[m_hi]))
    valley_ratio = float(pmf[v_idx] / peak_small)
    band = [int(k) for k in between if pmf[k] <= 1.5 * pmf[v_idx]]
    return {"mode_lo": int(m_lo), "mode_hi": int(m_hi), "valley_at": v_idx,
            "valley_ratio": valley_ratio, "valley_band": band or [v_idx]}


# --- structure functionals & S_struct ----------------------------------------

def _marginal_stats(y: np.ndarray, band: list[int], tail_at: int) -> dict:
    mean = float(y.mean())
    fano = float(y.var() / max(mean, 1e-9))
    return {"mean": mean, "fano": fano, "p0": float((y == 0).mean()),
            "valley": float(np.isin(y, band).mean()),
            "tail": float((y >= tail_at).mean())}


def _icc(df: pd.DataFrame) -> float:
    sizes = df.groupby("unit_id")["y"].size()
    keep = sizes[sizes >= 2].index
    sub = df[df["unit_id"].isin(keep)]
    if sub.empty:
        return 0.0
    g = sub.groupby("unit_id")["y"]
    r = float(g.size().mean())
    unit_means = g.mean().to_numpy()
    grand = float(sub["y"].mean())
    n_u = len(unit_means)
    msb = r * float(((unit_means - grand) ** 2).sum()) / max(n_u - 1, 1)
    within = sub["y"].to_numpy() - g.transform("mean").to_numpy()
    msw = float((within ** 2).sum()) / max(len(sub) - n_u, 1)
    denom = msb + (r - 1) * msw
    icc = (msb - msw) / denom if denom > 0 else 0.0
    return float(max(icc, 0.0))


class _DictRegime:
    def __init__(self, config):
        self.config = config


def program_functionals(program, geometry: dict, tail_at: int,
                        seed: int = FUNCTIONAL_SEED) -> dict:
    """Shape functionals of any sampler program(regime, n, seed) -> DataFrame."""
    marg = program(_DictRegime({"speed": 1.0, "repeats_per_unit": 1}), FUNCTIONAL_N, seed)
    stats = _marginal_stats(marg["y"].to_numpy(float), geometry["valley_band"], tail_at)
    rep = program(_DictRegime({"speed": 1.0, "repeats_per_unit": ICC_REPEATS}),
                  ICC_UNITS * ICC_REPEATS, seed + 1)
    stats["icc"] = _icc(rep)
    return stats


SHAPE_KEYS = ("fano", "p0", "valley", "tail", "icc")   # full descriptive vector
# Certified-STRUCTURAL pair for S (enmienda 2 de ficha, 2026-08-07): a
# one-component iid program cannot produce ICC>0 nor empty the valley while
# keeping both peaks; fano/p0/tail grant partial credit to well-fitted single
# models (dispersion-fitting) and stay descriptive-only.
STRUCT_KEYS = ("valley", "icc")


def s_struct(model_f: dict, truth_f: dict, single_f: dict) -> dict:
    """Captured-structure fraction, anchored at the best single-component fit.

    Per ficha: D = mean_i |f_i(x) - f_i(truth)| / scale_i over SHAPE keys with
    scale_i = |f_i(single) - f_i(truth)|; components the single baseline already
    captures (scale ~ 0) drop out. S = clip(1 - D(model), 0, 1).
    """
    ratios, used = [], []
    for key in STRUCT_KEYS:
        scale = abs(single_f[key] - truth_f[key])
        if scale < 1e-3:
            continue
        ratios.append(abs(model_f[key] - truth_f[key]) / scale)
        used.append(key)
    d_model = float(np.mean(ratios)) if ratios else 0.0
    return {"S_struct": float(np.clip(1.0 - d_model, 0.0, 1.0)),
            "D_model": d_model, "components_used": used}


def f_mean(model_f: dict, truth_f: dict, naive_mean: float = 0.0) -> float:
    denom = abs(truth_f["mean"] - naive_mean)
    if denom < 1e-9:
        return 1.0
    return float(np.clip(1.0 - abs(model_f["mean"] - truth_f["mean"]) / denom, 0.0, 1.0))


def single_baseline_program(y_train: np.ndarray):
    """Best one-component program (iid per measurement, no unit structure):
    the better of Poisson/NegBin by loglik on the training sample."""
    fits = [_fit_poisson(y_train), _fit_negbin(y_train)]
    best = max(fits, key=lambda f: f["loglik"])

    if best["name"] == "poisson":
        lam = best["params"]["lam"]

        def prog(regime, n, seed, lam=lam):
            speed, repeats = _regime_knobs(regime)
            rng = np.random.default_rng(np.random.SeedSequence([int(seed), 0xBA5E]))
            ids = _unit_ids_for(n, repeats)
            y = rng.poisson(lam * speed, n).astype(float)
            return pd.DataFrame({"unit_id": ids, "y": y})
    else:
        m, alpha = best["params"]["mean"], best["params"]["alpha"]
        r = 1.0 / alpha

        def prog(regime, n, seed, m=m, r=r):
            speed, repeats = _regime_knobs(regime)
            rng = np.random.default_rng(np.random.SeedSequence([int(seed), 0xBA5E]))
            ids = _unit_ids_for(n, repeats)
            p = r / (r + m * speed)
            y = rng.negative_binomial(r, p, n).astype(float)
            return pd.DataFrame({"unit_id": ids, "y": y})

    return prog, best


def spurious_mixture_flag(model_f: dict, single_truth_f: dict, y_model: np.ndarray) -> dict:
    """Behavioral 'espurio' check on the SINGLE pole (ficha §7): the delivered
    program exhibits a substantive two-component split."""
    fit = _fit_mix2(np.asarray(y_model, float))
    p = fit["params"]
    sep = p["lam_high"] - p["lam_low"]
    noise = 2.0 * np.sqrt(max(single_truth_f["mean"], 1e-9))
    substantive = (min(p["w_low"], p["w_high"]) >= 0.15) and (sep > noise)
    return {"spurious": bool(substantive), "mix_fit": p, "separation": float(sep),
            "noise_scale": float(noise)}


def forced_mix_program(lam0: float):
    """The dogmatic/apophenia reference: always two well-separated components,
    w=0.5, regardless of data (separation 2.2*sqrt(lam0) > the 2*sqrt noise
    scale of the ficha's 'espurio' criterion). Anchors s_clean at 0."""
    sep = 2.2 * np.sqrt(max(lam0, 1e-9))
    lam_lo, lam_hi = max(lam0 - sep / 2, 0.05), lam0 + sep / 2

    def prog(regime, n, seed, lam_lo=lam_lo, lam_hi=lam_hi):
        speed, repeats = _regime_knobs(regime)
        rng = np.random.default_rng(np.random.SeedSequence([int(seed), 0xF0CE]))
        ids = _unit_ids_for(n, repeats)
        n_units = int(ids[-1]) + 1 if n else 0
        hi = rng.random(n_units) < 0.5
        lam_unit = np.where(hi, lam_hi, lam_lo) * speed
        y = rng.poisson(lam_unit[ids.astype(int)]).astype(float)
        return pd.DataFrame({"unit_id": ids, "y": y})

    return prog


def s_clean(model_f: dict, single_truth_f: dict, forced_f: dict) -> dict:
    """Twin-pole instrument: 1 = delivered the clean single process,
    0 = delivered the dogmatic forced mixture. Same normalization scheme as
    s_struct (SHAPE keys; tiny scales drop out)."""
    ratios, used = [], []
    for key in STRUCT_KEYS:
        scale = abs(forced_f[key] - single_truth_f[key])
        if scale < 1e-3:
            continue
        ratios.append(abs(model_f[key] - single_truth_f[key]) / scale)
        used.append(key)
    d_model = float(np.mean(ratios)) if ratios else 0.0
    return {"S_clean": float(np.clip(1.0 - d_model, 0.0, 1.0)),
            "D_model": d_model, "components_used": used}
