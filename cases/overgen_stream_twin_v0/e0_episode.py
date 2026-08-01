"""One real-agent smoke for a longitudinal overgen pole (exploratory only)."""
import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from wager.harness.case_episode import build_world_server
from wager.harness.episode import run_episode


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", default=None)
    parser.add_argument("--seed-offset", type=int, default=0)
    parser.add_argument("--out", default=None)
    args = parser.parse_args()
    case = Path(__file__).parent
    result = run_episode(
        build_world_server(case, seed_offset=args.seed_offset),
        model=args.model,
        max_turns=18,
        capture_working_model=True,
    )
    target = Path(args.out) if args.out else case / f"smoke_{args.seed_offset}.json"
    target.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "case": case.name,
        "model": args.model,
        "R": result.get("R"),
        "turns": result.get("turns"),
        "abort": result.get("abort_reason"),
        "working_models": sum(
            t.get("working_model", {}).get("status") == "captured" for t in result["trace"]
        ),
        "out": str(target),
    }, indent=2))


if __name__ == "__main__":
    main()

