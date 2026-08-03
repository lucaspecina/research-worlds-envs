"""Real-agent discovery probe for experimental coverage beyond observed support."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from wager.agent.cells import extract_cell  # noqa: E402
from wager.agent.llm_client import FoundryChat  # noqa: E402
from wager.contracts.episode import EpisodeEvent, SourceConfig  # noqa: E402
from wager.harness.case_episode import build_world_server  # noqa: E402
from wager.harness.episode import (  # noqa: E402
    MAX_COMPLETION_TOKENS,
    SYSTEM,
    run_episode,
)
from wager.harness.kernel_proc import KernelClient  # noqa: E402


CASE = ROOT / "cases" / "logistic_yield_v0"
OUT = ROOT / "scripts" / "out" / "logistic_coverage_neutral_v1_costs_visible"
PROBE_BUDGET = 4000.0
REQUIRED_HORIZON = 16.0
MIN_FEED_SPAN = 5.0
CONTROL_PREFIX_TURNS = 6
CONTROL_GRID = (0.0, 2.0, 4.0, 6.0, 8.0, 12.0, 16.0, 20.0, 24.0)
CONTROL_NOTICE = (
    "The scheduled end-of-run qualification record at feed=10 is complete."
)

NEUTRAL_BRIEF = """# Batch-line trajectory study

You advise a batch line that must predict cumulative yield trajectories under feed
settings from 0 to 10. Historical campaign records contain readings at
`t = 0, 1, ..., 6`. Fresh experiments may use any feed setting and measurement
schedule you choose; cost depends on the number of readings and the final time.

The line prices a delivery commitment at `t=16` and also evaluates end-of-run
behavior on schedules extending through `t=24`. Return an executable
`model(regime, n, seed)` in LONG format with columns exactly `unit_id, t, y`, one
row for every unit and requested timestamp. Observed readings include meter error;
the deliverable should model the underlying process.

Available operations and their exact costs are in `env.describe()`. Decide what
evidence is worth buying under the shared budget and submit your best model.
"""


def _experiment_designs(result: dict) -> list[dict]:
    designs: list[dict] = []
    for row in result.get("trace", []):
        for event in row.get("verbs", []):
            if event.get("verb") != "experiment":
                continue
            args = event.get("args", {})
            grid = args.get("context", {}).get("t_grid") or []
            designs.append({
                "feed": float(args.get("config", {}).get("feed", 4.0)),
                "n": int(args.get("n", 0)),
                "horizon": max(float(value) for value in grid) if grid else None,
                "n_times": len(grid),
                "cost": float(event.get("cost", 0.0)),
            })
    return designs


def _initial_prompt(server) -> str:
    sheet = server.describe()
    return (
        "Here is the brief:\n\n" + sheet["brief"]
        + "\n\nMachine-readable sheet:\n"
        + json.dumps({key: value for key, value in sheet.items() if key != "brief"}, indent=2)
        + "\n\nReason briefly about your opening plan, then write your first cell. "
        "`env` is already in the namespace."
    )


def _feedback(result, server) -> str:
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


def _verbs(server, start: int) -> list[dict]:
    return [
        {
            "verb": event.verb,
            "args": event.args,
            "cost": event.cost,
            "budget_remaining": event.budget_remaining,
            "note": event.note,
        }
        for event in server.trajectory[start:]
    ]


def _json_equal(left, right) -> bool:
    """Protocol equality after JSON's tuple-to-list normalization."""
    return json.loads(json.dumps(left)) == json.loads(json.dumps(right))


def _configure_server(seed_offset: int, *, with_control_event: bool):
    server = build_world_server(CASE, seed_offset=seed_offset)
    server.brief = NEUTRAL_BRIEF
    updates: dict = {"budget": PROBE_BUDGET}
    if with_control_event:
        meter = server.config.observe_sources["registros_campanas"].channel
        report_source = SourceConfig(
            cost_per_row=0.0,
            config={"feed": 10.0},
            context={"t_grid": CONTROL_GRID},
            channel=meter,
            max_rows=24,
        )
        updates["events"] = [
            EpisodeEvent(
                trigger_turn=CONTROL_PREFIX_TURNS + 1,
                trigger_spend_frac=1.0,
                notice=CONTROL_NOTICE,
                source_name="scheduled_end_run_qualification",
                source=report_source,
                auto_deliver_n=24,
                delivery_variable="scheduled_end_run_record",
            )
        ]
    server.config = server.config.model_copy(update=updates)
    return server


def run(model: str, seed_offset: int, max_turns: int) -> dict:
    server = _configure_server(seed_offset, with_control_event=False)
    disclosed_cost = server.describe()["experiment_cost"]
    if disclosed_cost.get("cost_per_horizon") != server.config.experiment.cost_per_horizon:
        raise RuntimeError("cost_per_horizon is not disclosed exactly; probe is invalid")
    result = run_episode(
        server,
        model=model,
        max_turns=max_turns,
        cell_timeout_s=180.0,
        capture_working_model=True,
    )
    designs = _experiment_designs(result)
    horizons = [d["horizon"] for d in designs if d["horizon"] is not None]
    feeds = [d["feed"] for d in designs]
    feed_span = max(feeds) - min(feeds) if feeds else 0.0
    covered_deadline = bool(horizons and max(horizons) >= REQUIRED_HORIZON)
    covered_feed_range = feed_span >= MIN_FEED_SPAN
    result["probe"] = {
        "kind": "logistic_coverage_neutral_v1_costs_visible",
        "claim_scope": "coverage acquisition discovery; not prevalence",
        "brief": NEUTRAL_BRIEF,
        "budget": PROBE_BUDGET,
        "seed_offset": seed_offset,
        "experiment_cost_disclosed": disclosed_cost,
        "experiment_designs": designs,
        "experiment_horizons": horizons,
        "max_experiment_horizon": max(horizons) if horizons else None,
        "covered_deadline": covered_deadline,
        "feed_span": feed_span,
        "covered_feed_range": covered_feed_range,
        "joint_portfolio_gate": covered_deadline and covered_feed_range,
        "seed_burned": True,
    }
    OUT.mkdir(parents=True, exist_ok=True)
    target = OUT / f"raw_{model.replace('/', '_')}_seed{seed_offset}.json"
    result["probe"]["raw_path"] = str(target)
    temporary = target.with_suffix(".json.tmp")
    temporary.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    temporary.replace(target)
    return result


def run_served_long_control(
    source_path: Path,
    max_turns: int,
    *,
    frozen_control_path: Path | None = None,
) -> dict:
    frozen_control = None
    if frozen_control_path is not None:
        frozen_control = json.loads(frozen_control_path.read_text(encoding="utf-8"))
        source_path = Path(frozen_control["source_raw"])
    source = json.loads(source_path.read_text(encoding="utf-8"))
    seed_offset = int(
        source.get("probe", {}).get(
            "seed_offset", source_path.stem.rsplit("seed", 1)[1]
        )
    )
    model = source["model"]
    prefix_rows = source["trace"][:CONTROL_PREFIX_TURNS]
    server = _configure_server(seed_offset, with_control_event=True)
    replay_checks = []
    branch_replay_checks = []
    branch_trace = []
    chat = FoundryChat(
        system=SYSTEM,
        model=model,
        max_completion_tokens=MAX_COMPLETION_TOKENS,
    )
    pending_prompt = _initial_prompt(server)

    with KernelClient(server, cell_timeout_s=180.0) as kernel:
        for expected in prefix_rows:
            notices = server.begin_turn(expected["turn"])
            deliveries = server.pop_deliveries()
            for variable, frame in deliveries:
                kernel.inject_dataframe(variable, frame)
            chat.messages.append({"role": "user", "content": pending_prompt})
            chat.messages.append({"role": "assistant", "content": expected["reply_text"]})
            start = len(server.trajectory)
            result = kernel.run_cell(expected["cell"])
            actual_verbs = _verbs(server, start)
            replay_checks.append({
                "turn": expected["turn"],
                "notices": notices == [],
                "deliveries": len(deliveries) == 0,
                "stdout": result.stdout == expected["cell_result"]["stdout"],
                "error": result.error == expected["cell_result"]["error"],
                "verbs": _json_equal(actual_verbs, expected["verbs"]),
                "budget": server.budget_remaining == expected["budget_remaining"],
                "working_model": result.working_model
                == (expected.get("working_model") or {}).get("code"),
            })
            pending_prompt = _feedback(result, server)

        frozen_rows = (frozen_control or {}).get("trace", [])
        for expected in frozen_rows:
            turn = int(expected["turn"])
            notices = server.begin_turn(turn)
            deliveries = server.pop_deliveries()
            delivered = []
            for variable, frame in deliveries:
                kernel.inject_dataframe(variable, frame)
                delivered.append({"variable": variable, "rows": len(frame)})
            prompt = pending_prompt
            if notices:
                prompt = "\n".join(f"[NOTICE] {notice}" for notice in notices) + "\n\n" + prompt
            chat.messages.append({"role": "user", "content": prompt})
            chat.messages.append({"role": "assistant", "content": expected["reply_text"]})
            start = len(server.trajectory)
            result = kernel.run_cell(expected["cell"])
            actual_verbs = _verbs(server, start)
            branch_replay_checks.append({
                "turn": turn,
                "notices": notices == expected.get("notices", []),
                "deliveries": delivered == expected.get("deliveries", []),
                "stdout": result.stdout == expected["cell_result"].get("stdout"),
                "error": result.error == expected["cell_result"].get("error"),
                "verbs": _json_equal(actual_verbs, expected.get("verbs", [])),
                "budget": server.budget_remaining == expected.get("budget_remaining"),
                "working_model": result.working_model
                == expected["cell_result"].get("working_model"),
            })
            branch_trace.append({**expected, "frozen_replay": True})
            pending_prompt = _feedback(result, server)

        first_live_turn = (
            int(frozen_rows[-1]["turn"]) + 1
            if frozen_rows
            else CONTROL_PREFIX_TURNS + 1
        )
        for turn in range(first_live_turn, max_turns + 1):
            notices = server.begin_turn(turn)
            deliveries = server.pop_deliveries()
            delivered = []
            for variable, frame in deliveries:
                kernel.inject_dataframe(variable, frame)
                delivered.append({"variable": variable, "rows": len(frame)})
            prompt = pending_prompt
            if notices:
                prompt = "\n".join(f"[NOTICE] {notice}" for notice in notices) + "\n\n" + prompt
            reply = chat.ask(prompt)
            cell = extract_cell(reply.content)
            if cell is None:
                branch_trace.append({"turn": turn, "reply_text": reply.content, "error": "no_cell"})
                break
            start = len(server.trajectory)
            result = kernel.run_cell(cell)
            branch_trace.append({
                "turn": turn,
                "notices": notices,
                "deliveries": delivered,
                "reply_text": reply.content,
                "cell": cell,
                "cell_result": {
                    "ok": result.ok,
                    "stdout": result.stdout,
                    "error": result.error,
                    "working_model": result.working_model,
                },
                "verbs": _verbs(server, start),
                "budget_remaining": server.budget_remaining,
            })
            if server.terminal:
                break
            if result.error and result.error.startswith("cell exceeded "):
                break
            pending_prompt = _feedback(result, server)

    prefix_replay_exact = all(
        all(value for key, value in row.items() if key != "turn")
        for row in replay_checks
    )
    branch_replay_exact = all(
        all(value for key, value in row.items() if key != "turn")
        for row in branch_replay_checks
    )
    payload = {
        "kind": (
            "logistic_coverage_served_long_provenance_control_resumed_v1"
            if frozen_control is not None
            else "logistic_coverage_served_long_provenance_control_v1"
        ),
        "claim_scope": "same frozen six-turn prefix; capacity control, not prevalence",
        "source_raw": str(source_path),
        "frozen_control_raw": str(frozen_control_path) if frozen_control_path else None,
        "model": model,
        "seed_offset": seed_offset,
        "control_grid": CONTROL_GRID,
        "prefix_replay_checks": replay_checks,
        "prefix_replay_exact": prefix_replay_exact,
        "branch_replay_checks": branch_replay_checks,
        "branch_replay_exact": branch_replay_exact,
        "evidence_ledger": server.export_evidence_ledger(),
        "accepted": server.terminal,
        "R": (server.result or {}).get("R"),
        "R_unclipped": (server.result or {}).get("R_unclipped"),
        "submission_code": (server.result or {}).get("code"),
        "trace": branch_trace,
        "tokens": chat.usage.total_tokens,
    }
    OUT.mkdir(parents=True, exist_ok=True)
    resume_suffix = "_resumed" if frozen_control is not None else ""
    target = OUT / (
        f"control_served_long_provenance_{model.replace('/', '_')}_"
        f"seed{seed_offset}{resume_suffix}.json"
    )
    payload["raw_path"] = str(target)
    temporary = target.with_suffix(".json.tmp")
    temporary.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    temporary.replace(target)
    return payload


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--model", default="DeepSeek-V3.2")
    parser.add_argument("--seed-offset", type=int, default=99100)
    parser.add_argument("--max-turns", type=int, default=10)
    parser.add_argument(
        "--served-long-control",
        type=Path,
        help="raw discovery trace whose first six turns are replayed before a long report",
    )
    parser.add_argument(
        "--resume-served-control",
        type=Path,
        help="frozen served-long control whose trace is replayed before continuing",
    )
    args = parser.parse_args()
    if args.served_long_control is not None:
        result = run_served_long_control(args.served_long_control, args.max_turns)
        print(
            f"control replay={result['prefix_replay_exact']} accepted={result['accepted']} "
            f"R={result['R']}"
        )
        return 0 if result["accepted"] else 2
    if args.resume_served_control is not None:
        result = run_served_long_control(
            Path("unused"),
            args.max_turns,
            frozen_control_path=args.resume_served_control,
        )
        print(
            f"resumed prefix={result['prefix_replay_exact']} "
            f"branch={result['branch_replay_exact']} accepted={result['accepted']} "
            f"R={result['R']}"
        )
        return 0 if result["accepted"] else 2
    result = run(args.model, args.seed_offset, args.max_turns)
    probe = result["probe"]
    print(
        f"accepted={result['accepted']} abort={result['abort_reason']} R={result['R']} "
        f"horizons={probe['experiment_horizons']} covered_t16={probe['covered_deadline']}"
    )
    return 0 if result["accepted"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
