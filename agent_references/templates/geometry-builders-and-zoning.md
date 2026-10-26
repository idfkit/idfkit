# Geometry builders and zoning

idfkit's `geometry_builders` and `zoning` modules are for **synthesizing** building geometry from scratch — generating footprints, extruding them into multi-story blocks, splitting each floor into zones, and linking adjacent surfaces. This is the layer above `geometry.py` (which is about querying existing geometry — see [geometry-and-surfaces.md](geometry-and-surfaces.md)).

## When to use

- You're building a model from scratch and need a footprint + zones.
- You want to extrude a footprint into a multi-story block with one call.
- You need to link surfaces between adjacent zones or between stacked blocks.
- You need to scale or batch-edit existing geometry.

## Quick start

```python
--8<-- "agent_references/snippets/geometry-builders-and-zoning.py:quickstart"
```

That single call produces zones, floors, ceilings, exterior walls, interior walls, ground/roof boundary conditions, and inter-floor links for an entire 3-story block.

## Footprints

idfkit provides parametric footprint generators that return `list[tuple[float, float]]` in counter-clockwise order:

```python
--8<-- "agent_references/snippets/geometry-builders-and-zoning.py:footprints"
```

Or pass any CCW `list[tuple[float, float]]` you generate yourself.

## Courtyards (footprints with holes)

EnergyPlus surfaces cannot have holes, so a footprint with a courtyard has to become several simple pieces. Use `create_courtyard_block` from `idfkit.zoning`: it subtracts the courtyard polygons from the outer footprint with `polygon_difference_parts_2d`, makes one zone per piece per story (`"<name> Part <k>"`, largest first), and builds the pieces as `CUSTOM` zones of one block, so the walls along the cuts are interior `Surface` walls paired between the pieces' zones, not exterior walls. Courtyards may also touch or cross the outer edge (a notch). `footprint_courtyard_parts` returns the two hole-free halves of a centred rectangular courtyard if you want the polygons themselves:

```python
--8<-- "agent_references/snippets/geometry-builders-and-zoning.py:courtyard"
```

Each piece is concave, so there is no `zoning=` argument: every piece is one zone per story. For a finer split, compute the pieces yourself and pass them (or your own subdivision of them) as `custom_zones` to `create_block` with `ZoningScheme.CUSTOM`; walls whose edges match in reverse become interior walls.

## Zoning schemes

`ZoningScheme` controls how each story is partitioned:

- `BY_STOREY` (default) — one zone per floor.
- `CORE_PERIMETER` — core + 4 perimeter zones per floor. Perimeter depth defaults to `ASHRAE_PERIMETER_DEPTH` (4.57 m).
- `CUSTOM` — caller supplies `ZoneFootprint` polygons for each floor.

```python
--8<-- "agent_references/snippets/geometry-builders-and-zoning.py:zoning-schemes"
```

`create_block` also accepts:

- `air_boundary=True` — apply `Construction:AirBoundary` to all inter-zone walls. Use for open-plan spaces that share air but are still thermally distinct.
- `base_elevation` — ground floor Z (default 0). When > 0, the ground-floor boundary becomes `Outdoors` instead of `Ground`.

## Multi-block buildings (setbacks)

For setback geometries (e.g. a base + tower), call `create_block` twice and link the stacked surfaces:

```python
--8<-- "agent_references/snippets/geometry-builders-and-zoning.py:multi-block"
```

`link_blocks` finds matching ceiling/floor pairs between blocks and sets their boundary conditions to `Surface` pointing at each other.

## Shading blocks

For solar shading from neighbouring structures (not conditioned space):

```python
--8<-- "agent_references/snippets/geometry-builders-and-zoning.py:shading"
```

This adds `Shading:Building:Detailed` surfaces (not zones or interior walls).

## Building-wide edits

```python
--8<-- "agent_references/snippets/geometry-builders-and-zoning.py:building-edits"
```

## Horizontal adjacencies

For multi-story models where floors and ceilings need to be linked to their neighbours above/below:

```python
--8<-- "agent_references/snippets/geometry-builders-and-zoning.py:horizontal-adjacencies"
```

`create_block` calls this automatically for the block it produces; you need to invoke it yourself only when stitching together hand-authored stories.

## Splitting a single surface

When a footprint changes and you want to keep one surface but redraw it:

```python
--8<-- "agent_references/snippets/geometry-builders-and-zoning.py:split-surface"
```

The remainder is always EnergyPlus-safe: no holes and no zero-width slits. When the region sits strictly inside the surface, the remainder would be a frame with a hole, so it is cut into hole-free pieces. The original surface keeps the largest piece, and each other piece becomes a new `"<name> Remainder"` surface that copies its construction, zone and boundary conditions. To get those surfaces back, or to split under several adjacent regions at once (as `link_blocks` does for every floor resting on one roof), use `split_horizontal_surface_by_regions`:

```python
--8<-- "agent_references/snippets/geometry-builders-and-zoning.py:split-surface-regions"
```

## Common mistakes

!!! failure "passing a clockwise footprint"

    ```python
    cw_rect = [(0,0), (0,30), (50,30), (50,0)]  # clockwise
    create_block(doc, "Office", cw_rect, floor_to_floor=3.5, num_stories=1)
    # Surfaces will have inward normals; EnergyPlus thinks the building is inside-out.
    ```

!!! success "counter-clockwise"

    ```python
    --8<-- "agent_references/snippets/geometry-builders-and-zoning.py:mistake-ccw-good"
    ```

!!! failure "relying on `create_block` to add HVAC"

    ```python
    create_block(doc, "Office", rect, floor_to_floor=3.5, num_stories=3,
                 zoning=ZoningScheme.CORE_PERIMETER)
    simulate(doc, "weather.epw")               # zones have no HVAC — uncontrolled
    ```

!!! success "add HVAC explicitly"

    ```python
    --8<-- "agent_references/snippets/geometry-builders-and-zoning.py:mistake-hvac-good"
    ```

See [hvac-templates.md](hvac-templates.md).

!!! failure "the deprecated `footprint_courtyard` slit polygon"

    ```python
    fp = footprint_courtyard(50, 40, 20, 10)  # DeprecationWarning
    create_block(doc, "Office", fp, floor_to_floor=3.5)
    # The ring repeats a vertex and runs out and back along a zero-width slit:
    # two overlapping exterior walls and a self-touching floor. EnergyPlus fails.
    ```

!!! success "`create_courtyard_block`"

    ```python
    --8<-- "agent_references/snippets/geometry-builders-and-zoning.py:mistake-courtyard-good"
    ```

!!! failure "forgetting `link_blocks` between setbacks"

    ```python
    create_block(doc, "Base", base_footprint, floor_to_floor=3.5, num_stories=3)
    create_block(doc, "Tower", tower_footprint, floor_to_floor=3.5, num_stories=8,
                 base_elevation=10.5)
    # Tower floor and base ceiling are both `Outdoors` — heat flows where it shouldn't.
    ```

!!! success "link them"

    ```python
    --8<-- "agent_references/snippets/geometry-builders-and-zoning.py:mistake-link-good"
    ```

## Related

- [geometry-and-surfaces.md](geometry-and-surfaces.md) — calculations on the geometry once it's built.
- [hvac-templates.md](hvac-templates.md) — what to do with the zones you just generated.
- [visualization.md](visualization.md) — render the block to sanity-check it.
- API docs: [py.idfkit.com/api/zoning/](https://py.idfkit.com/api/zoning/) and [py.idfkit.com/api/geometry/](https://py.idfkit.com/api/geometry/)
