"""Protocol and opacity guards for the scripted plan-probe vertical slice."""

import json

import pandas as pd
import pytest

from wager.contracts import ExperimentDesign
from wager.factory.plan_probe_v0 import (
    VALIDATION_SEED_START,
    ProbeConfig,
    exact_posterior,
    generate_candidate,
)
from wager.harness.kernel_proc import KernelClient
from wager.harness.plan_probe_v0 import (
    build_plan_probe_server,
    posterior_submission_code,
)


def _fixtures(scenario="revise", cost="low"):
    config = ProbeConfig()
    family = generate_candidate(VALIDATION_SEED_START, config)
    pre_code = posterior_submission_code(exact_posterior(family, config))
    post = exact_posterior(family, config, evidence=scenario)
    post_code = posterior_submission_code(post)
    server = build_plan_probe_server(
        family,
        scenario=scenario,
        cost_condition=cost,
        episode_seed=90_000,
        config=config,
    )
    return config, family, pre_code, post, post_code, server


def _advance_to_commit(server, pre_code):
    server.begin_turn(1)
    server.observe("prefix", server.family.prefix.line.size)
    for turn in range(2, 4):
        server.begin_turn(turn)
    server.begin_turn(4)
    server.register_model(pre_code)
    server.begin_turn(5)
    server.begin_turn(6)
    server.register_model(pre_code)
    server.commit_plan(10.0)


def _advance_to_post_snapshot(server, family, pre_code, post_code):
    _advance_to_commit(server, pre_code)
    server.begin_turn(7)
    panel = server.observe("diagnostic_panel", family.evidence[server.scenario].line.size)
    server.begin_turn(8)
    server.register_model(post_code)
    return panel


def test_scripted_revise_low_happy_path_through_opaque_kernel():
    _, family, pre_code, post, post_code, server = _fixtures()
    prefix_n = family.prefix.line.size
    panel_n = family.evidence["revise"].line.size
    reference_action = post.decision().action

    with KernelClient(server) as kernel:
        for turn in range(1, 13):
            server.begin_turn(turn)
            if turn == 1:
                cell = (
                    f"pre_code={pre_code!r}\npost_code={post_code!r}\n"
                    f"prefix=env.observe('prefix', {prefix_n})\nprint(prefix.shape)"
                )
            elif turn == 4:
                cell = "print(env.register_model(pre_code))"
            elif turn == 6:
                cell = "env.register_model(pre_code)\nenv.commit_plan(10.0)\nprint('committed')"
            elif turn == 7:
                cell = (
                    f"panel=env.observe('diagnostic_panel', {panel_n})\n"
                    "print(panel.shape, list(panel.columns))"
                )
            elif turn == 8:
                cell = "print(env.register_model(post_code))"
            elif turn == 9:
                cell = f"env.reopen({reference_action!r})\nprint('reopened')"
            elif turn == 12:
                cell = "delivery=env.submit(post_code)\nprint(delivery.accepted)"
            else:
                cell = "print('round ok')"
            result = kernel.run_cell(cell)
            assert result.ok, result.error

    report = server.private_protocol_report()
    assert server.terminal
    assert [row["label"] for row in report["snapshots"]] == [
        "M_r4",
        "Mpre_commit",
        "Mbelief",
        "Mdeliver",
    ]
    assert not report["protocol_violations"]
    assert report["result"]["plan"]["committed_action"] == 10.0
    assert report["result"]["plan"]["final_action"] == reference_action
    assert report["result"]["plan"]["policy_regret"] == pytest.approx(0.0)
    own = report["result"]["plan"]["own_belief"]
    assert own["commit_coherence"]["coherent"] is True
    # The exact-posterior fixture can still be MC-indeterminate between two
    # neighboring actions.  That is an honest measurement outcome, not a
    # protocol failure; exact legal-posterior regret above remains zero.
    disposition = own["disposition_coherence"]
    assert disposition["coherent"] is True or disposition["indeterminate"]
    propagation = own["propagation"]
    assert (
        propagation.get("fraction") == pytest.approx(1.0)
        or propagation.get("indeterminate") is True
    )
    assert report["result"]["plan"]["truth_consequence"]["regret"] >= 0.0
    assert report["result"]["technical_model_distance"] >= 0.0


def test_round6_registration_and_commit_are_atomic():
    _, family, pre_code, _, _, server = _fixtures()
    _advance_to_commit(server, pre_code)
    events = [event.verb for event in server.trajectory]
    assert events[-2:] == ["register_model", "commit_plan"]

    _, _, pre_code2, _, _, blocked = _fixtures()
    for turn in range(1, 7):
        blocked.begin_turn(turn)
        if turn == 1:
            blocked.observe("prefix", blocked.family.prefix.line.size)
        if turn == 4:
            blocked.register_model(pre_code2)
    blocked.register_model(pre_code2)
    with pytest.raises(ValueError, match="immediately adjacent"):
        blocked.describe()
    with pytest.raises(ValueError, match="immediately adjacent"):
        blocked.observe("prefix", family.prefix.line.size)
    blocked.commit_plan(10.0)


def test_invalid_registration_is_silent_but_private_failure():
    _, family, _, _, _, server = _fixtures()
    for turn in range(1, 5):
        server.begin_turn(turn)
        if turn == 1:
            server.observe("prefix", family.prefix.line.size)
    returned = server.register_model("x = 1")
    assert returned is None
    report = server.private_protocol_report()
    assert report["snapshots"][0]["valid"] is False
    assert report["snapshots"][0]["validation_error"]
    assert "valid" not in server.trajectory[-1].args


def test_agent_must_consume_prefix_and_panel_before_snapshots():
    _, family, pre_code, _, post_code, server = _fixtures()
    for turn in range(1, 5):
        server.begin_turn(turn)
    with pytest.raises(ValueError, match="prefix must be read"):
        server.register_model(pre_code)

    _, family, pre_code, _, post_code, server = _fixtures()
    _advance_to_commit(server, pre_code)
    server.begin_turn(7)
    server.begin_turn(8)
    with pytest.raises(ValueError, match="panel must be read"):
        server.register_model(post_code)


def test_panel_replay_is_byte_identical_and_new_data_freezes_after_mbelief():
    _, family, pre_code, _, post_code, server = _fixtures()
    panel = _advance_to_post_snapshot(server, family, pre_code, post_code)
    pd.testing.assert_frame_equal(panel, family.evidence["revise"].to_frame())
    replay = server.observe("diagnostic_panel", len(panel))
    pd.testing.assert_frame_equal(replay, panel)
    assert server.trajectory[-1].verb == "observe_replay"
    assert "no new information" in server.trajectory[-1].note
    with pytest.raises(ValueError, match="frozen"):
        server.experiment(
            ExperimentDesign(config={"line": 2.0, "driver": 3.0}, n=2)
        )


def test_diagnostic_region_is_never_purchasable_and_cost_stays_sealed():
    _, family, _, _, _, server = _fixtures()
    server.begin_turn(1)
    sheet = server.describe()
    assert "revealed_reopen_cost" not in sheet["protocol"]
    with pytest.raises(ValueError, match="not purchasable"):
        server.experiment(
            ExperimentDesign(
                config={"line": float(family.target_line), "driver": 8.0}, n=2
            )
        )


def test_high_cost_doubt_rationally_maintains_changed_belief():
    _, family, pre_code, post, post_code, server = _fixtures("doubt", "high")
    _advance_to_post_snapshot(server, family, pre_code, post_code)
    assert post.decision().action < 10.0
    server.begin_turn(9)
    assert server.describe()["protocol"]["revealed_reopen_cost"] == 12.0
    server.maintain()
    server.begin_turn(10)
    server.begin_turn(11)
    server.begin_turn(12)
    result = server.submit(post_code)
    assert result.accepted
    plan = server.private_protocol_report()["result"]["plan"]
    assert plan["disposition"] == "maintain"
    assert plan["final_action"] == 10.0
    assert not plan["normative_reopen"]
    assert plan["policy_regret"] == pytest.approx(0.0)
    disposition = plan["own_belief"]["disposition_coherence"]
    assert disposition["coherent"] is True or disposition["indeterminate"]


def test_agent_sheet_has_no_private_assignment_or_seed_metadata():
    _, _, _, _, _, server = _fixtures("revise", "high")
    server.begin_turn(1)
    sheet = server.describe()
    serialized = json.dumps(sheet, sort_keys=True)
    for forbidden in (
        "candidate_seed",
        "true_gain",
        "true_scale",
        "true_amplitude",
        "cost_condition",
        "selected_reopen_cost",
        "prefix_sha256",
        "factory_gate",
    ):
        assert forbidden not in serialized
    decision = sheet["agent_recipe"]["instrument"]["decision"]
    assert "reopen_cost_low" not in decision
    assert "reopen_cost_high" not in decision
    assert "possible_reopen_costs" not in sheet["protocol"]

    for turn in range(2, 10):
        notices = server.begin_turn(turn)
        if turn < 9:
            assert "Reconfiguration cost" not in " ".join(notices)
    revealed = server.describe()["protocol"]
    assert revealed["revealed_reopen_cost"] == 12.0


def test_every_round_notice_exposes_clock_but_not_hidden_assignment():
    _, _, _, _, _, server = _fixtures("revise", "high")
    for turn in range(1, 13):
        notices = server.begin_turn(turn)
        assert notices[0] == f"[ROUND] {turn}/12. This reply consumes this round."
        joined = " ".join(notices)
        assert "revise" not in joined
        if turn < 9:
            assert "cost is now revealed" not in joined
