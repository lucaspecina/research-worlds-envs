"""Test whether one untouched MIXED donor statistically identifies two laws.

Fitting uses only the donor's delivered ledger.  Truth is loaded only after all
candidate fits and model-selection quantities have been computed, and is used
solely for the already-declared local outcome metrics at North, H=5, G=3/7.

The candidates are deliberately nested:

* one affine Gaussian response law;
* two Gaussian residual modes around parallel affine response laws;
* two independent affine Gaussian response laws.

Mixture fits use data-driven starts (within-cell clustering plus random starts),
never the hidden 75/25 weight or hidden coefficients.  Five-fold stratified
held-out likelihood and BIC guard against declaring a recoverable mixture just
because the larger model can overfit the finite ledger.
"""

from __future__ import annotations

import argparse
import json
import math
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Literal

import numpy as np
from scipy.optimize import minimize
from scipy.special import expit, logsumexp
from scipy.stats import energy_distance

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from wager.contracts import Regime  # noqa: E402
from wager.harness.case_episode import build_world_server  # noqa: E402
from wager.reward.sandbox import SandboxedSubmission  # noqa: E402


MIXED_CASE = ROOT / "cases" / "first_story_scm_transfer_mixed_v0"
EXPECTED_MIXED_A3 = 6.0 / (7.0**1.5)
MAX_ALIGNMENT_STARTS = 32
Candidate = Literal["single_gaussian", "residual_mixture", "law_mixture"]


@dataclass(frozen=True)
class Dataset:
    grade: np.ndarray
    humidity: np.ndarray
    outcome: np.ndarray
    sequence: np.ndarray

    @property
    def x(self) -> np.ndarray:
        return np.column_stack(
            [np.ones(len(self.outcome)), self.grade, self.humidity]
        )

    def subset(self, indices: np.ndarray) -> Dataset:
        return Dataset(
            grade=self.grade[indices],
            humidity=self.humidity[indices],
            outcome=self.outcome[indices],
            sequence=self.sequence[indices],
        )


@dataclass(frozen=True)
class Fit:
    candidate: Candidate
    parameters: dict[str, Any]
    vector: np.ndarray
    log_likelihood: float
    n_parameters: int
    converged: bool
    starts_attempted: int
    starts_converged: int


def _extract_dataset(payload: dict[str, Any]) -> tuple[Dataset, dict[str, Any]]:
    branch = payload.get("branches", {}).get("mixed")
    if not isinstance(branch, dict):
        raise ValueError("raw has no branches.mixed")
    ledger = branch.get("evidence_ledger")
    if not isinstance(ledger, list):
        raise ValueError("mixed branch has no evidence_ledger")

    grades: list[float] = []
    humidities: list[float] = []
    outcomes: list[float] = []
    sequences: list[int] = []
    included_records: list[dict[str, Any]] = []
    for record in ledger:
        request = record.get("request") or {}
        context = request.get("context") or {}
        config = request.get("config") or {}
        if str(context.get("site", "")).lower() != "north":
            continue
        if not {"feedstock_grade", "humidity"}.issubset(config):
            continue
        data = record.get("data") or {}
        columns = list(data.get("columns") or [])
        rows = list(data.get("data") or [])
        if "outcome" not in columns:
            raise ValueError(f"record {record.get('sequence')} lacks outcome")
        outcome_index = columns.index("outcome")
        grade = float(config["feedstock_grade"])
        humidity = float(config["humidity"])
        sequence = int(record["sequence"])
        for row in rows:
            grades.append(grade)
            humidities.append(humidity)
            outcomes.append(float(row[outcome_index]))
            sequences.append(sequence)
        included_records.append(
            {
                "sequence": sequence,
                "grade": grade,
                "humidity": humidity,
                "rows": len(rows),
            }
        )
    if len(outcomes) < 40:
        raise ValueError("fewer than 40 fully controlled North rows")
    dataset = Dataset(
        grade=np.asarray(grades, dtype=float),
        humidity=np.asarray(humidities, dtype=float),
        outcome=np.asarray(outcomes, dtype=float),
        sequence=np.asarray(sequences, dtype=int),
    )
    cells, counts = np.unique(
        np.column_stack([dataset.grade, dataset.humidity]),
        axis=0,
        return_counts=True,
    )
    provenance = {
        "branch": "mixed",
        "selection_rule": (
            "North experiment rows whose request explicitly sets both "
            "feedstock_grade and humidity"
        ),
        "included_records": included_records,
        "n_rows": len(outcomes),
        "cells": [
            {
                "grade": float(cell[0]),
                "humidity": float(cell[1]),
                "rows": int(count),
            }
            for cell, count in zip(cells, counts, strict=True)
        ],
        "fit_uses_truth": False,
    }
    return dataset, provenance


def _ols(x: np.ndarray, y: np.ndarray) -> tuple[np.ndarray, float]:
    beta = np.linalg.lstsq(x, y, rcond=None)[0]
    residual = y - x @ beta
    sigma = max(float(np.sqrt(np.mean(residual**2))), 0.3)
    return beta, sigma


def _normal_logpdf(y: np.ndarray, mean: np.ndarray, sigma: float) -> np.ndarray:
    z = (y - mean) / sigma
    return -0.5 * z**2 - math.log(sigma) - 0.5 * math.log(2.0 * math.pi)


def _decode(candidate: Candidate, vector: np.ndarray) -> dict[str, Any]:
    if candidate == "single_gaussian":
        return {
            "beta": vector[:3],
            "sigma": float(np.exp(vector[3])),
        }
    if candidate == "residual_mixture":
        return {
            "intercepts": vector[:2],
            "slopes": vector[2:4],
            "sigmas": np.exp(vector[4:6]),
            "weight_first": float(expit(vector[6])),
        }
    if candidate == "law_mixture":
        return {
            "betas": vector[:6].reshape(2, 3),
            "sigmas": np.exp(vector[6:8]),
            "weight_first": float(expit(vector[8])),
        }
    raise AssertionError(candidate)


def _component_means(
    candidate: Candidate, decoded: dict[str, Any], x: np.ndarray
) -> tuple[np.ndarray, ...]:
    if candidate == "single_gaussian":
        return (x @ decoded["beta"],)
    if candidate == "residual_mixture":
        shared = x[:, 1:] @ decoded["slopes"]
        return (
            decoded["intercepts"][0] + shared,
            decoded["intercepts"][1] + shared,
        )
    betas = decoded["betas"]
    return (x @ betas[0], x @ betas[1])


def _log_density(candidate: Candidate, vector: np.ndarray, data: Dataset) -> np.ndarray:
    decoded = _decode(candidate, vector)
    means = _component_means(candidate, decoded, data.x)
    if candidate == "single_gaussian":
        return _normal_logpdf(data.outcome, means[0], decoded["sigma"])
    weight = decoded["weight_first"]
    sigmas = decoded["sigmas"]
    first = math.log(weight) + _normal_logpdf(data.outcome, means[0], sigmas[0])
    second = math.log1p(-weight) + _normal_logpdf(
        data.outcome, means[1], sigmas[1]
    )
    return logsumexp(np.column_stack([first, second]), axis=1)


def _one_dimensional_clusters(values: np.ndarray) -> np.ndarray:
    centers = np.quantile(values, [0.25, 0.75]).astype(float)
    labels = np.zeros(len(values), dtype=int)
    for _ in range(30):
        updated = np.argmin(abs(values[:, None] - centers[None, :]), axis=1)
        if np.array_equal(updated, labels) and _ > 0:
            break
        labels = updated
        for label in (0, 1):
            if np.any(labels == label):
                centers[label] = float(np.mean(values[labels == label]))
    if centers[0] > centers[1]:
        labels = 1 - labels
    return labels


def _labels_to_start(
    candidate: Candidate, data: Dataset, labels: np.ndarray
) -> np.ndarray | None:
    counts = np.bincount(labels, minlength=2)
    if np.min(counts) < 6:
        return None
    x = data.x
    y = data.outcome
    weight = float(np.mean(labels == 0))
    logit = math.log(weight / (1.0 - weight))
    if candidate == "law_mixture":
        betas = []
        sigmas = []
        for label in (0, 1):
            beta, sigma = _ols(x[labels == label], y[labels == label])
            betas.extend(beta)
            sigmas.append(sigma)
        return np.asarray(
            [*betas, math.log(sigmas[0]), math.log(sigmas[1]), logit]
        )

    design = np.column_stack(
        [labels == 0, labels == 1, data.grade, data.humidity]
    ).astype(float)
    coefficients = np.linalg.lstsq(design, y, rcond=None)[0]
    residual = y - design @ coefficients
    sigmas = [
        max(float(np.sqrt(np.mean(residual[labels == label] ** 2))), 0.3)
        for label in (0, 1)
    ]
    return np.asarray(
        [
            *coefficients,
            math.log(sigmas[0]),
            math.log(sigmas[1]),
            logit,
        ]
    )


def _mixture_starts(
    candidate: Candidate,
    data: Dataset,
    *,
    seed: int,
    random_starts: int,
) -> list[np.ndarray]:
    cells = np.column_stack([data.grade, data.humidity])
    unique_cells, inverse = np.unique(cells, axis=0, return_inverse=True)
    low_high = np.zeros(len(data.outcome), dtype=int)
    for cell_index in range(len(unique_cells)):
        mask = inverse == cell_index
        low_high[mask] = _one_dimensional_clusters(data.outcome[mask])

    alignment_starts: list[tuple[float, int, np.ndarray]] = []
    # Enumerate all alignments of independently discovered low/high modes
    # across intervention cells.  Fixing the first cell removes label symmetry.
    for bits in range(2 ** max(len(unique_cells) - 1, 0)):
        labels = low_high.copy()
        for cell_index in range(1, len(unique_cells)):
            if bits & (1 << (cell_index - 1)):
                labels[inverse == cell_index] = 1 - labels[inverse == cell_index]
        start = _labels_to_start(candidate, data, labels)
        if start is not None:
            initial_likelihood = float(
                np.sum(_log_density(candidate, start, data))
            )
            alignment_starts.append((initial_likelihood, bits, start))

    # More intervention cells create exponentially many label alignments.  All
    # are scored cheaply from data alone, but only the best fixed number become
    # nonlinear optimizer starts.  This is identical to exhaustive use for the
    # 4- and 6-cell donors (8 and 32 alignments respectively).
    alignment_starts.sort(key=lambda item: (-item[0], item[1]))
    starts = [item[2] for item in alignment_starts[:MAX_ALIGNMENT_STARTS]]

    rng = np.random.default_rng(seed)
    for _ in range(random_starts):
        probability = float(rng.uniform(0.2, 0.8))
        labels = (rng.random(len(data.outcome)) >= probability).astype(int)
        start = _labels_to_start(candidate, data, labels)
        if start is not None:
            starts.append(start)
    return starts


def _canonicalize(candidate: Candidate, vector: np.ndarray, data: Dataset) -> np.ndarray:
    if candidate == "single_gaussian":
        return vector
    decoded = _decode(candidate, vector)
    reference = np.asarray(
        [[1.0, float(np.min(data.grade)), float(np.min(data.humidity))]]
    )
    means = _component_means(candidate, decoded, reference)
    if float(means[0][0]) <= float(means[1][0]):
        return vector
    if candidate == "residual_mixture":
        swapped = vector.copy()
        swapped[:2] = vector[1::-1]
        swapped[4:6] = vector[5:3:-1]
        swapped[6] = -vector[6]
        return swapped
    swapped = vector.copy()
    swapped[:3] = vector[3:6]
    swapped[3:6] = vector[:3]
    swapped[6:8] = vector[7:5:-1]
    swapped[8] = -vector[8]
    return swapped


def _json_parameters(candidate: Candidate, decoded: dict[str, Any]) -> dict[str, Any]:
    if candidate == "single_gaussian":
        return {
            "beta_intercept_grade_humidity": decoded["beta"].tolist(),
            "sigma": decoded["sigma"],
        }
    if candidate == "residual_mixture":
        return {
            "component_intercepts": decoded["intercepts"].tolist(),
            "shared_slopes_grade_humidity": decoded["slopes"].tolist(),
            "component_sigmas": decoded["sigmas"].tolist(),
            "weight_first": decoded["weight_first"],
        }
    return {
        "component_betas_intercept_grade_humidity": decoded["betas"].tolist(),
        "component_sigmas": decoded["sigmas"].tolist(),
        "weight_first": decoded["weight_first"],
    }


def _fit(candidate: Candidate, data: Dataset, *, seed: int) -> Fit:
    if candidate == "single_gaussian":
        beta, sigma = _ols(data.x, data.outcome)
        vector = np.asarray([*beta, math.log(sigma)])
        likelihood = float(np.sum(_log_density(candidate, vector, data)))
        return Fit(
            candidate=candidate,
            parameters=_json_parameters(candidate, _decode(candidate, vector)),
            vector=vector,
            log_likelihood=likelihood,
            n_parameters=4,
            converged=True,
            starts_attempted=1,
            starts_converged=1,
        )

    starts = _mixture_starts(
        candidate, data, seed=seed, random_starts=16
    )
    if candidate == "residual_mixture":
        bounds = [
            (-100.0, 100.0),
            (-100.0, 100.0),
            (-10.0, 10.0),
            (-10.0, 10.0),
            (math.log(0.25), math.log(20.0)),
            (math.log(0.25), math.log(20.0)),
            (-4.6, 4.6),
        ]
        n_parameters = 7
    else:
        bounds = [
            *[(-100.0, 100.0), (-10.0, 10.0), (-10.0, 10.0)] * 2,
            (math.log(0.25), math.log(20.0)),
            (math.log(0.25), math.log(20.0)),
            (-4.6, 4.6),
        ]
        n_parameters = 9

    best = None
    converged = 0
    for start in starts:
        result = minimize(
            lambda value: -float(np.sum(_log_density(candidate, value, data))),
            start,
            method="L-BFGS-B",
            bounds=bounds,
            options={"maxiter": 2500, "ftol": 1e-11, "gtol": 1e-7},
        )
        if result.success:
            converged += 1
        if np.isfinite(result.fun) and (best is None or result.fun < best.fun):
            best = result
    if best is None:
        raise RuntimeError(f"all {candidate} starts failed")
    vector = _canonicalize(candidate, np.asarray(best.x), data)
    likelihood = float(np.sum(_log_density(candidate, vector, data)))
    return Fit(
        candidate=candidate,
        parameters=_json_parameters(candidate, _decode(candidate, vector)),
        vector=vector,
        log_likelihood=likelihood,
        n_parameters=n_parameters,
        converged=bool(best.success),
        starts_attempted=len(starts),
        starts_converged=converged,
    )


def _stratified_folds(data: Dataset, *, folds: int, seed: int) -> np.ndarray:
    cell = np.column_stack([data.grade, data.humidity])
    _, inverse = np.unique(cell, axis=0, return_inverse=True)
    assignment = np.empty(len(data.outcome), dtype=int)
    rng = np.random.default_rng(seed)
    for cell_index in np.unique(inverse):
        indices = np.flatnonzero(inverse == cell_index)
        indices = rng.permutation(indices)
        assignment[indices] = np.arange(len(indices)) % folds
    return assignment


def _matched_campaign_holdout(
    data: Dataset,
) -> tuple[np.ndarray, np.ndarray, dict[str, Any]] | None:
    """Hold out the last campaign only in cells that were independently repeated."""
    cells = np.column_stack([data.grade, data.humidity])
    unique_cells, inverse = np.unique(cells, axis=0, return_inverse=True)
    train_parts: list[np.ndarray] = []
    test_parts: list[np.ndarray] = []
    repeated_cells = []
    for cell_index, cell in enumerate(unique_cells):
        cell_indices = np.flatnonzero(inverse == cell_index)
        sequences = np.unique(data.sequence[cell_indices])
        if len(sequences) < 2:
            continue
        heldout_sequence = int(np.max(sequences))
        train = cell_indices[data.sequence[cell_indices] != heldout_sequence]
        test = cell_indices[data.sequence[cell_indices] == heldout_sequence]
        if len(train) == 0 or len(test) == 0:
            continue
        train_parts.append(train)
        test_parts.append(test)
        repeated_cells.append(
            {
                "grade": float(cell[0]),
                "humidity": float(cell[1]),
                "train_sequences": sorted(
                    int(value) for value in np.unique(data.sequence[train])
                ),
                "heldout_sequence": heldout_sequence,
                "train_rows": len(train),
                "heldout_rows": len(test),
            }
        )
    if len(repeated_cells) < 3:
        return None
    train_indices = np.concatenate(train_parts)
    test_indices = np.concatenate(test_parts)
    if np.linalg.matrix_rank(data.x[train_indices]) < 3:
        return None
    return (
        train_indices,
        test_indices,
        {
            "definition": (
                "within each intervention cell repeated in a later independent "
                "campaign, fit earlier campaign(s) and hold out the last"
            ),
            "repeated_cells": repeated_cells,
            "train_rows": len(train_indices),
            "heldout_rows": len(test_indices),
        },
    )


def _draw_fit(
    fit: Fit,
    *,
    grade: float,
    humidity: float,
    n: int,
    seed: int,
) -> np.ndarray:
    decoded = _decode(fit.candidate, fit.vector)
    x = np.repeat([[1.0, grade, humidity]], n, axis=0)
    means = _component_means(fit.candidate, decoded, x)
    rng = np.random.default_rng(seed)
    if fit.candidate == "single_gaussian":
        return means[0] + rng.normal(0.0, decoded["sigma"], n)
    first = rng.random(n) < decoded["weight_first"]
    noise = rng.normal(0.0, 1.0, n)
    return np.where(
        first,
        means[0] + decoded["sigmas"][0] * noise,
        means[1] + decoded["sigmas"][1] * noise,
    )


def _regime(grade: float) -> Regime:
    return Regime(
        config={"feedstock_grade": grade, "humidity": 5.0},
        context={"site": "north"},
        horizon=None,
    )


def _truth_draws(*, n: int, seed: int) -> dict[str, np.ndarray]:
    server = build_world_server(MIXED_CASE)
    return {
        label: server.world_sample(_regime(grade), n, seed)["outcome"].to_numpy(
            dtype=float
        )
        for label, grade in (("G3", 3.0), ("G7", 7.0))
    }


def _agent_draws(code: str, *, n: int, seed: int) -> dict[str, np.ndarray]:
    with SandboxedSubmission(code, ["feedstock", "outcome"], timeout_s=15.0) as model:
        return {
            label: model.run(_regime(grade), n, seed)["outcome"].to_numpy(
                dtype=float
            )
            for label, grade in (("G3", 3.0), ("G7", 7.0))
        }


def _summary(values: np.ndarray) -> dict[str, float]:
    mean = float(np.mean(values))
    variance = float(np.var(values))
    sd = math.sqrt(max(variance, 0.0))
    skew = float(np.mean(((values - mean) / sd) ** 3)) if sd > 1e-12 else 0.0
    return {"mean": mean, "variance": variance, "skew": skew}


def _local_metrics(
    draws: dict[str, np.ndarray], truth: dict[str, np.ndarray]
) -> dict[str, Any]:
    summaries = {label: _summary(values) for label, values in draws.items()}
    truth_summaries = {
        label: _summary(values) for label, values in truth.items()
    }
    delta = summaries["G7"]["mean"] - summaries["G3"]["mean"]
    truth_delta = (
        truth_summaries["G7"]["mean"] - truth_summaries["G3"]["mean"]
    )
    a3 = (summaries["G7"]["skew"] - summaries["G3"]["skew"]) / 2.0
    truth_a3 = (
        truth_summaries["G7"]["skew"] - truth_summaries["G3"]["skew"]
    ) / 2.0
    w1_terms = []
    energy_terms = []
    for label in ("G3", "G7"):
        scale = float(np.std(truth[label]))
        w1_terms.append(
            float(np.mean(abs(np.sort(draws[label]) - np.sort(truth[label]))))
            / scale
        )
        energy_terms.append(float(energy_distance(draws[label], truth[label])) / scale)
    return {
        "regimes": summaries,
        "delta_mean_G7_minus_G3": float(delta),
        "truth_delta": float(truth_delta),
        "delta_absolute_error": float(abs(delta - truth_delta)),
        "U_mean_revision": float((8.0 - delta) / 8.0),
        "oriented_skew_A3": float(a3),
        "truth_empirical_A3": float(truth_a3),
        "declared_expected_A3": EXPECTED_MIXED_A3,
        "A3_capture_fraction": float(a3 / EXPECTED_MIXED_A3),
        "A3_absolute_error": float(abs(a3 - EXPECTED_MIXED_A3)),
        "mean_W1_to_truth_in_truth_sd": float(np.mean(w1_terms)),
        "mean_energy_to_truth_in_truth_sd": float(np.mean(energy_terms)),
    }


def _agent_codes(payload: dict[str, Any]) -> dict[str, str]:
    branch = payload["branches"]["mixed"]
    selection = payload.get("prefix", {}).get("selection") or {}
    result = {}
    if selection.get("M_pre"):
        result["agent_M_pre"] = selection["M_pre"]
    final = (
        branch.get("last_scoreable_model")
        or branch.get("last_working_model_code")
        or branch.get("submission_code")
    )
    if final:
        result["agent_M_last"] = final
    return result


def analyze(
    raw: Path,
    *,
    seed: int,
    folds: int,
    eval_n: int,
) -> dict[str, Any]:
    payload = json.loads(raw.read_text(encoding="utf-8"))
    data, provenance = _extract_dataset(payload)
    candidates: tuple[Candidate, ...] = (
        "single_gaussian",
        "residual_mixture",
        "law_mixture",
    )

    # All fitting and model selection occur before this function loads truth.
    full_fits = {
        candidate: _fit(candidate, data, seed=seed + 100 * index)
        for index, candidate in enumerate(candidates)
    }
    fold_assignment = _stratified_folds(data, folds=folds, seed=seed + 10_000)
    cv: dict[str, Any] = {}
    fold_fits: dict[str, list[Fit]] = {candidate: [] for candidate in candidates}
    for candidate_index, candidate in enumerate(candidates):
        heldout_ll = []
        heldout_n = []
        for fold in range(folds):
            train_indices = np.flatnonzero(fold_assignment != fold)
            test_indices = np.flatnonzero(fold_assignment == fold)
            fit = _fit(
                candidate,
                data.subset(train_indices),
                seed=seed + 20_000 + 1000 * candidate_index + fold,
            )
            fold_fits[candidate].append(fit)
            heldout_ll.append(
                float(
                    np.sum(
                        _log_density(candidate, fit.vector, data.subset(test_indices))
                    )
                )
            )
            heldout_n.append(len(test_indices))
        cv[candidate] = {
            "fold_log_likelihoods": heldout_ll,
            "fold_rows": heldout_n,
            "total_heldout_log_likelihood": float(np.sum(heldout_ll)),
            "mean_heldout_log_likelihood_per_row": float(
                np.sum(heldout_ll) / np.sum(heldout_n)
            ),
        }

    # A second, stricter generalization check holds out whole later campaigns
    # only where the same intervention cell was independently repeated.
    campaign_split = _matched_campaign_holdout(data)
    temporal_fits: dict[str, Fit] = {}
    temporal_holdout: dict[str, Any] = {"available": campaign_split is not None}
    if campaign_split is not None:
        early_indices, later_indices, split_description = campaign_split
        temporal_holdout["split"] = split_description
        temporal_holdout["by_candidate"] = {}
        for candidate_index, candidate in enumerate(candidates):
            fit = _fit(
                candidate,
                data.subset(early_indices),
                seed=seed + 30_000 + 1000 * candidate_index,
            )
            temporal_fits[candidate] = fit
            heldout_ll = float(
                np.sum(
                    _log_density(candidate, fit.vector, data.subset(later_indices))
                )
            )
            temporal_holdout["by_candidate"][candidate] = {
                "heldout_log_likelihood": heldout_ll,
                "mean_heldout_log_likelihood_per_row": float(
                    heldout_ll / len(later_indices)
                ),
                "parameters_fit_without_later_campaigns": fit.parameters,
            }

    selection = {}
    n_rows = len(data.outcome)
    for candidate, fit in full_fits.items():
        bic = fit.n_parameters * math.log(n_rows) - 2.0 * fit.log_likelihood
        selection[candidate] = {
            "full_log_likelihood": fit.log_likelihood,
            "n_parameters": fit.n_parameters,
            "BIC_lower_is_better": float(bic),
            **cv[candidate],
        }
    bic_winner = min(selection, key=lambda name: selection[name]["BIC_lower_is_better"])
    cv_winner = max(
        selection,
        key=lambda name: selection[name]["mean_heldout_log_likelihood_per_row"],
    )
    temporal_winner = None
    if campaign_split is not None:
        temporal_winner = max(
            temporal_holdout["by_candidate"],
            key=lambda name: temporal_holdout["by_candidate"][name][
                "mean_heldout_log_likelihood_per_row"
            ],
        )

    truth = _truth_draws(n=eval_n, seed=seed + 40_000)
    evaluations: dict[str, Any] = {}
    for candidate_index, (candidate, fit) in enumerate(full_fits.items()):
        draws = {
            label: _draw_fit(
                fit,
                grade=grade,
                humidity=5.0,
                n=eval_n,
                seed=seed + 50_000 + 100 * candidate_index,
            )
            for label, grade in (("G3", 3.0), ("G7", 7.0))
        }
        evaluations[candidate] = _local_metrics(draws, truth)

    fold_local: dict[str, list[dict[str, Any]]] = {}
    for candidate_index, candidate in enumerate(candidates):
        fold_local[candidate] = []
        for fold, fit in enumerate(fold_fits[candidate]):
            draws = {
                label: _draw_fit(
                    fit,
                    grade=grade,
                    humidity=5.0,
                    n=eval_n,
                    seed=seed + 60_000 + 1000 * candidate_index + fold,
                )
                for label, grade in (("G3", 3.0), ("G7", 7.0))
            }
            metrics = _local_metrics(draws, truth)
            fold_local[candidate].append(
                {
                    "fold": fold,
                    "delta_mean_G7_minus_G3": metrics[
                        "delta_mean_G7_minus_G3"
                    ],
                    "oriented_skew_A3": metrics["oriented_skew_A3"],
                    "A3_capture_fraction": metrics["A3_capture_fraction"],
                    "mean_W1_to_truth_in_truth_sd": metrics[
                        "mean_W1_to_truth_in_truth_sd"
                    ],
                    "parameters": fit.parameters,
                }
            )

    temporal_local = None
    if campaign_split is not None:
        temporal_local = {}
        for candidate_index, candidate in enumerate(candidates):
            fit = temporal_fits[candidate]
            draws = {
                label: _draw_fit(
                    fit,
                    grade=grade,
                    humidity=5.0,
                    n=eval_n,
                    seed=seed + 65_000 + 1000 * candidate_index,
                )
                for label, grade in (("G3", 3.0), ("G7", 7.0))
            }
            temporal_local[candidate] = _local_metrics(draws, truth)

    for name, code in _agent_codes(payload).items():
        evaluations[name] = _local_metrics(
            _agent_draws(code, n=eval_n, seed=seed + 70_000), truth
        )

    best_fit = full_fits["law_mixture"]
    law_eval = evaluations["law_mixture"]
    stable_fold_capture = [
        row["A3_capture_fraction"] for row in fold_local["law_mixture"]
    ]
    foldwise_law_advantage = [
        law - residual
        for law, residual in zip(
            cv["law_mixture"]["fold_log_likelihoods"],
            cv["residual_mixture"]["fold_log_likelihoods"],
            strict=True,
        )
    ]
    structural_support = {
        "bic_selects_law_mixture": bic_winner == "law_mixture",
        "heldout_likelihood_selects_law_mixture": cv_winner == "law_mixture",
        "law_mixture_beats_residual_mixture_in_every_cv_fold": all(
            value > 0.0 for value in foldwise_law_advantage
        ),
        "later_campaign_holdout_selects_law_mixture": (
            None if temporal_winner is None else temporal_winner == "law_mixture"
        ),
    }
    full_ledger_recovery = {
        "full_fit_A3_capture_at_least_half": law_eval["A3_capture_fraction"] >= 0.5,
        "full_fit_mean_delta_error_at_most_one": (
            law_eval["delta_absolute_error"] <= 1.0
        ),
    }
    deletion_stability = {
        "fold_A3_capture_fractions": stable_fold_capture,
        "folds_at_least_half_capture": int(
            sum(value >= 0.5 for value in stable_fold_capture)
        ),
        "fold_count": len(stable_fold_capture),
        "all_fold_fits_A3_capture_at_least_half": all(
            value >= 0.5 for value in stable_fold_capture
        ),
    }
    recoverability = {
        "structural_support": structural_support,
        "full_ledger_local_recovery": full_ledger_recovery,
        "twenty_percent_deletion_stability": deletion_stability,
        "structure_supported_by_all_selection_checks": all(
            value for value in structural_support.values() if value is not None
        ),
        "full_ledger_recovers_declared_local_target": all(
            full_ledger_recovery.values()
        ),
        "uniformly_stable_under_twenty_percent_deletion": deletion_stability[
            "all_fold_fits_A3_capture_at_least_half"
        ],
        "verdict": (
            "recoverable_from_full_ledger_and_stable_under_twenty_percent_deletion"
            if deletion_stability["all_fold_fits_A3_capture_at_least_half"]
            else "recoverable_from_full_ledger_but_not_uniformly_stable_under_"
            "twenty_percent_deletion"
        ),
    }

    fits_payload = {}
    for candidate, fit in full_fits.items():
        fits_payload[candidate] = {
            "parameters": fit.parameters,
            "converged": fit.converged,
            "starts_attempted": fit.starts_attempted,
            "starts_converged": fit.starts_converged,
        }
    return {
        "source": str(raw),
        "model": payload.get("model"),
        "seed_offset": payload.get("seed_offset"),
        "fit_data": provenance,
        "method": {
            "candidate_models": list(candidates),
            "initialization": (
                "data-only: 1D response clustering within each controlled cell, "
                "all cross-cell label alignments ranked by initial likelihood, "
                f"up to {MAX_ALIGNMENT_STARTS} optimizer starts, plus 16 random starts"
            ),
            "privileged_initialization": False,
            "cross_validation": f"{folds}-fold, stratified by intervention cell",
            "truth_loaded_after_fitting_and_selection": True,
            "evaluation_n_per_local_regime": eval_n,
        },
        "fits": fits_payload,
        "selection": {
            "by_candidate": selection,
            "BIC_winner": bic_winner,
            "heldout_likelihood_winner": cv_winner,
            "foldwise_law_minus_residual_heldout_log_likelihood": (
                foldwise_law_advantage
            ),
            "later_campaign_holdout": temporal_holdout,
            "later_campaign_holdout_winner": temporal_winner,
        },
        "local_evaluation_against_truth": evaluations,
        "fold_fit_local_stability": fold_local,
        "early_fit_local_evaluation_against_truth": temporal_local,
        "recoverability_certificate": recoverability,
        "caution": (
            "This establishes recoverability for this fixed donor and declared "
            "candidate family; it does not establish spontaneous discoverability "
            "by an unconstrained research agent or generalize to other donors."
        ),
        "law_mixture_fit_log_likelihood": best_fit.log_likelihood,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("raw", type=Path)
    parser.add_argument("--seed", type=int, default=1_610_031)
    parser.add_argument("--folds", type=int, default=5)
    parser.add_argument("--eval-n", type=int, default=30_000)
    parser.add_argument("--out", type=Path)
    args = parser.parse_args()
    if args.folds < 2:
        parser.error("--folds must be at least 2")
    if args.eval_n < 2_000:
        parser.error("--eval-n must be at least 2000")
    try:
        result = analyze(
            args.raw, seed=args.seed, folds=args.folds, eval_n=args.eval_n
        )
    except (OSError, ValueError, KeyError, json.JSONDecodeError) as exc:
        parser.error(str(exc))
    rendered = json.dumps(result, indent=2, allow_nan=False) + "\n"
    if args.out is None:
        print(rendered, end="")
    else:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(rendered, encoding="utf-8")
        print(args.out)


if __name__ == "__main__":
    main()
