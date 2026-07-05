"""ADR integrity lint (pre-commit; ADR 0070, ex Decision Log v0.56-4).

Decision records live in docs/adr/ -- one markdown file per decision (the
adr.github.io pattern). Append-only: you ADD new ADRs; existing files are
IMMUTABLE and never disappear (supersede = new file + a status note in the
index). README.md (the index) is the one mutable file. Compares the staged
tree against HEAD.

Born from a near-miss (a bulk regex once corrupted the monolithic log); the
scare became this guard. It moved from block-diffing one file to file-level
immutability when the log became per-file ADRs.
"""

import subprocess
import sys

ADR_DIR = "docs/adr/"
INDEX = "docs/adr/README.md"


def main():
    r = subprocess.run(
        ["git", "diff", "--cached", "--name-status", "HEAD", "--", ADR_DIR],
        capture_output=True, text=True, encoding="utf-8",
    )
    if r.returncode != 0:
        return 0  # no HEAD yet / dir absent: nothing to compare
    errs = []
    for line in r.stdout.splitlines():
        if not line.strip():
            continue
        parts = line.split("\t")
        status, path = parts[0], parts[-1]
        if path == INDEX or not path.endswith(".md"):
            continue  # the index is mutable
        if status.startswith("M"):
            errs.append(f"{path}: MODIFICADO (los ADR existentes son INMUTABLES; superseder = archivo nuevo)")
        elif status.startswith("D"):
            errs.append(f"{path}: BORRADO (nada se borra, se supersede)")
        elif status.startswith("R"):
            errs.append(f"{path}: RENOMBRADO (los ADR existentes son inmutables)")
    if errs:
        print("ADR integrity FAILED:", file=sys.stderr)
        for e in errs:
            print("  - " + e, file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
