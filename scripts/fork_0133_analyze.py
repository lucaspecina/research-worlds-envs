"""Final analysis of the fork experiment (ADR 0133): cross annotations x KEY x scores.

Runs ONLY after both blind annotation passes exist. Opens KEY.json (unblinding),
builds the per-cell table, computes the pre-registered endpoint and applies the
pre-signed readings verbatim.

Endpoint primario: tasa de entregas LIBRES de defectos (a|b|c|d, anotacion de Claude
como primaria; Codex reportado como segundo anotador con acuerdos/desacuerdos).
Primario sobre entregas VALIDAS (sin compras en la entrega); sensibilidad con todas.

Run: .venv/Scripts/python scripts/fork_0133_analyze.py
"""

import json
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BLIND = ROOT / "scripts" / "out" / "fork_0133" / "blind"
CELLS = ROOT / "scripts" / "out" / "fork_0133"

sys.stdout.reconfigure(encoding="utf-8", errors="replace")


def arm_group(arm: str) -> str:
    if arm.startswith("principle"):
        return "principle"
    return arm


def main() -> None:
    key = json.loads((BLIND / "KEY.json").read_text(encoding="utf-8"))
    mine = json.loads((BLIND / "annotations_claude.json").read_text(encoding="utf-8"))
    codex_file = BLIND / "annotations_codex.json"
    codex = json.loads(codex_file.read_text(encoding="utf-8")) if codex_file.exists() else {}

    rows = []
    for pid, meta in sorted(key.items()):
        if "skipped" in meta:
            continue
        cell = json.loads((CELLS / meta["file"]).read_text(encoding="utf-8"))
        m = mine.get(pid, {})
        cx = codex.get(pid, {})
        defects_m = [k for k in "abcd" if m.get(k)]
        defects_x = [k for k in "abcd" if cx.get(k)] if cx else None
        bought = "bought_during_delivery" in (m.get("notes") or "")
        rows.append({
            "pack": pid, "block": meta["block"], "donor": meta["donor"],
            "arm": meta["arm"], "grp": arm_group(meta["arm"]),
            "defects": "".join(defects_m) or "-",
            "defects_codex": ("".join(defects_x) or "-") if defects_x is not None else "?",
            "clean": not defects_m, "bought": bought,
            "valid": (not bought) and cell.get("abort") == "submitted",
            "R": cell.get("R"), "R_uncl": cell.get("R_uncl"),
            "catastrophic": (cell.get("R_uncl") or 0) < 0,
        })

    # ---- per-cell table ----
    print(f"{'pack':5} {'blk':3} {'don':4} {'arm':14} {'def(C)':7} {'def(X)':7} {'clean':6} {'valid':6} {'R':7} {'Runc':7}")
    for r in sorted(rows, key=lambda r: (r["block"], r["donor"], r["grp"])):
        print(f"{r['pack']:5} {r['block']:3} {r['donor']:4} {r['arm']:14} {r['defects']:7} "
              f"{r['defects_codex']:7} {str(r['clean']):6} {str(r['valid']):6} "
              f"{r['R']:.3f}   {r['R_uncl']:+.3f}" if r["R"] is not None else "")

    # ---- inter-annotator agreement ----
    if codex:
        agree = disagree = 0
        dis_list = []
        for r in rows:
            if r["defects_codex"] == "?":
                continue
            for k in "abcd":
                mv = k in r["defects"]
                xv = k in r["defects_codex"]
                if mv == xv:
                    agree += 1
                else:
                    disagree += 1
                    dis_list.append(f"{r['pack']}:{k} (C={mv} X={xv})")
        tot = agree + disagree
        print(f"\nAcuerdo inter-anotador: {agree}/{tot} = {agree/tot:.1%}")
        print("Desacuerdos:", "; ".join(dis_list) if dis_list else "ninguno")

    # ---- endpoint primario ----
    def rate(sel):
        ok = [r for r in sel if r["clean"]]
        return len(ok), len(sel), (len(ok) / len(sel) if sel else float("nan"))

    print("\n=== ENDPOINT PRIMARIO: tasa de entregas libres de defectos (validas) ===")
    for grp in ("neutral", "principle", "scaffold"):
        sel = [r for r in rows if r["grp"] == grp and r["valid"]]
        k, n, p = rate(sel)
        print(f"  {grp:10}: {k}/{n} = {p:.1%}")
    print("--- sensibilidad (todas, incluidas invalidas) ---")
    for grp in ("neutral", "principle", "scaffold"):
        sel = [r for r in rows if r["grp"] == grp]
        k, n, p = rate(sel)
        print(f"  {grp:10}: {k}/{n} = {p:.1%}")

    # per-defect per-arm
    print("\n=== defectos por tipo y brazo (validas) ===")
    for grp in ("neutral", "principle", "scaffold"):
        sel = [r for r in rows if r["grp"] == grp and r["valid"]]
        counts = {k: sum(1 for r in sel if k in r["defects"]) for k in "abcd"}
        print(f"  {grp:10}: " + "  ".join(f"{k}={v}/{len(sel)}" for k, v in counts.items()))

    # per-block clean-rate diff scaffold vs neutral (pre-signed reading needs >=4/5 blocks)
    print("\n=== scaffold vs neutral por bloque (tasa limpia, validas) ===")
    better = 0
    for b in range(5):
        sn = [r for r in rows if r["grp"] == "neutral" and r["block"] == b and r["valid"]]
        ss = [r for r in rows if r["grp"] == "scaffold" and r["block"] == b and r["valid"]]
        _, _, pn = rate(sn)
        _, _, ps = rate(ss)
        mark = "scaffold>" if ps > pn else ("=" if ps == pn else "neutral>")
        if ps > pn:
            better += 1
        print(f"  bloque {b}: neutral {pn:.0%} vs scaffold {ps:.0%}  [{mark}]")
    print(f"  bloques con scaffold mejor: {better}/5")

    # ---- secundarios ----
    print("\n=== SECUNDARIOS ===")
    for grp in ("neutral", "principle", "scaffold"):
        sel = [r for r in rows if r["grp"] == grp]
        rs = [r["R"] for r in sel if r["R"] is not None]
        cat = sum(1 for r in sel if r["catastrophic"])
        inv = sum(1 for r in sel if not r["valid"])
        print(f"  {grp:10}: R medio={sum(rs)/len(rs):.3f}  catastroficas={cat}/{len(sel)}  invalidas={inv}/{len(sel)}")

    # per-variant heterogeneity within principle
    print("\n=== heterogeneidad dentro del brazo principio (por variante) ===")
    per_v = defaultdict(list)
    for r in rows:
        if r["grp"] == "principle":
            per_v[r["arm"]].append(r)
    for v, sel in sorted(per_v.items()):
        k, n, p = rate([r for r in sel if r["valid"]])
        rs = [r["R"] for r in sel if r["R"] is not None]
        print(f"  {v:14}: limpias {k}/{n}  R medio={sum(rs)/len(rs):.3f}")

    # per-donor
    print("\n=== por donante (todas) ===")
    per_d = defaultdict(list)
    for r in rows:
        per_d[r["donor"]].append(r)
    for d, sel in sorted(per_d.items()):
        k, n, p = rate(sel)
        rs = [r["R"] for r in sel if r["R"] is not None]
        print(f"  donante {d}: limpias {k}/{n}  R medio={sum(rs)/len(rs):.3f}")


if __name__ == "__main__":
    main()
