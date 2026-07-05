"""Long -> wide pivot for trajectory worlds (v0.68-R1; ARCHITECTURE 9).

NEW CODE ON THE REWARD PATH -- treated as that class demands: one pure, small
function, property-tested BEFORE anything is scored with it. The deliverable
contract for dynamic worlds is LONG format (one row per reading):

    columns: unit_id, t, y      n = UNITS -> the table has n * len(t_grid) rows

Scoring compares distributions over UNITS: each unit's trajectory becomes one
row whose columns are its values at the item's declared time grid ("y@<t>").
Energy distance and the functional scorer then operate on those columns like
any other -- timestamps are columns (MUNDOS_DINAMICOS_CONTEXT 4.2). A table
that does not respect the grid (missing/duplicate/off-grid readings) raises
ValueError; the scorer prices that like any crash (D_MAX, ARCHITECTURE 8).

ZERO-LLM ZONE. numpy/pandas only; deterministic (rows sorted by unit_id,
columns in grid order).
"""

import numpy as np
import pandas as pd

LONG_COLUMNS = ("unit_id", "t", "y")


def wide_columns(t_grid) -> list[str]:
    """Deterministic scored-column names for a grid: y@0, y@2.5, ..."""
    return [f"y@{float(t):g}" for t in t_grid]


def pivot_trajectories(df: pd.DataFrame, t_grid, rtol: float = 1e-6) -> pd.DataFrame:
    """One row per unit, one column per grid timestamp, grid order, sorted by
    unit_id. Strict: every unit reports every grid time exactly once."""
    grid = np.asarray(tuple(t_grid), dtype=float)
    if grid.size == 0:
        raise ValueError("t_grid is empty")
    if set(df.columns) != set(LONG_COLUMNS):
        raise ValueError(
            f"long format must have columns {list(LONG_COLUMNS)}, got {list(df.columns)}"
        )
    t = df["t"].to_numpy(dtype=float)
    diffs = np.abs(t[:, None] - grid[None, :])
    k = diffs.argmin(axis=1)
    tol = rtol * np.maximum(1.0, np.abs(grid[k]))
    off = diffs[np.arange(t.size), k] > tol
    if off.any():
        bad = sorted(set(np.round(t[off], 6).tolist()))[:5]
        raise ValueError(f"readings at times {bad} are not on the item's t_grid {grid.tolist()}")
    try:
        piv = df.assign(_k=k).pivot(index="unit_id", columns="_k", values="y")
    except ValueError as exc:  # pandas: duplicate (unit, t) entries
        raise ValueError("duplicate reading for the same (unit_id, t)") from exc
    if piv.shape[1] != grid.size or piv.isna().to_numpy().any():
        raise ValueError(
            f"every unit must report every t in t_grid exactly once "
            f"({grid.size} readings/unit; got a unit with a missing grid time)"
        )
    piv = piv.reindex(columns=range(grid.size))
    return pd.DataFrame(
        {name: piv[i].to_numpy(dtype=float) for i, name in enumerate(wide_columns(grid))}
    )
