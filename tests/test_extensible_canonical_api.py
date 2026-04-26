"""
Tests for the canonical extensible-array access API (Phase 1 of issue #135 follow-up).

This file covers the new ``ExtensibleList`` / ``ExtensibleGroup`` types — list-like
views over the wrapper key (``vertices``, ``data``, ``branches``, ``extensions``).
During Phase 1 the views read and write flat ``vertex_x_coordinate_3``-style
storage; once Phase 2 lands they will operate over canonical wrapper-array
storage. The public API tested here must remain identical across both phases.
"""

from __future__ import annotations

from typing import Any

import pytest

from idfkit import LATEST_VERSION, new_document
from idfkit.objects import ExtensibleGroup, ExtensibleList


def _surface(doc: Any) -> Any:
    doc.add("Zone", "Z1")
    return doc.add(
        "BuildingSurface:Detailed",
        "WallA",
        surface_type="Wall",
        construction_name="C",
        zone_name="Z1",
        outside_boundary_condition="Outdoors",
        vertices=[
            {"vertex_x_coordinate": 0.0, "vertex_y_coordinate": 0.0, "vertex_z_coordinate": 3.0},
            {"vertex_x_coordinate": 5.0, "vertex_y_coordinate": 0.0, "vertex_z_coordinate": 0.0},
        ],
        validate=False,
    )


@pytest.fixture()
def surface() -> Any:
    return _surface(new_document(version=LATEST_VERSION, strict=False))


# ---------------------------------------------------------------------------
# Read access
# ---------------------------------------------------------------------------


def test_wrapper_attribute_returns_extensible_list(surface: Any) -> None:
    assert isinstance(surface.vertices, ExtensibleList)


def test_len(surface: Any) -> None:
    assert len(surface.vertices) == 2


def test_index_returns_group(surface: Any) -> None:
    assert isinstance(surface.vertices[0], ExtensibleGroup)


def test_negative_index(surface: Any) -> None:
    assert surface.vertices[-1].vertex_x_coordinate == 5.0


def test_index_out_of_range_raises(surface: Any) -> None:
    with pytest.raises(IndexError):
        _ = surface.vertices[5]


def test_attribute_access_on_group(surface: Any) -> None:
    v = surface.vertices[0]
    assert v.vertex_x_coordinate == 0.0
    assert v.vertex_y_coordinate == 0.0
    assert v.vertex_z_coordinate == 3.0


def test_dict_access_on_group(surface: Any) -> None:
    assert surface.vertices[0]["vertex_x_coordinate"] == 0.0


def test_unknown_attribute_on_group_raises(surface: Any) -> None:
    with pytest.raises(AttributeError, match="not an extensible field"):
        _ = surface.vertices[0].bogus


def test_iteration_yields_groups_in_order(surface: Any) -> None:
    xs = [v.vertex_x_coordinate for v in surface.vertices]
    assert xs == [0.0, 5.0]


def test_group_index_property(surface: Any) -> None:
    assert [v.group_index for v in surface.vertices] == [1, 2]


def test_group_keys_values_items(surface: Any) -> None:
    v = surface.vertices[0]
    assert v.keys() == ("vertex_x_coordinate", "vertex_y_coordinate", "vertex_z_coordinate")
    assert v.values() == [0.0, 0.0, 3.0]
    assert v.items() == [
        ("vertex_x_coordinate", 0.0),
        ("vertex_y_coordinate", 0.0),
        ("vertex_z_coordinate", 3.0),
    ]


def test_group_as_dict_snapshot(surface: Any) -> None:
    d = surface.vertices[0].as_dict()
    assert d == {"vertex_x_coordinate": 0.0, "vertex_y_coordinate": 0.0, "vertex_z_coordinate": 3.0}


def test_list_as_list_snapshot(surface: Any) -> None:
    assert surface.vertices.as_list() == [
        {"vertex_x_coordinate": 0.0, "vertex_y_coordinate": 0.0, "vertex_z_coordinate": 3.0},
        {"vertex_x_coordinate": 5.0, "vertex_y_coordinate": 0.0, "vertex_z_coordinate": 0.0},
    ]


# ---------------------------------------------------------------------------
# Mutation
# ---------------------------------------------------------------------------


def test_mutate_via_attribute_writes_canonical_storage(surface: Any) -> None:
    surface.vertices[0].vertex_x_coordinate = 1.0
    assert surface.data["vertices"][0]["vertex_x_coordinate"] == 1.0


def test_mutate_second_group_writes_canonical_slot(surface: Any) -> None:
    surface.vertices[1].vertex_x_coordinate = 99.0
    assert surface.data["vertices"][1]["vertex_x_coordinate"] == 99.0


def test_group_update_atomic(surface: Any) -> None:
    surface.vertices[0].update(vertex_x_coordinate=11.0, vertex_y_coordinate=22.0)
    assert surface.vertices[0].vertex_x_coordinate == 11.0
    assert surface.vertices[0].vertex_y_coordinate == 22.0


def test_append_with_kwargs(surface: Any) -> None:
    surface.vertices.append(vertex_x_coordinate=5, vertex_y_coordinate=0, vertex_z_coordinate=3)
    assert len(surface.vertices) == 3
    assert surface.vertices[2].vertex_x_coordinate == 5


def test_append_with_dict(surface: Any) -> None:
    surface.vertices.append({"vertex_x_coordinate": 7, "vertex_y_coordinate": 8, "vertex_z_coordinate": 9})
    assert surface.vertices[-1].vertex_z_coordinate == 9


def test_append_returns_new_group(surface: Any) -> None:
    g = surface.vertices.append(vertex_x_coordinate=10, vertex_y_coordinate=10, vertex_z_coordinate=10)
    assert isinstance(g, ExtensibleGroup)
    assert g.group_index == 3


def test_append_rejects_unknown_field(surface: Any) -> None:
    with pytest.raises(ValueError, match="unknown extensible field"):
        surface.vertices.append(bogus=1.0)


def test_append_rejects_dict_and_kwargs_together(surface: Any) -> None:
    with pytest.raises(TypeError, match="not both"):
        surface.vertices.append({"vertex_x_coordinate": 1}, vertex_y_coordinate=2)


def test_insert_shifts_existing_groups(surface: Any) -> None:
    surface.vertices.insert(0, vertex_x_coordinate=99, vertex_y_coordinate=99, vertex_z_coordinate=99)
    assert len(surface.vertices) == 3
    assert surface.vertices[0].vertex_x_coordinate == 99
    # original first group is now at index 1
    assert surface.vertices[1].vertex_z_coordinate == 3.0


def test_insert_at_end_equivalent_to_append(surface: Any) -> None:
    surface.vertices.insert(len(surface.vertices), vertex_x_coordinate=42, vertex_y_coordinate=0, vertex_z_coordinate=0)
    assert surface.vertices[-1].vertex_x_coordinate == 42


def test_delete_shifts_later_groups_down(surface: Any) -> None:
    # Original: [0,0,3], [5,0,0]; delete index 0 -> [5,0,0]
    del surface.vertices[0]
    assert len(surface.vertices) == 1
    assert surface.vertices[0].vertex_x_coordinate == 5.0
    assert len(surface.data["vertices"]) == 1


def test_pop_returns_dict(surface: Any) -> None:
    popped = surface.vertices.pop()
    assert popped == {"vertex_x_coordinate": 5.0, "vertex_y_coordinate": 0.0, "vertex_z_coordinate": 0.0}
    assert len(surface.vertices) == 1


def test_clear(surface: Any) -> None:
    surface.vertices.clear()
    assert len(surface.vertices) == 0
    assert "vertices" not in surface.data


def test_extend(surface: Any) -> None:
    surface.vertices.extend([
        {"vertex_x_coordinate": 1, "vertex_y_coordinate": 1, "vertex_z_coordinate": 1},
        {"vertex_x_coordinate": 2, "vertex_y_coordinate": 2, "vertex_z_coordinate": 2},
    ])
    assert len(surface.vertices) == 4


def test_bulk_replace_via_setattr(surface: Any) -> None:
    surface.vertices = [
        {"vertex_x_coordinate": 9, "vertex_y_coordinate": 9, "vertex_z_coordinate": 9},
    ]
    assert len(surface.vertices) == 1
    assert surface.vertices[0].vertex_x_coordinate == 9


def test_bulk_replace_with_groups(surface: Any) -> None:
    other = _surface(new_document(version=LATEST_VERSION, strict=False))
    other_groups = list(other.vertices)
    surface.vertices = other_groups
    assert surface.vertices.as_list() == other.vertices.as_list()


def test_setattr_non_list_to_wrapper_raises(surface: Any) -> None:
    with pytest.raises(TypeError, match="must be a list"):
        surface.vertices = {"vertex_x_coordinate": 0}  # type: ignore[assignment]


# ---------------------------------------------------------------------------
# Equality / repr
# ---------------------------------------------------------------------------


def test_group_equals_dict(surface: Any) -> None:
    assert surface.vertices[0] == {
        "vertex_x_coordinate": 0.0,
        "vertex_y_coordinate": 0.0,
        "vertex_z_coordinate": 3.0,
    }


def test_list_equals_list_of_dicts(surface: Any) -> None:
    assert surface.vertices == [
        {"vertex_x_coordinate": 0.0, "vertex_y_coordinate": 0.0, "vertex_z_coordinate": 3.0},
        {"vertex_x_coordinate": 5.0, "vertex_y_coordinate": 0.0, "vertex_z_coordinate": 0.0},
    ]


def test_group_repr_includes_index(surface: Any) -> None:
    r = repr(surface.vertices[0])
    assert "BuildingSurface:Detailed" in r
    assert "vertices[0]" in r


def test_list_repr(surface: Any) -> None:
    r = repr(surface.vertices)
    assert "BuildingSurface:Detailed" in r
    assert "vertices" in r


# ---------------------------------------------------------------------------
# Cross-type coverage: same shape works for every extensible type
# ---------------------------------------------------------------------------


def test_schedule_day_interval_data_wrapper() -> None:
    """Schedule:Day:Interval's wrapper key is "data", which collides with
    the ``IDFObject.data`` dict property. Use ``sched["data"]`` for the
    canonical view."""
    doc = new_document(version=LATEST_VERSION, strict=False)
    doc.add("ScheduleTypeLimits", "Fraction", validate=False)
    sched = doc.add(
        "Schedule:Day:Interval",
        "DayA",
        schedule_type_limits_name="Fraction",
        interpolate_to_timestep="No",
        data=[
            {"time": "08:00", "value_until_time": 0.1},
            {"time": "18:00", "value_until_time": 0.9},
        ],
        validate=False,
    )
    assert isinstance(sched["data"], ExtensibleList)
    assert len(sched["data"]) == 2
    assert sched["data"][0].time == "08:00"
    assert sched["data"][1].value_until_time == 0.9
    sched["data"].append(time="24:00", value_until_time=0.1)
    assert len(sched["data"]) == 3


def test_branchlist_branches_wrapper() -> None:
    doc = new_document(version=LATEST_VERSION, strict=False)
    bl = doc.add(
        "BranchList",
        "MyBranches",
        branches=[
            {"branch_name": "B1"},
            {"branch_name": "B2"},
        ],
        validate=False,
    )
    assert [b.branch_name for b in bl.branches] == ["B1", "B2"]
    bl.branches.append(branch_name="B3")
    assert bl.branches[-1].branch_name == "B3"


def test_schedule_compact_data_wrapper_with_mixed_types() -> None:
    """Schedule:Compact's ``field`` accepts both strings and numbers; access
    via ``sc["data"]`` since the wrapper key collides with the ``data`` property."""
    doc = new_document(version=LATEST_VERSION, strict=False)
    doc.add("ScheduleTypeLimits", "Any Number", validate=False)
    sc = doc.add(
        "Schedule:Compact",
        "ACTIVITY_SCH",
        schedule_type_limits_name="Any Number",
        data=[
            {"field": "Through: 12/31"},
            {"field": "For: AllDays"},
            {"field": "Until: 24:00"},
            {"field": 120.0},
        ],
        validate=False,
    )
    assert len(sc["data"]) == 4
    assert sc["data"][0].field == "Through: 12/31"
    assert sc["data"][3].field == 120.0


# ---------------------------------------------------------------------------
# Storage shape is canonical (Phase 2 invariant)
# ---------------------------------------------------------------------------


def test_storage_is_canonical_after_construction(surface: Any) -> None:
    """`obj.data[wrapper_key]` is a list of dicts; no flat keys leak in."""
    assert isinstance(surface.data["vertices"], list)
    assert all(isinstance(item, dict) for item in surface.data["vertices"])
    assert all(not (k.startswith("vertex_") and k != "vertices") for k in surface.data), (
        "no flat keys should be present at the top level of obj.data"
    )


def test_canonical_storage_round_trips_via_dict_access(surface: Any) -> None:
    """obj.data['vertices'][i] gives the raw inner dict, equivalent to the typed view."""
    assert surface.data["vertices"][0] == surface.vertices[0].as_dict()
    surface.vertices[0].vertex_x_coordinate = 42.0
    assert surface.data["vertices"][0]["vertex_x_coordinate"] == 42.0


# ---------------------------------------------------------------------------
# Non-extensible types reject wrapper access
# ---------------------------------------------------------------------------


def test_non_extensible_type_has_no_wrapper_view() -> None:
    doc = new_document(version=LATEST_VERSION, strict=False)
    zone = doc.add("Zone", "Z1")
    # Zone has no extensible wrapper; accessing a fake wrapper attribute
    # falls through __getattr__ and returns None (legacy eppy behaviour).
    assert zone.vertices is None
