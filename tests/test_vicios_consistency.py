"""Consistency guard for the docs/vicios/ layer (ADR 0140): the per-vice docs,
the README board, and the derivation doc can never silently drift apart.
Ships with its should-fail cases inline (ADR 0057: the assertions ARE the
should-fail pair -- delete a doc or an index row and the build breaks)."""

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VICIOS = ROOT / "docs" / "vicios"


def test_every_vicio_doc_is_on_the_board_and_viceversa():
    """docs/vicios/vicio-*.md <-> rows in the README index table."""
    readme = (VICIOS / "README.md").read_text(encoding="utf-8")
    docs = {p.name for p in VICIOS.glob("vicio-*.md")} | {"ahas.md"}
    linked = set(re.findall(r"\((vicio-[A-Za-z0-9-]+\.md|ahas\.md)\)", readme))
    missing_from_board = docs - linked
    dead_links = linked - docs
    assert not missing_from_board, (
        f"docs de vicios SIN fila en el tablero (docs/vicios/README.md): {missing_from_board}"
    )
    assert not dead_links, f"el tablero linkea docs que no existen: {dead_links}"


def test_derivation_doc_points_to_the_layer():
    """mundos-por-vicio.md must carry the pointer to docs/vicios/ (the evidence
    house) -- if a rewrite drops it, the layers disconnect silently."""
    t = (ROOT / "docs" / "mundos-por-vicio.md").read_text(encoding="utf-8")
    assert "docs/vicios/" in t, "mundos-por-vicio.md perdió el puntero a docs/vicios/"
    t2 = (ROOT / "docs" / "failure-modes.md").read_text(encoding="utf-8")
    assert "docs/vicios/" in t2, "failure-modes.md perdió el puntero a docs/vicios/"


def test_vicio_docs_carry_their_required_sections():
    """Every per-vice doc keeps its skeleton: sub-formas + estado. A bulk edit
    that drops a section fails before entering history."""
    for p in sorted(VICIOS.glob("vicio-*.md")):
        t = p.read_text(encoding="utf-8")
        assert ("Sub-forma" in t or "sub-forma" in t.lower() or "Firma" in t), (
            f"{p.name}: sin sección de sub-formas/firma")
        assert "Estado" in t, f"{p.name}: sin sección de estado"
