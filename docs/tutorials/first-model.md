# Build your first model

In this tutorial you'll build a small but complete EnergyPlus model from
nothing — a two-storey office block with zones, walls, windows, and
constructions — and write it out as an `.idf` file you could hand straight to
EnergyPlus. Along the way you'll meet the pieces every idfkit project is made
of: the document, objects, references, and validation.

You don't need to understand every line yet. Follow the steps in order, run
each snippet, and watch what happens. By the end you'll have a valid model on
disk and a feel for how idfkit fits together.

**You'll need:** idfkit installed (`pip install idfkit`). That's it — this
tutorial builds and writes a model, so no EnergyPlus installation is required.

Work through it in a Python file or a REPL, adding each snippet as you go.

## Step 1 — Start a new document

Everything in idfkit lives in a **document**: the in-memory container for one
EnergyPlus model. Create an empty one, pinned to a specific EnergyPlus version:

```python
--8<-- "docs/snippets/tutorials/first-model.py:new"
```

You'll see the version you asked for:

```
(24, 1, 0)
```

The document already holds a few required singleton objects (a `Building`, the
geometry rules, and so on), pre-seeded so the model is well-formed from the
start. You'll add the interesting parts next.

## Step 2 — Generate the building geometry

You *could* place every wall by hand, but idfkit ships high-level **builders**
that turn a footprint into a fully-zoned block. Give one a rectangle, a
floor-to-floor height, and a storey count, and ask it to split each floor into a
core and four perimeter zones:

```python
--8<-- "docs/snippets/tutorials/first-model.py:block"
```

The builder created ten zones (five per storey) and sixty surfaces:

```
10
60
```

`doc["Zone"]` is a name-indexed collection of every `Zone` object in the model,
and `len()` tells you how many there are. Your office now has a shape.

## Step 3 — Define constructions

Those surfaces reference *constructions* that don't exist yet. A construction is
a stack of material layers, so first add a `Material`, then a `Construction`
that uses it — and do the same for the glazing your windows will need:

```python
--8<-- "docs/snippets/tutorials/first-model.py:constructions"
```

`doc.add(type, name, **fields)` is how you create any object. Field names are
the EnergyPlus fields in `snake_case` (`specific_heat`, `outside_layer`), and
the value you pass for `outside_layer` is the *name* of the material — idfkit
records that as a reference from the construction to the material.

## Step 4 — Add windows and assign constructions

Punch windows into the exterior walls at a 40% window-to-wall ratio, then give
every remaining surface the opaque wall construction:

```python
--8<-- "docs/snippets/tutorials/first-model.py:windows"
```

```
8
60
```

`set_wwr()` returns the eight window objects it created, and
`set_default_constructions()` reports the sixty opaque surfaces it just filled
in. Notice the order: the windows claimed the glazing construction first, so the
fill step only touched the surfaces that still lacked one.

## Step 5 — Look at what you built

Objects are looked up by name in O(1), and you read their fields as attributes:

```python
--8<-- "docs/snippets/tutorials/first-model.py:inspect"
```

```
Office Story 1 Perimeter_South
```

`.first()` grabs any one zone from the collection so you can inspect it.

## Step 6 — Rename, and watch references follow

Here's the idfkit feature you'll come to rely on. Six surfaces name this zone as
the space they bound. Rename the zone, and every one of those references updates
itself — no dangling names left behind:

```python
--8<-- "docs/snippets/tutorials/first-model.py:rename"
```

```
6
0
6
```

Before the rename, six objects referenced the old name. After it, the old name
is referenced by nothing, and the new name is referenced by exactly those same
six. idfkit tracks every cross-object reference and rewrites them for you when
you `rename()`.

## Step 7 — Validate the model

Before writing the model out, ask idfkit to check it against the EnergyPlus
schema:

```python
--8<-- "docs/snippets/tutorials/first-model.py:validate"
```

```
True
0
```

A clean bill of health: every reference resolves and every required field is
present. (Try commenting out Step 3 and re-running — you'll see validation
report the surfaces pointing at a construction that doesn't exist.)

## Step 8 — Write it to disk

Finally, serialise the document to an EnergyPlus IDF file:

```python
--8<-- "docs/snippets/tutorials/first-model.py:write"
```

You now have an `office.idf` on disk — a valid, two-storey, windowed office
block that you built from an empty document in eight steps. Open it in a text
editor and you'll recognise the zones, surfaces, and constructions you created.

## What you learned

- A **document** holds one model; **objects** are added with
  `doc.add(...)` and looked up by name.
- **Builders** like `create_block()` and `set_wwr()` generate correct geometry
  so you don't place vertices by hand.
- **Constructions reference materials**, and **surfaces reference constructions
  and zones** — and idfkit keeps those references consistent, even across a
  `rename()`.
- **`validate_document()`** checks the whole model against the schema before you
  write it.

## Next steps

- [Common tasks](../getting-started/quick-start.md) — the everyday operations
  (loading existing files, querying, running a simulation) as quick recipes.
- [Core Tutorial](../getting-started/core-tutorial.ipynb) — a longer interactive
  walkthrough in a notebook.
- [How-to guides](../how-to/index.md) — goal-oriented recipes once you know what
  you want to do.
