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


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("results", nargs="+", type=Path)
    args = parser.parse_args()
    for path in args.results:
        payload = json.loads(path.read_text(encoding="utf-8"))
        result = score_code(payload["episode"]["submission_code"])
        print(json.dumps({"path": str(path), **result}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
