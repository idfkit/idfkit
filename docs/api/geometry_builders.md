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
from idfkit import load_idf, create_block

# Model uses Clockwise vertex convention
model = load_idf("existing_building.idf")

# New surfaces will automatically use Clockwise ordering
# to match the model's GlobalGeometryRules
create_block(model, "Addition", [(20, 0), (30, 0), (30, 10), (20, 10)], floor_to_floor=3)
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

## Horizontal Adjacency Detection

When building models with stacked blocks (e.g. setback towers), roof
and floor surfaces at shared elevations need to be detected, split, and
linked.  The high-level [`link_blocks`](zoning.md#stacked-blocks-setbacks)
handles this automatically, but you can use the lower-level API for
custom geometry workflows.

### Detecting Adjacencies

`detect_horizontal_adjacencies` scans all `BuildingSurface:Detailed`
surfaces for horizontal Roof/Floor pairs at the same z-elevation with
`Outdoors` boundary condition, and computes their 2-D polygon
intersection:

```python
from idfkit.geometry_builders import detect_horizontal_adjacencies

adjacencies = detect_horizontal_adjacencies(doc)
for adj in adjacencies:
    print(f"Roof '{adj.roof_surface.name}' overlaps floor "
          f"'{adj.floor_surface.name}' at z={adj.z} "
          f"({adj.intersection_area:.1f} m²)")
```

Each `HorizontalAdjacency` record contains the roof surface, floor
surface, z-elevation, 2-D intersection polygon, and intersection area.

### Splitting Surfaces

`split_horizontal_surface` creates a new surface for a 2-D region
within an existing horizontal surface.  The original surface is shrunk
to the remaining area:

```python
from idfkit.geometry_builders import split_horizontal_surface

new_surface, remaining = split_horizontal_surface(doc, adj.roof_surface, adj.intersection)
# new_surface covers the intersection region
# remaining is the original surface, now covering only the exposed area
```

### Linking Surfaces

`link_horizontal_surfaces` sets mutual `Surface` boundary conditions
between a ceiling and floor:

```python
from idfkit.geometry_builders import link_horizontal_surfaces

link_horizontal_surfaces(new_surface, adj.floor_surface)
# new_surface is now a Ceiling pointing at the floor, and vice versa
```

### Full Example

```python
from idfkit.geometry_builders import (
    detect_horizontal_adjacencies,
    link_horizontal_surfaces,
    split_horizontal_surface,
)

adjacencies = detect_horizontal_adjacencies(doc)
for adj in adjacencies:
    new_ceiling, _ = split_horizontal_surface(doc, adj.roof_surface, adj.intersection)
    link_horizontal_surfaces(new_ceiling, adj.floor_surface)
```

## API Reference

::: idfkit.geometry_builders

## See Also

- [Zoning](zoning.md) -- `create_block`, `link_blocks`, core-perimeter zoning,
  footprint helpers, and multi-zone building generation
- [Geometry](geometry.md) -- Lower-level 3D primitives, coordinate transforms,
  and surface intersection
- [Visualization](visualization.md) -- 3D rendering of building geometry
- [Thermal](thermal.md) -- R/U-value calculations for constructions
