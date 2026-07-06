"""Sealed mid-episode events (D4, ADR 0081) + hidden view columns (D2).

Should-pass / should-fail pairs (ADR 0057 rule): the event source is INVISIBLE
before firing and observable after; the trigger is min(turn, spend-fraction);
hidden_columns never leak through records OR experiments.
"""

import numpy as np
import pandas as pd
import pytest

from wager.contracts import ExperimentDesign
from wager.contracts.episode import (EpisodeConfig, EpisodeEvent, ExperimentCost,
                                     MeasurementChannel, SourceConfig)
from wager.contracts.world import Regime
from wager.harness.world_server import ScoringArtifacts, WorldServer


def _world(regime, n, seed):
    rng = np.random.default_rng(seed)
    secret = rng.normal(5.0, 1.0, n)
    return pd.DataFrame({"secret": secret,
                         "x": secret + rng.normal(0, 1, n),
                         "y": 2 * secret + rng.normal(0, 1, n)})


def _server():
    record = SourceConfig(cost_per_row=1.0,
                          channel=MeasurementChannel(column="y", noise_sd=0.5),
                          hidden_columns=("secret",))
    event_source = SourceConfig(cost_per_row=1.0, hidden_columns=("x", "y"))
    config = EpisodeConfig(
        budget=1000.0,
        observe_sources={"registros": record},
        experiment=ExperimentCost(cost_fixed=10.0, cost_per_row=1.0),
        experiment_meter="registros",
        smoke_regimes=[Regime(config={}, context={})],
        events=[EpisodeEvent(trigger_turn=3, trigger_spend_frac=0.5,
                             notice="the log appeared", source_name="log",
                             source=event_source)],
    )
    scoring = ScoringArtifacts(world_source="", naive_code="", null_code="",
                               battery=None, params=None)
    return WorldServer(world_sample=_world, columns=["x", "y"], brief="b",
                       config=config, scoring=scoring)


def test_hidden_columns_never_leak():
    s = _server()
    df = s.observe("registros", 50)
    assert "secret" not in df.columns and {"x", "y"} <= set(df.columns)
    dfe = s.experiment(ExperimentDesign(config={}, n=50))
    assert "secret" not in dfe.columns


def test_event_source_invisible_then_unlocked_by_turn():
    s = _server()
    assert "log" not in s.describe()["sources"]          # should-fail before
    with pytest.raises(KeyError):
        s.observe("log", 10)
    assert s.begin_turn(1) == [] and s.begin_turn(2) == []
    notices = s.begin_turn(3)                            # turn trigger
    assert notices == ["the log appeared"]
    assert "log" in s.describe()["sources"]
    df = s.observe("log", 20)                            # should-pass after
    assert list(df.columns) == ["secret"]                # the sealed payload
    assert s.begin_turn(4) == []                         # fires once


def test_event_fires_early_by_spend_fraction():
    s = _server()
    s.observe("registros", 600)                          # 600/1000 = 60% >= 50%
    notices = s.begin_turn(2)                            # before trigger_turn=3
    assert notices == ["the log appeared"]
