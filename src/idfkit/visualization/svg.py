"""
SVG generation utilities for construction visualization.

Generates architectural cross-section diagrams for opaque and glazing constructions,
using industry-standard hatching patterns and conventions.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING
from xml.sax.saxutils import escape

if TYPE_CHECKING:
    from ..thermal.properties import ConstructionThermalProperties, LayerThermalProperties


@dataclass(frozen=True)
class SVGConfig:
    """Configuration for SVG construction diagrams.

    Attributes:
        width: Total SVG width in pixels
        height: Total SVG height in pixels
        padding: Padding around the diagram
        header_height: Height of the header section
        footer_height: Height of the footer/labels section
        min_layer_width: Minimum width for thin layers
        font_family: Font family for text
        font_size: Base font size in pixels
        font_size_small: Small font size for labels
    """

    width: int = 600
    height: int = 200
    padding: int = 20
    header_height: int = 40
    footer_height: int = 50
    min_layer_width: int = 30
    font_family: str = "system-ui, -apple-system, sans-serif"
    font_size: int = 12
    font_size_small: int = 10


# Architectural color palette - more muted, professional tones
MATERIAL_COLORS: dict[str, str] = {
    "default": "#c4a77d",  # Warm tan
    "concrete": "#a8a8a8",  # Medium gray
    "brick": "#c9785d",  # Terracotta
    "insulation": "#f5e6a3",  # Pale yellow
    "wood": "#d4a574",  # Light wood
    "gypsum": "#e8e4dc",  # Off-white
    "plaster": "#f0ebe0",  # Cream
    "metal": "#b8bcc0",  # Steel gray
}

# Colors for special layer types
NOMASS_COLOR = "#d8d0e8"  # Soft lavender
AIRGAP_COLOR = "#e6f2f8"  # Very light blue

# Glazing colors
GLAZING_COLORS: dict[str, str] = {
    "WindowMaterial:Glazing": "#b8d4e8",  # Light blue-gray glass
    "WindowMaterial:Gas": "#f0f6fa",  # Nearly white for gas
    "WindowMaterial:SimpleGlazingSystem": "#b8d4e8",
}

# Pattern IDs for architectural hatching
PATTERN_IDS: dict[str, str] = {
    "concrete": "hatch-concrete",
    "brick": "hatch-brick",
    "insulation": "hatch-insulation",
    "wood": "hatch-wood",
    "gypsum": "hatch-gypsum",
    "metal": "hatch-metal",
    "glass": "hatch-glass",
    "air-gap": "hatch-air-gap",
    "nomass": "hatch-nomass",
    "gas-fill": "hatch-gas-fill",
}


def _guess_material_subtype(name: str) -> str:
    """Guess material subtype from name for pattern and color selection."""
    name_lower = name.lower()

    if any(x in name_lower for x in ["concrete", "cmu", "block", "heavyweight"]):
        return "concrete"
    if any(x in name_lower for x in ["brick", "masonry"]):
        return "brick"
    if any(x in name_lower for x in ["insul", "foam", "xps", "eps", "polyiso", "mineral wool", "fiberglass", "batt"]):
        return "insulation"
    if any(x in name_lower for x in ["wood", "timber", "plywood", "osb", "lumber"]):
        return "wood"
    if any(x in name_lower for x in ["gypsum", "drywall", "gyp", "sheetrock", "plasterboard"]):
        return "gypsum"
    if any(x in name_lower for x in ["plaster", "stucco", "render"]):
        return "plaster"
    if any(x in name_lower for x in ["metal", "steel", "aluminum", "aluminium", "copper"]):
        return "metal"

    return "default"


def _get_layer_fill(layer: LayerThermalProperties) -> tuple[str, str | None]:
    """Get fill color and pattern ID for a layer.

    Returns:
        Tuple of (base_color, pattern_id or None)
    """
    # Glazing layers
    if layer.is_glazing:
        color = GLAZING_COLORS.get(layer.obj_type, GLAZING_COLORS["WindowMaterial:Glazing"])
        if layer.obj_type == "WindowMaterial:Glazing":
            return color, PATTERN_IDS["glass"]
        return color, None

    # Gas/air gap layers
    if layer.is_gas:
        if layer.obj_type == "WindowMaterial:Gas":
            return GLAZING_COLORS["WindowMaterial:Gas"], PATTERN_IDS["gas-fill"]
        return AIRGAP_COLOR, PATTERN_IDS["air-gap"]

    # No-mass resistive layers
    if layer.obj_type == "Material:NoMass":
        return NOMASS_COLOR, PATTERN_IDS["nomass"]

    # Standard material layers
    if layer.obj_type == "Material":
        subtype = _guess_material_subtype(layer.name)
        color = MATERIAL_COLORS.get(subtype, MATERIAL_COLORS["default"])
        pattern = PATTERN_IDS.get(subtype)
        return color, pattern

    return "#d3d3d3", None


def _format_thickness_mm(thickness: float | None) -> str:
    """Format thickness in millimeters for display."""
    if thickness is None:
        return ""
    mm = thickness * 1000
    if mm < 10:
        return f"{mm:.1f}"
    return f"{mm:.0f}"


def _format_r_value(r_value: float) -> str:
    """Format R-value for display."""
    if r_value < 0.1:
        return f"R{r_value:.3f}"
    return f"R{r_value:.2f}"


def _truncate_name(name: str, max_len: int = 15) -> str:
    """Truncate name for display."""
    if len(name) <= max_len:
        return name
    return name[: max_len - 2] + ".."


def generate_construction_svg(
    props: ConstructionThermalProperties,
    config: SVGConfig | None = None,
) -> str:
    """Generate SVG diagram for a construction assembly.

    Creates an architectural cross-section with proper hatching patterns,
    dimension lines, and thermal property annotations.

    Args:
        props: ConstructionThermalProperties from get_thermal_properties()
        config: Optional SVGConfig for customization

    Returns:
        SVG string
    """
    if config is None:
        config = SVGConfig()

    layers = props.layers
    if not layers:
        return _generate_empty_svg(props.name, config)

    # Calculate layer widths proportional to thickness
    total_thickness = sum(layer.thickness or 0.01 for layer in layers)
    available_width = config.width - 2 * config.padding - 40  # Extra space for labels

    # Ensure minimum widths
    layer_widths: list[float] = []
    for layer in layers:
        thickness = layer.thickness or 0.01
        width = (thickness / total_thickness) * available_width
        layer_widths.append(max(width, config.min_layer_width))

    # Scale if needed
    total_width = sum(layer_widths)
    if total_width > available_width:
        scale = available_width / total_width
        layer_widths = [w * scale for w in layer_widths]

    actual_width = sum(layer_widths)

    # Generate SVG
    svg_parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" '
        f'width="{config.width}" height="{config.height}" '
        f'viewBox="0 0 {config.width} {config.height}">',
        _generate_defs(layers),
        _generate_styles(config),
    ]

    # Background
    svg_parts.append(f'<rect width="{config.width}" height="{config.height}" fill="#ffffff" />')

    # Header with title and thermal properties
    svg_parts.append(_generate_header(props, config))

    # Layer diagram positioning
    diagram_y = config.header_height + 5
    diagram_height = config.height - config.header_height - config.footer_height - 10
    diagram_x = config.padding + 20  # Space for OUT label

    # Draw layers
    x = diagram_x
    for i, (layer, width) in enumerate(zip(layers, layer_widths, strict=False)):
        svg_parts.append(_generate_layer(layer, x, diagram_y, width, diagram_height, i))
        x += width

    # Section cut indicators (diagonal lines at top and bottom corners)
    svg_parts.append(_generate_section_cuts(diagram_x, diagram_y, actual_width, diagram_height))

    # Outside/Inside labels with arrows
    svg_parts.append(_generate_side_labels(config, diagram_x, diagram_y, actual_width, diagram_height))

    # Dimension line at bottom
    svg_parts.append(_generate_dimension_line(layers, layer_widths, diagram_x, diagram_y + diagram_height, config))

    # Footer with material names
    svg_parts.append(_generate_footer(layers, layer_widths, config, diagram_x, diagram_y + diagram_height + 25))

    svg_parts.append("</svg>")

    return "\n".join(svg_parts)


def _generate_empty_svg(name: str, config: SVGConfig) -> str:
    """Generate SVG for construction with no layers."""
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{config.width}" height="60">
  <rect width="{config.width}" height="60" fill="#ffffff" />
  <text x="{config.width // 2}" y="35" text-anchor="middle"
        font-family="{config.font_family}" font-size="{config.font_size}" fill="#666">
    {escape(name)}: No layers defined
  </text>
</svg>"""


def _get_pattern_svg(pattern_id: str) -> str:
    """Get SVG pattern definition for a given pattern ID."""
    pattern_defs = {
        PATTERN_IDS["concrete"]: f"""
    <pattern id="{PATTERN_IDS["concrete"]}" patternUnits="userSpaceOnUse" width="12" height="12">
      <rect width="12" height="12" fill="{MATERIAL_COLORS["concrete"]}"/>
      <line x1="0" y1="12" x2="12" y2="0" stroke="#888" stroke-width="0.5"/>
      <circle cx="3" cy="3" r="0.8" fill="#999"/>
      <circle cx="9" cy="9" r="0.6" fill="#888"/>
      <circle cx="6" cy="7" r="0.5" fill="#999"/>
    </pattern>""",
        PATTERN_IDS["brick"]: f"""
    <pattern id="{PATTERN_IDS["brick"]}" patternUnits="userSpaceOnUse" width="8" height="8">
      <rect width="8" height="8" fill="{MATERIAL_COLORS["brick"]}"/>
      <line x1="0" y1="8" x2="8" y2="0" stroke="#a05040" stroke-width="0.6"/>
      <line x1="-2" y1="6" x2="6" y2="-2" stroke="#a05040" stroke-width="0.6"/>
    </pattern>""",
        PATTERN_IDS["insulation"]: f"""
    <pattern id="{PATTERN_IDS["insulation"]}" patternUnits="userSpaceOnUse" width="16" height="8">
      <rect width="16" height="8" fill="{MATERIAL_COLORS["insulation"]}"/>
      <path d="M0,4 L4,1 L8,4 L12,1 L16,4" stroke="#c4a000" stroke-width="0.8" fill="none"/>
      <path d="M0,7 L4,4 L8,7 L12,4 L16,7" stroke="#c4a000" stroke-width="0.8" fill="none"/>
    </pattern>""",
        PATTERN_IDS["wood"]: f"""
    <pattern id="{PATTERN_IDS["wood"]}" patternUnits="userSpaceOnUse" width="16" height="8">
      <rect width="16" height="8" fill="{MATERIAL_COLORS["wood"]}"/>
      <path d="M0,2 Q4,1 8,2 T16,2" stroke="#a07850" stroke-width="0.5" fill="none"/>
      <path d="M0,5 Q4,4 8,5 T16,5" stroke="#a07850" stroke-width="0.5" fill="none"/>
      <path d="M0,7 Q4,8 8,7 T16,7" stroke="#a07850" stroke-width="0.4" fill="none"/>
    </pattern>""",
        PATTERN_IDS["gypsum"]: f"""
    <pattern id="{PATTERN_IDS["gypsum"]}" patternUnits="userSpaceOnUse" width="6" height="6">
      <rect width="6" height="6" fill="{MATERIAL_COLORS["gypsum"]}"/>
      <circle cx="1" cy="1" r="0.3" fill="#ccc"/>
      <circle cx="4" cy="3" r="0.3" fill="#ccc"/>
      <circle cx="2" cy="5" r="0.3" fill="#ccc"/>
    </pattern>""",
        PATTERN_IDS["metal"]: f"""
    <pattern id="{PATTERN_IDS["metal"]}" patternUnits="userSpaceOnUse" width="4" height="4">
      <rect width="4" height="4" fill="{MATERIAL_COLORS["metal"]}"/>
      <line x1="0" y1="4" x2="4" y2="0" stroke="#909498" stroke-width="0.6"/>
    </pattern>""",
        PATTERN_IDS["glass"]: f"""
    <pattern id="{PATTERN_IDS["glass"]}" patternUnits="userSpaceOnUse" width="6" height="200">
      <rect width="6" height="200" fill="{GLAZING_COLORS["WindowMaterial:Glazing"]}"/>
      <line x1="1.5" y1="0" x2="1.5" y2="200" stroke="#8ab4d0" stroke-width="0.5" opacity="0.4"/>
    </pattern>""",
        PATTERN_IDS["air-gap"]: f"""
    <pattern id="{PATTERN_IDS["air-gap"]}" patternUnits="userSpaceOnUse" width="12" height="12">
      <rect width="12" height="12" fill="{AIRGAP_COLOR}"/>
      <line x1="0" y1="12" x2="12" y2="0" stroke="#b0c8d8" stroke-width="0.4"/>
    </pattern>""",
        PATTERN_IDS["nomass"]: f"""
    <pattern id="{PATTERN_IDS["nomass"]}" patternUnits="userSpaceOnUse" width="8" height="8">
      <rect width="8" height="8" fill="{NOMASS_COLOR}"/>
      <circle cx="4" cy="4" r="1" fill="#a090c0"/>
    </pattern>""",
        PATTERN_IDS["gas-fill"]: f"""
    <pattern id="{PATTERN_IDS["gas-fill"]}" patternUnits="userSpaceOnUse" width="16" height="16">
      <rect width="16" height="16" fill="{GLAZING_COLORS["WindowMaterial:Gas"]}"/>
      <line x1="0" y1="16" x2="16" y2="0" stroke="#d0e0f0" stroke-width="0.3"/>
    </pattern>""",
    }
    return pattern_defs.get(pattern_id, "")


def _generate_defs(layers: list[LayerThermalProperties]) -> str:
    """Generate SVG defs section with architectural hatching patterns."""
    # Determine which patterns we need
    needed_patterns: set[str] = set()
    for layer in layers:
        _, pattern_id = _get_layer_fill(layer)
        if pattern_id:
            needed_patterns.add(pattern_id)

    parts = ["<defs>"]

    # Add only needed patterns
    for pattern_id in needed_patterns:
        pattern_svg = _get_pattern_svg(pattern_id)
        if pattern_svg:
            parts.append(pattern_svg)

    # Arrow markers for dimension lines (always included)
    parts.append("""
    <marker id="arrow" markerWidth="6" markerHeight="6" refX="5" refY="3" orient="auto">
      <path d="M0,0 L0,6 L6,3 z" fill="#666"/>
    </marker>
    <marker id="arrow-rev" markerWidth="6" markerHeight="6" refX="1" refY="3" orient="auto">
      <path d="M6,0 L6,6 L0,3 z" fill="#666"/>
    </marker>""")

    parts.append("</defs>")
    return "\n".join(parts)


def _generate_styles(config: SVGConfig) -> str:
    """Generate SVG styles."""
    return f"""<style>
    .title {{ font-family: {config.font_family}; font-size: {config.font_size + 2}px; font-weight: 600; fill: #333; }}
    .thermal-props {{ font-family: {config.font_family}; font-size: {config.font_size}px; fill: #555; }}
    .layer-label {{ font-family: {config.font_family}; font-size: {config.font_size_small}px; fill: #333; }}
    .dim-text {{ font-family: {config.font_family}; font-size: {config.font_size_small - 1}px; fill: #666; }}
    .side-label {{ font-family: {config.font_family}; font-size: {config.font_size_small}px; fill: #555; font-weight: 500; }}
    .layer-rect {{ stroke: #444; stroke-width: 1; }}
    .section-cut {{ stroke: #333; stroke-width: 1.5; }}
    .dim-line {{ stroke: #888; stroke-width: 0.5; }}
    .low-e-coating {{ fill: none; stroke: #e65100; stroke-width: 2.5; stroke-linecap: round; }}
  </style>"""


def _generate_header(props: ConstructionThermalProperties, config: SVGConfig) -> str:
    """Generate header section with title and thermal properties."""
    parts = ['<g class="header">']

    # Title on left
    parts.append(f'<text x="{config.padding}" y="24" class="title">{escape(props.name)}</text>')

    # Thermal properties on right, formatted nicely
    if props.is_glazing:
        props_text = f"U = {props.u_value:.2f} W/m²·K"
        if props.shgc is not None:
            props_text += f"   SHGC = {props.shgc:.2f}"
    else:
        props_text = f"U = {props.u_value:.2f} W/m²·K   R = {props.r_value_with_films:.2f} m²·K/W"

    parts.append(
        f'<text x="{config.width - config.padding}" y="24" text-anchor="end" class="thermal-props">{props_text}</text>'
    )

    parts.append("</g>")
    return "\n".join(parts)


def _generate_layer(
    layer: LayerThermalProperties,
    x: float,
    y: float,
    width: float,
    height: float,
    index: int,
) -> str:
    """Generate SVG elements for a single layer."""
    color, pattern_id = _get_layer_fill(layer)
    fill = f"url(#{pattern_id})" if pattern_id else color

    parts = [f'<g class="layer" data-index="{index}" data-name="{escape(layer.name)}">']

    # Main layer rectangle
    parts.append(
        f'<rect x="{x:.1f}" y="{y:.1f}" width="{width:.1f}" height="{height:.1f}" fill="{fill}" class="layer-rect" />'
    )

    # Low-E coating indicator - orange line along the coated surface
    if layer.is_glazing:
        # Back side low-E (facing interior)
        if layer.emissivity_back is not None and layer.emissivity_back < 0.2:
            parts.append(
                f'<line x1="{x + width - 1.5:.1f}" y1="{y + 4:.1f}" '
                f'x2="{x + width - 1.5:.1f}" y2="{y + height - 4:.1f}" '
                f'class="low-e-coating" />'
            )

        # Front side low-E (facing exterior)
        if layer.emissivity_front is not None and layer.emissivity_front < 0.2:
            parts.append(
                f'<line x1="{x + 1.5:.1f}" y1="{y + 4:.1f}" '
                f'x2="{x + 1.5:.1f}" y2="{y + height - 4:.1f}" '
                f'class="low-e-coating" />'
            )

    parts.append("</g>")
    return "\n".join(parts)


def _generate_section_cuts(x: float, y: float, width: float, height: float) -> str:
    """Generate section cut indicators at corners (45° lines)."""
    cut_size = 6
    parts = ['<g class="section-cuts">']

    # Top-left
    parts.append(
        f'<line x1="{x - cut_size:.1f}" y1="{y - cut_size:.1f}" '
        f'x2="{x + cut_size:.1f}" y2="{y + cut_size:.1f}" class="section-cut" />'
    )
    # Top-right
    parts.append(
        f'<line x1="{x + width - cut_size:.1f}" y1="{y + cut_size:.1f}" '
        f'x2="{x + width + cut_size:.1f}" y2="{y - cut_size:.1f}" class="section-cut" />'
    )
    # Bottom-left
    parts.append(
        f'<line x1="{x - cut_size:.1f}" y1="{y + height + cut_size:.1f}" '
        f'x2="{x + cut_size:.1f}" y2="{y + height - cut_size:.1f}" class="section-cut" />'
    )
    # Bottom-right
    parts.append(
        f'<line x1="{x + width - cut_size:.1f}" y1="{y + height - cut_size:.1f}" '
        f'x2="{x + width + cut_size:.1f}" y2="{y + height + cut_size:.1f}" class="section-cut" />'
    )

    parts.append("</g>")
    return "\n".join(parts)


def _generate_side_labels(
    config: SVGConfig,
    diagram_x: float,
    diagram_y: float,
    diagram_width: float,
    diagram_height: float,
) -> str:
    """Generate Outside/Inside labels with small arrows."""
    mid_y = diagram_y + diagram_height / 2

    # Position labels outside the diagram
    out_x = diagram_x - 8
    in_x = diagram_x + diagram_width + 8

    return f"""<g class="side-labels">
    <text x="{out_x:.1f}" y="{mid_y:.1f}" text-anchor="end" dominant-baseline="middle" class="side-label">EXT</text>
    <text x="{in_x:.1f}" y="{mid_y:.1f}" text-anchor="start" dominant-baseline="middle" class="side-label">INT</text>
  </g>"""


def _generate_dimension_line(
    layers: list[LayerThermalProperties],
    widths: list[float],
    start_x: float,
    y: float,
    config: SVGConfig,
) -> str:
    """Generate dimension line with tick marks and thickness labels."""
    parts = ['<g class="dimensions">']

    y_line = y + 8  # Below the diagram
    tick_height = 4

    x = start_x
    for layer, width in zip(layers, widths, strict=False):
        # Tick marks at layer boundaries
        parts.append(
            f'<line x1="{x:.1f}" y1="{y_line - tick_height:.1f}" '
            f'x2="{x:.1f}" y2="{y_line + tick_height:.1f}" class="dim-line" />'
        )

        # Dimension text (thickness in mm)
        center_x = x + width / 2
        if layer.thickness:
            dim_text = _format_thickness_mm(layer.thickness)
            if width >= 25:  # Only show if there's enough space
                parts.append(
                    f'<text x="{center_x:.1f}" y="{y_line + 12:.1f}" '
                    f'text-anchor="middle" class="dim-text">{dim_text}</text>'
                )

        x += width

    # Final tick mark
    parts.append(
        f'<line x1="{x:.1f}" y1="{y_line - tick_height:.1f}" '
        f'x2="{x:.1f}" y2="{y_line + tick_height:.1f}" class="dim-line" />'
    )

    # Horizontal dimension line
    parts.append(f'<line x1="{start_x:.1f}" y1="{y_line:.1f}" x2="{x:.1f}" y2="{y_line:.1f}" class="dim-line" />')

    parts.append("</g>")
    return "\n".join(parts)


def _generate_footer(
    layers: list[LayerThermalProperties],
    widths: list[float],
    config: SVGConfig,
    start_x: float,
    y: float,
) -> str:
    """Generate footer with material names."""
    parts = ['<g class="footer">']

    x = start_x
    for layer, width in zip(layers, widths, strict=False):
        center_x = x + width / 2

        # Material name - truncate based on available width
        max_chars = max(3, int(width / 6))
        name = _truncate_name(layer.name, max_len=max_chars)

        # Only show name if there's reasonable space
        if width >= 20:
            parts.append(
                f'<text x="{center_x:.1f}" y="{y:.1f}" text-anchor="middle" class="layer-label">{escape(name)}</text>'
            )

            # Sub-label: gas type or R-value for no-mass
            if layer.is_gas and layer.gas_type:
                parts.append(
                    f'<text x="{center_x:.1f}" y="{y + 12:.1f}" '
                    f'text-anchor="middle" class="dim-text">{layer.gas_type}</text>'
                )
            elif layer.obj_type == "Material:NoMass":
                parts.append(
                    f'<text x="{center_x:.1f}" y="{y + 12:.1f}" '
                    f'text-anchor="middle" class="dim-text">{_format_r_value(layer.r_value)}</text>'
                )

        x += width

    parts.append("</g>")
    return "\n".join(parts)


def construction_to_svg(construction: object) -> str:
    """Generate SVG for a Construction IDFObject.

    This is the main entry point for construction visualization.
    Creates an architectural cross-section diagram with proper hatching
    patterns, dimension lines, and thermal property annotations.

    Args:
        construction: Construction IDFObject

    Returns:
        SVG string

    Raises:
        TypeError: If not a Construction IDFObject
    """
    # Import here to avoid circular imports
    from ..objects import IDFObject
    from ..thermal.properties import get_thermal_properties

    if not isinstance(construction, IDFObject):
        msg = f"Expected IDFObject, got {type(construction).__name__}"
        raise TypeError(msg)

    if construction.obj_type != "Construction":
        msg = f"Expected Construction object, got {construction.obj_type}"
        raise TypeError(msg)

    props = get_thermal_properties(construction)
    return generate_construction_svg(props)
