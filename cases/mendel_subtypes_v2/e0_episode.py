"""E0 -- real episodes on mendel_subtypes_v2 (the window world's first exam).

Pre-registered and SIGNED (autonomy, Decision Log v0.63/v0.64) BEFORE any
episode ran. Certification anchors: bayes ceiling R=1, plugin R=0.9991 global
(gap concentrates at small n_cal: +0.71 at n_cal=2, 16-lot diagnostic), pooled
R=0, null R=-0.26.

Signed branches:
  A (modal): the solver uses regime.context["cal_window"] for PER-LOT
     inference (window mean inversion or posterior) on top of the two-grade
     opposite-slope structure -> R in [0.85, 1.0].
  B: window read but not used for lot inference (lot-agnostic mixture at the
     historical composition) -> R in [0.2, 0.7].
  C: contract failure on the variable-length window (family #19) -> R = 0
     with sandbox errors. The pre-written ergonomics (brief line + control
     surface deliverable_note, v0.63-5) exist to prevent exactly this; this
     E0 is their test.
Signed expectations: 2/2 episodes zero-crash at scoring; >=1/2 lands in
branch A. Both currencies (R and |dP| of the scrap exceedance) in the report.

SEEDS 0-1 RESULT (autopsy in traces): zero crashes (ergonomics 5 worked; the
window WAS read) but both landed BELOW branch B (R_uncl -2.32 / -1.06): the
window fed only a marker bootstrap while the outcome came from an empirical
payload of their experiments -- and a NEW #19 flavor surfaced: experiment()
samples ONE fresh lot per call (undocumented), so their per-dose payload
confounded dose with lot luck. Per the world-3 precedent the ergonomics were
fixed (brief + control_surface.experiment_note document one-lot-per-call)
and seeds 2-3 re-run. RE-RUN PRE-REGISTRATION (signed before running): same
branches; zero crashes again; >=1/2 in branch A iff the solver now separates
lot composition (window) from dose response (experiments); if both still
ignore the window for the OUTCOME law, that is branch B and counts as v2
headroom evidence, not tooling failure.

Run:  .venv/Scripts/python cases/mendel_subtypes_v2/e0_episode.py [model] [seed_offset]
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
