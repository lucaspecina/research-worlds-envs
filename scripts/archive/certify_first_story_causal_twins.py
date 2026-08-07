"""Zero-LLM certificate for the paired ecological causal probe.

Checks the shared observational prefix, the intended intervention signatures,
and that neither fixed reflex (change/retain) wins in both hidden worlds.
The script is read-only: it prints a JSON report and exits nonzero on failure.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from types import SimpleNamespace

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from wager.factory.case_loader import load_battery, load_meta, load_world_module
from wager.harness.case_episode import build_world_server
from wager.harness.source_view import source_view
from wager.reward.sandbox import SandboxedSubmission
from wager.reward.scorer import WorldSide, score_callable

REVISE_DIR = ROOT / "cases" / "first_story_causal_revise_v0"
RETAIN_DIR = ROOT / "cases" / "first_story_causal_retain_v0"


def _ns(config):
    return SimpleNamespace(config=dict(config), context={}, horizon=None)


def _mean_effect(world, low, high, *, n=20_000, seed=771_031):
    y_low = world.sample(_ns(low), n, seed)["outcome"].mean()
    y_high = world.sample(_ns(high), n, seed)["outcome"].mean()
    return float(y_high - y_low)


def _null_sample(regime, n, seed):
    import numpy as np

    rng = np.random.default_rng(seed)
    return pd.DataFrame({
        "feedstock": rng.normal(5.0, 1.83, n),
        "outcome": rng.normal(30.0, 3.82, n),
    })


def _score_reflexes(truth_dir, truth_world, change_world, retain_world):
    meta = load_meta(truth_dir)
    world_side = WorldSide(
        truth_world.sample,
        load_battery(truth_dir),
        meta.column_names,
        meta.scoring.n_samples,
        null_sample=_null_sample,
        functionals=list(meta.stakes.functionals),
        c_f=meta.scoring.c_f,
    )
    return {
        "change_always": score_callable(change_world.sample, world_side, meta.scoring),
        "retain_always": score_callable(retain_world.sample, world_side, meta.scoring),
    }


def _sandbox_smoke(case_dir, meta):
    code = (case_dir / "world.py").read_text(encoding="utf-8")
    with SandboxedSubmission(
        code, meta.column_names, timeout_s=meta.scoring.model_call_timeout_s
    ) as submission:
        for regime in meta.episode.smoke_regimes:
            submission.run(regime, 64, 612_003)
    return True


def main():
    revise = load_world_module(REVISE_DIR)
    retain = load_world_module(RETAIN_DIR)
    # Reload the first pole after the second: catches module-name/state bleed.
    revise_again = load_world_module(REVISE_DIR)

    identity_checks = []
    configs = ({}, {"temp": 8.0}, {"line_speed": 2.0}, {"temp": 3.0, "line_speed": 7.0})
    for seed in (13, 2901, 880_041):
        for config in configs:
            left = revise.sample(_ns(config), 257, seed)
            right = retain.sample(_ns(config), 257, seed)
            replay = revise_again.sample(_ns(config), 257, seed)
            pd.testing.assert_frame_equal(left, right, check_exact=True)
            pd.testing.assert_frame_equal(left, replay, check_exact=True)
            identity_checks.append(left.to_numpy(copy=True).tobytes() == right.to_numpy(copy=True).tobytes())

    meta_revise = load_meta(REVISE_DIR)
    meta_retain = load_meta(RETAIN_DIR)
    history_revise = source_view(
        revise.sample, meta_revise.episode.observe_sources["production_history"], 401, 8128
    )
    history_retain = source_view(
        retain.sample, meta_retain.episode.observe_sources["production_history"], 401, 8128
    )
    pd.testing.assert_frame_equal(history_revise, history_retain, check_exact=True)

    effects = {
        "revise_grade": _mean_effect(revise, {"feedstock_grade": 2.0}, {"feedstock_grade": 8.0}),
        "retain_grade": _mean_effect(retain, {"feedstock_grade": 2.0}, {"feedstock_grade": 8.0}),
        "revise_humidity": _mean_effect(revise, {"humidity": 3.0}, {"humidity": 7.0}),
        "retain_humidity": _mean_effect(retain, {"humidity": 3.0}, {"humidity": 7.0}),
    }

    scores = {
        "revise_world": _score_reflexes(REVISE_DIR, revise, revise, retain),
        "retain_world": _score_reflexes(RETAIN_DIR, retain, revise, retain),
    }
    score_gaps = {
        "revise_prefers_change": (
            scores["revise_world"]["change_always"]
            - scores["revise_world"]["retain_always"]
        ),
        "retain_prefers_retain": (
            scores["retain_world"]["retain_always"]
            - scores["retain_world"]["change_always"]
        ),
    }

    # Building both servers checks schema, anchors, smoke contracts and episode wiring.
    build_world_server(REVISE_DIR)
    build_world_server(RETAIN_DIR)
    sandbox_valid = (
        _sandbox_smoke(REVISE_DIR, meta_revise)
        and _sandbox_smoke(RETAIN_DIR, meta_retain)
    )

    gates = {
        "brief_byte_identical": (REVISE_DIR / "brief.md").read_bytes() == (RETAIN_DIR / "brief.md").read_bytes(),
        "battery_byte_identical": (REVISE_DIR / "battery.json").read_bytes() == (RETAIN_DIR / "battery.json").read_bytes(),
        "common_queries_byte_identical": all(identity_checks),
        "history_byte_identical": history_revise.to_numpy(copy=True).tobytes() == history_retain.to_numpy(copy=True).tobytes(),
        "revise_responds_only_to_humidity": abs(effects["revise_grade"]) < 0.15 and effects["revise_humidity"] < -7.5,
        "retain_responds_only_to_grade": effects["retain_grade"] > 11.5 and abs(effects["retain_humidity"]) < 0.15,
        "change_not_universal_winner": score_gaps["revise_prefers_change"] > 0.05,
        "retain_not_universal_winner": score_gaps["retain_prefers_retain"] > 0.05,
        "truth_models_sandbox_valid": sandbox_valid,
    }
    report = {
        "cases": [meta_revise.case_id, meta_retain.case_id],
        "effects_high_minus_low": effects,
        "reflex_scores": scores,
        "score_gaps": score_gaps,
        "gates": gates,
        "all_pass": all(gates.values()),
    }
    print(json.dumps(report, indent=2, sort_keys=True))
    if not report["all_pass"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
