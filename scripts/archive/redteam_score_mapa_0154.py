"""Sensitivity floor of the 5-lines score for the LOAD MAP (paso 0, ADR 0153).

The map measures small deltas between forked deliveries. Before pre-registering,
document what defect sizes the battery can SEE: submit dense-table versions of
the truth with graded, behaviorally meaningful defects and record R.

Defects (line 3 = a mid line; sigma = world.NOISE-equivalent 0.7):
  shift_{0.25,0.5,1,2}sigma  -- mean shift on line 3 (the size of a belief error)
  pool_2345                  -- lines 2-5 replaced by their common average curve
                                (the canonical wrong belief of the nota worlds)
  noise_x{0.8,1.3}           -- dispersion mis-estimated
  sd_collapse_l3             -- line 3 delivered with sd 0.05

Gate (documented, not blocking): a 0.5-sigma shift on ONE line must cost
>= 0.005 R; pool_2345 must cost >= 0.05. If not, the battery needs hardening
BEFORE the map runs (receta ADR 0136).

Run: .venv/Scripts/python scripts/redteam_score_mapa_0154.py [case_dir=cases/rabbit_hole_v2]
"""

import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from wager.harness.case_episode import build_world_server  # noqa: E402

CASE = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "cases" / "rabbit_hole_v2"
sys.path.insert(0, str(CASE))
import world  # noqa: E402

SIGMA = 0.7
GRID = np.round(np.arange(0.0, 10.001, 0.05), 3)


def tables(mod=None):
    """line -> dense true-mean table, optionally perturbed by mod(name, vals)."""
    out = {}
    for name in world.LINES:
        vals = np.asarray(world.g_curve(name, GRID), dtype=float)
        if mod is not None:
            vals = mod(name, vals)
        out[name] = vals
    return out


def submission(tabs, sds):
    parts = []
    for name in world.LINES:
        xs = ", ".join(f"{v:g}" for v in GRID)
        vs = ", ".join(f"{v:.4f}" for v in tabs[name])
        parts.append(f'    {name}: (np.array([{xs}]), np.array([{vs}]), {sds[name]:.3f}),')
    tabs_s = "\n".join(parts)
    return f'''
import numpy as np
import pandas as pd

T = {{
{tabs_s}
}}

def model(regime, n, seed):
    rng = np.random.default_rng(seed)
    X, Y, sd = T[int(regime.config["line"])]
    d = np.full(n, float(regime.config["driver"]))
    y = np.interp(d, X, Y) + rng.normal(0.0, sd, n)
    return pd.DataFrame({{"outcome": y}})
'''


def score(code):
    server = build_world_server(CASE, seed_offset=3)
    r = server.submit(code)
    return round(server.result["R"], 4) if r.accepted else None


def main():
    sds = {n: SIGMA for n in world.LINES}
    base_tabs = tables()
    results = {"case": CASE.name, "truth_tables": score(submission(base_tabs, sds))}

    for k in (0.25, 0.5, 1.0, 2.0):
        mod = lambda name, v: v + (k * SIGMA if name == 3 else 0.0)  # noqa: E731
        results[f"shift_{k}sigma_l3"] = score(submission(tables(mod), sds))

    pooled = np.mean([np.asarray(world.g_curve(n, GRID), float) for n in (2, 3, 4, 5)], axis=0)
    mod_pool = lambda name, v: pooled if name != 1 else v  # noqa: E731
    results["pool_2345"] = score(submission(tables(mod_pool), sds))

    for f in (0.8, 1.3):
        sds_f = {n: SIGMA * f for n in world.LINES}
        results[f"noise_x{f}"] = score(submission(base_tabs, sds_f))

    sds_c = dict(sds)
    sds_c[3] = 0.05
    results["sd_collapse_l3"] = score(submission(base_tabs, sds_c))

    base = results["truth_tables"]
    results["gate_shift05_seen"] = (base - results["shift_0.5sigma_l3"]) >= 0.005
    results["gate_pool_seen"] = (base - results["pool_2345"]) >= 0.05
    results["floor_ok"] = bool(results["gate_shift05_seen"] and results["gate_pool_seen"])

    print(json.dumps(results, indent=2))
    out = ROOT / "scripts" / "out" / "redteam_mapa_0154"
    out.mkdir(parents=True, exist_ok=True)
    (out / f"{CASE.name}.json").write_text(json.dumps(results, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
