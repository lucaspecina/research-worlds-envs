"""register() -- the own-work verb (lab largo, r21). Should-pass/should-fail
pairs (ADR 0057): the diagnostic is coarse and LATE (begin_turn notices), one
registration per round, bounded in-flight jobs, and a flagged band unlocks
that line's finite focused lot. Inert for every world without RegisterConfig."""

import numpy as np
import pandas as pd
import pytest

from wager.contracts.episode import (
    EpisodeConfig,
    ExperimentCost,
    RegisterConfig,
    SourceConfig,
)
from wager.contracts.world import Regime
from wager.harness.world_server import ScoringArtifacts, WorldServer

GOOD = """
import numpy as np
import pandas as pd

def model(regime, n, seed):
    rng = np.random.default_rng(seed)
    d = float(regime.config["driver"])
    return pd.DataFrame({"outcome": 2.0 * d + rng.normal(0.0, 0.1, n)})
"""

BAD_HIGH = """
import numpy as np
import pandas as pd

def model(regime, n, seed):
    rng = np.random.default_rng(seed)
    d = float(regime.config["driver"])
    y = 2.0 * d + (8.0 if d >= 5.0 else 0.0)   # broken only in the high band
    return pd.DataFrame({"outcome": y + rng.normal(0.0, 0.1, n)})
"""


def _world(regime, n, seed):
    rng = np.random.default_rng(seed)
    d = np.full(n, float(regime.config.get("driver", 5.0)))
    return pd.DataFrame({"outcome": 2.0 * d + rng.normal(0.0, 0.1, n)})


def _server(register=True):
    config = EpisodeConfig(
        budget=1000.0,
        observe_sources={"src": SourceConfig(cost_per_row=1.0)},
        experiment=ExperimentCost(cost_fixed=10.0, cost_per_row=1.0),
        experiment_meter="src",
        smoke_regimes=[Regime(config={}, context={})],
        register=RegisterConfig(lines=(1, 2), bands=((0.0, 5.0), (5.0, 10.0)),
                                panel_n=16, panel_reps=4) if register else None,
    )
    scoring = ScoringArtifacts(world_source="", naive_code="", null_code="",
                               battery=None, params=None)
    return WorldServer(world_sample=_world, columns=["outcome"], brief="b",
                       config=config, scoring=scoring)


def test_inert_without_config_and_guards():
    s = _server(register=False)
    with pytest.raises(ValueError, match="no registration service"):
        s.register(1, GOOD)
    s = _server()
    with pytest.raises(ValueError, match="must be one of"):
        s.register(9, GOOD)


def test_one_per_round_and_max_pending():
    s = _server()
    s.begin_turn(1)
    s.register(1, GOOD)
    with pytest.raises(ValueError, match="ONE registration per round"):
        s.register(2, GOOD)                       # same round: refused
    s.begin_turn(2)                               # delivers job 1's diagnostic
    s.register(2, GOOD)
    s.begin_turn(3)
    s.register(1, GOOD)
    s.begin_turn(4)                               # one pending remains (turn-3 job due now)


def test_diagnostic_arrives_late_and_coarse():
    s = _server()
    s.begin_turn(1)
    ack = s.register(1, GOOD)
    assert ack["diagnostic_turn"] == 2
    notices = s.begin_turn(2)
    assert len(notices) == 1 and "RMSE" in notices[0]
    assert "band" in notices[0]                   # coarse band, never a spectrum
    assert "mini_line_1" not in s._sources        # good model: nothing flagged


def test_flagged_band_unlocks_finite_focused_lot():
    s = _server()
    s.begin_turn(1)
    s.register(1, BAD_HIGH)
    notices = s.begin_turn(2)
    assert "FLAGGED" in notices[0] and "5-10" in notices[0]
    df = s.observe("mini_line_1", 10)             # the focused lot exists...
    assert len(df) == 10
    with pytest.raises(ValueError, match="rows left"):
        s.observe("mini_line_1", 1)               # ...and is FINITE
