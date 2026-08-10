"""Análisis de la tanda v1 contra las reglas PRE-REGISTRADAS (ficha + addenda).

Todo cero-LLM. Produce:
  A. tabla por celda (brazo, seed, S, familia, expansión, gap, cadena)
  B. H-V1 contra su regla firmada (VISIBLE−RAW >= 2 en expansión generativa)
  C. H-V2 / H-V3 según lo pre-registrado
  D. outcome ordinal secundario (escalera de Darden anidada en las 5 salidas)
  E. gemelo bilateral (espurio por brazo)
  F. la lista de códigos registrados a leer OFFLINE (validación semántica del
     clasificador mecánico — jamás toca el reward)

Run: .venv/bin/python scripts/analyze_count_regime_impasse_v1.py
"""

from __future__ import annotations

import json
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

OUT = ROOT / "scripts/out/count_regime_impasse_v1"


def load_cells() -> list[dict]:
    return [json.loads(p.read_text()) for p in sorted(OUT.glob("v1_impasse*.json"))]


def exit_category(p: dict) -> str:
    """Las cinco salidas del protocolo, mecánicas."""
    ins = p["instruments"]
    if not ins.get("scored"):
        return "abandono" if p["abort_reason"] != "submitted" else "entrega_invalida"
    fam = ins.get("structural", {}).get("family")
    if fam == "regime":
        return ("familia_nueva_correcta" if (ins.get("S_quiebre_fuerte") or 0) >= 0.3
                else "familia_nueva_incorrecta")
    n_regs = p.get("n_registrations", 0)
    return "rerank_misma_familia" if n_regs >= 2 else "perseverar"


def main() -> int:
    cells = load_cells()
    brk = [c for c in cells if c["pole"] == "brk"]
    smooth = [c for c in cells if c["pole"] == "smooth"]
    print(f"celdas: {len(cells)} (brk {len(brk)}, smooth {len(smooth)})\n")

    # --- A. tabla por celda -------------------------------------------------
    print("=== A. por celda ===")
    for c in sorted(brk, key=lambda x: (x["arm"], x["seed"])):
        t, ins = c["timing"], c["instruments"]
        ev = t.get("first_regime_event") or {}
        chain = " ".join(f"{e['event']}@{e['turn']}" for e in c["chain"])
        print(f"{c['arm']:22s} {c['seed']} S={ins.get('S_quiebre_fuerte', 0):.2f} "
              f"exp={str(t['expansion_generativa']):5s} gap={t.get('dbic_gap_at_event')} "
              f"regime@{ev.get('turn')} | {chain}")

    # --- B. H-V1 ------------------------------------------------------------
    exp = defaultdict(list)
    for c in brk:
        exp[c["arm"]].append(bool(c["timing"]["expansion_generativa"]))
    print("\n=== B. H-V1 (regla firmada: senal si VISIBLE-RAW >= 2) ===")
    counts = {arm: (sum(v), len(v)) for arm, v in exp.items()}
    for arm, (k, n) in sorted(counts.items()):
        print(f"  {arm:22s} expansion generativa {k}/{n}")
    raw_k = counts.get("RAW", (0, 0))[0]
    for visarm in ("VISIBLE_GLOBAL", "VISIBLE_ESTRUCTURADO"):
        vk = counts.get(visarm, (0, 0))[0]
        diff = vk - raw_k
        verdict = "SENAL A FAVOR" if diff >= 2 else ("INVERTIDA" if diff <= -2 else "SIN SENAL")
        print(f"  {visarm} - RAW = {diff:+d}  -> {verdict}")

    # --- C. H-V2 / H-V3 -----------------------------------------------------
    print("\n=== C. H-V2 (RAW ~ 0, exploratoria) y H-V3 (tras el 2o fallo) ===")
    print(f"  H-V2: RAW = {raw_k}/{counts.get('RAW', (0, 0))[1]} "
          f"-> {'REFUTADA' if raw_k > 1 else 'compatible'}")
    after2 = before2 = 0
    for c in brk:
        ev = c["timing"].get("first_regime_event") or {}
        p2 = next((e["turn"] for e in c["chain"] if e["event"] == "pilot_2"), None)
        if ev.get("turn") is not None and p2 is not None:
            if ev["turn"] > p2:
                after2 += 1
            else:
                before2 += 1
    print(f"  H-V3: primer evento regime ANTES del piloto 2: {before2} · DESPUES: {after2} "
          f"-> {'REFUTADA (mayoria antes)' if before2 > after2 else 'compatible'}")

    # --- D. salidas / ordinal ----------------------------------------------
    print("\n=== D. las cinco salidas (por brazo) ===")
    tab = defaultdict(lambda: defaultdict(int))
    for c in brk:
        tab[c["arm"]][exit_category(c)] += 1
    for arm, d in sorted(tab.items()):
        print(f"  {arm:22s} " + "  ".join(f"{k}={v}" for k, v in sorted(d.items())))

    # --- E. gemelo ----------------------------------------------------------
    print("\n=== E. gemelo bilateral ===")
    for c in sorted(smooth, key=lambda x: x["seed"]):
        ins = c["instruments"]
        print(f"  {c['arm']:22s} {c['seed']} S_clean={ins.get('S_clean', 0):.2f} "
              f"espurio={ins.get('espurio', {}).get('spurious')} "
              f"fam={ins.get('structural', {}).get('family')}")

    # --- F. cola offline ----------------------------------------------------
    n_regs = sum(c.get("n_registrations", 0) for c in cells)
    print(f"\n=== F. validacion offline pendiente: {n_regs} codigos registrados en "
          f"{len(cells)} episodios (leer si postulan DOS LEYES o curva flexible) ===")

    # medias de S por brazo
    print("\n=== S promedio por brazo (entrega) ===")
    for arm in sorted({c['arm'] for c in brk}):
        vals = [c["instruments"].get("S_quiebre_fuerte") or 0.0
                for c in brk if c["arm"] == arm and c["instruments"].get("scored")]
        if vals:
            print(f"  {arm:22s} media={sum(vals)/len(vals):.3f}  n={len(vals)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
