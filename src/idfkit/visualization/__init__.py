"""
Visualization utilities for EnergyPlus models.

This module provides SVG diagram generation for construction assemblies,
showing layer sequence, thicknesses, and thermal properties.

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

from .svg import SVGConfig, construction_to_svg, generate_construction_svg

__all__ = [
    "SVGConfig",
    "construction_to_svg",
    "generate_construction_svg",
]
