"""Prospective phenotype gate for the over-generalization slice.

The gate reads only the agent's executable M_pre. It asks whether that model
actually embodies the target belief: similar high-range *shape increments*
across the five lines. It never queries either hidden world.
"""

from __future__ import annotations

from types import SimpleNamespace

import numpy as np

from wager.reward.sandbox import SandboxedSubmission, SandboxError

LINES = (1, 2, 3, 4, 5)
ANCHOR_DRIVER = 3.5
HIGH_DRIVERS = (5.0, 6.2, 7.4, 8.6, 9.6)


def shared_transfer_phenotype(
    code: str | None,
    *,
    max_shape_spread_noise=1.0,
    n=1200,
    timeout_s=10.0,
):
    """Classify whether M_pre commits to a shared extrapolation shape.

    Per line we subtract the prediction at the common low-range anchor, so
    harmless line intercepts do not count as fragmentation. Between-line RMS
    spread of the resulting high-range increments is normalized by the
    model's typical predictive SD. The threshold is fixed before looking at a
    donor and is independent of either world's truth.
    """
    if not code:
        return {"eligible": False, "reason": "missing_artifact"}
    means = np.empty((len(LINES), 1 + len(HIGH_DRIVERS)), dtype=float)
    spreads = np.empty_like(means)
    drivers = (ANCHOR_DRIVER,) + HIGH_DRIVERS
    try:
        with SandboxedSubmission(code, ["outcome"], timeout_s=timeout_s) as submission:
            for i, line in enumerate(LINES):
                for j, driver in enumerate(drivers):
                    regime = SimpleNamespace(
                        config={"line": line, "driver": driver},
                        context={},
                        horizon=None,
                    )
                    values = submission.run(regime, n, 960_000 + 101 * i + j)[
                        "outcome"
                    ].to_numpy(float)
                    means[i, j] = float(np.mean(values))
                    spreads[i, j] = float(np.std(values, ddof=1))
    except (SandboxError, ValueError) as exc:
        return {"eligible": False, "reason": "unscoreable", "error": str(exc)}

    increments = means[:, 1:] - means[:, [0]]
    between_line_rms = float(np.sqrt(np.mean(np.var(increments, axis=0, ddof=1))))
    predictive_sd = float(np.median(spreads))
    if not np.isfinite(predictive_sd) or predictive_sd <= 1e-9:
        return {
            "eligible": False,
            "reason": "degenerate_predictive_spread",
            "between_line_rms": between_line_rms,
            "predictive_sd": predictive_sd,
        }
    ratio = between_line_rms / predictive_sd
    return {
        "eligible": bool(ratio <= max_shape_spread_noise),
        "reason": None if ratio <= max_shape_spread_noise else "target_belief_absent",
        "shape_spread_noise_ratio": ratio,
        "threshold": float(max_shape_spread_noise),
        "between_line_rms": between_line_rms,
        "predictive_sd": predictive_sd,
        "mean_increments_by_line": {
            str(line): [float(value) for value in increments[i]]
            for i, line in enumerate(LINES)
        },
    }
