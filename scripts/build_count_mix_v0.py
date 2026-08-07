"""Chunk B builder for the count-mixture pair: meta.json (episode block),
ladder anchors and battery.json for BOTH poles, all frozen from instance.json.

Menu/prices (ficha + plan; provisional until G2/G3 pass and re-freeze):
  budget 1000 · observe("archivo") 0.5/row, cap 400 rows, natural regime ·
  experiment fixed 40 + 1.0/row (rows = lots x repeats) · knobs speed [0.8,1.2],
  repeats_per_unit [1,4]. Battery seeds burned: 99260-99279.

Ladder (server convention: [-2] = naive anchor, [-1] = null):
  MIX : rung_2 negbin (best single-component)  · rung_3 naive poisson · rung_4 null
  TWIN: rung_2 negbin inflated                 · rung_3 naive FORCED mixture
        (the dogmatic/apophenia rival)         · rung_4 null
Zero-LLM everywhere.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from cases.count_mix_v0_common import (  # noqa: E402
    _DictRegime, _fit_negbin, _sample_counts, load_instance,
)

BATTERY_SEEDS = list(range(99260, 99280))

BRIEF_NOTE = None  # briefs already written (byte-identical) in chunk A

CONTROL_SURFACE = {
    "settable": {
        "speed": {"low": 0.8, "high": 1.2,
                  "description": "line speed of the runs you launch; the evaluation may use any value in range"},
        "repeats_per_unit": {"low": 1, "high": 4,
                             "description": "measurements taken of EACH lot in the batch (same unit_id repeated)"},
    },
    "context": {},
    "instruments": {},
    "experiment_note": ("each experiment call produces n MEASUREMENTS at your speed, grouped into "
                        "lots of repeats_per_unit readings each; cost = fixed + per ROW; n counts MEASUREMENTS"),
    "deliverable_note": ("model(regime, n, seed) -> DataFrame with columns exactly [unit_id, y]; "
                         "n counts MEASUREMENT ROWS; honor regime.config speed and repeats_per_unit "
                         "(rows group into lots sharing unit_id; last lot may be short). Model the PROCESS."),
}


def episode_block() -> dict:
    return {
        "budget": 1000.0,
        "observe_sources": {
            "archivo": {"cost_per_row": 0.5, "config": {}, "context": {}, "max_rows": 400}
        },
        "experiment": {"cost_fixed": 40.0, "cost_per_row": 1.0, "cost_per_horizon": 0.0},
        "experiment_meter": None,
        "events": [],
        "submit_requires_all_events": False,
        "register": None,
        "smoke_regimes": [
            {"config": {}, "context": {}, "horizon": None},
            {"config": {"speed": 1.1}, "context": {}, "horizon": None},
            {"config": {"speed": 0.9, "repeats_per_unit": 2}, "context": {}, "horizon": None},
        ],
        "control_surface": CONTROL_SURFACE,
    }


def meta_for(pole_case: str, inst: dict) -> dict:
    p = inst["params"]
    if pole_case == "count_mix_v0":
        operators = [{"name": "latent_unit_mixture", "layer": "mechanism",
                      "knobs": {"w": p["w"], "lam_a": p["lam_a"], "lam_b": p["lam_b"]},
                      "ablation": {}}]
    else:
        operators = [{"name": "single_process", "layer": "mechanism",
                      "knobs": {"lam0": p["lam0"]}, "ablation": {}}]
    return {
        "case_id": pole_case,
        "suite": "count_mix_jump",
        "columns": [
            {"name": "unit_id", "dtype": "float", "unit": None,
             "description": "lot identifier within the returned batch (repeats share it)"},
            {"name": "y", "dtype": "int", "unit": "defects",
             "description": "defect count of one measurement of the lot"},
        ],
        "operators": operators,
        "stakes": {
            "narrative": ("A process line produces lots; management plans inspection and "
                          "scrap from a generative defect model that must hold across "
                          "line speeds and repeated measurements."),
            "decision_variables": [], "context_relevance": {},
            "decision_relevance": {}, "functionals": [],
        },
        "scoring": {"lambda_mdl": 0.0, "lambda_provisional": True,
                    "n_samples": 400, "m_reps": 2, "model_call_timeout_s": 10.0},
        "episode": episode_block(),
        "prior_reliability": None,
    }


LADDER_TEMPLATES = {
    "negbin": '''"""Rung -- single NegBin (best one-component; frozen from certifier fit)."""
import numpy as np
import pandas as pd

M, R = {m!r}, {r!r}


def model(regime, n, seed):
    config = regime.config or {{}}
    speed = float(config.get("speed", 1.0))
    repeats = int(round(float(config.get("repeats_per_unit", 1))))
    rng = np.random.default_rng(np.random.SeedSequence([int(seed), 0xAA01]))
    p = R / (R + M * speed)
    full, rem = divmod(n, repeats)
    ids = np.repeat(np.arange(full, dtype=float), repeats)
    if rem:
        ids = np.concatenate([ids, np.full(rem, float(full))])
    y = rng.negative_binomial(R, p, n).astype(float)
    return pd.DataFrame({{"unit_id": ids, "y": y}})
''',
    "poisson": '''"""Rung -- naive single Poisson at the archive mean (S_naive anchor)."""
import numpy as np
import pandas as pd

LAM = {lam!r}


def model(regime, n, seed):
    config = regime.config or {{}}
    speed = float(config.get("speed", 1.0))
    repeats = int(round(float(config.get("repeats_per_unit", 1))))
    rng = np.random.default_rng(np.random.SeedSequence([int(seed), 0xAA02]))
    full, rem = divmod(n, repeats)
    ids = np.repeat(np.arange(full, dtype=float), repeats)
    if rem:
        ids = np.concatenate([ids, np.full(rem, float(full))])
    y = rng.poisson(LAM * speed, n).astype(float)
    return pd.DataFrame({{"unit_id": ids, "y": y}})
''',
    "forced_mix": '''"""Rung -- DOGMATIC forced two-component split (the apophenia rival):
always claims two well-separated groups, w=0.5, regardless of the data."""
import numpy as np
import pandas as pd

LAM_LO, LAM_HI = {lam_lo!r}, {lam_hi!r}


def model(regime, n, seed):
    config = regime.config or {{}}
    speed = float(config.get("speed", 1.0))
    repeats = int(round(float(config.get("repeats_per_unit", 1))))
    rng = np.random.default_rng(np.random.SeedSequence([int(seed), 0xAA03]))
    full, rem = divmod(n, repeats)
    ids = np.repeat(np.arange(full, dtype=float), repeats)
    if rem:
        ids = np.concatenate([ids, np.full(rem, float(full))])
    n_units = int(ids[-1]) + 1 if n else 0
    hi = rng.random(n_units) < 0.5
    lam_unit = np.where(hi, LAM_HI, LAM_LO) * speed
    y = rng.poisson(lam_unit[ids.astype(int)]).astype(float)
    return pd.DataFrame({{"unit_id": ids, "y": y}})
''',
    "null": '''"""Rung -- null reference (degenerate: no defects ever)."""
import numpy as np
import pandas as pd


def model(regime, n, seed):
    config = regime.config or {}
    repeats = int(round(float(config.get("repeats_per_unit", 1))))
    full, rem = divmod(n, repeats)
    ids = np.repeat(np.arange(full, dtype=float), repeats)
    if rem:
        ids = np.concatenate([ids, np.full(rem, float(full))])
    return pd.DataFrame({"unit_id": ids, "y": np.zeros(n)})
''',
}




TRUTH_MIX_TEMPLATE = '''"""Self-contained truth program (sandbox-safe; frozen from instance.json).
Server-side artifact: the scorer runs THIS through the sandbox as S_truth."""
import numpy as np
import pandas as pd

W, LAM_A, LAM_B = {w!r}, {lam_a!r}, {lam_b!r}


def model(regime, n, seed):
    config = regime.config or {{}}
    speed = float(config.get("speed", 1.0))
    speed = min(max(speed, 0.8), 1.2)
    repeats = int(round(float(config.get("repeats_per_unit", 1))))
    repeats = min(max(repeats, 1), 4)
    rng = np.random.default_rng(np.random.SeedSequence([int(seed), 0xC0117]))
    full, rem = divmod(n, repeats)
    ids = np.repeat(np.arange(full, dtype=float), repeats)
    if rem:
        ids = np.concatenate([ids, np.full(rem, float(full))])
    n_units = int(ids[-1]) + 1 if n else 0
    z = rng.random(n_units) < W
    lam_unit = np.where(z, LAM_B, LAM_A) * speed
    y = rng.poisson(lam_unit[ids.astype(int)]).astype(float)
    return pd.DataFrame({{"unit_id": ids, "y": y}})
'''

TRUTH_SINGLE_TEMPLATE = '''"""Self-contained truth program (sandbox-safe; frozen from instance.json)."""
import numpy as np
import pandas as pd

LAM0 = {lam0!r}


def model(regime, n, seed):
    config = regime.config or {{}}
    speed = float(config.get("speed", 1.0))
    speed = min(max(speed, 0.8), 1.2)
    repeats = int(round(float(config.get("repeats_per_unit", 1))))
    repeats = min(max(repeats, 1), 4)
    rng = np.random.default_rng(np.random.SeedSequence([int(seed), 0xC0117]))
    full, rem = divmod(n, repeats)
    ids = np.repeat(np.arange(full, dtype=float), repeats)
    if rem:
        ids = np.concatenate([ids, np.full(rem, float(full))])
    n_units = int(ids[-1]) + 1 if n else 0
    lam_unit = np.full(n_units, LAM0) * speed
    y = rng.poisson(lam_unit[ids.astype(int)]).astype(float)
    return pd.DataFrame({{"unit_id": ids, "y": y}})
'''


def build_truth_codes(inst: dict) -> None:
    p = inst["params"]
    (ROOT / "cases/count_mix_v0/truth_code.py").write_text(
        TRUTH_MIX_TEMPLATE.format(w=p["w"], lam_a=p["lam_a"], lam_b=p["lam_b"]))
    (ROOT / "cases/count_mix_twin_v0/truth_code.py").write_text(
        TRUTH_SINGLE_TEMPLATE.format(lam0=p["lam0"]))


def build_ladders(inst: dict) -> None:
    p = inst["params"]
    y_train = _sample_counts("mix", p, _DictRegime({"speed": 1.0}),
                             inst["witness_n"], inst["witness_sample_seed"])["y"].to_numpy(float)
    nb = _fit_negbin(y_train)["params"]
    mix_dir = ROOT / "cases/count_mix_v0/ladder"
    twin_dir = ROOT / "cases/count_mix_twin_v0/ladder"
    mix_dir.mkdir(exist_ok=True)
    twin_dir.mkdir(exist_ok=True)

    (mix_dir / "rung_2_negbin.py").write_text(
        LADDER_TEMPLATES["negbin"].format(m=float(nb["mean"]), r=float(1.0 / nb["alpha"])))
    (mix_dir / "rung_3_naive_poisson.py").write_text(
        LADDER_TEMPLATES["poisson"].format(lam=float(y_train.mean())))
    (mix_dir / "rung_4_null.py").write_text(LADDER_TEMPLATES["null"])

    y_twin = _sample_counts("single", p, _DictRegime({"speed": 1.0}),
                            inst["witness_n"], inst["witness_sample_seed"])["y"].to_numpy(float)
    nb_t = _fit_negbin(y_twin)["params"]
    lam0 = p["lam0"]
    sep = 2.2 * np.sqrt(lam0)
    (twin_dir / "rung_2_negbin_inflated.py").write_text(
        LADDER_TEMPLATES["negbin"].format(m=float(nb_t["mean"]),
                                          r=float(max(1.0 / max(nb_t["alpha"], 1e-4), 1.0) / 4.0)))
    (twin_dir / "rung_3_naive_forced_mix.py").write_text(
        LADDER_TEMPLATES["forced_mix"].format(lam_lo=float(max(lam0 - sep / 2, 0.05)),
                                              lam_hi=float(lam0 + sep / 2)))
    (twin_dir / "rung_4_null.py").write_text(LADDER_TEMPLATES["null"])


def build_battery() -> None:
    items = []
    specs = [({"speed": 0.85}, 0.12), ({"speed": 0.95}, 0.12), ({"speed": 1.0}, 0.12),
             ({"speed": 1.05}, 0.12), ({"speed": 1.15}, 0.12),
             ({"speed": 1.0, "repeats_per_unit": 3}, 0.15),
             ({"speed": 1.1, "repeats_per_unit": 3}, 0.15),
             ({"speed": 1.2, "repeats_per_unit": 2}, 0.10)]
    for (config, weight), seed in zip(specs, BATTERY_SEEDS):
        items.append({"weight": weight,
                      "regime": {"config": {k: float(v) for k, v in config.items()},
                                 "context": {}, "horizon": None},
                      "seed_world": seed})
    payload = json.dumps({"items": items}, indent=2) + "\n"
    for pole in ("count_mix_v0", "count_mix_twin_v0"):
        (ROOT / "cases" / pole / "battery.json").write_text(payload)


def main() -> None:
    inst = load_instance()
    for pole in ("count_mix_v0", "count_mix_twin_v0"):
        (ROOT / "cases" / pole / "meta.json").write_text(
            json.dumps(meta_for(pole, inst), indent=2) + "\n")
    build_ladders(inst)
    build_truth_codes(inst)
    build_battery()
    print("meta.json + ladder/ + battery.json escritos para ambos polos")


if __name__ == "__main__":
    main()
