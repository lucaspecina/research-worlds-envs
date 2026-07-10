"""ADR 0118 runner -- corrected & minimal HINT experiment (DeepSeek-V3.2 only).

Implements the pre-registration in
`docs/adr/0118-v1.18-preregistro-experimento-pista-corregido-minimo.md`:

  6 cells = {first_story_scarce_v0, first_story_v0} x {libre, hint_T, placebo},
  8 seeds each (55..62) = 48 episodes, model DeepSeek-V3.2.

WIRING is copied from the existing episode pattern
(`cases/dummy_dose_v0/e05_episodes.py`, `cases/selection_bias_scarce_v0/e05_consolidation.py`):
build the opaque WorldServer with `build_world_server(case_dir, seed_offset=seed)`
and drive it with `run_episode(server, model=...)`. Credentials come from the env
via FoundryChat's `load_dotenv()` -- the SAME path e05 uses (AZURE_FOUNDRY_BASE_URL /
AZURE_INFERENCE_CREDENTIAL).

HINT INJECTION -- the exact mechanism of the prior experiment (ADRs 0095/0097/0098/0110):
the hint is passed as `run_episode(..., system_suffix=<text>)`. `system_suffix` is the
ONLY harness parameter for appending text to the episode prompt, and it was added in
ADR 0095 precisely for this construct-validity / hint manipulation (it appends to the
base SYSTEM, reward path untouched). The hint text NEVER names any world mechanism --
only the frozen strings copied verbatim from ADR 0118 are ever injected.

ZERO CLASSIFIER (`klass`) -- reimplemented faithfully to ADR 0110: `exec` = the episode
did NOT deliver a valid (accepted) model -> EXCLUDED from the per-cell median; `judge` =
a model was delivered, so its R (even R=0) is a judgment signal. Pure code, NO LLM
(reward-path rule: never an LLM in scoring/classification).

This runner ONLY orchestrates episodes. It never touches wager/reward/**, never edits
cases/** (read-only), and writes only under scripts/out/.

Run:
  .venv/Scripts/python scripts/exp_hint_0118.py --dry-run   # wiring check, NO API
  .venv/Scripts/python scripts/exp_hint_0118.py --smoke     # 2 real episodes
  .venv/Scripts/python scripts/exp_hint_0118.py --full      # 48 episodes, resumable
"""

import json
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from wager.harness.case_episode import build_world_server  # noqa: E402
from wager.harness.episode import run_episode  # noqa: E402

CASE_ROOT = ROOT / "cases"
OUT_PATH = ROOT / "scripts" / "out" / "exp_hint_0118_results.json"

MODEL = "DeepSeek-V3.2"  # the deployment id the e05 pattern uses for DeepSeek

# world -> the `type` label used in scratchpad_replica_ds_results.json
WORLDS = {
    "first_story_scarce_v0": "trap_scarce_live",   # TRAP: rushed termination under scarcity
    "first_story_v0": "trap_full_budget",          # CONTROL: same facade, full budget
}
CONDS = ("libre", "hint_T", "placebo")
SEEDS = (55, 56, 57, 58, 59, 60, 61, 62)  # SAME seeds as the 0110 replica, per world

# ---------------------------------------------------------------------------
# FROZEN hint texts -- copied VERBATIM (byte for byte) from ADR 0118 (do NOT
# "improve" them). hint_T is identical in both worlds (verbatim from ADR 0097).
# ---------------------------------------------------------------------------
HINT_T = (
    "A tight budget tempts you to rush the final answer. Do not: make sure "
    "your submitted model actually incorporates the evidence you paid for, and "
    "check every part of what you hand in before submitting."
)
PLACEBO = (
    "When you write your final model, prefer clear, descriptive variable names "
    "and consistent formatting; keep your code easy to read."
)
# guard against an accidental double-space from the line-continuation above
assert "  " not in HINT_T, "HINT_T has a stray double space"
assert "  " not in PLACEBO, "PLACEBO has a stray double space"


def suffix_for(cond: str) -> str:
    """The system_suffix injected for each arm. Appended as its own paragraph to
    the base SYSTEM prompt (the SYSTEM string has no trailing newline). `libre` =
    empty suffix = the standard 'free' condition every prior E0/replica used."""
    if cond == "libre":
        return ""
    if cond == "hint_T":
        return "\n\n" + HINT_T
    if cond == "placebo":
        return "\n\n" + PLACEBO
    raise ValueError(f"unknown cond: {cond}")


def full_plan() -> list[tuple[str, str, int]]:
    return [(w, c, s) for w in WORLDS for c in CONDS for s in SEEDS]


SMOKE_PLAN = [
    ("first_story_scarce_v0", "hint_T", SEEDS[0]),  # scarce/hint_T/seed55
    ("first_story_v0", "hint_T", SEEDS[0]),         # full/hint_T/seed55
]


def classify(accepted: bool) -> str:
    """ADR 0110 zero classifier (pure code, NO LLM): judge = a valid model was
    delivered (its R is the signal, even R=0); exec = no valid model delivered
    (max_tokens/max_turns/no_cell/hard error) -> excluded from the cell median."""
    return "judge" if accepted else "exec"


def _load_rows() -> list[dict]:
    if OUT_PATH.exists():
        return json.loads(OUT_PATH.read_text(encoding="utf-8"))
    return []


def _write_rows(rows: list[dict]) -> None:
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUT_PATH.write_text(json.dumps(rows, indent=2) + "\n", encoding="utf-8")


def _done_triples(rows: list[dict]) -> set[tuple[str, str, int]]:
    # a cell counts as done (skippable on resume) only if it has a row that
    # completed WITHOUT a hard error -- errored rows are retried on the next run.
    return {
        (r["world"], r["cond"], r["seed"])
        for r in rows
        if r.get("error") is None
    }


def run_one(world: str, cond: str, seed: int) -> tuple[dict, dict | None]:
    """Run a single episode. Returns (row, result). On a hard exception the row
    is an errored/exec row and result is None."""
    case_dir = CASE_ROOT / world
    t0 = time.perf_counter()
    try:
        server = build_world_server(case_dir, seed_offset=seed)
        result = run_episode(server, model=MODEL, system_suffix=suffix_for(cond))
        row = {
            "world": world,
            "type": WORLDS[world],
            "cond": cond,
            "seed": seed,
            "R": result["R"],
            "R_uncl": result["R_unclipped"],
            "accepted": result["accepted"],
            "abort": result["abort_reason"],
            "klass": classify(result["accepted"]),
            "error": None,
        }
        row["_wall_s"] = round(time.perf_counter() - t0, 1)
        row["_tokens"] = result["tokens"]
        return row, result
    except Exception as exc:  # noqa: BLE001  (infra/API failure -> excluded, retried)
        row = {
            "world": world,
            "type": WORLDS[world],
            "cond": cond,
            "seed": seed,
            "R": None,
            "R_uncl": None,
            "accepted": False,
            "abort": None,
            "klass": "exec",
            "error": f"{type(exc).__name__}: {exc}"[:300],
        }
        row["_wall_s"] = round(time.perf_counter() - t0, 1)
        return row, None


def _log(row: dict) -> None:
    r = row["R"]
    rs = f"{r:.3f}" if r is not None else " None"
    tok = row.get("_tokens", {})
    tokstr = ""
    if tok:
        tokstr = (f"  tokens={tok['total']} (p={tok['prompt']} c={tok['completion']}"
                  f" r={tok.get('reasoning', 0)})")
    err = f"  ERROR={row['error']}" if row.get("error") else ""
    print(f"  [{row['klass']:>5}] {row['world']}/{row['cond']}/seed{row['seed']}"
          f"  R={rs}  abort={row['abort']}{tokstr}  wall={row.get('_wall_s')}s{err}",
          flush=True)


def _persist(rows: list[dict], row: dict) -> None:
    """Replace any prior rows for this (world,cond,seed) and append the fresh one,
    then rewrite the file (checkpoint after every episode). The `_wall_s` /
    `_tokens` helper fields are stripped from what we persist (schema stays clean)."""
    key = (row["world"], row["cond"], row["seed"])
    kept = [r for r in rows if (r["world"], r["cond"], r["seed"]) != key]
    clean = {k: v for k, v in row.items() if not k.startswith("_")}
    kept.append(clean)
    rows[:] = kept
    _write_rows(rows)


def _preflight_env() -> None:
    """Fail fast (do NOT hunt for keys in files) if credentials are not in the env.
    FoundryChat calls load_dotenv(); we replicate that check here so we stop BEFORE
    building a world server if the key is simply not set."""
    from dotenv import load_dotenv  # noqa: PLC0415
    load_dotenv()
    import os  # noqa: PLC0415
    missing = [k for k in ("AZURE_FOUNDRY_BASE_URL", "AZURE_INFERENCE_CREDENTIAL")
               if not os.environ.get(k)]
    if missing:
        print("STOP: missing credentials in the environment: " + ", ".join(missing))
        print("      (set them as the e05 pattern expects; NOT hunting for keys in files)")
        sys.exit(2)


def _run_plan(plan: list[tuple[str, str, int]], label: str, resume: bool) -> None:
    _preflight_env()
    rows = _load_rows()
    done = _done_triples(rows) if resume else set()
    todo = [t for t in plan if t not in done]
    print("=" * 78)
    print(f"{label}: {len(todo)} episode(s) to run"
          + (f" ({len(plan) - len(todo)} already done, skipped)" if resume else "")
          + f"  ->  {OUT_PATH}")
    print("=" * 78, flush=True)

    tot = {"prompt": 0, "completion": 0, "reasoning": 0, "total": 0}
    ran = 0
    for (world, cond, seed) in todo:
        print(f"\n>>> {world}/{cond}/seed{seed} ...", flush=True)
        row, result = run_one(world, cond, seed)
        _log(row)
        _persist(rows, row)
        ran += 1
        if result is not None:
            for k in tot:
                tot[k] += result["tokens"][k]

    print("\n" + "=" * 78)
    print(f"{label} DONE: ran {ran} episode(s)")
    if ran:
        print(f"  tokens total: {tot['total']}  (prompt={tot['prompt']} "
              f"completion={tot['completion']} reasoning={tot['reasoning']})")
        # rough cost estimate -- rate is NOT wired in the repo; assumed external
        # public DeepSeek rate, labeled approximate so no fabricated precision.
        in_rate, out_rate = 0.28, 0.42  # US$ per 1M tokens (assumed, external)
        est = tot["prompt"] / 1e6 * in_rate + tot["completion"] / 1e6 * out_rate
        print(f"  cost approx: ~US${est:.4f} total, ~US${est / ran:.4f}/episode"
              f"  (assumed public rate ${in_rate}/${out_rate} per Mtok -- NOT a wired repo value)")
    print(f"  results -> {OUT_PATH}")
    print("=" * 78, flush=True)


def _dry_run() -> None:
    """Verify wiring with NO API call: import ok, build one server per world,
    and print the plan + the exact injected suffix strings."""
    print("DRY-RUN (no API). Plan =", len(full_plan()), "episodes; smoke =",
          len(SMOKE_PLAN))
    for cond in CONDS:
        s = suffix_for(cond)
        print(f"\n[cond={cond}] system_suffix ({len(s)} chars):")
        print(repr(s))
    for world in WORLDS:
        server = build_world_server(CASE_ROOT / world, seed_offset=SEEDS[0])
        print(f"\n[world={world}] built ok: case_id={server.case_id} "
              f"budget={server.config.budget}")
    print("\nSMOKE_PLAN:", SMOKE_PLAN)
    print("dry-run ok (imports + case load + suffixes verified; no episode run).")


def main() -> None:
    args = set(sys.argv[1:])
    if "--dry-run" in args:
        _dry_run()
    elif "--smoke" in args:
        _run_plan(SMOKE_PLAN, "SMOKE", resume=False)
    elif "--full" in args:
        _run_plan(full_plan(), "FULL", resume=True)
    else:
        print(__doc__)
        print("choose one: --dry-run | --smoke | --full")
        sys.exit(1)


if __name__ == "__main__":
    main()
