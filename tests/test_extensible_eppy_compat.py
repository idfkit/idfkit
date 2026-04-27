"""
Eppy-compat shim for flat extensible field access (Phase 4 of #135 follow-up).

After Phase 2 of the canonical-shape migration, ``obj.data`` stores
extensible groups under the schema's wrapper key. Legacy eppy-style flat
accessors (``surface.vertex_3_x_coordinate``) keep working through a
deprecation shim that translates to the canonical wrapper position.

The shim is scheduled for removal one minor release after the migration.
"""

from __future__ import annotations

import warnings

import pytest

from idfkit import LATEST_VERSION, new_document


@pytest.fixture()
def surface():
    doc = new_document(version=LATEST_VERSION, strict=False)
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


# ---------------------------------------------------------------------------
# Read access
# ---------------------------------------------------------------------------


def test_legacy_flat_read_returns_value(surface) -> None:
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", DeprecationWarning)
        assert surface.vertex_x_coordinate == 0.0  # group 1
        assert surface.vertex_x_coordinate_2 == 5.0  # group 2


def test_legacy_eppy_read_returns_value(surface) -> None:
    """eppy-style ``vertex_2_x_coordinate`` (number-in-the-middle) also works."""
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", DeprecationWarning)
        assert surface.vertex_2_x_coordinate == 5.0


def test_legacy_flat_read_emits_deprecation_warning(surface) -> None:
    with pytest.warns(DeprecationWarning, match="flat-extensible access is deprecated"):
        _ = surface.vertex_x_coordinate_2


def test_deprecation_warning_message_points_to_canonical(surface) -> None:
    with pytest.warns(DeprecationWarning) as record:
        _ = surface.vertex_x_coordinate_2
    msg = str(record[0].message)
    assert "BuildingSurface:Detailed.vertices[1].vertex_x_coordinate" in msg


def test_legacy_read_out_of_range_returns_none(surface) -> None:
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", DeprecationWarning)
        # Group 99 doesn't exist; returns None (no canonical slot to translate to).
        assert surface.vertex_x_coordinate_99 is None


# ---------------------------------------------------------------------------
# Write access
# ---------------------------------------------------------------------------


def test_legacy_flat_write_routes_to_canonical(surface) -> None:
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", DeprecationWarning)
        surface.vertex_x_coordinate_2 = 99.0
    assert surface.data["vertices"][1]["vertex_x_coordinate"] == 99.0


def test_legacy_flat_write_emits_deprecation_warning(surface) -> None:
    with pytest.warns(DeprecationWarning, match="flat-extensible assignment is deprecated"):
        surface.vertex_x_coordinate_2 = 99.0


def test_legacy_write_extends_wrapper(surface) -> None:
    """Writing a flat slot beyond the current length grows the canonical list."""
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", DeprecationWarning)
        surface.vertex_x_coordinate_4 = 7.0  # currently only 2 items
    assert len(surface.data["vertices"]) == 4
    assert surface.data["vertices"][3]["vertex_x_coordinate"] == 7.0


def test_legacy_eppy_write_routes_to_canonical(surface) -> None:
    """eppy-style ``vertex_2_x_coordinate = ...`` also works."""
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", DeprecationWarning)
        surface.vertex_2_x_coordinate = 11.0
    assert surface.data["vertices"][1]["vertex_x_coordinate"] == 11.0


# ---------------------------------------------------------------------------
# Canonical access never warns
# ---------------------------------------------------------------------------


def test_canonical_read_does_not_warn(surface) -> None:
    with warnings.catch_warnings():
        warnings.simplefilter("error", DeprecationWarning)
        _ = surface.vertices[1].vertex_x_coordinate
        _ = surface.data["vertices"][1]["vertex_x_coordinate"]


def test_canonical_write_does_not_warn(surface) -> None:
    with warnings.catch_warnings():
        warnings.simplefilter("error", DeprecationWarning)
        surface.vertices[1].vertex_x_coordinate = 88.0
        surface.data["vertices"][1]["vertex_x_coordinate"] = 77.0
