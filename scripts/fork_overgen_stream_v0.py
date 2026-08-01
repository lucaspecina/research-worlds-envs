"""One preregistered technical live-history fork for ADR 0163.

Run one real prefix through turn 4, replay that exact kernel history into both
worlds, clone the full chat messages, and continue from the routine report.
This script is exploratory plumbing, not a behavioral experiment.
"""

from __future__ import annotations

import argparse
import copy
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from wager.agent.cells import extract_cell  # noqa: E402
from wager.agent.llm_client import FoundryChat  # noqa: E402
from wager.harness.case_episode import build_world_server  # noqa: E402
from wager.harness.episode import (CELL_TIMEOUT_S, MAX_COMPLETION_TOKENS,  # noqa: E402
                                   SYSTEM)
from wager.harness.kernel_proc import KernelClient  # noqa: E402
from wager.report.checkpoint_score import CheckpointScorer  # noqa: E402

LIMITED = ROOT / "cases" / "overgen_stream_v0"
TRANSFER = ROOT / "cases" / "overgen_stream_twin_v0"
OUT = ROOT / "scripts" / "out" / "overgen_stream_fork"
FIXED_PREFIX_TURNS = 4
FIXED_MAX_TURNS = 18
ELIGIBLE_MAX_PREFIX_TURNS = 12
ELIGIBLE_MAX_TURNS = 25


def _initial_prompt(server):
    sheet = server.describe()
    return (
        "Here is the brief:\n\n" + sheet["brief"]
        + "\n\nMachine-readable sheet:\n"
        + json.dumps({k: v for k, v in sheet.items() if k != "brief"}, indent=2)
        + "\n\nReason briefly about your opening plan, then write your first cell. "
          "`env` is already in the namespace."
    )


def _feedback(result, server):
    prompt = (
        f"Kernel output (ok={result.ok}, budget remaining={server.budget_remaining:.0f}):\n"
        + (result.stdout or "(no stdout)")
    )
    if result.error:
        prompt += "\nTRACEBACK:\n" + result.error
    return prompt + (
        "\n\nReason about what this result tells you (does it confirm or refute your current "
        "hypothesis? what does it imply for the next step?), then write your next cell "
        "(or build and env.submit(code) when your reasoning has converged)."
    )


def _record(turn, reply, cell, result, server, notices, trajectory_start=0):
    return {
        "turn": turn,
        "notices": notices,
        "reply_text": reply.content,
        "cell": cell,
        "cell_result": {
            "ok": result.ok,
            "stdout": result.stdout,
            "error": result.error,
            "truncated": result.truncated,
        },
        "working_model": {
            "status": result.working_model_status,
            "code": result.working_model,
        },
        "budget_remaining": server.budget_remaining,
        "trajectory": [
            {
                "verb": event.verb,
                "args": event.args,
                "cost": event.cost,
                "note": event.note,
            }
            for event in server.trajectory[trajectory_start:]
        ],
    }


def run_prefix(model, seed_offset, checkpoint="fixed", max_prefix_turns=ELIGIBLE_MAX_PREFIX_TURNS):
    server = build_world_server(LIMITED, seed_offset=seed_offset)
    chat = FoundryChat(system=SYSTEM, model=model,
                       max_completion_tokens=MAX_COMPLETION_TOKENS)
    prompt = _initial_prompt(server)
    trace = []
    eligibility = None
    previous_code = None
    limit = FIXED_PREFIX_TURNS if checkpoint == "fixed" else max_prefix_turns
    with KernelClient(server, cell_timeout_s=CELL_TIMEOUT_S) as kernel:
        for turn in range(1, limit + 1):
            notices = server.begin_turn(turn, fire_events=(checkpoint == "fixed"))
            for variable, report in server.pop_deliveries():
                kernel.inject_dataframe(variable, report)
            if notices:
                raise RuntimeError("the routine report fired inside the frozen prefix")
            traj_before = len(server.trajectory)
            reply = chat.ask(prompt)
            cell = extract_cell(reply.content)
            if cell is None:
                raise RuntimeError(f"donor produced no cell at turn {turn}")
            result = kernel.run_cell(cell)
            new_events = server.trajectory[traj_before:]
            trace.append(_record(turn, reply, cell, result, server, notices, traj_before))
            if server.terminal:
                raise RuntimeError("donor submitted before the scheduled report")
            prompt = _feedback(result, server)
            if checkpoint == "eligible":
                observed = sum(
                    int(event.args.get("n", 0))
                    for event in server.trajectory
                    if event.verb == "observe"
                    and event.args.get("source") == "qualification_report"
                )
                code = result.working_model
                gates = {
                    "qualification_complete": observed >= 96,
                    "quiet_turn": not any(
                        event.verb in ("observe", "experiment", "event") for event in new_events
                    ),
                    "cell_ok": bool(result.ok),
                    "artifact_present": code is not None,
                    "artifact_changed_this_turn": code is not None and code != previous_code,
                    "artifact_scoreable": (
                        code is not None and server.validate_model(code) is None
                    ),
                }
                if all(gates.values()):
                    eligibility = {"eligible": True, "turn": turn, "gates": gates}
                    break
                if code is not None:
                    previous_code = code
    if checkpoint == "fixed":
        eligibility = {"eligible": True, "turn": FIXED_PREFIX_TURNS,
                       "gates": {"fixed_timing": True}}
    elif eligibility is None:
        eligibility = {"eligible": False, "turn": None, "gates": {}}
    return {
        "trace": trace,
        "messages": copy.deepcopy(chat.messages),
        "next_prompt": prompt,
        "tokens": chat.usage.total_tokens,
        "checkpoint": checkpoint,
        "eligibility": eligibility,
    }


def replay_and_continue(case_dir, prefix, model, seed_offset, checkpoint="fixed",
                        max_turns=FIXED_MAX_TURNS):
    server = build_world_server(case_dir, seed_offset=seed_offset)
    replay_checks = []
    branch_trace = []
    with KernelClient(server, cell_timeout_s=CELL_TIMEOUT_S) as kernel:
        for donor in prefix["trace"]:
            notices = server.begin_turn(
                donor["turn"], fire_events=(checkpoint == "fixed")
            )
            if notices or server.pop_deliveries():
                raise RuntimeError("a report fired while replaying the common prefix")
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

        chat = FoundryChat(system=SYSTEM, model=model,
                           max_completion_tokens=MAX_COMPLETION_TOKENS)
        chat.messages = copy.deepcopy(prefix["messages"])
        prompt = prefix["next_prompt"]
        report_count = 0
        abort = "max_turns"
        first_branch_turn = prefix["trace"][-1]["turn"] + 1
        for turn in range(first_branch_turn, max_turns + 1):
            notices = server.begin_turn(turn, fire_events=(checkpoint == "fixed"))
            if checkpoint == "eligible" and turn == first_branch_turn:
                notices.extend(server.fire_event(0, turn_idx=turn))
            deliveries = server.pop_deliveries()
            report_count += len(deliveries)
            for variable, report in deliveries:
                kernel.inject_dataframe(variable, report)
            if notices:
                prompt = "\n".join(f"[NOTICE] {n}" for n in notices) + "\n\n" + prompt
            reply = chat.ask(prompt)
            cell = extract_cell(reply.content)
            if cell is None:
                abort = "no_cell"
                break
            result = kernel.run_cell(cell)
            branch_trace.append(_record(turn, reply, cell, result, server, notices))
            if server.terminal:
                abort = "submitted"
                break
            if not result.ok and result.error and result.error.startswith("cell exceeded "):
                abort = "cell_timeout"
                break
            prompt = _feedback(result, server)

    final = server.result or {}
    return {
        "case_id": case_dir.name,
        "replay_checks": replay_checks,
        "replay_exact": all(all(v for k, v in row.items() if k != "turn")
                            for row in replay_checks),
        "report_count": report_count,
        "abort": abort,
        "accepted": server.terminal,
        "R": final.get("R"),
        "submission_code": final.get("code"),
        "trace": branch_trace,
        "tokens_continuation": chat.usage.total_tokens,
    }


def _checkpoint_codes(prefix, branch):
    pre = prefix["trace"][-1]["working_model"]["code"]
    first_post = None
    for row in branch["trace"]:
        code = row["working_model"]["code"]
        if code is not None:
            first_post = code
            break
    return {"M_pre": pre, "M_post_first": first_post, "M_final": branch["submission_code"]}


def score_checkpoints(prefix, branch, scorer):
    return scorer.score_many(_checkpoint_codes(prefix, branch))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", default="DeepSeek-V3.2")
    parser.add_argument("--seed-offset", type=int, default=91000)
    parser.add_argument("--checkpoint", choices=("fixed", "eligible"), default="fixed")
    parser.add_argument("--max-prefix-turns", type=int, default=ELIGIBLE_MAX_PREFIX_TURNS)
    parser.add_argument("--max-turns", type=int, default=None)
    parser.add_argument("--out", default=None)
    args = parser.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)
    tag = "" if args.checkpoint == "fixed" else "_eligible"
    target = (Path(args.out) if args.out else
              OUT / f"technical_{args.model}_seed{args.seed_offset}{tag}.json")

    max_turns = args.max_turns or (
        FIXED_MAX_TURNS if args.checkpoint == "fixed" else ELIGIBLE_MAX_TURNS
    )
    prefix = run_prefix(args.model, args.seed_offset, args.checkpoint, args.max_prefix_turns)
    if not prefix["eligibility"]["eligible"]:
        payload = {
            "kind": "technical_live_history_fork_not_behavioral_evidence",
            "model": args.model,
            "seed_offset": args.seed_offset,
            "checkpoint": args.checkpoint,
            "prefix": {k: v for k, v in prefix.items() if k != "messages"},
            "branches": {},
            "gates": {"eligible_prefix": False},
            "all": False,
        }
        target.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
        print(json.dumps({"out": str(target), "gates": payload["gates"], "all": False}, indent=2))
        return
    branches = {
        "limited": replay_and_continue(
            LIMITED, prefix, args.model, args.seed_offset, args.checkpoint, max_turns
        ),
        "transfer": replay_and_continue(
            TRANSFER, prefix, args.model, args.seed_offset, args.checkpoint, max_turns
        ),
    }
    for name, case_dir in (("limited", LIMITED), ("transfer", TRANSFER)):
        scorer = CheckpointScorer(case_dir)
        branches[name]["checkpoint_scores"] = score_checkpoints(prefix, branches[name], scorer)

    gates = {
        "M_pre_string": prefix["trace"][-1]["working_model"]["code"] is not None,
        "replay_exact_both": all(branch["replay_exact"] for branch in branches.values()),
        "one_report_each": all(branch["report_count"] == 1 for branch in branches.values()),
        "accepted_both": all(branch["accepted"] for branch in branches.values()),
    }
    payload = {
        "kind": "technical_live_history_fork_not_behavioral_evidence",
        "model": args.model,
        "seed_offset": args.seed_offset,
        "checkpoint": args.checkpoint,
        "prefix": {k: v for k, v in prefix.items() if k != "messages"},
        "branches": branches,
        "gates": gates,
        "all": all(gates.values()),
    }
    target.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "out": str(target),
        "gates": gates,
        "all": payload["all"],
        "R": {name: branch["R"] for name, branch in branches.items()},
        "turns_post": {name: len(branch["trace"]) for name, branch in branches.items()},
    }, indent=2))


if __name__ == "__main__":
    main()
