"""E0_LEDGER.md -- clean accounting of EVERY v2 episode (both currencies).

One row per trace in traces/ (E0 seeds 0-3 + E0.5 consolidation batch):
model, seed, phase (pre/post ergonomics fix), outcome, R, R_uncl, scrap
|dP| mean/max (server-side, enriched regimes, zero-LLM), window read
(mechanical: does the submission reference cal_window), code size, spend,
turns, tokens, branch per the signed pre-registration (A: R>=0.85 /
B: scored below / abort). The ledger is COMMITTED (the paper's accounting);
traces named exemplar are whitelisted into the repo (Decision Log v0.66).

Run:  .venv/Scripts/python cases/mendel_subtypes_v2/build_ledger.py
"""

import json
import sys
from pathlib import Path
from types import SimpleNamespace

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
CASE = Path(__file__).parent
sys.path.insert(0, str(CASE))

import world  # noqa: E402

from wager.contracts import CaseMeta  # noqa: E402
from wager.factory.case_loader import load_battery, make_window_enrich  # noqa: E402
from wager.reward.functionals import functional_value  # noqa: E402
from wager.reward.sandbox import SandboxedSubmission  # noqa: E402
from wager.reward.seeds import derive_seed  # noqa: E402

N_DIAG = 4000
PRE_FIX = {("gpt-5.4", 0), ("gpt-5.4", 1)}  # ran before the experiment_note fix


def dps_for(code, meta, battery, enrich, spec):
    vals = []
    try:
        with SandboxedSubmission(code, meta.column_names, timeout_s=30.0) as sb:
            for item in battery.items:
                ns = enrich(SimpleNamespace(config=dict(item.regime.config),
                                            context=dict(item.regime.context), horizon=None),
                            item.seed_world)
                pt = functional_value(spec, world.sample(ns, N_DIAG, item.seed_world))
                try:
                    ps = functional_value(spec, sb.run(ns, N_DIAG, derive_seed(item.seed_world, 5)))
                    vals.append(abs(ps - pt))
                except Exception:  # noqa: BLE001
                    pass
    except Exception:  # noqa: BLE001
        pass
    return vals


def main():
    meta = CaseMeta.from_json_file(CASE / "meta.json")
    battery = load_battery(CASE)
    enrich = make_window_enrich(CASE, meta)
    spec = meta.stakes.functionals[0]

    rows = []
    for path in sorted((CASE / "traces").glob("e0*.json")):
        tr = json.loads(path.read_text(encoding="utf-8"))
        model = tr.get("model", "?")
        seed = int(path.stem.rsplit("seed", 1)[-1])
        phase = "pre-fix" if (model, seed) in PRE_FIX else "post-fix"
        code = tr.get("submission_code") or ""
        r = tr.get("R")
        window_read = "cal_window" in code
        if r is None:
            branch, dp_mean, dp_max = f"abort:{tr.get('abort_reason')}", None, None
        else:
            branch = "A" if r >= 0.85 else "B"
            vals = dps_for(code, meta, battery, enrich, spec) if code else []
            dp_mean = round(float(np.mean(vals)), 3) if vals else None
            dp_max = round(float(np.max(vals)), 3) if vals else None
        rows.append({
            "file": path.name, "model": model, "seed": seed, "phase": phase,
            "R": None if r is None else round(r, 3),
            "R_uncl": None if tr.get("R_unclipped") is None else round(tr["R_unclipped"], 3),
            "dp_mean": dp_mean, "dp_max": dp_max, "window_read": window_read,
            "code_kb": round(len(code) / 1024, 1),
            "spent": tr.get("budget_spent"), "turns": tr.get("turns"),
            "tokens": tr.get("tokens", {}).get("total"), "branch": branch,
        })
        print(f"  {path.name}: R={rows[-1]['R']} branch={branch} dp_max={dp_max}")

    def fmt(v):
        return "—" if v is None else (f"{v:g}" if isinstance(v, (int, float)) else str(v))

    hdr = ("| trace | modelo | seed | fase | R | R_uncl | \\|dP\\| mean | \\|dP\\| max "
           "| lee ventana | KB | gasto | turnos | tokens | rama |")
    sep = "|" + "---|" * 14
    lines = [
        "# E0_LEDGER — mendel_subtypes_v2 (contabilidad completa de episodios)", "",
        "GENERADO por build_ledger.py — no editar a mano; regenerar para auditar.",
        "Fase pre-fix = antes de documentar experiment()=un-lote-por-llamada (v0.64-e).",
        "Rama A: R>=0.85 (uso la ventana para la ley del outcome). Rama B: scoreado abajo.",
        "|dP| = error absoluto de P(outcome<-5) (scrap) por item de bateria, server-side.", "",
        hdr, sep,
    ]
    for row in rows:
        lines.append("| " + " | ".join(fmt(row[k]) for k in (
            "file", "model", "seed", "phase", "R", "R_uncl", "dp_mean", "dp_max",
            "window_read", "code_kb", "spent", "turns", "tokens", "branch")) + " |")
    (CASE / "E0_LEDGER.md").write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")
    print(f"-> E0_LEDGER.md ({len(rows)} episodios)")


if __name__ == "__main__":
    main()
