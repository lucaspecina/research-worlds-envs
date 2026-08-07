"""Smoke runner for the count_regime pair (mundo 2, ficha 2026-08-07).

Modes:
  tecnico  1 episodio real barato (gpt-5.4, seed 99490, polo brk)
  tanda    2 modelos x 2 polos x 3 seeds (99500-99511), SIN ayuda
           (--only N corre una celda: util para paralelizar)

Salida: scripts/out/count_regime_smoke/<tag>__<model>__<pole>__<seed>.json con
el payload estandar de episodios (mismo esquema que count_mix_smoke).
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from datetime import datetime
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from cases.count_regime_v0_common import (  # noqa: E402
    _DictRegime, f_mean, load_instance, program_functionals, s_clean,
    s_quiebre, spurious_break_flag,
)
from wager.harness.case_episode import build_world_server  # noqa: E402
from wager.harness.episode import run_episode  # noqa: E402

OUT = ROOT / "scripts/out/count_regime_smoke"
POLES = {"brk": "count_regime_v0", "smooth": "count_regime_twin_v0"}
MODELS = ("DeepSeek-V3.2", "gpt-5.4")
TEC_SEED = 99490

TANDA = ([("DeepSeek-V3.2", "brk", s) for s in (99500, 99501, 99502)]
         + [("gpt-5.4", "brk", s) for s in (99503, 99504, 99505)]
         + [("DeepSeek-V3.2", "smooth", s) for s in (99506, 99507, 99508)]
         + [("gpt-5.4", "smooth", s) for s in (99509, 99510, 99511)])


def _score(code: str | None, pole: str, params: dict) -> dict:
    if not code:
        return {"scored": False, "reason": "no delivered code"}
    ns: dict = {}
    try:
        exec(code, ns)
        prog = ns["model"]
        f = program_functionals(prog, params)
    except Exception as e:  # pragma: no cover
        return {"scored": False, "reason": f"delivered code failed locally: {e!r}"}
    out: dict = {"scored": True, "functionals": f}
    if pole == "brk":
        out.update(s_quiebre(prog, params))
        out["F_mean"] = f_mean(prog, params, "brk")
    else:
        out.update(s_clean(prog, params))
        out["espurio"] = spurious_break_flag(prog, params)
    return out


def _shopping_signature(trace: list[dict]) -> dict:
    speeds: set[float] = set()
    experiments = 0
    observed_rows = 0
    for turn in trace:
        for v in turn.get("verbs", []):
            if v.get("verb") == "experiment":
                experiments += 1
                cfg = (v.get("args") or {}).get("config") or {}
                if "speed" in cfg:
                    speeds.add(round(float(cfg["speed"]), 3))
            elif v.get("verb") == "observe":
                observed_rows += int((v.get("args") or {}).get("n") or 0)
    interior_high = sorted(s for s in speeds if 1.0 < s < 1.2)
    return {"experiments": experiments, "observed_rows": observed_rows,
            "speeds": sorted(speeds), "n_speeds": len(speeds),
            "bought_interior_high": bool(interior_high),
            "interior_high_speeds": interior_high}


def run_cell(model: str, pole: str, seed: int, params: dict, tag: str) -> dict:
    srv = build_world_server(ROOT / "cases" / POLES[pole], seed_offset=seed)
    brief_snapshot = srv.describe().get("brief", "")
    run_at = datetime.now().isoformat(timespec="seconds")
    t0 = time.time()
    ep = run_episode(srv, model=model, initial_note="")
    wall = time.time() - t0
    code = ep.get("submission_code")
    payload = {
        "tag": tag, "model": model, "pole": pole, "seed": seed,
        "case_id": POLES[pole], "run_at": run_at,
        "initial_note": "", "brief": brief_snapshot,
        "ayuda_label": "no",
        "abort_reason": ep.get("abort_reason"),
        "turns": len(ep.get("trace", [])),
        "accepted": ep.get("accepted"), "R": ep.get("R"),
        "tokens": ep.get("tokens"),
        "wall_s": round(wall, 1),
        "budget_spent": float(ep.get("budget_spent", 0.0)),
        "shopping": _shopping_signature(ep.get("trace", [])),
        "delivered_code": code,
        "instruments": _score(code, pole, params),
        "episode": ep,
    }
    OUT.mkdir(parents=True, exist_ok=True)
    path = OUT / f"{tag}__{model}__{pole}__{seed}.json"
    path.write_text(json.dumps(payload, indent=1, default=str))
    ins = payload["instruments"]
    key = "S_quiebre_fuerte" if pole == "brk" else "S_clean"
    val = ins.get(key)
    print(f"[{tag}] {model} {pole} seed={seed}: abort={payload['abort_reason']} "
          f"turns={payload['turns']} spent={payload['budget_spent']:.0f} "
          f"{key}={val if val is None else round(val, 3)} "
          f"speeds={payload['shopping']['speeds']} -> {path.name}")
    return payload


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("mode", choices=["tecnico", "tanda"])
    ap.add_argument("--only", type=int, default=None)
    args = ap.parse_args()
    params = load_instance()["params"]
    if args.mode == "tecnico":
        run_cell("gpt-5.4", "brk", TEC_SEED, params, "tecnico")
        return 0
    cells = TANDA if args.only is None else [TANDA[args.only]]
    for model, pole, seed in cells:
        run_cell(model, pole, seed, params, "v0_principal")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
