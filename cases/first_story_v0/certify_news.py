"""first_story_v0 NEWS variant (D4): the incorporation certificate.

Pre-registered and SIGNED BEFORE running: the sealed HVAC event (turn 4 or 50%
spend) reveals the era's hall readings. The pair isolates PURE incorporation
(neither robot stratifies on its own):

  (i)  E[R_terco_noticia] within max(3 x std, 0.05) of the folklore twin (=0):
       playing through the notice and ignoring it = the seduced floor.
  (ii) E[R_cuidadoso_noticia] >= 0.85: reading the log, mapping the record's
       time trends into ambient space and re-estimating reaches the ceiling
       WITH WHAT REMAINS of the budget (D4 certificate clause).
  (iii) distributional over seeds; base certificates (certificates.json) must
       remain byte-identical (the event adds surface, never moves scoring --
       verified pin no-op).

Run:  .venv/Scripts/python cases/first_story_v0/certify_news.py
"""

import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
CASE = Path(__file__).parent
sys.path.insert(0, str(CASE))

import robots  # noqa: E402

N_SEEDS = 5


def main():
    runs = {"terco_noticia": [], "cuidadoso_noticia": []}
    for robot in runs:
        for k in range(N_SEEDS):
            runs[robot].append(robots.run_robot(CASE, robot, seed_offset=20 + k))
    stats = {robot: {"mean_R": float(np.mean([x["R"] for x in v])),
                     "std_R": float(np.std([x["R"] for x in v])),
                     "per_seed": [round(x["R"], 4) for x in v]}
             for robot, v in runs.items()}
    gates = {
        "terco_ignora_al_piso": abs(stats["terco_noticia"]["mean_R"]) <= max(
            3 * stats["terco_noticia"]["std_R"], 0.05),
        "cuidadoso_incorpora_llega": stats["cuidadoso_noticia"]["mean_R"] >= 0.85,
    }
    gates["all"] = all(gates.values())
    report = {"robots": stats, "gates": gates}
    print(json.dumps(report, indent=2))
    (CASE / "certificates_news.json").write_text(json.dumps(report, indent=2) + "\n",
                                                 encoding="utf-8")


if __name__ == "__main__":
    main()
