"""Probe 0135 stage-1 analysis: pre-signed readings, verbatim from ADR 0135.

Pass criterion per delivery: regret_mean <= 2.0 AND regret_max <= 3.0 (sealed).
Reading (i) "format is NOT the bottleneck": >=14/15 arm-A deliveries pass, zero
catastrophic (regret_mean > 10), majority of passes in all 5 blocks.

Run: .venv/Scripts/python scripts/probe_0135_analyze.py
"""

import json
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "scripts" / "out" / "probe_0135" / "stage1"
TAU_MEAN, TAU_MAX = 2.0, 3.0

sys.stdout.reconfigure(encoding="utf-8", errors="replace")


def main() -> None:
    cells = [json.loads(p.read_text(encoding="utf-8")) for p in sorted(OUT.glob("cell_*.json"))]
    print(f"celdas: {len(cells)}")
    by_arm = defaultdict(list)
    for c in cells:
        by_arm[c["arm"]].append(c)

    print(f"\n{'arm':4} {'n':3} {'pasan':6} {'1er-intento':11} {'regret_mean (med/max)':24} {'catastroficas':13}")
    for arm in ("A", "B", "C"):
        sel = by_arm[arm]
        ok = [c for c in sel if c.get("regret_mean") is not None
              and c["regret_mean"] <= TAU_MEAN and c["regret_max"] <= TAU_MAX]
        first = sum(1 for c in sel if c.get("passed_first_try"))
        means = sorted(c["regret_mean"] for c in sel if c.get("regret_mean") is not None)
        cat = sum(1 for c in sel if (c.get("regret_mean") or 0) > 10)
        med = means[len(means) // 2] if means else float("nan")
        mx = max(means) if means else float("nan")
        print(f"{arm:4} {len(sel):3} {len(ok):6} {first:11} {med:.3f} / {mx:.3f}{'':10} {cat:13}")

    # per-block pass rate for arm A (pre-signed: majority of passes in all blocks)
    print("\nbrazo A por bloque (pasan/total):")
    for b in range(5):
        sel = [c for c in by_arm["A"] if c["block"] == b]
        ok = sum(1 for c in sel if c.get("regret_mean") is not None
                 and c["regret_mean"] <= TAU_MEAN and c["regret_max"] <= TAU_MAX)
        print(f"  bloque {b}: {ok}/{len(sel)}")

    # verdict per pre-signed reading (i)
    a = by_arm["A"]
    a_ok = [c for c in a if c.get("regret_mean") is not None
            and c["regret_mean"] <= TAU_MEAN and c["regret_max"] <= TAU_MAX]
    a_cat = sum(1 for c in a if (c.get("regret_mean") or 0) > 10)
    blocks_ok = all(
        sum(1 for c in a if c["block"] == b and c.get("regret_mean") is not None
            and c["regret_mean"] <= TAU_MEAN and c["regret_max"] <= TAU_MAX) >= 2
        for b in range(5))
    reading_i = len(a_ok) >= 14 and a_cat == 0 and blocks_ok
    print(f"\nLECTURA (i) 'el formato NO es cuello': "
          f"{'SE CUMPLE' if reading_i else 'NO se cumple'} "
          f"(A pasan {len(a_ok)}/15, catastroficas {a_cat}, bloques ok {blocks_ok})")


if __name__ == "__main__":
    main()
