"""
Visualization utilities for EnergyPlus models.

This module provides SVG diagram generation for construction assemblies,
showing layer sequence, thicknesses, and thermal properties, as well as
interactive 3D building model visualization using plotly.

Example:
    >>> from idfkit import load_idf
    >>> from idfkit.visualization import construction_to_svg
    >>>
    >>> model = load_idf("building.idf")
    >>> wall = model["Construction"]["ExteriorWall"]
    >>>
    >>> svg = construction_to_svg(wall)
    >>> with open("wall_section.svg", "w") as f:
    ...     f.write(svg)

In Jupyter notebooks, constructions display automatically as SVG:
    >>> wall  # Displays graphical cross-section
"""

from __future__ import annotations

from .hvac import (
    HVACDiagramConfig,
    HVACEdge,
    HVACGraph,
    HVACLoop,
    HVACNode,
    HVACVertex,
    HVACWarning,
    HVACZone,
    LoopMembership,
    build_hvac_graph,
    hvac_to_dot,
    hvac_to_mermaid,
)
from .model import ColorBy, ModelViewConfig, view_exploded, view_floor_plan, view_model, view_normals
from .svg import SVGConfig, construction_to_svg, generate_construction_svg

__all__ = [
    "ColorBy",
    "HVACDiagramConfig",
    "HVACEdge",
    "HVACGraph",
    "HVACLoop",
    "HVACNode",
    "HVACVertex",
    "HVACWarning",
    "HVACZone",
    "LoopMembership",
    "ModelViewConfig",
    "SVGConfig",
    "build_hvac_graph",
    "construction_to_svg",
    "generate_construction_svg",
    "hvac_to_dot",
    "hvac_to_mermaid",
    "view_exploded",
    "view_floor_plan",
    "view_model",
    "view_normals",
]
