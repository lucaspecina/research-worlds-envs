"""Artefactos de diseño D1 v2.3 (ronda 3 de Codex consolidada). NO es el mundo.

Cambios de la ronda 3 (todos aplicados):
  - K=2: la horquilla DESPLEGADA {vial_fault, lot_mixture}, prior 1/2-1/2 con h0
    incluyendo la evidencia rutinaria gratuita; d_t = reduccion ESPERADA de
    entropia con posteriores actualizados; tau = 0.25 bits. La rutina vale
    d_t = 0 POR CONSTRUCCION (p_V = p_M en el canal rutinario).
    [TRIPWIRE declarable a Lucas: define el reward path del outcome primario]
  - Robots SIN acceso a la verdad: deciden desde sus posteriores sobre datos.
  - Seeds reproducibles (enteros fijos), nada de hash().
  - Potencia A4 valida: test binomial exacto con alfa controlado.
  - Apareo verificado con igualdad EXACTA (==), no allclose.
  - Kill-test correcto: "una sola adquisicion + regla dependiente del resultado
    alcanza rendimiento cercano al oraculo con costo trivial" -> se MIDE y se
    declara en rojo como decision de alcance (claim estrecho aceptado).

Run: .venv/bin/python scripts/design_d1_artifacts.py
"""

from __future__ import annotations

import numpy as np
from math import comb, log2

MU0, BETA, T0 = 92.0, -1.5, 1.0
SQ, SQ2, D, PI = 1.0, 1.3, 3.5, 0.20
SP, SM = 0.4, 0.3
S_EXTRA = float(np.sqrt(SQ2**2 - SQ**2))
STD_VAL = 95.0
TAU = 0.25                     # bits sobre la horquilla desplegada (K=2)
FORK = ("vial_fault", "lot_mixture")


# ------------------------------ generadores ----------------------------------
class Lot:
    __slots__ = ("lot_id", "q_clean", "affected", "fault")

    def __init__(self, i, q, a, f):
        self.lot_id, self.q_clean, self.affected, self.fault = i, q, a, f


def make_lots(n, rng):
    return [Lot(i, rng.normal(0, SQ), rng.random() < PI,
                -D + rng.normal(0, S_EXTRA)) for i in range(n)]


def reading(lot, pole, T, rng, vial_id=0):
    """El shift vale lo MISMO en ambos polos cuando aplica (misma secuencia de
    ops -> byte-exacto); lo que cambia entre polos es DONDE vive (material vs
    vial), visible solo en los canales diagnosticos y en la verdad del proceso."""
    applies = lot.affected and (pole == "A" or vial_id == 0)
    shift = lot.fault if applies else 0.0
    return (MU0 + BETA * (T - T0) + lot.q_clean + rng.normal(0, SP)
            + shift + rng.normal(0, SM))


# --------------------- verosimilitudes de la horquilla ------------------------
def loglik_standard(z_means, n_reps, fork):
    """z: medias por vial de estandar. V: cada vial cae con prob PI; M: nunca."""
    se = np.hypot(SM / np.sqrt(n_reps), 0.0)
    ll = 0.0
    for z in z_means:
        clean = np.exp(-0.5 * ((z - STD_VAL) / se) ** 2) / se
        fault = np.exp(-0.5 * ((z - (STD_VAL - D)) / np.hypot(se, S_EXTRA)) ** 2) / np.hypot(se, S_EXTRA)
        ll += np.log(max((1 - PI) * clean + PI * fault if fork == "vial_fault" else clean, 1e-300))
    return ll


def loglik_lab(z_vals, fork):
    """z: purezas de lab de lotes FLAGGED (elegidos bajos en el stream).
    V: material sano ~N(MU0, SQ) · M: material bajo ~N(MU0-D, SQ2)."""
    ll = 0.0
    for z in z_vals:
        if fork == "vial_fault":
            ll += -0.5 * ((z - MU0) / SQ) ** 2 - np.log(SQ)
        else:
            ll += -0.5 * ((z - (MU0 - D)) / SQ2) ** 2 - np.log(SQ2)
    return ll


def loglik_revial(z_vals, n_reps, fork):
    """z: media de lecturas en vial NUEVO de lotes flagged.
    V: se normaliza ~N(MU0, sqrt(SQ^2+SP^2/reps)) · M: sigue bajo."""
    ll = 0.0
    for z in z_vals:
        if fork == "vial_fault":
            s = np.hypot(SQ, SP / np.sqrt(n_reps))
            ll += -0.5 * ((z - MU0) / s) ** 2 - np.log(s)
        else:
            s = np.hypot(SQ2, SP / np.sqrt(n_reps))
            ll += -0.5 * ((z - (MU0 - D)) / s) ** 2 - np.log(s)
    return ll


def sample_channel(kind, cfg, fork, rng):
    if kind == "standard":
        out = []
        for _ in range(cfg["n_viales"]):
            f = (fork == "vial_fault") and (rng.random() < PI)
            base = STD_VAL + (-D + rng.normal(0, S_EXTRA) if f else 0.0)
            out.append(base + rng.normal(0, SM / np.sqrt(cfg["reps"])))
        return np.asarray(out)
    if kind == "lab":
        if fork == "vial_fault":
            return MU0 + rng.normal(0, SQ, cfg["n_lotes"])
        return MU0 - D + rng.normal(0, SQ2, cfg["n_lotes"])
    if kind == "revial":
        if fork == "vial_fault":
            return MU0 + rng.normal(0, np.hypot(SQ, SP / np.sqrt(cfg["reps"])), cfg["n_lotes"])
        return MU0 - D + rng.normal(0, np.hypot(SQ2, SP / np.sqrt(cfg["reps"])), cfg["n_lotes"])
    if kind == "routine":
        out = []
        for _ in range(cfg["n_lotes"]):
            low = rng.random() < PI
            out.append(MU0 + (rng.normal(-D, SQ2) if low else rng.normal(0, SQ)))
        return np.asarray(out)                 # identica bajo V y M por construccion
    raise ValueError(kind)


def loglik(kind, cfg, z, fork):
    if kind == "standard":
        return loglik_standard(z, cfg["reps"], fork)
    if kind == "lab":
        return loglik_lab(z, fork)
    if kind == "revial":
        return loglik_revial(z, cfg["reps"], fork)
    if kind == "routine":
        return 0.0                              # p_V = p_M exacto
    raise ValueError(kind)


def h2(p):
    p = min(max(p, 1e-12), 1 - 1e-12)
    return -(p * log2(p) + (1 - p) * log2(1 - p))


def expected_info(kind, cfg, w_v, M=4000, seed=777):
    """d_t = H2(w) - E[H2(w')] bajo la mezcla predictiva actual (formula r3)."""
    rng = np.random.default_rng(seed)
    h_now, acc = h2(w_v), 0.0
    for fork, w in (("vial_fault", w_v), ("lot_mixture", 1 - w_v)):
        m = max(1, int(M * w))
        for _ in range(m):
            z = sample_channel(kind, cfg, fork, rng)
            lv, lm = loglik(kind, cfg, z, "vial_fault"), loglik(kind, cfg, z, "lot_mixture")
            pv = w_v * np.exp(lv - max(lv, lm))
            pm = (1 - w_v) * np.exp(lm - max(lv, lm))
            acc += w / m * h2(pv / (pv + pm))
    return max(h_now - acc, 0.0)


# =============================== A1 ===========================================
def artifact_1():
    print("=== A1: apareo exacto (igualdad EXACTA) ===")
    lots = make_lots(60, np.random.default_rng(1234))
    ok = True
    for seed in (7, 8):
        ra, rb = np.random.default_rng(seed), np.random.default_rng(seed)
        A = [reading(l, "A", 1.0, ra) for l in lots]
        B = [reading(l, "B", 1.0, rb) for l in lots]
        ok &= (A == B)
    reps_ok = True
    for l in lots[:20]:
        ra, rb = np.random.default_rng(100 + l.lot_id), np.random.default_rng(100 + l.lot_id)
        reps_ok &= ([reading(l, "A", 1.0, ra) for _ in range(6)]
                    == [reading(l, "B", 1.0, rb) for _ in range(6)])
    print(f"  stream rutinario IDENTICO (==): {ok} | reps mismo vial identicas: {reps_ok}")
    return ok and reps_ok


# =============================== A2 ===========================================
ACCIONES = [
    ("estandar 1 vial x2",   "standard", {"n_viales": 1, "reps": 2},  17),
    ("estandar 1 vial x8",   "standard", {"n_viales": 1, "reps": 8},  23),
    ("estandar 4 viales x2", "standard", {"n_viales": 4, "reps": 2},  23),
    ("estandar 8 viales x2", "standard", {"n_viales": 8, "reps": 2},  31),
    ("lab 2 flagged",        "lab",      {"n_lotes": 2},              110),
    ("lab 4 flagged",        "lab",      {"n_lotes": 4},              160),
    ("re-vial 2 x4",         "revial",   {"n_lotes": 2, "reps": 4},   47),
    ("re-vial 4 x4",         "revial",   {"n_lotes": 4, "reps": 4},   79),
    ("rutina 10",            "routine",  {"n_lotes": 10},             60),
    ("rutina 30",            "routine",  {"n_lotes": 30},             140),
]


def artifact_2():
    print(f"\n=== A2: d_t (bits sobre la horquilla desplegada, K=2) — tau = {TAU} ===")
    vals = {}
    for i, (nombre, kind, cfg, costo) in enumerate(ACCIONES):
        d = expected_info(kind, cfg, 0.5, seed=1000 + i)
        vals[nombre] = d
        print(f"  {nombre:22s} d = {d:5.3f} bits  costo {costo:>3}  "
              f"{'>=tau' if d >= TAU else '<tau '}  ({d/costo*1000:.1f} mbits/$)")
    checks = {
        "rutina_vale_cero": vals["rutina 10"] < 1e-9 and vals["rutina 30"] < 1e-9,
        "estandar_pocas_reps_bajo_tau": vals["estandar 1 vial x2"] < TAU,
        "reps_no_acumulan_como_viales": vals["estandar 1 vial x8"] < vals["estandar 8 viales x2"],
        "hay_2_rutas_sobre_tau": sum(v >= TAU for v in vals.values()) >= 2,
    }
    for k, v in checks.items():
        print(f"  CHECK {k}: {'PASS' if v else 'FAIL'}")
    return all(checks.values()), vals


# =============================== A3 ===========================================
def run_robot(policy, pole, seed):
    """Robots SIN acceso a la verdad: posterior propio sobre la horquilla a
    partir de los DATOS que compran. Entregan mezcla sii w_M > 0.5."""
    rng = np.random.default_rng(seed)
    budget, w_v, D_pre, n_compras = 600.0, 0.5, 0.0, 0

    def buy(kind, cfg, costo):
        nonlocal budget, w_v, D_pre, n_compras
        if budget < costo:
            return False
        budget -= costo
        D_pre += expected_info(kind, cfg, w_v, M=800, seed=seed * 100 + n_compras)
        fork = "lot_mixture" if pole == "A" else "vial_fault"
        z = sample_channel(kind, cfg, fork, rng)
        lv, lm = loglik(kind, cfg, z, "vial_fault"), loglik(kind, cfg, z, "lot_mixture")
        pv = w_v * np.exp(lv - max(lv, lm)); pm = (1 - w_v) * np.exp(lm - max(lv, lm))
        w_v = pv / (pv + pm)
        n_compras += 1
        return True

    if policy == "checklist_condicional":
        buy("standard", {"n_viales": 6, "reps": 2}, 27)
        if w_v < 0.6:                       # el estandar no delato -> investigar proceso
            buy("lab", {"n_lotes": 2}, 110)
    elif policy == "single_action":         # el kill-test correcto de r3
        buy("standard", {"n_viales": 8, "reps": 2}, 31)
    elif policy == "greedy_eig":
        for _ in range(3):
            if max(w_v, 1 - w_v) > 0.95:
                break
            best = max(ACCIONES, key=lambda a: expected_info(a[1], a[2], w_v, M=400,
                                                             seed=seed) / a[3])
            buy(best[1], best[2], best[3])
    elif policy == "ciego":
        idx = list(rng.integers(0, len(ACCIONES), 5))
        for i in idx:
            buy(ACCIONES[i][1], ACCIONES[i][2], ACCIONES[i][3])
    elif policy == "oraculo":
        buy("lab", {"n_lotes": 2}, 110)

    entrega_mezcla = (w_v < 0.5)
    gate = entrega_mezcla if pole == "A" else (not entrega_mezcla)
    return {"Y": int(D_pre >= TAU and gate), "gate": gate, "D": D_pre}


def artifact_3(n_seeds=24):
    print(f"\n=== A3: robots SIN verdad, {n_seeds} seeds — kill-test r3 ===")
    tasas = {}
    for pol in ("checklist_condicional", "single_action", "greedy_eig", "ciego", "oraculo"):
        ya = [run_robot(pol, "A", 40 + k) for k in range(n_seeds)]
        yb = [run_robot(pol, "B", 40 + k) for k in range(n_seeds)]
        tasas[pol] = {"A_Y": np.mean([r["Y"] for r in ya]),
                      "B_Y": np.mean([r["Y"] for r in yb]),
                      "A_gate": np.mean([r["gate"] for r in ya]),
                      "B_gate": np.mean([r["gate"] for r in yb])}
        t = tasas[pol]
        print(f"  {pol:22s} Y: A={t['A_Y']:.0%} B={t['B_Y']:.0%} | "
              f"acierto de horquilla: A={t['A_gate']:.0%} B={t['B_gate']:.0%}")
    single = tasas["single_action"]; orac = tasas["oraculo"]
    near = (min(single["A_gate"], single["B_gate"])
            >= min(orac["A_gate"], orac["B_gate"]) - 0.10)
    print(f"  KILL-TEST r3 (una adquisicion ~ oraculo, costo trivial): {near}")
    print("  -> Si TRUE: se DECLARA EN ROJO como decision de alcance (claim estrecho:")
    print("     'ejecucion espontanea del chequeo de calibracion'), no se esconde.")
    return tasas, near


# =============================== A4 ===========================================
def artifact_4():
    print("\n=== A4: potencia valida (binomial exacto, alfa controlado) ===")

    def exact_test_power(p0, p1, n, alpha=0.05):
        # region critica de dos colas por probabilidad exacta bajo p0
        probs0 = [comb(n, k) * p0**k * (1 - p0)**(n - k) for k in range(n + 1)]
        order = np.argsort(probs0)
        region, a = [], 0.0
        for k in order:
            if a + probs0[k] <= alpha:
                region.append(k); a += probs0[k]
        return sum(comb(n, k) * p1**k * (1 - p1)**(n - k) for k in region), a

    for n in (10, 12, 15, 18):
        pw, a = exact_test_power(0.25, 0.70, n)
        pw2, a2 = exact_test_power(0.25, 0.60, n)
        print(f"  n={n}/polo (H0 p=0.25): alfa real {a:.3f} | "
              f"potencia vs p=0.70: {pw:.0%} | vs p=0.60: {pw2:.0%}")
    return True


if __name__ == "__main__":
    ok1 = artifact_1()
    ok2, tabla = artifact_2()
    tasas, kill = artifact_3()
    artifact_4()
    print(f"\nRESUMEN v2.3: apareo={'OK' if ok1 else 'FALLA'} · "
          f"diagnosticidad={'OK' if ok2 else 'FALLA'} · "
          f"dominancia-de-accion-unica={'SI (declarar en rojo)' if kill else 'no'}")
