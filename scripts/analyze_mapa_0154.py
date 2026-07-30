"""Analisis PRE-REGISTRADO de la pasada 1 del mapa (ADR 0154) - escrito ANTES
de mirar resultados.

Metricas por celda (donante x brazo):
  S_local  = -CRPS medio sobre la slice congelada (linea elegida x 5 drivers),
             CRPS por muestras contra draws frescos de la verdad (proper).
  dS_local = S_local(brazo) - media de las DOS bases del mismo self/peer x
             draft/bound del donante.
  F        = dS_local / (S_local(oraculo legal) - media bases), solo si la
             mejora legal >= EPS; sin clipear.
  dR       = R(brazo) - media R de las bases (consecuencia global, secundaria).

Freno de calibracion (se evalua PRIMERO): en SELF-DRAFT, mediana por donante
de dS_local debe ordenar CLEAN > MIXED > PLACEBO; si no, INSTRUMENTO ROTO.
Contrastes apareados (sign test por donante): SELF vs PEER, BOUND vs DRAFT,
interacciones (H1-H4 del ADR).

Run: .venv/Scripts/python scripts/analyze_mapa_0154.py
"""

import json
import sys
from pathlib import Path
from types import SimpleNamespace

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
CASE = ROOT / "cases" / "rabbit_hole_v2"
sys.path.insert(0, str(CASE))
import world  # noqa: E402

OUT = ROOT / "scripts" / "out" / "mapa_0154"
SIGMA = 0.7
EPS = 0.01
CAMP_DRIVERS = (0.5, 2.5, 5.0, 7.5, 9.5)
M_MODEL, K_TRUTH = 200, 60

NS = lambda c: SimpleNamespace(config=dict(c), context={}, horizon=None)  # noqa: E731


def exec_model(code):
    env = {}
    exec(code, env)
    return env["model"]


def crps(samples, ys):
    s = np.asarray(samples, float)
    d1 = np.mean([np.mean(np.abs(s - y)) for y in ys])
    d2 = np.mean(np.abs(s[:, None] - s[None, :]))
    return d1 - 0.5 * d2


def s_local(model, line, seed=95001):
    tot = 0.0
    for i, dv in enumerate(CAMP_DRIVERS):
        y = np.asarray(model(NS({"line": line, "driver": dv}), M_MODEL, seed + i)["outcome"], float)
        rng = np.random.default_rng(seed + 100 + i)
        truth = world.g_curve(line, np.full(K_TRUTH, dv)) + rng.normal(0.0, SIGMA, K_TRUTH)
        tot += -crps(y, truth)
    return tot / len(CAMP_DRIVERS)


def legal_oracle(m0, bundle):
    """Update M0 with ONLY the injected rows (no truth): replace its mean at
    observed (line,driver) points by the observed means; keep sd."""
    obs = {}
    for ln, dv, v in bundle["clean_rows"]:
        obs.setdefault((ln, dv), []).append(v)
    means = {k: float(np.mean(v)) for k, v in obs.items()}

    def model(regime, n, seed):
        import pandas as pd
        ln, dv = int(regime.config["line"]), float(regime.config["driver"])
        rng = np.random.default_rng(seed)
        if (ln, dv) in means:
            mu = means[(ln, dv)]
            y = rng.normal(mu, SIGMA, n)
            return pd.DataFrame({"outcome": y})
        y = np.asarray(m0(regime, n, seed)["outcome"], float)
        return pd.DataFrame({"outcome": y})
    return model


def main():
    cells = {}
    for p in OUT.glob("cell_*.json"):
        c = json.loads(p.read_text(encoding="utf-8"))
        if c.get("error") or not c.get("accepted") or not c.get("submission_code"):
            cells[p.stem] = {"donor": c.get("donor"), "arm": c.get("arm"), "invalid": True}
            continue
        cells[p.stem] = c
    bundles = {int(p.stem.split("_d")[1]): json.loads(p.read_text(encoding="utf-8"))
               for p in OUT.glob("bundle_d*.json")}
    donors = sorted(bundles)

    rows = []
    for seed in donors:
        b = bundles[seed]
        line = b["dose"]["line"]
        donor_trace = json.loads((CASE / "traces" / f"e0_gpt-5.4_seed{seed}.json")
                                 .read_text(encoding="utf-8"))
        m0 = exec_model(donor_trace["submission_code"])
        s_oracle = s_local(legal_oracle(m0, b), line)
        s_m0 = s_local(m0, line)
        base_s = {}
        for key in ("self_draft", "self_bound", "peer_draft", "peer_bound"):
            vals = []
            for suf in ("a", "b"):
                c = cells.get(f"cell_d{seed}_{key}_base_{suf}")
                if c and not c.get("invalid"):
                    vals.append(s_local(exec_model(c["submission_code"]), line))
            base_s[key] = float(np.mean(vals)) if vals else None
        for name, c in cells.items():
            if not name.startswith(f"cell_d{seed}_") or "base" in name:
                continue
            arm = c["arm"]
            key = "_".join(arm.split("_")[:2])
            if c.get("invalid") or base_s.get(key) is None:
                rows.append({"donor": seed, "arm": arm, "invalid": True})
                continue
            s_arm = s_local(exec_model(c["submission_code"]), line)
            legal_gain = s_oracle - base_s[key]
            row = {"donor": seed, "arm": arm, "s_local": round(s_arm, 4),
                   "s_base": round(base_s[key], 4), "s_oracle": round(s_oracle, 4),
                   "s_m0": round(s_m0, 4),
                   "dS": round(s_arm - base_s[key], 4),
                   "dR": (round(c["R"] - donor_trace["R"], 4)
                          if c.get("R") is not None else None),
                   "elr_clean": b["dose"]["elr_clean"], "elr_mixed": b["dose"]["elr_mixed"]}
            row["F"] = (round(row["dS"] / legal_gain, 3)
                        if legal_gain >= EPS else None)
            rows.append(row)

    # --- freno de calibracion (PRIMERO) ---------------------------------
    def med(arm):
        v = [r["dS"] for r in rows if r.get("arm") == arm and "dS" in r]
        return float(np.median(v)) if v else None

    cal = {"clean": med("self_draft_clean"), "mixed": med("self_draft_mixed"),
           "placebo": med("self_draft_placebo")}
    cal_ok = (cal["clean"] is not None and cal["mixed"] is not None
              and cal["placebo"] is not None
              and cal["clean"] > cal["mixed"] > cal["placebo"])

    # --- contrastes apareados (solo se INTERPRETAN si cal_ok) -----------
    def paired(arm_a, arm_b):
        diffs = []
        for seed in donors:
            a = next((r for r in rows if r.get("donor") == seed and r.get("arm") == arm_a
                      and "dS" in r), None)
            bb = next((r for r in rows if r.get("donor") == seed and r.get("arm") == arm_b
                       and "dS" in r), None)
            if a and bb:
                diffs.append(a["dS"] - bb["dS"])
        if not diffs:
            return None
        arr = np.array(diffs)
        return {"n": len(arr), "median": round(float(np.median(arr)), 4),
                "pos": int((arr > 0).sum()), "neg": int((arr < 0).sum())}

    contrasts = {
        "H1_self_vs_peer_draft_clean": paired("peer_draft_clean", "self_draft_clean"),
        "H1_self_vs_peer_draft_mixed": paired("peer_draft_mixed", "self_draft_mixed"),
        "H2_draft_vs_bound_self_clean": paired("self_draft_clean", "self_bound_clean"),
        "H2_draft_vs_bound_self_mixed": paired("self_draft_mixed", "self_bound_mixed"),
        "H3_peer_minus_self_bound_mixed": paired("peer_bound_mixed", "self_bound_mixed"),
        "H4_placebo_draft_vs_bound": paired("self_draft_placebo", "self_bound_placebo"),
    }

    n_invalid = sum(1 for r in rows if r.get("invalid"))
    report = {"n_rows": len(rows), "n_invalid": n_invalid,
              "calibracion": {**{k: (round(v, 4) if v is not None else None)
                                 for k, v in cal.items()},
                              "CLEAN>MIXED>PLACEBO": bool(cal_ok),
                              "veredicto": ("instrumento OK" if cal_ok
                                            else "INSTRUMENTO ROTO - no leer hipotesis")},
              "contrastes(dS; interpretar SOLO si calibracion OK)": contrasts,
              "medianas_por_brazo": {a: med(a) for a in sorted({r.get("arm") for r in rows
                                                                if r.get("arm")})}}
    print(json.dumps(report, indent=2, default=str))
    (OUT / "analysis.json").write_text(
        json.dumps({"report": report, "rows": rows}, indent=2, default=str) + "\n",
        encoding="utf-8")


if __name__ == "__main__":
    main()
