"""Real-agent fork for the structurally causal first-story SCM twins.

The runner freezes the first cell that *actually reaches* ``env.experiment``.
It forks only when an executable pre-evidence model is valid, expresses a
material causal belief about G at fixed H, and the chosen experiment can
distinguish the hidden twins.  Otherwise the raw prefix is saved without
calling the outcome a belief-revision test.

This is an exploratory runner, not a prevalence estimator.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import re
import sys
from pathlib import Path
from types import SimpleNamespace

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from wager.agent.cells import extract_cell  # noqa: E402
from wager.agent.llm_client import FoundryChat  # noqa: E402
from wager.contracts import Regime  # noqa: E402
from wager.harness.case_episode import build_world_server  # noqa: E402
from wager.harness.episode import CELL_TIMEOUT_S, MAX_COMPLETION_TOKENS  # noqa: E402
from wager.harness.kernel_proc import KernelClient  # noqa: E402
from wager.reward.sandbox import SandboxedSubmission, SandboxError  # noqa: E402

from scripts.probe_first_story_causal_fork import (  # noqa: E402
    SYSTEM,
    feedback,
    global_score,
    initial_prompt,
    record,
    select_last_scoreable,
)


REVISE = ROOT / "cases" / "first_story_scm_revise_v0"
RETAIN = ROOT / "cases" / "first_story_scm_retain_v0"
OUT = ROOT / "scripts" / "out" / "first_story_scm_fork"


def _artifact_hash(code: str | None) -> str | None:
    return hashlib.sha256(code.encode("utf-8")).hexdigest() if code else None


def _trajectory_view(events) -> list[dict]:
    return [
        {
            "verb": event.verb,
            "args": event.args,
            "cost": event.cost,
            "note": event.note,
        }
        for event in events
    ]


def _experiment_events(trajectory: list[dict]) -> list[dict]:
    return [event for event in trajectory if event["verb"] == "experiment"]


def causal_signature(
    code: str | None,
    columns: list[str],
    *,
    n_samples: int,
    seed: int,
) -> dict:
    """Measure the artifact's G effect at the fixed diagnostic H=5."""
    if not code:
        return {"scoreable": False, "error": "missing artifact"}
    regimes = {
        "H5_G3": {"humidity": 5.0, "feedstock_grade": 3.0},
        "H5_G7": {"humidity": 5.0, "feedstock_grade": 7.0},
    }
    try:
        means = {}
        with SandboxedSubmission(code, columns, timeout_s=15.0) as submission:
            for name, config in regimes.items():
                frame = submission.run(
                    Regime(config=config, context={}, horizon=None),
                    n_samples,
                    seed,
                )
                means[name] = {
                    column: float(frame[column].mean()) for column in columns
                }
        delta = means["H5_G7"]["outcome"] - means["H5_G3"]["outcome"]
        return {
            "scoreable": True,
            "error": None,
            "regimes": regimes,
            "means": means,
            "delta_outcome_G_at_H5": float(delta),
            "abs_delta_outcome_G_at_H5": abs(float(delta)),
        }
    except (SandboxError, ValueError, KeyError) as exc:
        return {"scoreable": False, "error": repr(exc)}


def truth_signature(case_dir: Path, *, n_samples: int, seed: int) -> dict:
    server = build_world_server(case_dir)
    regimes = {
        "H5_G3": {"humidity": 5.0, "feedstock_grade": 3.0},
        "H5_G7": {"humidity": 5.0, "feedstock_grade": 7.0},
    }
    means = {}
    for name, config in regimes.items():
        frame = server.world_sample(
            SimpleNamespace(config=config, context={}, horizon=None),
            n_samples,
            seed,
        )
        means[name] = {
            column: float(frame[column].mean()) for column in server.columns
        }
    delta = means["H5_G7"]["outcome"] - means["H5_G3"]["outcome"]
    return {
        "regimes": regimes,
        "means": means,
        "delta_outcome_G_at_H5": float(delta),
        "abs_delta_outcome_G_at_H5": abs(float(delta)),
    }


def run_common_prefix(
    model: str,
    seed_offset: int,
    max_prefix_turns: int,
    *,
    belief_delta_threshold: float,
    signature_n: int,
) -> dict:
    """Run one donor until its first experiment event, then freeze that cell."""
    server = build_world_server(REVISE, seed_offset=seed_offset)
    trace = []
    chat = FoundryChat(
        system=SYSTEM,
        model=model,
        max_completion_tokens=MAX_COMPLETION_TOKENS,
    )
    prompt = initial_prompt(server)
    selection = None
    abort = "no_experiment_selected"

    with KernelClient(server, cell_timeout_s=CELL_TIMEOUT_S) as kernel:
        for turn in range(1, max_prefix_turns + 1):
            notices = server.begin_turn(turn)
            for variable, frame in server.pop_deliveries():
                kernel.inject_dataframe(variable, frame)
            reply = chat.ask(prompt)
            cell = extract_cell(reply.content)
            if cell is None:
                abort = "no_cell"
                break

            mpre = trace[-1]["working_model"]["code"] if trace else None
            prefix_ledger = server.export_evidence_ledger()
            start = len(server.trajectory)
            result = kernel.run_cell(cell)
            row = record(
                turn, reply.content, cell, result, server, notices, start
            )
            events = row["trajectory"]
            if any(event["verb"] == "experiment" for event in events):
                selection = {
                    "turn": turn,
                    "reply_text": reply.content,
                    "cell": cell,
                    "cell_sha256": hashlib.sha256(cell.encode("utf-8")).hexdigest(),
                    "notices": notices,
                    "messages_through_action": copy.deepcopy(chat.messages),
                    "M_pre": mpre,
                    "prefix_evidence_ledger": prefix_ledger,
                    "preflight_action_record": row,
                    "preflight_action_trajectory": events,
                    "preflight_evidence_ledger_after": server.export_evidence_ledger(),
                }
                abort = "action_selected"
                break

            trace.append(row)
            if server.terminal:
                abort = "submitted_before_experiment"
                break
            if result.error and result.error.startswith("cell exceeded "):
                abort = "cell_timeout"
                break
            prompt = feedback(result, server)

    result = {
        "abort": abort,
        "trace": trace,
        "selection": selection,
        "evidence_ledger": (
            selection["prefix_evidence_ledger"]
            if selection is not None else server.export_evidence_ledger()
        ),
        "tokens": chat.usage.total_tokens,
        "llm_turn_usage": [
            {
                "prompt_tokens": turn.prompt_tokens,
                "completion_tokens": turn.completion_tokens,
                "reasoning_tokens": turn.reasoning_tokens,
                "latency_s": turn.latency_s,
            }
            for turn in chat.turns
        ],
    }
    if selection is None:
        return result

    mpre = selection["M_pre"]
    validation_error = "missing artifact" if mpre is None else server.validate_model(mpre)
    signature = causal_signature(
        mpre,
        server.columns,
        n_samples=signature_n,
        seed=seed_offset + 710_000,
    )
    formed = (
        validation_error is None
        and signature.get("scoreable", False)
        and signature["abs_delta_outcome_G_at_H5"] >= belief_delta_threshold
    )
    result.update({
        "M_pre_present": mpre is not None,
        "M_pre_valid": validation_error is None,
        "M_pre_validation_error": validation_error,
        "M_pre_signature": signature,
        "belief_delta_threshold": belief_delta_threshold,
        "causal_belief_formed": formed,
    })
    if validation_error is not None:
        result["abort"] = "M_pre_invalid" if mpre is not None else "M_pre_missing"
    elif not signature.get("scoreable", False):
        result["abort"] = "causal_belief_unscoreable"
    elif not formed:
        result["abort"] = "causal_belief_not_formed"
    return result


def classify_action(
    trajectory: list[dict],
    *,
    seed_offset: int,
    expectation_n: int,
    diagnostic_delta_threshold: float,
    off_manifold_tolerance: float,
) -> dict:
    """Classify whether the frozen experiment can distinguish the SCM twins."""
    revise = build_world_server(REVISE, seed_offset=seed_offset)
    retain = build_world_server(RETAIN, seed_offset=seed_offset)
    rows = []
    for index, event in enumerate(_experiment_events(trajectory)):
        args = event["args"]
        config = dict(args.get("config", {}))
        context = dict(args.get("context", {}))
        has_g = "feedstock_grade" in config
        has_h = "humidity" in config
        off_manifold = bool(has_g) and (
            not has_h
            or abs(
                float(config["feedstock_grade"])
                - (10.0 - float(config["humidity"]))
            ) > off_manifold_tolerance
        )
        regime = SimpleNamespace(
            config=config,
            context=context,
            horizon=args.get("horizon"),
        )
        seed = seed_offset + 810_000 + index
        revise_frame = revise.world_sample(regime, expectation_n, seed)
        retain_frame = retain.world_sample(regime, expectation_n, seed)
        revise_mean = float(revise_frame["outcome"].mean())
        retain_mean = float(retain_frame["outcome"].mean())
        expected_delta = retain_mean - revise_mean
        paired_difference = (
            retain_frame["outcome"].to_numpy()
            - revise_frame["outcome"].to_numpy()
        )
        expected_rms_delta = float(
            np.sqrt(np.mean(np.square(paired_difference)))
        )
        revise_std = float(revise_frame["outcome"].std(ddof=0))
        retain_std = float(retain_frame["outcome"].std(ddof=0))
        rows.append({
            "index": index,
            "request": args,
            "intervenes_G": has_g,
            "intervenes_H": has_h,
            "off_manifold_G": off_manifold,
            "expected_outcome_mean_revise": revise_mean,
            "expected_outcome_mean_retain": retain_mean,
            "expected_twin_delta_retain_minus_revise": expected_delta,
            "abs_expected_twin_delta": abs(expected_delta),
            "expected_paired_rms_delta": expected_rms_delta,
            "expected_outcome_std_revise": revise_std,
            "expected_outcome_std_retain": retain_std,
            "expected_twin_output_differs": (
                expected_rms_delta >= diagnostic_delta_threshold
            ),
        })
    has_off_manifold_g = any(row["off_manifold_G"] for row in rows)
    expected_diff = any(row["expected_twin_output_differs"] for row in rows)
    diagnostic_indices = [
        row["index"] for row in rows
        if row["off_manifold_G"] and row["expected_twin_output_differs"]
    ]
    diagnostic = bool(diagnostic_indices)
    return {
        "experiments": rows,
        "experiment_count": len(rows),
        "has_G_off_manifold_intervention": has_off_manifold_g,
        "expected_twin_output_differs": expected_diff,
        "diagnostic_experiment_indices": diagnostic_indices,
        "diagnostic_delta_threshold": diagnostic_delta_threshold,
        "off_manifold_tolerance": off_manifold_tolerance,
        "diagnostic": diagnostic,
        "classification": (
            "diagnostic_for_hidden_SCM"
            if diagnostic else "experimental_search_not_diagnostic"
        ),
    }


def replay_prefix_exact(server, prefix: dict, kernel: KernelClient) -> list[dict]:
    checks = []
    for donor in prefix["trace"]:
        ledger_before = server.export_evidence_ledger()
        notices = server.begin_turn(donor["turn"])
        deliveries = server.pop_deliveries()
        for variable, frame in deliveries:
            kernel.inject_dataframe(variable, frame)
        start = len(server.trajectory)
        result = kernel.run_cell(donor["cell"])
        actual_trajectory = _trajectory_view(server.trajectory[start:])
        checks.append({
            "turn": donor["turn"],
            "ledger_before": ledger_before,
            "notices": notices == donor["notices"],
            "delivery_count": len(deliveries),
            "no_deliveries": not deliveries,
            "stdout": _stable_stdout(result.stdout) == _stable_stdout(
                donor["cell_result"]["stdout"]
            ),
            "error": result.error == donor["cell_result"]["error"],
            "working_model": result.working_model == donor["working_model"]["code"],
            "working_model_status": (
                result.working_model_status == donor["working_model"]["status"]
            ),
            "trajectory": actual_trajectory == donor["trajectory"],
            "ledger_after": server.export_evidence_ledger(),
        })
    return checks


def _replay_checks_exact(checks: list[dict]) -> bool:
    ignored = {"turn", "ledger_before", "ledger_after", "delivery_count"}
    return all(
        all(value for key, value in row.items() if key not in ignored)
        for row in checks
    )


def _stable_stdout(value: str | None) -> str | None:
    """Remove only wall-clock metadata emitted by statsmodels summaries."""
    if value is None:
        return None
    return re.sub(
        r"(?m)^(Date|Time):\s+.*$",
        r"\1: <wall-clock normalized>",
        value,
    )


def _request_view(trajectory: list[dict]) -> list[dict]:
    return [
        {
            "verb": event["verb"],
            "args": event["args"],
            "cost": event["cost"],
        }
        for event in trajectory
    ]


def replay_and_continue(
    case_dir: Path,
    prefix: dict,
    model: str,
    seed_offset: int,
    max_turns: int,
) -> dict:
    server = build_world_server(case_dir, seed_offset=seed_offset)
    branch_trace = []
    action = prefix["selection"]
    preflight_requests = _request_view(action["preflight_action_trajectory"])

    with KernelClient(server, cell_timeout_s=CELL_TIMEOUT_S) as kernel:
        replay_checks = replay_prefix_exact(server, prefix, kernel)
        ledger_after_prefix = server.export_evidence_ledger()
        notices = server.begin_turn(action["turn"])
        action_notices = copy.deepcopy(notices)
        deliveries = server.pop_deliveries()
        for variable, frame in deliveries:
            kernel.inject_dataframe(variable, frame)
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
        action_record["phase"] = "frozen_diagnostic_action"
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
            for variable, frame in server.pop_deliveries():
                kernel.inject_dataframe(variable, frame)
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
            row["phase"] = "post_action"
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
                "prompt_tokens": turn.prompt_tokens,
                "completion_tokens": turn.completion_tokens,
                "reasoning_tokens": turn.reasoning_tokens,
                "latency_s": turn.latency_s,
            }
            for turn in chat.turns
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
    actual_requests = _request_view(action_record["trajectory"])
    return {
        "case_id": case_dir.name,
        "replay_checks": replay_checks,
        "replay_exact": _replay_checks_exact(replay_checks),
        "prefix_ledger_after_replay": ledger_after_prefix,
        "prefix_ledger_exact": ledger_after_prefix == prefix["evidence_ledger"],
        "ledger_after_action": ledger_after_action,
        "frozen_action_cell": action["cell"],
        "frozen_action_cell_sha256": hashlib.sha256(
            action["cell"].encode("utf-8")
        ).hexdigest(),
        "action_notices_exact": action_notices == action["notices"],
        "action_requests": actual_requests,
        "action_requests_match_preflight": actual_requests == preflight_requests,
        "abort": abort,
        "accepted": server.terminal,
        "R": final.get("R"),
        "submission_code": final.get("code"),
        "first_changed_model": first_changed,
        "last_working_model": last_code,
        "trace": branch_trace,
        "transcript": transcript,
        "evidence_ledger": server.export_evidence_ledger(),
        "tokens_continuation": tokens,
        "llm_turn_usage": llm_turn_usage,
    }


def _action_ledger(branch: dict, action_turn: int) -> list[dict]:
    return [
        row for row in branch["evidence_ledger"]
        if row["kind"] == "experiment" and row["turn"] == action_turn
    ]


def _ledger_requests(rows: list[dict]) -> list[dict]:
    return [row["request"] for row in rows]


def _action_record_exact(actual: dict, expected: dict) -> bool:
    """Full deterministic equality for the REVISE preflight replay."""
    keys = (
        "notices",
        "cell",
        "working_model",
        "budget_remaining",
        "trajectory",
    )
    if not all(actual.get(key) == expected.get(key) for key in keys):
        return False
    actual_result = actual.get("cell_result", {})
    expected_result = expected.get("cell_result", {})
    result_keys = ("ok", "error", "truncated")
    return (
        all(actual_result.get(key) == expected_result.get(key) for key in result_keys)
        and _stable_stdout(actual_result.get("stdout"))
        == _stable_stdout(expected_result.get("stdout"))
    )


def _score_delta(after: dict, before: dict) -> float | None:
    before_r = before.get("R") if before else None
    after_r = after.get("R") if after else None
    if before_r is None or after_r is None:
        return None
    return float(after_r - before_r)


def _signature_delta(after: dict, before: dict) -> float | None:
    key = "delta_outcome_G_at_H5"
    if not before.get("scoreable", False) or not after.get("scoreable", False):
        return None
    return float(after[key] - before[key])


def add_artifact_measurements(
    branch: dict,
    case_dir: Path,
    mpre: str,
    *,
    signature_n: int,
    signature_seed: int,
) -> None:
    artifact, source, last_score, failures = select_last_scoreable(
        case_dir, branch, mpre
    )
    mfirst = branch["first_changed_model"]
    scores = {
        "M_pre": global_score(case_dir, mpre),
        "M_first": global_score(case_dir, mfirst),
        "M_last": last_score,
    }
    signatures = {
        "truth": truth_signature(
            case_dir,
            n_samples=max(20_000, signature_n),
            seed=signature_seed,
        ),
        "M_pre": causal_signature(
            mpre,
            ["feedstock", "outcome"],
            n_samples=signature_n,
            seed=signature_seed,
        ),
        "M_first": causal_signature(
            mfirst,
            ["feedstock", "outcome"],
            n_samples=signature_n,
            seed=signature_seed,
        ),
        "M_last": causal_signature(
            artifact,
            ["feedstock", "outcome"],
            n_samples=signature_n,
            seed=signature_seed,
        ),
    }
    branch.update({
        "last_scoreable_model": artifact,
        "last_scoreable_source": source,
        "later_invalid_artifacts": failures,
        "scores": scores,
        "signatures": signatures,
        "change": {
            "M_first_differs_from_M_pre": bool(mfirst and mfirst != mpre),
            "M_last_differs_from_M_pre": bool(artifact and artifact != mpre),
            "hashes": {
                "M_pre": _artifact_hash(mpre),
                "M_first": _artifact_hash(mfirst),
                "M_last": _artifact_hash(artifact),
            },
            "score_R_delta_first_minus_pre": _score_delta(
                scores["M_first"], scores["M_pre"]
            ),
            "score_R_delta_last_minus_pre": _score_delta(
                scores["M_last"], scores["M_pre"]
            ),
            "causal_delta_first_minus_pre": _signature_delta(
                signatures["M_first"], signatures["M_pre"]
            ),
            "causal_delta_last_minus_pre": _signature_delta(
                signatures["M_last"], signatures["M_pre"]
            ),
        },
    })


def _sanitized_prefix(prefix: dict) -> dict:
    result = copy.deepcopy(prefix)
    selection = result.get("selection")
    if selection:
        selection.pop("messages_through_action", None)
    return result


def _write_early(
    target: Path,
    *,
    model: str,
    seed_offset: int,
    prefix: dict,
    action_classification: dict | None,
    gates: dict,
) -> None:
    payload = {
        "kind": "exploratory_first_story_SCM_action_fork",
        "claim_class": (
            "experimental_search_not_diagnostic"
            if action_classification is not None
            and not action_classification["diagnostic"]
            else "precondition_failed_no_update_inference"
        ),
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
        "claim_class": payload["claim_class"],
        "gates": gates,
    }, indent=2), flush=True)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", default="DeepSeek-V3.2")
    parser.add_argument("--seed-offset", type=int, default=95100)
    parser.add_argument("--belief-delta-threshold", type=float, default=3.0)
    parser.add_argument("--diagnostic-delta-threshold", type=float, default=1.0)
    parser.add_argument("--off-manifold-tolerance", type=float, default=0.25)
    parser.add_argument("--signature-n", type=int, default=4000)
    parser.add_argument("--action-expectation-n", type=int, default=20_000)
    parser.add_argument("--max-prefix-turns", type=int, default=12)
    parser.add_argument("--max-turns", type=int, default=24)
    parser.add_argument("--out", type=Path, default=None)
    args = parser.parse_args()

    OUT.mkdir(parents=True, exist_ok=True)
    target = args.out or OUT / f"probe_{args.model}_seed{args.seed_offset}.json"
    target.parent.mkdir(parents=True, exist_ok=True)
    revise_sheet = build_world_server(REVISE, seed_offset=args.seed_offset).describe()
    retain_sheet = build_world_server(RETAIN, seed_offset=args.seed_offset).describe()
    twin_sheet_identical = revise_sheet == retain_sheet
    if not twin_sheet_identical:
        prefix = {
            "abort": "agent_facing_twins_differ",
            "trace": [],
            "selection": None,
            "evidence_ledger": [],
            "tokens": 0,
        }
        _write_early(
            target,
            model=args.model,
            seed_offset=args.seed_offset,
            prefix=prefix,
            action_classification=None,
            gates={"twin_sheet_identical": False},
        )
        return

    prefix = run_common_prefix(
        args.model,
        args.seed_offset,
        args.max_prefix_turns,
        belief_delta_threshold=args.belief_delta_threshold,
        signature_n=args.signature_n,
    )
    prefix_gates = {
        "twin_sheet_identical": twin_sheet_identical,
        "action_selected": prefix.get("selection") is not None,
        "M_pre_present": prefix.get("M_pre_present", False),
        "M_pre_valid": prefix.get("M_pre_valid", False),
        "causal_belief_formed": prefix.get("causal_belief_formed", False),
    }
    if prefix["abort"] != "action_selected":
        _write_early(
            target,
            model=args.model,
            seed_offset=args.seed_offset,
            prefix=prefix,
            action_classification=None,
            gates=prefix_gates,
        )
        return

    action_classification = classify_action(
        prefix["selection"]["preflight_action_trajectory"],
        seed_offset=args.seed_offset,
        expectation_n=args.action_expectation_n,
        diagnostic_delta_threshold=args.diagnostic_delta_threshold,
        off_manifold_tolerance=args.off_manifold_tolerance,
    )
    prefix["action_classification"] = action_classification
    prefix_gates["action_diagnostic"] = action_classification["diagnostic"]
    if not action_classification["diagnostic"]:
        prefix["abort"] = "action_not_diagnostic"
        _write_early(
            target,
            model=args.model,
            seed_offset=args.seed_offset,
            prefix=prefix,
            action_classification=action_classification,
            gates=prefix_gates,
        )
        return

    branches = {
        "revise": replay_and_continue(
            REVISE, prefix, args.model, args.seed_offset, args.max_turns
        ),
        "retain": replay_and_continue(
            RETAIN, prefix, args.model, args.seed_offset, args.max_turns
        ),
    }
    mpre = prefix["selection"]["M_pre"]
    for index, (name, case_dir) in enumerate((("revise", REVISE), ("retain", RETAIN))):
        add_artifact_measurements(
            branches[name],
            case_dir,
            mpre,
            signature_n=args.signature_n,
            signature_seed=args.seed_offset + 910_000 + index,
        )

    action_turn = prefix["selection"]["turn"]
    action_ledgers = {
        name: _action_ledger(branch, action_turn)
        for name, branch in branches.items()
    }
    gates = {
        **prefix_gates,
        "replay_exact_both": all(branch["replay_exact"] for branch in branches.values()),
        "prefix_ledger_exact_both": all(
            branch["prefix_ledger_exact"] for branch in branches.values()
        ),
        "frozen_action_cell_exact_both": all(
            branch["frozen_action_cell_sha256"]
            == prefix["selection"]["cell_sha256"]
            for branch in branches.values()
        ),
        "action_notices_exact_both": all(
            branch["action_notices_exact"] for branch in branches.values()
        ),
        "action_requests_match_preflight_both": all(
            branch["action_requests_match_preflight"] for branch in branches.values()
        ),
        "preflight_action_record_exact_revise": _action_record_exact(
            branches["revise"]["trace"][0],
            prefix["selection"]["preflight_action_record"],
        ),
        "preflight_action_ledger_exact_revise": (
            branches["revise"]["ledger_after_action"]
            == prefix["selection"]["preflight_evidence_ledger_after"]
        ),
        "same_action_ledger_requests": (
            bool(action_ledgers["revise"])
            and _ledger_requests(action_ledgers["revise"])
            == _ledger_requests(action_ledgers["retain"])
        ),
        "action_results_differ": action_ledgers["revise"] != action_ledgers["retain"],
        "last_artifact_scoreable_both": all(
            branch["scores"]["M_last"].get("scoreable", False)
            for branch in branches.values()
        ),
    }
    payload = {
        "kind": "exploratory_first_story_SCM_action_fork",
        "claim_class": "diagnostic_causal_belief_update_probe",
        "model": args.model,
        "seed_offset": args.seed_offset,
        "thresholds": {
            "belief_delta": args.belief_delta_threshold,
            "diagnostic_delta": args.diagnostic_delta_threshold,
            "off_manifold_tolerance": args.off_manifold_tolerance,
        },
        "prefix": _sanitized_prefix(prefix),
        "action_classification": action_classification,
        "action_ledgers": action_ledgers,
        "branches": branches,
        "gates": gates,
        "all": all(gates.values()),
    }
    target.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "out": str(target),
        "gates": gates,
        "all": payload["all"],
        "abort": {name: branch["abort"] for name, branch in branches.items()},
        "scores_R": {
            name: {
                checkpoint: score.get("R")
                for checkpoint, score in branch["scores"].items()
            }
            for name, branch in branches.items()
        },
        "causal_delta": {
            name: {
                checkpoint: signature.get("delta_outcome_G_at_H5")
                for checkpoint, signature in branch["signatures"].items()
            }
            for name, branch in branches.items()
        },
    }, indent=2), flush=True)


if __name__ == "__main__":
    main()
