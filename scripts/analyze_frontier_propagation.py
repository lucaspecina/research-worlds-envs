"""Summarize frontier belief-to-plan propagation probes without inflating donor n."""

from __future__ import annotations

import argparse
import glob
import json
import math
from pathlib import Path
from typing import Any


def _expand_paths(patterns: list[str]) -> list[Path]:
    paths: list[Path] = []
    for pattern in patterns:
        matches = [Path(match) for match in glob.glob(pattern)]
        if not matches and Path(pattern).is_file():
            matches = [Path(pattern)]
        paths.extend(matches)
    return sorted(set(path.resolve() for path in paths))


def _number(value: Any) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(value)


def _branch_rows(path: Path) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    raw = json.loads(path.read_text(encoding="utf-8"))
    technical = raw.get("technical_gates") or {}
    technical_passed = raw.get("all_technical_gates")
    rows: list[dict[str, Any]] = []

    for branch_name, branch in (raw.get("branches") or {}).items():
        summary = (raw.get("summary") or {}).get(branch_name, {})
        certification = (raw.get("certifications") or {}).get(branch_name, {})
        plan_audits = branch.get("plan_audits") or []
        initial_plan_valid = bool(plan_audits and plan_audits[0].get("valid") is True)
        branch_technical_passed = bool(
            certification.get("all_gates") is True
            and branch.get("replay_exact") is True
            and initial_plan_valid
            and branch.get("report_rows") == 64
        )
        f_model = summary.get("F_model_final")
        valid = bool(
            summary.get("accepted") is True
            and branch_technical_passed
            and _number(f_model)
        )
        rows.append(
            {
                "donor_seed": raw.get("seed_offset"),
                "file": path.name,
                "path": str(path),
                "explicit_handoff": raw.get("explicit_handoff") is True,
                "consistency_reminder": raw.get("consistency_reminder") is True,
                "pole": branch.get("pole"),
                "radius": branch.get("radius"),
                "accepted": summary.get("accepted"),
                "abort": summary.get("abort"),
                "F_model": f_model,
                "F_model_reason": summary.get("F_model_reason"),
                "valid_F_model": valid,
                "assimilated_F_gt_0_8": bool(valid and f_model > 0.8),
                "required_changes_propagated": summary.get("required_changes_propagated"),
                "truth_accuracy": summary.get("final_truth_accuracy"),
                "model_coherence": summary.get("final_model_coherence"),
                "post_report_turns": summary.get("post_report_turns"),
                "technical_gates_passed": branch_technical_passed,
                "payload_technical_gates_passed": technical_passed,
                "technical_gates": technical,
            }
        )
    metadata = {
        "path": str(path),
        "kind": raw.get("kind"),
        "donor_seed": raw.get("seed_offset"),
        "branch_count": len(rows),
    }
    return rows, metadata


def _explicit_radius1_by_donor(
    rows: list[dict[str, Any]], *, consistency_reminder: bool
) -> dict[str, Any]:
    selected = [
        row for row in rows
        if row["explicit_handoff"]
        and row["radius"] == "radius1"
        and row["consistency_reminder"] is consistency_reminder
    ]
    grouped: dict[Any, list[dict[str, Any]]] = {}
    for row in selected:
        grouped.setdefault(row["donor_seed"], []).append(row)

    donor_rows: list[dict[str, Any]] = []
    for donor_seed, donor_branches in sorted(grouped.items(), key=lambda item: str(item[0])):
        revise = [row for row in donor_branches if row["pole"] == "revise"]
        retain = [row for row in donor_branches if row["pole"] == "retain"]
        valid_revise = [row for row in revise if row["valid_F_model"]]
        assimilated = [row for row in valid_revise if row["assimilated_F_gt_0_8"]]
        gaps = [
            row
            for row in assimilated
            if _number(row["required_changes_propagated"])
            and row["required_changes_propagated"] < 1.0
        ]
        clean_retain = [
            row
            for row in retain
            if row["accepted"] is True
            and row["technical_gates_passed"] is True
            and row["truth_accuracy"] == 1.0
            and row["model_coherence"] == 1.0
        ]
        donor_rows.append(
            {
                "donor_seed": donor_seed,
                "continuation_files": sorted({row["file"] for row in donor_branches}),
                "revise_continuations": len(revise),
                "valid_revise": len(valid_revise),
                "assimilated_revise": len(assimilated),
                "gap_among_assimilated": len(gaps),
                "retain_continuations": len(retain),
                "clean_retain": len(clean_retain),
            }
        )

    return {
        "consistency_reminder": consistency_reminder,
        "definition": {
            "valid_revise": "accepted, all technical gates pass, and F_model is finite",
            "assimilated": "valid REVISE with F_model > 0.8",
            "gap_among_assimilated": "assimilated REVISE with required_changes_propagated < 1",
            "clean_retain": "accepted RETAIN with all gates, truth_accuracy=1, model_coherence=1",
        },
        "donors": donor_rows,
        "donor_counts": {
            "total": len(donor_rows),
            "with_valid_revise": sum(row["valid_revise"] > 0 for row in donor_rows),
            "with_assimilated_revise": sum(row["assimilated_revise"] > 0 for row in donor_rows),
            "with_gap_among_assimilated": sum(row["gap_among_assimilated"] > 0 for row in donor_rows),
            "with_clean_retain": sum(row["clean_retain"] > 0 for row in donor_rows),
        },
    }


def _format(value: Any) -> str:
    if value is None:
        return "-"
    if isinstance(value, float):
        return f"{value:.3f}"
    if isinstance(value, bool):
        return "Y" if value else "N"
    return str(value)


def _print_table(rows: list[dict[str, Any]]) -> None:
    columns = [
        ("seed", "donor_seed"),
        ("file", "file"),
        ("pole", "pole"),
        ("radius", "radius"),
        ("accepted", "accepted"),
        ("abort", "abort"),
        ("F_model", "F_model"),
        ("assim", "assimilated_F_gt_0_8"),
        ("prop", "required_changes_propagated"),
        ("truth", "truth_accuracy"),
        ("coherent", "model_coherence"),
        ("turns", "post_report_turns"),
        ("gates", "technical_gates_passed"),
    ]
    rendered = [[_format(row[key]) for _, key in columns] for row in rows]
    widths = [len(label) for label, _ in columns]
    for values in rendered:
        widths = [max(width, len(value)) for width, value in zip(widths, values, strict=True)]
    print("  ".join(label.ljust(width) for (label, _), width in zip(columns, widths, strict=True)))
    print("  ".join("-" * width for width in widths))
    for values in rendered:
        print("  ".join(value.ljust(width) for value, width in zip(values, widths, strict=True)))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("paths", nargs="+", help="JSON paths or glob patterns")
    parser.add_argument("--out", type=Path, help="optional JSON output path")
    args = parser.parse_args()

    paths = _expand_paths(args.paths)
    if not paths:
        parser.error("no input files matched")

    rows: list[dict[str, Any]] = []
    files: list[dict[str, Any]] = []
    for path in paths:
        file_rows, metadata = _branch_rows(path)
        rows.extend(file_rows)
        files.append(metadata)

    payload = {
        "files": files,
        "branches": rows,
        "explicit_handoff_radius1": _explicit_radius1_by_donor(
            rows, consistency_reminder=False
        ),
        "consistency_reminder_radius1": _explicit_radius1_by_donor(
            rows, consistency_reminder=True
        ),
    }
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")

    _print_table(rows)
    for label, key in (
        ("Explicit-handoff radius1, no reminder", "explicit_handoff_radius1"),
        ("Generic consistency reminder radius1", "consistency_reminder_radius1"),
    ):
        aggregate = payload[key]
        print(f"\n{label} (continuations nested within donor):")
        for row in aggregate["donors"]:
            print(
                f"  seed={row['donor_seed']} continuations={len(row['continuation_files'])} "
                f"REVISE valid={row['valid_revise']}/{row['revise_continuations']} "
                f"assimilated={row['assimilated_revise']} "
                f"gaps={row['gap_among_assimilated']} "
                f"RETAIN clean={row['clean_retain']}/{row['retain_continuations']}"
            )
        counts = aggregate["donor_counts"]
        print(
            "  unique donors: "
            f"total={counts['total']} valid_REVISE={counts['with_valid_revise']} "
            f"assimilated={counts['with_assimilated_revise']} "
            f"gap={counts['with_gap_among_assimilated']} "
            f"clean_RETAIN={counts['with_clean_retain']}"
        )


if __name__ == "__main__":
    main()
