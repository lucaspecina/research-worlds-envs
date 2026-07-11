"""Blind annotation packs for the fork experiment (ADR 0133 endpoint).

Reads scripts/out/fork_0133/cell_*.json and produces:
  - blind/pack_<XX>.md      one per delivery, RANDOM id, treatment stripped:
                              donor context (same for all cells of a donor) +
                              fork delivery reasoning + submitted code.
                              NO arm label, NO R anywhere.
  - blind/KEY.json          random id -> (block, donor, arm, file). DO NOT OPEN
                              until all annotations are recorded.

Annotation task (per pack, defects a-d of ADR 0133):
  (a) discrepancy between pre-delivery conclusion and submitted code
  (b) causal arrow not backed by an experiment
  (c) invented or double-counted noise
  (d) observational/default branch incompatible with purchased evidence

Run: .venv/Scripts/python scripts/fork_0133_blind_pack.py
"""

import json
import random
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CELLS = ROOT / "scripts" / "out" / "fork_0133"
BLIND = CELLS / "blind"
AUTOPSY = ROOT / "scripts" / "out" / "autopsy_0127"

sys.stdout.reconfigure(encoding="utf-8", errors="replace")


def donor_context(seed: int) -> str:
    """What the donor bought and concluded BEFORE delivery (shared context)."""
    ep = json.loads((AUTOPSY / f"ep_libre_seed{seed}.json").read_text(encoding="utf-8"))
    trace = ep["trace"]
    cells = [t.get("cell") or "" for t in trace]
    code = "\n".join(cells)
    lines = [f"### Investigation context (donor D{seed % 7})", ""]
    lines.append("Purchases/experiments made during the (identical, replayed) investigation:")
    for i, c in enumerate(cells[:-1]):
        for ln in c.splitlines():
            s = ln.strip()
            if ".observe(" in s or ".experiment(" in s:
                lines.append(f"  - turn {i+1}: {s[:160]}")
    lines.append("")
    lines.append("Reasoning in the last two turns BEFORE the delivery turn:")
    for t in trace[-3:-1]:
        lines.append("---")
        lines.append((t.get("reply_text") or "")[:2500])
    return "\n".join(lines)


def main() -> None:
    files = sorted(CELLS.glob("cell_*.json"))
    if not files:
        print("no cells yet"); return
    BLIND.mkdir(exist_ok=True)
    rng = random.Random(20260711)
    ids = [f"{i:02d}" for i in range(len(files))]
    rng.shuffle(ids)

    key = {}
    ctx_cache: dict[int, str] = {}
    made = 0
    for f, pid in zip(files, ids):
        cell = json.loads(f.read_text(encoding="utf-8"))
        if cell.get("error"):
            key[pid] = {"file": f.name, "skipped": f"error: {cell['error']}"}
            continue
        seed = cell["donor_seed"]
        if seed not in ctx_cache:
            ctx_cache[seed] = donor_context(seed)
        replies = cell.get("fork_replies") or []
        body = [f"# Pack {pid}", "", ctx_cache[seed], "",
                "### Delivery-phase reasoning (the part under annotation)", ""]
        for j, r in enumerate(replies):
            body.append(f"--- delivery turn {j+1} ---")
            body.append(r[:6000])
        body += ["", "### Submitted model code", "", "```python",
                 (cell.get("submission_code") or "(no submission)")[:8000], "```", "",
                 "### Annotate (true/false + one-line quote as evidence)",
                 "(a) pre-delivery conclusion vs code discrepancy:",
                 "(b) causal arrow without experimental backing:",
                 "(c) invented or double-counted noise:",
                 "(d) obs/default branch incompatible with evidence:", ""]
        (BLIND / f"pack_{pid}.md").write_text("\n".join(body), encoding="utf-8")
        key[pid] = {"file": f.name, "block": cell.get("block"),
                    "donor": seed, "arm": cell.get("arm")}
        made += 1

    (BLIND / "KEY.json").write_text(json.dumps(key, indent=2) + "\n", encoding="utf-8")
    print(f"packs: {made} | key sellada en blind/KEY.json (NO abrir hasta anotar todo)")


if __name__ == "__main__":
    main()
