"""Decision Log integrity lint (pre-commit; Decision Log v0.56-4).

Born from a near-miss: a bulk regex script transiently corrupted NORTH_STAR
(recovered via git checkout). The scare becomes a guard: existing version
blocks are IMMUTABLE (append-only -- amendments are new entries) and the
version sequence is monotone. Compares the staged NORTH_STAR against HEAD.
"""

import re
import subprocess
import sys


def blocks(text):
    parts = re.split(r"(?=^\*\*v\d+\.\d+ \()", text, flags=re.M)
    out = []
    for p in parts:
        m = re.match(r"\*\*v(\d+\.\d+) \(", p)
        if m:
            out.append((tuple(int(x) for x in m.group(1).split(".")), p))
    return out


def show(ref):
    r = subprocess.run(["git", "show", ref], capture_output=True, text=True, encoding="utf-8")
    return r.stdout if r.returncode == 0 else ""


def main():
    staged = show(":NORTH_STAR.md")
    head = show("HEAD:NORTH_STAR.md")
    if not staged or not head:
        return 0  # file not staged / first commit: nothing to compare
    hb, sb = dict(blocks(head)), dict(blocks(staged))
    errs = []
    for v, b in hb.items():
        tag = "v" + ".".join(map(str, v))
        if v not in sb:
            errs.append(f"{tag}: REMOVED (nada se borra, se supersede)")
        elif sb[v].rstrip() != b.rstrip():
            # rstrip: the LAST block of HEAD runs to EOF; appending a new entry
            # moves its boundary by trailing whitespace only (maiden-commit
            # false positive, fixed like the denylist's --diff-filter=d)
            errs.append(f"{tag}: MODIFIED (bloques existentes son INMUTABLES; enmendar = entrada nueva)")
    versions = [v for v, _ in blocks(staged)]
    if versions != sorted(versions):
        errs.append("secuencia de versiones no monotona (append-only)")
    if errs:
        print("Decision Log integrity FAILED:", file=sys.stderr)
        for e in errs:
            print("  - " + e, file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
