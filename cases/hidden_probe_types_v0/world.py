"""Grupos escondidos — Particulas bajo una sonda.

Twenty-four labelled calibration particles persist across experiment calls.  Each particle has a
large continuous baseline and one of two hidden response types.  A single probe orientation shows
one broad population; paired orientations on the same IDs cancel the baseline and reveal two
opposite, persistent response curves.

The agent never sees this file.  All randomness and scoring are zero-LLM.
"""

import numpy as np
import pandas as pd

COLUMNS = ["unit_id", "t", "y"]

PHASE = 0.37
TYPE_AMPLITUDE = 0.75
LEVEL_SD = 1.0
ORTHOGONAL_SD = 0.25
READING_SD = 0.30

LAB_N = 24
ANGLE_MIN = 0.0
ANGLE_MAX = float(2.0 * np.pi)
SCORE_GRID = tuple(float(v) for v in np.arange(8) * np.pi / 4.0)


def _basis(theta: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    return np.cos(theta - PHASE), np.sin(theta - PHASE)


def _long(
    unit_ids: np.ndarray,
    theta: np.ndarray,
    level: np.ndarray,
    hidden_type: np.ndarray,
    orthogonal: np.ndarray,
    noise_rng: np.random.Generator,
) -> pd.DataFrame:
    cosine, sine = _basis(theta)
    y = (
        level[:, None]
        + TYPE_AMPLITUDE * hidden_type[:, None] * cosine[None, :]
        + orthogonal[:, None] * sine[None, :]
        + noise_rng.normal(0.0, READING_SD, size=(len(unit_ids), len(theta)))
    )
    return pd.DataFrame({
        "unit_id": np.repeat(unit_ids.astype(float), len(theta)),
        "t": np.tile(theta, len(unit_ids)),
        "y": y.ravel(),
    })


def _fresh_population(theta: np.ndarray, n: int, seed: int) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    level = rng.normal(0.0, LEVEL_SD, n)
    hidden_type = rng.choice((-1.0, 1.0), size=n)
    orthogonal = rng.normal(0.0, ORTHOGONAL_SD, n)
    return _long(
        np.arange(n), theta, level, hidden_type, orthogonal, rng
    )


def _routine_snapshots(n: int, seed: int) -> pd.DataFrame:
    """One orientation on each of n different particles: no persistent linkage."""
    rng = np.random.default_rng(seed)
    theta = rng.uniform(ANGLE_MIN, ANGLE_MAX, n)
    level = rng.normal(0.0, LEVEL_SD, n)
    hidden_type = rng.choice((-1.0, 1.0), size=n)
    orthogonal = rng.normal(0.0, ORTHOGONAL_SD, n)
    cosine, sine = _basis(theta)
    y = (
        level
        + TYPE_AMPLITUDE * hidden_type * cosine
        + orthogonal * sine
        + rng.normal(0.0, READING_SD, n)
    )
    return pd.DataFrame({
        "unit_id": np.arange(n, dtype=float),
        "t": theta,
        "y": y,
    })


def _lab_latents(seed: int) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """Stable particle identities inside one episode, fresh across episode seeds."""
    episode_key = int(seed) // 100_000
    rng = np.random.default_rng(2_026_081_400 + episode_key)
    hidden_type = np.r_[np.full(LAB_N // 2, -1.0), np.full(LAB_N // 2, 1.0)]
    rng.shuffle(hidden_type)
    level = rng.normal(0.0, LEVEL_SD, LAB_N)
    orthogonal = rng.normal(0.0, ORTHOGONAL_SD, LAB_N)
    return np.arange(1, LAB_N + 1), level, hidden_type, orthogonal


def sample(regime, n: int, seed: int) -> pd.DataFrame:
    if "__routine" in regime.config:
        return _routine_snapshots(n, seed)

    grid = regime.context.get("t_grid")
    if grid is None:
        raise ValueError("hidden_probe_types_v0 requires context['t_grid']")
    theta = np.asarray(tuple(grid), dtype=float)
    if theta.size == 0 or not np.isfinite(theta).all():
        raise ValueError("t_grid must contain finite probe orientations")

    if regime.context.get("panel") == "calibration":
        if n != LAB_N:
            raise ValueError(f"the calibration bank contains exactly {LAB_N} particles")
        unit_ids, level, hidden_type, orthogonal = _lab_latents(seed)
        return _long(
            unit_ids, theta, level, hidden_type, orthogonal,
            np.random.default_rng(seed + 71),
        )

    return _fresh_population(theta, n, seed)


def experiment_guard(design, turn, fired_events) -> None:
    del turn, fired_events
    if design.context.get("panel") != "calibration":
        raise ValueError("experiments must address context panel='calibration'")
    grid = design.context.get("t_grid")
    if not isinstance(grid, tuple) or len(grid) != 1:
        raise ValueError("one experiment measures exactly one chosen orientation")
    theta = float(grid[0])
    if not ANGLE_MIN <= theta < ANGLE_MAX:
        raise ValueError(f"orientation must be in [{ANGLE_MIN}, {ANGLE_MAX}) radians")


model = sample
