"""Source-locality probe with the complete raw provenance of donor 97800.

This is the state-fidelity repair of ``probe_scm_source_locality_refactor``.
``--cert-only`` performs deterministic checks and never constructs an LLM client.
Real runs may be restricted with ``--branches``; RETAIN is deliberately runnable
before REVISE.
"""

# ruff: noqa: E402 -- repository scripts add ROOT before importing local packages.

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.probe_first_story_causal_fork import feedback, record
from scripts.probe_first_story_scm_transfer_fork import add_artifact_measurements
from scripts.probe_scm_accelerated_lived_history import (
    _evidence_requests,
    _frame_from_ledger,
    _frame_hash,
    _ledger_hash,
)
from scripts.probe_scm_source_locality_refactor import (
    AUDIT_SPECS,
    AUDIT_VARIABLES,
    BRANCH_SPECS,
    DONOR_RAW,
    EXPECTED_DONOR_MPRE_SHA256,
    SYSTEM,
    _NON_NEUTRAL,
    _add_metrics,
    _chat_usage,
    _close_collection,
    _collection_closure_certificate,
    _load_sources,
    _prepare_audit_server,
    _source_equivalence,
)
from wager.agent.cells import extract_cell
from wager.agent.llm_client import FoundryChat
from wager.harness.case_episode import build_world_server
from wager.harness.episode import CELL_TIMEOUT_S, MAX_COMPLETION_TOKENS
from wager.harness.kernel_proc import KernelClient


OUT = ROOT / "scripts" / "out" / "first_story_scm_source_locality_refactor_provenance"
FROZEN_FICHA = (
    "docs/research/"
    "2026-08-01-ficha-probe-localizacion-refactor-con-procedencia-v1.md"
)
EXPECTED_LEDGER_SHA256 = (
    "d8d9c2a9fb833a170dfebcb05289fcb0bac7f54f2e7e5f5ba1517b22475f8e1d"
)
EXPECTED_MANIFEST_SHA256 = (
    "861960896c34292347c266fde764652904ea9e3f2a2e0bc73b1d55076eda199d"
)
EXPECTED_FRAME_HASHES = (
    "dcba04b5cee7260c0a4efb723c8917c0c5f30a9c9bfc9e69edac04d46237ba40",
    "4e5b90e9d87f63929f1b20b77a8a3368e85b470b5174942d429440b985802f89",
    "895e1d93edc115ad17016065332c894ebdca0813529e45ce379ebcbae12e6e1e",
    "035ed2086f0d1162e7345fedbc9bb8192a2bd1f325ab5182fa36c8d6161b706c",
    "67bb950e2963d165b22bd0913b4446ce6c81b7f68431d7bcc6d703956f3875f9",
    "c3915824a316ccb132177f0dda60cd235aaae5154986a58d7d1f3ab37cc07817",
    "e2b6374fdb1d23c324648471ccaa885c79b8bb8d2195fe3102cc27cff4945ce8",
    "f27f9281311859179e837f9e82ac08ba645dce635e2cd2436c09164a3779a823",
    "6beeebc0a76aba1e53bc71c33c9f405046c2553750718d4b05706285638768d2",
    "7587aba38fb53943f4761f8fafb501b0f10db9796b30432d28c17040a4887d93",
    "460ad0118775bed01147aa1faaa300eb5f373275df82e478e35ff2d8f298117a",
    "fd9b65f641bf2199d26ee42e21ad132ba00c2eee13163155191ff81687f68aa1",
    "4ea64362b82179717e07818941b4ca2364731fbb81d7e8f5e266c786df4e575c",
    "bc1b25664fd6605d6f2843b225b13583096db4602ba8220ae359102befdd65c6",
    "9257c5431a0b6217d06970b403e533549a2b1d1b88367f8f9220ecf0d5222d92",
    "f30efdfc3e7f0750913326e65035325c7a7a389bdd130c42b00244fdb103e81d",
)
MANIFEST_COLUMNS = (
    "sequence", "turn", "kind", "source", "site", "config_json", "rows", "variable"
)


def _canonical_hash(value: Any) -> str:
    raw = json.dumps(value, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


def _load_provenance() -> tuple[list[dict[str, Any]], dict[str, pd.DataFrame], pd.DataFrame]:
    payload = json.loads(DONOR_RAW.read_text(encoding="utf-8"))
    ledger = copy.deepcopy(payload["prefix"]["evidence_ledger"])
    frames: dict[str, pd.DataFrame] = {}
    manifest_rows: list[dict[str, Any]] = []
    for index, row in enumerate(ledger, start=1):
        variable = f"evidence_{index:03d}"
        frames[variable] = _frame_from_ledger(row)
        request = row.get("request") or {}
        context = request.get("context") or {}
        manifest_rows.append(
            {
                "sequence": int(row["sequence"]),
                "turn": int(row["turn"]),
                "kind": str(row["kind"]),
                "source": row.get("source") or "",
                "site": context.get("site") or "",
                "config_json": json.dumps(
                    request.get("config") or {}, sort_keys=True, separators=(",", ":")
                ),
                "rows": len(row["data"]["data"]),
                "variable": variable,
            }
        )
    return ledger, frames, pd.DataFrame(manifest_rows, columns=MANIFEST_COLUMNS)


def _prompt(server: Any) -> str:
    sheet = server.describe()
    machine = {key: value for key, value in sheet.items() if key != "brief"}
    return (
        "Here is the assignment:\n\n"
        + sheet["brief"]
        + "\n\nMachine-readable sheet:\n"
        + json.dumps(machine, indent=2)
        + "\n\nYou are continuing from a mechanically prepared project state. "
        "The executable project source at the checkpoint is loaded as the Python "
        "string `working_model`. The complete accumulated data record available "
        "immediately before the checkpoint that produced this artifact is loaded "
        "as pandas DataFrames `evidence_001` through `evidence_016`. The neutral "
        "index `evidence_manifest` gives their sequence, turn, kind, source, site, "
        "config_json, row count, and variable name. A later routine North "
        "quality-control cycle has closed; its raw outputs are the DataFrames "
        "`north_audit_grade3` and `north_audit_grade7`, each with columns "
        "['feedstock', 'outcome']. The data-collection window is closed: do not "
        "call env.observe or env.experiment. Use the accumulated record and the "
        "new routine batches as ordinary project evidence, keep the executable "
        "model current when warranted, and call env.submit(working_model) when "
        "the assignment is sufficient. The final model must cover South and North."
    )


def local_certificate(sources: dict[str, str], *, seed_offset: int) -> dict[str, Any]:
    ledger, frames, manifest = _load_provenance()
    manifest_rows = manifest.to_dict(orient="records")
    frame_hashes = [_frame_hash(frame) for frame in frames.values()]
    descriptions = {
        name: build_world_server(case_dir).describe()
        for name, _, case_dir, _ in BRANCH_SPECS
    }
    prompts = {
        name: _prompt(build_world_server(case_dir))
        for name, _, case_dir, _ in BRANCH_SPECS
    }
    audits: dict[str, dict[str, Any]] = {}
    for name, _, case_dir, _ in BRANCH_SPECS:
        _, _, audits[name] = _prepare_audit_server(case_dir, seed_offset)
    equivalence = _source_equivalence(sources)
    gates = {
        "donor_raw_present": DONOR_RAW.is_file(),
        "donor_Mpre_hash_expected": hashlib.sha256(
            sources["shared"].encode("utf-8")
        ).hexdigest() == EXPECTED_DONOR_MPRE_SHA256,
        "ledger_count_16": len(ledger) == 16 and len(frames) == 16,
        "ledger_frozen_hash_exact": _ledger_hash(ledger) == EXPECTED_LEDGER_SHA256,
        "ledger_sequence_exact": [row["sequence"] for row in ledger] == list(range(1, 17)),
        "manifest_columns_exact": tuple(manifest.columns) == MANIFEST_COLUMNS,
        "manifest_frozen_hash_exact": _canonical_hash(manifest_rows) == EXPECTED_MANIFEST_SHA256,
        "manifest_turn_exact": [row["turn"] for row in manifest_rows]
        == [1] + [2] * 11 + [3, 4, 5, 6],
        "manifest_kind_exact": [row["kind"] for row in manifest_rows]
        == ["observe"] + ["experiment"] * 15,
        "manifest_source_site_config_from_ledger": all(
            row["source"] == ((source.get("source") or ""))
            and row["site"] == (((source.get("request") or {}).get("context") or {}).get("site") or "")
            and row["config_json"] == json.dumps(
                (source.get("request") or {}).get("config") or {},
                sort_keys=True,
                separators=(",", ":"),
            )
            for row, source in zip(manifest_rows, ledger, strict=True)
        ),
        "manifest_rows_and_variables_exact": all(
            row["rows"] == len(source["data"]["data"])
            and row["variable"] == f"evidence_{index:03d}"
            for index, (row, source) in enumerate(
                zip(manifest_rows, ledger, strict=True), start=1
            )
        ),
        "all_frame_hashes_frozen_exact": tuple(frame_hashes) == EXPECTED_FRAME_HASHES,
        "source_equivalence_byte_exact": equivalence["all_byte_exact"],
        "source_equivalence_both_sites": equivalence["sites"] == ["north", "south"],
        "agent_facing_twins_identical": len({json.dumps(x, sort_keys=True) for x in descriptions.values()}) == 1,
        "prompt_exact_all": len(set(prompts.values())) == 1,
        "prompt_neutral_and_not_validated": all(
            _NON_NEUTRAL.search(text) is None and "validated" not in text.lower()
            for text in prompts.values()
        ),
        "prompt_declares_full_record": all(
            "`evidence_001` through `evidence_016`" in text
            and "`evidence_manifest`" in text
            and "checkpoint that produced this artifact" in text
            for text in prompts.values()
        ),
        "audit_raw_exact_within_poles": audits["shared_revise"]["frame_hashes"]
        == audits["split_revise"]["frame_hashes"]
        and audits["shared_retain"]["frame_hashes"]
        == audits["split_retain"]["frame_hashes"],
        "audit_two_frames_exact": all(
            set(row["frame_hashes"]) == set(AUDIT_VARIABLES)
            and all(n == 32 for n in row["frame_rows"].values())
            for row in audits.values()
        ),
        "collection_closed_server_side": all(
            _collection_closure_certificate(case_dir, seed_offset)["both_closed"]
            for case_dir in {spec[2] for spec in BRANCH_SPECS}
        ),
    }
    return {
        "kind": "zero_llm_source_locality_provenance_certificate",
        "seed_offset": seed_offset,
        "provenance": {
            "ledger_sha256": _ledger_hash(ledger),
            "manifest_sha256": _canonical_hash(manifest_rows),
            "manifest": manifest_rows,
            "frame_hashes": dict(zip(frames, frame_hashes, strict=True)),
        },
        "source_equivalence": equivalence,
        "audit": audits,
        "prompt_sha256": hashlib.sha256(next(iter(prompts.values())).encode()).hexdigest(),
        "gates": gates,
        "all": all(gates.values()),
    }


def run_branch(
    case_dir: Path,
    source: str,
    *,
    model: str,
    seed_offset: int,
    max_turns: int,
) -> dict[str, Any]:
    ledger, evidence_frames, manifest = _load_provenance()
    server, audit_frames, audit = _prepare_audit_server(case_dir, seed_offset)
    _close_collection(server)
    trace: list[dict[str, Any]] = []
    prompt = _prompt(server)
    initial_prompt = prompt
    abort = "max_turns"
    with KernelClient(server, cell_timeout_s=CELL_TIMEOUT_S) as kernel:
        for name, frame in evidence_frames.items():
            kernel.inject_dataframe(name, frame)
        kernel.inject_dataframe("evidence_manifest", manifest)
        initialization = kernel.run_cell("working_model = " + repr(source))
        for name, frame in audit_frames.items():
            kernel.inject_dataframe(name, frame)
        chat = FoundryChat(system=SYSTEM, model=model, max_completion_tokens=MAX_COMPLETION_TOKENS)
        for turn in range(1, max_turns + 1):
            notices = audit["notices"] if turn == 1 else server.begin_turn(turn)
            if turn > 1:
                for variable, delivered in server.pop_deliveries():
                    kernel.inject_dataframe(variable, delivered)
            reply = chat.ask(prompt)
            cell = extract_cell(reply.content)
            if cell is None:
                abort = "no_cell"
                break
            start = len(server.trajectory)
            result = kernel.run_cell(cell)
            row = record(turn, reply.content, cell, result, server, notices, start)
            row["phase"] = "fresh_complete_provenance_audit"
            trace.append(row)
            if server.terminal:
                abort = "submitted"
                break
            if result.error and result.error.startswith("cell exceeded "):
                abort = "cell_timeout"
                break
            prompt = feedback(result, server) + "\n\nThe data-collection window remains closed."
        transcript = copy.deepcopy(chat.messages)
        usage = _chat_usage(chat)
    final = server.result or {}
    mfirst = trace[0]["working_model"]["code"] if trace else None
    last_working = next(
        (row["working_model"]["code"] for row in reversed(trace) if row["working_model"]["code"]),
        source,
    )
    all_cells = "\n".join(row["cell"] for row in trace)
    literal_refs = {name: name in all_cells for name in evidence_frames}
    manifest_ref = "evidence_manifest" in all_cells
    dynamic_ref = "globals()" in all_cells or "globals()[" in all_cells
    server_ledger = server.export_evidence_ledger()
    return {
        "case_id": case_dir.name,
        "audit": audit,
        "initialization": {"ok": initialization.ok, "error": initialization.error, "working_model_exact": initialization.working_model == source},
        "handoff_prompt": initial_prompt,
        "handoff_prompt_sha256": hashlib.sha256(initial_prompt.encode()).hexdigest(),
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
        "prior_record": {"count": len(ledger), "ledger_sha256": _ledger_hash(ledger), "manifest": manifest.to_dict(orient="records"), "frame_hashes": {name: _frame_hash(frame) for name, frame in evidence_frames.items()}},
        "prior_record_references": {"manifest": manifest_ref, "dynamic_lookup": dynamic_ref, "literal_frames": literal_refs, "usable_record_inspected": manifest_ref and (dynamic_ref or any(literal_refs.values()))},
        "cell_errors": [
            row["cell_result"]["error"]
            for row in trace
            if row["cell_result"].get("error")
        ],
        "server_audit_ledger": server_ledger,
        "post_audit_non_audit_evidence": server_ledger[len(AUDIT_SPECS):],
        "post_audit_experiment_requests": [event for row in trace for event in _evidence_requests(row["trajectory"])],
        "audit_referenced": {variable: any(variable in row["cell"] for row in trace) for variable in AUDIT_VARIABLES},
        "usage": usage,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", default="DeepSeek-V3.2")
    parser.add_argument("--seed-offset", type=int, default=98100)
    parser.add_argument("--max-turns", type=int, default=5)
    parser.add_argument("--signature-n", type=int, default=4_000)
    parser.add_argument("--cert-only", action="store_true")
    parser.add_argument("--branches", nargs="+", choices=[row[0] for row in BRANCH_SPECS])
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
        raise RuntimeError("zero-LLM provenance certificate failed")

    requested = set(args.branches or [row[0] for row in BRANCH_SPECS])
    selected = [row for row in BRANCH_SPECS if row[0] in requested]
    tag = "all" if len(selected) == len(BRANCH_SPECS) else "-".join(row[0] for row in selected)
    OUT.mkdir(parents=True, exist_ok=True)
    target = args.out or OUT / f"probe_{args.model}_seed{args.seed_offset}_{tag}.json"
    branches: dict[str, Any] = {}
    for index, (name, layout, case_dir, truth_pole) in enumerate(selected):
        branch = run_branch(case_dir, sources[layout], model=args.model, seed_offset=args.seed_offset, max_turns=args.max_turns)
        branch["source_layout"] = layout
        branch["truth_pole"] = truth_pole
        branches[name] = branch
        # Persist the expensive real-agent trace before any derived measurement.
        # If scoring code fails, the behavioral raw remains available for autopsy.
        target.write_text(
            json.dumps(
                {
                    "kind": "partial_source_locality_provenance_probe",
                    "model": args.model,
                    "seed_offset": args.seed_offset,
                    "frozen_ficha": FROZEN_FICHA,
                    "completed_branch_order": list(branches),
                    "branches": branches,
                },
                indent=2,
            )
            + "\n",
            encoding="utf-8",
        )
        add_artifact_measurements(branch, case_dir, sources[layout], signature_n=args.signature_n, signature_seed=args.seed_offset + 1_500_000 + index)
        branch["M_first"] = branch["M_first_model"]
        branch["M_last"] = branch["last_scoreable_model"]
        _add_metrics(branch, truth_pole)
        target.write_text(
            json.dumps(
                {
                    "kind": "partial_source_locality_provenance_probe",
                    "model": args.model,
                    "seed_offset": args.seed_offset,
                    "frozen_ficha": FROZEN_FICHA,
                    "completed_branch_order": list(branches),
                    "branches": branches,
                },
                indent=2,
            )
            + "\n",
            encoding="utf-8",
        )
    gates = {
        "zero_llm_certificate": certificate["all"],
        "requested_branches_present": list(branches) == [row[0] for row in selected],
        "initialization_exact_all": all(row["initialization"]["working_model_exact"] for row in branches.values()),
        "prior_record_hash_exact_all": all(row["prior_record"]["ledger_sha256"] == EXPECTED_LEDGER_SHA256 for row in branches.values()),
        "prior_record_inspected_all": all(row["prior_record_references"]["usable_record_inspected"] for row in branches.values()),
        "audit_referenced_both_all": all(all(row["audit_referenced"].values()) for row in branches.values()),
        "zero_cell_errors_all": all(not row["cell_errors"] for row in branches.values()),
        "zero_post_audit_evidence_all": all(not row["post_audit_non_audit_evidence"] for row in branches.values()),
        "zero_post_audit_experiment_requests_all": all(not row["post_audit_experiment_requests"] for row in branches.values()),
        "accepted_all": all(row["accepted"] for row in branches.values()),
        "M_last_scoreable_all": all(row["scores"]["M_last"].get("scoreable", False) for row in branches.values()),
    }
    retain_names = {"shared_retain", "split_retain"}
    retention_gate = None
    if retain_names.issubset(branches):
        retention_gate = all(gates.values()) and all(
            branches[name]["metrics"]["retain_preserves_both_within_1_5"]
            for name in retain_names
        )
    payload = {
        "kind": "exploratory_source_locality_refactor_complete_provenance_probe",
        "model": args.model,
        "seed_offset": args.seed_offset,
        "frozen_ficha": FROZEN_FICHA,
        "branch_order": list(branches),
        "certificate": certificate,
        "branches": branches,
        "gates": gates,
        "all": all(gates.values()),
        "retention_fidelity_gate": retention_gate,
        "no_native_or_replay_baseline_scope_limit": True,
    }
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"out": str(target), "all": payload["all"], "gates": gates, "retention_fidelity_gate": retention_gate}, indent=2), flush=True)


if __name__ == "__main__":
    main()
