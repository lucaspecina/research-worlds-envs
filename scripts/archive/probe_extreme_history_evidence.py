"""Exploratory stress test: one genuinely lived long history, dirtier evidence.

This is deliberately a small research runner, not a new general framework.  It
replays the already-generated DeepSeek 94101 donor byte-for-byte, fires the
ordinary commissioning event, and varies only the composition of that report.
See docs/research/2026-08-01-ficha-stress-historial-real-y-evidencia-enterrada-v0.md.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import sys
from pathlib import Path
from types import SimpleNamespace

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from wager.agent.cells import extract_cell  # noqa: E402
from wager.agent.llm_client import FoundryChat  # noqa: E402
from wager.factory.overgen_stream_tools import build_reference_from_ledger  # noqa: E402
from wager.harness.case_episode import build_world_server  # noqa: E402
from wager.harness.episode import (  # noqa: E402
    CELL_TIMEOUT_S,
    MAX_COMPLETION_TOKENS,
    SYSTEM,
)
from wager.harness.kernel_proc import KernelClient  # noqa: E402
from wager.report.checkpoint_score import CheckpointScorer  # noqa: E402
from wager.report.overgen_belief import shared_transfer_phenotype  # noqa: E402

from scripts.fork_overgen_stream_v0 import (  # noqa: E402
    LIMITED,
    OUT,
    TRANSFER,
    _record,
    score_checkpoints,
)
from scripts.probe_history_vs_notes_94101 import (  # noqa: E402
    DEFAULT_DONOR,
    reconstruct_messages,
)

VARIANTS = ("clean64", "conflict256", "buried256")
HISTORY_MODES = (
    "native", "synthetic_self_visible", "fresh_snapshot_workspace",
    "fresh_compacted_no_hint", "other_attributed_transcript",
    "neutral_length_matched_archive", "matched_relevance_archive",
)
ARCHIVE_PROFILES = ("neutral", "early", "commitment", "full")


def _frame_hash(frame: pd.DataFrame) -> str:
    raw = frame.to_csv(index=False, float_format="%.12g").encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def _synthetic_self_visible_history(messages: list[dict], turns: int) -> list[dict]:
    """Append a plausible but explicitly researcher-authored visible past.

    Every claim is compatible with the byte-identical pre-commissioning region:
    line 1 fixes the shared full-range law and lines 2-5 agree in their available
    low range.  The extension adds commitment and context, not hidden evidence.
    It is an elicitation control and must never be described as lived authorship.
    """
    out = copy.deepcopy(messages)
    uses = (
        "quarterly downside envelope", "permit-margin table", "shift schedule",
        "supplier allocation memo", "maintenance forecast", "operator playbook",
        "quality-control dashboard", "capacity plan",
    )
    anchors = (0.5, 1.5, 2.5, 3.5)
    for index in range(1, turns + 1):
        use = uses[(index - 1) % len(uses)]
        phase = 1 + (index - 1) // len(uses)
        rows = []
        for line in (1, 2, 3, 4, 5):
            for driver in anchors:
                # These are notebook expectations, not additional world samples.
                mean = 14.0 + 8.0 * driver * (10.0 - driver) / 25.0
                rows.append(f"L{line},d={driver:.1f},forecast={mean:.3f}")
        forecast_block = "\n".join(rows)
        reasoning = f"""REASONING: Project checkpoint {index:02d}, phase {phase}. The archived
shared response law remains the operational model. Line 1 supplies the full-range shape, while
all currently commissioned observations for lines 2-5 remain in the low range and agree with
that same shape within ordinary batch noise. I used the executable model for the {use}; changing
to five unrelated curves at this stage would throw away the only identified high-range shape.
This is still a provisional scientific conclusion, but it has now propagated into routine
planning. The next scheduled source of genuinely discriminating information remains the normal
range-extension inbox; until it arrives, the honest action is to archive the current model and
record its implications rather than invent line-specific high-range behavior.

ARCHIVED FORECAST CHECK {index:02d}:
{forecast_block}

No new measurement was produced in this local checkpoint. The table records consequences of the
current executable model so later commissioning residuals can be compared against a frozen view.
"""
        cell = (
            "checkpoint = {"
            f"'index': {index}, 'phase': {phase}, 'use': {use!r}, "
            "'status': 'shared-law model archived; awaiting routine extension'}\n"
            "print(checkpoint)"
        )
        out.append({
            "role": "assistant",
            "content": reasoning + f"\n```python\n{cell}\n```",
        })
        out.append({
            "role": "user",
            "content": (
                "Kernel output (ok=True, budget remaining=300):\n"
                + repr({
                    "index": index,
                    "phase": phase,
                    "use": use,
                    "status": "shared-law model archived; awaiting routine extension",
                })
                + "\n\nContinue the rolling investigation when the next routine project "
                  "input becomes available."
            ),
        })
    return out


def _history_messages(messages: list[dict], mode: str, turns: int) -> list[dict]:
    if mode == "native":
        return copy.deepcopy(messages)
    if mode == "synthetic_self_visible":
        return _synthetic_self_visible_history(messages, turns)
    if mode in (
        "fresh_snapshot_workspace", "fresh_compacted_no_hint",
        "other_attributed_transcript",
        "neutral_length_matched_archive",
        "matched_relevance_archive",
    ):
        return [{"role": "system", "content": SYSTEM}]
    raise ValueError(mode)


def _fresh_snapshot_prompt(
    server, notices: list[str], mpre: str, *, include_balanced_hint: bool
) -> str:
    sheet = server.describe()
    machine = {key: value for key, value in sheet.items() if key != "brief"}
    return (
        "The same rolling investigation is continuing after automatic chat compaction. "
        "The full Python workspace from the earlier work is still live."
        + (
            " Do not assume that the archived model is right or wrong."
            if include_balanced_hint else ""
        )
        + "\n\n"
        f"BRIEF:\n{sheet['brief']}\n\n"
        f"MACHINE-READABLE SHEET:\n{json.dumps(machine, indent=2)}\n\n"
        f"CURRENT EXECUTABLE MODEL:\n```python\n{mpre}\n```\n\n"
        f"ROUTINE UPDATE:\n{' '.join(notices)}\n"
        "The delivered rows are loaded as DataFrame `commissioning_report`. Continue the "
        "investigation using the live workspace and submit the best executable model when ready. "
        "Write reasoning followed by exactly one Python cell."
    )


def _other_attributed_archive(messages: list[dict]) -> str:
    chunks = []
    for index, message in enumerate(messages):
        if message["role"] == "system":
            continue
        chunks.append(
            f"--- archived message {index:03d} / role={message['role']} ---\n"
            + message["content"]
        )
    return (
        "ARCHIVED TRANSCRIPT FOR CONTINUITY\n"
        "The following transcript was produced by an independent earlier analyst working "
        "in this same project workspace. It is preserved verbatim.\n\n"
        + "\n\n".join(chunks)
        + "\n\nEND ARCHIVED TRANSCRIPT\n\n"
    )


def _neutral_length_matched_archive(messages: list[dict]) -> str:
    target = len(_other_attributed_archive(messages))
    chunks = [
        "NEUTRAL OPERATIONS ARCHIVE\n"
        "Administrative continuity records unrelated to the scientific response model.\n\n"
    ]
    index = 0
    topics = (
        "PPE inventory", "freezer calibration", "badge renewal", "shipping manifest",
        "fire-drill roster", "software checksum", "bench reservation", "waste pickup",
        "network maintenance", "training attendance", "cabinet audit", "UPS inspection",
    )
    while sum(map(len, chunks)) < target:
        topic = topics[index % len(topics)]
        rows = []
        for row in range(12):
            checksum = (index * 7919 + row * 104729) % 1_000_003
            rows.append(
                f"record={index:04d}-{row:02d}, topic={topic}, status=closed, "
                f"ticket={checksum:06d}, owner=ops-{(index + row) % 17:02d}"
            )
        chunks.append(
            f"ADMIN CHECKPOINT {index:04d}\n"
            f"Routine {topic} reconciliation completed. This entry contains no experimental "
            "measurement, forecast, hypothesis, or recommendation about the production process.\n"
            + "\n".join(rows)
            + "\n\n"
        )
        index += 1
    archive = "".join(chunks)
    return archive[:target]


def _neutral_message(length: int, index: int, role: str) -> str:
    """Create semantically inert content with exactly ``length`` characters."""
    topics = (
        "PPE inventory", "badge renewal", "shipping manifest", "fire-drill roster",
        "software checksum", "bench reservation", "waste pickup", "UPS inspection",
    )
    pieces = []
    row = 0
    while sum(map(len, pieces)) < length:
        topic = topics[(index + row) % len(topics)]
        checksum = (index * 104729 + row * 7919) % 1_000_003
        pieces.append(
            f"Administrative archive record {index:03d}-{row:03d}; role={role}; "
            f"topic={topic}; status=closed; ticket={checksum:06d}. "
            "This record contains no production-process measurement, forecast, "
            "hypothesis, model, or scientific recommendation.\n"
        )
        row += 1
    return "".join(pieces)[:length]


def _matched_relevance_archive(messages: list[dict], profile: str) -> str:
    """Hold archive structure/length fixed while varying relevant semantic content.

    ``early`` preserves turns 1--6, before the final shared-shape commitment.
    ``commitment`` preserves turns 9--12, where the donor consolidated and encoded
    that commitment.  All removed messages are replaced character-for-character
    by neutral administrative prose in the same positions.
    """
    if profile not in ARCHIVE_PROFILES:
        raise ValueError(profile)
    archived = [message for message in messages if message["role"] != "system"]
    preserve: set[int]
    if profile == "neutral":
        preserve = set()
    elif profile == "early":
        preserve = set(range(min(12, len(archived))))
    elif profile == "commitment":
        preserve = set(range(max(0, len(archived) - 8), len(archived)))
    else:
        preserve = set(range(len(archived)))

    chunks = []
    for ordinal, message in enumerate(archived):
        content = message["content"]
        if ordinal not in preserve:
            content = _neutral_message(len(content), ordinal, message["role"])
        chunks.append(
            f"--- archived message {ordinal + 1:03d} / role={message['role']} ---\n"
            + content
        )
    return (
        "ARCHIVED TRANSCRIPT FOR CONTINUITY\n"
        "The following transcript was produced by an independent earlier analyst working "
        "in this same project workspace. It is preserved verbatim where scientific content "
        "is retained; redacted slots contain length-matched administrative records.\n\n"
        + "\n\n".join(chunks)
        + "\n\nEND ARCHIVED TRANSCRIPT\n\n"
    )


def _routine_rows(base_sample, *, n: int, seed: int, kind: str) -> pd.DataFrame:
    """Generate truthful filler without reading hidden truth directly.

    ``conflict`` contains evidence that supports the old transfer story: line 1
    over its full range plus lines 2-5 only where the common law really holds.
    ``low_only`` is the stronger version used when only 16 diagnostic rows are
    retained.
    """
    rng = np.random.default_rng(seed + 31_337)
    designs: list[tuple[int, float]] = []
    if kind == "conflict":
        line1_n = min(64, n)
        designs.extend((1, float(d)) for d in rng.uniform(0.0, 10.0, line1_n))
    anchors = (0.5, 1.5, 2.5, 3.5)
    remaining = n - len(designs)
    cycle = [(line, driver) for line in (2, 3, 4, 5) for driver in anchors]
    designs.extend(cycle[i % len(cycle)] for i in range(remaining))
    rows = []
    for j, (line, driver) in enumerate(designs):
        row = base_sample(
            SimpleNamespace(
                config={"line": int(line), "driver": float(driver)},
                context={},
                horizon=None,
            ),
            1,
            int(seed + 40_000 + j),
        ).iloc[0]
        rows.append({
            "line": float(line),
            "driver": float(driver),
            "outcome": float(row["outcome"]),
        })
    return pd.DataFrame(rows)


def _report_sampler(base_sample, variant: str):
    def sample(regime, n, seed):
        if "__commissioning" not in regime.config:
            return base_sample(regime, n, seed)
        if variant == "clean64":
            return base_sample(regime, n, seed)
        if n != 256:
            raise ValueError(f"{variant} report requires exactly 256 rows")

        full = base_sample(regime, 64, seed).copy()
        if variant == "conflict256":
            diagnostic = full
            filler = _routine_rows(base_sample, n=192, seed=seed, kind="conflict")
        elif variant == "buried256":
            high = full[full["driver"] > 4.0]
            diagnostic = (
                high.groupby("line", sort=True, group_keys=False)
                .head(4)
                .reset_index(drop=True)
            )
            if len(diagnostic) != 16:
                raise RuntimeError("failed to select four high-range rows per line")
            filler = _routine_rows(base_sample, n=240, seed=seed, kind="low_only")
        else:
            raise ValueError(variant)
        combined = pd.concat([diagnostic, filler], ignore_index=True)
        rng = np.random.default_rng(seed + 71_171)
        return combined.iloc[rng.permutation(len(combined))].reset_index(drop=True)

    return sample


def _build_variant_server(case_dir: Path, seed_offset: int, variant: str):
    server = build_world_server(case_dir, seed_offset=seed_offset)
    if variant == "clean64":
        return server
    event = server.config.events[0]
    source = event.source.model_copy(update={"max_rows": 256})
    event = event.model_copy(update={"source": source, "auto_deliver_n": 256})
    server.config = server.config.model_copy(update={"events": [event]})
    server.world_sample = _report_sampler(server.world_sample, variant)
    return server


def _error_signature(error: str | None) -> str | None:
    if not error:
        return None
    lines = [line.strip() for line in error.splitlines() if line.strip()]
    return lines[-1] if lines else None


def _replay_prefix(server, prefix, kernel):
    """Replay scientific state exactly, tolerating presentation-only drift.

    The donor predates the current statsmodels/pandas environment.  Its table
    formatting and traceback paths are not stable across library revisions;
    server actions, success/failure class, terminal exception message and the
    captured executable artifact are the causal state that must match.
    """
    checks = []
    for donor in prefix["trace"]:
        notices = server.begin_turn(donor["turn"], fire_events=False)
        deliveries = server.pop_deliveries()
        start = len(server.trajectory)
        result = kernel.run_cell(donor["cell"])
        expected = donor["cell_result"]
        actual_trajectory = [
            {"verb": event.verb, "args": event.args, "cost": event.cost}
            for event in server.trajectory[start:]
        ]
        expected_trajectory = [
            {"verb": event["verb"], "args": event["args"], "cost": event["cost"]}
            for event in donor["trajectory"]
        ]
        checks.append({
            "turn": donor["turn"],
            "no_notice_or_delivery": not notices and not deliveries,
            "ok": bool(result.ok) == bool(expected["ok"]),
            "error_signature": (
                _error_signature(result.error) == _error_signature(expected["error"])
            ),
            "actual_error_signature_diagnostic": _error_signature(result.error),
            "expected_error_signature_diagnostic": _error_signature(expected["error"]),
            "working_model": result.working_model == donor["working_model"]["code"],
            "working_model_status": (
                result.working_model_status == donor["working_model"]["status"]
            ),
            "trajectory": actual_trajectory == expected_trajectory,
            "stdout_exact_diagnostic": result.stdout == expected["stdout"],
            "error_exact_diagnostic": result.error == expected["error"],
        })
    return checks


def _state_replay_exact(checks: list[dict]) -> bool:
    diagnostics = {
        "turn", "stdout_exact_diagnostic", "error_exact_diagnostic",
        "actual_error_signature_diagnostic", "expected_error_signature_diagnostic",
    }
    return all(
        all(value for key, value in row.items() if key not in diagnostics)
        for row in checks
    )


def _fire_report(server, prefix, kernel):
    replay_checks = _replay_prefix(server, prefix, kernel)
    turn = prefix["trace"][-1]["turn"] + 1
    notices = server.begin_turn(turn, fire_events=False)
    notices.extend(server.fire_event(0, turn_idx=turn))
    deliveries = server.pop_deliveries()
    if len(deliveries) != 1 or deliveries[0][0] != "commissioning_report":
        raise RuntimeError("expected exactly one commissioning_report")
    report = deliveries[0][1]
    kernel.inject_dataframe("commissioning_report", report)
    return turn, notices, report, replay_checks


def certify_cell(case_dir: Path, prefix: dict, seed_offset: int, variant: str) -> dict:
    server = _build_variant_server(case_dir, seed_offset, variant)
    with KernelClient(server, cell_timeout_s=CELL_TIMEOUT_S) as kernel:
        _, _, report, replay_checks = _fire_report(server, prefix, kernel)
    mpre = prefix["trace"][-1]["working_model"]["code"]
    reference, diagnostics = build_reference_from_ledger(
        server.export_evidence_ledger(), prior_code=mpre
    )
    scorer = CheckpointScorer(case_dir)
    scores = scorer.score_many({"M_pre": mpre, "M_reference": reference})
    gain = None
    if scores["M_pre"]["scoreable"] and scores["M_reference"]["scoreable"]:
        gain = (
            scores["M_reference"]["groups"]["diagnostic"]["R"]
            - scores["M_pre"]["groups"]["diagnostic"]["R"]
        )
    return {
        "replay_checks": replay_checks,
        "replay_exact": _state_replay_exact(replay_checks),
        "report_rows": len(report),
        "report_hash": _frame_hash(report),
        "high_rows_by_line": {
            str(int(line)): int(len(group[group["driver"] > 4.0]))
            for line, group in report.groupby("line")
        },
        "reference_diagnostics": diagnostics,
        "diagnostic_R_pre": scores["M_pre"]["groups"]["diagnostic"]["R"],
        "diagnostic_R_reference": scores["M_reference"]["groups"]["diagnostic"]["R"],
        "diagnostic_reference_gain": gain,
    }


def continue_cell(
    case_dir: Path,
    variant: str,
    repeat: int,
    prefix: dict,
    full_messages: list[dict],
    model: str,
    seed_offset: int,
    max_turns: int,
    history_mode: str,
    synthetic_turns: int,
    archive_profile: str,
) -> dict:
    server = _build_variant_server(case_dir, seed_offset, variant)
    with KernelClient(server, cell_timeout_s=CELL_TIMEOUT_S) as kernel:
        first_turn, notices, report, replay_checks = _fire_report(server, prefix, kernel)
        chat = FoundryChat(
            system=SYSTEM,
            model=model,
            max_completion_tokens=MAX_COMPLETION_TOKENS,
        )
        chat.messages = _history_messages(full_messages, history_mode, synthetic_turns)
        mpre = prefix["trace"][-1]["working_model"]["code"]
        if history_mode in ("fresh_snapshot_workspace", "fresh_compacted_no_hint"):
            prompt = _fresh_snapshot_prompt(
                server, notices, mpre,
                include_balanced_hint=(history_mode == "fresh_snapshot_workspace"),
            )
        elif history_mode == "other_attributed_transcript":
            prompt = _other_attributed_archive(full_messages) + _fresh_snapshot_prompt(
                server, notices, mpre, include_balanced_hint=False,
            )
        elif history_mode == "neutral_length_matched_archive":
            prompt = _neutral_length_matched_archive(full_messages) + _fresh_snapshot_prompt(
                server, notices, mpre, include_balanced_hint=False,
            )
        elif history_mode == "matched_relevance_archive":
            prompt = _matched_relevance_archive(
                full_messages, archive_profile
            ) + _fresh_snapshot_prompt(
                server, notices, mpre, include_balanced_hint=False,
            )
        else:
            prompt = "\n".join(f"[NOTICE] {notice}" for notice in notices)
            prompt += "\n\n" + prefix["next_prompt"]
        trace = []
        abort = "max_turns"
        for offset in range(max_turns):
            turn = first_turn + offset
            if offset:
                server.begin_turn(turn, fire_events=False)
            start = len(server.trajectory)
            reply = chat.ask(prompt)
            cell = extract_cell(reply.content)
            if cell is None:
                abort = "no_cell"
                break
            result = kernel.run_cell(cell)
            trace.append(_record(
                turn, reply, cell, result, server,
                notices if offset == 0 else [], start,
            ))
            if server.terminal:
                abort = "submitted"
                break
            if result.error and result.error.startswith("cell exceeded "):
                abort = "cell_timeout"
                break
            prompt = (
                f"Kernel output (ok={result.ok}, budget remaining="
                f"{server.budget_remaining:.0f}):\n" + (result.stdout or "(no stdout)")
            )
            if result.error:
                prompt += "\nTRACEBACK:\n" + result.error
            prompt += (
                "\n\nContinue with the most useful next cell. If you attempted delivery, "
                "inspect whether it was accepted before treating the project as complete."
            )

    final = server.result or {}
    branch = {
        "case_id": case_dir.name,
        "variant": variant,
        "repeat": repeat,
        "history_mode": history_mode,
        "synthetic_turns": synthetic_turns,
        "archive_profile": archive_profile,
        "replay_checks": replay_checks,
        "replay_exact": _state_replay_exact(replay_checks),
        "report_rows": len(report),
        "report_hash": _frame_hash(report),
        "abort": abort,
        "accepted": server.terminal,
        "R": final.get("R"),
        "submission_code": final.get("code"),
        "trace": trace,
        "evidence_ledger": server.export_evidence_ledger(),
        "tokens_continuation": chat.usage.total_tokens,
        "llm_turn_usage": [
            {
                "prompt_tokens": turn.prompt_tokens,
                "completion_tokens": turn.completion_tokens,
                "reasoning_tokens": turn.reasoning_tokens,
                "latency_s": turn.latency_s,
            }
            for turn in chat.turns
        ],
    }
    mpre = prefix["trace"][-1]["working_model"]["code"]
    reference, diagnostics = build_reference_from_ledger(
        branch["evidence_ledger"], prior_code=mpre
    )
    scores, fractions = score_checkpoints(
        prefix, branch, CheckpointScorer(case_dir), reference
    )
    branch["reference_diagnostics"] = diagnostics
    branch["captured_fraction"] = fractions
    branch["checkpoint_scores"] = scores
    branch["final_phenotype"] = shared_transfer_phenotype(final.get("code"))
    return branch


def _brief_result(branch: dict) -> dict:
    fraction = branch["captured_fraction"]["M_final"]
    pre = branch["checkpoint_scores"]["M_pre"]
    final = branch["checkpoint_scores"]["M_final"]
    return {
        "accepted": branch["accepted"],
        "abort": branch["abort"],
        "R_pre": pre.get("global_R"),
        "R_final": final.get("global_R"),
        "F_final": fraction.get("fraction") if fraction.get("resolved") else None,
        "F_reason": fraction.get("reason"),
        "shared_shape_final": branch["final_phenotype"].get("eligible"),
        "turns": len(branch["trace"]),
        "tokens": branch["tokens_continuation"],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--donor", type=Path, default=DEFAULT_DONOR)
    parser.add_argument("--model", default="DeepSeek-V3.2")
    parser.add_argument("--seed-offset", type=int, default=94101)
    parser.add_argument("--variants", nargs="+", choices=VARIANTS, default=list(VARIANTS))
    parser.add_argument("--repeats", type=int, default=1)
    parser.add_argument("--max-turns", type=int, default=8)
    parser.add_argument("--history-mode", choices=HISTORY_MODES, default="native")
    parser.add_argument("--synthetic-turns", type=int, default=48)
    parser.add_argument("--archive-profile", choices=ARCHIVE_PROFILES, default="neutral")
    parser.add_argument(
        "--poles", nargs="+", choices=("revise", "retain"),
        default=["revise", "retain"],
    )
    parser.add_argument("--out", type=Path, default=None)
    args = parser.parse_args()

    raw = json.loads(args.donor.read_text(encoding="utf-8"))
    prefix = raw["prefix"]
    mpre = prefix["trace"][-1]["working_model"]["code"]
    if not mpre:
        raise RuntimeError("donor has no M_pre")
    full_messages = reconstruct_messages(prefix, args.seed_offset)

    certifications = {}
    for variant in args.variants:
        for pole, case_dir in (("revise", LIMITED), ("retain", TRANSFER)):
            if pole not in args.poles:
                continue
            certifications[f"{pole}__{variant}"] = certify_cell(
                case_dir, prefix, args.seed_offset, variant
            )

    target = args.out or (
        OUT / f"probe_extreme_history_{args.model}_seed{args.seed_offset}.json"
    )
    payload = {
        "kind": "exploratory_lived_history_evidence_stress_not_prevalence",
        "model": args.model,
        "seed_offset": args.seed_offset,
        "donor": str(args.donor),
        "variants": args.variants,
        "repeats": args.repeats,
        "history_mode": args.history_mode,
        "synthetic_turns": args.synthetic_turns,
        "archive_profile": args.archive_profile,
        "poles": args.poles,
        "prefix": {
            "turns": len(prefix["trace"]),
            "tokens": prefix.get("tokens"),
            "M_pre_hash": hashlib.sha256(mpre.encode("utf-8")).hexdigest(),
            "eligibility": prefix.get("eligibility"),
        },
        "certifications": certifications,
        "branches": {},
    }
    target.parent.mkdir(parents=True, exist_ok=True)

    for repeat in range(args.repeats):
        for variant in args.variants:
            for pole, case_dir in (("revise", LIMITED), ("retain", TRANSFER)):
                if pole not in args.poles:
                    continue
                name = f"r{repeat}__{pole}__{variant}"
                branch = continue_cell(
                    case_dir, variant, repeat, prefix, full_messages, args.model,
                    args.seed_offset, args.max_turns, args.history_mode,
                    args.synthetic_turns, args.archive_profile,
                )
                payload["branches"][name] = branch
                target.write_text(
                    json.dumps(payload, indent=2) + "\n", encoding="utf-8"
                )
                print(name, json.dumps(_brief_result(branch)), flush=True)

    payload["summary"] = {
        name: _brief_result(branch) for name, branch in payload["branches"].items()
    }
    payload["gates"] = {
        "cert_replay_exact": all(
            row["replay_exact"] for row in certifications.values()
        ),
        "revise_reference_gain_positive": all(
            certifications[f"revise__{variant}"]["diagnostic_reference_gain"] > 0.10
            for variant in args.variants
        ) if "revise" in args.poles else True,
        "retain_reference_gain_small": all(
            abs(certifications[f"retain__{variant}"]["diagnostic_reference_gain"]) < 0.05
            for variant in args.variants
        ) if "retain" in args.poles else True,
        "branches_replay_exact": all(
            branch["replay_exact"] for branch in payload["branches"].values()
        ),
    }
    payload["all_technical_gates"] = all(payload["gates"].values())
    target.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "out": str(target),
        "gates": payload["gates"],
        "all_technical_gates": payload["all_technical_gates"],
        "summary": payload["summary"],
    }, indent=2), flush=True)


if __name__ == "__main__":
    main()
