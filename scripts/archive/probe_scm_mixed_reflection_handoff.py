"""Contrast native reflection with a fresh, data-only handoff on MIXED.

This exploratory runner consumes a persisted three-pole donor.  It does not
generate new evidence: both modes reconstruct the donor's exact MIXED evidence
and remaining budget.  ``native_reflection`` keeps the original conversation
and live workspace; ``fresh_data_only`` starts a new conversation and kernel
containing only neutrally named raw campaign frames plus a manifest.
"""

from __future__ import annotations

import argparse
import ast
import copy
import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from wager.agent.cells import extract_cell  # noqa: E402
from wager.agent.llm_client import FoundryChat  # noqa: E402
from wager.contracts import ExperimentDesign  # noqa: E402
from wager.harness.case_episode import build_world_server  # noqa: E402
from wager.harness.episode import (  # noqa: E402
    CELL_TIMEOUT_S,
    MAX_COMPLETION_TOKENS,
)
from wager.harness.kernel_proc import KernelClient  # noqa: E402

from scripts.analyze_first_story_scm_transfer_mixed import (  # noqa: E402
    _model_draws,
    _site_metrics,
)
from scripts.probe_first_story_causal_fork import record  # noqa: E402
from scripts.probe_first_story_scm_fork import (  # noqa: E402
    _replay_checks_exact,
    replay_prefix_exact,
)
from scripts.probe_first_story_scm_transfer_fork import (  # noqa: E402
    MIXED,
    SYSTEM,
    feedback,
)

DEFAULT_OUT = ROOT / "scripts" / "out" / "first_story_scm_transfer_fork"
MODES = (
    "native_reflection",
    "fresh_data_only",
    "fresh_generic_check",
    "fresh_declared_family",
    "fresh_declared_mixture_laws",
)
_DECLARED_FAMILY_NOTE = (
    " Domain documentation permits either one response law for all units at a "
    "site or a stable blend of unobserved operating modes. Unit membership is not "
    "recorded, and any mode laws and blend weight are unknown; infer them from the "
    "raw campaigns rather than assuming that either structure is present."
)
_DECLARED_MIXTURE_LAWS_NOTE = (
    " Domain documentation permits response modes with distinct coefficients "
    "for the advertised controls. If the data support a blend, represent it as "
    "a mixture over complete response laws rather than only as constant residual "
    "offsets. The number of modes, their laws and their weights remain unknown."
)
_NEUTRAL_SUBMIT_RESULT = ast.parse(
    "type('DeferredSubmitResult', (), {"
    "'accepted': False, 'error': None, "
    "'__repr__': lambda self: "
    "\"DeferredSubmitResult(accepted=False, error=None)\"})()",
    mode="eval",
).body
_FRESH_FORBIDDEN = re.compile(
    r"\b(mixed|mixture|anomaly|anomalous|correction|corrective)\b",
    re.IGNORECASE,
)


class _SubmitDeferrer(ast.NodeTransformer):
    def __init__(self) -> None:
        self.count = 0

    def visit_Call(self, node: ast.Call) -> ast.AST:
        if (
            isinstance(node.func, ast.Attribute)
            and node.func.attr == "submit"
            and isinstance(node.func.value, ast.Name)
            and node.func.value.id == "env"
        ):
            self.count += 1
            return ast.copy_location(copy.deepcopy(_NEUTRAL_SUBMIT_RESULT), node)
        return self.generic_visit(node)


def _defer_submits(cell: str) -> tuple[str, int]:
    tree = ast.parse(cell)
    transformer = _SubmitDeferrer()
    transformed = transformer.visit(tree)
    ast.fix_missing_locations(transformed)
    return ast.unparse(transformed), transformer.count


def _env_calls(cell: str) -> list[str]:
    try:
        tree = ast.parse(cell)
    except SyntaxError:
        return ["unparseable"]
    return [
        node.func.attr
        for node in ast.walk(tree)
        if isinstance(node, ast.Call)
        and isinstance(node.func, ast.Attribute)
        and isinstance(node.func.value, ast.Name)
        and node.func.value.id == "env"
    ]


def _frame_from_ledger(row: dict) -> pd.DataFrame:
    blob = row["data"]
    frame = pd.DataFrame(blob["data"], columns=blob["columns"])
    for column, dtype in zip(blob["columns"], blob["dtypes"]):
        frame[column] = frame[column].astype(dtype)
    return frame


def _frame_hash(frame: pd.DataFrame) -> str:
    digest = hashlib.sha256()
    digest.update(json.dumps(list(frame.columns)).encode("utf-8"))
    digest.update(json.dumps([str(dtype) for dtype in frame.dtypes]).encode("utf-8"))
    values = pd.util.hash_pandas_object(frame, index=True).to_numpy(np.uint64)
    digest.update(values.tobytes())
    return digest.hexdigest()


def _ledger_hash(ledger: list[dict]) -> str:
    payload = json.dumps(
        ledger,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    )
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def _trajectory_requests(events: list[dict]) -> list[dict]:
    return [
        {"verb": event["verb"], "args": event["args"], "cost": event["cost"]}
        for event in events
        if event["verb"] in {"observe", "experiment"}
    ]


def _native_messages_through_action(donor: dict) -> list[dict]:
    action_text = donor["prefix"]["selection"]["reply_text"]
    transcript = donor["branches"]["mixed"].get("transcript") or []
    for index, message in enumerate(transcript):
        if message.get("role") == "assistant" and message.get("content") == action_text:
            return copy.deepcopy(transcript[: index + 1])
    raise ValueError("MIXED transcript does not contain the frozen action reply")


def _chat_usage(chat: FoundryChat) -> dict:
    return {
        "tokens": chat.usage.total_tokens,
        "turns": [
            {
                "prompt_tokens": turn.prompt_tokens,
                "completion_tokens": turn.completion_tokens,
                "reasoning_tokens": turn.reasoning_tokens,
                "latency_s": turn.latency_s,
            }
            for turn in chat.turns
        ],
    }


def _last_code(server, trace: list[dict], fallback: str | None = None) -> str | None:
    result = server.result or {}
    if result.get("code"):
        return result["code"]
    return next(
        (
            row["working_model"]["code"]
            for row in reversed(trace)
            if row["working_model"]["code"]
        ),
        fallback,
    )


def _metrics(code: str | None, columns: list[str], *, seed: int) -> dict:
    if not code:
        return {"scoreable": False, "error": "missing artifact"}
    try:
        draws = _model_draws(code, columns, n_samples=4000, seed=seed)
        sites = {site: _site_metrics(site_draws) for site, site_draws in draws.items()}
        return {
            "scoreable": True,
            "south_delta": sites["south"]["delta_mean_G7_minus_G3"],
            "north_delta": sites["north"]["delta_mean_G7_minus_G3"],
            "north_oriented_skew_A3": sites["north"]["oriented_skew_A3"],
            "north_normal_shape_gap": sites["north"]["normal_shape_gap"],
            "sites": sites,
        }
    except Exception as exc:  # exploratory raw must preserve failures
        return {"scoreable": False, "error": repr(exc)}


def _run_continuation(
    *,
    server,
    kernel: KernelClient,
    chat: FoundryChat,
    prompt: str,
    first_turn: int,
    max_turns: int,
    phase: str,
    defer_first_submit: bool = False,
) -> tuple[list[dict], str, dict]:
    trace: list[dict] = []
    abort = "max_turns"
    first_protocol = {
        "required": defer_first_submit,
        "original_env_calls": None,
        "original_had_submit": None,
        "only_local_or_describe": None,
        "submit_was_deferred": False,
    }
    for offset in range(max_turns):
        if server.terminal:
            abort = "submitted"
            break
        turn = first_turn + offset
        notices = server.begin_turn(turn)
        for variable, frame in server.pop_deliveries():
            kernel.inject_dataframe(variable, frame)
        reply = chat.ask(prompt)
        original_cell = extract_cell(reply.content)
        if original_cell is None:
            abort = "no_cell"
            break

        executed_cell = original_cell
        deferred_count = 0
        if defer_first_submit and offset == 0:
            calls = _env_calls(original_cell)
            first_protocol.update(
                {
                    "original_env_calls": calls,
                    "original_had_submit": "submit" in calls,
                    "only_local_or_describe": all(call == "describe" for call in calls),
                }
            )
            executed_cell, deferred_count = _defer_submits(original_cell)
            first_protocol["submit_was_deferred"] = deferred_count > 0

        start = len(server.trajectory)
        result = kernel.run_cell(executed_cell)
        row = record(
            turn,
            reply.content,
            executed_cell,
            result,
            server,
            notices,
            start,
        )
        row.update(
            {
                "phase": phase,
                "original_cell": original_cell,
                "executed_cell": executed_cell,
                "deferred_submit_calls": deferred_count,
            }
        )
        trace.append(row)
        if server.terminal:
            abort = "submitted"
            break
        if result.error and result.error.startswith("cell exceeded "):
            abort = "cell_timeout"
            break
        prompt = feedback(result, server)
    return trace, abort, first_protocol


def _run_native(
    donor: dict,
    *,
    model: str,
    seed_offset: int,
    max_turns: int,
) -> dict:
    prefix = donor["prefix"]
    action = prefix["selection"]
    expected_requests = _trajectory_requests(action["preflight_action_trajectory"])
    expected_ledger = donor["branches"]["mixed"]["ledger_after_action"]
    expected_action_model = donor["branches"]["mixed"]["trace"][0][
        "working_model"
    ]["code"]
    server = build_world_server(MIXED, seed_offset=seed_offset)
    trace: list[dict] = []

    with KernelClient(server, cell_timeout_s=CELL_TIMEOUT_S) as kernel:
        replay_checks = replay_prefix_exact(server, prefix, kernel)
        prefix_ledger = server.export_evidence_ledger()
        notices = server.begin_turn(action["turn"])
        for variable, frame in server.pop_deliveries():
            kernel.inject_dataframe(variable, frame)
        executed_action, deferred_count = _defer_submits(action["cell"])
        start = len(server.trajectory)
        action_result = kernel.run_cell(executed_action)
        action_row = record(
            action["turn"],
            action["reply_text"],
            executed_action,
            action_result,
            server,
            notices,
            start,
        )
        action_row.update(
            {
                "phase": "frozen_action_submit_deferred",
                "original_cell": action["cell"],
                "executed_cell": executed_action,
                "deferred_submit_calls": deferred_count,
            }
        )
        trace.append(action_row)
        action_ledger = server.export_evidence_ledger()
        action_requests = _trajectory_requests(action_row["trajectory"])
        budget_after_action = float(server.budget_remaining)

        chat = FoundryChat(
            system=SYSTEM,
            model=model,
            max_completion_tokens=MAX_COMPLETION_TOKENS,
        )
        chat.messages = _native_messages_through_action(donor)
        continuation, abort, _ = _run_continuation(
            server=server,
            kernel=kernel,
            chat=chat,
            prompt=feedback(action_result, server),
            first_turn=action["turn"] + 1,
            max_turns=max_turns,
            phase="native_reflection",
        )
        trace.extend(continuation)
        transcript = copy.deepcopy(chat.messages)
        usage = _chat_usage(chat)

    action_model = action_result.working_model
    final_code = _last_code(server, trace, action_model)
    gates = {
        "prefix_replay_exact": _replay_checks_exact(replay_checks),
        "prefix_ledger_exact": prefix_ledger == prefix["evidence_ledger"],
        "action_notices_exact": notices == action["notices"],
        "submit_call_deferred": deferred_count > 0,
        "action_did_not_terminate": not action_row["trajectory"]
        or not any(event["verb"] == "submit" for event in action_row["trajectory"]),
        "action_requests_exact": action_requests == expected_requests,
        "action_evidence_ledger_exact": action_ledger == expected_ledger,
        "action_working_model_exact": action_model == expected_action_model,
        "budget_after_action_exact": abs(
            budget_after_action
            - float(donor["branches"]["mixed"]["trace"][0]["budget_remaining"])
        )
        < 1e-12,
    }
    return {
        "mode": "native_reflection",
        "mechanical_gates": gates,
        "mechanical_all": all(gates.values()),
        "replay_checks": replay_checks,
        "action_requests": action_requests,
        "action_evidence_ledger": action_ledger,
        "action_evidence_hash": _ledger_hash(action_ledger),
        "budget_after_setup": budget_after_action,
        "abort": abort,
        "accepted": server.terminal,
        "trace": trace,
        "transcript": transcript,
        "final_code": final_code,
        "metrics": {
            "M_pre": _metrics(
                action["M_pre"], server.columns, seed=seed_offset + 1_020_000
            ),
            "M_action": _metrics(
                action_model, server.columns, seed=seed_offset + 1_020_000
            ),
            "M_final": _metrics(
                final_code, server.columns, seed=seed_offset + 1_020_000
            ),
        },
        "usage": usage,
    }


def _replay_raw_evidence(server, ledger: list[dict]) -> tuple[list[pd.DataFrame], dict]:
    frames: list[pd.DataFrame] = []
    rows: list[dict] = []
    delivery_count = 0
    max_turn = max((int(row["turn"]) for row in ledger), default=0)
    by_turn: dict[int, list[dict]] = {}
    for row in ledger:
        by_turn.setdefault(int(row["turn"]), []).append(row)

    for turn in range(1, max_turn + 1):
        server.begin_turn(turn)
        delivery_count += len(server.pop_deliveries())
        for expected in by_turn.get(turn, []):
            request = expected["request"]
            if expected["kind"] == "observe":
                actual = server.observe(expected["source"], int(request["n"]))
            elif expected["kind"] == "experiment":
                actual = server.experiment(
                    ExperimentDesign(
                        config=dict(request.get("config", {})),
                        context=dict(request.get("context", {})),
                        n=int(request["n"]),
                        horizon=request.get("horizon"),
                    )
                )
            else:
                raise ValueError(f"unsupported evidence kind {expected['kind']!r}")
            persisted = _frame_from_ledger(expected)
            frames.append(actual.copy())
            rows.append(
                {
                    "sequence": expected["sequence"],
                    "turn": turn,
                    "kind": expected["kind"],
                    "expected_hash": _frame_hash(persisted),
                    "actual_hash": _frame_hash(actual),
                    "frame_exact": actual.equals(persisted),
                }
            )
    replayed_ledger = server.export_evidence_ledger()
    return frames, {
        "rows": rows,
        "all_frames_exact": all(row["frame_exact"] for row in rows),
        "all_hashes_exact": all(
            row["expected_hash"] == row["actual_hash"] for row in rows
        ),
        "no_scheduled_deliveries": delivery_count == 0,
        "ledger_exact": replayed_ledger == ledger,
        "ledger_hash": _ledger_hash(replayed_ledger),
    }


def _campaign_catalog(ledger: list[dict], *, flat: bool = False) -> pd.DataFrame:
    records = []
    for index, row in enumerate(ledger, start=1):
        request = row["request"]
        config = request.get("config") or {}
        site = (
            request.get("context", {}).get("site")
            if row["kind"] == "experiment"
            else "south"
        )
        record = {
            "sequence": int(row["sequence"]),
            "site": site,
            "config": json.dumps(config, sort_keys=True, separators=(",", ":")),
            "n": int(request["n"]),
            "name": f"campaign_{index:03d}",
        }
        if flat:
            record.update(
                {
                    "feedstock_grade_set": "feedstock_grade" in config,
                    "feedstock_grade": config.get("feedstock_grade", np.nan),
                    "humidity_set": "humidity" in config,
                    "humidity": config.get("humidity", np.nan),
                }
            )
        records.append(record)
    columns = ["sequence", "site", "config", "n", "name"]
    if flat:
        columns += [
            "feedstock_grade_set",
            "feedstock_grade",
            "humidity_set",
            "humidity",
        ]
    return pd.DataFrame(records, columns=columns)


def _fresh_prompt(
    server,
    catalog: pd.DataFrame,
    *,
    generic_model_check: bool = False,
    declared_family: bool = False,
    declared_mixture_laws: bool = False,
) -> str:
    sheet = server.describe()
    machine = {key: value for key, value in sheet.items() if key != "brief"}
    names = ", ".join(catalog["name"].tolist())
    prompt = (
        "Here is the assignment:\n\n"
        + sheet["brief"]
        + "\n\nMachine-readable sheet:\n"
        + json.dumps(machine, indent=2)
        + "\n\nYou are taking over this investigation. The raw campaigns are loaded "
        "in the live Python workspace as "
        + names
        + ", and `campaign_catalog` is their manifest. Complete an executable "
        "model from these materials. On your first reply, only inspect the raw "
        "frames and perform calculations; do not call env.submit. You may submit "
        "from the following reply onward."
    )
    if generic_model_check:
        prompt += (
            " Before final delivery, inspect residual patterns and test whether one "
            "parametric error distribution adequately describes every intervention "
            "condition; let the raw campaigns determine the model."
        )
    if declared_family:
        prompt += _DECLARED_FAMILY_NOTE
    if declared_mixture_laws:
        prompt += _DECLARED_FAMILY_NOTE + _DECLARED_MIXTURE_LAWS_NOTE
    return prompt


def _run_fresh_data_only(
    donor: dict,
    *,
    model: str,
    seed_offset: int,
    max_turns: int,
    generic_model_check: bool = False,
    declared_family: bool = False,
    declared_mixture_laws: bool = False,
    flat_catalog: bool = False,
) -> dict:
    action_turn = int(donor["prefix"]["selection"]["turn"])
    ledger = donor["branches"]["mixed"]["ledger_after_action"]
    expected_budget = float(
        donor["branches"]["mixed"]["trace"][0]["budget_remaining"]
    )
    server = build_world_server(MIXED, seed_offset=seed_offset)
    frames, replay = _replay_raw_evidence(server, ledger)
    setup_ledger = server.export_evidence_ledger()
    budget_after_replay = float(server.budget_remaining)
    catalog = _campaign_catalog(ledger, flat=flat_catalog)

    with KernelClient(server, cell_timeout_s=CELL_TIMEOUT_S) as kernel:
        for index, frame in enumerate(frames, start=1):
            kernel.inject_dataframe(f"campaign_{index:03d}", frame)
        kernel.inject_dataframe("campaign_catalog", catalog)
        prompt = _fresh_prompt(
            server,
            catalog,
            generic_model_check=generic_model_check,
            declared_family=declared_family,
            declared_mixture_laws=declared_mixture_laws,
        )
        chat = FoundryChat(
            system=SYSTEM,
            model=model,
            max_completion_tokens=MAX_COMPLETION_TOKENS,
        )
        trace, abort, first_protocol = _run_continuation(
            server=server,
            kernel=kernel,
            chat=chat,
            prompt=prompt,
            first_turn=action_turn + 1,
            max_turns=max_turns,
            phase=(
                "fresh_declared_mixture_laws"
                if declared_mixture_laws
                else (
                    "fresh_declared_family"
                    if declared_family
                    else (
                        "fresh_generic_check"
                        if generic_model_check
                        else "fresh_data_only"
                    )
                )
            ),
            defer_first_submit=True,
        )
        transcript = copy.deepcopy(chat.messages)
        usage = _chat_usage(chat)

    final_code = _last_code(server, trace)
    mechanical_gates = {
        "all_raw_frames_exact": replay["all_frames_exact"],
        "all_raw_hashes_exact": replay["all_hashes_exact"],
        "evidence_ledger_exact": replay["ledger_exact"],
        "no_scheduled_deliveries": replay["no_scheduled_deliveries"],
        "budget_after_replay_exact": abs(budget_after_replay - expected_budget)
        < 1e-12,
        "fresh_prompt_condition_valid": (
            _DECLARED_MIXTURE_LAWS_NOTE in prompt
            if declared_mixture_laws
            else _FRESH_FORBIDDEN.search(prompt) is None
            if not declared_family
            else _DECLARED_FAMILY_NOTE in prompt
        ),
        "campaign_count_exact": len(frames) == len(ledger) == len(catalog),
        "catalog_schema_exact": list(catalog.columns)
        == (
            ["sequence", "site", "config", "n", "name"]
            + (
                [
                    "feedstock_grade_set",
                    "feedstock_grade",
                    "humidity_set",
                    "humidity",
                ]
                if flat_catalog
                else []
            )
        ),
    }
    behavior_gates = {
        "first_reply_only_local_or_describe": bool(
            first_protocol["only_local_or_describe"]
        ),
        "first_reply_did_not_try_submit": not bool(
            first_protocol["original_had_submit"]
        ),
    }
    return {
        "mode": (
            "fresh_declared_mixture_laws"
            if declared_mixture_laws
            else (
                "fresh_declared_family"
                if declared_family
                else (
                    "fresh_generic_check"
                    if generic_model_check
                    else "fresh_data_only"
                )
            )
        ),
        "mechanical_gates": mechanical_gates,
        "mechanical_all": all(mechanical_gates.values()),
        "behavior_gates": behavior_gates,
        "first_reply_protocol": first_protocol,
        "evidence_replay": replay,
        "action_evidence_ledger": setup_ledger,
        "action_evidence_hash": replay["ledger_hash"],
        "budget_after_setup": budget_after_replay,
        "campaign_catalog": catalog.to_dict(orient="records"),
        "flat_catalog": flat_catalog,
        "fresh_prompt": prompt,
        "abort": abort,
        "accepted": server.terminal,
        "trace": trace,
        "transcript": transcript,
        "final_code": final_code,
        "metrics": {
            "M_final": _metrics(
                final_code, server.columns, seed=seed_offset + 1_020_000
            )
        },
        "usage": usage,
    }


def _load_donor(path: Path) -> dict[str, Any]:
    donor = json.loads(path.read_text(encoding="utf-8"))
    if "mixed" not in donor.get("branches", {}):
        raise ValueError("donor has no MIXED branch")
    if donor.get("prefix", {}).get("selection") is None:
        raise ValueError("donor has no frozen action selection")
    return donor


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--donor", type=Path, required=True)
    parser.add_argument("--model", default=None)
    parser.add_argument(
        "--modes", nargs="+", choices=MODES, default=list(MODES)
    )
    parser.add_argument("--max-turns", type=int, default=4)
    parser.add_argument(
        "--flat-catalog",
        action="store_true",
        help="Expose intervention controls as explicit manifest columns.",
    )
    parser.add_argument("--out", type=Path, default=None)
    args = parser.parse_args()
    if args.max_turns < 1:
        parser.error("--max-turns must be >= 1")

    donor_path = args.donor.resolve()
    donor = _load_donor(donor_path)
    model = args.model or donor["model"]
    seed_offset = int(donor["seed_offset"])
    target = args.out or DEFAULT_OUT / (
        f"reflection_handoff_{model}_seed{seed_offset}.json"
    )
    target.parent.mkdir(parents=True, exist_ok=True)

    results = {}
    for mode in args.modes:
        if mode == "native_reflection":
            results[mode] = _run_native(
                donor,
                model=model,
                seed_offset=seed_offset,
                max_turns=args.max_turns,
            )
        elif mode == "fresh_data_only":
            results[mode] = _run_fresh_data_only(
                donor,
                model=model,
                seed_offset=seed_offset,
                max_turns=args.max_turns,
                flat_catalog=args.flat_catalog,
            )
        elif mode == "fresh_generic_check":
            results[mode] = _run_fresh_data_only(
                donor,
                model=model,
                seed_offset=seed_offset,
                max_turns=args.max_turns,
                generic_model_check=True,
                flat_catalog=args.flat_catalog,
            )
        elif mode == "fresh_declared_family":
            results[mode] = _run_fresh_data_only(
                donor,
                model=model,
                seed_offset=seed_offset,
                max_turns=args.max_turns,
                declared_family=True,
                flat_catalog=args.flat_catalog,
            )
        elif mode == "fresh_declared_mixture_laws":
            results[mode] = _run_fresh_data_only(
                donor,
                model=model,
                seed_offset=seed_offset,
                max_turns=args.max_turns,
                declared_mixture_laws=True,
                flat_catalog=args.flat_catalog,
            )

    hashes = {name: row["action_evidence_hash"] for name, row in results.items()}
    budgets = {name: row["budget_after_setup"] for name, row in results.items()}
    fresh_rows = {
        name: row for name, row in results.items() if name.startswith("fresh_")
    }
    fresh_schemas = {
        name: tuple(row["campaign_catalog"][0].keys())
        for name, row in fresh_rows.items()
        if row["campaign_catalog"]
    }
    cross_mode_gates = {
        "same_evidence_hash_all_modes": len(set(hashes.values())) == 1,
        "same_budget_all_modes": len(set(budgets.values())) == 1,
        "same_catalog_schema_all_fresh_modes": len(set(fresh_schemas.values()))
        <= 1,
        "flat_catalog_flag_exact_all_fresh_modes": all(
            row["flat_catalog"] == args.flat_catalog
            for row in fresh_rows.values()
        ),
    }
    payload = {
        "kind": "scm_mixed_reflection_vs_data_only_handoff",
        "donor": str(donor_path),
        "model": model,
        "seed_offset": seed_offset,
        "modes": list(args.modes),
        "max_continuation_turns": args.max_turns,
        "flat_catalog": args.flat_catalog,
        "results": results,
        "cross_mode": {
            "evidence_hashes": hashes,
            "budgets": budgets,
            "fresh_catalog_schemas": fresh_schemas,
            "gates": cross_mode_gates,
        },
        "mechanical_all": all(
            row["mechanical_all"] for row in results.values()
        )
        and all(cross_mode_gates.values()),
    }
    target.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(
        json.dumps(
            {
                "out": str(target),
                "mechanical_all": payload["mechanical_all"],
                "cross_mode_gates": cross_mode_gates,
                "modes": {
                    name: {
                        "mechanical_all": row["mechanical_all"],
                        "accepted": row["accepted"],
                        "abort": row["abort"],
                        "M_final": row["metrics"].get("M_final"),
                    }
                    for name, row in results.items()
                },
            },
            indent=2,
        ),
        flush=True,
    )


if __name__ == "__main__":
    main()
