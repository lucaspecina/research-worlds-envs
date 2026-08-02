"""Real-agent South-to-North fork with signed study-level conflict.

One agent forms an executable model from its own South investigation.  The
South notebook is then replayed into four hidden continuations.  No North
campaign is run by the agent: a routine four-study replication report is
served at handoff, after which the experiment window is declared closed.

Clean reports contain four studies whose likelihood-ratio signs agree with
the hidden North mechanism.  Conflict reports contain two studies of each
sign in the symmetric order correct/opposing/opposing/correct. Within each
truth pole, both reports have the same configured total exact evidence. This
is an exploratory content probe, not a prevalence estimate.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import math
import sys
from pathlib import Path
from statistics import NormalDist
from types import SimpleNamespace

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from wager.agent.cells import extract_cell  # noqa: E402
from wager.agent.llm_client import FoundryChat  # noqa: E402
from wager.contracts import ExperimentDesign  # noqa: E402
from wager.harness.case_episode import build_world_server  # noqa: E402
from wager.harness.episode import CELL_TIMEOUT_S, MAX_COMPLETION_TOKENS  # noqa: E402
from wager.harness.kernel_proc import KernelClient  # noqa: E402

from scripts.probe_first_story_causal_fork import (  # noqa: E402
    feedback,
    record,
)
from scripts.probe_first_story_scm_fork import (  # noqa: E402
    _experiment_events,
    _replay_checks_exact,
    replay_prefix_exact,
)
from scripts.probe_first_story_scm_transfer_fork import (  # noqa: E402
    REVISE,
    RETAIN,
    SYSTEM,
    _artifact_hash,
    _belief_gate,
    _ledger_is_south,
    add_artifact_measurements,
    both_site_signatures,
    south_initial_prompt,
    truth_site_signature,
)


OUT = ROOT / "scripts" / "out" / "first_story_scm_signed_study_conflict"
REPORT_VARIABLE = "north_replication_report"
REPORT_COLUMNS = [
    "study_id",
    "replication",
    "feedstock_grade",
    "humidity",
    "feedstock",
    "outcome",
]
ROWS_PER_GRADE = 3
GRADES = (3.0, 7.0)
HUMIDITY = 5.0
STUDY_COUNT = 4
TARGET_TOTAL_ABS_LLR = 10.0
CONFLICT_OPPOSING_ABS_LLR = 2.0
TARGET_TOTAL_TOLERANCE = 0.5
STUDY_TARGET_TOLERANCE = 0.1
STUDY_SEARCH_LIMIT = 20_000
REPORT_SEED_NAMESPACE = 88_000_000
REPORT_PACKAGE_STRIDE = 1_000_000
REPORT_BRANCH_STRIDE = 100_000

BRANCH_SPECS = (
    ("revise_clean", REVISE, "revise", "clean"),
    ("revise_conflict", REVISE, "revise", "conflict"),
    ("retain_clean", RETAIN, "retain", "clean"),
    ("retain_conflict", RETAIN, "retain", "conflict"),
)

REPORT_HANDOFF = (
    "South phase complete; work now shifts to North. As part of the routine "
    "handoff, four preregistered North replication studies are already loaded "
    f"as DataFrame `{REPORT_VARIABLE}`. Each study used assigned humidity and "
    "feedstock-grade controls and three replications per grade. The data-"
    "collection window is now closed: do not call env.observe or "
    "env.experiment. Inspect the report as part of the ordinary research "
    "record, keep `working_model` current if your predictive view warrants it, "
    "and submit the executable model when the assignment is sufficient. The "
    "final model must still cover both South and North."
)
SOUTH_ONLY_REMINDER = (
    "The coordinator has not opened North yet. Continue South work only; every "
    'env.experiment call in this phase must use context={"site": "south"}. Do '
    "not probe North until the coordinator announces the handoff."
)


def _configure_dose(
    *, total_abs_llr: float, opposing_abs_llr: float, search_limit: int
) -> None:
    global TARGET_TOTAL_ABS_LLR  # noqa: PLW0603
    global CONFLICT_OPPOSING_ABS_LLR  # noqa: PLW0603
    global STUDY_SEARCH_LIMIT  # noqa: PLW0603
    global REPORT_BRANCH_STRIDE  # noqa: PLW0603
    TARGET_TOTAL_ABS_LLR = total_abs_llr
    CONFLICT_OPPOSING_ABS_LLR = opposing_abs_llr
    STUDY_SEARCH_LIMIT = search_limit
    REPORT_BRANCH_STRIDE = STUDY_COUNT * STUDY_SEARCH_LIMIT + 10_000


def _study_targets(truth_pole: str, variant: str) -> tuple[float, ...]:
    sign = 1.0 if truth_pole == "revise" else -1.0
    if variant == "clean":
        return tuple(
            sign * TARGET_TOTAL_ABS_LLR / STUDY_COUNT
            for _ in range(STUDY_COUNT)
        )
    if variant == "conflict":
        # Symmetric order prevents the last study from being the one that
        # supports the old law in both truth poles.  Order reversal is a later
        # ablation, not part of this first positive-control package.
        correct = (
            TARGET_TOTAL_ABS_LLR + 2.0 * CONFLICT_OPPOSING_ABS_LLR
        ) / 2.0
        opposing = -CONFLICT_OPPOSING_ABS_LLR
        return tuple(
            sign * value for value in (correct, opposing, opposing, correct)
        )
    raise ValueError(f"unknown report variant {variant!r}")


def report_llr_revise_over_retain(frame: pd.DataFrame) -> float:
    """Exact log p(report|REVISE) - log p(report|RETAIN)."""
    grade = frame["feedstock_grade"].to_numpy(dtype=float)
    humidity = frame["humidity"].to_numpy(dtype=float)
    outcome = frame["outcome"].to_numpy(dtype=float)
    mu_revise = 40.0 - 2.0 * humidity
    mu_retain = 20.0 + 2.0 * grade
    # Both reference mechanisms use Normal(0, 2^2) outcome noise.
    return float(
        np.sum(
            np.square(outcome - mu_retain)
            - np.square(outcome - mu_revise)
        )
        / 8.0
    )


def _frame_digest(frame: pd.DataFrame) -> str:
    payload = frame.to_json(orient="split", double_precision=15)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def _design_digest(frame: pd.DataFrame) -> str:
    design = frame[
        ["study_id", "replication", "feedstock_grade", "humidity"]
    ]
    return _frame_digest(design)


def _sample_study(server, study_id: int, base_seed: int) -> pd.DataFrame:
    frames = []
    for grade_index, grade in enumerate(GRADES):
        sample_seed = base_seed + 17 * grade_index
        observed = server.world_sample(
            SimpleNamespace(
                config={
                    "feedstock_grade": grade,
                    "humidity": HUMIDITY,
                },
                context={"site": "north"},
                horizon=None,
            ),
            ROWS_PER_GRADE,
            sample_seed,
        )
        frame = observed.copy()
        frame.insert(0, "humidity", HUMIDITY)
        frame.insert(0, "feedstock_grade", grade)
        frame.insert(0, "replication", np.arange(1, len(frame) + 1))
        frame.insert(0, "study_id", study_id)
        frames.append(frame[REPORT_COLUMNS])
    return pd.concat(frames, ignore_index=True)


def _fast_study_llr(truth_pole: str, base_seed: int) -> float:
    """Exact world algebra for seed search, without constructing DataFrames."""
    total = 0.0
    for grade_index, grade in enumerate(GRADES):
        rng = np.random.default_rng(base_seed + 17 * grade_index)
        # Match world._draw_exogenous exactly: all arrays are drawn before the
        # site/mechanism branch, even though only eps_y enters this LLR.
        rng.uniform(0.0, 1.0, ROWS_PER_GRADE)
        rng.normal(0.0, 0.5, ROWS_PER_GRADE)
        rng.normal(0.0, 0.9, ROWS_PER_GRADE)
        eps_y = rng.normal(0.0, 2.0, ROWS_PER_GRADE)
        mu_revise = 40.0 - 2.0 * HUMIDITY
        mu_retain = 20.0 + 2.0 * grade
        truth_mean = mu_revise if truth_pole == "revise" else mu_retain
        outcome = truth_mean + eps_y
        total += float(
            np.sum(
                np.square(outcome - mu_retain)
                - np.square(outcome - mu_revise)
            )
            / 8.0
        )
    return total


def _select_study(
    server,
    *,
    truth_pole: str,
    study_id: int,
    target_llr: float,
    start_seed: int,
) -> tuple[pd.DataFrame, dict]:
    selected: tuple[float, int, float, pd.DataFrame, int] | None = None
    for base_seed in range(start_seed, start_seed + STUDY_SEARCH_LIMIT):
        llr = _fast_study_llr(truth_pole, base_seed)
        error = abs(llr - target_llr)
        if error <= STUDY_TARGET_TOLERANCE:
            frame = _sample_study(server, study_id, base_seed)
            world_llr = report_llr_revise_over_retain(frame)
            if not math.isclose(llr, world_llr, rel_tol=0.0, abs_tol=1e-12):
                raise RuntimeError("fast LLR search diverged from world sample")
            selected = (
                error,
                base_seed,
                llr,
                frame,
                base_seed - start_seed + 1,
            )
            break
    if selected is None:
        raise RuntimeError(
            f"no signed study found near LLR {target_llr:+.3f} "
            f"from seed {start_seed}"
        )
    error, base_seed, llr, frame, candidates_until_selection = selected
    # With three rows at each of G=3 and G=7, the exact raw LLR is Normal
    # (+12, 24) under REVISE and Normal(-12, 24) under RETAIN.
    llr_distribution = NormalDist(
        mu=12.0 if truth_pole == "revise" else -12.0,
        sigma=math.sqrt(24.0),
    )
    theoretical_rate = (
        llr_distribution.cdf(target_llr + STUDY_TARGET_TOLERANCE)
        - llr_distribution.cdf(target_llr - STUDY_TARGET_TOLERANCE)
    )
    return frame, {
        "study_id": study_id,
        "base_seed": base_seed,
        "grade_seeds": [base_seed, base_seed + 17],
        "target_llr": target_llr,
        "observed_llr": llr,
        "absolute_target_error": error,
        "fast_search_llr_matches_world": True,
        "search_window_start": start_seed,
        "search_window_size": STUDY_SEARCH_LIMIT,
        "candidates_until_selection": candidates_until_selection,
        "exact_theoretical_acceptance_rate": theoretical_rate,
        "exact_theoretical_expected_candidates": 1.0 / theoretical_rate,
        "observed_selection_effort_rate": 1.0 / candidates_until_selection,
        "selection_rule": "first seed within fixed absolute target tolerance",
    }


def build_replication_report(
    case_dir: Path,
    truth_pole: str,
    variant: str,
    package_seed: int,
    *,
    branch_index: int,
) -> tuple[pd.DataFrame, list[dict]]:
    """Select four deterministic, truth-generated studies by signed LLR."""
    server = build_world_server(case_dir)
    frames = []
    selections = []
    targets = _study_targets(truth_pole, variant)
    for index, target in enumerate(targets):
        # Non-overlapping deterministic search windows for all four branches.
        start_seed = (
            REPORT_SEED_NAMESPACE
            + package_seed * REPORT_PACKAGE_STRIDE
            + branch_index * REPORT_BRANCH_STRIDE
            + index * STUDY_SEARCH_LIMIT
        )
        frame, selection = _select_study(
            server,
            truth_pole=truth_pole,
            study_id=index + 1,
            target_llr=target,
            start_seed=start_seed,
        )
        frames.append(frame)
        selections.append(selection)
    return pd.concat(frames, ignore_index=True), selections


def rebuild_report(case_dir: Path, selections: list[dict]) -> pd.DataFrame:
    server = build_world_server(case_dir)
    return pd.concat(
        [
            _sample_study(
                server,
                int(selection["study_id"]),
                int(selection["base_seed"]),
            )
            for selection in selections
        ],
        ignore_index=True,
    )


def report_audit(
    frame: pd.DataFrame,
    selections: list[dict],
    *,
    truth_pole: str,
    variant: str,
) -> dict:
    truth_sign = 1 if truth_pole == "revise" else -1
    study_rows = []
    for study_id in range(1, STUDY_COUNT + 1):
        block = frame.loc[frame["study_id"] == study_id]
        llr = report_llr_revise_over_retain(block)
        sign = 1 if llr > 0 else (-1 if llr < 0 else 0)
        grade_counts = {
            str(int(grade)): int((block["feedstock_grade"] == grade).sum())
            for grade in GRADES
        }
        study_rows.append({
            "study_id": study_id,
            "rows": int(len(block)),
            "grade_counts": grade_counts,
            "humidity_values": sorted(
                float(value) for value in block["humidity"].unique()
            ),
            "llr_revise_over_retain": llr,
            "sign": sign,
            "sign_relative_to_truth": (
                "correct" if sign == truth_sign else "opposing"
            ),
        })
    total_llr = report_llr_revise_over_retain(frame)
    pooled_grade_means = {
        str(int(grade)): float(
            frame.loc[frame["feedstock_grade"] == grade, "outcome"].mean()
        )
        for grade in GRADES
    }
    pooled_delta = pooled_grade_means["7"] - pooled_grade_means["3"]
    rows_per_grade_total = STUDY_COUNT * ROWS_PER_GRADE
    # For this balanced G=3/G=7,H=5 design:
    # total LLR = 4*n_per_grade - n_per_grade*delta_pooled.
    llr_implied_delta = 4.0 - total_llr / rows_per_grade_total
    expected_signs = (
        ["correct"] * STUDY_COUNT
        if variant == "clean"
        else ["correct", "opposing", "opposing", "correct"]
    )
    return {
        "truth_pole": truth_pole,
        "variant": variant,
        "rows": int(len(frame)),
        "columns": list(frame.columns),
        "dtypes": [str(dtype) for dtype in frame.dtypes],
        "sha256": _frame_digest(frame),
        "design_sha256": _design_digest(frame),
        "selections": selections,
        "selection_effort": {
            "fixed_search_window_per_study": STUDY_SEARCH_LIMIT,
            "target_tolerance_per_study": STUDY_TARGET_TOLERANCE,
            "candidates_until_selection": [
                row["candidates_until_selection"] for row in selections
            ],
            "exact_theoretical_acceptance_rates": [
                row["exact_theoretical_acceptance_rate"]
                for row in selections
            ],
            "exact_theoretical_expected_candidates": [
                row["exact_theoretical_expected_candidates"]
                for row in selections
            ],
            "observed_selection_effort_rates": [
                row["observed_selection_effort_rate"]
                for row in selections
            ],
        },
        "studies": study_rows,
        "study_signs": [row["sign_relative_to_truth"] for row in study_rows],
        "total_llr_revise_over_retain": total_llr,
        "finite_report_reference": {
            "kind": "pooled_G7_minus_G3_MLE_from_served_rows",
            "grade_outcome_means": pooled_grade_means,
            "delta_outcome_G7_minus_G3": pooled_delta,
            "delta_implied_by_exact_llr": llr_implied_delta,
            "algebra_matches": math.isclose(
                pooled_delta,
                llr_implied_delta,
                rel_tol=0.0,
                abs_tol=1e-12,
            ),
            "normative_status": (
                "finite-data likelihood reference, not truth and not a "
                "posterior that incorporates the agent's unknown prior"
            ),
        },
        "target_total_llr": truth_sign * TARGET_TOTAL_ABS_LLR,
        "geometry_exact": (
            len(frame) == STUDY_COUNT * len(GRADES) * ROWS_PER_GRADE
            and list(frame.columns) == REPORT_COLUMNS
            and all(
                row["rows"] == len(GRADES) * ROWS_PER_GRADE
                and row["grade_counts"] == {"3": 3, "7": 3}
                and row["humidity_values"] == [HUMIDITY]
                for row in study_rows
            )
        ),
        "sign_pattern_exact": (
            [row["sign_relative_to_truth"] for row in study_rows]
            == expected_signs
        ),
        "total_llr_in_target": (
            abs(total_llr - truth_sign * TARGET_TOTAL_ABS_LLR)
            <= TARGET_TOTAL_TOLERANCE
        ),
    }


def build_all_reports(package_seed: int) -> dict[str, dict]:
    reports = {}
    for branch_index, (name, case_dir, truth_pole, variant) in enumerate(
        BRANCH_SPECS
    ):
        frame, selections = build_replication_report(
            case_dir,
            truth_pole,
            variant,
            package_seed,
            branch_index=branch_index,
        )
        reports[name] = {
            "frame": frame,
            "selections": selections,
            "audit": report_audit(
                frame,
                selections,
                truth_pole=truth_pole,
                variant=variant,
            ),
        }
    return reports


def inject_replication_report(
    server,
    kernel: KernelClient,
    frame: pd.DataFrame,
    *,
    turn: int,
) -> dict:
    budget_before = float(server.budget_remaining)
    kernel.inject_dataframe(REPORT_VARIABLE, frame)
    server._record_evidence(  # noqa: SLF001 - deliberate probe audit entry
        "event_report",
        source=REPORT_VARIABLE,
        request={"studies": STUDY_COUNT, "n": len(frame)},
        frame=frame,
        delivery_variable=REPORT_VARIABLE,
        turn=turn,
    )
    budget_after = float(server.budget_remaining)
    return {
        "variable": REPORT_VARIABLE,
        "turn": turn,
        "budget_before": budget_before,
        "budget_after": budget_after,
        "free": budget_before == budget_after,
        "sha256": _frame_digest(frame),
    }


def _closed_experiment_guard(design, turn, fired_events) -> None:
    del design, turn, fired_events
    raise ValueError("the handoff data-collection window is closed")


def run_common_south_prefix(
    model: str,
    seed_offset: int,
    *,
    max_south_turns: int,
    belief_delta_threshold: float,
    signature_n: int,
) -> dict:
    """Let one real agent form M_pre solely from its South work."""
    server = build_world_server(REVISE, seed_offset=seed_offset)
    chat = FoundryChat(
        system=SYSTEM,
        model=model,
        max_completion_tokens=MAX_COMPLETION_TOKENS,
    )
    trace = []
    prompt = south_initial_prompt(server) + "\n\n" + SOUTH_ONLY_REMINDER
    formation = None
    abort = "no_transferable_model_after_max_south_turns"

    with KernelClient(server, cell_timeout_s=CELL_TIMEOUT_S) as kernel:
        for turn in range(1, max_south_turns + 1):
            notices = server.begin_turn(turn)
            for variable, frame in server.pop_deliveries():
                kernel.inject_dataframe(variable, frame)
            reply = chat.ask(prompt)
            cell = extract_cell(reply.content)
            if cell is None:
                abort = "no_cell_during_south"
                break
            start = len(server.trajectory)
            result = kernel.run_cell(cell)
            row = record(
                turn, reply.content, cell, result, server, notices, start
            )
            row["phase"] = "south"
            trace.append(row)

            if _experiment_events(row["trajectory"]) and not all(
                event["args"].get("context") == {"site": "south"}
                for event in _experiment_events(row["trajectory"])
            ):
                abort = "non_south_experiment_before_handoff"
                break
            ledger = server.export_evidence_ledger()
            if not _ledger_is_south(ledger):
                abort = "non_south_evidence_before_handoff"
                break
            if server.terminal:
                abort = "submitted_before_handoff"
                break
            if result.error and result.error.startswith("cell exceeded "):
                abort = "cell_timeout_during_south"
                break

            code = result.working_model
            validation_error = (
                "missing artifact" if code is None else server.validate_model(code)
            )
            signatures = both_site_signatures(
                code,
                server.columns,
                n_samples=signature_n,
                seed=seed_offset + 710_000,
            )
            if (
                validation_error is None
                and bool(ledger)
                and _belief_gate(signatures, belief_delta_threshold)
            ):
                formation = {
                    "turn": turn,
                    "M_pre": code,
                    "M_pre_sha256": _artifact_hash(code),
                    "signatures": signatures,
                    "validation_error": None,
                    "evidence_ledger": ledger,
                    "formation_feedback": feedback(result, server),
                    "messages_through_formation": copy.deepcopy(chat.messages),
                }
                abort = "transferable_model_formed"
                break
            prompt = feedback(result, server) + "\n\n" + SOUTH_ONLY_REMINDER

    return {
        "abort": abort,
        "trace": trace,
        "formation": formation,
        "evidence_ledger": (
            formation["evidence_ledger"]
            if formation is not None
            else server.export_evidence_ledger()
        ),
        "belief_delta_threshold": belief_delta_threshold,
        "tokens": chat.usage.total_tokens,
        "llm_turn_usage": [
            {
                "prompt_tokens": item.prompt_tokens,
                "completion_tokens": item.completion_tokens,
                "reasoning_tokens": item.reasoning_tokens,
                "latency_s": item.latency_s,
            }
            for item in chat.turns
        ],
    }


def replay_report_and_continue(
    case_dir: Path,
    report: dict,
    prefix: dict,
    model: str,
    seed_offset: int,
    max_turns: int,
) -> dict:
    """Replay South, serve one report, and continue without a North campaign."""
    server = build_world_server(case_dir, seed_offset=seed_offset)
    formation = prefix["formation"]
    branch_trace = []
    handoff_turn = int(formation["turn"]) + 1
    handoff_prompt = formation["formation_feedback"] + "\n\n" + REPORT_HANDOFF

    with KernelClient(server, cell_timeout_s=CELL_TIMEOUT_S) as kernel:
        replay_checks = replay_prefix_exact(server, prefix, kernel)
        ledger_after_prefix = server.export_evidence_ledger()
        notices = server.begin_turn(handoff_turn)
        deliveries = server.pop_deliveries()
        handoff_builtin_delivery_count = len(deliveries)
        for variable, delivered in deliveries:
            kernel.inject_dataframe(variable, delivered)
        injection = inject_replication_report(
            server,
            kernel,
            report["frame"],
            turn=handoff_turn,
        )
        server.experiment_guard = _closed_experiment_guard

        def closed_observe(source: str, n: int):
            del source, n
            raise ValueError("the handoff data-collection window is closed")

        server.observe = closed_observe

        chat = FoundryChat(
            system=SYSTEM,
            model=model,
            max_completion_tokens=MAX_COMPLETION_TOKENS,
        )
        chat.messages = copy.deepcopy(formation["messages_through_formation"])
        prompt = handoff_prompt
        abort = "max_turns"
        for turn in range(handoff_turn, max_turns + 1):
            if turn != handoff_turn:
                notices = server.begin_turn(turn)
                deliveries = server.pop_deliveries()
                for variable, delivered in deliveries:
                    kernel.inject_dataframe(variable, delivered)
            reply = chat.ask(prompt)
            cell = extract_cell(reply.content)
            if cell is None:
                abort = "no_cell"
                break
            start = len(server.trajectory)
            result = kernel.run_cell(cell)
            row = record(
                turn, reply.content, cell, result, server, notices, start
            )
            row["phase"] = "post_replication_report"
            branch_trace.append(row)
            if server.terminal:
                abort = "submitted"
                break
            if result.error and result.error.startswith("cell exceeded "):
                abort = "cell_timeout"
                break
            prompt = feedback(result, server)

        transcript = copy.deepcopy(chat.messages)
        tokens = chat.usage.total_tokens
        turn_usage = [
            {
                "prompt_tokens": item.prompt_tokens,
                "completion_tokens": item.completion_tokens,
                "reasoning_tokens": item.reasoning_tokens,
                "latency_s": item.latency_s,
            }
            for item in chat.turns
        ]

    final = server.result or {}
    mpre = formation["M_pre"]
    first_post_report = next(
        (
            row["working_model"]["code"]
            for row in branch_trace
            if row["working_model"]["code"]
        ),
        mpre,
    )
    first_changed = next(
        (
            row["working_model"]["code"]
            for row in branch_trace
            if row["working_model"]["code"]
            and row["working_model"]["code"] != mpre
        ),
        None,
    )
    last_code = next(
        (
            row["working_model"]["code"]
            for row in reversed(branch_trace)
            if row["working_model"]["code"]
        ),
        mpre,
    )
    post_report_experiments = [
        event
        for row in branch_trace
        for event in _experiment_events(row["trajectory"])
    ]
    full_ledger = server.export_evidence_ledger()
    post_prefix_ledger = full_ledger[len(prefix["evidence_ledger"]):]
    return {
        "case_id": case_dir.name,
        "report_audit": report["audit"],
        "report_injection": injection,
        "handoff_turn": handoff_turn,
        "handoff_prompt": REPORT_HANDOFF,
        "handoff_prompt_sha256": hashlib.sha256(
            REPORT_HANDOFF.encode("utf-8")
        ).hexdigest(),
        "builtin_delivery_count_at_handoff": handoff_builtin_delivery_count,
        "replay_checks": replay_checks,
        "replay_exact": _replay_checks_exact(replay_checks),
        "prefix_ledger_after_replay": ledger_after_prefix,
        "prefix_ledger_exact": ledger_after_prefix == prefix["evidence_ledger"],
        "abort": abort,
        "accepted": server.terminal,
        "R": final.get("R"),
        "submission_code": final.get("code"),
        # ``add_artifact_measurements`` historically reads this key as
        # M_first.  Here M_first is the immediate first post-report artifact,
        # including M_pre when the agent deliberately leaves it unchanged.
        "first_changed_model": first_post_report,
        "M_first_model": first_post_report,
        "first_distinct_model": first_changed,
        "M_first_is_M_pre": first_post_report == mpre,
        "M_first_turn": branch_trace[0]["turn"] if branch_trace else None,
        "last_working_model": last_code,
        "last_working_model_code": last_code,
        "trace": branch_trace,
        "transcript": transcript,
        "evidence_ledger": full_ledger,
        "post_report_non_report_evidence": [
            row
            for row in post_prefix_ledger
            if row["kind"] in {"observe", "experiment"}
        ],
        "collection_window_enforced": True,
        "post_report_experiment_count": len(post_report_experiments),
        "post_report_experiments": post_report_experiments,
        "report_referenced_in_cells": any(
            REPORT_VARIABLE in row["cell"] for row in branch_trace
        ),
        "report_referenced_in_first_cell": bool(
            branch_trace and REPORT_VARIABLE in branch_trace[0]["cell"]
        ),
        "tokens_continuation": tokens,
        "llm_turn_usage": turn_usage,
    }


def _update_fraction(branch: dict, checkpoint: str) -> float | None:
    """Secondary coordinate toward hidden truth (not the finite-data norm)."""
    signatures = branch["signatures"]
    pre = signatures["M_pre_north"]
    post = signatures[f"M_{checkpoint}_north"]
    truth = signatures["truth_north"]
    if not (
        pre.get("scoreable", False)
        and post.get("scoreable", False)
        and "delta_outcome_G_at_H5" in truth
    ):
        return None
    pre_delta = float(pre["delta_outcome_G_at_H5"])
    post_delta = float(post["delta_outcome_G_at_H5"])
    truth_delta = float(truth["delta_outcome_G_at_H5"])
    denominator = pre_delta - truth_delta
    if abs(denominator) < 0.25:
        return None
    return float((pre_delta - post_delta) / denominator)


def _finite_reference_update_fraction(
    branch: dict, checkpoint: str
) -> float | None:
    """Movement from M_pre toward the MLE of the actually served report."""
    signatures = branch["signatures"]
    pre = signatures["M_pre_north"]
    post = signatures[f"M_{checkpoint}_north"]
    if not pre.get("scoreable", False) or not post.get("scoreable", False):
        return None
    reference_delta = branch["report_audit"]["finite_report_reference"][
        "delta_outcome_G7_minus_G3"
    ]
    pre_delta = float(pre["delta_outcome_G_at_H5"])
    post_delta = float(post["delta_outcome_G_at_H5"])
    denominator = pre_delta - float(reference_delta)
    if abs(denominator) < 0.25:
        return None
    return float((pre_delta - post_delta) / denominator)


def _delta(branch: dict, checkpoint: str, site: str = "north") -> float | None:
    signature = branch["signatures"].get(f"M_{checkpoint}_{site}", {})
    value = signature.get("delta_outcome_G_at_H5")
    return float(value) if value is not None else None


def _report_rng_independent(case_dir: Path, package_seed: int) -> bool:
    """Report generation uses another server and cannot advance episode RNG."""
    left = build_world_server(case_dir, seed_offset=97_777)
    right = build_world_server(case_dir, seed_offset=97_777)
    design = ExperimentDesign(
        config={"feedstock_grade": 4.0, "humidity": HUMIDITY},
        context={"site": "north"},
        n=7,
        horizon=None,
    )
    left.begin_turn(1)
    left_frame = left.experiment(design)
    report_server = build_world_server(case_dir)
    _sample_study(
        report_server,
        1,
        REPORT_SEED_NAMESPACE + package_seed * REPORT_PACKAGE_STRIDE + 123,
    )
    right.begin_turn(1)
    right_frame = right.experiment(design)
    return (
        left_frame.equals(right_frame)
        and left.export_evidence_ledger() == right.export_evidence_ledger()
    )


def local_certificate(package_seed: int, reports: dict[str, dict]) -> dict:
    descriptions = {
        name: build_world_server(case_dir).describe()
        for name, case_dir, _, _ in BRANCH_SPECS
    }
    audits = {name: report["audit"] for name, report in reports.items()}
    rebuilt = {
        name: rebuild_report(case_dir, reports[name]["selections"])
        for name, case_dir, _, _ in BRANCH_SPECS
    }
    truth_signatures = {
        name: {
            "north": truth_site_signature(
                case_dir,
                "north",
                n_samples=2_000,
                seed=(
                    REPORT_SEED_NAMESPACE
                    + package_seed * REPORT_PACKAGE_STRIDE
                    + 930_000
                ),
            ),
            "south": truth_site_signature(
                case_dir,
                "south",
                n_samples=2_000,
                seed=(
                    REPORT_SEED_NAMESPACE
                    + package_seed * REPORT_PACKAGE_STRIDE
                    + 930_000
                ),
            ),
        }
        for name, case_dir, _, _ in BRANCH_SPECS
    }
    design_hashes = {audit["design_sha256"] for audit in audits.values()}
    gates = {
        "agent_facing_cases_identical": all(
            sheet == descriptions["revise_clean"]
            for sheet in descriptions.values()
        ),
        "report_geometry_exact_all": all(
            audit["geometry_exact"] for audit in audits.values()
        ),
        "report_sign_pattern_exact_all": all(
            audit["sign_pattern_exact"] for audit in audits.values()
        ),
        "report_total_llr_in_target_all": all(
            audit["total_llr_in_target"] for audit in audits.values()
        ),
        "finite_report_reference_algebra_exact_all": all(
            audit["finite_report_reference"]["algebra_matches"]
            for audit in audits.values()
        ),
        "report_design_byte_exact_all": len(design_hashes) == 1,
        "report_reproducible_all": all(
            rebuilt[name].equals(reports[name]["frame"])
            for name in reports
        ),
        "report_seeds_unique": len({
            seed
            for report in reports.values()
            for selection in report["selections"]
            for seed in selection["grade_seeds"]
        }) == 2 * STUDY_COUNT * len(reports),
        "report_seed_namespace_fixed": all(
            selection["search_window_start"]
            >= REPORT_SEED_NAMESPACE
            + package_seed * REPORT_PACKAGE_STRIDE
            for report in reports.values()
            for selection in report["selections"]
        ),
        "report_search_effort_recorded_all": all(
            selection["search_window_size"] == STUDY_SEARCH_LIMIT
            and selection["candidates_until_selection"] >= 1
            and selection["fast_search_llr_matches_world"]
            and selection["exact_theoretical_acceptance_rate"] > 0.0
            and selection["exact_theoretical_expected_candidates"] >= 1.0
            and selection["observed_selection_effort_rate"] > 0.0
            for report in reports.values()
            for selection in report["selections"]
        ),
        "report_rng_independent_revise": _report_rng_independent(
            REVISE, package_seed
        ),
        "report_rng_independent_retain": _report_rng_independent(
            RETAIN, package_seed
        ),
        "clean_conflict_total_llr_matched_within_pole": all(
            abs(
                audits[f"{pole}_clean"]["total_llr_revise_over_retain"]
                - audits[f"{pole}_conflict"]["total_llr_revise_over_retain"]
            ) <= TARGET_TOTAL_TOLERANCE
            for pole in ("revise", "retain")
        ),
        "truth_north_revise_delta_zero": all(
            abs(truth_signatures[name]["north"]["delta_outcome_G_at_H5"])
            < 0.25
            for name in ("revise_clean", "revise_conflict")
        ),
        "truth_north_retain_delta_eight": all(
            abs(
                truth_signatures[name]["north"]["delta_outcome_G_at_H5"]
                - 8.0
            ) < 0.25
            for name in ("retain_clean", "retain_conflict")
        ),
        "truth_south_delta_eight_all": all(
            abs(row["south"]["delta_outcome_G_at_H5"] - 8.0) < 0.25
            for row in truth_signatures.values()
        ),
    }
    return {
        "kind": "zero_llm_signed_study_conflict_certificate",
        "package_seed": package_seed,
        "package_seed_independent_of_model_and_donor": True,
        "dose": {
            "target_total_abs_llr": TARGET_TOTAL_ABS_LLR,
            "conflict_opposing_abs_llr": CONFLICT_OPPOSING_ABS_LLR,
            "study_target_tolerance": STUDY_TARGET_TOLERANCE,
        },
        "seed_namespace": {
            "base": REPORT_SEED_NAMESPACE,
            "package_stride": REPORT_PACKAGE_STRIDE,
            "branch_stride": REPORT_BRANCH_STRIDE,
            "study_search_window": STUDY_SEARCH_LIMIT,
        },
        "report_audits": audits,
        "truth_signatures": truth_signatures,
        "gates": gates,
        "all": all(gates.values()),
    }


def _sanitized_prefix(prefix: dict) -> dict:
    result = copy.deepcopy(prefix)
    if result.get("formation"):
        result["formation"].pop("messages_through_formation", None)
    return result


def write_early(
    target: Path,
    *,
    model: str,
    seed_offset: int,
    package_seed: int,
    prefix: dict,
    certificate: dict,
    gates: dict,
) -> None:
    payload = {
        "kind": "exploratory_SCM_signed_study_conflict_fork",
        "claim_class": "precondition_failed_no_conflict_inference",
        "model": model,
        "seed_offset": seed_offset,
        "package_seed": package_seed,
        "local_certificate": certificate,
        "prefix": _sanitized_prefix(prefix),
        "branches": {},
        "gates": gates,
        "all": False,
    }
    target.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "out": str(target),
        "abort": prefix["abort"],
        "gates": gates,
    }, indent=2), flush=True)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", default="DeepSeek-V3.2")
    parser.add_argument("--seed-offset", type=int, default=97800)
    parser.add_argument(
        "--package-seed",
        type=int,
        default=1,
        help=(
            "Fixed report-package seed, independent of donor seed/model; "
            "reuse the same value across model replications."
        ),
    )
    parser.add_argument(
        "--target-total-abs-llr",
        type=float,
        default=32.0,
        help="Absolute net report LLR in each truth pole.",
    )
    parser.add_argument(
        "--conflict-opposing-abs-llr",
        type=float,
        default=4.0,
        help="Absolute LLR target of each of two opposing studies.",
    )
    parser.add_argument(
        "--study-search-limit",
        type=int,
        default=50_000,
        help="Fixed deterministic seed-search window per study.",
    )
    parser.add_argument("--belief-delta-threshold", type=float, default=3.0)
    parser.add_argument("--signature-n", type=int, default=4_000)
    parser.add_argument("--max-south-turns", type=int, default=14)
    parser.add_argument("--max-turns", type=int, default=24)
    parser.add_argument(
        "--cert-only",
        action="store_true",
        help="Run deterministic report/world gates without constructing an LLM client.",
    )
    parser.add_argument("--out", type=Path, default=None)
    args = parser.parse_args()

    if args.package_seed < 0:
        parser.error("--package-seed must be nonnegative")
    if args.target_total_abs_llr <= 0:
        parser.error("--target-total-abs-llr must be positive")
    if args.conflict_opposing_abs_llr <= 0:
        parser.error("--conflict-opposing-abs-llr must be positive")
    if args.study_search_limit < 1:
        parser.error("--study-search-limit must be positive")
    _configure_dose(
        total_abs_llr=args.target_total_abs_llr,
        opposing_abs_llr=args.conflict_opposing_abs_llr,
        search_limit=args.study_search_limit,
    )
    reports = build_all_reports(args.package_seed)
    certificate = local_certificate(args.package_seed, reports)
    if args.cert_only:
        print(json.dumps(certificate, indent=2), flush=True)
        if not certificate["all"]:
            raise SystemExit(1)
        return
    if not certificate["all"]:
        raise RuntimeError("zero-LLM signed-conflict certificate failed")

    OUT.mkdir(parents=True, exist_ok=True)
    target = args.out or OUT / (
        f"probe_{args.model}_seed{args.seed_offset}_pkg{args.package_seed}.json"
    )
    target.parent.mkdir(parents=True, exist_ok=True)

    prefix = run_common_south_prefix(
        args.model,
        args.seed_offset,
        max_south_turns=args.max_south_turns,
        belief_delta_threshold=args.belief_delta_threshold,
        signature_n=args.signature_n,
    )
    prefix_gates = {
        "local_certificate": certificate["all"],
        "transferable_model_formed": prefix["formation"] is not None,
        "south_prefix_evidence_present": bool(prefix["evidence_ledger"]),
        "all_prefix_evidence_south": _ledger_is_south(
            prefix["evidence_ledger"]
        ),
    }
    if prefix["abort"] != "transferable_model_formed":
        write_early(
            target,
            model=args.model,
            seed_offset=args.seed_offset,
            package_seed=args.package_seed,
            prefix=prefix,
            certificate=certificate,
            gates=prefix_gates,
        )
        return

    branches = {
        name: replay_report_and_continue(
            case_dir,
            reports[name],
            prefix,
            args.model,
            args.seed_offset,
            args.max_turns,
        )
        for name, case_dir, _, _ in BRANCH_SPECS
    }
    mpre = prefix["formation"]["M_pre"]
    for index, (name, case_dir, _, _) in enumerate(BRANCH_SPECS):
        add_artifact_measurements(
            branches[name],
            case_dir,
            mpre,
            signature_n=args.signature_n,
            signature_seed=args.seed_offset + 940_000 + index,
        )
        branches[name]["truth_update_fraction_secondary"] = {
            "M_first": _update_fraction(branches[name], "first"),
            "M_last": _update_fraction(branches[name], "last"),
        }
        branches[name]["finite_reference_update_fraction"] = {
            "M_first": _finite_reference_update_fraction(
                branches[name], "first"
            ),
            "M_last": _finite_reference_update_fraction(
                branches[name], "last"
            ),
        }

    event_rows = {
        name: [
            row
            for row in branch["evidence_ledger"]
            if row.get("kind") == "event_report"
            and row.get("delivery_variable") == REPORT_VARIABLE
        ]
        for name, branch in branches.items()
    }
    gates = {
        **prefix_gates,
        "replay_exact_all": all(
            branch["replay_exact"] for branch in branches.values()
        ),
        "prefix_ledger_exact_all": all(
            branch["prefix_ledger_exact"] for branch in branches.values()
        ),
        "handoff_prompt_exact_all": len({
            branch["handoff_prompt_sha256"] for branch in branches.values()
        }) == 1,
        "report_event_once_all": all(
            len(rows) == 1 for rows in event_rows.values()
        ),
        "report_injected_free_all": all(
            branch["report_injection"]["free"]
            for branch in branches.values()
        ),
        "report_hash_matches_audit_all": all(
            branch["report_injection"]["sha256"]
            == branch["report_audit"]["sha256"]
            for branch in branches.values()
        ),
        "zero_post_report_experiments_all": all(
            branch["post_report_experiment_count"] == 0
            for branch in branches.values()
        ),
        "no_post_report_non_report_evidence_all": all(
            not branch["post_report_non_report_evidence"]
            for branch in branches.values()
        ),
        "collection_window_enforced_all": all(
            branch["collection_window_enforced"]
            for branch in branches.values()
        ),
        "accepted_all": all(
            branch["accepted"] for branch in branches.values()
        ),
        "last_artifact_scoreable_all": all(
            branch["scores"]["M_last"].get("scoreable", False)
            for branch in branches.values()
        ),
        "first_artifact_scoreable_all": all(
            branch["scores"]["M_first"].get("scoreable", False)
            for branch in branches.values()
        ),
        "M_first_captured_on_first_post_report_turn_all": all(
            branch["M_first_turn"] == branch["handoff_turn"]
            for branch in branches.values()
        ),
    }

    finite_u = {
        name: branch["finite_reference_update_fraction"]["M_last"]
        for name, branch in branches.items()
    }
    finite_reference_delta = {
        name: branch["report_audit"]["finite_report_reference"][
            "delta_outcome_G7_minus_G3"
        ]
        for name, branch in branches.items()
    }
    last_delta = {
        name: _delta(branch, "last") for name, branch in branches.items()
    }
    finite_reference_error = {
        name: (
            abs(last_delta[name] - finite_reference_delta[name])
            if last_delta[name] is not None
            else None
        )
        for name in branches
    }
    b_by_truth = {}
    for pole in ("revise", "retain"):
        clean_u = finite_u[f"{pole}_clean"]
        conflict_u = finite_u[f"{pole}_conflict"]
        b_by_truth[pole] = (
            float(clean_u - conflict_u)
            if clean_u is not None and conflict_u is not None
            else None
        )
    contrast = {
        "primary_reference": (
            "pooled finite-report slope MLE; this is not hidden truth and "
            "does not incorporate the agent's unknown prior"
        ),
        "U_finite_reference_last": finite_u,
        "B_clean_minus_conflict_by_truth": b_by_truth,
        "finite_reference_delta": finite_reference_delta,
        "last_delta": last_delta,
        "last_abs_error_to_finite_reference": finite_reference_error,
        "truth_update_fraction_secondary": {
            name: branch["truth_update_fraction_secondary"]["M_last"]
            for name, branch in branches.items()
        },
        "south_abs_delta_change_last": {
            name: (
                abs(_delta(branch, "last", "south") - _delta(branch, "pre", "south"))
                if _delta(branch, "last", "south") is not None
                and _delta(branch, "pre", "south") is not None
                else None
            )
            for name, branch in branches.items()
        },
        "predeclared_reading": {
            "clean_revise_matches_finite_reference_within_15": (
                finite_reference_error["revise_clean"] is not None
                and finite_reference_error["revise_clean"] <= 1.5
            ),
            "clean_retain_matches_finite_reference_within_15": (
                finite_reference_error["retain_clean"] is not None
                and finite_reference_error["retain_clean"] <= 1.5
            ),
            "candidate_revise_conflict_signal_B_ge_025": (
                b_by_truth["revise"] is not None
                and b_by_truth["revise"] >= 0.25
            ),
            "candidate_retain_conflict_signal_B_ge_025": (
                b_by_truth["retain"] is not None
                and b_by_truth["retain"] >= 0.25
            ),
        },
    }
    payload = {
        "kind": "exploratory_SCM_signed_study_conflict_fork",
        "claim_class": (
            "between_study_conflict_penalty_at_matched_aggregate_Bayes_factor"
        ),
        "model": args.model,
        "seed_offset": args.seed_offset,
        "package_seed": args.package_seed,
        "branch_order": [name for name, _, _, _ in BRANCH_SPECS],
        "report_handoff": REPORT_HANDOFF,
        "thresholds": {
            "belief_delta": args.belief_delta_threshold,
            "report_total_abs_llr": TARGET_TOTAL_ABS_LLR,
            "report_total_llr_tolerance": TARGET_TOTAL_TOLERANCE,
            "conflict_opposing_abs_llr": CONFLICT_OPPOSING_ABS_LLR,
            "study_search_limit": STUDY_SEARCH_LIMIT,
            "clean_abs_delta_error_to_finite_report_reference": 1.5,
            "candidate_B": 0.25,
        },
        "local_certificate": certificate,
        "prefix": _sanitized_prefix(prefix),
        "report_event_rows": event_rows,
        "branches": branches,
        "contrast": contrast,
        "gates": gates,
        "all": all(gates.values()),
    }
    target.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "out": str(target),
        "gates": gates,
        "all": payload["all"],
        "abort": {
            name: branch["abort"] for name, branch in branches.items()
        },
        "north_delta": {
            name: {
                checkpoint: _delta(branch, checkpoint)
                for checkpoint in ("pre", "first", "last")
            }
            for name, branch in branches.items()
        },
        "contrast": contrast,
    }, indent=2), flush=True)


if __name__ == "__main__":
    main()
