"""Calibration-gate helpers (factory-side measurement; Decision Log v0.36).

Convention pinned here and guarded by the scale-sanity suite: every gate
threshold is expressed in ABSOLUTE R units (3 x std of the gated quantity),
never a relative CV. The fifth member of the scale-pathology family was a
threshold born where rung means sat near 1 -- there CV and absolute std
coincide numerically and the criterion accidentally works -- that broke
exactly when the instrument WORKED (the functional pushed rung means down,
0.583 -> 0.178, inflating CV x4.4 while absolute std barely moved,
0.0092 -> 0.0124). "Your ruler did not get worse because you measured
something smaller."

Visibility is an INSTRUMENT question and is measured on the sub-battery where
the operator's signature lives, with the LOCAL noise of that sub-battery;
weight is a STAKES question and is set by the full battery (Decision Log
v0.36; ARCHITECTURE §7). Conflating the two caused the v0.35 halt.
"""

from wager.contracts import ScoreReport


def gate_threshold(stds: list[float]) -> float:
    """3 x max absolute std of the gated quantity across the sweep extremes.

    Takes ABSOLUTE stds of R only. Deliberately has no mean/CV parameter:
    the dimensional-consistency test pins this signature (Decision Log v0.36-1b).
    """
    if not stds:
        raise ValueError("gate_threshold needs at least one std")
    return 3.0 * float(max(stds))


# Resolution floor: 5% of the normalization range, in the R units of the
# (sub-)battery where the gate lives -- the SAME house constant as the L1
# margins (Decision Log v0.10), reused with its semantics: the declared
# resolution of the instrument (Decision Log v0.38).
RESOLUTION_FLOOR = 0.05


def visibility_threshold(stds: list[float], floor: float = RESOLUTION_FLOOR) -> float:
    """Visibility gates have TWO components answering different questions
    (Decision Log v0.38): significance (3 x the gated quantity's OWN std --
    "is it real?") and magnitude (the resolution floor -- "does it matter at
    the level the instrument declares it can distinguish?"). With CRN crushing
    variance, significance is almost free and can NEVER be the selector:
    statistically-visible is not economically-visible."""
    return max(gate_threshold(stds), floor)


def sub_battery_fidelity(report: ScoreReport, idxs: list[int]) -> float:
    """Fidelity restricted to a sub-battery (weights renormalized within it).

    Fidelity-only on purpose: MDL is a property of the whole submission, not of
    an item subset -- sub-battery R compares the SAME code across item subsets,
    so the MDL term cancels by construction and is excluded.
    """
    total_w = sum(report.items[i].weight for i in idxs)
    if total_w <= 0:
        raise ValueError("sub-battery has no weight")
    return -sum(report.items[i].weight * report.items[i].mean_distance for i in idxs) / total_w


def sub_battery_r(
    rung: ScoreReport, truth: ScoreReport, naive: ScoreReport, idxs: list[int]
) -> float:
    """R of one rung on a sub-battery, anchored on the SAME sub-battery."""
    f_truth = sub_battery_fidelity(truth, idxs)
    f_naive = sub_battery_fidelity(naive, idxs)
    denom = f_truth - f_naive
    if denom == 0:
        raise ValueError("sub-battery does not discriminate (denom = 0)")
    return (sub_battery_fidelity(rung, idxs) - f_naive) / denom
