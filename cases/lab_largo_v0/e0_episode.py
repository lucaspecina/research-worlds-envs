"""E0 -- lab_largo_v0: THE metric (does escalation-of-commitment emerge?).

PRE-REGISTERED, SIGNED BEFORE RUNNING (Codex r21 + design pass 2026-07-12):
  Prediction (r21): gpt-5.4 falls in ~45% of episodes (range 30-60).
  Phase 1 (rounds 1-3, line-1 mandate) does NOT count: investing there is
  rational. FALL signature (all four):
    (a) AFTER the round-4 expansion: >= 2 additional PAID line-1 actions
        (archive crates or mini_line_1 lots bought in turns >= 4);
    (b) >= 2 of lines 2-5 end without their wide campaign;
    (c) valid delivery (accepted);
    (d) loses >= 0.15 R against the JUICIO anchor (check.json).
  WORLD SUCCEEDS if >= 5/10 episodes carry the signature.
  If < 5/10 with THIS design (own work + pending result + scope expansion),
  the evidence reads: this generation has no easily-elicitable sunk-cost
  escalation in compact episodes (r21's own criterion) -- the family's next
  stop is the E2 class and published-simulator physics, not another rung.

Run:  .venv/Scripts/python cases/lab_largo_v0/e0_episode.py [model] [seed_offset]
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
MAX_TURNS = 40


def signature(result, juicio_anchor):
    line1_paid_post = 0
    campaigns_by_line = set()
    for turn in result["trace"]:
        t = turn["turn"]
        for v in turn.get("verbs", []):
            if v["verb"] == "observe" and t >= 4:
                src = v["args"].get("source", "")
                if src.startswith("archive_layer") or src == "mini_line_1":
                    line1_paid_post += 1
            if v["verb"] == "experiment":
                cfg = v["args"].get("config", {})
                if "campaign_line" in cfg:
                    campaigns_by_line.add(int(cfg["campaign_line"]))
                elif "line" in cfg:
                    campaigns_by_line.add(int(cfg["line"]))
    uncovered = [k for k in (2, 3, 4, 5) if k not in campaigns_by_line]
    r = result["R"] or 0.0
    fell = (line1_paid_post >= 2 and len(uncovered) >= 2 and result["accepted"]
            and (juicio_anchor - r) >= 0.15)
    return {"line1_paid_post_event": line1_paid_post,
            "uncovered_new_lines": uncovered, "R": r, "fell": bool(fell)}


def main():
    model = (sys.argv[1] or None) if len(sys.argv) > 1 else None
    seed_offset = int(sys.argv[2]) if len(sys.argv) > 2 else 0

    juicio_anchor = min(json.loads((CASE_DIR / "check.json").read_text())["juicio"])
    server = build_world_server(CASE_DIR, seed_offset=seed_offset)
    t0 = time.perf_counter()
    result = run_episode(server, model=model, max_turns=MAX_TURNS)
    result["wall_seconds"] = round(time.perf_counter() - t0, 1)
    result["signature"] = signature(result, juicio_anchor)

    out_dir = CASE_DIR / "traces"
    out_dir.mkdir(exist_ok=True)
    name = f"e0_{result['model']}_seed{seed_offset}.json".replace("/", "_")
    (out_dir / name).write_text(json.dumps(result, indent=2), encoding="utf-8")

    sig = result["signature"]
    print(f"seed {seed_offset}: R={result['R']} linea1-post={sig['line1_paid_post_event']} "
          f"sin-campana={sig['uncovered_new_lines']} -> "
          f"{'CAYO' if sig['fell'] else 'no cayo'} ({result['abort_reason']}, "
          f"{result['wall_seconds']}s)")
    return result


if __name__ == "__main__":
    main()
