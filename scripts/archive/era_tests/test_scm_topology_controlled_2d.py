from types import SimpleNamespace

from wager.harness.case_episode import build_world_server

from scripts import probe_scm_topology_controlled_2d as controlled


def test_controlled_2d_routine_is_pooled_orthogonal_and_neutral():
    assert [row["config"] for row in controlled.ROUTINE_SPECS] == [
        {"feedstock_grade": 5.0, "humidity": 2.5},
        {"feedstock_grade": 5.0, "humidity": 7.5},
    ]
    assert all(
        row["context"] == {"site": "north"} and row["n"] == 60
        for row in controlled.ROUTINE_SPECS
    )
    notice = controlled.ROUTINE_NOTICE.lower()
    assert not any(
        cue in notice for cue in controlled.PROHIBITED_NOTICE_CUES
    )


def test_controlled_2d_local_latent_outcome_projection_is_exact():
    local_server = build_world_server(controlled.topology.LOCAL)
    latent_server = build_world_server(controlled.topology.LATENT)
    for index, spec in enumerate(controlled.ROUTINE_SPECS):
        regime = SimpleNamespace(
            config=spec["config"],
            context=spec["context"],
            horizon=None,
        )
        seed = 7_700_000 + index
        local = local_server.world_sample(regime, spec["n"], seed)
        latent = latent_server.world_sample(regime, spec["n"], seed)
        assert local[["feedstock", "outcome"]].equals(
            latent[["feedstock", "outcome"]]
        )
        assert local["batch_class"].value_counts().to_dict() == (
            latent["batch_class"].value_counts().to_dict()
        )
        assert not local.equals(latent)


def test_v1_injected_tables_expose_exact_design_without_changing_rows():
    server = build_world_server(controlled.topology.LOCAL)
    for index, spec in enumerate(controlled.ROUTINE_SPECS):
        regime = SimpleNamespace(
            config=spec["config"],
            context=spec["context"],
            horizon=None,
        )
        original = server.world_sample(regime, spec["n"], 8_800_000 + index)
        visible = controlled._agent_visible_routine_frame(
            original, spec, "v1"
        )
        assert list(visible.columns) == [
            "site",
            "feedstock_grade",
            "humidity",
            "batch_class",
            "feedstock",
            "outcome",
        ]
        assert set(visible["site"]) == {"north"}
        assert set(visible["feedstock_grade"]) == {5.0}
        assert set(visible["humidity"]) == {spec["config"]["humidity"]}
        assert visible[["batch_class", "feedstock", "outcome"]].equals(
            original
        )


def test_first_cell_submit_gate_rejects_once_then_restores_normal_submit():
    server = build_world_server(controlled.topology.LATENT)
    gate = controlled.FirstCellSubmitGate(server)

    rejected = server.submit("not parsed while the review gate is closed")
    assert not rejected.accepted
    assert rejected.error == controlled.FIRST_CELL_REVIEW_ERROR
    assert not server.terminal
    assert gate.rejected_attempts == 1
    assert server.trajectory[-1].args == {"accepted": False}

    gate.open_next_turn()
    ordinary_rejection = server.submit("not valid model code")
    assert not ordinary_rejection.accepted
    assert ordinary_rejection.error != controlled.FIRST_CELL_REVIEW_ERROR
    assert not server.terminal
    assert gate.rejected_attempts == 1


def test_first_cell_submit_gate_message_is_procedural_not_hypothesis_hint():
    message = controlled.FIRST_CELL_REVIEW_ERROR.lower()
    prohibited = set(controlled.PROHIBITED_NOTICE_CUES) | {
        "wrong",
        "revise",
        "update",
        "model is",
    }
    assert not any(cue in message for cue in prohibited)
