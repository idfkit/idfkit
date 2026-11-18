"""A field typed non-optional on read is one every release requires, and reading it never gives None."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from idfkit import IDFObject, load_epjson, load_idf, new_document
from idfkit._read_required import GROUP_READ_REQUIRED, READ_REQUIRED
from idfkit.exceptions import MissingRequiredFieldError, ValidationFailedError
from idfkit.schema import get_schema
from idfkit.validation import validate_document
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


# Extensible groups: a key every release whose group has it requires reads as its value type.

_WALL = """Version,24.1;
Zone, Z;
BuildingSurface:Detailed, W, Wall, , Z, , Outdoors, , SunExposed, WindExposed, , 4,
 0,0,3, 0,0,, 1,0,0, 1,0,3;
"""


def _group_required(schema_version: tuple[int, int, int]) -> dict[str, tuple[set[str], set[str]]]:
    """Each type's group keys in one release: those required with no default, and the others."""
    schema = get_schema(schema_version)
    keys: dict[str, tuple[set[str], set[str]]] = {}
    for obj_type in schema.object_types:
        pc = schema.get_parsing_cache(obj_type)
        if pc is None or not pc.ext_wrapper_key:
            continue
        inner = schema.get_inner_schema(obj_type) or {}
        items = inner.get("properties", {}).get(pc.ext_wrapper_key, {}).get("items", {})
        properties = items.get("properties", {})
        listed = {k for k in items.get("required", []) if "default" not in properties.get(k, {})}
        keys[obj_type] = (listed & set(properties), set(properties) - listed)
    return keys


def test_the_group_table_lists_every_key_required_everywhere_it_exists() -> None:
    required: dict[str, set[str]] = {}
    optional: dict[str, set[str]] = {}
    for version in ENERGYPLUS_VERSIONS:
        for obj_type, (req, opt) in _group_required(version).items():
            required.setdefault(obj_type, set()).update(req)
            optional.setdefault(obj_type, set()).update(opt)
    expected = {t: keys - optional.get(t, set()) for t, keys in required.items()}
    assert {t: set(k) for t, k in GROUP_READ_REQUIRED.items()} == {t: k for t, k in expected.items() if k}
    assert set(GROUP_READ_REQUIRED["BuildingSurface:Detailed"]) == {
        "vertex_x_coordinate",
        "vertex_y_coordinate",
        "vertex_z_coordinate",
    }
    # Required in some releases and optional in others: it stays optional everywhere.
    assert "EnergyManagementSystem:Program" not in GROUP_READ_REQUIRED


def _wall(tmp_path: Path) -> IDFObject:
    path = tmp_path / "w.idf"
    path.write_text(_WALL)
    return load_idf(path)["BuildingSurface:Detailed"]["W"]


def test_a_group_without_a_required_key_raises_on_read(tmp_path: Path) -> None:
    wall = _wall(tmp_path)
    vertex = wall.vertices[1]
    with pytest.raises(MissingRequiredFieldError, match=r"'vertex_z_coordinate' of vertices\[1\]") as caught:
        _ = vertex.vertex_z_coordinate
    assert isinstance(caught.value, AttributeError)
    assert (caught.value.obj_type, caught.value.obj_name) == ("BuildingSurface:Detailed", "W")
    assert (caught.value.field_name, caught.value.wrapper_key, caught.value.group_index) == (
        "vertex_z_coordinate",
        "vertices",
        2,
    )
    with pytest.raises(MissingRequiredFieldError):
        _ = vertex["vertex_z_coordinate"]
    # The untyped reads still answer None.
    assert vertex.get("vertex_z_coordinate") is None
    assert vertex.get("vertex_z_coordinate", 0.0) == 0.0
    assert getattr(vertex, "vertex_z_coordinate", None) is None
    assert dict(vertex.items())["vertex_z_coordinate"] is None
    assert vertex.values() == [0.0, 0.0, None]
    assert vertex.vertex_x_coordinate == 0.0
    # A name that is not a key of the group is still an error, not a missing value.
    with pytest.raises(AttributeError, match="not an extensible field"):
        vertex.get("vertex_w_coordinate")


def test_as_dict_and_as_list_do_not_give_a_dict_missing_a_required_key(tmp_path: Path) -> None:
    wall = _wall(tmp_path)
    assert wall.vertices[0].as_dict() == {
        "vertex_x_coordinate": 0.0,
        "vertex_y_coordinate": 0.0,
        "vertex_z_coordinate": 3.0,
    }
    with pytest.raises(MissingRequiredFieldError, match=r"vertices\[1\]"):
        wall.vertices[1].as_dict()
    with pytest.raises(MissingRequiredFieldError, match=r"vertices\[1\]"):
        wall.vertices.as_list()
    # repr, equality, pop and the stored data show the group as it is.
    assert "vertex_z_coordinate': 3.0" in repr(wall.vertices)
    assert "vertices[1]" in repr(wall.vertices[1])
    assert wall.vertices == wall.vertices
    assert wall.vertices[1] == {"vertex_x_coordinate": 0.0, "vertex_y_coordinate": 0.0}
    assert wall.data["vertices"][1] == {"vertex_x_coordinate": 0.0, "vertex_y_coordinate": 0.0}
    # Setting the key makes the snapshot whole again.
    wall.vertices[1].vertex_z_coordinate = 0.0
    assert [p["vertex_z_coordinate"] for p in wall.vertices.as_list()] == [3.0, 0.0, 0.0, 3.0]


def test_a_stale_group_view_raises_for_a_required_key(tmp_path: Path) -> None:
    wall = _wall(tmp_path)
    last = wall.vertices[3]
    wall.vertices.pop()
    with pytest.raises(MissingRequiredFieldError):
        _ = last.vertex_x_coordinate
    assert last.get("vertex_x_coordinate") is None


def test_an_optional_group_key_still_reads_none() -> None:
    doc = new_document()
    doc.add("Zone", "Z")
    zone_list = doc.add("ZoneList", "L", zones=[{"zone_name": "Z"}])
    assert zone_list.zones[0].zone_name == "Z"
    # EMS program lines are required by some releases only, so an unset one reads None.
    program = doc.add("EnergyManagementSystem:Program", "P", validate=False)
    program.lines.append({})
    assert program.lines[0].program_line is None


def test_add_refuses_a_group_without_a_required_key() -> None:
    doc = new_document()
    doc.add("Zone", "Z")
    fields = {
        "surface_type": "Wall",
        "zone_name": "Z",
        "outside_boundary_condition": "Outdoors",
    }
    with pytest.raises(ValidationFailedError, match=r"vertices\[1\]\.vertex_z_coordinate"):
        doc.add(
            "BuildingSurface:Detailed",
            "W",
            **fields,
            vertices=[
                {"vertex_x_coordinate": 0.0, "vertex_y_coordinate": 0.0, "vertex_z_coordinate": 0.0},
                {"vertex_x_coordinate": 1.0, "vertex_y_coordinate": 0.0},
            ],
        )
    # validate=False stores it; validate_document reports each missing key where it is.
    doc.add("BuildingSurface:Detailed", "V", **fields, vertices=[{"vertex_x_coordinate": 0.0}], validate=False)
    missing = {e.field for e in validate_document(doc).errors if e.code == "E001"}
    assert missing == {"vertices[0].vertex_y_coordinate", "vertices[0].vertex_z_coordinate"}


@pytest.mark.parametrize("version", ENERGYPLUS_VERSIONS, ids=lambda v: ".".join(map(str, v)))
def test_every_listed_group_key_is_required_in_each_release_that_has_it(version: tuple[int, int, int]) -> None:
    for obj_type, (_req, opt) in _group_required(version).items():
        # The run time raises only where every release agrees, so no static view types it optional.
        assert not set(GROUP_READ_REQUIRED.get(obj_type, ())) & opt, (obj_type, version)
