"""Type-check fixture for ``IDFObject.update`` (never called; checked by ``make check``).

Each seeded error below carries a ``pyright: ignore`` naming the rule it must trigger, and this file
turns on ``reportUnnecessaryTypeIgnoreComment``. If a seeded error stops being reported, the ignore
becomes unnecessary and the check fails, so the fixture proves the errors are caught rather than
merely tolerating them.
"""

# pyright: strict, reportUnnecessaryTypeIgnoreComment=true

from __future__ import annotations

from typing import Any

from idfkit import IDFDocument


def correct_calls(doc: IDFDocument[Any]) -> None:
    heater = doc["WaterHeater:Mixed"]["Heater"]
    heater.update(
        heater_fuel_type="Electricity",
        off_cycle_parasitic_fuel_type="Electricity",
        heater_thermal_efficiency=1.0,
        on_cycle_parasitic_fuel_type="Electricity",
    )
    doc["Zone"]["Office"].update({"x_origin": 10.0, "y_origin": 5.0}, z_origin=None)
    doc["Material"]["Concrete"].update(thickness=0.2, roughness="MediumRough")
    doc["BuildingSurface:Detailed"]["Wall"].update(
        surface_type="Wall",
        vertices=[{"vertex_x_coordinate": 0.0, "vertex_y_coordinate": 0.0, "vertex_z_coordinate": 0.0}],
    )
    doc["Construction"]["Wall"].update(outside_layer="Concrete")
    doc["Schedule:Constant"]["Always On"].update(hourly_value=1.0)
    # The positional mapping accepts what the method accepts at run time: a mapping built at run
    # time, ``None``, and the spaced field names single assignment resolves.
    computed: dict[str, Any] = {"x_origin": 1.0}
    doc["Zone"]["Office"].update(computed)
    doc["Zone"]["Office"].update(None, x_origin=2.0)
    doc["Zone"]["Office"].update({"X Origin": 3.0})


def seeded_errors(doc: IDFDocument[Any]) -> None:
    heater = doc["WaterHeater:Mixed"]["Heater"]
    zone = doc["Zone"]["Office"]
    heater.update(heater_fuel_typo="Electricity")  # pyright: ignore[reportCallIssue]  (unknown keyword)
    zone.update(x_origin="ten")  # pyright: ignore[reportArgumentType]  (wrong value type)
    heater.update(heater_fuel_type="Plutonium")  # pyright: ignore[reportArgumentType]  (value outside the Literal)
    doc["Material"]["Concrete"].update(thickness="thick")  # pyright: ignore[reportArgumentType]  (wrong value type)
    zone.update(name="Other")  # pyright: ignore[reportCallIssue]  (name is refused)
