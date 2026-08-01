"""The overgen v0 reference is reconstructed solely from the legal ledger."""

from pathlib import Path

from wager.factory.overgen_stream_tools import (
    _read_prefix,
    _receive_report,
    build_reference_from_ledger,
)
from wager.harness.case_episode import build_world_server
from wager.reward.sandbox import SandboxedSubmission
from wager.contracts.world import Regime


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


def test_prior_preserving_reference_returns_prior_exactly_when_evidence_confirms():
    case_dir = ROOT / "cases" / "overgen_stream_twin_v0"
    server = build_world_server(case_dir, seed_offset=24)
    _read_prefix(server)
    _receive_report(server)
    prior = (case_dir / "truth_code.py").read_text(encoding="utf-8")
    code, diagnostics = build_reference_from_ledger(
        server.export_evidence_ledger(), prior_code=prior
    )
    assert diagnostics["updated_lines"] == []
    assert diagnostics["prior_preserved_byte_exact"]
    assert code == prior


def test_prior_preserving_reference_changes_only_affected_high_range():
    limited = ROOT / "cases" / "overgen_stream_v0"
    server = build_world_server(limited, seed_offset=24)
    _read_prefix(server)
    _receive_report(server)
    prior = (ROOT / "cases" / "overgen_stream_twin_v0" / "truth_code.py").read_text(
        encoding="utf-8"
    )
    code, diagnostics = build_reference_from_ledger(
        server.export_evidence_ledger(), prior_code=prior
    )
    assert diagnostics["updated_lines"] == [2, 3]
    assert diagnostics["preserved_lines"] == [1, 4, 5]
    with (
        SandboxedSubmission(prior, ["outcome"]) as before,
        SandboxedSubmission(code, ["outcome"]) as after,
    ):
        preserved = Regime(config={"line": 4, "driver": 9.0}, context={})
        initial = Regime(config={"line": 2, "driver": 3.0}, context={})
        changed = Regime(config={"line": 2, "driver": 9.0}, context={})
        assert before.run(preserved, 50, 123).equals(after.run(preserved, 50, 123))
        assert before.run(initial, 50, 124).equals(after.run(initial, 50, 124))
        assert not before.run(changed, 50, 125).equals(after.run(changed, 50, 125))


def test_reference_wrapper_supports_prior_with_function_local_imports():
    limited = ROOT / "cases" / "overgen_stream_v0"
    server = build_world_server(limited, seed_offset=25)
    _read_prefix(server)
    _receive_report(server)
    prior = '''
def model(regime, n, seed):
    import numpy as np
    import pandas as pd
    rng = np.random.default_rng(seed)
    d = float(regime.config["driver"])
    return pd.DataFrame({"outcome": rng.normal(14 + 8*d*(10-d)/25, .7, n)})
'''
    code, diagnostics = build_reference_from_ledger(
        server.export_evidence_ledger(), prior_code=prior
    )
    assert diagnostics["updated_lines"] == [2, 3]
    with SandboxedSubmission(code, ["outcome"]) as submission:
        frame = submission.run(
            Regime(config={"line": 2, "driver": 9.0}, context={}), 20, 123
        )
    assert len(frame) == 20
