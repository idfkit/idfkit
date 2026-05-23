# Geometry builders and zoning

idfkit's `geometry_builders` and `zoning` modules are for **synthesizing** building geometry from scratch — generating footprints, extruding them into multi-story blocks, splitting each floor into zones, and linking adjacent surfaces. This is the layer above `geometry.py` (which is about querying existing geometry — see [geometry-and-surfaces.md](geometry-and-surfaces.md)).

## When to use

- You're building a model from scratch and need a footprint + zones.
- You want to extrude a footprint into a multi-story block with one call.
- You need to link surfaces between adjacent zones or between stacked blocks.
- You need to scale or batch-edit existing geometry.

## Quick start

```python
from idfkit import new_document, write_idf, ZoningScheme, create_block, footprint_rectangle

doc = new_document()
create_block(
    doc,
    name="Office",
    footprint=footprint_rectangle(width=50.0, depth=30.0),
    floor_to_floor=3.5,
    num_stories=3,
    zoning=ZoningScheme.CORE_PERIMETER,
)
write_idf(doc, "block.idf")
```

That single call produces zones, floors, ceilings, exterior walls, interior walls, ground/roof boundary conditions, and inter-floor links for an entire 3-story block.

## Footprints

idfkit provides parametric footprint generators that return `list[tuple[float, float]]` in counter-clockwise order:

```python
from idfkit import (
    footprint_rectangle,
    footprint_l_shape,
    footprint_u_shape,
    footprint_t_shape,
    footprint_h_shape,
    footprint_courtyard,
)

rect = footprint_rectangle(width=50, depth=30)
ell = footprint_l_shape(width=40, depth=20, wing_width=20, wing_depth=15)
u = footprint_u_shape(width=40, depth=30, courtyard_width=15, courtyard_depth=10)
courtyard = footprint_courtyard(width=40, depth=30, court_x=10, court_y=10, court_w=15, court_d=10)
```

Or pass any CCW `list[tuple[float, float]]` you generate yourself.

## Zoning schemes

`ZoningScheme` controls how each story is partitioned:

- `BY_STOREY` (default) — one zone per floor.
- `CORE_PERIMETER` — core + 4 perimeter zones per floor. Perimeter depth defaults to `ASHRAE_PERIMETER_DEPTH` (4.57 m).
- `CUSTOM` — caller supplies `ZoneFootprint` polygons for each floor.

```python
from idfkit import ZoningScheme, ZoneFootprint

create_block(doc, "Office", rect, floor_to_floor=3.5, num_stories=3,
             zoning=ZoningScheme.BY_STOREY)

create_block(doc, "Office", rect, floor_to_floor=3.5, num_stories=3,
             zoning=ZoningScheme.CORE_PERIMETER,
             perimeter_depth=4.0)

create_block(doc, "Office", rect, floor_to_floor=3.5, num_stories=3,
             zoning=ZoningScheme.CUSTOM,
             custom_zones=[
                 ZoneFootprint(name="MeetingRoom", polygon=[(0,0), (10,0), (10,10), (0,10)]),
                 ZoneFootprint(name="OpenPlan",    polygon=[(10,0), (50,0), (50,30), (10,30), (10,10), (0,10), (0,0)]),
             ])
```

`create_block` also accepts:

- `air_boundary=True` — apply `Construction:AirBoundary` to all inter-zone walls. Use for open-plan spaces that share air but are still thermally distinct.
- `base_elevation` — ground floor Z (default 0). When > 0, the ground-floor boundary becomes `Outdoors` instead of `Ground`.

## Multi-block buildings (setbacks)

For setback geometries (e.g. a base + tower), call `create_block` twice and link the stacked surfaces:

```python
from idfkit import create_block, link_blocks, footprint_rectangle, ZoningScheme

create_block(doc, "Base", footprint_rectangle(50, 30), floor_to_floor=3.5, num_stories=3,
             zoning=ZoningScheme.CORE_PERIMETER)
create_block(doc, "Tower", footprint_rectangle(30, 20, origin=(10, 5)),
             floor_to_floor=3.5, num_stories=8,
             base_elevation=3.5 * 3,
             zoning=ZoningScheme.CORE_PERIMETER)

link_blocks(doc)                           # auto-detect and link all stacked blocks
# or
link_blocks(doc, lower="Base", upper="Tower")  # link a specific pair
```

`link_blocks` finds matching ceiling/floor pairs between blocks and sets their boundary conditions to `Surface` pointing at each other.

## Shading blocks

For solar shading from neighbouring structures (not conditioned space):

```python
from idfkit import add_shading_block, footprint_rectangle

add_shading_block(
    doc,
    name="ParkingGarage",
    footprint=footprint_rectangle(40, 20, origin=(60, 0)),
    height=12.0,
)
```

This adds `Shading:Building:Detailed` surfaces (not zones or interior walls).

## Building-wide edits

```python
from idfkit import bounding_box, scale_building, set_default_constructions

# Inspect — returns None if the model has no surfaces
bb = bounding_box(doc)
if bb is not None:
    (xmin, ymin), (xmax, ymax) = bb

# Scale all surfaces uniformly (e.g. for unit conversion or sensitivity studies)
scale_building(doc, scale_factor=1.1)      # 10% larger

# Quickly assign a default construction to surfaces that lack one
set_default_constructions(doc, construction_name="Default Construction")
```

## Horizontal adjacencies

For multi-story models where floors and ceilings need to be linked to their neighbours above/below:

```python
from idfkit import detect_horizontal_adjacencies, link_horizontal_surfaces

adjacencies = detect_horizontal_adjacencies(doc)
for adj in adjacencies:
    link_horizontal_surfaces(adj.ceiling, adj.floor)
```

`create_block` calls this automatically for the block it produces; you need to invoke it yourself only when stitching together hand-authored stories.

## Splitting a single surface

When a footprint changes and you want to keep one surface but redraw it:

```python
from idfkit.geometry_builders import split_horizontal_surface

new_pieces = split_horizontal_surface(
    surface,
    cut_polygon=[(10, 0), (20, 0), (20, 10), (10, 10)],
)
```

## Common mistakes

**BAD — passing a clockwise footprint**

```python
cw_rect = [(0,0), (0,30), (50,30), (50,0)]  # clockwise
create_block(doc, "Office", cw_rect, floor_to_floor=3.5, num_stories=1)
# Surfaces will have inward normals; EnergyPlus thinks the building is inside-out.
```

**GOOD — counter-clockwise**

```python
ccw_rect = footprint_rectangle(50, 30)     # CCW by construction
```

**BAD — relying on `create_block` to add HVAC**

```python
create_block(doc, "Office", rect, floor_to_floor=3.5, num_stories=3,
             zoning=ZoningScheme.CORE_PERIMETER)
simulate(doc, "weather.epw")               # zones have no HVAC — uncontrolled
```

**GOOD — add HVAC explicitly**

```python
create_block(doc, ...)
for zone in doc["Zone"]:
    doc.add("HVACTemplate:Zone:IdealLoadsAirSystem",
            zone_name=zone.name,
            template_thermostat_name="OfficeThermostat")
```

See [hvac-templates.md](hvac-templates.md).

**BAD — forgetting `link_blocks` between setbacks**

```python
create_block(doc, "Base", ...)
create_block(doc, "Tower", base_elevation=10.5, ...)
# Tower floor and base ceiling are both `Outdoors` — heat flows where it shouldn't.
```

**GOOD — link them**

```python
link_blocks(doc)
```

## Related

- [geometry-and-surfaces.md](geometry-and-surfaces.md) — calculations on the geometry once it's built.
- [hvac-templates.md](hvac-templates.md) — what to do with the zones you just generated.
- [visualization.md](visualization.md) — render the block to sanity-check it.
- API docs: [py.idfkit.com/api/zoning/](https://py.idfkit.com/api/zoning/) and [py.idfkit.com/api/geometry/](https://py.idfkit.com/api/geometry/)
