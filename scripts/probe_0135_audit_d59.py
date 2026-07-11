"""Audit cero-LLM (ADR 0135 paso 2, Codex r12): are D59's defects COBRABLE?

Takes the real D59 delivery (R=0.9866 with defects), repairs its two annotated
defect families one at a time, and scores every variant BOTH ways:
  - R against the case's REAL battery (production path, server.submit)
  - regret_trans against the frozen conformity suite (fidelity scale)

If repairs move conformity but NOT production R -> the case battery is
insufficient for these defects (the exact mechanism of the fork's decoupling),
and the separating conformity regimes are the design coordinates for future
batteries. If NO possible regime separates -> behavioral equivalence: the
"defect" is one of justification, not of gradeable performance.

Run: .venv/Scripts/python scripts/probe_0135_audit_d59.py
"""

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))

from probe_0135_build import Conformity, EQUIVALENTS, reference_code, TRUTH_MANIFEST  # noqa: E402
from wager.harness.case_episode import build_world_server  # noqa: E402

CASE = ROOT / "cases" / "first_story_scarce_v0"
CELL = ROOT / "scripts" / "out" / "fork_0133" / "cell_b4_d59_neutral.json"
OUT = ROOT / "scripts" / "out" / "probe_0135" / "audit_d59.json"

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ORIGINAL = json.loads(CELL.read_text(encoding="utf-8"))["submission_code"]

# --- repair (d): fixed humidity=5.0 default -> the historical hall distribution
# D59 itself measured (N(5.18, 1.94) from the HVAC log) in its sibling deliveries.
FIX_D = ORIGINAL.replace(
    '    humidity = regime.config.get("humidity", 5.0)',
    '    if "humidity" in regime.config:\n'
    '        humidity = regime.config["humidity"]\n'
    '    else:\n'
    '        humidity = np.clip(rng.normal(5.18, 1.94, n), 2.0, 8.0)'
)

# --- repair (ruido): total residual 4.0008 used as process noise -> decompose
# out the measured meter (1.81): sqrt(4.0008^2 - 1.81^2) = 3.568
FIX_NOISE = ORIGINAL.replace(
    "    noise_o_std = 4.0008",
    "    noise_o_std = 3.568  # sqrt(4.0008**2 - 1.81**2): process only, meter removed"
)

BOTH = FIX_D.replace(
    "    noise_o_std = 4.0008",
    "    noise_o_std = 3.568  # sqrt(4.0008**2 - 1.81**2): process only, meter removed"
)

VARIANTS = {
    "original_R0.9866": ORIGINAL,
    "fix_d_historical_humidity": FIX_D,
    "fix_noise_decomposed": FIX_NOISE,
    "fix_both": BOTH,
    "reference_truth": reference_code(TRUTH_MANIFEST),
}


def main() -> None:
    print("Calibrating conformity floors ...", flush=True)
    conf = Conformity(reference_code(TRUTH_MANIFEST))
    conf.set_floors([conf.raw_distances(c, rep_seed=10 + i) for i, c in enumerate(EQUIVALENTS)])

    results = {}
    for name, code in VARIANTS.items():
        server = build_world_server(CASE, seed_offset=59)
        res = server.submit(code)
        R = server.result.get("R") if res.accepted else None
        R_uncl = server.result.get("R_unclipped") if res.accepted else None
        reg = conf.regret(code, rep_seed=555)
        results[name] = {"R_battery": R, "R_uncl": R_uncl,
                         "regret_mean": reg["regret_mean"], "regret_max": reg["regret_max"],
                         "per_regime": reg["per_regime"]}
        print(f"  {name:28}: R={R:.4f}  regret_mean={reg['regret_mean']:8.2f}  "
              f"regret_max={reg['regret_max']:8.2f}", flush=True)

    OUT.write_text(json.dumps(results, indent=2) + "\n", encoding="utf-8")
    print(f"\nwrote {OUT}")


if __name__ == "__main__":
    main()
