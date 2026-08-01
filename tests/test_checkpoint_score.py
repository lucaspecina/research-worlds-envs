import pytest

from wager.report.checkpoint_score import (
    captured_reference_fraction,
    normalized_group_score,
)


def test_normalized_group_score_maps_naive_truth_and_midpoint():
    truth = [0.0, 0.0]
    naive = [2.0, 4.0]
    weights = [1.0, 3.0]
    assert normalized_group_score(naive, truth, naive, weights)["R"] == pytest.approx(0.0)
    assert normalized_group_score(truth, truth, naive, weights)["R"] == pytest.approx(1.0)
    mid = [1.0, 2.0]
    assert normalized_group_score(mid, truth, naive, weights)["R"] == pytest.approx(0.5)


def test_normalized_group_score_reports_unresolved_and_clips():
    unresolved = normalized_group_score([1.0], [1.0], [1.0], [1.0])
    assert not unresolved["resolved"] and unresolved["R"] is None
    better = normalized_group_score([-1.0], [0.0], [2.0], [1.0])
    assert better["R"] == 1.0 and better["R_unclipped"] > 1.0


def _local_score(value):
    return {
        "scoreable": True,
        "groups": {"diagnostic": {"resolved": True, "R_unclipped": value}},
    }


def test_captured_reference_fraction_preserves_under_and_overshoot():
    half = captured_reference_fraction(
        _local_score(0.2), _local_score(0.5), _local_score(0.8)
    )
    over = captured_reference_fraction(
        _local_score(0.2), _local_score(0.95), _local_score(0.8)
    )
    assert half["resolved"] and half["fraction"] == pytest.approx(0.5)
    assert over["fraction"] == pytest.approx(1.25)


def test_captured_reference_fraction_refuses_tiny_denominator():
    result = captured_reference_fraction(
        _local_score(0.8), _local_score(0.79), _local_score(0.82)
    )
    assert not result["resolved"]
    assert result["reason"] == "reference_gain_too_small"
