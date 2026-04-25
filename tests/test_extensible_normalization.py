"""
Tests for canonical-shape extensible-group normalization (issue #135).

The bug: ``write_idf`` produced broken output whenever an object's
extensible-group data sat in canonical epJSON shape
(``{"vertices": [{...}, ...]}``) inside ``obj.data``. Two trigger paths:

1. ``doc.add(vertices=[{...}, ...])`` — IDF writer emitted Python ``repr(dict)``.
2. ``load_epjson`` of a canonical-shape file — IDF writer silently dropped
   the entire array.

Test gap that allowed the bug to ship: the existing roundtrip tests in
``tests/test_epjson_roundtrip.py`` start every case from IDF text. Since
``load_idf`` already produces flat shape, the canonical
``{"vertices": [...]}`` form never enters ``obj.data`` during those tests.
The two trigger paths above were therefore unexercised.

This file fills that gap with a 5-entry x 2-output x 2-type matrix that
exercises every combination where the canonical and flat shapes can collide.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest

from idfkit import get_schema, load_epjson, load_idf, new_document, write_epjson, write_idf
from idfkit.objects import expand_extensible_array

# v24.1.0 is the default test schema (matches conftest.py)
VERSION = (24, 1, 0)
VERSION_ID = "24.1"

# Reference flat-shape representations used to compare every (entry, output) cell.
SURFACE_FLAT: dict[str, Any] = {
    "surface_type": "Wall",
    "construction_name": "C",
    "zone_name": "Z1",
    "outside_boundary_condition": "Outdoors",
    "vertex_x_coordinate": 0.0,
    "vertex_y_coordinate": 0.0,
    "vertex_z_coordinate": 3.0,
    "vertex_x_coordinate_2": 0.0,
    "vertex_y_coordinate_2": 0.0,
    "vertex_z_coordinate_2": 0.0,
    "vertex_x_coordinate_3": 5.0,
    "vertex_y_coordinate_3": 0.0,
    "vertex_z_coordinate_3": 0.0,
    "vertex_x_coordinate_4": 5.0,
    "vertex_y_coordinate_4": 0.0,
    "vertex_z_coordinate_4": 3.0,
}

SURFACE_CANONICAL_ITEMS: list[dict[str, Any]] = [
    {"vertex_x_coordinate": 0.0, "vertex_y_coordinate": 0.0, "vertex_z_coordinate": 3.0},
    {"vertex_x_coordinate": 0.0, "vertex_y_coordinate": 0.0, "vertex_z_coordinate": 0.0},
    {"vertex_x_coordinate": 5.0, "vertex_y_coordinate": 0.0, "vertex_z_coordinate": 0.0},
    {"vertex_x_coordinate": 5.0, "vertex_y_coordinate": 0.0, "vertex_z_coordinate": 3.0},
]

SCHEDULE_FLAT: dict[str, Any] = {
    "schedule_type_limits_name": "Fraction",
    "interpolate_to_timestep": "No",
    "time": "08:00",
    "value_until_time": 0.1,
    "time_2": "18:00",
    "value_until_time_2": 0.9,
    "time_3": "24:00",
    "value_until_time_3": 0.1,
}

SCHEDULE_CANONICAL_ITEMS: list[dict[str, Any]] = [
    {"time": "08:00", "value_until_time": 0.1},
    {"time": "18:00", "value_until_time": 0.9},
    {"time": "24:00", "value_until_time": 0.1},
]


def _surface_idf_flat() -> str:
    """IDF text for a 4-vertex wall (flat shape — what load_idf produces)."""
    return f"""Version,{VERSION_ID};

GlobalGeometryRules,
  UpperLeftCorner,
  Counterclockwise,
  Relative;

Zone,
  Z1;

BuildingSurface:Detailed,
  WallA, Wall, C, Z1, , Outdoors, , , , , ,
  0, 0, 3,
  0, 0, 0,
  5, 0, 0,
  5, 0, 3;
"""


def _schedule_idf_flat() -> str:
    return f"""Version,{VERSION_ID};

ScheduleTypeLimits,
  Fraction, 0, 1, Continuous;

Schedule:Day:Interval,
  DayA, Fraction, No,
  08:00, 0.1,
  18:00, 0.9,
  24:00, 0.1;
"""


def _surface_epjson(*, canonical: bool) -> dict[str, Any]:
    surface_fields: dict[str, Any] = {
        "surface_type": "Wall",
        "construction_name": "C",
        "zone_name": "Z1",
        "outside_boundary_condition": "Outdoors",
    }
    if canonical:
        surface_fields["vertices"] = [dict(item) for item in SURFACE_CANONICAL_ITEMS]
    else:
        surface_fields.update({k: v for k, v in SURFACE_FLAT.items() if k.startswith("vertex_")})
    return {
        "Version": {"Version 1": {"version_identifier": VERSION_ID}},
        "GlobalGeometryRules": {
            "GlobalGeometryRules 1": {
                "starting_vertex_position": "UpperLeftCorner",
                "vertex_entry_direction": "Counterclockwise",
                "coordinate_system": "Relative",
            }
        },
        "Zone": {"Z1": {}},
        "BuildingSurface:Detailed": {"WallA": surface_fields},
    }


def _schedule_epjson(*, canonical: bool) -> dict[str, Any]:
    fields: dict[str, Any] = {
        "schedule_type_limits_name": "Fraction",
        "interpolate_to_timestep": "No",
    }
    if canonical:
        fields["data"] = [dict(item) for item in SCHEDULE_CANONICAL_ITEMS]
    else:
        fields.update({
            k: v
            for k, v in SCHEDULE_FLAT.items()
            if k != "schedule_type_limits_name" and k != "interpolate_to_timestep"
        })
    return {
        "Version": {"Version 1": {"version_identifier": VERSION_ID}},
        "ScheduleTypeLimits": {
            "Fraction": {"lower_limit_value": 0.0, "upper_limit_value": 1.0, "numeric_type": "Continuous"}
        },
        "Schedule:Day:Interval": {"DayA": fields},
    }


# Per-type test parameters: (object_type, name, expected_flat, idf_text, canonical_items, kw_for_add_canonical, kw_for_add_flat)
TYPE_PARAMS = [
    pytest.param(
        "BuildingSurface:Detailed",
        "WallA",
        SURFACE_FLAT,
        _surface_idf_flat(),
        SURFACE_CANONICAL_ITEMS,
        id="BuildingSurfaceDetailed",
    ),
    pytest.param(
        "Schedule:Day:Interval",
        "DayA",
        SCHEDULE_FLAT,
        _schedule_idf_flat(),
        SCHEDULE_CANONICAL_ITEMS,
        id="ScheduleDayInterval",
    ),
]


def _entry(
    entry_shape: str,
    obj_type: str,
    name: str,
    flat: dict[str, Any],
    idf_text: str,
    canonical_items: list[dict[str, Any]],
    tmp_path: Path,
):
    """Build a document via the requested entry shape and return (doc, obj)."""
    if entry_shape == "idf_flat":
        p = tmp_path / "in.idf"
        p.write_text(idf_text)
        doc = load_idf(p)
    elif entry_shape == "epjson_canonical":
        ep = (
            _surface_epjson(canonical=True)
            if obj_type == "BuildingSurface:Detailed"
            else _schedule_epjson(canonical=True)
        )
        p = tmp_path / "in.epjson"
        p.write_text(json.dumps(ep))
        doc = load_epjson(p)
    elif entry_shape == "epjson_flat":
        ep = (
            _surface_epjson(canonical=False)
            if obj_type == "BuildingSurface:Detailed"
            else _schedule_epjson(canonical=False)
        )
        p = tmp_path / "in.epjson"
        p.write_text(json.dumps(ep))
        doc = load_epjson(p)
    elif entry_shape == "add_canonical":
        doc = new_document(version=VERSION, strict=False)
        if obj_type == "BuildingSurface:Detailed":
            doc.add("Zone", "Z1")
            doc.add(
                obj_type,
                name,
                surface_type="Wall",
                construction_name="C",
                zone_name="Z1",
                outside_boundary_condition="Outdoors",
                vertices=[dict(item) for item in canonical_items],
                validate=False,
            )
        else:
            doc.add("ScheduleTypeLimits", "Fraction", validate=False)
            doc.add(
                obj_type,
                name,
                schedule_type_limits_name="Fraction",
                interpolate_to_timestep="No",
                data=[dict(item) for item in canonical_items],
                validate=False,
            )
    elif entry_shape == "add_flat":
        doc = new_document(version=VERSION, strict=False)
        if obj_type == "BuildingSurface:Detailed":
            doc.add("Zone", "Z1")
            doc.add(
                obj_type,
                name,
                surface_type="Wall",
                construction_name="C",
                zone_name="Z1",
                outside_boundary_condition="Outdoors",
                **{k: v for k, v in flat.items() if k.startswith("vertex_")},
                validate=False,
            )
        else:
            doc.add("ScheduleTypeLimits", "Fraction", validate=False)
            doc.add(
                obj_type,
                name,
                schedule_type_limits_name="Fraction",
                interpolate_to_timestep="No",
                **{k: v for k, v in flat.items() if k.startswith("time") or k.startswith("value_until_time")},
                validate=False,
            )
    else:
        raise AssertionError(f"unknown entry_shape: {entry_shape}")  # noqa: TRY003

    obj = doc[obj_type][name]
    return doc, obj


def _assert_storage_is_flat(obj: Any, expected_flat: dict[str, Any]) -> None:
    """Storage in obj.data must be uniformly flat regardless of entry shape."""
    # No wrapper key should leak into storage.
    assert "vertices" not in obj.data, f"wrapper key leaked into obj.data: {obj.data!r}"
    assert "data" not in obj.data or obj.obj_type != "Schedule:Day:Interval", f"wrapper key 'data' leaked: {obj.data!r}"
    # Every expected flat key must be present and equal.
    for k, v in expected_flat.items():
        assert k in obj.data, f"missing flat key {k!r} (have {list(obj.data)})"
        assert obj.data[k] == v, f"flat key {k!r}: got {obj.data[k]!r}, expected {v!r}"


ENTRY_SHAPES = ["idf_flat", "epjson_canonical", "epjson_flat", "add_canonical", "add_flat"]
OUTPUT_FORMATS = ["idf", "epjson"]


@pytest.mark.parametrize("entry_shape", ENTRY_SHAPES)
@pytest.mark.parametrize(
    ("obj_type", "name", "expected_flat", "idf_text", "canonical_items"),
    TYPE_PARAMS,
)
def test_entry_storage_is_flat(
    entry_shape: str,
    obj_type: str,
    name: str,
    expected_flat: dict[str, Any],
    idf_text: str,
    canonical_items: list[dict[str, Any]],
    tmp_path: Path,
) -> None:
    """After every entry path, obj.data is in the canonical flat shape."""
    _, obj = _entry(entry_shape, obj_type, name, expected_flat, idf_text, canonical_items, tmp_path)
    _assert_storage_is_flat(obj, expected_flat)


@pytest.mark.parametrize("output_format", OUTPUT_FORMATS)
@pytest.mark.parametrize("entry_shape", ENTRY_SHAPES)
@pytest.mark.parametrize(
    ("obj_type", "name", "expected_flat", "idf_text", "canonical_items"),
    TYPE_PARAMS,
)
def test_roundtrip_matrix(
    entry_shape: str,
    output_format: str,
    obj_type: str,
    name: str,
    expected_flat: dict[str, Any],
    idf_text: str,
    canonical_items: list[dict[str, Any]],
    tmp_path: Path,
) -> None:
    """5 entry shapes x 2 output formats x 2 object types = the full mixed-shapes matrix.

    For every combination the written output must be (a) shape-correct for the
    target format, and (b) re-parseable into the same flat-shape ``obj.data``.
    """
    _, obj = _entry(entry_shape, obj_type, name, expected_flat, idf_text, canonical_items, tmp_path)
    _assert_storage_is_flat(obj, expected_flat)
    doc = obj.document if hasattr(obj, "document") else None
    # Fall back to fetching doc from the entry — re-run for clarity
    doc, obj = _entry(entry_shape, obj_type, name, expected_flat, idf_text, canonical_items, tmp_path)

    if output_format == "idf":
        out = tmp_path / "out.idf"
        write_idf(doc, out)
        text = out.read_text()
        # No Python dict reprs leaked.
        assert "{" not in text, f"dict repr leaked into IDF: {text}"
        # Per-vertex/per-group comment for the second group must be present.
        if obj_type == "BuildingSurface:Detailed":
            assert "!- Vertex X Coordinate 2" in text
        else:
            assert "!- Time 2" in text or "!- Time" in text  # time fields present
        # Re-parse and compare flat data.
        doc2 = load_idf(out)
        obj2 = doc2[obj_type][name]
        for k, v in expected_flat.items():
            assert obj2.data.get(k) == v, f"IDF roundtrip mismatch on {k!r}"
    else:
        out = tmp_path / "out.epjson"
        write_epjson(doc, out)
        text = out.read_text()
        parsed = json.loads(text)
        body = parsed[obj_type][name]
        # Canonical shape: wrapper key is a list, no flat ext keys present.
        if obj_type == "BuildingSurface:Detailed":
            assert "vertices" in body and isinstance(body["vertices"], list)
            assert len(body["vertices"]) == 4
            for flat_key in expected_flat:
                if flat_key.startswith("vertex_"):
                    assert flat_key not in body, f"flat key {flat_key!r} leaked into epJSON"
        else:
            assert "data" in body and isinstance(body["data"], list)
            assert len(body["data"]) == 3
            for flat_key in expected_flat:
                if flat_key.startswith("time") or flat_key.startswith("value_until_time"):
                    assert flat_key not in body, f"flat key {flat_key!r} leaked into epJSON"
        # Re-parse and compare flat data.
        doc2 = load_epjson(out)
        obj2 = doc2[obj_type][name]
        for k, v in expected_flat.items():
            assert obj2.data.get(k) == v, f"epJSON roundtrip mismatch on {k!r}"


# ---------------------------------------------------------------------------
# Issue #135 reproductions, verbatim
# ---------------------------------------------------------------------------


def test_issue_135_repro_1_doc_add_with_vertices_array(tmp_path: Path) -> None:
    """Issue #135 Repro 1: doc.add with vertices=[{...}, ...] must produce valid IDF."""
    doc = new_document(version=VERSION, strict=True)
    doc.add("Zone", "Z1")
    doc.add(
        "BuildingSurface:Detailed",
        "WallA",
        surface_type="Wall",
        construction_name="C",
        zone_name="Z1",
        outside_boundary_condition="Outdoors",
        vertices=[
            {"vertex_x_coordinate": 0.0, "vertex_y_coordinate": 0.0, "vertex_z_coordinate": 3.0},
            {"vertex_x_coordinate": 0.0, "vertex_y_coordinate": 0.0, "vertex_z_coordinate": 0.0},
            {"vertex_x_coordinate": 5.0, "vertex_y_coordinate": 0.0, "vertex_z_coordinate": 0.0},
            {"vertex_x_coordinate": 5.0, "vertex_y_coordinate": 0.0, "vertex_z_coordinate": 3.0},
        ],
        validate=False,
    )
    p = tmp_path / "out.idf"
    write_idf(doc, p)
    text = p.read_text()
    s = text.index("BuildingSurface:Detailed,")
    e = text.find(";", s) + 1
    block = text[s:e]
    assert "{" not in block, f"dict repr leaked: {block}"
    assert "Vertex X Coordinate 4" in block


def test_issue_135_repro_2_load_epjson_canonical_then_write_idf(tmp_path: Path) -> None:
    """Issue #135 Repro 2: load_epjson canonical -> write_idf must preserve vertices."""
    epjson_data = {
        "Version": {"Version 1": {"version_identifier": VERSION_ID}},
        "GlobalGeometryRules": {
            "GlobalGeometryRules 1": {
                "starting_vertex_position": "UpperLeftCorner",
                "vertex_entry_direction": "Counterclockwise",
                "coordinate_system": "Relative",
            }
        },
        "Zone": {"Z1": {}},
        "BuildingSurface:Detailed": {
            "WallA": {
                "surface_type": "Wall",
                "construction_name": "C",
                "zone_name": "Z1",
                "outside_boundary_condition": "Outdoors",
                "vertices": [
                    {"vertex_x_coordinate": 0.0, "vertex_y_coordinate": 0.0, "vertex_z_coordinate": 3.0},
                    {"vertex_x_coordinate": 5.0, "vertex_y_coordinate": 0.0, "vertex_z_coordinate": 0.0},
                ],
            }
        },
    }
    pj = tmp_path / "in.epjson"
    pj.write_text(json.dumps(epjson_data))
    doc = load_epjson(pj)
    pi = tmp_path / "out.idf"
    write_idf(doc, pi)
    text = pi.read_text()
    s = text.index("BuildingSurface:Detailed,")
    e = text.find(";", s) + 1
    block = text[s:e]
    assert "Vertex X Coordinate 2" in block
    assert "{" not in block


# ---------------------------------------------------------------------------
# Edge cases
# ---------------------------------------------------------------------------


def test_mixed_input_raises() -> None:
    """Passing both wrapper list AND a flat extensible key must raise."""
    doc = new_document(version=VERSION, strict=False)
    doc.add("Zone", "Z1")
    with pytest.raises(ValueError, match="cannot mix 'vertices=\\[\\.\\.\\.\\]'"):
        doc.add(
            "BuildingSurface:Detailed",
            "WallA",
            surface_type="Wall",
            construction_name="C",
            zone_name="Z1",
            outside_boundary_condition="Outdoors",
            vertices=[{"vertex_x_coordinate": 0.0, "vertex_y_coordinate": 0.0, "vertex_z_coordinate": 3.0}],
            vertex_x_coordinate_2=5.0,
            validate=False,
        )


def test_empty_array_drops_wrapper(tmp_path: Path) -> None:
    """An empty vertices array yields no extensible storage and omits the wrapper on write."""
    doc = new_document(version=VERSION, strict=False)
    doc.add("Zone", "Z1")
    doc.add(
        "BuildingSurface:Detailed",
        "WallA",
        surface_type="Wall",
        construction_name="C",
        zone_name="Z1",
        outside_boundary_condition="Outdoors",
        vertices=[],
        validate=False,
    )
    obj = doc["BuildingSurface:Detailed"]["WallA"]
    assert "vertices" not in obj.data
    assert not any(k.startswith("vertex_") for k in obj.data)
    p = tmp_path / "out.epjson"
    write_epjson(doc, p)
    body = json.loads(p.read_text())["BuildingSurface:Detailed"]["WallA"]
    assert "vertices" not in body


def test_sparse_groups_survive_without_fabrication(tmp_path: Path) -> None:
    """Flat keys with a gap (e.g., only _3 present, no _2) round-trip without padding."""
    epjson_data = {
        "Version": {"Version 1": {"version_identifier": VERSION_ID}},
        "GlobalGeometryRules": {
            "GlobalGeometryRules 1": {
                "starting_vertex_position": "UpperLeftCorner",
                "vertex_entry_direction": "Counterclockwise",
                "coordinate_system": "Relative",
            }
        },
        "Zone": {"Z1": {}},
        "BuildingSurface:Detailed": {
            "WallA": {
                "surface_type": "Wall",
                "construction_name": "C",
                "zone_name": "Z1",
                "outside_boundary_condition": "Outdoors",
                # Sparse: groups 1 and 3 only, no 2.
                "vertex_x_coordinate": 0.0,
                "vertex_y_coordinate": 0.0,
                "vertex_z_coordinate": 3.0,
                "vertex_x_coordinate_3": 5.0,
                "vertex_y_coordinate_3": 0.0,
                "vertex_z_coordinate_3": 0.0,
            }
        },
    }
    pj = tmp_path / "in.epjson"
    pj.write_text(json.dumps(epjson_data))
    doc = load_epjson(pj)
    p = tmp_path / "out.epjson"
    write_epjson(doc, p)
    body = json.loads(p.read_text())["BuildingSurface:Detailed"]["WallA"]
    assert "vertices" in body
    # Two non-empty groups, emitted in numeric order, no padding.
    assert len(body["vertices"]) == 2
    assert body["vertices"][0]["vertex_z_coordinate"] == 3.0
    assert body["vertices"][1]["vertex_x_coordinate"] == 5.0


def test_unknown_inner_key_raises() -> None:
    """An unrecognised inner key inside a wrapper item raises ValueError."""
    doc = new_document(version=VERSION, strict=False)
    doc.add("Zone", "Z1")
    with pytest.raises(ValueError, match="Unknown extensible field"):
        doc.add(
            "BuildingSurface:Detailed",
            "WallA",
            surface_type="Wall",
            construction_name="C",
            zone_name="Z1",
            outside_boundary_condition="Outdoors",
            vertices=[{"vertex_x_coordinate": 0.0, "bogus": 1.0}],
            validate=False,
        )


def test_branchlist_canonical_roundtrip(tmp_path: Path) -> None:
    """Regression: BranchList uses 'branches' as wrapper key — ensure canonical input flattens."""
    epjson_data = {
        "Version": {"Version 1": {"version_identifier": VERSION_ID}},
        "BranchList": {
            "MyBranches": {
                "branches": [
                    {"branch_name": "B1"},
                    {"branch_name": "B2"},
                    {"branch_name": "B3"},
                ]
            }
        },
    }
    pj = tmp_path / "in.epjson"
    pj.write_text(json.dumps(epjson_data))
    doc = load_epjson(pj)
    obj = doc["BranchList"]["MyBranches"]
    assert "branches" not in obj.data
    assert obj.data.get("branch_name") == "B1"
    assert obj.data.get("branch_name_2") == "B2"
    assert obj.data.get("branch_name_3") == "B3"
    # IDF round-trip.
    pi = tmp_path / "out.idf"
    write_idf(doc, pi)
    idf = pi.read_text()
    assert "B1" in idf and "B2" in idf and "B3" in idf
    assert "{" not in idf
    # epJSON round-trip emits canonical.
    pj2 = tmp_path / "out.epjson"
    write_epjson(doc, pj2)
    body = json.loads(pj2.read_text())["BranchList"]["MyBranches"]
    assert body["branches"] == [{"branch_name": "B1"}, {"branch_name": "B2"}, {"branch_name": "B3"}]


def test_get_extensible_wrapper_key_helper() -> None:
    """The schema helper resolves wrapper keys for known extensible types and None otherwise."""
    s = get_schema(VERSION)
    assert s.get_extensible_wrapper_key("BuildingSurface:Detailed") == "vertices"
    assert s.get_extensible_wrapper_key("Schedule:Day:Interval") == "data"
    assert s.get_extensible_wrapper_key("BranchList") == "branches"
    assert s.get_extensible_wrapper_key("Zone") is None
    assert s.get_extensible_wrapper_key("DoesNotExist") is None


def test_expand_extensible_array_user_style_aliases() -> None:
    """expand_extensible_array tolerates user-style aliases inside items."""
    exts = frozenset({"vertex_x_coordinate", "vertex_y_coordinate", "vertex_z_coordinate"})
    out = expand_extensible_array(
        [
            {"vertex_1_x_coordinate": 1.0, "vertex_1_y_coordinate": 2.0, "vertex_1_z_coordinate": 3.0},
            {"vertex_2_x_coordinate": 4.0, "vertex_2_y_coordinate": 5.0, "vertex_2_z_coordinate": 6.0},
        ],
        exts,
    )
    # Array position drives the group index; alias indices inside items are
    # normalized but the array position wins.
    assert out["vertex_x_coordinate"] == 1.0
    assert out["vertex_y_coordinate"] == 2.0
    assert out["vertex_z_coordinate"] == 3.0
    assert out["vertex_x_coordinate_2"] == 4.0
    assert out["vertex_y_coordinate_2"] == 5.0
    assert out["vertex_z_coordinate_2"] == 6.0
