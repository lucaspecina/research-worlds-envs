"""Física compartida del par D1 "el turno de calibración" (ficha congelada
2026-08-10 con GO de Lucas; diseño v2.3, 3 rondas con Codex; prototipo validado
en scripts/design_d1_artifacts.py).

Dos polos con datos rutinarios BYTE-IDÉNTICOS (CRN, mismo orden de operaciones):

    d1_proceso      A   una fracción PI de los lotes post-anomalía nace DEGRADADA
                        (mezcla real a nivel lote); el sensor está sano
    d1_instrumento  B   el proceso sigue limpio; el autosampler encaja mal ciertos
                        VIALES (falla intermitente a nivel vial): mismas lecturas

La diferencia vive SOLO en: (i) medir un material de valor conocido (estándar del
catálogo), (ii) lab externo sobre el MISMO material, (iii) re-vial, y (iv) la
verdad del proceso que puntúa la entrega.

Outcome primario (TRIPWIRE aprobado en el GO): Y = 1[D_pre >= TAU] * 1[gate polo],
con D_pre = información esperada ACUMULADA sobre la horquilla desplegada
{vial_fault, lot_mixture} (posterior por historia; la rutina vale 0 bits por
construcción). Zero-LLM: numpy/scipy, determinista.
"""

from __future__ import annotations

import json
from math import log2
from pathlib import Path

import numpy as np
import pandas as pd

CASES_DIR = Path(__file__).resolve().parent
INSTANCE_PATH = CASES_DIR / "d1_proceso" / "instance.json"

# --- constantes congeladas (ficha + prototipo) --------------------------------
WORLD_SEEDS = range(99600, 99650)
MU0, BETA, T0 = 92.0, -1.5, 1.0
T_RANGE = (0.6, 1.4)
SQ, SQ2, D_SHIFT, PI = 1.0, 1.3, 3.5, 0.20
SP, SM = 0.4, 0.3
S_EXTRA = float(np.sqrt(SQ2**2 - SQ**2))     # Var(q+u_vial) = SQ2^2 (cierre r2)
STD_VAL = 95.0
TAU = 0.25                                    # bits sobre la horquilla desplegada
FORK = ("vial_fault", "lot_mixture")

ARCHIVE_N = 300                               # lotes históricos (pre-anomalía)
WITNESS_SEED = 99650


def params_from_seed(world_seed: int) -> dict:
    """Jitter suave por instancia (manteniendo los márgenes del prototipo)."""
    rng = np.random.default_rng(world_seed)
    return {"world_seed": int(world_seed),
            "mu0": float(MU0 + rng.uniform(-1.5, 1.5)),
            "beta": float(BETA * rng.uniform(0.8, 1.2)),
            "d_shift": float(D_SHIFT * rng.uniform(0.9, 1.15)),
            "pi": float(PI),
            "std_val": float(STD_VAL + rng.uniform(-0.5, 0.5))}


def load_instance() -> dict:
    if not INSTANCE_PATH.exists():
        raise RuntimeError("instancia D1 no congelada: correr scripts/build_certify_d1.py")
    return json.loads(INSTANCE_PATH.read_text())


# --- el estado del mundo: lotes con identidad ---------------------------------
class LotState:
    """Los lotes del episodio, deterministas por (world_seed, kind, index).
    kind: 'archive' (pre-anomalía, limpios) | 'new' (post-anomalía)."""

    def __init__(self, params: dict):
        self.p = params

    def lot(self, kind: str, index: int) -> dict:
        seed = np.random.SeedSequence([self.p["world_seed"], hash(kind) & 0xFFFF, index])
        rng = np.random.default_rng(seed)
        q = rng.normal(0.0, SQ)
        affected = (kind == "new") and (rng.random() < self.p["pi"])
        fault = -self.p["d_shift"] + rng.normal(0.0, S_EXTRA)
        return {"lot_id": f"{kind[0].upper()}{index:04d}", "kind": kind,
                "index": index, "q_clean": q, "affected": affected, "fault": fault}


def true_purity(lot: dict, pole: str, T: float, params: dict) -> float:
    """Pureza REAL del material (lo que puntúa y lo que ve el lab externo)."""
    base = params["mu0"] + params["beta"] * (T - T0) + lot["q_clean"]
    if pole == "proceso" and lot["affected"]:
        base += lot["fault"]
    return base


def sensor_reading(lot: dict, pole: str, T: float, rng, vial_id: int = 0) -> float:
    """Lectura del sensor. MISMO orden de operaciones en ambos polos (byte-exacto
    bajo CRN): el shift vale lo mismo cuando aplica; cambia DÓNDE vive."""
    applies = lot["affected"] and (pole == "proceso" or vial_id == 0)
    shift = lot["fault"] if applies else 0.0
    return (params_cache["mu0"] + params_cache["beta"] * (T - T0) + lot["q_clean"]
            + rng.normal(0, SP) + shift + rng.normal(0, SM))


params_cache: dict = {"mu0": MU0, "beta": BETA}     # se refresca al cargar instancia


def refresh_cache(params: dict) -> None:
    params_cache.update(params)


# --- la horquilla: verosimilitudes y D_pre (reward path, TRIPWIRE aprobado) ---
def h2(p: float) -> float:
    p = min(max(p, 1e-12), 1 - 1e-12)
    return -(p * log2(p) + (1 - p) * log2(1 - p))


def loglik_channel(kind: str, cfg: dict, z: np.ndarray, fork: str, params: dict) -> float:
    """log p(z | fork) para cada canal diagnóstico. La rutina devuelve 0 para
    ambos (idéntica por construcción)."""
    if kind == "routine":
        return 0.0
    if kind == "standard":
        se = SM / np.sqrt(cfg["reps"])
        ll = 0.0
        for zi in np.atleast_1d(z):
            clean = np.exp(-0.5 * ((zi - params["std_val"]) / se) ** 2) / se
            sfa = np.hypot(se, S_EXTRA)
            fa = np.exp(-0.5 * ((zi - (params["std_val"] - params["d_shift"])) / sfa) ** 2) / sfa
            dens = (1 - params["pi"]) * clean + params["pi"] * fa if fork == "vial_fault" else clean
            ll += float(np.log(max(dens, 1e-300)))
        return ll
    if kind == "lab":
        ll = 0.0
        for zi in np.atleast_1d(z):        # lotes FLAGGED (bajos en el stream)
            if fork == "vial_fault":
                ll += -0.5 * ((zi - params["mu0"]) / SQ) ** 2 - np.log(SQ)
            else:
                ll += -0.5 * ((zi - (params["mu0"] - params["d_shift"])) / SQ2) ** 2 - np.log(SQ2)
        return ll
    if kind == "revial":
        s_v = np.hypot(SQ, SP / np.sqrt(cfg.get("reps", 4)))
        s_m = np.hypot(SQ2, SP / np.sqrt(cfg.get("reps", 4)))
        ll = 0.0
        for zi in np.atleast_1d(z):
            if fork == "vial_fault":
                ll += -0.5 * ((zi - params["mu0"]) / s_v) ** 2 - np.log(s_v)
            else:
                ll += -0.5 * ((zi - (params["mu0"] - params["d_shift"])) / s_m) ** 2 - np.log(s_m)
        return ll
    raise ValueError(kind)


def sample_channel(kind: str, cfg: dict, fork: str, rng, params: dict) -> np.ndarray:
    if kind == "standard":
        out = []
        for _ in range(cfg["n_viales"]):
            f = (fork == "vial_fault") and (rng.random() < params["pi"])
            base = params["std_val"] + ((-params["d_shift"] + rng.normal(0, S_EXTRA)) if f else 0.0)
            out.append(base + rng.normal(0, SM / np.sqrt(cfg["reps"])))
        return np.asarray(out)
    if kind == "lab":
        if fork == "vial_fault":
            return params["mu0"] + rng.normal(0, SQ, cfg["n_lotes"])
        return params["mu0"] - params["d_shift"] + rng.normal(0, SQ2, cfg["n_lotes"])
    if kind == "revial":
        s_v = np.hypot(SQ, SP / np.sqrt(cfg.get("reps", 4)))
        s_m = np.hypot(SQ2, SP / np.sqrt(cfg.get("reps", 4)))
        if fork == "vial_fault":
            return params["mu0"] + rng.normal(0, s_v, cfg["n_lotes"])
        return params["mu0"] - params["d_shift"] + rng.normal(0, s_m, cfg["n_lotes"])
    if kind == "routine":
        out = []
        for _ in range(cfg["n_lotes"]):
            low = rng.random() < params["pi"]
            out.append(params["mu0"] + (rng.normal(-params["d_shift"], SQ2) if low
                                        else rng.normal(0, SQ)))
        return np.asarray(out)
    raise ValueError(kind)


def expected_info(kind: str, cfg: dict, w_v: float, params: dict,
                  M: int = 2000, seed: int = 777) -> float:
    """d_t = H2(w) − E[H2(w')] bajo la predictiva actual (fórmula r3 de Codex).
    Server-side, ANTES de observar; acumulativa vía el posterior del episodio."""
    if kind == "routine":
        return 0.0
    rng = np.random.default_rng(seed)
    h_now, acc = h2(w_v), 0.0
    for fork, w in (("vial_fault", w_v), ("lot_mixture", 1 - w_v)):
        m = max(1, int(M * w))
        for _ in range(m):
            z = sample_channel(kind, cfg, fork, rng, params)
            lv = loglik_channel(kind, cfg, z, "vial_fault", params)
            lm = loglik_channel(kind, cfg, z, "lot_mixture", params)
            top = max(lv, lm)
            pv = w_v * np.exp(lv - top)
            pm = (1 - w_v) * np.exp(lm - top)
            acc += w / m * h2(pv / (pv + pm))
    return max(h_now - acc, 0.0)


def posterior_update(w_v: float, kind: str, cfg: dict, z: np.ndarray, params: dict) -> float:
    lv = loglik_channel(kind, cfg, z, "vial_fault", params)
    lm = loglik_channel(kind, cfg, z, "lot_mixture", params)
    top = max(lv, lm)
    pv = w_v * np.exp(lv - top)
    pm = (1 - w_v) * np.exp(lm - top)
    return float(pv / (pv + pm))


# --- la entrega y su examen (proceso, no lecturas) ----------------------------
def _speed_T(regime) -> float:
    config = getattr(regime, "config", None) or (regime.get("config", {}) if isinstance(regime, dict) else {})
    return min(max(float((config or {}).get("T", 1.0)), T_RANGE[0]), T_RANGE[1])


def pole_truth_program(pole: str, params: dict):
    """La verdad como programa: genera purezas de LOTES NUEVOS a temperatura T."""
    def prog(regime, n, seed, pole=pole, params=params):
        T = _speed_T(regime)
        rng = np.random.default_rng(np.random.SeedSequence([int(seed), 0xD1]))
        out = []
        for _ in range(int(n)):
            q = rng.normal(0, SQ)
            affected = rng.random() < params["pi"]
            fault = -params["d_shift"] + rng.normal(0, S_EXTRA)
            y = params["mu0"] + params["beta"] * (T - T0) + q
            if pole == "proceso" and affected:
                y += fault
            out.append(y)
        return pd.DataFrame({"unit_id": np.arange(int(n), dtype=float),
                             "y": np.asarray(out)})
    return prog


def program_curve_stats(program, T: float, n: int = 3000, seed: int = 424242) -> dict:
    df = program(type("R", (), {"config": {"T": T}, "context": {}})(), n, seed) \
        if False else program({"config": {"T": T}}, n, seed)
    y = np.asarray(df["y"], float)
    lo = np.mean(y < np.mean(y) - 1.8)
    return {"mean": float(np.mean(y)), "sd": float(np.std(y)),
            "p10": float(np.percentile(y, 10)), "frac_low": float(lo)}


def s_metric(program, pole: str, params: dict) -> dict:
    """S por polo: A ancla 0=mejor unimodal, 1=verdad mezcla; B ancla 1=verdad
    limpia, 0=mezcla horneada. Distancia = |p10 - p10_truth| + |sd - sd_truth|
    sobre la grilla de T (estadísticos donde la mezcla muerde)."""
    grid = (0.8, 1.0, 1.2)
    truth = pole_truth_program(pole, params)
    anti = pole_truth_program("proceso" if pole == "instrumento" else "instrumento", params)

    def dist(a, b):
        tot = 0.0
        for T in grid:
            sa, sb = program_curve_stats(a, T), program_curve_stats(b, T)
            tot += abs(sa["p10"] - sb["p10"]) + abs(sa["sd"] - sb["sd"])
        return tot / len(grid)

    d_model = dist(program, truth)
    d_anchor = dist(anti, truth)
    s = 0.0 if d_anchor < 1e-9 else float(np.clip(1.0 - d_model / d_anchor, 0.0, 1.0))
    return {"S": s, "d_model": d_model, "d_anchor": d_anchor}


def structural_flag(program, params: dict) -> dict:
    """¿La entrega contiene estructura de mezcla? (dip/bimodalidad en lotes
    generados a T=1.0). Mecánico: gap entre modas > 1.5 con masa baja >= 8%."""
    df = program({"config": {"T": 1.0}}, 4000, 99)
    y = np.sort(np.asarray(df["y"], float))
    med = np.median(y)
    low = y[y < med - 1.5]
    frac_low = len(low) / len(y)
    gap = float(med - np.mean(low)) if len(low) else 0.0
    return {"has_mixture": bool(frac_low >= 0.08 and gap >= 2.0),
            "frac_low": frac_low, "gap": gap}
