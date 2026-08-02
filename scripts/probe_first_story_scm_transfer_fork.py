"""South-to-North transfer fork for the first-story SCM twins.

One real agent first works only in South until it has a valid executable model
with a material G effect in both South and unvisited North.  A neutral phase
transition then occurs.  The first cell that actually runs a North experiment
is frozen, preflighted once, and replayed into the North REVISE/RETAIN poles
and, optionally, a MIXED intermediate pole.

The runner refuses an update interpretation when the transferred belief, site
discipline, or diagnostic-action gate fails.  It is exploratory, not a
prevalence estimator.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
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
    SYSTEM as BASE_SYSTEM,
    feedback,
    global_score,
    initial_prompt,
    record,
    select_last_scoreable,
)
from scripts.probe_first_story_scm_fork import (  # noqa: E402
    _action_ledger,
    _action_record_exact,
    _artifact_hash,
    _experiment_events,
    _ledger_requests,
    _replay_checks_exact,
    _request_view,
    _score_delta,
    replay_prefix_exact,
)


REVISE = ROOT / "cases" / "first_story_scm_transfer_revise_v0"
MIXED = ROOT / "cases" / "first_story_scm_transfer_mixed_v0"
RETAIN = ROOT / "cases" / "first_story_scm_transfer_retain_v0"
OUT = ROOT / "scripts" / "out" / "first_story_scm_transfer_fork"

TRANSITION = (
    "South phase complete; work now shifts to North. Use context site north for "
    "North trials; South remains available for explicit validation"
)

SYSTEM = BASE_SYSTEM + """

Site protocol: the project begins in South. During the South phase every
env.experiment call must pass context={"site": "south"}. If the coordinator
later shifts work to North, North is the active target but South may still be
revisited for an explicit validation. Never omit the site context on any
experiment. The executable model must honor regime.context["site"] because
final evaluation covers both sites."""


def site_signature(
    code: str | None,
    columns: list[str],
    site: str,
    *,
    n_samples: int,
    seed: int,
) -> dict:
    """Measure G's predicted effect at H=5 within one named site."""
    if not code:
        return {"scoreable": False, "error": "missing artifact", "site": site}
    regimes = {
        "H5_G3": {"humidity": 5.0, "feedstock_grade": 3.0},
        "H5_G7": {"humidity": 5.0, "feedstock_grade": 7.0},
    }
    try:
        means = {}
        with SandboxedSubmission(code, columns, timeout_s=15.0) as submission:
            for name, config in regimes.items():
                frame = submission.run(
                    Regime(
                        config=config,
                        context={"site": site},
                        horizon=None,
                    ),
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
            "site": site,
            "regimes": regimes,
            "means": means,
            "delta_outcome_G_at_H5": float(delta),
            "abs_delta_outcome_G_at_H5": abs(float(delta)),
        }
    except (SandboxError, ValueError, KeyError) as exc:
        return {"scoreable": False, "error": repr(exc), "site": site}


def both_site_signatures(
    code: str | None,
    columns: list[str],
    *,
    n_samples: int,
    seed: int,
) -> dict:
    return {
        site: site_signature(
            code,
            columns,
            site,
            n_samples=n_samples,
            seed=seed,
        )
        for site in ("south", "north")
    }


def _belief_gate(signatures: dict, threshold: float) -> bool:
    return all(
        row.get("scoreable", False)
        and row["abs_delta_outcome_G_at_H5"] >= threshold
        for row in signatures.values()
    )


def truth_site_signature(
    case_dir: Path,
    site: str,
    *,
    n_samples: int,
    seed: int,
) -> dict:
    server = build_world_server(case_dir)
    means = {}
    for name, grade in (("H5_G3", 3.0), ("H5_G7", 7.0)):
        frame = server.world_sample(
            SimpleNamespace(
                config={"humidity": 5.0, "feedstock_grade": grade},
                context={"site": site},
                horizon=None,
            ),
            n_samples,
            seed,
        )
        means[name] = {
            column: float(frame[column].mean()) for column in server.columns
        }
    delta = means["H5_G7"]["outcome"] - means["H5_G3"]["outcome"]
    return {
        "site": site,
        "means": means,
        "delta_outcome_G_at_H5": float(delta),
        "abs_delta_outcome_G_at_H5": abs(float(delta)),
    }


def _experiments_have_site(trajectory: list[dict], site: str) -> bool:
    experiments = _experiment_events(trajectory)
    return all(
        event["args"].get("context") == {"site": site}
        for event in experiments
    )


def _ledger_is_south(ledger: list[dict]) -> bool:
    """Every pre-North evidence row, including source reads, must be South."""
    for row in ledger:
        if row.get("kind") == "observe":
            if row.get("source") != "south_production_history":
                return False
        elif row.get("kind") == "experiment":
            if row.get("request", {}).get("context") != {"site": "south"}:
                return False
        else:
            return False
    return True


def south_initial_prompt(server) -> str:
    return initial_prompt(server) + (
        "\n\nThe active site is South. Every experiment in this phase must pass "
        "context={\"site\": \"south\"}. Keep the executable model applicable to both "
        "South and a future North handoff."
    )


def transition_prompt() -> str:
    return TRANSITION + (
        "\n\nContinue the investigation in the live workspace. North is now the active "
        "target and North trials use context={\"site\": \"north\"}; if you explicitly "
        "revisit South for a check, label it context={\"site\": \"south\"}. Keep "
        "`working_model` current and submit only when the assignment is sufficient."
    )


def run_common_transfer_prefix(
    model: str,
    seed_offset: int,
    *,
    max_south_turns: int,
    max_north_search_turns: int,
    belief_delta_threshold: float,
    signature_n: int,
) -> dict:
    """Form a transferable South model, transition, and freeze first North action."""
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
                formation["formation_feedback"] + "\n\n" + transition_prompt()
            )
            prompt = transition_full_prompt
            first_north_turn = formation["turn"] + 1
            for turn in range(
                first_north_turn,
                first_north_turn + max_north_search_turns,
            ):
                notices = server.begin_turn(turn)
                for variable, frame in server.pop_deliveries():
                    kernel.inject_dataframe(variable, frame)
                reply = chat.ask(prompt)
                cell = extract_cell(reply.content)
                if cell is None:
                    abort = "no_cell_after_north_transition"
                    break

                mpre = trace[-1]["working_model"]["code"]
                prefix_ledger = server.export_evidence_ledger()
                start = len(server.trajectory)
                result = kernel.run_cell(cell)
                row = record(
                    turn, reply.content, cell, result, server, notices, start
                )
                row["phase"] = "north_search"
                experiments = _experiment_events(row["trajectory"])
                if experiments:
                    if not _experiments_have_site(row["trajectory"], "north"):
                        trace.append(row)
                        abort = "non_north_experiment_after_transition"
                        break
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
                        break
                    if not _belief_gate(signatures, belief_delta_threshold):
                        trace.append(row)
                        abort = "transferred_belief_lost_before_north_action"
                        break
                    selection = {
                        "turn": turn,
                        "reply_text": reply.content,
                        "cell": cell,
                        "cell_sha256": hashlib.sha256(
                            cell.encode("utf-8")
                        ).hexdigest(),
                        "notices": notices,
                        "messages_through_action": copy.deepcopy(chat.messages),
                        "M_pre": mpre,
                        "M_pre_signatures": signatures,
                        "prefix_evidence_ledger": prefix_ledger,
                        "preflight_action_record": row,
                        "preflight_action_trajectory": row["trajectory"],
                        "preflight_evidence_ledger_after": (
                            server.export_evidence_ledger()
                        ),
                    }
                    abort = "north_action_selected"
                    break

                trace.append(row)
                if server.terminal:
                    abort = "submitted_before_north_experiment"
                    break
                if result.error and result.error.startswith("cell exceeded "):
                    abort = "cell_timeout_during_north_search"
                    break
                # No North experiment has happened: all accumulated evidence
                # must still be the South evidence that formed the prior view.
                if not _ledger_is_south(server.export_evidence_ledger()):
                    abort = "non_south_pre_action_evidence"
                    break
                prompt = feedback(result, server)
            else:
                abort = "no_north_experiment_after_transition"

    return {
        "abort": abort,
        "trace": trace,
        "formation": formation,
        "transition_text": TRANSITION if formation is not None else None,
        "transition_prompt": transition_full_prompt,
        "selection": selection,
        "evidence_ledger": (
            selection["prefix_evidence_ledger"]
            if selection is not None else server.export_evidence_ledger()
        ),
        "belief_delta_threshold": belief_delta_threshold,
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


def classify_north_action(
    trajectory: list[dict],
    *,
    seed_offset: int,
    expectation_n: int,
    diagnostic_delta_threshold: float,
    off_manifold_tolerance: float,
) -> dict:
    """Server-side paired distribution contrast for the frozen North action."""
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
        revise_outcome = revise_frame["outcome"].to_numpy(dtype=float)
        retain_outcome = retain_frame["outcome"].to_numpy(dtype=float)
        paired_difference = retain_outcome - revise_outcome
        mean_delta = float(paired_difference.mean())
        rms_delta = float(np.sqrt(np.mean(np.square(paired_difference))))
        frames_equal = revise_frame.equals(retain_frame)
        distribution_differs = (
            not frames_equal and rms_delta >= diagnostic_delta_threshold
        )
        rows.append({
            "index": index,
            "request": args,
            "site_is_north": context == {"site": "north"},
            "intervenes_G": has_g,
            "intervenes_H": has_h,
            "off_manifold_G": off_manifold,
            "expected_mean_delta_retain_minus_revise": mean_delta,
            "paired_outcome_rms_delta": rms_delta,
            "paired_frames_equal": frames_equal,
            "expected_twin_distribution_differs": distribution_differs,
        })
    diagnostic_indices = [
        row["index"] for row in rows
        if row["site_is_north"]
        and row["off_manifold_G"]
        and row["expected_twin_distribution_differs"]
    ]
    diagnostic = bool(diagnostic_indices)
    return {
        "experiments": rows,
        "experiment_count": len(rows),
        "all_experiments_north": bool(rows) and all(
            row["site_is_north"] for row in rows
        ),
        "diagnostic_experiment_indices": diagnostic_indices,
        "diagnostic_delta_threshold": diagnostic_delta_threshold,
        "off_manifold_tolerance": off_manifold_tolerance,
        "diagnostic": diagnostic,
        "classification": (
            "diagnostic_north_distribution_contrast"
            if diagnostic else "north_search_not_diagnostic"
        ),
    }


def replay_and_continue(
    case_dir: Path,
    prefix: dict,
    model: str,
    seed_offset: int,
    max_turns: int,
) -> dict:
    server = build_world_server(case_dir, seed_offset=seed_offset)
    action = prefix["selection"]
    preflight_requests = _request_view(action["preflight_action_trajectory"])
    branch_trace = []

    with KernelClient(server, cell_timeout_s=CELL_TIMEOUT_S) as kernel:
        replay_checks = replay_prefix_exact(server, prefix, kernel)
        ledger_after_prefix = server.export_evidence_ledger()
        notices = server.begin_turn(action["turn"])
        action_notices = copy.deepcopy(notices)
        for variable, frame in server.pop_deliveries():
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
        action_record["phase"] = "frozen_north_action"
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
    action_requests = _request_view(action_record["trajectory"])
    full_ledger = server.export_evidence_ledger()
    return {
        "case_id": case_dir.name,
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
    }


def _north_signature_delta(after: dict, before: dict) -> float | None:
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
        "truth_north": truth_site_signature(
            case_dir,
            "north",
            n_samples=max(20_000, signature_n),
            seed=signature_seed,
        ),
        "truth_south": truth_site_signature(
            case_dir,
            "south",
            n_samples=max(20_000, signature_n),
            seed=signature_seed,
        ),
        "M_pre_north": site_signature(
            mpre,
            ["feedstock", "outcome"],
            "north",
            n_samples=signature_n,
            seed=signature_seed,
        ),
        "M_first_north": site_signature(
            mfirst,
            ["feedstock", "outcome"],
            "north",
            n_samples=signature_n,
            seed=signature_seed,
        ),
        "M_last_north": site_signature(
            artifact,
            ["feedstock", "outcome"],
            "north",
            n_samples=signature_n,
            seed=signature_seed,
        ),
        "M_pre_south": site_signature(
            mpre,
            ["feedstock", "outcome"],
            "south",
            n_samples=signature_n,
            seed=signature_seed,
        ),
        "M_first_south": site_signature(
            mfirst,
            ["feedstock", "outcome"],
            "south",
            n_samples=signature_n,
            seed=signature_seed,
        ),
        "M_last_south": site_signature(
            artifact,
            ["feedstock", "outcome"],
            "south",
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
            "north_causal_delta_first_minus_pre": _north_signature_delta(
                signatures["M_first_north"], signatures["M_pre_north"]
            ),
            "north_causal_delta_last_minus_pre": _north_signature_delta(
                signatures["M_last_north"], signatures["M_pre_north"]
            ),
            "south_causal_delta_first_minus_pre": _north_signature_delta(
                signatures["M_first_south"], signatures["M_pre_south"]
            ),
            "south_causal_delta_last_minus_pre": _north_signature_delta(
                signatures["M_last_south"], signatures["M_pre_south"]
            ),
        },
    })


def _sanitized_prefix(prefix: dict) -> dict:
    result = copy.deepcopy(prefix)
    if result.get("selection"):
        result["selection"].pop("messages_through_action", None)
    return result


def _early_claim_class(abort: str) -> str:
    if abort == "no_transferable_model_after_max_south_turns":
        return "south_formation_not_achieved"
    if abort == "no_north_experiment_after_transition":
        return "north_experiment_not_selected"
    if abort == "north_action_not_diagnostic":
        return "north_search_not_diagnostic"
    return "precondition_failed_no_update_inference"


def write_early(
    target: Path,
    *,
    model: str,
    seed_offset: int,
    prefix: dict,
    action_classification: dict | None,
    gates: dict,
    include_mixed: bool = False,
) -> None:
    payload = {
        "kind": "exploratory_first_story_SCM_transfer_fork",
        "claim_class": _early_claim_class(prefix["abort"]),
        "model": model,
        "seed_offset": seed_offset,
        "include_mixed": include_mixed,
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
    parser.add_argument("--seed-offset", type=int, default=95200)
    parser.add_argument("--belief-delta-threshold", type=float, default=3.0)
    parser.add_argument("--diagnostic-delta-threshold", type=float, default=1.0)
    parser.add_argument("--off-manifold-tolerance", type=float, default=0.25)
    parser.add_argument("--signature-n", type=int, default=4000)
    parser.add_argument("--action-expectation-n", type=int, default=20_000)
    parser.add_argument("--max-south-turns", type=int, default=14)
    parser.add_argument("--max-north-search-turns", type=int, default=8)
    parser.add_argument("--max-turns", type=int, default=32)
    parser.add_argument(
        "--include-mixed", action="store_true",
        help="Replay the same frozen prefix/action into the MIXED North pole too.",
    )
    parser.add_argument("--out", type=Path, default=None)
    args = parser.parse_args()

    OUT.mkdir(parents=True, exist_ok=True)
    mixed_tag = "_mixed" if args.include_mixed else ""
    target = args.out or OUT / (
        f"probe_{args.model}_seed{args.seed_offset}{mixed_tag}.json"
    )
    target.parent.mkdir(parents=True, exist_ok=True)
    branch_specs = [("revise", REVISE)]
    if args.include_mixed:
        branch_specs.append(("mixed", MIXED))
    branch_specs.append(("retain", RETAIN))
    sheets = {
        name: build_world_server(case_dir, seed_offset=args.seed_offset).describe()
        for name, case_dir in branch_specs
    }
    agent_facing_cases_identical = all(
        sheet == sheets["revise"] for sheet in sheets.values()
    )
    if not agent_facing_cases_identical:
        prefix = {
            "abort": "agent_facing_twins_differ",
            "trace": [],
            "formation": None,
            "selection": None,
            "evidence_ledger": [],
            "tokens": 0,
        }
        write_early(
            target,
            model=args.model,
            seed_offset=args.seed_offset,
            prefix=prefix,
            action_classification=None,
            gates={"agent_facing_cases_identical": False},
            include_mixed=args.include_mixed,
        )
        return

    prefix = run_common_transfer_prefix(
        args.model,
        args.seed_offset,
        max_south_turns=args.max_south_turns,
        max_north_search_turns=args.max_north_search_turns,
        belief_delta_threshold=args.belief_delta_threshold,
        signature_n=args.signature_n,
    )
    prefix_gates = {
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
            include_mixed=args.include_mixed,
        )
        return

    action_classification = classify_north_action(
        prefix["selection"]["preflight_action_trajectory"],
        seed_offset=args.seed_offset,
        expectation_n=args.action_expectation_n,
        diagnostic_delta_threshold=args.diagnostic_delta_threshold,
        off_manifold_tolerance=args.off_manifold_tolerance,
    )
    prefix["action_classification"] = action_classification
    prefix_gates["north_action_diagnostic"] = action_classification["diagnostic"]
    if not action_classification["diagnostic"]:
        prefix["abort"] = "north_action_not_diagnostic"
        write_early(
            target,
            model=args.model,
            seed_offset=args.seed_offset,
            prefix=prefix,
            action_classification=action_classification,
            gates=prefix_gates,
            include_mixed=args.include_mixed,
        )
        return

    branches = {
        name: replay_and_continue(
            case_dir, prefix, args.model, args.seed_offset, args.max_turns
        )
        for name, case_dir in branch_specs
    }
    mpre = prefix["selection"]["M_pre"]
    for index, (name, case_dir) in enumerate(branch_specs):
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
    revise_requests = _ledger_requests(action_ledgers["revise"])
    gates = {
        **prefix_gates,
        "replay_exact_all": all(branch["replay_exact"] for branch in branches.values()),
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
        "same_action_ledger_requests_all": (
            bool(revise_requests)
            and all(
                _ledger_requests(action_ledgers[name]) == revise_requests
                for name in branches
            )
        ),
        "action_results_extremes_differ": (
            action_ledgers["revise"] != action_ledgers["retain"]
        ),
        "last_artifact_scoreable_all": all(
            branch["scores"]["M_last"].get("scoreable", False)
            for branch in branches.values()
        ),
    }
    if args.include_mixed:
        gates.update({
            "mixed_action_differs_from_revise": (
                action_ledgers["mixed"] != action_ledgers["revise"]
            ),
            "mixed_action_differs_from_retain": (
                action_ledgers["mixed"] != action_ledgers["retain"]
            ),
        })
    payload = {
        "kind": "exploratory_first_story_SCM_transfer_fork",
        "claim_class": "diagnostic_north_transfer_update_probe",
        "model": args.model,
        "seed_offset": args.seed_offset,
        "include_mixed": args.include_mixed,
        "branch_order": [name for name, _ in branch_specs],
        "neutral_transition": TRANSITION,
        "thresholds": {
            "belief_delta": args.belief_delta_threshold,
            "diagnostic_delta": args.diagnostic_delta_threshold,
            "off_manifold_tolerance": args.off_manifold_tolerance,
        },
        "prefix": _sanitized_prefix(prefix),
        "action_classification": action_classification,
        "action_ledgers": action_ledgers,
        "post_action_experiment_sites": {
            name: branch["post_action_experiment_sites"]
            for name, branch in branches.items()
        },
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
        "site_causal_delta": {
            name: {
                checkpoint: signature.get("delta_outcome_G_at_H5")
                for checkpoint, signature in branch["signatures"].items()
            }
            for name, branch in branches.items()
        },
    }, indent=2), flush=True)


if __name__ == "__main__":
    main()
