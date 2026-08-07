"""Zero-LLM certificates for the paired South-to-North SCM transfer worlds.

Read-only: loads persisted cases, samples/scorers, and prints one JSON report.
It never edits a case and exits non-zero if any causal, pairing, schema, or
reward gate fails.
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

from wager.contracts import ExperimentDesign  # noqa: E402
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

REVISE_DIR = ROOT / "cases" / "first_story_scm_transfer_revise_v0"
RETAIN_DIR = ROOT / "cases" / "first_story_scm_transfer_retain_v0"


def _ns(
    config: dict | None = None,
    *,
    site: str = "south",
) -> SimpleNamespace:
    return SimpleNamespace(
        config=dict(config or {}), context={"site": site}, horizon=None
    )


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
    """Score both transfer hypotheses with one shared world-side draw."""
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
            r_value, r_unclipped = anchors.r_of(report.raw_score)
            scores[name] = {
                "R": float(r_value),
                "R_unclipped": float(r_unclipped),
                "raw_score": float(report.raw_score),
                "errors": int(sum(item.sandbox_errors for item in report.items)),
            }
    scores["denom_raw"] = float(
        reports["truth"].raw_score - reports["prior"].raw_score
    )
    return scores


def _north_campaign_power(revise, retain, *, n_per_arm: int = 30) -> dict:
    correct = {"revise": 0, "retain": 0}
    deltas = {"revise": [], "retain": []}
    for idx in range(100):
        for pole, world in (("revise", revise), ("retain", retain)):
            low = world.sample(
                _ns({"humidity": 5.0, "feedstock_grade": 3.0}, site="north"),
                n_per_arm,
                620_000 + 2 * idx,
            )
            high = world.sample(
                _ns({"humidity": 5.0, "feedstock_grade": 7.0}, site="north"),
                n_per_arm,
                620_001 + 2 * idx,
            )
            delta = float(high["outcome"].mean() - low["outcome"].mean())
            chosen = "retain" if abs(delta) > 4.0 else "revise"
            correct[pole] += int(chosen == pole)
            deltas[pole].append(delta)
    return {
        "n_per_arm": n_per_arm,
        "expected_llr": float(4 * n_per_arm),
        "accuracy": {pole: value / 100.0 for pole, value in correct.items()},
        "mean_delta": {
            pole: float(np.mean(values)) for pole, values in deltas.items()
        },
    }


def main() -> None:
    revise = load_world_module(REVISE_DIR)
    retain = load_world_module(RETAIN_DIR)
    meta_revise = load_meta(REVISE_DIR)
    meta_retain = load_meta(RETAIN_DIR)

    paired_configs = (
        {},
        {"humidity": 3.0},
        {"humidity": 7.0},
        {"feedstock_grade": 3.0},
        {"feedstock_grade": 7.0},
        {"humidity": 5.0, "feedstock_grade": 3.0},
        {"humidity": 5.0, "feedstock_grade": 7.0},
        {"humidity": 3.0, "feedstock_grade": 7.0},
        {"humidity": 7.0, "feedstock_grade": 3.0},
    )
    south_all_actions_exact = []
    north_natural_humidity_exact = []
    north_feedstock_exact = []
    north_off_manifold_errors = []
    visible_schema = []
    replay_exact = []
    for n in (1, 17, 257):
        for seed in (0, 13, 2901, 880_041):
            for config in paired_configs:
                south_left = revise.sample(_ns(config, site="south"), n, seed)
                south_right = retain.sample(_ns(config, site="south"), n, seed)
                south_all_actions_exact.append(south_left.equals(south_right))
                visible_schema.append(
                    list(south_left.columns) == ["feedstock", "outcome"]
                )
                replay_exact.append(
                    south_left.equals(
                        revise.sample(_ns(config, site="south"), n, seed)
                    )
                )

                north_left = revise.sample(_ns(config, site="north"), n, seed)
                north_right = retain.sample(_ns(config, site="north"), n, seed)
                north_feedstock_exact.append(
                    np.array_equal(
                        north_left["feedstock"].to_numpy(),
                        north_right["feedstock"].to_numpy(),
                    )
                )
                if "feedstock_grade" not in config:
                    north_natural_humidity_exact.append(
                        north_left.equals(north_right)
                    )
                else:
                    hidden = revise._latent_sample(
                        _ns(config, site="north"), n, seed
                    )
                    expected = 2.0 * (
                        hidden["humidity"].to_numpy()
                        + hidden["grade"].to_numpy()
                        - 10.0
                    )
                    observed = (
                        north_right["outcome"].to_numpy()
                        - north_left["outcome"].to_numpy()
                    )
                    north_off_manifold_errors.append(
                        float(np.max(np.abs(observed - expected)))
                    )

    source_revise = source_view(
        revise.sample,
        meta_revise.episode.observe_sources["south_production_history"],
        500,
        721_043,
    )
    source_retain = source_view(
        retain.sample,
        meta_retain.episode.observe_sources["south_production_history"],
        500,
        721_043,
    )
    south_large = revise.sample(_ns(site="south"), 50_000, 880_501)
    south_corr = float(
        south_large[["feedstock", "outcome"]].corr().iloc[0, 1]
    )

    exo_revise = revise._draw_exogenous(37, 330_019)
    exo_retain = retain._draw_exogenous(37, 330_019)
    exogenous_identical = all(
        np.array_equal(left, right)
        for left, right in zip(exo_revise, exo_retain)
    )

    # Standard WorldServer wiring, including string-valued site context.
    server_revise = build_world_server(REVISE_DIR, seed_offset=71)
    server_retain = build_world_server(RETAIN_DIR, seed_offset=71)
    observed_revise = server_revise.observe("south_production_history", 173)
    observed_retain = server_retain.observe("south_production_history", 173)
    south_joint_revise = server_revise.experiment(
        ExperimentDesign(
            config={"humidity": 5.0, "feedstock_grade": 7.0},
            context={"site": "south"},
            n=41,
        )
    )
    south_joint_retain = server_retain.experiment(
        ExperimentDesign(
            config={"humidity": 5.0, "feedstock_grade": 7.0},
            context={"site": "south"},
            n=41,
        )
    )
    north_h_revise = server_revise.experiment(
        ExperimentDesign(
            config={"humidity": 6.0}, context={"site": "north"}, n=41
        )
    )
    north_h_retain = server_retain.experiment(
        ExperimentDesign(
            config={"humidity": 6.0}, context={"site": "north"}, n=41
        )
    )
    north_joint_revise = server_revise.experiment(
        ExperimentDesign(
            config={"humidity": 5.0, "feedstock_grade": 7.0},
            context={"site": "north"},
            n=41,
        )
    )
    north_joint_retain = server_retain.experiment(
        ExperimentDesign(
            config={"humidity": 5.0, "feedstock_grade": 7.0},
            context={"site": "north"},
            n=41,
        )
    )
    replay_ledger = {
        "south_history_equal": observed_revise.equals(observed_retain),
        "south_joint_equal": south_joint_revise.equals(south_joint_retain),
        "north_humidity_equal": north_h_revise.equals(north_h_retain),
        "north_joint_feedstock_equal": np.array_equal(
            north_joint_revise["feedstock"].to_numpy(),
            north_joint_retain["feedstock"].to_numpy(),
        ),
        "north_joint_mean_delta": float(
            (north_joint_retain["outcome"] - north_joint_revise["outcome"]).mean()
        ),
        "budget_equal": (
            server_revise.budget_remaining == server_retain.budget_remaining
        ),
    }

    smoke_errors = {
        "revise": server_revise.validate_model(_code(REVISE_DIR, "truth_code.py")),
        "retain": server_retain.validate_model(_code(RETAIN_DIR, "truth_code.py")),
    }
    robots = _load_python(
        REVISE_DIR / "robots.py", "first_story_scm_transfer_robots"
    )
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
    campaign = _north_campaign_power(revise, retain)
    battery = load_battery(REVISE_DIR)
    south_weight = float(
        sum(
            item.weight
            for item in battery.items
            if item.regime.context.get("site") == "south"
        )
    )
    north_weight = float(
        sum(
            item.weight
            for item in battery.items
            if item.regime.context.get("site") == "north"
        )
    )
    north_diagnostic_weight = float(
        sum(
            item.weight
            for item in battery.items
            if item.regime.context.get("site") == "north"
            and "feedstock_grade" in item.regime.config
        )
    )

    world_normalized_revise = _code(REVISE_DIR, "world.py").replace(
        'POLE = "revise"', 'POLE = "paired"'
    )
    world_normalized_retain = _code(RETAIN_DIR, "world.py").replace(
        'POLE = "retain"', 'POLE = "paired"'
    )
    source_spec = meta_revise.episode.observe_sources["south_production_history"]
    gates = {
        "brief_byte_identical": (
            (REVISE_DIR / "brief.md").read_bytes()
            == (RETAIN_DIR / "brief.md").read_bytes()
        ),
        "battery_byte_identical": (
            (REVISE_DIR / "battery.json").read_bytes()
            == (RETAIN_DIR / "battery.json").read_bytes()
        ),
        "agent_facing_meta_identical": (
            _agent_facing_meta(REVISE_DIR) == _agent_facing_meta(RETAIN_DIR)
        ),
        "meta_differs_only_case_id": (
            _meta_without_case_id(REVISE_DIR) == _meta_without_case_id(RETAIN_DIR)
        ),
        "world_source_differs_only_pole": (
            world_normalized_revise == world_normalized_retain
        ),
        "prior_byte_identical": (
            (REVISE_DIR / "ladder/rung_7_prior.py").read_bytes()
            == (RETAIN_DIR / "ladder/rung_7_prior.py").read_bytes()
        ),
        "null_byte_identical": (
            (REVISE_DIR / "ladder/rung_8_null.py").read_bytes()
            == (RETAIN_DIR / "ladder/rung_8_null.py").read_bytes()
        ),
        "episode_robots_byte_identical": (
            (REVISE_DIR / "robots.py").read_bytes()
            == (RETAIN_DIR / "robots.py").read_bytes()
        ),
        "source_is_south_only": (
            source_spec.context == {"site": "south"}
            and set(meta_revise.episode.observe_sources)
            == {"south_production_history"}
        ),
        "no_served_events": (
            not meta_revise.episode.events and not meta_retain.episode.events
        ),
        "context_contract_has_both_sites": (
            meta_revise.episode.control_surface.get("context", {})
            .get("site", {})
            .get("values")
            == ["south", "north"]
        ),
        "only_deliverable_columns_visible": all(visible_schema),
        "south_all_actions_exact_twins": all(south_all_actions_exact),
        "north_natural_humidity_exact_twins": all(
            north_natural_humidity_exact
        ),
        "north_feedstock_rng_common_all_regimes": all(north_feedstock_exact),
        "north_off_manifold_delta_mechanical": (
            max(north_off_manifold_errors) < 1e-12
        ),
        "world_replay_exact": all(replay_exact),
        "source_history_exact_twins": source_revise.equals(source_retain),
        "south_history_correlation_seductive": 0.65 <= south_corr <= 0.90,
        "exogenous_draws_exact_twins": exogenous_identical,
        "worldserver_south_history_exact": replay_ledger["south_history_equal"],
        "worldserver_south_intervention_exact": replay_ledger["south_joint_equal"],
        "worldserver_north_humidity_exact": replay_ledger["north_humidity_equal"],
        "worldserver_north_common_feedstock": replay_ledger[
            "north_joint_feedstock_equal"
        ],
        "worldserver_north_expected_delta": (
            abs(replay_ledger["north_joint_mean_delta"] - 4.0) < 1e-12
        ),
        "worldserver_budget_exact": replay_ledger["budget_equal"],
        "truth_fixtures_smoke_valid": all(
            value is None for value in smoke_errors.values()
        ),
        "robot_models_smoke_valid": all(
            value is None for value in robot_smoke_errors.values()
        ),
        "battery_weights_sum_one": (
            abs(sum(item.weight for item in battery.items) - 1.0) < 1e-12
        ),
        "battery_south_verification_weight": abs(south_weight - 0.20) < 1e-12,
        "battery_north_primary_weight": abs(north_weight - 0.80) < 1e-12,
        "battery_north_diagnostic_weight": (
            abs(north_diagnostic_weight - 0.68) < 1e-12
        ),
        "truth_fixtures_reach_ceiling": (
            score_revise["truth"]["R"] >= 0.99
            and score_retain["truth"]["R"] >= 0.99
        ),
        "truth_fixtures_zero_errors": (
            score_revise["truth"]["errors"] == 0
            and score_retain["truth"]["errors"] == 0
        ),
        "never_update_loses_revise": score_revise["retain"]["R"] <= 0.30,
        "never_update_wins_retain": score_retain["retain"]["R"] >= 0.90,
        "change_wins_revise": score_revise["revise"]["R"] >= 0.90,
        "change_loses_retain": score_retain["revise"]["R"] <= 0.30,
        "prior_is_common_zero": (
            abs(score_revise["prior"]["R_unclipped"]) < 1e-12
            and abs(score_retain["prior"]["R_unclipped"]) < 1e-12
        ),
        "reward_denominator_resolved": (
            score_revise["denom_raw"] > 0.05
            and score_retain["denom_raw"] > 0.05
        ),
        "north_campaign_identifies_both": min(campaign["accuracy"].values())
        >= 0.90,
        "north_campaign_expected_llr_large": campaign["expected_llr"] >= 20.0,
    }
    report = {
        "cases": [meta_revise.case_id, meta_retain.case_id],
        "south_historical_correlation": south_corr,
        "max_north_off_manifold_delta_error": max(north_off_manifold_errors),
        "battery_weights": {
            "south": south_weight,
            "north": north_weight,
            "north_diagnostic": north_diagnostic_weight,
        },
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
