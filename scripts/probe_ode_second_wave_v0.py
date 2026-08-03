"""Paired real-agent discovery probe for parametric vs structural revision.

Default is zero-LLM certification.  A paid run requires ``--run-agent``.
One lived Line-A prefix is replayed exactly into RETAIN, PARAM and STRUCT;
only then is the routine Line-B report injected and each conversation resumed.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import sys
from pathlib import Path
from types import SimpleNamespace
from typing import Any

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from cases import ode_second_wave_v0_common as physics  # noqa: E402
from scripts.certify_ode_second_wave_v0 import (  # noqa: E402
    ARM_DIRS,
    run_certificates,
)
from scripts.probe_first_story_causal_fork import (  # noqa: E402
    SYSTEM,
    feedback,
    initial_prompt,
    record,
)
from scripts.probe_first_story_scm_fork import (  # noqa: E402
    _replay_checks_exact,
    replay_prefix_exact,
)
from wager.agent.cells import extract_cell  # noqa: E402
from wager.agent.llm_client import FoundryChat  # noqa: E402
from wager.contracts import Regime, SubmitResult  # noqa: E402
from wager.harness.case_episode import build_world_server  # noqa: E402
from wager.harness.kernel_proc import KernelClient  # noqa: E402
from wager.reward.sandbox import SandboxedSubmission, SandboxError  # noqa: E402

OUT = ROOT / "scripts" / "out" / "ode_second_wave_v0"
DEFAULT_MODEL = "gpt-5.4-mini"
MAX_COMPLETION_TOKENS = 5000
AGENT_CELL_TIMEOUT_S = 180.0
MIN_LONG_HORIZON = 16.0
MAX_A_MEAN_MAE = 12.0
MAX_TRANSFER_GAP = 6.0
MIN_MEANINGFUL_SECOND_PHASE_SHARE = 0.15
FIRST_CELL_REVIEW_ERROR = (
    "final handoff is unavailable until this notebook step completes; "
    "continue in the next turn using the returned cell output"
)


class FirstCellSubmitGate:
    """Force one real turn to see report-analysis stdout before handoff."""

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
            "submit", {"accepted": False}, 0.0, note=FIRST_CELL_REVIEW_ERROR
        )
        return SubmitResult(accepted=False, error=FIRST_CELL_REVIEW_ERROR)

    def open_next_turn(self) -> None:
        self.locked = False


def _atomic_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(payload, indent=2, default=float) + "\n", encoding="utf-8")
    temporary.replace(path)


def _artifact_hash(code: str | None) -> str | None:
    return hashlib.sha256(code.encode("utf-8")).hexdigest()[:12] if code else None


def _feedback_from_row(row: dict[str, Any], server) -> str:
    result = SimpleNamespace(
        ok=row["cell_result"]["ok"],
        stdout=row["cell_result"].get("stdout") or "",
        error=row["cell_result"].get("error"),
    )
    return feedback(result, server)


def _trajectory_has_long_experiment(trace: list[dict[str, Any]]) -> bool:
    for row in trace:
        for event in row.get("trajectory", []):
            if event.get("verb") != "experiment":
                continue
            grid = event.get("args", {}).get("context", {}).get("t_grid") or ()
            if grid and max(float(value) for value in grid) >= MIN_LONG_HORIZON:
                return True
    return False


def _effective_phase_count(signature: dict[str, Any]) -> int | None:
    """Ignore numerically fitted second phases too small to express the target pivot."""
    selected = signature.get("phases_selected")
    if selected != 2:
        return selected
    share = signature.get("second_wave_share_2p")
    return 2 if share is not None and share >= MIN_MEANINGFUL_SECOND_PHASE_SHARE else 1


def artifact_metrics(code: str | None, arm: str, *, seed: int) -> dict[str, Any]:
    if not code:
        return {"scoreable": False, "error": "missing artifact", "hash": None}
    server = build_world_server(ARM_DIRS[arm])
    grid = physics.REPORT_GRID
    regimes = {
        line: Regime(config={}, context={"line": line, "t_grid": grid}, horizon=None)
        for line in ("A", "B")
    }
    try:
        predictions = {}
        with SandboxedSubmission(code, server.columns, timeout_s=20.0) as submission:
            for index, (line, regime) in enumerate(regimes.items()):
                predictions[line] = submission.run(regime, 240, seed + index)
        means = {
            line: frame.groupby("t", sort=False)["y"].mean().to_numpy(dtype=float)
            for line, frame in predictions.items()
        }
        truths = {
            line: physics.mean_curve(arm, line, grid, n=6000, seed=seed + 100 + index)
            for index, line in enumerate(("A", "B"))
        }
        phase = physics.model_phase_signature(predictions["B"])
        return {
            "scoreable": True,
            "error": None,
            "hash": _artifact_hash(code),
            "phase_signature_B": phase,
            "effective_phases_B": _effective_phase_count(phase),
            "mean_mae_A": float(np.mean(np.abs(means["A"] - truths["A"]))),
            "mean_mae_B": float(np.mean(np.abs(means["B"] - truths["B"]))),
            "predicted_A_vs_B_mean_gap": float(np.mean(np.abs(means["A"] - means["B"]))),
            "predicted_B_curve": [float(value) for value in means["B"]],
        }
    except (SandboxError, ValueError, KeyError, RuntimeError) as exc:
        return {"scoreable": False, "error": repr(exc), "hash": _artifact_hash(code)}


def _eligibility(code: str | None, trace: list[dict[str, Any]], *, seed: int) -> dict[str, Any]:
    metrics = artifact_metrics(code, "retain", seed=seed)
    phase = metrics.get("phase_signature_B", {})
    checks = {
        "artifact_scoreable": bool(metrics.get("scoreable")),
        "long_A_experiment_seen": _trajectory_has_long_experiment(trace),
        "A_mean_competent": bool(
            metrics.get("scoreable") and metrics.get("mean_mae_A", np.inf) <= MAX_A_MEAN_MAE
        ),
        "B_transfers_A": bool(
            metrics.get("scoreable")
            and metrics.get("predicted_A_vs_B_mean_gap", np.inf) <= MAX_TRANSFER_GAP
        ),
        "Mpre_is_one_phase": _effective_phase_count(phase) == 1,
    }
    return {"checks": checks, "metrics": metrics, "eligible": all(checks.values())}


def form_prefix(
    model: str,
    seed_offset: int,
    max_prefix_turns: int,
    *,
    two_step_review: bool = False,
) -> dict[str, Any]:
    server = build_world_server(ARM_DIRS["retain"], seed_offset=seed_offset)
    chat = FoundryChat(system=SYSTEM, model=model, max_completion_tokens=MAX_COMPLETION_TOKENS)
    prompt = initial_prompt(server)
    if two_step_review:
        prompt += (
            "\n\nNotebook handoff protocol: after any scheduled workspace attachment, "
            "final handoff unlocks on the following notebook turn. Use the first "
            "turn to perform ordinary analysis; its returned output will be available "
            "before handoff."
        )
    trace: list[dict[str, Any]] = []
    abort = "max_prefix_turns"
    eligibility = None

    with KernelClient(server, cell_timeout_s=AGENT_CELL_TIMEOUT_S) as kernel:
        for turn in range(1, max_prefix_turns + 1):
            notices = server.begin_turn(turn, fire_events=False)
            reply = chat.ask(prompt)
            cell = extract_cell(reply.content)
            if cell is None:
                abort = "no_cell"
                break
            start = len(server.trajectory)
            result = kernel.run_cell(cell)
            row = record(turn, reply.content, cell, result, server, notices, start)
            row["phase"] = "line_A_prefix"
            trace.append(row)
            eligibility = _eligibility(result.working_model, trace, seed=950000 + seed_offset)
            if eligibility["eligible"]:
                abort = "eligible_Mpre_formed"
                break
            if result.error and result.error.startswith("cell exceeded "):
                abort = "cell_timeout"
                break
            prompt = feedback(result, server)

    mpre = next(
        (row["working_model"]["code"] for row in reversed(trace) if row["working_model"]["code"]),
        None,
    )
    if eligibility is None or eligibility["metrics"].get("hash") != _artifact_hash(mpre):
        eligibility = _eligibility(mpre, trace, seed=950000 + seed_offset)
    return {
        "abort": abort,
        "trace": trace,
        "messages": copy.deepcopy(chat.messages),
        "next_prompt": _feedback_from_row(trace[-1], server) if trace else prompt,
        "Mpre": mpre,
        "Mpre_hash": _artifact_hash(mpre),
        "eligibility": eligibility,
        "evidence_ledger": server.export_evidence_ledger(),
        "tokens": chat.usage.total_tokens,
        "turn_usage": [turn.__dict__ for turn in chat.turns],
    }


def run_branch(
    arm: str,
    prefix: dict[str, Any],
    model: str,
    seed_offset: int,
    max_total_turns: int,
    *,
    two_step_review: bool = False,
) -> dict[str, Any]:
    server = build_world_server(ARM_DIRS[arm], seed_offset=seed_offset)
    trace: list[dict[str, Any]] = []
    event_turn = len(prefix["trace"]) + 1
    mpre = prefix["Mpre"]
    abort = "max_turns"

    with KernelClient(server, cell_timeout_s=AGENT_CELL_TIMEOUT_S) as kernel:
        replay_checks = replay_prefix_exact(server, prefix, kernel)
        prefix_ledger_exact = server.export_evidence_ledger() == prefix["evidence_ledger"]
        server.begin_turn(event_turn, fire_events=False)
        notices = server.fire_event(0, turn_idx=event_turn)
        deliveries = server.pop_deliveries()
        delivered = []
        for variable, frame in deliveries:
            kernel.inject_dataframe(variable, frame)
            delivered.append({"variable": variable, "rows": len(frame), "columns": list(frame.columns)})
        submit_gate = FirstCellSubmitGate(server) if two_step_review else None
        chat = FoundryChat(system=None, model=model, max_completion_tokens=MAX_COMPLETION_TOKENS)
        chat.messages = copy.deepcopy(prefix["messages"])
        variable_note = "; ".join(row["variable"] for row in delivered)
        prompt = (
            "\n".join(f"[NOTICE] {notice}" for notice in notices)
            + f"\nWorkspace attachment: {variable_note}.\n\n"
            + prefix["next_prompt"]
        )
        for turn in range(event_turn, max_total_turns + 1):
            if turn > event_turn:
                notices = server.begin_turn(turn, fire_events=False)
            reply = chat.ask(prompt)
            cell = extract_cell(reply.content)
            if cell is None:
                abort = "no_cell"
                break
            start = len(server.trajectory)
            result = kernel.run_cell(cell)
            row = record(turn, reply.content, cell, result, server, notices, start)
            row["phase"] = "post_commissioning"
            if submit_gate is not None and not trace:
                row["first_cell_submit_gate"] = {
                    "rejected_attempts": submit_gate.rejected_attempts,
                    "terminal_after_cell": server.terminal,
                }
                submit_gate.open_next_turn()
            trace.append(row)
            if server.terminal:
                abort = "submitted"
                break
            if result.error and result.error.startswith("cell exceeded "):
                abort = "cell_timeout"
                break
            prompt = feedback(result, server)

    codes = [
        row["working_model"]["code"]
        for row in trace
        if row["working_model"]["code"]
    ]
    mpost = next((code for code in codes if code != mpre), None)
    final = (server.result or {}).get("code") or (codes[-1] if codes else mpre)
    pre_metrics = artifact_metrics(mpre, arm, seed=960000 + seed_offset)
    post_metrics = artifact_metrics(mpost, arm, seed=961000 + seed_offset)
    final_metrics = artifact_metrics(final, arm, seed=962000 + seed_offset)
    pre_error = pre_metrics.get("mean_mae_B")
    final_error = final_metrics.get("mean_mae_B")
    captured = None
    if pre_error is not None and final_error is not None and pre_error > 1e-9:
        captured = float(1.0 - final_error / pre_error)
    return {
        "arm": arm,
        "case_id": server.case_id,
        "replay_checks": replay_checks,
        "replay_exact": _replay_checks_exact(replay_checks),
        "prefix_ledger_exact": prefix_ledger_exact,
        "event_turn": event_turn,
        "two_step_review": two_step_review,
        "review_gate_rejected_attempts": (
            submit_gate.rejected_attempts if submit_gate is not None else 0
        ),
        "deliveries": delivered,
        "abort": abort,
        "accepted": server.terminal,
        "R": (server.result or {}).get("R"),
        "Mpre": mpre,
        "Mpost": mpost,
        "Mfinal": final,
        "Mpre_hash": _artifact_hash(mpre),
        "Mpost_hash": _artifact_hash(mpost),
        "Mfinal_hash": _artifact_hash(final),
        "metrics": {"pre": pre_metrics, "post": post_metrics, "final": final_metrics},
        "fraction_B_mean_error_removed": captured,
        "report_variable_referenced": any(
            "line_b_commissioning_report" in (row.get("cell") or "") for row in trace
        ),
        "trace": trace,
        "messages": copy.deepcopy(chat.messages),
        "tokens": chat.usage.total_tokens,
        "turn_usage": [turn.__dict__ for turn in chat.turns],
    }


def _restore_protocol_tuples(prefix: dict[str, Any]) -> dict[str, Any]:
    """Undo only JSON's tuple->list conversion for exact replay comparisons."""
    restored = copy.deepcopy(prefix)
    for row in restored.get("trace", []):
        for event in row.get("trajectory", []):
            context = event.get("args", {}).get("context", {})
            if isinstance(context.get("t_grid"), list):
                context["t_grid"] = tuple(context["t_grid"])
    for evidence in restored.get("evidence_ledger", []):
        context = evidence.get("request", {}).get("context", {})
        if isinstance(context.get("t_grid"), list):
            context["t_grid"] = tuple(context["t_grid"])
    return restored


def replay_frozen_timeout_cell(
    arm: str,
    prefix: dict[str, Any],
    frozen_row: dict[str, Any],
    seed_offset: int,
    *,
    cell_timeout_s: float,
) -> dict[str, Any]:
    """Recover a purely technical timeout without sampling another LLM action."""
    server = build_world_server(ARM_DIRS[arm], seed_offset=seed_offset)
    event_turn = len(prefix["trace"]) + 1
    with KernelClient(server, cell_timeout_s=cell_timeout_s) as kernel:
        replay_checks = replay_prefix_exact(server, prefix, kernel)
        prefix_ledger_exact = server.export_evidence_ledger() == prefix["evidence_ledger"]
        server.begin_turn(event_turn, fire_events=False)
        notices = server.fire_event(0, turn_idx=event_turn)
        deliveries = server.pop_deliveries()
        for variable, frame in deliveries:
            kernel.inject_dataframe(variable, frame)
        start = len(server.trajectory)
        result = kernel.run_cell(frozen_row["cell"])
        recovered_row = record(
            event_turn,
            frozen_row["reply_text"],
            frozen_row["cell"],
            result,
            server,
            notices,
            start,
        )
    code = (server.result or {}).get("code") or result.working_model or prefix["Mpre"]
    return {
        "kind": "ode_second_wave_frozen_timeout_recovery",
        "arm": arm,
        "seed_offset": seed_offset,
        "cell_timeout_s": cell_timeout_s,
        "no_new_llm_call": True,
        "replay_checks": replay_checks,
        "replay_exact": _replay_checks_exact(replay_checks),
        "prefix_ledger_exact": prefix_ledger_exact,
        "notices_exact": notices == frozen_row.get("notices"),
        "delivery_variables": [variable for variable, _ in deliveries],
        "cell_sha256": hashlib.sha256(frozen_row["cell"].encode("utf-8")).hexdigest(),
        "cell_result": recovered_row,
        "accepted": server.terminal,
        "R": (server.result or {}).get("R"),
        "Mfinal": code,
        "Mfinal_hash": _artifact_hash(code),
        "metrics_final": artifact_metrics(code, arm, seed=963000 + seed_offset),
    }


def run_frozen_struct_adequacy_control(
    source: dict[str, Any],
    *,
    max_continuation_turns: int,
    cell_timeout_s: float,
    plain_output_review: bool = False,
) -> dict[str, Any]:
    """Same frozen first action, then either plain output or adequacy review."""
    arm = "struct"
    seed_offset = int(source["seed_offset"])
    prefix = _restore_protocol_tuples(source["prefix"])
    frozen = source["branches"][arm]["trace"][0]
    server = build_world_server(ARM_DIRS[arm], seed_offset=seed_offset)
    event_turn = len(prefix["trace"]) + 1
    control_prompt = "" if plain_output_review else (
        "Before final handoff, evaluate whether the fitted model family is an "
        "adequate description of the returned record. Preserve it if it is "
        "adequate; revise it only if the record warrants it."
    )
    trace: list[dict[str, Any]] = []
    abort = "max_turns"

    with KernelClient(server, cell_timeout_s=cell_timeout_s) as kernel:
        replay_checks = replay_prefix_exact(server, prefix, kernel)
        prefix_ledger_exact = server.export_evidence_ledger() == prefix["evidence_ledger"]
        server.begin_turn(event_turn, fire_events=False)
        notices = server.fire_event(0, turn_idx=event_turn)
        deliveries = server.pop_deliveries()
        for variable, frame in deliveries:
            kernel.inject_dataframe(variable, frame)

        gate = FirstCellSubmitGate(server)
        start = len(server.trajectory)
        first_result = kernel.run_cell(frozen["cell"])
        first_row = record(
            event_turn,
            frozen["reply_text"],
            frozen["cell"],
            first_result,
            server,
            notices,
            start,
        )
        first_row["phase"] = "frozen_first_post_report_cell"
        first_row["submit_gate"] = {
            "rejected_attempts": gate.rejected_attempts,
            "terminal_after_cell": server.terminal,
        }
        trace.append(first_row)
        gate.open_next_turn()

        chat = FoundryChat(
            system=None,
            model=source["model"],
            max_completion_tokens=MAX_COMPLETION_TOKENS,
        )
        chat.messages = copy.deepcopy(source["branches"][arm]["messages"])
        prompt = feedback(first_result, server)
        if control_prompt:
            prompt += "\n\n" + control_prompt
        for turn in range(event_turn + 1, event_turn + 1 + max_continuation_turns):
            reply = chat.ask(prompt)
            cell = extract_cell(reply.content)
            if cell is None:
                abort = "no_cell"
                break
            start = len(server.trajectory)
            result = kernel.run_cell(cell)
            row = record(turn, reply.content, cell, result, server, [], start)
            row["phase"] = "generic_adequacy_review"
            trace.append(row)
            if server.terminal:
                abort = "submitted"
                break
            if result.error and result.error.startswith("cell exceeded "):
                abort = "cell_timeout"
                break
            prompt = feedback(result, server)

    codes = [row["working_model"]["code"] for row in trace if row["working_model"]["code"]]
    final = (server.result or {}).get("code") or (codes[-1] if codes else prefix["Mpre"])
    return {
        "kind": (
            "ode_second_wave_struct_plain_output_review"
            if plain_output_review
            else "ode_second_wave_struct_generic_adequacy_control"
        ),
        "claim_scope": (
            "same prefix, report and frozen first action; no added review instruction"
            if plain_output_review
            else "same prefix, report and frozen first action; one generic adequacy review"
        ),
        "model": source["model"],
        "seed_offset": seed_offset,
        "source_raw": source.get("raw_path"),
        "control_prompt": control_prompt,
        "replay_checks": replay_checks,
        "replay_exact": _replay_checks_exact(replay_checks),
        "prefix_ledger_exact": prefix_ledger_exact,
        "frozen_cell_sha256": hashlib.sha256(frozen["cell"].encode("utf-8")).hexdigest(),
        "frozen_cell_matches_source": frozen["cell"] == source["branches"][arm]["trace"][0]["cell"],
        "first_submit_rejected": gate.rejected_attempts == 1 and not first_row["submit_gate"]["terminal_after_cell"],
        "abort": abort,
        "accepted": server.terminal,
        "R": (server.result or {}).get("R"),
        "Mfirst": first_result.working_model,
        "Mfinal": final,
        "Mfirst_hash": _artifact_hash(first_result.working_model),
        "Mfinal_hash": _artifact_hash(final),
        "metrics_first": artifact_metrics(first_result.working_model, arm, seed=964000 + seed_offset),
        "metrics_final": artifact_metrics(final, arm, seed=965000 + seed_offset),
        "trace": trace,
        "messages": copy.deepcopy(chat.messages),
        "tokens": chat.usage.total_tokens,
        "turn_usage": [turn.__dict__ for turn in chat.turns],
    }


def run_agent(
    model: str,
    seed_offset: int,
    max_prefix_turns: int,
    max_total_turns: int,
    *,
    two_step_review: bool = False,
) -> dict:
    certificate = run_certificates(seed_offset)
    payload: dict[str, Any] = {
        "kind": (
            "exploratory_ode_second_wave_two_step_v1"
            if two_step_review
            else "exploratory_ode_second_wave_v0"
        ),
        "claim_scope": (
            "fresh-seed procedural-closure diagnostic; not confirmation or prevalence"
            if two_step_review
            else "late structural surprise discovery probe; not prevalence"
        ),
        "model": model,
        "seed_offset": seed_offset,
        "two_step_review": two_step_review,
        "certificate": certificate,
        "stage": "certificate",
    }
    if not certificate["all"]:
        payload["abort"] = "certificate_failed"
        return payload
    prefix = form_prefix(
        model,
        seed_offset,
        max_prefix_turns,
        two_step_review=two_step_review,
    )
    payload.update({"prefix": prefix, "stage": "prefix"})
    suffix = "_twostep" if two_step_review else ""
    out_path = OUT / f"raw_{model.replace('/', '_')}_seed{seed_offset}{suffix}.json"
    _atomic_json(out_path, payload)
    if not prefix["eligibility"]["eligible"]:
        payload["abort"] = "Mpre_ineligible"
        _atomic_json(out_path, payload)
        return payload
    branches = {}
    for arm in physics.ARMS:
        branches[arm] = run_branch(
            arm,
            prefix,
            model,
            seed_offset,
            max_total_turns,
            two_step_review=two_step_review,
        )
        payload.update({"branches": branches, "stage": f"branch_{arm}"})
        _atomic_json(out_path, payload)
    payload.update({
        "stage": "complete",
        "abort": None,
        "all_replays_exact": all(branch["replay_exact"] for branch in branches.values()),
        "raw_path": str(out_path),
    })
    _atomic_json(out_path, payload)
    return payload


def _print_summary(payload: dict[str, Any]) -> None:
    print(f"stage={payload.get('stage')} abort={payload.get('abort')}")
    prefix = payload.get("prefix")
    if prefix:
        print(f"Mpre eligible={prefix['eligibility']['eligible']} checks={prefix['eligibility']['checks']}")
    for arm, branch in (payload.get("branches") or {}).items():
        final_phase = branch["metrics"]["final"].get("effective_phases_B")
        print(
            f"{arm:6s} replay={branch['replay_exact']} accepted={branch['accepted']} "
            f"R={branch['R']} phase_B={final_phase} "
            f"Fmean={branch['fraction_B_mean_error_removed']} abort={branch['abort']}"
        )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--run-agent", action="store_true", help="perform real Foundry calls")
    parser.add_argument("--model", default=DEFAULT_MODEL)
    parser.add_argument("--seed-offset", type=int, default=0)
    parser.add_argument("--max-prefix-turns", type=int, default=6)
    parser.add_argument("--max-total-turns", type=int, default=12)
    parser.add_argument(
        "--two-step-review",
        action="store_true",
        help="block first post-report handoff identically in all arms",
    )
    parser.add_argument(
        "--resume-frozen-retain",
        type=Path,
        help="raw completed run whose timed-out RETAIN cell is replayed verbatim",
    )
    parser.add_argument("--cell-timeout-s", type=float, default=120.0)
    parser.add_argument(
        "--control-frozen-struct",
        type=Path,
        help="run the single generic-adequacy control from a completed raw run",
    )
    parser.add_argument(
        "--control-frozen-struct-plain",
        type=Path,
        help="replay frozen STRUCT action and allow a plain output-review turn",
    )
    args = parser.parse_args()
    if args.resume_frozen_retain is not None:
        source = json.loads(args.resume_frozen_retain.read_text(encoding="utf-8"))
        frozen = source["branches"]["retain"]["trace"][0]
        recovered = replay_frozen_timeout_cell(
            "retain",
            source["prefix"],
            frozen,
            int(source["seed_offset"]),
            cell_timeout_s=args.cell_timeout_s,
        )
        target = OUT / (
            f"frozen_recovery_retain_{str(source['model']).replace('/', '_')}_"
            f"seed{source['seed_offset']}.json"
        )
        _atomic_json(target, recovered)
        print(
            f"retain frozen recovery: replay={recovered['replay_exact']} "
            f"accepted={recovered['accepted']} R={recovered['R']} -> {target}"
        )
        return 0 if recovered["accepted"] else 2
    if args.control_frozen_struct is not None:
        source = json.loads(args.control_frozen_struct.read_text(encoding="utf-8"))
        controlled = run_frozen_struct_adequacy_control(
            source,
            max_continuation_turns=3,
            cell_timeout_s=args.cell_timeout_s,
        )
        target = OUT / (
            f"control_struct_adequacy_{str(source['model']).replace('/', '_')}_"
            f"seed{source['seed_offset']}.json"
        )
        _atomic_json(target, controlled)
        phase = controlled["metrics_final"].get("phase_signature_B", {}).get(
            "phases_selected"
        )
        print(
            f"STRUCT adequacy control: replay={controlled['replay_exact']} "
            f"accepted={controlled['accepted']} R={controlled['R']} "
            f"phase_B={phase} -> {target}"
        )
        return 0 if controlled["accepted"] else 2
    if args.control_frozen_struct_plain is not None:
        source = json.loads(args.control_frozen_struct_plain.read_text(encoding="utf-8"))
        controlled = run_frozen_struct_adequacy_control(
            source,
            max_continuation_turns=3,
            cell_timeout_s=args.cell_timeout_s,
            plain_output_review=True,
        )
        target = OUT / (
            f"control_struct_plain_{str(source['model']).replace('/', '_')}_"
            f"seed{source['seed_offset']}.json"
        )
        _atomic_json(target, controlled)
        phase = controlled["metrics_final"].get("effective_phases_B")
        print(
            f"STRUCT plain-output control: replay={controlled['replay_exact']} "
            f"accepted={controlled['accepted']} R={controlled['R']} "
            f"phase_B={phase} -> {target}"
        )
        return 0 if controlled["accepted"] else 2
    if not args.run_agent:
        certificate = run_certificates(args.seed_offset)
        print("ALL GATES PASS" if certificate["all"] else "CERTIFICATE FAILED")
        return 0 if certificate["all"] else 1
    payload = run_agent(
        args.model,
        args.seed_offset,
        args.max_prefix_turns,
        args.max_total_turns,
        two_step_review=args.two_step_review,
    )
    _print_summary(payload)
    return 0 if payload.get("stage") == "complete" else 2


if __name__ == "__main__":
    sys.exit(main())
