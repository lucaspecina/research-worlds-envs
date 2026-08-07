"""ADR 0128 step 2 -- MICRO-BATCH N=5 of the medio template (pilot + 4 fresh).

Sealed BEFORE running (this file's commit is the seal):
- Commissions (order fixed): 2x STRATUM_B (negative confounding, same band as
  the pilot -> measures domain/param diversity WITHIN a stratum) + 2x STRATUM_C
  (positive-weak band [+1.0, +1.6], distinct from the dev fixture's +2.24 ->
  measures range across strata). Domain collisions are DATA (medio() records
  them; one retry each), not something to prevent.
- Classification per commission: pass / fallo_dentro_de_clase / fuera_de_clase /
  colision_de_dominio / plumbing (exception).
- PANEL (sealed metric): per certified case, the behavioral vector = the
  certificate's rival R values (shared derived keys) + R_canonical. Report
  pairwise Pearson r and max|diff| across cases, plus domains and key params.
  Expected reading (sealed): within-template vectors SHOULD be near-identical
  (template-fill); the panel quantifies that baseline and the B-vs-C
  separation. "Yield" here is a first noisy hint (N=5), never a claim.

Run: .venv/Scripts/python scripts/run_medio_batch.py   (resumable by count)
"""

import json
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from wager.factory.proto_designer import STRATUM_B, medio  # noqa: E402

STRATUM_C = dict(STRATUM_B, confound_coef=(1.0, 1.6))  # positive-weak; fixture was +2.24

COMMISSIONS = [("B", STRATUM_B), ("B", STRATUM_B), ("C", STRATUM_C), ("C", STRATUM_C)]
OUT = ROOT / "scripts" / "out" / "medio_batch_report.json"


def main() -> None:
    report = json.loads(OUT.read_text(encoding="utf-8")) if OUT.exists() else {"runs": []}
    done = len(report["runs"])
    for i, (label, stratum) in enumerate(COMMISSIONS):
        if i < done:
            continue
        print(f"\n>>> commission {i + 1}/4 (stratum {label}) ...", flush=True)
        t0 = time.perf_counter()
        try:
            log = medio(stratum=stratum)
            run = {"i": i, "stratum": label,
                   "classification": log.get("classification"),
                   "case_id": (log.get("spec") or {}).get("case_id"),
                   "domain": (log.get("spec") or {}).get("domain"),
                   "confound_coef": ((log.get("spec") or {}).get("params") or {}).get("confound_coef"),
                   "threshold": log.get("threshold"),
                   "stages": [a.get("stage") for a in log.get("attempts", [])],
                   "wall_s": round(time.perf_counter() - t0, 1)}
        except Exception as exc:  # noqa: BLE001
            run = {"i": i, "stratum": label, "classification": "plumbing",
                   "error": f"{type(exc).__name__}: {exc}"[:300],
                   "wall_s": round(time.perf_counter() - t0, 1)}
        report["runs"].append(run)
        OUT.parent.mkdir(parents=True, exist_ok=True)
        OUT.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
        print("   ", json.dumps(run, ensure_ascii=False), flush=True)

    # ---- PANEL over every certified case of this template (pilot included) ----
    import numpy as np
    cases = sorted(p for p in (ROOT / "cases").glob("*_gen_v0")
                   if (p / "certificates.json").exists() and p.name != "confounded_gen_v0")
    vecs, doms = {}, {}
    for p in cases:
        c = json.loads((p / "certificates.json").read_text(encoding="utf-8"))
        keys = sorted(c["R"].keys())
        vecs[p.name] = [c["R"][k] for k in keys] + [c["R_canonical"]]
        m = json.loads((p / "meta.json").read_text(encoding="utf-8"))
        doms[p.name] = {"narrative_head": m["stakes"]["narrative"][:80],
                        "confound_coef": m["operators"][0]["knobs"]["confound_coef"],
                        "gates_all": c["gates"]["all"]}
    names = sorted(vecs)
    panel = {"cases": doms, "vector_keys_note": "sorted R keys + R_canonical",
             "pairs": {}}
    for a in range(len(names)):
        for b in range(a + 1, len(names)):
            va, vb = np.array(vecs[names[a]]), np.array(vecs[names[b]])
            k = min(len(va), len(vb))
            r = float(np.corrcoef(va[:k], vb[:k])[0, 1])
            panel["pairs"][f"{names[a]} vs {names[b]}"] = {
                "pearson": round(r, 4), "max_abs_diff": round(float(np.max(np.abs(va[:k] - vb[:k]))), 4)}
    report["panel"] = panel
    tally = {}
    for r in report["runs"]:
        tally[r["classification"]] = tally.get(r["classification"], 0) + 1
    report["tally_batch4"] = tally
    OUT.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print("\n=== TALLY (4 encargos):", json.dumps(tally), flush=True)
    print("=== PANEL:", json.dumps(panel["pairs"], indent=2), flush=True)


if __name__ == "__main__":
    main()
