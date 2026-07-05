"""Score one episode submission against the battery, normalized to R.

Reward side (ZERO-LLM). Builds the world side once with the null model as the
D_MAX reference (Decision Log v0.12), scores world.py / naive / null as the
anchors and the submission, returns R = clip((S - S_naive)/(S_truth - S_naive)).
Used by the harness on submit; the agent never sees R (the battery is secret).
"""

from typing import Callable

from wager.contracts import Battery, ScoringParams
from wager.reward.scorer import WorldSide, make_anchors, sandboxed_null_sample, score_submission


def score_episode_submission(
    code: str,
    world_sample: Callable,
    world_source: str,
    naive_code: str,
    null_code: str,
    battery: Battery,
    columns: list[str],
    params: ScoringParams,
    functionals=None,
    truth_code: str | None = None,
    enrich_regime: Callable | None = None,
) -> dict:
    # combined score (ARCHITECTURE 9.3): the declared functionals + the frozen
    # c_f from ScoringParams. Empty functionals -> identity with the energy
    # score (the dummy is byte-identical). v0.60 wiring: the episode path had
    # been scoring energy-only -- registered != implemented, third+1 instance.
    #
    # Window worlds (Decision Log v0.63): S_truth is TRUTH-AS-SCOREABLE -- the
    # LEGAL bayes-ceiling fixture (`truth_code`), never world_source: world.py
    # reads the lot's hidden state and is the ILLEGAL player there. None keeps
    # the historical semantics (S_truth = world.py) for every non-window world.
    # `enrich_regime` is the ONE choke point materializing runtime-only context
    # (cal_window) per item; every anchor and the submission consume the same
    # enriched regimes (CRN intact).
    with sandboxed_null_sample(null_code, columns, params.model_call_timeout_s) as null_sample:
        ws = WorldSide(world_sample, battery, columns, params.n_samples, null_sample=null_sample,
                       functionals=functionals or [], c_f=params.c_f,
                       enrich_regime=enrich_regime)
        s_truth = score_submission(truth_code or world_source, ws, params).raw_score
        s_naive = score_submission(naive_code, ws, params).raw_score
        s_null = score_submission(null_code, ws, params).raw_score
        sub = score_submission(code, ws, params)
    anchors = make_anchors(s_truth, s_naive, s_null)
    r, r_unclipped = anchors.r_of(sub.raw_score)
    return {
        "R": r,
        "R_unclipped": r_unclipped,
        "raw_score": sub.raw_score,
        "s_truth": s_truth,
        "s_naive": s_naive,
        "s_null": s_null,
        "mdl_bytes": sub.mdl_bytes,
    }
