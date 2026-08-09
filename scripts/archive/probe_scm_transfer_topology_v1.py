"""Real-agent four-pole probe for structural belief revision.

The runner extends the lived South-to-North transfer protocol without changing
the v0 cases or their runner.  One agent forms an executable model in South,
chooses its first North experiment, and that exact cell is replayed into four
v1 worlds: RETAIN, REVISE, LOCAL (an observable A/B partition), and LATENT (the
same two mechanisms with an uninformative A/B label).

This is an exploratory runner, not a prevalence estimator.  In particular, a
LOCAL/LATENT contrast is interpretable only when the pre-fork model did not
already distinguish A from B and the frozen action exposes both classes.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import math
import sys
from collections import Counter
from pathlib import Path
from types import SimpleNamespace
from typing import Any

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from wager.contracts import Regime  # noqa: E402
from wager.harness.case_episode import build_world_server  # noqa: E402
from wager.reward.sandbox import SandboxedSubmission, SandboxError  # noqa: E402

from scripts import probe_first_story_scm_transfer_fork as transfer  # noqa: E402
from scripts.analyze_scm_topology_recoverability import (  # noqa: E402
    recoverability_from_ledger,
)
from scripts.probe_first_story_scm_fork import (  # noqa: E402
    _action_ledger,
    _action_record_exact,
    _experiment_events,
    _ledger_requests,
)


RETAIN = ROOT / "cases" / "first_story_scm_transfer_retain_v1"
REVISE = ROOT / "cases" / "first_story_scm_transfer_revise_v1"
LOCAL = ROOT / "cases" / "first_story_scm_transfer_local_v1"
LATENT = ROOT / "cases" / "first_story_scm_transfer_latent_v1"
OUT = ROOT / "scripts" / "out" / "first_story_scm_transfer_topology_v1"

BRANCH_SPECS = (
    ("retain", RETAIN),
    ("revise", REVISE),
    ("local", LOCAL),
    ("latent", LATENT),
)
BRANCH_BY_NAME = dict(BRANCH_SPECS)
BATCH_CLASSES = ("A", "B")
MODEL_COLUMNS = ["feedstock", "outcome"]
BASE_TRANSFER_TRANSITION = transfer.TRANSITION
NORTH_REVIEW_TURN_PROTOCOL = (
    " Before final submission, inspect at least one returned North evidence "
    "batch in a later turn: if a cell purchases North evidence, do not call "
    "env.submit in that same cell. This is a workflow checkpoint and does not "
    "imply that your model should change."
)

SYSTEM = transfer.BASE_SYSTEM + """

Site protocol: the project begins in South. During the South phase every
env.experiment call must identify site="south" in context. If the coordinator
later shifts work to North, North is the active target but South may still be
revisited for an explicit validation. Context may also select the routine
logistical view batch_class="A" or batch_class="B"; leaving it unspecified
samples the ordinary class mix. Do not use any other context keys. The
executable model must honor both advertised context fields because final
evaluation covers both sites and both logistical views.
"""


def _valid_context_for_site(context: Any, site: str) -> bool:
    """Allow site plus an optional, valid batch_class and nothing else."""
    if not isinstance(context, dict):
        return False
    if str(context.get("site", "")).lower() != site:
        return False
    if not set(context).issubset({"site", "batch_class"}):
        return False
    batch_class = context.get("batch_class")
    return batch_class is None or str(batch_class).upper() in BATCH_CLASSES


def _experiments_have_site(trajectory: list[dict], site: str) -> bool:
    return all(
        _valid_context_for_site(event["args"].get("context"), site)
        for event in _experiment_events(trajectory)
    )


def _ledger_is_south(ledger: list[dict]) -> bool:
    """All evidence before the fork must be South, with optional A/B context."""
    for row in ledger:
        if row.get("kind") == "observe":
            if row.get("source") != "south_production_history":
                return False
        elif row.get("kind") == "experiment":
            if not _valid_context_for_site(
                row.get("request", {}).get("context"), "south"
            ):
                return False
        else:
            return False
    return True


def _configure_reused_runner(*, require_north_review_turn: bool = False) -> None:
    """Point the validated v0 machinery at v1 inside this process only."""
    transfer.REVISE = REVISE
    transfer.RETAIN = RETAIN
    transfer.MIXED = LATENT
    transfer.SYSTEM = SYSTEM
    transfer.TRANSITION = BASE_TRANSFER_TRANSITION + (
        NORTH_REVIEW_TURN_PROTOCOL if require_north_review_turn else ""
    )
    transfer._experiments_have_site = _experiments_have_site
    transfer._ledger_is_south = _ledger_is_south


def _summary(values: np.ndarray) -> dict[str, float | None]:
    values = np.asarray(values, dtype=float)
    mean = float(np.mean(values))
    variance = float(np.var(values))
    sd = math.sqrt(max(variance, 0.0))
    skew = None
    if sd > 1e-12:
        skew = float(np.mean(((values - mean) / sd) ** 3))
    return {"mean": mean, "variance": variance, "sd": sd, "skew": skew}


def _wasserstein_equal_n(left: np.ndarray, right: np.ndarray) -> float:
    if len(left) != len(right):
        raise ValueError("Wasserstein inputs must have equal length")
    return float(np.mean(np.abs(np.sort(left) - np.sort(right))))


def _regime(
    site: str,
    batch_class: str,
    grade: float,
    humidity: float = 5.0,
) -> Regime:
    return Regime(
        config={"humidity": humidity, "feedstock_grade": grade},
        context={"site": site, "batch_class": batch_class},
        horizon=None,
    )


def _site_class_metrics(
    draws: dict[str, dict[str, np.ndarray]],
    truth: dict[str, dict[str, np.ndarray]] | None = None,
) -> dict[str, Any]:
    by_class: dict[str, dict[str, Any]] = {}
    for batch_class in BATCH_CLASSES:
        summaries = {
            key: _summary(values)
            for key, values in draws[batch_class].items()
        }
        skew_low = summaries["G3_H5"]["skew"]
        skew_high = summaries["G7_H5"]["skew"]
        a3 = None
        if skew_low is not None and skew_high is not None:
            a3 = float((skew_high - skew_low) / 2.0)
        row: dict[str, Any] = {
            "regimes": summaries,
            "delta_G_at_H5": float(
                summaries["G7_H5"]["mean"]
                - summaries["G3_H5"]["mean"]
            ),
            "delta_H_at_G5": float(
                summaries["G5_H7"]["mean"]
                - summaries["G5_H3"]["mean"]
            ),
            "oriented_skew_A3": a3,
        }
        if truth is not None:
            distances = []
            for regime_key in draws[batch_class]:
                truth_values = truth[batch_class][regime_key]
                scale = max(float(np.std(truth_values)), 1e-12)
                distances.append(
                    _wasserstein_equal_n(
                        draws[batch_class][regime_key], truth_values
                    )
                    / scale
                )
            row["normalized_W1_error"] = float(np.mean(distances))
        by_class[batch_class] = row

    class_level_gaps = []
    class_centered_shape_gaps = []
    for regime_key in ("G3_H5", "G7_H5", "G5_H3", "G5_H7"):
        pooled = np.concatenate(
            [
                draws[batch_class][regime_key]
                for batch_class in BATCH_CLASSES
            ]
        )
        scale = max(float(np.std(pooled)), 1e-12)
        values_a = draws["A"][regime_key]
        values_b = draws["B"][regime_key]
        class_level_gaps.append(
            _wasserstein_equal_n(
                values_a, values_b
            )
            / scale
        )
        centered_a = values_a - float(np.mean(values_a))
        centered_b = values_b - float(np.mean(values_b))
        centered_scale = max(
            float(np.std(np.concatenate([centered_a, centered_b]))),
            1e-12,
        )
        class_centered_shape_gaps.append(
            _wasserstein_equal_n(centered_a, centered_b) / centered_scale
        )
    return {
        "by_class": by_class,
        "delta_G_B_minus_A": float(
            by_class["B"]["delta_G_at_H5"]
            - by_class["A"]["delta_G_at_H5"]
        ),
        "delta_H_B_minus_A": float(
            by_class["B"]["delta_H_at_G5"]
            - by_class["A"]["delta_H_at_G5"]
        ),
        "mean_oriented_skew_A3": float(
            np.mean(
                [
                    row["oriented_skew_A3"]
                    for row in by_class.values()
                    if row["oriented_skew_A3"] is not None
                ]
            )
        ),
        "class_level_gap_W1": float(np.mean(class_level_gaps)),
        "class_centered_shape_gap_W1": float(
            np.mean(class_centered_shape_gaps)
        ),
    }


def class_conditioned_signature(
    code: str | None,
    case_dir: Path,
    *,
    n_samples: int,
    seed: int,
) -> dict[str, Any]:
    """Score an executable model and the hidden truth by site and A/B view."""
    if not code:
        return {"scoreable": False, "error": "missing artifact"}
    server = build_world_server(case_dir)
    model_draws: dict[str, dict[str, dict[str, np.ndarray]]] = {}
    truth_draws: dict[str, dict[str, dict[str, np.ndarray]]] = {}
    try:
        with SandboxedSubmission(
            code,
            MODEL_COLUMNS,
            timeout_s=15.0,
        ) as submission:
            for site_index, site in enumerate(("south", "north")):
                model_draws[site] = {}
                truth_draws[site] = {}
                for batch_class in BATCH_CLASSES:
                    model_draws[site][batch_class] = {}
                    truth_draws[site][batch_class] = {}
                    regimes = (
                        ("G3_H5", 3.0, 5.0),
                        ("G7_H5", 7.0, 5.0),
                        ("G5_H3", 5.0, 3.0),
                        ("G5_H7", 5.0, 7.0),
                    )
                    for regime_key, grade, humidity in regimes:
                        # Common random numbers across A/B and across the
                        # paired intervention contrasts isolate mechanism and
                        # shape from Monte-Carlo level noise.
                        run_seed = seed + 100 * site_index
                        regime = _regime(
                            site, batch_class, grade, humidity
                        )
                        predicted = submission.run(regime, n_samples, run_seed)
                        actual = server.world_sample(
                            SimpleNamespace(
                                config=dict(regime.config),
                                context=dict(regime.context),
                                horizon=None,
                            ),
                            n_samples,
                            run_seed,
                        )
                        model_draws[site][batch_class][regime_key] = (
                            predicted["outcome"].to_numpy(dtype=float)
                        )
                        truth_draws[site][batch_class][regime_key] = actual[
                            "outcome"
                        ].to_numpy(dtype=float)
    except (SandboxError, ValueError, KeyError) as exc:
        return {"scoreable": False, "error": repr(exc)}

    return {
        "scoreable": True,
        "error": None,
        "model": {
            site: _site_class_metrics(model_draws[site], truth_draws[site])
            for site in ("south", "north")
        },
        "truth": {
            site: _site_class_metrics(truth_draws[site])
            for site in ("south", "north")
        },
    }


def _safe_fraction(numerator: float, denominator: float) -> float | None:
    if abs(denominator) < 0.25:
        return None
    return float(numerator / denominator)


def _checkpoint_contrasts(
    signatures: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    result: dict[str, Any] = {}
    pre = signatures["M_pre"]
    for checkpoint in ("M_first", "M_last"):
        post = signatures[checkpoint]
        if not (pre.get("scoreable") and post.get("scoreable")):
            result[checkpoint] = {"scoreable": False}
            continue
        north_pre = pre["model"]["north"]
        north_post = post["model"]["north"]
        north_truth = post["truth"]["north"]
        by_class = {}
        for batch_class in BATCH_CLASSES:
            pre_delta = north_pre["by_class"][batch_class]["delta_G_at_H5"]
            post_delta = north_post["by_class"][batch_class]["delta_G_at_H5"]
            truth_delta = north_truth["by_class"][batch_class]["delta_G_at_H5"]
            by_class[batch_class] = _safe_fraction(
                pre_delta - post_delta,
                pre_delta - truth_delta,
            )
        separation_capture = _safe_fraction(
            north_post["delta_G_B_minus_A"] - north_pre["delta_G_B_minus_A"],
            north_truth["delta_G_B_minus_A"]
            - north_pre["delta_G_B_minus_A"],
        )
        a3_capture = _safe_fraction(
            north_post["mean_oriented_skew_A3"]
            - north_pre["mean_oriented_skew_A3"],
            north_truth["mean_oriented_skew_A3"]
            - north_pre["mean_oriented_skew_A3"],
        )
        result[checkpoint] = {
            "scoreable": True,
            "update_fraction_by_class": by_class,
            "observable_partition_capture": separation_capture,
            "latent_A3_capture": a3_capture,
            "north_error_by_class": {
                batch_class: north_post["by_class"][batch_class][
                    "normalized_W1_error"
                ]
                for batch_class in BATCH_CLASSES
            },
            "south_error_by_class": {
                batch_class: post["model"]["south"]["by_class"][batch_class][
                    "normalized_W1_error"
                ]
                for batch_class in BATCH_CLASSES
            },
        }
    return result


def add_topology_measurements(
    branch: dict,
    case_dir: Path,
    mpre: str,
    *,
    signature_n: int,
    signature_seed: int,
) -> None:
    artifacts = {
        "M_pre": mpre,
        "M_first": branch.get("first_changed_model"),
        "M_last": branch.get("last_scoreable_model"),
    }
    signatures = {
        checkpoint: class_conditioned_signature(
            code,
            case_dir,
            n_samples=signature_n,
            seed=signature_seed,
        )
        for checkpoint, code in artifacts.items()
    }
    branch["topology_signatures"] = signatures
    branch["topology_contrasts"] = _checkpoint_contrasts(signatures)


def _off_manifold(config: dict, tolerance: float) -> bool:
    if "feedstock_grade" not in config:
        return False
    if "humidity" not in config:
        return True
    return abs(
        float(config["feedstock_grade"])
        - (10.0 - float(config["humidity"]))
    ) > tolerance


def _frame_class_counts(frame, context: dict) -> dict[str, int]:
    if "batch_class" in frame.columns:
        counts = Counter(str(value).upper() for value in frame["batch_class"])
        return {name: int(counts.get(name, 0)) for name in BATCH_CLASSES}
    fixed = context.get("batch_class")
    if fixed is not None:
        return {
            name: int(len(frame) if str(fixed).upper() == name else 0)
            for name in BATCH_CLASSES
        }
    return {name: 0 for name in BATCH_CLASSES}


def classify_north_action_v1(
    trajectory: list[dict],
    *,
    seed_offset: int,
    expectation_n: int,
    diagnostic_delta_threshold: float,
    off_manifold_tolerance: float,
) -> dict[str, Any]:
    """Classify the frozen action against all four hidden worlds."""
    servers = {
        name: build_world_server(case_dir, seed_offset=seed_offset)
        for name, case_dir in BRANCH_SPECS
    }
    rows = []
    expected_coverage = Counter()
    pooled_local_latent_equal = []
    for index, event in enumerate(_experiment_events(trajectory)):
        args = event["args"]
        config = dict(args.get("config", {}))
        context = dict(args.get("context", {}))
        regime = SimpleNamespace(
            config=config,
            context=context,
            horizon=args.get("horizon"),
        )
        frames = {
            name: server.world_sample(
                regime,
                expectation_n,
                seed_offset + 810_000 + index,
            )
            for name, server in servers.items()
        }
        outcomes = {
            name: frame["outcome"].to_numpy(dtype=float)
            for name, frame in frames.items()
        }
        pairwise_rms = {
            f"{left}_vs_{right}": float(
                np.sqrt(np.mean((outcomes[left] - outcomes[right]) ** 2))
            )
            for left, right in (
                ("retain", "revise"),
                ("local", "latent"),
                ("local", "retain"),
                ("local", "revise"),
            )
        }
        pooled = "batch_class" not in context
        projected_equal = frames["local"][MODEL_COLUMNS].equals(
            frames["latent"][MODEL_COLUMNS]
        )
        if pooled:
            pooled_local_latent_equal.append(projected_equal)
        counts = _frame_class_counts(frames["local"], context)
        expected_coverage.update(counts)
        diagnostic = (
            _valid_context_for_site(context, "north")
            and _off_manifold(config, off_manifold_tolerance)
            and max(pairwise_rms.values()) >= diagnostic_delta_threshold
        )
        rows.append(
            {
                "index": index,
                "request": args,
                "context_valid": _valid_context_for_site(context, "north"),
                "off_manifold_G": _off_manifold(
                    config, off_manifold_tolerance
                ),
                "batch_context_mode": (
                    "pooled" if pooled else str(context["batch_class"]).upper()
                ),
                "expected_class_counts_at_large_n": counts,
                "pairwise_outcome_rms": pairwise_rms,
                "local_latent_feedstock_outcome_exact": projected_equal,
                "diagnostic": diagnostic,
            }
        )
    modes = {row["batch_context_mode"] for row in rows}
    return {
        "experiments": rows,
        "experiment_count": len(rows),
        "all_contexts_valid": bool(rows)
        and all(row["context_valid"] for row in rows),
        "diagnostic_indices": [
            row["index"] for row in rows if row["diagnostic"]
        ],
        "diagnostic": any(row["diagnostic"] for row in rows),
        "expected_class_coverage_at_large_n": {
            name: int(expected_coverage.get(name, 0))
            for name in BATCH_CLASSES
        },
        "expected_both_classes_at_large_n": all(
            expected_coverage.get(name, 0) > 0 for name in BATCH_CLASSES
        ),
        "batch_context_modes": sorted(modes),
        "pooled_local_latent_feedstock_outcome_exact": (
            bool(pooled_local_latent_equal)
            and all(pooled_local_latent_equal)
        ),
        "diagnostic_delta_threshold": diagnostic_delta_threshold,
        "off_manifold_tolerance": off_manifold_tolerance,
    }


def replay_frozen_action_only(
    case_dir: Path,
    prefix: dict,
    seed_offset: int,
) -> dict[str, Any]:
    """Replay through the frozen cell without constructing a continuation LLM.

    This is the only admissible source for pre-branch A/B coverage and finite
    recoverability gates: it uses the exact row counts and server seeds bought
    by the agent, rather than an expectation-sized synthetic campaign.
    """
    server = build_world_server(case_dir, seed_offset=seed_offset)
    action = prefix["selection"]
    preflight_requests = transfer._request_view(
        action["preflight_action_trajectory"]
    )
    with transfer.KernelClient(
        server, cell_timeout_s=transfer.CELL_TIMEOUT_S
    ) as kernel:
        replay_checks = transfer.replay_prefix_exact(server, prefix, kernel)
        ledger_after_prefix = server.export_evidence_ledger()
        notices = server.begin_turn(action["turn"])
        action_notices = copy.deepcopy(notices)
        for variable, frame in server.pop_deliveries():
            kernel.inject_dataframe(variable, frame)
        start = len(server.trajectory)
        result = kernel.run_cell(action["cell"])
        action_record = transfer.record(
            action["turn"],
            action["reply_text"],
            action["cell"],
            result,
            server,
            notices,
            start,
        )
    action_ledger = _action_ledger(
        {"evidence_ledger": server.export_evidence_ledger()},
        action["turn"],
    )
    action_requests = transfer._request_view(action_record["trajectory"])
    return {
        "case_id": case_dir.name,
        "replay_checks": replay_checks,
        "replay_exact": transfer._replay_checks_exact(replay_checks),
        "prefix_ledger_exact": (
            ledger_after_prefix == prefix["evidence_ledger"]
        ),
        "frozen_action_cell_sha256": hashlib.sha256(
            action["cell"].encode("utf-8")
        ).hexdigest(),
        "action_notices_exact": action_notices == action["notices"],
        "action_requests": action_requests,
        "action_requests_match_preflight": (
            action_requests == preflight_requests
        ),
        "action_record": action_record,
        "action_ledger": action_ledger,
        "terminal_after_action": server.terminal,
        "working_model_after_action": result.working_model,
        "error": result.error,
    }


def _ledger_projection(
    ledger: list[dict], columns: tuple[str, ...]
) -> list[dict[str, Any]]:
    result = []
    for row in ledger:
        data = row.get("data", {})
        names = list(data.get("columns", []))
        indexes = [names.index(name) for name in columns]
        result.append(
            {
                "request": row.get("request"),
                "columns": list(columns),
                "data": [
                    [values[index] for index in indexes]
                    for values in data.get("data", [])
                ],
            }
        )
    return result


def _ledger_class_counts(ledger: list[dict]) -> dict[str, int]:
    counts = Counter()
    for row in ledger:
        data = row.get("data", {})
        columns = list(data.get("columns", []))
        if "batch_class" in columns:
            index = columns.index("batch_class")
            counts.update(
                str(values[index]).upper() for values in data.get("data", [])
            )
        else:
            context = row.get("request", {}).get("context", {})
            fixed = context.get("batch_class")
            if fixed is not None:
                counts[str(fixed).upper()] += len(data.get("data", []))
    return {name: int(counts.get(name, 0)) for name in BATCH_CLASSES}


def _real_action_diagnostic_summary(
    ledger: list[dict],
    *,
    off_manifold_tolerance: float,
    min_rows_per_class: int,
) -> dict[str, Any]:
    """Summarize only real, paid North rows with G and H both fixed."""
    diagnostic_rows = []
    cells: dict[str, dict[str, Any]] = {}
    total_counts = Counter()
    for row in ledger:
        request = row.get("request", {})
        config = dict(request.get("config", {}))
        context = dict(request.get("context", {}))
        if not _valid_context_for_site(context, "north"):
            continue
        if not {"feedstock_grade", "humidity"}.issubset(config):
            continue
        if not _off_manifold(config, off_manifold_tolerance):
            continue
        counts = _ledger_class_counts([row])
        total_counts.update(counts)
        cell_key = json.dumps(
            {
                "feedstock_grade": float(config["feedstock_grade"]),
                "humidity": float(config["humidity"]),
            },
            sort_keys=True,
            separators=(",", ":"),
        )
        cell = cells.setdefault(
            cell_key,
            {
                "config": {
                    "feedstock_grade": float(config["feedstock_grade"]),
                    "humidity": float(config["humidity"]),
                },
                "rows": 0,
                "class_counts": Counter(),
            },
        )
        row_count = len(row.get("data", {}).get("data", []))
        cell["rows"] += row_count
        cell["class_counts"].update(counts)
        diagnostic_rows.append(row)
    serialized_cells = []
    for key in sorted(cells):
        cell = cells[key]
        serialized_cells.append(
            {
                "config": cell["config"],
                "rows": int(cell["rows"]),
                "class_counts": {
                    name: int(cell["class_counts"].get(name, 0))
                    for name in BATCH_CLASSES
                },
            }
        )
    class_counts = {
        name: int(total_counts.get(name, 0)) for name in BATCH_CLASSES
    }
    return {
        "diagnostic_ledger": diagnostic_rows,
        "diagnostic_rows": int(sum(class_counts.values())),
        "distinct_off_manifold_cells": len(cells),
        "cells": serialized_cells,
        "class_counts": class_counts,
        "min_rows_per_class": min_rows_per_class,
        "both_classes_have_minimum_real_rows": all(
            class_counts[name] >= min_rows_per_class
            for name in BATCH_CLASSES
        ),
        "at_least_two_distinct_off_manifold_cells": len(cells) >= 2,
    }


def _post_action_contexts_valid(branch: dict) -> bool:
    return all(
        _valid_context_for_site(event["args"].get("context"), site)
        for row in branch.get("trace", [])
        for event in _experiment_events(row.get("trajectory", []))
        for site in (str(event["args"].get("context", {}).get("site", "")).lower(),)
        if site in {"south", "north"}
    ) and all(
        str(event["args"].get("context", {}).get("site", "")).lower()
        in {"south", "north"}
        for row in branch.get("trace", [])
        for event in _experiment_events(row.get("trajectory", []))
    )


def physical_certificate(
    seed_offset: int,
    *,
    signature_n: int,
    tolerance: float = 0.20,
) -> dict[str, Any]:
    """Small zero-LLM check needed by this runner, not the full case certifier."""
    missing = [str(path) for _, path in BRANCH_SPECS if not path.is_dir()]
    if missing:
        return {
            "kind": "topology_v1_runner_preflight",
            "missing_cases": missing,
            "gates": {"all_case_directories_exist": False},
            "all": False,
        }
    descriptions = {
        name: build_world_server(case_dir, seed_offset=seed_offset).describe()
        for name, case_dir in BRANCH_SPECS
    }
    expected = {
        "retain": {"A": 8.0, "B": 8.0},
        "revise": {"A": 0.0, "B": 0.0},
        "local": {"A": 0.0, "B": 8.0},
        "latent": {"A": 2.0, "B": 2.0},
    }
    truth = {}
    batch_context_supported = True
    for pole, case_dir in BRANCH_SPECS:
        server = build_world_server(case_dir, seed_offset=seed_offset)
        truth[pole] = {}
        for site in ("south", "north"):
            truth[pole][site] = {}
            for batch_class in BATCH_CLASSES:
                try:
                    low = server.world_sample(
                        _regime(site, batch_class, 3.0),
                        signature_n,
                        seed_offset + 610_000,
                    )
                    high = server.world_sample(
                        _regime(site, batch_class, 7.0),
                        signature_n,
                        seed_offset + 610_000,
                    )
                except (KeyError, ValueError):
                    batch_context_supported = False
                    continue
                truth[pole][site][batch_class] = float(
                    high["outcome"].mean() - low["outcome"].mean()
                )
    south_correct = batch_context_supported and all(
        abs(truth[pole]["south"][batch_class] - 8.0) <= tolerance
        for pole, _ in BRANCH_SPECS
        for batch_class in BATCH_CLASSES
    )
    north_correct = batch_context_supported and all(
        abs(truth[pole]["north"][batch_class] - expected[pole][batch_class])
        <= tolerance
        for pole, _ in BRANCH_SPECS
        for batch_class in BATCH_CLASSES
    )
    gates = {
        "all_case_directories_exist": True,
        "agent_facing_descriptions_identical": all(
            value == descriptions["retain"] for value in descriptions.values()
        ),
        "batch_class_context_supported_all": batch_context_supported,
        "south_truth_grade_8_by_class_all": south_correct,
        "north_truth_matches_8_0_local_0_8_latent_2_2": north_correct,
    }
    return {
        "kind": "topology_v1_runner_preflight",
        "seed_offset": seed_offset,
        "signature_n": signature_n,
        "tolerance": tolerance,
        "truth_delta_G_at_H5": truth,
        "gates": gates,
        "all": all(gates.values()),
    }


def _atomic_write_json(target: Path, payload: dict[str, Any]) -> None:
    temporary = target.with_suffix(target.suffix + ".tmp")
    temporary.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    temporary.replace(target)


def _sanitized_prefix(prefix: dict) -> dict:
    result = copy.deepcopy(prefix)
    if result.get("selection"):
        result["selection"].pop("messages_through_action", None)
    return result


def _feedback_from_trace_row(row: dict[str, Any]) -> str:
    """Recreate ``feedback(result, server)`` byte-for-byte from a raw row."""
    result = row["cell_result"]
    prompt = (
        f"Kernel output (ok={result['ok']}, budget remaining="
        f"{float(row['budget_remaining']):.0f}):\n"
        + (result.get("stdout") or "(no stdout)")
    )
    if result.get("error"):
        prompt += "\nTRACEBACK:\n" + result["error"]
    return prompt + (
        "\n\nContinue the investigation. Keep `working_model` current when your "
        "predictive view changes, and call env.submit(code) when the work is "
        "sufficient."
    )


def reconstruct_messages_through_action(prefix: dict) -> dict[str, Any]:
    """Rebuild the FoundryChat message list using the original runner rules.

    The historical raw deliberately omitted ``messages_through_action``.  It
    did preserve every assistant reply, cell result, budget, phase, the full
    transition prompt, and the selected reply.  These are sufficient to
    replay the deterministic prompt-building code.  The checks below prove
    consistency with the current runner and raw; they do not claim an
    independent byte comparison against the omitted historical list.
    """
    trace = list(prefix.get("trace") or [])
    selection = prefix.get("selection") or {}
    formation = prefix.get("formation") or {}
    server = build_world_server(REVISE)
    initial = transfer.south_initial_prompt(server)
    formation_turn = formation.get("turn")
    formation_rows = [
        row for row in trace if row.get("turn") == formation_turn
    ]
    formation_feedback = (
        _feedback_from_trace_row(formation_rows[0])
        if len(formation_rows) == 1
        else None
    )
    expected_transition = (
        formation_feedback + "\n\n" + transfer.transition_prompt()
        if formation_feedback is not None
        else None
    )
    checks = {
        "trace_nonempty": bool(trace),
        "turns_strictly_increasing": [row.get("turn") for row in trace]
        == sorted({row.get("turn") for row in trace}),
        "exactly_one_formation_row": len(formation_rows) == 1,
        "formation_feedback_exact": (
            formation_feedback == formation.get("formation_feedback")
        ),
        "transition_prompt_exact": (
            expected_transition == prefix.get("transition_prompt")
        ),
        "selection_turn_follows_trace": bool(trace)
        and selection.get("turn") == trace[-1].get("turn") + 1,
        "trace_cells_extract_exact": all(
            transfer.extract_cell(row.get("reply_text", ""))
            == row.get("cell")
            for row in trace
        ),
        "selection_cell_extract_exact": (
            transfer.extract_cell(selection.get("reply_text", ""))
            == selection.get("cell")
        ),
        "selection_cell_hash_exact": hashlib.sha256(
            selection.get("cell", "").encode("utf-8")
        ).hexdigest()
        == selection.get("cell_sha256"),
    }

    messages: list[dict[str, str]] = [
        {"role": "system", "content": SYSTEM}
    ]
    current_prompt = initial
    transitioned = False
    formation_seen = False
    for row in trace:
        phase = row.get("phase")
        if phase == "north_search" and not transitioned:
            current_prompt = prefix.get("transition_prompt")
            transitioned = True
        messages.extend(
            [
                {"role": "user", "content": current_prompt},
                {"role": "assistant", "content": row["reply_text"]},
            ]
        )
        row_feedback = _feedback_from_trace_row(row)
        if phase == "south" and row.get("turn") == formation_turn:
            formation_seen = True
            current_prompt = prefix.get("transition_prompt")
            transitioned = True
        else:
            current_prompt = row_feedback

    checks.update(
        {
            "formation_seen_in_trace": formation_seen,
            "known_trace_phases": all(
                row.get("phase") in {"south", "north_search"}
                for row in trace
            ),
        }
    )
    messages.extend(
        [
            {"role": "user", "content": current_prompt},
            {"role": "assistant", "content": selection.get("reply_text", "")},
        ]
    )
    checks["message_count_exact"] = len(messages) == 1 + 2 * (
        len(trace) + 1
    )
    digest = hashlib.sha256(
        json.dumps(
            messages,
            ensure_ascii=False,
            separators=(",", ":"),
        ).encode("utf-8")
    ).hexdigest()
    return {
        "messages": messages,
        "checks": checks,
        "all": all(checks.values()),
        "messages_sha256": digest,
        "system_sha256": hashlib.sha256(SYSTEM.encode("utf-8")).hexdigest(),
        "initial_prompt_sha256": hashlib.sha256(
            initial.encode("utf-8")
        ).hexdigest(),
        "proof_scope": (
            "Exact reconstruction under current deterministic runner code; "
            "the sanitized historical raw contains no independent original "
            "message-list hash for byte-comparison."
        ),
    }


def load_resumable_prefix(
    raw_path: Path,
    *,
    expected_model: str,
    expected_seed: int,
) -> tuple[dict, dict[str, Any]]:
    payload = json.loads(raw_path.read_text(encoding="utf-8"))
    checks = {
        "kind_matches": payload.get("kind")
        == "exploratory_SCM_transfer_topology_v1",
        "model_matches": payload.get("model") == expected_model,
        "seed_matches": payload.get("seed_offset") == expected_seed,
        "prefix_present": isinstance(payload.get("prefix"), dict),
        "selection_present": bool(
            payload.get("prefix", {}).get("selection")
        ),
        "historical_messages_absent": (
            "messages_through_action"
            not in payload.get("prefix", {}).get("selection", {})
        ),
    }
    prefix = copy.deepcopy(payload.get("prefix") or {})
    reconstruction = reconstruct_messages_through_action(prefix)
    checks["message_reconstruction_checks_pass"] = reconstruction["all"]
    provenance = {
        "mode": "resume_reconstructed_prefix",
        "source": str(raw_path.resolve()),
        "source_sha256": hashlib.sha256(raw_path.read_bytes()).hexdigest(),
        "source_stage": payload.get("stage"),
        "source_prefix_abort": prefix.get("abort"),
        "checks": checks,
        "message_reconstruction": {
            key: value
            for key, value in reconstruction.items()
            if key != "messages"
        },
        "all": all(checks.values()),
    }
    if provenance["all"]:
        prefix["selection"]["messages_through_action"] = reconstruction[
            "messages"
        ]
        prefix["abort"] = "north_action_selected"
        prefix.pop("M_pre_topology_signature", None)
        prefix["resume_provenance"] = provenance
    return prefix, provenance


def _progress_payload(
    *,
    model: str,
    seed_offset: int,
    certificate: dict,
    prefix: dict,
    action_classification: dict | None,
    branches: dict,
    stage: str,
    gates: dict | None = None,
    frozen_action_preflight: dict | None = None,
) -> dict[str, Any]:
    return {
        "kind": "exploratory_SCM_transfer_topology_v1",
        "claim_class": (
            "observable_partition_vs_latent_structure_probe"
        ),
        "claim_scope": (
            "LOCAL tests use of an observable partition; LATENT jointly tests "
            "discovery, estimation, and executable representation of hidden laws"
        ),
        "model": model,
        "seed_offset": seed_offset,
        "branch_order": [name for name, _ in BRANCH_SPECS],
        "stage": stage,
        "complete": stage == "complete",
        "physical_certificate": certificate,
        "resume_provenance": prefix.get("resume_provenance"),
        "prefix": _sanitized_prefix(prefix),
        "action_classification": action_classification,
        "frozen_action_preflight": frozen_action_preflight or {},
        "branches": branches,
        "gates": gates or {},
        "all": bool(stage == "complete" and gates and all(gates.values())),
    }


def _write_early(
    target: Path,
    *,
    model: str,
    seed_offset: int,
    certificate: dict,
    prefix: dict,
    stage: str,
    gates: dict,
    action_classification: dict | None = None,
    frozen_action_preflight: dict | None = None,
) -> None:
    payload = _progress_payload(
        model=model,
        seed_offset=seed_offset,
        certificate=certificate,
        prefix=prefix,
        action_classification=action_classification,
        branches={},
        stage=stage,
        gates=gates,
        frozen_action_preflight=frozen_action_preflight,
    )
    _atomic_write_json(target, payload)
    print(
        json.dumps(
            {"out": str(target), "stage": stage, "gates": gates}, indent=2
        ),
        flush=True,
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", default="DeepSeek-V3.2")
    parser.add_argument("--seed-offset", type=int, default=98300)
    parser.add_argument("--belief-delta-threshold", type=float, default=3.0)
    parser.add_argument("--diagnostic-delta-threshold", type=float, default=1.0)
    parser.add_argument("--off-manifold-tolerance", type=float, default=0.25)
    parser.add_argument("--signature-n", type=int, default=4000)
    parser.add_argument("--action-expectation-n", type=int, default=20_000)
    parser.add_argument("--preclass-delta-tolerance", type=float, default=0.75)
    parser.add_argument("--preclass-w1-tolerance", type=float, default=0.25)
    parser.add_argument(
        "--preclass-shape-w1-tolerance", type=float, default=0.25
    )
    parser.add_argument("--min-action-class-rows", type=int, default=10)
    parser.add_argument("--max-south-turns", type=int, default=14)
    parser.add_argument("--max-north-search-turns", type=int, default=8)
    parser.add_argument("--max-turns", type=int, default=32)
    parser.add_argument(
        "--resume-prefix-json",
        type=Path,
        default=None,
        help=(
            "Reuse a sanitized topology-v1 prefix raw by deterministically "
            "reconstructing messages_through_action; makes no formation call."
        ),
    )
    parser.add_argument(
        "--preflight-only",
        action="store_true",
        help=(
            "Stop after real frozen-action replay and BIC+CV gates, before "
            "any continuation LLM branch."
        ),
    )
    parser.add_argument(
        "--require-north-review-turn",
        action="store_true",
        help=(
            "Add a neutral protocol boundary: North evidence bought in a "
            "cell must be inspected in a later turn before submission."
        ),
    )
    parser.add_argument(
        "--cert-only",
        action="store_true",
        help="Run the runner-level physical checks without constructing an LLM client.",
    )
    parser.add_argument("--out", type=Path, default=None)
    args = parser.parse_args()

    _configure_reused_runner(
        require_north_review_turn=args.require_north_review_turn
    )
    certificate = physical_certificate(
        args.seed_offset,
        signature_n=max(args.signature_n, 20_000),
    )
    if args.cert_only:
        print(json.dumps(certificate, indent=2), flush=True)
        if not certificate["all"]:
            raise SystemExit(1)
        return

    OUT.mkdir(parents=True, exist_ok=True)
    if args.resume_prefix_json is not None:
        default_suffix = (
            "_resumed_preflight" if args.preflight_only else "_resumed"
        )
    elif args.preflight_only:
        default_suffix = "_preflight"
    else:
        default_suffix = ""
    target = args.out or OUT / (
        f"probe_{args.model}_seed{args.seed_offset}{default_suffix}.json"
    )
    target.parent.mkdir(parents=True, exist_ok=True)
    if (
        args.resume_prefix_json is not None
        and target.resolve() == args.resume_prefix_json.resolve()
    ):
        raise ValueError("resume output must not overwrite its source raw")
    empty_prefix = {
        "abort": "physical_certificate_failed",
        "trace": [],
        "formation": None,
        "selection": None,
        "evidence_ledger": [],
        "tokens": 0,
    }
    if not certificate["all"]:
        _write_early(
            target,
            model=args.model,
            seed_offset=args.seed_offset,
            certificate=certificate,
            prefix=empty_prefix,
            stage="physical_certificate_failed",
            gates={"physical_certificate": False},
        )
        return

    resume_provenance = None
    if args.resume_prefix_json is not None:
        prefix, resume_provenance = load_resumable_prefix(
            args.resume_prefix_json,
            expected_model=args.model,
            expected_seed=args.seed_offset,
        )
        if not resume_provenance["all"]:
            _write_early(
                target,
                model=args.model,
                seed_offset=args.seed_offset,
                certificate=certificate,
                prefix=prefix,
                stage="resume_message_reconstruction_failed",
                gates={
                    "physical_certificate": certificate["all"],
                    "resume_message_reconstruction": False,
                },
            )
            return
    else:
        prefix = transfer.run_common_transfer_prefix(
            args.model,
            args.seed_offset,
            max_south_turns=args.max_south_turns,
            max_north_search_turns=args.max_north_search_turns,
            belief_delta_threshold=args.belief_delta_threshold,
            signature_n=args.signature_n,
        )
    prefix["require_north_review_turn"] = bool(
        args.require_north_review_turn
    )
    prefix_gates = {
        "physical_certificate": certificate["all"],
        "resume_message_reconstruction": (
            resume_provenance["all"]
            if resume_provenance is not None
            else True
        ),
        "transferable_model_formed": prefix["formation"] is not None,
        "south_prefix_evidence_present": bool(
            prefix.get("formation", {})
            and prefix["formation"].get("evidence_ledger")
        ),
        "all_pre_action_evidence_south": _ledger_is_south(
            prefix["evidence_ledger"]
        ),
        "north_action_selected": prefix["selection"] is not None,
    }
    if prefix["abort"] != "north_action_selected":
        _write_early(
            target,
            model=args.model,
            seed_offset=args.seed_offset,
            certificate=certificate,
            prefix=prefix,
            stage="prefix_gate_failed",
            gates=prefix_gates,
        )
        return

    mpre = prefix["selection"]["M_pre"]
    mpre_topology = class_conditioned_signature(
        mpre,
        REVISE,
        n_samples=args.signature_n,
        seed=args.seed_offset + 900_000,
    )
    prefix["M_pre_topology_signature"] = mpre_topology
    if mpre_topology.get("scoreable"):
        north_mpre = mpre_topology["model"]["north"]
        mpre_no_class_partition = (
            abs(north_mpre["delta_G_B_minus_A"])
            <= args.preclass_delta_tolerance
            and abs(north_mpre["delta_H_B_minus_A"])
            <= args.preclass_delta_tolerance
            and north_mpre["class_centered_shape_gap_W1"]
            <= args.preclass_shape_w1_tolerance
            and north_mpre["class_level_gap_W1"]
            <= args.preclass_w1_tolerance
        )
    else:
        mpre_no_class_partition = False
    prefix_gates.update(
        {
            "M_pre_topology_scoreable": mpre_topology.get("scoreable", False),
            "M_pre_did_not_already_partition_A_B": mpre_no_class_partition,
        }
    )

    action_classification = classify_north_action_v1(
        prefix["selection"]["preflight_action_trajectory"],
        seed_offset=args.seed_offset,
        expectation_n=args.action_expectation_n,
        diagnostic_delta_threshold=args.diagnostic_delta_threshold,
        off_manifold_tolerance=args.off_manifold_tolerance,
    )
    prefix["action_classification"] = action_classification
    prefix_gates.update(
        {
            "north_action_diagnostic": action_classification["diagnostic"],
            "north_action_contexts_valid": action_classification[
                "all_contexts_valid"
            ],
        }
    )
    if not all(prefix_gates.values()):
        prefix["abort"] = "north_action_or_M_pre_gate_failed"
        _write_early(
            target,
            model=args.model,
            seed_offset=args.seed_offset,
            certificate=certificate,
            prefix=prefix,
            stage="interpretability_gate_failed",
            gates=prefix_gates,
            action_classification=action_classification,
        )
        return

    frozen_action_preflight = {
        name: replay_frozen_action_only(
            BRANCH_BY_NAME[name], prefix, args.seed_offset
        )
        for name in ("local", "latent")
    }
    real_action_summaries = {
        name: _real_action_diagnostic_summary(
            row["action_ledger"],
            off_manifold_tolerance=args.off_manifold_tolerance,
            min_rows_per_class=args.min_action_class_rows,
        )
        for name, row in frozen_action_preflight.items()
    }
    for name, summary in real_action_summaries.items():
        frozen_action_preflight[name]["real_action_summary"] = summary
    real_action_recoverability = {
        name: recoverability_from_ledger(
            row["action_ledger"],
            target=name,
            folds=None,
            seed=args.seed_offset + 1_700_000 + index,
        )
        for index, (name, row) in enumerate(
            frozen_action_preflight.items()
        )
    }
    for name, result in real_action_recoverability.items():
        frozen_action_preflight[name]["recoverability"] = result
    local_preflight = frozen_action_preflight["local"]
    latent_preflight = frozen_action_preflight["latent"]
    local_requests = _ledger_requests(local_preflight["action_ledger"])
    prebranch_gates = {
        **prefix_gates,
        "prebranch_replay_exact_LOCAL_LATENT": all(
            row["replay_exact"]
            for row in frozen_action_preflight.values()
        ),
        "prebranch_prefix_ledger_exact_LOCAL_LATENT": all(
            row["prefix_ledger_exact"]
            for row in frozen_action_preflight.values()
        ),
        "prebranch_frozen_cell_exact_LOCAL_LATENT": all(
            row["frozen_action_cell_sha256"]
            == prefix["selection"]["cell_sha256"]
            for row in frozen_action_preflight.values()
        ),
        "prebranch_notices_exact_LOCAL_LATENT": all(
            row["action_notices_exact"]
            for row in frozen_action_preflight.values()
        ),
        "prebranch_requests_match_agent_action_LOCAL_LATENT": all(
            row["action_requests_match_preflight"]
            for row in frozen_action_preflight.values()
        ),
        "prebranch_same_requests_LOCAL_LATENT": bool(local_requests)
        and _ledger_requests(latent_preflight["action_ledger"])
        == local_requests,
        "prebranch_action_not_terminal_LOCAL_LATENT": not any(
            row["terminal_after_action"]
            for row in frozen_action_preflight.values()
        ),
        "real_A_B_counts_useful_LOCAL_LATENT": all(
            summary["both_classes_have_minimum_real_rows"]
            for summary in real_action_summaries.values()
        ),
        "real_two_off_manifold_cells_LOCAL_LATENT": all(
            summary["at_least_two_distinct_off_manifold_cells"]
            for summary in real_action_summaries.values()
        ),
        "real_action_recoverability_informative_LOCAL_LATENT": all(
            result.get("informative", False)
            for result in real_action_recoverability.values()
        ),
        "real_action_recoverability_BIC_CV_LOCAL_LATENT": all(
            result.get("recoverable", False)
            for result in real_action_recoverability.values()
        ),
    }
    if not all(prebranch_gates.values()):
        prefix["abort"] = "real_frozen_action_gate_failed"
        _write_early(
            target,
            model=args.model,
            seed_offset=args.seed_offset,
            certificate=certificate,
            prefix=prefix,
            stage="real_frozen_action_gate_failed",
            gates=prebranch_gates,
            action_classification=action_classification,
            frozen_action_preflight=frozen_action_preflight,
        )
        return

    if args.preflight_only:
        prefix["abort"] = "preflight_complete_no_continuation_requested"
        payload = _progress_payload(
            model=args.model,
            seed_offset=args.seed_offset,
            certificate=certificate,
            prefix=prefix,
            action_classification=action_classification,
            branches={},
            stage="preflight_complete",
            gates=prebranch_gates,
            frozen_action_preflight=frozen_action_preflight,
        )
        payload["preflight_all"] = all(prebranch_gates.values())
        payload["thresholds"] = {
            "belief_delta": args.belief_delta_threshold,
            "diagnostic_delta": args.diagnostic_delta_threshold,
            "off_manifold_tolerance": args.off_manifold_tolerance,
            "M_pre_mechanism_delta": args.preclass_delta_tolerance,
            "M_pre_level_W1": args.preclass_w1_tolerance,
            "M_pre_centered_shape_W1": (
                args.preclass_shape_w1_tolerance
            ),
            "minimum_real_action_rows_per_class": (
                args.min_action_class_rows
            ),
        }
        _atomic_write_json(target, payload)
        print(
            json.dumps(
                {
                    "out": str(target),
                    "stage": payload["stage"],
                    "preflight_all": payload["preflight_all"],
                    "gates": prebranch_gates,
                    "recoverability": {
                        name: row["recoverability"]
                        for name, row in frozen_action_preflight.items()
                    },
                },
                indent=2,
            ),
            flush=True,
        )
        return

    branches: dict[str, dict] = {}
    initial_payload = _progress_payload(
        model=args.model,
        seed_offset=args.seed_offset,
        certificate=certificate,
        prefix=prefix,
        action_classification=action_classification,
        branches=branches,
        stage="prefix_complete",
        gates=prebranch_gates,
        frozen_action_preflight=frozen_action_preflight,
    )
    _atomic_write_json(target, initial_payload)

    for index, (name, case_dir) in enumerate(BRANCH_SPECS):
        branch = transfer.replay_and_continue(
            case_dir,
            prefix,
            args.model,
            args.seed_offset,
            args.max_turns,
        )
        transfer.add_artifact_measurements(
            branch,
            case_dir,
            mpre,
            signature_n=args.signature_n,
            signature_seed=args.seed_offset + 910_000 + index,
        )
        add_topology_measurements(
            branch,
            case_dir,
            mpre,
            signature_n=args.signature_n,
            signature_seed=args.seed_offset + 920_000 + index,
        )
        branches[name] = branch
        _atomic_write_json(
            target,
            _progress_payload(
                model=args.model,
                seed_offset=args.seed_offset,
                certificate=certificate,
                prefix=prefix,
                action_classification=action_classification,
                branches=branches,
                stage=f"branch_{name}_complete",
                gates=prebranch_gates,
                frozen_action_preflight=frozen_action_preflight,
            ),
        )

    action_turn = prefix["selection"]["turn"]
    action_ledgers = {
        name: _action_ledger(branch, action_turn)
        for name, branch in branches.items()
    }
    retain_requests = _ledger_requests(action_ledgers["retain"])
    action_class_counts = {
        name: _ledger_class_counts(ledger)
        for name, ledger in action_ledgers.items()
    }
    pooled_action = action_classification["batch_context_modes"] == ["pooled"]
    local_latent_projected_equal = _ledger_projection(
        action_ledgers["local"], ("feedstock", "outcome")
    ) == _ledger_projection(
        action_ledgers["latent"], ("feedstock", "outcome")
    )
    gates = {
        **prebranch_gates,
        "replay_exact_all": all(
            branch["replay_exact"] for branch in branches.values()
        ),
        "prefix_ledger_exact_all": all(
            branch["prefix_ledger_exact"] for branch in branches.values()
        ),
        "frozen_action_cell_exact_all": all(
            branch["frozen_action_cell_sha256"]
            == prefix["selection"]["cell_sha256"]
            for branch in branches.values()
        ),
        "action_notices_exact_all": all(
            branch["action_notices_exact"] for branch in branches.values()
        ),
        "action_requests_match_preflight_all": all(
            branch["action_requests_match_preflight"]
            for branch in branches.values()
        ),
        "preflight_action_record_exact_revise": _action_record_exact(
            branches["revise"]["trace"][0],
            prefix["selection"]["preflight_action_record"],
        ),
        "preflight_action_ledger_exact_revise": (
            branches["revise"]["ledger_after_action"]
            == prefix["selection"]["preflight_evidence_ledger_after"]
        ),
        "full_replay_action_ledger_matches_prebranch_LOCAL_LATENT": all(
            action_ledgers[name]
            == frozen_action_preflight[name]["action_ledger"]
            for name in ("local", "latent")
        ),
        "same_action_ledger_requests_all": bool(retain_requests)
        and all(
            _ledger_requests(ledger) == retain_requests
            for ledger in action_ledgers.values()
        ),
        "action_results_retain_revise_differ": (
            action_ledgers["retain"] != action_ledgers["revise"]
        ),
        "pooled_LOCAL_LATENT_outcomes_exact_if_applicable": (
            local_latent_projected_equal if pooled_action else True
        ),
        "frozen_action_A_B_coverage_all": all(
            all(counts[batch_class] > 0 for batch_class in BATCH_CLASSES)
            for counts in action_class_counts.values()
        ),
        "post_action_contexts_valid_all": all(
            _post_action_contexts_valid(branch) for branch in branches.values()
        ),
        "accepted_all": all(branch["accepted"] for branch in branches.values()),
        "last_artifact_scoreable_all": all(
            branch["scores"]["M_last"].get("scoreable", False)
            for branch in branches.values()
        ),
        "topology_signatures_scoreable_all": all(
            branch["topology_signatures"]["M_last"].get("scoreable", False)
            for branch in branches.values()
        ),
    }
    payload = _progress_payload(
        model=args.model,
        seed_offset=args.seed_offset,
        certificate=certificate,
        prefix=prefix,
        action_classification=action_classification,
        branches=branches,
        stage="complete",
        gates=gates,
        frozen_action_preflight=frozen_action_preflight,
    )
    payload.update(
        {
            "thresholds": {
                "belief_delta": args.belief_delta_threshold,
                "diagnostic_delta": args.diagnostic_delta_threshold,
                "off_manifold_tolerance": args.off_manifold_tolerance,
                "M_pre_class_delta": args.preclass_delta_tolerance,
                "M_pre_class_W1": args.preclass_w1_tolerance,
                "M_pre_centered_shape_W1": (
                    args.preclass_shape_w1_tolerance
                ),
                "minimum_real_action_rows_per_class": (
                    args.min_action_class_rows
                ),
            },
            "action_ledgers": action_ledgers,
            "action_class_counts": action_class_counts,
            "local_latent_action_projection": {
                "pooled_action": pooled_action,
                "feedstock_outcome_exact": local_latent_projected_equal,
            },
        }
    )
    _atomic_write_json(target, payload)
    print(
        json.dumps(
            {
                "out": str(target),
                "all": payload["all"],
                "gates": gates,
                "abort": {
                    name: branch["abort"] for name, branch in branches.items()
                },
                "scores_R": {
                    name: {
                        checkpoint: score.get("R")
                        for checkpoint, score in branch["scores"].items()
                    }
                    for name, branch in branches.items()
                },
                "north_topology_last": {
                    name: branch["topology_signatures"]["M_last"]
                    .get("model", {})
                    .get("north")
                    for name, branch in branches.items()
                },
            },
            indent=2,
        ),
        flush=True,
    )


if __name__ == "__main__":
    main()
