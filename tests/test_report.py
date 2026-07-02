"""Smoke test for the human-inspection report generator (needs [report] extra).

Uses a SYNTHETIC minimal trace written to tmp_path -- the dossier smoke test must
not depend on committed episode traces (those are evidence artifacts, archived
outside the repo). The synthetic trace carries a valid submission so the
evaluation section re-scores and renders the grading table.
"""

import importlib.util
import json
from pathlib import Path

import pytest

CASE_DIR = Path(__file__).resolve().parents[1] / "cases" / "dummy_dose_v0"

# a valid (deliberately mediocre) submission over the exact schema, so the report
# can re-score it and render "final R" / "Per-item grading"
_SUBMISSION = (
    "import numpy as np, pandas as pd\n"
    "def model(regime, n, seed):\n"
    "    rng = np.random.default_rng(seed)\n"
    "    d = regime.config.get('dose')\n"
    "    dose = np.full(n, float(d)) if d is not None else rng.uniform(0, 10, n)\n"
    "    return pd.DataFrame({'dose': dose,\n"
    "                         'marker': rng.normal(0, 1, n),\n"
    "                         'outcome': 5.0 + rng.normal(0, 1, n)})\n"
)

_TRACE = {
    "model": "test-model",
    "R": 0.5,
    "R_unclipped": 0.5,
    "turns": 1,
    "tokens": {"total": 100},
    "wall_seconds": 1.0,
    "accepted": True,
    "abort_reason": "submitted",
    "budget_spent": 100,
    "budget_total": 1000,
    "signal": {
        "attribution_before_experiment": True,
        "first_attribution_turn": 1,
        "first_experiment_turn": 2,
    },
    "verbs": [{"verb": "observe", "args": {"source": "registros_proceso_2019_2023", "n": 50},
               "cost": 50, "budget_remaining": 950, "note": ""}],
    "trace": [{"turn": 1, "reply_text": "inspect the records then submit",
               "cell": "print(df.shape)", "cell_result": {"stdout": "(50, 3)"}}],
    "submission_code": _SUBMISSION,
}


@pytest.mark.slow
@pytest.mark.skipif(importlib.util.find_spec("markdown") is None, reason="install .[report]")
def test_build_report_has_all_sections(tmp_path):
    from wager.report.case_report import build_report

    trace = tmp_path / "synthetic_trace.json"
    trace.write_text(json.dumps(_TRACE), encoding="utf-8")
    html = build_report(CASE_DIR, trace)
    for needle in ("<html>", "The brief", "The hidden truth", "secret exam",
                   "agent&#x27;s full trajectory", "The evaluation"):
        assert needle in html, needle
    # the synthetic trace carries a submission -> the evaluation re-scored it
    assert "final R" in html and "Per-item grading" in html
