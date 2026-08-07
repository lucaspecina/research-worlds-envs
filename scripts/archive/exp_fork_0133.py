"""FORK diagnostico (ADR 0133, pre-registered): 4 donors x 3 arms x 5 temporal blocks = 60 deliveries.

Measures integration/compilation analysis->delivery under FIXED evidence: each cell
deterministically replays a donor investigation (zero LLM cost), then lets the model
produce the delivery under one of three system-suffix arms:
  - neutral:   no suffix
  - principle: one of 4 frozen variants from the ADR 0127 bank (#1/#4/#7/#10),
               rotated donor x block in a latin square
  - scaffold:  frozen mechanical checklist (the deliberate operational upper bound)

Donors (eligibility audited per ADR 0133 criteria, chosen by seed order among eligible):
libre seeds 56, 57, 59, 60 from scripts/out/autopsy_0127/.

Blocks start >= 60 min apart (block = temporal factor). Within a block the 12 cells run
in seeded-random order. Resumable: existing cell files are skipped.

Run (background): .venv/Scripts/python scripts/exp_fork_0133.py
Single block:     .venv/Scripts/python scripts/exp_fork_0133.py --block 0
"""

import argparse
import json
import random
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from wager.agent.cells import extract_cell  # noqa: E402
from wager.agent.llm_client import FoundryChat  # noqa: E402
from wager.harness.case_episode import build_world_server  # noqa: E402
from wager.harness.episode import MAX_COMPLETION_TOKENS, SYSTEM  # noqa: E402
from wager.harness.kernel_proc import KernelClient  # noqa: E402

CASE = ROOT / "cases" / "first_story_scarce_v0"
MODEL = "DeepSeek-V3.2"
DONORS = [56, 57, 59, 60]
OUT = ROOT / "scripts" / "out" / "fork_0133"
BLOCK_GAP_S = 60 * 60  # >= 60 min between block starts
MAX_FORK_TURNS = 5

# ADR 0127 bank, mechanical rule "one per quarter": #1, #4, #7, #10
PRINCIPLE_VARIANTS = {
    1: "Before submitting, make sure your final model reflects what you actually "
       "learned during the investigation.",
    4: "When you finish, check that the model you deliver is consistent with the "
       "evidence you gathered.",
    7: "Close the loop before closing the episode: verify your deliverable reflects "
       "your analysis.",
    10: "Finish deliberately: confirm the delivered model embodies the conclusions "
        "you reached.",
}
VARIANT_ORDER = [1, 4, 7, 10]

SCAFFOLD = (
    "Before submitting, complete this mechanical checklist: (1) List each claim your "
    "final model encodes, and next to each the specific evidence (source, rows, or "
    "experiment) that supports it. (2) For every causal arrow or do()-branch in your "
    "code, name the experiment that identifies it; if none does, use an observational "
    "default and say so explicitly. (3) For every noise or variance parameter, point "
    "to the measurement that produced it; never invent or double-count noise. "
    "(4) Compare your final code against your stated conclusions: every conclusion "
    "must appear in the code, and nothing in the code may contradict your conclusions. "
    "Only after completing all four steps, submit."
)


def _initial_prompt(server) -> str:
    sheet = server.describe()
    return ("Here is the brief:\n\n" + sheet["brief"]
            + "\n\nMachine-readable sheet:\n"
            + json.dumps({k: v for k, v in sheet.items() if k != "brief"}, indent=2)
            + "\n\nReason briefly about your opening plan, then write your first cell. "
            "`env` is already in the namespace.")


def _feedback(result_ok, stdout, error, budget_remaining) -> str:
    fb = (f"Kernel output (ok={result_ok}, budget remaining={budget_remaining:.0f}):\n"
          + (stdout or "(no stdout)"))
    if error:
        fb += "\nTRACEBACK:\n" + error
    fb += ("\n\nReason about what this result tells you (does it confirm or refute your current "
           "hypothesis? what does it imply for the next step?), then write your next cell "
           "(or build and env.submit(code) when your reasoning has converged).")
    return fb


def fork(donor_file: Path, system_suffix: str) -> dict:
    """Replay the donor investigation (zero LLM), then deliver under the suffix.

    Same machinery as exp_fork_smoke.fork, plus: fork replies are captured for the
    blinded defect annotation (endpoint of ADR 0133)."""
    donor = json.loads(donor_file.read_text(encoding="utf-8"))
    seed = donor["_autopsy"]["seed"]
    trace = donor["trace"]
    n_replay = len(trace) - 1

    server = build_world_server(CASE, seed_offset=seed)
    history: list[dict] = []
    replay_mismatches = 0

    out: dict = {"donor_seed": seed, "n_replay": n_replay}
    with KernelClient(server, cell_timeout_s=30.0) as kernel:
        prompt = _initial_prompt(server)
        for i in range(n_replay):
            rec = trace[i]
            turn_idx = i + 1
            notices = server.begin_turn(turn_idx)
            if notices:
                prompt = ("\n".join(f"[NOTICE] {n}" for n in notices)
                          + "\n(env.describe() now lists any newly available source.)\n\n" + prompt)
            history.append({"role": "user", "content": prompt})
            history.append({"role": "assistant", "content": rec["reply_text"]})
            cell = rec.get("cell")
            if cell is None:
                out["error"] = f"donor turn {turn_idx} sin cell"
                return out
            result = kernel.run_cell(cell)
            src_ok = (rec.get("cell_result") or {}).get("ok")
            if bool(result.ok) != bool(src_ok):
                replay_mismatches += 1
            prompt = _feedback(result.ok, result.stdout, result.error, server.budget_remaining)

        out["replay_mismatches"] = replay_mismatches
        out["budget_after_replay"] = server.budget_remaining

        chat = FoundryChat(system=SYSTEM + system_suffix, model=MODEL,
                           max_completion_tokens=MAX_COMPLETION_TOKENS)
        chat.messages.extend(history)

        fork_replies: list[str] = []
        fork_turns = 0
        abort = "max_fork_turns"
        for j in range(MAX_FORK_TURNS):
            turn_idx = n_replay + 1 + j
            notices = server.begin_turn(turn_idx)
            if notices:
                prompt = ("\n".join(f"[NOTICE] {n}" for n in notices)
                          + "\n(env.describe() now lists any newly available source.)\n\n" + prompt)
            reply = chat.ask(prompt)
            fork_turns += 1
            fork_replies.append(reply.content)
            cell = extract_cell(reply.content)
            if cell is None:
                abort = "no_cell"
                break
            result = kernel.run_cell(cell)
            if server.terminal:
                abort = "submitted"
                break
            prompt = _feedback(result.ok, result.stdout, result.error, server.budget_remaining)

    res = server.result or {}
    out.update({"abort": abort, "fork_turns": fork_turns, "accepted": server.terminal,
                "R": res.get("R"), "R_uncl": res.get("R_unclipped"),
                "tokens_fork": chat.usage.total_tokens,
                "submission_code": res.get("code"),
                "fork_replies": fork_replies})
    return out


def cells_for_block(block: int) -> list[dict]:
    """The 12 cells of a block, arms resolved, in seeded-random order."""
    cells = []
    for d_idx, donor in enumerate(DONORS):
        variant_id = VARIANT_ORDER[(block + d_idx) % 4]  # latin square donor x block
        cells.append({"donor": donor, "arm": "neutral", "suffix": ""})
        cells.append({"donor": donor, "arm": f"principle_v{variant_id}",
                      "suffix": "\n\n" + PRINCIPLE_VARIANTS[variant_id]})
        cells.append({"donor": donor, "arm": "scaffold", "suffix": "\n\n" + SCAFFOLD})
    random.Random(5501 + block).shuffle(cells)
    return cells


def run_block(block: int) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    print(f"\n===== BLOCK {block} start {datetime.now(timezone.utc).isoformat()} =====", flush=True)
    for c in cells_for_block(block):
        name = f"cell_b{block}_d{c['donor']}_{c['arm']}.json"
        path = OUT / name
        if path.exists():
            print(f"   skip (exists): {name}", flush=True)
            continue
        donor_file = ROOT / "scripts" / "out" / "autopsy_0127" / f"ep_libre_seed{c['donor']}.json"
        t0 = time.time()
        try:
            r = fork(donor_file, c["suffix"])
        except Exception as e:  # una celda caida no tumba el bloque
            r = {"donor_seed": c["donor"], "error": f"{type(e).__name__}: {e}"}
        r.update({"block": block, "arm": c["arm"],
                  "started_at": datetime.now(timezone.utc).isoformat(),
                  "elapsed_s": round(time.time() - t0, 1), "model": MODEL})
        path.write_text(json.dumps(r, indent=2, default=str) + "\n", encoding="utf-8")
        brief = {k: r.get(k) for k in ("block", "arm", "donor_seed", "replay_mismatches",
                                       "abort", "R", "R_uncl", "tokens_fork", "elapsed_s", "error")}
        print("   " + json.dumps(brief, ensure_ascii=False, default=str), flush=True)
    print(f"===== BLOCK {block} done {datetime.now(timezone.utc).isoformat()} =====", flush=True)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--block", type=int, default=None, help="run a single block (0-4)")
    args = ap.parse_args()
    if args.block is not None:
        run_block(args.block)
        return
    for b in range(5):
        t0 = time.time()
        run_block(b)
        if b < 4:
            wait = max(0.0, BLOCK_GAP_S - (time.time() - t0))
            print(f"(sleeping {wait/60:.1f} min so block starts are >= 60 min apart)", flush=True)
            time.sleep(wait)
    print("\nALL BLOCKS DONE", flush=True)


if __name__ == "__main__":
    main()
