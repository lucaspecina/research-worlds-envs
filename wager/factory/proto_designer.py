"""Proto-designer -- the world GENERATOR half of the factory (ADR 0093).

FACTORY SIDE: LLMs are allowed here (the reward path stays zero-LLM; a generated
world.py is verified ONLY by the zero-LLM certification pipeline). This module is
never imported by wager.reward.

Rung 1 (FACIL, re-skin): re-skin a certified world into a NEW domain with the
mathematics IDENTICAL, and verify the certificates' R values are preserved (a
no-op test of the generator plumbing). Higher rungs (new static world, World B)
compose from the operator library and are added as their commissions are signed
(decisions A/B/C/D of docs/proto-designer.md).
"""

import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

RESKIN_SYSTEM = (
    "You are a world-designer on the factory side of an ML research harness. You re-skin "
    "an existing simulated 'world' into a NEW industrial/scientific domain WITHOUT changing "
    "any mathematics. A pure vocabulary/domain swap: mechanism, all numbers and all structure "
    "stay byte-for-byte equivalent; only human-facing names and prose change."
)

RESKIN_RULES = """Re-skin this world into a NEW concrete domain of your choice, different from
the source. HARD RULES (a verifier checks them mechanically):

1. CHANGE the column names to fit the new domain, keeping their ROLES (the settable decision
   knob; any inline reading(s); the final quality/outcome score with its threshold).
2. CHANGE all prose: column descriptions, the stakes narrative, the brief, the notes.
3. KEEP EVERY NUMBER IDENTICAL: all PARAMS values, knobs/ablations, functional threshold and
   direction, all weights/budgets/costs/seeds, n_samples/m_reps/lambda_mdl/c_f.
4. KEEP the mechanism STRUCTURE identical: the same equations in world.py, the same operator
   name+knobs+ablation in meta, the same smoke_regimes shape.
5. KEEP the PARAMS dict KEYS identical -- only the COLUMN names change, never internal keys.
6. The functional's "column" must be your NEW outcome column name; its "brief_clause" must be
   a sentence appearing VERBATIM in your new brief.md (copy it exactly).
7. In world.py, COLUMNS and the returned DataFrame keys are your new column names; the
   regime.config / control_surface settable keys use the new decision-knob name.

Return EXACTLY three fenced code blocks, each preceded by a line with only its filename:
world.py
```python
...
```
meta.json
```json
...
```
brief.md
```markdown
...
```
No other prose."""


def _extract_blocks(text: str) -> dict:
    blocks = {}
    for name, lang in (("world.py", "python"), ("meta.json", "json"), ("brief.md", "markdown")):
        m = re.search(rf"{re.escape(name)}\s*```(?:{lang}|\w*)?\n(.*?)```", text, re.S)
        blocks[name] = (m.group(1).rstrip() + "\n") if m else None
    return blocks


def reskin(source_dir: Path, target_dir: Path, model: str = "gpt-5.4") -> dict:
    """Generate a re-skinned world and CERTIFY it. Returns a yield record:
    {passed: bool, r_identical: bool, gates_ok: bool, domain, reason}."""
    from wager.agent.llm_client import FoundryChat  # lazy: keeps LLM out of import graph

    source_dir, target_dir = Path(source_dir), Path(target_dir)
    src = {f: (source_dir / f).read_text(encoding="utf-8")
           for f in ("world.py", "meta.json", "brief.md")}
    src_cert = json.loads((source_dir / "certificates.json").read_text(encoding="utf-8"))

    chat = FoundryChat(system=RESKIN_SYSTEM, model=model, max_completion_tokens=8000)
    reply = chat.ask(f"{RESKIN_RULES}\n\n=== SOURCE world.py ===\n{src['world.py']}\n\n"
                     f"=== SOURCE meta.json ===\n{src['meta.json']}\n\n"
                     f"=== SOURCE brief.md ===\n{src['brief.md']}")
    blocks = _extract_blocks(reply.content)
    if any(v is None for v in blocks.values()):
        return {"passed": False, "reason": "parse_fail",
                "have": {k: v is not None for k, v in blocks.items()}}

    target_dir.mkdir(exist_ok=True)
    (target_dir / "world.py").write_text(blocks["world.py"], encoding="utf-8", newline="\n")
    meta = json.loads(blocks["meta.json"])
    meta["case_id"] = target_dir.name
    (target_dir / "meta.json").write_text(json.dumps(meta, indent=2) + "\n", encoding="utf-8")
    (target_dir / "brief.md").write_text(blocks["brief.md"], encoding="utf-8", newline="\n")
    for f in ("build_and_certify.py", "make_ladder_fixtures.py"):
        if (source_dir / f).exists():
            (target_dir / f).write_text((source_dir / f).read_text(encoding="utf-8"),
                                        encoding="utf-8", newline="\n")

    r = subprocess.run([sys.executable, str(target_dir / "build_and_certify.py")],
                       capture_output=True, text=True, cwd=str(ROOT))
    if r.returncode != 0:
        return {"passed": False, "reason": "certify_crash", "stderr": r.stderr[-800:],
                "domain": [c["name"] for c in meta["columns"]]}
    gen_cert = json.loads((target_dir / "certificates.json").read_text(encoding="utf-8"))
    r_identical = all(abs(src_cert["R"][k] - gen_cert["R"].get(k, 1e9)) < 1e-6
                      for k in src_cert["R"])
    gates_ok = bool(gen_cert["gates"]["all"])
    return {"passed": r_identical and gates_ok, "r_identical": r_identical,
            "gates_ok": gates_ok, "domain": [c["name"] for c in meta["columns"]],
            "reason": "ok" if (r_identical and gates_ok) else "math_not_preserved"}


if __name__ == "__main__":
    src = ROOT / "cases" / (sys.argv[1] if len(sys.argv) > 1 else "prior_sweetspot_v0")
    tgt = ROOT / "cases" / (sys.argv[2] if len(sys.argv) > 2 else "reskin_pilot_v0")
    print(json.dumps(reskin(src, tgt), indent=2))
