"""Exploratory Corral-lite probe: fork after the agent chooses its own action.

The high range opens without a served report.  One common agent chooses the
first experiment/submit action; that exact cell is then executed in both
hidden-world twins.  Thus the causal fork starts at the result, not at two
independent stochastic action choices.
"""

from __future__ import annotations

import argparse
import copy
import json
import re
import sys
from pathlib import Path
from types import SimpleNamespace

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from wager.agent.cells import extract_cell  # noqa: E402
from wager.agent.llm_client import FoundryChat  # noqa: E402
from wager.factory.overgen_stream_tools import build_reference_from_ledger  # noqa: E402
from wager.harness.case_episode import build_world_server  # noqa: E402
from wager.harness.episode import CELL_TIMEOUT_S, MAX_COMPLETION_TOKENS  # noqa: E402
from wager.harness.kernel_proc import KernelClient  # noqa: E402
from wager.report.checkpoint_score import CheckpointScorer  # noqa: E402

from scripts.fork_overgen_stream_v0 import (  # noqa: E402
    ELIGIBLE_MAX_PREFIX_TURNS,
    ELIGIBLE_MAX_TURNS,
    LIMITED,
    OUT,
    TRANSFER,
    _apply_content_variant,
    _apply_protocol_variant,
    _checkpoint_codes,
    _initial_prompt,
    _record,
    run_prefix,
    score_checkpoints,
)


NEUTRAL_SYSTEM = """You are an investigator building a predictive model of an unknown system through a Python REPL, on a budget.

Each reply has TWO parts, IN THIS ORDER:
1. REASONING (a few sentences): what the latest result means for the practical modeling objective, what remains unresolved, and what you will do next and why.
2. Exactly ONE Python cell inside a ```python fence: the concrete next step.

The kernel runs the cell and returns stdout, so PRINT what you want to inspect; variables persist across cells. `env` provides describe, observe, experiment and submit as documented in the brief. You are responsible for deciding when the investigation is sufficient and for handing back a valid executable model."""


def neutral_feedback(result, server):
    prompt = (
        f"Kernel output (ok={result.ok}, budget remaining={server.budget_remaining:.0f}):\n"
        + (result.stdout or "(no stdout)")
    )
    if result.error:
        prompt += "\nTRACEBACK:\n" + result.error
    return prompt + (
        "\n\nDecide the most useful next step for the modeling objective, then write your next "
        "cell (or build and env.submit(code) when the work is sufficient)."
    )


def build_probe_server(case_dir, seed_offset, content_variant):
    return _apply_protocol_variant(
        _apply_content_variant(
            build_world_server(case_dir, seed_offset=seed_offset), content_variant
        ),
        "own_experiment",
    )


def replay_frozen_prefix(server, prefix, kernel):
    checks = []
    for donor in prefix["trace"]:
        notices = server.begin_turn(donor["turn"], fire_events=False)
        if notices or server.pop_deliveries():
            raise RuntimeError("event fired inside the frozen prefix")
        result = kernel.run_cell(donor["cell"])
        checks.append({
            "turn": donor["turn"],
            "stdout": result.stdout == donor["cell_result"]["stdout"],
            "error": result.error == donor["cell_result"]["error"],
            "working_model": result.working_model == donor["working_model"]["code"],
            "working_model_status": (
                result.working_model_status == donor["working_model"]["status"]
            ),
        })
    return checks


def classify_action(cell):
    if re.search(r"\benv\s*\.\s*experiment\s*\(", cell):
        return "experiment"
    if re.search(r"\benv\s*\.\s*submit\s*\(", cell):
        return "submit"
    return "local"


def choose_common_action(prefix, model, seed_offset, content_variant, max_turns):
    """Run identical post-unlock local work until the first experiment/submit cell.

    The chosen action cell is sampled once but deliberately not executed here.
    """
    server = build_probe_server(LIMITED, seed_offset, content_variant)
    common_trace = []
    with KernelClient(server, cell_timeout_s=CELL_TIMEOUT_S) as kernel:
        replay_checks = replay_frozen_prefix(server, prefix, kernel)
        chat = FoundryChat(
            system=NEUTRAL_SYSTEM,
            model=model,
            max_completion_tokens=MAX_COMPLETION_TOKENS,
        )
        chat.messages = copy.deepcopy(prefix["messages"])
        prompt = prefix["next_prompt"]
        first_turn = prefix["trace"][-1]["turn"] + 1
        for turn in range(first_turn, max_turns + 1):
            traj_before = len(server.trajectory)
            notices = server.begin_turn(turn, fire_events=False)
            if turn == first_turn:
                notices.extend(server.fire_event(0, turn_idx=turn))
            if server.pop_deliveries():
                raise RuntimeError("own_experiment event unexpectedly delivered data")
            if notices:
                prompt = "\n".join(f"[NOTICE] {n}" for n in notices) + "\n\n" + prompt
            reply = chat.ask(prompt)
            cell = extract_cell(reply.content)
            if cell is None:
                return {
                    "abort": "no_cell",
                    "replay_checks": replay_checks,
                    "common_trace": common_trace,
                    "tokens": chat.usage.total_tokens,
                }
            action_kind = classify_action(cell)
            if action_kind != "local":
                return {
                    "abort": "action_selected",
                    "replay_checks": replay_checks,
                    "common_trace": common_trace,
                    "action": {
                        "turn": turn,
                        "kind": action_kind,
                        "reply_text": reply.content,
                        "cell": cell,
                        "notices": notices,
                        "trajectory_start": traj_before,
                    },
                    "messages_through_action": copy.deepcopy(chat.messages),
                    "tokens": chat.usage.total_tokens,
                    "unlock_turn": first_turn,
                }
            result = kernel.run_cell(cell)
            common_trace.append(
                _record(turn, reply, cell, result, server, notices, traj_before)
            )
            if server.terminal:
                raise RuntimeError("a local-classified cell unexpectedly terminated the episode")
            if not result.ok and result.error and result.error.startswith("cell exceeded "):
                return {
                    "abort": "cell_timeout",
                    "replay_checks": replay_checks,
                    "common_trace": common_trace,
                    "tokens": chat.usage.total_tokens,
                }
            prompt = neutral_feedback(result, server)
    return {
        "abort": "max_turns_before_action",
        "replay_checks": replay_checks,
        "common_trace": common_trace,
        "tokens": chat.usage.total_tokens,
    }


def replay_common_and_continue(
    case_dir, prefix, selection, model, seed_offset, content_variant, max_turns
):
    server = build_probe_server(case_dir, seed_offset, content_variant)
    branch_trace = []
    with KernelClient(server, cell_timeout_s=CELL_TIMEOUT_S) as kernel:
        replay_checks = replay_frozen_prefix(server, prefix, kernel)
        for donor in selection["common_trace"]:
            notices = server.begin_turn(donor["turn"], fire_events=False)
            if donor["turn"] == selection["unlock_turn"]:
                notices.extend(server.fire_event(0, turn_idx=donor["turn"]))
            if server.pop_deliveries():
                raise RuntimeError("own_experiment event unexpectedly delivered data")
            result = kernel.run_cell(donor["cell"])
            replay_checks.append({
                "turn": donor["turn"],
                "stdout": result.stdout == donor["cell_result"]["stdout"],
                "error": result.error == donor["cell_result"]["error"],
                "working_model": result.working_model == donor["working_model"]["code"],
                "working_model_status": (
                    result.working_model_status == donor["working_model"]["status"]
                ),
            })

        action = selection["action"]
        traj_before = len(server.trajectory)
        notices = server.begin_turn(action["turn"], fire_events=False)
        if action["turn"] == selection["unlock_turn"]:
            notices.extend(server.fire_event(0, turn_idx=action["turn"]))
        if server.pop_deliveries():
            raise RuntimeError("own_experiment event unexpectedly delivered data")
        result = kernel.run_cell(action["cell"])
        branch_trace.append(_record(
            action["turn"],
            SimpleNamespace(content=action["reply_text"]),
            action["cell"],
            result,
            server,
            notices,
            traj_before,
        ))

        chat = FoundryChat(
            system=NEUTRAL_SYSTEM,
            model=model,
            max_completion_tokens=MAX_COMPLETION_TOKENS,
        )
        chat.messages = copy.deepcopy(selection["messages_through_action"])
        abort = "submitted" if server.terminal else "max_turns"
        prompt = neutral_feedback(result, server)
        for turn in range(action["turn"] + 1, max_turns + 1):
            if server.terminal:
                break
            traj_before = len(server.trajectory)
            notices = server.begin_turn(turn, fire_events=False)
            if notices:
                prompt = "\n".join(f"[NOTICE] {n}" for n in notices) + "\n\n" + prompt
            reply = chat.ask(prompt)
            cell = extract_cell(reply.content)
            if cell is None:
                abort = "no_cell"
                break
            result = kernel.run_cell(cell)
            branch_trace.append(_record(
                turn, reply, cell, result, server, notices, traj_before
            ))
            if server.terminal:
                abort = "submitted"
                break
            if not result.ok and result.error and result.error.startswith("cell exceeded "):
                abort = "cell_timeout"
                break
            prompt = neutral_feedback(result, server)

    final = server.result or {}
    exact = all(
        all(value for key, value in row.items() if key != "turn")
        for row in replay_checks
    )
    return {
        "case_id": case_dir.name,
        "replay_checks": replay_checks,
        "replay_exact": exact,
        "abort": abort,
        "accepted": server.terminal,
        "R": final.get("R"),
        "submission_code": final.get("code"),
        "trace": branch_trace,
        "evidence_ledger": server.export_evidence_ledger(),
        "tokens_continuation": chat.usage.total_tokens,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", default="DeepSeek-V3.2")
    parser.add_argument("--seed-offset", type=int, default=94700)
    parser.add_argument("--max-prefix-turns", type=int, default=ELIGIBLE_MAX_PREFIX_TURNS)
    parser.add_argument("--max-turns", type=int, default=ELIGIBLE_MAX_TURNS)
    parser.add_argument("--content-variant", choices=("paired_low",), default=None)
    parser.add_argument("--out", default=None)
    args = parser.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)
    target = Path(args.out) if args.out else (
        OUT / f"probe_own_experiment_{args.model}_seed{args.seed_offset}.json"
    )

    prefix = run_prefix(
        args.model,
        args.seed_offset,
        checkpoint="eligible",
        max_prefix_turns=args.max_prefix_turns,
        content_variant=args.content_variant,
        protocol_variant="own_experiment",
        system_prompt=NEUTRAL_SYSTEM,
        feedback_builder=neutral_feedback,
    )
    if not prefix["eligibility"]["eligible"]:
        payload = {
            "kind": "exploratory_own_experiment_action_fork",
            "model": args.model,
            "seed_offset": args.seed_offset,
            "content_variant": args.content_variant,
            "prefix": {key: value for key, value in prefix.items() if key != "messages"},
            "selection": None,
            "branches": {},
            "gates": {"eligible_prefix": False},
            "all": False,
        }
        target.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
        print(json.dumps({"out": str(target), "gates": payload["gates"]}, indent=2))
        return

    selection = choose_common_action(
        prefix, args.model, args.seed_offset, args.content_variant, args.max_turns
    )
    if selection["abort"] != "action_selected":
        payload = {
            "kind": "exploratory_own_experiment_action_fork",
            "model": args.model,
            "seed_offset": args.seed_offset,
            "content_variant": args.content_variant,
            "prefix": {key: value for key, value in prefix.items() if key != "messages"},
            "selection": {key: value for key, value in selection.items()
                          if key != "messages_through_action"},
            "branches": {},
            "gates": {"eligible_prefix": True, "action_selected": False},
            "all": False,
        }
        target.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
        print(json.dumps({"out": str(target), "gates": payload["gates"]}, indent=2))
        return

    branches = {
        "limited": replay_common_and_continue(
            LIMITED, prefix, selection, args.model, args.seed_offset,
            args.content_variant, args.max_turns,
        ),
        "transfer": replay_common_and_continue(
            TRANSFER, prefix, selection, args.model, args.seed_offset,
            args.content_variant, args.max_turns,
        ),
    }
    for name, case_dir in (("limited", LIMITED), ("transfer", TRANSFER)):
        scorer = CheckpointScorer(case_dir)
        reference_code, diagnostics = build_reference_from_ledger(
            branches[name]["evidence_ledger"],
            prior_code=prefix["trace"][-1]["working_model"]["code"],
        )
        scores, fractions = score_checkpoints(
            prefix, branches[name], scorer, reference_code
        )
        branches[name]["reference"] = {
            "code": reference_code,
            "diagnostics": diagnostics,
            "captured_fraction_diagnostic": fractions,
        }
        branches[name]["checkpoint_scores"] = scores
        branches[name]["checkpoint_codes_present"] = {
            key: value is not None
            for key, value in _checkpoint_codes(prefix, branches[name]).items()
        }

    gates = {
        "eligible_prefix": True,
        "action_selected": True,
        "same_selected_cell_by_construction": True,
        "selected_cell_reached_experiment_both": all(
            any(event["verb"] == "experiment" for event in branch["trace"][0]["trajectory"])
            for branch in branches.values()
        ),
        "same_experiment_request_both": (
            [event["args"] for event in branches["limited"]["trace"][0]["trajectory"]
             if event["verb"] == "experiment"]
            == [event["args"] for event in branches["transfer"]["trace"][0]["trajectory"]
                if event["verb"] == "experiment"]
            and any(event["verb"] == "experiment"
                    for event in branches["limited"]["trace"][0]["trajectory"])
        ),
        "event_delivered_no_data": all(
            not any(row.get("kind") == "event_report"
                    for row in branch["evidence_ledger"])
            for branch in branches.values()
        ),
        "replay_exact_both": all(branch["replay_exact"] for branch in branches.values()),
        "accepted_both": all(branch["accepted"] for branch in branches.values()),
    }
    payload = {
        "kind": "exploratory_own_experiment_action_fork",
        "model": args.model,
        "seed_offset": args.seed_offset,
        "content_variant": args.content_variant,
        "prefix": {key: value for key, value in prefix.items() if key != "messages"},
        "selection": {key: value for key, value in selection.items()
                      if key != "messages_through_action"},
        "branches": branches,
        "gates": gates,
        "all": all(gates.values()),
    }
    target.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "out": str(target),
        "gates": gates,
        "action_kind": selection["action"]["kind"],
        "action_cell": selection["action"]["cell"],
        "R": {name: branch["R"] for name, branch in branches.items()},
    }, indent=2))


if __name__ == "__main__":
    main()
