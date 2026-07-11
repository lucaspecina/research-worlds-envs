"""The robot pair of rabbit_hole_v0 (Codex r14 SS4/SS6): scripted EPISODE agents.

All run through the REAL episode pipeline (observe/experiment/submit, budget
charged, smoke validated); their R comes from server.result like any solver's.

The construct is PERSISTENCE ON A SOURCE OF EXHAUSTED MARGINAL VALUE, so the
central pair shares EVERYTHING up to and including the negative signal and
differs ONLY in post-signal allocation (r14: "el par comparte hipotesis y
evidencia; difiere despues de la senal"):

- DISCIPLINADO: 128 cheap rows (rational first probe: the proxy visibly
  predicts) + the two discriminating campaigns (d=2.2, 7.5) that carry the
  observable negative signal (telemetry adds ~nothing within driver strata).
  Post-signal it allocates the rest to do(): three more campaigns (0.6, 3.8,
  9.3). Total 1928 <= 2000.
- POZO PROFUNDO (THE certified vicious pole, r16): digs until nothing is
  left -- 1024 more cheap rows after the shared probe (1152 decoy rows
  total, spend 1992, residual 8: not even one direct row). The narrow
  certified claim: extreme persistence on the exhausted source, consuming
  the budget the useful investigation needed.
- POZO moderado (DIAGNOSTIC only, r16 -- no gate): 1000 decoy rows total;
  the remainder (160) buys 10 direct rows and sometimes RESCUES the episode
  (a lottery of lucky knots: R swung 0.55-0.87 across seeds). Reported to
  document where the moderate depth stops being reliably punished.

Controls (r14 SS4; r16 rolled the economy back to 15/row after the 45/row
correction was refuted on both of its objectives):
- CINICO: ignores the decoy completely -- zero cheap rows, six campaigns.
  Must NOT be punished (R >= 0.88): the world rewards evidence allocation,
  not decoy archaeology.
- ASOCIACIONAL: direct source only, no causal sophistication -- 133
  certified rows, same estimator. Must reach R >= 0.88: separates the pit
  from causality worlds (a plain regression on the right source wins).

THE SHARED ESTIMATOR (curve_submission): every robot ships the same code
shape -- level/bin means -> monotone-cubic curve baked as a small interp
table + pooled residual sd; historical regime = feed ~ U(0,10) (declared in
the brief). Differences in R come from the EVIDENCE, never the estimator.

Zero-LLM. Deterministic given the server's seed_offset.
"""

import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from wager.contracts import ExperimentDesign  # noqa: E402

INIT_CHEAP = 128
INIT_LEVELS = [(2.2, 40), (7.5, 40)]          # the discriminating campaigns (signal)
FOLLOW_LEVELS = [(0.6, 20), (3.8, 20), (9.3, 20)]
CINICO_LEVELS = [(0.6, 20), (2.2, 20), (3.8, 20), (5.6, 20), (7.5, 20), (9.3, 20)]
DIG_ROWS = 872          # pozo moderado: cheap 128+872 = 1000 (DIAGNOSTIC, r16)
POZO_LAB_ROWS = 10      # what its remainder (160) buys at 15/row (r16 rollback)
DIG_ROWS_DEEP = 1024    # pozo profundo (THE certified pair): 1152 rows, residual 8
ASOC_LAB_ROWS = 133     # direct-route control restored (r16 rollback): 1995

TELEMETRY = ["telemetry_A", "telemetry_B", "telemetry_C",
             "telemetry_D", "telemetry_E", "telemetry_F"]


# --- the shared machinery -------------------------------------------------

def r2_cv(X, y, k=5, seed=0):
    """5-fold CV R^2 of OLS -- the yardstick of 'does this evidence still pay'."""
    X = np.asarray(X, float)
    y = np.asarray(y, float)
    folds = np.array_split(np.random.default_rng(seed).permutation(y.size), k)
    press = 0.0
    for j in range(k):
        tr = np.concatenate([folds[i] for i in range(k) if i != j])
        beta, *_ = np.linalg.lstsq(X[tr], y[tr], rcond=None)
        press += float(np.sum((y[folds[j]] - X[folds[j]] @ beta) ** 2))
    return 1.0 - press / float(np.sum((y - y.mean()) ** 2))


def feats_proxy(p):
    p = np.asarray(p, float)
    return np.column_stack([np.ones_like(p), p, p ** 2])


def feats_telemetry(df):
    cols = [np.ones(len(df))]
    for c in TELEMETRY:
        v = df[c].to_numpy(float)
        cols += [v, v ** 2]
    return np.column_stack(cols)


def signal_stats(cheap, campaigns):
    """The negative signal BOTH robots receive (r14 SS2): the proxy visibly
    predicts on the cheap probe, but within fixed-driver strata the telemetry
    adds ~nothing -- continuing to dig is the losing move."""
    y = cheap["gas_yield"].to_numpy(float)
    r2_cheap = r2_cv(feats_proxy(cheap["telemetry_A"].to_numpy(float)), y, seed=1)
    within = [r2_cv(feats_telemetry(df), df["gas_yield"].to_numpy(float), seed=2)
              for _, df in campaigns]
    return {"r2_proxy_cheap": float(r2_cheap),
            "r2_telemetry_within_stratum": [float(v) for v in within]}


def curve_submission(d, y):
    """THE shared final estimator: (feed, yield) pairs -> submission code.

    Level/bin means -> PCHIP curve baked as a 26-point interp table (tiny MDL
    footprint), flat beyond covered range, pooled within-group residual sd,
    historical regime feed ~ U(0,10) as the brief declares."""
    from scipy.interpolate import PchipInterpolator

    d = np.asarray(d, float)
    y = np.asarray(y, float)
    order = np.argsort(d)
    ds, ys = d[order], y[order]
    if np.unique(np.round(ds, 2)).size <= 10:          # replicated levels
        cuts = np.where(np.diff(ds) > 1e-6)[0]
        groups = np.split(np.arange(ds.size), cuts + 1)
    else:                                              # scattered rows
        edges = np.quantile(ds, np.linspace(0.0, 1.0, min(10, ds.size // 10) + 1))
        edges[-1] += 1e-9
        lab = np.clip(np.digitize(ds, edges) - 1, 0, len(edges) - 2)
        groups = [np.where(lab == j)[0] for j in range(len(edges) - 1) if np.any(lab == j)]
    merged = []
    for g in groups:                                   # near-duplicate centers fold
        if merged and ds[g].mean() - ds[merged[-1]].mean() < 0.25:
            merged[-1] = np.concatenate([merged[-1], g])
        else:
            merged.append(g)
    centers = np.array([ds[g].mean() for g in merged])
    means = np.array([ys[g].mean() for g in merged])
    ss = sum(float(np.sum((ys[g] - ys[g].mean()) ** 2)) for g in merged)
    dof = sum(g.size - 1 for g in merged)
    sd = float(max(np.sqrt(ss / max(dof, 1)), 0.3))
    grid = np.round(np.linspace(0.0, 10.0, 26), 2)
    if centers.size >= 3:
        vals = PchipInterpolator(centers, means)(np.clip(grid, centers[0], centers[-1]))
    else:
        vals = np.interp(grid, centers, means)
    xs = ", ".join(f"{v:.2f}" for v in grid)
    vs = ", ".join(f"{v:.3f}" for v in vals)
    return f'''
import numpy as np
import pandas as pd

X = np.array([{xs}])
Y = np.array([{vs}])

def model(regime, n, seed):
    rng = np.random.default_rng(seed)
    if "feed_setting" in regime.config:
        d = np.full(n, float(regime.config["feed_setting"]))
    else:
        d = rng.uniform(0.0, 10.0, n)
    y = np.interp(d, X, Y) + rng.normal(0.0, {sd:.3f}, n)
    return pd.DataFrame({{"gas_yield": y}})
'''


def _campaigns(server, levels):
    out = []
    for lvl, n in levels:
        df = server.experiment(ExperimentDesign(config={"feed_setting": lvl}, n=n))
        out.append((lvl, df))
    return out


def _stack(campaigns, lab=None):
    d = np.concatenate([np.full(len(df), lvl) for lvl, df in campaigns]
                       + ([lab["feed_setting"].to_numpy(float)] if lab is not None else []))
    y = np.concatenate([df["gas_yield"].to_numpy(float) for _, df in campaigns]
                       + ([lab["gas_yield"].to_numpy(float)] if lab is not None else []))
    return d, y


def _shared_probe(server):
    """Identical opening for the central pair: cheap probe + the two
    discriminating campaigns + the signal computed from them."""
    cheap = server.observe("operations_archive", INIT_CHEAP)
    campaigns = _campaigns(server, INIT_LEVELS)
    return cheap, campaigns, signal_stats(cheap, campaigns)


# --- the robots -----------------------------------------------------------

def run_disciplinado(server) -> None:
    _, campaigns, _ = _shared_probe(server)
    campaigns += _campaigns(server, FOLLOW_LEVELS)
    d, y = _stack(campaigns)
    server.submit(curve_submission(d, y))


def run_pozo(server) -> None:
    cheap, campaigns, _ = _shared_probe(server)
    # the pit: SAME signal received, keeps digging the decoy anyway
    import pandas as pd
    dig = server.observe("operations_archive", DIG_ROWS)
    allrows = pd.concat([cheap, dig], ignore_index=True)
    r2_cv(feats_telemetry(allrows),
          allrows["gas_yield"].to_numpy(float), seed=3)  # decoy modeling: spectacle
    lab = server.observe("lab_assays", POZO_LAB_ROWS)  # what 160 still buys
    d, y = _stack(campaigns, lab=lab)
    server.submit(curve_submission(d, y))


def run_cinico(server) -> None:
    campaigns = _campaigns(server, CINICO_LEVELS)
    d, y = _stack(campaigns)
    server.submit(curve_submission(d, y))


def run_pozo_profundo(server) -> None:
    cheap, campaigns, _ = _shared_probe(server)
    import pandas as pd
    dig = server.observe("operations_archive", DIG_ROWS_DEEP)
    allrows = pd.concat([cheap, dig], ignore_index=True)
    r2_cv(feats_telemetry(allrows),
          allrows["gas_yield"].to_numpy(float), seed=3)  # bottom of the pit
    d, y = _stack(campaigns)                             # residual 8: buys nothing
    server.submit(curve_submission(d, y))


def run_asociacional(server) -> None:
    lab = server.observe("lab_assays", ASOC_LAB_ROWS)
    d = lab["feed_setting"].to_numpy(float)
    y = lab["gas_yield"].to_numpy(float)
    server.submit(curve_submission(d, y))


ROBOTS = {
    "disciplinado": run_disciplinado,
    "pozo": run_pozo,
    "pozo_profundo": run_pozo_profundo,
    "cinico": run_cinico,
    "asociacional": run_asociacional,
}


def run_robot(case_dir, robot: str, seed_offset: int) -> dict:
    from wager.harness.case_episode import build_world_server

    server = build_world_server(case_dir, seed_offset=seed_offset)
    ROBOTS[robot](server)
    if server.result is None:
        raise RuntimeError(f"robot {robot} (seed {seed_offset}): submission rejected by smoke")
    return {"robot": robot, "seed_offset": seed_offset,
            "R": server.result["R"], "R_uncl": server.result["R_unclipped"],
            "left": server.budget_remaining}
