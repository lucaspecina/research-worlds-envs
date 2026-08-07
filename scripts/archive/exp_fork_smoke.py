"""FORK smoke (machinery test, ADR 0130): same frozen investigation, vary ONLY
the hint at delivery time.

Takes a completed AUTOPSY episode (the acquisition DONOR, from the libre arm),
deterministically REPLAYS its cells against a fresh server (same world, same
seed -> same data, same budget path, zero LLM calls), injects the donor's
conversation into a fresh chat whose system prompt carries the VARIANT suffix,
and lets the model produce the delivery under that suffix (up to a few turns).

This is a SMOKE of the machinery (2 forks: control suffix="" + original hint),
NOT the fork experiment -- that one gets its own pre-registration with the
frozen variant bank (ADR 0127) before running.

Run: .venv/Scripts/python scripts/exp_fork_smoke.py
"""

import json
import sys
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
HINT_T = (
    "A tight budget tempts you to rush the final answer. Do not: make sure "
    "your submitted model actually incorporates the evidence you paid for, and "
    "check every part of what you hand in before submitting."
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


def fork(donor_file: Path, system_suffix: str, label: str, max_fork_turns: int = 5) -> dict:
    donor = json.loads(donor_file.read_text(encoding="utf-8"))
    seed = donor["_autopsy"]["seed"]
    trace = donor["trace"]
    n_replay = len(trace) - 1  # todo menos el turno de la entrega del donante

    server = build_world_server(CASE, seed_offset=seed)
    history: list[dict] = []  # pares (user, assistant) reconstruidos
    replay_mismatches = 0

    out: dict = {"label": label, "donor_seed": seed, "n_replay": n_replay}
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

        # el fork: chat nuevo con el sufijo VARIANTE + el historial inyectado
        chat = FoundryChat(system=SYSTEM + system_suffix, model=MODEL,
                           max_completion_tokens=MAX_COMPLETION_TOKENS)
        chat.messages.extend(history)

        fork_turns = 0
        abort = "max_fork_turns"
        for j in range(max_fork_turns):
            turn_idx = n_replay + 1 + j
            notices = server.begin_turn(turn_idx)
            if notices:
                prompt = ("\n".join(f"[NOTICE] {n}" for n in notices)
                          + "\n(env.describe() now lists any newly available source.)\n\n" + prompt)
            reply = chat.ask(prompt)
            fork_turns += 1
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
                "submission_code": res.get("code")})
    return out


def main() -> None:
    donor = ROOT / "scripts" / "out" / "autopsy_0127" / "ep_libre_seed62.json"  # donante: R bajo (0.13)
    rows = []
    for suffix, label in (("", "control_sin_pista"), ("\n\n" + HINT_T, "pista_original")):
        print(f"\n>>> fork [{label}] sobre donante libre/s62 ...", flush=True)
        r = fork(donor, suffix, label)
        rows.append({k: v for k, v in r.items() if k != "submission_code"})
        print("   ", json.dumps(rows[-1], ensure_ascii=False, default=str), flush=True)
        (ROOT / "scripts" / "out" / f"fork_smoke_{label}.json").write_text(
            json.dumps(r, indent=2, default=str) + "\n", encoding="utf-8")
    print("\nDONANTE: libre/s62 tenia R=0.132 con su propia entrega.", flush=True)


if __name__ == "__main__":
    main()
