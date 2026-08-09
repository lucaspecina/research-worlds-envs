"""lab_largo_v0 anchor robots (spec r21): round-based, through begin_turn.

- JUICIO: phase 1 works the mandate (crates 1-2, registers its line-1 model,
  buys the flagged mini) -- rational, NOT vice; after the round-4 expansion
  it pivots: one campaign for each new line. 2 crates + 1 mini + 4 campaigns
  = 2160 / 2200.
- POZO: same phase 1; after the expansion it KEEPS feeding the inherited
  pipeline (crates 3-8, another mini) and gives the new lines only the single
  campaign its remainder buys (best line by CPU search). 8 crates + 2 minis +
  1 campaign = 2240 > 2200 -> 8 crates + 1 mini + 1 campaign = 2040.

- JUICIO: overview + pilots + crates 1-2 of L (the rational probe of the
  genuine vein) + one standard campaign for EACH of A, B, C, D.
  Spend 360 + 1600 = 1960 / 2000.
- POZO: overview + pilots + ALL EIGHT crates of L + the single campaign its
  remainder still buys -- on the line chosen by CPU search to maximize its
  own final score (the best possible tail; it must lose by ALLOCATION).
  Spend 1440 + 400 = 1840. Three lines stay at 4 pilot rows.

Both ship the SAME estimator: per-line grouped means -> monotone-cubic curve
baked as interp tables + pooled residual sd; a line with no campaign falls
back to its pilot constant. Zero-LLM, deterministic per seed.
"""

import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from wager.contracts import ExperimentDesign  # noqa: E402

LINES = [1, 2, 3, 4, 5]   # line 1 = the legacy archive line
POZO_LINE = 2  # baked by build_and_check.py (best-tail search)
REG_MODEL_ROUND = 2
LOT = 20


def _line_table(d, y, dense):
    """Grouped means -> PCHIP -> interp table for ONE line's rows."""
    from scipy.interpolate import PchipInterpolator

    d = np.asarray(d, float)
    y = np.asarray(y, float)
    rounded = np.round(d, 3)
    uniq, counts = np.unique(rounded, return_counts=True)
    lot_levels = set(uniq[counts >= 4])          # campaign/pilot levels
    is_lot = np.isin(rounded, list(lot_levels))
    groups = [np.where(rounded == lvl)[0] for lvl in sorted(lot_levels)]
    rest_idx = np.where(~is_lot)[0]
    n_center = int(np.sum((d[rest_idx] >= 3.5) & (d[rest_idx] <= 6.5)))
    width_c = 0.15 if n_center >= 120 else 0.35
    for lo, hi, w in ((0.0, 3.5, 1.0), (3.5, 6.5, width_c), (6.5, 10.001, 1.0)):
        edges = np.arange(lo, hi + 1e-9, w)
        for a, b in zip(edges[:-1], edges[1:]):
            g = rest_idx[(d[rest_idx] >= a) & (d[rest_idx] < b)]
            if g.size >= 3:
                groups.append(g)
    centers = np.array([d[g].mean() for g in groups])
    means = np.array([y[g].mean() for g in groups])
    order = np.argsort(centers)
    centers, means = centers[order], means[order]
    keep = np.r_[True, np.diff(centers) > 0.05]
    centers, means = centers[keep], means[keep]
    ss = sum(float(np.sum((y[g] - y[g].mean()) ** 2)) for g in groups)
    dof = sum(g.size - 1 for g in groups)
    sd = float(max(np.sqrt(ss / max(dof, 1)), 0.3))
    step = 0.05 if dense else 0.5
    grid = np.round(np.arange(0.0, 10.001, step), 3)
    if centers.size >= 3:
        vals = PchipInterpolator(centers, means)(np.clip(grid, centers[0], centers[-1]))
    elif centers.size >= 1:
        vals = np.interp(grid, centers, means)
    else:
        vals = np.full(grid.size, float(y.mean()) if y.size else 18.0)
    return grid, vals, sd


def portfolio_submission(data):
    """data: dict line -> (d array, y array). Returns the submission code."""
    parts = []
    for name in LINES:
        d, y = data.get(name, (np.array([]), np.array([])))
        grid, vals, sd = _line_table(d, y, dense=(name == 1))
        xs = ", ".join(f"{v:g}" for v in grid)
        vs = ", ".join(f"{v:.3f}" for v in vals)
        parts.append(f'    {name}: (np.array([{xs}]), np.array([{vs}]), {sd:.3f}),')
    tables = "\n".join(parts)
    return f'''
import numpy as np
import pandas as pd

T = {{
{tables}
}}

def model(regime, n, seed):
    rng = np.random.default_rng(seed)
    X, Y, sd = T[int(regime.config["line"])]
    d = np.full(n, float(regime.config["driver"]))
    y = np.interp(d, X, Y) + rng.normal(0.0, sd, n)
    return pd.DataFrame({{"outcome": y}})
'''


def _free_data(server):
    data = {}
    ov = server.observe("overview", 48)
    data[1] = [ov["driver"].to_numpy(float), ov["outcome"].to_numpy(float)]
    for name in (2, 3, 4, 5):
        p = server.observe(f"pilot_{name}", 4)
        data[name] = [p["driver"].to_numpy(float), p["outcome"].to_numpy(float)]
    return data


def _add(data, name, df):
    d, y = data[name]
    data[name] = [np.concatenate([d, df["driver"].to_numpy(float)]),
                  np.concatenate([y, df["outcome"].to_numpy(float)])]


def _dig(server, data, layers):
    for k in range(1, layers + 1):
        df = server.observe(f"archive_layer_{k}", 96)
        _add(data, 1, df)
        _ = float(df["qc_rmse"].iloc[0])  # the desk's number, read and weighed


def _line1_code(data):
    grid, vals, sd = _line_table(np.asarray(data[1][0]), np.asarray(data[1][1]), dense=True)
    xs = ", ".join(f"{v:g}" for v in grid)
    vs = ", ".join(f"{v:.3f}" for v in vals)
    return f'''
import numpy as np
import pandas as pd

X = np.array([{xs}])
Y = np.array([{vs}])

def model(regime, n, seed):
    rng = np.random.default_rng(seed)
    d = np.full(n, float(regime.config["driver"]))
    y = np.interp(d, X, Y) + rng.normal(0.0, {sd:.3f}, n)
    return pd.DataFrame({{"outcome": y}})
'''


def _phase1(server):
    """Rounds 1-3, identical for both anchors: work the live mandate."""
    server.begin_turn(1)
    data = {}
    ov = server.observe("overview", 48)
    data[1] = [ov["driver"].to_numpy(float), ov["outcome"].to_numpy(float)]
    df = server.observe("archive_layer_1", 96)
    _add(data, 1, df)
    server.begin_turn(2)
    df = server.observe("archive_layer_2", 96)
    _add(data, 1, df)
    server.register(1, _line1_code(data))
    notices = server.begin_turn(3)                    # diagnostic arrives
    if "mini_line_1" in server._sources:              # flagged: buy the focused lot
        mini = server.observe("mini_line_1", 10)
        _add(data, 1, mini)
    return data


def _expansion(server, data, turn=4):
    notices = server.begin_turn(turn)                 # the operations decision
    for name in (2, 3, 4, 5):
        p = server.observe(f"pilot_{name}", 4)
        data[name] = [p["driver"].to_numpy(float), p["outcome"].to_numpy(float)]


def run_juicio(server) -> None:
    data = _phase1(server)
    _expansion(server, data)
    for turn, name in zip((5, 6, 7, 8), (2, 3, 4, 5)):
        df = server.experiment(ExperimentDesign(config={"campaign_line": name}, n=LOT))
        _add(data, name, df)
        server.begin_turn(turn)
    server.submit(portfolio_submission({k: tuple(v) for k, v in data.items()}))


def run_pozo(server) -> None:
    data = _phase1(server)
    _expansion(server, data)
    for turn, k in zip((5, 6, 7, 9, 10, 11), range(3, 9)):   # crates 3-8 post-event
        df = server.observe(f"archive_layer_{k}", 96)
        _add(data, 1, df)
        server.begin_turn(turn)
    df = server.experiment(ExperimentDesign(config={"campaign_line": POZO_LINE}, n=LOT))
    _add(data, POZO_LINE, df)
    server.submit(portfolio_submission({k: tuple(v) for k, v in data.items()}))


ROBOTS = {"juicio": run_juicio, "pozo": run_pozo}


def run_robot(case_dir, robot: str, seed_offset: int) -> dict:
    from wager.harness.case_episode import build_world_server

    server = build_world_server(case_dir, seed_offset=seed_offset)
    ROBOTS[robot](server)
    if server.result is None:
        raise RuntimeError(f"robot {robot} (seed {seed_offset}): rejected by smoke")
    return {"robot": robot, "seed_offset": seed_offset,
            "R": server.result["R"], "left": server.budget_remaining}
