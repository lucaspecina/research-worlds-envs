"""Run one omniscient scripted episode through the opaque kernel.

This is a wiring artifact, not agent behavior and not paper evidence.  It uses
an exact posterior fixture to exercise every protocol transition authorized by
ADR 0159, then writes a private trace.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

SCRIPTED_MODEL_DISTANCE_MAX = 0.03

from wager.factory.plan_probe_v0 import (  # noqa: E402
    VALIDATION_SEED_START,
    ProbeConfig,
    exact_posterior,
    generate_candidate,
)
from wager.harness.kernel_proc import KernelClient  # noqa: E402
from wager.harness.plan_probe_v0 import (  # noqa: E402
    build_plan_probe_server,
    posterior_submission_code,
)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output",
        type=Path,
        default=(
            ROOT
            / "scripts"
            / "out"
            / "probe_v0_plan"
            / "technical"
            / "private"
            / "technical_revise_low.json"
        ),
    )
    args = parser.parse_args()

    factory_path = (
        ROOT
        / "scripts"
        / "out"
        / "probe_v0_plan"
        / "factory"
        / "private"
        / "factory_certification.json"
    )
    factory = json.loads(factory_path.read_text(encoding="utf-8"))
    if not factory["all"]:
        raise RuntimeError("factory gate is not green")
    fixed_start = factory["fixed_cohort"]["candidate_seed_start"]
    if fixed_start != VALIDATION_SEED_START:
        raise RuntimeError("factory artifact and code disagree on the fixed cohort")

    config = ProbeConfig()
    family = generate_candidate(VALIDATION_SEED_START, config)
    pre = exact_posterior(family, config)
    post = exact_posterior(family, config, evidence="revise")
    pre_code = posterior_submission_code(pre)
    post_code = posterior_submission_code(post)
    server = build_plan_probe_server(
        family,
        scenario="revise",
        cost_condition="low",
        episode_seed=90_000,
        config=config,
    )
    prefix_n = family.prefix.line.size
    panel_n = family.evidence["revise"].line.size
    reference_action = post.decision().action
    trace: list[dict] = []

    with KernelClient(server) as kernel:
        for turn in range(1, 13):
            notices = server.begin_turn(turn)
            if turn == 1:
                cell = (
                    f"pre_code={pre_code!r}\npost_code={post_code!r}\n"
                    f"prefix=env.observe('prefix', {prefix_n})\n"
                    "print(prefix.shape, list(prefix.columns))"
                )
            elif turn == 4:
                cell = "print(env.register_model(pre_code))"
            elif turn == 6:
                cell = (
                    "env.register_model(pre_code)\n"
                    f"env.commit_plan({pre.decision().action!r})\n"
                    "print('committed')"
                )
            elif turn == 7:
                cell = (
                    f"panel=env.observe('diagnostic_panel', {panel_n})\n"
                    "print(panel.shape, list(panel.columns))"
                )
            elif turn == 8:
                cell = "print(env.register_model(post_code))"
            elif turn == 9:
                cell = (
                    f"env.reopen({reference_action!r})\n"
                    "print('reopened')"
                )
            elif turn == 12:
                cell = (
                    "delivery=env.submit(post_code)\n"
                    "print(delivery.accepted, delivery.error)"
                )
            else:
                cell = "print('round ok')"
            result = kernel.run_cell(cell)
            trace.append(
                {
                    "round": turn,
                    "notices": notices,
                    "cell": cell,
                    "ok": result.ok,
                    "stdout": result.stdout,
                    "error": result.error,
                }
            )
            if not result.ok:
                break

    private_report = server.private_protocol_report(include_code=False)
    output = {
        "kind": "private_scripted_technical_wiring_not_agent_evidence",
        "factory_schema": factory["schema_version"],
        "episode_seed": 90_000,
        "scripted_fixture": "exact legal posterior before/after revise evidence",
        "trace": trace,
        "trajectory": [
            {
                "verb": event.verb,
                "args": event.args,
                "cost": event.cost,
                "budget_remaining": event.budget_remaining,
                "note": event.note,
            }
            for event in server.trajectory
        ],
        "private_protocol_report": private_report,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(output, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )

    plan = (private_report.get("result") or {}).get("plan") or {}
    passed = bool(
        server.terminal
        and not private_report["protocol_violations"]
        and len(private_report["snapshots"]) == 4
        and all(snapshot["valid"] for snapshot in private_report["snapshots"])
        and abs(float(plan.get("policy_regret", 1.0))) <= 1e-9
        and float(
            (private_report.get("result") or {}).get(
                "technical_model_distance", float("inf")
            )
        )
        <= SCRIPTED_MODEL_DISTANCE_MAX
        and all(row["ok"] for row in trace)
    )
    print(
        json.dumps(
            {
                "all": passed,
                "terminal": server.terminal,
                "snapshots": len(private_report["snapshots"]),
                "policy_regret": plan.get("policy_regret"),
                "technical_model_distance": (
                    (private_report.get("result") or {}).get(
                        "technical_model_distance"
                    )
                ),
                "output": str(args.output),
            },
            indent=2,
        )
    )
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
