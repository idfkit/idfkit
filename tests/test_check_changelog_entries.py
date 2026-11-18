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
