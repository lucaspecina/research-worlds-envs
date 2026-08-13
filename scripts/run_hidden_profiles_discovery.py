"""Primer slice con agente real para Grupos escondidos — Perfiles persistentes.

La celda está congelada en la ficha del 2026-08-13. La semilla se quema escribiendo un recibo
antes de llamar a la API; un recibo existente impide re-ejecutarla.
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


CASE = ROOT / "cases/hidden_profiles_v0"
OUT = ROOT / "scripts/out/hidden_profiles_discovery"
GPT_MODEL = "gpt-5.4"
DEEPSEEK_MODEL = "DeepSeek-V3.2"
HINT = (
    "Considerá la posibilidad de que los perfiles completos provengan de unos pocos tipos "
    "ocultos que se mantienen a través de las doce pruebas. Investigá esa idea con los datos "
    "antes de decidir cómo modelar."
)
CELLS = {
    "idea_nombrada": {"seed": 99810, "hint": HINT},
    "sin_ayuda": {"seed": 99811, "hint": ""},
    # Same seed_offset by design: finite_archive makes the source one fixed
    # table, so both branches receive identical prefixes regardless of batching.
    "pareado_sin_ayuda": {"seed": 99820, "hint": ""},
    "pareado_idea_nombrada": {"seed": 99820, "hint": HINT},
    "desempate_idea_nombrada": {"seed": 99821, "hint": HINT},
}
CELLS.update({
    f"confirmacion_sin_ayuda_{i:02d}": {"seed": seed, "hint": ""}
    for i, seed in enumerate(range(99830, 99840), start=1)
})
for cell in CELLS.values():
    cell["model"] = GPT_MODEL

# External model replication, frozen after the gpt-5.4 batch. The no-hint cells are
# contingent on at least 2/3 valid hint cells crossing S_profile >= 0.5.
CELLS.update({
    f"replica_deepseek_idea_nombrada_{i:02d}": {
        "seed": seed, "hint": HINT, "model": DEEPSEEK_MODEL,
    }
    for i, seed in enumerate(range(99840, 99843), start=1)
})
CELLS.update({
    f"replica_deepseek_sin_ayuda_{i:02d}": {
        "seed": seed, "hint": "", "model": DEEPSEEK_MODEL,
    }
    for i, seed in enumerate(range(99843, 99853), start=1)
})


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("condition", choices=tuple(CELLS))
    args = parser.parse_args()
    condition = args.condition
    seed = CELLS[condition]["seed"]
    hint = CELLS[condition]["hint"]
    model = CELLS[condition]["model"]

    OUT.mkdir(parents=True, exist_ok=True)
    stem = f"{condition}__{model}__{seed}"
    receipt = OUT / f"{stem}.started.json"
    result_path = OUT / f"{stem}.json"
    if receipt.exists() or result_path.exists():
        raise SystemExit(
            f"seed {seed} ya fue quemada; no se re-ejecuta ({receipt.name})"
        )

    if condition.startswith("replica_deepseek_sin_ayuda_"):
        interpretation = "external-model no-hint replication"
    elif condition.startswith("replica_deepseek_idea_nombrada_"):
        interpretation = "external-model resolvability gate"
    elif condition.startswith("confirmacion_sin_ayuda_"):
        interpretation = "frozen no-hint confirmation"
    else:
        interpretation = "exploratory resolvability slice; not confirmation"

    started = {
        "experiment_id": "exp__grupos-escondidos__perfiles-persistentes__v1",
        "case_id": "hidden_profiles_v0",
        "condition": condition,
        "model": model,
        "seed": seed,
        "seed_burned": True,
        "hint": hint,
        "started_at_utc": datetime.now(timezone.utc).isoformat(),
        "interpretation": interpretation,
    }
    receipt.write_text(json.dumps(started, indent=2) + "\n", encoding="utf-8")

    server = build_world_server(CASE, seed_offset=seed)
    brief_snapshot = server.describe()["brief"]
    t0 = time.time()
    try:
        episode = run_episode(
            server,
            model=model,
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
