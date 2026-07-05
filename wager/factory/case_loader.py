"""Loads the on-disk anatomy of a case (ARCHITECTURE 1) into runtime objects.

The reward path never reads the filesystem itself: tests and runners load
artifacts here and hand plain objects (callables, strings, contracts) to
wager.reward. Visibility rule: everything loaded here is factory/server side;
the agent only ever sees brief.md and the env handle.
"""

import importlib.util
import sys
from pathlib import Path
from typing import Callable

from wager.contracts import Battery, CaseMeta

LADDER_DIRNAME = "ladder"


def load_world_source(case_dir: str | Path) -> str:
    return (Path(case_dir) / "world.py").read_text(encoding="utf-8")


def load_world_module(case_dir: str | Path):
    """Import world.py in-process (server side: the truth is ours) and return the
    module -- exposes sample, and (structured worlds) mechanism + PARAMS for the
    factory to perturb/ablate when deriving twins/ladder."""
    case_dir = Path(case_dir)
    module_name = f"wager_world_{case_dir.name}"
    spec = importlib.util.spec_from_file_location(module_name, case_dir / "world.py")
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


def load_world_sample(case_dir: str | Path) -> Callable:
    """The world's sample(regime, n, seed) callable."""
    return load_world_module(case_dir).sample


def load_battery(case_dir: str | Path) -> Battery:
    return Battery.from_json_file(Path(case_dir) / "battery.json")


def load_meta(case_dir: str | Path) -> CaseMeta:
    return CaseMeta.from_json_file(Path(case_dir) / "meta.json")


def load_ladder(case_dir: str | Path) -> list[tuple[str, str]]:
    """Committed ladder fixtures (rungs 2..N), sorted by filename.

    Rung 1 is never a fixture: it is world.py itself (Decision Log v0.11) --
    except in window worlds, where world.py is the ILLEGAL player and the
    legal R=1 anchor is the separate truth_code.py fixture (v0.63).
    """
    ladder_dir = Path(case_dir) / LADDER_DIRNAME
    return [
        (path.stem, path.read_text(encoding="utf-8"))
        for path in sorted(ladder_dir.glob("rung_*.py"))
    ]


def load_truth_code(case_dir: str | Path) -> str | None:
    """Window worlds (meta.window_protocol set): the LEGAL R=1 ceiling as a
    committed fixture -- world.py reads the lot's hidden state and is the
    ILLEGAL player (Decision Log v0.63), so the episode's S_truth anchor is
    this code, never world_source. None when the fixture is absent."""
    path = Path(case_dir) / "truth_code.py"
    return path.read_text(encoding="utf-8") if path.exists() else None


def make_window_enrich(case_dir: str | Path, meta: CaseMeta) -> Callable | None:
    """The ONE choke point for window worlds (v0.63-4): (ns, seed_world) -> ns
    with runtime-only context[context_key] = world.make_window(seed_world,
    n_cal), n_cal read LOUDLY from the persisted context scalar. None (inert)
    for every non-window world."""
    if meta.window_protocol is None:
        return None
    protocol = meta.window_protocol
    context_key = protocol["context_key"]
    n_cal_key = protocol.get("n_cal_key", "n_cal")
    module = load_world_module(case_dir)

    def enrich(ns, seed_world: int):
        ns.context = dict(ns.context)
        ns.context[context_key] = module.make_window(seed_world, int(ns.context[n_cal_key]))
        return ns

    return enrich


def make_sample_transform(meta: CaseMeta) -> Callable | None:
    """Trajectory worlds (v0.68-R1): the long->wide pivot applied to EVERY
    sample crossing the scorer (truth, null, rivals, submissions), on the
    item's DECLARED grid (context[grid_key]). None (inert) for static worlds."""
    if meta.trajectory_protocol is None:
        return None
    from wager.reward.trajectory import pivot_trajectories

    grid_key = meta.trajectory_protocol.get("grid_key", "t_grid")

    def transform(ns, df):
        return pivot_trajectories(df, ns.context[grid_key])

    return transform
