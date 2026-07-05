"""E0 -- real episodes on selection_bias_scarce_v0 (matrix slot #6).

THE HYPOTHESIS TEST (E1_MATRIX rule iv, signed in autonomy BEFORE running):
the same world the frontier saturated at full budget (v0.60: R=0.974/0.993,
spend 7-11k of 20000) now offers budget 5000 with the replicated source at
15/row. If it STAYS easy, difficulty-by-budget is refuted for this class and
difficulty must be built from composition.

Signed branches:
  A (modal, my prediction: 2/2): triage keeps the deconvolution -- fewer
     replica rows (>=30) still give sigma_hat, fewer/leaner experiments still
     give the do-curve -> R >= 0.95. Scarcity /4 does NOT bite; composition
     is the difficulty axis.
  B: deconvolution DROPPED under scarcity (no replicas purchase / sigma
     absent) -> R < 0.85 with the "dispersion believed real" signature;
     budget IS a difficulty axis.
  C: partial triage -> R in [0.85, 0.95); report spending pattern + sigma_hat
     error against the certificate's 1.4996.
Both currencies (R and cull-line |dP|); spending pattern from the trace is
part of the result.

Run:  .venv/Scripts/python cases/selection_bias_scarce_v0/e0_episode.py [model] [seed_offset]
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
