"""Build and certify Grupos escondidos — Particulas bajo una sonda.

The certification asks whether a legal sequence of one-orientation scans can recover two response
types, while every isolated orientation remains one broad population and a strong arbitrary
one-band rival still loses on fresh complete curves.

Run:
    .venv/bin/python cases/hidden_probe_types_v0/build_and_certify.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from types import SimpleNamespace

import numpy as np
import pandas as pd
from scipy.optimize import minimize_scalar, nnls
from scipy.stats import norm
from sklearn.mixture import GaussianMixture

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
CASE = Path(__file__).parent
sys.path.insert(0, str(CASE))

import world  # noqa: E402

from wager.contracts import Battery, BatteryItem, CaseMeta, Regime  # noqa: E402
from wager.factory.case_loader import make_sample_transform  # noqa: E402
from wager.reward.scorer import WorldSide, score_callable  # noqa: E402
from wager.reward.trajectory import pivot_trajectories  # noqa: E402


BATTERY_SEEDS = tuple(range(2026081451, 2026081456))
LAB_INSTANCE_KEYS = tuple(range(410, 415))
LAB_GRID = (0.0, np.pi / 2.0, np.pi, 3.0 * np.pi / 2.0)
FIT_RANDOM_STATE = 20260814

MAX_ISOLATED_DBIC = 10.0
MIN_LEGAL_DBIC = 10.0
MAX_ONE_BAND_S = 0.55
MIN_LEGAL_TWO_TYPE_S = 0.85
MIN_LEGAL_PRODUCTION_R = 0.80
MIN_RAW_HEADROOM = 0.05

CDF_GRID_N = 1801
ENDPOINT_N = 181
MODE_N = 101
SUM_CONSTRAINT_WEIGHT = 100.0
WEIGHT_FLOOR = 1e-7


def _ns(*, config=None, context=None):
    return SimpleNamespace(config=config or {}, context=context or {}, horizon=None)


def _projection(grid) -> np.ndarray:
    theta = np.asarray(tuple(grid), dtype=float)
    direction = np.cos(theta - world.PHASE)
    return direction / np.linalg.norm(direction)


def _truth_projection_cdf(x: np.ndarray) -> np.ndarray:
    grid = np.asarray(world.SCORE_GRID)
    mean = world.TYPE_AMPLITUDE * np.linalg.norm(np.cos(grid - world.PHASE))
    sd = world.READING_SD
    return 0.5 * norm.cdf(x, -mean, sd) + 0.5 * norm.cdf(x, mean, sd)


def _projection_grid() -> tuple[np.ndarray, np.ndarray]:
    grid = np.asarray(world.SCORE_GRID)
    mean = world.TYPE_AMPLITUDE * np.linalg.norm(np.cos(grid - world.PHASE))
    limit = mean + 8.0 * world.READING_SD
    x = np.linspace(-limit, limit, CDF_GRID_N)
    return x, _truth_projection_cdf(x)


def _cdf_regret(x: np.ndarray, truth_cdf: np.ndarray, candidate_cdf: np.ndarray) -> float:
    return float(np.trapezoid((candidate_cdf - truth_cdf) ** 2, x))


def _best_gaussian(x: np.ndarray, truth_cdf: np.ndarray) -> dict:
    fit = minimize_scalar(
        lambda log_sd: _cdf_regret(x, truth_cdf, norm.cdf(x, 0.0, np.exp(log_sd))),
        bounds=(-4.0, 3.0), method="bounded", options={"xatol": 1e-12},
    )
    return {"sd": float(np.exp(fit.x)), "regret": float(fit.fun)}


def _uniform_cdf_basis(x: np.ndarray, mode: float, endpoints: np.ndarray) -> np.ndarray:
    basis = np.empty((x.size, endpoints.size), dtype=float)
    for j, endpoint in enumerate(endpoints):
        if abs(endpoint - mode) < 1e-12:
            basis[:, j] = (x >= mode).astype(float)
        elif endpoint > mode:
            basis[:, j] = np.clip((x - mode) / (endpoint - mode), 0.0, 1.0)
        else:
            basis[:, j] = np.clip((endpoint - x) / (endpoint - mode), 0.0, 1.0)
    return basis


def best_unimodal_oracle(x: np.ndarray, truth_cdf: np.ndarray) -> dict:
    """Dense Khintchine-mixture oracle over arbitrary one-band projected laws."""
    endpoints = np.linspace(float(x[0]), float(x[-1]), ENDPOINT_N)
    modes = np.linspace(float(x[0]), float(x[-1]), MODE_N)
    dx = float(x[1] - x[0])
    target = np.r_[truth_cdf * np.sqrt(dx), SUM_CONSTRAINT_WEIGHT]
    best = None
    for mode in modes:
        basis = _uniform_cdf_basis(x, float(mode), endpoints)
        design = np.vstack([
            basis * np.sqrt(dx),
            np.full((1, endpoints.size), SUM_CONSTRAINT_WEIGHT),
        ])
        weights, _ = nnls(design, target, maxiter=10000)
        weights /= weights.sum()
        regret = _cdf_regret(x, truth_cdf, basis @ weights)
        if best is None or regret < best[0]:
            best = (regret, float(mode), weights)
    assert best is not None
    _, mode, weights = best
    keep = weights > WEIGHT_FLOOR
    kept_weights = weights[keep]
    kept_weights /= kept_weights.sum()
    kept_endpoints = endpoints[keep]
    cdf = _uniform_cdf_basis(x, mode, kept_endpoints) @ kept_weights
    return {
        "mode": mode,
        "endpoints": kept_endpoints.tolist(),
        "weights": kept_weights.tolist(),
        "regret": _cdf_regret(x, truth_cdf, cdf),
        "class": "arbitrary unimodal law on the structural curve contrast",
        "grid": {"x_n": CDF_GRID_N, "endpoint_n": ENDPOINT_N, "mode_n": MODE_N},
    }


def _fit_gmm(values: np.ndarray, components: int, covariance_type: str) -> GaussianMixture:
    return GaussianMixture(
        n_components=components,
        covariance_type=covariance_type,
        n_init=30,
        max_iter=1000,
        reg_covar=1e-6,
        random_state=FIT_RANDOM_STATE,
    ).fit(values)


def _lab_panel(instance_key: int) -> tuple[np.ndarray, np.ndarray]:
    columns = []
    ids = None
    for call_index, theta in enumerate(LAB_GRID, start=1):
        seed = 800_000 + instance_key * 100_000 + call_index
        frame = world.sample(
            _ns(context={"panel": "calibration", "t_grid": (float(theta),)}),
            world.LAB_N,
            seed,
        ).sort_values("unit_id")
        if ids is None:
            ids = frame["unit_id"].to_numpy(float)
        else:
            assert np.array_equal(ids, frame["unit_id"].to_numpy(float))
        columns.append(frame["y"].to_numpy(float))
    assert ids is not None
    return np.column_stack(columns), np.asarray(LAB_GRID, dtype=float)


def _harmonic_coefficients(panel: np.ndarray, theta: np.ndarray) -> tuple[np.ndarray, float]:
    design = np.column_stack([np.ones(theta.size), np.cos(theta), np.sin(theta)])
    coefficients = np.linalg.lstsq(design, panel.T, rcond=None)[0].T
    residual = panel - coefficients @ design.T
    dof = panel.shape[0] * max(theta.size - design.shape[1], 1)
    residual_sd = float(np.sqrt(np.sum(residual**2) / dof))
    return coefficients, residual_sd


def fit_legal_two_type(instance_key: int) -> tuple[dict, dict]:
    panel, theta = _lab_panel(instance_key)
    coefficients, residual_sd = _harmonic_coefficients(panel, theta)
    one = _fit_gmm(coefficients, 1, "full")
    two = _fit_gmm(coefficients, 2, "tied")
    delta_bic = float(one.bic(coefficients) - two.bic(coefficients))

    labels = two.predict(coefficients)
    means = np.vstack([coefficients[labels == j].mean(axis=0) for j in range(2)])
    weights = np.asarray([(labels == j).mean() for j in range(2)], dtype=float)
    centered = np.vstack([
        coefficients[labels == j] - means[j] for j in range(2) if np.any(labels == j)
    ])
    covariance = centered.T @ centered / max(len(coefficients) - 2, 1)
    design = np.column_stack([np.ones(theta.size), np.cos(theta), np.sin(theta)])
    covariance -= residual_sd**2 * np.linalg.inv(design.T @ design)
    eigenvalues, eigenvectors = np.linalg.eigh((covariance + covariance.T) / 2.0)
    covariance = eigenvectors @ np.diag(np.maximum(eigenvalues, 1e-5)) @ eigenvectors.T

    fit = {
        "weights": weights,
        "means": means,
        "covariance": covariance,
        "residual_sd": residual_sd,
    }
    audit = {
        "instance_key": instance_key,
        "legal_scan_orientations": [float(v) for v in theta],
        "delta_BIC_two_tied_minus_one_full": delta_bic,
        "weights": weights.tolist(),
        "residual_sd": residual_sd,
    }
    return fit, audit


def fitted_sampler(fit: dict):
    weights = np.asarray(fit["weights"], dtype=float)
    means = np.asarray(fit["means"], dtype=float)
    covariance = np.asarray(fit["covariance"], dtype=float)
    residual_sd = float(fit["residual_sd"])
    chol = np.linalg.cholesky(covariance)

    def sample(regime, n: int, seed: int) -> pd.DataFrame:
        theta = np.asarray(tuple(regime.context["t_grid"]), dtype=float)
        rng = np.random.default_rng(seed)
        component = rng.choice(len(weights), size=n, p=weights)
        coefficients = means[component] + rng.normal(size=(n, 3)) @ chol.T
        y = (
            coefficients[:, [0]]
            + coefficients[:, [1]] * np.cos(theta)[None, :]
            + coefficients[:, [2]] * np.sin(theta)[None, :]
            + rng.normal(0.0, residual_sd, size=(n, theta.size))
        )
        return pd.DataFrame({
            "unit_id": np.repeat(np.arange(n, dtype=float), theta.size),
            "t": np.tile(theta, n),
            "y": y.ravel(),
        })

    return sample


def _decomposed_sampler(draw_projection):
    """Keep every direction except the structural one equal to the truth."""
    def sample(regime, n: int, seed: int) -> pd.DataFrame:
        theta = np.asarray(tuple(regime.context["t_grid"]), dtype=float)
        direction = np.cos(theta - world.PHASE)
        direction /= np.linalg.norm(direction)
        sine = np.sin(theta - world.PHASE)
        rng = np.random.default_rng(seed)
        level = rng.normal(0.0, world.LEVEL_SD, n)
        orthogonal = rng.normal(0.0, world.ORTHOGONAL_SD, n)
        residual = rng.normal(0.0, world.READING_SD, size=(n, theta.size))
        residual -= np.outer(residual @ direction, direction)
        projected = draw_projection(rng, n)
        y = (
            level[:, None]
            + orthogonal[:, None] * sine[None, :]
            + projected[:, None] * direction[None, :]
            + residual
        )
        return pd.DataFrame({
            "unit_id": np.repeat(np.arange(n, dtype=float), theta.size),
            "t": np.tile(theta, n),
            "y": y.ravel(),
        })
    return sample


def oracle_sampler(oracle: dict):
    endpoints = np.asarray(oracle["endpoints"], dtype=float)
    weights = np.asarray(oracle["weights"], dtype=float)
    mode = float(oracle["mode"])

    def draw(rng, n):
        component = rng.choice(len(weights), size=n, p=weights)
        other = endpoints[component]
        lo = np.minimum(other, mode)
        hi = np.maximum(other, mode)
        return lo + rng.random(n) * (hi - lo)

    return _decomposed_sampler(draw)


def gaussian_sampler(sd: float):
    return _decomposed_sampler(lambda rng, n: rng.normal(0.0, sd, n))


def null_sampler(regime, n: int, seed: int) -> pd.DataFrame:
    theta = np.asarray(tuple(regime.context["t_grid"]), dtype=float)
    cosine, sine = world._basis(theta)
    marginal_sd = np.sqrt(
        world.LEVEL_SD**2
        + world.TYPE_AMPLITUDE**2 * cosine**2
        + world.ORTHOGONAL_SD**2 * sine**2
        + world.READING_SD**2
    )
    rng = np.random.default_rng(seed)
    y = rng.normal(0.0, marginal_sd[None, :], size=(n, theta.size))
    return pd.DataFrame({
        "unit_id": np.repeat(np.arange(n, dtype=float), theta.size),
        "t": np.tile(theta, n),
        "y": y.ravel(),
    })


def _profile_score(sample_fn, x: np.ndarray, truth_cdf: np.ndarray, gaussian_regret: float) -> float:
    ns = _ns(context={"t_grid": world.SCORE_GRID})
    frame = sample_fn(ns, 30_000, 2026081490)
    wide = pivot_trajectories(frame, world.SCORE_GRID)
    projected = wide.to_numpy(float) @ _projection(world.SCORE_GRID)
    ordered = np.sort(projected)
    candidate_cdf = np.searchsorted(ordered, x, side="right") / len(ordered)
    regret = _cdf_regret(x, truth_cdf, candidate_cdf)
    return float(1.0 - regret / gaussian_regret)


def build_battery() -> Battery:
    return Battery(items=[
        BatteryItem(
            weight=1.0 / len(BATTERY_SEEDS),
            regime=Regime(context={"t_grid": world.SCORE_GRID}),
            seed_world=seed,
        )
        for seed in BATTERY_SEEDS
    ])


def _fixture_code(kind: str, *, gaussian_sd=None, oracle=None) -> str:
    common = f'''import numpy as np
import pandas as pd

PHASE = {world.PHASE!r}
LEVEL_SD = {world.LEVEL_SD!r}
ORTHOGONAL_SD = {world.ORTHOGONAL_SD!r}
READING_SD = {world.READING_SD!r}
'''
    if kind == "gaussian":
        draw = f'''GAUSSIAN_SD = {float(gaussian_sd)!r}

def draw_projection(rng, n):
    return rng.normal(0.0, GAUSSIAN_SD, n)
'''
    elif kind == "oracle":
        draw = f'''MODE = {float(oracle["mode"])!r}
ENDPOINTS = np.array({oracle["endpoints"]!r}, dtype=float)
WEIGHTS = np.array({oracle["weights"]!r}, dtype=float)

def draw_projection(rng, n):
    component = rng.choice(len(WEIGHTS), size=n, p=WEIGHTS)
    other = ENDPOINTS[component]
    lo = np.minimum(other, MODE)
    hi = np.maximum(other, MODE)
    return lo + rng.random(n) * (hi - lo)
'''
    elif kind == "null":
        return common + f'''TYPE_AMPLITUDE = {world.TYPE_AMPLITUDE!r}

def model(regime, n, seed):
    theta = np.asarray(tuple(regime.context["t_grid"]), dtype=float)
    cosine = np.cos(theta - PHASE)
    sine = np.sin(theta - PHASE)
    sd = np.sqrt(LEVEL_SD**2 + TYPE_AMPLITUDE**2 * cosine**2
                 + ORTHOGONAL_SD**2 * sine**2 + READING_SD**2)
    rng = np.random.default_rng(seed)
    y = rng.normal(0.0, sd[None, :], size=(n, theta.size))
    return pd.DataFrame({{"unit_id": np.repeat(np.arange(n, dtype=float), theta.size),
                         "t": np.tile(theta, n), "y": y.ravel()}})
'''
    else:
        raise ValueError(kind)

    return common + draw + '''

def model(regime, n, seed):
    theta = np.asarray(tuple(regime.context["t_grid"]), dtype=float)
    direction = np.cos(theta - PHASE)
    direction = direction / np.linalg.norm(direction)
    sine = np.sin(theta - PHASE)
    rng = np.random.default_rng(seed)
    level = rng.normal(0.0, LEVEL_SD, n)
    orthogonal = rng.normal(0.0, ORTHOGONAL_SD, n)
    residual = rng.normal(0.0, READING_SD, size=(n, theta.size))
    residual = residual - np.outer(residual @ direction, direction)
    projected = draw_projection(rng, n)
    y = (level[:, None] + orthogonal[:, None] * sine[None, :]
         + projected[:, None] * direction[None, :] + residual)
    return pd.DataFrame({"unit_id": np.repeat(np.arange(n, dtype=float), theta.size),
                         "t": np.tile(theta, n), "y": y.ravel()})
'''


def write_fixtures(gaussian: dict, oracle: dict) -> None:
    ladder = CASE / "ladder"
    ladder.mkdir(exist_ok=True)
    (ladder / "rung_2_gaussian_band.py").write_text(
        _fixture_code("gaussian", gaussian_sd=gaussian["sd"]), encoding="utf-8"
    )
    (ladder / "rung_3_best_unimodal.py").write_text(
        _fixture_code("oracle", oracle=oracle), encoding="utf-8"
    )
    (ladder / "rung_4_null.py").write_text(
        _fixture_code("null"), encoding="utf-8"
    )


def main() -> int:
    meta = CaseMeta.from_json_file(CASE / "meta.json")
    x, truth_cdf = _projection_grid()
    gaussian = _best_gaussian(x, truth_cdf)
    oracle = best_unimodal_oracle(x, truth_cdf)
    oracle_s = float(1.0 - oracle["regret"] / gaussian["regret"])

    isolated = []
    for j, theta in enumerate(world.SCORE_GRID):
        frame = world.sample(_ns(context={"t_grid": (theta,)}), 500, 2026081400 + j)
        values = frame[["y"]].to_numpy(float)
        one = _fit_gmm(values, 1, "full")
        two = _fit_gmm(values, 2, "full")
        isolated.append(float(one.bic(values) - two.bic(values)))

    routine = world.sample(_ns(config={"__routine": 1.0}), 200, 2026081409)
    routine_unique = int(routine["unit_id"].nunique()) == len(routine)

    finite = []
    fitted_samplers = []
    for key in LAB_INSTANCE_KEYS:
        fit, audit = fit_legal_two_type(key)
        sampler = fitted_sampler(fit)
        audit["two_type_S"] = _profile_score(sampler, x, truth_cdf, gaussian["regret"])
        finite.append(audit)
        fitted_samplers.append(sampler)

    battery = build_battery()
    battery.to_json_file(CASE / "battery.json")
    oracle_fn = oracle_sampler(oracle)
    gaussian_fn = gaussian_sampler(gaussian["sd"])
    transform = make_sample_transform(meta)
    ws = WorldSide(
        world.sample, battery, meta.column_names, meta.scoring.n_samples,
        null_sample=null_sampler, functionals=meta.stakes.functionals,
        c_f=meta.scoring.c_f, sample_transform=transform,
    )
    s_truth = score_callable(world.sample, ws, meta.scoring)
    s_oracle = score_callable(oracle_fn, ws, meta.scoring)
    s_gaussian = score_callable(gaussian_fn, ws, meta.scoring)
    s_null = score_callable(null_sampler, ws, meta.scoring)
    denominator = s_truth - s_oracle
    production_r = [
        float((score_callable(fn, ws, meta.scoring) - s_oracle) / denominator)
        for fn in fitted_samplers
    ]

    gates = {
        "isolated_orientations_not_split": max(isolated) <= MAX_ISOLATED_DBIC,
        "routine_has_no_repeated_ids": routine_unique,
        "legal_scan_split_visible": min(
            row["delta_BIC_two_tied_minus_one_full"] for row in finite
        ) >= MIN_LEGAL_DBIC,
        "best_one_band_below_frontier": oracle_s <= MAX_ONE_BAND_S,
        "legal_two_type_above_frontier": min(row["two_type_S"] for row in finite) >= MIN_LEGAL_TWO_TYPE_S,
        "production_headroom_material": denominator >= MIN_RAW_HEADROOM,
        "production_legal_recoverability": min(production_r) >= MIN_LEGAL_PRODUCTION_R,
        "anchor_order": s_truth > s_oracle > s_null,
    }
    gates["all"] = all(gates.values())

    report = {
        "experiment": "Grupos escondidos — Particulas bajo una sonda",
        "experiment_id": "exp__grupos-escondidos__sondas-persistentes__v1",
        "status": "mechanical certification; no agent episode yet",
        "world": {
            "lab_particles": world.LAB_N,
            "type_amplitude": world.TYPE_AMPLITUDE,
            "level_sd": world.LEVEL_SD,
            "orthogonal_sd": world.ORTHOGONAL_SD,
            "reading_sd": world.READING_SD,
            "phase": world.PHASE,
            "legal_scan_orientations": [float(v) for v in LAB_GRID],
        },
        "isolated_delta_BIC_two_minus_one": isolated,
        "best_one_band": {**oracle, "S_profile": oracle_s},
        "optimized_gaussian": gaussian,
        "finite_legal_solvers": finite,
        "production": {
            "raw_scores": {
                "truth": s_truth,
                "best_one_band": s_oracle,
                "gaussian_band": s_gaussian,
                "null": s_null,
            },
            "truth_minus_best_one_band": denominator,
            "legal_two_type_R": production_r,
        },
        "gates": gates,
        "frozen_seeds": {
            "battery": list(BATTERY_SEEDS),
            "legal_lab_instances": list(LAB_INSTANCE_KEYS),
        },
        "limits": [
            "The one-band oracle is exhaustive on the declared structural projection, not every multivariate topology.",
            "This v0 proves sequential intervention with persistent training IDs; it does not yet prove a long investigation.",
            "Agent resolvability remains untested until fresh idea-named episodes pass a frozen gate.",
        ],
    }
    write_fixtures(gaussian, oracle)
    (CASE / "certificates.json").write_text(
        json.dumps(report, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(report, indent=2))
    return 0 if gates["all"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
