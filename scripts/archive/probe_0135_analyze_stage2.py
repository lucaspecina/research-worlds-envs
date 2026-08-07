"""Stage-2 analysis: order preservation across the belief ladder (pre-signed).

Per rung: fidelity vs its OWN reference (must sit at floor: mean<=2, max<=3) and
quality vs TRUTH. Order preserved = median quality(truth deliveries from stage 1)
< quality(intermediate) < quality(folklore), in every block, with no overlap of
the per-block medians.

Run: .venv/Scripts/python scripts/probe_0135_analyze_stage2.py
"""

import json
import sys
from collections import defaultdict
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
S1 = ROOT / "scripts" / "out" / "probe_0135" / "stage1"
S2 = ROOT / "scripts" / "out" / "probe_0135" / "stage2"
TAU_MEAN, TAU_MAX = 2.0, 3.0

sys.stdout.reconfigure(encoding="utf-8", errors="replace")


def main() -> None:
    s2 = [json.loads(p.read_text(encoding="utf-8")) for p in sorted(S2.glob("cell_*.json"))]
    # stage-1 arm A deliveries are the 'truth' rung (quality == their regret vs truth)
    s1 = [json.loads(p.read_text(encoding="utf-8")) for p in sorted(S1.glob("cell_*_A*.json"))]
    truth_q = {b: [c["regret_mean"] for c in s1 if c["block"] == b] for b in range(5)}

    by_rung = defaultdict(list)
    for c in s2:
        by_rung[c["rung"]].append(c)

    print(f"{'rung':13} {'n':3} {'fidelidad med (pasa piso)':26} {'calidad-vs-verdad med':22} {'1er intento':11}")
    med_all = {"truth": float(np.median([q for b in truth_q.values() for q in b]))}
    for rung in ("intermediate", "folklore"):
        sel = by_rung[rung]
        fid = [c["fidelity_mean"] for c in sel if c.get("fidelity_mean") is not None]
        qual = [c["quality_vs_truth_mean"] for c in sel if c.get("quality_vs_truth_mean") is not None]
        ok = sum(1 for c in sel if c.get("fidelity_mean") is not None
                 and c["fidelity_mean"] <= TAU_MEAN and c["fidelity_max"] <= TAU_MAX)
        first = sum(1 for c in sel if c.get("attempts") == 1)
        med_all[rung] = float(np.median(qual)) if qual else float("nan")
        print(f"{rung:13} {len(sel):3} {np.median(fid):.3f} ({ok}/{len(sel)}){'':12} "
              f"{np.median(qual):10.1f}{'':10} {first:11}")
    print(f"{'truth (s1-A)':13} {sum(len(v) for v in truth_q.values()):3} "
          f"{'(=fidelidad, ya reportada)':26} {med_all['truth']:10.3f}")

    print("\norden por bloque (mediana calidad-vs-verdad):")
    order_ok_all = True
    for b in range(5):
        t = float(np.median(truth_q[b]))
        i = float(np.median([c["quality_vs_truth_mean"] for c in by_rung["intermediate"]
                             if c["block"] == b and c.get("quality_vs_truth_mean") is not None]))
        f = float(np.median([c["quality_vs_truth_mean"] for c in by_rung["folklore"]
                             if c["block"] == b and c.get("quality_vs_truth_mean") is not None]))
        ok = t < i < f
        order_ok_all = order_ok_all and ok
        print(f"  bloque {b}: verdad {t:6.2f} < intermedio {i:8.1f} < folklore {f:8.1f}  "
              f"[{'OK' if ok else 'ROTO'}]")

    fid_ok = all(
        c.get("fidelity_mean") is not None and c["fidelity_mean"] <= TAU_MEAN
        and c["fidelity_max"] <= TAU_MAX
        for rung in ("intermediate", "folklore") for c in by_rung[rung])
    print(f"\nESCALERA: orden preservado en 5/5 bloques: {order_ok_all}; "
          f"fidelidad de todos los peldanos al piso: {fid_ok}")
    print("VEREDICTO ETAPA 2: " + ("LA TRADUCCION PRESERVA LA SENAL"
          if order_ok_all and fid_ok else "SENAL DEGRADADA — ver detalle"))


if __name__ == "__main__":
    main()
