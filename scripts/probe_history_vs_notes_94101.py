"""One-donor exploratory comparison: full history + notes vs notes only.

This is intentionally specialized and disposable.  It reuses the real
DeepSeek 94101 donor instead of building a general memory framework before we
know whether state representation moves behavior at all.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from wager.agent.cells import extract_cell  # noqa: E402
from wager.agent.llm_client import FoundryChat  # noqa: E402
from wager.harness.case_episode import build_world_server  # noqa: E402
from wager.harness.episode import (  # noqa: E402
    CELL_TIMEOUT_S,
    MAX_COMPLETION_TOKENS,
    SYSTEM,
)
from wager.harness.kernel_proc import KernelClient  # noqa: E402
from wager.report.checkpoint_score import CheckpointScorer  # noqa: E402
from wager.report.overgen_belief import shared_transfer_phenotype  # noqa: E402

from scripts.fork_overgen_stream_v0 import (  # noqa: E402
    LIMITED,
    OUT,
    TRANSFER,
    _initial_prompt,
    _record,
)


DEFAULT_DONOR = OUT / "technical_DeepSeek-V3.2_seed94101_eligible.json"


def feedback_from_record(row):
    result = row["cell_result"]
    prompt = (
        f"Kernel output (ok={result['ok']}, budget remaining={row['budget_remaining']:.0f}):\n"
        + (result["stdout"] or "(no stdout)")
    )
    if result["error"]:
        prompt += "\nTRACEBACK:\n" + result["error"]
    return prompt + (
        "\n\nReason about what this result tells you (does it confirm or refute your current "
        "hypothesis? what does it imply for the next step?), then write your next cell "
        "(or build and env.submit(code) when your reasoning has converged)."
    )


def reconstruct_messages(prefix, seed_offset):
    server = build_world_server(LIMITED, seed_offset=seed_offset)
    messages = [
        {"role": "system", "content": SYSTEM},
        {"role": "user", "content": _initial_prompt(server)},
    ]
    for index, row in enumerate(prefix["trace"]):
        messages.append({"role": "assistant", "content": row["reply_text"]})
        if index < len(prefix["trace"]) - 1:
            messages.append({"role": "user", "content": feedback_from_record(row)})
    return messages


def own_notes(trace):
    parts = []
    for row in trace:
        reasoning = row["reply_text"].split("```python", 1)[0].strip()
        if len(reasoning) > 900:
            reasoning = reasoning[:900] + " ..."
        parts.append(f"NOTE t{row['turn']}: {reasoning}")
    return "\n\n".join(parts)


def mechanical_log(trace):
    entries = []
    for row in trace:
        actions = "; ".join(
            f"{event['verb']}({json.dumps(event['args'], sort_keys=True)[:100]})"
            for event in row["trajectory"]
        ) or "analysis only"
        stdout = (row["cell_result"]["stdout"] or "").replace("\n", " ")[:260]
        entries.append(f"t{row['turn']}: {actions}; output={stdout}")
    return "\n".join(entries)


def snapshot_prompt(server, prefix, notices, mpre):
    sheet = server.describe()
    return (
        "You are continuing the same rolling-forecast project. The following handoff was "
        "assembled before the current commissioning result.\n\n"
        f"BRIEF:\n{sheet['brief']}\n\n"
        f"CURRENT STATE: budget remaining={server.budget_remaining:.0f}.\n\n"
        f"MECHANICAL PROJECT LOG:\n{mechanical_log(prefix['trace'])}\n\n"
        "WORKING NOTES (verbatim excerpts from reasoning you produced during this project):\n"
        f"{own_notes(prefix['trace'])}\n\n"
        "CURRENT EXECUTABLE MODEL:\n"
        f"```python\n{mpre}\n```\n\n"
        f"ROUTINE UPDATE:\n{' '.join(notices)}\n"
        "The newly completed rows are loaded as DataFrame `commissioning_report`.\n\n"
        "Continue the investigation and hand back the best executable model. You may inspect "
        "the current workspace, use remaining budget, and call `env.submit(code)` when done. "
        "Print the returned `.accepted` and `.error` fields so delivery failures are visible. "
        "Write one ```python cell per turn."
    )


def replay_prefix(server, prefix, kernel):
    checks = []
    for donor in prefix["trace"]:
        notices = server.begin_turn(donor["turn"], fire_events=False)
        if notices or server.pop_deliveries():
            raise RuntimeError("event fired inside donor prefix")
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


def report_hash(frame):
    data = frame.to_csv(index=False, float_format="%.12g").encode("utf-8")
    return hashlib.sha256(data).hexdigest()


def continue_branch(
    case_dir, representation, prefix, full_messages, model, seed_offset, max_turns
):
    server = build_world_server(case_dir, seed_offset=seed_offset)
    mpre = prefix["trace"][-1]["working_model"]["code"]
    replay_checks = []
    persistent_kernel = None

    if representation == "history_plus_notes":
        persistent_kernel = KernelClient(server, cell_timeout_s=CELL_TIMEOUT_S)
        persistent_kernel.__enter__()
        replay_checks = replay_prefix(server, prefix, persistent_kernel)
    else:
        with KernelClient(server, cell_timeout_s=CELL_TIMEOUT_S) as replay_kernel:
            replay_checks = replay_prefix(server, prefix, replay_kernel)

    first_turn = prefix["trace"][-1]["turn"] + 1
    notices = server.begin_turn(first_turn, fire_events=False)
    notices.extend(server.fire_event(0, turn_idx=first_turn))
    deliveries = server.pop_deliveries()
    if len(deliveries) != 1 or deliveries[0][0] != "commissioning_report":
        raise RuntimeError("expected one routine commissioning report")
    report = deliveries[0][1]
    budget_at_fork = server.budget_remaining

    kernel_context = persistent_kernel or KernelClient(
        server, cell_timeout_s=CELL_TIMEOUT_S
    )
    if persistent_kernel is None:
        kernel_context.__enter__()
    kernel = kernel_context
    try:
        kernel.inject_dataframe("commissioning_report", report)
        if representation == "notes_only":
            restored = kernel.run_cell(f"working_model = {mpre!r}")
            if not restored.ok or restored.working_model != mpre:
                raise RuntimeError("failed to restore M_pre in notes-only workspace")

        chat = FoundryChat(
            system=SYSTEM,
            model=model,
            max_completion_tokens=MAX_COMPLETION_TOKENS,
        )
        if representation == "history_plus_notes":
            chat.messages = copy.deepcopy(full_messages)
        prompt = snapshot_prompt(server, prefix, notices, mpre)
        trace = []
        abort = "max_turns"
        for offset in range(max_turns):
            turn = first_turn + offset
            if offset:
                server.begin_turn(turn, fire_events=False)
            traj_before = len(server.trajectory)
            reply = chat.ask(prompt)
            cell = extract_cell(reply.content)
            if cell is None:
                abort = "no_cell"
                break
            result = kernel.run_cell(cell)
            trace.append(_record(
                turn, reply, cell, result, server, notices if offset == 0 else [], traj_before
            ))
            if server.terminal:
                abort = "submitted"
                break
            if not result.ok and result.error and result.error.startswith("cell exceeded "):
                abort = "cell_timeout"
                break
            prompt = (
                f"Kernel output (ok={result.ok}, budget remaining={server.budget_remaining:.0f}):\n"
                + (result.stdout or "(no stdout)")
            )
            if result.error:
                prompt += "\nTRACEBACK:\n" + result.error
            prompt += (
                "\n\nContinue with the most useful next cell. If you attempted delivery, inspect "
                "whether it was accepted before treating the project as complete."
            )
    finally:
        kernel_context.__exit__(None, None, None)

    final = server.result or {}
    scorer = CheckpointScorer(case_dir)
    scores = scorer.score_many({"M_pre": mpre, "M_final": final.get("code")})
    return {
        "case_id": case_dir.name,
        "representation": representation,
        "replay_checks": replay_checks,
        "replay_exact": all(
            all(value for key, value in row.items() if key != "turn")
            for row in replay_checks
        ),
        "report_hash": report_hash(report),
        "report_rows": len(report),
        "budget_at_fork": budget_at_fork,
        "abort": abort,
        "accepted": server.terminal,
        "R": final.get("R"),
        "submission_code": final.get("code"),
        "trace": trace,
        "checkpoint_scores": scores,
        "final_phenotype": shared_transfer_phenotype(final.get("code")),
        "tokens_continuation": chat.usage.total_tokens,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--donor", type=Path, default=DEFAULT_DONOR)
    parser.add_argument("--model", default="DeepSeek-V3.2")
    parser.add_argument("--seed-offset", type=int, default=94101)
    parser.add_argument("--max-turns", type=int, default=8)
    parser.add_argument("--out", type=Path, default=None)
    args = parser.parse_args()
    target = args.out or OUT / "probe_history_vs_notes_DeepSeek94101.json"
    raw = json.loads(args.donor.read_text(encoding="utf-8"))
    prefix = raw["prefix"]
    full_messages = reconstruct_messages(prefix, args.seed_offset)

    branches = {}
    for pole, case_dir in (("limited", LIMITED), ("transfer", TRANSFER)):
        for representation in ("history_plus_notes", "notes_only"):
            name = f"{pole}__{representation}"
            branches[name] = continue_branch(
                case_dir, representation, prefix, full_messages, args.model,
                args.seed_offset, args.max_turns,
            )

    gates = {
        "replay_exact_all": all(branch["replay_exact"] for branch in branches.values()),
        "same_report_within_limited": (
            branches["limited__history_plus_notes"]["report_hash"]
            == branches["limited__notes_only"]["report_hash"]
        ),
        "same_report_within_transfer": (
            branches["transfer__history_plus_notes"]["report_hash"]
            == branches["transfer__notes_only"]["report_hash"]
        ),
        "accepted_all": all(branch["accepted"] for branch in branches.values()),
    }
    payload = {
        "kind": "exploratory_history_plus_notes_vs_notes_only",
        "model": args.model,
        "seed_offset": args.seed_offset,
        "donor": str(args.donor),
        "branches": branches,
        "gates": gates,
        "all": all(gates.values()),
    }
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "out": str(target),
        "gates": gates,
        "R": {name: branch["R"] for name, branch in branches.items()},
        "abort": {name: branch["abort"] for name, branch in branches.items()},
    }, indent=2))


if __name__ == "__main__":
    main()
