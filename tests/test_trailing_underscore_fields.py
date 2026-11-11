"""Fields whose epJSON property name ends in ``_`` are reachable by assignment and ``update()``.

``to_python_name`` strips a trailing underscore, so ``cond_flag_is_the_basement_conditioned_``
used to resolve to ``cond_flag_is_the_basement_conditioned``, which is not a field, and
assignment and ``update()`` refused a real field. ``add()`` already accepted these names.
"""

from __future__ import annotations

from typing import Any

import pytest

from idfkit import IDFDocument, IDFObject, new_document, write_idf
from idfkit.exceptions import InvalidFieldError
from idfkit.objects import to_python_name
from idfkit.schema import get_schema
from idfkit.versions import ENERGYPLUS_VERSIONS


def _trailing_underscore_fields() -> list[tuple[tuple[int, int, int], str, str]]:
    """Every (latest version, type, field) whose field name ``to_python_name`` would change."""
    found: dict[tuple[str, str], tuple[int, int, int]] = {}
    for version in ENERGYPLUS_VERSIONS:
        schema = get_schema(version)
        for obj_type in schema.object_types:
            pc = schema.get_parsing_cache(obj_type)
            if pc is None:
                continue
            for key in pc.all_field_names:
                if to_python_name(key) != key:
                    found[(obj_type, key)] = version
    return [(version, obj_type, key) for (obj_type, key), version in sorted(found.items())]


_FIELDS = _trailing_underscore_fields()


def _add(doc: IDFDocument[Any], obj_type: str) -> IDFObject:
    pc = doc.schema.get_parsing_cache(obj_type) if doc.schema is not None else None
    name = "Obj" if pc is not None and pc.has_name else ""
    return doc.add(obj_type, name, validate=False)


def test_the_schemas_have_trailing_underscore_fields() -> None:
    keys = {key for _, _, key in _FIELDS}
    assert "cond_flag_is_the_basement_conditioned_" in keys
    assert "nx_number_of_cells_in_the_x_direction_20_" in keys
    assert "type_of_rectangular_large_vertical_opening_lvo_" in keys
    assert all(key.endswith("_") for key in keys)


@pytest.mark.parametrize(("version", "obj_type", "key"), _FIELDS, ids=[f"{t}.{k}" for _, t, k in _FIELDS])
def test_assignment_accepts_trailing_underscore_field(version: tuple[int, int, int], obj_type: str, key: str) -> None:
    doc = new_document(version)
    obj = _add(doc, obj_type)
    setattr(obj, key, "X")
    assert getattr(obj, key) == "X"
    assert obj.data[key] == "X"


@pytest.mark.parametrize(("version", "obj_type", "key"), _FIELDS, ids=[f"{t}.{k}" for _, t, k in _FIELDS])
def test_update_accepts_trailing_underscore_field(version: tuple[int, int, int], obj_type: str, key: str) -> None:
    doc = new_document(version)
    obj = _add(doc, obj_type)
    obj.update({key: "X"})
    assert obj.data[key] == "X"


@pytest.mark.parametrize(("version", "obj_type", "key"), _FIELDS, ids=[f"{t}.{k}" for _, t, k in _FIELDS])
def test_strict_read_of_unset_trailing_underscore_field(version: tuple[int, int, int], obj_type: str, key: str) -> None:
    doc = new_document(version)
    obj = _add(doc, obj_type)
    assert getattr(obj, key) is None


def test_basement_interior_update_and_write() -> None:
    doc = new_document((24, 1, 0))
    obj = doc.add("GroundHeatTransfer:Basement:Interior", "", validate=False)
    obj.update(cond_flag_is_the_basement_conditioned_="FALSE")
    assert obj.cond_flag_is_the_basement_conditioned_ == "FALSE"
    assert "FALSE" in write_idf(doc)


def test_report_period_name_underscore_is_a_field_not_the_object_name() -> None:
    doc = new_document((24, 1, 0))
    obj = doc.add("Output:Table:ReportPeriod", "Period", validate=False)
    obj.update(name_="Summer", report_name_="AllSummary")
    assert obj.name == "Period"
    assert obj.data["name_"] == "Summer"
    assert obj.data["report_name_"] == "AllSummary"


def test_stripped_spelling_is_still_unknown() -> None:
    doc = new_document((24, 1, 0))
    obj = doc.add("GroundHeatTransfer:Basement:Interior", "", validate=False)
    with pytest.raises(InvalidFieldError):
        obj.update(cond_flag_is_the_basement_conditioned="FALSE")
    with pytest.raises(InvalidFieldError):
        obj.cond_flag_is_the_basement_conditioned = "FALSE"


def test_trailing_underscore_on_an_ordinary_field_still_normalizes() -> None:
    doc = new_document((24, 1, 0))
    zone = doc.add("Zone", "Office")
    zone.update(x_origin_=3.0)
    assert zone.data["x_origin"] == 3.0
    assert "x_origin_" not in zone.data


def test_eppy_dotted_update_accepts_trailing_underscore_field() -> None:
    doc: Any = new_document((24, 1, 0))
    doc.add("GroundHeatTransfer:Basement:ManualGrid", "", validate=False)
    obj = doc["GroundHeatTransfer:Basement:ManualGrid"][0]
    doc.update({f"GroundHeatTransfer:Basement:ManualGrid.{obj.name}.nx_number_of_cells_in_the_x_direction_20_": 12})
    assert obj.data["nx_number_of_cells_in_the_x_direction_20_"] == 12
