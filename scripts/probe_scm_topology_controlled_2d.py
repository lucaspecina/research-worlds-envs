"""Paired LOCAL/LATENT control with a fixed orthogonal North audit.

This runner reuses the frozen gpt-5.4/98403 prefix and first North action.  It
then serves two routine pooled cells which add humidity support without naming
the structural hypothesis. Interface v1 also exposes the experimental
provenance columns which v0 accidentally hid. By default it performs only the
zero-LLM mechanical certificate; ``--run-agent`` is required to spend API
budget.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from wager.agent.cells import extract_cell  # noqa: E402
from wager.contracts import ExperimentDesign, SubmitResult  # noqa: E402
from wager.harness.case_episode import build_world_server  # noqa: E402
from wager.harness.episode import (  # noqa: E402
    CELL_TIMEOUT_S,
    MAX_COMPLETION_TOKENS,
)
from wager.harness.kernel_proc import KernelClient  # noqa: E402

from scripts import probe_first_story_scm_transfer_fork as transfer  # noqa: E402
from scripts import probe_scm_transfer_topology_v1 as topology  # noqa: E402
from scripts.analyze_scm_topology_recoverability import (  # noqa: E402
    recoverability_from_ledger,
)


MODEL = "gpt-5.4"
SEED_OFFSET = 98_403
SOURCE = (
    ROOT
    / "scripts"
    / "out"
    / "first_story_scm_transfer_topology_v1"
    / "probe_gpt-5.4_seed98403_resumed_preflight.json"
)
SOURCE_SHA256 = (
    "f049262592a770a21c6d8feea35505b1e38d5d347733d1b788d647302a269acc"
)
OUT = ROOT / "scripts" / "out" / "first_story_scm_topology_controlled_2d"

BRANCH_SPECS = (
    ("local", topology.LOCAL),
    ("latent", topology.LATENT),
)
ROUTINE_SPECS = (
    {
        "variable": "north_routine_humidity_low",
        "config": {"feedstock_grade": 5.0, "humidity": 2.5},
        "context": {"site": "north"},
        "n": 60,
    },
    {
        "variable": "north_routine_humidity_high",
        "config": {"feedstock_grade": 5.0, "humidity": 7.5},
        "context": {"site": "north"},
        "n": 60,
    },
)
ROUTINE_NOTICE = (
    "The scheduled North production check has completed. Two additional "
    "operating-point tables are already loaded as DataFrames "
    "`north_routine_humidity_low` and `north_routine_humidity_high`. No "
    "further trials are available in this control. Continue the assignment "
    "using the evidence in the live workspace."
)
PROHIBITED_NOTICE_CUES = (
    "mixture",
    "mixing",
    "batch_class",
    "a/b",
    "subpopulation",
    "anomal",
    "residual",
    "error",
)
INTERFACE_VERSIONS = ("v0", "v1")

FIRST_CELL_REVIEW_ERROR = (
    "final handoff is unavailable until this notebook step completes; "
    "continue in the next turn using the returned cell output"
)


class FirstCellSubmitGate:
    """Reject submissions in one cell, then restore the ordinary handoff.

    This is a runner-only procedural control. It does not inspect the submitted
    code or any world data and is inert after ``open_next_turn``.
    """

    def __init__(self, server) -> None:
        self.server = server
        self._ordinary_submit = server.submit
        self.locked = True
        self.rejected_attempts = 0
        server.submit = self.submit

    def submit(self, code: str) -> SubmitResult:
        if not self.locked:
            return self._ordinary_submit(code)
        self.server._guard_open()
        self.rejected_attempts += 1
        self.server._log(
            "submit",
            {"accepted": False},
            0.0,
            note=FIRST_CELL_REVIEW_ERROR,
        )
        return SubmitResult(accepted=False, error=FIRST_CELL_REVIEW_ERROR)

    def open_next_turn(self) -> None:
        self.locked = False


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _events(server, start: int) -> list[dict[str, Any]]:
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


def _routine_seed(server, seed_offset: int) -> int:
    """Mirror WorldServer._next_seed(800_000) before one experiment call."""
    return 800_000 + seed_offset * 100_000 + int(server._seq) + 1


def _freeze_further_experiments(server) -> None:
    previous_guard = server.experiment_guard

    def no_more_experiments(design, turn, fired_events):
        if previous_guard is not None:
            previous_guard(design, turn, fired_events)
        raise ValueError(
            "the scheduled production check is complete; no further trials "
            "are available in this control"
        )

    server.experiment_guard = no_more_experiments


def _agent_visible_routine_frame(frame, spec: dict, interface_version: str):
    """Add only the experiment provenance omitted by the v0 interface."""
    visible = frame.copy(deep=True)
    if interface_version == "v0":
        return visible
    if interface_version != "v1":
        raise ValueError(f"unknown interface version: {interface_version}")
    visible.insert(0, "humidity", float(spec["config"]["humidity"]))
    visible.insert(
        0, "feedstock_grade", float(spec["config"]["feedstock_grade"])
    )
    visible.insert(0, "site", str(spec["context"]["site"]))
    return visible


def _json_scalar(value):
    return value.item() if hasattr(value, "item") else value


def _frame_payload(frame) -> dict[str, Any]:
    return {
        "columns": list(frame.columns),
        "data": [
            [_json_scalar(value) for value in row]
            for row in frame.itertuples(index=False, name=None)
        ],
    }


def _first_post_routine_artifact(trace: list[dict[str, Any]]) -> str | None:
    if not trace:
        return None
    first = trace[0]
    return first.get("submission_code") or first.get("working_model", {}).get(
        "code"
    )


def _first_changed_artifact(
    trace: list[dict[str, Any]], mpre: str
) -> str | None:
    for row in trace:
        candidates = [
            row.get("working_model", {}).get("code"),
            row.get("submission_code"),
        ]
        for code in candidates:
            if code and code != mpre:
                return code
    return None


def replay_routine_and_optionally_continue(
    case_dir: Path,
    prefix: dict[str, Any],
    *,
    interface_version: str,
    run_agent: bool,
    max_post_routine_turns: int,
    require_post_output_review: bool = False,
) -> dict[str, Any]:
    """Replay the frozen action, inject the fixed audit, then optionally ask."""
    server = build_world_server(case_dir, seed_offset=SEED_OFFSET)
    action = prefix["selection"]
    source_requests = transfer._request_view(
        action["preflight_action_trajectory"]
    )
    continuation_trace: list[dict[str, Any]] = []
    chat = None

    with KernelClient(server, cell_timeout_s=CELL_TIMEOUT_S) as kernel:
        replay_checks = transfer.replay_prefix_exact(server, prefix, kernel)
        ledger_after_prefix = server.export_evidence_ledger()

        action_notices = server.begin_turn(action["turn"])
        for variable, frame in server.pop_deliveries():
            kernel.inject_dataframe(variable, frame)
        action_start = len(server.trajectory)
        action_result = kernel.run_cell(action["cell"])
        action_record = transfer.record(
            action["turn"],
            action["reply_text"],
            action["cell"],
            action_result,
            server,
            action_notices,
            action_start,
        )
        action_record["phase"] = "frozen_north_action"
        ledger_after_action = server.export_evidence_ledger()
        action_ledger = ledger_after_action[len(ledger_after_prefix) :]

        routine_turn = action["turn"] + 1
        routine_notices = server.begin_turn(routine_turn)
        for variable, frame in server.pop_deliveries():
            kernel.inject_dataframe(variable, frame)
        routine_ledger_start = len(ledger_after_action)
        routine_trajectory_start = len(server.trajectory)
        budget_before_routine = server.budget_remaining
        routine_seeds = []
        routine_agent_visible = []
        for spec in ROUTINE_SPECS:
            seed = _routine_seed(server, SEED_OFFSET)
            frame = server.experiment(
                ExperimentDesign(
                    config=spec["config"],
                    context=spec["context"],
                    n=spec["n"],
                    horizon=None,
                )
            )
            routine_seeds.append(seed)
            visible = _agent_visible_routine_frame(
                frame, spec, interface_version
            )
            kernel.inject_dataframe(spec["variable"], visible)
            routine_agent_visible.append(
                {
                    "variable": spec["variable"],
                    "request": {
                        "config": spec["config"],
                        "context": spec["context"],
                        "n": spec["n"],
                        "horizon": None,
                    },
                    "frame": _frame_payload(visible),
                }
            )
        budget_after_routine = server.budget_remaining
        routine_ledger = server.export_evidence_ledger()[
            routine_ledger_start:
        ]
        routine_events = _events(server, routine_trajectory_start)
        _freeze_further_experiments(server)
        submit_gate = (
            FirstCellSubmitGate(server)
            if require_post_output_review
            else None
        )

        abort = "mechanical_certificate_only"
        if run_agent:
            chat = transfer.FoundryChat(
                system=topology.SYSTEM,
                model=MODEL,
                max_completion_tokens=MAX_COMPLETION_TOKENS,
            )
            chat.messages = copy.deepcopy(action["messages_through_action"])
            prompt = transfer.feedback(action_result, server) + (
                "\n\n" + ROUTINE_NOTICE
            )
            abort = "submitted" if server.terminal else "max_turns"
            last_turn = routine_turn + max_post_routine_turns - 1
            for turn in range(routine_turn, last_turn + 1):
                if server.terminal:
                    break
                if turn == routine_turn:
                    notices = routine_notices
                else:
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
                row = transfer.record(
                    turn,
                    reply.content,
                    cell,
                    result,
                    server,
                    notices,
                    start,
                )
                row["phase"] = "post_controlled_2d_routine"
                row["submission_code"] = (
                    server.result.get("code")
                    if server.terminal and server.result
                    else None
                )
                row["terminal_after_cell"] = server.terminal
                if submit_gate is not None and not continuation_trace:
                    row["first_cell_submit_gate"] = {
                        "rejected_attempts": submit_gate.rejected_attempts,
                        "terminal_after_cell": server.terminal,
                    }
                    submit_gate.open_next_turn()
                continuation_trace.append(row)
                if server.terminal:
                    abort = "submitted"
                    break
                if result.error and result.error.startswith("cell exceeded "):
                    abort = "cell_timeout"
                    break
                prompt = transfer.feedback(result, server)

        transcript = copy.deepcopy(chat.messages) if chat is not None else []
        tokens = chat.usage.total_tokens if chat is not None else 0
        llm_turn_usage = (
            [
                {
                    "prompt_tokens": turn.prompt_tokens,
                    "completion_tokens": turn.completion_tokens,
                    "reasoning_tokens": turn.reasoning_tokens,
                    "latency_s": turn.latency_s,
                }
                for turn in chat.turns
            ]
            if chat is not None
            else []
        )

    final = server.result or {}
    mpre = action["M_pre"]
    last_working = next(
        (
            row["working_model"]["code"]
            for row in reversed(continuation_trace)
            if row["working_model"]["code"]
        ),
        action_result.working_model or mpre,
    )
    return {
        "case_id": case_dir.name,
        "replay_checks": replay_checks,
        "replay_exact": transfer._replay_checks_exact(replay_checks),
        "prefix_ledger_exact": ledger_after_prefix == prefix["evidence_ledger"],
        "action_cell_sha256": hashlib.sha256(
            action["cell"].encode("utf-8")
        ).hexdigest(),
        "action_notices_exact": action_notices == action["notices"],
        "action_requests": transfer._request_view(action_record["trajectory"]),
        "action_requests_match_source": (
            transfer._request_view(action_record["trajectory"])
            == source_requests
        ),
        "action_record": action_record,
        "action_ledger": action_ledger,
        "ledger_after_action": ledger_after_action,
        "terminal_after_action": bool(action_record["trajectory"])
        and server.terminal
        and not continuation_trace,
        "working_model_after_action": action_result.working_model,
        "routine_turn": routine_turn,
        "routine_notice": ROUTINE_NOTICE,
        "interface_version": interface_version,
        "routine_notices": routine_notices,
        "routine_specs": list(ROUTINE_SPECS),
        "routine_seeds": routine_seeds,
        "routine_events": routine_events,
        "routine_ledger": routine_ledger,
        "routine_agent_visible": routine_agent_visible,
        "budget_before_routine": budget_before_routine,
        "budget_after_routine": budget_after_routine,
        "further_experiments_blocked": True,
        "post_output_review_required": require_post_output_review,
        "review_gate_rejected_attempts": (
            submit_gate.rejected_attempts if submit_gate is not None else 0
        ),
        "review_gate_open_after_first_cell": (
            not submit_gate.locked if submit_gate is not None and continuation_trace
            else False
        ),
        "abort": abort,
        "accepted": server.terminal,
        "R": final.get("R"),
        "submission_code": final.get("code"),
        "first_post_routine_model": _first_post_routine_artifact(
            continuation_trace
        ),
        "first_changed_model": _first_changed_artifact(
            continuation_trace, mpre
        ),
        "last_working_model": last_working,
        "last_working_model_code": last_working,
        "trace": continuation_trace,
        "transcript": transcript,
        "evidence_ledger": server.export_evidence_ledger(),
        "tokens_continuation": tokens,
        "llm_turn_usage": llm_turn_usage,
    }


def _projection(ledger: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return topology._ledger_projection(ledger, ("feedstock", "outcome"))


def _payload_projection(
    tables: list[dict[str, Any]], columns: tuple[str, ...]
) -> list[dict[str, Any]]:
    result = []
    for table in tables:
        frame = table["frame"]
        names = frame["columns"]
        indexes = [names.index(column) for column in columns]
        result.append(
            {
                "variable": table["variable"],
                "columns": list(columns),
                "data": [
                    [row[index] for index in indexes]
                    for row in frame["data"]
                ],
            }
        )
    return result


def _visible_provenance_exact(branch: dict[str, Any]) -> bool:
    if branch.get("interface_version") != "v1":
        return False
    if len(branch["routine_agent_visible"]) != len(ROUTINE_SPECS):
        return False
    for table, spec in zip(
        branch["routine_agent_visible"], ROUTINE_SPECS, strict=True
    ):
        frame = table["frame"]
        columns = frame["columns"]
        if not {"site", "feedstock_grade", "humidity"}.issubset(columns):
            return False
        indexes = {
            column: columns.index(column)
            for column in ("site", "feedstock_grade", "humidity")
        }
        expected = {
            "site": spec["context"]["site"],
            "feedstock_grade": float(spec["config"]["feedstock_grade"]),
            "humidity": float(spec["config"]["humidity"]),
        }
        if any(
            row[indexes[column]] != value
            for row in frame["data"]
            for column, value in expected.items()
        ):
            return False
    return True


def build_mechanical_certificate(
    source: Path,
    prefix: dict[str, Any],
    provenance: dict[str, Any],
    *,
    interface_version: str,
) -> dict[str, Any]:
    source_payload = json.loads(source.read_text(encoding="utf-8"))
    physical = topology.physical_certificate(SEED_OFFSET, signature_n=20_000)
    branches = {
        name: replay_routine_and_optionally_continue(
            case_dir,
            prefix,
            interface_version=interface_version,
            run_agent=False,
            max_post_routine_turns=1,
        )
        for name, case_dir in BRANCH_SPECS
    }
    recoverability = {
        name: recoverability_from_ledger(
            branch["action_ledger"] + branch["routine_ledger"],
            target=name,
            folds=None,
            seed=SEED_OFFSET + 1_900_000 + index,
        )
        for index, (name, branch) in enumerate(branches.items())
    }
    local = branches["local"]
    latent = branches["latent"]
    expected_routine_requests = [
        {
            "config": spec["config"],
            "context": spec["context"],
            "n": spec["n"],
            "horizon": None,
        }
        for spec in ROUTINE_SPECS
    ]
    source_preflight = source_payload.get("frozen_action_preflight", {})
    notice_lower = ROUTINE_NOTICE.lower()
    ledger_columns = ("batch_class", "feedstock", "outcome")
    visible_nonlabel_columns = (
        "site",
        "feedstock_grade",
        "humidity",
        "feedstock",
        "outcome",
    )
    gates = {
        "source_sha256_exact": _sha256(source) == SOURCE_SHA256,
        "source_preflight_passed": source_payload.get("preflight_all") is True,
        "source_has_no_completed_branches": not source_payload.get("branches"),
        "prefix_reconstruction_exact": provenance.get("all") is True,
        "physical_topology_certificate_passed": physical.get("all") is True,
        "replay_exact_both": all(
            branch["replay_exact"] for branch in branches.values()
        ),
        "prefix_ledger_exact_both": all(
            branch["prefix_ledger_exact"] for branch in branches.values()
        ),
        "same_frozen_action_hash_both": all(
            branch["action_cell_sha256"]
            == prefix["selection"]["cell_sha256"]
            for branch in branches.values()
        ),
        "action_notices_exact_both": all(
            branch["action_notices_exact"] for branch in branches.values()
        ),
        "action_requests_match_source_both": all(
            branch["action_requests_match_source"]
            for branch in branches.values()
        ),
        "action_ledgers_match_source_preflight": all(
            branch["action_ledger"]
            == source_preflight[name]["action_ledger"]
            for name, branch in branches.items()
        ),
        "action_nonterminal_both": all(
            not source_preflight[name]["terminal_after_action"]
            for name, _ in BRANCH_SPECS
        ),
        "routine_has_no_event_notice": all(
            not branch["routine_notices"] for branch in branches.values()
        ),
        "routine_requests_exact_both": all(
            [row["request"] for row in branch["routine_ledger"]]
            == expected_routine_requests
            for branch in branches.values()
        ),
        "routine_server_seeds_exact_both": (
            bool(local["routine_seeds"])
            and local["routine_seeds"] == latent["routine_seeds"]
        ),
        "routine_projection_feedstock_outcome_exact": (
            _projection(local["routine_ledger"])
            == _projection(latent["routine_ledger"])
        ),
        "routine_class_counts_equal": (
            topology._ledger_class_counts(local["routine_ledger"])
            == topology._ledger_class_counts(latent["routine_ledger"])
        ),
        "agent_visible_provenance_exact_both": all(
            _visible_provenance_exact(branch)
            for branch in branches.values()
        ),
        "agent_visible_rows_preserve_server_response_both": all(
            _payload_projection(
                branch["routine_agent_visible"], ledger_columns
            )
            == [
                {
                    "variable": spec["variable"],
                    "columns": list(ledger_columns),
                    "data": [
                        [row[index] for index in indexes]
                        for row in ledger_row["data"]["data"]
                    ],
                }
                for spec, ledger_row in zip(
                    ROUTINE_SPECS,
                    branch["routine_ledger"],
                    strict=True,
                )
                for indexes in ([
                    ledger_row["data"]["columns"].index(column)
                    for column in ledger_columns
                ],)
            ]
            for branch in branches.values()
        ),
        "agent_visible_nonlabel_projection_exact_LOCAL_LATENT": (
            _payload_projection(
                local["routine_agent_visible"], visible_nonlabel_columns
            )
            == _payload_projection(
                latent["routine_agent_visible"], visible_nonlabel_columns
            )
        ),
        "routine_cost_is_440_both": all(
            abs(
                branch["budget_before_routine"]
                - branch["budget_after_routine"]
                - 440.0
            )
            < 1e-9
            for branch in branches.values()
        ),
        "budget_after_routine_is_1040_both": all(
            abs(branch["budget_after_routine"] - 1040.0) < 1e-9
            for branch in branches.values()
        ),
        "notice_has_no_hypothesis_cues": not any(
            cue in notice_lower for cue in PROHIBITED_NOTICE_CUES
        ),
        "recoverability_full_2D_both": all(
            row.get("design_rank") == 3
            and row.get("design_dimension") == 3
            and set(row.get("varying_controls", []))
            == {"feedstock_grade", "humidity"}
            for row in recoverability.values()
        ),
        "recoverability_BIC_CV_expected_both": all(
            row.get("informative") and row.get("recoverable")
            for row in recoverability.values()
        ),
        "future_experiments_blocked_both": all(
            branch["further_experiments_blocked"]
            for branch in branches.values()
        ),
    }
    return {
        "kind": "SCM_topology_controlled_2d_mechanical_certificate_v0",
        "interface_version": interface_version,
        "model": MODEL,
        "seed_offset": SEED_OFFSET,
        "source": str(source),
        "source_sha256": _sha256(source),
        "prefix_provenance": provenance,
        "physical_certificate": physical,
        "routine_notice": ROUTINE_NOTICE,
        "routine_specs": list(ROUTINE_SPECS),
        "branches": branches,
        "recoverability": recoverability,
        "gates": gates,
        "all": all(gates.values()),
    }


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    temporary.replace(path)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, default=SOURCE)
    parser.add_argument(
        "--interface-version",
        required=True,
        choices=INTERFACE_VERSIONS,
        help="v0 reproduces the hidden-provenance interface; v1 exposes it.",
    )
    parser.add_argument(
        "--run-agent",
        action="store_true",
        help="After the zero-LLM certificate passes, run both real branches.",
    )
    parser.add_argument("--max-post-routine-turns", type=int, default=6)
    parser.add_argument("--signature-n", type=int, default=4_000)
    parser.add_argument("--out", type=Path, default=None)
    args = parser.parse_args()
    if args.max_post_routine_turns < 1:
        raise ValueError("max-post-routine-turns must be at least 1")

    topology._configure_reused_runner(require_north_review_turn=True)
    prefix, provenance = topology.load_resumable_prefix(
        args.source,
        expected_model=MODEL,
        expected_seed=SEED_OFFSET,
    )
    certificate = build_mechanical_certificate(
        args.source,
        prefix,
        provenance,
        interface_version=args.interface_version,
    )
    certificate["kind"] = (
        "SCM_topology_controlled_2d_mechanical_certificate_"
        + args.interface_version
    )
    certificate_path = OUT / (
        f"gpt98403_controlled_2d_{args.interface_version}_certificate.json"
    )
    _write_json(certificate_path, certificate)
    if not certificate["all"]:
        print(
            json.dumps(
                {
                    "certificate": str(certificate_path),
                    "all": False,
                    "gates": certificate["gates"],
                },
                indent=2,
            ),
            flush=True,
        )
        raise SystemExit(1)

    if not args.run_agent:
        print(
            json.dumps(
                {
                    "certificate": str(certificate_path),
                    "all": True,
                    "agent_calls": 0,
                    "recoverability": {
                        name: {
                            "BIC_winner": row["BIC_winner"],
                            "CV_winner": row["CV_winner"],
                            "design_rank": row["design_rank"],
                        }
                        for name, row in certificate["recoverability"].items()
                    },
                },
                indent=2,
            ),
            flush=True,
        )
        return

    branches = {
        name: replay_routine_and_optionally_continue(
            case_dir,
            prefix,
            interface_version=args.interface_version,
            run_agent=True,
            max_post_routine_turns=args.max_post_routine_turns,
        )
        for name, case_dir in BRANCH_SPECS
    }
    mpre = prefix["selection"]["M_pre"]
    for index, (name, case_dir) in enumerate(BRANCH_SPECS):
        branch = branches[name]
        transfer.add_artifact_measurements(
            branch,
            case_dir,
            mpre,
            signature_n=args.signature_n,
            signature_seed=SEED_OFFSET + 2_100_000 + index,
        )
        topology.add_topology_measurements(
            branch,
            case_dir,
            mpre,
            signature_n=args.signature_n,
            signature_seed=SEED_OFFSET + 2_200_000 + index,
        )

    local = branches["local"]
    latent = branches["latent"]
    gates = {
        "mechanical_certificate_passed": certificate["all"],
        "at_least_one_real_post_routine_turn_both": all(
            len(branch["trace"]) >= 1 for branch in branches.values()
        ),
        "routine_ledgers_match_certificate": all(
            branch["routine_ledger"]
            == certificate["branches"][name]["routine_ledger"]
            for name, branch in branches.items()
        ),
        "agent_visible_tables_match_certificate": all(
            branch["routine_agent_visible"]
            == certificate["branches"][name]["routine_agent_visible"]
            for name, branch in branches.items()
        ),
        "routine_projection_still_exact": (
            _projection(local["routine_ledger"])
            == _projection(latent["routine_ledger"])
        ),
        "no_post_routine_experiments_both": all(
            not any(
                event["verb"] == "experiment"
                for row in branch["trace"]
                for event in row["trajectory"]
            )
            for branch in branches.values()
        ),
        "accepted_both": all(
            branch["accepted"] for branch in branches.values()
        ),
        "last_artifact_scoreable_both": all(
            branch["scores"]["M_last"].get("scoreable", False)
            for branch in branches.values()
        ),
        "topology_last_scoreable_both": all(
            branch["topology_signatures"]["M_last"].get(
                "scoreable", False
            )
            for branch in branches.values()
        ),
    }
    payload = {
        "kind": (
            "exploratory_SCM_topology_controlled_2d_"
            + args.interface_version
        ),
        "interface_version": args.interface_version,
        "claim_scope": (
            "Paired LOCAL/LATENT topology control under a fixed minimally "
            "sufficient 2D evidence geometry; not a prevalence estimate."
        ),
        "model": MODEL,
        "seed_offset": SEED_OFFSET,
        "source": str(args.source),
        "mechanical_certificate": certificate,
        "branches": branches,
        "gates": gates,
        "all": all(gates.values()),
    }
    target = args.out or OUT / (
        "probe_gpt-5.4_seed98403_controlled_2d_"
        f"{args.interface_version}.json"
    )
    _write_json(target, payload)
    print(
        json.dumps(
            {
                "out": str(target),
                "all": payload["all"],
                "gates": gates,
                "abort": {
                    name: branch["abort"]
                    for name, branch in branches.items()
                },
            },
            indent=2,
        ),
        flush=True,
    )


if __name__ == "__main__":
    main()
