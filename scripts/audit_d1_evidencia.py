"""Auditoría POST-TANDA cero-LLM (pedida por Codex en el cierre de ciclo D1):
¿la evidencia que cada agente COMPRÓ exigía estructura de mezcla en su entrega?

Por celda: (a) sobre los lotes nuevos que el agente realmente vio (experimentos +
monitoreo, promediado por lote, detrend lineal en T), ajustar mezcla de 2
gaussianas (EM, k=5) vs unimodal (k=2) → ΔBIC y CV 5-fold held-out; (b) el
posterior server-side final w_v (<0.5 = la horquilla favorecía causa material).

Certificación (regla de Codex): mezcla gana claro (ΔBIC>=10 y CV a favor) en
>=12/15 de proceso → la evidencia disponible exigía estructura y el claim
conductual queda en pie; si no, el gate cobraba más de lo que la historia
justificaba. Instrumento se corre como control: la MISMA flagrancia en lecturas
debe aparecer (rutina byte-idéntica); allí la entrega correcta sigue siendo
limpia (la horquilla decide, no las lecturas). POST-HOC, jamás reward.
"""

from __future__ import annotations

import glob
import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))


def lots_seen(rec: dict) -> np.ndarray:
    """Residuales por lote nuevo (detrend lineal en T) de lo que el agente vio."""
    per_lot: dict[str, list[tuple[float, float]]] = {}
    for s in rec["served"]:
        if s["verb"] not in ("experiment", "monitor"):
            continue
        for row in s["rows"]:
            per_lot.setdefault(row["lot_id"], []).append((row["T"], row["y"]))
    ts, ys = [], []
    for vals in per_lot.values():
        ts.append(np.mean([v[0] for v in vals]))
        ys.append(np.mean([v[1] for v in vals]))
    ts, ys = np.asarray(ts), np.asarray(ys)
    X = np.column_stack([np.ones_like(ts), ts - 1.0])
    beta, *_ = np.linalg.lstsq(X, ys, rcond=None)
    return ys - X @ beta


def loglik_1(r: np.ndarray, mu: float, s: float) -> float:
    s = max(s, 1e-6)
    return float(np.sum(-0.5 * ((r - mu) / s) ** 2 - np.log(s) - 0.9189385332046727))


def fit_1(r: np.ndarray) -> tuple[float, float, float]:
    mu, s = float(np.mean(r)), float(np.std(r))
    return mu, s, loglik_1(r, mu, s)


def fit_2_em(r: np.ndarray, iters: int = 300) -> tuple[dict, float]:
    """EM de mezcla 2-comp (varianzas libres), init por cuantiles."""
    pi, mu1, mu2 = 0.8, float(np.percentile(r, 60)), float(np.percentile(r, 5))
    s1 = s2 = max(float(np.std(r)) * 0.6, 1e-3)
    for _ in range(iters):
        d1 = pi * np.exp(-0.5 * ((r - mu1) / s1) ** 2) / max(s1, 1e-9)
        d2 = (1 - pi) * np.exp(-0.5 * ((r - mu2) / s2) ** 2) / max(s2, 1e-9)
        g = d1 / np.maximum(d1 + d2, 1e-300)
        pi = float(np.clip(np.mean(g), 0.02, 0.98))
        mu1 = float(np.sum(g * r) / max(np.sum(g), 1e-9))
        mu2 = float(np.sum((1 - g) * r) / max(np.sum(1 - g), 1e-9))
        s1 = float(np.sqrt(np.sum(g * (r - mu1) ** 2) / max(np.sum(g), 1e-9)))
        s2 = float(np.sqrt(np.sum((1 - g) * (r - mu2) ** 2) / max(np.sum(1 - g), 1e-9)))
        s1, s2 = max(s1, 0.05), max(s2, 0.05)
    ll = float(np.sum(np.log(np.maximum(
        pi * np.exp(-0.5 * ((r - mu1) / s1) ** 2) / (s1 * np.sqrt(2 * np.pi))
        + (1 - pi) * np.exp(-0.5 * ((r - mu2) / s2) ** 2) / (s2 * np.sqrt(2 * np.pi)),
        1e-300))))
    return {"pi_low": 1 - pi, "mu_main": mu1, "mu_low": mu2, "s1": s1, "s2": s2}, ll


def cv_gain(r: np.ndarray, k: int = 5, seed: int = 7) -> float:
    """Media held-out (LL2 - LL1) por punto, 5-fold."""
    rng = np.random.default_rng(seed)
    idx = rng.permutation(len(r))
    gains = []
    for f in range(k):
        te = idx[f::k]
        tr = np.setdiff1d(idx, te)
        mu, s, _ = fit_1(r[tr])
        p2, _ = fit_2_em(r[tr], iters=150)
        ll1 = loglik_1(r[te], mu, s)
        d1 = (1 - p2["pi_low"]) * np.exp(-0.5 * ((r[te] - p2["mu_main"]) / p2["s1"]) ** 2) / p2["s1"]
        d2 = p2["pi_low"] * np.exp(-0.5 * ((r[te] - p2["mu_low"]) / p2["s2"]) ** 2) / p2["s2"]
        ll2 = float(np.sum(np.log(np.maximum((d1 + d2) / np.sqrt(2 * np.pi), 1e-300))))
        gains.append((ll2 - ll1) / len(te))
    return float(np.mean(gains))


def main() -> int:
    print("celda                n_lotes  dBIC   CV/pto  pi_low  d_hat  w_v   veredicto")
    resumen: dict[str, list] = {"proceso": [], "instrumento": []}
    for pole in ("proceso", "instrumento"):
        for f in sorted(glob.glob(f"scripts/out/d1_calibracion/tanda_{pole}_*.json")):
            rec = json.loads(Path(f).read_text())
            r = lots_seen(rec)
            n = len(r)
            _, _, ll1 = fit_1(r)
            p2, ll2 = fit_2_em(r)
            dbic = (2 * ll2 - 5 * np.log(n)) - (2 * ll1 - 2 * np.log(n))
            cv = cv_gain(r)
            wv = rec["outcome"]["w_v_final"]
            wins = dbic >= 10.0 and cv > 0.0
            resumen[pole].append((wins, wv < 0.5))
            print(f"{Path(f).stem[6:]:20s} {n:6d} {dbic:6.1f} {cv:8.3f} "
                  f"{p2['pi_low']:6.2f} {p2['mu_main']-p2['mu_low']:6.2f} {wv:5.2f}  "
                  f"{'MEZCLA-GANA' if wins else 'no-claro'}")
    for pole, rs in resumen.items():
        w = sum(1 for a, _ in rs if a)
        both = sum(1 for a, b in rs if a and b)
        print(f"\n{pole}: mezcla gana claro en lecturas {w}/15 | "
              f"(gana Y ademas horquilla favorecia material) {both}/15")
    print("\nregla de Codex: >=12/15 en proceso certifica que la evidencia exigia "
          "estructura; instrumento con la misma flagrancia = control (la horquilla "
          "decide la entrega, no las lecturas)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
