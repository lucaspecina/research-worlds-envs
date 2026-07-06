"""Wiring tests for the WorldServer (verbs, budget, channel, submit smoke)."""

from pathlib import Path

import pytest

from wager.contracts import ExperimentDesign
from wager.harness.case_episode import build_world_server
from wager.harness.world_server import BudgetError

CASE_DIR = Path(__file__).resolve().parents[1] / "cases" / "dummy_dose_v0"
SOURCE = "registros_proceso_2019_2023"


@pytest.fixture
def server():
    return build_world_server(CASE_DIR)


def test_describe_is_free_and_shows_surface(server):
    rem0 = server.budget_remaining
    d = server.describe()
    assert d["schema"] == ["dose", "marker", "outcome"]
    assert "settable" in d["control_surface"]
    assert server.budget_remaining == rem0  # describe is free


def test_observe_debits_budget(server):
    rem0 = server.budget_remaining
    df = server.observe(SOURCE, 300)
    assert list(df.columns) == ["dose", "marker", "outcome"] and len(df) == 300
    assert server.budget_remaining == rem0 - 300.0


def test_budget_error_when_overspending(server):
    server.experiment(ExperimentDesign(config={"dose": 1.0}, n=5000))  # cost 100 + 10000
    with pytest.raises(BudgetError):
        server.experiment(ExperimentDesign(config={"dose": 1.0}, n=5000))  # > remaining


def test_experiment_respects_measurement_channel(server):
    """Decision Log v0.14, precision 1: experiment runs the mechanism fresh
    (bypasses the dose assignment) but NEVER the measurement channel -- same
    schema, marker still a noisy proxy."""
    obs = server.observe(SOURCE, 3000)
    exp = server.experiment(ExperimentDesign(config={"dose": 3.0}, context={"cohort": 0.0}, n=3000))
    assert list(obs.columns) == list(exp.columns) == ["dose", "marker", "outcome"]
    # marker noise (severity ~ N(0,1) in both) is the same channel
    assert abs(obs["marker"].std() - exp["marker"].std()) < 0.3
    # but the assignment is bypassed: experiment fixes dose, observe varies it
    assert exp["dose"].std() < 1e-6
    assert obs["dose"].std() > 0.5


def test_submit_bad_columns_gives_actionable_error(server):
    bad = (
        "import pandas as pd\n"
        "def model(regime, n, seed):\n"
        " return pd.DataFrame({'dose':[0.0]*n,'outcome':[0.0]*n})\n"  # missing 'marker'
    )
    res = server.submit(bad)
    assert res.accepted is False
    assert "marker" in res.error or "columns" in res.error
    assert not server.terminal  # episode stays open after a failed submit


def test_submit_truth_is_accepted_and_scores_high(server):
    res = server.submit(server.scoring.world_source)
    assert res.accepted is True
    assert server.terminal
    assert server.result["R"] == pytest.approx(1.0, abs=1e-6)  # world.py -> R=1


def test_submit_with_hasattr_is_accepted(server):
    # regression for the E0 friction: hasattr is a safe builtin submissions use
    code = (
        "import numpy as np, pandas as pd\n"
        "def model(regime, n, seed):\n"
        " rng = np.random.default_rng(seed)\n"
        " c = regime.context.get('cohort', 0.0) if hasattr(regime, 'context') else 0.0\n"
        " dose = np.full(n, float(regime.config.get('dose', 3.0)))\n"
        " return pd.DataFrame({'dose': dose, 'marker': rng.normal(c, 1, n), 'outcome': rng.normal(0, 1, n)})\n"
    )
    res = server.submit(code)
    assert res.accepted is True


def test_server_serves_views_and_split_schemas_on_source_trap_worlds():
    """v0.54-2/v0.56 wiring, verified pre-E0 (family #19): describe() separates
    the DELIVERABLE schema from per-source VIEW schemas (__rep1/__rep2, costs);
    observe() returns the corrupted view, never the clean mechanism; the
    acceptance rate appears nowhere."""
    import json
    from pathlib import Path

    from wager.factory.case_loader import load_meta, load_world_sample

    case_dir = Path(__file__).resolve().parents[1] / "cases" / "selection_bias_v0"
    meta = load_meta(case_dir)
    from wager.harness.world_server import WorldServer

    server = WorldServer(
        world_sample=load_world_sample(case_dir),
        columns=meta.column_names,
        brief="(test)",
        config=meta.episode,
        scoring=None,
        control_surface=meta.episode.control_surface,
    )
    d = server.describe()
    assert d["schema"] == ["driver", "signal", "outcome", "ambient"]  # deliverable
    assert d["sources"]["registros_linea"]["columns"] == d["schema"]  # measured in place
    # view schemas are EMPIRICAL since D2/D4 (drawn through the real view):
    # the replicate columns sit where the channel actually puts them -- what
    # the agent truly receives, order included.
    assert set(d["sources"]["replicas_calibracion"]["columns"]) == {
        "driver", "signal", "outcome__rep1", "outcome__rep2", "ambient",
    }
    assert "outcome" not in d["sources"]["replicas_calibracion"]["columns"]
    assert "threshold" not in json.dumps(d) and "selection" not in json.dumps(d)

    reps = server.observe("replicas_calibracion", 300)
    assert "outcome" not in reps.columns and "outcome__rep1" in reps.columns
    rec = server.observe("registros_linea", 1500)
    # the view carries the collider: kept rows beat the intensity-adjusted bar
    # on TRUE values; the MEASURED outcome dips below via channel noise
    # (survivorship ordering, v0.53-1) -- fraction far above the population
    # base rate (~0.24) without being 1.0
    assert (rec["signal"] + rec["outcome"] - 2 * rec["driver"] > 1.0).mean() > 0.6

    from wager.contracts import ExperimentDesign

    exp = server.experiment(ExperimentDesign(config={"driver": 5.0}, context={"shift": 0.0}, n=2000))
    clean_var = load_world_sample(case_dir)(
        __import__("types").SimpleNamespace(config={"driver": 5.0}, context={"shift": 0.0}, horizon=None),
        2000, 999,
    )["outcome"].var()
    assert exp["outcome"].var() > clean_var + 1.0  # the meter never sleeps (v0.9)


def test_meter_is_declared_never_positional():
    """v0.58-2 guard WITH its autotest pair (v0.57-1 rule, applied to itself):
    should-pass = declared meter resolves; should-fail = a channel without
    declaration raises instead of guessing positionally."""
    from pathlib import Path

    import pytest as _pytest

    from wager.factory.case_loader import load_meta, load_world_sample
    from wager.harness.world_server import WorldServer

    case_dir = Path(__file__).resolve().parents[1] / "cases" / "selection_bias_v0"
    meta = load_meta(case_dir)
    ws = load_world_sample(case_dir)
    ok = WorldServer(world_sample=ws, columns=meta.column_names, brief="", config=meta.episode,
                     scoring=None, control_surface={})
    assert ok._meter is not None and ok._meter.noise_sd == 1.5   # should-pass

    undeclared = meta.episode.model_copy(update={"experiment_meter": None})
    bad = WorldServer(world_sample=ws, columns=meta.column_names, brief="", config=undeclared,
                      scoring=None, control_surface={})
    with _pytest.raises(ValueError, match="experiment_meter"):    # should-fail
        _ = bad._meter
