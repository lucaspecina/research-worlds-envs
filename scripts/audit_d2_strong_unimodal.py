"""Audita D2 contra un rival unimodal asimétrico optimizado (ADR 0175).

El certificado D2 vigente llama "mejor rival sin el salto de dos grupos" a una
Gaussiana. Este control enfrenta la misma verdad y la misma grilla con una
skew-normal: una sola distribución unimodal que puede tener cola asimétrica. El ajuste minimiza
directamente el log-score esperado contra la mezcla verdadera mediante
cuadratura Gauss-Hermite, sin muestras de entrenamiento ni LLM.

No modifica artefactos. Imprime JSON reproducible:

    .venv/bin/python scripts/audit_d2_strong_unimodal.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from numpy.polynomial.hermite import hermgauss
from scipy.optimize import minimize
from scipy.stats import norm, skewnorm

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from cases import d1_calibracion_common as C  # noqa: E402
from cases import d2_decision_common as D2  # noqa: E402

QUAD_N = 64
SCORE_SEEDS = (4242, 4243, 4244, 4245, 4246)


def _d2_param(params: dict, key: str, fallback: float) -> float:
    value = params.get(key)
    return fallback if value is None else float(value)


def _params_at(theta: np.ndarray, T: float) -> tuple[float, float, float]:
    """loc, scale y shape skew-normal; los tres varían suavemente con T."""
    x = T - 1.0
    basis = np.asarray([1.0, x, x * x])
    loc = float(theta[0:3] @ basis)
    scale = float(np.exp(theta[3:6] @ basis))
    shape = float(theta[6:9] @ basis)
    return loc, scale, shape


def _truth_quadrature(params: dict, T: float) -> tuple[np.ndarray, np.ndarray]:
    """Nodos y pesos exactos de expectativa para la mezcla de dos Gaussianas."""
    nodes, weights = hermgauss(QUAD_N)
    weights = weights / np.sqrt(np.pi)
    base = params["mu0"] + params["beta"] * (T - 1.0)
    p = D2.pi_T(T, params)
    d_shift = _d2_param(params, "d_shift_d2", params["d_shift"])
    s_extra = _d2_param(params, "s_extra_d2", C.S_EXTRA)
    affected_sd = float(np.sqrt(C.SQ**2 + s_extra**2))
    clean_y = base + np.sqrt(2.0) * C.SQ * nodes
    affected_y = base - d_shift + np.sqrt(2.0) * affected_sd * nodes
    ys = np.concatenate([clean_y, affected_y])
    ws = np.concatenate([(1.0 - p) * weights, p * weights])
    return ys, ws


def _truth_logpdf(y: np.ndarray, params: dict, T: float) -> np.ndarray:
    base = params["mu0"] + params["beta"] * (T - 1.0)
    p = D2.pi_T(T, params)
    d_shift = _d2_param(params, "d_shift_d2", params["d_shift"])
    s_extra = _d2_param(params, "s_extra_d2", C.S_EXTRA)
    affected_sd = float(np.sqrt(C.SQ**2 + s_extra**2))
    a = np.log1p(-p) + norm.logpdf(y, loc=base, scale=C.SQ)
    b = np.log(p) + norm.logpdf(y, loc=base - d_shift, scale=affected_sd)
    return np.logaddexp(a, b)


def _expected_gaps(theta: np.ndarray, params: dict,
                   cm: np.ndarray, cs: np.ndarray) -> tuple[float, float]:
    """Nats perdidos por skew-normal y por el ancla Gaussiana actual."""
    skew_gap = gauss_gap = 0.0
    for T in D2.EXAM_GRID:
        y, w = _truth_quadrature(params, T)
        truth_lp = _truth_logpdf(y, params, T)
        loc, scale, shape = _params_at(theta, T)
        skew_gap += float(np.sum(w * (truth_lp - skewnorm.logpdf(
            y, shape, loc=loc, scale=scale))))
        x = T - 1.0
        basis = np.asarray([1.0, x, x * x])
        mu = float(cm @ basis)
        sd = float(np.exp(cs @ basis))
        gauss_gap += float(np.sum(w * (truth_lp - norm.logpdf(y, loc=mu, scale=sd))))
    n = len(D2.EXAM_GRID)
    return skew_gap / n, gauss_gap / n


def _fit(params: dict, cm: np.ndarray, cs: np.ndarray) -> tuple[np.ndarray, object]:
    def loss(theta: np.ndarray) -> float:
        gap, _ = _expected_gaps(theta, params, cm, cs)
        return gap

    mean0 = params["mu0"] - params["pi"] * params["d_shift"]
    starts = [
        [mean0, params["beta"] - params["pi_slope"] * params["d_shift"], 0.0,
         np.log(1.8), 0.0, 0.0, 0.0, 0.0, 0.0],
        [params["mu0"] + 0.4, params["beta"], 0.0,
         np.log(2.2), 0.0, 0.0, -3.0, -1.0, 0.0],
        [params["mu0"] + 0.8, params["beta"], 0.0,
         np.log(2.8), 0.0, 0.0, -6.0, -2.0, 0.0],
        [params["mu0"], params["beta"], 0.0,
         np.log(2.0), 0.0, 0.0, -10.0, 0.0, 0.0],
    ]
    bounds = [
        (80.0, 105.0), (-20.0, 20.0), (-20.0, 20.0),
        (np.log(0.2), np.log(8.0)), (-6.0, 6.0), (-6.0, 6.0),
        (-25.0, 25.0), (-25.0, 25.0), (-25.0, 25.0),
    ]
    best = None
    for start in starts:
        fit = minimize(loss, np.asarray(start), method="L-BFGS-B", bounds=bounds,
                       options={"maxiter": 2500, "ftol": 1e-12, "gtol": 1e-8})
        if best is None or fit.fun < best.fun:
            best = fit
    assert best is not None
    return np.asarray(best.x), best


def _program(theta: np.ndarray):
    def model(regime, n, seed):
        T = C._speed_T(regime)
        loc, scale, shape = _params_at(theta, T)
        rng = np.random.default_rng(seed)
        y = skewnorm.rvs(shape, loc=loc, scale=scale, size=int(n), random_state=rng)
        return pd.DataFrame({"unit_id": np.arange(int(n), dtype=float), "y": y})

    return model


def _gaussian_anchor(inst: dict):
    cm, cs = np.asarray(inst["ancla_cm"]), np.asarray(inst["ancla_cs"])

    def model(regime, n, seed):
        T = C._speed_T(regime)
        x = T - 1.0
        basis = np.asarray([1.0, x, x * x])
        mu = float(cm @ basis)
        sd = float(np.exp(cs @ basis))
        rng = np.random.default_rng(seed)
        y = rng.normal(mu, sd, int(n))
        return pd.DataFrame({"unit_id": np.arange(int(n), dtype=float), "y": y})

    return model


def main() -> int:
    inst = json.loads((ROOT / "cases/d2_proceso/instance.json").read_text())
    params = inst["params"]
    cm, cs = np.asarray(inst["ancla_cm"]), np.asarray(inst["ancla_cs"])
    theta, fit = _fit(params, cm, cs)
    exact_gap, current_gauss_gap = _expected_gaps(theta, params, cm, cs)
    model = _program(theta)

    production_scores = []
    anchor = _gaussian_anchor(inst)
    for seed in SCORE_SEEDS:
        score = D2.s_metric_log(model, "proceso", params, seed=seed, anchor_zero=anchor)
        production_scores.append({
            "seed": seed,
            "S": score["S"],
            "nats_model": score["nats_model"],
            "nats_anchor": score["nats_anchor"],
        })

    flag = C.structural_flag(model, params)
    payload = {
        "rival": "skew-normal unimodal; no discrete groups; quadratic loc/log-scale/shape in T",
        "optimizer_success": bool(fit.success),
        "optimizer_message": str(fit.message),
        "theta": [float(x) for x in theta],
        "exact": {
            "current_gaussian_gap_nats_per_lot": current_gauss_gap,
            "skew_normal_gap_nats_per_lot": exact_gap,
            "fraction_of_old_headroom_captured": 1.0 - exact_gap / current_gauss_gap,
        },
        "production_scorer": production_scores,
        "production_S_mean": float(np.mean([row["S"] for row in production_scores])),
        "production_S_range": [
            float(min(row["S"] for row in production_scores)),
            float(max(row["S"] for row in production_scores)),
        ],
        "production_nats_model_mean": float(np.mean(
            [row["nats_model"] for row in production_scores])),
        "production_nats_model_range": [
            float(min(row["nats_model"] for row in production_scores)),
            float(max(row["nats_model"] for row in production_scores)),
        ],
        "production_protocol": (
            "evaluation seeds vary truth/floor draws; candidate ensemble seed is fixed at 777"
        ),
        "current_gate": (
            "best rival without a discrete-group split must have S <= 0.5 "
            "and remaining gap >= 0.10 nats/lot"
        ),
        "structural_flag": flag,
    }
    print(json.dumps(payload, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
