"""Sequential-access guards (rabbit_hole_v1, doctrina 2026-07-11): max_rows,
unlock_after, n_exact. Each guard ships with its should-pass/should-fail pair
(ADR 0057) -- without these three the escalation construct does not exist (an
agent could buy the whole archive in one action, drain a free source, or run
loose-knot micro-campaigns, the v0 failure mode)."""

import numpy as np
import pandas as pd
import pytest

from wager.contracts import ExperimentDesign
from wager.contracts.episode import EpisodeConfig, ExperimentCost, SourceConfig
from wager.contracts.world import Regime
from wager.harness.world_server import ScoringArtifacts, WorldServer


def _world(regime, n, seed):
    rng = np.random.default_rng(seed)
    return pd.DataFrame({"x": rng.normal(0, 1, n), "y": rng.normal(0, 1, n)})


def _server(n_exact=None):
    config = EpisodeConfig(
        budget=10_000.0,
        observe_sources={
            "overview": SourceConfig(cost_per_row=0.0, max_rows=48),
            "layer_1": SourceConfig(cost_per_row=2.0, max_rows=96),
            "layer_2": SourceConfig(cost_per_row=2.0, max_rows=96, unlock_after="layer_1"),
        },
        experiment=ExperimentCost(cost_fixed=100.0, cost_per_row=0.0, n_exact=n_exact),
        experiment_meter="overview",
        smoke_regimes=[Regime(config={}, context={})],
    )
    scoring = ScoringArtifacts(world_source="", naive_code="", null_code="",
                               battery=None, params=None)
    return WorldServer(world_sample=_world, columns=["x", "y"], brief="b",
                       config=config, scoring=scoring)


def test_max_rows_pass_then_fail():
    s = _server()
    assert len(s.observe("overview", 40)) == 40      # under the cap: passes
    assert len(s.observe("overview", 8)) == 8        # exactly exhausts it
    with pytest.raises(ValueError, match="rows left"):
        s.observe("overview", 1)                     # the free source is FINITE


def test_unlock_chain_fail_then_pass():
    s = _server()
    with pytest.raises(ValueError, match="locked"):
        s.observe("layer_2", 10)                     # skipping a layer: refused
    s.observe("layer_1", 10)
    with pytest.raises(ValueError, match="locked"):
        s.observe("layer_2", 10)                     # a token row does NOT unlock
    s.observe("layer_1", 86)                         # layer_1 fully read (96)
    assert len(s.observe("layer_2", 10)) == 10       # now it opens


def test_n_exact_lot_fail_then_pass():
    s = _server(n_exact=20)
    with pytest.raises(ValueError, match="indivisible"):
        s.experiment(ExperimentDesign(config={}, n=5000))   # free-rows exploit dies
    with pytest.raises(ValueError, match="indivisible"):
        s.experiment(ExperimentDesign(config={}, n=3))      # loose-knot lottery dies
    assert len(s.experiment(ExperimentDesign(config={}, n=20))) == 20


def test_guards_inert_for_existing_worlds():
    """None/None defaults leave every pre-v1 case byte-identical."""
    s = _server()
    assert len(s.observe("layer_1", 96)) == 96
    assert len(s.experiment(ExperimentDesign(config={}, n=7))) == 7  # no n_exact
