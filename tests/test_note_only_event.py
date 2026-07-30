"""Wiring for NOTE-ONLY events (ADR 0149/0150, mundo del foco): a sealed claim
with no data attached fires at the terminal-spend threshold and unlocks
nothing. Ships its should-fail pair (ADR 0057): a half-declared source is
rejected at validation time."""

import pytest
from pydantic import ValidationError

from wager.contracts.episode import EpisodeEvent, SourceConfig
from wager.harness.case_episode import build_world_server

CASE = "cases/final_note_decoy_v0"


def test_note_only_event_validates():
    ev = EpisodeEvent(trigger_turn=10, trigger_spend_frac=0.85, notice="claim")
    assert ev.source_name is None and ev.source is None


def test_half_declared_source_rejected():
    with pytest.raises(ValidationError):
        EpisodeEvent(trigger_turn=10, notice="claim", source_name="memo")
    with pytest.raises(ValidationError):
        EpisodeEvent(trigger_turn=10, notice="claim",
                     source=SourceConfig(cost_per_row=0.5))


def test_note_fires_on_terminal_spend_and_unlocks_nothing():
    server = build_world_server(CASE, seed_offset=0)
    assert server.begin_turn(1) == []  # nothing spent, early turn: sealed
    sources_before = set(server._sources)
    server._spent = 0.9 * server.config.budget  # terminal-revision territory
    notices = server.begin_turn(2)
    assert len(notices) == 1 and "note pinned" in notices[0]
    assert set(server._sources) == sources_before  # note-only: no unlock
    assert server.begin_turn(3) == []  # fires once


def test_data_events_keep_original_shape():
    ev = EpisodeEvent(trigger_turn=4, notice="news", source_name="log",
                      source=SourceConfig(cost_per_row=0.5))
    assert ev.source_name == "log"
