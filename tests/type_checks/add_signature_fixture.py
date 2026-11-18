"""Type-check fixture for the creation signature of ``IDFCollection.add`` (never called; checked by ``make check``).

``add`` takes the parameters of the collection's class's creation signature, generated from the
schema: the name first, positional-only, for a type with a Name field (required when the schema
requires one) and none for a type without; then the fields the schema requires, with no default and
not ``None``; then the other fields with their schema defaults. So leaving out a required field is a
type error, as it is a ``ValidationFailedError`` at run time (``tests/test_add_signature.py`` checks
the two agree). The required fields are the release's: through ``IDFDocumentV9_4`` 9.4's, through
``AnyIDFDocument`` only those every release requires, and through an untyped collection none.

Each seeded error below carries a ``pyright: ignore`` naming the rule it must trigger, and this file
turns on ``reportUnnecessaryTypeIgnoreComment``: if a seeded error stops being reported, the ignore
becomes unnecessary and the check fails, so the fixture proves the errors are caught.
"""

# pyright: strict, reportUnnecessaryTypeIgnoreComment=true

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from typing_extensions import assert_type

from idfkit import IDFDocument
from idfkit.objects import IDFObject
from idfkit.versioned import AnyIDFDocument, IDFDocumentV9_4

if TYPE_CHECKING:
    from idfkit.document import Building, InternalMass, Material, Zone
    from idfkit.versioned import InternalMass_v9_2_to_v9_5


def required_fields(doc: IDFDocument[Any]) -> None:
    xps = doc.materials.add(
        "XPS", roughness="MediumSmooth", thickness=0.05, conductivity=0.034, density=35.0, specific_heat=1400.0
    )
    assert_type(xps, Material)
    doc.materials.add("XPS", thickness=0.05, conductivity=0.034, density=35.0, specific_heat=1400.0)  # pyright: ignore[reportCallIssue]  (roughness is required)
    doc.materials.add("XPS")  # pyright: ignore[reportCallIssue]  (five required fields missing)
    doc.materials.add(
        "XPS",
        roughness=None,  # pyright: ignore[reportArgumentType]  (a required field takes a value, not None)
        thickness=0.05,
        conductivity=0.034,
        density=35.0,
        specific_heat=1400.0,
    )


def defaults(doc: IDFDocument[Any]) -> None:
    # An optional field takes its default, any other value of its type, or None (left empty).
    doc.materials.add(
        "XPS",
        roughness="MediumSmooth",
        thickness=0.05,
        conductivity=0.034,
        density=35.0,
        specific_heat=1400.0,
        thermal_absorptance=0.9,
        solar_absorptance=None,
        visible_absorptance=0.5,
    )
    # Zone requires no field: every one has a default or may be left empty.
    assert_type(doc.zones.add("Office", multiplier=1, ceiling_height="Autocalculate"), Zone)


def names(doc: IDFDocument[Any]) -> None:
    doc.zones.add()  # pyright: ignore[reportCallIssue]  (Zone requires a name)
    assert_type(doc["Building"].add(), Building)  # the schema does not require Building's name
    doc["Output:SQLite"].add("Out", option_type="Simple")  # pyright: ignore[reportCallIssue]  (no Name field)
    doc["Timestep"].add(number_of_timesteps_per_hour=6)


def release_specific(latest: IDFDocument[Any], old: IDFDocumentV9_4) -> None:
    # 9.2 to 24.1 require InternalMass's zone; 26.2 requires only the surface area.
    assert_type(latest["InternalMass"].add("Mass", surface_area=10.0), InternalMass)
    old["InternalMass"].add("Mass", construction_name="Wall", surface_area=10.0)  # pyright: ignore[reportCallIssue]  (9.4 requires the zone)
    old["InternalMass"].add("Mass", construction_name="Wall", zone_or_zonelist_name="Office", surface_area=10.0)
    # 26.2 requires a CO2 setpoint schedule, which no earlier release does.
    latest["ZoneControl:ContaminantController"].add("CO2", zone_name="Office")  # pyright: ignore[reportCallIssue]  (26.2 requires the schedule)
    old["ZoneControl:ContaminantController"].add("CO2", zone_name="Office")


def any_release(doc: AnyIDFDocument, recent: IDFDocumentV9_4) -> None:
    # Required through AnyIDFDocument where any release requires it, so no release refuses a call
    # that type-checks: 8.9 to 26.1 require the construction, 26.2 the CO2 schedule.
    doc["ZoneControl:ContaminantController"].add("CO2", zone_name="Office")  # pyright: ignore[reportCallIssue]  (26.2 requires the schedule)
    doc["ZoneControl:ContaminantController"].add("CO2", zone_name="Office", carbon_dioxide_setpoint_schedule_name="S")
    doc["BuildingSurface:Detailed"].add(
        "Floor", surface_type="Floor", zone_name="Z", outside_boundary_condition="Ground"
    )  # pyright: ignore[reportCallIssue]  (8.9 to 26.1 require the construction)
    doc["BuildingSurface:Detailed"].add(
        "Floor", surface_type="Floor", construction_name="C", zone_name="Z", outside_boundary_condition="Ground"
    )
    # InternalMass's zone field was renamed (zone_name, zone_or_zonelist_name), and every release up
    # to 24.1 requires it: no call suits every release, so the signature asks to narrow first.
    doc["InternalMass"].add("Mass", construction_name="C", surface_area=10.0)  # pyright: ignore[reportCallIssue]  (narrow_with_as_version_first)
    assert_type(
        recent["InternalMass"].add("Mass", construction_name="C", zone_or_zonelist_name="Z", surface_area=10.0),
        InternalMass_v9_2_to_v9_5,
    )


def untyped(doc: IDFDocument[Any], obj_type: str) -> None:
    # A collection a type checker cannot narrow requires nothing and accepts any name and field.
    assert_type(doc.get_collection(obj_type).add(), IDFObject)
    assert_type(doc.get_collection(obj_type).add("Anything", whatever=1), IDFObject)
