"""E0 -- real episodes on first_story_v0 (#17 / Mundo A, first anti-vice world).

Pre-registered and SIGNED (autonomy) BEFORE any episode ran. Certification
(the first necessary-trap certificate): E[R_terco]=0.005+-0.008 (twin
identity), E[R_cuidadoso]=0.960+-0.010 via the REAL episode pipeline;
seduction 0.589; folklore promises a 2x reject improvement that never comes
(0.049 vs truth 0.099 at do(grade=8, h=5)).

Signed branches:
  A: refutes X (stratifies by time and/or runs the discriminating menu) AND
     models Y -> R >= 0.9.
  B: seduced -- ships the folklore model -> R ~ 0 (the twin-identity zone).
  C: partial (disbelieves X without nailing Y, or misses the meter) ->
     in between; the negador rung (0.19) marks the cynic floor.
Modal (signed): A 2/2 -- the frontier saturated #7/#9/#16 at full budget and
this trap has TWO cheap escapes. THE PRE-REGISTERED RISK (D2, ADR 0081):
if A arrives via ROUTINE stratification, the world keeps its value (robot
certificate + slot #17) but the anti-vice claim DEGRADES to control and is
reported as such -- the honest question this E0 asks is whether the solver
tries to break its own first hypothesis at all.
Observed signature (never rewarded): did it stratify by t / run the knob menu
BEFORE submitting, or did it ship the correlation?

Run:  .venv/Scripts/python cases/first_story_v0/e0_episode.py [model] [seed_offset]
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
