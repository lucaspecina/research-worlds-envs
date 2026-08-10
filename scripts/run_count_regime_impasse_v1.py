"""Runner del episodio de IMPASSE — count_regime_v1 (ficha 2026-08-09 + addendum ratificado).

Protocolo (episode_protocol.json, congelado): el agente registra su modelo provisional
(`env.register_model(code)`); producción corre DOS lotes piloto en calendario FIJO
(idéntico entre brazos y polos) y devuelve resultados según el brazo:

  RAW                   filas crudas del piloto, nada más
  VISIBLE_GLOBAL        filas + desajuste GLOBAL del último modelo registrado
  VISIBLE_ESTRUCTURADO  filas + global + residuos deviance FIRMADOS por celda de
                        velocidad sobre TODOS los lotes registrados (archivo +
                        compras + piloto), en orden de velocidad, sin ranking ni
                        etiquetas (compuerta C)

El piloto 2 se evalúa contra el ÚLTIMO modelo registrado (Mpatch; si no re-registró,
Mpatch = M0 — compuerta B). Cadena con turnos: M0/registros, pilotos, entrega.

Modos:
  tecnico            1 episodio (gpt-5.4, brazo VISIBLE_ESTRUCTURADO, seed 99520, brk)
  tanda              opción B aprobada: gpt-5.4 × 3 brazos × 10 seeds en brk
                     (99521-99550) + gemelo 2×2 (99551-99554). --only N para paralelizar.

Todo el scoring es cero-LLM. La clasificación estructural del modelo registrado es
mecánica (forma de la curva); validación semántica offline, jamás en el reward.
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

from cases import count_regime_v1_common as C  # noqa: E402
from wager.agent.cells import extract_cell  # noqa: E402
from wager.agent.llm_client import FoundryChat  # noqa: E402
from wager.harness.case_episode import build_world_server  # noqa: E402
from wager.harness.episode import (  # noqa: E402
    MAX_COMPLETION_TOKENS, SYSTEM,
)
from wager.harness.kernel_proc import KernelClient  # noqa: E402

OUT = ROOT / "scripts/out/count_regime_impasse_v1"
POLES = {"brk": "count_regime_v1", "smooth": "count_regime_twin_v1"}
MODEL = "gpt-5.4"

PILOT1_TURN = 6
PILOT2_TURN = 10
MAX_TURNS = 14            # = PILOT1_TURN + persistence budget (8) del protocolo
CELL_TIMEOUT_S = 30.0
MAX_TOKENS = 200_000

TEC_SEED = 99520
TANDA_BRK_SEEDS = list(range(99521, 99551))       # 30 = 3 brazos x 10 seeds
TANDA_SMOOTH_SEEDS = [99551, 99552, 99553, 99554]  # gemelo: RAW y ESTRUCTURADO x 2
ARMS = ("RAW", "VISIBLE_GLOBAL", "VISIBLE_ESTRUCTURADO")

REGISTER_DOC = """

One more verb exists in this world:
  env.register_model(code_string)     -> registers your provisional model with the plant
        (free). Production uses your LAST registered model for its routine reporting on
        scheduled lots. You may re-register whenever your model changes."""


# ----------------------------------------------------------------- registration
def attach_register(srv) -> None:
    """Attach the impasse protocol state: registration verb + EXACT capture of
    every lot the agent sees (the calibration report must reflect the agent's
    actual data, never a re-draw)."""
    srv._impasse_regs = []
    srv._impasse_cells = []          # {"turn", "speed", "ys"} - actual data

    _orig_observe, _orig_experiment = srv.observe, srv.experiment

    def observe(source, n):
        df = _orig_observe(source, n)
        if source == "archivo":
            srv._impasse_cells.append({"turn": srv._turn,
                                       "speed": C.PREFIX_ARCHIVE_SPEED,
                                       "ys": [float(v) for v in df["y"]]})
        return df

    def experiment(config=None, context=None, n=500, horizon=None):
        df = _orig_experiment(config=config, context=context, n=n, horizon=horizon)
        speed = float((config or {}).get("speed", 1.0))
        srv._impasse_cells.append({"turn": srv._turn, "speed": speed,
                                   "ys": [float(v) for v in df["y"]]})
        return df

    srv.observe, srv.experiment = observe, experiment

    def register_model(self, code: str):
        self._guard_open()
        try:
            ns: dict = {}
            exec(compile(code, "<registered>", "exec"), ns)
            assert callable(ns.get("model"))
        except Exception as e:
            return {"registered": False, "error": f"code must define model(regime,n,seed): {e!r}"}
        self._impasse_regs.append({"turn": self._turn, "code": code})
        self._log("register_model", {"version": len(self._impasse_regs)}, 0.0,
                  note="registered with production")
        return {"registered": True, "version": len(self._impasse_regs)}

    srv.register_model = types.MethodType(register_model, srv)


def _last_model(srv):
    if not getattr(srv, "_impasse_regs", None):
        return None, None
    reg = srv._impasse_regs[-1]
    ns: dict = {}
    exec(compile(reg["code"], "<registered>", "exec"), ns)
    return ns["model"], reg


# ----------------------------------------------------------------- pilot lots
def _bought_cells(srv, pole: str, params: dict, pilots: list[dict],
                  up_to_turn: int | None = None) -> list[dict]:
    """Every speed cell the agent has ACTUALLY seen (captured server-side):
    archive + experiments + pilots delivered so far. Exact data, no re-draws."""
    cells: dict[float, dict] = {}

    def add(speed, ys):
        speed = round(float(speed), 4)
        prev = cells.get(speed, {"speed": speed, "n": 0, "sum": 0.0})
        prev["n"] += len(ys)
        prev["sum"] += float(np.sum(ys))
        cells[speed] = prev

    for cell in getattr(srv, "_impasse_cells", []):
        if up_to_turn is None or cell["turn"] <= up_to_turn:
            add(cell["speed"], cell["ys"])
    for p in pilots:
        if up_to_turn is None or p.get("turn", 0) <= up_to_turn:
            add(p["speed"], p["rows"]["y"])
    out = sorted(cells.values(), key=lambda c: c["speed"])
    for c in out:
        c["mean"] = c["sum"] / max(c["n"], 1)
    return out


def _deviance(obs_mean: float, n: float, mu: float) -> float:
    """Signed Poisson deviance residual of a cell mean (aggregated)."""
    mu = max(mu, 1e-9)
    y = max(obs_mean, 1e-9)
    dev = 2.0 * n * (y * np.log(y / mu) - (y - mu))
    return float(np.sign(obs_mean - mu) * np.sqrt(max(dev, 0.0)))


def make_pilot(srv, pole: str, params: dict, which: int, arm: str,
               pilots_done: list[dict]) -> tuple[pd.DataFrame, str, dict]:
    proto = json.loads((ROOT / "cases" / POLES[pole] / "episode_protocol.json").read_text())
    ctl = proto["controls"][which - 1]
    df = C.pole_sample(pole, C._DictRegime({"speed": ctl["speed"]}), ctl["n"], ctl["seed"])
    rows = pd.DataFrame({"unit_id": df["unit_id"], "speed": ctl["speed"], "y": df["y"]})

    model_fn, reg = _last_model(srv)
    meta: dict = {"pilot": which, "speed": ctl["speed"], "n": ctl["n"],
                  "registered_version": (len(srv._impasse_regs) if getattr(srv, "_impasse_regs", None) else 0)}
    notice = (f"Production completed scheduled pilot lot {which} at speed {ctl['speed']} "
              f"(n={ctl['n']} lots) for the speed-increase evaluation. "
              f"Rows attached as dataframe `pilot_{which}`.")

    meta["observed_mean"] = float(rows["y"].mean())
    if model_fn is None or arm == "RAW":
        if model_fn is None:
            notice += " No model is registered with the plant, so no model report accompanies this lot."
        return rows, notice, meta

    # model expectation at the pilot speed (deterministic mean over many draws)
    mu = float(np.asarray(model_fn(C._DictRegime({"speed": ctl["speed"]}),
                                   4000, 777)["y"], float).mean())
    obs = meta["observed_mean"]
    dev_tot = _deviance(obs, ctl["n"], mu) ** 2
    chi2_95 = 3.84   # 1 dof, aggregated-cell test
    meta.update({"model_mean": mu,
                 "deviance_total": dev_tot, "chi2_95": chi2_95})
    notice += (f" Registered-model report: expected mean {mu:.2f}, observed mean {obs:.2f}, "
               f"deviance {dev_tot:.1f} (reference chi2 5% = {chi2_95}).")
    if arm == "VISIBLE_GLOBAL":
        return rows, notice, meta

    # VISIBLE_ESTRUCTURADO: signed deviance residuals per speed cell over ALL
    # logged lots, in speed order (compuerta C: no ranking, no labels).
    cells = _bought_cells(srv, pole, params, pilots_done + [{"speed": ctl["speed"], "rows": rows}])
    table = pd.DataFrame([{
        "speed": c["speed"], "n_lots": c["n"], "observed_mean": round(c["mean"], 3),
        "model_mean": round(float(np.asarray(model_fn(C._DictRegime({"speed": c["speed"]}),
                                                      4000, 778)["y"], float).mean()), 3),
    } for c in cells])
    table["deviance_residual"] = [
        round(_deviance(r.observed_mean, r.n_lots, r.model_mean), 2)
        for r in table.itertuples()]
    notice += (" A standard calibration table for your registered model over all logged "
               "lots is attached as dataframe `pilot_%d_report` (speed order)." % which)
    return rows, notice, {**meta, "report_table": table.to_dict("records")}, table  # type: ignore[return-value]


# ----------------------------------------------------------------- episode loop
def run_impasse_episode(srv, pole: str, params: dict, arm: str, model: str) -> dict:
    chat = FoundryChat(system=SYSTEM + REGISTER_DOC, model=model,
                       max_completion_tokens=MAX_COMPLETION_TOKENS)
    sheet = srv.describe()
    prompt = ("Here is the brief:\n\n" + sheet["brief"]
              + "\n\nMachine-readable sheet:\n"
              + json.dumps({k: v for k, v in sheet.items() if k != "brief"}, indent=2)
              + "\n\nReason briefly about your opening plan, then write your first cell. "
                "`env` is already in the namespace.")

    trace: list[dict] = []
    chain: list[dict] = []
    pilots_done: list[dict] = []
    abort_reason = "max_turns"
    tokens = 0

    with KernelClient(srv, cell_timeout_s=CELL_TIMEOUT_S) as kernel:
        for turn_idx in range(1, MAX_TURNS + 1):
            srv.begin_turn(turn_idx)

            for which, pturn in ((1, PILOT1_TURN), (2, PILOT2_TURN)):
                if turn_idx == pturn:
                    made = make_pilot(srv, pole, params, which, arm, pilots_done)
                    rows, notice, meta = made[0], made[1], made[2]
                    kernel.inject_dataframe(f"pilot_{which}", rows)
                    if len(made) == 4:
                        kernel.inject_dataframe(f"pilot_{which}_report", made[3])
                    prompt = f"[NOTICE] {notice}\n\n" + prompt
                    pilots_done.append({"speed": meta["speed"], "rows": rows,
                                        "turn": turn_idx})
                    chain.append({"event": f"pilot_{which}", "turn": turn_idx, **{
                        k: v for k, v in meta.items() if k != "report_table"}})

            regs_before = len(getattr(srv, "_impasse_regs", []))
            reply = chat.ask(prompt)
            tokens += getattr(reply, "total_tokens", 0) or 0
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

            for i in range(regs_before, len(getattr(srv, "_impasse_regs", []))):
                chain.append({"event": "register", "turn": turn_idx,
                              "version": i + 1})

            if srv.result is not None:
                abort_reason = "submitted"
                chain.append({"event": "submit", "turn": turn_idx})
                break
            if tokens > MAX_TOKENS:
                abort_reason = "token_budget"
                break
            prompt = ("Kernel output:\n" + (rec["stdout"] or "(no output)")
                      + "\n\nContinue: reasoning first, then ONE cell.")

    return {"trace": trace, "chain": chain, "abort_reason": abort_reason,
            "tokens": tokens,
            "accepted": bool(srv.result and srv.result.get("accepted", True)),
            "R": (srv.result or {}).get("R"),
            "budget_spent": float(getattr(srv, "spent", 0.0) or 0.0),
            "submission_code": (srv.result or {}).get("code") or getattr(srv, "submission_code", None),
            "registrations": list(getattr(srv, "_impasse_regs", []))}


# ----------------------------------------------------------------- outcomes
def structural_class(code: str | None, params: dict) -> dict:
    """Mechanical family classifier of a delivered/registered model: does its
    OWN curve carry a slope break in-range? Requires an ABSOLUTE effect floor
    (a pure power law yields near-zero SSEs and the gain ratio alone is noise).
    Zero-LLM."""
    if not code:
        return {"family": "none"}
    try:
        ns: dict = {}
        exec(compile(code, "<m>", "exec"), ns)
        prog = ns["model"]
        grid = np.asarray(C.DENSE_GRID[::2], float)
        lam = C.program_curve(prog, grid, n=2000, seed=999)
        nn = np.full(len(grid), 2000.0)
        rg = C.fit_regime_family(grid, lam, nn)
        smooth_pred = C._predict_logpoly(C._fit_logpoly(grid, lam, 2), grid)
        sse_smooth = float(np.sum(nn * (lam - smooth_pred) ** 2 / np.maximum(smooth_pred, 1e-9)))
        sse_regime = float(rg.get("sse", np.inf))
        is_regime = (np.isfinite(sse_regime)
                     and sse_regime < 0.5 * max(sse_smooth, 1e-9)
                     and rg.get("delta1", 0.0) >= 8.0
                     and 1.05 < rg.get("s_star", 0.0) < 1.39)
        return {"family": "regime" if is_regime else "smooth",
                "delta1_hat": rg.get("delta1"), "sstar_hat": rg.get("s_star"),
                "sse_regime": sse_regime, "sse_smooth": sse_smooth}
    except Exception as e:
        return {"family": "error", "error": repr(e)}


def timing_outcome(srv, ep: dict, pole: str, params: dict) -> dict:
    """Outcome primario pre-registrado: candidata de familia regime registrada
    ANTES del punto de discriminacion (dBIC>=6 con la evidencia que el agente
    tenia EN ESE MOMENTO). Server-side, cero-LLM."""
    pilots = [{"speed": c["speed"], "turn": c["turn"],
               "rows": pd.DataFrame({"y": []})} for c in ep["chain"]
              if c["event"].startswith("pilot")]
    # pilot rows for gap computation come from the captured chain meta (mean/n)
    pilot_cells = [{"speed": c["speed"], "mean": c.get("observed_mean"),
                    "n": c["n"], "turn": c["turn"]} for c in ep["chain"]
                   if c["event"].startswith("pilot")]

    def gap_at(turn: int) -> float | None:
        cells = _bought_cells(srv, pole, params, [], up_to_turn=turn)
        extras = [{"speed": c["speed"], "mean": c["mean"], "n": float(c["n"])}
                  for c in cells]
        extras += [{"speed": p["speed"], "mean": p["mean"], "n": float(p["n"])}
                   for p in pilot_cells if p["turn"] <= turn and p["mean"] is not None]
        if len(extras) < 5:
            return None
        try:
            return float(C.discrimination_gap([], extras))
        except Exception:
            return None

    events = [{"turn": r["turn"], "code": r["code"], "kind": "register"}
              for r in ep["registrations"]]
    if ep.get("submission_code"):
        sub_turn = max((c["turn"] for c in ep["chain"] if c["event"] == "submit"),
                       default=99)
        events.append({"turn": sub_turn, "code": ep["submission_code"], "kind": "submit"})

    first_regime = None
    for ev in sorted(events, key=lambda e: e["turn"]):
        if structural_class(ev["code"], params)["family"] == "regime":
            first_regime = ev
            break
    if first_regime is None:
        return {"first_regime_event": None, "expansion_generativa": False}
    g = gap_at(first_regime["turn"])
    return {"first_regime_event": {"turn": first_regime["turn"],
                                   "kind": first_regime["kind"]},
            "dbic_gap_at_event": g,
            "expansion_generativa": bool(g is None or g < C.NODICT_MAX_DBIC)}


def score(code: str | None, pole: str, params: dict) -> dict:
    if not code:
        return {"scored": False, "reason": "no delivered code"}
    try:
        ns: dict = {}
        exec(code, ns)
        prog = ns["model"]
    except Exception as e:
        return {"scored": False, "reason": f"delivered code failed locally: {e!r}"}
    out: dict = {"scored": True}
    if pole == "brk":
        out.update(C.s_quiebre(prog, params))
        out["F_mean"] = C.f_mean(prog, params, "brk")
    else:
        out.update(C.s_clean(prog, params))
        out["espurio"] = C.spurious_break_flag(prog, params)
    out["structural"] = structural_class(code, params)
    return out


# ----------------------------------------------------------------- cells
def run_cell(arm: str, pole: str, seed: int, params: dict, tag: str) -> dict:
    srv = build_world_server(ROOT / "cases" / POLES[pole], seed_offset=seed)
    attach_register(srv)
    run_at = datetime.now().isoformat(timespec="seconds")
    t0 = time.time()
    ep = run_impasse_episode(srv, pole, params, arm, MODEL)
    wall = time.time() - t0
    code = ep.get("submission_code")
    payload = {
        "tag": tag, "model": MODEL, "pole": pole, "arm": arm, "seed": seed,
        "case_id": POLES[pole], "run_at": run_at,
        "abort_reason": ep["abort_reason"], "turns": len(ep["trace"]),
        "accepted": ep["accepted"], "R": ep["R"], "tokens": ep["tokens"],
        "wall_s": round(wall, 1), "budget_spent": ep["budget_spent"],
        "chain": ep["chain"],
        "n_registrations": len(ep["registrations"]),
        "registered_codes": [r["code"] for r in ep["registrations"]],
        "delivered_code": code,
        "instruments": score(code, pole, params),
        "timing": timing_outcome(srv, ep, pole, params),
        "episode": {k: v for k, v in ep.items() if k != "registrations"},
    }
    OUT.mkdir(parents=True, exist_ok=True)
    path = OUT / f"{tag}__{MODEL}__{pole}__{arm}__{seed}.json"
    path.write_text(json.dumps(payload, indent=1, default=str))
    ins = payload["instruments"]
    key = "S_quiebre_fuerte" if pole == "brk" else "S_clean"
    print(f"[{tag}] {arm} {pole} seed={seed}: abort={payload['abort_reason']} "
          f"turns={payload['turns']} regs={payload['n_registrations']} "
          f"{key}={ins.get(key) if not ins.get(key) else round(ins.get(key), 3)} "
          f"expansion={payload['timing']['expansion_generativa']} -> {path.name}")
    return payload


def tanda_cells() -> list[tuple[str, str, int]]:
    cells = []
    for i, seed in enumerate(TANDA_BRK_SEEDS):
        cells.append((ARMS[i % 3], "brk", seed))
    cells += [("RAW", "smooth", TANDA_SMOOTH_SEEDS[0]),
              ("RAW", "smooth", TANDA_SMOOTH_SEEDS[1]),
              ("VISIBLE_ESTRUCTURADO", "smooth", TANDA_SMOOTH_SEEDS[2]),
              ("VISIBLE_ESTRUCTURADO", "smooth", TANDA_SMOOTH_SEEDS[3])]
    return cells


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("mode", choices=["tecnico", "tanda"])
    ap.add_argument("--only", type=int, default=None)
    args = ap.parse_args()
    params = C.load_instance()["params"]
    if args.mode == "tecnico":
        run_cell("VISIBLE_ESTRUCTURADO", "brk", TEC_SEED, params, "tecnico")
        return 0
    cells = tanda_cells() if args.only is None else [tanda_cells()[args.only]]
    for arm, pole, seed in cells:
        run_cell(arm, pole, seed, params, "v1_impasse")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
