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
from types import SimpleNamespace

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from wager.agent.cells import extract_cell  # noqa: E402
from wager.agent.llm_client import FoundryChat  # noqa: E402
from wager.factory.overgen_stream_tools import build_reference_from_ledger  # noqa: E402
from wager.harness.case_episode import build_world_server  # noqa: E402
from wager.harness.episode import (CELL_TIMEOUT_S, MAX_COMPLETION_TOKENS,  # noqa: E402
                                   SYSTEM)
from wager.harness.kernel_proc import KernelClient  # noqa: E402
from wager.report.checkpoint_score import (  # noqa: E402
    CheckpointScorer,
    captured_reference_fraction,
)
from wager.report.overgen_belief import shared_transfer_phenotype  # noqa: E402

LIMITED = ROOT / "cases" / "overgen_stream_v0"
TRANSFER = ROOT / "cases" / "overgen_stream_twin_v0"
OUT = ROOT / "scripts" / "out" / "overgen_stream_fork"
FIXED_PREFIX_TURNS = 4
FIXED_MAX_TURNS = 18
ELIGIBLE_MAX_PREFIX_TURNS = 12
ELIGIBLE_MAX_TURNS = 25


def _paired_low_grid_sample(base_sample):
    """Same 96-row report, with low-range anchors shared across all lines."""
    def sample(regime, n, seed):
        if "__qualification" not in regime.config:
            return base_sample(regime, n, seed)
        if n > 96:
            raise ValueError("paired-low exploratory report contains at most 96 rows")
        rng = np.random.default_rng(seed)
        anchors = (0.5, 1.5, 2.5, 3.5)
        designs = [(1, float(d)) for d in rng.uniform(0.0, 10.0, 32)]
        designs.extend((1, d) for d in anchors for _ in range(4))
        for line in (2, 3, 4, 5):
            designs.extend((line, d) for d in anchors for _ in range(3))
        order = rng.permutation(len(designs))
        rows = []
        for j, index in enumerate(order):
            line, driver = designs[int(index)]
            row = base_sample(
                SimpleNamespace(
                    config={"line": line, "driver": driver},
                    context={}, horizon=None,
                ),
                1,
                int(seed + 10_000 + j),
            ).iloc[0]
            rows.append({
                "line": float(line),
                "driver": float(driver),
                "outcome": float(row["outcome"]),
            })
        return pd.DataFrame(rows[:n])
    return sample


def _apply_content_variant(server, variant):
    if variant == "paired_low":
        server.world_sample = _paired_low_grid_sample(server.world_sample)
    return server


def _mixed_commissioning_sample(base_sample):
    """Preserve the 64 diagnostic rows and hide them among 192 routine rows."""
    def sample(regime, n, seed):
        if "__commissioning" not in regime.config or n != 256:
            return base_sample(regime, n, seed)
        diagnostic = base_sample(regime, 64, seed).copy()
        diagnostic["__diagnostic"] = 1.0
        rng = np.random.default_rng(seed + 31_337)
        designs = [(1, float(d)) for d in rng.uniform(0.0, 10.0, 64)]
        anchors = (0.5, 1.5, 2.5, 3.5)
        for line in (2, 3, 4, 5):
            designs.extend((line, d) for d in anchors for _ in range(8))
        filler = []
        for j, (line, driver) in enumerate(designs):
            row = base_sample(
                SimpleNamespace(
                    config={"line": line, "driver": driver},
                    context={}, horizon=None,
                ),
                1,
                int(seed + 40_000 + j),
            ).iloc[0]
            filler.append({
                "line": float(line),
                "driver": float(driver),
                "outcome": float(row["outcome"]),
                "__diagnostic": 0.0,
            })
        combined = pd.concat([diagnostic, pd.DataFrame(filler)], ignore_index=True)
        return combined.iloc[rng.permutation(len(combined))].reset_index(drop=True)
    return sample


def _apply_report_variant(server, variant):
    if variant != "mixed":
        return server
    event = server.config.events[0]
    source = event.source.model_copy(
        update={"max_rows": 256, "hidden_columns": ("__diagnostic",)}
    )
    mixed_event = event.model_copy(update={"source": source, "auto_deliver_n": 256})
    server.config = server.config.model_copy(update={"events": [mixed_event]})
    server.world_sample = _mixed_commissioning_sample(server.world_sample)
    return server


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


def run_prefix(model, seed_offset, checkpoint="fixed", max_prefix_turns=ELIGIBLE_MAX_PREFIX_TURNS,
               content_variant=None):
    server = _apply_content_variant(
        build_world_server(LIMITED, seed_offset=seed_offset), content_variant
    )
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
                eligibility = {
                    "eligible": False,
                    "turn": None,
                    "gates": {},
                    "reason": "submitted_before_checkpoint",
                    "failed_turn": turn,
                }
                break
            if (
                not result.ok
                and result.error
                and result.error.startswith("cell exceeded ")
            ):
                eligibility = {
                    "eligible": False,
                    "turn": None,
                    "gates": {},
                    "reason": "cell_timeout",
                    "failed_turn": turn,
                }
                break
            prompt = _feedback(result, server)
            if checkpoint in ("eligible", "formed"):
                observed = sum(
                    int(event.args.get("n", 0))
                    for event in server.trajectory
                    if event.verb == "observe"
                    and event.args.get("source") == "qualification_report"
                )
                code = result.working_model
                gates = {
                    "qualification_complete": observed >= 96,
                    "cell_ok": bool(result.ok),
                    "artifact_present": code is not None,
                    "artifact_scoreable": (
                        code is not None and server.validate_model(code) is None
                    ),
                }
                if checkpoint == "eligible":
                    gates["quiet_turn"] = not any(
                        event.verb in ("observe", "experiment", "event") for event in new_events
                    )
                    gates["artifact_changed_this_turn"] = (
                        code is not None and code != previous_code
                    )
                phenotype = None
                if checkpoint == "eligible" and all(gates.values()):
                    phenotype = shared_transfer_phenotype(code)
                    gates["target_shared_transfer_belief"] = phenotype["eligible"]
                if all(gates.values()):
                    eligibility = {
                        "eligible": True,
                        "turn": turn,
                        "gates": gates,
                        "phenotype": phenotype,
                    }
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
        "evidence_ledger": server.export_evidence_ledger(),
        "messages": copy.deepcopy(chat.messages),
        "next_prompt": prompt,
        "tokens": chat.usage.total_tokens,
        "checkpoint": checkpoint,
        "eligibility": eligibility,
    }


def replay_and_continue(case_dir, prefix, model, seed_offset, checkpoint="fixed",
                        max_turns=FIXED_MAX_TURNS, content_variant=None,
                        report_variant=None):
    server = _apply_report_variant(_apply_content_variant(
        build_world_server(case_dir, seed_offset=seed_offset), content_variant
    ), report_variant)
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
            if checkpoint in ("eligible", "formed") and turn == first_branch_turn:
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
        "evidence_ledger": server.export_evidence_ledger(),
        "tokens_continuation": chat.usage.total_tokens,
    }


def _checkpoint_codes(prefix, branch):
    pre = prefix["trace"][-1]["working_model"]["code"]
    first_seen = next(
        (row["working_model"]["code"] for row in branch["trace"]
         if row["working_model"]["code"] is not None),
        None,
    )
    first_changed = next(
        (row["working_model"]["code"] for row in branch["trace"]
         if row["working_model"]["code"] is not None
         and row["working_model"]["code"] != pre),
        None,
    )
    return {
        "M_pre": pre,
        "M_post_first_seen": first_seen,
        "M_post_first_changed": first_changed,
        "M_final": branch["submission_code"],
    }


def score_checkpoints(prefix, branch, scorer, reference_code):
    codes = _checkpoint_codes(prefix, branch)
    codes["M_reference"] = reference_code
    scores = scorer.score_many(codes)
    fractions = {
        name: captured_reference_fraction(
            scores["M_pre"], scores[name], scores["M_reference"]
        )
        for name in ("M_post_first_changed", "M_final")
    }
    return scores, fractions


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", default="DeepSeek-V3.2")
    parser.add_argument("--seed-offset", type=int, default=91000)
    parser.add_argument(
        "--checkpoint", choices=("fixed", "eligible", "formed"), default="fixed"
    )
    parser.add_argument("--max-prefix-turns", type=int, default=ELIGIBLE_MAX_PREFIX_TURNS)
    parser.add_argument("--max-turns", type=int, default=None)
    parser.add_argument("--content-variant", choices=("paired_low",), default=None)
    parser.add_argument("--include-mixed-arms", action="store_true")
    parser.add_argument("--out", default=None)
    args = parser.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)
    tag = "" if args.checkpoint == "fixed" else f"_{args.checkpoint}"
    target = (Path(args.out) if args.out else
              OUT / f"technical_{args.model}_seed{args.seed_offset}{tag}.json")

    max_turns = args.max_turns or (
        FIXED_MAX_TURNS if args.checkpoint == "fixed" else ELIGIBLE_MAX_TURNS
    )
    prefix = run_prefix(
        args.model,
        args.seed_offset,
        args.checkpoint,
        args.max_prefix_turns,
        args.content_variant,
    )
    if not prefix["eligibility"]["eligible"]:
        payload = {
            "kind": "technical_live_history_fork_not_behavioral_evidence",
            "model": args.model,
            "seed_offset": args.seed_offset,
            "checkpoint": args.checkpoint,
            "content_variant": args.content_variant,
            "include_mixed_arms": args.include_mixed_arms,
            "prefix": {k: v for k, v in prefix.items() if k != "messages"},
            "branches": {},
            "gates": {"eligible_prefix": False},
            "all": False,
        }
        target.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
        print(json.dumps({"out": str(target), "gates": payload["gates"], "all": False}, indent=2))
        return
    branch_specs = {
        "limited": (LIMITED, None),
        "transfer": (TRANSFER, None),
    }
    if args.include_mixed_arms:
        branch_specs.update({
            "limited_mixed": (LIMITED, "mixed"),
            "transfer_mixed": (TRANSFER, "mixed"),
        })
    branches = {
        name: replay_and_continue(
            case_dir, prefix, args.model, args.seed_offset, args.checkpoint, max_turns,
            args.content_variant, report_variant,
        )
        for name, (case_dir, report_variant) in branch_specs.items()
    }
    for name, (case_dir, _) in branch_specs.items():
        scorer = CheckpointScorer(case_dir)
        reference_code, reference_diagnostics = build_reference_from_ledger(
            branches[name]["evidence_ledger"],
            prior_code=prefix["trace"][-1]["working_model"]["code"],
        )
        scores, fractions = score_checkpoints(
            prefix, branches[name], scorer, reference_code
        )
        branches[name]["reference"] = {
            "code": reference_code,
            "diagnostics": reference_diagnostics,
            "captured_fraction_diagnostic": fractions,
        }
        branches[name]["checkpoint_scores"] = scores

    gates = {
        "M_pre_string": prefix["trace"][-1]["working_model"]["code"] is not None,
        "replay_exact_both": all(branch["replay_exact"] for branch in branches.values()),
        "one_report_each": all(branch["report_count"] == 1 for branch in branches.values()),
        "accepted_both": all(branch["accepted"] for branch in branches.values()),
        "prefix_evidence_replay_exact_both": all(
            branch["evidence_ledger"][:len(prefix["evidence_ledger"])]
            == prefix["evidence_ledger"]
            for branch in branches.values()
        ),
    }
    payload = {
        "kind": "technical_live_history_fork_not_behavioral_evidence",
        "model": args.model,
        "seed_offset": args.seed_offset,
        "checkpoint": args.checkpoint,
        "content_variant": args.content_variant,
        "include_mixed_arms": args.include_mixed_arms,
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
