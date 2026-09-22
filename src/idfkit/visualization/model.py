"""3D building model visualization using plotly.

Provides interactive 3D viewers for EnergyPlus building geometry,
including standard views, floor plans, exploded diagrams, and
surface normal visualization.

Example:
    >>> from idfkit import load_idf
    >>> from idfkit.visualization import view_model
    >>>
    >>> model = load_idf("building.idf")
    >>> fig = view_model(model)
    >>> fig.show()
"""

from __future__ import annotations

from dataclasses import dataclass, replace
from enum import Enum
from typing import TYPE_CHECKING, Any

from ..geometry import Polygon3D, Vector3D
from ..scene import ResolvedSurface, get_scene

if TYPE_CHECKING:
    from ..document import IDFDocument


class ColorBy(Enum):
    """Strategy for coloring surfaces in 3D views."""

    ZONE = "zone"
    SURFACE_TYPE = "surface_type"
    BOUNDARY_CONDITION = "boundary"
    CONSTRUCTION = "construction"


@dataclass(frozen=True)
class ModelViewConfig:
    """Configuration for 3D model visualization.

    Attributes:
        width: Figure width in pixels.
        height: Figure height in pixels.
        color_by: Strategy for coloring surfaces.
        show_fenestration: Whether to display windows/doors.
        show_edges: Whether to display wireframe edges.
        show_labels: Whether to display zone labels.
        opacity: Surface opacity (0-1).
        fenestration_opacity: Window/door opacity (0-1).
        background_color: Plot background color.
        edge_color: Wireframe edge color.
        edge_width: Wireframe edge width.
    """

    width: int = 1000
    height: int = 700
    color_by: ColorBy = ColorBy.ZONE
    show_fenestration: bool = True
    show_edges: bool = True
    show_labels: bool = True
    opacity: float = 0.85
    fenestration_opacity: float = 0.4
    background_color: str = "#f8f9fa"
    edge_color: str = "rgba(40, 40, 40, 0.6)"
    edge_width: float = 1.5


# ---------------------------------------------------------------------------
# Color palettes
# ---------------------------------------------------------------------------

_ZONE_PALETTE: list[str] = [
    "#4e79a7",
    "#f28e2b",
    "#e15759",
    "#76b7b2",
    "#59a14f",
    "#edc948",
    "#b07aa1",
    "#ff9da7",
    "#9c755f",
    "#bab0ac",
    "#5fa2ce",
    "#fc7d0b",
    "#a3acb9",
    "#c85200",
    "#1170aa",
    "#57606c",
    "#7b848f",
    "#c7c7c7",
    "#8cd17d",
    "#b6992d",
]

_SURFACE_TYPE_COLORS: dict[str, str] = {
    "wall": "#4e79a7",
    "floor": "#59a14f",
    "roof": "#e15759",
    "ceiling": "#edc948",
}

_BOUNDARY_COLORS: dict[str, str] = {
    "outdoors": "#4e79a7",
    "ground": "#59a14f",
    "surface": "#edc948",
    "adiabatic": "#b07aa1",
    "zone": "#76b7b2",
}

_FENESTRATION_COLOR = "#87ceeb"
_SHADING_COLOR = "#b0b0b0"


# ---------------------------------------------------------------------------
# Lazy plotly import
# ---------------------------------------------------------------------------


def _get_go() -> Any:
    """Get plotly.graph_objects, raising ImportError if unavailable."""
    try:
        import plotly.graph_objects as go  # type: ignore[import-not-found]
    except ImportError:
        msg = "plotly is required for 3D model visualization. Install it with: pip install idfkit[plotly]"
        raise ImportError(msg) from None
    return go


# ---------------------------------------------------------------------------
# Surface resolution
# ---------------------------------------------------------------------------

#: The one geometry type that names a parent surface rather than a zone. The renderer draws it
#: differently, and the scene records the parent it resolved against rather than a flag.
_FENESTRATION = "FenestrationSurface:Detailed"


def _is_fenestration(surface: ResolvedSurface) -> bool:
    """Whether the scene placed this surface in its parent's frame."""
    return surface.object_type == _FENESTRATION


def _surfaces(doc: IDFDocument, zones: list[str] | None = None) -> list[ResolvedSurface]:
    """Every surface the public extraction resolved, optionally narrowed to some zones.

    THE RENDERER NO LONGER RESOLVES ANYTHING.

    It used to carry its own rule, which agreed with EnergyPlus on five of seventeen example models
    and was wrong by up to 201.98 m on the rest. The rule now lives in one place,
    [get_scene][idfkit.scene.get_scene], proven against the engine's own vertex report, and this is
    the whole of what is left here: a call and a filter.

    The filter is the renderer's and not the extraction's. ``get_scene`` takes one argument and
    returns one scene, because narrowing a list is something every caller can already do, and
    shading belongs to no zone and is kept whatever is asked for.
    """
    scene = get_scene(doc)
    if zones is None:
        return list(scene.surfaces)
    wanted = {zone.upper() for zone in zones}
    return [s for s in scene.surfaces if s.is_shading or s.zone.upper() in wanted]


# ---------------------------------------------------------------------------
# Triangulation and edge helpers
# ---------------------------------------------------------------------------


def _triangulate_polygon(num_vertices: int, offset: int) -> tuple[list[int], list[int], list[int]]:
    """Fan triangulation for convex polygons.

    Returns (i, j, k) lists of vertex indices for Mesh3d.
    """
    i_list: list[int] = []
    j_list: list[int] = []
    k_list: list[int] = []
    for n in range(1, num_vertices - 1):
        i_list.append(offset)
        j_list.append(offset + n)
        k_list.append(offset + n + 1)
    return i_list, j_list, k_list


def _polygon_edges(polygon: Polygon3D) -> tuple[list[float | None], list[float | None], list[float | None]]:
    """Return x, y, z coordinate lists with None breaks for wireframe edges."""
    xs: list[float | None] = []
    ys: list[float | None] = []
    zs: list[float | None] = []
    verts = polygon.vertices
    for idx in range(len(verts)):
        v1 = verts[idx]
        v2 = verts[(idx + 1) % len(verts)]
        xs.extend([v1.x, v2.x, None])
        ys.extend([v1.y, v2.y, None])
        zs.extend([v1.z, v2.z, None])
    return xs, ys, zs


# ---------------------------------------------------------------------------
# Color helpers
# ---------------------------------------------------------------------------


def _get_color(surface: ResolvedSurface, config: ModelViewConfig, zone_colors: dict[str, str]) -> str:
    """Get the color for a surface based on the coloring strategy."""
    if _is_fenestration(surface):
        return _FENESTRATION_COLOR
    if surface.is_shading:
        return _SHADING_COLOR

    if config.color_by == ColorBy.ZONE:
        return zone_colors.get(surface.zone.upper(), _ZONE_PALETTE[0])
    if config.color_by == ColorBy.SURFACE_TYPE:
        return _SURFACE_TYPE_COLORS.get(surface.surface_type.lower(), "#999999")
    if config.color_by == ColorBy.BOUNDARY_CONDITION:
        return _BOUNDARY_COLORS.get(surface.boundary.lower(), "#999999")
    # ColorBy.CONSTRUCTION — reuse zone palette by construction name
    return zone_colors.get(surface.construction.upper(), _ZONE_PALETTE[0])


def _assign_zone_colors(surfaces: list[ResolvedSurface], config: ModelViewConfig) -> dict[str, str]:
    """Build a mapping of zone/construction names to palette colors."""
    if config.color_by == ColorBy.CONSTRUCTION:
        keys = sorted({s.construction.upper() for s in surfaces if not _is_fenestration(s) and not s.is_shading})
    else:
        keys = sorted({s.zone.upper() for s in surfaces if s.zone})
    return {key: _ZONE_PALETTE[i % len(_ZONE_PALETTE)] for i, key in enumerate(keys)}


# ---------------------------------------------------------------------------
# Hover text
# ---------------------------------------------------------------------------


def _build_hover_text(surface: ResolvedSurface) -> str:
    """Build an HTML hover tooltip for a surface."""
    lines = [f"<b>{surface.name}</b>"]
    if surface.zone:
        lines.append(f"Zone: {surface.zone}")
    lines.append(f"Type: {surface.surface_type}")
    lines.append(f"Area: {surface.area:.2f} m\u00b2")
    if surface.construction:
        lines.append(f"Construction: {surface.construction}")
    if surface.boundary:
        lines.append(f"Boundary: {surface.boundary}")
    return "<br>".join(lines)


# ---------------------------------------------------------------------------
# Fenestration offset
# ---------------------------------------------------------------------------


def _offset_fenestration(polygon: Polygon3D, normal: Vector3D) -> Polygon3D:
    """Nudge fenestration slightly along normal so it renders visibly."""
    offset = normal * 0.02
    return polygon.translate(offset)


# ---------------------------------------------------------------------------
# Grouped trace building
# ---------------------------------------------------------------------------


def _build_mesh_traces(
    surfaces: list[ResolvedSurface],
    config: ModelViewConfig,
    zone_colors: dict[str, str],
) -> list[Any]:
    """Build Mesh3d traces grouped by color for performance."""
    go = _get_go()

    # Group surfaces by (color, legend_label)
    groups: dict[tuple[str, str], list[ResolvedSurface]] = {}
    for s in surfaces:
        if _is_fenestration(s) and not config.show_fenestration:
            continue
        color = _get_color(s, config, zone_colors)
        label = _legend_label(s, config)
        key = (color, label)
        groups.setdefault(key, []).append(s)

    traces: list[Any] = []
    for (color, label), group in groups.items():
        all_x: list[float] = []
        all_y: list[float] = []
        all_z: list[float] = []
        all_i: list[int] = []
        all_j: list[int] = []
        all_k: list[int] = []
        all_hover: list[str] = []

        for s in group:
            poly = s.polygon
            if _is_fenestration(s):
                poly = _offset_fenestration(poly, poly.normal)

            offset = len(all_x)
            for v in poly.vertices:
                all_x.append(v.x)
                all_y.append(v.y)
                all_z.append(v.z)

            i_list, j_list, k_list = _triangulate_polygon(poly.num_vertices, offset)
            all_i.extend(i_list)
            all_j.extend(j_list)
            all_k.extend(k_list)

            hover = _build_hover_text(s)
            all_hover.extend([hover] * poly.num_vertices)

        is_fen = _is_fenestration(group[0])
        opacity = config.fenestration_opacity if is_fen else config.opacity

        traces.append(
            go.Mesh3d(
                x=all_x,
                y=all_y,
                z=all_z,
                i=all_i,
                j=all_j,
                k=all_k,
                color=color,
                opacity=opacity,
                name=label,
                text=all_hover,
                hoverinfo="text",
                showlegend=True,
                flatshading=True,
            )
        )

    return traces


def _legend_label(surface: ResolvedSurface, config: ModelViewConfig) -> str:
    """Determine legend label for a surface based on coloring mode."""
    if _is_fenestration(surface):
        return "Fenestration"
    if surface.is_shading:
        return "Shading"
    if config.color_by == ColorBy.ZONE:
        return surface.zone or "Unknown"
    if config.color_by == ColorBy.SURFACE_TYPE:
        return surface.surface_type or "Unknown"
    if config.color_by == ColorBy.BOUNDARY_CONDITION:
        return surface.boundary or "Unknown"
    return surface.construction or "Unknown"


def _build_edge_traces(surfaces: list[ResolvedSurface], config: ModelViewConfig) -> list[Any]:
    """Build Scatter3d wireframe traces."""
    go = _get_go()

    all_x: list[float | None] = []
    all_y: list[float | None] = []
    all_z: list[float | None] = []

    for s in surfaces:
        if _is_fenestration(s) and not config.show_fenestration:
            continue
        poly = s.polygon
        if _is_fenestration(s):
            poly = _offset_fenestration(poly, poly.normal)
        ex, ey, ez = _polygon_edges(poly)
        all_x.extend(ex)
        all_y.extend(ey)
        all_z.extend(ez)

    return [
        go.Scatter3d(
            x=all_x,
            y=all_y,
            z=all_z,
            mode="lines",
            line={"color": config.edge_color, "width": config.edge_width},
            hoverinfo="skip",
            showlegend=False,
        )
    ]


def _build_label_traces(surfaces: list[ResolvedSurface]) -> list[Any]:
    """Build Scatter3d traces for zone labels at zone centroids."""
    go = _get_go()

    # Compute zone centroids
    zone_points: dict[str, list[Vector3D]] = {}
    for s in surfaces:
        if not s.zone or _is_fenestration(s) or s.is_shading:
            continue
        zone_points.setdefault(s.zone, []).append(s.polygon.centroid)

    if not zone_points:
        return []

    xs: list[float] = []
    ys: list[float] = []
    zs: list[float] = []
    texts: list[str] = []

    for zone_name, centroids in zone_points.items():
        cx = sum(c.x for c in centroids) / len(centroids)
        cy = sum(c.y for c in centroids) / len(centroids)
        cz = sum(c.z for c in centroids) / len(centroids)
        xs.append(cx)
        ys.append(cy)
        zs.append(cz)
        texts.append(zone_name)

    return [
        go.Scatter3d(
            x=xs,
            y=ys,
            z=zs,
            mode="text",
            text=texts,
            textfont={"size": 12, "color": "black"},
            hoverinfo="skip",
            showlegend=False,
        )
    ]


# ---------------------------------------------------------------------------
# Layout helpers
# ---------------------------------------------------------------------------


def _make_3d_layout(go: Any, config: ModelViewConfig, title: str | None) -> Any:
    """Create a standard 3D layout with equal aspect ratio."""
    return go.Layout(
        title=title,
        width=config.width,
        height=config.height,
        scene={
            "aspectmode": "data",
            "xaxis": {"title": "X (m)", "backgroundcolor": config.background_color},
            "yaxis": {"title": "Y (m)", "backgroundcolor": config.background_color},
            "zaxis": {"title": "Z (m)", "backgroundcolor": config.background_color},
        },
        paper_bgcolor=config.background_color,
        showlegend=True,
    )


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


def view_model(
    doc: IDFDocument,
    *,
    config: ModelViewConfig | None = None,
    title: str | None = "3D Building Model",
    zones: list[str] | None = None,
) -> Any:
    """Interactive 3D building viewer with orbit/pan/zoom.

    Args:
        doc: An IDFDocument with building geometry.
        config: Optional view configuration.
        title: Optional plot title.
        zones: Optional list of zone names to include (all if None).

    Returns:
        A plotly Figure.

    Raises:
        ImportError: If plotly is not installed.
    """
    go = _get_go()
    cfg = config or ModelViewConfig()
    surfaces = _surfaces(doc, zones)
    zone_colors = _assign_zone_colors(surfaces, cfg)

    traces: list[Any] = _build_mesh_traces(surfaces, cfg, zone_colors)
    if cfg.show_edges:
        traces.extend(_build_edge_traces(surfaces, cfg))
    if cfg.show_labels:
        traces.extend(_build_label_traces(surfaces))

    layout = _make_3d_layout(go, cfg, title)
    return go.Figure(data=traces, layout=layout)


def view_floor_plan(
    doc: IDFDocument,
    *,
    config: ModelViewConfig | None = None,
    title: str | None = "Floor Plan",
    z_cut: float | None = None,
    zones: list[str] | None = None,
) -> Any:
    """2D top-down floor plan projection.

    Projects floor polygons onto the XY plane. If ``z_cut`` is given,
    wall polygons intersecting that height are also shown.

    Args:
        doc: An IDFDocument with building geometry.
        config: Optional view configuration.
        title: Optional plot title.
        z_cut: Optional Z height for wall slicing.
        zones: Optional list of zone names to include.

    Returns:
        A plotly Figure.

    Raises:
        ImportError: If plotly is not installed.
    """
    go = _get_go()
    cfg = config or ModelViewConfig()
    surfaces = _surfaces(doc, zones)
    zone_colors = _assign_zone_colors(surfaces, cfg)

    fig = go.Figure()
    seen_labels: set[str] = set()

    for s in surfaces:
        if _is_fenestration(s) or s.is_shading:
            continue

        stype = s.surface_type.lower()
        show = False

        if stype == "floor":
            show = True
        elif z_cut is not None and stype == "wall":
            zs = [v.z for v in s.polygon.vertices]
            if min(zs) <= z_cut <= max(zs):
                show = True

        if not show:
            continue

        color = _get_color(s, cfg, zone_colors)
        label = _legend_label(s, cfg)
        show_legend = label not in seen_labels
        seen_labels.add(label)

        xs = [v.x for v in s.polygon.vertices] + [s.polygon.vertices[0].x]
        ys = [v.y for v in s.polygon.vertices] + [s.polygon.vertices[0].y]

        fig.add_trace(
            go.Scatter(
                x=xs,
                y=ys,
                fill="toself",
                fillcolor=color,
                opacity=cfg.opacity,
                line={"color": cfg.edge_color, "width": cfg.edge_width},
                name=label,
                text=_build_hover_text(s),
                hoverinfo="text",
                showlegend=show_legend,
            )
        )

    fig.update_layout(
        title=title,
        width=cfg.width,
        height=cfg.height,
        xaxis={"title": "X (m)", "scaleanchor": "y", "scaleratio": 1},
        yaxis={"title": "Y (m)"},
        paper_bgcolor=cfg.background_color,
        plot_bgcolor=cfg.background_color,
        showlegend=True,
    )
    return fig


def _compute_zone_offsets(
    surfaces: list[ResolvedSurface],
    separation: float,
) -> dict[str, Vector3D]:
    """Compute per-zone translation offsets for exploded views."""
    # Building centroid from all non-shading surfaces
    all_centroids = [s.polygon.centroid for s in surfaces if not s.is_shading and s.zone]
    if all_centroids:
        bx = sum(c.x for c in all_centroids) / len(all_centroids)
        by = sum(c.y for c in all_centroids) / len(all_centroids)
        bz = sum(c.z for c in all_centroids) / len(all_centroids)
        building_centroid = Vector3D(bx, by, bz)
    else:
        building_centroid = Vector3D.origin()

    # Per-zone centroid
    zone_counts: dict[str, int] = {}
    zone_sums: dict[str, Vector3D] = {}
    for s in surfaces:
        if not s.zone or s.is_shading:
            continue
        key = s.zone.upper()
        c = s.polygon.centroid
        if key not in zone_sums:
            zone_sums[key] = Vector3D(0, 0, 0)
            zone_counts[key] = 0
        zone_sums[key] = zone_sums[key] + c
        zone_counts[key] = zone_counts[key] + 1

    zone_offsets: dict[str, Vector3D] = {}
    for key in zone_sums:
        zone_centroid = zone_sums[key] / zone_counts[key]
        direction = zone_centroid - building_centroid
        length = direction.length()
        if length > 1e-6:
            zone_offsets[key] = direction.normalize() * separation
        else:
            zone_offsets[key] = Vector3D(separation, 0, 0)

    return zone_offsets


def _apply_zone_offsets(
    surfaces: list[ResolvedSurface],
    zone_offsets: dict[str, Vector3D],
) -> list[ResolvedSurface]:
    """Apply per-zone translation offsets to surfaces."""
    exploded: list[ResolvedSurface] = []
    for s in surfaces:
        if not s.zone:
            exploded.append(s)
            continue
        offset = zone_offsets.get(s.zone.upper(), Vector3D.origin())
        exploded.append(replace(s, polygon=s.polygon.translate(offset)))
    return exploded


def view_exploded(
    doc: IDFDocument,
    *,
    config: ModelViewConfig | None = None,
    title: str | None = "Exploded View",
    separation: float = 5.0,
    zones: list[str] | None = None,
) -> Any:
    """Zones pulled apart to reveal internal partitions.

    Each zone's surfaces are translated outward from the building centroid
    by ``separation`` meters.

    Args:
        doc: An IDFDocument with building geometry.
        config: Optional view configuration.
        title: Optional plot title.
        separation: Distance in meters to pull zones apart.
        zones: Optional list of zone names to include.

    Returns:
        A plotly Figure.

    Raises:
        ImportError: If plotly is not installed.
    """
    go = _get_go()
    cfg = config or ModelViewConfig()
    surfaces = _surfaces(doc, zones)
    zone_colors = _assign_zone_colors(surfaces, cfg)

    zone_offsets = _compute_zone_offsets(surfaces, separation)
    exploded = _apply_zone_offsets(surfaces, zone_offsets)

    traces: list[Any] = _build_mesh_traces(exploded, cfg, zone_colors)
    if cfg.show_edges:
        traces.extend(_build_edge_traces(exploded, cfg))
    if cfg.show_labels:
        traces.extend(_build_label_traces(exploded))

    layout = _make_3d_layout(go, cfg, title)
    return go.Figure(data=traces, layout=layout)


def view_normals(
    doc: IDFDocument,
    *,
    config: ModelViewConfig | None = None,
    title: str | None = "Surface Normals",
    arrow_length: float = 1.0,
    zones: list[str] | None = None,
) -> Any:
    """Surface normal arrows for orientation QA.

    Renders the model at reduced opacity with cone traces at surface
    centroids pointing in the normal direction.

    Args:
        doc: An IDFDocument with building geometry.
        config: Optional view configuration.
        title: Optional plot title.
        arrow_length: Length of normal arrows in meters.
        zones: Optional list of zone names to include.

    Returns:
        A plotly Figure.

    Raises:
        ImportError: If plotly is not installed.
    """
    go = _get_go()
    cfg = config or ModelViewConfig()

    # Render model at reduced opacity
    reduced_cfg = ModelViewConfig(
        width=cfg.width,
        height=cfg.height,
        color_by=cfg.color_by,
        show_fenestration=cfg.show_fenestration,
        show_edges=cfg.show_edges,
        show_labels=False,
        opacity=cfg.opacity * 0.4,
        fenestration_opacity=cfg.fenestration_opacity * 0.4,
        background_color=cfg.background_color,
        edge_color=cfg.edge_color,
        edge_width=cfg.edge_width,
    )

    surfaces = _surfaces(doc, zones)
    zone_colors = _assign_zone_colors(surfaces, reduced_cfg)

    traces: list[Any] = _build_mesh_traces(surfaces, reduced_cfg, zone_colors)
    if reduced_cfg.show_edges:
        traces.extend(_build_edge_traces(surfaces, reduced_cfg))

    # Build cone traces for normals
    cone_x: list[float] = []
    cone_y: list[float] = []
    cone_z: list[float] = []
    cone_u: list[float] = []
    cone_v: list[float] = []
    cone_w: list[float] = []
    cone_hover: list[str] = []

    for s in surfaces:
        if _is_fenestration(s) or s.is_shading:
            continue
        centroid = s.polygon.centroid
        normal = s.polygon.normal
        cone_x.append(centroid.x)
        cone_y.append(centroid.y)
        cone_z.append(centroid.z)
        cone_u.append(normal.x * arrow_length)
        cone_v.append(normal.y * arrow_length)
        cone_w.append(normal.z * arrow_length)
        cone_hover.append(_build_hover_text(s))

    if cone_x:
        traces.append(
            go.Cone(
                x=cone_x,
                y=cone_y,
                z=cone_z,
                u=cone_u,
                v=cone_v,
                w=cone_w,
                sizemode="absolute",
                sizeref=arrow_length,
                anchor="tail",
                colorscale=[[0, "#e15759"], [1, "#e15759"]],
                showscale=False,
                text=cone_hover,
                hoverinfo="text",
                name="Normals",
            )
        )

    layout = _make_3d_layout(go, cfg, title)
    return go.Figure(data=traces, layout=layout)
