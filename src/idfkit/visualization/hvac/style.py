"""Shared styling for HVAC diagram renderers.

A single category -> color/shape table keeps the Mermaid and DOT renderers in
visual agreement. Colors are deliberately muted, professional tones matching the
construction-SVG palette in :mod:`idfkit.visualization.svg`.
"""

from __future__ import annotations

from dataclasses import dataclass

from .model import Category


@dataclass(frozen=True)
class CategoryStyle:
    """Visual style for a component category.

    Attributes:
        fill: Background fill color (hex).
        stroke: Border color (hex).
        mermaid_shape: Mermaid node-shape delimiters as a ``(open, close)`` pair,
            e.g. ``("[", "]")`` for a rectangle or ``("{{", "}}")`` for a hexagon.
        dot_shape: Graphviz node shape name.
    """

    fill: str
    stroke: str
    mermaid_shape: tuple[str, str]
    dot_shape: str


# Rectangle is the default body shape; junctions are hexagons to read as splits.
_RECT = ("[", "]")
_ROUND = ("(", ")")
_HEX = ("{{", "}}")
_STADIUM = ("([", "])")

CATEGORY_STYLES: dict[Category, CategoryStyle] = {
    "coil": CategoryStyle("#b8d4e8", "#5a7a8c", _RECT, "box"),
    "fan": CategoryStyle("#f5e6a3", "#b0a05a", _RECT, "box"),
    "pump": CategoryStyle("#d4a574", "#9c7848", _ROUND, "ellipse"),
    "plant_equipment": CategoryStyle("#c9785d", "#8c4f3c", _RECT, "box3d"),
    "junction": CategoryStyle("#d8d0e8", "#8c7fb0", _HEX, "diamond"),
    "terminal": CategoryStyle("#a8d5ba", "#5f8c70", _RECT, "box"),
    "outdoor_air": CategoryStyle("#e6f2f8", "#7fa8bc", _STADIUM, "box"),
    "pipe": CategoryStyle("#d3d3d3", "#909090", _ROUND, "ellipse"),
    "other": CategoryStyle("#e8e4dc", "#9c968c", _RECT, "box"),
}

#: Fallback when a category somehow has no entry.
DEFAULT_STYLE = CATEGORY_STYLES["other"]

#: Conditioned zones are drawn with a distinct warm tone (zones are not vertices,
#: so they get a fixed style rather than a :data:`Category` entry).
ZONE_FILL = "#f7e7c3"
ZONE_STROKE = "#b08a3c"

#: Readable dark text on the light category fills.
TEXT_COLOR = "#1a1a1a"


def style_for(category: Category) -> CategoryStyle:
    """Return the :class:`CategoryStyle` for *category*."""
    return CATEGORY_STYLES.get(category, DEFAULT_STYLE)
