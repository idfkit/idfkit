"""
SVG generation utilities for construction visualization.

Generates cross-section diagrams for opaque and glazing constructions,
showing layer sequence, thicknesses, and thermal properties.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING
from xml.sax.saxutils import escape

if TYPE_CHECKING:
    from ..thermal.properties import ConstructionThermalProperties, LayerThermalProperties


@dataclass
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


# Material subtype to color mapping
MATERIAL_SUBTYPE_COLORS: dict[str, str] = {
    "default": "#a0522d",  # Sienna brown
    "concrete": "#808080",  # Gray
    "brick": "#b22222",  # Firebrick
    "insulation": "#ffd700",  # Gold/yellow
    "wood": "#deb887",  # Burlywood
    "gypsum": "#f5f5dc",  # Beige
    "plaster": "#fffaf0",  # Floral white
    "metal": "#c0c0c0",  # Silver
}

# Special layer type colors
NOMASS_COLOR = "#e6e6fa"  # Lavender (for resistive layers)
AIRGAP_COLOR = "#add8e6"  # Light blue

# Glazing layer type colors
GLAZING_COLORS: dict[str, str] = {
    "WindowMaterial:Glazing": "#87ceeb",  # Sky blue (glass)
    "WindowMaterial:Gas": "#f0f8ff",  # Alice blue (gas fill)
    "WindowMaterial:SimpleGlazingSystem": "#87ceeb",
}


def _guess_material_subtype(name: str) -> str:
    """Guess material subtype from name for color selection."""
    name_lower = name.lower()

    if any(x in name_lower for x in ["concrete", "cmu", "block"]):
        return "concrete"
    if any(x in name_lower for x in ["brick", "masonry"]):
        return "brick"
    if any(x in name_lower for x in ["insul", "foam", "xps", "eps", "polyiso", "mineral wool", "fiberglass"]):
        return "insulation"
    if any(x in name_lower for x in ["wood", "timber", "plywood", "osb"]):
        return "wood"
    if any(x in name_lower for x in ["gypsum", "drywall", "gyp", "sheetrock"]):
        return "gypsum"
    if any(x in name_lower for x in ["plaster", "stucco", "render"]):
        return "plaster"
    if any(x in name_lower for x in ["metal", "steel", "aluminum", "aluminium"]):
        return "metal"

    return "default"


def _get_layer_color(layer: LayerThermalProperties) -> str:
    """Get fill color for a layer based on type and name."""
    if layer.is_glazing:
        return GLAZING_COLORS.get(layer.obj_type, "#87ceeb")

    if layer.is_gas:
        if layer.obj_type == "WindowMaterial:Gas":
            return GLAZING_COLORS["WindowMaterial:Gas"]
        return AIRGAP_COLOR

    if layer.obj_type == "Material:NoMass":
        return NOMASS_COLOR

    if layer.obj_type == "Material":
        subtype = _guess_material_subtype(layer.name)
        return MATERIAL_SUBTYPE_COLORS.get(subtype, MATERIAL_SUBTYPE_COLORS["default"])

    return "#d3d3d3"  # Light gray fallback


def _get_layer_pattern(layer: LayerThermalProperties) -> str | None:
    """Get fill pattern ID for special layer types."""
    if layer.is_gas and not layer.is_glazing:
        return "air-gap-pattern"
    if layer.obj_type == "Material:NoMass":
        return "nomass-pattern"
    if layer.is_glazing and layer.obj_type == "WindowMaterial:Glazing":
        return "glass-pattern"
    return None


def _format_thickness(thickness: float | None) -> str:
    """Format thickness for display."""
    if thickness is None:
        return ""
    if thickness < 0.01:
        return f"{thickness * 1000:.1f}mm"
    return f"{thickness:.3f}m"


def _format_r_value(r_value: float) -> str:
    """Format R-value for display."""
    if r_value < 0.01:
        return f"R={r_value:.4f}"
    return f"R={r_value:.2f}"


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
    available_width = config.width - 2 * config.padding

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

    # Generate SVG
    svg_parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" '
        f'width="{config.width}" height="{config.height}" '
        f'viewBox="0 0 {config.width} {config.height}">',
        _generate_defs(props.is_glazing),
        _generate_styles(config),
    ]

    # Background
    svg_parts.append(f'<rect width="{config.width}" height="{config.height}" fill="#ffffff" />')

    # Header with title and thermal properties
    svg_parts.append(_generate_header(props, config))

    # Layer diagram
    diagram_y = config.header_height + 10
    diagram_height = config.height - config.header_height - config.footer_height - 20

    x = config.padding
    for i, (layer, width) in enumerate(zip(layers, layer_widths, strict=False)):
        svg_parts.append(_generate_layer_rect(layer, x, diagram_y, width, diagram_height, i))
        x += width

    # Outside/Inside labels
    svg_parts.append(_generate_side_labels(config, diagram_y, diagram_height))

    # Footer with layer labels
    svg_parts.append(_generate_footer(layers, layer_widths, config, diagram_y + diagram_height))

    svg_parts.append("</svg>")

    return "\n".join(svg_parts)


def _generate_empty_svg(name: str, config: SVGConfig) -> str:
    """Generate SVG for construction with no layers."""
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{config.width}" height="60">
  <rect width="{config.width}" height="60" fill="#ffffff" />
  <text x="{config.width // 2}" y="35" text-anchor="middle"
        font-family="{config.font_family}" font-size="{config.font_size}">
    {escape(name)}: No layers defined
  </text>
</svg>"""


def _generate_defs(is_glazing: bool) -> str:
    """Generate SVG defs section with patterns."""
    return """<defs>
    <!-- Air gap pattern (diagonal lines) -->
    <pattern id="air-gap-pattern" patternUnits="userSpaceOnUse" width="8" height="8">
      <rect width="8" height="8" fill="#add8e6"/>
      <line x1="0" y1="8" x2="8" y2="0" stroke="#87ceeb" stroke-width="1"/>
    </pattern>
    <!-- No-mass pattern (dotted) -->
    <pattern id="nomass-pattern" patternUnits="userSpaceOnUse" width="6" height="6">
      <rect width="6" height="6" fill="#e6e6fa"/>
      <circle cx="3" cy="3" r="1" fill="#9370db"/>
    </pattern>
    <!-- Glass pattern (vertical lines) -->
    <pattern id="glass-pattern" patternUnits="userSpaceOnUse" width="4" height="4">
      <rect width="4" height="4" fill="#87ceeb"/>
      <line x1="2" y1="0" x2="2" y2="4" stroke="#4682b4" stroke-width="0.5" opacity="0.5"/>
    </pattern>
  </defs>"""


def _generate_styles(config: SVGConfig) -> str:
    """Generate SVG styles."""
    return f"""<style>
    .title {{ font-family: {config.font_family}; font-size: {config.font_size + 2}px; font-weight: bold; }}
    .subtitle {{ font-family: {config.font_family}; font-size: {config.font_size}px; fill: #666; }}
    .layer-label {{ font-family: {config.font_family}; font-size: {config.font_size_small}px; }}
    .layer-sublabel {{ font-family: {config.font_family}; font-size: {config.font_size_small - 1}px; fill: #666; }}
    .side-label {{ font-family: {config.font_family}; font-size: {config.font_size_small}px; fill: #666; }}
    .layer-rect {{ stroke: #333; stroke-width: 1; }}
    .low-e-indicator {{ fill: none; stroke: #ff6600; stroke-width: 2; }}
  </style>"""


def _generate_header(props: ConstructionThermalProperties, config: SVGConfig) -> str:
    """Generate header section with title and thermal properties."""
    parts = ['<g class="header">']

    # Title
    parts.append(f'<text x="{config.padding}" y="25" class="title">{escape(props.name)}</text>')

    # Thermal properties on the right
    if props.is_glazing:
        u_text = f"U={props.u_value:.2f} W/m\u00b2\u00b7K"
        if props.shgc is not None:
            u_text += f"  SHGC={props.shgc:.2f}"
    else:
        u_text = f"U={props.u_value:.2f} W/m\u00b2\u00b7K  R={props.r_value_with_films:.2f} m\u00b2\u00b7K/W"

    parts.append(f'<text x="{config.width - config.padding}" y="25" text-anchor="end" class="subtitle">{u_text}</text>')

    parts.append("</g>")
    return "\n".join(parts)


def _generate_layer_rect(
    layer: LayerThermalProperties,
    x: float,
    y: float,
    width: float,
    height: float,
    index: int,
) -> str:
    """Generate SVG rectangle for a single layer."""
    color = _get_layer_color(layer)
    pattern = _get_layer_pattern(layer)

    fill = f"url(#{pattern})" if pattern else color

    parts = [
        f'<g class="layer" data-index="{index}">',
        f'<rect x="{x:.1f}" y="{y:.1f}" width="{width:.1f}" height="{height:.1f}" fill="{fill}" class="layer-rect" />',
    ]

    # Add Low-E indicator for glazing with low emissivity
    if layer.is_glazing and layer.emissivity_back is not None and layer.emissivity_back < 0.2:
        # Draw indicator line on right side (inside surface)
        parts.append(
            f'<line x1="{x + width - 2:.1f}" y1="{y + 5:.1f}" '
            f'x2="{x + width - 2:.1f}" y2="{y + height - 5:.1f}" '
            f'class="low-e-indicator" />'
        )

    if layer.is_glazing and layer.emissivity_front is not None and layer.emissivity_front < 0.2:
        # Draw indicator line on left side (outside surface)
        parts.append(
            f'<line x1="{x + 2:.1f}" y1="{y + 5:.1f}" '
            f'x2="{x + 2:.1f}" y2="{y + height - 5:.1f}" '
            f'class="low-e-indicator" />'
        )

    parts.append("</g>")
    return "\n".join(parts)


def _generate_side_labels(
    config: SVGConfig,
    diagram_y: float,
    diagram_height: float,
) -> str:
    """Generate Outside/Inside side labels."""
    mid_y = diagram_y + diagram_height / 2

    return f"""<g class="side-labels">
    <text x="{config.padding - 5}" y="{mid_y}"
          text-anchor="end" dominant-baseline="middle" class="side-label"
          transform="rotate(-90, {config.padding - 5}, {mid_y})">OUT</text>
    <text x="{config.width - config.padding + 5}" y="{mid_y}"
          text-anchor="start" dominant-baseline="middle" class="side-label"
          transform="rotate(90, {config.width - config.padding + 5}, {mid_y})">IN</text>
  </g>"""


def _generate_footer(
    layers: list[LayerThermalProperties],
    widths: list[float],
    config: SVGConfig,
    y: float,
) -> str:
    """Generate footer with layer labels."""
    parts = ['<g class="footer">']

    x = config.padding
    for layer, width in zip(layers, widths, strict=False):
        center_x = x + width / 2

        # Material name (truncated)
        name = _truncate_name(layer.name, max_len=int(width / 6))
        parts.append(
            f'<text x="{center_x:.1f}" y="{y + 15}" text-anchor="middle" class="layer-label">{escape(name)}</text>'
        )

        # Thickness or gas type
        if layer.is_gas and layer.gas_type:
            sublabel = layer.gas_type
            if layer.thickness:
                sublabel += f" {layer.thickness * 1000:.0f}mm"
        elif layer.thickness:
            sublabel = _format_thickness(layer.thickness)
        else:
            sublabel = _format_r_value(layer.r_value)

        parts.append(
            f'<text x="{center_x:.1f}" y="{y + 28}" '
            f'text-anchor="middle" class="layer-sublabel">{escape(sublabel)}</text>'
        )

        x += width

    parts.append("</g>")
    return "\n".join(parts)


def construction_to_svg(construction: object) -> str:
    """Generate SVG for a Construction IDFObject.

    This is the main entry point for construction visualization.

    Args:
        construction: Construction IDFObject

    Returns:
        SVG string
    """
    # Import here to avoid circular imports
    # Type check
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
