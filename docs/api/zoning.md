# Zoning

Automatic thermal zoning for EnergyPlus models.  Splits a 2-D building
footprint into thermal zones and creates all `Zone`,
`BuildingSurface:Detailed`, and (optionally) `Construction:AirBoundary`
objects needed for simulation.

## Quick Start

```python
from idfkit import new_document, create_building, ZoningScheme
from idfkit.zoning import footprint_rectangle

doc = new_document()
create_building(
    doc,
    name="Office",
    footprint=footprint_rectangle(50, 30),
    floor_to_floor=3.5,
    num_stories=3,
    zoning=ZoningScheme.CORE_PERIMETER,
)

# 3 stories × 5 zones (4 perimeter + 1 core) = 15 zones
print(len(doc["Zone"]))  # 15
```

## Zoning Schemes

`create_building` supports three zoning strategies via the `zoning` parameter:

| Scheme | Zones per floor | Description |
|--------|-----------------|-------------|
| `BY_STOREY` | 1 | One zone per floor (default). |
| `CORE_PERIMETER` | 5 | Four orientation-based perimeter zones plus an interior core zone. |
| `CUSTOM` | User-defined | Caller supplies named zone polygons via `custom_zones`. |

### By Storey (default)

The simplest scheme — one thermal zone per floor:

```python
from idfkit import new_document, create_building

doc = new_document()
create_building(
    doc,
    name="Warehouse",
    footprint=[(0, 0), (40, 0), (40, 20), (0, 20)],
    floor_to_floor=4.0,
    num_stories=2,
)

print(len(doc["Zone"]))  # 2
```

### Core-Perimeter

Splits each floor into four perimeter zones (North, East, South, West)
and one interior core zone.  The perimeter depth defaults to **4.57 m
(15 ft)** per ASHRAE 90.1 Appendix G and the DOE prototype buildings.

```python
from idfkit import new_document, create_building, ZoningScheme
from idfkit.zoning import footprint_rectangle

doc = new_document()
create_building(
    doc,
    name="Office",
    footprint=footprint_rectangle(50, 30),
    floor_to_floor=3.5,
    num_stories=3,
    zoning=ZoningScheme.CORE_PERIMETER,
)

# 3 stories × 5 zones = 15 zones
print(len(doc["Zone"]))  # 15
```

You can override the perimeter depth:

```python
from idfkit import new_document, create_building, ZoningScheme
from idfkit.zoning import footprint_rectangle

doc = new_document()
create_building(
    doc,
    name="Office",
    footprint=footprint_rectangle(50, 30),
    floor_to_floor=3.5,
    num_stories=1,
    zoning=ZoningScheme.CORE_PERIMETER,
    perimeter_depth=3.0,  # 3 m instead of the default 4.57 m
)
```

!!! note
    When the footprint is too small for the requested perimeter depth
    (i.e. the inradius is less than 0.5 m after insetting), zoning
    automatically falls back to a single zone per floor.

### Custom Zoning

Supply your own named zone polygons per floor using `custom_zones`.
Each entry is a `(name, polygon)` tuple:

```python
from idfkit import ZoneFootprint, ZoningScheme, create_building, new_document

doc = new_document()
create_building(
    doc,
    name="Lab",
    footprint=[(0, 0), (30, 0), (30, 20), (0, 20)],
    floor_to_floor=3.5,
    num_stories=1,
    zoning=ZoningScheme.CUSTOM,
    custom_zones=[
        ZoneFootprint("Wet Lab", [(0, 0), (15, 0), (15, 20), (0, 20)]),
        ZoneFootprint("Dry Lab", [(15, 0), (30, 0), (30, 20), (15, 20)]),
    ],
)

print(len(doc["Zone"]))  # 2
```

## Air Boundaries

Set `air_boundary=True` to apply `Construction:AirBoundary` to all
inter-zone walls.  This is useful for open-plan spaces where zone
boundaries are notional rather than physical:

```python
from idfkit import new_document, create_building, ZoningScheme
from idfkit.zoning import footprint_rectangle

doc = new_document()
create_building(
    doc,
    name="Open Office",
    footprint=footprint_rectangle(50, 30),
    floor_to_floor=3.5,
    num_stories=1,
    zoning=ZoningScheme.CORE_PERIMETER,
    air_boundary=True,
)

# A Construction:AirBoundary object is created automatically
print(len(doc["Construction:AirBoundary"]))  # 1
```

## Multi-Story Boundary Conditions

For multi-story buildings, inter-story floors and ceilings are
automatically linked with `Surface` boundary conditions:

| Story | Floor BC | Ceiling BC |
|-------|----------|------------|
| Ground floor | `Ground` | `Surface` (story above) |
| Mid floors | `Surface` (story below) | `Surface` (story above) |
| Top floor | `Surface` (story below) | `Outdoors` (Roof) |

## Footprint Helpers

Pre-built footprint generators for common commercial building shapes.
All return a list of `(x, y)` tuples in counter-clockwise order.

### `footprint_rectangle`

```python
from idfkit.zoning import footprint_rectangle

fp = footprint_rectangle(50, 30)
# [(0, 0), (50, 0), (50, 30), (0, 30)]
```

### `footprint_l_shape`

```
┌────────┐
│  wing  │
│        │
├────────┴──────────┐
│      base         │
└───────────────────┘
```

```python
from idfkit.zoning import footprint_l_shape

fp = footprint_l_shape(width=40, depth=10, wing_width=15, wing_depth=20)
```

### `footprint_u_shape`

```
┌──────┐    ┌──────┐
│      │    │      │
│      └────┘      │
│                  │
└──────────────────┘
```

```python
from idfkit.zoning import footprint_u_shape

fp = footprint_u_shape(width=40, depth=30, courtyard_width=20, courtyard_depth=15)
```

### `footprint_t_shape`

```
┌──────────────────────┐
│       top bar        │
└───┐              ┌───┘
    │    base      │
    └──────────────┘
```

```python
from idfkit.zoning import footprint_t_shape

fp = footprint_t_shape(base_width=20, base_depth=15, top_width=40, top_depth=10)
```

### `footprint_h_shape`

```
┌──────┐    ┌──────┐
│      └────┘      │
│     connector    │
│      ┌────┐      │
└──────┘    └──────┘
```

```python
from idfkit.zoning import footprint_h_shape

fp = footprint_h_shape(width=40, depth=30, courtyard_width=20, courtyard_depth=10)
```

### `footprint_courtyard`

```
┌──────────────────┐
│  ┌────────────┐  │
│  │  courtyard │  │
│  └────────────┘  │
└──────────────────┘
```

```python
from idfkit.zoning import footprint_courtyard

fp = footprint_courtyard(outer_width=50, outer_depth=40, inner_width=30, inner_depth=20)
```

### Using Footprint Helpers with `create_building`

All footprint helpers plug directly into `create_building`:

```python
from idfkit import new_document, create_building, ZoningScheme
from idfkit.zoning import footprint_l_shape

doc = new_document()
create_building(
    doc,
    name="L-Wing",
    footprint=footprint_l_shape(40, 10, 15, 20),
    floor_to_floor=3.5,
    num_stories=2,
    zoning=ZoningScheme.CORE_PERIMETER,
)
```

## ZonedBlock (Describe-then-Apply)

`ZonedBlock` is a frozen dataclass alternative that validates all
parameters up front.  Call `build()` to realise the geometry.
This *describe-then-apply* pattern lets you inspect computed properties
before committing to a document.

```python
from idfkit import new_document, ZonedBlock, ZoningScheme
from idfkit.zoning import footprint_rectangle

block = ZonedBlock(
    name="Office",
    footprint=footprint_rectangle(50, 30),
    floor_to_floor=3.5,
    num_stories=3,
    zoning=ZoningScheme.CORE_PERIMETER,
)

print(f"Building height: {block.height} m")              # 10.5
print(f"Floor area: {block.floor_area} m²")               # 1500.0
print(f"Total floor area: {block.total_floor_area} m²")  # 4500.0

doc = new_document()
objects = block.build(doc)
print(len(objects))  # all created Zone + BuildingSurface:Detailed objects
```

## API Reference

::: idfkit.zoning

## See Also

- [Geometry Builders](geometry_builders.md) -- Shading blocks and utility functions
  (`bounding_box`, `scale_building`, `set_default_constructions`)
- [Geometry](geometry.md) -- Lower-level 3D primitives, coordinate transforms,
  and surface intersection
- [Visualization](visualization.md) -- 3D rendering of building geometry
