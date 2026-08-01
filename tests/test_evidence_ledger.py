"""The evidence ledger contains exactly the data views available to the agent."""

import numpy as np
import pandas as pd

from wager.contracts import ExperimentDesign
from wager.contracts.episode import (
    EpisodeConfig,
    EpisodeEvent,
    ExperimentCost,
    SourceConfig,
)
from wager.contracts.world import Regime
from wager.harness.world_server import ScoringArtifacts, WorldServer


def _world(regime, n, seed):
    rng = np.random.default_rng(seed)
    return pd.DataFrame({
        "visible": rng.normal(0, 1, n),
        "secret": rng.normal(10, 1, n),
    })


def _server():
    visible = SourceConfig(cost_per_row=0.0, hidden_columns=("secret",))
    event = SourceConfig(cost_per_row=0.0, hidden_columns=("secret",), max_rows=3)
    config = EpisodeConfig(
        budget=100.0,
        observe_sources={"records": visible},
        experiment=ExperimentCost(cost_fixed=0.0, cost_per_row=0.0),
        experiment_meter="records",
        smoke_regimes=[Regime(config={}, context={})],
        events=[EpisodeEvent(
            trigger_turn=2,
            notice="routine report",
            source_name="report_source",
            source=event,
            auto_deliver_n=3,
            delivery_variable="routine_report",
        )],
    )
    scoring = ScoringArtifacts(
        world_source="", naive_code="", null_code="", battery=None, params=None
    )
    return WorldServer(
        world_sample=_world,
        columns=["visible", "secret"],
        brief="brief",
        config=config,
        scoring=scoring,
    )


def test_ledger_records_returned_views_in_order_without_hidden_columns():
    server = _server()
    observed = server.observe("records", 4)
    experimented = server.experiment(ExperimentDesign(config={}, n=2))
    server.begin_turn(2)
    delivered = server.pop_deliveries()[0][1]

    ledger = server.export_evidence_ledger()
    assert [row["kind"] for row in ledger] == [
        "observe", "experiment", "event_report"
    ]
    assert [row["sequence"] for row in ledger] == [1, 2, 3]
    assert ledger[2]["delivery_variable"] == "routine_report"
    assert all(row["data"]["columns"] == ["visible"] for row in ledger)
    assert "secret" not in str(ledger)
    assert ledger[0]["data"]["data"] == observed[["visible"]].values.tolist()
    assert ledger[1]["data"]["data"] == experimented[["visible"]].values.tolist()
    assert ledger[2]["data"]["data"] == delivered[["visible"]].values.tolist()


def test_export_is_detached_from_later_dataframe_mutation():
    server = _server()
    observed = server.observe("records", 2)
    before = server.export_evidence_ledger()
    observed.loc[:, "visible"] = 999.0
    assert server.export_evidence_ledger() == before
