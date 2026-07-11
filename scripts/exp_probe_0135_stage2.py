"""Probe 0135 stage 2 (pre-signed ladder): does translation PRESERVE the order
of belief qualities? Two degraded manifests x 15 deliveries, arm A (raw), with
the instruction "implement EXACTLY this belief".

For each degraded manifest we also build its deterministic REFERENCE, so each
delivery gets two numbers:
  - fidelity: regret vs its OWN reference (must sit at the floor if translation
    is faithful, regardless of the belief's quality);
  - quality: regret vs the TRUTH reference (the belief's real distance).
Order preservation: median quality(truth) < quality(intermediate) < quality(folklore)
in every block, with the fidelity of every rung at the floor.

INTERMEDIATE: the best fork delivery (D59, R=0.9866) with its two defects repaired
(historical humidity + decomposed noise) -- a real certified-world program.
FOLKLORE: the plant's story (feedstock drives outcome; supplier is the lever;
hall irrelevant), coefficients from the historical record's regression.

Run: .venv/Scripts/python scripts/exp_probe_0135_stage2.py
"""

import json
import random
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))

from probe_0135_build import (  # noqa: E402
    COLUMNS, TRUTH_MANIFEST, Conformity, EQUIVALENTS, reference_code, render_manifest,
)
from exp_probe_0135 import build_prompt, extract_code, mechanical_check, SYSTEM, MODEL  # noqa: E402
from wager.agent.llm_client import FoundryChat  # noqa: E402

OUT = ROOT / "scripts" / "out" / "probe_0135" / "stage2"
MAX_ATTEMPTS = 3

INTERMEDIATE_MANIFEST = {
    "name": "intermediate",
    "outputs": ["feedstock", "outcome"],
    "latents": {
        "humidity_eff": "hall humidity actually driving the process; if humidity is set in config: humidity_eff = that value for all units; if absent: humidity_eff ~ Normal(5.18, 1.94) clipped to [2, 8] per unit",
        "grade_eff": "supplier grade; if feedstock_grade is set: grade_eff = that exact value; if absent: grade_eff = 5.0 for all units",
    },
    "equations": {
        "feedstock": "5.6894 + 0.9645*grade_eff - 0.8878*humidity_eff + Normal(0, 0.9531)",
        "outcome": "42.8276 - 0.0473*grade_eff - 2.4906*humidity_eff + Normal(0, 3.568)",
    },
    "notes": [
        "temp and line_speed affect NOTHING.",
        "all Normal noises are fresh independent per-unit draws.",
    ],
}

FOLKLORE_MANIFEST = {
    "name": "folklore",
    "outputs": ["feedstock", "outcome"],
    "latents": {
        "grade_eff": "supplier grade; if feedstock_grade is set: grade_eff = that exact value; if absent: grade_eff ~ Normal(5, 1) clipped to [0, 10] per unit",
    },
    "equations": {
        "feedstock": "6.0 + 1.0*(grade_eff - 5.0) + Normal(0, 1.85)",
        "outcome": "30.0 + 0.85*(feedstock - 6.0) + Normal(0, 3.2)",
    },
    "notes": [
        "the hall (humidity, temp, line_speed) affects NOTHING in this belief.",
        "outcome is driven by the material: it reads the generated feedstock value.",
        "all Normal noises are fresh independent per-unit draws.",
    ],
}

REF_INTERMEDIATE = '''
import numpy as np
import pandas as pd

def model(regime, n, seed):
    rng = np.random.default_rng(seed)
    cfg = regime.config
    if "humidity" in cfg:
        hum = np.full(n, float(cfg["humidity"]))
    else:
        hum = np.clip(rng.normal(5.18, 1.94, n), 2.0, 8.0)
    if "feedstock_grade" in cfg:
        grade = np.full(n, float(cfg["feedstock_grade"]))
    else:
        grade = np.full(n, 5.0)
    feedstock = 5.6894 + 0.9645 * grade - 0.8878 * hum + rng.normal(0.0, 0.9531, n)
    outcome = 42.8276 - 0.0473 * grade - 2.4906 * hum + rng.normal(0.0, 3.568, n)
    return pd.DataFrame({"feedstock": feedstock, "outcome": outcome})
'''

REF_FOLKLORE = '''
import numpy as np
import pandas as pd

def model(regime, n, seed):
    rng = np.random.default_rng(seed)
    cfg = regime.config
    if "feedstock_grade" in cfg:
        grade = np.full(n, float(cfg["feedstock_grade"]))
    else:
        grade = np.clip(rng.normal(5.0, 1.0, n), 0.0, 10.0)
    feedstock = 6.0 + 1.0 * (grade - 5.0) + rng.normal(0.0, 1.85, n)
    outcome = 30.0 + 0.85 * (feedstock - 6.0) + rng.normal(0.0, 3.2, n)
    return pd.DataFrame({"feedstock": feedstock, "outcome": outcome})
'''

RUNGS = [
    ("intermediate", INTERMEDIATE_MANIFEST, REF_INTERMEDIATE),
    ("folklore", FOLKLORE_MANIFEST, REF_FOLKLORE),
]


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    print("Calibrating floors (truth conformity) ...", flush=True)
    conf_truth = Conformity(reference_code(TRUTH_MANIFEST))
    conf_truth.set_floors([conf_truth.raw_distances(c, rep_seed=10 + i)
                           for i, c in enumerate(EQUIVALENTS)])

    rung_data = {}
    for name, manifest, ref in RUNGS:
        print(f"Building conformity for rung '{name}' ...", flush=True)
        cr = Conformity(ref, base_seed=515151 + hash(name) % 1000)
        cr.set_floors([cr.raw_distances(c, rep_seed=40 + i) for i, c in enumerate([ref] * 3)])
        q = conf_truth.regret(ref, rep_seed=888)
        rung_data[name] = (manifest, ref, cr, q)
        print(f"  quality of '{name}' belief vs truth: mean={q['regret_mean']:.1f} "
              f"max={q['regret_max']:.1f}", flush=True)

    cells = [(name, b, k) for b in range(5) for name, *_ in RUNGS for k in range(3)]
    for b in range(5):
        blk = [c for c in cells if c[1] == b]
        random.Random(8200 + b).shuffle(blk)
        print(f"\n===== BLOCK {b} ({datetime.now(timezone.utc).isoformat()}) =====", flush=True)
        for name, block, k in blk:
            path = OUT / f"cell_b{block}_{name}_{k}.json"
            if path.exists():
                continue
            manifest, ref, cr, _ = rung_data[name]
            t0 = time.time()
            chat = FoundryChat(system=SYSTEM, model=MODEL, max_completion_tokens=4000)
            prompt = "\n".join([
                __import__("probe_0135_build").DELIVERY_SPEC_V1, "",
                render_manifest(manifest), "", "Deliver the code now."])
            code, attempts, errors = None, 0, []
            while attempts < MAX_ATTEMPTS:
                attempts += 1
                reply = chat.ask(prompt)
                cand = extract_code(reply.content)
                if cand is None:
                    errors.append("no code block")
                    prompt = "Your reply contained no ```python code block. Deliver the code now."
                    continue
                err = mechanical_check(cand)
                if err is None:
                    code = cand
                    break
                errors.append(err)
                prompt = (f"Your delivery failed a mechanical check: {err}\n"
                          f"Fix ONLY that and deliver the full corrected code.")
            cell = {"rung": name, "block": block, "k": k, "attempts": attempts,
                    "mechanical_errors": errors, "tokens": chat.usage.total_tokens,
                    "code": code, "elapsed_s": round(time.time() - t0, 1),
                    "started_at": datetime.now(timezone.utc).isoformat()}
            if code is not None:
                fid = cr.regret(code, rep_seed=2000 + block * 100 + k)
                qual = conf_truth.regret(code, rep_seed=3000 + block * 100 + k)
                cell.update({"fidelity_mean": fid["regret_mean"], "fidelity_max": fid["regret_max"],
                             "quality_vs_truth_mean": qual["regret_mean"],
                             "quality_vs_truth_max": qual["regret_max"]})
            path.write_text(json.dumps(cell, indent=2, default=str) + "\n", encoding="utf-8")
            brief = {kk: cell.get(kk) for kk in ("rung", "block", "k", "attempts",
                                                 "fidelity_mean", "quality_vs_truth_mean")}
            print("  " + json.dumps(brief, default=str), flush=True)
    print("\nSTAGE 2 DONE", flush=True)


if __name__ == "__main__":
    main()
