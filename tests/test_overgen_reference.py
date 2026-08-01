"""The overgen v0 reference is reconstructed solely from the legal ledger."""

from pathlib import Path

from wager.factory.overgen_stream_tools import (
    _read_prefix,
    _receive_report,
    build_reference_from_ledger,
)
from wager.harness.case_episode import build_world_server


ROOT = Path(__file__).resolve().parents[1]


def _reference_result(case_name, seed_offset):
    server = build_world_server(ROOT / "cases" / case_name, seed_offset=seed_offset)
    _read_prefix(server)
    _receive_report(server)
    code, diagnostics = build_reference_from_ledger(server.export_evidence_ledger())
    accepted = server.submit(code)
    assert accepted.accepted
    return diagnostics, server.result["R"]


def test_reference_selectively_updates_limited_transfer_world():
    diagnostics, score = _reference_result("overgen_stream_v0", 20)
    assert diagnostics["updated_lines"] == [2, 3]
    assert score >= 0.72


def test_reference_maintains_all_lines_in_transfer_twin():
    diagnostics, score = _reference_result("overgen_stream_twin_v0", 20)
    assert diagnostics["updated_lines"] == []
    assert score >= 0.80
