"""Paso 5 del slice de saltos: smoke con agentes reales sobre el par count_mix.

Ficha congelada: docs/research/2026-08-06-ficha-mundo-count-mix-v0.md
  - episodio TECNICO primero (seed 99290; sin lectura conductual)
  - brazo principal: {DeepSeek-V3.2, gpt-5.4} x {mix, single} x seeds 99300-99311
  - techo USD 50; censura por interfaz se reporta, jamas se re-rollea

Uso:
  python scripts/run_count_mix_smoke_v0.py tecnico
  python scripts/run_count_mix_smoke_v0.py main            # las 12 celdas
  python scripts/run_count_mix_smoke_v0.py main --only i   # una celda (0-11)

Salida: scripts/out/count_mix_smoke/<arm>__<model>__<pole>__<seed>.json con
trace completa + codigo entregado + instrumentos (S_struct/F_mean o
S_clean/espurio) computados cero-LLM. La lectura conductual agregada NO la hace
este script: eso es la autopsia (ficha §7).
"""

from __future__ import annotations

import argparse
import json
from datetime import datetime
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import numpy as np  # noqa: E402

from cases.count_mix_v0_common import (  # noqa: E402
    _DictRegime, forced_mix_program, load_instance, program_functionals,
    s_clean, s_struct, s_valley, single_baseline_program,
    spurious_mixture_flag, strong_baseline_program,
)
from wager.harness.case_episode import build_world_server  # noqa: E402
from wager.harness.episode import run_episode  # noqa: E402

OUT = ROOT / "scripts/out/count_mix_smoke"
POLES = {"mix": "count_mix_v0", "single": "count_mix_twin_v0"}
MODELS = ("DeepSeek-V3.2", "gpt-5.4")
MAIN_SEEDS = list(range(99300, 99312))          # 12, orden fijo de la ficha
TEC_SEED = 99290
PISTA = "Nota del encargo: consider\u00e1 que los datos pueden venir de m\u00e1s de una subpoblaci\u00f3n."
PISTA_CELLS = [("DeepSeek-V3.2", "mix", 99350), ("DeepSeek-V3.2", "mix", 99351),
               ("gpt-5.4", "mix", 99352), ("gpt-5.4", "mix", 99353),
               ("DeepSeek-V3.2", "single", 99354), ("DeepSeek-V3.2", "single", 99355),
               ("gpt-5.4", "single", 99356), ("gpt-5.4", "single", 99357)]

# --- escalera v0.2 (ficha addendum 2026-08-07; frases CONGELADAS) -----------
NIVEL3 = "Nota del encargo: considerá la posibilidad de que los lotes vengan en unos pocos tipos distintos."
NIVEL4 = "Nota del encargo: considerá probar un modelo de mezcla finita: 2 o 3 grupos de lotes, cada grupo con su propia tasa."
ESCALERA_CELLS = (
    [("nivel0", "", "DeepSeek-V3.2", "mix", s) for s in (99360, 99361)]
    + [("nivel0", "", "gpt-5.4", "mix", s) for s in (99362, 99363)]
    + [("nivel3", NIVEL3, "DeepSeek-V3.2", "mix", s) for s in (99364, 99365)]
    + [("nivel3", NIVEL3, "gpt-5.4", "mix", s) for s in (99366, 99367)]
    + [("nivel4", NIVEL4, "DeepSeek-V3.2", "mix", s) for s in (99368, 99369)]
    + [("nivel4", NIVEL4, "gpt-5.4", "mix", s) for s in (99370, 99371)]
    + [("nivel3", NIVEL3, "DeepSeek-V3.2", "single", 99372), ("nivel3", NIVEL3, "gpt-5.4", "single", 99373),
       ("nivel4", NIVEL4, "DeepSeek-V3.2", "single", 99374), ("nivel4", NIVEL4, "gpt-5.4", "single", 99375)]
)
TEC_MODEL = "DeepSeek-V3.2"                     # tecnico barato con sujeto real

# celdas del brazo principal en orden fijo: (model, pole, seed)
MAIN_CELLS = [(MODELS[(i // 3) % 2], ("mix" if i < 6 else "single"), MAIN_SEEDS[i])
              for i in range(12)]
# -> DeepSeek mix x3, gpt mix x3, DeepSeek single x3, gpt single x3


def _instruments():
    inst = load_instance()
    from cases.count_mix_v0_common import _sample_counts
    params, geo, tail_at = inst["params"], inst["geometry"], inst["tail_at"]

    def t_mix(regime, n, seed):
        return _sample_counts("mix", params, regime, n, seed)

    def t_single(regime, n, seed):
        return _sample_counts("single", params, regime, n, seed)

    truth_f = program_functionals(t_mix, geo, tail_at)
    single_truth_f = program_functionals(t_single, geo, tail_at)
    y_train = t_mix(_DictRegime({"speed": 1.0}), inst["witness_n"],
                    inst["witness_sample_seed"])["y"].to_numpy(float)
    base_prog, _ = single_baseline_program(y_train)
    base_f = program_functionals(base_prog, geo, tail_at)
    strong_f = program_functionals(strong_baseline_program(y_train), geo, tail_at)
    forced_f = program_functionals(forced_mix_program(params["lam0"]), geo, tail_at)
    return {"geo": geo, "tail_at": tail_at, "truth_f": truth_f,
            "single_truth_f": single_truth_f, "base_f": base_f,
            "strong_f": strong_f, "forced_f": forced_f}


def _score(code: str | None, pole: str, ins) -> dict:
    if not code:
        return {"scored": False, "reason": "no delivered code"}
    ns: dict = {}
    try:
        exec(code, ns)  # server-side re-execution of the DELIVERED code
        prog = ns["model"]
        f = program_functionals(prog, ins["geo"], ins["tail_at"])
    except Exception as e:  # pragma: no cover
        return {"scored": False, "reason": f"delivered code failed locally: {e!r}"}
    out: dict = {"scored": True, "functionals": f}
    if pole == "mix":
        out.update(s_struct(f, ins["truth_f"], ins["base_f"]))
        out["S_valley_fuerte"] = s_valley(f, ins["truth_f"], ins["strong_f"])
        out["F_mean"] = float(np.clip(
            1 - abs(f["mean"] - ins["truth_f"]["mean"]) / ins["truth_f"]["mean"], 0, 1))
    else:
        out.update(s_clean(f, ins["single_truth_f"], ins["forced_f"]))
        y_model = prog(_DictRegime({"speed": 1.0}), 2000, 777)["y"].to_numpy(float)
        out["espurio"] = spurious_mixture_flag(f, ins["single_truth_f"], y_model)
    return out


def _shopping_signature(trace: list[dict]) -> dict:
    bought_repeats = False
    repeats_turn = None
    experiments = 0
    observed_rows = 0
    for rec in trace:
        for v in rec.get("verbs", []):
            if v["verb"] == "experiment":
                experiments += 1
                cfg = (v.get("args") or {}).get("config") or {}
                if float(cfg.get("repeats_per_unit", 1)) > 1 and not bought_repeats:
                    bought_repeats = True
                    repeats_turn = rec["turn"]
            if v["verb"] == "observe":
                observed_rows += int((v.get("args") or {}).get("n", 0))
    return {"bought_repeats": bought_repeats, "repeats_turn": repeats_turn,
            "experiments": experiments, "observed_rows": observed_rows}


def run_cell(model: str, pole: str, seed: int, ins, tag: str, initial_note: str = "") -> dict:
    srv = build_world_server(ROOT / "cases" / POLES[pole], seed_offset=seed)
    brief_snapshot = srv.describe().get("brief", "")
    run_at = datetime.now().isoformat(timespec="seconds")
    t0 = time.time()
    ep = run_episode(srv, model=model, initial_note=initial_note)
    wall = time.time() - t0
    code = ep.get("submission_code")
    payload = {
        "tag": tag, "model": model, "pole": pole, "seed": seed,
        "case_id": POLES[pole], "run_at": run_at,
        "initial_note": initial_note, "brief": brief_snapshot,
        "ayuda_label": ("no" if not initial_note else
                        ("poca" if "subpoblaci" in initial_note else
                         "media" if "tipos distintos" in initial_note else
                         "mucha" if "mezcla finita" in initial_note else "sí")),
        "abort_reason": ep.get("abort_reason"),
        "turns": len(ep.get("trace", [])),
        "accepted": ep.get("accepted"), "R": ep.get("R"),
        "tokens": ep.get("tokens"),
        "wall_s": round(wall, 1),
        "budget_spent": float(ep.get("budget_spent", 0.0)),
        "shopping": _shopping_signature(ep.get("trace", [])),
        "delivered_code": code,
        "instruments": _score(code, pole, ins),
        "episode": ep,
    }
    OUT.mkdir(parents=True, exist_ok=True)
    path = OUT / f"{tag}__{model}__{pole}__{seed}.json"
    path.write_text(json.dumps(payload, indent=1, default=str))
    ins_line = payload["instruments"]
    key = "S_valley_fuerte" if (pole == "mix" and "S_valley_fuerte" in ins_line) else ("S_struct" if pole == "mix" else "S_clean")
    val = ins_line.get(key)
    print(f"[{tag}] {model} {pole} seed={seed}: abort={payload['abort_reason']} "
          f"turns={payload['turns']} spent={payload['budget_spent']:.0f} "
          f"{key}={val if val is None else round(val, 3)} "
          f"repeats={payload['shopping']['bought_repeats']} -> {path.name}")
    return payload


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("mode", choices=["tecnico", "main", "pista", "escalera"])
    ap.add_argument("--only", type=int, default=None)
    args = ap.parse_args()
    ins = _instruments()
    if args.mode == "tecnico":
        run_cell(TEC_MODEL, "mix", TEC_SEED, ins, "tecnico")
        return 0
    if args.mode == "escalera":
        cells = ESCALERA_CELLS if args.only is None else [ESCALERA_CELLS[args.only]]
        for nivel, note, model, pole, seed in cells:
            run_cell(model, pole, seed, ins, f"v02_{nivel}", initial_note=note)
        return 0
    if args.mode == "pista":
        cells = PISTA_CELLS if args.only is None else [PISTA_CELLS[args.only]]
        for model, pole, seed in cells:
            run_cell(model, pole, seed, ins, "pista", initial_note=PISTA)
        return 0
    cells = MAIN_CELLS if args.only is None else [MAIN_CELLS[args.only]]
    for model, pole, seed in cells:
        run_cell(model, pole, seed, ins, "main")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
