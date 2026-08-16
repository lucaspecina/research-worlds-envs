"""Zero-LLM structural and evidence audit for hidden-probe agent episodes."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from cases.hidden_probe_types_v0 import build_and_certify as cert  # noqa: E402
from cases.hidden_probe_types_v0 import world  # noqa: E402
from wager.contracts import Regime  # noqa: E402
from wager.reward.sandbox import SandboxedSubmission  # noqa: E402
from wager.reward.trajectory import pivot_trajectories  # noqa: E402


N = 20_000
MODEL_SEED = 2026081690


def score_code(code: str) -> dict:
    x, truth_cdf = cert._projection_grid()
    gaussian = cert._best_gaussian(x, truth_cdf)
    regime = Regime(context={"t_grid": world.SCORE_GRID})
    with SandboxedSubmission(code, world.COLUMNS, timeout_s=30.0) as sandbox:
        pred = sandbox.run(regime, N, MODEL_SEED)
    wide = pivot_trajectories(pred, world.SCORE_GRID)
    projected = wide.to_numpy(float) @ cert._projection(world.SCORE_GRID)
    ordered = np.sort(projected)
    candidate_cdf = np.searchsorted(ordered, x, side="right") / len(ordered)
    regret = cert._cdf_regret(x, truth_cdf, candidate_cdf)
    s_unclipped = 1.0 - regret / gaussian["regret"]
    return {
        "n": N,
        "model_seed": MODEL_SEED,
        "projection_regret": regret,
        "gaussian_anchor_regret": gaussian["regret"],
        "S_probe_unclipped": s_unclipped,
        "S_probe": float(np.clip(s_unclipped, 0.0, 1.0)),
        "crosses_jump_frontier": bool(s_unclipped >= 0.5),
    }


def _ledger_frame(entry: dict) -> pd.DataFrame:
    data = entry["data"]
    return pd.DataFrame(data["data"], columns=data["columns"])


def audit_evidence(payload: dict) -> dict:
    experiments = [
        entry for entry in payload.get("evidence_ledger", [])
        if entry.get("kind") == "experiment"
    ]
    routine = [
        entry for entry in payload.get("evidence_ledger", [])
        if entry.get("kind") == "observe" and entry.get("source") == "routine_snapshots"
    ]
    out = {
        "routine_rows_bought": sum(len(_ledger_frame(row)) for row in routine),
        "experiment_calls": len(experiments),
        "orientations": [
            float(row["request"]["context"]["t_grid"][0]) for row in experiments
        ],
    }
    if not experiments:
        return out | {"persistent_ids_exact": False, "evidence_auditable": False}

    frames = [_ledger_frame(row) for row in experiments]
    id_sets = [tuple(frame.unit_id.tolist()) for frame in frames]
    persistent = all(ids == id_sets[0] for ids in id_sets[1:])
    out["persistent_ids_exact"] = persistent
    theta = np.asarray(out["orientations"], dtype=float)
    design = np.column_stack([np.ones(len(theta)), np.cos(theta), np.sin(theta)])
    if not persistent or len(np.unique(np.round(theta, 10))) < 3 or np.linalg.matrix_rank(design) < 3:
        return out | {"evidence_auditable": False}

    panel = np.column_stack([frame.sort_values("unit_id").y.to_numpy(float) for frame in frames])
    coefficients, _ = cert._harmonic_coefficients(panel, theta)
    responses = coefficients[:, 1:]
    one = cert._fit_gmm(responses, 1, "full")
    two = cert._fit_gmm(responses, 2, "tied")
    return out | {
        "evidence_auditable": True,
        "evidence_delta_BIC_two_tied_minus_one_full": float(
            one.bic(responses) - two.bic(responses)
        ),
        "evidence_two_type_weights": two.weights_.tolist(),
    }


def analyze_payload(payload: dict) -> dict:
    episode = payload["episode"]
    code = episode.get("submission_code")
    structural = score_code(code) if code else {
        "S_probe": None,
        "S_probe_unclipped": None,
        "crosses_jump_frontier": False,
    }
    r = episode.get("R")
    return {
        **structural,
        **audit_evidence(payload),
        "R": r,
        "R_unclipped": episode.get("R_unclipped"),
        "capacity_pass": bool(
            episode.get("accepted")
            and structural["crosses_jump_frontier"]
            and r is not None
            and r >= 0.5
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("results", nargs="+", type=Path)
    args = parser.parse_args()
    for path in args.results:
        payload = json.loads(path.read_text(encoding="utf-8"))
        print(json.dumps({"path": str(path), **analyze_payload(payload)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

