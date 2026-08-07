"""Zero-LLM certificate for the four-pole transfer-topology v1 family.

No agent is called.  The certificate checks the shared interface, exact
LOCAL/LATENT outcome pairing, class-conditional causal signatures, official
scoring margin, fixed-reflex failures, and recoverability on a frozen two-cell
North protocol using BIC plus held-out likelihood.
"""

from __future__ import annotations

import json
import math
import sys
from dataclasses import dataclass
from pathlib import Path
from types import SimpleNamespace

import numpy as np
from scipy.optimize import minimize
from scipy.special import logsumexp

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from cases.first_story_scm_transfer_topology_v1_robots import (  # noqa: E402
    model_code,
)
from wager.contracts import Regime  # noqa: E402
from wager.factory.case_loader import (  # noqa: E402
    load_battery,
    load_meta,
    load_world_module,
)
from wager.harness.case_episode import build_world_server  # noqa: E402
from wager.reward.sandbox import SandboxedSubmission  # noqa: E402
from wager.reward.scorer import (  # noqa: E402
    WorldSide,
    sandboxed_null_sample,
    score_submission,
)
from scripts.analyze_scm_topology_recoverability import (  # noqa: E402
    recoverability_from_ledger,
)

CASES = {
    "retain": ROOT / "cases" / "first_story_scm_transfer_retain_v1",
    "revise": ROOT / "cases" / "first_story_scm_transfer_revise_v1",
    "local": ROOT / "cases" / "first_story_scm_transfer_local_v1",
    "latent": ROOT / "cases" / "first_story_scm_transfer_latent_v1",
}
OUTPUT_COLUMNS = ["feedstock", "outcome"]
RECOVERABILITY_PROTOCOL = {
    "cells": [
        {"humidity": 3.0, "feedstock_grade": 3.0},
        {"humidity": 3.0, "feedstock_grade": 7.0},
        {"humidity": 7.0, "feedstock_grade": 3.0},
        {"humidity": 7.0, "feedstock_grade": 7.0},
    ],
    "rows_per_cell": 60,
    "total_rows": 240,
    "experiment_cost_fixed": 100.0,
    "experiment_cost_per_row": 2.0,
    "total_cost": 880.0,
    "minimum_post_South_budget_required": 880.0,
    "folds": 5,
}


def _ns(config=None, *, site="south", batch_class=None):
    context = {"site": site}
    if batch_class is not None:
        context["batch_class"] = batch_class
    return SimpleNamespace(config=dict(config or {}), context=context, horizon=None)


def _code(case_dir: Path, relative: str) -> str:
    return (case_dir / relative).read_text(encoding="utf-8")


def _callable(code: str):
    namespace: dict = {}
    exec(compile(code, "<topology-certificate>", "exec"), namespace)  # noqa: S102
    return namespace["model"]


def _agent_meta(case_dir: Path) -> dict:
    value = json.loads((case_dir / "meta.json").read_text(encoding="utf-8"))
    value.pop("case_id")
    value.pop("operators")
    return value


def _key(value) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def _delta(world, batch_class: str, *, n=200_000, seed=1_100_001) -> float:
    low = world.sample(
        _ns(
            {"humidity": 5.0, "feedstock_grade": 3.0},
            site="north",
            batch_class=batch_class,
        ),
        n,
        seed,
    )
    high = world.sample(
        _ns(
            {"humidity": 5.0, "feedstock_grade": 7.0},
            site="north",
            batch_class=batch_class,
        ),
        n,
        seed,
    )
    return float(high["outcome"].mean() - low["outcome"].mean())


def _model_delta(code: str, batch_class: str, *, n=40_000) -> float:
    with SandboxedSubmission(code, OUTPUT_COLUMNS, timeout_s=15.0) as model:
        frames = {}
        for label, grade in (("low", 3.0), ("high", 7.0)):
            frames[label] = model.run(
                Regime(
                    config={"humidity": 5.0, "feedstock_grade": grade},
                    context={"site": "north", "batch_class": batch_class},
                ),
                n,
                1_200_001,
            )
    return float(
        frames["high"]["outcome"].mean()
        - frames["low"]["outcome"].mean()
    )


def _official_margin(case_dir: Path) -> dict:
    meta = load_meta(case_dir)
    world = load_world_module(case_dir)
    truth = _code(case_dir, "truth_code.py")
    # The transferable pre-North belief required by the lived runner is the
    # South grade law, not the 50/50 ladder anchor.  This is the relevant
    # truth-side ceiling for gate 7; each real donor Mpre is gated separately.
    mpre_grade = model_code("retain")
    null = _code(case_dir, "ladder/rung_8_null.py")
    with sandboxed_null_sample(
        null, meta.column_names, meta.scoring.model_call_timeout_s
    ) as null_sample:
        side = WorldSide(
            world.sample,
            load_battery(case_dir),
            meta.column_names,
            meta.scoring.n_samples,
            null_sample=null_sample,
            functionals=list(meta.stakes.functionals),
            c_f=meta.scoring.c_f,
        )
        reports = {
            name: score_submission(code, side, meta.scoring)
            for name, code in {"truth": truth, "Mpre_grade": mpre_grade}.items()
        }
    return {
        name: {
            "fidelity": float(report.fidelity),
            "raw_score": float(report.raw_score),
            "sandbox_errors": int(
                sum(item.sandbox_errors for item in report.items)
            ),
        }
        for name, report in reports.items()
    } | {
        "truth_minus_Mpre_fidelity": float(
            reports["truth"].fidelity - reports["Mpre_grade"].fidelity
        ),
        "truth_minus_Mpre_raw": float(
            reports["truth"].raw_score - reports["Mpre_grade"].raw_score
        ),
    }


@dataclass(frozen=True)
class Data:
    grade: np.ndarray
    is_a: np.ndarray
    outcome: np.ndarray

    def take(self, indices: np.ndarray) -> "Data":
        return Data(self.grade[indices], self.is_a[indices], self.outcome[indices])


@dataclass(frozen=True)
class Fit:
    candidate: str
    vector: np.ndarray
    n_parameters: int
    log_likelihood: float


def _normal_logpdf(y, mean, sigma):
    return -0.5 * ((y - mean) / sigma) ** 2 - math.log(sigma) - 0.5 * math.log(2.0 * math.pi)


def _log_density(candidate: str, vector: np.ndarray, data: Data) -> np.ndarray:
    if candidate == "single":
        mean = vector[0] + vector[1] * data.grade
        return _normal_logpdf(data.outcome, mean, math.exp(vector[2]))
    if candidate == "class_split":
        mean_a = vector[0] + vector[1] * data.grade
        mean_b = vector[2] + vector[3] * data.grade
        mean = np.where(data.is_a, mean_a, mean_b)
        return _normal_logpdf(data.outcome, mean, math.exp(vector[4]))
    mean_1 = vector[0] + vector[1] * data.grade
    mean_2 = vector[2] + vector[3] * data.grade
    sigma = math.exp(vector[4])
    weight = 1.0 / (1.0 + math.exp(-vector[5]))
    terms = np.column_stack(
        [
            math.log(weight) + _normal_logpdf(data.outcome, mean_1, sigma),
            math.log(1.0 - weight)
            + _normal_logpdf(data.outcome, mean_2, sigma),
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


def _fit(candidate: str, data: Data, *, seed: int) -> Fit:
    if candidate == "single":
        x = np.column_stack([np.ones(len(data.grade)), data.grade])
        beta, sigma = _ols(x, data.outcome)
        vector = np.array([*beta, math.log(sigma)])
        return Fit(candidate, vector, 3, float(np.sum(_log_density(candidate, vector, data))))
    if candidate == "class_split":
        coefficients = []
        residuals = []
        for mask in (data.is_a, ~data.is_a):
            x = np.column_stack([np.ones(int(mask.sum())), data.grade[mask]])
            beta, _ = _ols(x, data.outcome[mask])
            coefficients.extend(beta)
            residuals.append(data.outcome[mask] - x @ beta)
        sigma = max(float(np.sqrt(np.mean(np.concatenate(residuals) ** 2))), 0.25)
        vector = np.array([*coefficients, math.log(sigma)])
        return Fit(candidate, vector, 5, float(np.sum(_log_density(candidate, vector, data))))

    grades = sorted(float(value) for value in np.unique(data.grade))
    if len(grades) != 2:
        raise ValueError("recoverability protocol requires exactly two grades")
    low_centers = _cluster_centers(data.outcome[data.grade == grades[0]])
    high_centers = _cluster_centers(data.outcome[data.grade == grades[1]])
    starts = []
    for high in (high_centers, high_centers[::-1]):
        components = []
        for low_value, high_value in zip(low_centers, high, strict=True):
            slope = (high_value - low_value) / (grades[1] - grades[0])
            components.extend([low_value - slope * grades[0], slope])
        for weight in (0.25, 0.5, 0.75):
            starts.append(
                np.array(
                    [
                        *components,
                        math.log(2.0),
                        math.log(weight / (1.0 - weight)),
                    ]
                )
            )
    rng = np.random.default_rng(seed)
    starts.extend(
        np.array([30.0, 0.0, 20.0, 2.0, math.log(2.0), 1.0])
        + rng.normal(0.0, [3.0, 0.5, 3.0, 0.5, 0.2, 0.5])
        for _ in range(6)
    )
    bounds = [(-80, 100), (-10, 10), (-80, 100), (-10, 10), (math.log(0.25), math.log(20)), (-5, 5)]
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
    return Fit(candidate, vector, 6, float(np.sum(_log_density(candidate, vector, data))))


def _protocol_ledger(world, *, seed: int) -> list[dict]:
    """Materialize exactly the affordable protocol through ledger-shaped rows."""
    ledger = []
    for index, config in enumerate(RECOVERABILITY_PROTOCOL["cells"]):
        frame = world.sample(
            _ns(config, site="north"),
            RECOVERABILITY_PROTOCOL["rows_per_cell"],
            seed + index,
        )
        ledger.append(
            {
                "sequence": index + 1,
                "turn": index + 1,
                "kind": "experiment",
                "source": None,
                "request": {
                    "config": config,
                    "context": {"site": "north"},
                    "n": RECOVERABILITY_PROTOCOL["rows_per_cell"],
                    "horizon": None,
                },
                "data": {
                    "columns": list(frame.columns),
                    "dtypes": [str(value) for value in frame.dtypes],
                    "data": frame.values.tolist(),
                },
            }
        )
    return ledger


def _recoverability(world, *, target: str, seed: int) -> dict:
    return recoverability_from_ledger(
        _protocol_ledger(world, seed=seed),
        target=target,
        folds=RECOVERABILITY_PROTOCOL["folds"],
        seed=seed + 100_000,
    )


def main() -> None:
    worlds = {name: load_world_module(path) for name, path in CASES.items()}
    descriptions = {
        name: build_world_server(path).describe() for name, path in CASES.items()
    }

    south_frames = {}
    for name, path in CASES.items():
        south_frames[name] = build_world_server(
            path, seed_offset=98_300
        ).observe("south_production_history", 600)

    nondiagnostic = []
    for seed in (17, 98_301, 401_003):
        for site, config in (
            ("south", {}),
            ("south", {"feedstock_grade": 3.0}),
            ("north", {}),
            ("north", {"humidity": 3.0}),
            ("north", {"humidity": 7.0}),
        ):
            frames = {
                name: world.sample(_ns(config, site=site), 400, seed)
                for name, world in worlds.items()
            }
            nondiagnostic.append(
                {
                    "site": site,
                    "config": config,
                    "seed": seed,
                    "all_visible_exact": all(
                        frame.equals(frames["retain"])
                        for frame in frames.values()
                    ),
                }
            )

    paired_rows = []
    association = []
    for seed in (29, 98_307, 410_003):
        for grade in (3.0, 7.0):
            regime = _ns(
                {"humidity": 5.0, "feedstock_grade": grade}, site="north"
            )
            local = worlds["local"].sample(regime, 20_000, seed)
            latent = worlds["latent"].sample(regime, 20_000, seed)
            local_audit = worlds["local"]._latent_sample(regime, 20_000, seed)
            latent_audit = worlds["latent"]._latent_sample(regime, 20_000, seed)
            paired_rows.append(
                {
                    "seed": seed,
                    "grade": grade,
                    "outputs_exact": local[OUTPUT_COLUMNS].equals(
                        latent[OUTPUT_COLUMNS]
                    ),
                    "class_counts_exact": local["batch_class"].value_counts().to_dict()
                    == latent["batch_class"].value_counts().to_dict(),
                    "full_view_differs": not local.equals(latent),
                }
            )
            association.append(
                {
                    "seed": seed,
                    "grade": grade,
                    "local_phi": float(
                        np.corrcoef(
                            local_audit["batch_class"].to_numpy() == "A",
                            local_audit["use_humidity"].to_numpy(),
                        )[0, 1]
                    ),
                    "latent_phi": float(
                        np.corrcoef(
                            latent_audit["batch_class"].to_numpy() == "A",
                            latent_audit["use_humidity"].to_numpy(),
                        )[0, 1]
                    ),
                }
            )

    fixed_context = []
    for name, world in worlds.items():
        for batch_class in ("A", "B"):
            frame = world.sample(
                _ns(
                    {"humidity": 5.0, "feedstock_grade": 3.0},
                    site="north",
                    batch_class=batch_class,
                ),
                1_000,
                98_311,
            )
            audit = world._latent_sample(
                _ns(
                    {"humidity": 5.0, "feedstock_grade": 3.0},
                    site="north",
                    batch_class=batch_class,
                ),
                20_000,
                98_311,
            )
            fixed_context.append(
                {
                    "pole": name,
                    "batch_class": batch_class,
                    "reported_only_requested_class": set(frame["batch_class"])
                    == {batch_class},
                    "humidity_mechanism_fraction": float(
                        audit["use_humidity"].mean()
                    ),
                }
            )

    signatures = {
        name: {
            batch_class: _delta(world, batch_class)
            for batch_class in ("A", "B")
        }
        for name, world in worlds.items()
    }
    expected = {
        "retain": {"A": 8.0, "B": 8.0},
        "revise": {"A": 0.0, "B": 0.0},
        "local": {"A": 0.0, "B": 8.0},
        "latent": {"A": 2.0, "B": 2.0},
    }

    truth_exact = []
    truth_south_class_invariance = []
    validation = {}
    for name, path in CASES.items():
        truth = _callable(_code(path, "truth_code.py"))
        validation[name] = build_world_server(path).validate_model(
            _code(path, "truth_code.py")
        )
        for seed in (41, 98_313):
            for site, batch_class, config in (
                ("south", "A", {"feedstock_grade": 7.0}),
                ("south", "B", {"humidity": 5.0, "feedstock_grade": 3.0}),
                ("north", "A", {"humidity": 5.0, "feedstock_grade": 3.0}),
                ("north", "B", {"humidity": 5.0, "feedstock_grade": 7.0}),
            ):
                regime = _ns(config, site=site, batch_class=batch_class)
                actual = worlds[name].sample(regime, 500, seed)[OUTPUT_COLUMNS]
                predicted = truth(regime, 500, seed)
                truth_exact.append(actual.equals(predicted))
        for config in ({}, {"humidity": 5.0, "feedstock_grade": 3.0}):
            a = truth(_ns(config, site="south", batch_class="A"), 1_000, 98_317)
            b = truth(_ns(config, site="south", batch_class="B"), 1_000, 98_317)
            truth_south_class_invariance.append(a.equals(b))

    battery_weights = {}
    for name, path in CASES.items():
        weights = {"A": 0.0, "B": 0.0, "unfixed": 0.0}
        for item in load_battery(path).items:
            batch_class = item.regime.context.get("batch_class", "unfixed")
            weights[batch_class] += float(item.weight)
        battery_weights[name] = weights

    margins = {
        name: _official_margin(CASES[name]) for name in ("local", "latent")
    }
    margin_values = [
        row["truth_minus_Mpre_fidelity"] for row in margins.values()
    ]

    robot_signatures = {
        robot: {
            batch_class: _model_delta(model_code(robot), batch_class)
            for batch_class in ("A", "B")
        }
        for robot in ("retain", "revise", "local", "latent")
    }
    robot_losses = {}
    for robot, predicted in robot_signatures.items():
        errors = {
            pole: float(
                np.mean(
                    [
                        abs(predicted[batch_class] - expected[pole][batch_class])
                        for batch_class in ("A", "B")
                    ]
                )
            )
            for pole in expected
        }
        robot_losses[robot] = {
            "mean_signature_error_by_pole": errors,
            "loses_at_least_one_pole": max(errors.values()) > 1.0,
        }

    recoverability = {
        "local": _recoverability(
            worlds["local"], target="local", seed=1_500_001
        ),
        "latent": _recoverability(
            worlds["latent"], target="latent", seed=1_600_001
        ),
    }

    fixed_lookup = {
        (row["pole"], row["batch_class"]): row for row in fixed_context
    }
    gates = {
        "brief_byte_identical": len(
            {(path / "brief.md").read_bytes() for path in CASES.values()}
        )
        == 1,
        "battery_byte_identical": len(
            {(path / "battery.json").read_bytes() for path in CASES.values()}
        )
        == 1,
        "agent_facing_meta_identical": len(
            {_key(_agent_meta(path)) for path in CASES.values()}
        )
        == 1,
        "describe_identical": all(
            value == descriptions["retain"] for value in descriptions.values()
        ),
        "deliverable_schema_is_two_outputs": all(
            description["schema"] == OUTPUT_COLUMNS
            for description in descriptions.values()
        ),
        "view_exposes_batch_class": all(
            description["sources"]["south_production_history"]["columns"]
            == ["batch_class", "feedstock", "outcome"]
            for description in descriptions.values()
        ),
        "first_south_evidence_exact_all": all(
            frame.equals(south_frames["retain"])
            for frame in south_frames.values()
        ),
        "first_south_evidence_has_both_classes": set(
            south_frames["retain"]["batch_class"]
        )
        == {"A", "B"},
        "nondiagnostic_visible_samples_exact": all(
            row["all_visible_exact"] for row in nondiagnostic
        ),
        "local_latent_outputs_exact": all(
            row["outputs_exact"] for row in paired_rows
        ),
        "local_latent_class_counts_exact": all(
            row["class_counts_exact"] for row in paired_rows
        ),
        "local_latent_treatment_changes_labels": all(
            row["full_view_differs"] for row in paired_rows
        ),
        "local_class_identifies_mechanism": all(
            row["local_phi"] > 0.999 for row in association
        ),
        "latent_class_is_independent": all(
            abs(row["latent_phi"]) < 0.03 for row in association
        ),
        "fixed_context_reports_only_requested_class": all(
            row["reported_only_requested_class"] for row in fixed_context
        ),
        "local_fixed_A_is_humidity": fixed_lookup[("local", "A")][
            "humidity_mechanism_fraction"
        ]
        == 1.0,
        "local_fixed_B_is_grade": fixed_lookup[("local", "B")][
            "humidity_mechanism_fraction"
        ]
        == 0.0,
        "latent_fixed_classes_remain_75_25": all(
            abs(
                fixed_lookup[("latent", batch_class)][
                    "humidity_mechanism_fraction"
                ]
                - 0.75
            )
            < 0.01
            for batch_class in ("A", "B")
        ),
        "class_conditional_truth_signatures": all(
            abs(signatures[pole][batch_class] - target) < 0.06
            for pole, classes in expected.items()
            for batch_class, target in classes.items()
        ),
        "battery_A_B_weight_equal": all(
            abs(weights["A"] - weights["B"]) < 1e-12
            and weights["A"] >= 0.3
            for weights in battery_weights.values()
        ),
        "truth_code_matches_world_outputs_exact": all(truth_exact),
        "truth_models_validate_with_two_output_contract": all(
            error is None for error in validation.values()
        ),
        "truth_South_invariant_to_batch_class": all(
            truth_south_class_invariance
        ),
        "local_latent_truth_margin_material": all(
            value > 0.01 for value in margin_values
        ),
        "local_latent_truth_margin_comparable": max(margin_values)
        / min(margin_values)
        < 1.5,
        "official_scoring_has_no_sandbox_errors": all(
            row[name]["sandbox_errors"] == 0
            for row in margins.values()
            for name in ("truth", "Mpre_grade")
        ),
        "each_fixed_robot_loses_somewhere": all(
            row["loses_at_least_one_pole"] for row in robot_losses.values()
        ),
        "recoverability_LOCAL_selects_class_split": (
            recoverability["local"]["informative"]
            and recoverability["local"]["recoverable"]
        ),
        "recoverability_LATENT_selects_latent_mixture": (
            recoverability["latent"]["informative"]
            and recoverability["latent"]["recoverable"]
        ),
        "recoverability_protocol_fits_post_South_budget": (
            RECOVERABILITY_PROTOCOL["total_rows"] <= 280
            and RECOVERABILITY_PROTOCOL["total_cost"]
            == RECOVERABILITY_PROTOCOL["minimum_post_South_budget_required"]
            and RECOVERABILITY_PROTOCOL["total_cost"] <= 1_000.0
        ),
    }
    payload = {
        "kind": "first_story_scm_transfer_topology_v1_certificate",
        "case_dirs": {name: str(path) for name, path in CASES.items()},
        "output_contract": OUTPUT_COLUMNS,
        "south_class_A_fraction": float(
            np.mean(
                south_frames["retain"]["batch_class"].to_numpy() == "A"
            )
        ),
        "nondiagnostic_pairing": nondiagnostic,
        "local_latent_diagnostic_pairing": paired_rows,
        "class_mechanism_association": association,
        "fixed_context": fixed_context,
        "class_conditional_delta_G_at_H5": signatures,
        "expected_delta_G_at_H5": expected,
        "battery_weights": battery_weights,
        "official_margin": margins,
        "robot_signatures": robot_signatures,
        "robot_losses": robot_losses,
        "recoverability_protocol": RECOVERABILITY_PROTOCOL,
        "recoverability": recoverability,
        "validation_errors": validation,
        "gates": gates,
        "all": all(gates.values()),
        "scope": (
            "The certificate covers truth-side South A/B invariance. A future "
            "runner must separately gate each donor Mpre for the same invariance."
        ),
    }
    print(json.dumps(payload, indent=2, allow_nan=False), flush=True)
    if not payload["all"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
