"""Real-agent probe of an accelerated, genuinely lived research past.

The validated South-to-North SCM twins are reused unchanged.  One donor agent
forms a transferable executable model in South and then processes four real,
routine North campaigns over four separate turns.  Those on-manifold campaign
outputs are byte-identical between REVISE and RETAIN.  A fixed ordinary audit
then intervenes on grade and is replayed into four continuations:

* native full trajectory x REVISE/RETAIN;
* fresh neutral compact state x REVISE/RETAIN.

The script records Mpre/Mfirst/Mlast and causal signatures without putting an
LLM in scoring.  ``--cert-only`` exercises every zero-LLM geometry gate.  The
exploratory contract is frozen in
``docs/research/2026-08-01-ficha-probe-pasado-acelerado-vivido-v0.md``.
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
from typing import Any

import pandas as pd

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
    global_score,
    record,
    select_last_scoreable,
)
from scripts.probe_first_story_scm_fork import (  # noqa: E402
    _artifact_hash,
    _score_delta,
    _stable_stdout,
)
from scripts.probe_first_story_scm_transfer_fork import (  # noqa: E402
    REVISE,
    RETAIN,
    SYSTEM,
    _belief_gate,
    _experiments_have_site,
    _ledger_is_south,
    both_site_signatures,
    site_signature,
    south_initial_prompt,
    truth_site_signature,
)


OUT = ROOT / "scripts" / "out" / "first_story_scm_accelerated_lived_history"
AUDIT_VARIABLES = ("north_audit_grade3", "north_audit_grade7")
ROUTINE_SPECS = (
    {"name": "north_routine_01", "config": {}, "n": 32},
    {"name": "north_routine_02", "config": {"humidity": 3.0}, "n": 32},
    {"name": "north_routine_03", "config": {"humidity": 5.0}, "n": 32},
    {"name": "north_routine_04", "config": {"humidity": 7.0}, "n": 32},
)
AUDIT_SPECS = (
    {
        "name": AUDIT_VARIABLES[0],
        "config": {"humidity": 5.0, "feedstock_grade": 3.0},
        "n": 32,
    },
    {
        "name": AUDIT_VARIABLES[1],
        "config": {"humidity": 5.0, "feedstock_grade": 7.0},
        "n": 32,
    },
)
BRANCHES = (
    ("native_revise", "native", REVISE, "revise"),
    ("native_retain", "native", RETAIN, "retain"),
    ("fresh_revise", "fresh", REVISE, "revise"),
    ("fresh_retain", "fresh", RETAIN, "retain"),
)

TRANSITION = (
    "South work is complete and the same project now enters routine North transfer "
    "operations. North uses context={\"site\": \"north\"}."
)
AUDIT_NOTICE = (
    "The next standard North audit cycle has closed. The two raw batches are "
    "available as `north_audit_grade3` and `north_audit_grade7`. Data collection "
    "is now closed for this delivery cycle. Inspect the batches, keep "
    "`working_model` current, and submit when the assignment is sufficient."
)
_NON_NEUTRAL = re.compile(
    r"\b(revise|retain|refut|contradic|correction|wrong|change your mind)\w*\b",
    re.IGNORECASE,
)


def _request(spec: dict[str, Any]) -> dict[str, Any]:
    return {
        "config": copy.deepcopy(spec["config"]),
        "context": {"site": "north"},
        "n": int(spec["n"]),
        "horizon": None,
    }


def _design(spec: dict[str, Any]) -> ExperimentDesign:
    return ExperimentDesign(**_request(spec))


def _frame_from_ledger(row: dict[str, Any]) -> pd.DataFrame:
    data = row["data"]
    frame = pd.DataFrame(data["data"], columns=data["columns"])
    for column, dtype in zip(data["columns"], data["dtypes"], strict=True):
        frame[column] = frame[column].astype(dtype)
    return frame


def _frame_hash(frame: pd.DataFrame) -> str:
    payload = frame.to_json(
        orient="split", double_precision=15, date_unit="ns", index=False
    )
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def _ledger_hash(ledger: list[dict[str, Any]]) -> str:
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def _evidence_requests(trajectory: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        {"verb": row["verb"], "args": row["args"], "cost": row["cost"]}
        for row in trajectory
        if row["verb"] in {"observe", "experiment"}
    ]


def _expected_experiment_request(spec: dict[str, Any], cost: float) -> dict[str, Any]:
    request = _request(spec)
    request.pop("horizon")
    return {"verb": "experiment", "args": request, "cost": cost}


def _chat_usage(chat: FoundryChat) -> dict[str, Any]:
    return {
        "tokens": chat.usage.total_tokens,
        "turns": [
            {
                "prompt_tokens": row.prompt_tokens,
                "completion_tokens": row.completion_tokens,
                "reasoning_tokens": row.reasoning_tokens,
                "latency_s": row.latency_s,
            }
            for row in chat.turns
        ],
    }


def _routine_prompt(
    previous_feedback: str,
    spec: dict[str, Any],
    index: int,
) -> str:
    transition = TRANSITION + "\n\n" if index == 1 else ""
    return (
        previous_feedback
        + "\n\n"
        + transition
        + f"Routine North cycle {index}/{len(ROUTINE_SPECS)} has closed. Its raw "
        + f"output is loaded as `{spec['name']}`. Inspect this batch and keep the "
        + "executable project model current. Collection for this checkpoint is "
        + "complete: do not call env.observe, env.experiment, or env.submit in this "
        + "turn."
    )


def _fresh_prompt(
    server,
    summary: pd.DataFrame,
    catalog: pd.DataFrame | None = None,
) -> str:
    sheet = server.describe()
    machine = {key: value for key, value in sheet.items() if key != "brief"}
    prompt = (
        "Here is the assignment:\n\n"
        + sheet["brief"]
        + "\n\nMachine-readable sheet:\n"
        + json.dumps(machine, indent=2)
        + "\n\nYou are continuing from a compact, mechanically prepared project state. "
        "The current executable source is loaded as the string `working_model`. "
        f"`campaign_summary` is a pandas DataFrame with {len(summary)} neutral rows "
        f"and columns {summary.columns.tolist()}. `campaign_catalog` is also a pandas "
        f"DataFrame, with columns {catalog.columns.tolist() if catalog is not None else []}; "
        "its `name` column lists a complete raw archive under the canonical names "
        "`campaign_001`, `campaign_002`, and so on. Those raw campaigns are separate "
        "DataFrame variables in the workspace, not values stored inside the catalog; "
        "for example, use `campaign_001` directly or `globals()[row['name']]`. The two raw "
        "batches from the current standard North audit are "
        "loaded as `north_audit_grade3` and `north_audit_grade7`. Data collection is "
        "closed for this delivery cycle. Inspect the audit batches, keep "
        "`working_model` current, and submit when the assignment is sufficient."
    )
    return prompt


def _artifact_valid(server, code: str | None) -> tuple[bool, str | None]:
    if code is None:
        return False, "missing artifact"
    error = server.validate_model(code)
    return error is None, error


def run_lived_prefix(
    model: str,
    seed_offset: int,
    *,
    max_south_turns: int,
    belief_delta_threshold: float,
    signature_n: int,
) -> dict[str, Any]:
    """Create the sole lived donor, stopping immediately before the audit."""
    server = build_world_server(REVISE, seed_offset=seed_offset)
    chat = FoundryChat(
        system=SYSTEM,
        model=model,
        max_completion_tokens=MAX_COMPLETION_TOKENS,
    )
    trace: list[dict[str, Any]] = []
    checkpoints: list[dict[str, Any]] = []
    prompt = south_initial_prompt(server)
    abort = "no_transferable_model_after_max_south_turns"
    formation: dict[str, Any] | None = None
    previous_feedback = ""

    with KernelClient(server, cell_timeout_s=CELL_TIMEOUT_S) as kernel:
        for turn in range(1, max_south_turns + 1):
            notices = server.begin_turn(turn)
            deliveries = server.pop_deliveries()
            for variable, frame in deliveries:
                kernel.inject_dataframe(variable, frame)
            reply = chat.ask(prompt)
            cell = extract_cell(reply.content)
            if cell is None:
                abort = "no_cell_during_south"
                break
            start = len(server.trajectory)
            result = kernel.run_cell(cell)
            row = record(turn, reply.content, cell, result, server, notices, start)
            row.update({"phase": "south", "scheduled_campaign": None})
            trace.append(row)
            if not _experiments_have_site(row["trajectory"], "south"):
                abort = "non_south_experiment_before_transition"
                break
            ledger = server.export_evidence_ledger()
            if not _ledger_is_south(ledger):
                abort = "non_south_evidence_before_transition"
                break
            if server.terminal:
                abort = "submitted_before_lived_north"
                break
            if result.error and result.error.startswith("cell exceeded "):
                abort = "cell_timeout_during_south"
                break
            code = result.working_model
            valid, validation_error = _artifact_valid(server, code)
            signatures = both_site_signatures(
                code,
                server.columns,
                n_samples=signature_n,
                seed=seed_offset + 710_000,
            )
            previous_feedback = feedback(result, server)
            if valid and bool(ledger) and _belief_gate(
                signatures, belief_delta_threshold
            ):
                formation = {
                    "turn": turn,
                    "code": code,
                    "sha256": _artifact_hash(code),
                    "signatures": signatures,
                    "validation_error": validation_error,
                    "evidence_ledger": ledger,
                }
                abort = "transferable_model_formed"
                break
            prompt = previous_feedback

        if formation is not None:
            required_cost = sum(
                server.config.experiment.cost_fixed
                + server.config.experiment.cost_per_row * int(spec["n"])
                for spec in (*ROUTINE_SPECS, *AUDIT_SPECS)
            )
            if server.budget_remaining + 1e-9 < required_cost:
                abort = "insufficient_budget_for_frozen_protocol"
            else:
                first_routine_turn = formation["turn"] + 1
                for index, spec in enumerate(ROUTINE_SPECS, start=1):
                    turn = first_routine_turn + index - 1
                    notices = server.begin_turn(turn)
                    deliveries = server.pop_deliveries()
                    for variable, frame in deliveries:
                        kernel.inject_dataframe(variable, frame)
                    start = len(server.trajectory)
                    frame = server.experiment(_design(spec))
                    kernel.inject_dataframe(spec["name"], frame)
                    stage_prompt = _routine_prompt(previous_feedback, spec, index)
                    reply = chat.ask(stage_prompt)
                    cell = extract_cell(reply.content)
                    if cell is None:
                        abort = f"no_cell_routine_{index}"
                        break
                    result = kernel.run_cell(cell)
                    row = record(
                        turn, reply.content, cell, result, server, notices, start
                    )
                    row.update(
                        {
                            "phase": "north_routine",
                            "routine_index": index,
                            "scheduled_campaign": {
                                "name": spec["name"],
                                "request": _request(spec),
                                "frame_hash": _frame_hash(frame),
                            },
                            "stage_prompt": stage_prompt,
                        }
                    )
                    trace.append(row)
                    evidence_calls = _evidence_requests(row["trajectory"])
                    expected = _expected_experiment_request(
                        spec,
                        server.config.experiment.cost_fixed
                        + server.config.experiment.cost_per_row * int(spec["n"]),
                    )
                    if evidence_calls != [expected]:
                        abort = f"extra_or_missing_evidence_routine_{index}"
                        break
                    if server.terminal:
                        abort = f"submitted_during_routine_{index}"
                        break
                    if result.error and result.error.startswith("cell exceeded "):
                        abort = f"cell_timeout_routine_{index}"
                        break
                    code = result.working_model
                    valid, validation_error = _artifact_valid(server, code)
                    inspected = re.search(
                        rf"\b{re.escape(spec['name'])}\b", cell
                    ) is not None
                    signatures = both_site_signatures(
                        code,
                        server.columns,
                        n_samples=signature_n,
                        seed=seed_offset + 720_000 + index,
                    )
                    checkpoints.append(
                        {
                            "index": index,
                            "turn": turn,
                            "campaign_name": spec["name"],
                            "campaign_hash": _frame_hash(frame),
                            "code": code,
                            "sha256": _artifact_hash(code),
                            "inspected": inspected,
                            "valid": valid,
                            "validation_error": validation_error,
                            "signatures": signatures,
                        }
                    )
                    if not valid:
                        abort = f"invalid_model_routine_{index}"
                        break
                    if not inspected:
                        abort = f"routine_not_inspected_{index}"
                        break
                    previous_feedback = feedback(result, server)
                else:
                    if not _belief_gate(
                        checkpoints[-1]["signatures"], belief_delta_threshold
                    ):
                        abort = "Mpre_lost_transfer_belief"
                    else:
                        abort = "lived_prefix_ready"

    ledger = server.export_evidence_ledger()
    return {
        "abort": abort,
        "trace": trace,
        "formation": formation,
        "routine_checkpoints": checkpoints,
        "M_pre": checkpoints[-1]["code"] if checkpoints else None,
        "M_pre_sha256": (
            _artifact_hash(checkpoints[-1]["code"]) if checkpoints else None
        ),
        "messages": copy.deepcopy(chat.messages),
        "last_feedback": previous_feedback,
        "evidence_ledger": ledger,
        "evidence_hash": _ledger_hash(ledger),
        "budget_before_audit": float(server.budget_remaining),
        "last_turn": trace[-1]["turn"] if trace else 0,
        "usage": _chat_usage(chat),
    }


def replay_lived_prefix(
    server,
    prefix: dict[str, Any],
    kernel: KernelClient,
) -> tuple[list[dict[str, Any]], dict[str, Any] | None]:
    """Replay both agent cells and server-scheduled routine campaigns exactly."""
    checks: list[dict[str, Any]] = []
    last_record = None
    ledger_rows = {int(row["sequence"]): row for row in prefix["evidence_ledger"]}
    for donor in prefix["trace"]:
        notices = server.begin_turn(int(donor["turn"]))
        deliveries = server.pop_deliveries()
        for variable, frame in deliveries:
            kernel.inject_dataframe(variable, frame)
        start = len(server.trajectory)
        scheduled = donor.get("scheduled_campaign")
        frame_exact = True
        frame_hash_exact = True
        if scheduled is not None:
            before = len(server.export_evidence_ledger())
            frame = server.experiment(ExperimentDesign(**scheduled["request"]))
            kernel.inject_dataframe(scheduled["name"], frame)
            expected = ledger_rows[before + 1]
            expected_frame = _frame_from_ledger(expected)
            frame_exact = frame.equals(expected_frame)
            frame_hash_exact = _frame_hash(frame) == scheduled["frame_hash"]
        result = kernel.run_cell(donor["cell"])
        actual = record(
            donor["turn"],
            donor["reply_text"],
            donor["cell"],
            result,
            server,
            notices,
            start,
        )
        last_record = actual
        checks.append(
            {
                "turn": donor["turn"],
                "notices_exact": notices == donor["notices"],
                "no_unscheduled_deliveries": not deliveries,
                "scheduled_frame_exact": frame_exact,
                "scheduled_frame_hash_exact": frame_hash_exact,
                "stdout_exact": _stable_stdout(result.stdout)
                == _stable_stdout(donor["cell_result"]["stdout"]),
                "error_exact": result.error == donor["cell_result"]["error"],
                "working_model_exact": result.working_model
                == donor["working_model"]["code"],
                "working_model_status_exact": result.working_model_status
                == donor["working_model"]["status"],
                "trajectory_exact": actual["trajectory"] == donor["trajectory"],
            }
        )
    return checks, last_record


def _replay_evidence_only(
    server,
    ledger: list[dict[str, Any]],
) -> dict[str, Any]:
    """Recreate the server state for a fresh compact handoff."""
    by_turn: dict[int, list[dict[str, Any]]] = {}
    for row in ledger:
        by_turn.setdefault(int(row["turn"]), []).append(row)
    checks: list[dict[str, Any]] = []
    for turn in range(1, max(by_turn, default=0) + 1):
        server.begin_turn(turn)
        deliveries = server.pop_deliveries()
        for expected in by_turn.get(turn, []):
            request = expected["request"]
            if expected["kind"] == "observe":
                actual = server.observe(expected["source"], int(request["n"]))
            elif expected["kind"] == "experiment":
                actual = server.experiment(ExperimentDesign(**request))
            else:
                raise ValueError(f"unsupported evidence kind {expected['kind']!r}")
            expected_frame = _frame_from_ledger(expected)
            checks.append(
                {
                    "sequence": expected["sequence"],
                    "frame_exact": actual.equals(expected_frame),
                    "hash_exact": _frame_hash(actual) == _frame_hash(expected_frame),
                }
            )
        if deliveries:
            checks.append(
                {
                    "sequence": f"turn_{turn}_delivery",
                    "frame_exact": False,
                    "hash_exact": False,
                }
            )
    actual_ledger = server.export_evidence_ledger()
    return {
        "rows": checks,
        "all_frames_exact": all(row["frame_exact"] for row in checks),
        "all_hashes_exact": all(row["hash_exact"] for row in checks),
        "ledger_exact": actual_ledger == ledger,
        "ledger_hash": _ledger_hash(actual_ledger),
    }


def _compact_summary(ledger: list[dict[str, Any]]) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    for index, row in enumerate(ledger, start=1):
        frame = _frame_from_ledger(row)
        request = row["request"]
        config = request.get("config", {})
        rows.append(
            {
                "sequence": int(row["sequence"]),
                "turn": int(row["turn"]),
                "name": f"campaign_{index:03d}",
                "kind": row["kind"],
                "source": row.get("source") or "",
                "site": request.get("context", {}).get("site", "south"),
                "config": json.dumps(config, sort_keys=True, separators=(",", ":")),
                "n": len(frame),
                "feedstock_mean": float(frame["feedstock"].mean()),
                "feedstock_sd": float(frame["feedstock"].std(ddof=1)),
                "outcome_mean": float(frame["outcome"].mean()),
                "outcome_sd": float(frame["outcome"].std(ddof=1)),
                "feedstock_outcome_corr": float(
                    frame[["feedstock", "outcome"]].corr().iloc[0, 1]
                ),
            }
        )
    return pd.DataFrame(rows)


def _archive_catalog(ledger: list[dict[str, Any]]) -> pd.DataFrame:
    rows = []
    for index, row in enumerate(ledger, start=1):
        request = row["request"]
        rows.append(
            {
                "sequence": int(row["sequence"]),
                "turn": int(row["turn"]),
                "name": f"campaign_{index:03d}",
                "kind": row["kind"],
                "source": row.get("source") or "",
                "site": request.get("context", {}).get("site", "south"),
                "config": json.dumps(
                    request.get("config", {}),
                    sort_keys=True,
                    separators=(",", ":"),
                ),
                "n": int(request["n"]),
            }
        )
    return pd.DataFrame(rows)


def _inject_audit(server, kernel: KernelClient, turn: int) -> dict[str, Any]:
    notices = server.begin_turn(turn)
    deliveries = server.pop_deliveries()
    for variable, frame in deliveries:
        kernel.inject_dataframe(variable, frame)
    start = len(server.trajectory)
    frames: dict[str, pd.DataFrame] = {}
    for spec in AUDIT_SPECS:
        frame = server.experiment(_design(spec))
        kernel.inject_dataframe(spec["name"], frame)
        frames[spec["name"]] = frame
    trajectory = [
        {
            "verb": event.verb,
            "args": event.args,
            "cost": event.cost,
            "note": event.note,
        }
        for event in server.trajectory[start:]
    ]
    return {
        "turn": turn,
        "notices": notices,
        "deliveries": len(deliveries),
        "trajectory_start": start,
        "requests": _evidence_requests(trajectory),
        "frame_hashes": {name: _frame_hash(frame) for name, frame in frames.items()},
        "frames": frames,
    }


def _cell_inspects_audit(cell: str) -> dict[str, bool]:
    return {
        name: re.search(rf"\b{re.escape(name)}\b", cell) is not None
        for name in AUDIT_VARIABLES
    }


def _continue_after_audit(
    *,
    server,
    kernel: KernelClient,
    chat: FoundryChat,
    prompt: str,
    audit_turn: int,
    post_audit_turns: int,
    phase: str,
) -> dict[str, Any]:
    trace: list[dict[str, Any]] = []
    audit = _inject_audit(server, kernel, audit_turn)
    abort = "max_turns"
    inspection = {name: False for name in AUDIT_VARIABLES}
    for offset in range(post_audit_turns):
        turn = audit_turn + offset
        if offset == 0:
            notices = audit["notices"]
            start = int(audit["trajectory_start"])
        else:
            if server.terminal:
                abort = "submitted"
                break
            notices = server.begin_turn(turn)
            deliveries = server.pop_deliveries()
            for variable, frame in deliveries:
                kernel.inject_dataframe(variable, frame)
            start = len(server.trajectory)
        reply = chat.ask(prompt)
        cell = extract_cell(reply.content)
        if cell is None:
            abort = "no_cell"
            break
        if offset == 0:
            inspection = _cell_inspects_audit(cell)
        result = kernel.run_cell(cell)
        row = record(turn, reply.content, cell, result, server, notices, start)
        row.update({"phase": phase, "post_audit_index": offset + 1})
        trace.append(row)
        if server.terminal:
            abort = "submitted"
            break
        if result.error and result.error.startswith("cell exceeded "):
            abort = "cell_timeout"
            break
        prompt = feedback(result, server) + (
            "\n\nData collection remains closed for this delivery cycle."
        )
    return {
        "trace": trace,
        "audit": {
            key: value for key, value in audit.items() if key != "frames"
        },
        "inspection": inspection,
        "abort": abort,
    }


def _run_native(
    case_dir: Path,
    prefix: dict[str, Any],
    *,
    model: str,
    seed_offset: int,
    post_audit_turns: int,
) -> dict[str, Any]:
    server = build_world_server(case_dir, seed_offset=seed_offset)
    with KernelClient(server, cell_timeout_s=CELL_TIMEOUT_S) as kernel:
        replay_checks, _ = replay_lived_prefix(server, prefix, kernel)
        replay_ledger = server.export_evidence_ledger()
        replay_budget = float(server.budget_remaining)
        chat = FoundryChat(
            system=SYSTEM,
            model=model,
            max_completion_tokens=MAX_COMPLETION_TOKENS,
        )
        chat.messages = copy.deepcopy(prefix["messages"])
        prompt = prefix["last_feedback"] + "\n\n" + AUDIT_NOTICE
        continuation = _continue_after_audit(
            server=server,
            kernel=kernel,
            chat=chat,
            prompt=prompt,
            audit_turn=int(prefix["last_turn"]) + 1,
            post_audit_turns=post_audit_turns,
            phase="native_full_trajectory",
        )
        transcript = copy.deepcopy(chat.messages)
        usage = _chat_usage(chat)
    final = server.result or {}
    return {
        "mode": "native",
        "case_id": case_dir.name,
        "prefix_replay_checks": replay_checks,
        "prefix_replay_exact": all(
            all(value for key, value in row.items() if key != "turn")
            for row in replay_checks
        ),
        "prefix_ledger_exact": replay_ledger == prefix["evidence_ledger"],
        "prefix_evidence_hash": _ledger_hash(replay_ledger),
        "budget_before_audit": replay_budget,
        "native_prompt": prompt,
        **continuation,
        "accepted": server.terminal,
        "submission_code": final.get("code"),
        "R": final.get("R"),
        "evidence_ledger": server.export_evidence_ledger(),
        "transcript": transcript,
        "usage": usage,
    }


def _run_fresh(
    case_dir: Path,
    prefix: dict[str, Any],
    *,
    model: str,
    seed_offset: int,
    post_audit_turns: int,
) -> dict[str, Any]:
    server = build_world_server(case_dir, seed_offset=seed_offset)
    evidence_replay = _replay_evidence_only(server, prefix["evidence_ledger"])
    replay_budget = float(server.budget_remaining)
    summary = _compact_summary(prefix["evidence_ledger"])
    catalog = _archive_catalog(prefix["evidence_ledger"])
    archive_hashes: dict[str, str] = {}
    with KernelClient(server, cell_timeout_s=CELL_TIMEOUT_S) as kernel:
        for index, row in enumerate(prefix["evidence_ledger"], start=1):
            name = f"campaign_{index:03d}"
            frame = _frame_from_ledger(row)
            kernel.inject_dataframe(name, frame)
            archive_hashes[name] = _frame_hash(frame)
        kernel.inject_dataframe("campaign_catalog", catalog)
        kernel.inject_dataframe("campaign_summary", summary)
        initialization = kernel.run_cell(
            "working_model = " + repr(prefix["M_pre"])
        )
        chat = FoundryChat(
            system=SYSTEM,
            model=model,
            max_completion_tokens=MAX_COMPLETION_TOKENS,
        )
        prompt = _fresh_prompt(server, summary, catalog)
        continuation = _continue_after_audit(
            server=server,
            kernel=kernel,
            chat=chat,
            prompt=prompt,
            audit_turn=int(prefix["last_turn"]) + 1,
            post_audit_turns=post_audit_turns,
            phase="fresh_neutral_compact",
        )
        transcript = copy.deepcopy(chat.messages)
        usage = _chat_usage(chat)
    final = server.result or {}
    expected_archive_hashes = {
        f"campaign_{index:03d}": _frame_hash(_frame_from_ledger(row))
        for index, row in enumerate(prefix["evidence_ledger"], start=1)
    }
    return {
        "mode": "fresh",
        "case_id": case_dir.name,
        "evidence_replay": evidence_replay,
        "prefix_replay_exact": evidence_replay["ledger_exact"]
        and evidence_replay["all_frames_exact"]
        and evidence_replay["all_hashes_exact"],
        "prefix_ledger_exact": evidence_replay["ledger_exact"],
        "prefix_evidence_hash": evidence_replay["ledger_hash"],
        "budget_before_audit": replay_budget,
        "raw_archive": {
            "count": len(archive_hashes),
            "frame_hashes": archive_hashes,
            "catalog": catalog.to_dict(orient="records"),
            "exact": archive_hashes == expected_archive_hashes,
        },
        "compact_summary": summary.to_dict(orient="records"),
        "M_pre_initialization": {
            "ok": initialization.ok,
            "error": initialization.error,
            "working_model_exact": initialization.working_model == prefix["M_pre"],
        },
        "fresh_prompt": prompt,
        "fresh_prompt_neutral": _NON_NEUTRAL.search(prompt) is None,
        **continuation,
        "accepted": server.terminal,
        "submission_code": final.get("code"),
        "R": final.get("R"),
        "evidence_ledger": server.export_evidence_ledger(),
        "transcript": transcript,
        "usage": usage,
    }


def _update_fraction(pre: float, post: float, truth: float) -> float | None:
    denominator = pre - truth
    if abs(denominator) < 0.5:
        return None
    return float((pre - post) / denominator)


def _measure_branch(
    branch: dict[str, Any],
    case_dir: Path,
    mpre: str,
    *,
    truth_pole: str,
    signature_n: int,
    signature_seed: int,
) -> None:
    first_code = next(
        (
            row["working_model"]["code"]
            for row in branch["trace"]
            if row["working_model"]["code"] is not None
        ),
        None,
    )
    branch_for_selection = {
        "submission_code": branch.get("submission_code"),
        "trace": branch["trace"],
    }
    last_code, source, last_score, failures = select_last_scoreable(
        case_dir, branch_for_selection, mpre
    )
    scores = {
        "M_pre": global_score(case_dir, mpre),
        "M_first": global_score(case_dir, first_code),
        "M_last": last_score,
    }
    truth = {
        site: truth_site_signature(
            case_dir,
            site,
            n_samples=max(20_000, signature_n),
            seed=signature_seed,
        )
        for site in ("south", "north")
    }
    signatures: dict[str, Any] = {"truth": truth}
    for checkpoint, code in (
        ("M_pre", mpre),
        ("M_first", first_code),
        ("M_last", last_code),
    ):
        for site in ("south", "north"):
            signatures[f"{checkpoint}_{site}"] = site_signature(
                code,
                ["feedstock", "outcome"],
                site,
                n_samples=signature_n,
                seed=signature_seed,
            )
    pre_north = signatures["M_pre_north"].get("delta_outcome_G_at_H5")
    first_north = signatures["M_first_north"].get("delta_outcome_G_at_H5")
    last_north = signatures["M_last_north"].get("delta_outcome_G_at_H5")
    truth_north = truth["north"]["delta_outcome_G_at_H5"]
    pre_south = signatures["M_pre_south"].get("delta_outcome_G_at_H5")
    last_south = signatures["M_last_south"].get("delta_outcome_G_at_H5")
    u_first = (
        _update_fraction(pre_north, first_north, truth_north)
        if None not in (pre_north, first_north)
        else None
    )
    u_last = (
        _update_fraction(pre_north, last_north, truth_north)
        if None not in (pre_north, last_north)
        else None
    )
    revise_correct = bool(
        truth_pole == "revise"
        and u_last is not None
        and u_last >= 0.60
        and abs(float(last_north) - truth_north) <= 2.0
    )
    retain_correct = bool(
        truth_pole == "retain"
        and last_north is not None
        and pre_north is not None
        and abs(float(last_north) - float(pre_north)) <= 1.5
        and abs(float(last_north) - truth_north) <= 2.0
    )
    south_preserved = bool(
        pre_south is not None
        and last_south is not None
        and abs(float(last_south) - float(pre_south)) <= 1.5
    )
    branch.update(
        {
            "M_pre": mpre,
            "M_first": first_code,
            "M_last": last_code,
            "M_last_source": source,
            "later_invalid_artifacts": failures,
            "artifact_hashes": {
                "M_pre": _artifact_hash(mpre),
                "M_first": _artifact_hash(first_code),
                "M_last": _artifact_hash(last_code),
            },
            "scores": scores,
            "signatures": signatures,
            "metrics": {
                "U_first": u_first,
                "U_last": u_last,
                "revise_correct": revise_correct,
                "retain_correct": retain_correct,
                "south_preserved": south_preserved,
                "score_R_delta_first_minus_pre": _score_delta(
                    scores["M_first"], scores["M_pre"]
                ),
                "score_R_delta_last_minus_pre": _score_delta(
                    scores["M_last"], scores["M_pre"]
                ),
            },
        }
    )


def local_certificate(seed_offset: int, signature_n: int) -> dict[str, Any]:
    revise = build_world_server(REVISE, seed_offset=seed_offset)
    retain = build_world_server(RETAIN, seed_offset=seed_offset)
    routine_rows = []
    for index, spec in enumerate(ROUTINE_SPECS):
        regime = SimpleNamespace(
            config=copy.deepcopy(spec["config"]),
            context={"site": "north"},
            horizon=None,
        )
        seed = seed_offset + 1_100_000 + index
        left = revise.world_sample(regime, int(spec["n"]), seed)
        right = retain.world_sample(regime, int(spec["n"]), seed)
        routine_rows.append(
            {
                "name": spec["name"],
                "grade_unset": "feedstock_grade" not in spec["config"],
                "frames_equal": left.equals(right),
                "hash_equal": _frame_hash(left) == _frame_hash(right),
            }
        )
    audit_truth = {}
    for name, server in (("revise", revise), ("retain", retain)):
        means = {}
        for index, spec in enumerate(AUDIT_SPECS):
            regime = SimpleNamespace(
                config=copy.deepcopy(spec["config"]),
                context={"site": "north"},
                horizon=None,
            )
            frame = server.world_sample(
                regime, max(20_000, signature_n), seed_offset + 1_200_000 + index
            )
            means[spec["name"]] = float(frame["outcome"].mean())
        audit_truth[name] = {
            "means": means,
            "delta_grade7_minus_grade3": means[AUDIT_VARIABLES[1]]
            - means[AUDIT_VARIABLES[0]],
        }
    experiment_cost = (
        revise.config.experiment.cost_fixed
        + revise.config.experiment.cost_per_row * int(ROUTINE_SPECS[0]["n"])
    )
    expected_requests = [
        _expected_experiment_request(spec, experiment_cost)
        for spec in AUDIT_SPECS
    ]
    gates = {
        "agent_facing_twins_identical": revise.describe() == retain.describe(),
        "four_routine_cycles": len(ROUTINE_SPECS) == 4,
        "routine_grade_unset_all": all(row["grade_unset"] for row in routine_rows),
        "routine_frames_byte_identical_all": all(
            row["frames_equal"] and row["hash_equal"] for row in routine_rows
        ),
        "audit_requests_distinct_and_fixed": (
            len(expected_requests) == 2
            and expected_requests[0] != expected_requests[1]
        ),
        "audit_revise_truth_near_zero": abs(
            audit_truth["revise"]["delta_grade7_minus_grade3"]
        )
        <= 0.15,
        "audit_retain_truth_near_eight": abs(
            audit_truth["retain"]["delta_grade7_minus_grade3"] - 8.0
        )
        <= 0.15,
        "fresh_prompt_neutral": _NON_NEUTRAL.search(
            _fresh_prompt(revise, pd.DataFrame([{"x": 1}]))
        )
        is None,
    }
    return {
        "kind": "zero_llm_accelerated_lived_history_certificate",
        "seed_offset": seed_offset,
        "routine": routine_rows,
        "audit_truth": audit_truth,
        "expected_audit_requests": expected_requests,
        "gates": gates,
        "all": all(gates.values()),
    }


def _write_early(
    target: Path,
    *,
    model: str,
    seed_offset: int,
    certificate: dict[str, Any],
    prefix: dict[str, Any],
    gates: dict[str, bool],
) -> None:
    payload = {
        "kind": "exploratory_accelerated_lived_history_probe",
        "claim_class": "precondition_failed_no_trajectory_inference",
        "model": model,
        "seed_offset": seed_offset,
        "certificate": certificate,
        "prefix": prefix,
        "branches": {},
        "gates": gates,
        "all": False,
    }
    target.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(
        json.dumps(
            {"out": str(target), "abort": prefix["abort"], "gates": gates},
            indent=2,
        ),
        flush=True,
    )




def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", default="DeepSeek-V3.2")
    parser.add_argument("--seed-offset", type=int, default=97800)
    parser.add_argument("--max-south-turns", type=int, default=14)
    parser.add_argument("--post-audit-turns", type=int, default=4)
    parser.add_argument("--belief-delta-threshold", type=float, default=3.0)
    parser.add_argument("--signature-n", type=int, default=4000)
    parser.add_argument("--cert-only", action="store_true")
    parser.add_argument("--out", type=Path, default=None)
    args = parser.parse_args()

    model = args.model
    seed_offset = args.seed_offset
    certificate = local_certificate(seed_offset, args.signature_n)
    if args.cert_only:
        print(json.dumps(certificate, indent=2), flush=True)
        if not certificate["all"]:
            raise SystemExit(1)
        return
    if not certificate["all"]:
        raise RuntimeError("zero-LLM certificate failed")
    if not 97800 <= seed_offset <= 97849:
        raise ValueError("exploratory ficha reserves seed offsets 97800..97849")

    OUT.mkdir(parents=True, exist_ok=True)
    target = args.out or OUT / f"probe_{model}_seed{seed_offset}.json"
    target.parent.mkdir(parents=True, exist_ok=True)
    prefix = run_lived_prefix(
        model,
        seed_offset,
        max_south_turns=args.max_south_turns,
        belief_delta_threshold=args.belief_delta_threshold,
        signature_n=args.signature_n,
    )
    prefix_gates = {
        "zero_llm_certificate": certificate["all"],
        "lived_prefix_ready": prefix["abort"] == "lived_prefix_ready",
        "four_routine_checkpoints": len(prefix["routine_checkpoints"]) == 4,
        "routine_models_valid_all": len(prefix["routine_checkpoints"]) == 4
        and all(row["valid"] for row in prefix["routine_checkpoints"]),
        "routine_campaigns_inspected_all": len(prefix["routine_checkpoints"]) == 4
        and all(row["inspected"] for row in prefix["routine_checkpoints"]),
        "M_pre_present": prefix["M_pre"] is not None,
        "M_pre_belief_gate": bool(prefix["routine_checkpoints"])
        and _belief_gate(
            prefix["routine_checkpoints"][-1]["signatures"],
            args.belief_delta_threshold,
        ),
        "budget_covers_audit": prefix["budget_before_audit"]
        >= sum(
            100.0 + 2.0 * int(spec["n"])
            for spec in AUDIT_SPECS
        ),
    }
    if not all(prefix_gates.values()):
        _write_early(
            target,
            model=model,
            seed_offset=seed_offset,
            certificate=certificate,
            prefix=prefix,
            gates=prefix_gates,
        )
        return

    branches: dict[str, Any] = {}
    for name, mode, case_dir, truth_pole in BRANCHES:
        if mode == "native":
            branch = _run_native(
                case_dir,
                prefix,
                model=model,
                seed_offset=seed_offset,
                post_audit_turns=args.post_audit_turns,
            )
        else:
            branch = _run_fresh(
                case_dir,
                prefix,
                model=model,
                seed_offset=seed_offset,
                post_audit_turns=args.post_audit_turns,
            )
        branch["truth_pole"] = truth_pole
        _measure_branch(
            branch,
            case_dir,
            prefix["M_pre"],
            truth_pole=truth_pole,
            signature_n=args.signature_n,
            signature_seed=seed_offset + 1_300_000,
        )
        branches[name] = branch

    expected_requests = certificate["expected_audit_requests"]
    audit_requests = {
        name: branch["audit"]["requests"] for name, branch in branches.items()
    }
    setup_ledgers = {
        name: branch["evidence_ledger"][: len(prefix["evidence_ledger"]) + 2]
        for name, branch in branches.items()
    }
    native_revise = branches["native_revise"]
    fresh_revise = branches["fresh_revise"]
    u_native = native_revise["metrics"]["U_last"]
    u_fresh = fresh_revise["metrics"]["U_last"]
    trajectory_gap = (
        float(u_fresh - u_native)
        if u_native is not None and u_fresh is not None
        else None
    )
    gates = {
        **prefix_gates,
        "prefix_replay_exact_all": all(
            branch["prefix_replay_exact"] for branch in branches.values()
        ),
        "prefix_ledger_exact_all": all(
            branch["prefix_ledger_exact"] for branch in branches.values()
        ),
        "prefix_hash_exact_all": all(
            branch["prefix_evidence_hash"] == prefix["evidence_hash"]
            for branch in branches.values()
        ),
        "budget_before_audit_exact_all": all(
            abs(branch["budget_before_audit"] - prefix["budget_before_audit"])
            < 1e-12
            for branch in branches.values()
        ),
        "audit_requests_exact_all": all(
            requests == expected_requests for requests in audit_requests.values()
        ),
        "audit_action_equal_all": len(
            {json.dumps(value, sort_keys=True) for value in audit_requests.values()}
        )
        == 1,
        "audit_evidence_native_fresh_exact_within_pole": (
            native_revise["audit"]["frame_hashes"]
            == fresh_revise["audit"]["frame_hashes"]
            and branches["native_retain"]["audit"]["frame_hashes"]
            == branches["fresh_retain"]["audit"]["frame_hashes"]
        ),
        "audit_evidence_differs_between_poles": (
            native_revise["audit"]["frame_hashes"]
            != branches["native_retain"]["audit"]["frame_hashes"]
        ),
        "setup_ledgers_exact_within_pole": (
            setup_ledgers["native_revise"] == setup_ledgers["fresh_revise"]
            and setup_ledgers["native_retain"] == setup_ledgers["fresh_retain"]
        ),
        "audit_inspected_both_all": all(
            all(branch["inspection"].values()) for branch in branches.values()
        ),
        "no_post_audit_evidence_all": all(
            all(
                _evidence_requests(row["trajectory"])
                == (expected_requests if index == 0 else [])
                for index, row in enumerate(branch["trace"])
            )
            for branch in branches.values()
        ),
        "M_pre_hash_exact_all": all(
            branch["artifact_hashes"]["M_pre"] == prefix["M_pre_sha256"]
            for branch in branches.values()
        ),
        "M_first_recorded_all": all(
            branch["M_first"] is not None for branch in branches.values()
        ),
        "M_last_scoreable_all": all(
            branch["scores"]["M_last"].get("scoreable", False)
            for branch in branches.values()
        ),
        "accepted_submission_all": all(
            branch["accepted"] for branch in branches.values()
        ),
        "fresh_prompt_neutral_both": all(
            branches[name]["fresh_prompt_neutral"]
            for name in ("fresh_revise", "fresh_retain")
        ),
        "fresh_raw_archive_exact_both": all(
            branches[name]["raw_archive"]["exact"]
            for name in ("fresh_revise", "fresh_retain")
        ),
    }
    payload = {
        "kind": "exploratory_accelerated_lived_history_probe",
        "claim_class": "paired_lived_trajectory_vs_neutral_compact_state",
        "model": model,
        "seed_offset": seed_offset,
        "frozen_ficha": (
            "docs/research/2026-08-01-ficha-probe-pasado-acelerado-vivido-v0.md"
        ),
        "thresholds": {
            "belief_delta": args.belief_delta_threshold,
            "revise_U": 0.60,
            "revise_truth_error": 2.0,
            "retain_pre_error": 1.5,
            "retain_truth_error": 2.0,
            "south_preservation": 1.5,
            "trajectory_gap_for_replication": 0.25,
        },
        "certificate": certificate,
        "prefix": prefix,
        "branch_order": [name for name, _, _, _ in BRANCHES],
        "branches": branches,
        "contrast": {
            "U_native_revise": u_native,
            "U_fresh_revise": u_fresh,
            "trajectory_gap_fresh_minus_native": trajectory_gap,
            "trajectory_signal_for_replication": bool(
                trajectory_gap is not None
                and trajectory_gap >= 0.25
                and all(branch["accepted"] for branch in branches.values())
                and branches["native_retain"]["metrics"]["retain_correct"]
                and branches["fresh_retain"]["metrics"]["retain_correct"]
            ),
        },
        "audit_requests": audit_requests,
        "gates": gates,
        "all": all(gates.values()),
    }
    target.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(
        json.dumps(
            {
                "out": str(target),
                "all": payload["all"],
                "gates": gates,
                "abort": {
                    name: branch["abort"] for name, branch in branches.items()
                },
                "north_delta": {
                    name: {
                        checkpoint: branch["signatures"][
                            f"{checkpoint}_north"
                        ].get("delta_outcome_G_at_H5")
                        for checkpoint in ("M_pre", "M_first", "M_last")
                    }
                    for name, branch in branches.items()
                },
                "contrast": payload["contrast"],
            },
            indent=2,
        ),
        flush=True,
    )


if __name__ == "__main__":
    main()
