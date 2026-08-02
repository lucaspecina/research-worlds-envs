from pathlib import Path
from types import SimpleNamespace

import numpy as np
from pandas.testing import assert_frame_equal

from cases import ode_second_wave_v0_common as physics
from wager.factory.case_loader import load_truth_code, load_world_module
from wager.reward.sandbox import SandboxedSubmission


ROOT = Path(__file__).resolve().parents[1]
CASES = {
    arm: ROOT / "cases" / f"ode_second_wave_{arm}_v0"
    for arm in physics.ARMS
}


def _regime(line, grid):
    return SimpleNamespace(config={}, context={"line": line, "t_grid": tuple(grid)}, horizon=None)


def test_line_a_is_identical_and_truth_fixtures_match_worlds():
    regime = _regime("A", physics.HISTORY_GRID)
    reference = None
    for arm, case_dir in CASES.items():
        world = load_world_module(case_dir)
        actual = world.sample(regime, 12, 94001)
        if reference is None:
            reference = actual
        else:
            assert_frame_equal(actual, reference, check_exact=True)
        with SandboxedSubmission(load_truth_code(case_dir), physics.LONG_COLUMNS) as truth:
            expected = truth.run(regime, 12, 94001)
            b_regime = _regime("B", physics.REPORT_GRID)
            expected_b = truth.run(b_regime, 12, 94002)
        assert_frame_equal(actual, expected, check_exact=True)
        actual_b = world.sample(b_regime, 12, 94002)
        assert_frame_equal(actual_b, expected_b, check_exact=True)


def test_served_report_identifies_only_the_structural_arm_as_two_phase():
    regime = _regime("B", physics.REPORT_GRID)
    fits = {}
    rng = np.random.default_rng(77123)
    shared_noise = rng.normal(0.0, physics.NOISE_SD, physics.REPORT_UNITS * len(physics.REPORT_GRID))
    for arm, case_dir in CASES.items():
        frame = load_world_module(case_dir).sample(regime, physics.REPORT_UNITS, 740001)
        frame = frame.copy()
        frame["y"] += shared_noise
        fits[arm] = physics.fit_phase_selection(frame)
    assert {arm: row["phases_selected"] for arm, row in fits.items()} == {
        "retain": 1,
        "param": 1,
        "struct": 2,
    }
    assert fits["struct"]["single_phase_holdout_ratio"] >= 1.10
    assert fits["retain"]["single_phase_holdout_ratio"] <= 1.10
    assert fits["param"]["single_phase_holdout_ratio"] <= 1.10


def test_param_and_struct_have_matched_update_size_and_plateau():
    doses = {arm: physics.dose_from_transfer(arm) for arm in physics.ARMS}
    relative_gap = abs(doses["param"] - doses["struct"]) / np.mean(
        [doses["param"], doses["struct"]]
    )
    assert doses["retain"] == 0.0
    assert relative_gap <= 0.01
    z = physics._draws_b(1000, 424243)
    param = physics._b_components("param", z)
    struct = physics._b_components("struct", z)
    np.testing.assert_allclose(param["K"], struct["K1"] + struct["K2"], atol=1e-12)
