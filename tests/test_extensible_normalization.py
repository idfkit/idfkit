"""
Round-trip matrix for canonical extensible-array storage (issue #135 follow-up).

After Phase 2 of the canonical-shape migration, ``obj.data[wrapper_key]`` is the
canonical list of dicts that EnergyPlus's epJSON format itself uses (verified
against ``RefBldgMediumOfficeNew2004_Chicago_epJSON.epJSON`` from
NREL/EnergyPlus v24.1.0). This file covers every combination of input shape
x output format x object type, ensuring the underlying storage stays
canonical regardless of how data entered the document.

Test gap that allowed issue #135 to ship: the original roundtrip tests
started every case from IDF text. Since ``load_idf`` produced flat keys,
the canonical ``{"vertices": [...]}`` shape never entered ``obj.data``
during those tests. The matrix below fills exactly that gap.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest

from idfkit import LATEST_VERSION, load_epjson, load_idf, new_document, write_epjson, write_idf

VERSION = LATEST_VERSION
VERSION_ID = f"{VERSION[0]}.{VERSION[1]}"


# ---------------------------------------------------------------------------
# Per-type fixture data
# ---------------------------------------------------------------------------


SURFACE_CANONICAL: list[dict[str, Any]] = [
    {"vertex_x_coordinate": 0.0, "vertex_y_coordinate": 0.0, "vertex_z_coordinate": 3.0},
    {"vertex_x_coordinate": 0.0, "vertex_y_coordinate": 0.0, "vertex_z_coordinate": 0.0},
    {"vertex_x_coordinate": 5.0, "vertex_y_coordinate": 0.0, "vertex_z_coordinate": 0.0},
    {"vertex_x_coordinate": 5.0, "vertex_y_coordinate": 0.0, "vertex_z_coordinate": 3.0},
]

SURFACE_FLAT_KWARGS: dict[str, Any] = {
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

SCHEDULE_CANONICAL: list[dict[str, Any]] = [
    {"time": "08:00", "value_until_time": 0.1},
    {"time": "18:00", "value_until_time": 0.9},
    {"time": "24:00", "value_until_time": 0.1},
]

SCHEDULE_FLAT_KWARGS: dict[str, Any] = {
    "time": "08:00",
    "value_until_time": 0.1,
    "time_2": "18:00",
    "value_until_time_2": 0.9,
    "time_3": "24:00",
    "value_until_time_3": 0.1,
}


def _surface_idf_text() -> str:
    return f"""Version,{VERSION_ID};

GlobalGeometryRules, UpperLeftCorner, Counterclockwise, Relative;
Zone, Z1;
BuildingSurface:Detailed,
  WallA, Wall, C, Z1, , Outdoors, , , , , ,
  0, 0, 3,
  0, 0, 0,
  5, 0, 0,
  5, 0, 3;
"""


def _schedule_idf_text() -> str:
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
    fields: dict[str, Any] = {
        "surface_type": "Wall",
        "construction_name": "C",
        "zone_name": "Z1",
        "outside_boundary_condition": "Outdoors",
    }
    if canonical:
        fields["vertices"] = [dict(item) for item in SURFACE_CANONICAL]
    else:
        fields.update(SURFACE_FLAT_KWARGS)
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
        "BuildingSurface:Detailed": {"WallA": fields},
    }


def _schedule_epjson(*, canonical: bool) -> dict[str, Any]:
    fields: dict[str, Any] = {
        "schedule_type_limits_name": "Fraction",
        "interpolate_to_timestep": "No",
    }
    if canonical:
        fields["data"] = [dict(item) for item in SCHEDULE_CANONICAL]
    else:
        fields.update(SCHEDULE_FLAT_KWARGS)
    return {
        "Version": {"Version 1": {"version_identifier": VERSION_ID}},
        "ScheduleTypeLimits": {
            "Fraction": {"lower_limit_value": 0.0, "upper_limit_value": 1.0, "numeric_type": "Continuous"}
        },
        "Schedule:Day:Interval": {"DayA": fields},
    }


TYPE_PARAMS = [
    pytest.param(
        "BuildingSurface:Detailed",
        "WallA",
        "vertices",
        SURFACE_CANONICAL,
        SURFACE_FLAT_KWARGS,
        _surface_idf_text(),
        id="BuildingSurfaceDetailed",
    ),
    pytest.param(
        "Schedule:Day:Interval",
        "DayA",
        "data",
        SCHEDULE_CANONICAL,
        SCHEDULE_FLAT_KWARGS,
        _schedule_idf_text(),
        id="ScheduleDayInterval",
    ),
]


# ---------------------------------------------------------------------------
# Entry-shape constructors
# ---------------------------------------------------------------------------


def _entry(
    entry_shape: str,
    obj_type: str,
    name: str,
    canonical_items: list[dict[str, Any]],
    flat_kwargs: dict[str, Any],
    idf_text: str,
    tmp_path: Path,
) -> Any:
    """Build a document via the requested entry shape and return it."""
    if entry_shape == "idf_flat":
        p = tmp_path / "in.idf"
        p.write_text(idf_text)
        return load_idf(p)

    if entry_shape in ("epjson_canonical", "epjson_flat"):
        canonical = entry_shape == "epjson_canonical"
        ep = (
            _surface_epjson(canonical=canonical)
            if obj_type == "BuildingSurface:Detailed"
            else _schedule_epjson(canonical=canonical)
        )
        p = tmp_path / "in.epjson"
        p.write_text(json.dumps(ep))
        return load_epjson(p)

    # add_canonical / add_flat
    doc = new_document(version=VERSION, strict=False)
    if obj_type == "BuildingSurface:Detailed":
        doc.add("Zone", "Z1")
        common = {
            "surface_type": "Wall",
            "construction_name": "C",
            "zone_name": "Z1",
            "outside_boundary_condition": "Outdoors",
        }
        if entry_shape == "add_canonical":
            doc.add(obj_type, name, **common, vertices=[dict(item) for item in canonical_items], validate=False)
        else:
            doc.add(obj_type, name, **common, **flat_kwargs, validate=False)
        return doc

    # Schedule:Day:Interval
    doc.add("ScheduleTypeLimits", "Fraction", validate=False)
    common = {"schedule_type_limits_name": "Fraction", "interpolate_to_timestep": "No"}
    if entry_shape == "add_canonical":
        doc.add(obj_type, name, **common, data=[dict(item) for item in canonical_items], validate=False)
    else:
        doc.add(obj_type, name, **common, **flat_kwargs, validate=False)
    return doc


# ---------------------------------------------------------------------------
# Storage shape invariant
# ---------------------------------------------------------------------------


ENTRY_SHAPES = ["idf_flat", "epjson_canonical", "epjson_flat", "add_canonical", "add_flat"]
OUTPUT_FORMATS = ["idf", "epjson"]


@pytest.mark.parametrize("entry_shape", ENTRY_SHAPES)
@pytest.mark.parametrize(
    ("obj_type", "name", "wrapper_key", "canonical_items", "flat_kwargs", "idf_text"),
    TYPE_PARAMS,
)
def test_entry_storage_is_canonical(
    entry_shape: str,
    obj_type: str,
    name: str,
    wrapper_key: str,
    canonical_items: list[dict[str, Any]],
    flat_kwargs: dict[str, Any],
    idf_text: str,
    tmp_path: Path,
) -> None:
    """No matter how data enters the document, ``obj.data[wrapper_key]`` is canonical."""
    doc = _entry(entry_shape, obj_type, name, canonical_items, flat_kwargs, idf_text, tmp_path)
    obj = doc[obj_type][name]
    items = obj.data.get(wrapper_key)
    assert isinstance(items, list), f"{wrapper_key!r} should be a list, got {type(items).__name__}"
    assert len(items) == len(canonical_items)
    # Inner dicts must contain the schema-defined inner field names.
    for item, expected in zip(items, canonical_items, strict=True):
        for inner_name, inner_value in expected.items():
            assert item.get(inner_name) == inner_value
    # Flat extensible keys must NOT leak into top-level storage.
    flat_keys = [
        k
        for k in obj.data
        if any(k.startswith(p) and k != wrapper_key for p in ("vertex_", "time", "value_until_time"))
    ]
    assert not flat_keys, f"flat keys leaked into top-level storage: {flat_keys!r}"


# ---------------------------------------------------------------------------
# 5 entries x 2 outputs x 2 types = 20 round-trip cases
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("output_format", OUTPUT_FORMATS)
@pytest.mark.parametrize("entry_shape", ENTRY_SHAPES)
@pytest.mark.parametrize(
    ("obj_type", "name", "wrapper_key", "canonical_items", "flat_kwargs", "idf_text"),
    TYPE_PARAMS,
)
def test_roundtrip_matrix(
    entry_shape: str,
    output_format: str,
    obj_type: str,
    name: str,
    wrapper_key: str,
    canonical_items: list[dict[str, Any]],
    flat_kwargs: dict[str, Any],
    idf_text: str,
    tmp_path: Path,
) -> None:
    """Every (entry x output) cell preserves the canonical wrapper contents."""
    doc = _entry(entry_shape, obj_type, name, canonical_items, flat_kwargs, idf_text, tmp_path)

    if output_format == "idf":
        out = tmp_path / "out.idf"
        write_idf(doc, out)
        text = out.read_text()
        assert "{" not in text, f"dict repr leaked into IDF: {text}"
        # Comment for the second group must be present.
        if obj_type == "BuildingSurface:Detailed":
            assert "Vertex X Coordinate 2" in text
        else:
            assert "Time 2" in text
        # Re-parse and verify canonical content is preserved.
        doc2 = load_idf(out)
        obj2 = doc2[obj_type][name]
        items2 = obj2.data.get(wrapper_key) or []
        assert len(items2) == len(canonical_items)
        for got, expected in zip(items2, canonical_items, strict=True):
            for k, v in expected.items():
                assert got.get(k) == v
    else:
        out = tmp_path / "out.epjson"
        write_epjson(doc, out)
        body = json.loads(out.read_text())[obj_type][name]
        # Wrapper present, list of dicts, no flat key leakage.
        assert wrapper_key in body and isinstance(body[wrapper_key], list)
        assert len(body[wrapper_key]) == len(canonical_items)
        for k in body:
            if k != wrapper_key:
                assert not k.startswith("vertex_"), f"flat key {k!r} leaked into epJSON"
        # Re-parse and verify canonical content is preserved.
        doc2 = load_epjson(out)
        obj2 = doc2[obj_type][name]
        items2 = obj2.data.get(wrapper_key) or []
        assert len(items2) == len(canonical_items)
        for got, expected in zip(items2, canonical_items, strict=True):
            for k, v in expected.items():
                assert got.get(k) == v


# ---------------------------------------------------------------------------
# Issue #135 reproductions, verbatim
# ---------------------------------------------------------------------------


def test_issue_135_repro_1_doc_add_with_vertices_array(tmp_path: Path) -> None:
    """Repro 1: doc.add with vertices=[{...}, ...] must produce valid IDF."""
    doc = new_document(version=VERSION, strict=True)
    doc.add("Zone", "Z1")
    doc.add(
        "BuildingSurface:Detailed",
        "WallA",
        surface_type="Wall",
        construction_name="C",
        zone_name="Z1",
        outside_boundary_condition="Outdoors",
        vertices=[dict(item) for item in SURFACE_CANONICAL],
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
    """Repro 2: load_epjson canonical -> write_idf must preserve vertices."""
    epjson_data = _surface_epjson(canonical=True)
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


def test_flat_kwargs_emit_deprecation_warning() -> None:
    """Passing flat extensible kwargs to ``.add()`` emits a DeprecationWarning.

    The setattr/getattr paths already warn (see test_extensible_eppy_compat),
    but the canonical ``doc.add(**kwargs)`` path used to silently rewrite flat
    keys to the wrapper-array shape — leaving callers (idfkit-mcp's add_object,
    autogenerated agent prompts, etc.) with no signal that they were using a
    deprecated form.
    """
    doc = new_document(version=VERSION, strict=False)
    doc.add("Zone", "Z1")
    with pytest.warns(DeprecationWarning, match="flat-extensible kwargs"):
        doc.add(
            "BuildingSurface:Detailed",
            "WallA",
            surface_type="Wall",
            construction_name="C",
            zone_name="Z1",
            outside_boundary_condition="Outdoors",
            **SURFACE_FLAT_KWARGS,
            validate=False,
        )


def test_structured_array_kwargs_do_not_warn(recwarn: pytest.WarningsRecorder) -> None:
    """The canonical wrapper-array form must not emit a deprecation."""
    doc = new_document(version=VERSION, strict=False)
    doc.add("Zone", "Z1")
    doc.add(
        "BuildingSurface:Detailed",
        "WallA",
        surface_type="Wall",
        construction_name="C",
        zone_name="Z1",
        outside_boundary_condition="Outdoors",
        vertices=SURFACE_CANONICAL,
        validate=False,
    )
    deprecations = [w for w in recwarn.list if issubclass(w.category, DeprecationWarning)]
    assert deprecations == []


def test_mixed_input_raises() -> None:
    """Passing both wrapper list AND a flat extensible key must raise."""
    doc = new_document(version=VERSION, strict=False)
    doc.add("Zone", "Z1")
    with pytest.raises(ValueError, match="cannot mix 'vertices'=\\[\\.\\.\\.\\]"):
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
    # Either the wrapper is absent or it's an empty list.
    assert obj.data.get("vertices", []) == []
    p = tmp_path / "out.epjson"
    write_epjson(doc, p)
    body = json.loads(p.read_text())["BuildingSurface:Detailed"]["WallA"]
    assert "vertices" not in body or body["vertices"] == []


def test_branchlist_canonical_roundtrip(tmp_path: Path) -> None:
    """Regression: BranchList uses 'branches' as wrapper key — different from 'vertices'/'data'."""
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
    branches = obj.data["branches"]
    assert isinstance(branches, list)
    assert [b["branch_name"] for b in branches] == ["B1", "B2", "B3"]
    # IDF round-trip works.
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
