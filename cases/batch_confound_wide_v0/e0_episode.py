"""E0 -- real episodes on batch_confound_v0 (#9).

Pre-registered and SIGNED (autonomy) BEFORE any episode ran. Certification:
world.py = R=1; canonical 0.9998 (sigma_hat 1.4996); naive = 0 with reject
rate 0.87-vs-0.64 at do(2); twin_deriva -0.115 (spurious slope +87%: believing
the record's driver response is BELOW naive); twin_offsets 0.942.

Signed branches:
  A: de-confounds the slope (within-batch fits on the record, or experiments)
     AND treats between-batch scatter as meter, not process -> R >= 0.9.
  B: believes the pooled record slope -> R <= 0.3 with reject rates badly off
     at off-center intensities.
  C: partial -- de-confounded slope but scatter/joint imperfect -> [0.3, 0.9).
Modal (signed): 2/2 >= 0.6 with >=1/2 in A -- the confound is discoverable
two independent ways (batch_id within-fits are cheap; experiments are the
manual move every prior world showed). Zero-crash expectation. The
discriminating signature: does the submission's outcome variance EXCLUDE the
offset variance (~16) the record shows?

Run:  .venv/Scripts/python cases/batch_confound_v0/e0_episode.py [model] [seed_offset]
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
