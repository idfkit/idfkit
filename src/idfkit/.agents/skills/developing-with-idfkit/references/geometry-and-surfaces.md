# Geometry and surfaces

idfkit ships a small, dependency-free 3D geometry layer for the calculations you do most often on EnergyPlus models: surface area, azimuth, tilt, zone volume, and 2D polygon ops. `Vector3D` and `Polygon3D` are the two building-block types; everything else is a free function that takes them or operates on `IDFObject` surfaces directly.

## When to use

- You need to compute area/azimuth/tilt/volume from a model on disk.
- You want to translate or rotate a building.
- You're doing area-weighted aggregations (e.g. WWR per orientation, U-value × area).
- You're cleaning up a model with `intersect_match()` to detect adjacency.

For building **synthesis** (footprints, zoning, fenestration), see [geometry-builders-and-zoning.md](geometry-builders-and-zoning.md).

## Quick start

```python
from idfkit import (
    load_idf,
    calculate_surface_area,
    calculate_surface_azimuth,
    calculate_zone_volume,
    set_wwr,
    intersect_match,
    Vector3D,
    Polygon3D,
)

doc = load_idf("building.idf")

# Per-surface
for surface in doc["BuildingSurface:Detailed"]:
    print(surface.name, calculate_surface_area(surface),
          calculate_surface_azimuth(surface))

# Per-zone
print(calculate_zone_volume(doc, "Office"))

# Bulk
set_wwr(doc, wwr=0.4, orientation="South")
intersect_match(doc)
```

## Core types

### `Vector3D`

```python
v = Vector3D(1.0, 0.0, 0.0)
v.x, v.y, v.z
v + Vector3D(0, 1, 0)                      # vector addition
v - Vector3D(0, 1, 0)
v.dot(other)
v.cross(other)
v.length()
v.normalize()
v.rotate_z(angle_deg=45)                   # rotate about Z (vertical), degrees
```

### `Polygon3D`

```python
poly = Polygon3D([Vector3D(0,0,0), Vector3D(10,0,0), Vector3D(10,5,0), Vector3D(0,5,0)])
poly.area                                  # 50.0
poly.centroid                              # Vector3D
poly.normal                                # outward normal as Vector3D
poly.azimuth                               # 0–360, degrees clockwise from North
poly.tilt                                  # 0–180, degrees from horizontal
```

`Polygon3D` does not expose a "reverse winding" helper — for floor↔ceiling matching, build a new polygon with the vertices in the opposite order (`Polygon3D(list(reversed(poly.vertices)))`).

## Surface calculations

```python
from idfkit import (
    calculate_surface_area,
    calculate_surface_azimuth,
    calculate_surface_tilt,
)

surface = doc["BuildingSurface:Detailed"]["South Wall"]
calculate_surface_area(surface)            # m²
calculate_surface_azimuth(surface)         # 180 for a south wall (relative to North)
calculate_surface_tilt(surface)            # 90 for a vertical wall, 0 for a roof
```

Internally these read the vertex list off the surface object and build a `Polygon3D`. To work with the polygon directly:

```python
from idfkit.geometry import get_surface_coords, set_surface_coords

poly = get_surface_coords(surface)         # Polygon3D | None
set_surface_coords(surface, new_poly)      # writes vertices back, normal recomputed
```

## Zone calculations

```python
from idfkit import (
    calculate_zone_floor_area,
    calculate_zone_ceiling_area,
    calculate_zone_height,
    calculate_zone_volume,
)

zone_name = "Office"
calculate_zone_floor_area(doc, zone_name)
calculate_zone_ceiling_area(doc, zone_name)
calculate_zone_height(doc, zone_name)
calculate_zone_volume(doc, zone_name)
```

Zone volume is computed from the bounding surfaces — it works for any prismatic and most non-prismatic geometries.

## Building-wide transforms

```python
from idfkit import translate_building, rotate_building, Vector3D

translate_building(doc, Vector3D(10.0, 5.0, 0.0))   # shift all vertices
rotate_building(doc, angle_deg=15.0)                # rotate about Z, anchor=origin
rotate_building(doc, angle_deg=15.0, anchor=Vector3D(50, 50, 0))
```

These walk every `BuildingSurface:Detailed`, `Shading:*`, and `FenestrationSurface:Detailed` and transform vertices in place. Zone origins update too.

## Window-to-wall ratio (WWR)

`set_wwr` rewrites fenestration on exterior walls to match a target WWR:

```python
from idfkit import set_wwr

set_wwr(doc, wwr=0.4)                      # all exterior walls
set_wwr(doc, wwr=0.4, orientation="South") # only south walls
# Per-orientation ratios: call once per orientation.
for orientation, ratio in [("North", 0.3), ("South", 0.5), ("East", 0.4), ("West", 0.4)]:
    set_wwr(doc, wwr=ratio, orientation=orientation)
```

`wwr` is a single float in the open interval `(0, 1)`. The existing windows on matched walls are removed; new `FenestrationSurface:Detailed` objects are inserted with the target ratio, centred on each wall.

## Surface matching

`intersect_match()` finds pairs of surfaces that overlap (e.g. interior walls shared between two zones) and sets their `outside_boundary_condition` to `Surface` and `outside_boundary_condition_object` to point at each other:

```python
from idfkit import intersect_match

intersect_match(doc)                       # mutates surfaces in place
# Every shared interior wall now has its boundary linked to the matching surface in the neighbour zone.
```

For ceiling↔floor matching specifically (often what you want for multi-story models), see [geometry-builders-and-zoning.md](geometry-builders-and-zoning.md) for `link_horizontal_surfaces` and `detect_horizontal_adjacencies`.

## 2D polygon utilities

For computing footprint overlaps or differences (e.g. courtyard cut-outs):

```python
from idfkit import (
    polygon_area_2d,
    polygon_contains_2d,
    polygon_intersection_2d,
    polygon_difference_2d,
)

a = [(0, 0), (10, 0), (10, 5), (0, 5)]
b = [(5, 0), (15, 0), (15, 5), (5, 5)]

polygon_area_2d(a)                         # 50.0
polygon_contains_2d(a, (1, 1))             # True
polygon_intersection_2d(a, b)              # overlapping rectangle
polygon_difference_2d(a, b)                # a minus b
```

These take 2D `(x, y)` tuples (not `Vector3D`) because the typical use is on building footprints in plan view.

## Common mistakes

**BAD — manually summing vertex coordinates**

```python
verts = surface._data.get("vertices", [])
# ... bespoke area calculation, easy to get wrong on non-planar inputs
```

**GOOD — `calculate_surface_area`**

```python
calculate_surface_area(surface)
```

**BAD — rotating only `Zone` objects**

```python
for zone in doc["Zone"]:
    zone.direction_of_relative_north = 90.0
# surfaces still have their original vertices; the geometry is now inconsistent.
```

**GOOD — `rotate_building`**

```python
rotate_building(doc, angle_deg=90.0)       # rotates all vertices and zone origins
```

**BAD — passing a dict to `set_wwr`**

```python
set_wwr(doc, wwr={"North": 0.3, "South": 0.5, "East": 0.4, "West": 0.4})  # TypeError
```

**GOOD — call once per orientation**

```python
for orientation, ratio in [("North", 0.3), ("South", 0.5), ("East", 0.4), ("West", 0.4)]:
    set_wwr(doc, wwr=ratio, orientation=orientation)
```

## Related

- [geometry-builders-and-zoning.md](geometry-builders-and-zoning.md) — building footprints and zoning.
- [visualization.md](visualization.md) — render the geometry to confirm what you just edited.
- [thermal-properties.md](thermal-properties.md) — combine geometry with material properties for whole-wall U-values.
- API docs: [py.idfkit.com/api/geometry/](https://py.idfkit.com/api/geometry/)
