"""Guards for the LEGAL canonical (ADR 0120) -- guardias con autotest (ADR 0057).

Fast unit guards run always. The two end-to-end certifications are gated behind
WAGER_SLOW=1 (30s each) -- they were RUN GREEN before this guard was installed
(should-pass), and the pre-0120 failure is pinned in git history
(confounded_gen_v0 certificates.json @ R_canonical 0.8929, gates.all=false).
"""

import os
from pathlib import Path
from types import SimpleNamespace as NS

import pytest

from wager.factory.generic_certify import (
    FLOOR, _legal_plan_v0, _partition_gate, _source_is_identity,
)

ROOT = Path(__file__).resolve().parents[1]


def _meta_stub(budget, obs_cost=1.0, exp_fixed=100.0, exp_row=2.0):
    return NS(episode=NS(
        budget=budget,
        observe_sources={"a": NS(cost_per_row=obs_cost)},
        experiment=NS(cost_fixed=exp_fixed, cost_per_row=exp_row),
    ))


# ---------------------------------------------------------------- legal plan --
def test_plan_fits_declared_budget():
    plan = _legal_plan_v0(_meta_stub(20000.0), want_pool=True, reps_src=None)
    assert plan is not None
    assert plan["cost"] <= plan["budget"]
    assert plan["pool_n"] >= 300 and plan["rows_per_cell"] >= 50


def test_plan_fail_closed_on_tiny_budget():
    # even the minimum viable design (3x2x50 rows) cannot fit -> None, and the
    # recoverability gate downstream fails explicitly (no oracular fallback).
    assert _legal_plan_v0(_meta_stub(500.0), want_pool=True, reps_src=None) is None
    assert _legal_plan_v0(_meta_stub(500.0), want_pool=False, reps_src=None) is None


def test_plan_buys_replicas_when_affordable():
    reps = NS(cost_per_row=5.0)
    plan = _legal_plan_v0(_meta_stub(20000.0), want_pool=False, reps_src=reps)
    assert plan is not None and plan["reps_n"] >= 200
    assert plan["cost"] <= plan["budget"]


# ---------------------------------------------------------- source allowlist --
def _src(**kw):
    base = dict(channel=None, selection=None, censoring=None, batch=None,
                hidden_columns=())
    base.update(kw)
    return NS(**base)


def test_identity_source_is_positive_allowlist():
    assert _source_is_identity(_src())
    assert not _source_is_identity(_src(channel=object()))
    assert not _source_is_identity(_src(selection=object()))
    assert not _source_is_identity(_src(censoring=object()))
    assert not _source_is_identity(_src(batch=object()))
    assert not _source_is_identity(_src(hidden_columns=("u",)))


# ------------------------------------------- partition gates (regret form) --
# _partition_gate(canon_scores, s_truth_p, den_full) gates on ABSOLUTE regret
# against the stable full-battery scale (ADR 0120 as amended by Codex ronda 4:
# the earlier 10%-denominator branch had an exploitable cliff + a sign hole).
def test_do_broken_fails_even_if_full_would_pass():
    # regret = (s_truth_p - score)/|den_full|; a do-broken canonical is far
    # below truth on its partition -> way over the 5% bar.
    assert _partition_gate([-0.40, -0.38], s_truth_p=0.0, den_full=1.0) is False
    assert _partition_gate([-0.01, -0.02], s_truth_p=0.0, den_full=1.0) is True


def test_tiny_denominator_noise_passes_but_old_bug_fails():
    # measured live (confounded_gen_v0): the obs partition denominator is ~1.3%
    # of the full scale; the NEW canonical's obs regret is 0.94% of scale ->
    # PASS without dividing by the tiny partition denominator...
    assert _partition_gate([-0.003835, -0.003005], s_truth_p=0.0, den_full=0.409975) is True
    # ...while the PRE-0120 canonical (obs regret ~6.7% of scale) FAILS,
    assert _partition_gate([-0.0275], s_truth_p=0.0, den_full=0.41) is False
    # and the reskin legacy path (4.05% of scale) passes -- barely.
    assert _partition_gate([-0.04307], s_truth_p=0.0, den_full=1.063686) is True


def test_seed_robustness_worst_governs():
    # one good acquisition seed cannot rescue a bad one: MAX regret gates.
    assert _partition_gate([-0.01, -0.08], s_truth_p=0.0, den_full=1.0) is False


# ------------------------------------------------------------- integration ---
slow = pytest.mark.skipif(os.environ.get("WAGER_SLOW") != "1",
                          reason="30s end-to-end certification; set WAGER_SLOW=1")


@slow
def test_confounded_gen_v0_certifies_legal():
    from wager.factory.generic_certify import certify
    rep = certify(ROOT / "cases" / "confounded_gen_v0")
    assert rep["canonical"]["plan"]["cost"] <= rep["canonical"]["plan"]["budget"]
    assert rep["R_canonical"] >= 1.0 - FLOOR
    for k in ("recoverability", "recoverability_do", "recoverability_obs"):
        assert rep["gates"][k], k
    assert rep["gates"]["all"]


@slow
def test_reskin_pilot_v0_regression_still_certifies():
    from wager.factory.generic_certify import certify
    rep = certify(ROOT / "cases" / "reskin_pilot_v0")
    assert rep["canonical"]["plan"]["cost"] <= rep["canonical"]["plan"]["budget"]
    assert rep["gates"]["all"]
