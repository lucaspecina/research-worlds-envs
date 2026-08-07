"""ADR 0127 -- AUTOPSY runs for the hint method (Fase 1 of ADRs 0124/0125).

NOT confirmatory: these episodes exist to diagnose MECHANISM (the zeros of
ADR 0121) and to estimate rates/power for Fase 3. Key difference vs the 0118
runner (whose lesson is registered in ADR 0122): the FULL episode record is
persisted -- turn-by-turn trace, submission_code, purchases/budget, tokens --
one JSON per episode, so the blind failure taxonomy of ADR 0127 can be applied
to complete evidence.

Plan: first_story_scarce_v0 x {libre, hint_T (EXACT 0118 text)} x seeds 55-62
= 16 episodes, DeepSeek-V3.2, N FIXED (never stop early on zeros).

Run:  .venv/Scripts/python scripts/exp_hint_autopsy_0127.py   (resumable)
Out:  scripts/out/autopsy_0127/ep_<cond>_seed<seed>.json  (full record)
      scripts/out/autopsy_0127/summary.json               (thin rows)
"""

import json
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from wager.harness.case_episode import build_world_server  # noqa: E402
from wager.harness.episode import run_episode  # noqa: E402

CASE = ROOT / "cases" / "first_story_scarce_v0"
OUT_DIR = ROOT / "scripts" / "out" / "autopsy_0127"
MODEL = "DeepSeek-V3.2"
SEEDS = (55, 56, 57, 58, 59, 60, 61, 62)

# EXACT 0118 hint text (frozen in ADR 0118; do not edit)
HINT_T = (
    "A tight budget tempts you to rush the final answer. Do not: make sure "
    "your submitted model actually incorporates the evidence you paid for, and "
    "check every part of what you hand in before submitting."
)
SUFFIX = {"libre": "", "hint_T": "\n\n" + HINT_T}


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    summary_path = OUT_DIR / "summary.json"
    rows = json.loads(summary_path.read_text(encoding="utf-8")) if summary_path.exists() else []
    done = {(r["cond"], r["seed"]) for r in rows if r.get("error") is None}

    plan = [(cond, seed) for cond in ("libre", "hint_T") for seed in SEEDS]
    todo = [t for t in plan if t not in done]
    print(f"AUTOPSY 0127: {len(todo)} episode(s) to run ({len(plan) - len(todo)} done) -> {OUT_DIR}",
          flush=True)

    for cond, seed in todo:
        print(f"\n>>> {cond}/seed{seed} ...", flush=True)
        t0 = time.perf_counter()
        try:
            server = build_world_server(CASE, seed_offset=seed)
            result = run_episode(server, model=MODEL, system_suffix=SUFFIX[cond])
            result["_autopsy"] = {"cond": cond, "seed": seed,
                                  "wall_s": round(time.perf_counter() - t0, 1)}
            (OUT_DIR / f"ep_{cond}_seed{seed}.json").write_text(
                json.dumps(result, indent=2, default=str), encoding="utf-8")
            row = {"cond": cond, "seed": seed, "R": result["R"],
                   "R_uncl": result["R_unclipped"], "accepted": result["accepted"],
                   "abort": result["abort_reason"], "turns": result["turns"],
                   "spent": result["budget_spent"], "error": None}
        except Exception as exc:  # noqa: BLE001 -- infra failure: recorded, retried on rerun
            row = {"cond": cond, "seed": seed, "R": None, "R_uncl": None,
                   "accepted": False, "abort": None, "turns": None, "spent": None,
                   "error": f"{type(exc).__name__}: {exc}"[:300]}
        rows = [r for r in rows if (r["cond"], r["seed"]) != (cond, seed)] + [row]
        summary_path.write_text(json.dumps(rows, indent=2) + "\n", encoding="utf-8")
        print(f"  R={row['R']}  R_uncl={row['R_uncl']}  abort={row['abort']}"
              f"  turns={row['turns']}  spent={row['spent']}  err={row['error']}", flush=True)

    print(f"\nAUTOPSY runs DONE ({len(plan)} planned). Taxonomy pass (ADR 0127) comes next -- "
          f"traces first, R/condition last.", flush=True)


if __name__ == "__main__":
    main()
