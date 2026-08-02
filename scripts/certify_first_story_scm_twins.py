"""Zero-LLM certificates for the paired hidden-SCM first-story worlds.

The script is intentionally read-only.  It checks observational identity,
intervention/RNG semantics, standard WorldServer wiring, the diagnostic
campaign's power, and fixed structural robot losses.  It prints one JSON
report and exits non-zero if any gate fails.
"""

from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path
from types import SimpleNamespace

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from wager.factory.case_loader import (  # noqa: E402
    load_battery,
    load_ladder,
    load_meta,
    load_world_module,
)
from wager.harness.case_episode import build_world_server  # noqa: E402
from wager.harness.source_view import source_view  # noqa: E402
from wager.reward.scorer import (  # noqa: E402
    WorldSide,
    make_anchors,
    sandboxed_null_sample,
    score_submission,
)

REVISE_DIR = ROOT / "cases" / "first_story_scm_revise_v0"
RETAIN_DIR = ROOT / "cases" / "first_story_scm_retain_v0"


def _ns(config: dict | None = None) -> SimpleNamespace:
    return SimpleNamespace(config=dict(config or {}), context={}, horizon=None)


def _code(case_dir: Path, relative: str) -> str:
    return (case_dir / relative).read_text(encoding="utf-8")


def _load_python(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _agent_facing_meta(case_dir: Path) -> dict:
    raw = json.loads((case_dir / "meta.json").read_text(encoding="utf-8"))
    raw.pop("case_id")
    raw.pop("operators")
    return raw


def _meta_without_case_id(case_dir: Path) -> dict:
    raw = json.loads((case_dir / "meta.json").read_text(encoding="utf-8"))
    raw.pop("case_id")
    return raw


def _score_structural_models(case_dir: Path) -> dict:
    """Score the fixed SCM reflexes once per world with shared world-side CRN."""
    meta = load_meta(case_dir)
    world = load_world_module(case_dir)
    ladder = dict(load_ladder(case_dir))
    truth = _code(case_dir, "truth_code.py")
    revise = _code(REVISE_DIR, "truth_code.py")
    retain = _code(RETAIN_DIR, "truth_code.py")
    prior = ladder["rung_7_prior"]
    null = ladder["rung_8_null"]
    with sandboxed_null_sample(
        null, meta.column_names, meta.scoring.model_call_timeout_s
    ) as null_sample:
        world_side = WorldSide(
            world.sample,
            load_battery(case_dir),
            meta.column_names,
            meta.scoring.n_samples,
            null_sample=null_sample,
            functionals=list(meta.stakes.functionals),
            c_f=meta.scoring.c_f,
        )
        reports = {
            "truth": score_submission(truth, world_side, meta.scoring),
            "revise": score_submission(revise, world_side, meta.scoring),
            "retain": score_submission(retain, world_side, meta.scoring),
            "prior": score_submission(prior, world_side, meta.scoring),
            "null": score_submission(null, world_side, meta.scoring),
        }
        anchors = make_anchors(
            reports["truth"].raw_score,
            reports["prior"].raw_score,
            reports["null"].raw_score,
        )
        scores = {}
        for name, report in reports.items():
            r, r_unclipped = anchors.r_of(report.raw_score)
            scores[name] = {
                "R": float(r),
                "R_unclipped": float(r_unclipped),
                "raw_score": float(report.raw_score),
                "errors": int(sum(item.sandbox_errors for item in report.items)),
            }
    scores["denom_raw"] = float(
        reports["truth"].raw_score - reports["prior"].raw_score
    )
    return scores


def _campaign_power(revise, retain, *, n_per_arm: int = 30) -> dict:
    correct = {"revise": 0, "retain": 0}
    deltas = {"revise": [], "retain": []}
    for idx in range(100):
        for pole, world in (("revise", revise), ("retain", retain)):
            low = world.sample(
                _ns({"humidity": 5.0, "feedstock_grade": 3.0}),
                n_per_arm,
                610_000 + 2 * idx,
            )
            high = world.sample(
                _ns({"humidity": 5.0, "feedstock_grade": 7.0}),
                n_per_arm,
                610_001 + 2 * idx,
            )
            delta = float(high["outcome"].mean() - low["outcome"].mean())
            chosen = "retain" if abs(delta) > 4.0 else "revise"
            correct[pole] += int(chosen == pole)
            deltas[pole].append(delta)
    # Each arm differs by four outcome units between hypotheses and sigma=2:
    # KL per row = delta_mu^2/(2*sigma^2)=2, across two arms = 4*n.
    return {
        "n_per_arm": n_per_arm,
        "expected_llr": float(4 * n_per_arm),
        "accuracy": {pole: value / 100.0 for pole, value in correct.items()},
        "mean_delta": {pole: float(np.mean(values)) for pole, values in deltas.items()},
    }


def main() -> None:
    revise = load_world_module(REVISE_DIR)
    retain = load_world_module(RETAIN_DIR)
    revise_reloaded = load_world_module(REVISE_DIR)
    meta_revise = load_meta(REVISE_DIR)
    meta_retain = load_meta(RETAIN_DIR)

    natural_identity = []
    replay_identity = []
    visible_columns = []
    for n in (1, 17, 257):
        for seed in (0, 13, 2901, 880_041):
            left = revise.sample(_ns(), n, seed)
            right = retain.sample(_ns(), n, seed)
            replay = revise_reloaded.sample(_ns(), n, seed)
            natural_identity.append(left.equals(right))
            replay_identity.append(left.equals(replay))
            visible_columns.append(list(left.columns) == ["feedstock", "outcome"])

    history_revise = source_view(
        revise.sample,
        meta_revise.episode.observe_sources["production_history"],
        500,
        711_043,
    )
    history_retain = source_view(
        retain.sample,
        meta_retain.episode.observe_sources["production_history"],
        500,
        711_043,
    )

    natural_large = revise.sample(_ns(), 50_000, 880_501)
    historical_corr = float(
        natural_large[["feedstock", "outcome"]].corr().iloc[0, 1]
    )

    paired_configs = (
        {},
        {"humidity": 3.0},
        {"humidity": 7.0},
        {"feedstock_grade": 3.0},
        {"feedstock_grade": 7.0},
        {"humidity": 3.0, "feedstock_grade": 7.0},
        {"humidity": 7.0, "feedstock_grade": 3.0},
        {"humidity": 5.0, "feedstock_grade": 3.0},
        {"humidity": 5.0, "feedstock_grade": 7.0},
        {"humidity": 3.0, "feedstock_grade": 3.0},
        {"humidity": 7.0, "feedstock_grade": 7.0},
    )
    feedstock_identity = []
    humidity_only_identity = []
    manifold_identity = []
    off_manifold_errors = []
    for config in paired_configs:
        left = revise.sample(_ns(config), 313, 991_007)
        right = retain.sample(_ns(config), 313, 991_007)
        feedstock_identity.append(
            np.array_equal(left["feedstock"].to_numpy(), right["feedstock"].to_numpy())
        )
        if "feedstock_grade" not in config:
            humidity_only_identity.append(left.equals(right))
        else:
            hidden = revise._latent_sample(_ns(config), 313, 991_007)
            expected = 2.0 * (
                hidden["humidity"].to_numpy()
                + hidden["grade"].to_numpy()
                - 10.0
            )
            observed = (
                right["outcome"].to_numpy() - left["outcome"].to_numpy()
            )
            off_manifold_errors.append(float(np.max(np.abs(observed - expected))))
            if "humidity" in config and (
                float(config["humidity"]) + float(config["feedstock_grade"]) == 10.0
            ):
                manifold_identity.append(left.equals(right))

    # Exogenous draw order is configuration-invariant and equal across twins.
    exo_revise = revise._draw_exogenous(37, 330_019)
    exo_retain = retain._draw_exogenous(37, 330_019)
    exogenous_identical = all(
        np.array_equal(left, right) for left, right in zip(exo_revise, exo_retain)
    )
    latent_noise_checks = []
    for world in (revise, retain):
        era, eps_h, eps_f, eps_y = world._draw_exogenous(37, 330_019)
        del era, eps_h
        for config in ({}, {"humidity": 4.25}, {"feedstock_grade": 6.75},
                       {"humidity": 4.25, "feedstock_grade": 6.75}):
            hidden = world._latent_sample(_ns(config), 37, 330_019)
            latent_noise_checks.append(
                np.allclose(hidden["feedstock"] - hidden["grade"], eps_f, atol=1e-14)
            )
            mu = (
                40.0 - 2.0 * hidden["humidity"]
                if world.POLE == "revise" or "feedstock_grade" not in config
                else 20.0 + 2.0 * hidden["grade"]
            )
            latent_noise_checks.append(
                np.allclose(hidden["outcome"] - mu, eps_y, atol=1e-14)
            )

    # Standard episode replay: same verb order and seed offset on both twins.
    server_revise = build_world_server(REVISE_DIR, seed_offset=71)
    server_retain = build_world_server(RETAIN_DIR, seed_offset=71)
    observed_revise = server_revise.observe("production_history", 173)
    observed_retain = server_retain.observe("production_history", 173)
    from wager.contracts import ExperimentDesign

    h_revise = server_revise.experiment(
        ExperimentDesign(config={"humidity": 6.0}, n=41)
    )
    h_retain = server_retain.experiment(
        ExperimentDesign(config={"humidity": 6.0}, n=41)
    )
    joint_revise = server_revise.experiment(
        ExperimentDesign(config={"humidity": 5.0, "feedstock_grade": 7.0}, n=41)
    )
    joint_retain = server_retain.experiment(
        ExperimentDesign(config={"humidity": 5.0, "feedstock_grade": 7.0}, n=41)
    )
    replay_ledger = {
        "history_equal": observed_revise.equals(observed_retain),
        "humidity_equal": h_revise.equals(h_retain),
        "joint_feedstock_equal": np.array_equal(
            joint_revise["feedstock"].to_numpy(),
            joint_retain["feedstock"].to_numpy(),
        ),
        "joint_mean_delta": float(
            (joint_retain["outcome"] - joint_revise["outcome"]).mean()
        ),
        "budget_equal": server_revise.budget_remaining == server_retain.budget_remaining,
    }

    smoke_errors = {
        "revise": server_revise.validate_model(_code(REVISE_DIR, "truth_code.py")),
        "retain": server_retain.validate_model(_code(RETAIN_DIR, "truth_code.py")),
    }
    robots = _load_python(REVISE_DIR / "robots.py", "first_story_scm_robots")
    robot_smoke_errors = {
        f"{case}_{pole}": server.validate_model(robots._pole_code(pole))
        for case, server in (("revise", server_revise), ("retain", server_retain))
        for pole in ("revise", "retain")
    }
    robot_smoke_errors["revise_prior"] = server_revise.validate_model(
        robots._prior_code()
    )
    score_revise = _score_structural_models(REVISE_DIR)
    score_retain = _score_structural_models(RETAIN_DIR)
    campaign = _campaign_power(revise, retain)

    battery = load_battery(REVISE_DIR)
    diagnostic_weight = float(
        sum(
            item.weight
            for item in battery.items
            if "feedstock_grade" in item.regime.config
            and (
                "humidity" not in item.regime.config
                or item.regime.config["humidity"] + item.regime.config["feedstock_grade"] != 10
            )
        )
    )

    gates = {
        "brief_byte_identical": _code(REVISE_DIR, "brief.md") == _code(RETAIN_DIR, "brief.md"),
        "battery_byte_identical": (REVISE_DIR / "battery.json").read_bytes() == (RETAIN_DIR / "battery.json").read_bytes(),
        "agent_facing_meta_identical": _agent_facing_meta(REVISE_DIR) == _agent_facing_meta(RETAIN_DIR),
        "meta_differs_only_by_case_id": _meta_without_case_id(REVISE_DIR) == _meta_without_case_id(RETAIN_DIR),
        "world_source_differs_only_by_pole": _code(REVISE_DIR, "world.py").replace('POLE = "revise"', 'POLE = "paired"') == _code(RETAIN_DIR, "world.py").replace('POLE = "retain"', 'POLE = "paired"'),
        "prior_rival_byte_identical": _code(REVISE_DIR, "ladder/rung_7_prior.py") == _code(RETAIN_DIR, "ladder/rung_7_prior.py"),
        "null_rival_byte_identical": _code(REVISE_DIR, "ladder/rung_8_null.py") == _code(RETAIN_DIR, "ladder/rung_8_null.py"),
        "episode_robots_byte_identical": (REVISE_DIR / "robots.py").read_bytes() == (RETAIN_DIR / "robots.py").read_bytes(),
        "only_deliverable_columns_visible": all(visible_columns),
        "natural_frames_exact_twins": all(natural_identity),
        "world_reload_replays_exactly": all(replay_identity),
        "observational_source_exact_twins": history_revise.equals(history_retain),
        "historical_llr_zero_by_identity": history_revise.equals(history_retain),
        "historical_correlation_seductive": 0.65 <= historical_corr <= 0.90,
        "humidity_only_is_nondiagnostic": all(humidity_only_identity),
        "joint_manifold_is_nondiagnostic_exactly": all(manifold_identity),
        "feedstock_rng_common_all_regimes": all(feedstock_identity),
        "off_manifold_delta_is_mechanical": max(off_manifold_errors) < 1e-12,
        "exogenous_draws_exact_twins": exogenous_identical,
        "exogenous_noise_reused_across_branches": all(latent_noise_checks),
        "worldserver_replay_history_exact": replay_ledger["history_equal"],
        "worldserver_replay_humidity_exact": replay_ledger["humidity_equal"],
        "worldserver_replay_joint_common_f": replay_ledger["joint_feedstock_equal"],
        "worldserver_replay_joint_expected_delta": abs(replay_ledger["joint_mean_delta"] - 4.0) < 1e-12,
        "worldserver_replay_budget_exact": replay_ledger["budget_equal"],
        "truth_fixtures_smoke_valid": all(value is None for value in smoke_errors.values()),
        "episode_robot_models_smoke_valid": all(value is None for value in robot_smoke_errors.values()),
        "battery_weights_sum_one": abs(sum(item.weight for item in battery.items) - 1.0) < 1e-12,
        "battery_diagnostic_weight": abs(diagnostic_weight - 0.76) < 1e-12,
        "truth_fixtures_reach_ceiling": score_revise["truth"]["R"] >= 0.99 and score_retain["truth"]["R"] >= 0.99,
        "truth_fixtures_zero_errors": score_revise["truth"]["errors"] == 0 and score_retain["truth"]["errors"] == 0,
        "never_update_loses_revise": score_revise["retain"]["R"] <= 0.20,
        "never_update_wins_retain": score_retain["retain"]["R"] >= 0.90,
        "associational_extension_loses_revise": score_revise["retain"]["R"] <= 0.20,
        "change_always_wins_revise": score_revise["revise"]["R"] >= 0.90,
        "change_always_loses_retain": score_retain["revise"]["R"] <= 0.20,
        "prior_is_common_zero_point": abs(score_revise["prior"]["R_unclipped"]) < 1e-12 and abs(score_retain["prior"]["R_unclipped"]) < 1e-12,
        "humidity_only_robot_cannot_beat_prior": all(humidity_only_identity) and abs(score_revise["prior"]["R_unclipped"]) < 1e-12 and abs(score_retain["prior"]["R_unclipped"]) < 1e-12,
        "reward_denominator_resolved": score_revise["denom_raw"] > 0.05 and score_retain["denom_raw"] > 0.05,
        "adaptive_campaign_identifies_both": min(campaign["accuracy"].values()) >= 0.90,
        "adaptive_robot_reaches_both_ceilings": score_revise["revise"]["R"] >= 0.80 and score_retain["retain"]["R"] >= 0.80,
        "adaptive_campaign_expected_llr_large": campaign["expected_llr"] >= 20.0,
    }
    report = {
        "cases": [meta_revise.case_id, meta_retain.case_id],
        "historical_correlation": historical_corr,
        "max_off_manifold_delta_error": max(off_manifold_errors),
        "diagnostic_battery_weight": diagnostic_weight,
        "replay_ledger": replay_ledger,
        "campaign": campaign,
        "structural_robot_scores": {
            "revise_world": score_revise,
            "retain_world": score_retain,
        },
        "smoke_errors": smoke_errors,
        "robot_smoke_errors": robot_smoke_errors,
        "gates": gates,
        "all_pass": all(gates.values()),
    }
    print(json.dumps(report, indent=2, sort_keys=True))
    if not report["all_pass"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
