"""Re-score an existing technical fork with the cached checkpoint scorer."""

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from wager.report.checkpoint_score import CheckpointScorer  # noqa: E402
from wager.report.checkpoint_score import captured_reference_fraction  # noqa: E402
from wager.factory.overgen_stream_tools import build_reference_from_ledger  # noqa: E402

CASES = {
    "limited": ROOT / "cases" / "overgen_stream_v0",
    "transfer": ROOT / "cases" / "overgen_stream_twin_v0",
}


def checkpoint_codes(prefix, branch):
    pre = prefix["trace"][-1]["working_model"]["code"]
    first_seen = next(
        (row["working_model"]["code"] for row in branch["trace"]
         if row["working_model"]["code"] is not None),
        None,
    )
    first_changed = next(
        (row["working_model"]["code"] for row in branch["trace"]
         if row["working_model"]["code"] is not None
         and row["working_model"]["code"] != pre),
        None,
    )
    return {
        "M_pre": pre,
        "M_post_first_seen": first_seen,
        "M_post_first_changed": first_changed,
        "M_final": branch.get("submission_code"),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("path")
    parser.add_argument("--out", default=None)
    args = parser.parse_args()
    source = Path(args.path)
    payload = json.loads(source.read_text(encoding="utf-8"))
    result = {"source": str(source), "scores": {}, "references": {}}
    prior = payload["prefix"]["trace"][-1]["working_model"]["code"]
    for arm, case_dir in CASES.items():
        scorer = CheckpointScorer(case_dir)
        codes = checkpoint_codes(payload["prefix"], payload["branches"][arm])
        ledger = payload["branches"][arm].get("evidence_ledger")
        if ledger:
            reference_code, diagnostics = build_reference_from_ledger(
                ledger, prior_code=prior
            )
            codes["M_reference"] = reference_code
            result["references"][arm] = {"diagnostics": diagnostics}
        scores = scorer.score_many(codes)
        result["scores"][arm] = scores
        if "M_reference" in scores:
            result["references"][arm]["captured_fraction_diagnostic"] = {
                name: captured_reference_fraction(
                    scores["M_pre"], scores[name], scores["M_reference"]
                )
                for name in ("M_post_first_changed", "M_final")
            }
    target = Path(args.out) if args.out else source.with_name(source.stem + "_scores_v1.json")
    target.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    compact = {}
    for arm, checkpoints in result["scores"].items():
        compact[arm] = {}
        for name, score in checkpoints.items():
            groups = score.get("groups", {})
            compact[arm][name] = {
                "global": score.get("global_R"),
                "initial": (groups.get("initial") or {}).get("R"),
                "diagnostic": (groups.get("diagnostic") or {}).get("R"),
                "line_diagnostic": {
                    str(line): (groups.get(f"line_{line}_diagnostic") or {}).get("R")
                    for line in range(1, 6)
                },
            }
    print(json.dumps({"out": str(target), "scores": compact}, indent=2))


if __name__ == "__main__":
    main()
