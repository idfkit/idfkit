"""Fail when an entry under ``## [Unreleased]`` in CHANGELOG.md is too long.

A changelog entry says what changed, for whom, and links the PR. Benchmarks,
edge cases, error-message transcripts and internal mechanics belong in the PR
description, the docs (idfkit/idfkit-developers) or the bundled agent reference
(``agent_references/``). See the "Changelog" section of CLAUDE.md.

An entry is a top-level ``- `` bullet plus its continuation lines (indented
lines, nested bullets and blank lines inside it) up to the next top-level
bullet or heading. Released sections are not checked.

Usage::

    uv run python scripts/check_changelog_entries.py [CHANGELOG.md]
"""

from __future__ import annotations

import sys
from dataclasses import dataclass
from pathlib import Path

MAX_LINES = 5
"""Wrapped source lines an entry may span, the bullet line included."""

MAX_CHARS = 450
"""Characters an entry may hold, its lines joined by single spaces, links included."""

RULE = f"""\
Rule (CLAUDE.md, "Changelog"): an [Unreleased] entry is 1-2 sentences, at most {MAX_LINES} lines
and {MAX_CHARS} characters including links. Say what changed for users and, for a **Breaking:**
entry, the migration in one clause. No benchmarks, error-message transcripts, edge-case catalogs
or internal mechanics: put those in the PR description, the docs (idfkit/idfkit-developers) or
agent_references/. Group PRs that form one feature into one entry with several refs."""


@dataclass(frozen=True)
class Entry:
    """One top-level bullet of the ``[Unreleased]`` section."""

    line: int
    """1-based line number of the bullet in the file."""
    lines: list[str]
    """The bullet's source lines, trailing blank lines removed."""

    @property
    def text(self) -> str:
        """The entry's text, its lines stripped and joined by single spaces."""
        return " ".join(part.strip() for part in self.lines if part.strip())


def unreleased_entries(text: str) -> list[Entry]:
    """Return the top-level bullets of the ``## [Unreleased]`` section of a changelog."""
    entries: list[Entry] = []
    in_unreleased = False
    current: Entry | None = None
    for number, line in enumerate(text.splitlines(), start=1):
        if line.startswith("## "):
            in_unreleased = line.startswith("## [Unreleased]")
            current = None
            continue
        if not in_unreleased:
            continue
        if line.startswith("#"):
            current = None
        elif line.startswith("- "):
            current = Entry(number, [line])
            entries.append(current)
        elif current is not None and (line.startswith(" ") or not line.strip()):
            current.lines.append(line)
        else:
            current = None
    for entry in entries:
        while entry.lines and not entry.lines[-1].strip():
            entry.lines.pop()
    return entries


def check(path: Path) -> list[str]:
    """Return one message per entry of ``path``'s ``[Unreleased]`` section that is over budget."""
    problems: list[str] = []
    for entry in unreleased_entries(path.read_text(encoding="utf-8")):
        n_lines, n_chars = len(entry.lines), len(entry.text)
        if n_lines > MAX_LINES or n_chars > MAX_CHARS:
            preview = entry.text[:80] + ("..." if n_chars > 80 else "")
            problems.append(
                f"{path}:{entry.line}: entry is {n_lines} lines / {n_chars} chars "
                f"(max {MAX_LINES} / {MAX_CHARS}): {preview}"
            )
    return problems


def main(argv: list[str]) -> int:
    """Check the changelog named in ``argv`` (default ``CHANGELOG.md``) and report overlong entries."""
    paths = [Path(arg) for arg in argv] or [Path("CHANGELOG.md")]
    problems = [problem for path in paths for problem in check(path)]
    if problems:
        print("\n".join(problems), file=sys.stderr)
        print(f"\n{RULE}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
