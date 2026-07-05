"""Build a WorldServer for a case (shared by C2 scripted solvers and C3 LLM).

Loads the server-side artifacts (world, battery, ladder anchors used for scoring,
episode config) and assembles the authority. The agent only ever sees brief +
verbs; everything loaded here is server side.
"""

from pathlib import Path

from wager.factory.case_loader import (
    load_battery,
    load_ladder,
    load_meta,
    load_truth_code,
    load_world_sample,
    load_world_source,
    make_sample_transform,
    make_window_enrich,
)
from wager.harness.world_server import ScoringArtifacts, WorldServer


def build_world_server(case_dir: str | Path, seed_offset: int = 0) -> WorldServer:
    case_dir = Path(case_dir)
    meta = load_meta(case_dir)
    if meta.episode is None:
        raise ValueError(f"{meta.case_id} has no episode config (meta.episode)")
    ladder = load_ladder(case_dir)
    brief = (case_dir / "brief.md").read_text(encoding="utf-8")
    # window worlds (v0.63): S_truth = the LEGAL bayes-ceiling fixture; scoring
    # world.py there would anchor R=1 to the ILLEGAL player (it reads the lot's
    # hidden state) and no legal submission could ever reach it.
    truth_code = load_truth_code(case_dir)
    if meta.window_protocol is not None and truth_code is None:
        raise ValueError(
            f"{meta.case_id} declares window_protocol but has no truth_code.py: "
            "commit the legal ceiling fixture (anchors.write_fixtures)"
        )
    # anchors by the run_ladder CONVENTION (second-to-last = naive, last = null;
    # v0.59: dummy-ism-family fix -- the dummy's rung NAMES were hardcoded here,
    # which would have KeyError'd on any case with a different ladder length)
    scoring = ScoringArtifacts(
        world_source=load_world_source(case_dir),
        naive_code=ladder[-2][1],  # the S_naive anchor (rival a)
        null_code=ladder[-1][1],  # the S_null / D_MAX reference
        battery=load_battery(case_dir),
        params=meta.scoring,
        functionals=list(meta.stakes.functionals),
        truth_code=truth_code,
        enrich_regime=make_window_enrich(case_dir, meta),
        sample_transform=make_sample_transform(meta),
    )
    return WorldServer(
        world_sample=load_world_sample(case_dir),
        columns=meta.column_names,
        brief=brief,
        config=meta.episode,
        scoring=scoring,
        control_surface=meta.episode.control_surface,
        case_id=meta.case_id,
        seed_offset=seed_offset,
    )
