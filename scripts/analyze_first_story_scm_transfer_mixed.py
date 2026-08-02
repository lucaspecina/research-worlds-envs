"""Analyze mean revision and distribution shape in South-to-North SCM forks.

The analyzer is deliberately separate from the exploratory runner.  It can
read historical two-pole raws as well as future three-pole raws, and it never
changes or replays an agent trajectory.

For the intended MIXED pole (75% REVISE + 25% RETAIN), the North outcome at
H=5 has these two diagnostic distributions::

    G=3: .75 N(30, 4) + .25 N(26, 4)
    G=7: .75 N(30, 4) + .25 N(34, 4)

They have the same first two moments as N(29, 7) and N(31, 7), respectively.
The oriented skew signature A3=(skew_G7-skew_G3)/2 distinguishes them:
A3=6/7**1.5 ~= .324 for the mixture and A3=0 for the matched Normals.
"""

from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path
from statistics import NormalDist
from typing import Any

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from wager.contracts import Regime  # noqa: E402
from wager.harness.case_episode import build_world_server  # noqa: E402
from wager.reward.sandbox import SandboxedSubmission, SandboxError  # noqa: E402


REVISE_CASE = ROOT / "cases" / "first_story_scm_transfer_revise_v0"
RETAIN_CASE = ROOT / "cases" / "first_story_scm_transfer_retain_v0"
DEFAULT_N = 4000
EXPECTED_MIXED_A3 = 6.0 / (7.0**1.5)
CHECKPOINTS = ("M_pre", "M_first", "M_last")
GLOBAL_SCORE_FIELDS = (
    "scoreable",
    "raw_score",
    "R",
    "R_unclipped",
    "s_truth",
    "s_naive",
    "s_null",
    "mdl_bytes",
    "error",
)


def _regime(site: str, grade: float) -> Regime:
    return Regime(
        config={"humidity": 5.0, "feedstock_grade": grade},
        context={"site": site},
        horizon=None,
    )


def _summary(values: np.ndarray) -> dict[str, float | None]:
    values = np.asarray(values, dtype=float)
    mean = float(np.mean(values))
    variance = float(np.var(values))
    sd = math.sqrt(max(variance, 0.0))
    skew = None
    if sd > 1e-12:
        skew = float(np.mean(np.power((values - mean) / sd, 3)))
    return {
        "mean": mean,
        "variance": variance,
        "sd": sd,
        "skew": skew,
    }


def _normal_shape_gap(values: np.ndarray) -> float | None:
    """Wasserstein-1 gap to a moment-matched Normal, in SD units."""
    values = np.asarray(values, dtype=float)
    sd = float(np.std(values))
    if sd <= 1e-12:
        return None
    standardized = np.sort((values - float(np.mean(values))) / sd)
    n = len(standardized)
    probabilities = (np.arange(n, dtype=float) + 0.5) / n
    normal = NormalDist()
    target = np.fromiter(
        (normal.inv_cdf(float(p)) for p in probabilities),
        dtype=float,
        count=n,
    )
    return float(np.mean(np.abs(standardized - target)))


def _site_metrics(draws: dict[str, np.ndarray]) -> dict[str, Any]:
    low = _summary(draws["G3"])
    high = _summary(draws["G7"])
    skew_low = low["skew"]
    skew_high = high["skew"]
    oriented_skew = None
    if skew_low is not None and skew_high is not None:
        oriented_skew = float((skew_high - skew_low) / 2.0)
    normal_gaps = [
        gap
        for gap in (
            _normal_shape_gap(draws["G3"]),
            _normal_shape_gap(draws["G7"]),
        )
        if gap is not None
    ]
    return {
        "regimes": {"G3": low, "G7": high},
        "delta_mean_G7_minus_G3": float(high["mean"] - low["mean"]),
        "oriented_skew_A3": oriented_skew,
        "normal_shape_gap": (
            float(np.mean(normal_gaps)) if normal_gaps else None
        ),
    }


def _model_draws(
    code: str,
    columns: list[str],
    *,
    n_samples: int,
    seed: int,
) -> dict[str, dict[str, np.ndarray]]:
    result: dict[str, dict[str, np.ndarray]] = {}
    with SandboxedSubmission(code, columns, timeout_s=15.0) as submission:
        for site_index, site in enumerate(("south", "north")):
            result[site] = {}
            for label, grade in (("G3", 3.0), ("G7", 7.0)):
                # Common random numbers make the causal mean contrast much
                # less noisy and match the existing transfer signature.
                run_seed = seed + 100 * site_index
                frame = submission.run(
                    _regime(site, grade), n_samples, run_seed
                )
                result[site][label] = frame["outcome"].to_numpy(dtype=float)
    return result


def _truth_draws(
    case_dir: Path,
    *,
    n_samples: int,
    seed: int,
) -> tuple[dict[str, dict[str, np.ndarray]], list[str]]:
    server = build_world_server(case_dir)
    result: dict[str, dict[str, np.ndarray]] = {}
    for site_index, site in enumerate(("south", "north")):
        result[site] = {}
        for label, grade in (("G3", 3.0), ("G7", 7.0)):
            run_seed = seed + 100 * site_index
            frame = server.world_sample(
                _regime(site, grade), n_samples, run_seed
            )
            result[site][label] = frame["outcome"].to_numpy(dtype=float)
    return result, list(server.columns)


def _wasserstein_equal_n(left: np.ndarray, right: np.ndarray) -> float:
    if len(left) != len(right):
        raise ValueError("Wasserstein inputs must have equal length")
    return float(np.mean(np.abs(np.sort(left) - np.sort(right))))


def _south_error(
    model: dict[str, np.ndarray],
    truth: dict[str, np.ndarray],
) -> float:
    terms = []
    for label in ("G3", "G7"):
        scale = float(np.std(truth[label]))
        if scale <= 1e-12:
            raise ValueError("South truth has zero outcome variance")
        terms.append(_wasserstein_equal_n(model[label], truth[label]) / scale)
    return float(np.mean(terms))


def _checkpoint_codes(payload: dict[str, Any], branch: dict[str, Any]) -> dict:
    selection = payload.get("prefix", {}).get("selection") or {}
    return {
        "M_pre": selection.get("M_pre"),
        # Historical runners call this the first *changed* model.  A missing
        # value therefore means "not observed", not an invalid artifact and
        # not permission to silently substitute M_pre.
        "M_first": branch.get("first_changed_model"),
        "M_last": (
            branch.get("last_scoreable_model")
            or branch.get("last_working_model_code")
            or branch.get("last_working_model")
            or branch.get("submission_code")
        ),
    }


def _global_scores(branch: dict[str, Any], checkpoint: str) -> dict[str, Any]:
    score = (branch.get("scores", {}).get(checkpoint) or {})
    return {key: score.get(key) for key in GLOBAL_SCORE_FIELDS if key in score}


def _case_dir(branch_name: str, branch: dict[str, Any]) -> Path:
    case_id = branch.get("case_id")
    if not case_id:
        raise ValueError(f"branch {branch_name!r} has no case_id")
    path = ROOT / "cases" / str(case_id)
    if not path.is_dir():
        raise FileNotFoundError(
            f"case directory for branch {branch_name!r} does not exist: {path}"
        )
    return path


def _endpoint_deltas(*, n_samples: int, seed: int) -> dict[str, float]:
    result = {}
    for name, path in (("revise", REVISE_CASE), ("retain", RETAIN_CASE)):
        draws, _ = _truth_draws(path, n_samples=n_samples, seed=seed)
        result[name] = _site_metrics(draws["north"])[
            "delta_mean_G7_minus_G3"
        ]
    return result


def analyze_payload(
    payload: dict[str, Any],
    *,
    source: Path,
    n_samples: int,
    seed: int,
) -> dict[str, Any]:
    branches = payload.get("branches")
    if not isinstance(branches, dict) or not branches:
        raise ValueError(f"{source}: raw has no non-empty 'branches' mapping")

    endpoints = _endpoint_deltas(n_samples=n_samples, seed=seed + 50_000)
    denominator = endpoints["retain"] - endpoints["revise"]
    if abs(denominator) <= 1e-12:
        raise ValueError("RETAIN and REVISE mean-effect endpoints coincide")

    analyzed_branches: dict[str, Any] = {}
    for branch_index, (branch_name, branch) in enumerate(branches.items()):
        case_dir = _case_dir(branch_name, branch)
        branch_seed = seed + 10_000 * branch_index
        truth_draws, columns = _truth_draws(
            case_dir, n_samples=n_samples, seed=branch_seed
        )
        truth_metrics = {
            site: _site_metrics(site_draws)
            for site, site_draws in truth_draws.items()
        }
        truth_delta = truth_metrics["north"]["delta_mean_G7_minus_G3"]
        truth_u = (endpoints["retain"] - truth_delta) / denominator

        checkpoints: dict[str, Any] = {}
        model_draws_by_checkpoint: dict[
            str, dict[str, dict[str, np.ndarray]]
        ] = {}
        for checkpoint, code in _checkpoint_codes(payload, branch).items():
            if not code:
                checkpoints[checkpoint] = {
                    "scoreable": False,
                    "error": "artifact not present in raw",
                    "global_score": _global_scores(branch, checkpoint),
                }
                continue
            try:
                draws = _model_draws(
                    code,
                    columns,
                    n_samples=n_samples,
                    seed=branch_seed,
                )
                model_draws_by_checkpoint[checkpoint] = draws
                metrics = {
                    site: _site_metrics(site_draws)
                    for site, site_draws in draws.items()
                }
                delta = metrics["north"]["delta_mean_G7_minus_G3"]
                u_mean = (endpoints["retain"] - delta) / denominator
                a3 = metrics["north"]["oriented_skew_A3"]
                row = {
                    "scoreable": True,
                    "north": metrics["north"],
                    "south": metrics["south"],
                    "U_mean_revision": float(u_mean),
                    "delta_error_signed": float(delta - truth_delta),
                    "delta_error_abs_normalized": float(
                        abs(delta - truth_delta) / abs(denominator)
                    ),
                    "south_truth_error_W1_sd": _south_error(
                        draws["south"], truth_draws["south"]
                    ),
                    "global_score": _global_scores(branch, checkpoint),
                }
                if branch_name.lower() == "mixed" and a3 is not None:
                    row["mixed_shape"] = {
                        "expected_oriented_skew_A3": EXPECTED_MIXED_A3,
                        "capture_fraction_unclipped": float(
                            a3 / EXPECTED_MIXED_A3
                        ),
                        "absolute_error": float(abs(a3 - EXPECTED_MIXED_A3)),
                    }
                checkpoints[checkpoint] = row
            except (SandboxError, TypeError, ValueError, KeyError) as exc:
                checkpoints[checkpoint] = {
                    "scoreable": False,
                    "error": repr(exc),
                    "global_score": _global_scores(branch, checkpoint),
                }

        preservation: dict[str, Any] = {"available": False}
        pre = checkpoints.get("M_pre", {})
        last = checkpoints.get("M_last", {})
        if pre.get("scoreable") and last.get("scoreable"):
            south_delta_pre = pre["south"]["delta_mean_G7_minus_G3"]
            south_delta_last = last["south"]["delta_mean_G7_minus_G3"]
            preservation = {
                "available": True,
                "delta_drift_last_minus_pre": float(
                    south_delta_last - south_delta_pre
                ),
                "truth_error_change_last_minus_pre": float(
                    last["south_truth_error_W1_sd"]
                    - pre["south_truth_error_W1_sd"]
                ),
                "interpretation": (
                    "nonpositive means preserved or improved; positive means damaged"
                ),
            }

        global_change = None
        if pre.get("scoreable") and last.get("scoreable"):
            pre_r = pre["global_score"].get("R_unclipped")
            last_r = last["global_score"].get("R_unclipped")
            if pre_r is not None and last_r is not None:
                global_change = float(last_r - pre_r)

        analyzed_branches[branch_name] = {
            "case_id": branch.get("case_id"),
            "truth": {
                "north": truth_metrics["north"],
                "south": truth_metrics["south"],
                "U_mean_revision_target": float(truth_u),
            },
            "checkpoints": checkpoints,
            "south_preservation": preservation,
            "global_R_unclipped_change_last_minus_pre": global_change,
        }

    warnings = []
    if "mixed" not in {name.lower() for name in branches}:
        warnings.append(
            "raw has no MIXED branch; endpoint and historical-pole metrics were "
            "computed, but mixture-specific shape capture is unavailable"
        )
    return {
        "source": str(source),
        "model": payload.get("model"),
        "seed_offset": payload.get("seed_offset"),
        "available_poles": list(branches),
        "analysis": {
            "n_samples_per_regime": n_samples,
            "seed": seed,
            "mean_revision_endpoints": endpoints,
            "U_definition": "(delta_retain - delta_model) / (delta_retain - delta_revise)",
            "expected_targets_if_mixed_is_75pct_revise": {
                "retain": 0.0,
                "mixed": 0.75,
                "revise": 1.0,
            },
            "expected_mixed_oriented_skew_A3": EXPECTED_MIXED_A3,
        },
        "branches": analyzed_branches,
        "warnings": warnings,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("raw", nargs="+", type=Path)
    parser.add_argument("--n-samples", type=int, default=DEFAULT_N)
    parser.add_argument("--seed", type=int, default=1_300_001)
    parser.add_argument("--out", type=Path, default=None)
    args = parser.parse_args()
    if args.n_samples < 100:
        parser.error("--n-samples must be at least 100")
    if args.out is not None and len(args.raw) != 1:
        parser.error("--out is only valid with one raw JSON")

    results = []
    for path in args.raw:
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
            results.append(analyze_payload(
                payload,
                source=path,
                n_samples=args.n_samples,
                seed=args.seed,
            ))
        except (OSError, json.JSONDecodeError, ValueError) as exc:
            parser.error(str(exc))

    output: Any = results[0] if len(results) == 1 else {"runs": results}
    rendered = json.dumps(output, indent=2, allow_nan=False) + "\n"
    if args.out is not None:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(rendered, encoding="utf-8")
        print(args.out)
    else:
        print(rendered, end="")


if __name__ == "__main__":
    main()
