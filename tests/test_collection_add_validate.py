"""``validate=`` on the typed ``IDFCollection.add``, at run time and under mypy.

``doc["Zone"].add("A", validate=False)`` skips validation as ``IDFDocument.add(..., validate=False)``
does: values, required fields and ranges are not checked, but a key the schema does not name is
still refused. What pyright reports is checked by ``tests/type_checks/collection_add_validate_fixture.py``
under ``make check``; :func:`test_mypy_reports_exactly_the_seeded_errors` checks that file with mypy.
"""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path
from typing import Any

import pytest

from idfkit import IDFDocument, new_document
from idfkit.exceptions import InvalidFieldError, ValidationFailedError

FIXTURE = Path(__file__).parent / "type_checks" / "collection_add_validate_fixture.py"


@pytest.fixture
def doc() -> IDFDocument[Any]:
    return new_document()


class TestValidateFalse:
    def test_skips_value_validation(self, doc: IDFDocument[Any]) -> None:
        zone = doc.zones.add("A", validate=False, **{"ceiling_height": "tall"})
        assert zone.ceiling_height == "tall"
        assert doc["Zone"]["A"] is zone

    def test_skips_required_field_validation(self, doc: IDFDocument[Any]) -> None:
        material = doc["Material"].add("XPS", validate=False, **{"thickness": 0.05})
        assert material.thickness == 0.05
        assert "XPS" in doc["Material"]

    def test_matches_the_string_keyed_form(self, doc: IDFDocument[Any]) -> None:
        typed = doc["Zone"].add("A", validate=False, **{"multiplier": -3})
        keyed = doc.add("Zone", "B", multiplier=-3, validate=False)
        assert typed.multiplier == keyed.multiplier == -3

    def test_still_refuses_an_unknown_key(self, doc: IDFDocument[Any]) -> None:
        with pytest.raises(InvalidFieldError, match="ceiling_hieght"):
            doc.zones.add("A", validate=False, **{"ceiling_hieght": 3.0})
        assert "A" not in doc["Zone"]

    def test_through_an_absent_type_stores_the_collection(self, doc: IDFDocument[Any]) -> None:
        zones = doc["Zone"]
        zones.add("A", validate=False)
        assert [z.name for z in zones] == ["A"]
        assert doc["Zone"] is zones


class TestValidateTrue:
    def test_is_the_default(self, doc: IDFDocument[Any]) -> None:
        with pytest.raises(ValidationFailedError):
            doc.zones.add("A", **{"ceiling_height": "tall"})
        assert "A" not in doc["Zone"]

    def test_explicit(self, doc: IDFDocument[Any]) -> None:
        with pytest.raises(ValidationFailedError):
            doc["Material"].add("XPS", validate=True, **{"thickness": 0.05})
        assert doc.zones.add("A", ceiling_height=3.0, validate=True).ceiling_height == 3.0


@pytest.mark.parametrize("value", ["no", 0, None])
def test_a_non_bool_is_refused(doc: IDFDocument[Any], value: object) -> None:
    with pytest.raises(TypeError, match="validate=True or validate=False"):
        doc.zones.add("A", **{"validate": value})
    assert "A" not in doc["Zone"]


def test_the_deprecated_object_form_takes_no_validate(doc: IDFDocument[Any]) -> None:
    other = new_document()
    zone = other.zones.add("A")
    with pytest.raises(TypeError, match="takes the object alone"):
        doc.zones.add(zone, **{"validate": False})  # pyright: ignore[reportCallIssue, reportArgumentType]


def _seeded_lines(text: str) -> set[int]:
    return {number for number, line in enumerate(text.splitlines(), 1) if "# pyright: ignore[" in line}


def test_mypy_reports_exactly_the_seeded_errors(tmp_path: Path) -> None:
    pytest.importorskip("mypy")
    result = subprocess.run(  # noqa: S603  (the interpreter running the tests, on a file of this repository)
        [
            sys.executable,
            "-m",
            "mypy",
            "--strict",
            "--no-error-summary",
            "--hide-error-context",
            "--cache-dir",
            str(tmp_path / "mypy_cache"),
            str(FIXTURE),
        ],
        capture_output=True,
        text=True,
        check=False,
    )
    errors = re.findall(rf"{re.escape(FIXTURE.name)}:(\d+): error: ", result.stdout)
    assert errors, result.stdout + result.stderr
    assert {int(n) for n in errors} == _seeded_lines(FIXTURE.read_text(encoding="utf-8")), result.stdout
