"""Type-check fixture for the per-version document types (never called; checked by ``make check``).

A renamed field is seeded through ``update``, whose keywords are typed for each release.

Each seeded error below carries a ``pyright: ignore`` naming the rule it must trigger, and this file
turns on ``reportUnnecessaryTypeIgnoreComment``. If a seeded error stops being reported, the ignore
becomes unnecessary and the check fails, so the fixture proves the errors are caught rather than
merely tolerating them.

The examples are real differences between EnergyPlus 9.4 and the latest release: ``People`` renamed
``zone_or_zonelist_name`` to ``zone_or_zonelist_or_space_or_spacelist_name`` when spaces arrived in
9.6, ``Space`` itself is new in 9.6, and the water heater fuel ``DistrictHeating`` became
``DistrictHeatingWater`` and ``DistrictHeatingSteam``.
"""

# pyright: strict, reportUnnecessaryTypeIgnoreComment=true

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Literal, TypeAlias

from typing_extensions import assert_type

from idfkit import IDFDocument, load_idf, new_document, save_idf
from idfkit.migration import MigrationReport, async_migrate, migrate
from idfkit.objects import IDFCollection, IDFObject
from idfkit.simulation import expand_objects
from idfkit.versioned import (
    AnyIDFDocument,
    IDFDocumentBefore9_6,
    IDFDocumentSince9_6,
    IDFDocumentSince26_1,
    IDFDocumentV8_9,
    IDFDocumentV9_4,
    IDFDocumentV9_6,
    IDFDocumentV26_1,
    IDFDocumentV26_2,
    as_version,
)

if TYPE_CHECKING:
    from idfkit.document import AnyBuildingSurfaceDetailed, AnyOutputTableAnnual, AnySpace, AnyZone, AnyZoneList


def raw_spelling(doc: IDFDocument[Any]) -> None:
    """The raw type name with ``_`` for ``:`` stays an untyped fallback on IDFDocument alone."""
    print(doc.Site_Location)


def people_count(doc: AnyIDFDocument) -> int:
    """Version-agnostic code: what every supported version has, typed as all of them declare it."""
    total = 0
    for people in doc["People"]:
        total += 1 if people.number_of_people_schedule_name else 0
    # An accessor returning a private shared base is typed, not partially Unknown (strict mode).
    for zone in doc.zones:
        print(zone.name)
    for material in doc.materials:
        print(material.thickness)
    return total


def latest_only(doc: IDFDocument[Any]) -> None: ...


def zone_height(zone: AnyZone) -> float | None:
    """A helper for a zone of any release: the latest one, an older one, or one from AnyIDFDocument."""
    height = zone.ceiling_height
    return height if isinstance(height, float) else None


def top_height(surface: AnyBuildingSurfaceDetailed) -> float:
    """The vertices group, though 8.9 lists its fields in another order; every release requires them."""
    return max(vertex.vertex_z_coordinate for vertex in surface.vertices)


def zone_list_size(zone_list: AnyZoneList) -> int:
    """A type every release declares alike: AnyZoneList is ZoneList."""
    return len(zone_list.zones)


def any_release_objects(
    latest: IDFDocument, oldest: IDFDocumentV8_9, legacy: IDFDocumentV9_4, any_doc: AnyIDFDocument
) -> None:
    for doc in (latest, oldest, legacy):
        zone_height(doc["Zone"]["Office"])
        top_height(doc["BuildingSurface:Detailed"]["Wall"])
        zone_list_size(doc["ZoneList"]["All"])
    for zone in any_doc.zones:
        zone_height(zone)
    for table in any_doc["Output:Table:Annual"]:
        for detail in table.variable_details:
            detail.digits_after_decimal = 2  # an int: every release accepts it


def dict_like_methods(latest: IDFDocument, legacy: IDFDocumentV9_4, any_doc: AnyIDFDocument) -> None:
    """keys(), values() and items() are the document's own."""
    assert_type(latest.keys(), list[str])
    assert_type(latest.values(), list[IDFCollection[IDFObject]])
    assert_type(latest.items(), list[tuple[str, IDFCollection[IDFObject]]])
    assert_type(legacy.values(), list[IDFCollection[IDFObject]])
    assert_type(any_doc.values(), list[IDFCollection[IDFObject]])
    for collection in any_doc.values():
        print(collection.obj_type)


_Since9_6: TypeAlias = IDFDocumentV9_6 | IDFDocumentV26_1 | IDFDocument


def classify_space(space: AnySpace) -> None:
    """A Space of any release that has one (9.6 on)."""
    space.space_type = "Office"


def classify_spaces(doc: AnyIDFDocument) -> int:
    """Narrow a model of any release into the releases that have Space, with one as_version call."""
    if doc.version < (9, 6, 0):
        return 0
    recent = as_version(doc, (IDFDocumentV9_6, IDFDocumentV26_1, IDFDocument))
    assert_type(recent, IDFDocumentV9_6[bool] | IDFDocumentV26_1[bool] | IDFDocument[bool])
    inline = as_version(doc, IDFDocumentV9_6 | IDFDocument)  # pyright reads A | B as type[A] | type[B]
    assert_type(inline, IDFDocumentV9_6[bool] | IDFDocument[bool])
    for space in recent["Space"]:
        classify_space(space)
    return len(recent["Space"])


def narrow_by_range(doc: AnyIDFDocument, first: str, until: str | None) -> None:
    """since= and before= type a document as the union of the supported releases in the range."""
    assert_type(as_version(doc, since="26.1"), IDFDocumentSince26_1)
    assert_type(as_version(doc, since=IDFDocumentV26_1), IDFDocumentV26_1[bool] | IDFDocument[bool])
    assert_type(as_version(doc, since="26.1.0"), IDFDocumentSince26_1)
    assert_type(as_version(doc, since=IDFDocumentV26_2), IDFDocument[bool])
    assert_type(as_version(doc, before="9.0"), IDFDocumentV8_9[bool])
    assert_type(as_version(doc, since=IDFDocumentV9_6, before="22.1"), IDFDocumentV9_6[bool])
    # A bound the checker cannot read as one release types the document as any release's.
    assert_type(as_version(doc, since=first), AnyIDFDocument)
    assert_type(as_version(doc, since="9.6", before=until), AnyIDFDocument)
    assert_type(as_version(doc, before=until), AnyIDFDocument)
    assert_type(as_version(doc, since=(9, 6, 0)), AnyIDFDocument)
    assert_type(as_version(doc, since=doc.version), AnyIDFDocument)
    assert_type(as_version(doc, since="27.1"), AnyIDFDocument)  # no such release: ValueError when run
    assert_type(as_version(doc, since="26.1", before="9.6"), AnyIDFDocument)  # empty: ValueError when run
    # A renamed field: each branch narrowed to the releases that use one name.
    if doc.version < (9, 6, 0):
        before: IDFDocumentBefore9_6 = as_version(doc, before="9.6")
        before["People"]["Office"].update(zone_or_zonelist_name="Office")
    else:
        since: IDFDocumentSince9_6 = as_version(doc, since="9.6")
        since["People"]["Office"].update(zone_or_zonelist_or_space_or_spacelist_name="Office")


def write_safe_fuel(doc: AnyIDFDocument) -> None:
    heater = doc["WaterHeater:Mixed"]["Heater"]
    fuel = heater.heater_fuel_type  # whatever the document's version holds, DistrictHeating included
    print(fuel)
    heater.heater_fuel_type = "NaturalGas"  # every version accepts it
    heater.update(heater_fuel_type="Electricity")
    heater.heater_fuel_type = None  # pyright: ignore[reportAttributeAccessIssue]  (every release requires it: not cleared)


def correct_calls() -> None:
    legacy = as_version(load_idf("legacy.idf"), IDFDocumentV9_4)
    assert_type(legacy, IDFDocumentV9_4)
    people = legacy["People"]["Office"]
    people.zone_or_zonelist_name = "Office"
    legacy["WaterHeater:Mixed"]["Heater"].heater_fuel_type = "DistrictHeating"
    legacy["WaterHeater:Mixed"]["Heater"].update(heater_fuel_type="DistrictHeating")
    assert_type(legacy.copy(), IDFDocumentV9_4)
    assert_type(expand_objects(legacy), IDFDocumentV9_4)
    # Library functions and version-agnostic code accept a document of any version ...
    save_idf(legacy, "legacy.idf")
    people_count(legacy)
    # Through AnyIDFDocument a field whose choices changed reads as any version's value and accepts
    # a value every version accepts.
    write_safe_fuel(legacy)
    # ... and a latest-release document, typed once its release is stated.
    model = load_idf("model.idf", as_type=IDFDocumentV26_2)
    assert_type(model, IDFDocument)
    model["People"]["Office"].zone_or_zonelist_or_space_or_spacelist_name = "Office"
    people_count(model)
    assert_type(as_version(model, IDFDocumentV26_2), IDFDocument[bool])
    # A typed collection is a collection of IDFObject.
    objects: IDFCollection[IDFObject] = model["Zone"]
    print(objects)


def new_documents(any_version: Any, versions: list[tuple[int, int, int]]) -> None:
    """A document created for a release, typed for it: the release is named once, by the type."""
    assert_type(new_document(IDFDocumentV9_4), IDFDocumentV9_4)
    # The strictness is stated by the type, and kept: a per-release annotation checks it.
    strict_94: IDFDocumentV9_4[Literal[True]] = new_document(IDFDocumentV9_4[Literal[True]])
    lax_94: IDFDocumentV9_4[Literal[False]] = new_document(IDFDocumentV9_4[Literal[False]])
    print(strict_94, lax_94)
    # The tuple form is unchanged, an untyped version included, and so is new_document as a callable.
    assert_type(new_document(), IDFDocument[Literal[True]])
    assert_type(new_document(version=(9, 4, 0)), IDFDocument[Literal[True]])
    assert_type(new_document((9, 4, 0), strict=False), IDFDocument[Literal[False]])
    assert_type(new_document(any_version), IDFDocument[Literal[True]])
    assert_type(new_document(any_version, strict=False), IDFDocument[Literal[False]])
    assert_type(list(map(new_document, versions)), list[IDFDocument[Literal[True]]])


async def migrated_documents(old: IDFDocumentV8_9) -> None:
    """A migration names its target's document type to get a report typed for that release."""
    report = migrate(old, IDFDocumentV9_4)
    assert_type(report, MigrationReport[IDFDocumentV9_4])
    assert_type(report.migrated_model, IDFDocumentV9_4 | None)
    assert_type((await async_migrate(old, target_version=IDFDocumentV9_4)).migrated_model, IDFDocumentV9_4 | None)
    if report.migrated_model is not None:
        report.migrated_model["People"]["Office"].zone_or_zonelist_name = "Office"
    assert_type(migrate(old, IDFDocument).migrated_model, IDFDocument | None)
    # A version a type checker cannot know gives a document of any release, as strict as the source.
    assert_type(migrate(old, (24, 1, 0)).migrated_model, AnyIDFDocument[bool] | None)
    assert_type((await async_migrate(old, "24.1.0")).migrated_model, AnyIDFDocument[bool] | None)
    loaded = load_idf("old.idf")
    assert_type(migrate(loaded, "24.1.0").migrated_model, AnyIDFDocument[Literal[True]] | None)
    # A bare MigrationReport accepts a report of any release.
    reports: list[MigrationReport] = [report, migrate(old, "24.1.0")]
    print(reports)


def seeded_errors(legacy: IDFDocumentV9_4, any_doc: AnyIDFDocument) -> None:
    legacy["Space"]  # pyright: ignore[reportCallIssue, reportArgumentType]  (Space is new in 9.6)
    people = legacy["People"]["Office"]
    people.update(zone_or_zonelist_or_space_or_spacelist_name="Office")  # pyright: ignore[reportCallIssue]  (the 9.6 name)
    heater = legacy["WaterHeater:Mixed"]["Heater"]
    heater.heater_fuel_type = "DistrictHeatingWater"  # pyright: ignore[reportAttributeAccessIssue]  (a later choice)
    heater.update(heater_fuel_type="DistrictHeatingWater")  # pyright: ignore[reportArgumentType]  (a later choice)
    latest_only(legacy)  # pyright: ignore[reportArgumentType]  (a 9.4 document is not a latest one)
    print(legacy.spaces)  # pyright: ignore[reportAttributeAccessIssue, reportUnknownMemberType, reportUnknownArgumentType]  (no Space before 9.6)
    # Through AnyIDFDocument, only what every version has: a type some version lacks is not a key.
    print(any_doc["Space"])  # pyright: ignore[reportCallIssue, reportArgumentType, reportUnknownArgumentType]  (not in every version)
    print(any_doc.spaces)  # pyright: ignore[reportAttributeAccessIssue, reportUnknownMemberType, reportUnknownArgumentType]  (not in every version)
    any_doc["People"]["Office"].update(zone_or_zonelist_name="Office")  # pyright: ignore[reportCallIssue]  (renamed in 9.6)
    any_doc["WaterHeater:Mixed"]["Heater"].heater_fuel_type = "Plutonium"  # pyright: ignore[reportAttributeAccessIssue]  (no version)
    # Writing takes only what every version accepts: 9.3 to 23.1 reject DistrictHeatingWater, 23.2 on reject Steam.
    any_doc["WaterHeater:Mixed"]["Heater"].heater_fuel_type = "DistrictHeatingWater"  # pyright: ignore[reportAttributeAccessIssue]  (not before 23.2)
    any_doc["WaterHeater:Mixed"]["Heater"].update(heater_fuel_type="Steam")  # pyright: ignore[reportArgumentType]  (not from 23.2)
    zone_height(legacy["Material"]["Brick"])  # pyright: ignore[reportArgumentType]  (not a zone)
    table: AnyOutputTableAnnual = any_doc["Output:Table:Annual"]["Annual"]
    table.variable_details[0].digits_after_decimal = 2.5  # pyright: ignore[reportAttributeAccessIssue]  (an int from 22.2 on)
    as_version(any_doc, _Since9_6)  # pyright: ignore[reportCallIssue, reportArgumentType]  (an alias is no class)
    as_version(any_doc)  # pyright: ignore[reportCallIssue]  (a type or a range is needed)
    as_version(any_doc, since=1.5)  # pyright: ignore[reportCallIssue, reportArgumentType]  (not a release)
    as_version(any_doc, IDFDocument, since="9.6")  # pyright: ignore[reportCallIssue]  (a type or a range, not both)
    as_version(any_doc, before="9.6")["Space"]  # pyright: ignore[reportCallIssue, reportArgumentType]  (Space is new in 9.6)
    any_doc["Zone"]["Office"].update(x_orign=1.0)  # pyright: ignore[reportCallIssue]  (a typo, also through AnyIDFDocument)
    new_document(dict)  # pyright: ignore[reportArgumentType, reportCallIssue]  (not a document type)
    new_document(IDFDocumentV9_4, strict=False)  # pyright: ignore[reportArgumentType, reportCallIssue]  (the type states it: [Literal[False]])
    lax: IDFDocumentV9_4[Literal[False]] = new_document(IDFDocumentV9_4)  # pyright: ignore[reportAssignmentType]  (strict)
    print(lax)
    migrated = migrate(legacy, (24, 1, 0)).migrated_model
    assert migrated is not None
    latest_only(migrated)  # pyright: ignore[reportArgumentType]  (a version tuple names no release a checker knows)
    migrate(legacy, IDFDocumentV9_6).migrated_model["Space"]  # pyright: ignore[reportOptionalSubscript]  (None on a no-op)
    # A migration reaches one release: AnyIDFDocument and a union of release types name none.
    migrate(legacy, AnyIDFDocument)  # pyright: ignore[reportCallIssue, reportArgumentType]  (no single release)
    # A union of release types also names no single release, and raises TypeError at run time. mypy
    # rejects it; pyright tries each member against the overloads and types it as either report.
    assert_type(
        migrate(legacy, IDFDocumentV9_6 | IDFDocument),
        MigrationReport[IDFDocumentV9_6] | MigrationReport[IDFDocument],
    )
