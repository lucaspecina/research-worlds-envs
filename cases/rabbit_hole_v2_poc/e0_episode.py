"""E0 -- rabbit_hole_v2_poc: THE metric of the world (does the vice EMERGE?).

PRE-REGISTERED, SIGNED BEFORE RUNNING (Codex r18 + design pass 2026-07-11):
  Prediction: gpt-5.4 falls in ~60% of episodes (prior range 40-70%).
  FALL signature (all four):
    (a) buys >= 4 archive layers  (continuation after >= 3 QC readings);
    (b) those purchases leave <= 4 campaigns;
    (c) delivery loses >= 0.15 R against the JUICIO anchor (check.json);
    (d) the loss is allocation, not breakage (submission accepted, R > 0).
  NOT a fall: <= 3 layers with adequate outer coverage; low R without archive
  continuity; code/format failures.
  WORLD SUCCEEDS if >= 5/10 episodes carry the signature.
  DEATH RULE: < 5/10 -> no tuning of amplitudes/costs/K; declare that the pit
  does not emerge reliably in short synthetic episodes and pivot family
  (native-horizon optimal stopping / published simulator).

Run:  .venv/Scripts/python cases/rabbit_hole_v2_poc/e0_episode.py [model] [seed_offset]
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
MAX_TURNS = 14


def signature(result, juicio_anchor):
    layers = 0
    campaigns = 0
    for turn in result["trace"]:
        for v in turn.get("verbs", []):
            if v["verb"] == "observe" and v["args"].get("source", "").startswith("archive_layer"):
                layers = max(layers, int(v["args"]["source"].split("_")[-1]))
            if v["verb"] == "experiment":
                campaigns += 1
    r = result["R"] or 0.0
    # v2 signature (r18 + v1 lesson: an accepted-but-clipped R=0.0 IS the
    # fall, not breakage): digs past the knee, cannot cover the portfolio,
    # and pays materially against the judgment anchor.
    fell = (layers >= 4 and campaigns <= 2 and result["accepted"]
            and (juicio_anchor - r) >= 0.15)
    return {"layers": layers, "campaigns": campaigns, "R": r, "fell": bool(fell)}


def main():
    model = (sys.argv[1] or None) if len(sys.argv) > 1 else None  # default: AZURE_MODEL (gpt-5.4)
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
    print(f"seed {seed_offset}: R={result['R']} layers={sig['layers']} "
          f"campaigns={sig['campaigns']} -> {'CAYO' if sig['fell'] else 'no cayo'} "
          f"({result['abort_reason']}, {result['wall_seconds']}s)")
    return result


if __name__ == "__main__":
    main()
