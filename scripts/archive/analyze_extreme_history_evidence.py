"""Compact deterministic analysis for exploratory history/evidence stress probes."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from wager.report.checkpoint_score import (  # noqa: E402
    CheckpointScorer,
    captured_reference_fraction,
)
from wager.report.overgen_belief import shared_transfer_phenotype  # noqa: E402


def _last_artifact(branch: dict):
    if branch.get("submission_code"):
        return "submission", branch["submission_code"]
    for row in reversed(branch.get("trace", [])):
        code = row.get("working_model", {}).get("code")
        if code:
            return f"working_model_t{row['turn']}", code
    return None, None


def summarize_file(path: Path) -> dict:
    raw = json.loads(path.read_text(encoding="utf-8"))
    rows = {}
    if not raw.get("branches") and raw.get("prefix", {}).get("trace"):
        prefix = raw["prefix"]
        code = prefix["trace"][-1].get("working_model", {}).get("code")
        revise = CheckpointScorer(ROOT / "cases" / "overgen_stream_v0").score(code)
        retain = CheckpointScorer(ROOT / "cases" / "overgen_stream_twin_v0").score(code)
        phenotype = shared_transfer_phenotype(code)
        rows["prefix_candidate"] = {
            "case_id": None,
            "variant": None,
            "history_mode": "prefix_only",
            "repeat": None,
            "accepted": None,
            "artifact_source": f"working_model_t{prefix['trace'][-1]['turn']}",
            "scoreable": bool(revise.get("scoreable") and retain.get("scoreable")),
            "R_pre": None,
            "R_last": revise.get("global_R"),
            "R_last_diagnostic": revise.get("groups", {}).get("diagnostic", {}).get("R"),
            "R_retain": retain.get("global_R"),
            "R_retain_diagnostic": retain.get("groups", {}).get("diagnostic", {}).get("R"),
            "F_last": None,
            "F_reason": None,
            "shared_shape_last": phenotype.get("eligible"),
            "turns": len(prefix["trace"]),
            "tokens": prefix.get("tokens"),
            "eligible": prefix.get("eligibility", {}).get("eligible"),
        }
    for name, branch in raw.get("branches", {}).items():
        source, code = _last_artifact(branch)
        case_dir = ROOT / "cases" / branch["case_id"]
        scores = branch.get("checkpoint_scores", {})
        pre = scores.get("M_pre", {})
        reference = scores.get("M_reference", {})
        if source == "submission":
            last = scores.get("M_final", {})
        elif code:
            last = CheckpointScorer(case_dir).score(code)
        else:
            last = {"scoreable": False, "global_R": None, "groups": {}}
        fraction = captured_reference_fraction(pre, last, reference)
        phenotype = shared_transfer_phenotype(code)
        rows[name] = {
            "case_id": branch["case_id"],
            "variant": branch.get("variant"),
            "history_mode": branch.get("history_mode", raw.get("history_mode", "native")),
            "repeat": branch.get("repeat"),
            "accepted": branch.get("accepted"),
            "artifact_source": source,
            "scoreable": last.get("scoreable"),
            "R_pre": pre.get("global_R"),
            "R_last": last.get("global_R"),
            "R_last_diagnostic": last.get("groups", {}).get("diagnostic", {}).get("R"),
            "F_last": fraction.get("fraction") if fraction.get("resolved") else None,
            "F_reason": fraction.get("reason"),
            "shared_shape_last": phenotype.get("eligible"),
            "turns": len(branch.get("trace", [])),
            "tokens": branch.get("tokens_continuation"),
        }
    return {
        "source": str(path),
        "model": raw.get("model"),
        "seed_offset": raw.get("seed_offset"),
        "rows": rows,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("paths", nargs="+", type=Path)
    parser.add_argument("--out", type=Path, default=None)
    args = parser.parse_args()
    result = {str(path): summarize_file(path) for path in args.paths}
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    for file_result in result.values():
        print(f"\n{file_result['source']} ({file_result['model']})")
        for name, row in file_result["rows"].items():
            print(
                f"  {name}: source={row['artifact_source']} "
                f"R={row['R_pre']}->{row['R_last']} F={row['F_last']} "
                f"R_retain={row.get('R_retain')} "
                f"shared={row['shared_shape_last']} accepted={row['accepted']}"
            )


if __name__ == "__main__":
    main()
