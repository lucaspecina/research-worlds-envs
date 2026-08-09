"""E0 -- real episodes on twotank_clearance_v0 (#12, second dynamic world).

Pre-registered and SIGNED (autonomy) BEFORE any episode ran. Simple anchors
(world.py = R=1); certification numbers in certificates.json.

Signed branches (prior UPDATED by #11's outcome -- both its episodes landed in
C via the historical-regime triangulation gap):
  A: buys horizon, sees the peak+drain, AND triangulates the historical
     valve -> R >= 0.9.
  B: truncation bites -- extrapolates the build-up without paying horizon ->
     R <= 0.3 with clearance |dP| ~ 1.
  C (modal, my prediction: 2/2): saturating... rise-fall family found via
     long experiments but the historical regime and/or drain tail imperfect
     -> R in [0.6, 0.9).
Zero-crash expectation on the LONG contract (same pre-written ergonomics as
#11, which held 2/2 there). Both currencies; traces gitignored (archive per
policy).

Run:  .venv/Scripts/python cases/twotank_clearance_v0/e0_episode.py [model] [seed_offset]
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
