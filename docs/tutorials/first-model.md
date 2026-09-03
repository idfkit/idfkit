# Build your first model

By the end of this you will have built an EnergyPlus model from nothing,
watched the reference graph rewrite itself when you rename a zone, written the
model to an IDF file, and read it back.

It takes about fifteen minutes, and the code is the same lesson in both
languages. Every step below carries a Python tab and a TypeScript tab that do
the same thing and print the same output, so pick your language once and follow
one column down the page.

## Before you start

You need one of the two libraries and nothing else: no EnergyPlus, no build
step, no schema files to fetch. Both carry every supported EnergyPlus schema,
8.9.0 through 26.1.0, so nothing is downloaded while you work.

Python installs from PyPI with `pip install idfkit`, and [How to install
idfkit](../getting-started/installation.md) covers the extras and the supported
interpreters. The TypeScript packages are not yet published under the shared
`idfkit` install name; until they are, work from a checkout of the [idfkit-js
repository](https://github.com/idfkit/idfkit-js) on Node 20 or newer.

Keep the code in one file as you go, `build_model.py` or `build-model.ts`, and
re-run it after each step. You do not need to know EnergyPlus: where the model
needs a number, this page gives you one.

## Step 1: Create an empty model

Every model is bound to one EnergyPlus version, because field order genuinely
differs between releases. Pinning it is therefore the first thing you do, and
it is the one step where the two libraries ask for different work. Python
resolves the schema from the version you name and seeds the singleton objects
a model cannot do without (`Version`, `Building`, `SimulationControl`, and
`GlobalGeometryRules`). The TypeScript core cannot assume a filesystem, because
the same build has to run in a browser, a worker, and an edge runtime, so you
load the schema yourself, await it, hand it to the constructor, and add
`Version` by hand. `Version` takes `null` where every other object takes a
name, because it has no name field at all.

=== "Python"

    ```python
    --8<-- "docs/snippets/tutorials/first-model.py:create"
    ```

=== "TypeScript"

    ```ts
    --8<-- "docs/snippets/js/tutorials/first-model/step_1_create_an_empty_model.ts:example"
    ```

```
26.1.0
```

That string is the version in the form both libraries agree on. The underlying
value differs: Python's `doc.version` is the tuple `(26, 1, 0)`, which sorts and
compares without a helper, and TypeScript's is the string `'26.1.0'`, which is
what its schema keys already are. `version_string()` renders the Python tuple
into the shared form, and anything crossing between the two languages uses the
string.

## Step 2: Add a zone

A zone is a volume of air EnergyPlus solves for. `add` takes the object type,
the name, and the fields, and hands back the object it created; its fields are
ordinary properties from there on.

=== "Python"

    ```python
    --8<-- "docs/snippets/tutorials/first-model.py:zone"
    ```

=== "TypeScript"

    ```ts
    --8<-- "docs/snippets/js/tutorials/first-model/step_2_add_a_zone.ts:example"
    ```

```
Open Office 2.7
```

Those field names are the epJSON names, spelled exactly as the schema spells
them: `ceiling_height` in both languages, not `ceilingHeight`, and [not the
IDD's `Ceiling Height`](../explanation/epjson-field-names.md). An editor can
complete them, from the shipped stubs in Python and from an opt-in type package
in TypeScript, which is [Static types generated from the
schema](../explanation/generated-types.md).

## Step 3: Add a wall, its construction, and its material

Three objects, each naming the next: the wall names a construction, the
construction names a material. Add them in that order.

=== "Python"

    ```python
    --8<-- "docs/snippets/tutorials/first-model.py:surface"
    ```

=== "TypeScript"

    ```ts
    --8<-- "docs/snippets/js/tutorials/first-model/step_3_add_a_wall_its_construction_and_its_material.ts:example"
    ```

The wall has no shape yet. Its corners live in an *extensible group*, a section
of the object that repeats, which both libraries expose as a live list you add
rows to. Python reaches it under the name of the group, `wall.vertices`;
TypeScript reaches every group under one property, `wall.extensible`.

=== "Python"

    ```python
    --8<-- "docs/snippets/tutorials/first-model.py:vertices"
    ```

=== "TypeScript"

    ```ts
    --8<-- "docs/snippets/js/tutorials/first-model/step_3_add_a_wall_its_construction_and_its_material_2.ts:example"
    ```

```
4
```

That is a 5 m by 2.7 m wall, listed anticlockwise from the top left, which is
the order `GlobalGeometryRules` declares and EnergyPlus expects.

## Step 4: Check that the model hangs together

Validation reads the model against the schema and reports what it finds, one
record per finding. Nothing is raised: you get a result and decide what to do
with it.

=== "Python"

    ```python
    --8<-- "docs/snippets/tutorials/first-model.py:validate"
    ```

=== "TypeScript"

    ```ts
    --8<-- "docs/snippets/js/tutorials/first-model/step_4_check_that_the_model_hangs_together.ts:example"
    ```

```
0
```

No errors means every required field is present and every name the model refers
to actually exists. Change `Exterior Wall` to `Exteriar Wall` on the wall and
run it again: both libraries report one error, coded `E009`, for a reference to
an object that does not exist. Then change it back. The codes are identical in
both languages and the human-readable messages are not, so match on the code.

## Step 5: Rename the zone and watch the references follow

This is the part worth slowing down for. The wall names the zone, so renaming
the zone would normally mean finding and fixing that name everywhere it appears.
Instead, ask the document to do the rename.

=== "Python"

    ```python
    --8<-- "docs/snippets/tutorials/first-model.py:rename"
    ```

=== "TypeScript"

    ```ts
    --8<-- "docs/snippets/js/tutorials/first-model/step_5_rename_the_zone_and_watch_the_references_follow.ts:example"
    ```

```
Open Office
Open Plan
North Wall
```

The wall's `zone_name` changed and you never touched it. Both libraries keep a
live reference graph, so the rename moved an edge in that graph and rewrote
every field anywhere in the model that pointed at the old name. There is no
`update()` to call and no index to rebuild, so there is nothing to forget.

The two spellings differ where each language's receiver differs. Python hangs
the query on the document, `doc.get_referencing(name)`, and returns a set;
TypeScript exposes the graph itself as `doc.references` and hangs the query
there, `doc.references.referencingObjects(name)`, returning an array. Why
TypeScript can do this with real properties rather than a `Proxy` is [Accessors,
not proxies](../explanation/accessors-not-proxies.md).

## Step 6: Write it to an IDF file

Writing is where the two libraries part on shape rather than on vocabulary.
Python's file API is synchronous, so `save_idf` returns when the file is on
disk. The TypeScript core is synchronous and pure so that it can run in a
browser, which pushes everything touching a disk into `@idfkit/core/node`, where
it is awaited: [a synchronous core with async
edges](../explanation/sync-core-async-edge.md). The verb is the same on both
sides.

=== "Python"

    ```python
    --8<-- "docs/snippets/tutorials/first-model.py:save"
    ```

=== "TypeScript"

    ```ts
    --8<-- "docs/snippets/js/tutorials/first-model/step_6_write_it_to_an_idf_file.ts:example"
    ```

Open `office.idf` in a text editor. The zone is there under its new name, and so
is the wall's `Zone Name` field further down. Notice the empty fields you never
set: IDF has no field names, the `!-` markers are comments, and a value's
meaning comes entirely from how many commas precede it. Those blanks hold
positions open, which matters most on the wall, where dropping one would shift
every vertex coordinate into the wrong slot. [The hazards of a positional
format](../explanation/positional-format-hazards.md) is the long version.

## Step 7: Read it back

Parsing detects the version from the file and resolves the matching schema on
its own, so reading takes no more setup than writing did.

=== "Python"

    ```python
    --8<-- "docs/snippets/tutorials/first-model.py:reread"
    ```

=== "TypeScript"

    ```ts
    --8<-- "docs/snippets/js/tutorials/first-model/step_7_read_it_back.ts:example"
    ```

```
26.1.0
Open Plan: ceiling 2.7 m
4
2.7
```

The vertices came back as the same rows you added. Collections are iterable in
both languages, and both offer a lookup that returns nothing on a miss and one
that fails on a miss. The spellings follow each language's habits: Python reads
a collection with the subscript operator, `doc["Zone"]["Open Plan"]`, which
raises `KeyError` when the name is absent, while TypeScript needs a method and
names it for what it does, `doc.require('Zone', 'Open Plan')`. Where you would
rather have the absent value than an error, both spell it `get`.

## What you built

You created a model, connected four objects by name, renamed one and watched the
others follow, wrote real IDF, and parsed it back into the same objects. That is
the whole object model. Everything else is more object types.

It is also the whole shared vocabulary. The names you used are the ones the two
libraries agreed on, and where they differ, they differ because the languages
do: a subscript against a method, a set against an array, a tuple against a
string, a synchronous call against an awaited one. [The naming
map](../explanation/naming-map.md) records every pair and the reason for each
difference.

## Where to go next

- [How-to guides](../how-to/index.md) for the task you actually came here to do.
- [Static types generated from the
  schema](../explanation/generated-types.md), so a misspelled field name becomes
  an editor error rather than a surprise at simulation time.
- Run the model you just built. In Python that is [How to run a
  simulation](../simulation/running.md), which drives a local EnergyPlus
  installation; in TypeScript it is [How to run a simulation in the
  browser](../how-to/run-a-simulation-in-the-browser.md), which runs EnergyPlus
  compiled to WebAssembly.
- [Simulate an office block](office-block.md), the next tutorial, which builds a
  real two-storey block instead of one wall and takes it all the way to a
  heating load. It needs a local EnergyPlus, so it is Python only.
- [What each language has](../explanation/parity.md), before you plan work
  around a capability one of them does not carry yet.
