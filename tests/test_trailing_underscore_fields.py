"""Fields whose epJSON property name ends in ``_`` are reachable by assignment, ``update()`` and ``add()``.

EnergyPlus derives an epJSON key from the IDD field name without trimming it, so a name that ends in
punctuation or a space ends in ``_`` (``"COND: Flag: Is the basement conditioned?"`` is
``cond_flag_is_the_basement_conditioned_``). ``to_python_name`` trims that underscore, so assignment
and ``update()`` used to refuse the real field. Both the schema's key and the spelling without the
underscore now resolve to the schema's key, which is what is stored and written. ``name`` is never
such a spelling.
"""

from __future__ import annotations

import copy
import pickle
from typing import Any

import pytest

from idfkit import IDFDocument, IDFObject, new_document, write_epjson, write_idf
from idfkit.exceptions import InvalidFieldError, RangeError
from idfkit.objects import to_python_name
from idfkit.schema import get_schema, trailing_underscore_aliases
from idfkit.versions import ENERGYPLUS_VERSIONS

_STEM = "cond_flag_is_the_basement_conditioned"
_KEY = _STEM + "_"


def _trailing_underscore_fields() -> list[tuple[tuple[int, int, int], str, str]]:
    """Every (latest version, type, field) whose field name ``to_python_name`` would change."""
    found: dict[tuple[str, str], tuple[int, int, int]] = {}
    for version in ENERGYPLUS_VERSIONS:
        schema = get_schema(version)
        for obj_type in schema.object_types:
            for key in schema.get_all_field_names(obj_type):
                if to_python_name(key) != key:
                    found[(obj_type, key)] = version
    return [(version, obj_type, key) for (obj_type, key), version in sorted(found.items())]


_FIELDS = _trailing_underscore_fields()
_IDS = [f"{t}.{k}" for _, t, k in _FIELDS]


def _add(doc: IDFDocument[Any], obj_type: str, fields: dict[str, Any] | None = None) -> IDFObject:
    name = "Obj" if doc.schema is not None and doc.schema.has_name(obj_type) else ""
    return doc.add(obj_type, name, fields, validate=False)


def _report_period(doc: IDFDocument[Any]) -> IDFObject:
    # Nameless in 22.2 to 25.1: its IDD "Name," field is name_, so add() refuses an object name.
    return doc.add("Output:Table:ReportPeriod", validate=False)


def test_the_schemas_have_trailing_underscore_fields() -> None:
    keys = {key for _, _, key in _FIELDS}
    assert "cond_flag_is_the_basement_conditioned_" in keys
    assert "nx_number_of_cells_in_the_x_direction_20_" in keys
    assert "type_of_rectangular_large_vertical_opening_lvo_" in keys
    assert all(key.endswith("_") for key in keys)


def test_alias_map_covers_both_spellings_but_never_name() -> None:
    aliases = trailing_underscore_aliases(["name_", "report_name_", "begin_year", "x", "x_"])
    assert aliases == {"name_": "name_", "report_name_": "report_name_", "report_name": "report_name_"}


@pytest.mark.parametrize(("version", "obj_type", "key"), _FIELDS, ids=_IDS)
def test_assignment_accepts_trailing_underscore_field(version: tuple[int, int, int], obj_type: str, key: str) -> None:
    obj = _add(new_document(version), obj_type)
    setattr(obj, key, "X")
    assert getattr(obj, key) == "X"
    assert obj.data[key] == "X"


@pytest.mark.parametrize(("version", "obj_type", "key"), _FIELDS, ids=_IDS)
def test_update_accepts_trailing_underscore_field(version: tuple[int, int, int], obj_type: str, key: str) -> None:
    obj = _add(new_document(version), obj_type)
    obj.update({key: "X"})
    assert obj.data[key] == "X"


@pytest.mark.parametrize(("version", "obj_type", "key"), _FIELDS, ids=_IDS)
def test_strict_read_of_unset_trailing_underscore_field(version: tuple[int, int, int], obj_type: str, key: str) -> None:
    obj = _add(new_document(version), obj_type)
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
    obj = new_document((24, 1, 0)).add("GroundHeatTransfer:Basement:Interior", "", validate=False)
    with pytest.raises(InvalidFieldError):
        obj.update(cond_flag_is_the_basement_conditionned="FALSE")
    with pytest.raises(InvalidFieldError):
        obj.cond_flag_is_the_basement_conditionned = "FALSE"


def test_trailing_underscore_on_an_ordinary_field_still_normalizes() -> None:
    zone = new_document((24, 1, 0)).add("Zone", "Office")
    zone.update(x_origin_=3.0)
    assert zone.data["x_origin"] == 3.0
    assert "x_origin_" not in zone.data


@pytest.mark.parametrize(("version", "obj_type", "key"), _FIELDS, ids=_IDS)
def test_eppy_dotted_update_accepts_trailing_underscore_field(
    version: tuple[int, int, int], obj_type: str, key: str
) -> None:
    doc: Any = new_document(version)
    obj = _add(doc, obj_type)
    doc.update({f"{obj_type}.{obj.name}.{key}": "X"})
    assert obj.data == {key: "X"}


# The spelling without the underscore reaches the field; ``name`` never does (see the name tests).
_STEM_FIELDS = [(v, t, k) for v, t, k in _FIELDS if k != "name_"]
_STEM_IDS = [f"{t}.{k[:-1]}" for _, t, k in _STEM_FIELDS]


@pytest.mark.parametrize(("version", "obj_type", "key"), _STEM_FIELDS, ids=_STEM_IDS)
def test_stripped_spelling_resolves_to_the_schema_key(version: tuple[int, int, int], obj_type: str, key: str) -> None:
    stem = key[:-1]
    obj = _add(new_document(version), obj_type)
    setattr(obj, stem, "A")
    assert obj.data == {key: "A"}
    assert getattr(obj, stem) == "A"
    assert getattr(obj, key) == "A"
    obj.update({stem: "B"})
    assert obj.data == {key: "B"}


@pytest.mark.parametrize(("version", "obj_type", "key"), _STEM_FIELDS, ids=_STEM_IDS)
def test_add_stores_stripped_spelling_under_the_schema_key(
    version: tuple[int, int, int], obj_type: str, key: str
) -> None:
    obj = _add(new_document(version), obj_type, {key[:-1]: "A"})
    assert obj.data == {key: "A"}


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


@pytest.mark.parametrize("stem_value", ["TRUE", None, ""])
@pytest.mark.parametrize("validate", [False, True])
def test_add_refuses_both_spellings_of_one_field(stem_value: str | None, validate: bool) -> None:
    doc = new_document((24, 1, 0))
    with pytest.raises(InvalidFieldError, match=f"'{_STEM}'"):
        doc.add("GroundHeatTransfer:Basement:Interior", "", {_KEY: "FALSE", _STEM: stem_value}, validate=validate)
    assert len(doc["GroundHeatTransfer:Basement:Interior"]) == 0


def test_a_stray_stem_in_the_data_does_not_capture_the_field() -> None:
    # What an older idfkit left behind after a non-strict assignment, or an epJSON file spelled so.
    obj = new_document((24, 1, 0)).add("GroundHeatTransfer:Basement:Interior", "", validate=False)
    obj.data[_STEM] = "TRUE"
    obj.cond_flag_is_the_basement_conditioned_ = "FALSE"
    assert obj.data[_KEY] == "FALSE"
    obj.update({_STEM: "TRUE"})
    assert obj.data[_KEY] == "TRUE"
    assert getattr(obj, _STEM) == "TRUE"


# -- ``name`` is never an alias for ``name_`` ------------------------------------------------


def test_update_refuses_name_beside_name_underscore() -> None:
    obj = _report_period(new_document((24, 1, 0)))
    for group in ({"name": "Renamed", "name_": "Summer"}, {"name_": "Summer", "name": "Renamed"}, {"Name ": "X"}):
        with pytest.raises(InvalidFieldError):
            obj.update(group)
    assert obj.data == {}


def test_reading_a_name_spelling_does_not_reach_name_underscore() -> None:
    obj = _report_period(new_document((24, 1, 0)))
    obj.name_ = "Summer"
    with pytest.raises(InvalidFieldError):
        _ = obj.NAME


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


def test_add_refuses_name_in_fields_of_report_period() -> None:
    doc = new_document((24, 1, 0))
    # The refusal names the key `name` (quoted in one message format, listed as "- name:" in the
    # other); it must not resolve `name` to the `name_` field.
    with pytest.raises(InvalidFieldError, match=r"'name'|- name: name\b"):
        # The 24.1 type has no Name field, so the stray `name` key is tested with no object name.
        doc.add("Output:Table:ReportPeriod", "", {"name": "Summer"}, validate=False)


# -- eppy compatibility ----------------------------------------------------------------------


def test_dotted_update_keeps_private_names_out_and_renames() -> None:
    doc: Any = new_document((24, 1, 0))
    doc.add("Zone", "Office")
    doc.update({"Zone.Office._name": "Lobby"})
    assert doc.getobject("Zone", "Lobby") is not None
    assert doc.getobject("Zone", "Office") is None
    doc.update({"Zone.Lobby.Name ": "Lab"})
    assert doc.getobject("Zone", "Lab") is not None


def _gap_doc() -> tuple[IDFDocument[Any], IDFObject, IDFObject]:
    doc = new_document((24, 1, 0))
    # A same-named object of another type, added first, must not be mistaken for the gas.
    doc.add("Material", "Argon", roughness="Rough", thickness=0.1, conductivity=1.0, density=1.0, specific_heat=1000.0)
    gas = doc.add("WindowMaterial:Gas", "Argon", gas_type="Argon", thickness=0.01)
    gap = doc.add("WindowMaterial:Gap", "Gap1", validate=False)
    gap.gas_or_gas_mixture = "Argon"
    return doc, gas, gap


@pytest.mark.parametrize("field", ["gas_or_gas_mixture", "gas_or_gas_mixture_"])
def test_get_referenced_object_uses_the_field_reference_list(field: str) -> None:
    _, gas, gap = _gap_doc()
    assert gap.get_referenced_object(field) is gas


@pytest.mark.parametrize("field", ["gas_or_gas_mixture", "gas_or_gas_mixture_"])
def test_getreferingobjs_filters_by_a_trailing_underscore_field(field: str) -> None:
    _, gas, gap = _gap_doc()
    assert gas.getreferingobjs(fields=[field]) == [gap]


def test_checkrange_applies_the_schema_range() -> None:
    dd = new_document((24, 1, 0)).add("SizingPeriod:DesignDay", "DD", validate=False)
    dd.ashrae_clear_sky_optical_depth_for_beam_irradiance_taub = 5.0
    assert dd.getrange("ashrae_clear_sky_optical_depth_for_beam_irradiance_taub")["maximum"] == 1.2
    with pytest.raises(RangeError):
        dd.checkrange("ashrae_clear_sky_optical_depth_for_beam_irradiance_taub_")


# -- Objects that do not come from add() or a parser ----------------------------------------


def test_object_built_without_aliases_derives_them_from_its_field_order() -> None:
    doc = new_document((24, 1, 0))
    t = "GroundHeatTransfer:Basement:Interior"
    obj = IDFObject(t, "", {}, field_order=doc.schema.get_all_field_names(t) if doc.schema else None)
    doc.addidfobject(obj)
    obj.cond_flag_is_the_basement_conditioned = "TRUE"
    assert obj.data == {_KEY: "TRUE"}


def test_copies_keep_resolving_the_stem() -> None:
    doc = new_document((24, 1, 0))
    obj = doc.add("GroundHeatTransfer:Basement:Interior", "", validate=False)
    for clone in (obj.copy(), copy.deepcopy(obj), pickle.loads(pickle.dumps(obj))):  # noqa: S301
        clone.cond_flag_is_the_basement_conditioned = "TRUE"
        assert clone.data == {_KEY: "TRUE"}


def test_object_pickled_before_the_alias_map_existed() -> None:
    obj = new_document((24, 1, 0)).add("GroundHeatTransfer:Basement:Interior", "", validate=False)
    state = obj.__reduce_ex__(2)[2]
    slots = dict(state[1])
    del slots["_aliases"]  # an older idfkit had no such slot
    old = IDFObject.__new__(IDFObject)
    old.__setstate__((None, slots))
    old.cond_flag_is_the_basement_conditioned = "TRUE"
    assert old.data == {_KEY: "TRUE"}
