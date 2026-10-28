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
--8<-- "agent_references/snippets/geometry-and-surfaces.py:quickstart"
```

## Core types

### `Vector3D`

```python
--8<-- "agent_references/snippets/geometry-and-surfaces.py:vector3d"
```

### `Polygon3D`

```python
--8<-- "agent_references/snippets/geometry-and-surfaces.py:polygon3d"
```

`Polygon3D` does not expose a "reverse winding" helper — for floor↔ceiling matching, build a new polygon with the vertices in the opposite order (`Polygon3D(list(reversed(poly.vertices)))`).

## Surface calculations

```python
--8<-- "agent_references/snippets/geometry-and-surfaces.py:surface-calculations"
```

Internally these read the vertex list off the surface object and build a `Polygon3D`. To work with the polygon directly:

```python
--8<-- "agent_references/snippets/geometry-and-surfaces.py:surface-coords"
```

## Zone calculations

```python
--8<-- "agent_references/snippets/geometry-and-surfaces.py:zone-calculations"
```

Zone volume is computed from the bounding surfaces — it works for any prismatic and most non-prismatic geometries.

## Building-wide transforms

```python
--8<-- "agent_references/snippets/geometry-and-surfaces.py:transforms"
```

These walk every `BuildingSurface:Detailed`, `Shading:*`, and `FenestrationSurface:Detailed` and transform vertices in place. Zone origins update too.

## Window-to-wall ratio (WWR)

`set_wwr` rewrites fenestration on exterior walls to match a target WWR:

```python
--8<-- "agent_references/snippets/geometry-and-surfaces.py:wwr"
```

`wwr` is a single float in the open interval `(0, 1)`. The existing windows on matched walls are removed; new `FenestrationSurface:Detailed` objects are inserted with the target ratio, centred on each wall.

## Surface matching

`intersect_and_match()` finds coplanar, oppositely-facing surfaces from adjacent zones that overlap and **splits** them as needed into congruent matched fragments (interior `Surface` boundary, cross-referenced) plus exterior remainders. A single long wall shared with several smaller neighbouring zones is split into one matched fragment per neighbour. It works for walls and horizontal floor/ceiling pairs alike, returns a typed `MatchReport`, and accepts a `MatchOptions` for tuning tolerances and scope. Detailed windows are re-homed onto the fragment that contains them; a window straddling a cut leaves that surface unsplit and is recorded in `report.fenestration_conflicts` (never silently clipped). `intersect_match()` is a void-returning shorthand that runs it with default options.

```python
--8<-- "agent_references/snippets/geometry-and-surfaces.py:intersect-match"
```

For higher-level ceiling↔floor helpers, see [geometry-builders-and-zoning.md](geometry-builders-and-zoning.md) for `link_horizontal_surfaces` and `detect_horizontal_adjacencies`.

## 2D polygon utilities

For computing footprint overlaps or differences (e.g. corner cut-outs):

```python
--8<-- "agent_references/snippets/geometry-and-surfaces.py:polygon-2d"
```

These take 2D `(x, y)` tuples (not `Vector3D`) because the typical use is on building footprints in plan view.

`polygon_difference_2d` returns one clean, counter-clockwise, simple polygon with no duplicate or coincident vertices, ready for `create_block`. The subtracted polygon may cross the outer boundary, sit flush with a corner, or extend outside it. A single ring cannot describe a result with a hole (the subtracted polygon strictly inside) or a result in several pieces, so `polygon_difference_2d` raises `ValueError` for those. Use `polygon_difference_parts_2d` from `idfkit.geometry` there. It subtracts any number of polygons and returns hole-free pieces, largest first, each one a valid EnergyPlus surface outline or `create_block` footprint. Building each piece with its own `create_block` call leaves the walls along the cuts as exterior walls; `create_courtyard_block` (in `idfkit.zoning`) builds the pieces as zones of one block so those walls are paired interior walls:

```python
--8<-- "agent_references/snippets/geometry-and-surfaces.py:polygon-difference-parts"
```

To cut a concave outline into triangles (for a mesh, or for area-weighted sampling), use `triangulate_2d` from `idfkit.geometry`. It returns index triples into the input, in the input's winding, and it handles keyhole outlines whose bridge vertices are doubled:

```python
--8<-- "agent_references/snippets/geometry-and-surfaces.py:triangulate-2d"
```

## Common mistakes

!!! failure "stitching a hole into one polygon with a slit"

    ```python
    # Joining the outer ring and the hole ring with a zero-width "bridge" edge
    # gives coincident vertices, so create_block makes degenerate surfaces and EnergyPlus fatals.
    slit = [*outer, outer[0], hole[0], *reversed(hole), hole[0]]
    create_block(doc, "Block", slit, floor_to_floor=3.5)
    ```

!!! success "split it into hole-free pieces in one block"

    ```python
    --8<-- "agent_references/snippets/geometry-and-surfaces.py:mistake-hole-good"
    ```

!!! failure "manually summing vertex coordinates"

    ```python
    verts = surface._data.get("vertices", [])
    # ... bespoke area calculation, easy to get wrong on non-planar inputs
    ```

!!! success "`calculate_surface_area`"

    ```python
    --8<-- "agent_references/snippets/geometry-and-surfaces.py:mistake-area-good"
    ```

!!! failure "rotating only `Zone` objects"

    ```python
    for zone in doc["Zone"]:
        zone.direction_of_relative_north = 90.0
    # surfaces still have their original vertices; the geometry is now inconsistent.
    ```

!!! success "`rotate_building`"

    ```python
    --8<-- "agent_references/snippets/geometry-and-surfaces.py:mistake-rotate-good"
    ```

!!! failure "passing a dict to `set_wwr`"

    ```python
    set_wwr(doc, wwr={"North": 0.3, "South": 0.5, "East": 0.4, "West": 0.4})  # TypeError
    ```

!!! success "call once per orientation"

    ```python
    --8<-- "agent_references/snippets/geometry-and-surfaces.py:mistake-wwr-good"
    ```

## Related

- [geometry-builders-and-zoning.md](geometry-builders-and-zoning.md) — building footprints and zoning.
- [visualization.md](visualization.md) — render the geometry to confirm what you just edited.
- [thermal-properties.md](thermal-properties.md) — combine geometry with material properties for whole-wall U-values.
- API docs: [py.idfkit.com/api/geometry/](https://py.idfkit.com/api/geometry/)
