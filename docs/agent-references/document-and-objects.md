# Document and objects

The `IDFDocument` is the in-memory representation of an EnergyPlus model. Every workflow — loading, creating, querying, mutating, simulating — starts from a document. This reference covers the four core types you interact with: `IDFDocument`, `IDFCollection`, `IDFObject`, and `ExtensibleList`.

## When to use

- You are loading a model, looking up objects, adding new objects, or modifying existing ones.
- You need to iterate the model by type or by individual object.
- You want O(1) lookups by name (`doc["Zone"]["Office"]`) rather than linear scans.

## Quick start

```python
--8<-- "docs/snippets/agent_references/document-and-objects.py:quickstart"
```

## Core API

| Symbol | Purpose |
|---|---|
| `new_document(version=LATEST_VERSION)` | Empty model with `Version`, `Building`, `SimulationControl`, `GlobalGeometryRules` seeded. |
| `load_idf(path)` / `load_epjson(path)` | Parse from disk. See [parsing-idf-epjson.md](parsing-idf-epjson.md). |
| `doc.version` | `tuple[int, int, int]` — e.g. `(25, 2, 0)`. |
| `doc.schema` | `EpJSONSchema` for the document's version. |
| `doc[obj_type]` | Returns the `IDFCollection` for the type. Raises `UnknownObjectTypeError` if the type isn't in the schema. |
| `doc.get_collection(obj_type)` | Same as `doc[obj_type]`, but returns an empty collection rather than raising. |
| `doc.<attr>` | Python-name accessors for common types: `doc.zones`, `doc.buildings`, `doc.materials`, `doc.constructions`, `doc.hvac_templates`, etc. |
| `doc.add(obj_type, name=None, **fields)` | Create and insert an object. Returns the new `IDFObject`. |
| `doc.rename(obj_type, old, new)` | Rename + cascade updates through every reference. |
| `doc.removeidfobject(obj)` | Delete an object. |
| `doc.copy()` | Deep copy. |
| `doc.all_objects` | Iterator over every object in the model (a property, not a method). |
| `len(doc)` | Total object count. |
| `obj_type in doc` | Is this type present (and non-empty)? |

## Adding objects

`doc.add()` is the canonical constructor. Pass field values as keyword arguments using Python snake_case names (`x_origin`, not `"X Origin"`):

```python
--8<-- "docs/snippets/agent_references/document-and-objects.py:add-object"
```

Singletons (objects EnergyPlus requires exactly one of, like `Building` or `SimulationControl`) accept a positional name or no name at all; idfkit fills in the type-name where applicable. Objects without a name field (e.g. `GlobalGeometryRules`) accept no name.

## Looking up objects

```python
--8<-- "docs/snippets/agent_references/document-and-objects.py:lookup"
```

Collections support `.first()` (when you know there's a singleton), `.values()`, name-keyed `[name]` access, and `in` membership tests.

## Modifying objects

Field access is via attribute. Setting a value re-validates against the schema and updates the reference graph automatically:

```python
--8<-- "docs/snippets/agent_references/document-and-objects.py:modify"
```

Dict-style access also works and accepts either Python or IDD field names — `zone["x_origin"]`, `zone["X Origin"]`, and `zone.x_origin` are all equivalent. Attribute access is the idiomatic form (better IDE autocomplete and type checking).

Renaming uses `doc.rename()` (or `obj.name = "new"`) so the reference graph cascades the change:

```python
--8<-- "docs/snippets/agent_references/document-and-objects.py:rename"
```

See [reference-tracking.md](reference-tracking.md) for the full reference-graph workflow.

## Extensible fields (repeated groups)

Some object types have repeated field groups — vertices on a surface, branches on a `BranchList`, layers in a `Construction`. idfkit exposes them as `ExtensibleList` accessors:

```python
--8<-- "docs/snippets/agent_references/document-and-objects.py:extensible"
```

`ExtensibleList` supports `append`, `insert`, `extend`, `clear`, `pop`, indexing, iteration, and `as_list()`.

## Iterating the whole model

```python
--8<-- "docs/snippets/agent_references/document-and-objects.py:iterate"
```

## Common mistakes

**BAD — mutating a list of extensibles in place**

```python
surface._data["vertices"].append({"vertex_x_coordinate": 1.0})  # bypasses validation
```

**GOOD — use the typed wrapper**

```python
--8<-- "docs/snippets/agent_references/document-and-objects.py:mistake-extensible-good"
```

**BAD — renaming via raw string edits**

```python
# Renames the zone but leaves every BuildingSurface:Detailed.zone_name stale
zone._data["name"] = "OpenPlanArea"
```

**GOOD — rename through the document**

```python
--8<-- "docs/snippets/agent_references/document-and-objects.py:mistake-rename-good"
```

## Related

- [parsing-idf-epjson.md](parsing-idf-epjson.md) — turning files on disk into documents.
- [writing-output.md](writing-output.md) — serializing documents back out.
- [reference-tracking.md](reference-tracking.md) — cross-object references and cascading renames.
- [schema-and-validation.md](schema-and-validation.md) — checking a model is well-formed before simulation.
- API docs: [py.idfkit.com/api/document/](https://py.idfkit.com/api/document/)
