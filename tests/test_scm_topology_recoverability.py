import numpy as np
import pandas as pd

from scripts.analyze_scm_topology_recoverability import (
    _campaign_data,
    recoverability_from_rows,
)


def _one_control_local_rows(seed: int = 23) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    rows = []
    for grade in (1.0, 5.0, 9.0):
        for batch_class in ("A", "B"):
            for _ in range(24):
                mean = 40.0 - 2.0 * grade if batch_class == "A" else 20.0 + 2.0 * grade
                rows.append(
                    {
                        "feedstock_grade": grade,
                        "humidity": 5.0,
                        "batch_class": batch_class,
                        "outcome": mean + rng.normal(0.0, 0.35),
                    }
                )
    return pd.DataFrame(rows)


def _one_control_latent_rows(seed: int = 29) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    rows = []
    for grade in (1.0, 5.0, 9.0):
        for batch_class in ("A", "B"):
            # Same 75/25 mixture inside each visible class: the label carries
            # no information about which response law generated the row.
            for use_flat in ([True] * 36 + [False] * 12):
                mean = 30.0 if use_flat else 20.0 + 2.0 * grade
                rows.append(
                    {
                        "feedstock_grade": grade,
                        "humidity": 5.0,
                        "batch_class": batch_class,
                        "outcome": mean + rng.normal(0.0, 0.35),
                    }
                )
    return pd.DataFrame(rows)


def test_one_varying_control_uses_observed_subspace_and_parameter_counts():
    result = recoverability_from_rows(
        _one_control_local_rows(), target="local", folds=2, seed=101
    )

    assert result["informative"] is True
    assert result["design_columns"] == ["intercept", "feedstock_grade"]
    assert result["design_dimension"] == 2
    assert result["n_parameters"] == {
        "single": 3,
        "class_split": 5,
        "latent_mixture": 6,
    }
    assert result["selected_structure"] == "class_split"
    assert result["recoverable"] is True


def test_one_varying_control_recovers_latent_laws_independent_of_class():
    result = recoverability_from_rows(
        _one_control_latent_rows(), target="latent", folds=3, seed=103
    )

    assert result["informative"] is True
    assert result["design_columns"] == ["intercept", "feedstock_grade"]
    assert result["BIC_winner"] == "latent_mixture"
    assert result["CV_winner"] == "latent_mixture"
    assert result["recoverable"] is True


def test_two_control_protocol_keeps_full_design():
    rows = _one_control_local_rows().iloc[:4].copy()
    rows["feedstock_grade"] = [1.0, 1.0, 9.0, 9.0]
    rows["humidity"] = [2.0, 8.0, 2.0, 8.0]

    data = _campaign_data(rows)

    assert data.design_columns == (
        "intercept",
        "feedstock_grade",
        "humidity",
    )
    assert data.x.shape == (4, 3)
    assert np.linalg.matrix_rank(data.x) == 3


def test_collinear_two_control_campaign_is_not_collapsed_to_one_dimension():
    rows = _one_control_local_rows()
    rows["humidity"] = rows["feedstock_grade"]

    result = recoverability_from_rows(rows, target="local", folds=2)

    assert result["informative"] is False
    assert result["design_columns"] == [
        "intercept",
        "feedstock_grade",
        "humidity",
    ]
    assert "must span the full [1,G,H] design" in result["reason"]
