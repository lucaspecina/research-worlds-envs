"""Aggregate the frozen three-donor overgen probe at the donor level."""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "scripts" / "out" / "overgen_stream_fork"
SEEDS = (94100, 94101, 94102)


def _local(score, group="diagnostic"):
    return score["groups"][group]["R_unclipped"]


def main():
    donors = []
    for seed in SEEDS:
        raw_path = OUT / f"technical_DeepSeek-V3.2_seed{seed}_eligible.json"
        score_path = OUT / f"probe_DeepSeek-V3.2_seed{seed}_scores_v3.json"
        raw = json.loads(raw_path.read_text(encoding="utf-8"))
        derived = json.loads(score_path.read_text(encoding="utf-8"))
        eligibility = raw["prefix"]["eligibility"]
        prior = raw["prefix"]["trace"][-1]["working_model"]["code"]
        row = {
            "seed": seed,
            "eligible_turn": eligibility["turn"],
            "shape_spread_noise_ratio": eligibility["phenotype"][
                "shape_spread_noise_ratio"
            ],
            "M_pre_predictive_sd": eligibility["phenotype"]["predictive_sd"],
            "arms": {},
        }
        for arm in ("limited", "transfer"):
            branch = raw["branches"][arm]
            scores = derived["scores"][arm]
            changed = next(
                (item for item in branch["trace"]
                 if item["working_model"]["code"] is not None
                 and item["working_model"]["code"] != prior),
                None,
            )
            reference = derived["references"][arm]
            row["arms"][arm] = {
                "final_R": branch["R"],
                "post_turns": len(branch["trace"]),
                "first_changed_turn": None if changed is None else changed["turn"],
                "M_pre_diagnostic": _local(scores["M_pre"]),
                "M_first_changed_diagnostic": (
                    None if not scores["M_post_first_changed"]["scoreable"]
                    else _local(scores["M_post_first_changed"])
                ),
                "M_final_diagnostic": _local(scores["M_final"]),
                "M_reference_diagnostic": _local(scores["M_reference"]),
                "captured_fraction_final": reference[
                    "captured_fraction_diagnostic"
                ]["M_final"],
                "line_diagnostic_final": {
                    str(line): scores["M_final"]["groups"][
                        f"line_{line}_diagnostic"
                    ]["R_unclipped"]
                    for line in range(1, 6)
                },
            }
        row["paired_final_R_limited_minus_transfer"] = (
            row["arms"]["limited"]["final_R"]
            - row["arms"]["transfer"]["final_R"]
        )
        donors.append(row)

    payload = {
        "kind": "exploratory_three_donor_summary_not_inference",
        "model": "DeepSeek-V3.2",
        "seeds": list(SEEDS),
        "unit": "donor",
        "donors": donors,
    }
    target = OUT / "probe_DeepSeek-V3.2_94100_94102_summary_v1.json"
    target.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"out": str(target), "donors": donors}, indent=2))


if __name__ == "__main__":
    main()
