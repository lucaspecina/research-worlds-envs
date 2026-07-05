"""E0-v2 second currency: per-item |dP| of the scrap exceedance, per trace.

For each battery item: P_truth(outcome < -5) vs P_sub(outcome < -5) at 4000
draws (submission run in the sandbox with the ENRICHED regime -- same choke
point as scoring). Zero-LLM. Reports mean/max |dP| per n_cal and flags items
where the submission's scrap price is off by more than the 5% resolution floor.

Run:  .venv/Scripts/python cases/latent_mix_v2/diagnose_e0.py <trace.json>
"""

import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
CASE = Path(__file__).parent
sys.path.insert(0, str(CASE))

import world  # noqa: E402

from wager.contracts import CaseMeta  # noqa: E402
from wager.factory.case_loader import load_battery, make_window_enrich  # noqa: E402
from wager.reward.functionals import functional_value  # noqa: E402
from wager.reward.sandbox import SandboxedSubmission  # noqa: E402
from wager.reward.seeds import derive_seed  # noqa: E402

N_DIAG = 4000
FLOOR = 0.05  # 5% resolution floor (Decision Log v0.38)


def main():
    trace_path = Path(sys.argv[1])
    tr = json.loads(trace_path.read_text(encoding="utf-8"))
    code = tr["submission_code"]
    meta = CaseMeta.from_json_file(CASE / "meta.json")
    spec = meta.stakes.functionals[0]
    battery = load_battery(CASE)
    enrich = make_window_enrich(CASE, meta)

    rows = []
    with SandboxedSubmission(code, meta.column_names, timeout_s=30.0) as sb:
        for i, item in enumerate(battery.items):
            ns = enrich(_ns(item.regime), item.seed_world)
            p_truth = functional_value(spec, world.sample(ns, N_DIAG, item.seed_world))
            try:
                p_sub = functional_value(spec, sb.run(ns, N_DIAG, derive_seed(item.seed_world, 5)))
            except Exception as exc:  # noqa: BLE001
                rows.append((i, item, p_truth, None, str(exc)[:60]))
                continue
            rows.append((i, item, p_truth, p_sub, ""))

    print(f"trace: {trace_path.name}  R={tr['R']}  R_uncl={tr['R_unclipped']:+.3f}")
    print("n_cal  |dP| mean   max   items>floor")
    for nc in sorted({it.regime.context["n_cal"] for it in battery.items}):
        dps = [abs(ps - pt) for (_, it, pt, ps, _) in rows
               if it.regime.context["n_cal"] == nc and ps is not None]
        over = sum(1 for d in dps if d > FLOOR)
        print(f"{nc:>5.0f}  {np.mean(dps):9.3f} {np.max(dps):6.3f}   {over}/{len(dps)}")
    worst = sorted((r for r in rows if r[3] is not None), key=lambda r: -abs(r[3] - r[2]))[:4]
    print("worst items:")
    for i, item, pt, ps, _ in worst:
        mix = world.lot_mix(item.seed_world)
        print(f"  item{i}: dose={item.regime.config['dose']} n_cal={item.regime.context['n_cal']:.0f} "
              f"mix={mix:+.2f}  P_truth={pt:.3f} P_sub={ps:.3f} |dP|={abs(ps - pt):.3f}")


def _ns(regime):
    from types import SimpleNamespace
    return SimpleNamespace(config=dict(regime.config), context=dict(regime.context),
                           horizon=regime.horizon)


if __name__ == "__main__":
    main()
