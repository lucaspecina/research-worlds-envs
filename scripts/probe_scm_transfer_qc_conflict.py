"""Real-agent South-to-North fork with an on-manifold QC conflict.

The agent forms one executable model while working in South.  At handoff it
writes its first North campaign cell after being told that a routine
``north_qc_report`` will be present when the cell runs, but before seeing the
report's contents.  That one cell is then replayed into three continuations:

* REVISE with a neutral central QC report;
* REVISE with a strongly grade-confirming but zero-LLR QC report; and
* RETAIN with the same conflict report byte for byte.

The report is generated and seeded outside ``WorldServer._next_seed`` so it
cannot perturb the agent's own experimental evidence.  This is an exploratory
content probe, not a prevalence estimator.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import math
import sys
from pathlib import Path
from types import SimpleNamespace

import numpy as np
import pandas as pd
from scipy.stats import norm

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
    _action_ledger,
    _action_record_exact,
    _experiment_events,
    _ledger_requests,
    _replay_checks_exact,
    _request_view,
    replay_prefix_exact,
)
from scripts.probe_first_story_scm_transfer_fork import (  # noqa: E402
    REVISE,
    RETAIN,
    SYSTEM,
    _artifact_hash,
    _belief_gate,
    _experiments_have_site,
    _ledger_is_south,
    add_artifact_measurements,
    both_site_signatures,
    classify_north_action,
    south_initial_prompt,
)


OUT = ROOT / "scripts" / "out" / "first_story_scm_transfer_qc_conflict"
QC_VARIABLE = "north_qc_report"
QC_ROWS_PER_BATCH = 400
QC_COLUMNS = [
    "qc_batch",
    "feedstock_grade",
    "humidity",
    "feedstock",
    "outcome",
]
BRANCH_SPECS = (
    ("revise_clean", REVISE, "clean", "revise"),
    ("revise_conflict", REVISE, "conflict", "revise"),
    ("retain_conflict", RETAIN, "conflict", "retain"),
)

QC_TRANSITION = (
    "South phase complete; work now shifts to North. Routine handoff: when "
    "your first North campaign cell runs, the latest North QC extract will "
    f"already be loaded as DataFrame `{QC_VARIABLE}`. In this next single "
    "campaign cell, first inspect that routine report and then run at least "
    "one North trial; do not stop after local inspection. Analyze both as "
    "one research record. North trials use "
    'context={"site": "north"}; South remains available for an explicit '
    "validation. Keep `working_model` current and submit only when the "
    "assignment is sufficient."
)


def _qc_specs(variant: str) -> tuple[tuple[int, float, float], ...]:
    if variant == "clean":
        return ((1, 5.0, 5.0), (2, 5.0, 5.0))
    if variant == "conflict":
        return ((1, 3.0, 7.0), (2, 7.0, 3.0))
    raise ValueError(f"unknown QC variant {variant!r}")


def build_qc_report(
    variant: str,
    seed_offset: int,
    *,
    case_dir: Path = REVISE,
) -> pd.DataFrame:
    """Generate the served QC table without advancing episode RNG state."""
    server = build_world_server(case_dir, seed_offset=seed_offset)
    frames = []
    for index, (batch, grade, humidity) in enumerate(_qc_specs(variant)):
        # Direct world_sample with an explicit probe seed: no _next_seed call.
        observed = server.world_sample(
            SimpleNamespace(
                config={
                    "feedstock_grade": grade,
                    "humidity": humidity,
                },
                context={"site": "north"},
                horizon=None,
            ),
            QC_ROWS_PER_BATCH,
            seed_offset + 860_000 + index,
        )
        frame = observed.copy()
        frame.insert(0, "humidity", humidity)
        frame.insert(0, "feedstock_grade", grade)
        frame.insert(0, "qc_batch", batch)
        frames.append(frame[QC_COLUMNS])
    return pd.concat(frames, ignore_index=True)


def qc_llr_revise_over_retain(frame: pd.DataFrame) -> float:
    """Exact log likelihood ratio for the two declared reference mechanisms."""
    grade = frame["feedstock_grade"].to_numpy(dtype=float)
    humidity = frame["humidity"].to_numpy(dtype=float)
    outcome = frame["outcome"].to_numpy(dtype=float)
    mu_revise = 40.0 - 2.0 * humidity
    mu_retain = 20.0 + 2.0 * grade
    # Both mechanisms have Normal(0, 2^2) outcome noise.
    return float(
        np.sum(np.square(outcome - mu_retain) - np.square(outcome - mu_revise))
        / 8.0
    )


def _frame_digest(frame: pd.DataFrame) -> str:
    payload = frame.to_json(orient="split", double_precision=15)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def qc_audit(frame: pd.DataFrame, variant: str) -> dict:
    specs = _qc_specs(variant)
    expected_rows = 2 * QC_ROWS_PER_BATCH
    batches = []
    for batch, grade, humidity in specs:
        block = frame.loc[frame["qc_batch"] == batch]
        batches.append({
            "name": batch,
            "rows": int(len(block)),
            "feedstock_grade_values": sorted(
                float(value) for value in block["feedstock_grade"].unique()
            ),
            "humidity_values": sorted(
                float(value) for value in block["humidity"].unique()
            ),
            "geometry_exact": (
                len(block) == QC_ROWS_PER_BATCH
                and bool((block["feedstock_grade"] == grade).all())
                and bool((block["humidity"] == humidity).all())
            ),
        })
    llr = qc_llr_revise_over_retain(frame)
    return {
        "variant": variant,
        "rows": int(len(frame)),
        "columns": list(frame.columns),
        "dtypes": [str(dtype) for dtype in frame.dtypes],
        "sha256": _frame_digest(frame),
        "batches": batches,
        "llr_revise_over_retain": llr,
        "geometry_exact": (
            len(frame) == expected_rows
            and list(frame.columns) == QC_COLUMNS
            and all(batch["geometry_exact"] for batch in batches)
        ),
        "llr_zero": abs(llr) < 1e-12,
    }


def inject_qc_report(
    server,
    kernel: KernelClient,
    frame: pd.DataFrame,
    *,
    turn: int,
) -> dict:
    """Inject and archive one researcher-served report without charging it."""
    budget_before = float(server.budget_remaining)
    kernel.inject_dataframe(QC_VARIABLE, frame)
    server._record_evidence(  # noqa: SLF001 - deliberate probe-side audit
        "event_report",
        source="north_qc_report",
        request={"n": len(frame), "batches": 2},
        frame=frame,
        delivery_variable=QC_VARIABLE,
        turn=turn,
    )
    budget_after = float(server.budget_remaining)
    return {
        "variable": QC_VARIABLE,
        "turn": turn,
        "budget_before": budget_before,
        "budget_after": budget_after,
        "free": budget_before == budget_after,
        "sha256": _frame_digest(frame),
    }


def _cell_references_qc(cell: str) -> bool:
    return QC_VARIABLE in cell


def run_common_qc_prefix(
    model: str,
    seed_offset: int,
    *,
    max_south_turns: int,
    belief_delta_threshold: float,
    signature_n: int,
) -> dict:
    """Build a South belief and freeze one QC-aware North campaign cell."""
    server = build_world_server(REVISE, seed_offset=seed_offset)
    chat = FoundryChat(
        system=SYSTEM,
        model=model,
        max_completion_tokens=MAX_COMPLETION_TOKENS,
    )
    trace = []
    prompt = south_initial_prompt(server)
    abort = "no_transferable_model_after_max_south_turns"
    formation = None
    selection = None
    transition_full_prompt = None

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

            if not _experiments_have_site(row["trajectory"], "south"):
                abort = "non_south_experiment_before_transition"
                break
            ledger = server.export_evidence_ledger()
            if not _ledger_is_south(ledger):
                abort = "non_south_evidence_before_transition"
                break
            if server.terminal:
                abort = "submitted_before_transfer"
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
                    "M_formed": code,
                    "M_formed_sha256": _artifact_hash(code),
                    "signatures": signatures,
                    "validation_error": None,
                    "evidence_ledger": ledger,
                    "south_evidence_rows": len(ledger),
                    "formation_feedback": feedback(result, server),
                }
                abort = "transferable_model_formed"
                break
            prompt = feedback(result, server)

        if formation is not None:
            transition_full_prompt = (
                formation["formation_feedback"] + "\n\n" + QC_TRANSITION
            )
            turn = formation["turn"] + 1
            notices = server.begin_turn(turn)
            for variable, frame in server.pop_deliveries():
                kernel.inject_dataframe(variable, frame)
            reply = chat.ask(transition_full_prompt)
            cell = extract_cell(reply.content)
            if cell is None:
                abort = "no_cell_after_north_transition"
            else:
                # Freeze first; only then materialize the clean preflight report.
                mpre = trace[-1]["working_model"]["code"]
                prefix_ledger = server.export_evidence_ledger()
                qc_frame = build_qc_report("clean", seed_offset)
                qc_injection = inject_qc_report(
                    server, kernel, qc_frame, turn=turn
                )
                start = len(server.trajectory)
                result = kernel.run_cell(cell)
                row = record(
                    turn, reply.content, cell, result, server, notices, start
                )
                row["phase"] = "frozen_north_action_preflight"
                experiments = _experiment_events(row["trajectory"])
                if not experiments:
                    trace.append(row)
                    abort = "first_north_cell_not_experimental"
                elif not _experiments_have_site(row["trajectory"], "north"):
                    trace.append(row)
                    abort = "non_north_experiment_after_transition"
                else:
                    validation_error = (
                        "missing artifact"
                        if mpre is None else server.validate_model(mpre)
                    )
                    signatures = both_site_signatures(
                        mpre,
                        server.columns,
                        n_samples=signature_n,
                        seed=seed_offset + 720_000,
                    )
                    if validation_error is not None:
                        trace.append(row)
                        abort = "M_pre_invalid_before_north_action"
                    elif not _belief_gate(
                        signatures, belief_delta_threshold
                    ):
                        trace.append(row)
                        abort = "transferred_belief_lost_before_north_action"
                    else:
                        selection = {
                            "turn": turn,
                            "reply_text": reply.content,
                            "cell": cell,
                            "cell_sha256": hashlib.sha256(
                                cell.encode("utf-8")
                            ).hexdigest(),
                            "cell_references_qc": _cell_references_qc(cell),
                            "notices": notices,
                            "messages_through_action": copy.deepcopy(
                                chat.messages
                            ),
                            "M_pre": mpre,
                            "M_pre_signatures": signatures,
                            "prefix_evidence_ledger": prefix_ledger,
                            "preflight_qc_audit": qc_audit(
                                qc_frame, "clean"
                            ),
                            "preflight_qc_injection": qc_injection,
                            "preflight_action_record": row,
                            "preflight_action_trajectory": row["trajectory"],
                            "preflight_evidence_ledger_after": (
                                server.export_evidence_ledger()
                            ),
                        }
                        abort = "north_action_selected"

    return {
        "abort": abort,
        "trace": trace,
        "formation": formation,
        "transition_text": QC_TRANSITION if formation is not None else None,
        "transition_prompt": transition_full_prompt,
        "selection": selection,
        "evidence_ledger": (
            selection["prefix_evidence_ledger"]
            if selection is not None
            else (
                formation["evidence_ledger"]
                if formation is not None
                else server.export_evidence_ledger()
            )
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


def replay_qc_and_continue(
    case_dir: Path,
    qc_variant: str,
    prefix: dict,
    model: str,
    seed_offset: int,
    max_turns: int,
) -> dict:
    """Replay the common notebook, inject one QC variant, and continue."""
    server = build_world_server(case_dir, seed_offset=seed_offset)
    action = prefix["selection"]
    preflight_requests = _request_view(action["preflight_action_trajectory"])
    branch_trace = []

    with KernelClient(server, cell_timeout_s=CELL_TIMEOUT_S) as kernel:
        replay_checks = replay_prefix_exact(server, prefix, kernel)
        ledger_after_prefix = server.export_evidence_ledger()
        notices = server.begin_turn(action["turn"])
        action_notices = copy.deepcopy(notices)
        for variable, delivered in server.pop_deliveries():
            kernel.inject_dataframe(variable, delivered)
        qc_frame = build_qc_report(
            qc_variant, seed_offset, case_dir=case_dir
        )
        qc_injection = inject_qc_report(
            server, kernel, qc_frame, turn=action["turn"]
        )
        start = len(server.trajectory)
        action_result = kernel.run_cell(action["cell"])
        action_record = record(
            action["turn"],
            action["reply_text"],
            action["cell"],
            action_result,
            server,
            notices,
            start,
        )
        action_record["phase"] = "frozen_north_action_with_qc"
        branch_trace.append(action_record)
        ledger_after_action = server.export_evidence_ledger()

        chat = FoundryChat(
            system=SYSTEM,
            model=model,
            max_completion_tokens=MAX_COMPLETION_TOKENS,
        )
        chat.messages = copy.deepcopy(action["messages_through_action"])
        prompt = feedback(action_result, server)
        abort = "submitted" if server.terminal else "max_turns"
        for turn in range(action["turn"] + 1, max_turns + 1):
            if server.terminal:
                break
            notices = server.begin_turn(turn)
            for variable, delivered in server.pop_deliveries():
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
            row["phase"] = "post_north_action"
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
        llm_turn_usage = [
            {
                "prompt_tokens": item.prompt_tokens,
                "completion_tokens": item.completion_tokens,
                "reasoning_tokens": item.reasoning_tokens,
                "latency_s": item.latency_s,
            }
            for item in chat.turns
        ]

    final = server.result or {}
    mpre = action["M_pre"]
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
    action_requests = _request_view(action_record["trajectory"])
    full_ledger = server.export_evidence_ledger()
    return {
        "case_id": case_dir.name,
        "qc_variant": qc_variant,
        "qc_audit": qc_audit(qc_frame, qc_variant),
        "qc_injection": qc_injection,
        "replay_checks": replay_checks,
        "replay_exact": _replay_checks_exact(replay_checks),
        "prefix_ledger_after_replay": ledger_after_prefix,
        "prefix_ledger_exact": ledger_after_prefix == prefix["evidence_ledger"],
        "frozen_action_cell": action["cell"],
        "frozen_action_cell_sha256": hashlib.sha256(
            action["cell"].encode("utf-8")
        ).hexdigest(),
        "action_notices_exact": action_notices == action["notices"],
        "action_requests": action_requests,
        "action_requests_match_preflight": action_requests == preflight_requests,
        "ledger_after_action": ledger_after_action,
        "abort": abort,
        "accepted": server.terminal,
        "R": final.get("R"),
        "submission_code": final.get("code"),
        "first_changed_model": first_changed,
        "last_working_model": last_code,
        "trace": branch_trace,
        "transcript": transcript,
        "evidence_ledger": full_ledger,
        "post_action_experiment_sites": [
            event["args"].get("context", {}).get("site")
            for row in branch_trace
            for event in _experiment_events(row["trajectory"])
        ],
        "tokens_continuation": tokens,
        "llm_turn_usage": llm_turn_usage,
        "last_working_model_code": last_code,
        "qc_referenced_in_action_cell": _cell_references_qc(action["cell"]),
        "qc_referenced_in_any_cell": any(
            _cell_references_qc(row["cell"]) for row in branch_trace
        ),
    }


def action_reference_update(
    ledger: list[dict], truth_pole: str, *, tolerance: float = 0.25
) -> dict:
    """Exact two-hypothesis reference update from both-set North actions."""
    llr_revise_over_retain = 0.0
    rows_used = 0
    experiments_used = 0
    both_set_experiments = 0
    grade_only_experiments = 0
    requests = []
    for row in ledger:
        request = row["request"]
        config = request.get("config", {})
        context = request.get("context", {})
        if context != {"site": "north"}:
            continue
        if "feedstock_grade" not in config:
            continue
        grade = float(config["feedstock_grade"])
        data = row["data"]
        columns = data["columns"]
        outcome_index = columns.index("outcome")
        outcome = np.asarray(
            [values[outcome_index] for values in data["data"]], dtype=float
        )
        mu_retain = 20.0 + 2.0 * grade
        if "humidity" in config:
            humidity = float(config["humidity"])
            if abs(grade - (10.0 - humidity)) <= tolerance:
                continue
            mu_revise = 40.0 - 2.0 * humidity
            llr_revise_over_retain += float(
                np.sum(
                    np.square(outcome - mu_retain)
                    - np.square(outcome - mu_revise)
                )
                / 8.0
            )
            both_set_experiments += 1
        else:
            # In REVISE with grade fixed and humidity left ordinary:
            # H=2+6U+eps_h, U~Uniform(0,1), eps_h~N(0,.5), and
            # Y=40-2H+eps_y.  Therefore Y is Uniform(24,36) convolved
            # with Normal(0, sqrt(5)).  RETAIN is Normal(20+2G, 2).
            sigma_revise = math.sqrt(5.0)
            density_revise = (
                norm.cdf((outcome - 24.0) / sigma_revise)
                - norm.cdf((outcome - 36.0) / sigma_revise)
            ) / 12.0
            logp_revise = np.log(np.maximum(density_revise, 1e-300))
            logp_retain = norm.logpdf(outcome, loc=mu_retain, scale=2.0)
            llr_revise_over_retain += float(
                np.sum(logp_revise - logp_retain)
            )
            grade_only_experiments += 1
        rows_used += len(outcome)
        experiments_used += 1
        requests.append(request)
    signed_llr = (
        llr_revise_over_retain
        if truth_pole == "revise"
        else -llr_revise_over_retain
    )
    if signed_llr >= 0:
        posterior_correct = 1.0 / (1.0 + math.exp(-min(signed_llr, 745.0)))
    else:
        posterior_correct = math.exp(max(signed_llr, -745.0)) / (
            1.0 + math.exp(max(signed_llr, -745.0))
        )
    return {
        "truth_pole": truth_pole,
        "llr_revise_over_retain": llr_revise_over_retain,
        "signed_llr_for_correct_pole": signed_llr,
        "posterior_correct_equal_prior": posterior_correct,
        "experiments_used": experiments_used,
        "both_set_experiments_used": both_set_experiments,
        "grade_only_experiments_used": grade_only_experiments,
        "rows_used": rows_used,
        "requests_used": requests,
        "diagnostic_experiment_present": experiments_used > 0,
        "both_set_off_manifold_present": both_set_experiments > 0,
    }


def _update_fraction(branch: dict, checkpoint: str) -> float | None:
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


def local_certificate(seed_offset: int) -> dict:
    clean = build_qc_report("clean", seed_offset, case_dir=REVISE)
    conflict_revise = build_qc_report(
        "conflict", seed_offset, case_dir=REVISE
    )
    conflict_retain = build_qc_report(
        "conflict", seed_offset, case_dir=RETAIN
    )
    repeated = build_qc_report("conflict", seed_offset, case_dir=REVISE)

    # A fixed, zero-LLM diagnostic campaign certifies the exact LLR routine.
    action_ledgers = {}
    for name, case_dir, _, truth_pole in BRANCH_SPECS:
        server = build_world_server(case_dir, seed_offset=seed_offset)
        server.begin_turn(1)
        for grade in (3.0, 7.0):
            frame = server.experiment(
                ExperimentDesign(
                    config={"feedstock_grade": grade, "humidity": 5.0},
                    context={"site": "north"},
                    n=30,
                    horizon=None,
                )
            )
        del frame
        action_ledgers[name] = {
            "ledger": _action_ledger(
                {"evidence_ledger": server.export_evidence_ledger()}, 1
            ),
            "reference": action_reference_update(
                _action_ledger(
                    {"evidence_ledger": server.export_evidence_ledger()}, 1
                ),
                truth_pole,
            ),
        }

    audits = {
        "clean": qc_audit(clean, "clean"),
        "conflict_revise": qc_audit(conflict_revise, "conflict"),
        "conflict_retain": qc_audit(conflict_retain, "conflict"),
    }
    gates = {
        "agent_facing_twins_identical": (
            build_world_server(REVISE, seed_offset=seed_offset).describe()
            == build_world_server(RETAIN, seed_offset=seed_offset).describe()
        ),
        "qc_geometry_exact_all": all(
            audit["geometry_exact"] for audit in audits.values()
        ),
        "qc_llr_zero_all": all(audit["llr_zero"] for audit in audits.values()),
        "qc_conflict_reproducible": conflict_revise.equals(repeated),
        "qc_conflict_byte_exact_twins": conflict_revise.equals(conflict_retain),
        "qc_shape_order_matched": (
            clean.shape == conflict_revise.shape
            and list(clean.columns) == list(conflict_revise.columns)
        ),
        "diagnostic_action_revise_outputs_exact": (
            action_ledgers["revise_clean"]["ledger"]
            == action_ledgers["revise_conflict"]["ledger"]
        ),
        "diagnostic_action_requests_all_exact": all(
            _ledger_requests(row["ledger"])
            == _ledger_requests(action_ledgers["revise_clean"]["ledger"])
            for row in action_ledgers.values()
        ),
        "diagnostic_reference_posterior_ge_099_all": all(
            row["reference"]["posterior_correct_equal_prior"] >= 0.99
            for row in action_ledgers.values()
        ),
        "diagnostic_experiment_present_all": all(
            row["reference"]["diagnostic_experiment_present"]
            for row in action_ledgers.values()
        ),
    }
    return {
        "kind": "zero_llm_qc_conflict_certificate",
        "seed_offset": seed_offset,
        "qc_audits": audits,
        "action_reference": {
            name: row["reference"] for name, row in action_ledgers.items()
        },
        "gates": gates,
        "all": all(gates.values()),
    }


def _sanitized_prefix(prefix: dict) -> dict:
    result = copy.deepcopy(prefix)
    if result.get("selection"):
        result["selection"].pop("messages_through_action", None)
    return result


def write_early(
    target: Path,
    *,
    model: str,
    seed_offset: int,
    prefix: dict,
    action_classification: dict | None,
    gates: dict,
) -> None:
    payload = {
        "kind": "exploratory_SCM_transfer_QC_conflict_fork",
        "claim_class": "precondition_failed_no_QC_conflict_inference",
        "model": model,
        "seed_offset": seed_offset,
        "prefix": _sanitized_prefix(prefix),
        "action_classification": action_classification,
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
    parser.add_argument("--seed-offset", type=int, default=97600)
    parser.add_argument("--belief-delta-threshold", type=float, default=3.0)
    parser.add_argument("--diagnostic-delta-threshold", type=float, default=1.0)
    parser.add_argument("--off-manifold-tolerance", type=float, default=0.25)
    parser.add_argument("--signature-n", type=int, default=4000)
    parser.add_argument("--action-expectation-n", type=int, default=20_000)
    parser.add_argument("--max-south-turns", type=int, default=14)
    parser.add_argument("--max-turns", type=int, default=32)
    parser.add_argument(
        "--cert-only",
        action="store_true",
        help="Run deterministic QC/world gates without constructing an LLM client.",
    )
    parser.add_argument("--out", type=Path, default=None)
    args = parser.parse_args()

    certificate = local_certificate(args.seed_offset)
    if args.cert_only:
        print(json.dumps(certificate, indent=2), flush=True)
        if not certificate["all"]:
            raise SystemExit(1)
        return
    if not certificate["all"]:
        raise RuntimeError("zero-LLM QC conflict certificate failed")

    OUT.mkdir(parents=True, exist_ok=True)
    target = args.out or OUT / (
        f"probe_{args.model}_seed{args.seed_offset}.json"
    )
    target.parent.mkdir(parents=True, exist_ok=True)

    sheets = {
        name: build_world_server(case_dir, seed_offset=args.seed_offset).describe()
        for name, case_dir, _, _ in BRANCH_SPECS
    }
    agent_facing_cases_identical = all(
        sheet == sheets["revise_clean"] for sheet in sheets.values()
    )
    prefix = run_common_qc_prefix(
        args.model,
        args.seed_offset,
        max_south_turns=args.max_south_turns,
        belief_delta_threshold=args.belief_delta_threshold,
        signature_n=args.signature_n,
    )
    prefix_gates = {
        "local_certificate": certificate["all"],
        "agent_facing_cases_identical": agent_facing_cases_identical,
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
        write_early(
            target,
            model=args.model,
            seed_offset=args.seed_offset,
            prefix=prefix,
            action_classification=None,
            gates=prefix_gates,
        )
        return

    action_classification = classify_north_action(
        prefix["selection"]["preflight_action_trajectory"],
        seed_offset=args.seed_offset,
        expectation_n=args.action_expectation_n,
        diagnostic_delta_threshold=args.diagnostic_delta_threshold,
        off_manifold_tolerance=args.off_manifold_tolerance,
    )
    preflight_ledger = _action_ledger(
        {
            "evidence_ledger": prefix["selection"][
                "preflight_evidence_ledger_after"
            ]
        },
        prefix["selection"]["turn"],
    )
    preflight_reference = action_reference_update(
        preflight_ledger, "revise", tolerance=args.off_manifold_tolerance
    )
    prefix["action_classification"] = action_classification
    prefix["preflight_action_reference"] = preflight_reference
    prefix_gates.update({
        "north_action_diagnostic": action_classification["diagnostic"],
        "north_action_reference_diagnostic": preflight_reference[
            "diagnostic_experiment_present"
        ],
        "north_action_reference_posterior_ge_099": (
            preflight_reference["posterior_correct_equal_prior"] >= 0.99
        ),
        "qc_referenced_in_frozen_action_cell": prefix["selection"][
            "cell_references_qc"
        ],
    })
    hard_prefix_gates = {
        key: value
        for key, value in prefix_gates.items()
        if key != "qc_referenced_in_frozen_action_cell"
    }
    if not all(hard_prefix_gates.values()):
        prefix["abort"] = "north_action_protocol_gate_failed"
        write_early(
            target,
            model=args.model,
            seed_offset=args.seed_offset,
            prefix=prefix,
            action_classification=action_classification,
            gates=prefix_gates,
        )
        return

    branches = {
        name: replay_qc_and_continue(
            case_dir,
            qc_variant,
            prefix,
            args.model,
            args.seed_offset,
            args.max_turns,
        )
        for name, case_dir, qc_variant, _ in BRANCH_SPECS
    }
    mpre = prefix["selection"]["M_pre"]
    for index, (name, case_dir, _, _) in enumerate(BRANCH_SPECS):
        add_artifact_measurements(
            branches[name],
            case_dir,
            mpre,
            signature_n=args.signature_n,
            signature_seed=args.seed_offset + 910_000 + index,
        )
        branches[name]["update_fraction"] = {
            "M_first": _update_fraction(branches[name], "first"),
            "M_last": _update_fraction(branches[name], "last"),
        }

    action_turn = prefix["selection"]["turn"]
    action_ledgers = {
        name: _action_ledger(branch, action_turn)
        for name, branch in branches.items()
    }
    action_references = {
        name: action_reference_update(
            action_ledgers[name],
            truth_pole,
            tolerance=args.off_manifold_tolerance,
        )
        for name, _, _, truth_pole in BRANCH_SPECS
    }
    revise_requests = _ledger_requests(action_ledgers["revise_clean"])
    qc_event_rows = {
        name: [
            row
            for row in branch["evidence_ledger"]
            if row["kind"] == "event_report"
            and row["delivery_variable"] == QC_VARIABLE
            and row["turn"] == action_turn
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
        "preflight_action_record_exact_revise_clean": _action_record_exact(
            branches["revise_clean"]["trace"][0],
            prefix["selection"]["preflight_action_record"],
        ),
        "same_action_ledger_requests_all": (
            bool(revise_requests)
            and all(
                _ledger_requests(action_ledgers[name]) == revise_requests
                for name in branches
            )
        ),
        "diagnostic_action_ledger_exact_revise_clean_conflict": (
            action_ledgers["revise_clean"]
            == action_ledgers["revise_conflict"]
        ),
        "diagnostic_action_extremes_differ": (
            action_ledgers["revise_conflict"]
            != action_ledgers["retain_conflict"]
        ),
        "qc_event_report_once_all": all(
            len(rows) == 1 for rows in qc_event_rows.values()
        ),
        "qc_injected_free_all": all(
            branch["qc_injection"]["free"] for branch in branches.values()
        ),
        "qc_geometry_exact_all": all(
            branch["qc_audit"]["geometry_exact"]
            for branch in branches.values()
        ),
        "qc_llr_zero_all": all(
            branch["qc_audit"]["llr_zero"] for branch in branches.values()
        ),
        "qc_conflict_byte_exact_twins": (
            branches["revise_conflict"]["qc_audit"]["sha256"]
            == branches["retain_conflict"]["qc_audit"]["sha256"]
        ),
        "reference_diagnostic_action_all": all(
            row["diagnostic_experiment_present"]
            for row in action_references.values()
        ),
        "reference_posterior_ge_099_all": all(
            row["posterior_correct_equal_prior"] >= 0.99
            for row in action_references.values()
        ),
        "accepted_all": all(
            branch["accepted"] for branch in branches.values()
        ),
        "last_artifact_scoreable_all": all(
            branch["scores"]["M_last"].get("scoreable", False)
            for branch in branches.values()
        ),
    }
    u_clean = branches["revise_clean"]["update_fraction"]["M_last"]
    u_conflict = branches["revise_conflict"]["update_fraction"]["M_last"]
    b_mix = (
        float(u_clean - u_conflict)
        if u_clean is not None and u_conflict is not None
        else None
    )
    payload = {
        "kind": "exploratory_SCM_transfer_QC_conflict_fork",
        "claim_class": "on_manifold_confirmatory_camouflage_probe",
        "model": args.model,
        "seed_offset": args.seed_offset,
        "branch_order": [name for name, _, _, _ in BRANCH_SPECS],
        "transition": QC_TRANSITION,
        "thresholds": {
            "belief_delta": args.belief_delta_threshold,
            "diagnostic_delta": args.diagnostic_delta_threshold,
            "off_manifold_tolerance": args.off_manifold_tolerance,
            "reference_posterior": 0.99,
        },
        "local_certificate": certificate,
        "prefix": _sanitized_prefix(prefix),
        "action_classification": action_classification,
        "action_references": action_references,
        "action_ledgers": action_ledgers,
        "qc_event_rows": qc_event_rows,
        "exposure_outcomes": {
            "qc_referenced_in_frozen_action_cell": prefix["selection"][
                "cell_references_qc"
            ],
            "qc_referenced_in_action_all": all(
                branch["qc_referenced_in_action_cell"]
                for branch in branches.values()
            ),
            "qc_referenced_in_any_cell": {
                name: branch["qc_referenced_in_any_cell"]
                for name, branch in branches.items()
            },
        },
        "branches": branches,
        "contrast": {
            "U_clean_last": u_clean,
            "U_camouflage_last": u_conflict,
            "B_cam_clean_minus_camouflage": b_mix,
        },
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
        "scores_R": {
            name: {
                checkpoint: score.get("R")
                for checkpoint, score in branch["scores"].items()
            }
            for name, branch in branches.items()
        },
        "north_delta": {
            name: {
                checkpoint: branch["signatures"][
                    f"M_{checkpoint}_north"
                ].get("delta_outcome_G_at_H5")
                for checkpoint in ("pre", "first", "last")
            }
            for name, branch in branches.items()
        },
        "contrast": payload["contrast"],
    }, indent=2), flush=True)


if __name__ == "__main__":
    main()
