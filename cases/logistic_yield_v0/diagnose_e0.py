"""E0 second currency for #11: per-item deadline |dP| = |P(y@16<80)_sub - truth|.

Zero-LLM. Runs the trace's submission in the sandbox on every battery item
whose grid carries t=16 (the functional's home), at 2000 units.

Run:  .venv/Scripts/python cases/logistic_yield_v0/diagnose_e0.py <trace.json>
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
from wager.factory.case_loader import load_battery, make_sample_transform  # noqa: E402
from wager.reward.functionals import functional_value  # noqa: E402
from wager.reward.sandbox import SandboxedSubmission  # noqa: E402
from wager.reward.seeds import derive_seed  # noqa: E402

N_DIAG = 2000


def main():
    trace_path = Path(sys.argv[1])
    tr = json.loads(trace_path.read_text(encoding="utf-8"))
    code = tr["submission_code"]
    meta = CaseMeta.from_json_file(CASE / "meta.json")
    spec = meta.stakes.functionals[0]
    battery = load_battery(CASE)
    transform = make_sample_transform(meta)

    print(f"trace: {trace_path.name}  R={tr['R']}  R_uncl={tr['R_unclipped']:+.3f}")
    print("item  feed   P_truth  P_sub   |dP|")
    rows = []
    with SandboxedSubmission(code, meta.column_names, timeout_s=30.0) as sb:
        for i, item in enumerate(battery.items):
            grid = item.regime.context["t_grid"]
            if 16.0 not in grid:
                continue
            ns = SimpleNamespace(config=dict(item.regime.config),
                                 context=dict(item.regime.context), horizon=None)
            truth_w = transform(ns, world.sample(ns, N_DIAG, item.seed_world))
            p_truth = functional_value(spec, truth_w)
            try:
                pred_w = transform(ns, sb.run(ns, N_DIAG, derive_seed(item.seed_world, 5)))
                p_sub = functional_value(spec, pred_w)
            except Exception as exc:  # noqa: BLE001
                print(f"  {i}  {item.regime.config.get('feed', 'obs')}: CRASH {str(exc)[:70]}")
                continue
            rows.append(abs(p_sub - p_truth))
            print(f"  {i}  {str(item.regime.config.get('feed', 'obs')):>4}   "
                  f"{p_truth:.3f}   {p_sub:.3f}   {abs(p_sub - p_truth):.3f}")
    if rows:
        print(f"deadline |dP|: mean={np.mean(rows):.3f}  max={np.max(rows):.3f}  "
              f"items>0.05: {sum(1 for d in rows if d > 0.05)}/{len(rows)}")


if __name__ == "__main__":
    main()
