"""Per-item diagnosis of an E0 trace on selection_bias_v0 -- BOTH currencies.

The mandatory step for a clipped/low R (v0.57-3c branch: ergonomics audited
BEFORE reading judgment): crash-vs-honest breakdown under the COMBINED score
(frozen c_f + declared functionals -- the v0.60 wiring), plus the client
currency |dP| = |P_sub(outcome<2) - P_truth| per regime.

Usage: .venv/Scripts/python cases/selection_bias_v0/diagnose_e0.py <trace.json>
"""

import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
CASE = Path(__file__).parent

from wager.factory.case_loader import (  # noqa: E402
    load_battery, load_ladder, load_meta, load_world_sample, load_world_source,
)
from wager.reward.functionals import functional_value  # noqa: E402
from wager.reward.sandbox import SandboxedSubmission  # noqa: E402
from wager.reward.scorer import (  # noqa: E402
    WorldSide, make_anchors, regime_to_namespace, sandboxed_null_sample, score_submission,
)
from wager.reward.seeds import derive_seed  # noqa: E402


def main():
    trace = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    code = trace.get("submission_code") or trace.get("result", {}).get("code")
    if not code:
        raise SystemExit("trace has no submission code")
    meta = load_meta(CASE)
    battery = load_battery(CASE)
    world_sample = load_world_sample(CASE)
    ladder = load_ladder(CASE)
    naive_code, null_code = ladder[-2][1], ladder[-1][1]
    params = meta.scoring
    spec = meta.stakes.functionals[0]

    with sandboxed_null_sample(null_code, meta.column_names, params.model_call_timeout_s) as null_sample:
        ws = WorldSide(world_sample, battery, meta.column_names, params.n_samples,
                       null_sample=null_sample, functionals=meta.stakes.functionals,
                       c_f=params.c_f)
        s_truth = score_submission(load_world_source(CASE), ws, params).raw_score
        s_naive = score_submission(naive_code, ws, params).raw_score
        s_null = score_submission(null_code, ws, params).raw_score
        rep = score_submission(code, ws, params)
    anchors = make_anchors(s_truth, s_naive, s_null)
    r, r_uncl = anchors.r_of(rep.raw_score)

    print("=" * 70)
    print(f"DIAGNOSE {Path(sys.argv[1]).name}: R={r:.3f} R_uncl={r_uncl:+.3f} (COMBINED score)")
    crash_c = honest_c = 0.0
    n_crash = 0
    for it, bi in zip(rep.items, battery.items):
        contrib = it.weight * it.mean_distance
        if it.sandbox_errors > 0:
            n_crash += 1
            crash_c += contrib
        else:
            honest_c += contrib
    tot = crash_c + honest_c or 1.0
    print(f"  crashes: {n_crash}/{len(battery.items)} items | contrib crashed {100*crash_c/tot:.0f}% "
          f"vs honest {100*honest_c/tot:.0f}%")
    print("  VERDICT:", "CRASH-DOMINATED (ergonomics #17/#19 -- audit before judgment)"
          if crash_c > honest_c else "HONEST distances (model inadequacy, readable)")

    # client currency
    dps = []
    with SandboxedSubmission(code, meta.column_names, timeout_s=params.model_call_timeout_s) as sb:
        for bi in battery.items:
            ns = regime_to_namespace(bi.regime)
            pt = functional_value(spec, world_sample(ns, 4000, bi.seed_world))
            try:
                pred = sb.run(bi.regime, 4000, derive_seed(bi.seed_world, 5))
                dps.append((abs(functional_value(spec, pred) - pt), bi))
            except Exception:  # noqa: BLE001
                dps.append((float("nan"), bi))
    vals = [d for d, _ in dps if not np.isnan(d)]
    print(f"  |dP| mean={np.mean(vals):.3f} max={np.max(vals):.3f} "
          f"(n_ok={len(vals)}/{len(dps)})")
    worst = sorted([x for x in dps if not np.isnan(x[0])], key=lambda t: -t[0])[:4]
    for d, bi in worst:
        dec = bi.regime.config.get("driver")
        print(f"    worst |dP|={d:.3f} at driver={'obs' if dec is None else dec} "
              f"shift={bi.regime.context.get('shift', 0.0)}")
    print("=" * 70)


if __name__ == "__main__":
    main()
