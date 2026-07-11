"""Probe 0135 build (zero-LLM): manifest, reference, equivalents, conformity suite, tau.

Pieces (ADR 0135, Codex r12 design), all derived from the TRUTH of
first_story_scarce_v0 -- server-side, the agent never sees this file:

- DELIVERY_SPEC_V1: unambiguous delivery contract (fixes the process-vs-meter bug).
- MANIFEST: lossless belief description auto-rendered from world PARAMS (stage-1 = truth).
- reference_code(manifest): deterministic manifest->program translation (the ceiling).
- equivalents(): K correct implementations (style/RNG/rounding variation) -> tau.
- CONFORMITY: frozen regime suite; regret_trans(code) = mean_i D_i(sub, ref)/D_i(null, ref).

Run: .venv/Scripts/python scripts/probe_0135_build.py   (writes scripts/out/probe_0135/)
"""

import json
import sys
from pathlib import Path
from types import SimpleNamespace

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from wager.reward.distance import TruthSide  # noqa: E402
from wager.reward.sandbox import SandboxedSubmission  # noqa: E402
from wager.reward.seeds import derive_seed  # noqa: E402

OUT = ROOT / "scripts" / "out" / "probe_0135"
COLUMNS = ["feedstock", "outcome"]
N_CONF = 6000          # samples per side per regime
M_REPS = 2             # submission-side reps averaged (as production does)
BASE_SEED = 424242

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

# --------------------------------------------------------------------------
# DeliverySpec v1 -- the frozen, unambiguous contract (fixes process-vs-meter)
# --------------------------------------------------------------------------
DELIVERY_SPEC_V1 = """DELIVERY CONTRACT (v1) -- read carefully; every clause is graded.

Deliver ONE python code string defining:  model(regime, n, seed) -> pandas.DataFrame

1. OUTPUT: a DataFrame with columns exactly ['feedstock', 'outcome'], exactly n rows,
   finite floats. `regime.config` is a dict; `seed` is an integer.
2. WHAT model() MUST GENERATE: the PROCESS distribution -- the true per-unit values,
   BEFORE any measurement instrument. Do NOT add instrument/meter error to the output.
   (Instrument error exists only in the readings served by observe()/experiment()
   during an investigation; the deliverable models the plant, not the meter.)
3. KNOB SEMANTICS: regime.config may contain any subset of
   {feedstock_grade, humidity, temp, line_speed}.
   - If a knob IS present: the process runs with that knob held at the given value
     for all n units.
   - If a knob is ABSENT: that knob is NOT held -- the process runs with that factor
     behaving as it does historically/ambiently (its natural distribution across
     units, as described in the belief you are implementing).
   - An EMPTY config means: the historical/observational process, exactly as the era
     that produced the records.
4. RANDOMNESS: use ONLY numpy randomness seeded from `seed`
   (np.random.default_rng(seed) or equivalent). Same (regime, n, seed) -> same table.
5. Per-unit heterogeneity is real: units differ by process noise and by any
   historically-varying factors. Do not collapse distributions to their means.
6. Implement EXACTLY the belief specified in the MODEL SPEC you were given -- even
   where you would personally disagree. Fidelity to the spec is what is graded.
"""

# --------------------------------------------------------------------------
# Manifest: lossless belief spec. Stage 1 = the truth of first_story_scarce_v0.
# --------------------------------------------------------------------------
TRUTH_MANIFEST = {
    "name": "truth",
    "outputs": ["feedstock", "outcome"],
    "latents": {
        "t": "era position; historically t ~ Uniform(0,1) per unit; under ANY config that sets humidity, t = 0 for all units",
        "ambient": "hall condition; historically ambient = 2.0 + 6.0*t + Normal(0, 0.5) per unit; if humidity is set: ambient = humidity + Normal(0, 0.5) per unit",
        "u": "unit-level latent quality factor; u ~ Normal(0, 1) per unit, ALWAYS (every regime)",
        "grade": "supplier grade; if feedstock_grade is set: grade = that exact value (no noise); historically grade ~ Normal(5, 1) clipped to [0, 10] per unit",
    },
    "equations": {
        "feedstock": "6.0 + 1.0*(grade - 5.0) - 0.9*(ambient - 5.0) + Normal(0, 0.9)",
        "outcome": "30.0 - 2.5*(ambient - 5.0) + 3.0*u + Normal(0, 2.0)",
    },
    "notes": [
        "feedstock_grade does NOT enter the outcome equation at all (no direct or indirect effect on outcome).",
        "temp and line_speed affect NOTHING (no equation reads them).",
        "all Normal(mu, sd) noises are fresh independent per-unit draws.",
    ],
}


def render_manifest(m: dict) -> str:
    lines = [f"MODEL SPEC ('{m['name']}') -- implement EXACTLY this belief.",
             "", "Outputs (the DataFrame columns): " + ", ".join(m["outputs"]), "",
             "Per-unit generative process:"]
    for name, desc in m["latents"].items():
        lines.append(f"  {name}: {desc}")
    lines.append("")
    for col, eq in m["equations"].items():
        lines.append(f"  {col} = {eq}")
    lines.append("")
    for note in m["notes"]:
        lines.append(f"NOTE: {note}")
    return "\n".join(lines)


# --------------------------------------------------------------------------
# Reference: deterministic manifest->program translation (the ceiling)
# --------------------------------------------------------------------------
def reference_code(m: dict) -> str:
    # For this probe the manifests share the first_story structure with varying
    # coefficients; stage-2 degraded manifests override the equations dict.
    return '''
import numpy as np
import pandas as pd

def model(regime, n, seed):
    rng = np.random.default_rng(seed)
    cfg = regime.config
    u = rng.normal(0.0, 1.0, n)
    if "humidity" in cfg:
        ambient = float(cfg["humidity"]) + rng.normal(0.0, 0.5, n)
    else:
        t = rng.uniform(0.0, 1.0, n)
        ambient = 2.0 + 6.0 * t + rng.normal(0.0, 0.5, n)
    if "feedstock_grade" in cfg:
        grade = np.full(n, float(cfg["feedstock_grade"]))
    else:
        grade = np.clip(rng.normal(5.0, 1.0, n), 0.0, 10.0)
    feedstock = 6.0 + 1.0 * (grade - 5.0) - 0.9 * (ambient - 5.0) + rng.normal(0.0, 0.9, n)
    outcome = 30.0 - 2.5 * (ambient - 5.0) + 3.0 * u + rng.normal(0.0, 2.0, n)
    return pd.DataFrame({"feedstock": feedstock, "outcome": outcome})
'''


# K correct-but-different implementations of the SAME truth manifest: RNG family,
# draw order, combined vs separate noises, rounded coefficients. Distributionally
# equivalent -- their conformity regret defines the implementation-noise floor.
EQUIVALENTS: list[str] = [
    # 1: RandomState instead of default_rng, same structure
    '''
import numpy as np
import pandas as pd

def model(regime, n, seed):
    rng = np.random.RandomState(seed)
    cfg = regime.config
    u = rng.normal(0.0, 1.0, n)
    if "humidity" in cfg:
        ambient = float(cfg["humidity"]) + rng.normal(0.0, 0.5, n)
    else:
        ambient = 2.0 + 6.0 * rng.uniform(0.0, 1.0, n) + rng.normal(0.0, 0.5, n)
    if "feedstock_grade" in cfg:
        grade = np.full(n, float(cfg["feedstock_grade"]))
    else:
        grade = np.clip(rng.normal(5.0, 1.0, n), 0.0, 10.0)
    feedstock = 6.0 + (grade - 5.0) - 0.9 * (ambient - 5.0) + rng.normal(0.0, 0.9, n)
    outcome = 30.0 - 2.5 * (ambient - 5.0) + 3.0 * u + rng.normal(0.0, 2.0, n)
    return pd.DataFrame({"feedstock": feedstock, "outcome": outcome})
''',
    # 2: combined outcome noise sqrt(9+4) in ONE draw (u marginalized)
    '''
import numpy as np
import pandas as pd

def model(regime, n, seed):
    rng = np.random.default_rng(seed)
    cfg = regime.config
    if "humidity" in cfg:
        ambient = float(cfg["humidity"]) + rng.normal(0.0, 0.5, n)
    else:
        ambient = 2.0 + 6.0 * rng.uniform(0.0, 1.0, n) + rng.normal(0.0, 0.5, n)
    if "feedstock_grade" in cfg:
        grade = np.full(n, float(cfg["feedstock_grade"]))
    else:
        grade = np.clip(rng.normal(5.0, 1.0, n), 0.0, 10.0)
    feedstock = 6.0 + 1.0 * (grade - 5.0) - 0.9 * (ambient - 5.0) + rng.normal(0.0, 0.9, n)
    outcome = 30.0 - 2.5 * (ambient - 5.0) + rng.normal(0.0, np.sqrt(13.0), n)
    return pd.DataFrame({"feedstock": feedstock, "outcome": outcome})
''',
    # 3: different draw order (grade first), separate rng streams per block
    '''
import numpy as np
import pandas as pd

def model(regime, n, seed):
    rng = np.random.default_rng(seed)
    cfg = regime.config
    if "feedstock_grade" in cfg:
        grade = np.full(n, float(cfg["feedstock_grade"]))
    else:
        grade = np.clip(rng.normal(5.0, 1.0, n), 0.0, 10.0)
    if "humidity" in cfg:
        ambient = float(cfg["humidity"]) + rng.normal(0.0, 0.5, n)
    else:
        t = rng.uniform(0.0, 1.0, n)
        ambient = 2.0 + 6.0 * t + rng.normal(0.0, 0.5, n)
    fs_mu = 6.0 + 1.0 * (grade - 5.0) - 0.9 * (ambient - 5.0)
    out_mu = 30.0 - 2.5 * (ambient - 5.0)
    feedstock = rng.normal(fs_mu, 0.9)
    outcome = rng.normal(out_mu + 3.0 * rng.normal(0.0, 1.0, n), 2.0)
    return pd.DataFrame({"feedstock": feedstock, "outcome": outcome})
''',
    # 4: rounded coefficients to 2 decimals (a faithful but rounded translation)
    '''
import numpy as np
import pandas as pd

def model(regime, n, seed):
    rng = np.random.default_rng(seed)
    cfg = regime.config
    u = rng.normal(0.0, 1.0, n)
    if "humidity" in cfg:
        ambient = float(cfg["humidity"]) + rng.normal(0.0, 0.5, n)
    else:
        ambient = 2.0 + 6.0 * rng.uniform(0.0, 1.0, n) + rng.normal(0.0, 0.5, n)
    if "feedstock_grade" in cfg:
        grade = np.full(n, float(cfg["feedstock_grade"]))
    else:
        grade = np.clip(rng.normal(5.0, 1.0, n), 0.0, 10.0)
    feedstock = 6.0 + 1.0 * (grade - 5.0) - 0.9 * (ambient - 5.0) + rng.normal(0.0, 0.9, n)
    outcome = 30.0 - 2.5 * (ambient - 5.0) + 3.0 * u + rng.normal(0.0, 2.0, n)
    df = pd.DataFrame({"feedstock": np.round(feedstock, 2), "outcome": np.round(outcome, 2)})
    return df
''',
    # 5: loop-free but computes t even when humidity set (extra unused draw)
    '''
import numpy as np
import pandas as pd

def model(regime, n, seed):
    rng = np.random.default_rng(seed)
    cfg = regime.config
    t = rng.uniform(0.0, 1.0, n)
    amb_noise = rng.normal(0.0, 0.5, n)
    if "humidity" in cfg:
        ambient = float(cfg["humidity"]) + amb_noise
    else:
        ambient = 2.0 + 6.0 * t + amb_noise
    if "feedstock_grade" in cfg:
        grade = np.full(n, float(cfg["feedstock_grade"]))
    else:
        grade = np.clip(rng.normal(5.0, 1.0, n), 0.0, 10.0)
    u = rng.normal(0.0, 1.0, n)
    feedstock = 6.0 + 1.0 * (grade - 5.0) - 0.9 * (ambient - 5.0) + rng.normal(0.0, 0.9, n)
    outcome = 30.0 - 2.5 * (ambient - 5.0) + 3.0 * u + rng.normal(0.0, 2.0, n)
    return pd.DataFrame({"feedstock": feedstock, "outcome": outcome})
''',
    # 6: RandomState + combined noise + rounded 3 decimals
    '''
import numpy as np
import pandas as pd

def model(regime, n, seed):
    rng = np.random.RandomState(seed)
    cfg = regime.config
    if "humidity" in cfg:
        ambient = float(cfg["humidity"]) + rng.normal(0.0, 0.5, n)
    else:
        ambient = 2.0 + 6.0 * rng.uniform(0.0, 1.0, n) + rng.normal(0.0, 0.5, n)
    if "feedstock_grade" in cfg:
        grade = float(cfg["feedstock_grade"]) * np.ones(n)
    else:
        grade = np.clip(rng.normal(5.0, 1.0, n), 0.0, 10.0)
    feedstock = np.round(6.0 + (grade - 5.0) - 0.9 * (ambient - 5.0) + rng.normal(0.0, 0.9, n), 3)
    outcome = np.round(30.0 - 2.5 * (ambient - 5.0) + rng.normal(0.0, 13.0 ** 0.5, n), 3)
    return pd.DataFrame({"feedstock": feedstock, "outcome": outcome})
''',
    # 7: generates in two halves and concatenates (chunked implementation)
    '''
import numpy as np
import pandas as pd

def model(regime, n, seed):
    def gen(k, rng):
        cfg = regime.config
        u = rng.normal(0.0, 1.0, k)
        if "humidity" in cfg:
            ambient = float(cfg["humidity"]) + rng.normal(0.0, 0.5, k)
        else:
            ambient = 2.0 + 6.0 * rng.uniform(0.0, 1.0, k) + rng.normal(0.0, 0.5, k)
        if "feedstock_grade" in cfg:
            grade = np.full(k, float(cfg["feedstock_grade"]))
        else:
            grade = np.clip(rng.normal(5.0, 1.0, k), 0.0, 10.0)
        fs = 6.0 + 1.0 * (grade - 5.0) - 0.9 * (ambient - 5.0) + rng.normal(0.0, 0.9, k)
        out = 30.0 - 2.5 * (ambient - 5.0) + 3.0 * u + rng.normal(0.0, 2.0, k)
        return fs, out
    rng = np.random.default_rng(seed)
    h = n // 2
    f1, o1 = gen(h, rng)
    f2, o2 = gen(n - h, rng)
    return pd.DataFrame({"feedstock": np.concatenate([f1, f2]),
                         "outcome": np.concatenate([o1, o2])})
''',
    # 8: standard-normal reparametrization (mu + sd*z draws)
    '''
import numpy as np
import pandas as pd

def model(regime, n, seed):
    rng = np.random.default_rng(seed)
    cfg = regime.config
    z1, z2, z3, z4 = (rng.standard_normal(n) for _ in range(4))
    if "humidity" in cfg:
        ambient = float(cfg["humidity"]) + 0.5 * z1
    else:
        ambient = 2.0 + 6.0 * rng.uniform(0.0, 1.0, n) + 0.5 * z1
    if "feedstock_grade" in cfg:
        grade = np.full(n, float(cfg["feedstock_grade"]))
    else:
        grade = np.clip(5.0 + 1.0 * rng.standard_normal(n), 0.0, 10.0)
    feedstock = 6.0 + 1.0 * (grade - 5.0) - 0.9 * (ambient - 5.0) + 0.9 * z2
    outcome = 30.0 - 2.5 * (ambient - 5.0) + 3.0 * z3 + 2.0 * z4
    return pd.DataFrame({"feedstock": feedstock, "outcome": outcome})
''',
]

# --------------------------------------------------------------------------
# Conformity suite: frozen regimes covering the whole contract surface
# --------------------------------------------------------------------------
CONFORMITY_REGIMES: list[dict] = [
    {},                                                        # empty = historical
    {"feedstock_grade": 0.0},
    {"feedstock_grade": 10.0},
    {"humidity": 2.0},
    {"humidity": 8.0},
    {"feedstock_grade": 5.0, "humidity": 5.0},
    {"feedstock_grade": 8.0, "humidity": 5.0},                 # smoke regime 1
    {"humidity": 7.0},                                         # smoke regime 2
    {"temp": 8.0},                                             # decoy alone = historical
    {"line_speed": 2.0, "temp": 2.0},                          # decoys only
    {"feedstock_grade": 10.0, "humidity": 2.0, "temp": 8.0, "line_speed": 2.0},
    {"feedstock_grade": 0.0, "humidity": 8.0},
]


def _ns(config: dict) -> SimpleNamespace:
    return SimpleNamespace(config=dict(config), context={}, horizon=None)


class Conformity:
    """Frozen suite vs a reference program. Fidelity scale: the floor of each
    regime is the MEDIAN distance of correct-but-different implementations
    (the implementation/sampling noise); regret_i = d_i / floor_i, i.e. "how
    many times the noise of a correct translation away is this delivery".
    Equivalents sit at ~1 by construction; defects must stand above tau."""

    def __init__(self, ref_code: str, base_seed: int = BASE_SEED) -> None:
        self.truth_sides: list[TruthSide] = []
        self.regimes = [_ns(c) for c in CONFORMITY_REGIMES]
        self.floors: list[float] | None = None
        with SandboxedSubmission(ref_code, COLUMNS, timeout_s=20.0) as sb:
            for i, ns in enumerate(self.regimes):
                ref = sb.run(ns, N_CONF, derive_seed(base_seed, 2 * i))
                self.truth_sides.append(TruthSide(ref, COLUMNS))

    def raw_distances(self, code: str, rep_seed: int = 1) -> list[float]:
        out: list[float] = []
        with SandboxedSubmission(code, COLUMNS, timeout_s=20.0) as sb:
            for i, ns in enumerate(self.regimes):
                ds = [float(self.truth_sides[i].distance_to(
                    sb.run(ns, N_CONF, derive_seed(BASE_SEED + rep_seed, 100 + 20 * j + i))))
                    for j in range(M_REPS)]
                out.append(float(np.mean(ds)))
        return out

    def set_floors(self, equivalent_distances: list[list[float]]) -> None:
        arr = np.array(equivalent_distances)          # (K, n_regimes)
        self.floors = [max(float(m), 1e-9) for m in np.median(arr, axis=0)]

    def regret_from_raw(self, raw: list[float]) -> dict:
        assert self.floors is not None
        per = [d / f for d, f in zip(raw, self.floors)]
        return {"regret_mean": float(np.mean(per)), "regret_max": float(np.max(per)),
                "per_regime": per}

    def regret(self, code: str, rep_seed: int = 1) -> dict:
        return self.regret_from_raw(self.raw_distances(code, rep_seed))


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "DELIVERY_SPEC_v1.md").write_text(DELIVERY_SPEC_V1, encoding="utf-8")
    (OUT / "manifest_truth.json").write_text(json.dumps(TRUTH_MANIFEST, indent=2), encoding="utf-8")
    (OUT / "manifest_truth.md").write_text(render_manifest(TRUTH_MANIFEST), encoding="utf-8")
    ref = reference_code(TRUTH_MANIFEST)
    (OUT / "reference_truth.py").write_text(ref, encoding="utf-8")

    print("Building conformity suite against the reference ...", flush=True)
    conf = Conformity(ref)

    # sanity: the reference vs the REAL world.sample (distributional identity check)
    print("Raw distances of the equivalents (floor calibration) ...", flush=True)
    sys.path.insert(0, str(ROOT / "cases" / "first_story_scarce_v0"))
    import world as truth_world  # noqa: E402
    equiv_raw: list[list[float]] = []
    for k, code in enumerate(EQUIVALENTS):
        equiv_raw.append(conf.raw_distances(code, rep_seed=10 + k))
    # the real world.sample counts as one more correct implementation
    world_raw = []
    for i, ns in enumerate(conf.regimes):
        ds = [float(conf.truth_sides[i].distance_to(
            truth_world.sample(ns, N_CONF, derive_seed(BASE_SEED + 7 + j, 300 + i))[COLUMNS]))
            for j in range(M_REPS)]
        world_raw.append(float(np.mean(ds)))
    equiv_raw.append(world_raw)
    conf.set_floors(equiv_raw)

    means, maxes, rows = [], [], []
    for k, raw in enumerate(equiv_raw):
        r = conf.regret_from_raw(raw)
        means.append(r["regret_mean"])
        maxes.append(r["regret_max"])
        rows.append({"equivalent": k + 1, **r})
        label = "world.sample" if k == len(equiv_raw) - 1 else f"equivalent {k+1}"
        print(f"  {label:14}: mean={r['regret_mean']:.3f} max={r['regret_max']:.3f}")

    tau_mean = max(2.0, float(np.quantile(means, 0.95)))
    tau_max = max(3.0, float(np.quantile(maxes, 0.95)))
    print(f"\nTAU_MEAN = {tau_mean:.3f}   TAU_MAX = {tau_max:.3f}  (unidades: veces el piso de implementacion)")

    # --- separation panel: the metric MUST separate the fork's real defect
    # families from the implementation floor, or it cannot arbitrate the probe.
    DEFECTIVE = {
        "fixed5_historical": reference_code(TRUTH_MANIFEST).replace(
            "        t = rng.uniform(0.0, 1.0, n)\n        ambient = 2.0 + 6.0 * t + rng.normal(0.0, 0.5, n)",
            "        ambient = 5.0 + rng.normal(0.0, 0.5, n)"),
        "meter_added": reference_code(TRUTH_MANIFEST).replace(
            "    return pd.DataFrame({\"feedstock\": feedstock, \"outcome\": outcome})",
            "    outcome = outcome + rng.normal(0.0, 1.5, n)\n"
            "    return pd.DataFrame({\"feedstock\": feedstock, \"outcome\": outcome})"),
        "grade_into_outcome": reference_code(TRUTH_MANIFEST).replace(
            "    outcome = 30.0 - 2.5 * (ambient - 5.0) + 3.0 * u + rng.normal(0.0, 2.0, n)",
            "    outcome = 30.0 - 0.464 * (grade - 5.0) - 2.5 * (ambient - 5.0) + 3.0 * u + rng.normal(0.0, 2.0, n)"),
    }
    sep = {}
    print("\nSeparation panel (defective implementations, must exceed tau):")
    for name, code in DEFECTIVE.items():
        r = conf.regret(code, rep_seed=77)
        sep[name] = r
        flag = "SEPARATES" if (r["regret_mean"] > tau_mean or r["regret_max"] > tau_max) else "!!NO-SEP!!"
        print(f"  {name:22}: mean={r['regret_mean']:.4f} max={r['regret_max']:.4f}  [{flag}]")

    (OUT / "tau.json").write_text(json.dumps({
        "tau_mean": tau_mean, "tau_max": tau_max,
        "equivalent_means": means, "equivalent_maxes": maxes,
        "n_conf": N_CONF, "m_reps": M_REPS, "regimes": CONFORMITY_REGIMES,
        "detail": rows, "separation_panel": sep,
    }, indent=2), encoding="utf-8")
    print(f"\nwrote {OUT}")


if __name__ == "__main__":
    main()
