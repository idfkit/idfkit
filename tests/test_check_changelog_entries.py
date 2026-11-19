"""Guard the changelog entry-length gate.

The gate lives in ``scripts/check_changelog_entries.py`` and is loaded by path, as a maintainer
script rather than part of the distributed package. It keeps ``[Unreleased]`` entries to a short
summary so that readers scanning for breaking changes can find them.
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path
from typing import Any

import pytest

_REPO_ROOT = Path(__file__).resolve().parent.parent
_SCRIPT = _REPO_ROOT / "scripts" / "check_changelog_entries.py"


def _load(name: str, path: Path) -> Any:
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


gate = _load("check_changelog_entries", _SCRIPT)

_CHANGELOG = """\
# Changelog

## [Unreleased]

### Added

- Short entry ([#1](https://example.invalid/1)).
- Wrapped entry that continues
  on a second line.
  - with a nested bullet.

### Fixed

- Another entry.

## [1.0.0] - 2026-01-01

### Added

- A released entry that is not checked
  even though
  it is
  much
  longer
  than
  the budget.
"""


def test_entries_are_read_from_unreleased_only() -> None:
    entries = gate.unreleased_entries(_CHANGELOG)
    assert [len(e.lines) for e in entries] == [1, 3, 1]
    assert entries[1].text == "- Wrapped entry that continues on a second line. - with a nested bullet."
    assert entries[0].line == 7


def test_released_sections_are_ignored(tmp_path: Path) -> None:
    path = tmp_path / "CHANGELOG.md"
    path.write_text(_CHANGELOG, encoding="utf-8")
    assert gate.check(path) == []


@pytest.mark.parametrize(
    "body",
    [
        "- one\n" + "  more\n" * gate.MAX_LINES,
        "- " + "x" * gate.MAX_CHARS,
    ],
    ids=["too-many-lines", "too-many-chars"],
)
def test_overlong_entry_fails_with_the_rule(tmp_path: Path, body: str, capsys: pytest.CaptureFixture[str]) -> None:
    path = tmp_path / "CHANGELOG.md"
    path.write_text(f"## [Unreleased]\n\n### Added\n\n{body}\n", encoding="utf-8")
    assert gate.main([str(path)]) == 1
    err = capsys.readouterr().err
    assert f"{path}:5:" in err
    assert "Rule (CLAUDE.md" in err


def test_repository_changelog_passes() -> None:
    assert gate.check(_REPO_ROOT / "CHANGELOG.md") == []


def test_entry_at_the_limit_passes(tmp_path: Path) -> None:
    body = "- " + "x" * (gate.MAX_CHARS - 2 - (gate.MAX_LINES - 1) * 2) + "\n" + "  y\n" * (gate.MAX_LINES - 1)
    path = tmp_path / "CHANGELOG.md"
    path.write_text(f"## [Unreleased]\n\n{body}", encoding="utf-8")
    (entry,) = gate.unreleased_entries(path.read_text(encoding="utf-8"))
    assert (len(entry.lines), len(entry.text)) == (gate.MAX_LINES, gate.MAX_CHARS)
    assert gate.check(path) == []


@pytest.mark.parametrize(
    ("body", "lines"),
    [
        ("- first\nlazy continuation\nanother\n", 3),
        ("- first\n\tTab-indented\n", 2),
        ("* star bullet\n  continued\n", 2),
        ("+ plus bullet\n", 1),
        ("- first\n\n  indented after a blank\n", 3),
        ("- first\n\nA paragraph after a blank is not the entry's\n", 1),
    ],
    ids=["lazy", "tab", "star", "plus", "indented-after-blank", "paragraph-after-blank"],
)
def test_every_line_markdown_puts_in_an_item_is_counted(body: str, lines: int) -> None:
    (entry,) = gate.unreleased_entries(f"## [Unreleased]\n\n{body}")
    assert len(entry.lines) == lines


def test_a_changelog_without_unreleased_fails(tmp_path: Path) -> None:
    path = tmp_path / "CHANGELOG.md"
    path.write_text("## Unreleased\n\n- " + "x" * 1000 + "\n", encoding="utf-8")
    (problem,) = gate.check(path)
    assert "no '## [Unreleased]' heading" in problem


def test_default_path_is_the_repository_changelog() -> None:
    assert gate.CHANGELOG == _REPO_ROOT / "CHANGELOG.md"


@pytest.mark.parametrize(
    ("body", "counts"),
    [
        (" - one space before the marker\n  continued\n", [2]),
        ("- first\n - a sibling, not nested\n", [1, 1]),
        ("- first\n  - nested\n", [2]),
        ("- first\n#305 is text, not a heading\n", [2]),
    ],
    ids=["indented-top-level", "indented-sibling", "nested", "hash-text"],
)
def test_items_are_split_as_markdown_splits_them(body: str, counts: list[int]) -> None:
    entries = gate.unreleased_entries(f"## [Unreleased]\n\n### Added\n\n{body}")
    assert entries is not None
    assert [len(e.lines) for e in entries] == counts


def test_missing_heading_does_not_print_the_length_rule(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    path = tmp_path / "CHANGELOG.md"
    path.write_text("# Changelog\n", encoding="utf-8")
    assert gate.main([str(path)]) == 1
    assert "Rule (CLAUDE.md" not in capsys.readouterr().err


def test_a_fenced_heading_does_not_end_the_unreleased_section() -> None:
    text = "## [Unreleased]\n\n```bash\n## a shell comment\n- not an entry\n```\n\n- Real entry.\n\n## [1.0.0]\n"
    entries = gate.unreleased_entries(text)
    assert [entry.line for entry in entries] == [8]
