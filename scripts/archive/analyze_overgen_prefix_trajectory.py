"""Audit when an overgen prefix contains a substantive executable belief."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from wager.report.checkpoint_score import CheckpointScorer  # noqa: E402
from wager.report.overgen_belief import shared_transfer_phenotype  # noqa: E402

CASE = ROOT / "cases" / "overgen_stream_v0"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("paths", nargs="+")
    parser.add_argument("--out", required=True)
    args = parser.parse_args()

    scorer = CheckpointScorer(CASE)
    runs = []
    for raw in map(Path, args.paths):
        payload = json.loads(raw.read_text(encoding="utf-8"))
        codes = {}
        turns = []
        for row in payload["prefix"]["trace"]:
            code = row["working_model"]["code"]
            name = f"t{row['turn']}"
            if code:
                codes[name] = code
            turns.append((row["turn"], name, code))
        scores = scorer.score_many(codes) if codes else {}
        trajectory = []
        for turn, name, code in turns:
            if not code:
                trajectory.append({"turn": turn, "artifact": False})
                continue
            shape = shared_transfer_phenotype(code)
            score = scores[name]
            trajectory.append({
                "turn": turn,
                "artifact": True,
                "shape_ratio": shape.get("shape_spread_noise_ratio"),
                "shape_shared": shape.get("eligible", False),
                "predictive_sd": shape.get("predictive_sd"),
                "R_global": score.get("global_R"),
                "R_line1": score.get("groups", {}).get("line_1", {}).get("R"),
                "R_initial": score.get("groups", {}).get("initial", {}).get("R"),
                "substantive_shared": bool(
                    shape.get("eligible", False)
                    and (score.get("groups", {}).get("line_1", {}).get("R") or 0) >= 0.60
                ),
            })
        runs.append({
            "source": str(raw),
            "model": payload["model"],
            "seed": payload["seed_offset"],
            "trajectory": trajectory,
        })

    output = {
        "kind": "exploratory_prefix_belief_maturity_audit",
        "substantive_definition": "shape_ratio<=1 and R_line1>=0.60",
        "runs": runs,
    }
    target = Path(args.out)
    target.write_text(json.dumps(output, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
