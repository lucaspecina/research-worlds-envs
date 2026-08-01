import pytest

from wager.report.checkpoint_score import normalized_group_score


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
