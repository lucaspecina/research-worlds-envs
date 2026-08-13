"""Build and certify Grupos escondidos — Perfiles persistentes.

This is a finite-data kill test, not a truth-vs-toy demonstration. It checks that:

* every isolated test is analytically one-peaked;
* 400 legally purchasable complete profiles reveal a joint split;
* a two-profile model fitted only to those rows predicts fresh profiles well;
* the best arbitrary one-band distribution on the structural contrast still loses;
* the production zero-LLM score preserves that headroom.

Run:
    .venv/bin/python cases/hidden_profiles_v0/build_and_certify.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from types import SimpleNamespace

import numpy as np
from scipy.optimize import minimize_scalar, nnls
from scipy.stats import norm
from sklearn.mixture import GaussianMixture

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
CASE = Path(__file__).parent
sys.path.insert(0, str(CASE))

import world  # noqa: E402

from wager.contracts import Battery, BatteryItem, CaseMeta, Regime  # noqa: E402
from wager.reward.scorer import WorldSide, score_callable  # noqa: E402


TRAIN_N = 400
TRAIN_SEEDS = tuple(range(2026081301, 2026081306))
BATTERY_SEEDS = tuple(range(2026081351, 2026081356))
FIT_RANDOM_STATE = 20260813

# Frozen before agent calls. Positive ΔBIC means the split model wins.
MAX_ISOLATED_DBIC = 10.0
MIN_JOINT_DBIC = 50.0
MIN_LEGAL_DIRECTION_COSINE = 0.95
MAX_ONE_BAND_S = 0.50
MIN_FINITE_TWO_PROFILE_S = 0.90
MIN_PROFILE_GAP = 0.20
MIN_PRODUCTION_R = 0.80

GRID_N = 2401
ENDPOINT_N = 241
MODE_N = 101
SUM_CONSTRAINT_WEIGHT = 100.0
WEIGHT_FLOOR = 1e-7


def _ns():
    return SimpleNamespace(config={}, context={}, horizon=None)


def _training(seed: int) -> np.ndarray:
    return world.sample(_ns(), TRAIN_N, seed)[world.COLUMNS].to_numpy(float)


def _truth_projection_cdf(x: np.ndarray) -> np.ndarray:
    m = world.TYPE_SIGNAL * np.sqrt(world.K) / world.RESIDUAL_SD
    return 0.5 * norm.cdf(x, -m, 1.0) + 0.5 * norm.cdf(x, m, 1.0)


def _projection_grid() -> tuple[np.ndarray, np.ndarray]:
    m = world.TYPE_SIGNAL * np.sqrt(world.K) / world.RESIDUAL_SD
    limit = m + 8.0
    x = np.linspace(-limit, limit, GRID_N)
    return x, _truth_projection_cdf(x)


def _cdf_regret(x: np.ndarray, truth_cdf: np.ndarray, candidate_cdf: np.ndarray) -> float:
    return float(np.trapezoid((candidate_cdf - truth_cdf) ** 2, x))


def _best_gaussian(x: np.ndarray, truth_cdf: np.ndarray) -> dict:
    fit = minimize_scalar(
        lambda log_sd: _cdf_regret(x, truth_cdf, norm.cdf(x, 0.0, np.exp(log_sd))),
        bounds=(-2.0, 5.0),
        method="bounded",
        options={"xatol": 1e-12},
    )
    return {"sd": float(np.exp(fit.x)), "regret": float(fit.fun)}


def _uniform_cdf_basis(x: np.ndarray, mode: float, endpoints: np.ndarray) -> np.ndarray:
    """CDFs of uniforms with one endpoint at `mode` (Khintchine basis)."""
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
    """Discretized oracle over all univariate unimodal laws.

    Khintchine's representation says any univariate density with mode c is a mixture of uniforms
    having c as one endpoint. We search c and the other endpoint on dense frozen grids and solve
    the mixture weights by non-negative least squares. The result is a conservative strong rival,
    not an agent-facing algorithm.
    """
    limit = float(max(abs(x[0]), abs(x[-1])))
    endpoints = np.linspace(-limit, limit, ENDPOINT_N)
    mode_limit = min(9.0, limit - 1.0)
    modes = np.linspace(-mode_limit, mode_limit, MODE_N)
    dx = float(x[1] - x[0])
    target = np.r_[truth_cdf * np.sqrt(dx), SUM_CONSTRAINT_WEIGHT]
    best: tuple[float, float, np.ndarray] | None = None
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
    regret, mode, weights = best
    keep = weights > WEIGHT_FLOOR
    kept_weights = weights[keep]
    kept_weights /= kept_weights.sum()
    kept_endpoints = endpoints[keep]
    # Report the pruned fixture's actual regret, not the denser optimization's number.
    pruned_cdf = _uniform_cdf_basis(x, mode, kept_endpoints) @ kept_weights
    return {
        "mode": mode,
        "endpoints": kept_endpoints.tolist(),
        "weights": kept_weights.tolist(),
        "regret": _cdf_regret(x, truth_cdf, pruned_cdf),
        "grid": {"x_n": GRID_N, "endpoint_n": ENDPOINT_N, "mode_n": MODE_N},
        "class": "arbitrary univariate unimodal distribution (Khintchine mixture oracle)",
    }


def _fit_gmm(y: np.ndarray, components: int, covariance_type: str) -> GaussianMixture:
    return GaussianMixture(
        n_components=components,
        covariance_type=covariance_type,
        n_init=20,
        max_iter=1000,
        reg_covar=1e-6,
        random_state=FIT_RANDOM_STATE,
    ).fit(y)


def _fitted_projection_cdf(gmm: GaussianMixture, x: np.ndarray) -> np.ndarray:
    direction = world.SIGNATURE / np.sqrt(world.K)
    means = (gmm.means_ @ direction) / world.RESIDUAL_SD
    if gmm.covariance_type == "tied":
        sd = float(np.sqrt(direction @ gmm.covariances_ @ direction) / world.RESIDUAL_SD)
        sds = np.full(gmm.n_components, sd)
    else:  # pragma: no cover - current finite solver is tied
        sds = np.asarray([
            np.sqrt(direction @ cov @ direction) / world.RESIDUAL_SD
            for cov in gmm.covariances_
        ])
    out = np.zeros_like(x)
    for weight, mean, component_sd in zip(gmm.weights_, means, sds):
        out += weight * norm.cdf(x, mean, component_sd)
    return out


def _gmm_sampler(gmm: GaussianMixture):
    means = np.asarray(gmm.means_, float)
    covariance = np.asarray(gmm.covariances_, float)
    chol = np.linalg.cholesky(covariance)
    weights = np.asarray(gmm.weights_, float)

    def sample(regime, n, seed):
        rng = np.random.default_rng(seed)
        component = rng.choice(len(weights), size=n, p=weights)
        values = means[component] + rng.normal(size=(n, world.K)) @ chol.T
        import pandas as pd

        return pd.DataFrame(values, columns=world.COLUMNS)

    return sample


def finite_data_checks(x: np.ndarray, truth_cdf: np.ndarray, gaussian_regret: float) -> list[dict]:
    direction_truth = world.SIGNATURE / np.sqrt(world.K)
    rows = []
    for seed in TRAIN_SEEDS:
        y = _training(seed)
        isolated_dbic = []
        for j in range(world.K):
            one = _fit_gmm(y[:, [j]], 1, "full")
            two = _fit_gmm(y[:, [j]], 2, "full")
            isolated_dbic.append(float(one.bic(y[:, [j]]) - two.bic(y[:, [j]])))

        one_joint = _fit_gmm(y, 1, "full")
        two_joint = _fit_gmm(y, 2, "tied")
        joint_dbic = float(one_joint.bic(y) - two_joint.bic(y))

        # Legal discovery direction: remove each specimen's overall level, then take the leading
        # sample covariance direction. Truth is used only after the fact to audit recovery.
        centered = y - y.mean(axis=1, keepdims=True)
        _, eigenvectors = np.linalg.eigh(np.cov(centered, rowvar=False))
        learned_direction = eigenvectors[:, -1]
        cosine = float(abs(learned_direction @ direction_truth))

        fitted_regret = _cdf_regret(
            x, truth_cdf, _fitted_projection_cdf(two_joint, x)
        )
        s_profile = float(np.clip(1.0 - fitted_regret / gaussian_regret, 0.0, 1.0))
        rows.append({
            "train_seed": seed,
            "max_isolated_dbic_two_minus_one": max(isolated_dbic),
            "joint_dbic_two_tied_minus_one_full": joint_dbic,
            "legal_direction_cosine_to_truth": cosine,
            "two_profile_weights": two_joint.weights_.tolist(),
            "two_profile_S": s_profile,
            "gmm": two_joint,
        })
    return rows


def _decomposed_profile_sample(t_sampler):
    """Match truth off the structural direction; let t_sampler choose only that direction."""
    direction = world.SIGNATURE / np.sqrt(world.K)

    def sample(regime, n, seed):
        import pandas as pd

        rng = np.random.default_rng(seed)
        t = np.asarray(t_sampler(rng, n), dtype=float)
        level = rng.normal(0.0, world.LEVEL_SD, size=(n, 1))
        residual = rng.normal(0.0, world.RESIDUAL_SD, size=(n, world.K))
        residual -= np.outer(residual @ direction, direction)
        values = level + world.RESIDUAL_SD * t[:, None] * direction[None, :] + residual
        return pd.DataFrame(values, columns=world.COLUMNS)

    return sample


def _oracle_sampler(oracle: dict):
    endpoints = np.asarray(oracle["endpoints"], float)
    weights = np.asarray(oracle["weights"], float)
    mode = float(oracle["mode"])

    def draw(rng, n):
        component = rng.choice(len(weights), size=n, p=weights)
        other = endpoints[component]
        lo = np.minimum(other, mode)
        hi = np.maximum(other, mode)
        return lo + rng.random(n) * (hi - lo)

    return _decomposed_profile_sample(draw)


def _gaussian_sampler(sd: float):
    return _decomposed_profile_sample(lambda rng, n: rng.normal(0.0, sd, size=n))


def _null_sampler(regime, n, seed):
    import pandas as pd

    rng = np.random.default_rng(seed)
    marginal_sd = np.sqrt(world.TYPE_SIGNAL**2 + world.LEVEL_SD**2 + world.RESIDUAL_SD**2)
    return pd.DataFrame(
        rng.normal(0.0, marginal_sd, size=(n, world.K)), columns=world.COLUMNS
    )


def _profile_code(kind: str, *, oracle: dict | None = None, gaussian_sd: float | None = None) -> str:
    signature = world.SIGNATURE.tolist()
    columns = repr(world.COLUMNS)
    common = f'''import numpy as np
import pandas as pd

COLUMNS = {columns}
SIGNATURE = np.array({signature!r}, dtype=float)
DIRECTION = SIGNATURE / np.sqrt(len(SIGNATURE))
RESIDUAL_SD = {world.RESIDUAL_SD!r}
LEVEL_SD = {world.LEVEL_SD!r}
'''
    if kind == "oracle":
        assert oracle is not None
        draw = f'''MODE = {oracle["mode"]!r}
ENDPOINTS = np.array({oracle["endpoints"]!r}, dtype=float)
WEIGHTS = np.array({oracle["weights"]!r}, dtype=float)


def draw_t(rng, n):
    component = rng.choice(len(WEIGHTS), size=n, p=WEIGHTS)
    other = ENDPOINTS[component]
    lo = np.minimum(other, MODE)
    hi = np.maximum(other, MODE)
    return lo + rng.random(n) * (hi - lo)
'''
    elif kind == "gaussian":
        assert gaussian_sd is not None
        draw = f'''GAUSSIAN_SD = {gaussian_sd!r}


def draw_t(rng, n):
    return rng.normal(0.0, GAUSSIAN_SD, size=n)
'''
    elif kind == "null":
        marginal_sd = np.sqrt(
            world.TYPE_SIGNAL**2 + world.LEVEL_SD**2 + world.RESIDUAL_SD**2
        )
        return common + f'''
MARGINAL_SD = {float(marginal_sd)!r}


def model(regime, n, seed):
    rng = np.random.default_rng(seed)
    return pd.DataFrame(rng.normal(0.0, MARGINAL_SD, size=(n, len(COLUMNS))), columns=COLUMNS)
'''
    else:  # pragma: no cover
        raise ValueError(kind)
    return common + draw + '''

def model(regime, n, seed):
    rng = np.random.default_rng(seed)
    t = draw_t(rng, n)
    level = rng.normal(0.0, LEVEL_SD, size=(n, 1))
    residual = rng.normal(0.0, RESIDUAL_SD, size=(n, len(COLUMNS)))
    residual = residual - np.outer(residual @ DIRECTION, DIRECTION)
    values = level + RESIDUAL_SD * t[:, None] * DIRECTION[None, :] + residual
    return pd.DataFrame(values, columns=COLUMNS)
'''


def build_battery() -> Battery:
    return Battery(items=[
        BatteryItem(weight=1.0 / len(BATTERY_SEEDS), regime=Regime(), seed_world=seed)
        for seed in BATTERY_SEEDS
    ])


def main() -> int:
    meta = CaseMeta.from_json_file(CASE / "meta.json")
    x, truth_cdf = _projection_grid()
    gaussian = _best_gaussian(x, truth_cdf)
    oracle = best_unimodal_oracle(x, truth_cdf)
    oracle_s = float(1.0 - oracle["regret"] / gaussian["regret"])
    finite = finite_data_checks(x, truth_cdf, gaussian["regret"])

    battery = build_battery()
    battery.to_json_file(CASE / "battery.json")
    oracle_fn = _oracle_sampler(oracle)
    gaussian_fn = _gaussian_sampler(gaussian["sd"])
    ws = WorldSide(
        world.sample,
        battery,
        meta.column_names,
        meta.scoring.n_samples,
        null_sample=_null_sampler,
        functionals=meta.stakes.functionals,
        c_f=meta.scoring.c_f,
    )
    production_scores = {
        "truth": score_callable(world.sample, ws, meta.scoring),
        "unimodal_oracle": score_callable(oracle_fn, ws, meta.scoring),
        "optimized_gaussian_band": score_callable(gaussian_fn, ws, meta.scoring),
        "null_independent_marginals": score_callable(_null_sampler, ws, meta.scoring),
    }
    # The mathematical oracle is mandatory. If the Gaussian happens to win under the secondary
    # full-profile term, use it as the production anchor instead; never choose the weaker rival.
    rival_name = max(
        ("unimodal_oracle", "optimized_gaussian_band"), key=production_scores.get
    )
    rival_fn = oracle_fn if rival_name == "unimodal_oracle" else gaussian_fn
    rival_code = (
        _profile_code("oracle", oracle=oracle)
        if rival_name == "unimodal_oracle"
        else _profile_code("gaussian", gaussian_sd=gaussian["sd"])
    )
    s_truth = production_scores["truth"]
    s_rival = production_scores[rival_name]
    denominator = s_truth - s_rival

    canonical_rows = []
    for row in finite:
        score = score_callable(_gmm_sampler(row.pop("gmm")), ws, meta.scoring)
        production_r = float((score - s_rival) / denominator)
        row["production_raw_score"] = score
        row["production_R_vs_best_one_band"] = production_r
        canonical_rows.append(row)

    ladder = CASE / "ladder"
    ladder.mkdir(exist_ok=True)
    (ladder / "rung_2_gaussian_band.py").write_text(
        _profile_code("gaussian", gaussian_sd=gaussian["sd"]), encoding="utf-8"
    )
    (ladder / "rung_3_best_unimodal.py").write_text(rival_code, encoding="utf-8")
    (ladder / "rung_4_null.py").write_text(_profile_code("null"), encoding="utf-8")

    max_isolated = max(row["max_isolated_dbic_two_minus_one"] for row in canonical_rows)
    min_joint = min(row["joint_dbic_two_tied_minus_one_full"] for row in canonical_rows)
    min_cosine = min(row["legal_direction_cosine_to_truth"] for row in canonical_rows)
    min_two_s = min(row["two_profile_S"] for row in canonical_rows)
    min_two_r = min(row["production_R_vs_best_one_band"] for row in canonical_rows)
    gates = {
        "isolated_tests_not_strongly_split": max_isolated < MAX_ISOLATED_DBIC,
        "joint_split_visible": min_joint >= MIN_JOINT_DBIC,
        "direction_recoverable_legally": min_cosine >= MIN_LEGAL_DIRECTION_COSINE,
        "best_one_band_below_half": oracle_s <= MAX_ONE_BAND_S,
        "finite_two_profile_above_90pct": min_two_s >= MIN_FINITE_TWO_PROFILE_S,
        "finite_gap_material": (min_two_s - oracle_s) >= MIN_PROFILE_GAP,
        "production_recoverability": min_two_r >= MIN_PRODUCTION_R,
        "production_headroom_positive": denominator > 0.0,
    }
    gates["all"] = all(gates.values())

    entropy_rng = np.random.default_rng(2026081399)
    m = world.TYPE_SIGNAL * np.sqrt(world.K) / world.RESIDUAL_SD
    entropy_x = entropy_rng.choice((-1.0, 1.0), 1_000_000) * m + entropy_rng.normal(
        size=1_000_000
    )
    entropy_y = entropy_rng.choice((-1.0, 1.0), 1_000_000) * m + entropy_rng.normal(
        size=1_000_000
    )
    truth_crps_entropy = float(0.5 * np.mean(np.abs(entropy_x - entropy_y)))

    report = {
        "experiment": "Grupos escondidos — Perfiles persistentes",
        "experiment_id": "exp__grupos-escondidos__perfiles-persistentes__v1",
        "status": "mathematical and finite-data certification; no agent episode yet",
        "world": {
            "conditions": world.K,
            "type_signal": world.TYPE_SIGNAL,
            "continuous_level_sd": world.LEVEL_SD,
            "residual_sd": world.RESIDUAL_SD,
            "isolated_signal_in_total_sd": world.TYPE_SIGNAL,
            "joint_signal_in_contrast_noise_sd": m,
            "train_panels_available": TRAIN_N,
        },
        "score": {
            "primary": "full-profile energy plus declared projected energy; zero-LLM",
            "S_profile_scale": "0=best optimized Gaussian band, 1=truth",
            "optimized_gaussian": gaussian,
            "best_unimodal_oracle": {
                "S_profile": oracle_s,
                "regret": oracle["regret"],
                "mode": oracle["mode"],
                "active_uniform_components": len(oracle["weights"]),
                "grid": oracle["grid"],
                "class": oracle["class"],
            },
            "truth_crps_entropy": truth_crps_entropy,
            "one_band_regret_fraction_of_truth_crps": oracle["regret"] / truth_crps_entropy,
        },
        "finite_data": canonical_rows,
        "production": {
            "raw_scores": production_scores,
            "best_one_band_anchor": rival_name,
            "truth_minus_best_one_band": denominator,
        },
        "gates": gates,
        "frozen_seeds": {
            "finite_training": TRAIN_SEEDS,
            "battery_world": BATTERY_SEEDS,
            "entropy_diagnostic": 2026081399,
        },
        "limits": [
            "The one-band oracle is exhaustive on the declared one-dimensional structural contrast, not over every conceivable multivariate topology.",
            "Agent resolvability is not certified until agents receive only the named idea and solve the playable task.",
            "No spontaneous-discovery claim is authorized by these factory calculations.",
        ],
    }
    (CASE / "certificates.json").write_text(
        json.dumps(report, indent=2, default=float) + "\n", encoding="utf-8"
    )
    print(json.dumps({
        "oracle_S": oracle_s,
        "finite_two_profile_S": [row["two_profile_S"] for row in canonical_rows],
        "finite_production_R": [
            row["production_R_vs_best_one_band"] for row in canonical_rows
        ],
        "production_anchor": rival_name,
        "gates": gates,
    }, indent=2))
    return 0 if gates["all"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
