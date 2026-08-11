"""D2 "El turno de decisión" — la vara nueva sobre el esqueleto D1 (ADR 0175/0176/0177).

Física compartida: cases/d1_calibracion_common.py (polos, lotes, canales — intactos).
Lo NUEVO es la vara y el examen:

  - **CRPS** (Continuous Ranked Probability Score): regla propia, continua, cero-LLM,
    cobra la CDF COMPLETA — una familia de k parámetros no puede clavarla (el fix del
    agujero S=0.986; Codex la eligió sobre multi-cuantil como primaria).
  - **Grilla con EXTRAPOLACIÓN**: el agente opera certificado en T∈[0.8,1.2]; el examen
    evalúa también T=0.7 y T=1.3 (regímenes no visitados — donde el salto paga, ADR 0150).
  - **Error de decisión** (diagnóstico, no primario): |P_model(y<L) − P_true(y<L)| —
    la cantidad que la planta usa para aceptar lotes (la intervención do() del episodio).

S bilateral como siempre: 1 = verdad del polo, 0 = anti-ancla (la verdad del otro polo).
Reward path cero-LLM.
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from cases import d1_calibracion_common as C  # noqa: E402  (la física)

EXAM_GRID = (0.7, 0.9, 1.1, 1.3)      # 0.7/1.3 EXTRAPOLACIÓN (banda operable 0.8-1.2)
OPER_BAND = (0.8, 1.2)                 # límite certificado para experimentos del agente
SPEC_OFFSET = 2.0                      # límite de especificación L = mu0 - SPEC_OFFSET
N_OBS = 3000                           # lotes de verdad por T para el examen
N_ENS = 2000                           # muestras del modelo por T

# --- la física D2: la subpoblación INTERACTÚA con T (la brecha causal) ---------
# La reacción lateral que degrada lotes se acelera con la temperatura: dentro de
# la banda operable es leve; fuera, domina. El que no escribe la estructura no
# puede extrapolar (ahí paga el salto — ADR 0150). En el polo B, la tasa de
# fallas de vial sigue la MISMA curva (byte-identidad de rutina intacta).
PI_SLOPE = 0.5                         # pi(T) = clip(pi0 + PI_SLOPE*(T-1), .02, .65)

# La PERILLA FÍSICA de la brecha (regla de Lucas: se ajusta y certifica ANTES del
# mundo). D2 sobreescribe la física D1 donde haga falta; los valores se fijan con
# el scan de scripts/design_d2_vara.py --scan y quedan congelados en la instancia.
D2_DEFAULTS = {"d_shift_d2": None,     # None -> hereda params["d_shift"] de D1
               "pi_slope": PI_SLOPE,
               "s_extra_d2": None}     # None -> hereda C.S_EXTRA


def _d2(params: dict, key: str, fallback):
    v = params.get(key, D2_DEFAULTS.get(key))
    return fallback if v is None else v


def pi_T(T: float, params: dict) -> float:
    slope = _d2(params, "pi_slope", PI_SLOPE)
    return float(np.clip(params["pi"] + slope * (T - 1.0), 0.02, 0.65))


def pole_truth_program_d2(pole: str, params: dict):
    """La verdad D2: mezcla cuya fracción degradada crece con T (proceso) /
    proceso limpio con la misma tasa de fallas de vial (instrumento)."""
    d_shift = _d2(params, "d_shift_d2", params["d_shift"])
    s_extra = _d2(params, "s_extra_d2", C.S_EXTRA)

    def prog(regime, n, seed, pole=pole, params=params):
        T = C._speed_T(regime)
        p = pi_T(T, params)
        rng = np.random.default_rng(np.random.SeedSequence([int(seed), 0xD2]))
        q = rng.normal(0, C.SQ, int(n))
        affected = rng.random(int(n)) < p
        fault = -d_shift + rng.normal(0, s_extra, int(n))
        y = params["mu0"] + params["beta"] * (T - 1.0) + q
        if pole == "proceso":
            y = y + np.where(affected, fault, 0.0)
        import pandas as pd
        return pd.DataFrame({"unit_id": np.arange(int(n), dtype=float), "y": y})
    return prog


def lot_d2(params: dict, kind: str, index: int, T_prod: float) -> dict:
    """Lote D2: como C.LotState pero `affected` depende de la T de PRODUCCIÓN
    (pi(T)). El uniforme u es el MISMO stream keyed que D1 → byte-identidad entre
    polos para la misma secuencia de acciones (el umbral cambia, el stream no)."""
    tag = {"archive": 1, "new": 2}[kind]
    rng = np.random.default_rng(np.random.SeedSequence([params["world_seed"], tag, index]))
    q = rng.normal(0.0, C.SQ)
    u = rng.random()
    affected = (kind == "new") and (u < pi_T(T_prod, params))
    d_shift = _d2(params, "d_shift_d2", params["d_shift"])
    s_extra = _d2(params, "s_extra_d2", C.S_EXTRA)
    fault = -d_shift + rng.normal(0.0, s_extra)
    return {"lot_id": f"{kind[0].upper()}{index:04d}", "kind": kind, "index": index,
            "q_clean": q, "affected": affected, "fault": fault, "T_prod": T_prod}


def crps_sample(ens: np.ndarray, obs: np.ndarray) -> float:
    """CRPS empírico promedio: E|X−y| − ½E|X−X′| (estimador fair, vectorizado)."""
    ens = np.sort(np.asarray(ens, float))
    obs = np.asarray(obs, float)
    m = len(ens)
    # E|X−y| para cada y (via CDF empírica ordenada)
    term1 = np.mean(np.abs(obs[:, None] - ens[None, :]), axis=1)
    # ½E|X−X′| con la identidad de Gini sobre la muestra ordenada
    i = np.arange(1, m + 1)
    gini = 2.0 * np.sum((2 * i - m - 1) * ens) / (m * m)
    return float(np.mean(term1) - 0.5 * gini)


def model_crps_at(program, T: float, obs: np.ndarray, seed: int = 777) -> float:
    df = program(C._regime(T), N_ENS, seed)
    return crps_sample(np.asarray(df["y"], float), obs)


def s_metric_crps(program, pole: str, params: dict,
                  grid: tuple = EXAM_GRID, seed: int = 4242,
                  anchor_zero=None) -> dict:
    """S por CRPS sobre la grilla del examen (incl. extrapolación).

    ANCLAJE (la lección del agujero D1, patrón del rung 0 restaurado):
      1 = piso de la verdad del polo
      0 = **el mejor rival SIN el salto** (anchor_zero, congelado en certificación
          para el polo proceso) — S mide la fracción del VALOR DEL DESCUBRIMIENTO
          capturada, no la distancia al peor modelo posible.
    Si anchor_zero es None se usa la anti-ancla del gemelo (verdad del otro polo)
    — el comportamiento correcto para el polo instrumento (0 = hornear la mezcla)."""
    truth = pole_truth_program_d2(pole, params)
    if anchor_zero is None:
        anchor_zero = pole_truth_program_d2(
            "proceso" if pole == "instrumento" else "instrumento", params)
    d_model = d_zero = 0.0
    floors = []
    for k, T in enumerate(grid):
        obs = np.asarray(truth(C._regime(T), N_OBS, seed + k)["y"], float)
        floor = model_crps_at(truth, T, obs, seed=seed + 50 + k)
        floors.append(floor)
        d_model += model_crps_at(program, T, obs) - floor
        d_zero += model_crps_at(anchor_zero, T, obs) - floor
    d_model, d_zero = d_model / len(grid), d_zero / len(grid)
    s = 0.0 if d_zero < 1e-9 else float(np.clip(1.0 - d_model / d_zero, 0.0, 1.0))
    return {"S": s, "d_model": d_model, "d_anchor": d_zero,
            "floor": float(np.mean(floors))}


def logscore_at(program, T: float, obs: np.ndarray, seed: int = 777) -> float:
    """Log-score (ignorance) vía KDE gaussiana determinista sobre el ensemble del
    modelo (Silverman; densidad clipeada en 1e-9). LA VARA PRIMARIA D2: paga la
    estructura exponencialmente donde CRPS paga migajas (verificado en el scan:
    CRPS ratio<=0.07 hasta con d=7; la verosimilitud separó 0.07-0.16 nats/lote
    ya en la auditoría D1). Cero-LLM, determinista dado el seed."""
    ens = np.asarray(program(C._regime(T), N_ENS, seed)["y"], float)
    m = len(ens)
    sd = float(np.std(ens))
    iqr = float(np.subtract(*np.percentile(ens, [75, 25])))
    h = max(0.9 * min(sd, iqr / 1.34 if iqr > 0 else sd) * m ** (-0.2), 1e-3)
    obs = np.asarray(obs, float)
    out = np.empty(len(obs))
    for i0 in range(0, len(obs), 500):          # chunk: 500×m sin explotar memoria
        z = (obs[i0:i0 + 500, None] - ens[None, :]) / h
        dens = np.exp(-0.5 * z * z).sum(axis=1) / (m * h * np.sqrt(2 * np.pi))
        out[i0:i0 + 500] = np.log(np.maximum(dens, 1e-9))
    return float(np.mean(out))


def s_metric_log(program, pole: str, params: dict,
                 grid: tuple = EXAM_GRID, seed: int = 4242,
                 anchor_zero=None) -> dict:
    """S primaria D2 por log-score, mismo anclaje que s_metric_crps:
    1 = piso de la verdad · 0 = mejor rival sin salto (proceso) / anti (instrumento).
    Devuelve además la brecha en NATS/lote (la unidad física de la paga)."""
    truth = pole_truth_program_d2(pole, params)
    if anchor_zero is None:
        anchor_zero = pole_truth_program_d2(
            "proceso" if pole == "instrumento" else "instrumento", params)
    d_model = d_zero = 0.0
    floors = []
    for k, T in enumerate(grid):
        obs = np.asarray(truth(C._regime(T), N_OBS, seed + k)["y"], float)
        floor = logscore_at(truth, T, obs, seed=seed + 50 + k)
        floors.append(floor)
        d_model += floor - logscore_at(program, T, obs)      # nats perdidos
        d_zero += floor - logscore_at(anchor_zero, T, obs)
    d_model, d_zero = d_model / len(grid), d_zero / len(grid)
    s = 0.0 if d_zero < 1e-9 else float(np.clip(1.0 - d_model / d_zero, 0.0, 1.0))
    return {"S": s, "nats_model": d_model, "nats_anchor": d_zero,
            "floor": float(np.mean(floors))}


def decision_tail_error(program, pole: str, params: dict,
                        grid: tuple = EXAM_GRID, seed: int = 993) -> dict:
    """Diagnóstico de decisión: error absoluto medio en P(y < L) sobre la grilla —
    la cantidad con la que la planta acepta lotes (la intervención del episodio)."""
    truth = pole_truth_program_d2(pole, params)
    L = params["mu0"] - SPEC_OFFSET
    errs = []
    for k, T in enumerate(grid):
        yt = np.asarray(truth(C._regime(T), 20000, seed + k)["y"], float)
        ym = np.asarray(program(C._regime(T), 20000, seed + 30 + k)["y"], float)
        errs.append(abs(float((ym < L).mean()) - float((yt < L).mean())))
    return {"mae_tail": float(np.mean(errs)), "spec_limit": L}
