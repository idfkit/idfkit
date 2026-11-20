"""Fail when an entry under ``## [Unreleased]`` in CHANGELOG.md is too long.

A changelog entry says what changed, for whom, and links the PR. Benchmarks,
edge cases, error-message transcripts and internal mechanics belong in the PR
description, the docs (idfkit/idfkit-developers) or the bundled agent reference
(``agent_references/``). See the "Changelog" section of CLAUDE.md.

An entry is a top-level bullet (``-``, ``*`` or ``+``) plus every line that
belongs to it in Markdown: indented lines, nested bullets, blank lines inside
it and unindented ("lazy") continuation lines, up to the next top-level bullet
or heading. Released sections are not checked; a changelog with no
``## [Unreleased]`` heading fails.

Usage::

    uv run python scripts/check_changelog_entries.py [CHANGELOG.md]
"""

from __future__ import annotations

import re
import sys
from dataclasses import dataclass
from pathlib import Path

CHANGELOG = Path(__file__).resolve().parent.parent / "CHANGELOG.md"
"""The repository's changelog, checked when no path is given."""

UNRELEASED = "## [Unreleased]"

BULLETS = ("- ", "* ", "+ ")

HEADING = re.compile(r"#{1,6}(\s|$)")

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


@dataclass
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


def _starts_entry(line: str, in_entry: bool) -> bool:
    """Whether ``line`` is a top-level bullet, as Markdown reads list items.

    A bullet indented by up to three spaces is still top-level, except inside an entry, where two
    or more spaces (the width of ``- ``) make it a nested bullet of that entry.
    """
    stripped = line.lstrip(" ")
    indent = len(line) - len(stripped)
    return stripped.startswith(BULLETS) and indent < (2 if in_entry else 4)


def _indent_fenced(lines: list[str]) -> list[str]:
    """*lines*, with each line inside a fenced code block indented.

    A fenced line is code: a ``## `` or ``- `` in it is neither a heading nor an entry. Indented, it
    reads as a continuation of the entry around it, as Markdown reads it.
    """
    out: list[str] = []
    in_fence = False
    for line in lines:
        if line.lstrip().startswith(("```", "~~~")):
            in_fence = not in_fence
        elif in_fence and line.strip():
            line = "    " + line
        out.append(line)
    return out


def unreleased_entries(text: str) -> list[Entry] | None:
    """Return the top-level bullets of the ``## [Unreleased]`` section, or ``None`` with no such heading."""
    entries: list[Entry] = []
    found = in_unreleased = False
    current: Entry | None = None
    previous_blank = False
    for number, line in enumerate(_indent_fenced(text.splitlines()), start=1):
        if line.startswith("## "):
            in_unreleased = line.startswith(UNRELEASED)
            found = found or in_unreleased
            current = None
            continue
        if not in_unreleased:
            continue
        blank = not line.strip()
        if HEADING.match(line):
            current = None
        elif _starts_entry(line, current is not None):
            current = Entry(number, [line])
            entries.append(current)
        elif current is not None and (blank or line[0] in " \t" or not previous_blank):
            # Indented lines stay in the item across blank lines; an unindented line continues it
            # only straight after another line of it (lazy continuation), as Markdown reads it.
            current.lines.append(line)
        else:
            current = None
        previous_blank = blank
    for entry in entries:
        while entry.lines and not entry.lines[-1].strip():
            entry.lines.pop()
    return entries if found else None


def missing_heading(path: Path) -> str:
    """The message for a changelog with no ``## [Unreleased]`` heading."""
    return f"{path}: no '{UNRELEASED}' heading; keep one at the top, empty if need be"


def check(path: Path) -> list[str]:
    """Return one message per entry of ``path``'s ``[Unreleased]`` section that is over budget."""
    entries = unreleased_entries(path.read_text(encoding="utf-8"))
    if entries is None:
        return [missing_heading(path)]
    problems: list[str] = []
    for entry in entries:
        text = entry.text
        n_lines, n_chars = len(entry.lines), len(text)
        if n_lines > MAX_LINES or n_chars > MAX_CHARS:
            preview = text[:80] + ("..." if n_chars > 80 else "")
            problems.append(
                f"{path}:{entry.line}: entry is {n_lines} lines / {n_chars} chars "
                f"(max {MAX_LINES} / {MAX_CHARS}): {preview}"
            )
    return problems


def main(argv: list[str]) -> int:
    """Check the changelogs named in ``argv`` (default: the repository's) and report overlong entries."""
    paths = [Path(arg) for arg in argv] or [CHANGELOG]
    problems = [problem for path in paths for problem in check(path)]
    if problems:
        print("\n".join(problems), file=sys.stderr)
        headings = {missing_heading(path) for path in paths}
        if any(problem not in headings for problem in problems):  # the rule is about length only
            print(f"\n{RULE}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
