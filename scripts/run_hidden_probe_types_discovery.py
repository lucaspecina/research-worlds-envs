"""Fresh capacity and discovery probes for Grupos escondidos — Particulas bajo una sonda.

Every seed is burned before the API call.  Capacity episodes are separate from the one fresh
unassisted exploratory episode; the latter runs only after at least two of three capacity episodes
cross both the structural and utility gates.
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from wager.harness.case_episode import build_world_server  # noqa: E402
from wager.harness.episode import run_episode  # noqa: E402


CASE = ROOT / "cases/hidden_probe_types_v0"
OUT = ROOT / "scripts/out/hidden_probe_types_discovery"
MODEL = "gpt-5.4"
IDEA_NAMED = (
    "Considerá seriamente que podrían existir dos tipos ocultos de partículas y que cada "
    "partícula conservaría su tipo entre orientaciones. Investigá esa posibilidad antes de "
    "decidir cómo modelar curvas completas nuevas."
)
CELLS = {
    "capacidad_idea_nombrada_01": {"seed": 99910, "hint": IDEA_NAMED},
    "capacidad_idea_nombrada_02": {"seed": 99911, "hint": IDEA_NAMED},
    "capacidad_idea_nombrada_03": {"seed": 99912, "hint": IDEA_NAMED},
    "exploratoria_sin_ayuda_01": {"seed": 99920, "hint": ""},
}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("condition", choices=tuple(CELLS))
    args = parser.parse_args()
    condition = args.condition
    if condition == "exploratoria_sin_ayuda_01":
        raise SystemExit(
            "no se corre sin ayuda: la capacidad condicionada cerró 1/3 y el gate exigía 2/3"
        )
    seed = CELLS[condition]["seed"]
    hint = CELLS[condition]["hint"]

    OUT.mkdir(parents=True, exist_ok=True)
    stem = f"{condition}__{MODEL}__{seed}"
    receipt = OUT / f"{stem}.started.json"
    result_path = OUT / f"{stem}.json"
    if receipt.exists() or result_path.exists():
        raise SystemExit(f"seed {seed} ya fue quemada; no se re-ejecuta ({receipt.name})")

    started = {
        "experiment_id": "exp__grupos-escondidos__sondas-persistentes__v1",
        "case_id": "hidden_probe_types_v0",
        "condition": condition,
        "model": MODEL,
        "seed": seed,
        "seed_burned": True,
        "idea_named": bool(hint),
        "initial_note": hint,
        "started_at_utc": datetime.now(timezone.utc).isoformat(),
        "interpretation": (
            "conditioned capacity validation; not spontaneous discovery"
            if hint else "single fresh unassisted discovery probe; not a rate estimate"
        ),
        "frozen_gates": {
            "per_episode": "accepted and S_probe >= 0.5 and R >= 0.5",
            "capacity_batch": "at least 2 of 3 episodes pass",
        },
    }
    receipt.write_text(json.dumps(started, indent=2) + "\n", encoding="utf-8")

    server = build_world_server(CASE, seed_offset=seed)
    brief_snapshot = server.describe()["brief"]
    t0 = time.time()
    try:
        episode = run_episode(
            server,
            model=MODEL,
            initial_note=hint,
            capture_working_model=True,
        )
        payload = {
            **started,
            "brief": brief_snapshot,
            "finished_at_utc": datetime.now(timezone.utc).isoformat(),
            "wall_s": round(time.time() - t0, 1),
            "evidence_ledger": server.export_evidence_ledger(),
            "episode": episode,
        }
        result_path.write_text(
            json.dumps(payload, indent=2, default=str) + "\n", encoding="utf-8"
        )
        print(json.dumps({
            "path": str(result_path),
            "accepted": episode.get("accepted"),
            "abort_reason": episode.get("abort_reason"),
            "turns": episode.get("turns"),
            "R": episode.get("R"),
            "R_unclipped": episode.get("R_unclipped"),
            "budget_spent": episode.get("budget_spent"),
            "tokens": episode.get("tokens"),
        }, indent=2))
    except Exception as exc:
        failed = {
            **started,
            "failed_at_utc": datetime.now(timezone.utc).isoformat(),
            "wall_s": round(time.time() - t0, 1),
            "error": repr(exc),
        }
        (OUT / f"{stem}.failed.json").write_text(
            json.dumps(failed, indent=2) + "\n", encoding="utf-8"
        )
        raise
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
