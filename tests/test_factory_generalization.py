"""Structural test of the factory generalization pass (Decision Log v0.39).

The class being killed: derivation machinery that RECITES THE DUMMY'S SCHEMA
instead of deriving from the world's declared meta. Two known instances --
hardcoded `cohort` context var, and the twin refit over `effect_dose` (a key
v1 does not have -> silently inert rival, family #13). The kill is structural:
the FULL derivation must run on a world whose schema DIFFERS from the dummy's.
mendel_subtypes_v1 (context var `mix_logit`, params slope_a/slope_b/...) is
that world.
"""

from pathlib import Path
from types import SimpleNamespace

import numpy as np
import pytest

from wager.factory.case_loader import load_meta, load_world_module, load_world_sample
from wager.factory.derive_rivals import (
    build_standard_rivals,
    case_schema,
    free_knobs,
    rival_twin,
)

ROOT = Path(__file__).resolve().parents[1]
V1 = ROOT / "cases" / "mendel_subtypes_v1"
DUMMY = ROOT / "cases" / "dummy_dose_v0"


def _regimes(schema):
    return [
        SimpleNamespace(config={schema.decision: 6.0}, context={schema.context: 0.5}, horizon=None),
        SimpleNamespace(config={}, context={schema.context: -1.0}, horizon=None),
    ]


def test_case_schema_reads_the_declared_meta():
    v1 = case_schema(load_meta(V1))
    assert v1.decision == "dose" and v1.context == "mix_logit"
    assert v1.columns == ("dose", "marker", "outcome")
    # experimentable_range declared in v1's control surface -> 5 levels across it
    assert v1.ctx_levels[0] == pytest.approx(-1.5) and v1.ctx_levels[-1] == pytest.approx(1.5)
    dummy = case_schema(load_meta(DUMMY))
    assert dummy.context == "cohort"  # a DIFFERENT schema: the test's whole point


@pytest.mark.slow
def test_full_derivation_runs_on_a_non_dummy_schema():
    """build_standard_rivals (naive + full ladder + twins) on v1: every rival
    generates the declared columns under do() and observational regimes."""
    meta = load_meta(V1)
    schema = case_schema(meta)
    rivals, pool, train = build_standard_rivals(V1, load_world_sample(V1), meta,
                                                n_pool=800, n_train=60)
    assert schema.context in train.columns  # grid labeled with the DECLARED context
    assert len(rivals) == 4 + len([o for o in meta.operators if o.ablation])
    for fn in rivals:
        for regime in _regimes(schema):
            df = fn(regime, 200, 12345)
            assert list(df.columns) == list(schema.columns)
            assert len(df) == 200 and not df.isna().any().any()


def test_twin_refit_touches_only_declared_knobs():
    """The v0.34-D bug, structurally closed: the refit adjusts ONLY the declared
    knobs of the non-ablated operators -- no hardcoded names, nothing inert."""
    meta = load_meta(V1)
    schema = case_schema(meta)
    wmod = load_world_module(V1)
    pool = load_world_sample(V1)(
        SimpleNamespace(config={}, context={schema.context: 0.0}, horizon=None), 800, 50001
    )
    hetero = next(o for o in meta.operators if o.name == "heterogeneidad_latente")
    conf = next(o for o in meta.operators if o.name == "confounding_por_clase")

    twin_h = rival_twin(wmod.mechanism, wmod.PARAMS, meta, hetero, pool, schema)
    assert twin_h.refit_knobs == ["class_coef_dose"]  # the OTHER operator's knob
    twin_c = rival_twin(wmod.mechanism, wmod.PARAMS, meta, conf, pool, schema)
    assert set(twin_c.refit_knobs) == {"slope_a", "slope_b"}
    # ablation applied; every param outside {ablation, declared free knobs} intact
    assert twin_c.params["class_coef_dose"] == 0.0
    untouched = set(wmod.PARAMS) - {"class_coef_dose"} - set(twin_c.refit_knobs)
    for k in untouched:
        assert twin_c.params[k] == wmod.PARAMS[k], f"{k} moved without declaration"
    # the refit MOVED at least one declared knob (not inert -- the v0.34-D failure)
    assert any(twin_c.params[k] != wmod.PARAMS[k] for k in twin_c.refit_knobs)
    assert any(twin_h.params[k] != wmod.PARAMS[k] for k in twin_h.refit_knobs)


def test_no_dummy_schema_names_hardcoded_in_factory():
    """Audit as regression guard: the dummy's schema words may not appear as
    string literals in the derivation modules (comments/docstrings excluded by
    checking only lines that survive a comment strip)."""
    import re

    banned = re.compile(r"[\"'](cohort|effect_dose|sev_coef|severity)[\"']")
    for mod in ("derive_rivals.py", "battery_builder.py", "certificates.py"):
        text = (ROOT / "wager" / "factory" / mod).read_text(encoding="utf-8")
        for i, line in enumerate(text.splitlines(), 1):
            code = line.split("#", 1)[0]
            assert not banned.search(code), f"{mod}:{i} hardcodes a dummy schema name: {line.strip()}"
