# Geometry builders and zoning

idfkit's `geometry_builders` and `zoning` modules are for **synthesizing** building geometry from scratch — generating footprints, extruding them into multi-story blocks, splitting each floor into zones, and linking adjacent surfaces. This is the layer above `geometry.py` (which is about querying existing geometry — see [geometry-and-surfaces.md](geometry-and-surfaces.md)).

## When to use

- You're building a model from scratch and need a footprint + zones.
- You want to extrude a footprint into a multi-story block with one call.
- You need to link surfaces between adjacent zones or between stacked blocks.
- You need to scale or batch-edit existing geometry.

## Quick start

```python
--8<-- "docs/snippets/agent_references/geometry-builders-and-zoning.py:quickstart"
```

That single call produces zones, floors, ceilings, exterior walls, interior walls, ground/roof boundary conditions, and inter-floor links for an entire 3-story block.

## Footprints

idfkit provides parametric footprint generators that return `list[tuple[float, float]]` in counter-clockwise order:

```python
--8<-- "docs/snippets/agent_references/geometry-builders-and-zoning.py:footprints"
```

Or pass any CCW `list[tuple[float, float]]` you generate yourself.

## Zoning schemes

`ZoningScheme` controls how each story is partitioned:

- `BY_STOREY` (default) — one zone per floor.
- `CORE_PERIMETER` — core + 4 perimeter zones per floor. Perimeter depth defaults to `ASHRAE_PERIMETER_DEPTH` (4.57 m).
- `CUSTOM` — caller supplies `ZoneFootprint` polygons for each floor.

```python
--8<-- "docs/snippets/agent_references/geometry-builders-and-zoning.py:zoning-schemes"
```

`create_block` also accepts:

- `air_boundary=True` — apply `Construction:AirBoundary` to all inter-zone walls. Use for open-plan spaces that share air but are still thermally distinct.
- `base_elevation` — ground floor Z (default 0). When > 0, the ground-floor boundary becomes `Outdoors` instead of `Ground`.

## Multi-block buildings (setbacks)

For setback geometries (e.g. a base + tower), call `create_block` twice and link the stacked surfaces:

```python
--8<-- "docs/snippets/agent_references/geometry-builders-and-zoning.py:multi-block"
```

`link_blocks` finds matching ceiling/floor pairs between blocks and sets their boundary conditions to `Surface` pointing at each other.

## Shading blocks

For solar shading from neighbouring structures (not conditioned space):

```python
--8<-- "docs/snippets/agent_references/geometry-builders-and-zoning.py:shading"
```

This adds `Shading:Building:Detailed` surfaces (not zones or interior walls).

## Building-wide edits

```python
--8<-- "docs/snippets/agent_references/geometry-builders-and-zoning.py:building-edits"
```

## Horizontal adjacencies

For multi-story models where floors and ceilings need to be linked to their neighbours above/below:

```python
--8<-- "docs/snippets/agent_references/geometry-builders-and-zoning.py:horizontal-adjacencies"
```

`create_block` calls this automatically for the block it produces; you need to invoke it yourself only when stitching together hand-authored stories.

## Splitting a single surface

When a footprint changes and you want to keep one surface but redraw it:

```python
--8<-- "docs/snippets/agent_references/geometry-builders-and-zoning.py:split-surface"
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
--8<-- "docs/snippets/agent_references/geometry-builders-and-zoning.py:mistake-ccw-good"
```

**BAD — relying on `create_block` to add HVAC**

```python
create_block(doc, "Office", rect, floor_to_floor=3.5, num_stories=3,
             zoning=ZoningScheme.CORE_PERIMETER)
simulate(doc, "weather.epw")               # zones have no HVAC — uncontrolled
```

**GOOD — add HVAC explicitly**

```python
--8<-- "docs/snippets/agent_references/geometry-builders-and-zoning.py:mistake-hvac-good"
```

See [hvac-templates.md](hvac-templates.md).

**BAD — forgetting `link_blocks` between setbacks**

```python
create_block(doc, "Base", base_footprint, floor_to_floor=3.5, num_stories=3)
create_block(doc, "Tower", tower_footprint, floor_to_floor=3.5, num_stories=8,
             base_elevation=10.5)
# Tower floor and base ceiling are both `Outdoors` — heat flows where it shouldn't.
```

**GOOD — link them**

```python
--8<-- "docs/snippets/agent_references/geometry-builders-and-zoning.py:mistake-link-good"
```

## Related

- [geometry-and-surfaces.md](geometry-and-surfaces.md) — calculations on the geometry once it's built.
- [hvac-templates.md](hvac-templates.md) — what to do with the zones you just generated.
- [visualization.md](visualization.md) — render the block to sanity-check it.
- API docs: [py.idfkit.com/api/zoning/](https://py.idfkit.com/api/zoning/) and [py.idfkit.com/api/geometry/](https://py.idfkit.com/api/geometry/)
