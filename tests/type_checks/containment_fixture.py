"""Type-check fixture for ``"Type" in doc`` and the mapping methods a document does not have (checked by ``make check``).

At run time ``"Space" in doc`` is true when the document holds at least one ``Space``. It is false
for an empty collection and for a release without the type, and ``doc["Space"]`` never raises. So
the test says nothing about which release a document is of, and a type checker must not narrow on
it. The document types used to be ``TypedDict`` subclasses, which pyright narrows on ``in`` by its
own rules. A positive test then retyped an ``AnyIDFDocument`` as the latest release. A negative test
on a type every release has marked its branch unreachable, so its body went unchecked. And pyright
offered ``get``, ``setdefault`` and ``pop``, which raise at run time.

Each seeded error carries a ``pyright: ignore`` naming the rule it must trigger, under
``reportUnnecessaryTypeIgnoreComment``, so an error that stops being reported fails the check. A
seeded error inside a ``not in`` branch proves the branch is checked: were it unreachable again, the
error would go unreported and its ignore would become unnecessary. ``reportUnreachable`` is on too.
"""

# pyright: strict, reportUnnecessaryTypeIgnoreComment=true, reportUnreachable=true

from __future__ import annotations

from typing import TYPE_CHECKING, Literal, TypeVar

from typing_extensions import assert_type

from idfkit import IDFDocument
from idfkit.document import IDFDocumentAllVersions
from idfkit.objects import IDFCollection, IDFObject
from idfkit.versioned import AnyIDFDocument, IDFDocumentV9_4, IDFDocumentV9_6, as_version

if TYPE_CHECKING:
    from idfkit.document import AnyZone, Zone

# ---------------------------------------------------------------------------
# A positive test does not retype the document (it used to become IDFDocument, the latest release)
# ---------------------------------------------------------------------------


def size_spaces(doc: AnyIDFDocument[Literal[True]]) -> None:
    if "Space" in doc:
        assert_type(doc, IDFDocumentAllVersions[Literal[True]])
        for space in doc["Space"]:  # pyright: ignore[reportCallIssue, reportArgumentType, reportUnknownVariableType]  (not every release has Space)
            space.ceiling_height = 3.0  # unknown, as the lookup failed
    else:
        assert_type(doc, IDFDocumentAllVersions[Literal[True]])


def output_files(doc: AnyIDFDocument) -> None:
    if "OutputControl:Files" in doc:  # 9.4 on
        assert_type(doc, IDFDocumentAllVersions[bool])


def early_return(doc: AnyIDFDocument) -> None:
    if "Space" not in doc:
        return
    assert_type(doc, IDFDocumentAllVersions[bool])


_D = TypeVar("_D", bound=AnyIDFDocument)


def bound_typevar(doc: _D) -> _D:
    if "Space" in doc:
        doc["Space"]  # pyright: ignore[reportCallIssue, reportArgumentType]  (still any release)
        return doc
    return doc


def aliased_condition(doc: AnyIDFDocument) -> None:
    has_space = "Space" in doc
    if has_space:
        assert_type(doc, IDFDocumentAllVersions[bool])


def removed_type(doc: AnyIDFDocument) -> None:
    """DistrictHeating left in 23.2; 8.9 to 23.1 documents reach this branch."""
    if "DistrictHeating" in doc:
        assert_type(doc, IDFDocumentAllVersions[bool])
        doc["DistrictHeating"]  # pyright: ignore[reportCallIssue, reportArgumentType]  (not every release has it)


# ---------------------------------------------------------------------------
# A negative test on a type every release has leaves its branch reachable, and checked
# ---------------------------------------------------------------------------


def first_zone_name(doc: AnyIDFDocument) -> str | None:
    if "Zone" not in doc:
        assert_type(doc, IDFDocumentAllVersions[bool])
        unchecked: int = "checked"  # pyright: ignore[reportAssignmentType]  (the branch is checked)
        print(unchecked)
        return None
    return doc["Zone"][0].name


def add_sqlite_output(doc: IDFDocument) -> None:
    if "Output:SQLite" not in doc:
        assert_type(doc, IDFDocument[bool])
        doc.add("Output:SQLite", option_type="SimpleAndTabular")
        doc["Output:SQLite"][0].option_type = "Bogus"  # pyright: ignore[reportAttributeAccessIssue]  (the branch is checked)


def legacy_zone(doc: IDFDocumentV9_4) -> None:
    if "Zone" not in doc:
        assert_type(doc, IDFDocumentV9_4[bool])
        doc["Space"]  # pyright: ignore[reportCallIssue, reportArgumentType]  (the branch is checked; no Space in 9.4)


# ---------------------------------------------------------------------------
# A test on a union of releases leaves the union whole in both branches
# ---------------------------------------------------------------------------


def people_zone(doc: AnyIDFDocument) -> None:
    d = as_version(doc, (IDFDocumentV9_4, IDFDocumentV9_6, IDFDocument))
    if "Space" in d:
        assert_type(d, IDFDocumentV9_4[bool] | IDFDocumentV9_6[bool] | IDFDocument[bool])
    else:
        # A 9.6 or 26.2 document with no Space lands here as well as a 9.4 one: the 9.4 name is not
        # every member's.
        assert_type(d, IDFDocumentV9_4[bool] | IDFDocumentV9_6[bool] | IDFDocument[bool])
        for people in d["People"]:
            people.update(zone_or_zonelist_name="Office")  # pyright: ignore[reportCallIssue]  (renamed in 9.6)


# ---------------------------------------------------------------------------
# Mapping methods a document does not have at run time are not offered
# ---------------------------------------------------------------------------


def mapping_methods(doc: AnyIDFDocument, latest: IDFDocument, legacy: IDFDocumentV9_4) -> None:
    doc.get("Space")  # pyright: ignore[reportAttributeAccessIssue, reportUnknownMemberType]  (no get)
    doc.setdefault("Zone", latest["Zone"])  # pyright: ignore[reportAttributeAccessIssue, reportUnknownMemberType]
    doc.pop("Zone")  # pyright: ignore[reportAttributeAccessIssue, reportUnknownMemberType]
    doc.popitem()  # pyright: ignore[reportAttributeAccessIssue, reportUnknownMemberType]
    doc.clear()  # pyright: ignore[reportAttributeAccessIssue, reportUnknownMemberType]
    legacy.get("Zone")  # pyright: ignore[reportAttributeAccessIssue, reportUnknownMemberType]
    latest.get("Space")  # pyright: ignore[reportAttributeAccessIssue, reportUnknownMemberType]  (no get)
    print(doc | {})  # pyright: ignore[reportOperatorIssue, reportUnknownArgumentType]  (no |)
    del latest["Zone"]  # pyright: ignore[reportIndexIssue]  (no __delitem__)
    match doc:
        case {"Zone": zones}:  # pyright: ignore[reportUnnecessaryComparison]  (not a Mapping: never matches)
            print(zones)  # pyright: ignore[reportUnreachable]  (as at run time)
        case _:
            pass


def methods_it_has(doc: AnyIDFDocument, latest: IDFDocument) -> None:
    # update() is the eppy batch update, not a dict's.
    latest.update({"Zone.Office.x_origin": 1.0})
    doc.update({"Zone.Office.x_origin": 1.0})
    assert_type(doc.copy(), IDFDocumentAllVersions[bool])
    assert_type(latest.copy(), IDFDocument[bool])
    assert_type(doc.keys(), list[str])
    assert_type("Zone" in doc, bool)


# ---------------------------------------------------------------------------
# Indexing: a literal it lacks is an error at the subscript; a name known only at run time uses
# get_collection
# ---------------------------------------------------------------------------


def dynamic_names(doc: AnyIDFDocument, latest: IDFDocument, obj_type: str) -> None:
    assert_type(doc.get_collection(obj_type), IDFCollection[IDFObject])
    assert_type(latest.get_collection(obj_type), IDFCollection[IDFObject])
    latest[obj_type]  # pyright: ignore[reportCallIssue, reportArgumentType]  (not a literal: use get_collection)
    latest["Zoen"]  # pyright: ignore[reportCallIssue, reportArgumentType]  (a typo)
    assert_type(latest["Zone"], IDFCollection[Zone])
    assert_type(doc["Zone"], IDFCollection[AnyZone])
