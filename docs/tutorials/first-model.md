# Build your first model

In this tutorial you'll build a small but complete EnergyPlus model from
nothing — a two-storey office block with zones, walls, windows, and
constructions — and then **run it through EnergyPlus and read a result back**.
Along the way you'll meet the pieces every idfkit project is made of: the
document, objects, references, validation, and the weather and simulation
helpers.

You don't need to understand every line yet. Follow the steps in order, run
each snippet, and watch what happens. By the end you'll have built a model,
simulated it, and pulled a number out of the results.

**You'll need:**

- **idfkit** — `pip install idfkit`
- For the last three steps, **EnergyPlus installed** (8.9 or newer) and a
  **network connection** the first time, so idfkit can download the weather
  data. Steps 1–8 need neither, so you can build and write the whole model
  before installing EnergyPlus.

Work through it in a Python file or a REPL, adding each snippet as you go.

## Step 1 — Start a new document

Everything in idfkit lives in a **document**: the in-memory container for one
EnergyPlus model. Every document is pinned to one EnergyPlus version, because
that version decides which objects and fields are valid. Pin it to the
EnergyPlus you actually have, so the simulation in Step 10 has no version gap to
close:

```python
--8<-- "docs/snippets/tutorials/first-model.py:new"
```

You'll see whichever version idfkit found on your machine:

```
Building for EnergyPlus 26.1.0
```

If you don't have EnergyPlus yet, `find_energyplus()` raises
`EnergyPlusNotFoundError` and the fallback pins the document to
`LATEST_VERSION` instead, so Steps 1–8 still work offline.

!!! note "If you install EnergyPlus later"

    idfkit can migrate a model *forward* to a newer EnergyPlus, but never
    backward, because EnergyPlus ships no reverse transition binaries. So if
    you ran Step 1 with no EnergyPlus and then installed an **older** release,
    re-run Step 1 to re-pin the document before you simulate.

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
block that you built from an empty document. Open it in a text editor and you'll
recognise the zones, surfaces, and constructions you created. But the whole point
of a model is to *run* it, so let's do that next.

## Step 9 — Fetch weather and design days

To simulate, EnergyPlus needs weather data and at least one *design day* — an
extreme day used for sizing. idfkit fetches both for you: it finds the nearest
weather station to a latitude/longitude, downloads its files, and injects a
design day into your model.

```python
--8<-- "docs/snippets/tutorials/first-model.py:weather"
```

```
1
```

idfkit downloaded a weather file and its design-day (`.ddy`) companion for a
station near Chicago, added one `SizingPeriod:DesignDay` — a cold winter sizing
day — and updated the model's `Site:Location` to match. The first run downloads
and caches the files; later runs reuse the cache.

## Step 10 — Run the simulation

Ask EnergyPlus for an output variable so the run has something to report, then
simulate. We run only the design day (`design_day=True`), which takes seconds
rather than the minutes a full-year run needs:

```python
--8<-- "docs/snippets/tutorials/first-model.py:simulate"
```

```
True
```

`result.success` is `True` — EnergyPlus ran and finished cleanly. Passing
`energyplus=config` reuses the installation you already found in Step 1 instead
of searching for it again. `auto_migrate=True` is the safety net: your document
is already pinned to the installed version, so there's normally nothing to
migrate, but if you pinned it to `LATEST_VERSION` back when EnergyPlus wasn't
installed, idfkit forward-migrates it for you here.

## Step 11 — Read a result back

The outputs live in an SQLite database that idfkit reads for you. Count the
variables, then pull the lobby's temperature series:

```python
--8<-- "docs/snippets/tutorials/first-model.py:read"
```

```
10
24
-0.9
```

Ten temperature series came back — one per zone. The lobby's has 24 hourly
values (one design day), and its warmest hour is about **−0.9 °C**. That exact
number will shift a little with your EnergyPlus version and the weather file —
and it's cold on purpose: we never added a heating system, so the unconditioned
shell just tracks the winter design conditions. Giving the zones an HVAC system
is the natural next move — see [How to run a simulation](../simulation/running.md).

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
- **idfkit fetches weather and design days** for you (`StationIndex`,
  `WeatherDownloader`, `DesignDayManager`) — no hand-built sizing periods.
- **`find_energyplus()` locates your EnergyPlus**, and pinning the document to
  its version keeps model and engine in step; `auto_migrate=True` closes the gap
  forward if one opens up.
- **`simulate()` runs EnergyPlus** and **`result.sql`** reads the outputs back.

## Next steps

- [Common tasks](../getting-started/quick-start.md) — the everyday operations
  (loading existing files, querying, running a simulation) as quick recipes.
- [Core Tutorial](../getting-started/core-tutorial.ipynb) — a longer interactive
  walkthrough in a notebook.
- [How-to guides](../how-to/index.md) — goal-oriented recipes once you know what
  you want to do.
