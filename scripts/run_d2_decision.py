"""Runner del episodio D2 — "El turno de decisión" (paso 3; GO de Lucas 2026-08-11).

Reusa la maquinaria D1 (attach parametrizado: lotes pi(T) + banda certificada) y
agrega el calendario D2:

  turno 2   aviso: monitoreo (t5) y DECISIÓN OPERATIVA programada (t8) — la planta
            usa el último modelo registrado
  turno 5   monitoreo de rutina (40 lotes a T=1.0, byte-idénticos entre polos)
  turno 8   EL EVENTO DE DECISIÓN: la planta corre su piloto de alta temperatura
            (T=1.3, n=30 — fuera de la banda del agente) y toma la decisión de
            aceptación con el modelo registrado; el costo del error de predicción
            se DEBITA del presupuesto (ΔU real). AMBOS brazos reciben filas+débito;
            el brazo REBOTE recibe además la confrontación mecánica (V — la única
            diferencia entre brazos).

Endpoint primario: has_mixture (escribe estructura) por brazo × polo. Secundario:
Y = 1[D_pre ≥ 0.25] · 1[S_log ≥ 0.5 y flag del polo] (vara log, ancla congelada).

Modos:
  pistas    P2 (idea nombrada) × 3 seeds QUEMADAS (99700-99702) — certificación 0176/0177
  tecnico   1 episodio d2_proceso REBOTE, seed 99703
  tanda     2 brazos × 2 polos × 10 seeds apareadas (99704-99713), --only N
"""

from __future__ import annotations

import argparse
import json
import sys
import time
import types
from datetime import datetime
from pathlib import Path
from types import SimpleNamespace

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from cases import d1_calibracion_common as C  # noqa: E402
from cases import d2_decision_common as D2  # noqa: E402
from scripts.run_d1_calibracion import (  # noqa: E402
    CELL_TIMEOUT_S, MAX_TOKENS, VERB_DOC, attach_d1, outcome as d1_outcome,
)
from wager.agent.cells import extract_cell  # noqa: E402
from wager.agent.llm_client import FoundryChat  # noqa: E402
from wager.harness.case_episode import build_world_server  # noqa: E402
from wager.harness.episode import MAX_COMPLETION_TOKENS, SYSTEM  # noqa: E402
from wager.harness.kernel_proc import KernelClient  # noqa: E402

OUT = ROOT / "scripts/out/d2_decision"
POLES = {"proceso": "d2_proceso", "instrumento": "d2_instrumento"}
MODEL = "gpt-5.4"

NOTICE_TURN = 2
MONITOR_TURN = 5
MONITOR_N = 40
DECISION_TURN = 8
PILOT_T = 1.3
PILOT_N = 60
DEBIT_SCALE = 600.0
DEBIT_CAP = 150.0
NO_MODEL_DEBIT = 100.0
MAX_TURNS = 14

PISTA_SEEDS = [99714, 99715, 99716]     # QUEMADAS (certificación; 99700-99702
                                        # descartadas: 99700 crasheo por el bug del debito)
TEC_SEED = 99703
TANDA_SEEDS = list(range(99704, 99714))  # 10 seeds × 2 brazos × 2 polos = 40 celdas
ARMS = ("SILENCIO", "REBOTE")

# P2 — la idea nombrada (ADR 0177), texto CONGELADO; solo en modo pistas
PISTA_P2 = ("\n\n[NOTE from a colleague, mentioned in passing] "
            "'With signals like these I would consider the possibility that there "
            "are TWO populations of lots rather than one.'")

D2_VERB_DOC = VERB_DOC + """
  NOTE: the plant's calendar USES your latest filed model: routine monitoring
        reports against it, and scheduled operating decisions are taken with it —
        the resulting operating costs are debited from your budget."""


def _lazy_anchor(instance: dict):
    cm, cs = instance["ancla_cm"], instance["ancla_cs"]

    def prog(regime, n, seed):
        T = C._speed_T(regime)
        mu = cm[0] + cm[1] * (T - 1.0) + cm[2] * (T - 1.0) ** 2
        sd = min(max(float(np.exp(cs[0] + cs[1] * (T - 1.0) + cs[2] * (T - 1.0) ** 2)),
                     0.3), 6.0)
        rng = np.random.default_rng(seed)
        return pd.DataFrame({"unit_id": np.arange(int(n), dtype=float),
                             "y": mu + rng.normal(0, sd, int(n))})
    return prog


def _last_model_fn(srv):
    regs = srv._d1.get("regs") or []
    if not regs:
        return None
    ns: dict = {}
    exec(compile(regs[-1]["code"], "<registered>", "exec"), ns)
    return ns["model"]


def make_monitor_d2(srv, pole: str, params: dict) -> tuple[pd.DataFrame, str, dict]:
    """Monitoreo t5 (T=1.0): bloque reservado de lotes pi(T), CRN — como D1 pero
    con lot_fn D2. NO abre el gate de submit (eso lo hace la decisión, t8)."""
    d = srv._d1
    rows = []
    for j in range(MONITOR_N):
        lot = d["lot_fn"]("new", 100_000 + j, 1.0)
        rng = np.random.default_rng(np.random.SeedSequence([d["ep_seed"], 80, j]))
        y = C.sensor_reading(lot, pole, 1.0, rng)
        d["lots"][lot["lot_id"]] = {"lot": lot, "T": 1.0, "last_y": float(y)}
        rows.append({"lot_id": lot["lot_id"], "T": 1.0, "y": float(y)})
    df = pd.DataFrame(rows)
    d["served"].append({"turn": srv._turn, "verb": "monitor",
                        "rows": df.to_dict("records")})
    meta = {"n": MONITOR_N, "obs_mean": float(df["y"].mean()),
            "obs_min": float(df["y"].min())}
    notice = (f"Routine monitoring ran on schedule: {MONITOR_N} production lots "
              "measured by the line spectrometer, attached as dataframe `monitoreo`.")
    fn = _last_model_fn(srv)
    if fn is None:
        notice += " No model is on file with the plant, so no model report accompanies it."
        return df, notice, meta
    sim = np.asarray(fn(C._regime(1.0), 4000, 777)["y"], float)
    p05, mmean = float(np.quantile(sim, 0.05)), float(sim.mean())
    share = float((df["y"] < p05).mean())
    meta.update({"model_mean": mmean, "model_p05": p05, "share_below_p05": share})
    notice += (f" Filed-model report: expected mean {mmean:.2f}, observed mean "
               f"{meta['obs_mean']:.2f}; {share:.0%} of lots fell below your model's "
               f"5th percentile ({p05:.2f}).")
    return df, notice, meta


def make_decision(srv, pole: str, params: dict, arm: str) -> tuple[pd.DataFrame, str, dict]:
    """EL EVENTO (t8): piloto de producción a T=1.3 (bloque reservado, CRN) +
    decisión con el modelo registrado + DÉBITO por error de predicción. Ambos
    brazos: filas + débito. REBOTE: + confrontación mecánica. Cero-LLM."""
    d = srv._d1
    L = params["mu0"] - D2.SPEC_OFFSET
    rows, y_true = [], []
    for j in range(PILOT_N):
        lot = d["lot_fn"]("new", 200_000 + j, PILOT_T)
        rng = np.random.default_rng(np.random.SeedSequence([d["ep_seed"], 90, j]))
        y = C.sensor_reading(lot, pole, PILOT_T, rng)
        d["lots"][lot["lot_id"]] = {"lot": lot, "T": PILOT_T, "last_y": float(y)}
        rows.append({"lot_id": lot["lot_id"], "T": PILOT_T, "y": float(y)})
        y_true.append(C.true_purity(lot, pole, PILOT_T, params))
    df = pd.DataFrame(rows)
    # la decision se AUDITA contra laboratorio externo (pureza VERDADERA): el
    # debito queda alineado con la verdad del polo en A y en B (fix del dry-run:
    # con p_real por sensor, en B el debito castigaba al agente correcto)
    p_real = float((np.asarray(y_true) < L).mean())

    fn = _last_model_fn(srv)
    if fn is None:
        p_pred, debit = None, NO_MODEL_DEBIT
    else:
        sim = np.asarray(fn(C._regime(PILOT_T), 4000, 778)["y"], float)
        p_pred = float((sim < L).mean())
        debit = min(round(DEBIT_SCALE * abs(p_pred - p_real)), DEBIT_CAP)
    # el debito es CONSECUENCIA, no compra: se clampa a lo disponible y jamas
    # crashea el episodio (bug cazado por las pistas P2: BudgetError con 0.0)
    available = float(max(srv.budget_remaining, 0.0))
    charged = float(min(float(debit), available))
    if charged > 0:
        srv._charge(charged, "operating_decision_debit")
    srv._log("decision_event", {"p_pred": p_pred, "p_real": p_real,
                                "debit": float(debit), "charged": charged},
             charged, note="scheduled operating decision (plant calendar)")
    d["served"].append({"turn": srv._turn, "verb": "decision_pilot",
                        "rows": df.to_dict("records")})
    d["decision_fired"] = True

    notice = (f"The plant ran its scheduled high-temperature pilot (T={PILOT_T}, "
              f"n={PILOT_N} lots; attached as dataframe `piloto_decision`) and took "
              f"its lot-acceptance decision using your filed model"
              + ("." if fn is not None else
                 " — no model was on file, so the historical default was used."))
    notice += f" Operating cost adjustment debited from your budget: -{debit:.0f}."
    meta = {"p_pred": p_pred, "p_real": p_real, "debit": float(debit),
            "spec_limit": L, "arm": arm}
    if arm == "REBOTE" and fn is not None:
        notice += (f" DECISION REPORT — your model predicted {p_pred:.0%} of lots "
                   f"below spec ({L:.1f}) at T={PILOT_T}; the lab-audited pilot realized "
                   f"{p_real:.0%}. The mismatch is what you were charged for.")
    return df, notice, meta


def run_episode_d2(srv, pole: str, params: dict, arm: str, model: str,
                   pista: str | None = None) -> dict:
    chat = FoundryChat(system=SYSTEM + D2_VERB_DOC, model=model,
                       max_completion_tokens=MAX_COMPLETION_TOKENS)
    sheet = srv.describe()
    prompt = ("Here is the brief:\n\n" + sheet["brief"]
              + "\n\nMachine-readable sheet:\n"
              + json.dumps({k: v for k, v in sheet.items() if k != "brief"}, indent=2)
              + (pista or "")
              + "\n\nReason briefly about your opening plan, then write your first cell. "
                "`env` is already in the namespace.")

    trace, chain = [], []
    abort_reason, tokens = "max_turns", 0
    monitor_meta = decision_meta = None
    d = srv._d1
    d["decision_fired"] = False

    # gate de submit D2: hasta el evento de decisión (t8)
    _orig_submit = srv.submit

    def submit(self, code: str):
        if not self._d1.get("decision_fired"):
            from wager.contracts.episode import SubmitResult
            self._d1["early_submits"].append({"turn": self._turn})
            self._log("submit", {"accepted": False}, 0.0, note="early submit deferred")
            return SubmitResult(accepted=False, error=(
                "the plant's calendar has a scheduled operating decision pending; "
                "final models are accepted once it has run. You may keep working "
                "and register provisional models meanwhile."))
        return _orig_submit(code)

    srv.submit = types.MethodType(submit, srv)

    with KernelClient(srv, cell_timeout_s=CELL_TIMEOUT_S) as kernel:
        for turn_idx in range(1, MAX_TURNS + 1):
            srv.begin_turn(turn_idx)

            due = [p for p in d["lab_pending"] if p["ordered_turn"] < turn_idx]
            for p in due:
                d["lab_pending"].remove(p)
                dfl = pd.DataFrame([{"lot_id": r["lot_id"], "y_lab": r["y_lab"]}
                                    for r in p["results"]])
                name = f"lab_results_{len(d['lab_results']) + 1}"
                kernel.inject_dataframe(name, dfl)
                prompt = (f"[NOTICE] External lab results for your order (turn "
                          f"{p['ordered_turn']}) arrived as dataframe `{name}`.\n\n") + prompt
                flagged = [r["y_lab"] for r in p["results"] if r["flagged"]]
                bits = 0.0
                if flagged:
                    cfg = {"n_lotes": len(flagged)}
                    bits = float(C.expected_info("lab", cfg, d["w_v"], params, M=600,
                                                 seed=d["ep_seed"] * 89 + turn_idx))
                    d["D_pre"] += bits
                    d["w_v"] = float(C.posterior_update(
                        d["w_v"], "lab", cfg, np.asarray(flagged, float), params))
                d["purchases"].append({"turn": turn_idx, "kind": "lab_delivery",
                                       "cfg": {"n_flagged": len(flagged)}, "cost": 0.0,
                                       "d_bits": bits, "w_v_after": d["w_v"]})
                d["lab_results"].append(p)
                chain.append({"event": "lab_delivery", "turn": turn_idx,
                              "n_flagged": len(flagged), "d_bits": bits})

            if turn_idx == NOTICE_TURN:
                prompt = ("[NOTICE] Plant schedule: routine monitoring will run at "
                          f"your turn {MONITOR_TURN}, and the plant's scheduled "
                          f"OPERATING DECISION (high-temperature evaluation) will be "
                          f"taken at your turn {DECISION_TURN} using your latest "
                          "filed model (env.register_model). Resulting operating "
                          "costs are debited from your budget. Final submissions "
                          "are accepted once the decision has run.\n\n") + prompt
                chain.append({"event": "calendar_notice", "turn": turn_idx})

            if turn_idx == MONITOR_TURN:
                dfm, notice, monitor_meta = make_monitor_d2(srv, pole, params)
                kernel.inject_dataframe("monitoreo", dfm)
                prompt = f"[NOTICE] {notice}\n\n" + prompt
                chain.append({"event": "monitor", "turn": turn_idx, **monitor_meta})

            if turn_idx == DECISION_TURN:
                dfd, notice, decision_meta = make_decision(srv, pole, params, arm)
                kernel.inject_dataframe("piloto_decision", dfd)
                prompt = f"[NOTICE] {notice}\n\n" + prompt
                chain.append({"event": "decision", "turn": turn_idx, **decision_meta})

            regs_before = len(d.get("regs") or [])
            reply = chat.ask(prompt)
            tokens = chat.usage.total_tokens
            cell = extract_cell(reply.content)
            traj_before = len(srv.trajectory)
            rec = {"turn": turn_idx, "reply_text": reply.content, "cell": cell,
                   "verbs": [], "stdout": ""}
            if cell:
                res = kernel.run_cell(cell)
                rec["stdout"] = res.stdout + (f"\n[cell error] {res.error}" if res.error else "")
                rec["verbs"] = [{"verb": ev.verb, "args": ev.args}
                                for ev in srv.trajectory[traj_before:]]
            trace.append(rec)

            for i in range(regs_before, len(d.get("regs") or [])):
                chain.append({"event": "register", "turn": turn_idx, "version": i + 1})

            if srv.result is not None:
                abort_reason = "submitted"
                chain.append({"event": "submit", "turn": turn_idx})
                break
            if tokens > MAX_TOKENS:
                abort_reason = "token_budget"
                break
            prompt = ("Kernel output:\n" + (rec["stdout"] or "(no output)")
                      + "\n\nContinue: reasoning first, then ONE cell.")

    for att in d["early_submits"]:
        chain.append({"event": "early_submit_attempt", "turn": att["turn"]})
    chain.sort(key=lambda c: c["turn"])
    return {"trace": trace, "chain": chain, "abort_reason": abort_reason,
            "tokens": tokens, "monitor_meta": monitor_meta,
            "decision_meta": decision_meta,
            "accepted": bool(srv.result and srv.result.get("accepted", True)),
            "R": (srv.result or {}).get("R"),
            "budget_spent": float(getattr(srv, "_spent", 0.0) or 0.0),
            "submission_code": (srv.result or {}).get("code")
            or getattr(srv, "submission_code", None),
            "registrations": list(d.get("regs") or [])}


def outcome_d2(srv, ep: dict, pole: str, params: dict, instance: dict) -> dict:
    """Endpoint primario: has_mixture. Secundario: Y = conducta · gate(S_log+flag)."""
    d = srv._d1
    res = {"D_pre": float(d["D_pre"]), "tau": C.TAU,
           "conducta": bool(d["D_pre"] >= C.TAU),
           "w_v_final": float(d["w_v"]), "w_v_traj": d["w_v_traj"],
           "purchases": d["purchases"], "S_log": None, "has_mixture": None,
           "gate": False, "Y": 0}
    code = ep.get("submission_code")
    if code:
        try:
            ns: dict = {}
            exec(compile(code, "<sub>", "exec"), ns)
            prog = ns["model"]
            anchor = _lazy_anchor(instance) if pole == "proceso" else None
            sm = D2.s_metric_log(prog, pole, params, anchor_zero=anchor)
            fl = C.structural_flag(prog, params)
            res["S_log"] = float(sm["S"])
            res["nats_model"] = float(sm["nats_model"])
            res["has_mixture"] = bool(fl["has_mixture"])
            want = pole == "proceso"
            res["gate"] = bool(res["S_log"] >= 0.5 and res["has_mixture"] == want)
        except Exception as e:
            res["score_error"] = repr(e)
    res["Y"] = int(res["conducta"] and res["gate"])
    return res


def run_cell_episode(pole: str, seed: int, arm: str, tag: str,
                     pista: str | None = None) -> dict:
    case_dir = ROOT / "cases" / POLES[pole]
    instance = json.loads((ROOT / "cases" / "d2_proceso" / "instance.json").read_text())
    params = instance["params"]
    srv = build_world_server(case_dir, seed_offset=seed)
    attach_d1(srv, pole, params, seed,
              lot_fn=lambda kind, index, T: D2.lot_d2(params, kind, index, T),
              band=D2.OPER_BAND)
    t0 = time.time()
    ep = run_episode_d2(srv, pole, params, arm, MODEL, pista=pista)
    out = outcome_d2(srv, ep, pole, params, instance)
    rec = {"tag": tag, "pole": pole, "arm": arm, "case": POLES[pole], "seed": seed,
           "model": MODEL, "pista": bool(pista),
           "started": datetime.now().isoformat(timespec="seconds"),
           "wall_s": round(time.time() - t0, 1), **ep, "outcome": out,
           "served": srv._d1["served"]}
    OUT.mkdir(parents=True, exist_ok=True)
    path = OUT / f"{tag}_{arm}_{pole}_{seed}.json"
    path.write_text(json.dumps(rec, indent=1, default=str))
    dm = ep.get("decision_meta") or {}
    print(f"[{tag}] {arm}/{pole}/{seed}: flag={out['has_mixture']} S_log={out['S_log']} "
          f"Y={out['Y']} D_pre={out['D_pre']:.2f} debit={dm.get('debit')} "
          f"p_pred={dm.get('p_pred')} p_real={dm.get('p_real')} "
          f"spent={rec['budget_spent']:.0f} turns={len(ep['trace'])} "
          f"abort={ep['abort_reason']} -> {path.name}")
    return rec


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("mode", choices=["pistas", "tecnico", "tanda"])
    ap.add_argument("--only", type=int, default=None)
    args = ap.parse_args()

    if args.mode == "pistas":
        cells = [("proceso", PISTA_SEEDS[0]), ("proceso", PISTA_SEEDS[1]),
                 ("instrumento", PISTA_SEEDS[2])]
        for pole, s in cells:
            done = OUT / f"pistas_SILENCIO_{pole}_{s}.json"
            if done.exists():
                print(f"[skip] {done.name}")
                continue
            run_cell_episode(pole, s, "SILENCIO", "pistas", pista=PISTA_P2)
        return 0

    if args.mode == "tecnico":
        run_cell_episode("proceso", TEC_SEED, "REBOTE", "tecnico")
        return 0

    cells = [(arm, pole, s) for s in TANDA_SEEDS
             for arm in ARMS for pole in ("proceso", "instrumento")]
    for i, (arm, pole, s) in enumerate(cells):
        if args.only is not None and i != args.only:
            continue
        done = OUT / f"tanda_{arm}_{pole}_{s}.json"
        if done.exists():
            print(f"[skip] {done.name}")
            continue
        run_cell_episode(pole, s, arm, "tanda")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
