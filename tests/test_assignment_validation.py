"""Assignment and ``update()`` check a value as ``add()`` does, in a strict document.

``add()`` refuses a value of the wrong type, a choice the schema does not list and a number out of
range. Assignment, item assignment and ``update()`` used to store all three, so the error surfaced only
in ``validate_document()`` or as an EnergyPlus severe. In a strict document (the default) they now
raise :class:`~idfkit.exceptions.ValidationFailedError` and leave the object unchanged. A lax document
(``strict=False``) still stores any value, for ``validate_document()`` to report.
"""

from __future__ import annotations

from typing import Any

import pytest

from idfkit import IDFObject, new_document, validate_document, write_idf
from idfkit.exceptions import InvalidFieldError, ValidationFailedError


def _material(doc: Any) -> IDFObject:
    return doc.add(
        "Material", "M", roughness="Rough", thickness=0.1, conductivity=1.0, density=1.0, specific_heat=100.0
    )


@pytest.mark.parametrize(
    ("field", "value", "code"),
    [
        ("thickness", -5.0, "E006"),
        ("thickness", "abc", "E003"),
        ("roughness", "Lumpy", "E004"),
    ],
)
def test_assignment_refuses_what_add_refuses(field: str, value: Any, code: str) -> None:
    doc = new_document()
    mat = _material(doc)
    before = mat.mutation_version
    with pytest.raises(ValidationFailedError) as excinfo:
        setattr(mat, field, value)
    assert [(e.code, e.field) for e in excinfo.value.errors] == [(code, field)]
    assert mat.mutation_version == before
    # add() refuses the same value with an error of the same code.
    with pytest.raises(ValidationFailedError) as add_exc:
        doc.add("Material", "M2", **{**_material_fields(), field: value})
    assert add_exc.value.errors[0].code == excinfo.value.errors[0].code


def _material_fields() -> dict[str, Any]:
    return {"roughness": "Rough", "thickness": 0.1, "conductivity": 1.0, "density": 1.0, "specific_heat": 100.0}


def test_item_assignment_by_name_and_index_is_checked() -> None:
    doc = new_document()
    zone = doc.zones.add("Office")
    with pytest.raises(ValidationFailedError, match="multiplier"):
        doc["Zone"]["Office"]["multiplier"] = -3
    with pytest.raises(ValidationFailedError, match="x_origin"):
        zone[2] = "abc"
    assert zone.get("multiplier") is None
    assert zone.get("x_origin") is None


def test_update_is_all_or_nothing_and_reports_every_value() -> None:
    zone = new_document().zones.add("Office")
    with pytest.raises(ValidationFailedError) as excinfo:
        zone.update(x_origin="abc", y_origin=2.0, multiplier=-3)
    assert sorted(e.field for e in excinfo.value.errors) == ["multiplier", "x_origin"]
    assert zone.get("y_origin") is None


def test_update_reports_unknown_names_before_values() -> None:
    zone = new_document().zones.add("Office")
    with pytest.raises(InvalidFieldError):
        zone.update(x_orign=1.0, multiplier=-3)


def test_valid_values_and_clearing_are_accepted() -> None:
    doc = new_document()
    zone = doc.zones.add("Office", multiplier=2)
    zone.multiplier = 3
    zone.zone_inside_convection_algorithm = "tarp"
    zone.update(x_origin=1, y_origin=2.5)
    zone.multiplier = None
    assert zone.zone_inside_convection_algorithm == "TARP"
    assert zone.get("multiplier") is None
    assert zone.x_origin == 1


def test_autosize_keyword_is_accepted_on_a_numeric_field() -> None:
    zone = new_document().zones.add("Office")
    zone.volume = "Autocalculate"
    assert zone.volume == "Autocalculate"


def test_lax_document_stores_any_value_for_validate_document() -> None:
    doc = new_document(strict=False)
    zone = doc.add("Zone", "Office")
    zone.multiplier = -3
    zone.zone_inside_convection_algorithm = "Bogus"
    assert "-3," in write_idf(doc)
    found = {(e.code, e.field) for e in validate_document(doc).errors}
    assert found == {("E005", "multiplier"), ("E004", "zone_inside_convection_algorithm")}


def test_detached_object_is_not_checked() -> None:
    zone = IDFObject("Zone", "Office", {})
    zone.multiplier = -3
    assert zone.data["multiplier"] == -3
