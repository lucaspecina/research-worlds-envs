"""Measure shared-vs-fragmented shape along saved real-agent trajectories."""

import argparse
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from wager.report.overgen_belief import shared_transfer_phenotype  # noqa: E402


def _codes(payload, arm):
    pre = payload["prefix"]["trace"][-1]["working_model"]["code"]
    trace = payload["branches"][arm]["trace"]
    first_changed = next(
        (row["working_model"]["code"] for row in trace
         if row["working_model"]["code"] is not None
         and row["working_model"]["code"] != pre),
        None,
    )
    return {
        "M_pre": pre,
        "M_post_first_changed": first_changed,
        "M_final": payload["branches"][arm]["submission_code"],
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("paths", nargs="+")
    parser.add_argument("--out", required=True)
    args = parser.parse_args()
    cache = {}
    donors = []
    for raw_path in map(Path, args.paths):
        payload = json.loads(raw_path.read_text(encoding="utf-8"))
        donor = {
            "source": str(raw_path),
            "model": payload["model"],
            "seed": payload["seed_offset"],
            "arms": {},
        }
        for arm in ("limited", "transfer"):
            donor["arms"][arm] = {}
            for name, code in _codes(payload, arm).items():
                if code is None:
                    result = {"eligible": False, "reason": "missing_artifact"}
                else:
                    key = hashlib.sha256(code.encode("utf-8")).hexdigest()
                    if key not in cache:
                        cache[key] = shared_transfer_phenotype(code)
                    result = cache[key]
                donor["arms"][arm][name] = result
        donors.append(donor)
    output = {
        "kind": "structural_shared_shape_trajectory_not_performance",
        "donors": donors,
    }
    target = Path(args.out)
    target.write_text(json.dumps(output, indent=2) + "\n", encoding="utf-8")
    compact = {}
    for donor in donors:
        compact[f"{donor['model']}:{donor['seed']}"] = {
            arm: {
                name: {
                    "ratio": row.get("shape_spread_noise_ratio"),
                    "absolute_spread": row.get("between_line_rms"),
                    "predictive_sd": row.get("predictive_sd"),
                }
                for name, row in checkpoints.items()
            }
            for arm, checkpoints in donor["arms"].items()
        }
    print(json.dumps({"out": str(target), "summary": compact}, indent=2))


if __name__ == "__main__":
    main()
