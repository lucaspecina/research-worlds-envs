"""Zero-LLM structural score for hidden-profiles discovery submissions."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from cases.hidden_profiles_v0 import build_and_certify as cert  # noqa: E402
from cases.hidden_profiles_v0 import world  # noqa: E402
from wager.contracts import Regime  # noqa: E402
from wager.reward.sandbox import SandboxedSubmission  # noqa: E402

N = 20_000
MODEL_SEED = 2026081390


def score_code(code: str) -> dict:
    x, truth_cdf = cert._projection_grid()
    gaussian = cert._best_gaussian(x, truth_cdf)
    with SandboxedSubmission(code, world.COLUMNS, timeout_s=30.0) as sandbox:
        pred = sandbox.run(Regime(), N, MODEL_SEED)
    direction = world.SIGNATURE / np.sqrt(world.K)
    projected = (pred[world.COLUMNS].to_numpy(float) @ direction) / world.RESIDUAL_SD
    ordered = np.sort(projected)
    candidate_cdf = np.searchsorted(ordered, x, side="right") / len(ordered)
    regret = cert._cdf_regret(x, truth_cdf, candidate_cdf)
    s_unclipped = 1.0 - regret / gaussian["regret"]
    return {
        "n": N,
        "model_seed": MODEL_SEED,
        "projection_regret": regret,
        "gaussian_anchor_regret": gaussian["regret"],
        "S_profile_unclipped": s_unclipped,
        "S_profile": float(np.clip(s_unclipped, 0.0, 1.0)),
        "crosses_jump_frontier": bool(s_unclipped >= 0.5),
    }


def audit_archive_evidence(payload: dict) -> dict:
    """Check whether the exact archive rows bought in an episode support the split."""
    blocks = []
    for entry in payload.get("evidence_ledger", []):
        if entry.get("kind") != "observe" or entry.get("source") != "profile_archive":
            continue
        data = entry.get("data") or {}
        if data.get("data"):
            blocks.extend(data["data"])
    if not blocks:
        return {"archive_n": 0, "archive_auditable": False}

    y = np.asarray(blocks, dtype=float)
    one = cert._fit_gmm(y, 1, "full")
    two = cert._fit_gmm(y, 2, "tied")
    delta_bic = float(one.bic(y) - two.bic(y))

    x, truth_cdf = cert._projection_grid()
    gaussian = cert._best_gaussian(x, truth_cdf)
    fitted_regret = cert._cdf_regret(
        x, truth_cdf, cert._fitted_projection_cdf(two, x)
    )
    fitted_s = float(np.clip(1.0 - fitted_regret / gaussian["regret"], 0.0, 1.0))
    posterior = two.predict_proba(y).max(axis=1)
    return {
        "archive_n": int(len(y)),
        "archive_auditable": True,
        "archive_delta_BIC_two_tied_minus_one_full": delta_bic,
        "archive_two_profile_S": fitted_s,
        "archive_two_profile_weights": two.weights_.tolist(),
        "archive_mean_assignment_confidence": float(posterior.mean()),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("results", nargs="+", type=Path)
    args = parser.parse_args()
    for path in args.results:
        payload = json.loads(path.read_text(encoding="utf-8"))
        result = score_code(payload["episode"]["submission_code"])
        evidence = audit_archive_evidence(payload)
        print(json.dumps({"path": str(path), **result, **evidence}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
