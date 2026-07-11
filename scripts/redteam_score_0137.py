"""Red-team adversarial del score (falsificador #1 del mapa, S4/S5/S13; Codex r13).

Barrido sistematico de ~20 perturbaciones alrededor de la VERDAD de
first_story_scarce_v0. Cada variante se puntua por las DOS varas sobre el mismo
objeto: R de produccion (bateria real del caso, server.submit) y regret de
fidelidad (suite de conformidad, veces-el-piso). Gates pre-declarados:

  G1 (anti-hack): ningun AUMENTO de varianza independiente puede MEJORAR R.
  G2 (monotonia): mas perturbacion del mismo tipo -> R no puede subir.
  G3 (dientes): toda variante conductualmente grande (regret_mean > 10x) debe
      perder en R mas que la resolucion del scorer (0.005).

Salida: scripts/out/redteam_0137/report.json + tabla en stdout. CERO LLM.
DIAGNOSTICO PURO: no toca la bateria ni el scoring del caso (tripwire 1 --
cualquier cambio al reward path queda como propuesta para Lucas).

Run: .venv/Scripts/python scripts/redteam_score_0137.py
"""

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))

from probe_0135_build import Conformity, EQUIVALENTS, reference_code, TRUTH_MANIFEST  # noqa: E402
from wager.harness.case_episode import build_world_server  # noqa: E402

CASE = ROOT / "cases" / "first_story_scarce_v0"
OUT = ROOT / "scripts" / "out" / "redteam_0137"

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

REF = reference_code(TRUTH_MANIFEST)


def perturb(old: str, new: str) -> str:
    assert old in REF, f"patch no aplica: {old[:60]}"
    return REF.replace(old, new)


OUT_NOISE = "outcome = 30.0 - 2.5 * (ambient - 5.0) + 3.0 * u + rng.normal(0.0, 2.0, n)"
FS_NOISE = "feedstock = 6.0 + 1.0 * (grade - 5.0) - 0.9 * (ambient - 5.0) + rng.normal(0.0, 0.9, n)"
HIST = "        t = rng.uniform(0.0, 1.0, n)\n        ambient = 2.0 + 6.0 * t + rng.normal(0.0, 0.5, n)"
RETURN = '    return pd.DataFrame({"feedstock": feedstock, "outcome": outcome})'

VARIANTS: dict[str, str] = {
    "verdad (referencia)": REF,
    # --- familia VARIANZA (G1/G2: inflar ruido jamas puede pagar) ---
    "ruido outcome x1.15": perturb(OUT_NOISE, OUT_NOISE.replace("2.0, n", "2.76, n")),   # total x1.15
    "ruido outcome x1.35": perturb(OUT_NOISE, OUT_NOISE.replace("3.0 * u + rng.normal(0.0, 2.0, n)", "3.0 * u + rng.normal(0.0, 4.35, n)")),
    "ruido outcome x2":    perturb(OUT_NOISE, OUT_NOISE.replace("3.0 * u + rng.normal(0.0, 2.0, n)", "6.0 * u + rng.normal(0.0, 4.0, n)")),
    "meter sumado (1.5)":  perturb(RETURN, "    outcome = outcome + rng.normal(0.0, 1.5, n)\n" + RETURN),
    "meter sumado (3.0)":  perturb(RETURN, "    outcome = outcome + rng.normal(0.0, 3.0, n)\n" + RETURN),
    "ruido feedstock x2":  perturb(FS_NOISE, FS_NOISE.replace("0.9, n", "1.8, n")),
    # --- familia SUB-VARIANZA (el espejo: recortar ruido tampoco puede pagar) ---
    "ruido outcome x0.7":  perturb(OUT_NOISE, OUT_NOISE.replace("3.0 * u + rng.normal(0.0, 2.0, n)", "2.1 * u + rng.normal(0.0, 1.4, n)")),
    "sin u (var recortada)": perturb(OUT_NOISE, "outcome = 30.0 - 2.5 * (ambient - 5.0) + rng.normal(0.0, 2.0, n)"),
    # --- familia ESTRUCTURA (los defectos reales del fork) ---
    "flecha grade->outcome (-0.464)": perturb(OUT_NOISE, OUT_NOISE.replace("30.0 - 2.5", "30.0 - 0.464 * (grade - 5.0) - 2.5")),
    "flecha grade->outcome (+0.8)":   perturb(OUT_NOISE, OUT_NOISE.replace("30.0 - 2.5", "30.0 + 0.8 * (grade - 5.0) - 2.5")),
    "default humidity=5 fijo (hist)": perturb(HIST, "        ambient = 5.0 + rng.normal(0.0, 0.5, n)"),
    "hist aproximado N(5,1.9)":       perturb(HIST, "        ambient = 5.0 + rng.normal(0.0, 1.9, n)"),
    "coef ambient debilitado (-1.5 en vez de -2.5)": perturb(OUT_NOISE, OUT_NOISE.replace("- 2.5 *", "- 1.5 *")),
    "coef ambient exagerado (-3.5)":  perturb(OUT_NOISE, OUT_NOISE.replace("- 2.5 *", "- 3.5 *")),
    "coefs de la verdad +-10%":       perturb(OUT_NOISE, OUT_NOISE.replace("30.0 - 2.5", "31.5 - 2.25")).replace("1.0 * (grade - 5.0) - 0.9", "1.1 * (grade - 5.0) - 0.81"),
    "media corrida +1.5":             perturb(OUT_NOISE, OUT_NOISE.replace("30.0", "31.5")),
    "media corrida -1.5":             perturb(OUT_NOISE, OUT_NOISE.replace("30.0", "28.5")),
}

# la entrega real D59 (forma reducida completa, del fork) como variante extra
D59 = json.loads((ROOT / "scripts/out/fork_0133/cell_b4_d59_neutral.json").read_text(encoding="utf-8"))["submission_code"]
VARIANTS["forma reducida D59 (entrega real R=0.9866)"] = D59


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    print("Calibrando la suite de fidelidad ...", flush=True)
    conf = Conformity(REF)
    conf.set_floors([conf.raw_distances(c, rep_seed=10 + i) for i, c in enumerate(EQUIVALENTS)])

    rows = []
    print(f"\n{'variante':46} {'R (bateria real)':>16} {'fidelidad (x piso)':>18}")
    for name, code in VARIANTS.items():
        server = build_world_server(CASE, seed_offset=31)
        ok = server.submit(code)
        R = server.result.get("R") if ok.accepted else None
        RU = server.result.get("R_unclipped") if ok.accepted else None
        reg = conf.regret(code, rep_seed=4242)
        rows.append({"variante": name, "R": R, "R_uncl": RU,
                     "regret_mean": reg["regret_mean"], "regret_max": reg["regret_max"]})
        print(f"{name:46} {R:16.4f} {reg['regret_mean']:18.2f}", flush=True)

    base = next(r for r in rows if r["variante"].startswith("verdad"))
    # --- gates pre-declarados ---
    fails = []
    for r in rows:
        n = r["variante"]
        if any(k in n for k in ("ruido outcome x1", "ruido outcome x2", "meter", "ruido feedstock")):
            if r["R"] > base["R"] + 1e-6:
                fails.append(f"G1 ROTO: '{n}' con MAS varianza saca MAS R ({r['R']:.4f} > {base['R']:.4f})")
        if r["regret_mean"] > 10 and r["R"] > base["R"] - 0.005:
            fails.append(f"G3 ROTO: '{n}' es conductualmente grande ({r['regret_mean']:.0f}x) y pierde <0.005 de R (R={r['R']:.4f})")
    mono = [("ruido outcome x1.15", "ruido outcome x1.35", "ruido outcome x2"),
            ("meter sumado (1.5)", "meter sumado (3.0)")]
    for chain in mono:
        vals = [next(r["R"] for r in rows if r["variante"] == v) for v in chain]
        if any(vals[i + 1] > vals[i] + 1e-6 for i in range(len(vals) - 1)):
            fails.append(f"G2 ROTO: la cadena {chain} no es monotona: {[round(v,4) for v in vals]}")

    print("\n=== GATES ===")
    if fails:
        for f in fails:
            print("  " + f)
    else:
        print("  todos los gates PASAN (con esta bateria y este barrido)")

    (OUT / "report.json").write_text(json.dumps({"rows": rows, "gate_failures": fails},
                                     indent=2) + "\n", encoding="utf-8")
    print(f"\nwrote {OUT / 'report.json'}")


if __name__ == "__main__":
    main()
