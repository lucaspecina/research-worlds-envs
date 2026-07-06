"""E0 -- real episodes on logistic_yield_v0 (#11, the first dynamic world).

Pre-registered and SIGNED (autonomy) BEFORE any episode ran. Certification:
ceiling = world.py R=1 (simple anchors -- no hidden per-item state here);
canonical solver 0.9847; naive-exp = 0; twin_truncation 0.233; the K-invisibility
is CERTIFIED (best saturating fit on the truncated pool: K=2000, upper bound).

Signed branches:
  A (modal, my prediction: 2/2): the solver buys long-horizon and/or
     high-feed experiments, sees saturation, fits a saturating family ->
     R >= 0.9 (saturation expected: #11 is the formalism test, not the
     trophy; spec 2 pre-registers this honestly).
  B: truncation trap bites -- extrapolates the ramp-up story without paying
     for horizon -> R <= 0.3 with deadline |dP| ~ 1 at low feeds.
  C: partial -- saturating family with K poorly pinned (short experiments
     only) -> R in (0.3, 0.9).
Zero-crash expectation on the LONG-format contract (deliverable_note +
experiment_note pre-written; THIS E0 tests the trajectory ergonomics -- the
#19 watch item is the n x len(t_grid) row echo).
Both currencies (R and deadline |dP|); traces to traces/ (exemplars
whitelisted per-file if cited, ADR 0066 policy).

Run:  .venv/Scripts/python cases/logistic_yield_v0/e0_episode.py [model] [seed_offset]
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
