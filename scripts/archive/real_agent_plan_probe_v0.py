"""Run one real-LLM UX/integration smoke for ``plan_probe_v0``.

THIS IS NOT BEHAVIORAL EVIDENCE AND NOT PAPER EVIDENCE.  The current factory
support is deliberately narrow, so this runner is only allowed to answer a
technical question: can a real agent understand and complete the full 12-round
protocol through the same opaque kernel used by WAGER?

Unlike ``technical_plan_probe_v0.py``, this script does not use an omniscient
fixture.  It calls ``run_episode`` with an actual Foundry deployment and stores
the complete private trace plus the server-side protocol report.  Its outputs
must never be mixed with pilot or study artifacts.
"""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import re
import sys
import traceback


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from wager.factory.plan_probe_v0 import (  # noqa: E402
    VALIDATION_SEED_START,
    ProbeConfig,
    generate_candidate,
)
from wager.harness.episode import run_episode  # noqa: E402
from wager.harness.plan_probe_v0 import build_plan_probe_server  # noqa: E402


DEFAULT_MODEL = "DeepSeek-V3.2"
DEFAULT_OUTPUT_DIR = (
    ROOT
    / "scripts"
    / "out"
    / "probe_v0_plan"
    / "technical"
    / "real_agent"
    / "private"
)
FACTORY_REPORT = (
    ROOT
    / "scripts"
    / "out"
    / "probe_v0_plan"
    / "factory"
    / "private"
    / "factory_certification.json"
)
KIND = "real_llm_ux_integration_smoke_not_behavioral_or_paper_evidence"


# This suffix only teaches the mechanics introduced by the probe server.  It
# intentionally says nothing about the hidden scenario or the correct update.
PROTOCOL_SYSTEM_SUFFIX = r"""

This episode uses a STRICT 12-round protocol. The generic instruction above to
submit whenever you have converged does NOT apply here: do not call env.submit
before round 12. You receive a protocol notice at each required checkpoint.
Every assistant reply consumes exactly one numbered round even if its Python
cell raises an error. There are no retry turns. On a required round, do any
needed calculation and the required env verb in that same cell before it ends.

Additional env verbs:
  env.register_model(code_string) -> None
      Store a silent executable model snapshot. Required in rounds 4, 6, and 8.
      Pass the complete Python SOURCE STRING (never bytecode or a function
      object). It intentionally returns no validation feedback; None is expected.
  env.commit_plan(action) -> None
      In round 6 only, commit one operating action from the declared action grid.
      It must be called immediately after env.register_model(code_string), in the
      same Python cell, with no intervening env call.
  env.maintain() -> None
      In round 9 only, keep the round-6 operating action after the cost is shown.
  env.reopen(new_action) -> None
      In round 9 only, pay the shown reconfiguration cost and replace the action.

Required chronology:
  - Before round 4: read the complete fixed 'prefix' lot exactly once using
    the row count declared in the machine-readable sheet. A checkpoint made
    without consuming the prefix is a protocol failure.
  - Round 4: call env.register_model(code_string).
  - Round 6: call env.register_model(code_string), then immediately
    env.commit_plan(action) in that same cell.
  - Round 7: the fixed diagnostic_panel becomes available. Read exactly the row
    count declared in env.describe()/the machine-readable sheet.
  - Round 8: call env.register_model(code_string). This freezes data acquisition.
  - Round 9: after seeing the cost notice, call exactly one of env.maintain() or
    env.reopen(new_action).
  - Round 12: call env.submit(final_code_string).

In all other rounds, continue investigating, modelling, checking your work, or
preparing the next required action, but still return exactly one Python cell.
The registered object and final delivery use the same executable contract:
define model(regime, n, seed) and return exactly a pandas DataFrame with the
single column 'outcome'. Do not mistake silent registration for final delivery.
"""


def _slug(value: str) -> str:
    cleaned = re.sub(r"[^A-Za-z0-9_.-]+", "-", value).strip("-._")
    return cleaned or "model"


def _load_green_factory() -> dict:
    if not FACTORY_REPORT.exists():
        raise FileNotFoundError(
            "missing private factory certificate; run certify_plan_probe_v0.py first: "
            f"{FACTORY_REPORT}"
        )
    report = json.loads(FACTORY_REPORT.read_text(encoding="utf-8"))
    if not report.get("all"):
        raise RuntimeError("factory certificate is not green; refusing an LLM call")
    fixed = report.get("fixed_cohort") or {}
    if fixed.get("candidate_seed_start") != VALIDATION_SEED_START:
        raise RuntimeError(
            "factory artifact and source disagree on the fixed-cohort start"
        )
    return report


def _write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Run one real-agent 12-round UX/integration smoke. This is not "
            "behavioral evidence and not paper evidence."
        )
    )
    parser.add_argument(
        "--model",
        default=DEFAULT_MODEL,
        help=f"Foundry deployment name (default: {DEFAULT_MODEL})",
    )
    parser.add_argument(
        "--scenario",
        choices=("maintain", "revise", "doubt"),
        default="revise",
        help="Private hidden continuation used by the server (default: revise)",
    )
    parser.add_argument(
        "--cost",
        choices=("low", "high"),
        default="low",
        help="Reconfiguration-cost condition revealed in round 9 (default: low)",
    )
    parser.add_argument(
        "--episode-seed",
        type=int,
        default=90_001,
        help="Private episode/scoring seed (default: 90001; technical/burned)",
    )
    parser.add_argument(
        "--family-seed",
        type=int,
        default=VALIDATION_SEED_START,
        help=(
            "Private factory candidate seed (default: first certified fixed-cohort "
            "family)"
        ),
    )
    parser.add_argument(
        "--max-tokens",
        type=int,
        default=200_000,
        help="Conversation token guard; protocol length remains exactly 12 rounds",
    )
    parser.add_argument(
        "--cell-timeout-s",
        type=float,
        default=90.0,
        help="Timeout for each opaque-kernel cell (default: 90 seconds)",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=DEFAULT_OUTPUT_DIR,
        help="Private technical-artifact directory",
    )
    parser.add_argument(
        "--run-id",
        help="Optional filename stem; default includes UTC timestamp and conditions",
    )
    return parser.parse_args()


def main() -> int:
    args = _parse_args()
    factory = _load_green_factory()
    fixed = factory["fixed_cohort"]
    certified_start = int(fixed["candidate_seed_start"])
    certified_stop = certified_start + int(fixed["count"])
    if not certified_start <= args.family_seed < certified_stop:
        raise ValueError(
            "--family-seed must belong to the certified fixed cohort "
            f"[{certified_start}, {certified_stop - 1}]"
        )
    config = ProbeConfig()
    family = generate_candidate(args.family_seed, config)
    server = build_plan_probe_server(
        family,
        scenario=args.scenario,
        cost_condition=args.cost,
        episode_seed=args.episode_seed,
        config=config,
    )

    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    run_id = args.run_id or (
        f"{timestamp}_{_slug(args.model)}_{args.scenario}_{args.cost}"
        f"_e{args.episode_seed}_f{args.family_seed}"
    )
    trace_path = args.output_dir / f"{run_id}_trace.json"
    report_path = args.output_dir / f"{run_id}_protocol_report.json"

    common = {
        "kind": KIND,
        "interpretation_boundary": {
            "allowed": "real-agent UX and end-to-end integration debugging only",
            "forbidden": [
                "behavioral conclusion",
                "model comparison",
                "effect estimate",
                "pilot evidence",
                "paper evidence",
            ],
            "reason": (
                "the current factory has narrow admissible support and this seed is "
                "burned for technical validation"
            ),
        },
        "model": args.model,
        "scenario_private": args.scenario,
        "cost_condition_private": args.cost,
        "episode_seed_private": args.episode_seed,
        "family_seed_private": args.family_seed,
        "factory_schema": factory.get("schema_version"),
        "started_at_utc": timestamp,
    }

    try:
        episode = run_episode(
            server,
            model=args.model,
            max_turns=12,
            max_tokens=args.max_tokens,
            cell_timeout_s=args.cell_timeout_s,
            system_suffix=PROTOCOL_SYSTEM_SUFFIX,
        )
        trace_payload = {
            **common,
            "status": "completed",
            "episode": episode,
        }
        exit_code = 0
    except Exception as exc:  # noqa: BLE001 - preserve failed integration smoke
        trace_payload = {
            **common,
            "status": "runner_exception",
            "error": f"{type(exc).__name__}: {exc}",
            "traceback": traceback.format_exc(),
        }
        exit_code = 1

    protocol_payload = {
        **common,
        "status": trace_payload["status"],
        "server_report": server.private_protocol_report(include_code=False),
        "note": "Real-LLM technical smoke, never behavioral or paper evidence.",
    }
    _write_json(trace_path, trace_payload)
    _write_json(report_path, protocol_payload)

    episode_summary = trace_payload.get("episode") or {}
    print(
        json.dumps(
            {
                "kind": KIND,
                "status": trace_payload["status"],
                "accepted": episode_summary.get("accepted", server.terminal),
                "turns": episode_summary.get("turns"),
                "abort_reason": episode_summary.get("abort_reason"),
                "model": args.model,
                "trace": str(trace_path),
                "private_protocol_report": str(report_path),
                "warning": "UX/integration smoke only; no behavioral or paper inference",
            },
            indent=2,
        )
    )
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
