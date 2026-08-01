"""Replay a saved real-agent fork to recover its exact legal evidence ledger.

No LLM is called.  The saved cells are executed against fresh twin servers,
then the frozen legal reference and checkpoint scores are derived from only
the data returned during that replay.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from wager.factory.overgen_stream_tools import build_reference_from_ledger  # noqa: E402
from wager.harness.case_episode import build_world_server  # noqa: E402
from wager.harness.episode import CELL_TIMEOUT_S  # noqa: E402
from wager.harness.kernel_proc import KernelClient  # noqa: E402
from wager.report.checkpoint_score import (  # noqa: E402
    CheckpointScorer,
    captured_reference_fraction,
)
from wager.report.overgen_belief import shared_transfer_phenotype  # noqa: E402

CASES = {
    "limited": ROOT / "cases" / "overgen_stream_v0",
    "transfer": ROOT / "cases" / "overgen_stream_twin_v0",
}


def _checkpoint_codes(payload, arm):
    pre = payload["prefix"]["trace"][-1]["working_model"]["code"]
    trace = payload["branches"][arm]["trace"]
    first_seen = next(
        (row["working_model"]["code"] for row in trace
         if row["working_model"]["code"] is not None),
        None,
    )
    first_changed = next(
        (row["working_model"]["code"] for row in trace
         if row["working_model"]["code"] is not None
         and row["working_model"]["code"] != pre),
        None,
    )
    return {
        "M_pre": pre,
        "M_post_first_seen": first_seen,
        "M_post_first_changed": first_changed,
        "M_final": payload["branches"][arm].get("submission_code"),
    }


def replay_ledger(payload, arm):
    server = build_world_server(CASES[arm], seed_offset=payload["seed_offset"])
    # Mirror the original runner's initial machine-readable sheet call before
    # any saved cell. Even read-only setup calls belong in an exact replay.
    server.describe()
    checkpoint = payload.get("checkpoint", "fixed")
    checks = []
    with KernelClient(server, cell_timeout_s=CELL_TIMEOUT_S) as kernel:
        for saved in payload["prefix"]["trace"]:
            server.begin_turn(saved["turn"], fire_events=(checkpoint == "fixed"))
            for variable, frame in server.pop_deliveries():
                kernel.inject_dataframe(variable, frame)
            result = kernel.run_cell(saved["cell"])
            checks.append({
                "phase": "prefix",
                "turn": saved["turn"],
                "stdout": result.stdout == saved["cell_result"]["stdout"],
                "error": result.error == saved["cell_result"]["error"],
                "working_model": result.working_model == saved["working_model"]["code"],
            })

        first_branch_turn = payload["prefix"]["trace"][-1]["turn"] + 1
        branch_trace = payload["branches"][arm]["trace"]
        acquisition_indices = [
            index for index, saved in enumerate(branch_trace)
            if "env.observe(" in saved["cell"] or "env.experiment(" in saved["cell"]
        ]
        # The scheduled report itself is evidence and arrives before the first
        # branch cell. If no later cell buys data, do not replay irrelevant
        # fitting/submission code merely to reconstruct the evidence ledger.
        last_needed = max(acquisition_indices, default=-1)
        if last_needed < 0:
            server.begin_turn(first_branch_turn, fire_events=(checkpoint == "fixed"))
            if checkpoint == "eligible":
                server.fire_event(0, turn_idx=first_branch_turn)
            server.pop_deliveries()

        for saved in branch_trace[:last_needed + 1]:
            server.begin_turn(saved["turn"], fire_events=(checkpoint == "fixed"))
            if checkpoint == "eligible" and saved["turn"] == first_branch_turn:
                server.fire_event(0, turn_idx=saved["turn"])
            for variable, frame in server.pop_deliveries():
                kernel.inject_dataframe(variable, frame)
            result = kernel.run_cell(saved["cell"])
            checks.append({
                "phase": "branch",
                "turn": saved["turn"],
                "stdout": result.stdout == saved["cell_result"]["stdout"],
                "error": result.error == saved["cell_result"]["error"],
                "working_model": result.working_model == saved["working_model"]["code"],
            })

    return server.export_evidence_ledger(), checks


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("path")
    parser.add_argument("--out", default=None)
    args = parser.parse_args()
    source = Path(args.path)
    payload = json.loads(source.read_text(encoding="utf-8"))
    result = {
        "kind": "replayed_legal_ledger_and_reference_no_llm",
        "source": str(source),
        "model": payload["model"],
        "seed_offset": payload["seed_offset"],
        "checkpoint": payload.get("checkpoint", "fixed"),
        "M_pre_phenotype": shared_transfer_phenotype(
            payload["prefix"]["trace"][-1]["working_model"]["code"]
        ),
        "arms": {},
    }
    for arm, case_dir in CASES.items():
        ledger, checks = replay_ledger(payload, arm)
        reference_code, diagnostics = build_reference_from_ledger(
            ledger,
            prior_code=payload["prefix"]["trace"][-1]["working_model"]["code"],
        )
        codes = _checkpoint_codes(payload, arm)
        codes["M_reference"] = reference_code
        scores = CheckpointScorer(case_dir).score_many(codes)
        fractions = {
            name: captured_reference_fraction(
                scores["M_pre"], scores[name], scores["M_reference"]
            )
            for name in ("M_post_first_changed", "M_final")
        }
        result["arms"][arm] = {
            "evidence_replay_exact": all(
                row["stdout"] and row["error"] and row["working_model"]
                for row in checks
            ),
            "replay_checks": checks,
            "evidence_ledger": ledger,
            "reference": {
                "code": reference_code,
                "diagnostics": diagnostics,
            },
            "checkpoint_scores": scores,
            "captured_fraction_diagnostic": fractions,
        }

    target = (
        Path(args.out) if args.out
        else source.with_name(source.stem + "_ledger_reference_v1.json")
    )
    target.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "out": str(target),
        "summary": {
            "M_pre_phenotype": result["M_pre_phenotype"],
            "arms": {
            arm: {
                "evidence_replay_exact": row["evidence_replay_exact"],
                "ledger_records": len(row["evidence_ledger"]),
                "updated_lines": row["reference"]["diagnostics"]["updated_lines"],
                "M_reference_diagnostic_R": row["checkpoint_scores"]["M_reference"]
                    ["groups"]["diagnostic"]["R"],
                "M_final_fraction": row["captured_fraction_diagnostic"]["M_final"],
            }
            for arm, row in result["arms"].items()
            },
        },
    }, indent=2))


if __name__ == "__main__":
    main()
