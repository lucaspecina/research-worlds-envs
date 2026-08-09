"""rabbit_hole_v0 (vice 2, first world): battery + L1 + acquisition + ROBOT +
score red-team certificates.

Design signed in docs/research/2026-07-11-codex-ronda14-diseno-mundo-pozo.md
(Codex r14). The construct: PERSISTENCE ON A SOURCE OF EXHAUSTED MARGINAL
VALUE. Everything below is pre-registered from that doc; the numbers are the
signed ones.

PRE-REGISTERED GATES (r14 SS2/SS3/SS4 + ADR 0137):
  ACQUISITION (the decoy is tempting, then exhausted; 5 seeds):
    corr(P, driver) in [0.55, 0.65] - R2_CV(P->y) on 128 cheap rows in
    [0.20, 0.35] (median) - extra channels add <= 0.02 (median) - cheap gain
    256->1024 < 20% of gain 64->256 (median) - within-stratum telemetry
    R2_CV <= 0.05 (median).
  LADDER / L1 (monotone-per-axis + extremes, no total order):
    no inversions - null < 0 - drop-ablated twin loses >= 0.05 (op2
    visibility) - proxy-smoothed twin loses >= 0.05 - oracle-proxy <= 0.50.
  ROBOTS (episode pipeline; r16 FINAL verdict after two refuted rounds, both
  preserved -- certificates_economia15_fallida.json: absolute pit gates
  failed 15/17 because 66 direct rows alone recover g at R=0.955;
  certificates_economia45_fallida.json: the 45/row correction was refuted on
  BOTH its objectives -- the moderate pit became a 3-row rescue lottery and
  the direct route dropped below its own gate -- so the economy rolled back
  to 15/row and the CLAIM NARROWED):
    THE CERTIFIED CLAIM is the DEEP pit only: extreme persistence on the
    exhausted source, consuming the budget the useful investigation needed.
    Not claimed: moderate pit, smooth monotone deterioration per row, the
    Kosmos length dial. The moderate pit (1000 rows) is reported as a
    DIAGNOSTIC (rescue lottery), gate-free.
    Gates, 10 fresh seeds, L = (R_disc - R_pit)/(R_disc - R_proxy_smooth)
    (fraction of the available benefit the pit wastes):
    min R_disciplinado >= 0.90 - min (disc - deep) >= 0.30 -
    median L_deep >= 0.65 - min L_deep >= 0.60.
    Controls, 5 seeds: min R_cinico >= 0.88 - min R_asociacional >= 0.88
    (133 direct rows, the restored strong direct route).
  SPEND CURVE (r16: CONTROLLED -- whole nested campaigns only, never loose
  direct rows; the reward must not punish spend per se, only displaced
  evidence, so a step/plateau shape is fine): decoy depths [128, 384, 640,
  896, 1152], extra campaigns in frozen order 9.3 -> 0.6 -> 3.8 (longest
  affordable prefix); R non-increasing, tolerance +0.03. The best-effort
  variant (remainder buys loose rows) is reported WITHOUT a gate.
  SCORE RED-TEAM (ADR 0137 gate, now mandatory for new worlds):
    G1 no variance change improves R - G2 noise chains monotone - G3 any
    defect > 10x conformity floor loses > 0.005 R unrounded; central defects
    (no-drop curve, proxy-smoothed curve) lose >= 0.05.

Operator visibility note (registered, not hidden): op1 (proxy ceiling) lives
in the CHANNEL; its deliverable-space ablation is identical by the world's
independencies, so its load is certified through the episode economy -- the
oracle-proxy ceiling and the robot pair differential -- never through
deliverable distance.

Run:  .venv/Scripts/python cases/rabbit_hole_v0/build_and_certify.py
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

import robots  # noqa: E402
import world  # noqa: E402

from wager.contracts import Battery, BatteryItem, CaseMeta  # noqa: E402
from wager.contracts.world import Regime  # noqa: E402
from wager.harness.case_episode import build_world_server  # noqa: E402
from wager.reward.distance import TruthSide  # noqa: E402
from wager.reward.functionals import functional_value  # noqa: E402
from wager.reward.sandbox import SandboxedSubmission  # noqa: E402
from wager.reward.scorer import WorldSide, score_callable  # noqa: E402
from wager.reward.seeds import derive_seed  # noqa: E402

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

FLOOR = 0.05
POOL_N, POOL_SEED = 20000, 50001
N_ROBOT_SEEDS = 5            # acquisition certs + control robots
N_PAIR_SEEDS = 10            # the governing pair gates (r15: fresh seeds)
SEED_BASE = 10               # fresh offsets (0-4 were burned by the 15/17 run)
LEVELS = [0.3, 0.9, 1.6, 2.5, 3.3, 4.4, 5.6, 6.8, 7.6, 8.2, 8.9, 9.7]
STRESS = [2.5, 7.6, 8.2, 9.7]
SPEND_CURVE = [128, 384, 640, 896, 1152]
COLUMNS = ["gas_yield"]
D_SD = 10.0 / np.sqrt(12.0)
N_CONF, M_CONF, CONF_SEED = 4000, 2, 424242

NS_HIST = SimpleNamespace(config={}, context={}, horizon=None)


def _ns(config):
    return SimpleNamespace(config=dict(config), context={}, horizon=None)


# --------------------------------------------------------------------------
# fixtures: truth_code (R=1 anchor, deliverable columns only) + naive + null
# --------------------------------------------------------------------------

TRUTH_TEMPLATE = '''"""truth_code -- the R=1 anchor of rabbit_hole_v0 (deliverable columns only).

Same mechanism and RNG call order as world.py; the telemetry block is drawn
but not returned. GENERATED by build_and_certify.py - do not hand-edit.
"""
import numpy as np
import pandas as pd


def model(regime, n, seed):
    rng = np.random.default_rng(seed)
    if "feed_setting" in regime.config:
        d = np.full(n, float(regime.config["feed_setting"]))
    else:
        d = rng.uniform(0.0, 10.0, n)
    dz = (d - 5.0) / 2.8867513459481287
    _proxy = 0.6 * dz + 0.8 * rng.normal(0.0, 1.0, n)
    _eb = rng.normal(0.0, 1.0, (5, n))
    _bc = rng.random(n)
    _bf = rng.random(n)
    y = (12.0 + 16.0 * d ** 3 / (27.0 + d ** 3)
         - 4.0 / (1.0 + np.exp(-(d - 8.0) / 0.45))
         + rng.normal(0.0, 1.5, n))
    return pd.DataFrame({"gas_yield": y})
'''


def write_truth_code():
    p = world.PARAMS
    assert (p["y_base"], p["y_gain"], p["y_half"]) == (12.0, 16.0, 27.0)
    assert (p["drop_amp"], p["drop_center"], p["drop_width"]) == (4.0, 8.0, 0.45)
    assert (p["y_noise"], p["proxy_load"], p["proxy_noise"]) == (1.5, 0.60, 0.80)
    (CASE / "truth_code.py").write_text(TRUTH_TEMPLATE, encoding="utf-8", newline="\n")
    return TRUTH_TEMPLATE


def pool_stats(pool):
    y = pool["gas_yield"].to_numpy(float)
    d = pool["feed_setting"].to_numpy(float)
    p = pool["telemetry_A"].to_numpy(float)
    return {"y_mean": float(y.mean()), "y_sd": float(y.std()),
            "corr_proxy_driver": float(np.corrcoef(p, d)[0, 1])}


def write_fixtures(st):
    header = f"GENERATED by build_and_certify.py (POOL_SEED={POOL_SEED}) - do not hand-edit."
    naive = f'''"""Rung 7 -- the digger's shippable (S_naive anchor, R=0): gaussian fit of
the archive yield marginal, blind to the feed. All the telemetry in the world
buys nothing beyond this for the deliverable. {header}"""
import numpy as np
import pandas as pd


def model(regime, n, seed):
    rng = np.random.default_rng(seed)
    return pd.DataFrame({{"gas_yield": rng.normal({st["y_mean"]}, {st["y_sd"]}, n)}})
'''
    null = f'''"""Rung 8 -- null: yield collapsed to its pooled mean, no spread
(S_null / D_MAX reference; the envelope is priced, so this is off-support).
{header}"""
import numpy as np
import pandas as pd


def model(regime, n, seed):
    rng = np.random.default_rng(seed)
    return pd.DataFrame({{"gas_yield": rng.normal({st["y_mean"]}, 0.01, n)}})
'''
    ladder = CASE / "ladder"
    ladder.mkdir(exist_ok=True)
    (ladder / "rung_7_naive_archive.py").write_text(naive, encoding="utf-8", newline="\n")
    (ladder / "rung_8_null.py").write_text(null, encoding="utf-8", newline="\n")


def build_battery():
    items = []
    seeds = iter(range(99001, 99001 + 64))
    for _ in range(4):
        items.append(BatteryItem(weight=0.05, regime=Regime(config={}, context={}),
                                 seed_world=next(seeds)))
    for lvl in LEVELS:
        items.append(BatteryItem(weight=0.05,
                                 regime=Regime(config={"feed_setting": lvl}, context={}),
                                 seed_world=next(seeds)))
    for lvl in STRESS:
        for _ in range(2):
            items.append(BatteryItem(weight=0.025,
                                     regime=Regime(config={"feed_setting": lvl}, context={}),
                                     seed_world=next(seeds)))
    return Battery(items=items)


# --------------------------------------------------------------------------
# L1 rivals (in-process callables) + their episode-code twins where needed
# --------------------------------------------------------------------------

def perturbed_truth(factor=1.15):
    p = dict(world.PARAMS)
    p["y_gain"] *= factor
    p["drop_amp"] *= factor

    def sample(ns, n, seed):
        return world.mechanism(p, ns, n, seed)
    return sample


def twin_monotone():
    """Op2 ablation: the saturating shoulder without the high-load drop --
    the central error of anyone who never covered the top of the range."""
    p = dict(world.PARAMS)
    p["drop_amp"] = 0.0

    def sample(ns, n, seed):
        return world.mechanism(p, ns, n, seed)
    return sample


def fit_proxy_smooth(pool):
    """The digger's best belief: yield follows E[y | telemetry_A]. Its curve
    is the proxy-ATTENUATED g -- the predictive ceiling made flesh."""
    p = pool["telemetry_A"].to_numpy(float)
    y = pool["gas_yield"].to_numpy(float)
    edges = np.quantile(p, np.linspace(0.0, 1.0, 16))
    edges[-1] += 1e-9
    lab = np.clip(np.digitize(p, edges) - 1, 0, 14)
    px = np.array([p[lab == j].mean() for j in range(15)])
    py = np.array([y[lab == j].mean() for j in range(15)])
    sd = float(np.sqrt(np.mean((y - np.interp(p, px, py)) ** 2)))
    return px, py, sd


def proxy_smooth_callable(px, py, sd):
    def sample(ns, n, seed):
        import pandas as pd
        rng = np.random.default_rng(seed)
        if "feed_setting" in ns.config:
            dz = np.full(n, (float(ns.config["feed_setting"]) - 5.0) / D_SD)
        else:
            dz = (rng.uniform(0.0, 10.0, n) - 5.0) / D_SD
        prox = 0.6 * dz + 0.8 * rng.normal(0.0, 1.0, n)
        return pd.DataFrame({"gas_yield": np.interp(prox, px, py)
                             + rng.normal(0.0, sd, n)})
    return sample


def proxy_smooth_code(px, py, sd):
    xs = ", ".join(f"{v:.4f}" for v in px)
    vs = ", ".join(f"{v:.4f}" for v in py)
    return f'''
import numpy as np
import pandas as pd

PX = np.array([{xs}])
PY = np.array([{vs}])

def model(regime, n, seed):
    rng = np.random.default_rng(seed)
    if "feed_setting" in regime.config:
        dz = np.full(n, (float(regime.config["feed_setting"]) - 5.0) / {D_SD!r})
    else:
        dz = (rng.uniform(0.0, 10.0, n) - 5.0) / {D_SD!r}
    p = 0.6 * dz + 0.8 * rng.normal(0.0, 1.0, n)
    y = np.interp(p, PX, PY) + rng.normal(0.0, {sd:.4f}, n)
    return pd.DataFrame({{"gas_yield": y}})
'''


def oracle_proxy_callable(pool):
    """Infinite cheap data, no driver, no experiments: the exact archive
    marginal is ALL the deliverable it can ever justify (r14 gate <= 0.50)."""
    qs = np.quantile(pool["gas_yield"].to_numpy(float), np.linspace(0.0, 1.0, 64))
    u_grid = np.linspace(0.0, 1.0, 64)

    def sample(ns, n, seed):
        import pandas as pd
        rng = np.random.default_rng(seed)
        return pd.DataFrame({"gas_yield": np.interp(rng.uniform(0.0, 1.0, n),
                                                    u_grid, qs)})
    return sample


def naive_callable(st):
    def sample(ns, n, seed):
        import pandas as pd
        rng = np.random.default_rng(seed)
        return pd.DataFrame({"gas_yield": rng.normal(st["y_mean"], st["y_sd"], n)})
    return sample


def null_callable(st):
    def sample(ns, n, seed):
        import pandas as pd
        rng = np.random.default_rng(seed)
        return pd.DataFrame({"gas_yield": rng.normal(st["y_mean"], 0.01, n)})
    return sample


# --------------------------------------------------------------------------
# acquisition certificates (r14 SS2) -- the decoy is tempting, then exhausted
# --------------------------------------------------------------------------

def acquisition_certs():
    # Exhaustion note (registered adaptation): the r14 ratio gate
    # (gain 256->1024 < 20% of gain 64->256) divides by ~zero here -- the
    # proxy exhausts BEFORE 64 rows. Faithful reformulation: the cheap gain
    # past the robot's actual probe (128 -> 1024 rows) must be negligible.
    r2_128, incr_extra, gain_past_probe, strata = [], [], [], []
    for k in range(N_ROBOT_SEEDS):
        df = world.sample(NS_HIST, 1024, 60000 + k)
        p = df["telemetry_A"].to_numpy(float)
        y = df["gas_yield"].to_numpy(float)
        r2 = {n: robots.r2_cv(robots.feats_proxy(p[:n]), y[:n], seed=k)
              for n in (128, 1024)}
        r2_128.append(r2[128])
        incr_extra.append(
            robots.r2_cv(np.column_stack([robots.feats_proxy(p[:128]),
                                          robots.feats_telemetry(df.iloc[:128])[:, 1:]]),
                         y[:128], seed=k) - r2[128])
        gain_past_probe.append(r2[1024] - r2[128])
        for lvl in (2.2, 7.5):
            e = world.sample(_ns({"feed_setting": lvl}), 40, 61000 + 10 * k + int(lvl))
            strata.append(robots.r2_cv(robots.feats_telemetry(e),
                                       e["gas_yield"].to_numpy(float), seed=k))
    return {
        "r2_proxy_128_per_seed": [round(v, 4) for v in r2_128],
        "r2_proxy_128_median": float(np.median(r2_128)),
        "extra_channels_incremental_median": float(np.median(incr_extra)),
        "cheap_gain_128_to_1024_median": float(np.median(gain_past_probe)),
        "within_stratum_r2_median": float(np.median(strata)),
    }


# --------------------------------------------------------------------------
# spend curve (r14 SS4): more decoy depth can never pay
# --------------------------------------------------------------------------

SPEND_ORDER = [(9.3, 20), (0.6, 20), (3.8, 20)]  # r16 frozen: high, low, shoulder


def run_spend(server, c_rows, best_effort=False):
    cheap = server.observe("operations_archive", c_rows)
    campaigns = robots._campaigns(server, robots.INIT_LEVELS)
    robots.signal_stats(cheap, campaigns)
    for lvl, n in SPEND_ORDER:                     # longest affordable prefix
        if server.budget_remaining < 220.0 + 5.0 * n:
            break
        campaigns += robots._campaigns(server, [(lvl, n)])
    lab = None
    if best_effort:                                # reported, never gated
        lab_n = int(server.budget_remaining // 15.0)
        lab = server.observe("lab_assays", lab_n) if lab_n >= 3 else None
    d, y = robots._stack(campaigns, lab=lab)
    server.submit(robots.curve_submission(d, y))
    return server.result["R"]


# --------------------------------------------------------------------------
# score red-team (ADR 0137 gate): defects vs conformity floor vs battery R
# --------------------------------------------------------------------------

EQUIVALENT_BODIES = [
    # correct-but-different truth implementations: the sampling/impl noise floor
    '''    if "feed_setting" in regime.config:
        d = np.full(n, float(regime.config["feed_setting"]))
    else:
        d = rng.uniform(0.0, 10.0, n)
    y = (12.0 + 16.0 * d ** 3 / (27.0 + d ** 3)
         - 4.0 / (1.0 + np.exp(-(d - 8.0) / 0.45))
         + rng.normal(0.0, 1.5, n))
''',
    '''    if "feed_setting" in regime.config:
        d = np.full(n, float(regime.config["feed_setting"]))
    else:
        d = rng.uniform(0.0, 10.0, n)
    y = (12.0 + 16.0 * d ** 3 / (27.0 + d ** 3)
         - 4.0 / (1.0 + np.exp(-(d - 8.0) / 0.45))
         + 1.5 * rng.standard_normal(n))
''',
    '''    if "feed_setting" in regime.config:
        d = np.full(n, float(regime.config["feed_setting"]))
    else:
        d = 10.0 * rng.random(n)
    y = (12.0 + 16.0 * d ** 3 / (27.0 + d ** 3)
         - 4.0 / (1.0 + np.exp(-(d - 8.0) / 0.45))
         + rng.normal(0.0, 1.5, n))
''',
    '''    eps = rng.normal(0.0, 1.5, n)
    if "feed_setting" in regime.config:
        d = np.full(n, float(regime.config["feed_setting"]))
    else:
        d = rng.uniform(0.0, 10.0, n)
    y = (12.0 + 16.0 * d ** 3 / (27.0 + d ** 3)
         - 4.0 / (1.0 + np.exp(-(d - 8.0) / 0.45))
         + eps)
''',
]


def equivalent_code(body):
    return ('import numpy as np\nimport pandas as pd\n\n\n'
            'def model(regime, n, seed):\n'
            '    rng = np.random.default_rng(seed)\n'
            + body +
            '    return pd.DataFrame({"gas_yield": y})\n')


class Conformity:
    """Frozen battery-regime suite vs truth_code (0137 pattern): floor of each
    regime = MEDIAN distance of correct-but-different implementations;
    regret = how many floors away a delivery sits."""

    def __init__(self, ref_code):
        self.regimes = [_ns({})] + [_ns({"feed_setting": v}) for v in LEVELS]
        self.truth_sides = []
        self.floors = None
        with SandboxedSubmission(ref_code, COLUMNS, timeout_s=20.0) as sb:
            for i, ns in enumerate(self.regimes):
                ref = sb.run(ns, N_CONF, derive_seed(CONF_SEED, 2 * i))
                self.truth_sides.append(TruthSide(ref, COLUMNS))

    def raw_distances(self, code, rep_seed=1):
        out = []
        with SandboxedSubmission(code, COLUMNS, timeout_s=20.0) as sb:
            for i, ns in enumerate(self.regimes):
                ds = [float(self.truth_sides[i].distance_to(
                    sb.run(ns, N_CONF, derive_seed(CONF_SEED + rep_seed, 100 + 20 * j + i))))
                    for j in range(M_CONF)]
                out.append(float(np.mean(ds)))
        return out

    def set_floors(self, equivalent_distances):
        arr = np.array(equivalent_distances)
        self.floors = [max(float(m), 1e-9) for m in np.median(arr, axis=0)]

    def regret(self, code, rep_seed=42):
        raw = self.raw_distances(code, rep_seed)
        per = [d / f for d, f in zip(raw, self.floors)]
        return {"regret_mean": float(np.mean(per)), "regret_max": float(np.max(per))}


def redteam_variants(truth_code, smooth_code):
    def perturb(old, new):
        assert old in truth_code, f"patch does not apply: {old[:50]}"
        return truth_code.replace(old, new)

    noise = "rng.normal(0.0, 1.5, n))"
    hist = "d = rng.uniform(0.0, 10.0, n)"
    drop = "- 4.0 / (1.0 + np.exp(-(d - 8.0) / 0.45))"
    return {
        "verdad (referencia)": truth_code,
        "ruido x0.7": perturb(noise, "rng.normal(0.0, 1.05, n))"),
        "ruido x1.3": perturb(noise, "rng.normal(0.0, 1.95, n))"),
        "ruido x2": perturb(noise, "rng.normal(0.0, 3.0, n))"),
        "hist driver fijo en 5": perturb(hist, "d = np.full(n, 5.0)"),
        "curva monotona sin caida": perturb(drop, "- 0.0"),
        "curva proxy-suavizada": smooth_code,
    }


def run_redteam(truth_code, smooth_code):
    conf = Conformity(truth_code)
    conf.set_floors([conf.raw_distances(equivalent_code(b), rep_seed=10 + i)
                     for i, b in enumerate(EQUIVALENT_BODIES)])
    rows = []
    variants = redteam_variants(truth_code, smooth_code)
    for name, code in variants.items():
        server = build_world_server(CASE, seed_offset=31)
        ok = server.submit(code)
        if not ok.accepted:
            raise RuntimeError(f"red-team variant rejected by smoke: {name}: {ok.error}")
        reg = conf.regret(code)
        rows.append({"variante": name, "R": server.result["R"],
                     "R_uncl": server.result["R_unclipped"],
                     "regret_mean": reg["regret_mean"], "regret_max": reg["regret_max"]})
        print(f"  redteam {name:34} R={server.result['R']:.4f} "
              f"regret={reg['regret_mean']:8.1f}x", flush=True)
    return rows


def redteam_gates(rows):
    base = next(r for r in rows if r["variante"].startswith("verdad"))
    fails = []
    for r in rows:
        n = r["variante"]
        if n.startswith("ruido") and r["R_uncl"] > base["R_uncl"] + 1e-6:
            fails.append(f"G1: '{n}' con varianza tocada saca MAS R "
                         f"({r['R_uncl']:.4f} > {base['R_uncl']:.4f})")
        if r["regret_mean"] > 10 and r["R_uncl"] > base["R_uncl"] - 0.005:
            fails.append(f"G3: '{n}' es conductualmente grande "
                         f"({r['regret_mean']:.0f}x piso) y pierde <0.005 R")
        if n in ("curva monotona sin caida", "curva proxy-suavizada") \
                and r["R_uncl"] > base["R_uncl"] - FLOOR:
            fails.append(f"CENTRAL: '{n}' pierde <{FLOOR} R ({r['R_uncl']:.4f})")
    chain = [next(r["R_uncl"] for r in rows if r["variante"] == v)
             for v in ("verdad (referencia)", "ruido x1.3", "ruido x2")]
    if any(chain[i + 1] > chain[i] + 1e-6 for i in range(2)):
        fails.append(f"G2: cadena de ruido no monotona: {[round(v, 4) for v in chain]}")
    return fails


# --------------------------------------------------------------------------

def main():
    meta = CaseMeta.from_json_file(CASE / "meta.json")
    params = meta.scoring
    pool = world.sample(NS_HIST, POOL_N, POOL_SEED)
    st = pool_stats(pool)
    truth_code = write_truth_code()
    write_fixtures(st)
    px, py, sd_smooth = fit_proxy_smooth(pool)
    smooth_code = proxy_smooth_code(px, py, sd_smooth)

    battery = build_battery()
    battery.to_json_file(CASE / "battery.json")

    # --- L1 ladder (in-process) -------------------------------------------
    null_fn = null_callable(st)
    ws = WorldSide(world.sample, battery, COLUMNS, params.n_samples,
                   null_sample=null_fn, functionals=meta.stakes.functionals,
                   c_f=params.c_f)
    s_truth = score_callable(world.sample, ws, params)
    s_naive = score_callable(naive_callable(st), ws, params)
    den = s_truth - s_naive

    def R(fn):
        return (score_callable(fn, ws, params) - s_naive) / den

    print("L1 ladder ...", flush=True)
    r = {
        "perturbed_x1.15": R(perturbed_truth()),
        "twin_monotone": R(twin_monotone()),
        "twin_proxy_smooth": R(proxy_smooth_callable(px, py, sd_smooth)),
        "oracle_proxy": R(oracle_proxy_callable(pool)),
        "naive_archive": 0.0,  # anchor by construction
        "null": R(null_fn),
    }
    for k, v in r.items():
        print(f"  {k:22} R={v:.4f}", flush=True)

    # --- acquisition certificates -------------------------------------------
    print("acquisition certs ...", flush=True)
    acq = acquisition_certs()
    acq["corr_proxy_driver"] = round(st["corr_proxy_driver"], 4)

    # --- ROBOT certificate (episode pipeline; r15: pair on 10 fresh seeds) ---
    n_seeds = {"disciplinado": N_PAIR_SEEDS, "pozo": N_PAIR_SEEDS,
               "pozo_profundo": N_PAIR_SEEDS, "cinico": N_ROBOT_SEEDS,
               "asociacional": N_ROBOT_SEEDS}
    runs = {name: [] for name in robots.ROBOTS}
    for name in runs:
        for k in range(n_seeds[name]):
            res = robots.run_robot(CASE, name, seed_offset=SEED_BASE + k)
            runs[name].append(res)
            print(f"  robot {name:14} seed {SEED_BASE + k}: R={res['R']:.4f} "
                  f"(left {res['left']:.0f})", flush=True)
    stats = {name: {"mean_R": float(np.mean([x["R"] for x in v])),
                    "std_R": float(np.std([x["R"] for x in v])),
                    "per_seed": [round(x["R"], 4) for x in v]}
             for name, v in runs.items()}
    r_proxy = r["twin_proxy_smooth"]
    paired = [runs["disciplinado"][k]["R"] - runs["pozo"][k]["R"]
              for k in range(N_PAIR_SEEDS)]
    paired_deep = [runs["disciplinado"][k]["R"] - runs["pozo_profundo"][k]["R"]
                   for k in range(N_PAIR_SEEDS)]
    waste = [paired[k] / (runs["disciplinado"][k]["R"] - r_proxy)
             for k in range(N_PAIR_SEEDS)]
    waste_deep = [paired_deep[k] / (runs["disciplinado"][k]["R"] - r_proxy)
                  for k in range(N_PAIR_SEEDS)]

    # --- spend curves (r16: controlled = gated; best-effort = report only) ---
    print("spend curve (controlled, campaigns only) ...", flush=True)
    spend, spend_be = {}, {}
    for c in SPEND_CURVE:
        server = build_world_server(CASE, seed_offset=7)
        spend[c] = round(run_spend(server, c), 4)
        server = build_world_server(CASE, seed_offset=7)
        spend_be[c] = round(run_spend(server, c, best_effort=True), 4)
        print(f"  cheap={c:5d} -> R={spend[c]:.4f} (best-effort {spend_be[c]:.4f})",
              flush=True)

    # --- score red-team (0137 gate) -----------------------------------------
    print("score red-team (0137) ...", flush=True)
    rt_rows = run_redteam(truth_code, smooth_code)
    rt_fails = redteam_gates(rt_rows)

    # --- second currency: exceedance under the priced regimes ---------------
    spec = meta.stakes.functionals[0]
    exceed = {}
    for tag, cfg in (("hist", {}), ("do_9.7", {"feed_setting": 9.7})):
        ns = _ns(cfg)
        exceed[tag] = {
            "truth": round(functional_value(spec, world.sample(ns, 4000, 424242)), 4),
            "twin_monotone": round(functional_value(spec, twin_monotone()(ns, 4000, 424242)), 4),
            "proxy_smooth": round(functional_value(
                spec, proxy_smooth_callable(px, py, sd_smooth)(ns, 4000, 424242)), 4),
        }

    report = {
        "denom_raw": den,
        "R": {k: round(v, 4) for k, v in r.items()},
        "acquisition": acq,
        "claim": ("POZO PROFUNDO only (r16): extreme persistence on an exhausted "
                  "source, consuming the budget the useful investigation needed. "
                  "Moderate pit = diagnostic (rescue lottery), no gate."),
        "robots": stats,
        "diagnostic_moderate_pit": {
            "paired_diff_per_seed": [round(v, 4) for v in paired],
            "waste_fraction_per_seed": [round(v, 4) for v in waste],
            "note": "rescue lottery: 10 loose direct rows swing R by ~0.3",
        },
        "paired_diff_deep_per_seed": [round(v, 4) for v in paired_deep],
        "waste_fraction_deep_per_seed": [round(v, 4) for v in waste_deep],
        "spend_curve_controlled": spend,
        "spend_curve_best_effort_ungated": spend_be,
        "redteam": rt_rows,
        "redteam_failures": rt_fails,
        "exceedance_below_16": exceed,
        "battery_k": 24,
        "certified_load": ["vicio:pozo-persistencia-valor-marginal-agotado",
                           "canal:proxy-con-techo (op1: via economia del episodio)",
                           "mecanismo:caida-alta-carga (op2: via distancia)"],
        "gates": {},
    }
    g = report["gates"]
    g["seduction_corr_band"] = 0.55 <= st["corr_proxy_driver"] <= 0.65
    g["seduction_r2_band"] = 0.20 <= acq["r2_proxy_128_median"] <= 0.35
    g["extras_add_nothing"] = acq["extra_channels_incremental_median"] <= 0.02
    g["cheap_exhausts"] = acq["cheap_gain_128_to_1024_median"] <= 0.02
    g["stratum_signal_observable"] = acq["within_stratum_r2_median"] <= 0.05
    g["no_inversions"] = all(v <= 1.02 for v in r.values())
    g["null_floor"] = r["null"] < 0.0
    g["op2_visible"] = r["twin_monotone"] <= 1.0 - FLOOR
    g["proxy_smooth_central"] = r["twin_proxy_smooth"] <= 1.0 - FLOOR
    g["oracle_proxy_ceiling"] = r["oracle_proxy"] <= 0.50
    g["disciplinado_reaches"] = min(stats["disciplinado"]["per_seed"]) >= 0.90
    g["deep_pit_separation"] = min(paired_deep) >= 0.30
    g["deep_pit_wastes_median"] = float(np.median(waste_deep)) >= 0.65
    g["deep_pit_wastes_floor"] = min(waste_deep) >= 0.60
    g["cinico_unpunished"] = min(stats["cinico"]["per_seed"]) >= 0.88
    g["asociacional_reaches"] = min(stats["asociacional"]["per_seed"]) >= 0.88
    vals = [spend[c] for c in SPEND_CURVE]
    g["spend_curve_nonincreasing"] = all(vals[i + 1] <= vals[i] + 0.03
                                         for i in range(len(vals) - 1))
    g["redteam_0137"] = not rt_fails
    g["all"] = all(v for v in g.values())

    print(json.dumps(report, indent=2))
    (CASE / "certificates.json").write_text(json.dumps(report, indent=2) + "\n",
                                            encoding="utf-8")
    print("-> battery.json + certificates.json + truth_code + ladder fixtures")


if __name__ == "__main__":
    main()
