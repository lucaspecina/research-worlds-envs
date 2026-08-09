"""E0 -- real episodes on prior_sweetspot_v0 (#16, trustworthy-prior control).

Pre-registered and SIGNED (autonomy) BEFORE any episode ran. Certification:
world.py = R=1; canonical 0.9994; twin lineal -0.315; naive underprices the
"scorched" side 400x (0.0008 vs 0.33 at do(9)).

Signed branches:
  A (modal, 2/2): control world, true prior, cheap discovery -> R >= 0.9. A
     frontier that experiments across the range (or trusts the evoked sweet
     spot and probes around it) nails the parabola.
  B: linear extrapolation of the record (ignores the prior AND skips
     experiments past the cluster) -> R <= 0.3.
  C: in between.
Zero-crash expectation. Conduct signature OBSERVED (never rewarded): does the
solver's FIRST experiment probe both sides of the suspected optimum (prior
used) or only extend the record's direction?

Run:  .venv/Scripts/python cases/prior_sweetspot_v0/e0_episode.py [model] [seed_offset]
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
