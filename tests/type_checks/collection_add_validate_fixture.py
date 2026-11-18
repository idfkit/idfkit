"""Type-check fixture for ``validate=`` on ``IDFCollection.add`` (never called; checked by ``make check``).

``add`` takes the switch ``IDFDocument.add`` takes, keyword-only, after the object type's fields:
``doc["Zone"].add("A", validate=False)`` creates the object without validating its values. Every
generated creation signature declares it, so it is accepted through ``IDFDocument`` and through
``AnyIDFDocument``, by subscript and by attribute, and only as a ``bool``. It turns off no other
check of the type checker's: a misspelled field is still an error.

pyright checks this file under ``make check``; mypy checks it in ``tests/test_collection_add_validate.py``,
which requires mypy to report an error on exactly the lines carrying a ``pyright: ignore`` below.

Each seeded error below carries a ``pyright: ignore`` naming the rule it must trigger, and this file
turns on ``reportUnnecessaryTypeIgnoreComment``: if a seeded error stops being reported, the ignore
becomes unnecessary and the check fails, so the fixture proves the errors are caught.
"""

# pyright: strict, reportUnnecessaryTypeIgnoreComment=true

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from typing_extensions import assert_type

from idfkit import IDFDocument
from idfkit.versioned import AnyIDFDocument

if TYPE_CHECKING:
    from idfkit.document import AnyZone, Zone


def latest(doc: IDFDocument[Any]) -> None:
    assert_type(doc["Zone"].add("A", validate=False), Zone)
    assert_type(doc["Zone"].add("A", validate=True), Zone)
    assert_type(doc.zones.add("A", validate=False), Zone)
    assert_type(doc.zones.add("A", ceiling_height=3.0, validate=True), Zone)
    flag: bool = False
    assert_type(doc.zones.add("A", validate=flag), Zone)


def any_release(doc: AnyIDFDocument) -> None:
    assert_type(doc["Zone"].add("A", validate=False), AnyZone)
    assert_type(doc["Zone"].add("A", validate=True), AnyZone)
    assert_type(doc.zones.add("A", validate=False), AnyZone)
    assert_type(doc.zones.add("A", multiplier=2, validate=True), AnyZone)


def nameless_type(doc: IDFDocument[Any]) -> None:
    # A type without a Name field takes the switch too, after its fields.
    doc["Output:SQLite"].add(option_type="SimpleAndTabular", validate=False)
    doc["Output:SQLite"].add(validate=False)


def errors(doc: IDFDocument[Any], any_doc: AnyIDFDocument) -> None:
    doc["Zone"].add("A", validate="no")  # pyright: ignore[reportArgumentType]  (not a bool)
    doc.zones.add("A", validate=0)  # pyright: ignore[reportArgumentType]  (not a bool)
    any_doc.zones.add("A", validate=None)  # pyright: ignore[reportArgumentType]  (not a bool)
    doc["Zone"].add("A", ceiling_hieght=3.0, validate=False)  # pyright: ignore[reportCallIssue]  (misspelled field)
    any_doc["Zone"].add("A", ceiling_hieght=3.0, validate=False)  # pyright: ignore[reportCallIssue]  (misspelled field)
    # validate=False relaxes no required field: Material's roughness, thickness, ... are still required.
    doc.materials.add("XPS", validate=False)  # pyright: ignore[reportCallIssue]  (required fields left out)
