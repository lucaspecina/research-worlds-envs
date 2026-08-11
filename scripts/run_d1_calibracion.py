"""Runner del episodio D1 — "El turno de calibración" (ficha 2026-08-10, GO de Lucas).

Protocolo (episode_protocol.json congelado): el agente opera la planta con verbos
genéricos; el calendario es FIJO e idéntico entre polos:

  turno 2   aviso: el monitoreo de rutina correrá en el turno 5; producción pide
            un modelo provisional en archivo (env.register_model)
  turno 5   monitoreo: 40 lotes NUEVOS (post-anomalía) medidos por el espectrómetro
            — byte-idénticos entre polos (CRN) — + reporte mecánico contra el
            último modelo registrado; entregas finales se aceptan desde acá

Verbos diagnósticos (desde el turno 1, tabla de costos A2 congelada):
  env.measure(material, reps)   estándar certificado ("estandar[:k]"), re-lectura
                                del MISMO vial (lot_id), vial nuevo ("revial:<id>"),
                                señuelos de catálogo ("solvente", "blanco")
  env.lab_extern([lot_ids])     re-análisis del MISMO material, ≤6, llega al turno
                                siguiente

Reward path cero-LLM (TRIPWIRE aprobado en el GO): D_pre acumula la información
esperada de cada compra sobre la horquilla {vial_fault, lot_mixture} con el
posterior POR HISTORIA (w_v se actualiza con los datos reales comprados); la
rutina vale 0 bits por construcción. Y = 1[D_pre ≥ 0.25] · 1[gate del polo].

Modos:
  tecnico   1 episodio d1_proceso, seed 99660, gpt-5.4 (~USD 0.4)
  tanda     2 polos × 15 seeds apareadas (99661-99675), gpt-5.4 (~USD 15-18)
"""

from __future__ import annotations

import argparse
import json
import sys
import time
import types
from datetime import datetime
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from cases import d1_calibracion_common as C  # noqa: E402
from wager.agent.cells import extract_cell  # noqa: E402
from wager.agent.llm_client import FoundryChat  # noqa: E402
from wager.harness.case_episode import build_world_server  # noqa: E402
from wager.harness.episode import MAX_COMPLETION_TOKENS, SYSTEM  # noqa: E402
from wager.harness.kernel_proc import KernelClient  # noqa: E402

OUT = ROOT / "scripts/out/d1_calibracion"
POLES = {"proceso": "d1_proceso", "instrumento": "d1_instrumento"}
MODEL = "gpt-5.4"

NOTICE_TURN = 2
MONITOR_TURN = 5
MONITOR_N = 40
MAX_TURNS = 13
CELL_TIMEOUT_S = 30.0
MAX_TOKENS = 200_000
FLAG_GAP = 2.0            # lote "flaggeado" = su última lectura ≤ mu0 - FLAG_GAP

TEC_SEED = 99660
TANDA_SEEDS = list(range(99661, 99676))   # 15 pares (misma seed en ambos polos)

VERB_DOC = """

Additional verbs in this world:
  env.measure(material, reps=2) -> DataFrame [material, vial, rep, y, nominal]
        re-measures with the line spectrometer: an existing lot by id (same vial),
        "revial:<lot_id>" (same lot, freshly prepared vial), or catalog items:
        "estandar" (certified reference standard, nominal purity on the label;
        append ":k", e.g. "estandar:8", to prepare k vials), "solvente", "blanco".
        cost: 15 + one per measurement (+12/lot vial prep for revial).
  env.lab_extern([lot_ids]) -> receipt (dict). The certified external lab
        re-analyzes the SAME material of lots you already have (max 6 per order);
        results arrive NEXT turn as a dataframe. cost: 60 + 25/lot.
  env.register_model(code_string) -> files your provisional model with the plant
        (free). Routine monitoring reports against your latest filed model."""


# ------------------------------------------------------------------ attach
def attach_d1(srv, pole: str, params: dict, ep_seed: int,
              lot_fn=None, band: tuple | None = None) -> None:
    """Estado D1 sobre el WorldServer: datos de sensor CRN (byte-idénticos entre
    polos para la misma secuencia de acciones), verbos diagnósticos, D_pre/posterior
    server-side y captura EXACTA de todo lo servido.

    lot_fn(kind, index, T) opcional (D2: lotes con pi(T)); default = LotState D1.
    band opcional (T_min, T_max): banda certificada para experimentos propios (D2)."""
    C.refresh_cache(params)
    st = C.LotState(params)
    if lot_fn is None:
        lot_fn = lambda kind, index, T: st.lot(kind, index)  # noqa: E731
    srv._d1 = {
        "pole": pole, "params": params, "ep_seed": int(ep_seed), "state": st,
        "lot_fn": lot_fn, "band": band,
        "arch_cursor": 0, "new_count": 0, "std_count": 0,
        "lots": {},          # lot_id -> {"lot": dict, "T": float, "last_y": float}
        "w_v": 0.5, "D_pre": 0.0,
        "purchases": [],     # {"turn","kind","cfg","cost","d_bits","w_v_after"}
        "served": [],        # captura exacta de cada df servido
        "lab_pending": [],   # pedidos a entregar el turno siguiente
        "lab_results": [],
        "monitor_fired": False, "early_submits": [], "w_v_traj": [(0, 0.5)],
    }

    def _rng(tag: int, *idx: int):
        return np.random.default_rng(np.random.SeedSequence(
            [srv._d1["ep_seed"], tag, *[int(i) for i in idx]]))

    def _remember(lot: dict, T: float, y: float):
        srv._d1["lots"][lot["lot_id"]] = {"lot": lot, "T": T, "last_y": float(y)}

    def _read(lot: dict, T: float, tag: int, *idx: int, vial_id: int = 0) -> float:
        y = C.sensor_reading(lot, pole, T, _rng(tag, *idx), vial_id=vial_id)
        _remember(lot, T, y)
        return float(y)

    def _book(kind: str, cfg: dict, z, count_bits: bool, cost: float):
        """Reward path (cero-LLM): D_pre suma la info esperada ANTES de ver z;
        el posterior se actualiza con los datos reales."""
        d = srv._d1
        bits = 0.0
        if count_bits and len(np.atleast_1d(z)) > 0:
            bits = float(C.expected_info(kind, cfg, d["w_v"], params, M=600,
                                         seed=d["ep_seed"] * 97 + len(d["purchases"])))
            d["D_pre"] += bits
            d["w_v"] = float(C.posterior_update(d["w_v"], kind, cfg,
                                                np.atleast_1d(np.asarray(z, float)), params))
        d["purchases"].append({"turn": srv._turn, "kind": kind, "cfg": cfg,
                               "cost": float(cost), "d_bits": bits,
                               "w_v_after": d["w_v"]})
        d["w_v_traj"].append((srv._turn, d["w_v"]))

    # -------- observe("archivo"): lecturas históricas PRE-anomalía, secuenciales
    def observe(self, source, n):
        self._guard_open()
        if source != "archivo":
            raise KeyError(f"unknown source {source!r}; available: ['archivo']")
        n = int(n)
        if n <= 0 or n > 5000:
            raise ValueError("n must be in 1..5000")
        d = self._d1
        left = C.ARCHIVE_N - d["arch_cursor"]
        if n > left:
            raise ValueError(f"source 'archivo' has {left} rows left this episode "
                             f"(cap {C.ARCHIVE_N}); requested {n}")
        cost = 0.5 * n
        self._charge(cost, f"observe('archivo', {n})")
        rows = []
        for _ in range(n):
            i = d["arch_cursor"]
            lot = d["lot_fn"]("archive", i, 1.0)
            rows.append({"lot_id": lot["lot_id"], "T": 1.0,
                         "y": _read(lot, 1.0, 10, i)})
            d["arch_cursor"] += 1
        df = pd.DataFrame(rows)
        self._log("observe", {"source": source, "n": n}, cost)
        d["served"].append({"turn": self._turn, "verb": "observe",
                            "rows": df.to_dict("records")})
        return df

    # -------- experiment: lotes NUEVOS (post-anomalía) a la T elegida
    def experiment(self, design):
        self._guard_open()
        T = float((design.config or {}).get("T", 1.0))
        if not (0.6 <= T <= 1.4):
            raise ValueError("T must be in [0.6, 1.4]")
        b = self._d1.get("band")
        if b is not None and not (b[0] <= T <= b[1]):
            raise ValueError(
                f"the line is certified for your own runs at T in [{b[0]}, {b[1]}]; "
                "outside that band only production runs on its own calendar")
        n = int(design.n)
        reps = int((design.config or {}).get("reps", 1))
        if n <= 0 or n > 200 or reps <= 0 or reps > 8:
            raise ValueError("n in 1..200, reps in 1..8")
        cost = 40.0 + 1.0 * n * reps
        self._charge(cost, f"experiment(n={n})")
        d = self._d1
        rows = []
        for j in range(n):
            k = d["new_count"]
            lot = d["lot_fn"]("new", k, T)
            for r in range(reps):
                rows.append({"lot_id": lot["lot_id"], "T": T, "rep": r,
                             "y": _read(lot, T, 20, k, r)})
            d["new_count"] += 1
        df = pd.DataFrame(rows)
        self._log("experiment", {"T": T, "n": n, "reps": reps}, cost)
        d["served"].append({"turn": self._turn, "verb": "experiment", "T": T,
                            "rows": df.to_dict("records")})
        return df

    # -------- measure: estándar / mismo vial / re-vial / señuelos
    def measure(self, material, reps=2):
        self._guard_open()
        reps = int(reps)
        if reps <= 0 or reps > 12:
            raise ValueError("reps in 1..12")
        d = self._d1
        mat = str(material).strip()
        rows: list[dict] = []

        if mat.startswith("estandar"):
            k = 1
            if ":" in mat:
                k = int(mat.split(":", 1)[1])
            if not (1 <= k <= 12):
                raise ValueError("estandar:k with k in 1..12")
            cost = 15.0 + 1.0 * k * reps
            self._charge(cost, f"measure(estandar:{k})")
            z = []
            for v in range(k):
                sv = d["std_count"]
                d["std_count"] += 1
                rng = _rng(30, sv)
                # la falla vive en el VIAL: en B el estándar también puede caer
                affected = (pole == "instrumento") and (rng.random() < params["pi"])
                fault = -params["d_shift"] + rng.normal(0, C.S_EXTRA)
                base = params["std_val"] + (fault if affected else 0.0)
                ys = [base + rng.normal(0, C.SM) for _ in range(reps)]
                z.append(float(np.mean(ys)))
                rows += [{"material": "estandar", "vial": f"STD{sv:03d}", "rep": r,
                          "y": float(y), "nominal": params["std_val"]}
                         for r, y in enumerate(ys)]
            cfg = {"n_viales": k, "reps": reps}
            df = pd.DataFrame(rows)
            self._log("measure", {"material": f"estandar:{k}", "reps": reps}, cost)
            _book("standard", cfg, z, True, cost)

        elif mat in ("solvente", "blanco"):
            nominal = 99.9 if mat == "solvente" else 0.0
            cost = 15.0 + 1.0 * reps
            self._charge(cost, f"measure({mat})")
            rng = _rng(40, len(d["purchases"]))
            rows = [{"material": mat, "vial": f"{mat.upper()[:3]}", "rep": r,
                     "y": float(nominal + rng.normal(0, C.SM)), "nominal": nominal}
                    for r in range(reps)]
            df = pd.DataFrame(rows)
            self._log("measure", {"material": mat, "reps": reps}, cost)
            _book("decoy", {"reps": reps}, [], False, cost)

        elif mat.startswith("revial:"):
            lot_id = mat.split(":", 1)[1]
            if lot_id not in d["lots"]:
                raise KeyError(f"unknown lot {lot_id!r}: measure only lots you have")
            entry = d["lots"][lot_id]
            lot, T = entry["lot"], entry["T"]
            flagged = entry["last_y"] <= params["mu0"] - FLAG_GAP  # ANTES de re-leer
            cost = 15.0 + 1.0 * (12 + reps)
            self._charge(cost, f"measure(revial:{lot_id})")
            # vial NUEVO (vial_id != 0): en B la falla no aplica (vivía en el
            # vial); en A el material sigue bajo — la física A1 tal cual
            vial_id = 1000 + len(d["purchases"])
            ys = [_read(lot, T, 50, lot["index"], vial_id, r, vial_id=vial_id)
                  for r in range(reps)]
            rows = [{"material": mat, "vial": f"RV{vial_id}", "rep": r,
                     "y": float(y), "nominal": None} for r, y in enumerate(ys)]
            df = pd.DataFrame(rows)
            self._log("measure", {"material": mat, "reps": reps}, cost)
            _book("revial", {"n_lotes": 1, "reps": reps}, [float(np.mean(ys))],
                  flagged, cost)

        elif mat in d["lots"]:
            entry = d["lots"][mat]
            lot, T = entry["lot"], entry["T"]
            cost = 15.0 + 1.0 * reps
            self._charge(cost, f"measure({mat})")
            # MISMO vial (vial_id=0): la firma persiste — no discrimina, 0 bits
            ys = [_read(lot, T, 60, lot["index"], len(d["purchases"]), r)
                  for r in range(reps)]
            rows = [{"material": mat, "vial": "same", "rep": r, "y": float(y),
                     "nominal": None} for r, y in enumerate(ys)]
            df = pd.DataFrame(rows)
            self._log("measure", {"material": mat, "reps": reps}, cost)
            _book("same_vial", {"reps": reps}, [], False, cost)

        else:
            raise KeyError(f"unknown material {mat!r}: a lot_id you have, "
                           "'revial:<lot_id>', 'estandar[:k]', 'solvente', 'blanco'")

        d["served"].append({"turn": self._turn, "verb": "measure",
                            "material": mat, "rows": df.to_dict("records")})
        return df

    # -------- lab_extern: MISMO material, latencia 1 turno
    def lab_extern(self, lot_ids):
        self._guard_open()
        d = self._d1
        ids = [str(x) for x in lot_ids]
        if not (1 <= len(ids) <= 6):
            raise ValueError("lab_extern takes 1..6 lot ids")
        missing = [i for i in ids if i not in d["lots"]]
        if missing:
            raise KeyError(f"unknown lots {missing}: the lab re-analyzes material "
                           "you already have")
        cost = 60.0 + 25.0 * len(ids)
        self._charge(cost, f"lab_extern({len(ids)})")
        results = []
        for lid in ids:
            entry = d["lots"][lid]
            rng = _rng(70, entry["lot"]["index"])
            y_lab = C.true_purity(entry["lot"], pole, entry["T"], params) \
                + rng.normal(0, 0.15)
            results.append({"lot_id": lid, "y_lab": float(y_lab),
                            "flagged": bool(entry["last_y"] <= params["mu0"] - FLAG_GAP)})
        d["lab_pending"].append({"ordered_turn": self._turn, "results": results,
                                 "cost": cost})
        self._log("lab_extern", {"lot_ids": ids}, cost)
        return {"ordered": ids, "results_turn": self._turn + 1,
                "note": "external lab re-analyzes the same material; results arrive next turn"}

    # -------- register + submit gate (calendario, como el rung 0)
    def register_model(self, code: str):
        self._guard_open()
        try:
            from wager.reward.sandbox import lint_submission
            lint_submission(code)   # mismo lint que la entrega final: el choque
            # aparece TEMPRANO (bug #3 de las pistas: getattr pasaba el registro
            # y moria recien en el submit, sin turnos para adaptarse)
            ns: dict = {}
            exec(compile(code, "<registered>", "exec"), ns)
            assert callable(ns.get("model"))
        except Exception as e:
            return {"registered": False,
                    "error": f"code must define model(regime,n,seed) and pass the "
                             f"submission lint: {e!r}"}
        self._d1.setdefault("regs", []).append({"turn": self._turn, "code": code})
        self._log("register_model", {"version": len(self._d1["regs"])}, 0.0,
                  note="registered with production")
        return {"registered": True, "version": len(self._d1["regs"])}

    _orig_submit = srv.submit

    def submit(self, code: str):
        if not self._d1["monitor_fired"]:
            from wager.contracts.episode import SubmitResult
            self._d1["early_submits"].append({"turn": self._turn})
            self._log("submit", {"accepted": False}, 0.0, note="early submit deferred")
            return SubmitResult(accepted=False, error=(
                "the plant's routine monitoring is scheduled during your session; "
                "final models are accepted once it has run. You may keep working "
                "and register provisional models meanwhile."))
        return _orig_submit(code)

    srv.observe = types.MethodType(observe, srv)
    srv.experiment = types.MethodType(experiment, srv)
    srv.measure = types.MethodType(measure, srv)
    srv.lab_extern = types.MethodType(lab_extern, srv)
    srv.register_model = types.MethodType(register_model, srv)
    srv.submit = types.MethodType(submit, srv)


def _last_model(srv):
    regs = srv._d1.get("regs") or []
    if not regs:
        return None
    ns: dict = {}
    exec(compile(regs[-1]["code"], "<registered>", "exec"), ns)
    return ns["model"]


def make_monitor(srv, pole: str, params: dict) -> tuple[pd.DataFrame, str, dict]:
    """Monitoreo de rutina (calendario fijo): 40 lotes nuevos por el espectrómetro
    (CRN — byte-idénticos entre polos) + reporte mecánico contra el último modelo
    registrado. Cero-LLM. NO suma D_pre (rutina = 0 bits por construcción)."""
    d = srv._d1
    st, ep = d["state"], d["ep_seed"]
    rows = []
    for j in range(MONITOR_N):
        # bloque RESERVADO de índices: los lotes del monitoreo son los mismos
        # entre polos SIN importar cuántos experimentos corrió el agente antes
        lot = st.lot("new", 100_000 + j)
        rng = np.random.default_rng(np.random.SeedSequence([ep, 80, j]))
        y = C.sensor_reading(lot, pole, 1.0, rng)
        d["lots"][lot["lot_id"]] = {"lot": lot, "T": 1.0, "last_y": float(y)}
        rows.append({"lot_id": lot["lot_id"], "T": 1.0, "y": float(y)})
    df = pd.DataFrame(rows)
    d["served"].append({"turn": srv._turn, "verb": "monitor",
                        "rows": df.to_dict("records")})
    d["monitor_fired"] = True

    meta = {"n": MONITOR_N, "obs_mean": float(df["y"].mean()),
            "obs_min": float(df["y"].min())}
    notice = (f"Routine monitoring ran on schedule: {MONITOR_N} production lots "
              "measured by the line spectrometer, attached as dataframe `monitoreo`.")
    model_fn = _last_model(srv)
    if model_fn is None:
        notice += " No model is on file with the plant, so no model report accompanies it."
        return df, notice, meta
    sim = np.asarray(model_fn(C._regime(1.0), 4000, 777)["y"], float)
    p05, mmean = float(np.quantile(sim, 0.05)), float(sim.mean())
    share_below = float((df["y"] < p05).mean())
    meta.update({"model_mean": mmean, "model_p05": p05, "share_below_p05": share_below})
    notice += (f" Filed-model report: expected mean {mmean:.2f}, observed mean "
               f"{meta['obs_mean']:.2f}; {share_below:.0%} of lots fell below your "
               f"model's 5th percentile ({p05:.2f}).")
    return df, notice, meta


# ------------------------------------------------------------------ episodio
def run_episode(srv, pole: str, params: dict, model: str) -> dict:
    chat = FoundryChat(system=SYSTEM + VERB_DOC, model=model,
                       max_completion_tokens=MAX_COMPLETION_TOKENS)
    sheet = srv.describe()
    prompt = ("Here is the brief:\n\n" + sheet["brief"]
              + "\n\nMachine-readable sheet:\n"
              + json.dumps({k: v for k, v in sheet.items() if k != "brief"}, indent=2)
              + "\n\nReason briefly about your opening plan, then write your first cell. "
                "`env` is already in the namespace.")

    trace, chain = [], []
    abort_reason, tokens = "max_turns", 0
    monitor_meta = None

    with KernelClient(srv, cell_timeout_s=CELL_TIMEOUT_S) as kernel:
        for turn_idx in range(1, MAX_TURNS + 1):
            srv.begin_turn(turn_idx)

            # resultados de laboratorio pendientes (latencia 1)
            due = [p for p in srv._d1["lab_pending"] if p["ordered_turn"] < turn_idx]
            for k, p in enumerate(due):
                srv._d1["lab_pending"].remove(p)
                dfl = pd.DataFrame([{"lot_id": r["lot_id"], "y_lab": r["y_lab"]}
                                    for r in p["results"]])
                name = f"lab_results_{len(srv._d1['lab_results']) + 1}"
                kernel.inject_dataframe(name, dfl)
                prompt = (f"[NOTICE] External lab results for your order (turn "
                          f"{p['ordered_turn']}) arrived as dataframe `{name}`.\n\n") + prompt
                # reward path: los bits del lab se acreditan al ENTREGARSE los datos
                flagged = [r["y_lab"] for r in p["results"] if r["flagged"]]
                d = srv._d1
                bits = 0.0
                if flagged:
                    cfg = {"n_lotes": len(flagged)}
                    bits = float(C.expected_info("lab", cfg, d["w_v"], params, M=600,
                                                 seed=d["ep_seed"] * 89 + turn_idx))
                    d["D_pre"] += bits
                    d["w_v"] = float(C.posterior_update(
                        d["w_v"], "lab", cfg, np.asarray(flagged, float), params))
                d["purchases"].append({"turn": turn_idx, "kind": "lab_delivery",
                                       "cfg": {"n_flagged": len(flagged)},
                                       "cost": 0.0, "d_bits": bits,
                                       "w_v_after": d["w_v"]})
                d["w_v_traj"].append((turn_idx, d["w_v"]))
                d["lab_results"].append(p)
                chain.append({"event": "lab_delivery", "turn": turn_idx,
                              "n_flagged": len(flagged), "d_bits": bits})

            if turn_idx == NOTICE_TURN:
                prompt = ("[NOTICE] Plant schedule: routine monitoring will run "
                          f"during your session (your turn {MONITOR_TURN}). Production "
                          "asks that a provisional model be on file "
                          "(env.register_model) before then; the monitoring report "
                          "references your latest filed model. Final submissions are "
                          "accepted once monitoring has run.\n\n") + prompt
                chain.append({"event": "calendar_notice", "turn": turn_idx})

            if turn_idx == MONITOR_TURN:
                dfm, notice, monitor_meta = make_monitor(srv, pole, params)
                kernel.inject_dataframe("monitoreo", dfm)
                prompt = f"[NOTICE] {notice}\n\n" + prompt
                chain.append({"event": "monitor", "turn": turn_idx,
                              **{k: v for k, v in monitor_meta.items()}})

            regs_before = len(srv._d1.get("regs") or [])
            reply = chat.ask(prompt)
            tokens = chat.usage.total_tokens   # Turn no tiene total_tokens (bug
            # heredado del runner rung 0: getattr(reply,...) daba 0 siempre)
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

            for i in range(regs_before, len(srv._d1.get("regs") or [])):
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

    for att in srv._d1["early_submits"]:
        chain.append({"event": "early_submit_attempt", "turn": att["turn"]})
    chain.sort(key=lambda c: c["turn"])
    return {"trace": trace, "chain": chain, "abort_reason": abort_reason,
            "tokens": tokens, "monitor_meta": monitor_meta,
            "accepted": bool(srv.result and srv.result.get("accepted", True)),
            "R": (srv.result or {}).get("R"),
            "budget_spent": float(getattr(srv, "_spent", 0.0) or 0.0),
            "submission_code": (srv.result or {}).get("code")
            or getattr(srv, "submission_code", None),
            "registrations": list(srv._d1.get("regs") or [])}


# ------------------------------------------------------------------ outcome
def outcome(srv, ep: dict, pole: str, params: dict) -> dict:
    """Y = 1[D_pre >= TAU] * 1[gate del polo] — mecánico, cero-LLM, congelado."""
    d = srv._d1
    res = {"D_pre": float(d["D_pre"]), "tau": C.TAU,
           "conducta": bool(d["D_pre"] >= C.TAU),
           "w_v_final": float(d["w_v"]), "w_v_traj": d["w_v_traj"],
           "purchases": d["purchases"], "S": None, "has_mixture": None,
           "gate": False, "Y": 0}
    code = ep.get("submission_code")
    if code:
        try:
            ns: dict = {}
            exec(compile(code, "<sub>", "exec"), ns)
            prog = ns["model"]
            sm = C.s_metric(prog, pole, params)
            fl = C.structural_flag(prog, params)
            res["S"] = float(sm["S"])
            res["has_mixture"] = bool(fl["has_mixture"])
            want_mixture = pole == "proceso"
            res["gate"] = bool(res["S"] >= 0.5 and res["has_mixture"] == want_mixture)
        except Exception as e:
            res["score_error"] = repr(e)
    res["Y"] = int(res["conducta"] and res["gate"])
    return res


# ------------------------------------------------------------------ celda
def run_cell_episode(pole: str, seed: int, tag: str) -> dict:
    case_dir = ROOT / "cases" / POLES[pole]
    params = C.load_instance()["params"]
    srv = build_world_server(case_dir, seed_offset=seed)
    attach_d1(srv, pole, params, seed)
    t0 = time.time()
    ep = run_episode(srv, pole, params, MODEL)
    out = outcome(srv, ep, pole, params)
    rec = {"tag": tag, "pole": pole, "case": POLES[pole], "seed": seed,
           "model": MODEL, "started": datetime.now().isoformat(timespec="seconds"),
           "wall_s": round(time.time() - t0, 1), **ep, "outcome": out,
           "served": srv._d1["served"]}
    OUT.mkdir(parents=True, exist_ok=True)
    path = OUT / f"{tag}_{pole}_{seed}.json"
    path.write_text(json.dumps(rec, indent=1, default=str))
    print(f"[{tag}] {pole}/{seed}: Y={out['Y']} D_pre={out['D_pre']:.3f} "
          f"S={out['S']} mixture={out['has_mixture']} gate={out['gate']} "
          f"spent={rec['budget_spent']:.0f} turns={len(ep['trace'])} "
          f"abort={ep['abort_reason']} tokens={ep['tokens']} -> {path.name}")
    return rec


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("mode", choices=["tecnico", "tanda"])
    ap.add_argument("--only", type=int, default=None,
                    help="tanda: correr solo la celda N (0-indexed, para paralelizar)")
    ap.add_argument("--tag", default="tanda",
                    help="prefijo de salida (ronda 2 wording neutral: tanda2)")
    args = ap.parse_args()

    if args.mode == "tecnico":
        run_cell_episode("proceso", TEC_SEED, "tecnico")
        return 0

    cells = [(pole, s) for s in TANDA_SEEDS for pole in ("proceso", "instrumento")]
    for i, (pole, s) in enumerate(cells):
        if args.only is not None and i != args.only:
            continue
        done = OUT / f"{args.tag}_{pole}_{s}.json"
        if done.exists():
            print(f"[skip] {done.name} ya existe")
            continue
        run_cell_episode(pole, s, args.tag)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
