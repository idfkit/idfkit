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

from idfkit import IDFDocument, load_idf, save_idf
from idfkit.objects import IDFCollection, IDFObject
from idfkit.simulation import expand_objects
from idfkit.versioned import (
    AnyIDFDocument,
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


def vertex_count(surface: AnyBuildingSurfaceDetailed) -> int:
    """The vertices group, though 8.9 lists its fields in another order."""
    return sum(1 for vertex in surface.vertices if vertex.vertex_x_coordinate is not None)


def zone_list_size(zone_list: AnyZoneList) -> int:
    """A type every release declares alike: AnyZoneList is ZoneList."""
    return len(zone_list.zones)


def any_release_objects(
    latest: IDFDocument, oldest: IDFDocumentV8_9, legacy: IDFDocumentV9_4, any_doc: AnyIDFDocument
) -> None:
    for doc in (latest, oldest, legacy):
        zone_height(doc["Zone"]["Office"])
        vertex_count(doc["BuildingSurface:Detailed"]["Wall"])
        zone_list_size(doc["ZoneList"]["All"])
    for zone in any_doc.zones:
        zone_height(zone)
    for table in any_doc["Output:Table:Annual"]:
        for detail in table.variable_details:
            detail.digits_after_decimal = 2  # an int: every release accepts it


def dict_like_methods(latest: IDFDocument, legacy: IDFDocumentV9_4, any_doc: AnyIDFDocument) -> None:
    """keys(), values() and items() are the document's own, not the TypedDict's behind its lookups."""
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


def write_safe_fuel(doc: AnyIDFDocument) -> None:
    heater = doc["WaterHeater:Mixed"]["Heater"]
    fuel = heater.heater_fuel_type  # whatever the document's version holds, DistrictHeating included
    print(fuel)
    heater.heater_fuel_type = "NaturalGas"  # every version accepts it
    heater.update(heater_fuel_type="Electricity")
    heater.heater_fuel_type = None


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
    # ... and a latest-release document, typed as before.
    model = load_idf("model.idf")
    assert_type(model, IDFDocument[Literal[True]])
    model["People"]["Office"].zone_or_zonelist_or_space_or_spacelist_name = "Office"
    people_count(model)
    assert_type(as_version(model, IDFDocumentV26_2), IDFDocument[bool])
    # A typed collection is a collection of IDFObject.
    objects: IDFCollection[IDFObject] = model["Zone"]
    print(objects)


def seeded_errors(legacy: IDFDocumentV9_4, any_doc: AnyIDFDocument) -> None:
    legacy["Space"]  # pyright: ignore[reportGeneralTypeIssues]  (Space is new in 9.6)
    people = legacy["People"]["Office"]
    people.update(zone_or_zonelist_or_space_or_spacelist_name="Office")  # pyright: ignore[reportCallIssue]  (the 9.6 name)
    heater = legacy["WaterHeater:Mixed"]["Heater"]
    heater.heater_fuel_type = "DistrictHeatingWater"  # pyright: ignore[reportAttributeAccessIssue]  (a later choice)
    heater.update(heater_fuel_type="DistrictHeatingWater")  # pyright: ignore[reportArgumentType]  (a later choice)
    latest_only(legacy)  # pyright: ignore[reportArgumentType]  (a 9.4 document is not a latest one)
    print(legacy.spaces)  # pyright: ignore[reportAttributeAccessIssue, reportUnknownMemberType, reportUnknownArgumentType]  (no Space before 9.6)
    # Through AnyIDFDocument, only what every version has: a type some version lacks is not a key.
    print(any_doc["Space"])  # pyright: ignore[reportGeneralTypeIssues, reportUnknownArgumentType]  (not in every version)
    print(any_doc.spaces)  # pyright: ignore[reportAttributeAccessIssue, reportUnknownMemberType, reportUnknownArgumentType]  (not in every version)
    any_doc["People"]["Office"].update(zone_or_zonelist_name="Office")  # pyright: ignore[reportCallIssue]  (renamed in 9.6)
    any_doc["WaterHeater:Mixed"]["Heater"].heater_fuel_type = "Plutonium"  # pyright: ignore[reportAttributeAccessIssue]  (no version)
    # Writing takes only what every version accepts: 9.3 to 23.1 reject DistrictHeatingWater, 23.2 on reject Steam.
    any_doc["WaterHeater:Mixed"]["Heater"].heater_fuel_type = "DistrictHeatingWater"  # pyright: ignore[reportAttributeAccessIssue]  (not before 23.2)
    any_doc["WaterHeater:Mixed"]["Heater"].update(heater_fuel_type="Steam")  # pyright: ignore[reportArgumentType]  (not from 23.2)
    zone_height(legacy["Material"]["Brick"])  # pyright: ignore[reportArgumentType]  (not a zone)
    table: AnyOutputTableAnnual = any_doc["Output:Table:Annual"]["Annual"]
    table.variable_details[0].digits_after_decimal = 2.5  # pyright: ignore[reportAttributeAccessIssue]  (an int from 22.2 on)
    as_version(any_doc, _Since9_6)  # pyright: ignore[reportCallIssue, reportArgumentType]  (an alias is not a class; pass a tuple)
    any_doc["Zone"]["Office"].update(x_orign=1.0)  # pyright: ignore[reportCallIssue]  (a typo, also through AnyIDFDocument)
