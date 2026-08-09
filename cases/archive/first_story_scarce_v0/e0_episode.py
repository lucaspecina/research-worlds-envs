"""E0 -- first_story_SCARCE_v0: THE scarcity x vice cell (ledger item 2, ADR 0086).

The #6 recipe on Mundo A: budget /4 (5000) and replicas x3 (15/row);
certificates re-derived as a new case. THE QUESTION this cell exists for:
at full budget the frontier broke its first hypothesis ROUTINELY (base E0:
seduced branch empty, 2/2 stratified AND ran the full knob menu). Does that
habit survive when every peso hurts? Precedent AGAINST survival: #6/ADR 0067
("scarcity separates styles"; gpt's bought-unused-evidence became LAW under
scarcity, 4/4).

Pre-registered and SIGNED BEFORE running:
  A: still breaks X (cheap stratification costs ~0!) and models Y -> R >= 0.85.
  B: seduced -- ships the folklore correlation -> R ~ 0.
  C: partial in between.
Modal (signed): DEGRADATION -- <=1/2 in A; >=1/2 skips the discriminating
knob menu (the expensive escape) and, if it escapes at all, does so via the
FREE one (time stratification). Signature watched: menu run? stratified?
News variant (seeds 30+): the 50%-spend trigger = 2500 here, so the notice
fires EARLIER relative to the investigation; signed: the incorporation habit
degrades less than the menu habit (reading a cheap unlocked log costs ~400).

Run:  .venv/Scripts/python cases/first_story_scarce_v0/e0_episode.py [model] [seed_offset]
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
