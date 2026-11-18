"""Type-check fixture for ``IDFCollection.add`` (never called; checked by ``make check``).

``add`` takes its parameters from the creation signature of the class the collection is typed
with, so ``doc["Zone"].add(...)`` accepts exactly the latest release's ``Zone`` fields and value
types and returns a ``Zone``; through ``IDFDocumentV9_4`` the fields are 9.4's, through
``AnyIDFDocument`` only those every release accepts, and through an untyped
``IDFCollection[IDFObject]`` anything, as ``IDFDocument.add`` does. Required fields and defaults
are checked by ``add_signature_fixture.py``.

Each seeded error below carries a ``pyright: ignore`` naming the rule it must trigger, and this file
turns on ``reportUnnecessaryTypeIgnoreComment``: if a seeded error stops being reported, the ignore
becomes unnecessary and the check fails, so the fixture proves the errors are caught.
"""

# pyright: strict, reportUnnecessaryTypeIgnoreComment=true

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from typing_extensions import assert_type

from idfkit import IDFDocument
from idfkit.objects import IDFCollection, IDFObject
from idfkit.versioned import AnyIDFDocument, IDFDocumentV9_4

if TYPE_CHECKING:
    from idfkit.document import AnyPeople, AnyZone, BuildingSurfaceDetailed, OutputSQLite, People, Zone
    from idfkit.versioned import People_v8_9_to_v9_4


def latest(doc: IDFDocument[Any]) -> None:
    assert_type(doc["Zone"].add("Office", ceiling_height=3.0, multiplier=2), Zone)
    assert_type(doc.zones.add("Lab", zone_inside_convection_algorithm="TARP"), Zone)
    assert_type(doc["Output:SQLite"].add(option_type="SimpleAndTabular"), OutputSQLite)
    surface = doc["BuildingSurface:Detailed"].add(
        "Floor",
        surface_type="Floor",
        zone_name="Office",
        outside_boundary_condition="Ground",
        vertices=[{"vertex_x_coordinate": 0.0, "vertex_y_coordinate": 0.0, "vertex_z_coordinate": 0.0}],
    )
    assert_type(surface, BuildingSurfaceDetailed)
    people = doc["People"].add(
        "Staff",
        zone_or_zonelist_or_space_or_spacelist_name="Office",
        number_of_people_schedule_name="Occ",
        activity_level_schedule_name="Act",
    )
    assert_type(people, People)


def release_specific(doc: IDFDocumentV9_4) -> None:
    people = doc["People"].add(
        "Staff",
        zone_or_zonelist_name="Office",
        number_of_people_schedule_name="Occ",
        activity_level_schedule_name="Act",
    )
    assert_type(people, People_v8_9_to_v9_4)
    doc["People"].add(
        "Staff",
        zone_or_zonelist_or_space_or_spacelist_name="Office",  # pyright: ignore[reportCallIssue]  (9.6's name)
        number_of_people_schedule_name="Occ",
        activity_level_schedule_name="Act",
    )


def any_release(doc: AnyIDFDocument) -> None:
    assert_type(doc["Zone"].add("Office", ceiling_height=3.0), AnyZone)
    for heater in doc["WaterHeater:Mixed"]:
        print(heater.name)
    doc["WaterHeater:Mixed"].add(
        "Heater",
        heater_fuel_type="NaturalGas",
        setpoint_temperature_schedule_name="Set",
        heater_thermal_efficiency=0.9,
        ambient_temperature_indicator="Schedule",
    )
    doc["WaterHeater:Mixed"].add(
        "Heater",
        heater_fuel_type="Steam",  # pyright: ignore[reportArgumentType]  (23.2 on reject it)
        setpoint_temperature_schedule_name="Set",
        heater_thermal_efficiency=0.9,
        ambient_temperature_indicator="Schedule",
    )
    assert_type(doc["People"], IDFCollection[AnyPeople])
    # Every release requires People's zone, which 9.6 renamed: no add() suits them all.
    doc["People"].add(  # pyright: ignore[reportCallIssue]  (narrow_with_as_version_first)
        "Staff", number_of_people_schedule_name="Occ", activity_level_schedule_name="Act"
    )
    doc["People"].add(
        "Staff",
        zone_or_zonelist_name="Office",  # pyright: ignore[reportCallIssue]  (9.6 renamed it)
        number_of_people_schedule_name="Occ",
        activity_level_schedule_name="Act",
    )


def untyped(doc: IDFDocument[Any], obj_type: str) -> None:
    assert_type(doc.get_collection(obj_type).add("Anything", whatever=1), IDFObject)


def seeded_errors(doc: IDFDocument[Any]) -> None:
    doc["Zone"].add("Office", ceiling_hieght=3.0)  # pyright: ignore[reportCallIssue]  (typo in a field name)
    doc["Zone"].add("Office", zone_inside_convection_algorithm="Tarp")  # pyright: ignore[reportArgumentType]  (not a choice)
    doc["Zone"].add("Office", multiplier="2")  # pyright: ignore[reportArgumentType]  (wrong value type)
    doc["Zone"].add("Office", 2)  # pyright: ignore[reportCallIssue]  (a field passed positionally)
    doc["Zone"].add(name="Office")  # pyright: ignore[reportCallIssue]  (the name is positional-only)
    doc["Zone"].add(doc["Zone"]["Office"])  # pyright: ignore[reportArgumentType]  (the object form, deprecated)
