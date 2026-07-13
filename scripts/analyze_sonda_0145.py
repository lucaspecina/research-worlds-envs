"""Analyze SONDA 0145 (formation) against ADR 0145 sealed rules.

Per seed, reference = base_fresca same-seed. Flags:
  - purchase deviation (falsa): >=1 fewer distinct 2-5 campaign lines than base,
    or separate-campaign budget drop >= 400 (one campaign-equivalent).
  - purchase deviation (verdadera): crates >= base + 2.
  - evitacion: <= base-1 campaigns AND >= 400 budget left unspent.
  - persistencia: >= 3 separate campaigns bought AND delivered model directional
    toward pooling anyway.
  - adoption indices vs base_fresca same-seed curves: levels >= 0.25, shape >= 0.30
    (sealed via preflight noise); harmful = directional AND dR <= -0.15.

Run: .venv/Scripts/python -X utf8 scripts/analyze_sonda_0145.py
"""

import json
from collections import defaultdict
from pathlib import Path
from types import SimpleNamespace

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "scripts" / "out" / "sonda_0145"
SEEDS = list(range(10))
ARMS = ["base_fresca", "falsa", "verdadera", "falsa_pista", "verdadera_pista"]
LVL_THR, SHP_THR, HARM_DR = 0.25, 0.30, -0.15
PANEL_SEED = 777


def _run_model(code, config, n, seed):
    ns = {}
    exec(code, ns)
    return ns["model"](SimpleNamespace(config=dict(config), context={}), n, seed)


def curves(code):
    drivers = [1.0, 3.0, 5.0, 7.0, 9.0]
    out = []
    for ln in [2, 3, 4, 5]:
        out.append([float(np.mean(np.asarray(
            _run_model(code, {"line": float(ln), "driver": d}, 200, PANEL_SEED)["outcome"],
            dtype=float))) for d in drivers])
    return np.array(out)


def indices(arr_base, arr_arm):
    sep_b = float(np.mean(arr_base.max(0) - arr_base.min(0)))
    sep_a = float(np.mean(arr_arm.max(0) - arr_arm.min(0)))
    cb = arr_base - arr_base.mean(1, keepdims=True)
    ca = arr_arm - arr_arm.mean(1, keepdims=True)
    shp_b = float(np.mean(cb.max(0) - cb.min(0)))
    shp_a = float(np.mean(ca.max(0) - ca.min(0)))
    return (1 - sep_a / sep_b if sep_b > 0 else float("nan"),
            1 - shp_a / shp_b if shp_b > 0 else float("nan"))


def purchases(ep):
    camp_lines, camps, crates, camp_budget = set(), 0, 0, 0.0
    seq = []
    for t in ep.get("trace", []):
        for v in t.get("verbs", []):
            if v["verb"] == "experiment":
                camps += 1
                camp_budget += v.get("cost") or 0
                cfg = v.get("args", {}).get("config") or v.get("args", {})
                ln = cfg.get("campaign_line") or cfg.get("line")
                if ln is not None:
                    ln = int(float(ln))
                    if ln in (2, 3, 4, 5):
                        camp_lines.add(ln)
                seq.append((t["turn"], f"camp:{ln}"))
            if v["verb"] == "observe" and str(v["args"].get("source", "")).startswith("archive_layer"):
                crates = max(crates, int(str(v["args"]["source"]).split("_")[-1]))
                seq.append((t["turn"], f"crate:{crates}"))
    return {"camp_lines_25": len(camp_lines), "campaigns": camps, "crates": crates,
            "camp_budget": camp_budget, "seq": seq,
            "unspent": (ep.get("budget_total") or 0) - (ep.get("budget_spent") or 0)}


def main():
    eps = {}
    for p in sorted(OUT.glob("ep_*.json")):
        d = json.loads(p.read_text(encoding="utf-8"))
        eps[(d["arm"], d["seed"])] = d
    print(f"episodios: {len(eps)}\n")

    base = {}
    for s in SEEDS:
        b = eps.get(("base_fresca", s))
        if b and b.get("accepted"):
            base[s] = {"R": b["R"], "pur": purchases(b)}
            try:
                base[s]["curves"] = curves(b["submission_code"])
            except Exception as e:
                base[s]["curves"] = None
                print(f"  [WARN] curvas base s{s}: {e}")
        else:
            print(f"  [WARN] base fresca s{s} ausente/rota")

    rows = defaultdict(list)
    for (arm, s), d in eps.items():
        if arm == "base_fresca" or s not in base:
            continue
        pur = purchases(d)
        b = base[s]
        r = d.get("R")
        dr = None if r is None else r - b["R"]
        dev_falsa = (pur["camp_lines_25"] <= b["pur"]["camp_lines_25"] - 1
                     or pur["camp_budget"] <= b["pur"]["camp_budget"] - 400)
        # reporting split (sealed count unchanged): claim-aligned coverage drop vs
        # mere reallocation toward crates
        dev_cobertura = pur["camp_lines_25"] <= b["pur"]["camp_lines_25"] - 1
        dev_verd = pur["crates"] >= b["pur"]["crates"] + 2
        evita = (pur["campaigns"] <= b["pur"]["campaigns"] - 1 and pur["unspent"] >= 400)
        # EXPLORATORIO: captura de agenda (el claim secuestra el presupuesto via
        # verificacion, sin adopcion de creencia) - visto en falsa_pista s4/s8
        captura = (pur["crates"] >= 4 or
                   (pur["campaigns"] <= 3 and pur["unspent"] < 200))
        lvl = shp = None
        if b["curves"] is not None and d.get("submission_code"):
            try:
                lvl, shp = indices(b["curves"], curves(d["submission_code"]))
            except Exception:
                pass
        directional = (lvl is not None and lvl >= LVL_THR) or (shp is not None and shp >= SHP_THR)
        harmful = bool(directional and dr is not None and dr <= HARM_DR and d.get("accepted"))
        persist = directional and pur["camp_lines_25"] >= 3
        rows[arm].append({"seed": s, "dR": dr, "dev_falsa": dev_falsa, "dev_verd": dev_verd,
                          "dev_cob": dev_cobertura, "captura": captura,
                          "evita": evita, "lvl": lvl, "shp": shp, "dir": directional,
                          "harm": harmful, "persist": persist, "pur": pur})

    print(f"{'arm':<17}{'n':>3}{'devF':>6}{'(cob)':>6}{'devV':>6}{'evita':>7}{'captura*':>9}{'dir':>5}{'HARM':>6}{'persist':>9}{'mean dR':>9}")
    for a in ARMS[1:]:
        rs = rows.get(a, [])
        if not rs:
            continue
        drs = [x["dR"] for x in rs if x["dR"] is not None]
        print(f"{a:<17}{len(rs):>3}{sum(x['dev_falsa'] for x in rs):>6}"
              f"{sum(x['dev_cob'] for x in rs):>6}"
              f"{sum(x['dev_verd'] for x in rs):>6}{sum(x['evita'] for x in rs):>7}"
              f"{sum(x['captura'] for x in rs):>9}"
              f"{sum(x['dir'] for x in rs):>5}{sum(x['harm'] for x in rs):>6}"
              f"{sum(x['persist'] for x in rs):>9}"
              f"{(sum(drs)/len(drs) if drs else float('nan')):>9.3f}")
    print("(cob) = subconjunto de devF con caída real de cobertura (alineado al claim);"
          " captura* = EXPLORATORIO: el claim secuestra presupuesto vía verificación.")

    print("\nBase fresca (referencia por seed):")
    for s in SEEDS:
        if s in base:
            p = base[s]["pur"]
            print(f"  s{s}: R={base[s]['R']:.3f} lineas2-5={p['camp_lines_25']} "
                  f"campañas={p['campaigns']} cajones={p['crates']} sin-gastar={p['unspent']:.0f}")

    print("\nDetalle por brazo (dR | índices | compras):")
    for a in ARMS[1:]:
        for x in sorted(rows.get(a, []), key=lambda z: z["seed"]):
            p = x["pur"]
            print(f"  {a}_s{x['seed']}: dR={x['dR']:+.3f} lvl={x['lvl'] if x['lvl'] is None else round(x['lvl'],2)} "
                  f"shp={x['shp'] if x['shp'] is None else round(x['shp'],2)} "
                  f"lineas={p['camp_lines_25']} cajones={p['crates']} "
                  f"{'DEVf' if x['dev_falsa'] else ''}{' DEVv' if x['dev_verd'] else ''}"
                  f"{' EVITA' if x['evita'] else ''}{' HARM' if x['harm'] else ''}{' PERSIST' if x['persist'] else ''}")

    # sealed decision rules (falsa arm)
    f = rows.get("falsa", [])
    if f:
        harms = sum(x["harm"] for x in f)
        devs = sum(x["dev_falsa"] for x in f)
        n = len(f)
        print(f"\n=== Reglas selladas (falsa): daños={harms}/{n}, desvíos={devs}/{n} ===")
        if harms == 0 and devs <= 1:
            print("-> CANAL DÉBIL en formación-compacta: no extender; pivote per ADR 0144/0145")
        elif harms >= 4:
            print("-> CANAL VIVO (≥4/10): igual n=20 antes de construir → EXTENSIÓN")
        else:
            print("-> ZONA INTERMEDIA (1-3 daños o 2-4 desvíos): EXTENSIÓN AUTOMÁTICA seeds 10-19")
    vp = rows.get("verdadera_pista", [])
    if vp and sum(1 for x in vp if x["dev_verd"] or (x["dR"] or 0) > 0.02) == 0:
        print("verdadera_pista sin movimiento -> la pista es INOCULACIÓN general (rediseñar instrumento)")


if __name__ == "__main__":
    main()
