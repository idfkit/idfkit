"""Type-check fixture for field access on typed objects (never called; checked by ``make check``).

A typed object (``doc["Material"][...]``) declares its fields, and an undeclared name is a type
error for reading and for assigning. Plain ``IDFObject`` stays permissive. Each seeded error below
carries a ``pyright: ignore`` naming the rule it must trigger, and this file turns on
``reportUnnecessaryTypeIgnoreComment``: if a seeded error stops being reported, the ignore becomes
unnecessary and the check fails, so the fixture proves the errors are caught.
"""

# pyright: strict, reportUnnecessaryTypeIgnoreComment=true

from __future__ import annotations

from typing import Any

from idfkit import IDFDocument
from idfkit.objects import IDFObject


def correct_access(doc: IDFDocument[Any]) -> None:
    for material in doc["Material"]:
        material.thickness = 0.2
        material.roughness = "MediumRough"
        material.name = "Concrete"
        thickness: float | None = material.thickness
        name: str = material.name
        print(thickness, name)
    surface = doc["BuildingSurface:Detailed"]["Wall"]
    surface.vertices[0].vertex_x_coordinate = 1.0
    x: float | None = surface.vertices[0].vertex_x_coordinate
    print(x)
    # The first field of a nameless type is a declared field, not a name.
    timestep = doc["Timestep"].first()
    if timestep is not None:
        timestep.number_of_timesteps_per_hour = 6
    # Plain IDFObject is untyped and stays permissive.
    plain: IDFObject = doc.get_collection("Material")["Concrete"]
    plain.thermal_resistance = 1.0
    print(plain.anything)
    for obj in doc.get_collection("Zone"):
        print(obj.whatever)
    # The eppy API returns plain IDFObject, so eppy-style capitalised names stay permissive there.
    for eppy_material in doc.idfobjects["MATERIAL"]:
        eppy_material.Thickness = 0.2
    # A field whose key ends in an underscore is also declared without it, as the runtime accepts.
    interior = doc["GroundHeatTransfer:Basement:Interior"]["Interior"]
    interior.cond_flag_is_the_basement_conditioned_ = "TRUE"
    interior.cond_flag_is_the_basement_conditioned = "TRUE"
    # Item access and getattr take a name known only at run time.
    print(getattr(doc["Material"]["Concrete"], "thermal_resistance", None))
    field_name = "x_origin"
    doc["Zone"]["Office"][field_name] = 1.0


def seeded_errors(doc: IDFDocument[Any]) -> None:
    material = doc["Material"]["Concrete"]
    material.Thermal_Resistance = 1.0  # pyright: ignore[reportArgumentType]  (undeclared name, assigned)
    print(material.bogus)  # pyright: ignore[reportArgumentType]  (undeclared name, read)
    conductivity: float = material.conductivty  # pyright: ignore[reportArgumentType, reportAssignmentType]  (typo, read as object)
    print(conductivity)
    material.Thickness = 0.2  # pyright: ignore[reportArgumentType]  (typed objects declare snake_case only)
    material.thickness = "abc"  # pyright: ignore[reportAttributeAccessIssue]  (declared field, wrong type)
    vertex = doc["BuildingSurface:Detailed"]["Wall"].vertices[0]
    vertex.bogus = 1.0  # pyright: ignore[reportArgumentType]  (undeclared name on a typed group)
    print(vertex.bogus)  # pyright: ignore[reportArgumentType]  (undeclared name read on a typed group)
