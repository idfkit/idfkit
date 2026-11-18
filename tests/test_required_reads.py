"""A field typed non-optional on read is one every release requires, and reading it never gives None."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from idfkit import load_epjson, load_idf, new_document
from idfkit._read_required import READ_REQUIRED
from idfkit.exceptions import MissingRequiredFieldError
from idfkit.schema import get_schema
from idfkit.versions import ENERGYPLUS_VERSIONS


@pytest.mark.parametrize("version", ENERGYPLUS_VERSIONS, ids=lambda v: ".".join(map(str, v)))
def test_every_listed_field_is_required_with_no_default_in_each_release_that_has_it(
    version: tuple[int, int, int],
) -> None:
    # The run time raises only where every release agrees, so the error never fires for a field some
    # static view (AnyIDFDocument, an older release's class) types as optional.
    schema = get_schema(version)
    for obj_type, fields in READ_REQUIRED.items():
        inner = schema.get_inner_schema(obj_type) if obj_type in schema.object_types else None
        if inner is None:
            continue
        properties = inner.get("properties", {})
        listed = set(inner.get("required", []))
        for field in set(fields) & set(schema.get_field_names(obj_type)):
            assert field in listed, (obj_type, field, version)
            assert "default" not in properties.get(field, {}), (obj_type, field, version)


def test_a_created_object_reads_its_required_fields() -> None:
    doc = new_document()
    mat = doc.materials.add(
        "B", roughness="Rough", thickness=0.1, conductivity=0.7, density=1900.0, specific_heat=800.0
    )
    assert mat.thickness / mat.conductivity == pytest.approx(0.1 / 0.7)


def test_a_loaded_object_without_a_required_field_raises_on_read(tmp_path: Path) -> None:
    path = tmp_path / "m.idf"
    path.write_text("Version,24.1;\nMaterial, M1, Rough, , 0.7, 1900, 800;\n")
    mat = load_idf(path).materials["M1"]
    with pytest.raises(MissingRequiredFieldError, match="'thickness'") as caught:
        _ = mat.thickness
    assert isinstance(caught.value, AttributeError)
    assert getattr(mat, "thickness", None) is None
    assert mat.get("thickness") is None
    assert mat.conductivity == 0.7


def test_epjson_blank_and_null_are_unset(tmp_path: Path) -> None:
    path = tmp_path / "m.epJSON"
    path.write_text(
        json.dumps({
            "Version": {"Version 1": {"version_identifier": "24.1"}},
            "Zone": {"Z": {"ceiling_height": "", "volume": None}},
            "Material": {
                "M": {
                    "roughness": "Rough",
                    "thickness": None,
                    "conductivity": 0.7,
                    "density": 1900,
                    "specific_heat": 800,
                }
            },
        })
    )
    doc = load_epjson(path)
    zone = doc.zones["Z"]
    assert zone.ceiling_height is None
    assert zone.volume is None
    with pytest.raises(MissingRequiredFieldError):
        _ = doc.materials["M"].thickness


def test_add_stores_a_blank_as_unset() -> None:
    doc = new_document()
    zone = doc.add("Zone", "Z", {"ceiling_height": ""})
    assert "ceiling_height" not in zone.data
    assert zone.ceiling_height is None


def test_the_table_lists_every_field_required_everywhere_it_exists() -> None:
    # The other direction: a field missing from the table reads | None and returns None when unset,
    # which is honest but loses the guarantee; the table must be the whole rule, not part of it.
    required: dict[str, set[str]] = {}
    optional: dict[str, set[str]] = {}
    for version in ENERGYPLUS_VERSIONS:
        schema = get_schema(version)
        for obj_type in schema.object_types:
            inner = schema.get_inner_schema(obj_type) or {}
            properties = inner.get("properties", {})
            listed = {f for f in inner.get("required", []) if "default" not in properties.get(f, {})}
            for field in schema.get_field_names(obj_type):
                if field.isidentifier():
                    (required if field in listed else optional).setdefault(obj_type, set()).add(field)
    expected = {t: fields - optional.get(t, set()) for t, fields in required.items()}
    assert {t: set(f) for t, f in READ_REQUIRED.items()} == {t: f for t, f in expected.items() if f}
