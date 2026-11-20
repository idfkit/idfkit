"""
SVG generation utilities for construction visualization.

Generates architectural cross-section diagrams for opaque and glazing constructions,
using industry-standard hatching patterns and conventions.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Literal
from xml.sax.saxutils import escape, quoteattr

if TYPE_CHECKING:
    from ..thermal.properties import ConstructionThermalProperties, LayerThermalProperties

__all__ = [
    "SVGConfig",
    "construction_to_svg",
    "generate_construction_svg",
]


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
    theme: Literal["light", "dark", "auto"] = "auto"


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

# ---------------------------------------------------------------------------
# Theme color palettes (CSS custom property values)
# ---------------------------------------------------------------------------

_LIGHT_COLORS: dict[str, str] = {
    # Background
    "idfkit-bg": "#ffffff",
    # Text fills
    "idfkit-text-title": "#333",
    "idfkit-text-props": "#555",
    "idfkit-text-label": "#333",
    "idfkit-text-dim": "#666",
    "idfkit-text-side": "#555",
    "idfkit-text-empty": "#666",
    # Strokes
    "idfkit-stroke-layer": "#444",
    "idfkit-stroke-section": "#333",
    "idfkit-stroke-dim": "#888",
    "idfkit-stroke-low-e": "#e65100",
    "idfkit-arrow-fill": "#666",
    # Material base fills
    "idfkit-mat-default": "#c4a77d",
    "idfkit-mat-concrete": "#a8a8a8",
    "idfkit-mat-brick": "#c9785d",
    "idfkit-mat-insulation": "#f5e6a3",
    "idfkit-mat-wood": "#d4a574",
    "idfkit-mat-gypsum": "#e8e4dc",
    "idfkit-mat-plaster": "#f0ebe0",
    "idfkit-mat-metal": "#b8bcc0",
    "idfkit-mat-nomass": "#d8d0e8",
    "idfkit-mat-airgap": "#e6f2f8",
    "idfkit-mat-glazing": "#b8d4e8",
    "idfkit-mat-gas": "#f0f6fa",
    "idfkit-mat-fallback": "#d3d3d3",
    # Hatch overlay strokes / dots
    "idfkit-hatch-concrete-stroke": "#888",
    "idfkit-hatch-concrete-dot": "#999",
    "idfkit-hatch-brick-stroke": "#a05040",
    "idfkit-hatch-insulation-stroke": "#c4a000",
    "idfkit-hatch-wood-stroke": "#a07850",
    "idfkit-hatch-gypsum-dot": "#ccc",
    "idfkit-hatch-metal-stroke": "#909498",
    "idfkit-hatch-glass-stroke": "#8ab4d0",
    "idfkit-hatch-airgap-stroke": "#b0c8d8",
    "idfkit-hatch-nomass-dot": "#a090c0",
    "idfkit-hatch-gasfill-stroke": "#d0e0f0",
}

_DARK_COLORS: dict[str, str] = {
    # Background
    "idfkit-bg": "#1e1e1e",
    # Text fills
    "idfkit-text-title": "#e0e0e0",
    "idfkit-text-props": "#b0b0b0",
    "idfkit-text-label": "#d0d0d0",
    "idfkit-text-dim": "#999",
    "idfkit-text-side": "#b0b0b0",
    "idfkit-text-empty": "#999",
    # Strokes
    "idfkit-stroke-layer": "#888",
    "idfkit-stroke-section": "#aaa",
    "idfkit-stroke-dim": "#666",
    "idfkit-stroke-low-e": "#ff8a50",
    "idfkit-arrow-fill": "#999",
    # Material base fills
    "idfkit-mat-default": "#7a6548",
    "idfkit-mat-concrete": "#6a6a6a",
    "idfkit-mat-brick": "#8b4f3d",
    "idfkit-mat-insulation": "#a89850",
    "idfkit-mat-wood": "#8b6d42",
    "idfkit-mat-gypsum": "#5a5750",
    "idfkit-mat-plaster": "#636058",
    "idfkit-mat-metal": "#606468",
    "idfkit-mat-nomass": "#5a4e70",
    "idfkit-mat-airgap": "#2e4858",
    "idfkit-mat-glazing": "#3a6888",
    "idfkit-mat-gas": "#2a3a48",
    "idfkit-mat-fallback": "#4a4a4a",
    # Hatch overlay strokes / dots
    "idfkit-hatch-concrete-stroke": "#555",
    "idfkit-hatch-concrete-dot": "#888",
    "idfkit-hatch-brick-stroke": "#6a3830",
    "idfkit-hatch-insulation-stroke": "#8a7020",
    "idfkit-hatch-wood-stroke": "#6a5030",
    "idfkit-hatch-gypsum-dot": "#777",
    "idfkit-hatch-metal-stroke": "#808488",
    "idfkit-hatch-glass-stroke": "#5a8ab0",
    "idfkit-hatch-airgap-stroke": "#4a7898",
    "idfkit-hatch-nomass-dot": "#7060a0",
    "idfkit-hatch-gasfill-stroke": "#3a5a78",
}

# CSS variable references for layer fills (used instead of raw hex values)
_MATERIAL_CSS_VARS: dict[str, str] = {
    "default": "var(--idfkit-mat-default)",
    "concrete": "var(--idfkit-mat-concrete)",
    "brick": "var(--idfkit-mat-brick)",
    "insulation": "var(--idfkit-mat-insulation)",
    "wood": "var(--idfkit-mat-wood)",
    "gypsum": "var(--idfkit-mat-gypsum)",
    "plaster": "var(--idfkit-mat-plaster)",
    "metal": "var(--idfkit-mat-metal)",
}

_GLAZING_CSS_VARS: dict[str, str] = {
    "WindowMaterial:Glazing": "var(--idfkit-mat-glazing)",
    "WindowMaterial:Gas": "var(--idfkit-mat-gas)",
    "WindowMaterial:SimpleGlazingSystem": "var(--idfkit-mat-glazing)",
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
        Tuple of (css_var_reference, pattern_id or None)
    """
    # Glazing layers
    if layer.is_glazing:
        color = _GLAZING_CSS_VARS.get(layer.obj_type, _GLAZING_CSS_VARS["WindowMaterial:Glazing"])
        if layer.obj_type == "WindowMaterial:Glazing":
            return color, PATTERN_IDS["glass"]
        return color, None

    # Gas/air gap layers
    if layer.is_gas:
        if layer.obj_type == "WindowMaterial:Gas":
            return _GLAZING_CSS_VARS["WindowMaterial:Gas"], PATTERN_IDS["gas-fill"]
        return "var(--idfkit-mat-airgap)", PATTERN_IDS["air-gap"]

    # No-mass resistive layers
    if layer.obj_type == "Material:NoMass":
        return "var(--idfkit-mat-nomass)", PATTERN_IDS["nomass"]

    # Standard material layers
    if layer.obj_type == "Material":
        subtype = _guess_material_subtype(layer.name)
        color = _MATERIAL_CSS_VARS.get(subtype, _MATERIAL_CSS_VARS["default"])
        pattern = PATTERN_IDS.get(subtype)
        return color, pattern

    return "var(--idfkit-mat-fallback)", None


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
    theme_class = f"idfkit-theme-{config.theme}"
    svg_parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" '
        f'class="{theme_class}" '
        f'width="{config.width}" height="{config.height}" '
        f'viewBox="0 0 {config.width} {config.height}">',
        _generate_defs(layers),
        _generate_styles(config),
    ]

    # Background
    svg_parts.append(f'<rect width="{config.width}" height="{config.height}" fill="var(--idfkit-bg)" />')

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
    theme_class = f"idfkit-theme-{config.theme}"
    theme_css = _generate_theme_css(config.theme)
    return f"""<svg xmlns="http://www.w3.org/2000/svg" class="{theme_class}" width="{config.width}" height="60">
  <style>
{theme_css}
  </style>
  <rect width="{config.width}" height="60" fill="var(--idfkit-bg)" />
  <text x="{config.width // 2}" y="35" text-anchor="middle"
        font-family="{config.font_family}" font-size="{config.font_size}" fill="var(--idfkit-text-empty)">
    {escape(name)}: No layers defined
  </text>
</svg>"""


def _get_pattern_svg(pattern_id: str) -> str:
    """Get SVG pattern definition for a given pattern ID."""
    pattern_defs: dict[str, str] = {
        PATTERN_IDS["concrete"]: f"""
    <pattern id="{PATTERN_IDS["concrete"]}" patternUnits="userSpaceOnUse" width="12" height="12">
      <rect width="12" height="12" fill="var(--idfkit-mat-concrete)"/>
      <line x1="0" y1="12" x2="12" y2="0" stroke="var(--idfkit-hatch-concrete-stroke)" stroke-width="0.5"/>
      <circle cx="3" cy="3" r="0.8" fill="var(--idfkit-hatch-concrete-dot)"/>
      <circle cx="9" cy="9" r="0.6" fill="var(--idfkit-hatch-concrete-stroke)"/>
      <circle cx="6" cy="7" r="0.5" fill="var(--idfkit-hatch-concrete-dot)"/>
    </pattern>""",
        PATTERN_IDS["brick"]: f"""
    <pattern id="{PATTERN_IDS["brick"]}" patternUnits="userSpaceOnUse" width="8" height="8">
      <rect width="8" height="8" fill="var(--idfkit-mat-brick)"/>
      <line x1="0" y1="8" x2="8" y2="0" stroke="var(--idfkit-hatch-brick-stroke)" stroke-width="0.6"/>
      <line x1="-2" y1="6" x2="6" y2="-2" stroke="var(--idfkit-hatch-brick-stroke)" stroke-width="0.6"/>
    </pattern>""",
        PATTERN_IDS["insulation"]: f"""
    <pattern id="{PATTERN_IDS["insulation"]}" patternUnits="userSpaceOnUse" width="16" height="8">
      <rect width="16" height="8" fill="var(--idfkit-mat-insulation)"/>
      <path d="M0,4 L4,1 L8,4 L12,1 L16,4" stroke="var(--idfkit-hatch-insulation-stroke)" stroke-width="0.8" fill="none"/>
      <path d="M0,7 L4,4 L8,7 L12,4 L16,7" stroke="var(--idfkit-hatch-insulation-stroke)" stroke-width="0.8" fill="none"/>
    </pattern>""",
        PATTERN_IDS["wood"]: f"""
    <pattern id="{PATTERN_IDS["wood"]}" patternUnits="userSpaceOnUse" width="16" height="8">
      <rect width="16" height="8" fill="var(--idfkit-mat-wood)"/>
      <path d="M0,2 Q4,1 8,2 T16,2" stroke="var(--idfkit-hatch-wood-stroke)" stroke-width="0.5" fill="none"/>
      <path d="M0,5 Q4,4 8,5 T16,5" stroke="var(--idfkit-hatch-wood-stroke)" stroke-width="0.5" fill="none"/>
      <path d="M0,7 Q4,8 8,7 T16,7" stroke="var(--idfkit-hatch-wood-stroke)" stroke-width="0.4" fill="none"/>
    </pattern>""",
        PATTERN_IDS["gypsum"]: f"""
    <pattern id="{PATTERN_IDS["gypsum"]}" patternUnits="userSpaceOnUse" width="6" height="6">
      <rect width="6" height="6" fill="var(--idfkit-mat-gypsum)"/>
      <circle cx="1" cy="1" r="0.3" fill="var(--idfkit-hatch-gypsum-dot)"/>
      <circle cx="4" cy="3" r="0.3" fill="var(--idfkit-hatch-gypsum-dot)"/>
      <circle cx="2" cy="5" r="0.3" fill="var(--idfkit-hatch-gypsum-dot)"/>
    </pattern>""",
        PATTERN_IDS["metal"]: f"""
    <pattern id="{PATTERN_IDS["metal"]}" patternUnits="userSpaceOnUse" width="4" height="4">
      <rect width="4" height="4" fill="var(--idfkit-mat-metal)"/>
      <line x1="0" y1="4" x2="4" y2="0" stroke="var(--idfkit-hatch-metal-stroke)" stroke-width="0.6"/>
    </pattern>""",
        PATTERN_IDS["glass"]: f"""
    <pattern id="{PATTERN_IDS["glass"]}" patternUnits="userSpaceOnUse" width="6" height="200">
      <rect width="6" height="200" fill="var(--idfkit-mat-glazing)"/>
      <line x1="1.5" y1="0" x2="1.5" y2="200" stroke="var(--idfkit-hatch-glass-stroke)" stroke-width="0.5" opacity="0.4"/>
    </pattern>""",
        PATTERN_IDS["air-gap"]: f"""
    <pattern id="{PATTERN_IDS["air-gap"]}" patternUnits="userSpaceOnUse" width="12" height="12">
      <rect width="12" height="12" fill="var(--idfkit-mat-airgap)"/>
      <line x1="0" y1="12" x2="12" y2="0" stroke="var(--idfkit-hatch-airgap-stroke)" stroke-width="0.4"/>
    </pattern>""",
        PATTERN_IDS["nomass"]: f"""
    <pattern id="{PATTERN_IDS["nomass"]}" patternUnits="userSpaceOnUse" width="8" height="8">
      <rect width="8" height="8" fill="var(--idfkit-mat-nomass)"/>
      <circle cx="4" cy="4" r="1" fill="var(--idfkit-hatch-nomass-dot)"/>
    </pattern>""",
        PATTERN_IDS["gas-fill"]: f"""
    <pattern id="{PATTERN_IDS["gas-fill"]}" patternUnits="userSpaceOnUse" width="16" height="16">
      <rect width="16" height="16" fill="var(--idfkit-mat-gas)"/>
      <line x1="0" y1="16" x2="16" y2="0" stroke="var(--idfkit-hatch-gasfill-stroke)" stroke-width="0.3"/>
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
      <path d="M0,0 L0,6 L6,3 z" fill="var(--idfkit-arrow-fill)"/>
    </marker>
    <marker id="arrow-rev" markerWidth="6" markerHeight="6" refX="1" refY="3" orient="auto">
      <path d="M6,0 L6,6 L0,3 z" fill="var(--idfkit-arrow-fill)"/>
    </marker>""")

    parts.append("</defs>")
    return "\n".join(parts)


def _css_variable_block(colors: dict[str, str]) -> str:
    """Generate CSS custom property declarations from a color dict."""
    lines = [f"    --{name}: {value};" for name, value in colors.items()]
    return "\n".join(lines)


def _generate_theme_css(theme: str) -> str:
    """Generate the CSS variable declarations for the selected theme."""
    if theme == "dark":
        return f"  .idfkit-theme-dark {{\n{_css_variable_block(_DARK_COLORS)}\n  }}"
    if theme == "auto":
        return (
            f"  .idfkit-theme-auto {{\n{_css_variable_block(_LIGHT_COLORS)}\n  }}\n"
            f"  @media (prefers-color-scheme: dark) {{\n"
            f"    .idfkit-theme-auto {{\n{_css_variable_block(_DARK_COLORS)}\n    }}\n"
            f"  }}"
        )
    # Default: light
    return f"  .idfkit-theme-light {{\n{_css_variable_block(_LIGHT_COLORS)}\n  }}"


def _generate_styles(config: SVGConfig) -> str:
    """Generate SVG styles with CSS custom properties for theming."""
    theme_css = _generate_theme_css(config.theme)
    return f"""<style>
{theme_css}
    .title {{ font-family: {config.font_family}; font-size: {config.font_size + 2}px; font-weight: 600; fill: var(--idfkit-text-title); }}
    .thermal-props {{ font-family: {config.font_family}; font-size: {config.font_size}px; fill: var(--idfkit-text-props); }}
    .layer-label {{ font-family: {config.font_family}; font-size: {config.font_size_small}px; fill: var(--idfkit-text-label); }}
    .dim-text {{ font-family: {config.font_family}; font-size: {config.font_size_small - 1}px; fill: var(--idfkit-text-dim); }}
    .side-label {{ font-family: {config.font_family}; font-size: {config.font_size_small}px; fill: var(--idfkit-text-side); font-weight: 500; }}
    .layer-rect {{ stroke: var(--idfkit-stroke-layer); stroke-width: 1; }}
    .section-cut {{ stroke: var(--idfkit-stroke-section); stroke-width: 1.5; }}
    .dim-line {{ stroke: var(--idfkit-stroke-dim); stroke-width: 0.5; }}
    .low-e-coating {{ fill: none; stroke: var(--idfkit-stroke-low-e); stroke-width: 2.5; stroke-linecap: round; }}
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

    parts = [f'<g class="layer" data-index="{index}" data-name={quoteattr(layer.name)}>']

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


def construction_to_svg(
    construction: object,
    config: SVGConfig | None = None,
) -> str:
    """Generate SVG for a Construction IDFObject.

    This is the main entry point for construction visualization.
    Creates an architectural cross-section diagram with proper hatching
    patterns, dimension lines, and thermal property annotations.

    Args:
        construction: Construction IDFObject
        config: Optional SVGConfig for customization (including theme)

    Returns:
        SVG string

    Raises:
        TypeError: If not a Construction IDFObject
        DanglingReferenceError: If a layer names a material the document does not have.
        ValueError: If *construction* has layers but is not in a document, so they cannot be resolved.
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
    return generate_construction_svg(props, config)
