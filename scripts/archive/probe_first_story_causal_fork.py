"""Exploratory real-agent fork on the causal supplier-vs-hall twins.

One common agent forms an executable provisional model from byte-identical
observational data.  Its first experiment cell is sampled once, frozen before
execution, replayed into both hidden worlds, and the two continuations then
run independently.  This is a content smoke, not a behavioral estimate.
"""

from __future__ import annotations

import argparse
import copy
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
from wager.reward.episode_score import score_episode_submission  # noqa: E402
from wager.reward.sandbox import SandboxedSubmission, SandboxError  # noqa: E402

REVISE = ROOT / "cases" / "first_story_causal_revise_v0"
RETAIN = ROOT / "cases" / "first_story_causal_retain_v0"
OUT = ROOT / "scripts" / "out" / "first_story_causal_fork"

SYSTEM = """You are an investigator building a predictive model of an unknown process through a Python REPL, on a budget.

Your lab protocol keeps an executable provisional model in a string named `working_model` whenever you have a current predictive view. It must define model(regime, n, seed) under the deliverable contract. This is a silent notebook checkpoint: it gives no score or feedback, and you may replace it whenever your view changes.

Each reply has TWO parts, IN THIS ORDER:
1. REASONING (a few sentences): what the latest result means for the practical objective and the most useful next step.
2. Exactly ONE Python cell inside a ```python fence.

The kernel runs the cell and returns stdout. Variables persist. `env` provides describe, observe, experiment and submit as documented in the brief. Read costs and remaining budget from `env.describe()` rather than assuming public attributes. In submitted code, read `regime.config` directly; the sandbox forbids the builtin `getattr`. Decide what evidence to gather and when the model is sufficient."""


def initial_prompt(server):
    sheet = server.describe()
    return (
        "Here is the assignment:\n\n"
        + sheet["brief"]
        + "\n\nMachine-readable sheet:\n"
        + json.dumps({k: v for k, v in sheet.items() if k != "brief"}, indent=2)
        + "\n\nWrite your opening reasoning and first Python cell. `env` is already available."
    )


def feedback(result, server):
    prompt = (
        f"Kernel output (ok={result.ok}, budget remaining={server.budget_remaining:.0f}):\n"
        + (result.stdout or "(no stdout)")
    )
    if result.error:
        prompt += "\nTRACEBACK:\n" + result.error
    return prompt + (
        "\n\nContinue the investigation. Keep `working_model` current when your predictive "
        "view changes, and call env.submit(code) when the work is sufficient."
    )


def record(turn, reply_text, cell, result, server, notices, trajectory_start):
    return {
        "turn": turn,
        "notices": notices,
        "reply_text": reply_text,
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


def cell_kind(cell):
    if re.search(r"\benv\s*\.\s*experiment\s*\(", cell):
        return "experiment"
    if re.search(r"\benv\s*\.\s*submit\s*\(", cell):
        return "submit"
    return "local"


def run_common_prefix(model, seed_offset, max_prefix_turns):
    server = build_world_server(REVISE, seed_offset=seed_offset)
    trace = []
    chat = FoundryChat(
        system=SYSTEM,
        model=model,
        max_completion_tokens=MAX_COMPLETION_TOKENS,
    )
    prompt = initial_prompt(server)
    selection = None
    with KernelClient(server, cell_timeout_s=CELL_TIMEOUT_S) as kernel:
        for turn in range(1, max_prefix_turns + 1):
            notices = server.begin_turn(turn)
            for variable, frame in server.pop_deliveries():
                kernel.inject_dataframe(variable, frame)
            reply = chat.ask(prompt)
            cell = extract_cell(reply.content)
            if cell is None:
                return {"abort": "no_cell", "trace": trace}
            kind = cell_kind(cell)
            if kind == "submit":
                return {"abort": "submitted_before_experiment", "trace": trace}
            if kind == "experiment":
                # A cell may mention env.experiment syntactically but fail before
                # reaching it (the first real smoke did exactly this while reading
                # a nonexistent env attribute).  Execute once on this disposable
                # common server to verify that an experiment is actually reached.
                # If it is reached, discard the result and replay the frozen cell in
                # both hidden worlds; the agent never receives this preflight output.
                mpre = trace[-1]["working_model"]["code"] if trace else None
                prefix_ledger = server.export_evidence_ledger()
                start = len(server.trajectory)
                preflight = kernel.run_cell(cell)
                reached = any(
                    event.verb == "experiment"
                    for event in server.trajectory[start:]
                )
                if not reached:
                    trace.append(record(
                        turn, reply.content, cell, preflight, server, notices, start
                    ))
                    if (
                        not preflight.ok
                        and preflight.error
                        and preflight.error.startswith("cell exceeded ")
                    ):
                        return {"abort": "cell_timeout", "trace": trace}
                    prompt = feedback(preflight, server)
                    continue
                selection = {
                    "turn": turn,
                    "reply_text": reply.content,
                    "cell": cell,
                    "notices": notices,
                    "messages_through_action": copy.deepcopy(chat.messages),
                    "M_pre": mpre,
                    "preflight": {
                        "result_ok": preflight.ok,
                        "experiment_calls": sum(
                            event.verb == "experiment"
                            for event in server.trajectory[start:]
                        ),
                    },
                    "prefix_evidence_ledger": prefix_ledger,
                }
                break
            start = len(server.trajectory)
            result = kernel.run_cell(cell)
            trace.append(record(
                turn, reply.content, cell, result, server, notices, start
            ))
            if not result.ok and result.error and result.error.startswith("cell exceeded "):
                return {"abort": "cell_timeout", "trace": trace}
            prompt = feedback(result, server)

    if selection is None:
        return {"abort": "no_experiment_selected", "trace": trace}
    mpre = selection["M_pre"]
    return {
        "abort": "action_selected",
        "trace": trace,
        "selection": selection,
        "evidence_ledger": selection["prefix_evidence_ledger"],
        "M_pre_present": mpre is not None,
        "M_pre_valid": mpre is not None and server.validate_model(mpre) is None,
        "tokens": chat.usage.total_tokens,
    }


def replay_prefix(server, prefix, kernel):
    checks = []
    for donor in prefix["trace"]:
        notices = server.begin_turn(donor["turn"])
        for variable, frame in server.pop_deliveries():
            kernel.inject_dataframe(variable, frame)
        start = len(server.trajectory)
        result = kernel.run_cell(donor["cell"])
        checks.append({
            "turn": donor["turn"],
            "notices": notices == donor["notices"],
            "stdout": result.stdout == donor["cell_result"]["stdout"],
            "error": result.error == donor["cell_result"]["error"],
            "working_model": result.working_model == donor["working_model"]["code"],
            "trajectory": [
                {"verb": event.verb, "args": event.args, "cost": event.cost}
                for event in server.trajectory[start:]
            ] == [
                {"verb": event["verb"], "args": event["args"], "cost": event["cost"]}
                for event in donor["trajectory"]
            ],
        })
    return checks


def replay_and_continue(case_dir, prefix, model, seed_offset, max_turns):
    server = build_world_server(case_dir, seed_offset=seed_offset)
    branch_trace = []
    with KernelClient(server, cell_timeout_s=CELL_TIMEOUT_S) as kernel:
        replay_checks = replay_prefix(server, prefix, kernel)
        action = prefix["selection"]
        notices = server.begin_turn(action["turn"])
        for variable, frame in server.pop_deliveries():
            kernel.inject_dataframe(variable, frame)
        start = len(server.trajectory)
        result = kernel.run_cell(action["cell"])
        branch_trace.append(record(
            action["turn"], action["reply_text"], action["cell"], result,
            server, notices, start,
        ))

        chat = FoundryChat(
            system=SYSTEM,
            model=model,
            max_completion_tokens=MAX_COMPLETION_TOKENS,
        )
        chat.messages = copy.deepcopy(action["messages_through_action"])
        prompt = feedback(result, server)
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
            branch_trace.append(record(
                turn, reply.content, cell, result, server, notices, start
            ))
            if server.terminal:
                abort = "submitted"
                break
            if not result.ok and result.error and result.error.startswith("cell exceeded "):
                abort = "cell_timeout"
                break
            prompt = feedback(result, server)

    final = server.result or {}
    last_code = next(
        (
            row["working_model"]["code"]
            for row in reversed(branch_trace)
            if row["working_model"]["code"]
        ),
        prefix["selection"]["M_pre"],
    )
    first_changed = next(
        (
            row["working_model"]["code"]
            for row in branch_trace
            if row["working_model"]["code"]
            and row["working_model"]["code"] != prefix["selection"]["M_pre"]
        ),
        None,
    )
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
        "first_changed_model": first_changed,
        "last_working_model": last_code,
        "trace": branch_trace,
        "evidence_ledger": server.export_evidence_ledger(),
        "tokens_continuation": chat.usage.total_tokens,
    }


def global_score(case_dir, code):
    if not code:
        return {"scoreable": False, "error": "missing artifact"}
    server = build_world_server(case_dir)
    try:
        result = score_episode_submission(
            code=code,
            world_sample=server.world_sample,
            world_source=server.scoring.world_source,
            naive_code=server.scoring.naive_code,
            null_code=server.scoring.null_code,
            battery=server.scoring.battery,
            columns=server.columns,
            params=server.scoring.params,
            functionals=server.scoring.functionals,
            truth_code=server.scoring.truth_code,
            enrich_regime=server.scoring.enrich_regime,
            sample_transform=server.scoring.sample_transform,
        )
        return {"scoreable": True, **result}
    except Exception as exc:  # exploratory analyzer must preserve raw failure
        return {"scoreable": False, "error": repr(exc)}


def select_last_scoreable(case_dir, branch, mpre):
    """Return the latest runnable artifact without hiding later invalid edits."""
    candidates = []
    if branch.get("submission_code"):
        candidates.append(("accepted_submission", branch["submission_code"]))
    for row in reversed(branch["trace"]):
        code = row["working_model"]["code"]
        if code:
            candidates.append((f"working_model_turn_{row['turn']}", code))
    if mpre:
        candidates.append(("M_pre_fallback", mpre))

    seen = set()
    failures = []
    for source, code in candidates:
        if code in seen:
            continue
        seen.add(code)
        score = global_score(case_dir, code)
        if score.get("scoreable", False):
            return code, source, score, failures
        failures.append({"source": source, "error": score.get("error")})
    return None, None, {"scoreable": False, "error": "no scoreable artifact"}, failures


def causal_signature(code, columns):
    if not code:
        return {"scoreable": False, "error": "missing artifact"}
    regimes = {
        "grade_low": {"feedstock_grade": 2.0, "humidity": 5.0},
        "grade_high": {"feedstock_grade": 8.0, "humidity": 5.0},
        "humidity_low": {"feedstock_grade": 5.0, "humidity": 2.0},
        "humidity_high": {"feedstock_grade": 5.0, "humidity": 8.0},
    }
    try:
        means = {}
        with SandboxedSubmission(code, columns, timeout_s=15.0) as submission:
            for name, config in regimes.items():
                frame = submission.run(
                    Regime(config=config, context={}, horizon=None), 2000, 77123
                )
                means[name] = {
                    column: float(frame[column].mean()) for column in columns
                }
        return {
            "scoreable": True,
            "means": means,
            "delta_outcome_grade": (
                means["grade_high"]["outcome"] - means["grade_low"]["outcome"]
            ),
            "delta_outcome_humidity": (
                means["humidity_high"]["outcome"]
                - means["humidity_low"]["outcome"]
            ),
        }
    except (SandboxError, ValueError, KeyError) as exc:
        return {"scoreable": False, "error": repr(exc)}


def truth_signature(case_dir):
    server = build_world_server(case_dir)
    regimes = {
        "grade_low": {"feedstock_grade": 2.0, "humidity": 5.0},
        "grade_high": {"feedstock_grade": 8.0, "humidity": 5.0},
        "humidity_low": {"feedstock_grade": 5.0, "humidity": 2.0},
        "humidity_high": {"feedstock_grade": 5.0, "humidity": 8.0},
    }
    means = {}
    for name, config in regimes.items():
        frame = server.world_sample(
            SimpleNamespace(config=config, context={}, horizon=None), 20_000, 77123
        )
        means[name] = {
            column: float(frame[column].mean()) for column in server.columns
        }
    return {
        "means": means,
        "delta_outcome_grade": (
            means["grade_high"]["outcome"] - means["grade_low"]["outcome"]
        ),
        "delta_outcome_humidity": (
            means["humidity_high"]["outcome"]
            - means["humidity_low"]["outcome"]
        ),
    }


def experiment_requests(branch):
    return [
        event["args"]
        for event in branch["trace"][0]["trajectory"]
        if event["verb"] == "experiment"
    ]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", default="DeepSeek-V3.2")
    parser.add_argument("--seed-offset", type=int, default=94800)
    parser.add_argument("--max-prefix-turns", type=int, default=10)
    parser.add_argument("--max-turns", type=int, default=18)
    parser.add_argument("--out", type=Path, default=None)
    args = parser.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)
    target = args.out or OUT / f"probe_{args.model}_seed{args.seed_offset}.json"

    prefix = run_common_prefix(args.model, args.seed_offset, args.max_prefix_turns)
    if prefix["abort"] != "action_selected":
        payload = {
            "kind": "exploratory_first_story_causal_action_fork",
            "model": args.model,
            "seed_offset": args.seed_offset,
            "prefix": prefix,
            "branches": {},
            "gates": {"action_selected": False},
            "all": False,
        }
        target.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
        print(json.dumps({"out": str(target), "gates": payload["gates"]}, indent=2))
        return

    if not (prefix["M_pre_present"] and prefix["M_pre_valid"]):
        sanitized = copy.deepcopy(prefix)
        sanitized["selection"].pop("messages_through_action", None)
        gates = {
            "action_selected": True,
            "M_pre_present": prefix["M_pre_present"],
            "M_pre_valid": prefix["M_pre_valid"],
        }
        payload = {
            "kind": "exploratory_first_story_causal_action_fork",
            "model": args.model,
            "seed_offset": args.seed_offset,
            "prefix": sanitized,
            "branches": {},
            "gates": gates,
            "all": False,
        }
        target.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
        print(json.dumps({"out": str(target), "gates": gates}, indent=2))
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
    for name, case_dir in (("revise", REVISE), ("retain", RETAIN)):
        artifact, artifact_source, artifact_score, artifact_failures = select_last_scoreable(
            case_dir, branches[name], mpre
        )
        branches[name]["last_scoreable_model"] = artifact
        branches[name]["last_scoreable_source"] = artifact_source
        branches[name]["later_invalid_artifacts"] = artifact_failures
        branches[name]["scores"] = {
            "M_pre": global_score(case_dir, mpre),
            "M_first_changed": global_score(case_dir, branches[name]["first_changed_model"]),
            "M_last": artifact_score,
        }
        branches[name]["signatures"] = {
            "truth": truth_signature(case_dir),
            "M_pre": causal_signature(mpre, ["feedstock", "outcome"]),
            "M_first_changed": causal_signature(
                branches[name]["first_changed_model"], ["feedstock", "outcome"]
            ),
            "M_last": causal_signature(artifact, ["feedstock", "outcome"]),
        }

    revise_requests = experiment_requests(branches["revise"])
    retain_requests = experiment_requests(branches["retain"])
    action_frames = {
        name: [
            row for row in branch["evidence_ledger"]
            if row["kind"] == "experiment"
            and row["turn"] == prefix["selection"]["turn"]
        ]
        for name, branch in branches.items()
    }
    gates = {
        "M_pre_present": prefix["M_pre_present"],
        "M_pre_valid": prefix["M_pre_valid"],
        "replay_exact_both": all(branch["replay_exact"] for branch in branches.values()),
        "prefix_evidence_identical": (
            branches["revise"]["evidence_ledger"][: len(prefix["evidence_ledger"])]
            == branches["retain"]["evidence_ledger"][: len(prefix["evidence_ledger"])]
        ),
        "experiment_reached_both": bool(revise_requests and retain_requests),
        "same_experiment_requests": (
            bool(revise_requests) and revise_requests == retain_requests
        ),
        "action_results_differ": (
            action_frames["revise"] != action_frames["retain"]
        ),
        "last_artifact_scoreable_both": all(
            branch["scores"]["M_last"].get("scoreable", False)
            for branch in branches.values()
        ),
    }
    sanitized_prefix = copy.deepcopy(prefix)
    sanitized_prefix["selection"].pop("messages_through_action", None)
    payload = {
        "kind": "exploratory_first_story_causal_action_fork",
        "model": args.model,
        "seed_offset": args.seed_offset,
        "prefix": sanitized_prefix,
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
        "R": {
            name: branch["scores"]["M_last"].get("R")
            for name, branch in branches.items()
        },
        "signature": {
            name: branch["signatures"]["M_last"] for name, branch in branches.items()
        },
    }, indent=2))


if __name__ == "__main__":
    main()
