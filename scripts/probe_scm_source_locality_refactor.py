"""Pilot of source-layout effects on local belief revision.

The executable Mpre from the exploratory DeepSeek seed-97800 run is used only
as discovery material.  Two predictively identical source layouts are exposed
in fresh neutral handoffs: the original SHARED grade coefficient and a SPLIT
version whose South/North coefficients start equal.  Each layout is crossed
with the validated REVISE/RETAIN twins.

``--cert-only`` validates the source equivalence, twin geometry, raw audit
pairing, and closed collection window without constructing an LLM client.
The frozen exploratory contract lives in
``docs/research/2026-08-01-ficha-probe-localizacion-refactor-mpre97800-v0.md``.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import re
import sys
from pathlib import Path
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
from wager.reward.sandbox import SandboxedSubmission  # noqa: E402

from scripts.probe_first_story_causal_fork import (  # noqa: E402
    feedback,
    record,
)
from scripts.probe_first_story_scm_transfer_fork import (  # noqa: E402
    REVISE,
    RETAIN,
    SYSTEM,
    _artifact_hash,
    add_artifact_measurements,
)
from scripts.probe_scm_accelerated_lived_history import (  # noqa: E402
    AUDIT_SPECS,
    AUDIT_VARIABLES,
    _design,
    _evidence_requests,
    _frame_hash,
    _ledger_hash,
)


OUT = ROOT / "scripts" / "out" / "first_story_scm_source_locality_refactor"
DONOR_RAW = (
    ROOT
    / "scripts"
    / "out"
    / "first_story_scm_accelerated_lived_history"
    / "probe_DeepSeek-V3.2_seed97800.json"
)
EXPECTED_DONOR_MPRE_SHA256 = (
    "fddd222dd6cb754ae7fc91c1bad1faa1ecb34109de2b12f1a507dc3a878e7c9a"
)
FROZEN_FICHA = (
    "docs/research/"
    "2026-08-01-ficha-probe-localizacion-refactor-mpre97800-v0.md"
)
SOURCE_ANCHOR = "    beta_grade = 1.893\n"
SOURCE_REPLACEMENT = (
    "    beta_grade_south = 1.893\n"
    "    beta_grade_north = 1.893\n"
    "    beta_grade = beta_grade_north if site == 'north' else beta_grade_south\n"
)
BRANCH_SPECS = (
    ("shared_revise", "shared", REVISE, "revise"),
    ("split_revise", "split", REVISE, "revise"),
    ("shared_retain", "shared", RETAIN, "retain"),
    ("split_retain", "split", RETAIN, "retain"),
)
_NON_NEUTRAL = re.compile(
    r"\b(revise|retain|refut|contradic|correction|wrong|change your mind|"
    r"refactor|shared|split)\w*\b",
    re.IGNORECASE,
)


def _load_sources() -> dict[str, str]:
    payload = json.loads(DONOR_RAW.read_text(encoding="utf-8"))
    shared = payload["prefix"]["M_pre"]
    shared_hash = hashlib.sha256(shared.encode("utf-8")).hexdigest()
    if shared_hash != EXPECTED_DONOR_MPRE_SHA256:
        raise ValueError(
            "seed-97800 donor Mpre hash changed; refusing silent source drift"
        )
    if shared.count(SOURCE_ANCHOR) != 1:
        raise ValueError("expected exactly one global beta_grade source anchor")
    split = shared.replace(SOURCE_ANCHOR, SOURCE_REPLACEMENT)
    return {"shared": shared, "split": split}


def _request(spec: dict[str, Any]) -> dict[str, Any]:
    return {
        "config": copy.deepcopy(spec["config"]),
        "context": {"site": "north"},
        "n": int(spec["n"]),
        "horizon": None,
    }


def _handoff_prompt(server) -> str:
    sheet = server.describe()
    machine = {key: value for key, value in sheet.items() if key != "brief"}
    return (
        "Here is the assignment:\n\n"
        + sheet["brief"]
        + "\n\nMachine-readable sheet:\n"
        + json.dumps(machine, indent=2)
        + "\n\nYou are continuing from a mechanically prepared project state. "
        "The current executable project source is loaded as the Python string "
        "`working_model`. A routine North quality-control cycle has closed. Its "
        "two raw outputs are loaded as pandas DataFrames "
        "`north_audit_grade3` and `north_audit_grade7`; each has exactly the "
        "columns ['feedstock', 'outcome']. They are separate DataFrame variables "
        "available directly in the workspace. The data-collection window is "
        "closed: do not call env.observe or env.experiment. Inspect the raw "
        "batches as part of the ordinary research record, keep the executable "
        "project model current if your predictive view warrants it, and call "
        "env.submit(working_model) when the assignment is sufficient. The final "
        "model must cover both South and North."
    )


def _closed_experiment_guard(design, turn, fired_events) -> None:
    del design, turn, fired_events
    raise ValueError("the handoff data-collection window is closed")


def _close_collection(server) -> None:
    server.experiment_guard = _closed_experiment_guard

    def closed_observe(source: str, n: int):
        del source, n
        raise ValueError("the handoff data-collection window is closed")

    server.observe = closed_observe


def _prepare_audit_server(case_dir: Path, seed_offset: int):
    server = build_world_server(case_dir, seed_offset=seed_offset)
    notices = server.begin_turn(1)
    builtin_deliveries = server.pop_deliveries()
    start = len(server.trajectory)
    frames: dict[str, pd.DataFrame] = {}
    for spec in AUDIT_SPECS:
        frames[spec["name"]] = server.experiment(_design(spec))
    trajectory = [
        {
            "verb": event.verb,
            "args": event.args,
            "cost": event.cost,
            "note": event.note,
        }
        for event in server.trajectory[start:]
    ]
    audit = {
        "turn": 1,
        "notices": notices,
        "builtin_delivery_count": len(builtin_deliveries),
        "requests": _evidence_requests(trajectory),
        "frame_hashes": {
            name: _frame_hash(frame) for name, frame in frames.items()
        },
        "frame_rows": {name: len(frame) for name, frame in frames.items()},
        "columns": {name: frame.columns.tolist() for name, frame in frames.items()},
        "budget_after_audit": float(server.budget_remaining),
        "evidence_ledger_sha256": _ledger_hash(
            server.export_evidence_ledger()
        ),
    }
    return server, frames, audit


def _source_equivalence(
    sources: dict[str, str], *, repetitions: int = 2
) -> dict[str, Any]:
    rows: list[dict[str, Any]] = []
    for case_dir in (REVISE, RETAIN):
        server = build_world_server(case_dir)
        n_samples = int(server.scoring.params.n_samples)
        with (
            SandboxedSubmission(
                sources["shared"], server.columns, timeout_s=15.0
            ) as shared,
            SandboxedSubmission(
                sources["split"], server.columns, timeout_s=15.0
            ) as split,
        ):
            for item_index, item in enumerate(server.scoring.battery.items):
                for repetition in range(repetitions):
                    seed = int(item.seed_world) + repetition * 1_000_003
                    left = shared.run(item.regime, n_samples, seed)
                    right = split.run(item.regime, n_samples, seed)
                    numeric_diff = (left - right).abs().to_numpy().max()
                    rows.append(
                        {
                            "case_id": case_dir.name,
                            "battery_index": item_index,
                            "repetition": repetition,
                            "weight": float(item.weight),
                            "regime": item.regime.model_dump(),
                            "n": n_samples,
                            "seed": seed,
                            "shared_sha256": _frame_hash(left),
                            "split_sha256": _frame_hash(right),
                            "byte_exact": left.equals(right),
                            "max_abs_numeric_diff": float(numeric_diff),
                        }
                    )
    sites = {
        row["regime"]["context"].get("site", "south") for row in rows
    }
    return {
        "repetitions": repetitions,
        "rows": rows,
        "sites": sorted(sites),
        "all_byte_exact": all(row["byte_exact"] for row in rows),
        "max_abs_numeric_diff": max(
            row["max_abs_numeric_diff"] for row in rows
        ),
    }


def _collection_closure_certificate(case_dir: Path, seed_offset: int) -> dict:
    server, _, _ = _prepare_audit_server(case_dir, seed_offset)
    _close_collection(server)
    experiment_error = None
    observe_error = None
    try:
        server.experiment(
            ExperimentDesign(
                config={"humidity": 5.0},
                context={"site": "north"},
                n=1,
                horizon=None,
            )
        )
    except ValueError as exc:
        experiment_error = str(exc)
    try:
        server.observe("routine", 1)
    except ValueError as exc:
        observe_error = str(exc)
    return {
        "experiment_error": experiment_error,
        "observe_error": observe_error,
        "both_closed": bool(experiment_error and observe_error),
    }


def local_certificate(
    sources: dict[str, str], *, seed_offset: int
) -> dict[str, Any]:
    descriptions = {
        name: build_world_server(case_dir).describe()
        for name, _, case_dir, _ in BRANCH_SPECS
    }
    prompts = {
        name: _handoff_prompt(build_world_server(case_dir))
        for name, _, case_dir, _ in BRANCH_SPECS
    }
    validations = {
        f"{layout}_{case_dir.name}": build_world_server(case_dir).validate_model(
            source
        )
        for layout, source in sources.items()
        for case_dir in (REVISE, RETAIN)
    }
    equivalence = _source_equivalence(sources)
    audits: dict[str, dict[str, Any]] = {}
    for name, _, case_dir, _ in BRANCH_SPECS:
        _, _, audit = _prepare_audit_server(case_dir, seed_offset)
        audits[name] = audit
    source_hashes = {
        layout: _artifact_hash(source) for layout, source in sources.items()
    }
    gates = {
        "donor_raw_present": DONOR_RAW.is_file(),
        "donor_Mpre_hash_expected": (
            source_hashes["shared"] == EXPECTED_DONOR_MPRE_SHA256
        ),
        "source_hashes_distinct": len(set(source_hashes.values())) == 2,
        "split_coefficients_explicit_and_equal": (
            "beta_grade_south = 1.893" in sources["split"]
            and "beta_grade_north = 1.893" in sources["split"]
        ),
        "sources_valid_both_cases": all(
            error is None for error in validations.values()
        ),
        "battery_equivalence_byte_exact_all": equivalence["all_byte_exact"],
        "battery_equivalence_zero_numeric_diff": (
            equivalence["max_abs_numeric_diff"] == 0.0
        ),
        "battery_covers_both_sites": equivalence["sites"] == ["north", "south"],
        "agent_facing_twins_identical": all(
            sheet == descriptions["shared_revise"]
            for sheet in descriptions.values()
        ),
        "handoff_prompt_exact_all": len(set(prompts.values())) == 1,
        "handoff_prompt_neutral": all(
            _NON_NEUTRAL.search(prompt) is None for prompt in prompts.values()
        ),
        "handoff_declares_types_and_columns": all(
            "pandas DataFrames" in prompt
            and "['feedstock', 'outcome']" in prompt
            and all(variable in prompt for variable in AUDIT_VARIABLES)
            for prompt in prompts.values()
        ),
        "audit_requests_exact_all": len({
            json.dumps(audit["requests"], sort_keys=True)
            for audit in audits.values()
        }) == 1,
        "audit_raw_exact_shared_split_revise": (
            audits["shared_revise"]["frame_hashes"]
            == audits["split_revise"]["frame_hashes"]
        ),
        "audit_raw_exact_shared_split_retain": (
            audits["shared_retain"]["frame_hashes"]
            == audits["split_retain"]["frame_hashes"]
        ),
        "audit_differs_between_truth_poles": (
            audits["shared_revise"]["frame_hashes"]
            != audits["shared_retain"]["frame_hashes"]
        ),
        "audit_two_frames_32_rows_exact_columns": all(
            len(audit["frame_hashes"]) == 2
            and set(audit["frame_hashes"]) == set(AUDIT_VARIABLES)
            and all(rows == 32 for rows in audit["frame_rows"].values())
            and all(
                columns == ["feedstock", "outcome"]
                for columns in audit["columns"].values()
            )
            for audit in audits.values()
        ),
        "collection_closed_server_side": all(
            _collection_closure_certificate(case_dir, seed_offset)["both_closed"]
            for case_dir in (REVISE, RETAIN)
        ),
    }
    return {
        "kind": "zero_llm_source_locality_refactor_certificate",
        "seed_offset": seed_offset,
        "donor_raw": str(DONOR_RAW.relative_to(ROOT)).replace("\\", "/"),
        "donor_result_outside_estimand": True,
        "source_hashes": source_hashes,
        "source_validations": validations,
        "source_equivalence": equivalence,
        "audit": audits,
        "handoff_prompt_sha256": {
            name: hashlib.sha256(prompt.encode("utf-8")).hexdigest()
            for name, prompt in prompts.items()
        },
        "gates": gates,
        "all": all(gates.values()),
    }


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


def run_branch(
    case_dir: Path,
    source: str,
    *,
    model: str,
    seed_offset: int,
    max_turns: int,
) -> dict[str, Any]:
    server, audit_frames, audit = _prepare_audit_server(case_dir, seed_offset)
    _close_collection(server)
    trace: list[dict[str, Any]] = []
    prompt = _handoff_prompt(server)
    initial_prompt = prompt
    abort = "max_turns"
    with KernelClient(server, cell_timeout_s=CELL_TIMEOUT_S) as kernel:
        initialization = kernel.run_cell("working_model = " + repr(source))
        for name, frame in audit_frames.items():
            kernel.inject_dataframe(name, frame)
        chat = FoundryChat(
            system=SYSTEM,
            model=model,
            max_completion_tokens=MAX_COMPLETION_TOKENS,
        )
        for turn in range(1, max_turns + 1):
            if turn > 1:
                notices = server.begin_turn(turn)
                for variable, delivered in server.pop_deliveries():
                    kernel.inject_dataframe(variable, delivered)
            else:
                notices = audit["notices"]
            reply = chat.ask(prompt)
            cell = extract_cell(reply.content)
            if cell is None:
                abort = "no_cell"
                break
            start = len(server.trajectory)
            result = kernel.run_cell(cell)
            row = record(turn, reply.content, cell, result, server, notices, start)
            row["phase"] = "fresh_neutral_audit"
            trace.append(row)
            if server.terminal:
                abort = "submitted"
                break
            if result.error and result.error.startswith("cell exceeded "):
                abort = "cell_timeout"
                break
            prompt = feedback(result, server) + (
                "\n\nThe data-collection window remains closed."
            )
        transcript = copy.deepcopy(chat.messages)
        usage = _chat_usage(chat)
    final = server.result or {}
    mfirst = trace[0]["working_model"]["code"] if trace else None
    last_working = next(
        (
            row["working_model"]["code"]
            for row in reversed(trace)
            if row["working_model"]["code"]
        ),
        source,
    )
    ledger = server.export_evidence_ledger()
    return {
        "case_id": case_dir.name,
        "audit": audit,
        "initialization": {
            "ok": initialization.ok,
            "error": initialization.error,
            "working_model_exact": initialization.working_model == source,
        },
        "handoff_prompt": initial_prompt,
        "handoff_prompt_sha256": hashlib.sha256(
            initial_prompt.encode("utf-8")
        ).hexdigest(),
        "abort": abort,
        "accepted": server.terminal,
        "R": final.get("R"),
        "submission_code": final.get("code"),
        "M_pre": source,
        "M_first_model": mfirst,
        "first_changed_model": mfirst,
        "last_working_model": last_working,
        "last_working_model_code": last_working,
        "trace": trace,
        "transcript": transcript,
        "evidence_ledger": ledger,
        "post_audit_non_audit_evidence": ledger[len(AUDIT_SPECS):],
        "post_audit_experiment_requests": [
            event
            for row in trace
            for event in _evidence_requests(row["trajectory"])
        ],
        "audit_referenced": {
            variable: any(variable in row["cell"] for row in trace)
            for variable in AUDIT_VARIABLES
        },
        "audit_referenced_first_cell": {
            variable: bool(trace and variable in trace[0]["cell"])
            for variable in AUDIT_VARIABLES
        },
        "raw_prose_and_code": [
            {
                "turn": row["turn"],
                "reply_text": row["reply_text"],
                "cell": row["cell"],
                "working_model_code": row["working_model"]["code"],
            }
            for row in trace
        ],
        "usage": usage,
    }


def _delta(branch: dict[str, Any], checkpoint: str, site: str) -> float | None:
    row = branch["signatures"].get(f"M_{checkpoint}_{site}", {})
    value = row.get("delta_outcome_G_at_H5")
    return float(value) if value is not None else None


def _add_metrics(branch: dict[str, Any], truth_pole: str) -> None:
    pre_north = _delta(branch, "pre", "north")
    last_north = _delta(branch, "last", "north")
    pre_south = _delta(branch, "pre", "south")
    last_south = _delta(branch, "last", "south")
    truth_north = branch["signatures"]["truth_north"].get(
        "delta_outcome_G_at_H5"
    )
    denominator = (
        float(pre_north) - float(truth_north)
        if pre_north is not None and truth_north is not None
        else 0.0
    )
    update_fraction = (
        float((pre_north - last_north) / denominator)
        if last_north is not None and abs(denominator) >= 0.5
        else None
    )
    south_loss_fraction = (
        abs(float(last_south) - float(pre_south)) / abs(float(pre_south))
        if None not in (pre_south, last_south) and abs(float(pre_south)) >= 0.5
        else None
    )
    retain_preserves_both = bool(
        truth_pole == "retain"
        and None not in (pre_north, last_north, pre_south, last_south)
        and abs(float(last_north) - float(pre_north)) <= 1.5
        and abs(float(last_south) - float(pre_south)) <= 1.5
    )
    branch["metrics"] = {
        "truth_pole": truth_pole,
        "north_update_fraction_U": update_fraction,
        "south_effect_loss_fraction": south_loss_fraction,
        "retain_preserves_both_within_1_5": retain_preserves_both,
        "delta": {
            "M_pre_north": pre_north,
            "M_first_north": _delta(branch, "first", "north"),
            "M_last_north": last_north,
            "truth_north": truth_north,
            "M_pre_south": pre_south,
            "M_first_south": _delta(branch, "first", "south"),
            "M_last_south": last_south,
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", default="DeepSeek-V3.2")
    parser.add_argument("--seed-offset", type=int, default=98000)
    parser.add_argument("--max-turns", type=int, default=5)
    parser.add_argument("--signature-n", type=int, default=4_000)
    parser.add_argument(
        "--cert-only",
        action="store_true",
        help="Run all deterministic gates without constructing an LLM client.",
    )
    parser.add_argument("--out", type=Path, default=None)
    args = parser.parse_args()

    sources = _load_sources()
    certificate = local_certificate(sources, seed_offset=args.seed_offset)
    if args.cert_only:
        print(json.dumps(certificate, indent=2), flush=True)
        if not certificate["all"]:
            raise SystemExit(1)
        return
    if not certificate["all"]:
        raise RuntimeError("zero-LLM source-locality certificate failed")

    OUT.mkdir(parents=True, exist_ok=True)
    target = args.out or OUT / (
        f"probe_{args.model}_seed{args.seed_offset}.json"
    )
    target.parent.mkdir(parents=True, exist_ok=True)
    branches: dict[str, dict[str, Any]] = {}
    for index, (name, layout, case_dir, truth_pole) in enumerate(BRANCH_SPECS):
        branch = run_branch(
            case_dir,
            sources[layout],
            model=args.model,
            seed_offset=args.seed_offset,
            max_turns=args.max_turns,
        )
        branch["source_layout"] = layout
        branch["truth_pole"] = truth_pole
        add_artifact_measurements(
            branch,
            case_dir,
            sources[layout],
            signature_n=args.signature_n,
            signature_seed=args.seed_offset + 1_400_000 + index,
        )
        branch["M_first"] = branch["M_first_model"]
        branch["M_last"] = branch["last_scoreable_model"]
        branch["artifact_validity"] = {
            checkpoint: {
                "scoreable": branch["scores"][checkpoint].get(
                    "scoreable", False
                ),
                "error": branch["scores"][checkpoint].get("error"),
            }
            for checkpoint in ("M_pre", "M_first", "M_last")
        }
        _add_metrics(branch, truth_pole)
        branches[name] = branch

    gates = {
        "zero_llm_certificate": certificate["all"],
        "initialization_exact_all": all(
            branch["initialization"]["working_model_exact"]
            for branch in branches.values()
        ),
        "handoff_prompt_exact_all": len({
            branch["handoff_prompt_sha256"] for branch in branches.values()
        }) == 1,
        "audit_raw_exact_shared_split_revise": (
            branches["shared_revise"]["audit"]["frame_hashes"]
            == branches["split_revise"]["audit"]["frame_hashes"]
        ),
        "audit_raw_exact_shared_split_retain": (
            branches["shared_retain"]["audit"]["frame_hashes"]
            == branches["split_retain"]["audit"]["frame_hashes"]
        ),
        "audit_referenced_both_all": all(
            all(branch["audit_referenced"].values())
            for branch in branches.values()
        ),
        "zero_post_audit_evidence_all": all(
            not branch["post_audit_non_audit_evidence"]
            for branch in branches.values()
        ),
        "zero_post_audit_experiment_requests_all": all(
            not branch["post_audit_experiment_requests"]
            for branch in branches.values()
        ),
        "accepted_all": all(branch["accepted"] for branch in branches.values()),
        "M_first_captured_all": all(
            branch["M_first_model"] is not None for branch in branches.values()
        ),
        "M_last_scoreable_all": all(
            branch["scores"]["M_last"].get("scoreable", False)
            for branch in branches.values()
        ),
    }
    signal = {
        "both_revise_U_ge_0_75": all(
            branches[name]["metrics"]["north_update_fraction_U"] is not None
            and branches[name]["metrics"]["north_update_fraction_U"] >= 0.75
            for name in ("shared_revise", "split_revise")
        ),
        "shared_revise_south_loss_ge_0_50": (
            branches["shared_revise"]["metrics"]["south_effect_loss_fraction"]
            is not None
            and branches["shared_revise"]["metrics"][
                "south_effect_loss_fraction"
            ]
            >= 0.50
        ),
        "split_revise_south_loss_le_0_15": (
            branches["split_revise"]["metrics"]["south_effect_loss_fraction"]
            is not None
            and branches["split_revise"]["metrics"][
                "south_effect_loss_fraction"
            ]
            <= 0.15
        ),
        "both_retain_preserve_both": all(
            branches[name]["metrics"]["retain_preserves_both_within_1_5"]
            for name in ("shared_retain", "split_retain")
        ),
    }
    payload = {
        "kind": "exploratory_source_locality_refactor_probe",
        "claim_class": "single_discovery_artifact_pilot_not_prevalence",
        "model": args.model,
        "seed_offset": args.seed_offset,
        "frozen_ficha": FROZEN_FICHA,
        "donor_97800_result_outside_estimand": True,
        "replication_required_on_new_donor_and_model": True,
        "source_hashes": certificate["source_hashes"],
        "certificate": certificate,
        "branch_order": [name for name, _, _, _ in BRANCH_SPECS],
        "branches": branches,
        "gates": gates,
        "all": all(gates.values()),
        "pilot_signal_components": signal,
        "pilot_signal_complete": all(gates.values()) and all(signal.values()),
    }
    target.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(
        json.dumps(
            {
                "out": str(target),
                "all": payload["all"],
                "gates": gates,
                "metrics": {
                    name: branch["metrics"] for name, branch in branches.items()
                },
                "pilot_signal_components": signal,
                "pilot_signal_complete": payload["pilot_signal_complete"],
            },
            indent=2,
        ),
        flush=True,
    )


if __name__ == "__main__":
    main()
