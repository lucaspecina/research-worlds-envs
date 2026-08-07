"""LATENT-only control requiring one real post-output review turn.

The runner reuses the exact controlled-2D v1 prefix and visible tables. Its
only intervention is a procedural rejection of ``submit`` in the first
post-routine cell, so a second LLM turn receives that cell's ordinary stdout
before final handoff. By default this performs only zero-LLM certification;
``--run-agent`` is required to spend API budget.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from wager.harness.case_episode import build_world_server  # noqa: E402

from scripts import probe_scm_topology_controlled_2d as controlled  # noqa: E402
from scripts import probe_scm_transfer_topology_v1 as topology  # noqa: E402
from scripts.analyze_scm_topology_recoverability import (  # noqa: E402
    recoverability_from_ledger,
)


MODEL = controlled.MODEL
SEED_OFFSET = controlled.SEED_OFFSET
SOURCE = controlled.SOURCE
LATENT = topology.LATENT
V1_RAW = (
    controlled.OUT
    / "probe_gpt-5.4_seed98403_controlled_2d_v1.json"
)
V1_RAW_SHA256 = (
    "0034e78ebff42f65014e323ef27d45880de625a0d138e2d1d0882cb16cf274f2"
)
CERTIFICATE_OUT = (
    controlled.OUT
    / "gpt98403_controlled_2d_latent_review_v2_certificate.json"
)
AGENT_OUT = (
    controlled.OUT
    / "probe_gpt-5.4_seed98403_controlled_2d_latent_review_v2.json"
)


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _submit_events(trace_row: dict[str, Any]) -> list[dict[str, Any]]:
    return [
        event
        for event in trace_row.get("trajectory", [])
        if event.get("verb") == "submit"
    ]


def _certify_submit_gate(valid_code: str) -> dict[str, Any]:
    """Exercise the guard on a real server without any LLM call."""
    server = build_world_server(LATENT, seed_offset=SEED_OFFSET)
    gate = controlled.FirstCellSubmitGate(server)

    rejected = server.submit(valid_code)
    terminal_while_locked = server.terminal
    first_event = server.trajectory[-1]

    gate.open_next_turn()
    accepted = server.submit(valid_code)
    return {
        "rejected_while_locked": not rejected.accepted,
        "neutral_error_exact": (
            rejected.error == controlled.FIRST_CELL_REVIEW_ERROR
        ),
        "terminal_while_locked": terminal_while_locked,
        "first_event_is_rejected_submit": (
            first_event.verb == "submit"
            and first_event.args == {"accepted": False}
        ),
        "ordinary_submit_accepted_after_open": accepted.accepted,
        "ordinary_submit_error_after_open": accepted.error,
        "terminal_after_open": server.terminal,
        "rejected_attempts": gate.rejected_attempts,
    }


def build_mechanical_certificate(
    source: Path,
    v1_raw: Path,
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    topology._configure_reused_runner(require_north_review_turn=True)
    prefix, provenance = topology.load_resumable_prefix(
        source,
        expected_model=MODEL,
        expected_seed=SEED_OFFSET,
    )
    v1_payload = json.loads(v1_raw.read_text(encoding="utf-8"))
    v1_latent = v1_payload["branches"]["latent"]

    branch = controlled.replay_routine_and_optionally_continue(
        LATENT,
        prefix,
        interface_version="v1",
        run_agent=False,
        max_post_routine_turns=1,
        require_post_output_review=True,
    )
    recoverability = recoverability_from_ledger(
        branch["action_ledger"] + branch["routine_ledger"],
        target="latent",
        folds=None,
        seed=SEED_OFFSET + 1_900_001,
    )
    guard = _certify_submit_gate(v1_latent["submission_code"])
    notice = controlled.ROUTINE_NOTICE.lower()
    gates = {
        "source_sha256_exact": (
            controlled._sha256(source) == controlled.SOURCE_SHA256
        ),
        "v1_raw_sha256_exact": _sha256(v1_raw) == V1_RAW_SHA256,
        "v1_run_passed": v1_payload.get("all") is True,
        "v1_interface_exact": v1_payload.get("interface_version") == "v1",
        "prefix_reconstruction_exact": provenance.get("all") is True,
        "replay_exact": branch["replay_exact"],
        "prefix_ledger_exact": branch["prefix_ledger_exact"],
        "frozen_action_hash_exact": (
            branch["action_cell_sha256"]
            == prefix["selection"]["cell_sha256"]
        ),
        "action_requests_match_source": (
            branch["action_requests_match_source"]
        ),
        "action_ledger_identical_to_v1": (
            branch["action_ledger"] == v1_latent["action_ledger"]
        ),
        "routine_ledger_identical_to_v1": (
            branch["routine_ledger"] == v1_latent["routine_ledger"]
        ),
        "visible_tables_identical_to_v1": (
            branch["routine_agent_visible"]
            == v1_latent["routine_agent_visible"]
        ),
        "visible_provenance_exact": (
            controlled._visible_provenance_exact(branch)
        ),
        "routine_cost_and_budget_exact": (
            abs(branch["budget_before_routine"] - 1480.0) < 1e-9
            and abs(branch["budget_after_routine"] - 1040.0) < 1e-9
        ),
        "no_hypothesis_cues_in_notice": not any(
            cue in notice for cue in controlled.PROHIBITED_NOTICE_CUES
        ),
        "future_experiments_blocked": branch["further_experiments_blocked"],
        "latent_recoverable_BIC_CV": (
            recoverability.get("informative") is True
            and recoverability.get("recoverable") is True
            and recoverability.get("BIC_winner") == "latent_mixture"
            and recoverability.get("CV_winner") == "latent_mixture"
        ),
        "review_guard_rejects_without_terminal": (
            guard["rejected_while_locked"]
            and guard["neutral_error_exact"]
            and not guard["terminal_while_locked"]
            and guard["first_event_is_rejected_submit"]
        ),
        "ordinary_submit_restored_after_review": (
            guard["ordinary_submit_accepted_after_open"]
            and guard["terminal_after_open"]
            and guard["rejected_attempts"] == 1
        ),
        "v2_paths_do_not_alias_v0_or_v1": (
            CERTIFICATE_OUT.name
            not in {
                "gpt98403_controlled_2d_certificate.json",
                "gpt98403_controlled_2d_v1_certificate.json",
            }
            and AGENT_OUT.name
            not in {
                "probe_gpt-5.4_seed98403_controlled_2d.json",
                "probe_gpt-5.4_seed98403_controlled_2d_v1.json",
            }
        ),
    }
    certificate = {
        "kind": "SCM_topology_LATENT_post_output_review_certificate_v2",
        "model": MODEL,
        "seed_offset": SEED_OFFSET,
        "source": str(source),
        "v1_raw": str(v1_raw),
        "v1_raw_sha256": _sha256(v1_raw),
        "prefix_provenance": provenance,
        "branch": branch,
        "recoverability": recoverability,
        "submit_gate": guard,
        "gates": gates,
        "all": all(gates.values()),
    }
    return certificate, prefix, v1_latent


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, default=SOURCE)
    parser.add_argument("--v1-raw", type=Path, default=V1_RAW)
    parser.add_argument(
        "--run-agent",
        action="store_true",
        help="Run the one real LATENT branch after zero-LLM gates pass.",
    )
    parser.add_argument("--max-post-routine-turns", type=int, default=3)
    parser.add_argument("--signature-n", type=int, default=4_000)
    parser.add_argument("--out", type=Path, default=None)
    args = parser.parse_args()
    if args.max_post_routine_turns not in {2, 3}:
        raise ValueError("max-post-routine-turns must be 2 or 3")

    certificate, prefix, v1_latent = build_mechanical_certificate(
        args.source,
        args.v1_raw,
    )
    controlled._write_json(CERTIFICATE_OUT, certificate)
    if not certificate["all"]:
        print(
            json.dumps(
                {
                    "certificate": str(CERTIFICATE_OUT),
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
                    "certificate": str(CERTIFICATE_OUT),
                    "all": True,
                    "agent_calls": 0,
                    "recoverability": {
                        "BIC_winner": certificate["recoverability"][
                            "BIC_winner"
                        ],
                        "CV_winner": certificate["recoverability"][
                            "CV_winner"
                        ],
                        "design_rank": certificate["recoverability"][
                            "design_rank"
                        ],
                    },
                },
                indent=2,
            ),
            flush=True,
        )
        return

    branch = controlled.replay_routine_and_optionally_continue(
        LATENT,
        prefix,
        interface_version="v1",
        run_agent=True,
        max_post_routine_turns=args.max_post_routine_turns,
        require_post_output_review=True,
    )
    mpre = prefix["selection"]["M_pre"]
    controlled.transfer.add_artifact_measurements(
        branch,
        LATENT,
        mpre,
        signature_n=args.signature_n,
        signature_seed=SEED_OFFSET + 2_100_001,
    )
    topology.add_topology_measurements(
        branch,
        LATENT,
        mpre,
        signature_n=args.signature_n,
        signature_seed=SEED_OFFSET + 2_200_001,
    )

    trace = branch["trace"]
    first_submit_events = _submit_events(trace[0]) if trace else []
    gates = {
        "mechanical_certificate_passed": certificate["all"],
        "at_least_two_real_post_routine_turns": len(trace) >= 2,
        "first_cell_attempted_submit": bool(first_submit_events),
        "first_submit_rejected": (
            bool(first_submit_events)
            and first_submit_events[0].get("args")
            == {"accepted": False}
        ),
        "no_accepted_submit_in_first_cell": not any(
            event.get("args", {}).get("accepted") is True
            for event in first_submit_events
        ),
        "first_cell_nonterminal": (
            bool(trace) and trace[0].get("terminal_after_cell") is False
        ),
        "review_gate_opened_after_first_cell": (
            branch["review_gate_open_after_first_cell"] is True
        ),
        "no_post_routine_experiments": not any(
            event.get("verb") == "experiment"
            for row in trace
            for event in row.get("trajectory", [])
        ),
        "routine_ledger_identical_to_v1": (
            branch["routine_ledger"] == v1_latent["routine_ledger"]
        ),
        "visible_tables_identical_to_v1": (
            branch["routine_agent_visible"]
            == v1_latent["routine_agent_visible"]
        ),
        "accepted": branch["accepted"],
        "last_artifact_scoreable": branch["scores"]["M_last"].get(
            "scoreable", False
        ),
        "topology_last_scoreable": branch["topology_signatures"][
            "M_last"
        ].get("scoreable", False),
    }
    payload = {
        "kind": "exploratory_SCM_topology_LATENT_post_output_review_v2",
        "claim_scope": (
            "LATENT-only mechanism control: same controlled-2D v1 evidence, "
            "with one real LLM turn seeing the first cell output before "
            "handoff. Not a prevalence estimate."
        ),
        "model": MODEL,
        "seed_offset": SEED_OFFSET,
        "source": str(args.source),
        "v1_raw": str(args.v1_raw),
        "mechanical_certificate": certificate,
        "branch": branch,
        "gates": gates,
        "all": all(gates.values()),
    }
    target = args.out or AGENT_OUT
    controlled._write_json(target, payload)
    print(
        json.dumps(
            {
                "out": str(target),
                "all": payload["all"],
                "gates": gates,
                "abort": branch["abort"],
            },
            indent=2,
        ),
        flush=True,
    )


if __name__ == "__main__":
    main()
