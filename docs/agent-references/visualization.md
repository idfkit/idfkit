# Visualization

`idfkit.visualization` renders models in two ways: an interactive 3D viewer (plotly) for whole-building geometry, and an SVG generator for construction cross-sections. Both are pure-Python and require no external CAD tooling.

## When to use

- You want to sanity-check geometry you just synthesised with `create_block`.
- You're debugging a surface normal orientation.
- You want a publication-ready construction cross-section diagram.
- You're embedding in Jupyter and want notebook-native visualisations.

## Quick start

### 3D model view

```python
--8<-- "docs/snippets/agent_references/visualization.py:model-view-quickstart"
```

### Construction cross-section

```python
--8<-- "docs/snippets/agent_references/visualization.py:construction-cross-section"
```

In Jupyter, `wall` displays automatically as the SVG cross-section thanks to `IDFObject._repr_svg_`.

## Core API

```python
--8<-- "docs/snippets/agent_references/visualization.py:core-api"
```

## 3D model views

```python
--8<-- "docs/snippets/agent_references/visualization.py:model-views"
```

`view_model` returns a `plotly.graph_objects.Figure` — call `.show()`, `.write_image()`, or `.write_html()` on it. Requires `idfkit[plotly]`. `ColorBy` members: `ZONE`, `SURFACE_TYPE`, `BOUNDARY_CONDITION`, `CONSTRUCTION`.

## Floor plans and exploded views

```python
--8<-- "docs/snippets/agent_references/visualization.py:floor-plans"
```

`view_floor_plan` is most useful for confirming zoning and core/perimeter splits. `view_exploded` is best for confirming surface ownership and adjacency.

## Normals view (debugging)

```python
--8<-- "docs/snippets/agent_references/visualization.py:normals-view"
```

When you see arrows pointing into the building, you know the surface vertices are in the wrong winding order. Fix the source geometry rather than trying to flip per-surface.

## Construction SVG diagrams

```python
--8<-- "docs/snippets/agent_references/visualization.py:construction-svg"
```

The SVG shows layered materials with proportional thicknesses, material names, and R-values per layer. Each material type gets a distinct fill colour (insulation, glass, gas, opaque mass, …).

For programmatic embedding into other diagrams, the lower-level `generate_construction_svg` returns a `bytes`-ready SVG with no surrounding `<svg>` boilerplate.

## Jupyter integration

`IDFObject` provides `_repr_svg_` for constructions, so just rendering a construction in a notebook cell shows the cross-section:

```python
--8<-- "docs/snippets/agent_references/visualization.py:jupyter-repr"
```

For 3D, `view_model(...)` returns a plotly Figure, which plotly automatically renders in notebooks.

## Workflow: edit-then-verify

```python
--8<-- "docs/snippets/agent_references/visualization.py:workflow"
```

This is the canonical "did I get the geometry right?" loop. Render, look, edit, re-render.

## Common mistakes

**BAD — silently hiding fenestration when you're studying it**

```python
view_model(doc, config=ModelViewConfig(show_fenestration=False)).show()
# Windows hidden — you may miss that south-facing fenestration didn't get applied
```

**GOOD — keep fenestration on for envelope studies**

```python
--8<-- "docs/snippets/agent_references/visualization.py:mistake-fenestration-good"
```

**BAD — `construction_to_svg` on an opaque material**

```python
construction_to_svg(doc["Material"]["XPS_50mm"])   # not a Construction
# TypeError-equivalent: expects a Construction, not a Material
```

**GOOD — operate on `Construction`**

```python
--8<-- "docs/snippets/agent_references/visualization.py:mistake-svg-good"
```

**BAD — large models with no opacity tuning**

```python
view_model(doc).show()                     # rooms hidden behind exterior walls
```

**GOOD — drop opacity for interior visibility**

```python
--8<-- "docs/snippets/agent_references/visualization.py:mistake-opacity-good"
```

## Related

- [geometry-and-surfaces.md](geometry-and-surfaces.md) — what's being rendered.
- [geometry-builders-and-zoning.md](geometry-builders-and-zoning.md) — the typical "create-then-verify" pair.
- [thermal-properties.md](thermal-properties.md) — the R-value annotations in the SVG.
- API docs: [py.idfkit.com/api/visualization/](https://py.idfkit.com/api/visualization/)
