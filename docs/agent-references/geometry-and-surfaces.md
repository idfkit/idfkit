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
--8<-- "docs/snippets/agent_references/geometry-and-surfaces.py:quickstart"
```

## Core types

### `Vector3D`

```python
--8<-- "docs/snippets/agent_references/geometry-and-surfaces.py:vector3d"
```

### `Polygon3D`

```python
--8<-- "docs/snippets/agent_references/geometry-and-surfaces.py:polygon3d"
```

`Polygon3D` does not expose a "reverse winding" helper — for floor↔ceiling matching, build a new polygon with the vertices in the opposite order (`Polygon3D(list(reversed(poly.vertices)))`).

## Surface calculations

```python
--8<-- "docs/snippets/agent_references/geometry-and-surfaces.py:surface-calculations"
```

Internally these read the vertex list off the surface object and build a `Polygon3D`. To work with the polygon directly:

```python
--8<-- "docs/snippets/agent_references/geometry-and-surfaces.py:surface-coords"
```

## Zone calculations

```python
--8<-- "docs/snippets/agent_references/geometry-and-surfaces.py:zone-calculations"
```

Zone volume is computed from the bounding surfaces — it works for any prismatic and most non-prismatic geometries.

## Building-wide transforms

```python
--8<-- "docs/snippets/agent_references/geometry-and-surfaces.py:transforms"
```

These walk every `BuildingSurface:Detailed`, `Shading:*`, and `FenestrationSurface:Detailed` and transform vertices in place. Zone origins update too.

## Window-to-wall ratio (WWR)

`set_wwr` rewrites fenestration on exterior walls to match a target WWR:

```python
--8<-- "docs/snippets/agent_references/geometry-and-surfaces.py:wwr"
```

`wwr` is a single float in the open interval `(0, 1)`. The existing windows on matched walls are removed; new `FenestrationSurface:Detailed` objects are inserted with the target ratio, centred on each wall.

## Surface matching

`intersect_match()` finds pairs of surfaces that overlap (e.g. interior walls shared between two zones) and sets their `outside_boundary_condition` to `Surface` and `outside_boundary_condition_object` to point at each other:

```python
--8<-- "docs/snippets/agent_references/geometry-and-surfaces.py:intersect-match"
```

For ceiling↔floor matching specifically (often what you want for multi-story models), see [geometry-builders-and-zoning.md](geometry-builders-and-zoning.md) for `link_horizontal_surfaces` and `detect_horizontal_adjacencies`.

## 2D polygon utilities

For computing footprint overlaps or differences (e.g. courtyard cut-outs):

```python
--8<-- "docs/snippets/agent_references/geometry-and-surfaces.py:polygon-2d"
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
--8<-- "docs/snippets/agent_references/geometry-and-surfaces.py:mistake-area-good"
```

**BAD — rotating only `Zone` objects**

```python
for zone in doc["Zone"]:
    zone.direction_of_relative_north = 90.0
# surfaces still have their original vertices; the geometry is now inconsistent.
```

**GOOD — `rotate_building`**

```python
--8<-- "docs/snippets/agent_references/geometry-and-surfaces.py:mistake-rotate-good"
```

**BAD — passing a dict to `set_wwr`**

```python
set_wwr(doc, wwr={"North": 0.3, "South": 0.5, "East": 0.4, "West": 0.4})  # TypeError
```

**GOOD — call once per orientation**

```python
--8<-- "docs/snippets/agent_references/geometry-and-surfaces.py:mistake-wwr-good"
```

## Related

- [geometry-builders-and-zoning.md](geometry-builders-and-zoning.md) — building footprints and zoning.
- [visualization.md](visualization.md) — render the geometry to confirm what you just edited.
- [thermal-properties.md](thermal-properties.md) — combine geometry with material properties for whole-wall U-values.
- API docs: [py.idfkit.com/api/geometry/](https://py.idfkit.com/api/geometry/)
