"""Probe 0135 stage 1 (pre-registered): oracle-to-code translation, 3 arms x 15.

Each cell: hand the model the DELIVERY CONTRACT + the truth MODEL SPEC (manifest)
and ask ONLY for the translation to model(regime, n, seed). No environment, no
budget, no score feedback. First code block = the delivery; up to 2 extra attempts
ONLY on mechanical failure (doesn't load / wrong columns / wrong rows / non-finite /
non-deterministic), with the error echoed back. regret_trans computed offline
against the frozen conformity suite (fidelity scale: times the implementation floor).

Arms: A = contract + spec, raw python. B = + neutral INTERFACE skeleton (no science).
C = + scientific skeleton with blanks (structure given; diagnostic upper bound).

5 blocks x 3 cells per arm = 45 cells. Run: .venv/Scripts/python scripts/exp_probe_0135.py
"""

import json
import random
import re
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))

from probe_0135_build import (  # noqa: E402
    COLUMNS, DELIVERY_SPEC_V1, TRUTH_MANIFEST, Conformity, EQUIVALENTS,
    reference_code, render_manifest, _ns,
)
from wager.agent.llm_client import FoundryChat  # noqa: E402
from wager.reward.sandbox import SandboxedSubmission, SandboxError  # noqa: E402
from wager.reward.seeds import derive_seed  # noqa: E402

OUT = ROOT / "scripts" / "out" / "probe_0135" / "stage1"
MODEL = "DeepSeek-V3.2"
MAX_ATTEMPTS = 3  # 1 delivery + up to 2 mechanical repairs
SMOKE_REGIMES = [{}, {"feedstock_grade": 8.0, "humidity": 5.0}, {"temp": 3.0}]

SKELETON_B = '''import numpy as np
import pandas as pd

def model(regime, n, seed):
    rng = np.random.default_rng(seed)
    cfg = regime.config  # dict; may contain feedstock_grade, humidity, temp, line_speed
    # TODO: implement the believed generative process EXACTLY as specified.
    # Build per-unit arrays of length n (broadcast scalars with np.full(n, x)).
    feedstock = ...
    outcome = ...
    return pd.DataFrame({"feedstock": feedstock, "outcome": outcome})'''

SKELETON_C = '''import numpy as np
import pandas as pd

def model(regime, n, seed):
    rng = np.random.default_rng(seed)
    cfg = regime.config
    u = rng.normal(0.0, ___, n)
    if "humidity" in cfg:
        ambient = float(cfg["humidity"]) + rng.normal(0.0, ___, n)
    else:
        t = rng.uniform(0.0, 1.0, n)
        ambient = ___ + ___ * t + rng.normal(0.0, ___, n)
    if "feedstock_grade" in cfg:
        grade = np.full(n, float(cfg["feedstock_grade"]))
    else:
        grade = np.clip(rng.normal(___, ___, n), 0.0, 10.0)
    feedstock = ___ + ___ * (grade - ___) - ___ * (ambient - ___) + rng.normal(0.0, ___, n)
    outcome = ___ - ___ * (ambient - ___) + ___ * u + rng.normal(0.0, ___, n)
    return pd.DataFrame({"feedstock": feedstock, "outcome": outcome})'''

SYSTEM = ("You are completing a single, well-specified coding task for a modeling "
          "harness. Follow the delivery contract exactly. Reply with exactly ONE "
          "```python code block containing the full deliverable.")


def build_prompt(arm: str) -> str:
    parts = [DELIVERY_SPEC_V1, "", render_manifest(TRUTH_MANIFEST), ""]
    if arm == "B":
        parts += ["You may start from this interface skeleton (fill in the process):",
                  "```python", SKELETON_B, "```", ""]
    elif arm == "C":
        parts += ["Complete this skeleton by replacing every ___ with the correct value "
                  "from the MODEL SPEC (do not change the structure):",
                  "```python", SKELETON_C, "```", ""]
    parts += ["Deliver the code now."]
    return "\n".join(parts)


def extract_code(text: str) -> str | None:
    m = re.findall(r"```(?:python)?\s*\n(.*?)```", text, re.DOTALL)
    return m[-1].strip() if m else None


def mechanical_check(code: str) -> str | None:
    """Contract mechanics only (never fidelity): loads, columns, rows, finite, deterministic."""
    try:
        with SandboxedSubmission(code, COLUMNS, timeout_s=15.0) as sb:
            for i, cfg in enumerate(SMOKE_REGIMES):
                a = sb.run(_ns(cfg), 200, derive_seed(31337, i))
                b = sb.run(_ns(cfg), 200, derive_seed(31337, i))
                if not np.allclose(a[COLUMNS].to_numpy(), b[COLUMNS].to_numpy()):
                    return (f"determinism violated for config={cfg}: same (regime, n, seed) "
                            f"must return the same table (use numpy randomness seeded from `seed`)")
    except SandboxError as exc:
        return f"submission failed to load/run: {exc}"
    return None


def run_cell(arm: str, block: int, k: int, conf: Conformity) -> dict:
    chat = FoundryChat(system=SYSTEM, model=MODEL, max_completion_tokens=4000)
    prompt = build_prompt(arm)
    out: dict = {"arm": arm, "block": block, "k": k, "model": MODEL,
                 "started_at": datetime.now(timezone.utc).isoformat()}
    code, attempts, errors = None, 0, []
    while attempts < MAX_ATTEMPTS:
        attempts += 1
        reply = chat.ask(prompt)
        cand = extract_code(reply.content)
        if cand is None:
            errors.append("no code block in reply")
            prompt = "Your reply contained no ```python code block. Deliver the code now."
            continue
        err = mechanical_check(cand)
        if err is None:
            code = cand
            break
        errors.append(err)
        prompt = (f"Your delivery failed a mechanical check: {err}\n"
                  f"Fix ONLY that and deliver the full corrected code.")
    out.update({"attempts": attempts, "mechanical_errors": errors,
                "tokens": chat.usage.total_tokens, "code": code})
    if code is not None:
        r = conf.regret(code, rep_seed=1000 + block * 100 + k)
        out.update(r)
        out["passed_first_try"] = attempts == 1
    return out


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    print("Calibrating conformity floors ...", flush=True)
    conf = Conformity(reference_code(TRUTH_MANIFEST))
    equiv_raw = [conf.raw_distances(c, rep_seed=10 + i) for i, c in enumerate(EQUIVALENTS)]
    conf.set_floors(equiv_raw)

    cells = [(arm, b, k) for b in range(5) for arm in ("A", "B", "C") for k in range(3)]
    for b in range(5):
        blk = [c for c in cells if c[1] == b]
        random.Random(7100 + b).shuffle(blk)
        print(f"\n===== BLOCK {b} ({datetime.now(timezone.utc).isoformat()}) =====", flush=True)
        for arm, block, k in blk:
            name = f"cell_b{block}_{arm}{k}.json"
            path = OUT / name
            if path.exists():
                print(f"  skip {name}", flush=True)
                continue
            t0 = time.time()
            try:
                cell = run_cell(arm, block, k, conf)
            except Exception as e:  # noqa: BLE001 — one dead cell must not kill the block
                cell = {"arm": arm, "block": block, "k": k, "error": f"{type(e).__name__}: {e}"}
            cell["elapsed_s"] = round(time.time() - t0, 1)
            path.write_text(json.dumps(cell, indent=2, default=str) + "\n", encoding="utf-8")
            brief = {kk: cell.get(kk) for kk in ("arm", "block", "k", "attempts",
                                                 "regret_mean", "regret_max", "error")}
            print("  " + json.dumps(brief, default=str), flush=True)
    print("\nSTAGE 1 DONE", flush=True)


if __name__ == "__main__":
    main()
