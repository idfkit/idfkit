"""Fields whose epJSON property name ends in ``_`` are reachable by assignment, ``update()`` and ``add()``.

The underscore comes from IDD field names that end in punctuation (``"COND: Flag: Is the basement
conditioned?"``). ``to_python_name`` strips it, so assignment and ``update()`` used to refuse the
real field. Both the schema's key and the spelling without the underscore now resolve to the
schema's key, which is what is stored and written.
"""

from __future__ import annotations

from typing import Any

import pytest

from idfkit import IDFDocument, IDFObject, new_document, write_epjson, write_idf
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
    """Up to 25.1 ``Output:Table:ReportPeriod`` has no Name field; ``name_`` is its first field."""
    doc = new_document((24, 1, 0))
    obj = doc.add("Output:Table:ReportPeriod", validate=False)
    obj.update(name_="Summer", report_name_="AllSummary")
    assert obj.name == ""
    assert obj.data["name_"] == "Summer"
    assert obj.data["report_name_"] == "AllSummary"


def test_a_misspelling_is_still_unknown() -> None:
    doc = new_document((24, 1, 0))
    obj = doc.add("GroundHeatTransfer:Basement:Interior", "", validate=False)
    with pytest.raises(InvalidFieldError):
        obj.update(cond_flag_is_the_basement_conditionned="FALSE")
    with pytest.raises(InvalidFieldError):
        obj.cond_flag_is_the_basement_conditionned = "FALSE"


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


# The spelling without the underscore is an alias for the schema's key. ``name`` is not: on
# Output:Table:ReportPeriod it is the object's name, and ``name_`` is the field.
_STEM_FIELDS = [(v, t, k) for v, t, k in _FIELDS if k != "name_"]
_STEM_IDS = [f"{t}.{k[:-1]}" for _, t, k in _STEM_FIELDS]


@pytest.mark.parametrize(("version", "obj_type", "key"), _STEM_FIELDS, ids=_STEM_IDS)
def test_stripped_spelling_resolves_to_the_schema_key(version: tuple[int, int, int], obj_type: str, key: str) -> None:
    stem = key.rstrip("_")
    doc = new_document(version)
    obj = _add(doc, obj_type)
    setattr(obj, stem, "A")
    assert obj.data[key] == "A"
    assert stem not in obj.data
    assert getattr(obj, stem) == "A"
    assert getattr(obj, key) == "A"
    obj.update({stem: "B"})
    assert obj.data[key] == "B"
    assert stem not in obj.data


@pytest.mark.parametrize(("version", "obj_type", "key"), _STEM_FIELDS, ids=_STEM_IDS)
def test_add_stores_stripped_spelling_under_the_schema_key(
    version: tuple[int, int, int], obj_type: str, key: str
) -> None:
    stem = key.rstrip("_")
    doc = new_document(version)
    pc = doc.schema.get_parsing_cache(obj_type) if doc.schema is not None else None
    name = "Obj" if pc is not None and pc.has_name else ""
    obj = doc.add(obj_type, name, {stem: "A"}, validate=False)
    assert obj.data[key] == "A"
    assert stem not in obj.data


def test_stripped_spelling_is_written_under_the_schema_key() -> None:
    doc = new_document((24, 1, 0))
    obj = doc.add("GroundHeatTransfer:Basement:Interior", "", validate=False)
    obj.cond_flag_is_the_basement_conditioned = "FALSE"
    epjson = write_epjson(doc)
    assert '"cond_flag_is_the_basement_conditioned_": "FALSE"' in epjson
    assert '"cond_flag_is_the_basement_conditioned"' not in epjson


def test_one_spelling_works_across_a_version_that_fixed_the_name() -> None:
    # 9.0.1 and 9.1.0 have construction_with_shading_name_; 9.2.0 onward dropped the underscore.
    old = new_document((9, 1, 0)).add("WindowShadingControl", "W", validate=False)
    new = new_document((24, 1, 0)).add("WindowShadingControl", "W", validate=False)
    old.construction_with_shading_name = "Shaded"
    new.construction_with_shading_name = "Shaded"
    assert old.data["construction_with_shading_name_"] == "Shaded"
    assert new.data["construction_with_shading_name"] == "Shaded"


def test_add_refuses_both_spellings_of_one_field() -> None:
    doc = new_document((24, 1, 0))
    with pytest.raises(InvalidFieldError):
        doc.add(
            "GroundHeatTransfer:Basement:Interior",
            "",
            validate=False,
            cond_flag_is_the_basement_conditioned="TRUE",
            cond_flag_is_the_basement_conditioned_="FALSE",
        )


def test_name_on_nameless_report_period_is_refused_not_moved_to_name_underscore() -> None:
    """A name on the 24.1 type, which has none, is refused and never lands in ``name_``."""
    doc = new_document((24, 1, 0))
    with pytest.raises(InvalidFieldError, match='name_="Period"'):
        doc.add("Output:Table:ReportPeriod", "Period", validate=False)
    obj = doc.add("Output:Table:ReportPeriod", validate=False)
    with pytest.raises(InvalidFieldError):
        obj.name = "Renamed"
    assert obj.name == ""
    assert "name_" not in obj.data


def test_name_on_named_report_period_is_the_object_name() -> None:
    """From 25.2 the type has a Name field, and a name is accepted."""
    doc = new_document((26, 1, 0))
    obj = doc.add("Output:Table:ReportPeriod", "Period", validate=False)
    obj.name = "Renamed"
    assert obj.name == "Renamed"
    assert "name_" not in obj.data
