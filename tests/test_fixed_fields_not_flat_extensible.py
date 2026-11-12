"""Fixed fields whose names fit a flat-extensible pattern stay fixed fields.

Some types have positional fields named like an eppy-style flat spelling of their own
extensible group: ``MaterialProperty:GlazingSpectralData`` has fixed ``wavelength_1`` ..
``back_reflectance_4`` beside an ``extensions`` group of ``wavelength`` / ``transmittance`` /
..., ``Site:SpectrumData`` has fixed ``wavelength`` / ``spectrum`` / ``wavelength_1`` /
``spectrum_2`` beside a ``wavelength`` / ``spectrum`` group, ``ZoneHVAC:HybridUnitaryHVAC``
has fixed ``mode_0_*`` fields beside a ``modes`` group of ``mode_*``, and
``Table:MultiVariableLookup`` (8.9 to 9.1) has fixed ``field_1_...`` / ``field_2_...`` beside a
``values`` group. A real field must never be folded into the extensible wrapper, refused as
legacy-flat, or read from a group.
"""

from __future__ import annotations

import copy
import json
import re
from pathlib import Path
from typing import Any

import pytest

from idfkit import (
    ENERGYPLUS_VERSIONS,
    LATEST_VERSION,
    get_schema,
    load_epjson,
    load_idf,
    new_document,
    save_epjson,
    save_idf,
    write_idf,
)
from idfkit.document import IDFDocument
from idfkit.schema import ParsingCache

pytestmark = pytest.mark.filterwarnings("error::DeprecationWarning")

AFFECTED = {
    "MaterialProperty:GlazingSpectralData": ENERGYPLUS_VERSIONS,
    "Site:SpectrumData": ENERGYPLUS_VERSIONS,
    "ZoneHVAC:HybridUnitaryHVAC": ENERGYPLUS_VERSIONS,
    "Table:MultiVariableLookup": [(8, 9, 0), (9, 0, 1), (9, 1, 0)],
}
VERSIONS = [(9, 1, 0), (24, 1, 0), LATEST_VERSION]
CASES = [
    pytest.param(t, v, id=f"{t}-{'.'.join(map(str, v))}")
    for t, versions in AFFECTED.items()
    for v in VERSIONS
    if v in versions
]

_NUMBERED = re.compile(r"_\d+(?=_|$)")


def _pc(obj_type: str, version: tuple[int, int, int]) -> ParsingCache:
    pc = get_schema(version).get_parsing_cache(obj_type)
    assert pc is not None
    return pc


def _lookalikes(pc: ParsingCache) -> list[str]:
    """The fixed fields spelled like a numbered (``_<n>`` / ``_<n>_``) form of an extensible name."""
    ext = set(pc.ext_field_names)
    return [f for f in pc.field_names if any(_NUMBERED.sub("", f, count=1) == e for e in ext) or f in ext]


def _fixed_values(pc: ParsingCache) -> dict[str, Any]:
    return {
        f: round(0.3 + i * 0.01, 4) if pc.field_types.get(f) in ("number", "integer") else f"Table {i}"
        for i, f in enumerate(_lookalikes(pc))
    }


def _one_group(pc: ParsingCache) -> tuple[str, dict[str, Any]]:
    assert pc.ext_wrapper_key is not None
    first = pc.ext_field_names[0]
    return pc.ext_wrapper_key, {first: 0.9 if pc.field_types.get(first) in ("number", "integer") else "Group Table"}


def _add(doc: IDFDocument, obj_type: str, **fields: Any) -> Any:
    # Deep-copied, so the assertions below compare stored data with an independent literal.
    return doc.add(obj_type, "Obj", validate=False, **copy.deepcopy(fields))


def test_affected_types_are_exactly_these() -> None:
    found: dict[str, list[tuple[int, int, int]]] = {}
    for version in ENERGYPLUS_VERSIONS:
        schema = get_schema(version)
        for obj_type in schema.object_types:
            pc = schema.get_parsing_cache(obj_type)
            if pc is not None and pc.ext_field_names and _lookalikes(pc):
                found.setdefault(obj_type, []).append(version)
    assert found == {t: list(v) for t, v in AFFECTED.items()}


@pytest.mark.parametrize(("obj_type", "version"), CASES)
def test_add_keeps_fixed_fields(obj_type: str, version: tuple[int, int, int]) -> None:
    pc = _pc(obj_type, version)
    fixed = _fixed_values(pc)
    wrapper, group = _one_group(pc)
    obj = _add(new_document(version=version), obj_type, **fixed, **{wrapper: [group]})
    assert obj.data == {**fixed, wrapper: [group]}
    for field, value in fixed.items():
        assert getattr(obj, field) == value


def test_spectrum_data_wavelength_and_wavelength_1_both_kept() -> None:
    obj = _add(new_document(version=(24, 1, 0)), "Site:SpectrumData", wavelength=0.3, wavelength_1=0.305)
    assert obj.data == {"wavelength": 0.3, "wavelength_1": 0.305}


def test_glazing_spectral_data_idf_output_not_shifted() -> None:
    doc = new_document(version=(24, 1, 0))
    group = {"wavelength": 0.5, "transmittance": 0.2, "front_reflectance": 0.07, "back_reflectance": 0.08}
    fixed = {"wavelength_1": 0.3, "transmittance_1": 0.1, "front_reflectance_1": 0.05, "back_reflectance_1": 0.06}
    _add(doc, "MaterialProperty:GlazingSpectralData", **fixed, extensions=[group])
    # Name, the 4 set fixed fields, 12 blank fixed fields, then the extensible group.
    expected = "MaterialProperty:GlazingSpectralData,Obj,0.3,0.1,0.05,0.06" + "," * 12 + ",0.5,0.2,0.07,0.08;"
    assert expected in write_idf(doc, output_type="compressed")


@pytest.mark.parametrize(("obj_type", "version"), CASES)
def test_setattr_and_update_write_fixed_fields(obj_type: str, version: tuple[int, int, int]) -> None:
    pc = _pc(obj_type, version)
    wrapper, group = _one_group(pc)
    obj = _add(new_document(version=version), obj_type, **{wrapper: [group]})
    fixed = _fixed_values(pc)
    first, *rest = fixed
    setattr(obj, first, fixed[first])
    obj.update({k: fixed[k] for k in rest})
    assert obj.data == {**fixed, wrapper: [group]}


@pytest.mark.parametrize(("obj_type", "version"), CASES)
def test_unset_fixed_field_reads_none_not_group(obj_type: str, version: tuple[int, int, int]) -> None:
    pc = _pc(obj_type, version)
    wrapper, group = _one_group(pc)
    obj = _add(new_document(version=version), obj_type, **{wrapper: [group, group]})
    for field in _lookalikes(pc):
        assert getattr(obj, field) is None


@pytest.mark.parametrize(("obj_type", "version"), CASES)
def test_round_trip_idf_epjson(obj_type: str, version: tuple[int, int, int], tmp_path: Path) -> None:
    pc = _pc(obj_type, version)
    fixed = _fixed_values(pc)
    wrapper, group = _one_group(pc)
    expected = {**fixed, wrapper: [group]}
    doc = new_document(version=version)
    _add(doc, obj_type, **expected)

    idf_path = tmp_path / "m.idf"
    save_idf(doc, idf_path)
    from_idf = load_idf(str(idf_path), version=version)
    assert from_idf[obj_type].first().data == expected  # pyright: ignore[reportOptionalMemberAccess]

    json_path = tmp_path / "m.epJSON"
    save_epjson(from_idf, json_path)
    stored = next(iter(json.loads(json_path.read_text())[obj_type].values()))
    assert stored == expected

    from_json = load_epjson(str(json_path), version=version)
    assert from_json[obj_type].first().data == expected  # pyright: ignore[reportOptionalMemberAccess]


def test_hand_built_object_without_field_order_keeps_fixed_fields() -> None:
    from idfkit.objects import IDFObject

    pc = _pc("Site:SpectrumData", (24, 1, 0))
    obj = IDFObject(
        "Site:SpectrumData",
        "S",
        schema=pc.obj_schema,
        extensibles=frozenset(pc.ext_field_names),
        wrapper_key=pc.ext_wrapper_key,
        ext_inner_names=tuple(pc.ext_inner_props),
    )
    obj.wavelength = 0.3
    obj.wavelength_1 = 0.31
    assert obj.data == {"wavelength": 0.3, "wavelength_1": 0.31}


class TestGroupZeroIsNotAGroup:
    """``_0`` names no group: it must never be read as ``wrapper[-1]`` (the last group)."""

    @pytest.mark.parametrize(
        "name",
        ["mode_0_minimum_outdoor_air_temperature", "mode_minimum_outdoor_air_temperature_0", "mode_01_name"],
    )
    def test_parse(self, name: str) -> None:
        from idfkit.objects import parse_extensible_index

        ext = frozenset(_pc("ZoneHVAC:HybridUnitaryHVAC", (24, 1, 0)).ext_field_names)
        assert parse_extensible_index(name, ext) == (None, 0)

    def test_parse_rejects_non_ascii_digits(self) -> None:
        from idfkit.objects import parse_extensible_index

        ext = frozenset({"vertex_x_coordinate"})
        assert parse_extensible_index("vertex_x_coordinate_" + chr(0xB2), ext) == (None, 0)
        assert parse_extensible_index("vertex_" + chr(0x661) + "_x_coordinate", ext) == (None, 0)
        assert parse_extensible_index("vertex_x_coordinate_12", ext) == ("vertex_x_coordinate", 12)

    def test_setattr_leaves_the_last_group_alone(self) -> None:
        from idfkit.exceptions import InvalidFieldError

        doc = new_document(version=(24, 1, 0))
        modes = [{"mode_name": "M1"}, {"mode_name": "M2", "mode_minimum_outdoor_air_temperature": 5.0}]
        obj = _add(doc, "ZoneHVAC:HybridUnitaryHVAC", modes=modes)
        # Not a field of mode 0 and not a group: a strict document refuses it as unknown.
        with pytest.raises(InvalidFieldError):
            obj.mode_0_minimum_outdoor_air_temperature = 99.0
        assert obj.data["modes"] == modes

    def test_add_refuses_group_zero(self) -> None:
        from idfkit.exceptions import InvalidFieldError

        doc = new_document(version=(24, 1, 0))
        with pytest.raises(InvalidFieldError):
            _add(doc, "BuildingSurface:Detailed", vertex_0_x_coordinate=1.0)
