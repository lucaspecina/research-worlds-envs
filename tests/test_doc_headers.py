"""Doc-state and traceability lints (ex Decision Log v0.33; ADR-ized in ADR 0070).

Two structural guards that turn maintenance rules into build failures:

- Traceability: a functional's `brief_clause` must appear VERBATIM in the
  case's brief.md -- literal by definition (ARCHITECTURE §9.3); a re-skin
  breaks it silently, so the build catches it.
- Key sections: constitutional docs must keep their named sections, so a bulk
  edit that drops one fails before entering history.
- ADR sanity: the decision log is now docs/adr/ (one file per decision); every
  ADR file must appear in the index and the index must exist.

(The old NORTH_STAR/ARCHITECTURE/CLAUDE version-sync lints were retired with the
move to per-file ADRs: there is no single "current version" to keep in sync.)
"""

import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]


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


def _assert_key_sections(text: str, sections: list[str]) -> None:
    missing = [s for s in sections if s not in text]
    assert not missing, f"missing constitutional sections: {missing}"


def test_constitutional_docs_keep_their_key_sections():
    """A bulk edit that drops a section fails before entering history. Includes
    its own should-fail (guards ship with their autotest pair, ADR 0057)."""
    claude = (ROOT / "CLAUDE.md").read_text(encoding="utf-8")
    _assert_key_sections(claude, ["## Reglas duras", "## Workflow", "## Convenciones",
                                  "## Infraestructura", "## Estado actual"])
    arch = (ROOT / "ARCHITECTURE.md").read_text(encoding="utf-8")
    _assert_key_sections(arch, ["## 1. Anatomía de un caso", "## 5. Rivales",
                                "## 7. Certificados", "## 9. Scoring",
                                "### 10.1 Contrato de ventana", "## 13. Validación"])
    with pytest.raises(AssertionError):  # should-fail half of the pair
        _assert_key_sections("## solo esto", ["## Reglas duras"])


def test_adr_index_lists_every_decision():
    """The decision log is docs/adr/. Every ADR file appears in the index, and
    the index exists -- so a new ADR that forgets the index is caught."""
    adr = ROOT / "docs" / "adr"
    index = adr / "README.md"
    assert index.exists(), "docs/adr/README.md (the ADR index) must exist"
    index_text = index.read_text(encoding="utf-8")
    files = [p.name for p in adr.glob("*.md") if p.name != "README.md"]
    assert files, "docs/adr/ must contain ADR files"
    missing = [f for f in files if f not in index_text]
    assert not missing, f"ADR files not listed in the index: {missing}"
