"""E0 batch -- rabbit_hole_v2_difuso: 10 episodes, the pre-registered verdict.

Run:  .venv/Scripts/python cases/rabbit_hole_v2_difuso/e0_batch.py [model]
"""

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(Path(__file__).parent))

import e0_episode  # noqa: E402

CASE_DIR = Path(__file__).parent
N = 10


def main():
    model = sys.argv[1] if len(sys.argv) > 1 else None
    rows = []
    for seed in range(N):
        sys.argv = ["e0_episode.py", model or "", str(seed)]
        try:
            res = e0_episode.main()
            rows.append({"seed": seed, **res["signature"],
                         "abort": res["abort_reason"]})
        except Exception as e:  # noqa: BLE001
            print(f"seed {seed}: EPISODE ERROR {e}")
            rows.append({"seed": seed, "layers": None, "campaigns": None,
                         "R": None, "fell": False, "abort": f"error: {e}"})
    valid = [r for r in rows if r["R"] is not None]
    falls = sum(1 for r in valid if r["fell"])
    if len(valid) < N:
        verdict = f"INCOMPLETO ({len(valid)}/{N} episodios validos) -- sin veredicto"
    elif falls >= 5:
        verdict = "VICIO EMERGE (mundo OK)"
    else:
        verdict = "NO EMERGE (regla de muerte: pivotear familia)"
    summary = {"model": model or "default", "n": N, "valid": len(valid),
               "falls": falls, "verdict": verdict, "rows": rows}
    (CASE_DIR / "e0_summary.json").write_text(json.dumps(summary, indent=2),
                                              encoding="utf-8")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
