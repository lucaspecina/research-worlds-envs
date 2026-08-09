"""overgen_v0 anchor robots -- the three points the PAIR needs (ADR 0152).

- OVERGEN (the vice reflex): fits the line-1 law from the free overview,
  absorbs each pilot as a per-line OFFSET ("the rest is noise"), buys
  nothing, ships law+offset for all five lines.
- FRAGMENT (the twin's losing reflex): never generalizes -- every line 2-5 is
  its own 4-point pilot fit; buys nothing.
- JUICIO (adaptive discrimination): fits the law, scores each line's pilot
  residuals against law+offset (z vs noise), buys campaigns for the two most
  suspicious lines, pools the consistent ones, pilot-fits the suspicious
  unbought remainder. Same code on both poles -- discrimination, no reflex.

All ship interp-table submissions. Zero-LLM, deterministic per seed.
"""

import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from wager.contracts import ExperimentDesign  # noqa: E402

LINES = [1, 2, 3, 4, 5]
LOT = 20
# Codex r-overgen: pilot evidence is decisive for ALLOCATION, not statistically
# decisive -- juicio always buys the top-2 lines by pilot residual RANK; the
# statistically decisive test happens on the 20-row campaign it buys.
GRID = np.round(np.arange(0.0, 10.001, 0.1), 3)


def _law_fit(d, y):
    """Least-squares fit of y = a + b * d*(10-d)/25 -> (a, b, resid_sd)."""
    d = np.asarray(d, float)
    y = np.asarray(y, float)
    X = np.column_stack([np.ones_like(d), d * (10.0 - d) / 25.0])
    coef, *_ = np.linalg.lstsq(X, y, rcond=None)
    resid = y - X @ coef
    return float(coef[0]), float(coef[1]), float(max(np.std(resid), 0.3))


def _law_vals(a, b, d):
    d = np.asarray(d, float)
    return a + b * d * (10.0 - d) / 25.0


def _pilot_z(a, b, d, y, sd):
    """Mean |residual|/sd of a line's pilot vs law + best offset."""
    pred = _law_vals(a, b, d)
    off = float(np.mean(y - pred))
    return float(np.mean(np.abs(y - pred - off)) / max(sd, 1e-6)), off


def _pchip_table(d, y):
    from scipy.interpolate import PchipInterpolator
    d = np.asarray(d, float)
    y = np.asarray(y, float)
    rounded = np.round(d, 3)
    uniq = np.unique(rounded)
    centers = np.array([d[rounded == u].mean() for u in uniq])
    means = np.array([y[rounded == u].mean() for u in uniq])
    order = np.argsort(centers)
    centers, means = centers[order], means[order]
    if centers.size >= 3:
        vals = PchipInterpolator(centers, means)(np.clip(GRID, centers[0], centers[-1]))
    else:
        vals = np.interp(GRID, centers, means)
    return vals


def _overview_table(d, y):
    """Line 1 from the overview: binned means -> PCHIP."""
    from scipy.interpolate import PchipInterpolator
    d = np.asarray(d, float)
    y = np.asarray(y, float)
    edges = np.arange(0.0, 10.001, 1.0)
    cs, ms = [], []
    for a, b in zip(edges[:-1], edges[1:]):
        m = (d >= a) & (d < b + (1e-9 if b > 9.9 else 0.0))
        if m.sum() >= 3:
            cs.append(d[m].mean())
            ms.append(y[m].mean())
    cs, ms = np.array(cs), np.array(ms)
    return PchipInterpolator(cs, ms)(np.clip(GRID, cs[0], cs[-1]))


def _submission(tables, sds):
    parts = []
    for name in LINES:
        xs = ", ".join(f"{v:g}" for v in GRID)
        vs = ", ".join(f"{v:.3f}" for v in tables[name])
        parts.append(f'    {name}: (np.array([{xs}]), np.array([{vs}]), {sds[name]:.3f}),')
    tabs = "\n".join(parts)
    return f'''
import numpy as np
import pandas as pd

T = {{
{tabs}
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
        p = server.observe(f"pilot_{name}", 8)
        data[name] = [p["driver"].to_numpy(float), p["outcome"].to_numpy(float)]
    return data


def run_overgen(server) -> None:
    data = _free_data(server)
    a, b, sd = _law_fit(*data[1])
    tables, sds = {1: _law_vals(a, b, GRID)}, {1: sd}
    for name in (2, 3, 4, 5):
        _, off = _pilot_z(a, b, data[name][0], data[name][1], sd)
        tables[name] = _law_vals(a, b, GRID) + off
        sds[name] = sd
    server.submit(_submission(tables, sds))


def run_fragment(server) -> None:
    data = _free_data(server)
    tables = {1: _overview_table(*data[1])}
    sds = {1: 0.75}
    for name in (2, 3, 4, 5):
        tables[name] = _pchip_table(data[name][0], data[name][1])
        sds[name] = 0.75
    server.submit(_submission(tables, sds))


def run_juicio(server) -> None:
    data = _free_data(server)
    a, b, sd = _law_fit(*data[1])
    zs, offs = {}, {}
    for name in (2, 3, 4, 5):
        zs[name], offs[name] = _pilot_z(a, b, data[name][0], data[name][1], sd)
    ranked = sorted((2, 3, 4, 5), key=lambda n: -zs[n])
    bought = []
    for name in ranked[:2]:                     # allocation by rank, always
        df = server.experiment(ExperimentDesign(config={"campaign_line": name}, n=LOT))
        d0, y0 = data[name]
        data[name] = [np.concatenate([d0, df["driver"].to_numpy(float)]),
                      np.concatenate([y0, df["outcome"].to_numpy(float)])]
        bought.append(name)
    tables, sds = {1: _law_vals(a, b, GRID)}, {1: sd}
    for name in (2, 3, 4, 5):
        if name in bought:
            # decisive test on the CAMPAIGN ONLY (solid level means; single
            # pilot rows would put noisy knots into the fit)
            d0, y0 = data[name]
            camp = np.isin(np.round(d0, 3), (0.5, 2.5, 5.0, 7.5, 9.5))
            dc, yc = d0[camp], y0[camp]
            pred = _law_vals(a, b, dc)
            off = float(np.mean(yc - pred))
            lev_z = []
            for lvl in np.unique(np.round(dc, 3)):
                m = np.round(dc, 3) == lvl
                se = sd / np.sqrt(max(m.sum(), 1))
                lev_z.append(abs(float(np.mean(yc[m] - pred[m] - off))) / se)
            if float(np.mean(lev_z)) >= 1.5:    # the law breaks here: localize
                tables[name] = _pchip_table(dc, yc)
                sds[name] = 0.75
            else:                               # the law holds here: pool
                tables[name] = _law_vals(a, b, GRID) + off
                sds[name] = sd
        else:                                   # unbought: pool on the offset;
            tables[name] = _law_vals(a, b, GRID) + offs[name]
            sds[name] = sd * (1.15 if zs[name] >= 1.1 else 1.0)
    server.submit(_submission(tables, sds))


ROBOTS = {"juicio": run_juicio, "overgen": run_overgen, "fragment": run_fragment}


def run_robot(case_dir, robot: str, seed_offset: int) -> dict:
    from wager.harness.case_episode import build_world_server

    server = build_world_server(case_dir, seed_offset=seed_offset)
    ROBOTS[robot](server)
    if server.result is None:
        raise RuntimeError(f"robot {robot} (seed {seed_offset}): rejected by smoke")
    return {"robot": robot, "seed_offset": seed_offset,
            "R": server.result["R"], "left": server.budget_remaining}
