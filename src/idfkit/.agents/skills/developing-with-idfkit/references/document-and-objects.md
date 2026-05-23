# Document and objects

The `IDFDocument` is the in-memory representation of an EnergyPlus model. Every workflow — loading, creating, querying, mutating, simulating — starts from a document. This reference covers the four core types you interact with: `IDFDocument`, `IDFCollection`, `IDFObject`, and `ExtensibleList`.

## When to use

- You are loading a model, looking up objects, adding new objects, or modifying existing ones.
- You need to iterate the model by type or by individual object.
- You want O(1) lookups by name (`doc["Zone"]["Office"]`) rather than linear scans.

## Quick start

```python
from idfkit import load_idf, new_document, write_idf

# Create or load
doc = new_document()                       # blank model at LATEST_VERSION
doc = load_idf("building.idf")             # from disk

# Add an object — keyword args use Python snake_case field names
zone = doc.add("Zone", "Office", x_origin=0.0, y_origin=0.0, ceiling_height=3.0)

# Look up by type, then by name (both are O(1))
zone = doc["Zone"]["Office"]
print(zone.ceiling_height)                 # 3.0

# Mutate fields by attribute
zone.ceiling_height = 3.5

# Persist
write_idf(doc, "out.idf")
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
| `doc.all_objects()` | Iterator over every object in the model. |
| `len(doc)` | Total object count. |
| `obj_type in doc` | Is this type present (and non-empty)? |

## Adding objects

`doc.add()` is the canonical constructor. Pass field values as keyword arguments using Python snake_case names (`x_origin`, not `"X Origin"`):

```python
material = doc.add(
    "Material", "XPS_50mm",
    roughness="Rough",
    thickness=0.05,
    conductivity=0.034,
    density=35.0,
    specific_heat=1400.0,
)
```

Singletons (objects EnergyPlus requires exactly one of, like `Building` or `SimulationControl`) accept a positional name or no name at all; idfkit fills in the type-name where applicable. Objects without a name field (e.g. `GlobalGeometryRules`) accept no name.

## Looking up objects

```python
# By type → collection
zones = doc["Zone"]
print(len(zones))                          # how many zones

# Iterate the collection
for zone in zones:
    print(zone.name, zone.x_origin)

# By name → individual object (O(1))
office = doc["Zone"]["Office"]

# Attribute access for common types
for material in doc.materials:
    print(material.conductivity)
```

Collections support `.first()` (when you know there's a singleton), `.values()`, name-keyed `[name]` access, and `in` membership tests.

## Modifying objects

Field access is via attribute. Setting a value re-validates against the schema and updates the reference graph automatically:

```python
zone = doc["Zone"]["Office"]
zone.ceiling_height = 3.5                  # plain field
zone.direction_of_relative_north = 90.0
```

Dict-style access also works and accepts either Python or IDD field names — `zone["x_origin"]`, `zone["X Origin"]`, and `zone.x_origin` are all equivalent. Attribute access is the idiomatic form (better IDE autocomplete and type checking).

Renaming uses `doc.rename()` (or `obj.name = "new"`) so the reference graph cascades the change:

```python
doc.rename("Zone", "Office", "OpenPlanArea")
# every BuildingSurface:Detailed.zone_name pointing at "Office" is now "OpenPlanArea"
```

See [reference-tracking.md](reference-tracking.md) for the full reference-graph workflow.

## Extensible fields (repeated groups)

Some object types have repeated field groups — vertices on a surface, branches on a `BranchList`, layers in a `Construction`. idfkit exposes them as `ExtensibleList` accessors:

```python
surface = doc.add(
    "BuildingSurface:Detailed", "South Wall",
    surface_type="Wall",
    construction_name="ExtWall",
    zone_name="Office",
    outside_boundary_condition="Outdoors",
)
surface.vertices.append(vertex_x_coordinate=0.0, vertex_y_coordinate=0.0, vertex_z_coordinate=3.0)
surface.vertices.append(vertex_x_coordinate=10.0, vertex_y_coordinate=0.0, vertex_z_coordinate=3.0)
# ...
print(len(surface.vertices))               # 4
```

`ExtensibleList` supports `append`, `insert`, `extend`, `clear`, `pop`, indexing, iteration, and `as_list()`.

## Iterating the whole model

```python
# Every type, in schema-defined order
for obj_type, collection in doc.objects_by_type():
    print(obj_type, len(collection))

# Every individual object
for obj in doc.all_objects():
    if obj.obj_type.startswith("Zone"):
        print(obj.name)
```

## Common mistakes

**BAD — mutating a list of extensibles in place**

```python
surface._data["vertices"].append({"vertex_x_coordinate": 1.0})  # bypasses validation
```

**GOOD — use the typed wrapper**

```python
surface.vertices.append(vertex_x_coordinate=1.0, vertex_y_coordinate=0.0, vertex_z_coordinate=3.0)
```

**BAD — renaming via raw string edits**

```python
# Renames the zone but leaves every BuildingSurface:Detailed.zone_name stale
zone._data["name"] = "OpenPlanArea"
```

**GOOD — rename through the document**

```python
doc.rename("Zone", "Office", "OpenPlanArea")   # or zone.name = "OpenPlanArea"
```

## Related

- [parsing-idf-epjson.md](parsing-idf-epjson.md) — turning files on disk into documents.
- [writing-output.md](writing-output.md) — serializing documents back out.
- [reference-tracking.md](reference-tracking.md) — cross-object references and cascading renames.
- [schema-and-validation.md](schema-and-validation.md) — checking a model is well-formed before simulation.
- API docs: [py.idfkit.com/api/document/](https://py.idfkit.com/api/document/)
