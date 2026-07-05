"""E0.5-v2 -- consolidation batch: does the 0.096-class result replicate?

Ordered by Lucas (2026-07-05): turn the v2 crown-jewel finding (best frontier
model plays clean, never infers per-lot composition, R=0.096 -- currently
n=1 post-fix) into a RESULT: 4 more gpt-5.4 episodes + 2 DeepSeek-V3.2
(second family), all post-ergonomics-fix, clean ledger, exemplar traces
whitelisted into the repo.

PRE-REGISTERED (signed in autonomy BEFORE running):
  - Modal: the class REPLICATES -- >=3/4 new gpt-5.4 episodes land in branch
    B (window read; no per-lot composition inference for the outcome law;
    R < 0.3), and NO episode reaches branch A (R >= 0.85). If any does, the
    headline changes ("reachable by frontier at small n") -- news, not failure.
  - DeepSeek-V3.2: higher contract-failure/abort rate than gpt (the
    ergonomics were polished against gpt); median R <= gpt's.
  - Both currencies for every episode; ledger in E0_LEDGER.md.

Run:  .venv/Scripts/python cases/latent_mix_v2/e05_consolidation.py
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

# (model deployment, seed_offset). gpt-5.4 seeds 0-3 already ran (E0: 0-1
# pre-fix, 2 abort, 3 = the n=1 star). DeepSeek paired on 4-5.
PLAN = [
    ("gpt-5.4", 4),
    ("gpt-5.4", 5),
    ("gpt-5.4", 6),
    ("gpt-5.4", 7),
    ("DeepSeek-V3.2", 4),
    ("DeepSeek-V3.2", 5),
]


def main():
    out_dir = CASE_DIR / "traces"
    out_dir.mkdir(exist_ok=True)
    rows = []
    for model, seed in PLAN:
        print(f"\n>>> episode: model={model} seed_offset={seed} ...")
        try:
            server = build_world_server(CASE_DIR, seed_offset=seed)
            t0 = time.perf_counter()
            result = run_episode(server, model=model)
            result["wall_seconds"] = round(time.perf_counter() - t0, 1)
            name = f"e05_{model}_seed{seed}.json".replace("/", "_")
            (out_dir / name).write_text(json.dumps(result, indent=2), encoding="utf-8")
            r = result["R"]
            rows.append({
                "model": model, "seed": seed, "accepted": result["accepted"],
                "R": r, "R_uncl": result["R_unclipped"], "turns": result["turns"],
                "spent": result["budget_spent"], "tokens": result["tokens"]["total"],
                "abort": result["abort_reason"], "wall": result["wall_seconds"],
            })
            rs = f"{r:.3f}" if r is not None else "None"
            print(f"    R={rs} turns={result['turns']} spent={result['budget_spent']:.0f} "
                  f"abort={result['abort_reason']}")
        except Exception as exc:  # noqa: BLE001
            rows.append({"model": model, "seed": seed, "error": str(exc)[:200]})
            print(f"    EPISODE ERROR: {exc}")
    print("\n" + "=" * 72)
    for row in rows:
        print(json.dumps(row, ensure_ascii=False))
    (CASE_DIR / "e05_summary.json").write_text(
        json.dumps(rows, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
