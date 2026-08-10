"""Análisis PRE-REGISTRADO de la tanda D1 (ficha 2026-08-10, congelada con el GO).

Escrito ANTES de ver ningún dato de tanda (disciplina de pre-registro; el técnico
solo valida harness). Reglas congeladas:

PRIMARIO (por polo, n=15):
  Y = 1[D_pre >= 0.25 bits] * 1[gate del polo]   (mecánico, cero-LLM, server-side)
  H0: p = 0.25 (tasa de acierto por reflejo direccional + azar de conducta)
  Test binomial EXACTO unilateral (greater), región crítica del diseño A4:
  n=15 -> k crítico 8, alfa real 0.017 (<= 0.031 declarado en la ficha).

SECUNDARIO (descriptivo, sin reward):
  - conducta (D_pre >= tau) y gate por separado; S medio por polo
  - mezcla de canales comprados (estandar / revial / mismo-vial / lab / señuelos)
  - timing: primera compra DISCRIMINANTE antes vs después del monitoreo (turno 5)
    (la lectura "espontáneo": ¿el triage aparece recién cuando la anomalía llega?)
  - gemelo apareado por seed: pares discordantes (McNemar exacto, descriptivo)
  - trayectorias w_v; presupuesto gastado; submits tempranos; turnos; tokens

Run: .venv/bin/python scripts/analyze_d1_calibracion.py [--dir scripts/out/d1_calibracion]
"""

from __future__ import annotations

import argparse
import json
from math import comb
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DIR = ROOT / "scripts/out/d1_calibracion"
TAU = 0.25
MONITOR_TURN = 5
P0 = 0.25


def exact_binom_greater(k: int, n: int, p0: float) -> float:
    return float(sum(comb(n, i) * p0**i * (1 - p0) ** (n - i) for i in range(k, n + 1)))


def critical_k(n: int, p0: float, alpha: float = 0.05) -> tuple[int, float]:
    for k in range(n + 1):
        a = exact_binom_greater(k, n, p0)
        if a <= alpha:
            return k, a
    return n + 1, 0.0


def load(dir_: Path, tag: str = "tanda") -> list[dict]:
    out = []
    for p in sorted(dir_.glob(f"{tag}_*.json")):
        out.append(json.loads(p.read_text()))
    return out


def first_discriminating_turn(rec: dict) -> int | None:
    for p in rec["outcome"]["purchases"]:
        if p.get("d_bits", 0.0) > 0.0:
            return int(p["turn"])
    return None


def channel_mix(rec: dict) -> dict:
    mix: dict = {}
    for p in rec["outcome"]["purchases"]:
        mix[p["kind"]] = mix.get(p["kind"], 0) + 1
    return mix


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dir", default=str(DEFAULT_DIR))
    ap.add_argument("--tag", default="tanda")
    args = ap.parse_args()
    recs = load(Path(args.dir), args.tag)
    if not recs:
        print(f"sin archivos {args.tag}_*.json — nada que analizar")
        return 1

    by_pole: dict[str, list[dict]] = {"proceso": [], "instrumento": []}
    for r in recs:
        by_pole[r["pole"]].append(r)

    print("=" * 72)
    print("ANALISIS PRE-REGISTRADO D1 — tanda")
    print("=" * 72)

    for pole, rs in by_pole.items():
        if not rs:
            continue
        n = len(rs)
        ys = [r["outcome"]["Y"] for r in rs]
        cond = [int(r["outcome"]["conducta"]) for r in rs]
        gate = [int(r["outcome"]["gate"]) for r in rs]
        svals = [r["outcome"]["S"] for r in rs if r["outcome"]["S"] is not None]
        dpre = [r["outcome"]["D_pre"] for r in rs]
        k = sum(ys)
        kcrit, areal = critical_k(n, P0, 0.05)
        pval = exact_binom_greater(k, n, P0)
        print(f"\n--- polo {pole} (n={n}) ---")
        print(f"PRIMARIO  Y: {k}/{n} = {k/n:.0%} | H0 p={P0} | k critico={kcrit} "
              f"(alfa real {areal:.3f}) | p-valor exacto={pval:.4f} | "
              f"{'RECHAZA H0' if k >= kcrit else 'no rechaza'}")
        print(f"conducta (D_pre>=tau): {sum(cond)}/{n} | gate: {sum(gate)}/{n} | "
              f"S medio: {np.mean(svals):.3f} (n={len(svals)})" if svals else
              f"conducta: {sum(cond)}/{n} | gate: {sum(gate)}/{n} | sin S")
        print(f"D_pre: mediana {np.median(dpre):.3f} | min {min(dpre):.3f} | "
              f"max {max(dpre):.3f}")
        mixes: dict = {}
        for r in rs:
            for kind, c in channel_mix(r).items():
                mixes[kind] = mixes.get(kind, 0) + c
        print(f"canales comprados (total): {dict(sorted(mixes.items()))}")
        f_turns = [first_discriminating_turn(r) for r in rs]
        pre = sum(1 for t in f_turns if t is not None and t < MONITOR_TURN)
        post = sum(1 for t in f_turns if t is not None and t >= MONITOR_TURN)
        nunca = sum(1 for t in f_turns if t is None)
        print(f"primera compra discriminante: pre-monitoreo {pre} | "
              f"post-monitoreo {post} | nunca {nunca}")
        esub = sum(len(r.get('chain', [])) and
                   sum(1 for c in r['chain'] if c['event'] == 'early_submit_attempt')
                   for r in rs)
        print(f"submits tempranos: {esub} | gasto medio: "
              f"{np.mean([r['budget_spent'] for r in rs]):.0f} | turnos medios: "
              f"{np.mean([len(r['trace']) for r in rs]):.1f} | abort: "
              f"{ {a: sum(1 for r in rs if r['abort_reason']==a) for a in set(r['abort_reason'] for r in rs)} }")

    # gemelo apareado por seed (descriptivo)
    pa = {r["seed"]: r for r in by_pole["proceso"]}
    pb = {r["seed"]: r for r in by_pole["instrumento"]}
    shared = sorted(set(pa) & set(pb))
    if shared:
        print(f"\n--- apareo gemelo (n pares={len(shared)}) ---")
        b = sum(1 for s in shared if pa[s]["outcome"]["Y"] and not pb[s]["outcome"]["Y"])
        c = sum(1 for s in shared if not pa[s]["outcome"]["Y"] and pb[s]["outcome"]["Y"])
        both = sum(1 for s in shared if pa[s]["outcome"]["Y"] and pb[s]["outcome"]["Y"])
        none = len(shared) - b - c - both
        p_mcnemar = (sum(comb(b + c, i) for i in range(min(b, c) + 1)) / 2 ** (b + c) * 2
                     if (b + c) else 1.0)
        print(f"ambos Y=1: {both} | solo proceso: {b} | solo instrumento: {c} | "
              f"ninguno: {none} | McNemar exacto (descriptivo) p={min(p_mcnemar, 1.0):.3f}")

    print("\n(las reglas de este script quedaron congeladas antes de la tanda; "
          "cualquier análisis extra se rotula POST-HOC en el dossier)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
