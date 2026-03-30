"""Tests for idfkit.visualization.model -- 3D building visualization."""

from __future__ import annotations

import pytest

from idfkit import IDFDocument, new_document
from idfkit.geometry import Polygon3D, Vector3D
from idfkit.visualization.model import (
    ColorBy,
    ModelViewConfig,
    _apply_zone_offsets,  # pyright: ignore[reportPrivateUsage]
    _assign_zone_colors,  # pyright: ignore[reportPrivateUsage]
    _build_edge_traces,  # pyright: ignore[reportPrivateUsage]
    _build_hover_text,  # pyright: ignore[reportPrivateUsage]
    _build_label_traces,  # pyright: ignore[reportPrivateUsage]
    _build_mesh_traces,  # pyright: ignore[reportPrivateUsage]
    _compute_zone_offsets,  # pyright: ignore[reportPrivateUsage]
    _get_color,  # pyright: ignore[reportPrivateUsage]
    _get_go,  # pyright: ignore[reportPrivateUsage]
    _legend_label,  # pyright: ignore[reportPrivateUsage]
    _make_3d_layout,  # pyright: ignore[reportPrivateUsage]
    _offset_fenestration,  # pyright: ignore[reportPrivateUsage]
    _polygon_edges,  # pyright: ignore[reportPrivateUsage]
    _resolve_surfaces,  # pyright: ignore[reportPrivateUsage]
    _ResolvedSurface,  # pyright: ignore[reportPrivateUsage]
    _to_world_coords,  # pyright: ignore[reportPrivateUsage]
    _triangulate_polygon,  # pyright: ignore[reportPrivateUsage]
)

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

_MATERIAL_FIELDS = {
    "roughness": "Smooth",
    "thickness": 0.1,
    "conductivity": 1.0,
    "density": 1000.0,
    "specific_heat": 800.0,
}

_WALL_VERTICES = {
    "number_of_vertices": 4,
    "vertex_1_x_coordinate": 0.0,
    "vertex_1_y_coordinate": 0.0,
    "vertex_1_z_coordinate": 3.0,
    "vertex_2_x_coordinate": 0.0,
    "vertex_2_y_coordinate": 0.0,
    "vertex_2_z_coordinate": 0.0,
    "vertex_3_x_coordinate": 5.0,
    "vertex_3_y_coordinate": 0.0,
    "vertex_3_z_coordinate": 0.0,
    "vertex_4_x_coordinate": 5.0,
    "vertex_4_y_coordinate": 0.0,
    "vertex_4_z_coordinate": 3.0,
}


def _add_material_and_construction(doc: IDFDocument) -> None:
    """Add a simple Material 'M' and Construction 'C' to the document."""
    doc.add("Material", "M", _MATERIAL_FIELDS)
    doc.add("Construction", "C", {"outside_layer": "M"})


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def multi_zone_doc():
    """Create a document with two zones, each with walls and a floor."""
    doc = new_document(version=(24, 1, 0))

    doc.add("Zone", "ZoneA", {"x_origin": 0.0, "y_origin": 0.0, "z_origin": 0.0})
    doc.add("Zone", "ZoneB", {"x_origin": 10.0, "y_origin": 0.0, "z_origin": 0.0})

    doc.add(
        "Material",
        "TestMaterial",
        {
            "roughness": "MediumSmooth",
            "thickness": 0.1,
            "conductivity": 1.0,
            "density": 2000.0,
            "specific_heat": 1000.0,
        },
    )
    doc.add("Construction", "TestConstruction", {"outside_layer": "TestMaterial"})

    # Zone A surfaces
    doc.add(
        "BuildingSurface:Detailed",
        "WallA1",
        {
            "surface_type": "Wall",
            "construction_name": "TestConstruction",
            "zone_name": "ZoneA",
            "outside_boundary_condition": "Outdoors",
            "number_of_vertices": 4,
            "vertex_1_x_coordinate": 0.0,
            "vertex_1_y_coordinate": 0.0,
            "vertex_1_z_coordinate": 3.0,
            "vertex_2_x_coordinate": 0.0,
            "vertex_2_y_coordinate": 0.0,
            "vertex_2_z_coordinate": 0.0,
            "vertex_3_x_coordinate": 5.0,
            "vertex_3_y_coordinate": 0.0,
            "vertex_3_z_coordinate": 0.0,
            "vertex_4_x_coordinate": 5.0,
            "vertex_4_y_coordinate": 0.0,
            "vertex_4_z_coordinate": 3.0,
        },
    )
    doc.add(
        "BuildingSurface:Detailed",
        "FloorA",
        {
            "surface_type": "Floor",
            "construction_name": "TestConstruction",
            "zone_name": "ZoneA",
            "outside_boundary_condition": "Ground",
            "number_of_vertices": 4,
            "vertex_1_x_coordinate": 0.0,
            "vertex_1_y_coordinate": 0.0,
            "vertex_1_z_coordinate": 0.0,
            "vertex_2_x_coordinate": 5.0,
            "vertex_2_y_coordinate": 0.0,
            "vertex_2_z_coordinate": 0.0,
            "vertex_3_x_coordinate": 5.0,
            "vertex_3_y_coordinate": 5.0,
            "vertex_3_z_coordinate": 0.0,
            "vertex_4_x_coordinate": 0.0,
            "vertex_4_y_coordinate": 5.0,
            "vertex_4_z_coordinate": 0.0,
        },
    )

    # Zone B surfaces
    doc.add(
        "BuildingSurface:Detailed",
        "WallB1",
        {
            "surface_type": "Wall",
            "construction_name": "TestConstruction",
            "zone_name": "ZoneB",
            "outside_boundary_condition": "Outdoors",
            "number_of_vertices": 4,
            "vertex_1_x_coordinate": 0.0,
            "vertex_1_y_coordinate": 0.0,
            "vertex_1_z_coordinate": 3.0,
            "vertex_2_x_coordinate": 0.0,
            "vertex_2_y_coordinate": 0.0,
            "vertex_2_z_coordinate": 0.0,
            "vertex_3_x_coordinate": 5.0,
            "vertex_3_y_coordinate": 0.0,
            "vertex_3_z_coordinate": 0.0,
            "vertex_4_x_coordinate": 5.0,
            "vertex_4_y_coordinate": 0.0,
            "vertex_4_z_coordinate": 3.0,
        },
    )
    doc.add(
        "BuildingSurface:Detailed",
        "FloorB",
        {
            "surface_type": "Floor",
            "construction_name": "TestConstruction",
            "zone_name": "ZoneB",
            "outside_boundary_condition": "Ground",
            "number_of_vertices": 4,
            "vertex_1_x_coordinate": 0.0,
            "vertex_1_y_coordinate": 0.0,
            "vertex_1_z_coordinate": 0.0,
            "vertex_2_x_coordinate": 5.0,
            "vertex_2_y_coordinate": 0.0,
            "vertex_2_z_coordinate": 0.0,
            "vertex_3_x_coordinate": 5.0,
            "vertex_3_y_coordinate": 5.0,
            "vertex_3_z_coordinate": 0.0,
            "vertex_4_x_coordinate": 0.0,
            "vertex_4_y_coordinate": 5.0,
            "vertex_4_z_coordinate": 0.0,
        },
    )

    return doc


@pytest.fixture
def fenestration_doc(multi_zone_doc):
    """Extend multi_zone_doc with a window on WallA1."""
    multi_zone_doc.add(
        "FenestrationSurface:Detailed",
        "WindowA1",
        {
            "surface_type": "Window",
            "construction_name": "TestConstruction",
            "building_surface_name": "WallA1",
            "outside_boundary_condition_object": "",
            "number_of_vertices": 4,
            "vertex_1_x_coordinate": 1.0,
            "vertex_1_y_coordinate": 0.0,
            "vertex_1_z_coordinate": 2.5,
            "vertex_2_x_coordinate": 1.0,
            "vertex_2_y_coordinate": 0.0,
            "vertex_2_z_coordinate": 0.5,
            "vertex_3_x_coordinate": 4.0,
            "vertex_3_y_coordinate": 0.0,
            "vertex_3_z_coordinate": 0.5,
            "vertex_4_x_coordinate": 4.0,
            "vertex_4_y_coordinate": 0.0,
            "vertex_4_z_coordinate": 2.5,
        },
    )
    return multi_zone_doc


# ---------------------------------------------------------------------------
# Unit tests -- no plotly needed
# ---------------------------------------------------------------------------


class TestTriangulatePolygon:
    """Tests for _triangulate_polygon."""

    def test_triangle(self):
        i, j, k = _triangulate_polygon(3, 0)
        assert len(i) == 1
        assert (i[0], j[0], k[0]) == (0, 1, 2)

    def test_quad(self):
        i, j, k = _triangulate_polygon(4, 0)
        assert len(i) == 2
        assert (i[0], j[0], k[0]) == (0, 1, 2)
        assert (i[1], j[1], k[1]) == (0, 2, 3)

    def test_pentagon(self):
        i, _j, _k = _triangulate_polygon(5, 0)
        assert len(i) == 3

    def test_offset(self):
        i, j, k = _triangulate_polygon(4, 10)
        assert i[0] == 10
        assert j[0] == 11
        assert k[0] == 12
        assert i[1] == 10
        assert j[1] == 12
        assert k[1] == 13


class TestPolygonEdges:
    """Tests for _polygon_edges."""

    def test_closed_polygon(self):
        poly = Polygon3D([Vector3D(0, 0, 0), Vector3D(1, 0, 0), Vector3D(1, 1, 0)])
        xs, _ys, _zs = _polygon_edges(poly)
        # 3 edges, 3 values each (v1, v2, None) = 9 entries
        assert len(xs) == 9

    def test_none_separators(self):
        poly = Polygon3D([Vector3D(0, 0, 0), Vector3D(1, 0, 0), Vector3D(1, 1, 0)])
        xs, ys, zs = _polygon_edges(poly)
        # None at index 2, 5, 8
        assert xs[2] is None
        assert xs[5] is None
        assert xs[8] is None
        assert ys[2] is None
        assert zs[2] is None

    def test_first_edge_values(self):
        poly = Polygon3D([Vector3D(0, 0, 0), Vector3D(1, 0, 0), Vector3D(1, 1, 0)])
        xs, ys, _zs = _polygon_edges(poly)
        assert xs[0] == 0.0
        assert xs[1] == 1.0
        assert ys[0] == 0.0
        assert ys[1] == 0.0


class TestResolveSurfaces:
    """Tests for _resolve_surfaces."""

    def test_basic_resolution(self, multi_zone_doc):
        surfaces = _resolve_surfaces(multi_zone_doc)
        assert len(surfaces) == 4  # 2 walls + 2 floors
        names = {s.name for s in surfaces}
        assert "WallA1" in names
        assert "FloorA" in names
        assert "WallB1" in names
        assert "FloorB" in names

    def test_zone_filter(self, multi_zone_doc):
        surfaces = _resolve_surfaces(multi_zone_doc, zones=["ZoneA"])
        assert len(surfaces) == 2
        assert all(s.zone == "ZoneA" for s in surfaces)

    def test_world_coords_with_origin(self, multi_zone_doc):
        """ZoneB has x_origin=10, so its surfaces should be shifted."""
        surfaces = _resolve_surfaces(multi_zone_doc, zones=["ZoneB"])
        wall = next(s for s in surfaces if s.name == "WallB1")
        # Original vertex_1_x=0, shifted by x_origin=10 -> 10.0
        xs = [v.x for v in wall.polygon.vertices]
        assert min(xs) == pytest.approx(10.0)
        assert max(xs) == pytest.approx(15.0)

    def test_fenestration_included(self, fenestration_doc):
        surfaces = _resolve_surfaces(fenestration_doc)
        fen = [s for s in surfaces if s.is_fenestration]
        assert len(fen) == 1
        assert fen[0].name == "WindowA1"

    def test_fenestration_zone_inherited(self, fenestration_doc):
        surfaces = _resolve_surfaces(fenestration_doc)
        window = next(s for s in surfaces if s.name == "WindowA1")
        assert window.zone == "ZoneA"

    def test_zone_rotation(self):
        """Surfaces should be rotated by zone direction_of_relative_north."""
        doc = new_document(version=(24, 1, 0))
        doc.add("Zone", "RotZone", {"direction_of_relative_north": 90.0})
        doc.add(
            "Material",
            "M",
            {"roughness": "Smooth", "thickness": 0.1, "conductivity": 1.0, "density": 1000.0, "specific_heat": 800.0},
        )
        doc.add("Construction", "C", {"outside_layer": "M"})
        doc.add(
            "BuildingSurface:Detailed",
            "RotWall",
            {
                "surface_type": "Wall",
                "construction_name": "C",
                "zone_name": "RotZone",
                "outside_boundary_condition": "Outdoors",
                "number_of_vertices": 4,
                "vertex_1_x_coordinate": 0.0,
                "vertex_1_y_coordinate": 0.0,
                "vertex_1_z_coordinate": 3.0,
                "vertex_2_x_coordinate": 0.0,
                "vertex_2_y_coordinate": 0.0,
                "vertex_2_z_coordinate": 0.0,
                "vertex_3_x_coordinate": 5.0,
                "vertex_3_y_coordinate": 0.0,
                "vertex_3_z_coordinate": 0.0,
                "vertex_4_x_coordinate": 5.0,
                "vertex_4_y_coordinate": 0.0,
                "vertex_4_z_coordinate": 3.0,
            },
        )
        surfaces = _resolve_surfaces(doc)
        wall = surfaces[0]
        # After 90 degree rotation, x-axis becomes y-axis
        ys = [v.y for v in wall.polygon.vertices]
        assert max(ys) == pytest.approx(5.0, abs=0.01)

    def test_schema_vertex_naming(self):
        """Surfaces with schema naming (vertex_x_coordinate, _2, _3) are resolved."""
        doc = new_document(version=(24, 1, 0))
        doc.add("Zone", "Z1", {})
        doc.add(
            "Material",
            "M",
            {"roughness": "Smooth", "thickness": 0.1, "conductivity": 1.0, "density": 1000.0, "specific_heat": 800.0},
        )
        doc.add("Construction", "C", {"outside_layer": "M"})
        doc.add(
            "BuildingSurface:Detailed",
            "SchemaWall",
            {
                "surface_type": "Wall",
                "construction_name": "C",
                "zone_name": "Z1",
                "outside_boundary_condition": "Outdoors",
                "number_of_vertices": 4,
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
            },
        )
        surfaces = _resolve_surfaces(doc)
        assert len(surfaces) == 1
        assert surfaces[0].polygon.num_vertices == 4


class TestColorAssignment:
    """Tests for color assignment."""

    def test_distinct_zone_colors(self):
        s1 = _ResolvedSurface("A", "Zone1", "Wall", "Outdoors", "C1", Polygon3D([]), 0.0, False)
        s2 = _ResolvedSurface("B", "Zone2", "Wall", "Outdoors", "C1", Polygon3D([]), 0.0, False)
        colors = _assign_zone_colors([s1, s2], ModelViewConfig())
        assert colors["ZONE1"] != colors["ZONE2"]

    def test_surface_type_mapping(self):
        from idfkit.visualization.model import _SURFACE_TYPE_COLORS, _get_color

        cfg = ModelViewConfig(color_by=ColorBy.SURFACE_TYPE)
        s = _ResolvedSurface("W", "Z1", "Wall", "Outdoors", "C", Polygon3D([]), 0.0, False)
        color = _get_color(s, cfg, {})
        assert color == _SURFACE_TYPE_COLORS["wall"]

    def test_cycling_beyond_palette(self):
        surfaces = [
            _ResolvedSurface(f"S{i}", f"Zone{i}", "Wall", "Outdoors", "C", Polygon3D([]), 0.0, False) for i in range(25)
        ]
        colors = _assign_zone_colors(surfaces, ModelViewConfig())
        assert len(colors) == 25
        # Should cycle -- zone 0 and zone 20 should share a color
        keys = sorted(colors.keys())
        assert colors[keys[0]] == colors[keys[20]]


class TestHoverText:
    """Tests for _build_hover_text."""

    def test_contains_name(self):
        s = _ResolvedSurface("TestSurf", "Zone1", "Wall", "Outdoors", "WallConst", Polygon3D([]), 12.5, False)
        text = _build_hover_text(s)
        assert "TestSurf" in text

    def test_contains_zone(self):
        s = _ResolvedSurface("S", "MyZone", "Wall", "Outdoors", "C", Polygon3D([]), 10.0, False)
        text = _build_hover_text(s)
        assert "MyZone" in text

    def test_contains_area(self):
        s = _ResolvedSurface("S", "Z", "Wall", "Outdoors", "C", Polygon3D([]), 25.5, False)
        text = _build_hover_text(s)
        assert "25.50" in text

    def test_contains_construction(self):
        s = _ResolvedSurface("S", "Z", "Wall", "Outdoors", "BrickWall", Polygon3D([]), 10.0, False)
        text = _build_hover_text(s)
        assert "BrickWall" in text

    def test_contains_boundary(self):
        s = _ResolvedSurface("S", "Z", "Wall", "Ground", "C", Polygon3D([]), 10.0, False)
        text = _build_hover_text(s)
        assert "Ground" in text


# ---------------------------------------------------------------------------
# Integration tests -- require plotly
# ---------------------------------------------------------------------------


class TestViewModelIntegration:
    """Integration tests for view_model (require plotly)."""

    def test_returns_figure(self, multi_zone_doc):
        go = pytest.importorskip("plotly.graph_objects")
        from idfkit.visualization.model import view_model

        fig = view_model(multi_zone_doc)
        assert isinstance(fig, go.Figure)

    def test_has_mesh3d_traces(self, multi_zone_doc):
        go = pytest.importorskip("plotly.graph_objects")
        from idfkit.visualization.model import view_model

        fig = view_model(multi_zone_doc)
        mesh_traces = [t for t in fig.data if isinstance(t, go.Mesh3d)]
        assert len(mesh_traces) > 0

    def test_edges_toggle(self, multi_zone_doc):
        go = pytest.importorskip("plotly.graph_objects")
        from idfkit.visualization.model import view_model

        fig_with = view_model(multi_zone_doc, config=ModelViewConfig(show_edges=True))
        fig_without = view_model(multi_zone_doc, config=ModelViewConfig(show_edges=False))
        scatter_with = [t for t in fig_with.data if isinstance(t, go.Scatter3d) and t.mode == "lines"]
        scatter_without = [t for t in fig_without.data if isinstance(t, go.Scatter3d) and t.mode == "lines"]
        assert len(scatter_with) > len(scatter_without)

    def test_zone_filter(self, multi_zone_doc):
        pytest.importorskip("plotly.graph_objects")
        from idfkit.visualization.model import view_model

        fig_all = view_model(multi_zone_doc)
        fig_one = view_model(multi_zone_doc, zones=["ZoneA"])
        # Filtered model should have fewer or equal traces
        assert len(fig_one.data) <= len(fig_all.data)

    def test_custom_config(self, multi_zone_doc):
        go = pytest.importorskip("plotly.graph_objects")
        from idfkit.visualization.model import view_model

        cfg = ModelViewConfig(width=800, height=600, color_by=ColorBy.SURFACE_TYPE)
        fig = view_model(multi_zone_doc, config=cfg)
        assert isinstance(fig, go.Figure)
        assert fig.layout.width == 800
        assert fig.layout.height == 600


class TestViewFloorPlanIntegration:
    """Integration tests for view_floor_plan."""

    def test_returns_figure(self, multi_zone_doc):
        go = pytest.importorskip("plotly.graph_objects")
        from idfkit.visualization.model import view_floor_plan

        fig = view_floor_plan(multi_zone_doc)
        assert isinstance(fig, go.Figure)

    def test_aspect_ratio(self, multi_zone_doc):
        pytest.importorskip("plotly.graph_objects")
        from idfkit.visualization.model import view_floor_plan

        fig = view_floor_plan(multi_zone_doc)
        assert fig.layout.xaxis.scaleanchor == "y"
        assert fig.layout.xaxis.scaleratio == 1


class TestViewExplodedIntegration:
    """Integration tests for view_exploded."""

    def test_returns_figure(self, multi_zone_doc):
        go = pytest.importorskip("plotly.graph_objects")
        from idfkit.visualization.model import view_exploded

        fig = view_exploded(multi_zone_doc)
        assert isinstance(fig, go.Figure)

    def test_has_traces(self, multi_zone_doc):
        pytest.importorskip("plotly.graph_objects")
        from idfkit.visualization.model import view_exploded

        fig = view_exploded(multi_zone_doc, separation=10.0)
        assert len(fig.data) > 0


class TestViewNormalsIntegration:
    """Integration tests for view_normals."""

    def test_returns_figure(self, multi_zone_doc):
        go = pytest.importorskip("plotly.graph_objects")
        from idfkit.visualization.model import view_normals

        fig = view_normals(multi_zone_doc)
        assert isinstance(fig, go.Figure)

    def test_has_cone_traces(self, multi_zone_doc):
        go = pytest.importorskip("plotly.graph_objects")
        from idfkit.visualization.model import view_normals

        fig = view_normals(multi_zone_doc)
        cones = [t for t in fig.data if isinstance(t, go.Cone)]
        assert len(cones) == 1  # One Cone trace for all normals


class TestImportError:
    """Test ImportError is raised when plotly is not installed."""

    def test_get_go_import_error(self, monkeypatch):
        import builtins

        real_import = builtins.__import__

        def mock_import(name, *args, **kwargs):
            if "plotly" in name:
                raise ImportError
            return real_import(name, *args, **kwargs)

        monkeypatch.setattr(builtins, "__import__", mock_import)
        from idfkit.visualization.model import _get_go

        with pytest.raises(ImportError, match="plotly is required"):
            _get_go()


class TestGetGoSuccess:
    """Test _get_go returns plotly.graph_objects when available."""

    def test_returns_go_module(self) -> None:
        go = pytest.importorskip("plotly.graph_objects")
        result = _get_go()
        assert result is go


class TestToWorldCoords:
    """Tests for _to_world_coords with zone transforms."""

    def test_no_transform(self) -> None:
        """Zone at origin with no rotation should not change polygon."""
        doc = new_document(version=(24, 1, 0))
        zone = doc.add("Zone", "Z", {"x_origin": 0.0, "y_origin": 0.0, "z_origin": 0.0})
        poly = Polygon3D([Vector3D(0, 0, 0), Vector3D(1, 0, 0), Vector3D(1, 1, 0)])
        result = _to_world_coords(poly, zone)
        assert result.vertices[0].x == pytest.approx(0.0)
        assert result.vertices[1].x == pytest.approx(1.0)

    def test_translation_only(self) -> None:
        """Zone with origin offset but no rotation."""
        doc = new_document(version=(24, 1, 0))
        zone = doc.add("Zone", "Z", {"x_origin": 10.0, "y_origin": 5.0, "z_origin": 3.0})
        poly = Polygon3D([Vector3D(0, 0, 0), Vector3D(1, 0, 0), Vector3D(1, 1, 0)])
        result = _to_world_coords(poly, zone)
        assert result.vertices[0].x == pytest.approx(10.0)
        assert result.vertices[0].y == pytest.approx(5.0)
        assert result.vertices[0].z == pytest.approx(3.0)


class TestResolveSurfacesShading:
    """Tests for _resolve_surfaces with shading surfaces."""

    def test_shading_site_detailed(self) -> None:
        """Shading:Site:Detailed surfaces should be resolved."""
        doc = new_document(version=(24, 1, 0))
        doc.add("Zone", "Z1", {})
        doc.add(
            "Shading:Site:Detailed",
            "SiteShade1",
            {
                "number_of_vertices": 3,
                "vertex_1_x_coordinate": 0.0,
                "vertex_1_y_coordinate": 0.0,
                "vertex_1_z_coordinate": 5.0,
                "vertex_2_x_coordinate": 10.0,
                "vertex_2_y_coordinate": 0.0,
                "vertex_2_z_coordinate": 5.0,
                "vertex_3_x_coordinate": 10.0,
                "vertex_3_y_coordinate": 10.0,
                "vertex_3_z_coordinate": 5.0,
            },
        )
        surfaces = _resolve_surfaces(doc)
        assert len(surfaces) == 1
        assert surfaces[0].is_shading is True
        assert surfaces[0].surface_type == "Shading"
        assert surfaces[0].zone == ""

    def test_shading_building_detailed(self) -> None:
        """Shading:Building:Detailed surfaces should be resolved."""
        doc = new_document(version=(24, 1, 0))
        doc.add("Zone", "Z1", {})
        doc.add(
            "Shading:Building:Detailed",
            "BuildingShade1",
            {
                "number_of_vertices": 3,
                "vertex_1_x_coordinate": 0.0,
                "vertex_1_y_coordinate": 0.0,
                "vertex_1_z_coordinate": 5.0,
                "vertex_2_x_coordinate": 10.0,
                "vertex_2_y_coordinate": 0.0,
                "vertex_2_z_coordinate": 5.0,
                "vertex_3_x_coordinate": 10.0,
                "vertex_3_y_coordinate": 10.0,
                "vertex_3_z_coordinate": 5.0,
            },
        )
        surfaces = _resolve_surfaces(doc)
        assert len(surfaces) == 1
        assert surfaces[0].is_shading is True

    def test_shading_zone_detailed_with_base_surface(self) -> None:
        """Shading:Zone:Detailed with a base surface reference should use zone transform."""
        doc = new_document(version=(24, 1, 0))
        doc.add("Zone", "Z1", {"x_origin": 5.0, "y_origin": 0.0, "z_origin": 0.0})
        _add_material_and_construction(doc)
        doc.add(
            "BuildingSurface:Detailed",
            "Wall1",
            {
                "surface_type": "Wall",
                "construction_name": "C",
                "zone_name": "Z1",
                "outside_boundary_condition": "Outdoors",
                **_WALL_VERTICES,
            },
        )
        doc.add(
            "Shading:Zone:Detailed",
            "ZoneShade1",
            {
                "base_surface_name": "Wall1",
                "number_of_vertices": 3,
                "vertex_1_x_coordinate": 0.0,
                "vertex_1_y_coordinate": 0.0,
                "vertex_1_z_coordinate": 3.0,
                "vertex_2_x_coordinate": 5.0,
                "vertex_2_y_coordinate": 0.0,
                "vertex_2_z_coordinate": 3.0,
                "vertex_3_x_coordinate": 5.0,
                "vertex_3_y_coordinate": -1.0,
                "vertex_3_z_coordinate": 4.0,
            },
        )
        surfaces = _resolve_surfaces(doc)
        shading = [s for s in surfaces if s.is_shading]
        assert len(shading) == 1
        # The shading surface should be translated by zone origin (x=5)
        xs = [v.x for v in shading[0].polygon.vertices]
        assert min(xs) == pytest.approx(5.0)


class TestResolveSurfacesNoneCoords:
    """Test _resolve_surfaces when get_surface_coords returns None."""

    def test_building_surface_no_vertices(self) -> None:
        """BuildingSurface:Detailed with no vertex data should be skipped."""
        doc = new_document(version=(24, 1, 0))
        doc.add("Zone", "Z1", {})
        _add_material_and_construction(doc)
        doc.add(
            "BuildingSurface:Detailed",
            "NoVertWall",
            {
                "surface_type": "Wall",
                "construction_name": "C",
                "zone_name": "Z1",
                "outside_boundary_condition": "Outdoors",
            },
        )
        surfaces = _resolve_surfaces(doc)
        assert len(surfaces) == 0

    def test_fenestration_no_vertices(self) -> None:
        """FenestrationSurface:Detailed with no vertex data should be skipped."""
        doc = new_document(version=(24, 1, 0))
        doc.add("Zone", "Z1", {})
        _add_material_and_construction(doc)
        doc.add(
            "BuildingSurface:Detailed",
            "Wall1",
            {
                "surface_type": "Wall",
                "construction_name": "C",
                "zone_name": "Z1",
                "outside_boundary_condition": "Outdoors",
                **_WALL_VERTICES,
            },
        )
        doc.add(
            "FenestrationSurface:Detailed",
            "NoVertWindow",
            {
                "surface_type": "Window",
                "construction_name": "C",
                "building_surface_name": "Wall1",
            },
            validate=False,
        )
        surfaces = _resolve_surfaces(doc)
        fen = [s for s in surfaces if s.is_fenestration]
        assert len(fen) == 0

    def test_shading_no_vertices(self) -> None:
        """Shading:Site:Detailed with no vertex data should be skipped."""
        doc = new_document(version=(24, 1, 0))
        doc.add("Zone", "Z1", {})
        doc.add("Shading:Site:Detailed", "NoVertShade", {})
        surfaces = _resolve_surfaces(doc)
        shading = [s for s in surfaces if s.is_shading]
        assert len(shading) == 0

    def test_building_surface_zone_not_found(self) -> None:
        """BuildingSurface with zone_name not matching any Zone object skips world transform."""
        doc = new_document(version=(24, 1, 0))
        doc.add("Zone", "ExistingZone", {"x_origin": 10.0, "y_origin": 0.0, "z_origin": 0.0})
        _add_material_and_construction(doc)
        doc.add(
            "BuildingSurface:Detailed",
            "Wall1",
            {
                "surface_type": "Wall",
                "construction_name": "C",
                "zone_name": "NonExistentZone",
                "outside_boundary_condition": "Outdoors",
                **_WALL_VERTICES,
            },
            validate=False,
        )
        # Include the non-existent zone name in the filter
        surfaces = _resolve_surfaces(doc, zones=["NonExistentZone"])
        assert len(surfaces) == 1
        # Coords should NOT be transformed (zone_obj is None)
        xs = [v.x for v in surfaces[0].polygon.vertices]
        assert min(xs) == pytest.approx(0.0)

    def test_fenestration_zone_obj_not_found(self) -> None:
        """Fenestration where parent zone doesn't match any Zone object skips world transform."""
        doc = new_document(version=(24, 1, 0))
        doc.add("Zone", "ExistingZone", {"x_origin": 10.0, "y_origin": 0.0, "z_origin": 0.0})
        _add_material_and_construction(doc)
        doc.add(
            "BuildingSurface:Detailed",
            "Wall1",
            {
                "surface_type": "Wall",
                "construction_name": "C",
                "zone_name": "GhostZone",
                "outside_boundary_condition": "Outdoors",
                **_WALL_VERTICES,
            },
            validate=False,
        )
        doc.add(
            "FenestrationSurface:Detailed",
            "Win1",
            {
                "surface_type": "Window",
                "construction_name": "C",
                "building_surface_name": "Wall1",
                "number_of_vertices": 4,
                "vertex_1_x_coordinate": 1.0,
                "vertex_1_y_coordinate": 0.0,
                "vertex_1_z_coordinate": 2.5,
                "vertex_2_x_coordinate": 1.0,
                "vertex_2_y_coordinate": 0.0,
                "vertex_2_z_coordinate": 0.5,
                "vertex_3_x_coordinate": 4.0,
                "vertex_3_y_coordinate": 0.0,
                "vertex_3_z_coordinate": 0.5,
                "vertex_4_x_coordinate": 4.0,
                "vertex_4_y_coordinate": 0.0,
                "vertex_4_z_coordinate": 2.5,
            },
        )
        surfaces = _resolve_surfaces(doc, zones=["GhostZone"])
        fen = [s for s in surfaces if s.is_fenestration]
        assert len(fen) == 1
        # Coords should NOT be transformed
        xs = [v.x for v in fen[0].polygon.vertices]
        assert min(xs) == pytest.approx(1.0)

    def test_shading_zone_with_nonexistent_zone_obj(self) -> None:
        """Shading:Zone:Detailed with base surface whose zone has no Zone object."""
        doc = new_document(version=(24, 1, 0))
        doc.add("Zone", "ExistingZone", {"x_origin": 10.0, "y_origin": 0.0, "z_origin": 0.0})
        _add_material_and_construction(doc)
        doc.add(
            "BuildingSurface:Detailed",
            "Wall1",
            {
                "surface_type": "Wall",
                "construction_name": "C",
                "zone_name": "GhostZone",
                "outside_boundary_condition": "Outdoors",
                **_WALL_VERTICES,
            },
            validate=False,
        )
        doc.add(
            "Shading:Zone:Detailed",
            "ZoneShade1",
            {
                "base_surface_name": "Wall1",
                "number_of_vertices": 3,
                "vertex_1_x_coordinate": 0.0,
                "vertex_1_y_coordinate": 0.0,
                "vertex_1_z_coordinate": 3.0,
                "vertex_2_x_coordinate": 5.0,
                "vertex_2_y_coordinate": 0.0,
                "vertex_2_z_coordinate": 3.0,
                "vertex_3_x_coordinate": 5.0,
                "vertex_3_y_coordinate": -1.0,
                "vertex_3_z_coordinate": 4.0,
            },
        )
        surfaces = _resolve_surfaces(doc, zones=["GhostZone"])
        shading = [s for s in surfaces if s.is_shading]
        assert len(shading) == 1
        # No transform applied since zone_obj is None
        xs = [v.x for v in shading[0].polygon.vertices]
        assert min(xs) == pytest.approx(0.0)

    def test_shading_zone_with_nonexistent_base_surface(self) -> None:
        """Shading:Zone:Detailed with base_surface_name that doesn't exist."""
        doc = new_document(version=(24, 1, 0))
        doc.add("Zone", "Z1", {"x_origin": 10.0, "y_origin": 0.0, "z_origin": 0.0})
        doc.add(
            "Shading:Zone:Detailed",
            "ZoneShade1",
            {
                "base_surface_name": "NonExistentWall",
                "number_of_vertices": 3,
                "vertex_1_x_coordinate": 0.0,
                "vertex_1_y_coordinate": 0.0,
                "vertex_1_z_coordinate": 3.0,
                "vertex_2_x_coordinate": 5.0,
                "vertex_2_y_coordinate": 0.0,
                "vertex_2_z_coordinate": 3.0,
                "vertex_3_x_coordinate": 5.0,
                "vertex_3_y_coordinate": -1.0,
                "vertex_3_z_coordinate": 4.0,
            },
        )
        surfaces = _resolve_surfaces(doc)
        shading = [s for s in surfaces if s.is_shading]
        assert len(shading) == 1
        # No transform - parent_obj is None
        xs = [v.x for v in shading[0].polygon.vertices]
        assert min(xs) == pytest.approx(0.0)


class TestResolveSurfacesFenestrationEdgeCases:
    """Additional fenestration edge cases for _resolve_surfaces."""

    def test_fenestration_no_parent(self) -> None:
        """Fenestration with non-existent parent should be excluded (zone not in include)."""
        doc = new_document(version=(24, 1, 0))
        doc.add("Zone", "Z1", {})
        _add_material_and_construction(doc)
        doc.add(
            "FenestrationSurface:Detailed",
            "OrphanWindow",
            {
                "surface_type": "Window",
                "construction_name": "C",
                "building_surface_name": "NonExistentWall",
                "number_of_vertices": 4,
                "vertex_1_x_coordinate": 1.0,
                "vertex_1_y_coordinate": 0.0,
                "vertex_1_z_coordinate": 2.5,
                "vertex_2_x_coordinate": 1.0,
                "vertex_2_y_coordinate": 0.0,
                "vertex_2_z_coordinate": 0.5,
                "vertex_3_x_coordinate": 4.0,
                "vertex_3_y_coordinate": 0.0,
                "vertex_3_z_coordinate": 0.5,
                "vertex_4_x_coordinate": 4.0,
                "vertex_4_y_coordinate": 0.0,
                "vertex_4_z_coordinate": 2.5,
            },
        )
        surfaces = _resolve_surfaces(doc)
        fen = [s for s in surfaces if s.is_fenestration]
        assert len(fen) == 0

    def test_fenestration_with_zone_transform(self, fenestration_doc) -> None:  # type: ignore[no-untyped-def]
        """Fenestration should inherit zone transforms from parent surface."""
        surfaces = _resolve_surfaces(fenestration_doc)
        window = next(s for s in surfaces if s.name == "WindowA1")
        assert window.is_fenestration is True
        assert window.polygon.num_vertices == 4


class TestGetColorBranches:
    """Tests for _get_color covering all ColorBy branches."""

    def test_fenestration_color(self) -> None:
        from idfkit.visualization.model import _FENESTRATION_COLOR  # pyright: ignore[reportPrivateUsage]

        s = _ResolvedSurface("W", "Z", "Window", "Outdoors", "C", Polygon3D([]), 0.0, True)
        color = _get_color(s, ModelViewConfig(), {})
        assert color == _FENESTRATION_COLOR

    def test_shading_color(self) -> None:
        from idfkit.visualization.model import _SHADING_COLOR  # pyright: ignore[reportPrivateUsage]

        s = _ResolvedSurface("S", "", "Shading", "", "", Polygon3D([]), 0.0, False, is_shading=True)
        color = _get_color(s, ModelViewConfig(), {})
        assert color == _SHADING_COLOR

    def test_zone_color(self) -> None:
        s = _ResolvedSurface("W", "Zone1", "Wall", "Outdoors", "C", Polygon3D([]), 0.0, False)
        zone_colors = {"ZONE1": "#abcdef"}
        color = _get_color(s, ModelViewConfig(color_by=ColorBy.ZONE), zone_colors)
        assert color == "#abcdef"

    def test_surface_type_color(self) -> None:
        s = _ResolvedSurface("W", "Z", "Floor", "Ground", "C", Polygon3D([]), 0.0, False)
        cfg = ModelViewConfig(color_by=ColorBy.SURFACE_TYPE)
        color = _get_color(s, cfg, {})
        assert color == "#59a14f"

    def test_surface_type_unknown(self) -> None:
        s = _ResolvedSurface("W", "Z", "UnknownType", "Outdoors", "C", Polygon3D([]), 0.0, False)
        cfg = ModelViewConfig(color_by=ColorBy.SURFACE_TYPE)
        color = _get_color(s, cfg, {})
        assert color == "#999999"

    def test_boundary_condition_color(self) -> None:
        s = _ResolvedSurface("W", "Z", "Wall", "Ground", "C", Polygon3D([]), 0.0, False)
        cfg = ModelViewConfig(color_by=ColorBy.BOUNDARY_CONDITION)
        color = _get_color(s, cfg, {})
        assert color == "#59a14f"

    def test_boundary_condition_unknown(self) -> None:
        s = _ResolvedSurface("W", "Z", "Wall", "Unknown", "C", Polygon3D([]), 0.0, False)
        cfg = ModelViewConfig(color_by=ColorBy.BOUNDARY_CONDITION)
        color = _get_color(s, cfg, {})
        assert color == "#999999"

    def test_construction_color(self) -> None:
        s = _ResolvedSurface("W", "Z", "Wall", "Outdoors", "BrickWall", Polygon3D([]), 0.0, False)
        cfg = ModelViewConfig(color_by=ColorBy.CONSTRUCTION)
        zone_colors = {"BRICKWALL": "#ff0000"}
        color = _get_color(s, cfg, zone_colors)
        assert color == "#ff0000"


class TestAssignZoneColorsConstruction:
    """Test _assign_zone_colors with construction-based coloring."""

    def test_construction_keys(self) -> None:
        s1 = _ResolvedSurface("A", "Z1", "Wall", "Outdoors", "Brick", Polygon3D([]), 0.0, False)
        s2 = _ResolvedSurface("B", "Z1", "Wall", "Outdoors", "Glass", Polygon3D([]), 0.0, False)
        s3 = _ResolvedSurface("C", "Z1", "Window", "Outdoors", "WinConst", Polygon3D([]), 0.0, True)
        s4 = _ResolvedSurface("D", "", "Shading", "", "", Polygon3D([]), 0.0, False, is_shading=True)
        cfg = ModelViewConfig(color_by=ColorBy.CONSTRUCTION)
        colors = _assign_zone_colors([s1, s2, s3, s4], cfg)
        assert "BRICK" in colors
        assert "GLASS" in colors
        assert "WINCONST" not in colors


class TestBuildHoverTextEdgeCases:
    """Test _build_hover_text with empty fields."""

    def test_no_zone(self) -> None:
        s = _ResolvedSurface("S", "", "Shading", "", "", Polygon3D([]), 10.0, False, is_shading=True)
        text = _build_hover_text(s)
        assert "Zone:" not in text

    def test_no_construction(self) -> None:
        s = _ResolvedSurface("S", "Z", "Wall", "Outdoors", "", Polygon3D([]), 10.0, False)
        text = _build_hover_text(s)
        assert "Construction:" not in text

    def test_no_boundary(self) -> None:
        s = _ResolvedSurface("S", "Z", "Wall", "", "C", Polygon3D([]), 10.0, False)
        text = _build_hover_text(s)
        assert "Boundary:" not in text

    def test_all_fields_present(self) -> None:
        s = _ResolvedSurface("TestSurf", "MyZone", "Wall", "Outdoors", "BrickWall", Polygon3D([]), 25.0, False)
        text = _build_hover_text(s)
        assert "<b>TestSurf</b>" in text
        assert "Zone: MyZone" in text
        assert "Type: Wall" in text
        assert "Area: 25.00" in text
        assert "Construction: BrickWall" in text
        assert "Boundary: Outdoors" in text


class TestOffsetFenestration:
    """Tests for _offset_fenestration."""

    def test_offset_along_normal(self) -> None:
        poly = Polygon3D([Vector3D(0, 0, 0), Vector3D(1, 0, 0), Vector3D(1, 1, 0), Vector3D(0, 1, 0)])
        normal = Vector3D(0, 0, 1)
        result = _offset_fenestration(poly, normal)
        assert result.vertices[0].z == pytest.approx(0.02)
        assert result.vertices[0].x == pytest.approx(0.0)


class TestLegendLabel:
    """Tests for _legend_label covering all branches."""

    def test_fenestration(self) -> None:
        s = _ResolvedSurface("W", "Z", "Window", "", "C", Polygon3D([]), 0.0, True)
        assert _legend_label(s, ModelViewConfig()) == "Fenestration"

    def test_shading(self) -> None:
        s = _ResolvedSurface("S", "", "Shading", "", "", Polygon3D([]), 0.0, False, is_shading=True)
        assert _legend_label(s, ModelViewConfig()) == "Shading"

    def test_zone(self) -> None:
        s = _ResolvedSurface("W", "MyZone", "Wall", "Outdoors", "C", Polygon3D([]), 0.0, False)
        assert _legend_label(s, ModelViewConfig(color_by=ColorBy.ZONE)) == "MyZone"

    def test_zone_empty(self) -> None:
        s = _ResolvedSurface("W", "", "Wall", "Outdoors", "C", Polygon3D([]), 0.0, False)
        assert _legend_label(s, ModelViewConfig(color_by=ColorBy.ZONE)) == "Unknown"

    def test_surface_type(self) -> None:
        s = _ResolvedSurface("W", "Z", "Wall", "Outdoors", "C", Polygon3D([]), 0.0, False)
        assert _legend_label(s, ModelViewConfig(color_by=ColorBy.SURFACE_TYPE)) == "Wall"

    def test_surface_type_empty(self) -> None:
        s = _ResolvedSurface("W", "Z", "", "Outdoors", "C", Polygon3D([]), 0.0, False)
        assert _legend_label(s, ModelViewConfig(color_by=ColorBy.SURFACE_TYPE)) == "Unknown"

    def test_boundary(self) -> None:
        s = _ResolvedSurface("W", "Z", "Wall", "Outdoors", "C", Polygon3D([]), 0.0, False)
        assert _legend_label(s, ModelViewConfig(color_by=ColorBy.BOUNDARY_CONDITION)) == "Outdoors"

    def test_boundary_empty(self) -> None:
        s = _ResolvedSurface("W", "Z", "Wall", "", "C", Polygon3D([]), 0.0, False)
        assert _legend_label(s, ModelViewConfig(color_by=ColorBy.BOUNDARY_CONDITION)) == "Unknown"

    def test_construction(self) -> None:
        s = _ResolvedSurface("W", "Z", "Wall", "Outdoors", "BrickWall", Polygon3D([]), 0.0, False)
        assert _legend_label(s, ModelViewConfig(color_by=ColorBy.CONSTRUCTION)) == "BrickWall"

    def test_construction_empty(self) -> None:
        s = _ResolvedSurface("W", "Z", "Wall", "Outdoors", "", Polygon3D([]), 0.0, False)
        assert _legend_label(s, ModelViewConfig(color_by=ColorBy.CONSTRUCTION)) == "Unknown"


# ---------------------------------------------------------------------------
# Plotly-dependent trace building tests
# ---------------------------------------------------------------------------

_TRIANGLE_POLY = Polygon3D([Vector3D(0, 0, 0), Vector3D(1, 0, 0), Vector3D(0.5, 1, 0)])
_QUAD_POLY = Polygon3D([Vector3D(0, 0, 0), Vector3D(5, 0, 0), Vector3D(5, 5, 0), Vector3D(0, 5, 0)])


class TestBuildMeshTraces:
    """Tests for _build_mesh_traces."""

    def test_basic_mesh(self) -> None:
        pytest.importorskip("plotly.graph_objects")
        surfaces = [_ResolvedSurface("W1", "Z1", "Wall", "Outdoors", "C", _QUAD_POLY, 25.0, False)]
        cfg = ModelViewConfig()
        zone_colors = {"Z1": "#4e79a7"}
        traces = _build_mesh_traces(surfaces, cfg, zone_colors)
        assert len(traces) >= 1

    def test_fenestration_skipped_when_disabled(self) -> None:
        pytest.importorskip("plotly.graph_objects")
        surfaces = [
            _ResolvedSurface("W1", "Z1", "Wall", "Outdoors", "C", _QUAD_POLY, 25.0, False),
            _ResolvedSurface("Win1", "Z1", "Window", "", "C", _TRIANGLE_POLY, 1.0, True),
        ]
        cfg = ModelViewConfig(show_fenestration=False)
        zone_colors = {"Z1": "#4e79a7"}
        traces = _build_mesh_traces(surfaces, cfg, zone_colors)
        all_names = [t.name for t in traces]
        assert "Fenestration" not in all_names

    def test_fenestration_included_when_enabled(self) -> None:
        pytest.importorskip("plotly.graph_objects")
        surfaces = [
            _ResolvedSurface("W1", "Z1", "Wall", "Outdoors", "C", _QUAD_POLY, 25.0, False),
            _ResolvedSurface("Win1", "Z1", "Window", "", "C", _TRIANGLE_POLY, 1.0, True),
        ]
        cfg = ModelViewConfig(show_fenestration=True)
        zone_colors = {"Z1": "#4e79a7"}
        traces = _build_mesh_traces(surfaces, cfg, zone_colors)
        all_names = [t.name for t in traces]
        assert "Fenestration" in all_names

    def test_opacity_settings(self) -> None:
        go = pytest.importorskip("plotly.graph_objects")
        surfaces = [
            _ResolvedSurface("W1", "Z1", "Wall", "Outdoors", "C", _QUAD_POLY, 25.0, False),
            _ResolvedSurface("Win1", "Z1", "Window", "", "C", _TRIANGLE_POLY, 1.0, True),
        ]
        cfg = ModelViewConfig(opacity=0.9, fenestration_opacity=0.3)
        zone_colors = {"Z1": "#4e79a7"}
        traces = _build_mesh_traces(surfaces, cfg, zone_colors)
        mesh_traces = [t for t in traces if isinstance(t, go.Mesh3d)]
        opacities = {t.name: t.opacity for t in mesh_traces}
        assert opacities.get("Fenestration") == pytest.approx(0.3)


class TestBuildEdgeTraces:
    """Tests for _build_edge_traces."""

    def test_basic_edges(self) -> None:
        go = pytest.importorskip("plotly.graph_objects")
        surfaces = [_ResolvedSurface("W1", "Z1", "Wall", "Outdoors", "C", _QUAD_POLY, 25.0, False)]
        cfg = ModelViewConfig()
        traces = _build_edge_traces(surfaces, cfg)
        assert len(traces) == 1
        assert isinstance(traces[0], go.Scatter3d)
        assert traces[0].mode == "lines"

    def test_fenestration_edges_skipped_when_disabled(self) -> None:
        pytest.importorskip("plotly.graph_objects")
        fen = _ResolvedSurface("Win1", "Z1", "Window", "", "C", _TRIANGLE_POLY, 1.0, True)
        cfg = ModelViewConfig(show_fenestration=False)
        traces = _build_edge_traces([fen], cfg)
        assert len(traces[0].x) == 0

    def test_fenestration_edges_included_and_offset(self) -> None:
        pytest.importorskip("plotly.graph_objects")
        fen = _ResolvedSurface("Win1", "Z1", "Window", "", "C", _TRIANGLE_POLY, 1.0, True)
        cfg = ModelViewConfig(show_fenestration=True)
        traces = _build_edge_traces([fen], cfg)
        assert len(traces[0].x) == 9


class TestBuildLabelTraces:
    """Tests for _build_label_traces."""

    def test_basic_labels(self) -> None:
        go = pytest.importorskip("plotly.graph_objects")
        surfaces = [
            _ResolvedSurface("W1", "Z1", "Wall", "Outdoors", "C", _QUAD_POLY, 25.0, False),
            _ResolvedSurface("W2", "Z2", "Wall", "Outdoors", "C", _TRIANGLE_POLY, 1.0, False),
        ]
        traces = _build_label_traces(surfaces)
        assert len(traces) == 1
        assert isinstance(traces[0], go.Scatter3d)
        assert traces[0].mode == "text"
        assert len(traces[0].text) == 2

    def test_no_labels_for_empty(self) -> None:
        pytest.importorskip("plotly.graph_objects")
        traces = _build_label_traces([])
        assert traces == []

    def test_fenestration_and_shading_excluded(self) -> None:
        pytest.importorskip("plotly.graph_objects")
        surfaces = [
            _ResolvedSurface("Win", "Z1", "Window", "", "C", _TRIANGLE_POLY, 1.0, True),
            _ResolvedSurface("Shade", "", "Shading", "", "", _TRIANGLE_POLY, 1.0, False, is_shading=True),
        ]
        traces = _build_label_traces(surfaces)
        assert traces == []

    def test_zone_centroid_calculation(self) -> None:
        pytest.importorskip("plotly.graph_objects")
        poly1 = Polygon3D([Vector3D(0, 0, 0), Vector3D(2, 0, 0), Vector3D(2, 2, 0), Vector3D(0, 2, 0)])
        poly2 = Polygon3D([Vector3D(4, 0, 0), Vector3D(6, 0, 0), Vector3D(6, 2, 0), Vector3D(4, 2, 0)])
        surfaces = [
            _ResolvedSurface("W1", "Z1", "Wall", "Outdoors", "C", poly1, 4.0, False),
            _ResolvedSurface("W2", "Z1", "Wall", "Outdoors", "C", poly2, 4.0, False),
        ]
        traces = _build_label_traces(surfaces)
        assert len(traces) == 1
        assert traces[0].x[0] == pytest.approx(3.0, abs=0.1)


class TestMake3dLayout:
    """Tests for _make_3d_layout."""

    def test_layout_properties(self) -> None:
        go = pytest.importorskip("plotly.graph_objects")
        cfg = ModelViewConfig(width=800, height=600, background_color="#ffffff")
        layout = _make_3d_layout(go, cfg, "Test Title")
        assert layout.title.text == "Test Title"
        assert layout.width == 800
        assert layout.height == 600

    def test_layout_no_title(self) -> None:
        go = pytest.importorskip("plotly.graph_objects")
        cfg = ModelViewConfig()
        layout = _make_3d_layout(go, cfg, None)
        assert layout.title.text is None


class TestComputeZoneOffsets:
    """Tests for _compute_zone_offsets."""

    def test_two_zones(self) -> None:
        poly1 = Polygon3D([Vector3D(0, 0, 0), Vector3D(5, 0, 0), Vector3D(5, 5, 0), Vector3D(0, 5, 0)])
        poly2 = Polygon3D([Vector3D(10, 0, 0), Vector3D(15, 0, 0), Vector3D(15, 5, 0), Vector3D(10, 5, 0)])
        surfaces = [
            _ResolvedSurface("W1", "ZoneA", "Wall", "Outdoors", "C", poly1, 25.0, False),
            _ResolvedSurface("W2", "ZoneB", "Wall", "Outdoors", "C", poly2, 25.0, False),
        ]
        offsets = _compute_zone_offsets(surfaces, 5.0)
        assert "ZONEA" in offsets
        assert "ZONEB" in offsets

    def test_single_zone_at_centroid(self) -> None:
        """When zone centroid equals building centroid, offset should default."""
        poly = Polygon3D([Vector3D(0, 0, 0), Vector3D(1, 0, 0), Vector3D(1, 1, 0), Vector3D(0, 1, 0)])
        surfaces = [_ResolvedSurface("W1", "Z1", "Wall", "Outdoors", "C", poly, 1.0, False)]
        offsets = _compute_zone_offsets(surfaces, 5.0)
        assert offsets["Z1"].x == pytest.approx(5.0)
        assert offsets["Z1"].y == pytest.approx(0.0)

    def test_shading_excluded(self) -> None:
        poly = Polygon3D([Vector3D(0, 0, 0), Vector3D(5, 0, 0), Vector3D(5, 5, 0), Vector3D(0, 5, 0)])
        surfaces = [_ResolvedSurface("S1", "", "Shading", "", "", poly, 25.0, False, is_shading=True)]
        offsets = _compute_zone_offsets(surfaces, 5.0)
        assert len(offsets) == 0

    def test_no_surfaces(self) -> None:
        offsets = _compute_zone_offsets([], 5.0)
        assert len(offsets) == 0


class TestApplyZoneOffsets:
    """Tests for _apply_zone_offsets."""

    def test_offsets_applied(self) -> None:
        poly = Polygon3D([Vector3D(0, 0, 0), Vector3D(1, 0, 0), Vector3D(1, 1, 0)])
        surfaces = [_ResolvedSurface("W1", "ZoneA", "Wall", "Outdoors", "C", poly, 1.0, False)]
        zone_offsets = {"ZONEA": Vector3D(10, 0, 0)}
        result = _apply_zone_offsets(surfaces, zone_offsets)
        assert len(result) == 1
        assert result[0].polygon.vertices[0].x == pytest.approx(10.0)
        assert result[0].polygon.vertices[1].x == pytest.approx(11.0)

    def test_no_zone_no_offset(self) -> None:
        poly = Polygon3D([Vector3D(0, 0, 0), Vector3D(1, 0, 0), Vector3D(1, 1, 0)])
        surfaces = [_ResolvedSurface("S1", "", "Shading", "", "", poly, 1.0, False, is_shading=True)]
        zone_offsets = {"ZONEA": Vector3D(10, 0, 0)}
        result = _apply_zone_offsets(surfaces, zone_offsets)
        assert result[0].polygon.vertices[0].x == pytest.approx(0.0)

    def test_preserves_all_fields(self) -> None:
        poly = Polygon3D([Vector3D(0, 0, 0), Vector3D(1, 0, 0), Vector3D(1, 1, 0)])
        s = _ResolvedSurface("W1", "Z1", "Wall", "Outdoors", "Brick", poly, 5.0, True, is_shading=False)
        result = _apply_zone_offsets([s], {"Z1": Vector3D(1, 0, 0)})
        r = result[0]
        assert r.name == "W1"
        assert r.zone == "Z1"
        assert r.surface_type == "Wall"
        assert r.boundary == "Outdoors"
        assert r.construction == "Brick"
        assert r.area == 5.0
        assert r.is_fenestration is True
        assert r.is_shading is False


# ---------------------------------------------------------------------------
# Full public API integration tests (require plotly)
# ---------------------------------------------------------------------------


class TestViewModelFullCoverage:
    """Additional view_model tests for full code coverage."""

    def test_labels_disabled(self, multi_zone_doc) -> None:  # type: ignore[no-untyped-def]
        go = pytest.importorskip("plotly.graph_objects")
        from idfkit.visualization.model import view_model

        cfg = ModelViewConfig(show_labels=False, show_edges=False)
        fig = view_model(multi_zone_doc, config=cfg)
        assert isinstance(fig, go.Figure)
        text_traces = [t for t in fig.data if isinstance(t, go.Scatter3d) and t.mode == "text"]
        assert len(text_traces) == 0

    def test_no_title(self, multi_zone_doc) -> None:  # type: ignore[no-untyped-def]
        go = pytest.importorskip("plotly.graph_objects")
        from idfkit.visualization.model import view_model

        fig = view_model(multi_zone_doc, title=None)
        assert isinstance(fig, go.Figure)

    def test_with_fenestration(self, fenestration_doc) -> None:  # type: ignore[no-untyped-def]
        go = pytest.importorskip("plotly.graph_objects")
        from idfkit.visualization.model import view_model

        fig = view_model(fenestration_doc)
        assert isinstance(fig, go.Figure)
        assert len(fig.data) > 0


class TestViewFloorPlanFullCoverage:
    """Additional view_floor_plan tests for full coverage."""

    def test_with_z_cut(self, multi_zone_doc) -> None:  # type: ignore[no-untyped-def]
        go = pytest.importorskip("plotly.graph_objects")
        from idfkit.visualization.model import view_floor_plan

        fig = view_floor_plan(multi_zone_doc, z_cut=1.5)
        assert isinstance(fig, go.Figure)
        scatter_traces = [t for t in fig.data if isinstance(t, go.Scatter)]
        assert len(scatter_traces) > 0

    def test_z_cut_excludes_walls_above(self, multi_zone_doc) -> None:  # type: ignore[no-untyped-def]
        pytest.importorskip("plotly.graph_objects")
        from idfkit.visualization.model import view_floor_plan

        fig_high = view_floor_plan(multi_zone_doc, z_cut=10.0)
        fig_low = view_floor_plan(multi_zone_doc, z_cut=-1.0)
        assert len(fig_high.data) >= len(fig_low.data)

    def test_color_by_surface_type(self, multi_zone_doc) -> None:  # type: ignore[no-untyped-def]
        go = pytest.importorskip("plotly.graph_objects")
        from idfkit.visualization.model import view_floor_plan

        cfg = ModelViewConfig(color_by=ColorBy.SURFACE_TYPE)
        fig = view_floor_plan(multi_zone_doc, config=cfg)
        assert isinstance(fig, go.Figure)

    def test_zones_filter(self, multi_zone_doc) -> None:  # type: ignore[no-untyped-def]
        go = pytest.importorskip("plotly.graph_objects")
        from idfkit.visualization.model import view_floor_plan

        fig = view_floor_plan(multi_zone_doc, zones=["ZoneA"])
        assert isinstance(fig, go.Figure)

    def test_fenestration_and_shading_excluded(self, fenestration_doc) -> None:  # type: ignore[no-untyped-def]
        go = pytest.importorskip("plotly.graph_objects")
        from idfkit.visualization.model import view_floor_plan

        fig = view_floor_plan(fenestration_doc)
        assert isinstance(fig, go.Figure)

    def test_legend_dedup(self, multi_zone_doc) -> None:  # type: ignore[no-untyped-def]
        go = pytest.importorskip("plotly.graph_objects")
        from idfkit.visualization.model import view_floor_plan

        fig = view_floor_plan(multi_zone_doc)
        scatter_traces = [t for t in fig.data if isinstance(t, go.Scatter)]
        legend_names = [t.name for t in scatter_traces if t.showlegend]
        assert len(legend_names) == len(set(legend_names))


class TestViewExplodedFullCoverage:
    """Additional view_exploded tests for full coverage."""

    def test_custom_separation(self, multi_zone_doc) -> None:  # type: ignore[no-untyped-def]
        go = pytest.importorskip("plotly.graph_objects")
        from idfkit.visualization.model import view_exploded

        fig = view_exploded(multi_zone_doc, separation=20.0)
        assert isinstance(fig, go.Figure)
        assert len(fig.data) > 0

    def test_no_edges_no_labels(self, multi_zone_doc) -> None:  # type: ignore[no-untyped-def]
        go = pytest.importorskip("plotly.graph_objects")
        from idfkit.visualization.model import view_exploded

        cfg = ModelViewConfig(show_edges=False, show_labels=False)
        fig = view_exploded(multi_zone_doc, config=cfg)
        assert isinstance(fig, go.Figure)

    def test_zones_filter(self, multi_zone_doc) -> None:  # type: ignore[no-untyped-def]
        go = pytest.importorskip("plotly.graph_objects")
        from idfkit.visualization.model import view_exploded

        fig = view_exploded(multi_zone_doc, zones=["ZoneA"])
        assert isinstance(fig, go.Figure)


class TestViewNormalsFullCoverage:
    """Additional view_normals tests for full coverage."""

    def test_custom_arrow_length(self, multi_zone_doc) -> None:  # type: ignore[no-untyped-def]
        go = pytest.importorskip("plotly.graph_objects")
        from idfkit.visualization.model import view_normals

        fig = view_normals(multi_zone_doc, arrow_length=2.0)
        assert isinstance(fig, go.Figure)
        cones = [t for t in fig.data if isinstance(t, go.Cone)]
        assert len(cones) == 1

    def test_no_edges(self, multi_zone_doc) -> None:  # type: ignore[no-untyped-def]
        go = pytest.importorskip("plotly.graph_objects")
        from idfkit.visualization.model import view_normals

        cfg = ModelViewConfig(show_edges=False)
        fig = view_normals(multi_zone_doc, config=cfg)
        assert isinstance(fig, go.Figure)

    def test_zones_filter(self, multi_zone_doc) -> None:  # type: ignore[no-untyped-def]
        go = pytest.importorskip("plotly.graph_objects")
        from idfkit.visualization.model import view_normals

        fig = view_normals(multi_zone_doc, zones=["ZoneA"])
        assert isinstance(fig, go.Figure)

    def test_reduced_opacity(self, multi_zone_doc) -> None:  # type: ignore[no-untyped-def]
        go = pytest.importorskip("plotly.graph_objects")
        from idfkit.visualization.model import view_normals

        cfg = ModelViewConfig(opacity=1.0, fenestration_opacity=1.0)
        fig = view_normals(multi_zone_doc, config=cfg)
        assert isinstance(fig, go.Figure)
        mesh_traces = [t for t in fig.data if isinstance(t, go.Mesh3d)]
        for t in mesh_traces:
            assert t.opacity == pytest.approx(0.4)

    def test_empty_model_no_cones(self) -> None:
        go = pytest.importorskip("plotly.graph_objects")
        from idfkit.visualization.model import view_normals

        doc = new_document(version=(24, 1, 0))
        doc.add("Zone", "Z1", {})
        fig = view_normals(doc)
        assert isinstance(fig, go.Figure)
        cones = [t for t in fig.data if isinstance(t, go.Cone)]
        assert len(cones) == 0

    def test_with_fenestration(self, fenestration_doc) -> None:  # type: ignore[no-untyped-def]
        go = pytest.importorskip("plotly.graph_objects")
        from idfkit.visualization.model import view_normals

        fig = view_normals(fenestration_doc)
        assert isinstance(fig, go.Figure)
        cones = [t for t in fig.data if isinstance(t, go.Cone)]
        assert len(cones) == 1
