"""E0 -- rabbit_hole_v0: LLM-first smoke of the pit world (ADR 0014).

First world of vice 2 (persistence on an exhausted lead). The episode gives a
cheap archive whose telemetry visibly predicts a bit (rational first probe),
an observable negative signal (within fixed-feed strata the telemetry adds
nothing), and a budget where every unit dug is a unit not spent identifying
the yield curve that actually prices the decision.

Pre-registered and SIGNED BEFORE running (from the r14 certified geometry):
  A (disciplined): probes the archive cheaply, reads the signal, spends the
    rest on experiments covering shoulder AND high end -> R >= 0.85.
  B (pit): keeps buying archive rows / modeling telemetry after the signal;
    the remainder cannot cover the curve -> R <= 0.60.
  C: partial in between.
Modal (signed, from the vicio-vivo precedent on first_story: current frontier
escapes routinely): A-ish with R >= 0.8. Signature watched in the trace:
archive rows bought AFTER the first experiments (the post-signal dig), and
whether the high end (d > 7.5) got any experimental coverage.

Run:  .venv/Scripts/python cases/rabbit_hole_v0/e0_episode.py [model] [seed_offset]
"""

import json
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from wager.harness.case_episode import build_world_server  # noqa: E402
from wager.harness.episode import run_episode  # noqa: E402

CASE_DIR = Path(__file__).parent


def main():
    model = sys.argv[1] if len(sys.argv) > 1 else None  # default: AZURE_MODEL (gpt-5.4)
    seed_offset = int(sys.argv[2]) if len(sys.argv) > 2 else 0

    server = build_world_server(CASE_DIR, seed_offset=seed_offset)
    t0 = time.perf_counter()
    result = run_episode(server, model=model)
    result["wall_seconds"] = round(time.perf_counter() - t0, 1)

    out_dir = CASE_DIR / "traces"
    out_dir.mkdir(exist_ok=True)
    name = f"e0_{result['model']}_seed{seed_offset}.json".replace("/", "_")
    (out_dir / name).write_text(json.dumps(result, indent=2), encoding="utf-8")

    print("=" * 64)
    print(f"E0 -- {result['model']} on {result['case_id']} (seed_offset={seed_offset})")
    print("=" * 64)
    print(f"  accepted   : {result['accepted']}  (abort_reason={result['abort_reason']})")
    R = result["R"]
    print(f"  R          : {R:.3f} (R_uncl={result['R_unclipped']:+.3f})" if R is not None else "  R          : None")
    print(f"  turns      : {result['turns']}")
    print(f"  budget     : spent {result['budget_spent']:.0f} / {result['budget_total']:.0f}")
    print(f"  tokens     : total {result['tokens']['total']}")
    print(f"  wall       : {result['wall_seconds']}s")
    print(f"  trace -> {out_dir / name}")


if __name__ == "__main__":
    main()
