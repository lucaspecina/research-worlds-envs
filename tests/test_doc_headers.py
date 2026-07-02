"""Doc-state and traceability lints (Decision Log v0.33).

Twenty-odd versions of header drift (NORTH_STAR header stuck at v0.10 and
ARCHITECTURE at v0.5 while their bodies incorporated content up to v0.31)
motivated turning the maintenance rule into structure: the build fails when a
doc's declared state falls behind its own content -- same pattern as the
zero-LLM CI (discipline as code, not memory).

Also here: the traceability lint. A functional's `brief_clause` must appear
VERBATIM in the case's brief.md -- literal by definition (ARCHITECTURE §9.3),
and a re-skin breaks it silently (the post-skin check that motivated this file).
"""

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def _vt(s: str) -> tuple[int, ...]:
    return tuple(int(x) for x in s.split("."))


def _north_star_last_entry() -> str:
    text = (ROOT / "NORTH_STAR.md").read_text(encoding="utf-8")
    entries = re.findall(r"^\*\*v(\d+\.\d+) \(", text, flags=re.M)
    assert entries, "NORTH_STAR must have Decision Log entries (**vX.Y (date)**)"
    return max(entries, key=_vt)


def test_north_star_header_matches_last_decision_log_entry():
    text = (ROOT / "NORTH_STAR.md").read_text(encoding="utf-8")
    header = re.search(r"\*\*Estado\*\*: v(\d+\.\d+)", text)
    assert header, "NORTH_STAR header must declare **Estado**: vX.Y"
    last = _north_star_last_entry()
    assert header.group(1) == last, (
        f"NORTH_STAR header declares v{header.group(1)} but the last Decision Log "
        f"entry is v{last}: a new entry requires bumping the header (and vice versa)"
    )


def test_architecture_header_acknowledges_all_cited_versions():
    """The drift mode: a section edited citing Decision Log vN without touching
    the header. Every v0.N cited in the body must be acknowledged (mentioned)
    by the header's Estado/changelog line."""
    lines = (ROOT / "ARCHITECTURE.md").read_text(encoding="utf-8").splitlines()
    header_line = next((l for l in lines if "**Estado**" in l), None)
    assert header_line, "ARCHITECTURE must declare **Estado**: vX.Y"
    own = re.search(r"\*\*Estado\*\*: v(\d+\.\d+)", header_line)
    assert own, "ARCHITECTURE Estado must carry a version"
    assert f"v{own.group(1)}:" in header_line, (
        f"ARCHITECTURE declares v{own.group(1)} but its header changelog has no "
        f"'v{own.group(1)}:' entry describing that version"
    )
    body = "\n".join(l for l in lines if l != header_line)
    cited = re.findall(r"v(0\.\d+)", body)
    acked = re.findall(r"v(0\.\d+)", header_line)
    max_cited, max_acked = max(map(_vt, cited)), max(map(_vt, acked))
    assert max_cited <= max_acked, (
        f"ARCHITECTURE body cites v{'.'.join(map(str, max_cited))} but the header "
        f"only acknowledges up to v{'.'.join(map(str, max_acked))}: update the "
        f"header changelog in the same edit (una regla, una casa)"
    )


def test_claude_md_cites_current_decision_log_version():
    text = (ROOT / "CLAUDE.md").read_text(encoding="utf-8")
    m = re.search(r"Decision Log en v(\d+\.\d+)", text)
    assert m, "CLAUDE.md must cite 'Decision Log en vX.Y' in Estado actual"
    last = _north_star_last_entry()
    assert m.group(1) == last, (
        f"CLAUDE.md cites Decision Log v{m.group(1)} but NORTH_STAR's last entry "
        f"is v{last}"
    )


def test_functional_brief_clauses_verbatim_in_brief():
    """Traceability is literal: every declared functional's brief_clause appears
    verbatim (whitespace-normalized for hard-wrapping) in the case's brief.md.
    A case that declares functionals without a brief.md fails outright."""
    metas = sorted((ROOT / "cases").glob("*/meta.json"))
    assert metas, "no cases found"
    for meta_path in metas:
        meta = json.loads(meta_path.read_text(encoding="utf-8"))
        functionals = (meta.get("stakes") or {}).get("functionals") or []
        if not functionals:
            continue
        brief_path = meta_path.parent / "brief.md"
        assert brief_path.exists(), (
            f"{meta_path.parent.name}: declares functionals but has no brief.md "
            f"(the clause must cite a brief that exists)"
        )
        brief_norm = " ".join(brief_path.read_text(encoding="utf-8").split())
        for f in functionals:
            clause = " ".join(f["brief_clause"].split())
            assert clause in brief_norm, (
                f"{meta_path.parent.name}: brief_clause of functional "
                f"'{f['name']}' is NOT verbatim in brief.md -- a re-skin or brief "
                f"edit broke traceability; fix the CASE (brief + meta), never "
                f"invent the clause"
            )
