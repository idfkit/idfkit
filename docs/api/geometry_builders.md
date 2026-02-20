# Geometry Builders

Geometry utility functions for EnergyPlus surface manipulation.  For
creating building zones and surfaces, see [Zoning](zoning.md).

## Quick Start

```python
from idfkit import new_document
from idfkit.geometry_builders import add_shading_block

doc = new_document()
add_shading_block(doc, "Neighbour", [(30, 0), (50, 0), (50, 20), (30, 20)], height=25)

print(len(doc["Shading:Site:Detailed"]))  # 5
```

## Shading Blocks

`add_shading_block` creates `Shading:Site:Detailed` surfaces --
opaque boxes that cast shadows but have no thermal zones.

```python
from idfkit import new_document
from idfkit.geometry_builders import add_shading_block

doc = new_document()

# Neighbouring building
add_shading_block(doc, "Neighbour", [(30, 0), (50, 0), (50, 20), (30, 20)], height=25)

# Elevated canopy
add_shading_block(doc, "Canopy", [(0, -3), (10, -3), (10, 0), (0, 0)], height=0.2, base_z=3)
```

Each call creates one wall surface per footprint edge plus a horizontal
top cap.

## GlobalGeometryRules Convention

All builder functions read the document's `GlobalGeometryRules` to
determine the vertex ordering convention:

- **`starting_vertex_position`** -- which corner is listed first for
  walls (`UpperLeftCorner`, `LowerLeftCorner`, etc.)
- **`vertex_entry_direction`** -- winding direction (`Counterclockwise`
  or `Clockwise`)

`new_document()` pre-seeds `GlobalGeometryRules` with
`UpperLeftCorner` / `Counterclockwise` defaults. If a model is missing
`GlobalGeometryRules` (for example, some legacy inputs), the same
EnergyPlus defaults are assumed.

This means you can safely add geometry to an existing model that uses a
non-default convention without having to rewrite all existing surfaces:

```python
from idfkit import load_idf, create_building

# Model uses Clockwise vertex convention
model = load_idf("existing_building.idf")

# New surfaces will automatically use Clockwise ordering
# to match the model's GlobalGeometryRules
create_building(model, "Addition", [(20, 0), (30, 0), (30, 10), (20, 10)], floor_to_floor=3)
```

### Wall Vertex Order by Convention

For a wall between footprint vertices **p1** and **p2** (height
*z_bot* to *z_top*), viewed from outside:

| Starting Position | Counterclockwise | Clockwise |
|-------------------|------------------|-----------|
| UpperLeftCorner | UL LL LR UR | UL UR LR LL |
| LowerLeftCorner | LL LR UR UL | LL UL UR LR |
| LowerRightCorner | LR UR UL LL | LR LL UL UR |
| UpperRightCorner | UR UL LL LR | UR LR LL UL |

Where UL = (p1, z_top), LL = (p1, z_bot), LR = (p2, z_bot),
UR = (p2, z_top).

### Horizontal Surfaces

For floors and ceilings, the winding direction is adapted so that
EnergyPlus computes the correct outward normal regardless of convention:

- **Floor**: outward normal points down (toward ground)
- **Ceiling / Roof**: outward normal points up (toward sky)

## Utility Functions

### `set_default_constructions`

Assigns a placeholder construction name to any surface that lacks one:

```python
from idfkit.geometry_builders import set_default_constructions

count = set_default_constructions(doc, "Generic Wall")
print(f"Updated {count} surfaces")
```

### `bounding_box`

Returns the 2D axis-aligned bounding box of all
`BuildingSurface:Detailed` objects:

```python
from idfkit.geometry_builders import bounding_box

bbox = bounding_box(doc)
if bbox:
    (min_x, min_y), (max_x, max_y) = bbox
    print(f"Footprint spans {max_x - min_x:.1f} x {max_y - min_y:.1f} m")
```

### `scale_building`

Scales all surface vertices around an anchor point:

```python
from idfkit.geometry_builders import scale_building
from idfkit.geometry import Vector3D

# Double the building in all directions
scale_building(doc, 2.0)

# Stretch only the X axis
scale_building(doc, (1.5, 1.0, 1.0))

# Scale around the building centroid
scale_building(doc, 0.5, anchor=Vector3D(15, 10, 0))
```

## API Reference

::: idfkit.geometry_builders

## See Also

- [Zoning](zoning.md) -- `create_building`, core-perimeter zoning, footprint
  helpers, and multi-zone building generation
- [Geometry](geometry.md) -- Lower-level 3D primitives, coordinate transforms,
  and surface intersection
- [Visualization](visualization.md) -- 3D rendering of building geometry
- [Thermal](thermal.md) -- R/U-value calculations for constructions
