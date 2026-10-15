"""Fail if any document contains a banned term or a pattern that looks like a leak.

Usage: python3 scripts/check_banned_terms.py [file ...]    (no arguments: every .md file)

Two layers:
- patterns built in below: email addresses, absolute home or server paths, long token-like strings;
- a local, git-ignored file `.banned-terms` (one case-insensitive regex per line, `#` comments allowed).
The terms list is never committed, so the list itself cannot leak what it blocks.
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BUILT_IN = {
    "email address": r"[\w.+-]+@[\w-]+\.[a-z]{2,}",
    "absolute path": r"(?:/Users/|/home/|/srv/)\S+",
    "token-like string": r"\b(?=[A-Za-z0-9_-]*\d)(?=[A-Za-z0-9_-]*[A-Za-z])[A-Za-z0-9_-]{32,}\b",
}


def load_terms(path):
    if not path.exists():
        return {}
    terms = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line and not line.startswith("#"):
            terms[f"banned term /{line}/"] = line
    return terms


def scan_text(text, patterns):
    """Return (label, line number, line) for every match, one entry per matching line and label."""
    hits = []
    for number, line in enumerate(text.splitlines(), 1):
        for label, pattern in patterns.items():
            if re.search(pattern, line, re.IGNORECASE):
                hits.append((label, number, line.strip()[:100]))
    return hits


def main(argv, root=ROOT):
    patterns = {**BUILT_IN, **load_terms(root / ".banned-terms")}
    files = [Path(a) for a in argv] if argv else sorted(root.rglob("*.md"))
    failed = 0
    for f in files:
        if f.suffix != ".md" or ".git" in f.parts:
            continue
        for label, number, line in scan_text(f.read_text(encoding="utf-8"), patterns):
            print(f"{f}:{number}: {label}: {line}")
            failed += 1
    if failed:
        print(f"\n{failed} problem(s). Fix them before committing.")
        return 1
    print(f"OK: {len(files)} file(s) clean")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
