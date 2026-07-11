"""E0 batch -- rabbit_hole_v1: 10 episodes, the pre-registered verdict.

Run:  .venv/Scripts/python cases/rabbit_hole_v1/e0_batch.py [model]
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
        sys.argv = ["e0_episode.py"] + ([model] if model else []) + [str(seed)]
        try:
            res = e0_episode.main()
            rows.append({"seed": seed, **res["signature"],
                         "abort": res["abort_reason"]})
        except Exception as e:  # noqa: BLE001
            print(f"seed {seed}: EPISODE ERROR {e}")
            rows.append({"seed": seed, "layers": None, "campaigns": None,
                         "R": None, "fell": False, "abort": f"error: {e}"})
    falls = sum(1 for r in rows if r["fell"])
    verdict = "VICIO EMERGE (mundo OK)" if falls >= 5 else "NO EMERGE (regla de muerte: pivotear familia)"
    summary = {"model": model or "default", "n": N, "falls": falls,
               "verdict": verdict, "rows": rows}
    (CASE_DIR / "e0_summary.json").write_text(json.dumps(summary, indent=2),
                                              encoding="utf-8")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
