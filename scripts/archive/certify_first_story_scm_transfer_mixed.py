"""Zero-LLM certificate for the three-pole South-to-North SCM probe.

The script is read-only.  It verifies observational twins, the independent
75/25 selector, causal signatures, distributional resolution, and production
reward separation.  It exits non-zero if any gate fails.
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
    load_meta,
    load_world_module,
)
from wager.harness.case_episode import build_world_server  # noqa: E402
from wager.reward.distance import TruthSide  # noqa: E402
from wager.reward.scorer import (  # noqa: E402
    WorldSide,
    make_anchors,
    sandboxed_null_sample,
    score_submission,
)

REVISE = ROOT / "cases" / "first_story_scm_transfer_revise_v0"
MIXED = ROOT / "cases" / "first_story_scm_transfer_mixed_v0"
RETAIN = ROOT / "cases" / "first_story_scm_transfer_retain_v0"


def _ns(config: dict | None = None, *, site: str = "south") -> SimpleNamespace:
    return SimpleNamespace(
        config=dict(config or {}), context={"site": site}, horizon=None
    )


def _load_python(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _code(case_dir: Path, relative: str) -> str:
    return (case_dir / relative).read_text(encoding="utf-8")


def _callable_from_code(code: str):
    namespace: dict = {}
    exec(compile(code, "<certificate-model>", "exec"), namespace)  # noqa: S102
    return namespace["model"]


def _agent_facing_meta(case_dir: Path) -> dict:
    raw = json.loads((case_dir / "meta.json").read_text(encoding="utf-8"))
    raw.pop("case_id")
    raw.pop("operators")
    return raw


def _distribution_resolution(world, models: dict[str, object]) -> dict:
    configs = (
        {"humidity": 5.0, "feedstock_grade": 3.0},
        {"humidity": 5.0, "feedstock_grade": 7.0},
        {"humidity": 3.0, "feedstock_grade": 3.0},
        {"humidity": 7.0, "feedstock_grade": 7.0},
    )
    distances = {name: [] for name in models}
    for config_index, config in enumerate(configs):
        regime = _ns(config, site="north")
        for rep in range(6):
            truth = world.sample(regime, 600, 710_000 + 20 * config_index + rep)
            truth_side = TruthSide(truth, ["outcome"])
            for name, model in models.items():
                prediction = model(
                    regime, 600, 720_000 + 20 * config_index + rep
                )
                distances[name].append(truth_side.distance_to(prediction))
    mean = {name: float(np.mean(values)) for name, values in distances.items()}
    return {
        "mean_energy_distance_outcome": mean,
        "moment_to_truth_ratio": float(
            mean["moment_matched"] / max(mean["mixed"], 1e-12)
        ),
        "pure_retain_to_truth_ratio": float(
            mean["retain"] / max(mean["mixed"], 1e-12)
        ),
        "pure_revise_to_truth_ratio": float(
            mean["revise"] / max(mean["mixed"], 1e-12)
        ),
    }


def _production_scores(model_codes: dict[str, str]) -> dict:
    meta = load_meta(MIXED)
    world = load_world_module(MIXED)
    null = _code(MIXED, "ladder/rung_8_null.py")
    with sandboxed_null_sample(
        null, meta.column_names, meta.scoring.model_call_timeout_s
    ) as null_sample:
        world_side = WorldSide(
            world.sample,
            load_battery(MIXED),
            meta.column_names,
            meta.scoring.n_samples,
            null_sample=null_sample,
            functionals=list(meta.stakes.functionals),
            c_f=meta.scoring.c_f,
        )
        reports = {
            name: score_submission(code, world_side, meta.scoring)
            for name, code in model_codes.items()
        }
    anchors = make_anchors(
        reports["mixed"].raw_score,
        reports["prior"].raw_score,
        reports["null"].raw_score,
    )
    result = {}
    for name, report in reports.items():
        r_value, r_unclipped = anchors.r_of(report.raw_score)
        result[name] = {
            "fidelity": float(report.fidelity),
            "raw_score": float(report.raw_score),
            "R": float(r_value),
            "R_unclipped": float(r_unclipped),
            "errors": int(sum(item.sandbox_errors for item in report.items)),
        }
    result["truth_minus_prior_raw"] = float(
        reports["mixed"].raw_score - reports["prior"].raw_score
    )
    return result


def main() -> None:
    worlds = {
        "revise": load_world_module(REVISE),
        "mixed": load_world_module(MIXED),
        "retain": load_world_module(RETAIN),
    }
    robots = _load_python(MIXED / "robots.py", "mixed_robots")
    codes = {
        "mixed": _code(MIXED, "truth_code.py"),
        "retain": _code(RETAIN, "truth_code.py"),
        "revise": _code(REVISE, "truth_code.py"),
        "moment_matched": robots._model_code("moment_matched"),
        "prior": _code(MIXED, "ladder/rung_7_prior.py"),
        "null": _code(MIXED, "ladder/rung_8_null.py"),
    }
    models = {
        name: _callable_from_code(code)
        for name, code in codes.items()
        if name in {"mixed", "retain", "revise", "moment_matched"}
    }

    nondiagnostic = (
        ("south", {}),
        ("south", {"feedstock_grade": 3.0}),
        ("south", {"humidity": 5.0, "feedstock_grade": 7.0}),
        ("north", {}),
        ("north", {"humidity": 3.0}),
        ("north", {"humidity": 7.0}),
    )
    twin_rows = []
    for seed in (17, 91_001, 400_003):
        for site, config in nondiagnostic:
            frames = {
                name: world.sample(_ns(config, site=site), 250, seed)
                for name, world in worlds.items()
            }
            twin_rows.append(
                {
                    "site": site,
                    "config": config,
                    "seed": seed,
                    "exact": (
                        frames["revise"].equals(frames["mixed"])
                        and frames["mixed"].equals(frames["retain"])
                    ),
                }
            )

    truth_exact_rows = []
    for seed in (23, 91_007):
        for site, config in nondiagnostic + (
            ("north", {"humidity": 5.0, "feedstock_grade": 3.0}),
            ("north", {"humidity": 5.0, "feedstock_grade": 7.0}),
        ):
            regime = _ns(config, site=site)
            actual = worlds["mixed"].sample(regime, 300, seed)
            predicted = models["mixed"](regime, 300, seed)
            truth_exact_rows.append(actual.equals(predicted))

    signature = {}
    for name, world in worlds.items():
        low = world.sample(
            _ns(
                {"humidity": 5.0, "feedstock_grade": 3.0}, site="north"
            ),
            200_000,
            810_001,
        )
        high = world.sample(
            _ns(
                {"humidity": 5.0, "feedstock_grade": 7.0}, site="north"
            ),
            200_000,
            810_001,
        )
        signature[name] = float(
            high["outcome"].mean() - low["outcome"].mean()
        )

    selector_a = worlds["mixed"]._humidity_selector(200_000, 830_001)
    selector_b = worlds["mixed"]._humidity_selector(200_000, 830_001)
    selector_c = worlds["mixed"]._humidity_selector(200_000, 830_002)
    distribution = _distribution_resolution(worlds["mixed"], models)
    production = _production_scores(codes)

    descriptions = {
        name: build_world_server(case_dir).describe()
        for name, case_dir in (
            ("revise", REVISE),
            ("mixed", MIXED),
            ("retain", RETAIN),
        )
    }
    gates = {
        "brief_byte_identical": len(
            {
                (case_dir / "brief.md").read_bytes()
                for case_dir in (REVISE, MIXED, RETAIN)
            }
        ) == 1,
        "battery_byte_identical": len(
            {
                (case_dir / "battery.json").read_bytes()
                for case_dir in (REVISE, MIXED, RETAIN)
            }
        ) == 1,
        "agent_facing_meta_identical": len(
            {_json_key(_agent_facing_meta(d)) for d in (REVISE, MIXED, RETAIN)}
        ) == 1,
        "describe_identical": all(
            value == descriptions["revise"] for value in descriptions.values()
        ),
        "nondiagnostic_samples_byte_identical": all(
            row["exact"] for row in twin_rows
        ),
        "truth_code_matches_world_exactly": all(truth_exact_rows),
        "selector_reproducible": np.array_equal(selector_a, selector_b),
        "selector_independent_across_seeds": not np.array_equal(
            selector_a, selector_c
        ),
        "selector_probability_is_075": abs(float(selector_a.mean()) - 0.75)
        < 0.005,
        "causal_signatures_8_2_0": (
            abs(signature["retain"] - 8.0) < 0.05
            and abs(signature["mixed"] - 2.0) < 0.05
            and abs(signature["revise"]) < 0.05
        ),
        "energy_separates_moment_matched": (
            distribution["moment_to_truth_ratio"] > 2.0
        ),
        "energy_separates_pure_retain": (
            distribution["pure_retain_to_truth_ratio"] > 10.0
        ),
        "energy_separates_pure_revise": (
            distribution["pure_revise_to_truth_ratio"] > 5.0
        ),
        "production_truth_anchor_valid": production["truth_minus_prior_raw"]
        > 0.01,
        "production_truth_beats_moment_fidelity": (
            production["mixed"]["fidelity"]
            > production["moment_matched"]["fidelity"] + 0.002
        ),
        "production_truth_beats_pures": (
            production["mixed"]["fidelity"]
            > max(
                production["retain"]["fidelity"],
                production["revise"]["fidelity"],
            )
            + 0.01
        ),
        "production_models_no_errors": all(
            row["errors"] == 0
            for name, row in production.items()
            if isinstance(row, dict) and name != "truth_minus_prior_raw"
        ),
    }
    payload = {
        "kind": "first_story_scm_transfer_mixed_certificate",
        "signature_delta_G_at_H5": signature,
        "selector_humidity_fraction": float(selector_a.mean()),
        "distribution_resolution": distribution,
        "production_scores": production,
        "nondiagnostic_pairing": twin_rows,
        "gates": gates,
        "all": all(gates.values()),
    }
    print(json.dumps(payload, indent=2), flush=True)
    if not payload["all"]:
        raise SystemExit(1)


def _json_key(value: dict) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


if __name__ == "__main__":
    main()
