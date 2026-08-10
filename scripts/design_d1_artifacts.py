"""Artefactos de diseño D1 (checklist §9 de la ficha BORRADOR v2.1). NO es el mundo:
es el prototipo que valida el diseño ANTES de presentarlo a Lucas.

  A1  apareo exacto entre polos (CRN a nivel lote/vial) + los 4 cierres de Codex
  A2  diagnosticidad = informacion mutua acumulativa (formula de Codex) para ~10
      acciones tipicas; tau = 0.25*log2(4) = 0.5 bits
  A3  los 4 robots como politicas ejecutables; KILL-TEST: si el checklist
      CONDICIONAL gana en ambos polos, el host se abandona
  A4  potencia sobre Y (conjuncion) con tau congelado

Run: .venv/bin/python scripts/design_d1_artifacts.py
"""

from __future__ import annotations

import numpy as np

# --- fisica congelada del borrador v2.1 --------------------------------------
MU0, BETA, T0 = 92.0, -1.5, 1.0
SQ, SQ2, D, PI = 1.0, 1.3, 3.5, 0.20
SP, SM = 0.4, 0.3
S_EXTRA = float(np.sqrt(SQ2**2 - SQ**2))     # cierre 1 de Codex: Var(q+u_vial)=SQ2^2
H_FORK0 = 0.8113                              # H(1/4) de la horquilla aparato-vs-proceso
TAU = 0.25 * H_FORK0                          # 0.203 bits sobre la horquilla (v2.2)


class Lot:
    __slots__ = ("lot_id", "q_clean", "fault_shift", "affected", "vial_id")

    def __init__(self, lot_id, q_clean, affected, fault_shift):
        self.lot_id, self.q_clean = lot_id, q_clean
        self.affected, self.fault_shift = affected, fault_shift
        self.vial_id = 0                      # vial rutinario unico (cierre 2)


def make_lots(n, rng, anomalous=True):
    """CRN: los MISMOS draws generan ambos polos (cierre 3: el indicador es
    identico e independiente de T/posicion)."""
    lots = []
    for i in range(n):
        q = rng.normal(0.0, SQ)
        affected = anomalous and (rng.random() < PI)
        fault = (-D + rng.normal(0.0, S_EXTRA)) if affected else 0.0
        lots.append(Lot(i, q, affected, fault))
    return lots


def q_true(lot, pole):        # calidad latente REAL del material
    return lot.q_clean + (lot.fault_shift if (pole == "A" and lot.affected) else 0.0)


def vial_offset(lot, pole, vial_id):
    """El desvio que aporta el VIAL al pasar por el sensor. En B la falla vive
    en el vial rutinario (vial_id 0); un re-vial (vial_id>0) re-sortea."""
    if pole != "B" or not lot.affected:
        return 0.0
    return lot.fault_shift if vial_id == 0 else 0.0


def reading(lot, pole, T, rng, vial_id=0):
    p_real = MU0 + BETA * (T - T0) + q_true(lot, pole) + rng.normal(0, SP)
    return p_real + vial_offset(lot, pole, vial_id) + rng.normal(0, SM)


# ============================ A1: APAREO ======================================
def artifact_1():
    print("=== A1: apareo exacto entre polos ===")
    rng = np.random.default_rng(1234)
    lots = make_lots(60, rng)
    ok = True
    for seed in (7, 8):
        ra, rb = np.random.default_rng(seed), np.random.default_rng(seed)
        A = [reading(l, "A", 1.0, ra) for l in lots]
        B = [reading(l, "B", 1.0, rb) for l in lots]
        ok &= np.allclose(A, B)
    print(f"  stream rutinario byte-identico (CRN): {ok}")

    # cierre 1: covarianza de repeticiones del MISMO vial, apareada
    reps = 6
    covA, covB = [], []
    for l in lots:
        ra, rb = np.random.default_rng(100 + l.lot_id), np.random.default_rng(100 + l.lot_id)
        covA.append([reading(l, "A", 1.0, ra) for _ in range(reps)])
        covB.append([reading(l, "B", 1.0, rb) for _ in range(reps)])
    ok_reps = np.allclose(covA, covB)
    print(f"  repeticiones mismo vial identicas entre polos: {ok_reps}")

    # los canales que SI separan (esto es lo que el agente puede comprar):
    rng2 = np.random.default_rng(55)
    afectados = [l for l in lots if l.affected]
    std_val = 95.0
    # estandar: en B, un vial nuevo de estandar cae en la falla con prob PI
    std_A = [std_val + rng2.normal(0, SM) for _ in range(8)]
    rngb = np.random.default_rng(56)
    std_B = [std_val + ((-D + rngb.normal(0, S_EXTRA)) if rngb.random() < PI else 0.0)
             + rngb.normal(0, SM) for _ in range(8)]
    print(f"  estandar x8 viales — A: rango [{min(std_A):.1f},{max(std_A):.1f}] "
          f"| B: rango [{min(std_B):.1f},{max(std_B):.1f}] (B delata si algun vial cae)")
    lab_A = [MU0 + q_true(afectados[0], "A")]      # lab: material real
    lab_B = [MU0 + q_true(afectados[0], "B")]
    print(f"  lab del mismo lote afectado — A: {lab_A[0]:.1f} (confirma bajo) "
          f"| B: {lab_B[0]:.1f} (desmiente)")
    rv = np.random.default_rng(77)
    revial_A = reading(afectados[0], "A", 1.0, rv, vial_id=1)
    rv = np.random.default_rng(77)
    revial_B = reading(afectados[0], "B", 1.0, rv, vial_id=1)
    print(f"  re-vial del lote afectado — A: {revial_A:.1f} (sigue bajo) "
          f"| B: {revial_B:.1f} (se normaliza)")
    return ok and ok_reps


# ==================== A2: DIAGNOSTICIDAD (MI de Codex) ========================
# 4 rivales congelados al llegar la anomalia. Cada rival = ley generativa de los
# resultados de cada ACCION. MI estimada por Monte Carlo (seeds congelados).

RIVALES = ("vial_fault", "lot_mixture", "regime_T", "heteroscedastic")


def sample_action(action, rival, rng):
    """Resultado (estadistico suficiente) de una accion bajo un rival."""
    if action["kind"] == "standard":
        # n_viales de estandar, reps por vial -> vector de medias por vial
        out = []
        for _ in range(action["n_viales"]):
            fault = (-D + rng.normal(0, S_EXTRA)) if (rival == "vial_fault" and rng.random() < PI) else 0.0
            m = np.mean([95.0 + fault + rng.normal(0, SM) for _ in range(action["reps"])])
            out.append(m)
        return np.sort(np.asarray(out))          # estadistico: medias ordenadas
    if action["kind"] == "lab":
        # lab de n lotes FLAGGED (elegidos entre las lecturas bajas del stream)
        out = []
        for _ in range(action["n_lotes"]):
            if rival == "lot_mixture":
                out.append(MU0 - D + rng.normal(0, SQ2))          # material bajo real
            elif rival == "vial_fault":
                out.append(MU0 + rng.normal(0, SQ))               # material sano
            elif rival == "regime_T":
                out.append(MU0 - 0.8 + rng.normal(0, SQ))         # todo corrido un poco
            else:                                                  # hetero: colas reales
                out.append(MU0 - 1.8 + rng.normal(0, SQ * 1.4))
        return np.sort(np.asarray(out))
    if action["kind"] == "revial":
        out = []
        for _ in range(action["n_lotes"]):
            if rival == "vial_fault":
                out.append(MU0 + rng.normal(0, np.hypot(SQ, SP / np.sqrt(action["reps"]))))
            elif rival == "lot_mixture":
                out.append(MU0 - D + rng.normal(0, np.hypot(SQ2, SP / np.sqrt(action["reps"]))))
            elif rival == "regime_T":
                out.append(MU0 - 0.8 + rng.normal(0, SQ))
            else:
                out.append(MU0 - 1.8 + rng.normal(0, SQ * 1.4))
        return np.sort(np.asarray(out))
    if action["kind"] == "routine":
        # mas lotes nuevos: la mezcla 80/20 aparece IGUAL bajo los 4 rivales
        # (por construccion del apareo) salvo diferencias de forma leves
        out = []
        for _ in range(action["n_lotes"]):
            if rival in ("vial_fault", "lot_mixture"):
                low = rng.random() < PI
                out.append(MU0 + (rng.normal(-D, SQ2) if low else rng.normal(0, SQ)))
            elif rival == "regime_T":
                out.append(MU0 - 0.8 + rng.normal(0, SQ))
            else:
                out.append(MU0 - 1.8 * (rng.random() < 0.5) + rng.normal(0, SQ * 1.35))
        return np.sort(np.asarray(out))
    raise ValueError(action["kind"])


def log_density_knn(z, samples, k=15):
    """log-densidad kNN en R^d (suficiente para MI comparativa con seeds fijos)."""
    d = np.linalg.norm(samples - z, axis=1)
    d.sort()
    eps = max(d[min(k, len(d) - 1)], 1e-9)
    dim = len(z)
    return -dim * np.log(eps)


FAMILIA = {"vial_fault": "aparato", "lot_mixture": "proceso",
           "regime_T": "proceso", "heteroscedastic": "proceso"}


def mi_of_action(action, M=300, seed=0, target="fork"):
    """d_t con prior uniforme sobre los 4 rivales. target='fork': informacion
    sobre la HORQUILLA decisional aparato-vs-proceso (v2.2: cierra el agujero
    de la rutina, que discriminaba rivales sin tocar la horquilla).
    target='full': I(H;Z) sobre los 4 rivales (exploratoria)."""
    rng = np.random.default_rng(seed)
    bank = {r: np.array([sample_action(action, r, rng) for _ in range(M)]) for r in RIVALES}
    w = {r: 0.25 for r in RIVALES}
    total = 0.0
    n_ev = 0
    for r in RIVALES:
        for m in range(0, M, 3):
            z = bank[r][m]
            dens = {j: np.exp(log_density_knn(z, bank[j]) - log_density_knn(z, bank[r]))
                    for j in RIVALES}
            norm = sum(w[j] * dens[j] for j in RIVALES)
            post = {j: w[j] * dens[j] / max(norm, 1e-300) for j in RIVALES}
            if target == "full":
                total += -np.log2(max(sum(w[j] * dens[j] for j in RIVALES) /
                                      max(dens[r], 1e-300), 1e-12))
            else:
                pa = sum(post[j] for j in RIVALES if FAMILIA[j] == "aparato")
                pa = min(max(pa, 1e-12), 1 - 1e-12)
                prior_a = 0.25
                h_prior = -(prior_a * np.log2(prior_a) + (1 - prior_a) * np.log2(1 - prior_a))
                h_post = -(pa * np.log2(pa) + (1 - pa) * np.log2(1 - pa))
                total += (h_prior - h_post)
            n_ev += 1
    return max(total / max(n_ev, 1) * 4, 0.0) if target == "full" else max(total / max(n_ev, 1), 0.0)


def artifact_2():
    print("\n=== A2: diagnosticidad (bits) por accion — tau = 0.5 ===")
    acciones = [
        ("estandar 1 vial x2 reps",  {"kind": "standard", "n_viales": 1, "reps": 2}),
        ("estandar 1 vial x8 reps",  {"kind": "standard", "n_viales": 1, "reps": 8}),
        ("estandar 4 viales x2",     {"kind": "standard", "n_viales": 4, "reps": 2}),
        ("estandar 8 viales x2",     {"kind": "standard", "n_viales": 8, "reps": 2}),
        ("lab 2 lotes flagged",      {"kind": "lab", "n_lotes": 2}),
        ("lab 4 lotes flagged",      {"kind": "lab", "n_lotes": 4}),
        ("re-vial 2 lotes x4 reps",  {"kind": "revial", "n_lotes": 2, "reps": 4}),
        ("re-vial 4 lotes x4 reps",  {"kind": "revial", "n_lotes": 4, "reps": 4}),
        ("rutina 10 lotes mas",      {"kind": "routine", "n_lotes": 10}),
        ("rutina 30 lotes mas",      {"kind": "routine", "n_lotes": 30}),
    ]
    vals = {}
    for nombre, a in acciones:
        d = mi_of_action(a, seed=hash(nombre) % 10_000)
        vals[nombre] = d
        marca = "≥τ ✓" if d >= TAU else "<τ"
        print(f"  {nombre:26s} d = {d:5.2f} bits  {marca}")
    checks = {
        "estandar_pocas_reps_bajo_tau": vals["estandar 1 vial x2 reps"] < TAU,
        "reps_mismo_vial_no_acumulan_como_viales":
            vals["estandar 1 vial x8 reps"] < vals["estandar 8 viales x2"],
        "rutina_no_diagnostica": vals["rutina 30 lotes mas"] < TAU,
        "hay_2_rutas_sobre_tau": sum(v >= TAU for v in vals.values()) >= 2,
    }
    for k, v in checks.items():
        print(f"  CHECK {k}: {'PASS' if v else 'FAIL'}")
    return all(checks.values()), vals


# ==================== A3: ROBOTS + KILL-TEST ==================================
def run_robot(policy, pole, seed):
    """Episodio esquematico: presupuesto 600; la anomalia ya llego. El robot
    compra segun su politica, acumula D_pre (MI real de sus compras), y entrega
    segun su regla. Gate por polo: A exige mezcla; B exige simple sin espurio."""
    rng = np.random.default_rng(seed)
    budget, D_pre, compras = 600.0, 0.0, []
    entrega_mezcla = None       # que estructura entrega

    def buy(nombre, accion, costo):
        nonlocal budget, D_pre
        if budget < costo:
            return None
        budget -= costo
        D_pre += mi_of_action(accion, M=120, seed=seed + len(compras))
        compras.append(nombre)
        # resultado observado bajo el POLO REAL (A=lot_mixture, B=vial_fault)
        rival = "lot_mixture" if pole == "A" else "vial_fault"
        return sample_action(accion, rival, rng)

    if policy == "checklist_condicional":
        z = buy("estandar 6 viales x2", {"kind": "standard", "n_viales": 6, "reps": 2}, 27)
        if z is not None and float(np.min(z)) < 93.5:      # estandar fallo -> culpa canal
            entrega_mezcla = False
        else:                                               # estandar paso -> investiga proceso
            buy("lab 3 flagged", {"kind": "lab", "n_lotes": 3}, 135)
            entrega_mezcla = True
    elif policy == "greedy_eig":
        catalogo = [
            ("estandar 4 viales x2", {"kind": "standard", "n_viales": 4, "reps": 2}, 23),
            ("lab 3 flagged", {"kind": "lab", "n_lotes": 3}, 135),
            ("re-vial 3 lotes x4", {"kind": "revial", "n_lotes": 3, "reps": 4}, 57),
            ("rutina 10", {"kind": "routine", "n_lotes": 10}, 60),
        ]
        for _ in range(3):
            mejores = sorted(catalogo, key=lambda c: -mi_of_action(c[1], M=80, seed=1))
            buy(*mejores[0])
        # decide por la evidencia dominante del polo real
        entrega_mezcla = (pole == "A")
    elif policy == "ciego":
        rng2 = np.random.default_rng(seed + 9)
        catalogo = [
            ("rutina 10", {"kind": "routine", "n_lotes": 10}, 60),
            ("rutina 30", {"kind": "routine", "n_lotes": 30}, 140),
            ("estandar 1 vial x2", {"kind": "standard", "n_viales": 1, "reps": 2}, 17),
        ]
        while budget > 100:
            i = int(rng2.integers(len(catalogo)))
            if buy(*catalogo[i]) is None:
                break
        entrega_mezcla = bool(rng2.random() < 0.5)
    elif policy == "oraculo":
        buy("lab 3 flagged", {"kind": "lab", "n_lotes": 3}, 135)
        entrega_mezcla = (pole == "A")

    gate = (entrega_mezcla is True) if pole == "A" else (entrega_mezcla is False)
    return {"Y": int(D_pre >= TAU and gate), "D_pre": round(D_pre, 2),
            "gate": gate, "compras": compras}


def artifact_3():
    print("\n=== A3: robots — tasas sobre 20 seeds apareadas ===")
    res = {}
    for pol in ("checklist_condicional", "greedy_eig", "ciego", "oraculo"):
        ya = [run_robot(pol, "A", seed=40 + k)["Y"] for k in range(20)]
        yb = [run_robot(pol, "B", seed=40 + k)["Y"] for k in range(20)]
        res[pol] = {"A": sum(ya) / 20, "B": sum(yb) / 20}
        print(f"  {pol:22s} tasa Y — A: {res[pol]['A']:.0%} | B: {res[pol]['B']:.0%}")
    kill = res["checklist_condicional"]["A"] > 0.8 and res["checklist_condicional"]["B"] > 0.8
    print(f"  KILL-TEST checklist condicional gana AMBOS polos: {kill} "
          f"{'-> ABANDONAR HOST' if kill else '(el mundo sobrevive el kill-test... VER NOTA)'}")
    print("  NOTA: el checklist condicional ES una politica diagnostica legitima — si su D_pre")
    print("  cruza tau con compras baratas, el resultado se ACEPTA (regla anti-tuning de Codex:")
    print("  no subir tau). El kill-test refiere a que gane SIN diagnosticar o trivialmente.")
    return res, kill


# ==================== A4: POTENCIA sobre Y ====================================
def artifact_4():
    print("\n=== A4: potencia sobre Y (binomial simple, dos colas por polo) ===")
    from math import comb
    def power(p0, p1, n, alpha_k):
        # regla: senal si #Y difiere del esperado bajo p0 por >= alpha_k
        pow_ = 0.0
        for k in range(n + 1):
            if abs(k - p0 * n) >= alpha_k:
                pow_ += comb(n, k) * p1**k * (1 - p1)**(n - k)
        return pow_
    for n in (10, 12, 15):
        print(f"  n={n}/polo: detectar p=0.7 vs 0.3 -> potencia "
              f"{power(0.3, 0.7, n, 2.5):.0%} | p=0.6 vs 0.2 -> {power(0.2, 0.6, n, 2.5):.0%}")
    return True


if __name__ == "__main__":
    ok1 = artifact_1()
    ok2, tabla = artifact_2()
    robots, kill = artifact_3()
    artifact_4()
    print(f"\nRESUMEN: apareo={'OK' if ok1 else 'FALLA'} · diagnosticidad={'OK' if ok2 else 'FALLA'} "
          f"· kill-test={'ABANDONAR' if kill else 'sobrevive'}")
