"""Scientific and interface checks for Grupos escondidos — Particulas bajo una sonda."""

from pathlib import Path
from types import SimpleNamespace

import numpy as np
import pytest

from cases.hidden_probe_types_v0 import build_and_certify as cert
from cases.hidden_probe_types_v0 import world
from wager.contracts import ExperimentDesign
from wager.harness.case_episode import build_world_server
from wager.reward.trajectory import pivot_trajectories


CASE = Path(__file__).resolve().parents[1] / "cases" / "hidden_probe_types_v0"


def _ns(*, config=None, context=None):
    return SimpleNamespace(config=config or {}, context=context or {}, horizon=None)


def test_routine_and_calibration_ids_cannot_be_falsely_joined():
    routine = world.sample(_ns(config={"__routine": 1.0}), 200, 2026081601)
    calibration = world.sample(
        _ns(context={"panel": "calibration", "t_grid": (0.2,)}),
        world.LAB_N,
        80_000_001,
    )
    assert set(routine.unit_id).isdisjoint(set(calibration.unit_id))
    assert routine.unit_id.nunique() == len(routine)


def test_calibration_bank_persists_and_fresh_exam_units_have_complete_curves():
    first = world.sample(
        _ns(context={"panel": "calibration", "t_grid": (0.1,)}),
        world.LAB_N,
        80_000_001,
    )
    second = world.sample(
        _ns(context={"panel": "calibration", "t_grid": (2.8,)}),
        world.LAB_N,
        80_000_002,
    )
    assert np.array_equal(first.unit_id.to_numpy(), second.unit_id.to_numpy())

    grid = (0.3, 1.1, 2.7, 5.4)
    fresh = world.sample(_ns(context={"t_grid": grid}), 37, 2026081602)
    wide = pivot_trajectories(fresh, grid)
    assert wide.shape == (37, len(grid))


def test_server_enforces_one_orientation_and_exact_bank_size():
    server = build_world_server(CASE, seed_offset=99001)
    with pytest.raises(ValueError, match="exactly one"):
        server.experiment(
            ExperimentDesign(
                config={}, context={"panel": "calibration", "t_grid": (0.0, 1.0)},
                n=world.LAB_N,
            )
        )
    with pytest.raises(ValueError, match="n=192"):
        server.experiment(
            ExperimentDesign(
                config={}, context={"panel": "calibration", "t_grid": (0.0,)}, n=24,
            )
        )
    with pytest.raises(ValueError, match="orientation"):
        server.experiment(
            ExperimentDesign(
                config={}, context={"panel": "calibration", "t_grid": (2 * np.pi,)},
                n=world.LAB_N,
            )
        )


def test_legal_campaign_fits_budget_and_preserves_ids():
    server = build_world_server(CASE, seed_offset=99002)
    routine = server.observe("routine_snapshots", 200)
    assert len(routine) == 200
    ids = None
    for theta in (0.0, np.pi / 2, np.pi, 3 * np.pi / 2, np.pi / 4):
        frame = server.experiment(
            ExperimentDesign(
                config={}, context={"panel": "calibration", "t_grid": (float(theta),)},
                n=world.LAB_N,
            )
        )
        current = frame.unit_id.to_numpy()
        if ids is None:
            ids = current
        else:
            assert np.array_equal(ids, current)
    assert server.budget_remaining == pytest.approx(25.0)


def test_committed_certificate_is_green_and_material():
    import json

    report = json.loads((CASE / "certificates.json").read_text(encoding="utf-8"))
    assert report["gates"]["all"] is True
    assert report["best_one_band"]["S_profile"] <= cert.MAX_ONE_BAND_S
    assert min(row["two_type_S"] for row in report["finite_legal_solvers"]) >= 0.85
    assert min(report["production"]["legal_two_type_R"]) >= 0.80
    assert report["production"]["truth_minus_best_one_band"] >= 0.05


def test_scoring_transform_removes_only_each_curve_level():
    from wager.contracts import CaseMeta
    from wager.factory.case_loader import make_sample_transform

    meta = CaseMeta.from_json_file(CASE / "meta.json")
    transform = make_sample_transform(meta)
    grid = (0.2, 1.3, 4.4)
    raw = world.sample(_ns(context={"t_grid": grid}), 20, 2026081603)
    centered = transform(_ns(context={"t_grid": grid}), raw)
    shifted = raw.copy()
    shifted["y"] += np.repeat(np.linspace(-5.0, 5.0, 20), len(grid))
    centered_shifted = transform(_ns(context={"t_grid": grid}), shifted)
    assert np.allclose(centered.mean(axis=1), 0.0)
    assert np.allclose(centered, centered_shifted)


def test_truth_submission_crosses_smoke_and_reward_path_on_irregular_grids():
    server = build_world_server(CASE, seed_offset=99003)
    result = server.submit(server.scoring.world_source)
    assert result.accepted is True
    assert server.result["R"] == pytest.approx(1.0, abs=1e-6)


def test_posthoc_structural_analyzer_recognizes_truth(monkeypatch):
    from scripts import analyze_hidden_probe_types_discovery as analyzer

    monkeypatch.setattr(analyzer, "N", 5_000)
    server = build_world_server(CASE, seed_offset=99004)
    result = analyzer.score_code(server.scoring.world_source)
    assert result["S_probe"] >= 0.95
    assert result["crosses_jump_frontier"] is True
