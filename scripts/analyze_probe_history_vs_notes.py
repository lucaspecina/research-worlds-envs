"""Zero-LLM post-hoc scoring for the history-vs-notes exploratory probe."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from wager.report.checkpoint_score import CheckpointScorer


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("path", type=Path)
    args = parser.parse_args()

    payload = json.loads(args.path.read_text(encoding="utf-8"))
    rows = {}
    for name, branch in payload["branches"].items():
        last_code = next(
            (
                turn.get("working_model", {}).get("code")
                for turn in reversed(branch["trace"])
                if turn.get("working_model", {}).get("code")
            ),
            None,
        )
        score = CheckpointScorer(Path("cases") / branch["case_id"]).score(last_code)
        rows[name] = {
            "accepted": branch["accepted"],
            "abort": branch["abort"],
            "last_working_hash": score.get("hash"),
            "last_working_R": score.get("global_R"),
            "last_working_R_unclipped": score.get("global_R_unclipped"),
            "last_working_diagnostic_R": score.get("groups", {})
            .get("diagnostic", {})
            .get("R"),
            "scoreable": score.get("scoreable"),
            "error": score.get("error"),
        }
    print(json.dumps(rows, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
