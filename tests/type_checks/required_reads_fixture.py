"""Type-check fixture for reading required fields (never called; checked by ``make check``).

A field that every release having it requires, with no default, reads as its value type: ``add()``
refuses an object without it, and reading it from an object that lacks it anyway (a loaded file,
``validate=False``) raises ``MissingRequiredFieldError`` instead of returning ``None``
(``tests/test_required_reads.py`` checks the run time). Assigning ``None`` to such a field is a type
error, since it makes an object EnergyPlus refuses. Every other field still reads ``| None``. A blank
is stored as absent, so ``""`` is not a value of any field: clearing is spelled ``None``.

Each seeded error below carries a ``pyright: ignore`` naming the rule it must trigger, and this file
turns on ``reportUnnecessaryTypeIgnoreComment``: if a seeded error stops being reported, the ignore
becomes unnecessary and the check fails, so the fixture proves the errors are caught.
"""

# pyright: strict, reportUnnecessaryTypeIgnoreComment=true

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Literal

from typing_extensions import assert_type

from idfkit import IDFDocument
from idfkit.versioned import AnyIDFDocument, IDFDocumentV9_4

if TYPE_CHECKING:
    from idfkit.document import AnyMaterial


def r_value(mat: AnyMaterial) -> float:
    # No guard: thickness and conductivity are required in every release.
    return mat.thickness / mat.conductivity


def created(doc: IDFDocument[Any]) -> None:
    mat = doc.materials.add(
        "B", roughness="Rough", thickness=0.1, conductivity=0.7, density=1900.0, specific_heat=800.0
    )
    assert_type(mat.thickness, float)
    assert_type(mat.roughness, Literal["MediumRough", "MediumSmooth", "Rough", "Smooth", "VeryRough", "VerySmooth"])
    print(r_value(mat))
    # A field with a schema default is not required: blank, it reads None.
    assert_type(mat.thermal_absorptance, float | None)


def read_from_collections(doc: AnyIDFDocument, old: IDFDocumentV9_4) -> None:
    for mat in doc.materials:
        print(mat.thickness * 2)
    surface = doc["BuildingSurface:Detailed"]["Wall"]
    assert_type(surface.zone_name, str)
    # 8.9 to 26.1 require a surface's construction and 26.2 does not: it reads optional everywhere,
    # so no static view promises a value some release may lack.
    assert_type(surface.construction_name, str | None)
    assert_type(old["BuildingSurface:Detailed"]["Wall"].construction_name, str | None)
    assert_type(old.materials["B"].thickness, float)


def blanks(doc: IDFDocument[Any]) -> None:
    zone = doc.zones.add("Office")
    assert_type(zone.ceiling_height, float | Literal["Autocalculate"] | None)
    zone.ceiling_height = None
    zone.ceiling_height = ""  # pyright: ignore[reportAttributeAccessIssue]  (a blank is None, not "")
    doc.zones.add("Hall", ceiling_height="")  # pyright: ignore[reportArgumentType]  (a blank is None, not "")


def clearing_a_required_field(doc: IDFDocument[Any]) -> None:
    mat = doc.materials["B"]
    mat.thickness = None  # pyright: ignore[reportAttributeAccessIssue]  (EnergyPlus refuses a material without it)
    mat.update(thickness=None)  # pyright: ignore[reportArgumentType]  (the same, through update)
    # The untyped read still asks whether the field is set.
    print(mat.get("thickness"))


def stale_guard(doc: IDFDocument[Any]) -> float:
    mat = doc.materials["B"]
    if mat.thickness is None:  # pyright: ignore[reportUnnecessaryComparison]  (it reads a float or raises)
        raise ValueError(mat.name)
    return mat.thickness
