"""Fixed fields whose names fit a flat-extensible pattern stay fixed fields.

Some types have positional fields named like an eppy-style flat spelling of their own
extensible group: ``MaterialProperty:GlazingSpectralData`` has fixed ``wavelength_1`` ..
``back_reflectance_4`` beside an ``extensions`` group of ``wavelength`` / ``transmittance`` /
..., ``Site:SpectrumData`` has fixed ``wavelength`` / ``spectrum`` / ``wavelength_1`` /
``spectrum_2`` beside a ``wavelength`` / ``spectrum`` group, and ``ZoneHVAC:HybridUnitaryHVAC``
has fixed ``mode_0_*`` fields beside a ``modes`` group of ``mode_*``. A real field must never
be folded into the extensible wrapper, refused as legacy-flat, or read from a group.
"""

from __future__ import annotations

import json
import warnings
from pathlib import Path
from typing import Any

import pytest

from idfkit import LATEST_VERSION, get_schema, load_epjson, load_idf, new_document, save_epjson, save_idf
from idfkit.document import IDFDocument
from idfkit.objects import parse_extensible_index

VERSIONS = [(9, 2, 0), (24, 1, 0), LATEST_VERSION]
TYPES = ["MaterialProperty:GlazingSpectralData", "Site:SpectrumData", "ZoneHVAC:HybridUnitaryHVAC"]
CASES = [pytest.param(t, v, id=f"{t}-{'.'.join(map(str, v))}") for t in TYPES for v in VERSIONS]


def _lookalikes(obj_type: str, version: tuple[int, int, int]) -> list[str]:
    """The fixed fields of *obj_type* a flat-extensible pattern alone would claim."""
    pc = get_schema(version).get_parsing_cache(obj_type)
    assert pc is not None
    ext = frozenset(pc.ext_field_names)
    return [f for f in pc.field_names if parse_extensible_index(f, ext)[0] is not None]


def _value(obj_type: str, version: tuple[int, int, int], field: str, i: int) -> Any:
    pc = get_schema(version).get_parsing_cache(obj_type)
    assert pc is not None
    if pc.field_types.get(field) in ("number", "integer"):
        return round(0.3 + i * 0.01, 4)
    return f"Table {i}"


def _fixed_values(obj_type: str, version: tuple[int, int, int]) -> dict[str, Any]:
    return {f: _value(obj_type, version, f, i) for i, f in enumerate(_lookalikes(obj_type, version))}


def _one_group(obj_type: str, version: tuple[int, int, int]) -> tuple[str, dict[str, Any]]:
    pc = get_schema(version).get_parsing_cache(obj_type)
    assert pc is not None
    assert pc.ext_wrapper_key is not None
    first = pc.ext_field_names[0]
    value = 0.9 if pc.field_types.get(first) in ("number", "integer") else "Group Table"
    return pc.ext_wrapper_key, {first: value}


def _add(doc: IDFDocument, obj_type: str, **fields: Any) -> Any:
    name = "Obj" if get_schema(doc.version).has_name(obj_type) else ""
    with warnings.catch_warnings():
        warnings.simplefilter("error", DeprecationWarning)
        return doc.add(obj_type, name, validate=False, **fields)


def test_every_case_has_lookalikes() -> None:
    for obj_type in TYPES:
        for version in VERSIONS:
            assert _lookalikes(obj_type, version), (obj_type, version)


def test_parse_extensible_index_honours_fixed() -> None:
    ext = frozenset({"wavelength", "spectrum"})
    assert parse_extensible_index("wavelength_1", ext) == ("wavelength", 1)
    assert parse_extensible_index("wavelength_1", ext, {"wavelength_1"}) == (None, 0)
    assert parse_extensible_index("wavelength", ext, {"wavelength"}) == (None, 0)
    assert parse_extensible_index("wavelength_3", ext, {"wavelength_1"}) == ("wavelength", 3)


@pytest.mark.parametrize(("obj_type", "version"), CASES)
def test_add_keeps_fixed_fields(obj_type: str, version: tuple[int, int, int]) -> None:
    doc = new_document(version=version)
    fixed = _fixed_values(obj_type, version)
    wrapper, group = _one_group(obj_type, version)
    obj = _add(doc, obj_type, **fixed, **{wrapper: [group]})
    for field, value in fixed.items():
        assert obj.data[field] == value
        assert getattr(obj, field) == value
    assert obj.data[wrapper] == [group]


def test_spectrum_data_wavelength_and_wavelength_1_both_kept() -> None:
    doc = new_document(version=(24, 1, 0))
    obj = _add(doc, "Site:SpectrumData", spectrum_data_type="Solar", wavelength=0.3, wavelength_1=0.305)
    assert obj.data == {"spectrum_data_type": "Solar", "wavelength": 0.3, "wavelength_1": 0.305}


def test_glazing_spectral_data_idf_output_not_shifted() -> None:
    doc = new_document(version=(24, 1, 0))
    _add(
        doc,
        "MaterialProperty:GlazingSpectralData",
        wavelength_1=0.3,
        transmittance_1=0.1,
        front_reflectance_1=0.05,
        back_reflectance_1=0.06,
        extensions=[{"wavelength": 0.5, "transmittance": 0.2, "front_reflectance": 0.07, "back_reflectance": 0.08}],
    )
    from idfkit import write_idf

    text = write_idf(doc)
    assert "0.3,                       !- Wavelength 1" in text
    body = text.split("MaterialProperty:GlazingSpectralData,")[1].split(";")[0]
    values = [line.split("!-")[0].strip().rstrip(",") for line in body.strip().splitlines()]
    # Name, 4 set fixed fields, 12 blank fixed fields, then the extensible group.
    assert values[1:5] == ["0.3", "0.1", "0.05", "0.06"]
    assert values[5:17] == [""] * 12
    assert values[17:] == ["0.5", "0.2", "0.07", "0.08"]


@pytest.mark.parametrize(("obj_type", "version"), CASES)
def test_setattr_and_update_write_fixed_fields(obj_type: str, version: tuple[int, int, int]) -> None:
    doc = new_document(version=version)
    wrapper, group = _one_group(obj_type, version)
    obj = _add(doc, obj_type, **{wrapper: [group]})
    fixed = _fixed_values(obj_type, version)
    first, *rest = fixed
    with warnings.catch_warnings():
        warnings.simplefilter("error", DeprecationWarning)
        setattr(obj, first, fixed[first])
        obj.update({k: fixed[k] for k in rest})
    for field, value in fixed.items():
        assert obj.data[field] == value
    assert obj.data[wrapper] == [group]


@pytest.mark.parametrize(("obj_type", "version"), CASES)
def test_unset_fixed_field_reads_none_not_group(obj_type: str, version: tuple[int, int, int]) -> None:
    doc = new_document(version=version)
    wrapper, group = _one_group(obj_type, version)
    obj = _add(doc, obj_type, **{wrapper: [group, group]})
    with warnings.catch_warnings():
        warnings.simplefilter("error", DeprecationWarning)
        for field in _lookalikes(obj_type, version):
            assert getattr(obj, field) is None


@pytest.mark.parametrize(("obj_type", "version"), CASES)
def test_round_trip_idf_epjson(obj_type: str, version: tuple[int, int, int], tmp_path: Path) -> None:
    doc = new_document(version=version)
    fixed = _fixed_values(obj_type, version)
    wrapper, group = _one_group(obj_type, version)
    _add(doc, obj_type, **fixed, **{wrapper: [group]})

    idf_path = tmp_path / "m.idf"
    save_idf(doc, idf_path)
    from_idf = load_idf(idf_path, version=version)
    obj = from_idf[obj_type].first()
    assert obj is not None
    for field, value in fixed.items():
        assert obj.data[field] == value
    assert obj.data[wrapper] == [group]

    json_path = tmp_path / "m.epJSON"
    save_epjson(from_idf, json_path)
    raw = json.loads(json_path.read_text())
    stored = next(iter(raw[obj_type].values()))
    for field, value in fixed.items():
        assert stored[field] == value
    assert stored[wrapper] == [group]

    with warnings.catch_warnings():
        warnings.simplefilter("error", DeprecationWarning)
        from_json = load_epjson(json_path, version=version)
    obj = from_json[obj_type].first()
    assert obj is not None
    for field, value in fixed.items():
        assert obj.data[field] == value
    assert obj.data[wrapper] == [group]

    idf_path_2 = tmp_path / "m2.idf"
    save_idf(from_json, idf_path_2)
    again = load_idf(idf_path_2, version=version)[obj_type].first()
    assert again is not None
    assert again.data == obj.data
