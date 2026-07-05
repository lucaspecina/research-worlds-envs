"""E0.5 -- consolidation batch for the scarce sibling (#6): does scarcity bite
reproducibly, and cross-family?

Ordered by Lucas (2026-07-05, same insurance as v2's v0.66 batch): the
"budget IS a difficulty axis" finding currently rests on n=2, one family.
4 new episodes: 2x gpt-5.4 (seeds 2-3) + 2x DeepSeek-V3.2 (seeds 2-3).

PRE-REGISTERED (signed in autonomy BEFORE running; the v2 batch already
refuted my "DeepSeek worse" prior, so it is NOT re-signed):
  (i)  scarcity replicates: NO new episode reaches R >= 0.95 (the same
       solver hit 0.974/0.993 at full budget on this world);
  (ii) >=2/4 submissions do NOT deconvolve (no sigma/replica machinery in
       the submitted model) -- "evidence bought and unused" or "replicas
       skipped" remains the modal signature under scarcity;
  (iii) DeepSeek plays deeper again (>=1.5x gpt's turns) -- 4th sighting of
       depth-tracks-outcome if its median R also matches or beats gpt's.

Run:  .venv/Scripts/python cases/selection_bias_scarce_v0/e05_consolidation.py
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

PLAN = [
    ("gpt-5.4", 2),
    ("gpt-5.4", 3),
    ("DeepSeek-V3.2", 2),
    ("DeepSeek-V3.2", 3),
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
