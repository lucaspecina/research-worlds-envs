"""Zero-LLM recoverability analysis for topology-v1 North campaigns.

The public helpers consume either a row table or WAGER evidence-ledger entries.
They never load a world truth.  Three candidate predictive structures are fit
and compared by BIC and stratified held-out likelihood.  Affine laws are fit
in the observed intervention subspace: ``[1, G, H]`` for the ordinary
two-control protocol, or ``[1, variable]`` when three or more cells vary
exactly one control:

* one affine law in the observed intervention subspace;
* two affine laws selected by the visible A/B class;
* two latent affine laws with a fitted mixture weight.

An underdetermined real campaign returns ``informative=False`` rather than a
misleading winner.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Any, Literal

import numpy as np
import pandas as pd
from scipy.optimize import minimize
from scipy.special import logsumexp

Candidate = Literal["single", "class_split", "latent_mixture"]
Target = Literal["local", "latent"]
CANDIDATES: tuple[Candidate, ...] = (
    "single",
    "class_split",
    "latent_mixture",
)


@dataclass(frozen=True)
class CampaignData:
    grade: np.ndarray
    humidity: np.ndarray
    is_a: np.ndarray
    outcome: np.ndarray

    @property
    def varying_controls(self) -> tuple[str, ...]:
        controls = []
        if np.unique(self.grade).size > 1:
            controls.append("feedstock_grade")
        if np.unique(self.humidity).size > 1:
            controls.append("humidity")
        return tuple(controls)

    @property
    def design_columns(self) -> tuple[str, ...]:
        return ("intercept", *self.varying_controls)

    def design_matrix(
        self,
        grade: np.ndarray | None = None,
        humidity: np.ndarray | None = None,
    ) -> np.ndarray:
        grade_values = self.grade if grade is None else np.asarray(grade)
        humidity_values = self.humidity if humidity is None else np.asarray(humidity)
        if len(grade_values) != len(humidity_values):
            raise ValueError("grade and humidity arrays must have equal length")
        columns = [np.ones(len(grade_values))]
        for control in self.varying_controls:
            columns.append(
                grade_values if control == "feedstock_grade" else humidity_values
            )
        return np.column_stack(columns)

    @property
    def x(self) -> np.ndarray:
        return self.design_matrix()

    def take(self, indices: np.ndarray) -> "CampaignData":
        return CampaignData(
            self.grade[indices],
            self.humidity[indices],
            self.is_a[indices],
            self.outcome[indices],
        )


@dataclass(frozen=True)
class Fit:
    candidate: Candidate
    vector: np.ndarray
    n_parameters: int
    log_likelihood: float
    converged: bool


def _normal_logpdf(y, mean, sigma):
    return (
        -0.5 * ((y - mean) / sigma) ** 2
        - math.log(sigma)
        - 0.5 * math.log(2.0 * math.pi)
    )


def _log_density(
    candidate: Candidate, vector: np.ndarray, data: CampaignData
) -> np.ndarray:
    x = data.x
    d = x.shape[1]
    if candidate == "single":
        mean = x @ vector[:d]
        return _normal_logpdf(data.outcome, mean, math.exp(vector[d]))
    if candidate == "class_split":
        mean_a = x @ vector[:d]
        mean_b = x @ vector[d : 2 * d]
        mean = np.where(data.is_a, mean_a, mean_b)
        return _normal_logpdf(data.outcome, mean, math.exp(vector[2 * d]))
    mean_1 = x @ vector[:d]
    mean_2 = x @ vector[d : 2 * d]
    sigma = math.exp(vector[2 * d])
    weight = 1.0 / (1.0 + math.exp(-vector[2 * d + 1]))
    terms = np.column_stack(
        [
            math.log(weight) + _normal_logpdf(data.outcome, mean_1, sigma),
            math.log(1.0 - weight) + _normal_logpdf(data.outcome, mean_2, sigma),
        ]
    )
    return logsumexp(terms, axis=1)


def _ols(x: np.ndarray, y: np.ndarray) -> tuple[np.ndarray, float]:
    beta = np.linalg.lstsq(x, y, rcond=None)[0]
    residual = y - x @ beta
    sigma = max(float(np.sqrt(np.mean(residual**2))), 0.25)
    return beta, sigma


def _cluster_centers(y: np.ndarray) -> tuple[float, float]:
    centers = np.quantile(y, [0.25, 0.75]).astype(float)
    for _ in range(30):
        assignment = np.abs(y[:, None] - centers[None, :]).argmin(axis=1)
        updated = np.array(
            [
                y[assignment == index].mean()
                if np.any(assignment == index)
                else centers[index]
                for index in range(2)
            ]
        )
        if np.max(np.abs(updated - centers)) < 1e-8:
            break
        centers = updated
    return tuple(sorted(float(value) for value in centers))


def _alignment_masks(cell_count: int, *, seed: int) -> list[int]:
    possibilities = 1 << max(cell_count - 1, 0)
    if possibilities <= 64:
        return list(range(possibilities))
    rng = np.random.default_rng(seed)
    selected = {0, possibilities - 1}
    selected.update(int(value) for value in rng.integers(0, possibilities, size=62))
    return sorted(selected)


def _fit(candidate: Candidate, data: CampaignData, *, seed: int) -> Fit:
    x = data.x
    d = x.shape[1]
    if np.linalg.matrix_rank(x) < d:
        raise ValueError(
            f"campaign design matrix {list(data.design_columns)} is rank deficient"
        )
    if candidate == "single":
        beta, sigma = _ols(x, data.outcome)
        vector = np.array([*beta, math.log(sigma)])
        return Fit(
            candidate,
            vector,
            d + 1,
            float(np.sum(_log_density(candidate, vector, data))),
            True,
        )
    if candidate == "class_split":
        coefficients = []
        residuals = []
        for mask in (data.is_a, ~data.is_a):
            if int(mask.sum()) < d or np.linalg.matrix_rank(x[mask]) < d:
                raise ValueError(
                    "each visible class needs full-rank coverage in the "
                    "observed intervention subspace"
                )
            beta, _ = _ols(x[mask], data.outcome[mask])
            coefficients.extend(beta)
            residuals.append(data.outcome[mask] - x[mask] @ beta)
        sigma = max(float(np.sqrt(np.mean(np.concatenate(residuals) ** 2))), 0.25)
        vector = np.array([*coefficients, math.log(sigma)])
        return Fit(
            candidate,
            vector,
            2 * d + 1,
            float(np.sum(_log_density(candidate, vector, data))),
            True,
        )

    cells = np.column_stack([data.grade, data.humidity])
    unique_cells, inverse = np.unique(cells, axis=0, return_inverse=True)
    cell_x = data.design_matrix(grade=unique_cells[:, 0], humidity=unique_cells[:, 1])
    if np.linalg.matrix_rank(cell_x) < d:
        raise ValueError(
            "unique intervention cells do not span the observed intervention subspace"
        )
    centers = [
        _cluster_centers(data.outcome[inverse == index])
        for index in range(len(unique_cells))
    ]
    starts = []
    for alignment in _alignment_masks(len(unique_cells), seed=seed):
        component_1 = []
        component_2 = []
        for index, pair in enumerate(centers):
            swap = index > 0 and bool(alignment & (1 << (index - 1)))
            component_1.append(pair[1] if swap else pair[0])
            component_2.append(pair[0] if swap else pair[1])
        beta_1 = np.linalg.lstsq(cell_x, np.asarray(component_1), rcond=None)[0]
        beta_2 = np.linalg.lstsq(cell_x, np.asarray(component_2), rcond=None)[0]
        for weight in (0.25, 0.75):
            starts.append(
                np.array(
                    [
                        *beta_1,
                        *beta_2,
                        math.log(2.0),
                        math.log(weight / (1.0 - weight)),
                    ]
                )
            )
    rng = np.random.default_rng(seed + 1)
    pooled, pooled_sigma = _ols(x, data.outcome)
    perturbation_scale = np.array([3.0, *([0.5] * (d - 1))])
    for _ in range(4):
        starts.append(
            np.array(
                [
                    *(pooled + rng.normal(0.0, perturbation_scale)),
                    *(pooled + rng.normal(0.0, perturbation_scale)),
                    math.log(pooled_sigma),
                    rng.normal(),
                ]
            )
        )
    coefficient_bounds = [
        (-100.0, 120.0),
        *([(-12.0, 12.0)] * (d - 1)),
    ]
    bounds = coefficient_bounds * 2 + [(math.log(0.25), math.log(20.0)), (-5.0, 5.0)]
    best = None
    for start in starts:
        result = minimize(
            lambda value: -float(np.sum(_log_density(candidate, value, data))),
            start,
            method="L-BFGS-B",
            bounds=bounds,
            options={"maxiter": 1800, "ftol": 1e-10},
        )
        if np.isfinite(result.fun) and (best is None or result.fun < best.fun):
            best = result
    if best is None:
        raise RuntimeError("latent-mixture optimizer failed")
    vector = np.asarray(best.x)
    return Fit(
        candidate,
        vector,
        2 * d + 2,
        float(np.sum(_log_density(candidate, vector, data))),
        bool(best.success),
    )


def _campaign_data(rows: pd.DataFrame) -> CampaignData:
    required = {"feedstock_grade", "humidity", "batch_class", "outcome"}
    missing = required - set(rows.columns)
    if missing:
        raise ValueError(f"campaign rows missing columns: {sorted(missing)}")
    if not set(rows["batch_class"].astype(str).str.upper()).issubset({"A", "B"}):
        raise ValueError("batch_class must contain only A/B")
    arrays = {
        column: rows[column].to_numpy(dtype=float)
        for column in ("feedstock_grade", "humidity", "outcome")
    }
    if not all(np.isfinite(value).all() for value in arrays.values()):
        raise ValueError("campaign contains non-finite numeric values")
    return CampaignData(
        arrays["feedstock_grade"],
        arrays["humidity"],
        rows["batch_class"].astype(str).str.upper().to_numpy() == "A",
        arrays["outcome"],
    )


def rows_from_ledger(ledger: list[dict[str, Any]]) -> tuple[pd.DataFrame, dict]:
    """Extract eligible controlled North rows without interpreting outcomes."""
    frames = []
    accepted_sequences = []
    excluded = []
    for index, entry in enumerate(ledger):
        request = entry.get("request") or {}
        config = request.get("config") or {}
        context = request.get("context") or {}
        reason = None
        if entry.get("kind") != "experiment":
            reason = "not_experiment"
        elif str(context.get("site", "")).lower() != "north":
            reason = "not_north"
        elif not {"feedstock_grade", "humidity"}.issubset(config):
            reason = "G_or_H_not_fixed"
        data = entry.get("data") or {}
        columns = data.get("columns") or []
        values = data.get("data") or []
        if reason is None and not {"batch_class", "outcome"}.issubset(columns):
            reason = "visible_class_or_outcome_missing"
        if reason is not None:
            excluded.append(
                {"index": index, "sequence": entry.get("sequence"), "reason": reason}
            )
            continue
        frame = pd.DataFrame(values, columns=columns)
        frame["feedstock_grade"] = float(config["feedstock_grade"])
        frame["humidity"] = float(config["humidity"])
        frames.append(frame)
        accepted_sequences.append(entry.get("sequence", index))
    if not frames:
        return pd.DataFrame(), {
            "accepted_sequences": [],
            "excluded": excluded,
            "eligible_rows": 0,
        }
    rows = pd.concat(frames, ignore_index=True)
    return rows, {
        "accepted_sequences": accepted_sequences,
        "excluded": excluded,
        "eligible_rows": len(rows),
    }


def _fold_assignment(data: CampaignData, *, folds: int, seed: int) -> np.ndarray:
    assignment = np.empty(len(data.grade), dtype=int)
    rng = np.random.default_rng(seed)
    strata = np.column_stack([data.grade, data.humidity, data.is_a.astype(int)])
    _, inverse = np.unique(strata, axis=0, return_inverse=True)
    for index in np.unique(inverse):
        rows = rng.permutation(np.flatnonzero(inverse == index))
        if len(rows) < folds:
            raise ValueError(
                f"stratum {index} has {len(rows)} rows, fewer than {folds} folds"
            )
        assignment[rows] = np.arange(len(rows)) % folds
    return assignment


def recoverability_from_rows(
    rows: pd.DataFrame,
    *,
    target: Target | None = None,
    folds: int | None = 5,
    seed: int = 1_700_001,
    provenance: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Fit/select all structures; return an explicit noninformative verdict."""
    summary = {
        "rows": len(rows),
        "target": target,
        "requested_fold_count": folds,
        "provenance": provenance or {},
    }
    try:
        if folds is not None and folds < 2:
            raise ValueError("folds must be at least 2")
        data = _campaign_data(rows)
        unique_cells = np.unique(np.column_stack([data.grade, data.humidity]), axis=0)
        summary.update(
            {
                "unique_cells": unique_cells.tolist(),
                "unique_cell_count": len(unique_cells),
                "design_rank": int(np.linalg.matrix_rank(data.x)),
                "design_columns": list(data.design_columns),
                "design_dimension": int(data.x.shape[1]),
                "varying_controls": list(data.varying_controls),
                "class_A_fraction": float(data.is_a.mean()),
                "class_counts": {
                    "A": int(data.is_a.sum()),
                    "B": int((~data.is_a).sum()),
                },
            }
        )
        if len(unique_cells) < 3:
            raise ValueError("need at least three controlled (G,H) cells")
        if not data.varying_controls:
            raise ValueError("at least one intervention control must vary")
        if np.linalg.matrix_rank(data.x) < data.x.shape[1]:
            raise ValueError(
                "when both controls vary, controlled (G,H) cells must span "
                "the full [1,G,H] design"
            )
        strata = np.column_stack([data.grade, data.humidity, data.is_a.astype(int)])
        _, stratum_counts = np.unique(strata, axis=0, return_counts=True)
        minimum_stratum_rows = int(stratum_counts.min())
        if folds is None:
            selected_folds = next(
                (
                    candidate
                    for candidate in range(5, 1, -1)
                    if minimum_stratum_rows >= candidate
                ),
                None,
            )
            if selected_folds is None:
                raise ValueError(
                    "every config×class stratum needs at least 2 rows for CV"
                )
            fold_selection = "target_blind_maximum_supported_in_5_to_2"
        else:
            selected_folds = folds
            fold_selection = "fixed"
        summary.update(
            {
                "fold_count": selected_folds,
                "fold_selection": fold_selection,
                "minimum_config_class_stratum_rows": minimum_stratum_rows,
            }
        )
        fold_id = _fold_assignment(data, folds=selected_folds, seed=seed + 10_000)
        full = {
            candidate: _fit(candidate, data, seed=seed + 100 * index)
            for index, candidate in enumerate(CANDIDATES)
        }
        bic = {
            candidate: fit.n_parameters * math.log(len(data.outcome))
            - 2.0 * fit.log_likelihood
            for candidate, fit in full.items()
        }
        heldout = {candidate: 0.0 for candidate in CANDIDATES}
        fold_rows = []
        for fold in range(selected_folds):
            train = np.flatnonzero(fold_id != fold)
            test = np.flatnonzero(fold_id == fold)
            fold_row: dict[str, Any] = {"fold": fold, "rows": len(test)}
            for index, candidate in enumerate(CANDIDATES):
                fit = _fit(
                    candidate,
                    data.take(train),
                    seed=seed + 20_000 + 1000 * fold + index,
                )
                value = float(
                    np.sum(_log_density(candidate, fit.vector, data.take(test)))
                )
                heldout[candidate] += value
                fold_row[candidate] = value
            fold_rows.append(fold_row)
        bic_winner = min(bic, key=bic.get)
        cv_winner = max(heldout, key=heldout.get)
        selected = bic_winner if bic_winner == cv_winner else "selection_disagrees"
        expected = (
            "class_split"
            if target == "local"
            else "latent_mixture"
            if target == "latent"
            else None
        )
        recoverable = (
            selected == expected
            if expected is not None
            else selected in {"class_split", "latent_mixture"}
        )
        return summary | {
            "informative": True,
            "reason": None,
            "n_parameters": {name: int(fit.n_parameters) for name, fit in full.items()},
            "BIC": {name: float(value) for name, value in bic.items()},
            "BIC_winner": bic_winner,
            "CV_heldout_log_likelihood": heldout,
            "CV_winner": cv_winner,
            "folds": fold_rows,
            "selected_structure": selected,
            "expected_structure": expected,
            "recoverable": bool(recoverable),
            "class_split_minus_best_ignoring_class_CV": float(
                heldout["class_split"]
                - max(heldout["single"], heldout["latent_mixture"])
            ),
            "latent_minus_best_nonlatent_CV": float(
                heldout["latent_mixture"]
                - max(heldout["single"], heldout["class_split"])
            ),
        }
    except (ValueError, RuntimeError, np.linalg.LinAlgError) as exc:
        return summary | {
            "informative": False,
            "reason": str(exc),
            "recoverable": False,
        }


def recoverability_from_ledger(
    ledger: list[dict[str, Any]],
    *,
    target: Target | None = None,
    folds: int | None = 5,
    seed: int = 1_700_001,
) -> dict[str, Any]:
    """Public runner API: extract eligible rows, then run BIC and CV."""
    rows, provenance = rows_from_ledger(ledger)
    return recoverability_from_rows(
        rows,
        target=target,
        folds=folds,
        seed=seed,
        provenance=provenance,
    )
