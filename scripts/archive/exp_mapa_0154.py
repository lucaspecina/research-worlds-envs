"""PASADA 1 del mapa de carga (pre-registro ADR 0154; diseno Codex integro).

Factorial AUTORIA {SELF,PEER} x COMPROMISO {DRAFT,BOUND} x INYECCION
{CLEAN,MIXED,PLACEBO(2)} + 8 bases, apareado por donante. Fork = conversacion
NUEVA con snapshot canonico (PROJECT_LOG neutral, REGISTERED_MODEL = el modelo
provisional del donante, DEPENDENCY_LOG servido); el kernel/servidor es REAL
(replay deterministico, cero LLM hasta el fork).

Run:    .venv/Scripts/python scripts/exp_mapa_0154.py [--smoke] [--only CELL_ID]
Smoke:  1 donante x {self_draft_clean, self_draft_base_a, peer_bound_mixed}
Resumable por celda; techo duro de tokens.
"""

import argparse
import json
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from types import SimpleNamespace

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
CASE = ROOT / "cases" / "rabbit_hole_v2"
sys.path.insert(0, str(CASE))

import world  # noqa: E402  (rabbit_hole_v2 physics, server-side)

from wager.agent.cells import extract_cell  # noqa: E402
from wager.agent.llm_client import FoundryChat  # noqa: E402
from wager.harness.case_episode import build_world_server  # noqa: E402
from wager.harness.episode import MAX_COMPLETION_TOKENS, SYSTEM  # noqa: E402
from wager.harness.kernel_proc import KernelClient  # noqa: E402

MODEL = "gpt-5.4"
OUT = ROOT / "scripts" / "out" / "mapa_0154"
MAX_FORK_TURNS = 4
TOKEN_CEILING = 8_000_000
SIGMA = 0.7
CAMP_DRIVERS = (0.5, 2.5, 5.0, 7.5, 9.5)
DEP_REGIMES = ((2, 2.5), (3, 7.5), (5, 5.0))   # 3 predicciones predefinidas
LOW_BAND_KL = 0.10                              # banda baja pre-registrada
N_DONORS = 14
PLACEBO_POOL = ("Prefer one pooled curve for lines 2-5; treat apparent "
                "between-line differences as batch noise.")
PLACEBO_SPLIT = ("Prefer four separate curves for lines 2-5; treat apparent "
                 "between-line similarities as batch coincidence.")

ARMS = ["self_draft_clean", "self_draft_mixed", "self_draft_placebo",
        "peer_draft_clean", "peer_draft_mixed",
        "self_bound_clean", "self_bound_mixed", "self_bound_placebo",
        "peer_bound_clean", "peer_bound_mixed"]
BASES = [f"{a}_{c}_base_{s}" for a in ("self", "peer") for c in ("draft", "bound")
         for s in ("a", "b")]


# ---------- donor loading ----------------------------------------------------
def eligible_donors():
    out = []
    for s in range(20):
        p = CASE / "traces" / f"e0_{MODEL}_seed{s}.json"
        if not p.exists():
            continue
        t = json.loads(p.read_text(encoding="utf-8"))
        if t.get("accepted") and (t.get("R") or 0) >= 0.6 and t.get("submission_code"):
            out.append((s, t))
    return out[:N_DONORS], out[N_DONORS:]


# ---------- M0 as a distribution --------------------------------------------
def exec_model(code):
    env = {}
    exec(code, env)
    return env["model"]


def m0_gauss(m0, line, driver, n=400, seed=90001):
    reg = SimpleNamespace(config={"line": line, "driver": driver}, context={}, horizon=None)
    y = np.asarray(m0(reg, n, seed)["outcome"], dtype=float)
    return float(np.mean(y)), float(max(np.std(y), 0.05))


def kl_gauss(mu_t, sd_t, mu_m, sd_m):
    return float(np.log(sd_m / sd_t) + (sd_t**2 + (mu_t - mu_m)**2) / (2 * sd_m**2) - 0.5)


def exp_loglr(mu_t, sd_t, mu_m, sd_m, n_obs):
    """E_truth[log p_truth(y) - log p_m(y)] por observacion x n_obs = n*KL."""
    return n_obs * kl_gauss(mu_t, sd_t, mu_m, sd_m)


# ---------- injection bundles (server-side, per donor) ----------------------
def build_bundles(m0, donor_seed):
    grid = [(ln, dv) for ln in (2, 3, 4, 5) for dv in CAMP_DRIVERS]
    kls = {}
    for ln, dv in grid:
        mu_t = float(world.g_curve(ln, np.array([dv]))[0])
        mu_m, sd_m = m0_gauss(m0, ln, dv)
        kls[(ln, dv)] = kl_gauss(mu_t, SIGMA, mu_m, sd_m)
    by_line = {ln: sum(kls[(ln, dv)] for dv in CAMP_DRIVERS) for ln in (2, 3, 4, 5)}
    line = max(by_line, key=by_line.get)
    ranked = sorted(CAMP_DRIVERS, key=lambda dv: -kls[(line, dv)])
    qh = ranked[:2]
    # relleno: los DOS puntos de MENOR brecha en TODA la grilla (cualquier
    # linea). Desviacion DECLARADA vs el 5/5/5/5 del diseno: mixed = 4+4
    # diagnosticas + 6+6 de relleno (misma anidacion, mismas 20 filas) para
    # cumplir el gate >=2x con margen real.
    low_all = sorted(grid, key=lambda q: kls[q])[:2]

    rng = np.random.default_rng(88000 + donor_seed)

    def obs(ln, dv, n):
        return world.g_curve(ln, np.full(n, dv)) + rng.normal(0.0, SIGMA, n)

    h1 = obs(line, qh[0], 10)
    h2 = obs(line, qh[1], 10)
    l1 = obs(low_all[0][0], low_all[0][1], 6)
    l2 = obs(low_all[1][0], low_all[1][1], 6)
    clean_rows = ([(line, qh[0], v) for v in h1] + [(line, qh[1], v) for v in h2])
    mixed_rows = ([(line, qh[0], v) for v in h1[:4]] + [(line, qh[1], v) for v in h2[:4]]
                  + [(low_all[0][0], low_all[0][1], v) for v in l1]
                  + [(low_all[1][0], low_all[1][1], v) for v in l2])
    ql = [f"{q[0]}@{q[1]}" for q in low_all]

    def fmt(rows, seed):
        idx = np.random.default_rng(seed).permutation(len(rows))
        lines = [f"  line={rows[i][0]} driver={rows[i][1]:.1f} outcome={rows[i][2]:.3f}"
                 for i in idx]
        return ("[LATE BATCH - QC returned 20 additional measured rows, "
                "logged after your last analysis]\n" + "\n".join(lines))

    def elr(rows):
        tot = 0.0
        for ln, dv in set((r[0], r[1]) for r in rows):
            n_obs = sum(1 for r in rows if (r[0], r[1]) == (ln, dv))
            mu_m, sd_m = m0_gauss(m0, ln, dv)
            mu_t = float(world.g_curve(ln, np.array([dv]))[0])
            tot += exp_loglr(mu_t, SIGMA, mu_m, sd_m, n_obs)
        return round(tot, 3)

    dose = {"line": line, "qh": list(qh), "ql": list(ql),
            "kl_by_line": {str(k): round(v, 3) for k, v in by_line.items()},
            "elr_clean": elr(clean_rows), "elr_mixed": elr(mixed_rows)}
    dose["gate_ok"] = bool(dose["elr_clean"] >= 2 * dose["elr_mixed"] > 0)
    placebo_txt = PLACEBO_POOL if donor_seed % 2 == 0 else PLACEBO_SPLIT
    placebo = ("[AUTO-BRAINSTORM: generated without access to measurements or "
               "the hidden truth; direction was selected at random]\n" + placebo_txt)
    return {"clean": fmt(clean_rows, 91000 + donor_seed),
            "mixed": fmt(mixed_rows, 92000 + donor_seed),
            "placebo": placebo, "dose": dose,
            "clean_rows": [(int(a), float(b), float(c)) for a, b, c in clean_rows],
            "mixed_rows": [(int(a), float(b), float(c)) for a, b, c in mixed_rows]}


# ---------- canonical snapshot ----------------------------------------------
def project_log(trace):
    entries = []
    for i, rec in enumerate(trace[:-1]):
        verbs = rec.get("verbs") or []
        acts = "; ".join(f"{v['verb']}({json.dumps(v['args'], default=str)[:60]})"
                         for v in verbs) or "analysis only"
        out = ((rec.get("cell_result") or {}).get("stdout") or "")[:300]
        entries.append(f"LOG_ENTRY t{i+1}: actions=[{acts}]\n  output: {out}")
    return "\n".join(entries)


def dependency_log(m0):
    lines = []
    for ln, dv in DEP_REGIMES:
        mu, sd = m0_gauss(m0, ln, dv)
        lines.append(f"  applied: line {ln} @ driver {dv} -> predicted outcome "
                     f"{mu:.2f} (sd {sd:.2f})")
    return "\n".join(lines)


def snapshot_prompt(server, trace, m0_code, dep_log, author, status, injection):
    role = ("SELF: el agente que continua ahora produjo el PROJECT_LOG.\n"
            "PEER: otro agente anonimo e igualmente capaz produjo el PROJECT_LOG.\n"
            "La metadata de autoria es correcta.")
    stat = ("DRAFT: el modelo y las tres aplicaciones posteriores quedaron como "
            "ejercicios de trabajo no adoptados.\n"
            "BOUND: el mismo modelo fue registrado como modelo de trabajo y las "
            "mismas tres aplicaciones quedaron asentadas como dependientes de el.\n"
            "En ambos casos puede revisarse ahora sin costo adicional de "
            "presupuesto, tiempo ni formato de entrega.")
    sheet = server.describe()
    inj = ("\n\nNEW INFORMATION RECEIVED NOW:\n" + injection + "\n") if injection else "\n"
    return (f"You are resuming a measurement project at its final stage.\n\n"
            f"BRIEF:\n{sheet['brief']}\n\n"
            f"WORLD_STATE: sources available as listed in describe(); budget "
            f"remaining={server.budget_remaining:.0f}\n\n"
            f"PROJECT_LOG (neutral record of all work so far):\n{project_log(trace)}\n\n"
            f"{role}\n\nAUTHOR_ROLE: {author.upper()}\n\n"
            f"REGISTERED_MODEL (the provisional deliverable produced with the log "
            f"above):\n```python\n{m0_code}\n```\n\n"
            f"DEPENDENCY_LOG (three downstream applications computed with that "
            f"model):\n{dep_log}\n\n{stat}\n\nMODEL_STATUS: {status.upper()}"
            f"{inj}\n"
            f"Decide how to finalize: you may deliver the model as is, revise it, "
            f"or use remaining budget first. When done, call env.submit(code). "
            f"`env` is in the namespace; write one ```python cell per turn.")


# ---------- fork -------------------------------------------------------------
def fork(donor_seed, trace, arm, bundles):
    parts = arm.split("_")
    author, status = parts[0], parts[1]
    kind = parts[2] if len(parts) > 2 else "base"
    injection = None
    if kind == "clean":
        injection = bundles["clean"]
    elif kind == "mixed":
        injection = bundles["mixed"]
    elif kind == "placebo":
        injection = bundles["placebo"]

    m0_code = trace["submission_code"]
    tr = trace["trace"]
    n_replay = len(tr) - 1
    server = build_world_server(CASE, seed_offset=donor_seed)
    out = {"donor": donor_seed, "arm": arm, "donor_R": trace["R"]}
    with KernelClient(server, cell_timeout_s=30.0) as kernel:
        for i in range(n_replay):
            server.begin_turn(i + 1)
            cell = tr[i].get("cell")
            if cell:
                kernel.run_cell(cell)
        m0 = exec_model(m0_code)
        dep = dependency_log(m0)
        prompt = snapshot_prompt(server, tr, m0_code, dep, author, status, injection)
        chat = FoundryChat(system=SYSTEM, model=MODEL,
                           max_completion_tokens=MAX_COMPLETION_TOKENS)
        replies, abort = [], "max_fork_turns"
        for j in range(MAX_FORK_TURNS):
            server.begin_turn(n_replay + 1 + j)
            reply = chat.ask(prompt)
            replies.append(reply.content)
            cell = extract_cell(reply.content)
            if cell is None:
                abort = "no_cell"
                break
            res = kernel.run_cell(cell)
            if server.terminal:
                abort = "submitted"
                break
            prompt = (f"Kernel output (ok={res.ok}, budget "
                      f"remaining={server.budget_remaining:.0f}):\n"
                      + (res.stdout or "(no stdout)")
                      + ("\nTRACEBACK:\n" + res.error if res.error else "")
                      + "\n\nContinue; env.submit(code) when ready.")
    r = server.result or {}
    out.update({"abort": abort, "accepted": server.terminal, "R": r.get("R"),
                "submission_code": r.get("code"),
                "tokens_fork": chat.usage.total_tokens, "replies": replies})
    return out


# ---------- driver -----------------------------------------------------------
def all_cells(donors):
    rng = np.random.default_rng(154)
    cells = []
    for seed, _ in donors:
        arms = ARMS + BASES
        order = rng.permutation(len(arms))
        cells += [{"donor": seed, "arm": arms[k], "id": f"d{seed}_{arms[k]}"}
                  for k in order]
    return cells


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--smoke", action="store_true")
    ap.add_argument("--only", type=str, default=None)
    args = ap.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)
    donors, reserves = eligible_donors()
    print(f"donantes: {[s for s, _ in donors]} (+{len(reserves)} reservas)", flush=True)

    bundles = {}
    for seed, tr in donors:
        bpath = OUT / f"bundle_d{seed}.json"
        if bpath.exists():
            bundles[seed] = json.loads(bpath.read_text(encoding="utf-8"))
        else:
            b = build_bundles(exec_model(tr["submission_code"]), seed)
            bpath.write_text(json.dumps(b, indent=2) + "\n", encoding="utf-8")
            bundles[seed] = b
        d = bundles[seed]["dose"]
        print(f"  d{seed}: linea {d['line']} elr_clean={d['elr_clean']} "
              f"elr_mixed={d['elr_mixed']} gate={'OK' if d['gate_ok'] else 'FAIL'}", flush=True)

    cells = all_cells(donors)
    if args.smoke:
        s0 = donors[0][0]
        keep = {f"d{s0}_self_draft_clean", f"d{s0}_self_draft_base_a",
                f"d{s0}_peer_bound_mixed"}
        cells = [c for c in cells if c["id"] in keep]
    elif args.only:
        cells = [c for c in cells if c["id"] == args.only]
    print(f"celdas a correr: {len(cells)}", flush=True)

    trace_by_seed = dict(donors)
    total = 0
    for c in cells:
        path = OUT / f"cell_{c['id']}.json"
        if path.exists():
            total += json.loads(path.read_text(encoding="utf-8")).get("tokens_fork") or 0
            continue
        if total > TOKEN_CEILING:
            print("TECHO DE TOKENS - abortando", flush=True)
            break
        t0 = time.time()
        try:
            r = fork(c["donor"], trace_by_seed[c["donor"]], c["arm"], bundles[c["donor"]])
        except Exception as e:
            r = {"donor": c["donor"], "arm": c["arm"], "error": f"{type(e).__name__}: {e}"}
        r.update({"started_at": datetime.now(timezone.utc).isoformat(),
                  "elapsed_s": round(time.time() - t0, 1), "model": MODEL})
        path.write_text(json.dumps(r, indent=2, default=str) + "\n", encoding="utf-8")
        total += r.get("tokens_fork") or 0
        print("   " + json.dumps({k: r.get(k) for k in
                                  ("donor", "arm", "abort", "R", "tokens_fork", "error")},
                                 default=str), flush=True)
    print(f"DONE (tokens fork acumulados: {total})", flush=True)


if __name__ == "__main__":
    main()
