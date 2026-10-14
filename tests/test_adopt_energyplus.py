"""Guard the two edits of an EnergyPlus release adoption that a script performs.

The script is ``scripts/adopt_energyplus.py``, loaded by path as a maintainer script rather than
part of the distributed package. Its commands are named in the adoption roster held in
idfkit-conformance and are executed unattended, so each edit is tested against the files it edits
as they stand in this repository, not against a simplified copy: a registry or a matrix reshaped
so that the script no longer finds it must fail here and not during an adoption.
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path
from typing import Any

import pytest

_REPO_ROOT = Path(__file__).resolve().parent.parent
_SCRIPTS = _REPO_ROOT / "scripts"
_VERSIONS = _REPO_ROOT / "src" / "idfkit" / "versions.py"
_WORKFLOW = _REPO_ROOT / ".github" / "workflows" / "main.yml"


def _load(name: str, path: Path) -> Any:
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


adopt = _load("adopt_energyplus", _SCRIPTS / "adopt_energyplus.py")

#: A release later than any that exists, so the tests do not change meaning at the next adoption.
_NEXT = adopt.Release(99, 1, 0)


def _registered(text: str) -> list[tuple[int, int, int]]:
    namespace: dict[str, Any] = {}
    exec(compile(text, "versions.py", "exec"), namespace)  # noqa: S102
    return list(namespace["ENERGYPLUS_VERSIONS"])


class TestRegister:
    def test_the_release_becomes_the_latest(self) -> None:
        edit = adopt.register(_VERSIONS.read_text(encoding="utf-8"), _NEXT)

        assert edit.changed
        versions = _registered(edit.text)
        assert versions[-1] == (99, 1, 0)
        assert versions == sorted(versions)

    def test_only_one_line_is_added(self) -> None:
        before = _VERSIONS.read_text(encoding="utf-8")
        after = adopt.register(before, _NEXT).text

        assert [line for line in after.splitlines() if line not in before.splitlines()] == ["    (99, 1, 0),"]
        assert len(after.splitlines()) == len(before.splitlines()) + 1

    def test_a_listed_release_is_left_as_it_is(self) -> None:
        once = adopt.register(_VERSIONS.read_text(encoding="utf-8"), _NEXT).text
        twice = adopt.register(once, _NEXT)

        assert not twice.changed
        assert twice.text == once

    def test_an_earlier_release_is_placed_in_order(self) -> None:
        edit = adopt.register(_VERSIONS.read_text(encoding="utf-8"), adopt.Release(9, 0, 0))

        versions = _registered(edit.text)
        assert versions == sorted(versions)
        assert (9, 0, 0) in versions

    def test_an_unrecognised_registry_is_refused(self) -> None:
        with pytest.raises(adopt.AdoptionError, match="ENERGYPLUS_VERSIONS"):
            adopt.register("ENERGYPLUS_VERSIONS = load()\n", _NEXT)


class TestSweepRow:
    @staticmethod
    def _rows(text: str) -> list[dict[str, Any]]:
        import yaml

        return yaml.safe_load(text)["jobs"]["example-sweep"]["strategy"]["matrix"]["include"]

    def test_the_row_is_added_last_with_the_measured_counts(self) -> None:
        before = _WORKFLOW.read_text(encoding="utf-8")
        edit = adopt.add_row(before, _NEXT, findings=7, errors=2)

        assert edit.changed
        rows = self._rows(edit.text)
        assert rows[-1] == {"version": "99.1.0", "findings": 7, "errors": 2}
        assert rows[:-1] == self._rows(before)

    def test_only_one_line_is_added(self) -> None:
        before = _WORKFLOW.read_text(encoding="utf-8")
        after = adopt.add_row(before, _NEXT, findings=7, errors=2).text

        added = [line for line in after.splitlines() if line not in before.splitlines()]
        assert added == ['          - { version: "99.1.0", findings: 7, errors: 2 }']

    def test_a_present_row_is_left_as_it_is(self) -> None:
        once = adopt.add_row(_WORKFLOW.read_text(encoding="utf-8"), _NEXT, findings=7, errors=2).text
        twice = adopt.add_row(once, _NEXT, findings=0, errors=0)

        assert adopt.has_row(once, _NEXT)
        assert not twice.changed
        assert twice.text == once

    def test_a_workflow_without_the_matrix_is_refused(self) -> None:
        with pytest.raises(adopt.AdoptionError, match="sweep matrix"):
            adopt.add_row("jobs: {}\n", _NEXT, findings=0, errors=0)

    def test_the_sparse_selection_drops_comments_and_blank_lines(self) -> None:
        text = "# a comment\n\ntestfiles/*.idf\n  # indented comment\n!testfiles/_1a-Long0.0.idf\n"

        assert adopt.sparse_patterns(text) == ["testfiles/*.idf", "!testfiles/_1a-Long0.0.idf"]

    def test_an_empty_directory_measures_nothing(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.syspath_prepend(str(_SCRIPTS))

        with pytest.raises(adopt.AdoptionError, match="nothing was measured"):
            adopt.measure(tmp_path)

    def test_a_directory_is_measured_with_the_sweep(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.syspath_prepend(str(_SCRIPTS))
        (tmp_path / "one.idf").write_text("Version,\n  24.1;\n\nZone,\n  Office;\n", encoding="utf-8")

        measured = adopt.measure(tmp_path)

        assert (measured.files, measured.findings, measured.errors) == (1, 0, 0)

    def test_a_release_without_a_bundled_schema_is_not_measured(self, tmp_path: Path) -> None:
        with pytest.raises(adopt.AdoptionError, match="no bundled schema"):
            adopt.require_bundled_schema(_NEXT, tmp_path)

    def test_a_bundled_release_may_be_measured(self) -> None:
        adopt.require_bundled_schema(adopt.Release(24, 1, 0), _REPO_ROOT / "src" / "idfkit" / "schemas")


class TestCommandLine:
    def test_a_malformed_release_is_refused(self) -> None:
        with pytest.raises(SystemExit) as stopped:
            adopt.main(["register", "26.2"])

        assert stopped.value.code == 2
