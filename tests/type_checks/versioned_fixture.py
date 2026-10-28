"""Type-check fixture for the per-version document types (never called; checked by ``make check``).

Field names are not checked by attribute access, as everywhere in idfkit (``IDFObject`` resolves
names at run time), so a renamed field is seeded through ``update``, whose keywords are typed.

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

from typing import Any, Literal

from typing_extensions import assert_type

from idfkit import IDFDocument, load_idf, save_idf
from idfkit.objects import IDFCollection, IDFObject
from idfkit.simulation import expand_objects
from idfkit.versioned import AnyIDFDocument, IDFDocumentV9_4, IDFDocumentV26_2, as_version


def raw_spelling(doc: IDFDocument[Any]) -> None:
    """The raw type name with ``_`` for ``:`` stays an untyped fallback on IDFDocument alone."""
    print(doc.Site_Location)


def people_count(doc: AnyIDFDocument) -> int:
    """Version-agnostic code: what every supported version has, typed as all of them declare it."""
    total = 0
    for people in doc["People"]:
        total += 1 if people.number_of_people_schedule_name else 0
    return total


def latest_only(doc: IDFDocument[Any]) -> None: ...


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
    # Through AnyIDFDocument, only what every version has.
    # A type some version lacks is a key that may be missing: reported, and still typed. Were the
    # result Unknown, strict mode would also report it here (reportUnknownVariableType), unignored.
    space = any_doc["Space"]  # pyright: ignore[reportTypedDictNotRequiredAccess]  (not in every version)
    print(space)
    print(any_doc.spaces)  # pyright: ignore[reportAttributeAccessIssue, reportUnknownMemberType, reportUnknownArgumentType]  (not in every version)
    any_doc["People"]["Office"].update(zone_or_zonelist_name="Office")  # pyright: ignore[reportCallIssue]  (renamed in 9.6)
    any_doc["WaterHeater:Mixed"]["Heater"].heater_fuel_type = "Plutonium"  # pyright: ignore[reportAttributeAccessIssue]  (no version)
