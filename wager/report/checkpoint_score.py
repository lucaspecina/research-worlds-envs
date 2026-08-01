"""Efficient zero-LLM analysis of several belief checkpoints in one world.

The world side and anchors are materialized once. Each agent artifact is then
scored once and decomposed from the per-item proper-score distances into full,
initial/diagnostic regions, lines, and line x region groups. Local summaries
exclude MDL: program length is a global delivery property, not a belief about
one slice of the world.
"""

from __future__ import annotations

import hashlib
from pathlib import Path

import numpy as np

from wager.harness.case_episode import build_world_server
from wager.reward.scorer import WorldSide, sandboxed_null_sample, score_submission
from wager.reward.sandbox import SandboxError


def _artifact_hash(code: str | None) -> str | None:
    return hashlib.sha256(code.encode("utf-8")).hexdigest()[:12] if code else None


def normalized_group_score(
    submission_distances,
    truth_distances,
    naive_distances,
    weights,
    *,
    epsilon: float = 1e-12,
):
    """Return a fidelity-only R for an arbitrary battery subset."""
    w = np.asarray(weights, dtype=float)
    if w.size == 0 or float(w.sum()) <= 0.0:
        return {"resolved": False, "R": None, "R_unclipped": None, "resolution": 0.0}
    w = w / w.sum()
    sub = -float(np.dot(w, np.asarray(submission_distances, dtype=float)))
    truth = -float(np.dot(w, np.asarray(truth_distances, dtype=float)))
    naive = -float(np.dot(w, np.asarray(naive_distances, dtype=float)))
    resolution = truth - naive
    if abs(resolution) <= epsilon:
        return {
            "resolved": False,
            "R": None,
            "R_unclipped": None,
            "resolution": resolution,
            "fidelity": sub,
        }
    value = (sub - naive) / resolution
    return {
        "resolved": True,
        "R": float(np.clip(value, 0.0, 1.0)),
        "R_unclipped": float(value),
        "resolution": float(resolution),
        "fidelity": sub,
    }


class CheckpointScorer:
    """Score many executable checkpoints against one cached world side."""

    def __init__(self, case_dir: str | Path, *, line_key="line", driver_key="driver",
                 split_driver=4.0):
        self.case_dir = Path(case_dir)
        self.line_key = line_key
        self.driver_key = driver_key
        self.split_driver = float(split_driver)
        server = build_world_server(self.case_dir)
        self.battery = server.scoring.battery
        self.params = server.scoring.params
        with sandboxed_null_sample(
            server.scoring.null_code,
            server.columns,
            self.params.model_call_timeout_s,
        ) as null_sample:
            self.world_side = WorldSide(
                server.world_sample,
                self.battery,
                server.columns,
                self.params.n_samples,
                null_sample=null_sample,
                functionals=server.scoring.functionals,
                c_f=self.params.c_f,
                enrich_regime=server.scoring.enrich_regime,
                sample_transform=server.scoring.sample_transform,
            )
        truth_code = server.scoring.truth_code or server.scoring.world_source
        self.anchor_reports = {
            "truth": score_submission(truth_code, self.world_side, self.params),
            "naive": score_submission(server.scoring.naive_code, self.world_side, self.params),
            "null": score_submission(server.scoring.null_code, self.world_side, self.params),
        }
        self._cache = {}
        self.groups = self._groups()

    def _groups(self):
        groups = {"full": [], "initial": [], "diagnostic": []}
        lines = sorted({int(item.regime.config[self.line_key]) for item in self.battery.items})
        for line in lines:
            groups[f"line_{line}"] = []
            groups[f"line_{line}_initial"] = []
            groups[f"line_{line}_diagnostic"] = []
        for idx, item in enumerate(self.battery.items):
            line = int(item.regime.config[self.line_key])
            driver = float(item.regime.config[self.driver_key])
            region = "initial" if driver <= self.split_driver else "diagnostic"
            groups["full"].append(idx)
            groups[region].append(idx)
            groups[f"line_{line}"].append(idx)
            groups[f"line_{line}_{region}"].append(idx)
        return groups

    @staticmethod
    def _distances(report, indices):
        return [report.items[i].mean_distance for i in indices]

    def _group_result(self, report, indices):
        weights = [self.battery.items[i].weight for i in indices]
        return normalized_group_score(
            self._distances(report, indices),
            self._distances(self.anchor_reports["truth"], indices),
            self._distances(self.anchor_reports["naive"], indices),
            weights,
        )

    def score(self, code: str | None):
        key = _artifact_hash(code)
        if key is None:
            return {"hash": None, "scoreable": False, "error": "missing artifact", "groups": {}}
        if key in self._cache:
            return self._cache[key]
        try:
            report = score_submission(code, self.world_side, self.params)
        except (SandboxError, ValueError) as exc:
            result = {"hash": key, "scoreable": False, "error": str(exc), "groups": {}}
            self._cache[key] = result
            return result
        truth = self.anchor_reports["truth"].raw_score
        naive = self.anchor_reports["naive"].raw_score
        denom = truth - naive
        global_unclipped = None if abs(denom) <= 1e-12 else (report.raw_score - naive) / denom
        result = {
            "hash": key,
            "scoreable": True,
            "error": None,
            "global_R": None if global_unclipped is None else float(np.clip(global_unclipped, 0.0, 1.0)),
            "global_R_unclipped": None if global_unclipped is None else float(global_unclipped),
            "mdl_bytes": report.mdl_bytes,
            "groups": {
                name: self._group_result(report, indices)
                for name, indices in self.groups.items()
            },
        }
        self._cache[key] = result
        return result

    def score_many(self, artifacts: dict[str, str | None]):
        return {name: self.score(code) for name, code in artifacts.items()}
