from __future__ import annotations

from idfkit import IDFDocument, IDFObject

doc: IDFDocument = ...  # type: ignore[assignment]
wall: IDFObject = ...  # type: ignore[assignment]

# --8<-- [start:model-view-quickstart]
from idfkit import load_idf
from idfkit.visualization import view_model

doc = load_idf("building.idf")
fig = view_model(doc)  # plotly Figure
fig.show()
# --8<-- [end:model-view-quickstart]


# --8<-- [start:construction-cross-section]
from idfkit.visualization import construction_to_svg

wall = doc["Construction"]["ExteriorWall"]
svg = construction_to_svg(wall)
with open("wall_section.svg", "w") as f:
    f.write(svg)
# --8<-- [end:construction-cross-section]


# --8<-- [start:core-api]
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
# --8<-- [end:core-api]


# --8<-- [start:model-views]
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
# --8<-- [end:model-views]


# --8<-- [start:floor-plans]
from idfkit.visualization import view_floor_plan, view_exploded

# Single-story plan
view_floor_plan(doc, z_cut=0.5).show()  # cuts at Z=0.5 m

# Per-zone exploded view
view_exploded(doc, separation=2.0).show()  # each zone offset by 2 m
# --8<-- [end:floor-plans]


# --8<-- [start:normals-view]
from idfkit.visualization import view_normals

view_normals(doc).show()
# Each surface gets an arrow pointing outward.
# Inward-pointing arrows usually mean a CW vertex order — see geometry-builders-and-zoning.md.
# --8<-- [end:normals-view]


# --8<-- [start:construction-svg]
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
# --8<-- [end:construction-svg]


# --8<-- [start:jupyter-repr]
wall  # SVG diagram appears inline
# --8<-- [end:jupyter-repr]


# --8<-- [start:workflow]
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
# --8<-- [end:workflow]


# --8<-- [start:mistake-fenestration-good]
view_model(doc, config=ModelViewConfig(show_fenestration=True)).show()
# --8<-- [end:mistake-fenestration-good]


# --8<-- [start:mistake-svg-good]
construction_to_svg(doc["Construction"]["ExteriorWall"])
# --8<-- [end:mistake-svg-good]


# --8<-- [start:mistake-opacity-good]
view_model(doc, config=ModelViewConfig(opacity=0.5)).show()
# --8<-- [end:mistake-opacity-good]
