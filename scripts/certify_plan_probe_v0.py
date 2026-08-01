"""Build the server-side factory gate for the frozen plan probe v0.

No agent, API client, prompt, or episode harness is imported.  This script
evaluates one fixed consecutive cohort and writes its certificates.

Run:
    .venv/Scripts/python scripts/certify_plan_probe_v0.py
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from wager.factory.plan_probe_v0 import (  # noqa: E402
    VALIDATION_SEED_START,
    write_factory_report,
)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output",
        type=Path,
        default=ROOT / "scripts" / "out" / "probe_v0_plan" / "factory",
    )
    parser.add_argument("--count", type=int, default=8)
    parser.add_argument("--seed-start", type=int, default=VALIDATION_SEED_START)
    args = parser.parse_args()

    report = write_factory_report(
        args.output,
        count=args.count,
        candidate_seed_start=args.seed_start,
    )
    print(json.dumps({
        "all": report["all"],
        "fixed_cohort_count": report["fixed_cohort"]["count"],
        "failed_families": sum(
            not family["all"] for family in report["families"]
        ),
        "private_output": str(
            args.output / "private" / "factory_certification.json"
        ),
        "public_output": str(args.output / "public" / "manifest.json"),
    }, indent=2))
    return 0 if report["all"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
