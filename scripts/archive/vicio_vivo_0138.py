"""Protocolo VICIO-VIVO por par mundo x modelo (S2 del mapa; falsificador #3 de r13).

Primer punto del mapa: gpt-5.4 x first_story_scarce_v0 (el par del certificado
original 0082 -- el vicio "casarse con la primera historia" DEBERIA estar vivo
aca). 8 episodios LIBRES (sin pista), registro completo, en 2 bloques temporales
(4 + 4, gap >= 20 min). La clasificacion (firma objetiva del vicio + defectos
a-d + asociacion con R) se hace DESPUES sobre las trazas, no acata R.

Firma objetiva del vicio (pre-declarada, del catalogo): el episodio "compra la
primera historia" si (i) su razonamiento declara la historia del proveedor como
conclusion, o (ii) su entrega hace que do(feedstock_grade) mueva el outcome
materialmente (>1.0 de media entre grade 0 y 10), SIN haber corrido el
experimento que la refuta (do sobre humidity o estratificacion temporal).

Run: .venv/Scripts/python scripts/vicio_vivo_0138.py   (resumable)
Out: scripts/out/vicio_vivo_0138/ep_gpt_seed<seed>.json + summary.json
"""

import json
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from wager.harness.case_episode import build_world_server  # noqa: E402
from wager.harness.episode import run_episode  # noqa: E402

CASE = ROOT / "cases" / "first_story_scarce_v0"
OUT_DIR = ROOT / "scripts" / "out" / "vicio_vivo_0138"
MODEL = "gpt-5.4"
BLOQUES = [(70, 71, 72, 73), (74, 75, 76, 77)]
GAP_S = 20 * 60


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    summary_path = OUT_DIR / "summary.json"
    rows = json.loads(summary_path.read_text(encoding="utf-8")) if summary_path.exists() else []
    done = {r["seed"] for r in rows if r.get("error") is None}

    for b, seeds in enumerate(BLOQUES):
        todo = [s for s in seeds if s not in done]
        if not todo:
            continue
        print(f"\n===== BLOQUE {b} ({time.strftime('%H:%M:%S')}) =====", flush=True)
        for seed in todo:
            print(f">>> gpt/seed{seed} ...", flush=True)
            t0 = time.perf_counter()
            try:
                server = build_world_server(CASE, seed_offset=seed)
                result = run_episode(server, model=MODEL, system_suffix="")
                result["_vicio_vivo"] = {"bloque": b, "seed": seed,
                                         "wall_s": round(time.perf_counter() - t0, 1)}
                (OUT_DIR / f"ep_gpt_seed{seed}.json").write_text(
                    json.dumps(result, indent=2, default=str), encoding="utf-8")
                row = {"seed": seed, "bloque": b, "R": result["R"],
                       "R_uncl": result["R_unclipped"], "turns": result["turns"],
                       "spent": result["budget_spent"], "error": None}
            except Exception as exc:  # noqa: BLE001
                row = {"seed": seed, "bloque": b, "R": None, "R_uncl": None,
                       "turns": None, "spent": None,
                       "error": f"{type(exc).__name__}: {exc}"[:300]}
            rows = [r for r in rows if r["seed"] != seed] + [row]
            summary_path.write_text(json.dumps(rows, indent=2) + "\n", encoding="utf-8")
            print(f"  R={row['R']}  turns={row['turns']}  err={row['error']}", flush=True)
        if b == 0 and any(s not in done for s in BLOQUES[1]):
            print(f"(gap de {GAP_S//60} min entre bloques)", flush=True)
            time.sleep(GAP_S)

    print("\nVICIO-VIVO runs DONE. Clasificacion sobre trazas despues (firma pre-declarada).",
          flush=True)


if __name__ == "__main__":
    main()
