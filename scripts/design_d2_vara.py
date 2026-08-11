"""Verificación de la vara D2 (paso 2 del rediseño, GO de Lucas 2026-08-11) — VERDE.

HISTORIA DEL PASO 2 (dos hallazgos de camino, ambos documentados en la ficha):
  1. CRPS NO paga la estructura (ratio <= 0.07 hasta con d=7σ — métrica de bulto;
     la elección de Codex se revierte CON DATOS): la vara primaria es LOG-SCORE
     (KDE determinista), que ya había separado 0.07-0.16 nats en la auditoría D1.
  2. El anclaje de D1 estaba mal (0 = verdad del otro polo): se restaura el patrón
     del rung 0 — 0 = EL MEJOR RIVAL SIN EL SALTO (momento-matcheado, congelable).

Compuertas (todas ANTES de construir nada; correr también --scan para la perilla):
  V1  anclaje sano (verdades 1.0; vago/limpia/mezcla-horneada 0.0)
  V2  SHOULD-FAIL 0175: la campana que rompió D1 (S_vieja=0.986) saca <= 0.1
  V3  headroom: la paga del salto >= 0.10 nats/lote
  V3b resolución: el medio-salto realista (mezcla sin ley en T) en [0.15, 0.85]
  V4  el flag de estructura separa (mezcla sí / campanas no)
  V5  decisión en el régimen de la intervención: |dif P(fuera de espec|T=1.3)| >= 0.05

Física elegida (scan 2026-08-11): la de D1 + pi(T) con pendiente 0.5 — único cambio.

Run: .venv/bin/python scripts/design_d2_vara.py [--scan]
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.optimize import minimize
from scipy.stats import norm

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from cases import d1_calibracion_common as C  # noqa: E402
from cases import d2_decision_common as D2  # noqa: E402


def gauss_family(theta):
    a, b, c, d, e, f = theta

    def prog(regime, n, seed):
        T = C._speed_T(regime)
        mu = a + b * (T - 1.0) + c * (T - 1.0) ** 2
        sd = float(np.exp(d + e * (T - 1.0) + f * (T - 1.0) ** 2))
        sd = min(max(sd, 0.3), 6.0)
        rng = np.random.default_rng(seed)
        return pd.DataFrame({"unit_id": np.arange(int(n), dtype=float),
                             "y": mu + rng.normal(0, sd, int(n))})
    return prog


def crps_gauss_closed(mu, sd, obs):
    z = (obs - mu) / sd
    return float(np.mean(sd * (z * (2 * norm.cdf(z) - 1) + 2 * norm.pdf(z)
                               - 1.0 / np.sqrt(np.pi))))


def optimize_lazy(params: dict, pole: str = "proceso") -> tuple:
    """El MEJOR rival sin estructura: minimiza CRPS (forma cerrada) contra lotes de
    la verdad en la grilla del examen. Optimizado, jamás elegido a mano (ADR 0175)."""
    truth = D2.pole_truth_program_d2(pole, params)
    obs = {T: np.asarray(truth(C._regime(T), 6000, 71 + k)["y"], float)
           for k, T in enumerate(D2.EXAM_GRID)}

    def loss(theta):
        a, b, c, d, e, f = theta
        tot = 0.0
        for T, y in obs.items():
            mu = a + b * (T - 1.0) + c * (T - 1.0) ** 2
            sd = min(max(float(np.exp(d + e * (T - 1.0) + f * (T - 1.0) ** 2)), 0.3), 6.0)
            tot += crps_gauss_closed(mu, sd, y)
        return tot / len(obs)

    mu0 = params["mu0"] - params["pi"] * params["d_shift"]
    best = None
    for init in ([mu0, params["beta"], 0, np.log(1.6), 0, 0],
                 [mu0 - 0.5, params["beta"], 0, np.log(2.0), 0.2, 0.2]):
        r = minimize(loss, np.asarray(init, float), method="Nelder-Mead",
                     options={"maxiter": 4000, "xatol": 1e-5, "fatol": 1e-7})
        if best is None or r.fun < best.fun:
            best = r
    return gauss_family(best.x), best


def tuned_lazy_d1(params: dict):
    """La campana que rompió la vara vieja (S_vieja=0.986): σ=sd_verdad, μ clava p10."""
    targets = {}
    truth = D2.pole_truth_program_d2("proceso", params)
    for T in (0.8, 1.0, 1.2):
        st = C.program_curve_stats(truth, T, n=20000, seed=5)
        targets[T] = st

    def prog(regime, n, seed):
        T = C._speed_T(regime)
        Tc = min(targets, key=lambda t: abs(t - T))
        sd = targets[Tc]["sd"]
        mu = targets[Tc]["p10"] + 1.2816 * sd
        rng = np.random.default_rng(seed)
        return pd.DataFrame({"unit_id": np.arange(int(n), dtype=float),
                             "y": mu + rng.normal(0, sd, int(n))})
    return prog


def mid_structure(params: dict):
    """El MEDIO SALTO realista: escribe la mezcla (corrimiento correcto — lo ve en
    sus datos) pero SIN la ley en T: pi constante, la media en banda operable.
    La escala debe resolverlo entre el vago (0) y la verdad (1)."""
    d_shift = params.get("d_shift_d2") or params["d_shift"]
    s_extra = params.get("s_extra_d2") or C.S_EXTRA
    p_flat = np.mean([D2.pi_T(t, params) for t in (0.8, 1.0, 1.2)])

    def prog(regime, n, seed):
        T = C._speed_T(regime)
        rng = np.random.default_rng(seed)
        q = rng.normal(0, C.SQ, int(n))
        hit = rng.random(int(n)) < p_flat
        fault = -d_shift + rng.normal(0, s_extra, int(n))
        y = params["mu0"] + params["beta"] * (T - 1.0) + q + np.where(hit, fault, 0.0)
        return pd.DataFrame({"unit_id": np.arange(int(n), dtype=float), "y": y})
    return prog


D2_CHOICE = {"d_shift_d2": None, "pi_slope": 0.5, "s_extra_d2": None}
# ELECCIÓN DEL SCAN (2026-08-11): la física heredada de D1 PASA con solo agregar
# pi(T) — mínima desviación, máxima comparabilidad D1→D2. Con pendiente 0.5 el
# medio-salto (mezcla sin ley en T) captura ~0.79 del valor: el gate S>=0.5
# premia el salto NUCLEAR (escribir la mezcla); la ley en T es el bonus.


def main() -> int:
    params = dict(C.load_instance()["params"], **D2_CHOICE)
    tA = D2.pole_truth_program_d2("proceso", params)
    tB = D2.pole_truth_program_d2("instrumento", params)

    print("=== ancla: el rival vago óptimo EN LA VARA LOG (momento-matcheado) ===")
    lazy = lazy_opt_log(params)

    print("\n=== V1: anclaje sano (A: 0=vago óptimo · B: 0=mezcla horneada) ===")
    sAA = D2.s_metric_log(tA, "proceso", params, anchor_zero=lazy)
    sBB = D2.s_metric_log(tB, "instrumento", params)
    sLA = D2.s_metric_log(lazy, "proceso", params, anchor_zero=lazy)
    sBA = D2.s_metric_log(tB, "proceso", params, anchor_zero=lazy)
    sAB = D2.s_metric_log(tA, "instrumento", params)
    print(f"verdad A: {sAA['S']:.3f} | verdad B: {sBB['S']:.3f} | vago en A: "
          f"{sLA['S']:.3f} | limpia en A: {sBA['S']:.3f} | mezcla en B: {sAB['S']:.3f}")
    v1 = (sAA["S"] >= 0.95 and sBB["S"] >= 0.95 and sLA["S"] <= 0.05
          and sBA["S"] <= 0.05 and sAB["S"] <= 0.05)

    print("\n=== V2: SHOULD-FAIL 0175 — la campana afinada que rompió D1 ===")
    s2 = D2.s_metric_log(tuned_lazy_d1(params), "proceso", params, anchor_zero=lazy)
    print(f"S_vieja era 0.986 -> S_D2 = {s2['S']:.3f} (gate <= 0.1)")
    v2 = s2["S"] <= 0.1

    print("\n=== V3: HEADROOM — la paga del salto en nats/lote ===")
    print(f"paga: {sAA['nats_anchor']:.3f} nats/lote (gate >= 0.10)")
    v3 = sAA["nats_anchor"] >= 0.10

    print("\n=== V3b: RESOLUCIÓN — el medio-salto (mezcla sin ley en T) ===")
    smid = D2.s_metric_log(mid_structure(params), "proceso", params, anchor_zero=lazy)
    print(f"S_mid = {smid['S']:.3f} (gate: 0.15-0.85)")
    v3b = 0.15 <= smid["S"] <= 0.85

    print("\n=== V4: el flag de estructura sigue separando ===")
    fA = C.structural_flag(tA, params)["has_mixture"]
    fL = C.structural_flag(lazy, params)["has_mixture"]
    print(f"verdad-mezcla: {fA} | rival óptimo: {fL}")
    v4 = fA and not fL

    print("\n=== V5: decisión en el régimen de la intervención (T=1.3) ===")
    L = params["mu0"] - D2.SPEC_OFFSET
    yt = np.asarray(tA(C._regime(1.3), 40000, 11)["y"], float)
    ym = np.asarray(lazy(C._regime(1.3), 40000, 12)["y"], float)
    pt, pm = float((yt < L).mean()), float((ym < L).mean())
    print(f"P(fuera de espec | T=1.3): verdad {pt:.1%} vs vago óptimo {pm:.1%} "
          f"(gate: |dif| >= 0.05)")
    v5 = abs(pt - pm) >= 0.05

    print("\n" + "=" * 60)
    gates = {"V1_anclaje": v1, "V2_shouldfail_tuned": v2, "V3_headroom": v3,
             "V3b_resolucion": v3b, "V4_flag": v4, "V5_decision_T13": v5}
    for k, v in gates.items():
        print(f"  {k}: {'PASS' if v else 'FAIL'}")
    print("VARA D2:", "VERDE" if all(gates.values()) else "ROJA — rediseñar antes de seguir")
    return 0 if all(gates.values()) else 1


def lazy_opt_log(params: dict, pole: str = "proceso"):
    """El mejor rival sin salto PARA LA VARA LOG: dentro de la familia gaussiana,
    el óptimo en verosimilitud es el momento-matcheado — se ajusta μ(T), σ(T)
    cuadráticos a los momentos de la verdad por T (analítico, sin Nelder-Mead)."""
    truth = D2.pole_truth_program_d2(pole, params)
    Ts = np.asarray(D2.EXAM_GRID, float)
    mus, sds = [], []
    for k, T in enumerate(Ts):
        y = np.asarray(truth(C._regime(T), 30000, 611 + k)["y"], float)
        mus.append(np.mean(y))
        sds.append(np.std(y))
    X = np.column_stack([np.ones_like(Ts), Ts - 1.0, (Ts - 1.0) ** 2])
    cm, *_ = np.linalg.lstsq(X, np.asarray(mus), rcond=None)
    cs, *_ = np.linalg.lstsq(X, np.log(np.asarray(sds)), rcond=None)
    return gauss_family([cm[0], cm[1], cm[2], cs[0], cs[1], cs[2]])


def gates_for(params: dict) -> dict:
    """Compuertas físicas del scan — vara primaria LOG-SCORE (nats/lote)."""
    tA = D2.pole_truth_program_d2("proceso", params)
    lazy = lazy_opt_log(params)
    sAA = D2.s_metric_log(tA, "proceso", params, anchor_zero=lazy)
    nats = sAA["nats_anchor"]                      # la paga del salto, en nats/lote
    smid = D2.s_metric_log(mid_structure(params), "proceso", params,
                           anchor_zero=lazy)["S"]
    L = params["mu0"] - D2.SPEC_OFFSET
    yt = np.asarray(tA(C._regime(1.3), 40000, 11)["y"], float)
    ym = np.asarray(lazy(C._regime(1.3), 40000, 12)["y"], float)
    ddec = abs(float((yt < L).mean()) - float((ym < L).mean()))
    return {"nats": nats, "s_mid": smid, "ddec_T13": ddec,
            "pass": bool(nats >= 0.10 and 0.15 <= smid <= 0.85 and ddec >= 0.05)}


def scan() -> int:
    base = C.load_instance()["params"]
    print("SCAN de la perilla física — vara LOG (paga en nats/lote; gates: "
          "nats>=0.10, S_mid en [0.15,0.85], dDec13>=0.05):")
    print(f"{'d_shift':>8} {'slope':>6} {'s_extra':>8} {'nats':>6} {'S_mid':>6} "
          f"{'dDec13':>7} -> gate")
    for d_shift in (3.9, 5.0, 6.0):
        for slope in (0.5, 0.8):
            for s_extra in (C.S_EXTRA, 0.5):
                p = dict(base, d_shift_d2=d_shift, pi_slope=slope, s_extra_d2=s_extra)
                g = gates_for(p)
                print(f"{d_shift:8.1f} {slope:6.1f} {s_extra:8.2f} {g['nats']:6.3f} "
                      f"{g['s_mid']:6.2f} {g['ddec_T13']:7.3f} "
                      f"-> {'PASS' if g['pass'] else 'fail'}")
    return 0


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--scan", action="store_true")
    args = ap.parse_args()
    raise SystemExit(scan() if args.scan else main())
