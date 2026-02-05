"""Tests for idfkit.visualization.model -- 3D building visualization."""

from __future__ import annotations

import pytest

from idfkit import new_document
from idfkit.geometry import Polygon3D, Vector3D
from idfkit.visualization.model import (
    ColorBy,
    ModelViewConfig,
    _assign_zone_colors,
    _build_hover_text,
    _polygon_edges,
    _resolve_surfaces,
    _ResolvedSurface,
    _triangulate_polygon,
)

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
