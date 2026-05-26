# Visualization

`idfkit.visualization` renders models in two ways: an interactive 3D viewer (plotly) for whole-building geometry, and an SVG generator for construction cross-sections. Both are pure-Python and require no external CAD tooling.

## When to use

- You want to sanity-check geometry you just synthesised with `create_block`.
- You're debugging a surface normal orientation.
- You want a publication-ready construction cross-section diagram.
- You're embedding in Jupyter and want notebook-native visualisations.

## Quick start

### 3D model view

```python
from idfkit import load_idf
from idfkit.visualization import view_model

doc = load_idf("building.idf")
fig = view_model(doc)  # plotly Figure
fig.show()
```

### Construction cross-section

```python
from idfkit.visualization import construction_to_svg

wall = doc["Construction"]["ExteriorWall"]
svg = construction_to_svg(wall)
with open("wall_section.svg", "w") as f:
    f.write(svg)
```

In Jupyter, `wall` displays automatically as the SVG cross-section thanks to `IDFObject._repr_svg_`.

## Core API

```python
from idfkit.visualization import (
    view_model,  # 3D building view (plotly)
    view_floor_plan,  # 2D top-down plan
    view_exploded,  # surfaces separated for inspection
    view_normals,  # outward-normal arrows for debugging
    ModelViewConfig,  # styling options
    ColorBy,  # color-by-zone, by-boundary, by-construction, …
    construction_to_svg,  # one-shot SVG string
    SVGConfig,  # SVG styling options
)
```

## 3D model views

```python
from idfkit.visualization import view_model, ColorBy, ModelViewConfig

# Default — colour by zone
view_model(doc).show()

# Colour by boundary condition (Outdoors / Surface / Ground / Adiabatic)
view_model(doc, config=ModelViewConfig(color_by=ColorBy.BOUNDARY_CONDITION)).show()

# Colour by construction (handy when you have many constructions)
view_model(doc, config=ModelViewConfig(color_by=ColorBy.CONSTRUCTION)).show()

# Restrict to specific zones
view_model(doc, zones=["Office_Core", "Office_Perimeter_N"]).show()

# Tune the styling (opacity, edges, labels, …)
cfg = ModelViewConfig(
    color_by=ColorBy.ZONE,
    show_fenestration=True,
    show_labels=False,
    opacity=0.8,
)
view_model(doc, config=cfg).show()
```

`view_model` returns a `plotly.graph_objects.Figure` — call `.show()`, `.write_image()`, or `.write_html()` on it. Requires `idfkit[plotly]`. `ColorBy` members: `ZONE`, `SURFACE_TYPE`, `BOUNDARY_CONDITION`, `CONSTRUCTION`.

## Floor plans and exploded views

```python
from idfkit.visualization import view_floor_plan, view_exploded

# Single-story plan
view_floor_plan(doc, z_cut=0.5).show()  # cuts at Z=0.5 m

# Per-zone exploded view
view_exploded(doc, separation=2.0).show()  # each zone offset by 2 m
```

`view_floor_plan` is most useful for confirming zoning and core/perimeter splits. `view_exploded` is best for confirming surface ownership and adjacency.

## Normals view (debugging)

```python
from idfkit.visualization import view_normals

view_normals(doc).show()
# Each surface gets an arrow pointing outward.
# Inward-pointing arrows usually mean a CW vertex order — see geometry-builders-and-zoning.md.
```

When you see arrows pointing into the building, you know the surface vertices are in the wrong winding order. Fix the source geometry rather than trying to flip per-surface.

## Construction SVG diagrams

```python
from idfkit.visualization import construction_to_svg, SVGConfig

wall = doc["Construction"]["ExteriorWall"]
svg = construction_to_svg(wall)  # default styling

# Custom styling (width/height/padding/font, plus light/dark/auto theme)
cfg = SVGConfig(
    width=800,
    height=400,
    theme="dark",
)
svg = construction_to_svg(wall, config=cfg)
```

The SVG shows layered materials with proportional thicknesses, material names, and R-values per layer. Each material type gets a distinct fill colour (insulation, glass, gas, opaque mass, …).

For programmatic embedding into other diagrams, the lower-level `generate_construction_svg` returns a `bytes`-ready SVG with no surrounding `<svg>` boilerplate.

## Jupyter integration

`IDFObject` provides `_repr_svg_` for constructions, so just rendering a construction in a notebook cell shows the cross-section:

```python
wall  # SVG diagram appears inline
```

For 3D, `view_model(...)` returns a plotly Figure, which plotly automatically renders in notebooks.

## Workflow: edit-then-verify

```python
from idfkit import new_document, create_block, footprint_l_shape, ZoningScheme, set_wwr
from idfkit.visualization import view_model

doc = new_document()
create_block(
    doc,
    "Office",
    footprint_l_shape(width=40, depth=20, wing_width=20, wing_depth=15),
    floor_to_floor=3.5,
    num_stories=3,
    zoning=ZoningScheme.CORE_PERIMETER,
)
for orientation, ratio in [("North", 0.3), ("South", 0.5), ("East", 0.4), ("West", 0.4)]:
    set_wwr(doc, wwr=ratio, orientation=orientation)

view_model(doc).show()  # sanity check before simulation
```

This is the canonical "did I get the geometry right?" loop. Render, look, edit, re-render.

## Common mistakes

!!! failure "silently hiding fenestration when you're studying it"

    ```python
    view_model(doc, config=ModelViewConfig(show_fenestration=False)).show()
    # Windows hidden — you may miss that south-facing fenestration didn't get applied
    ```

!!! success "keep fenestration on for envelope studies"

    ```python
    view_model(doc, config=ModelViewConfig(show_fenestration=True)).show()
    ```

!!! failure "`construction_to_svg` on an opaque material"

    ```python
    construction_to_svg(doc["Material"]["XPS_50mm"])   # not a Construction
    # TypeError-equivalent: expects a Construction, not a Material
    ```

!!! success "operate on `Construction`"

    ```python
    construction_to_svg(doc["Construction"]["ExteriorWall"])
    ```

!!! failure "large models with no opacity tuning"

    ```python
    view_model(doc).show()                     # rooms hidden behind exterior walls
    ```

!!! success "drop opacity for interior visibility"

    ```python
    view_model(doc, config=ModelViewConfig(opacity=0.5)).show()
    ```

## Related

- [geometry-and-surfaces.md](geometry-and-surfaces.md) — what's being rendered.
- [geometry-builders-and-zoning.md](geometry-builders-and-zoning.md) — the typical "create-then-verify" pair.
- [thermal-properties.md](thermal-properties.md) — the R-value annotations in the SVG.
- API docs: [py.idfkit.com/api/visualization/](https://py.idfkit.com/api/visualization/)
