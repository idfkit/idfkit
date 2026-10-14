# Document and objects

The `IDFDocument` is the in-memory representation of an EnergyPlus model. Every workflow — loading, creating, querying, mutating, simulating — starts from a document. This reference covers the four core types you interact with: `IDFDocument`, `IDFCollection`, `IDFObject`, and `ExtensibleList`.

## When to use

- You are loading a model, looking up objects, adding new objects, or modifying existing ones.
- You need to iterate the model by type or by individual object.
- You want O(1) lookups by name (`doc["Zone"]["Office"]`) rather than linear scans.

## Quick start

```python
--8<-- "agent_references/snippets/document-and-objects.py:quickstart"
```

## Core API

| Symbol | Purpose |
|---|---|
| `new_document(version=LATEST_VERSION)` | Empty model with `Version`, `Building`, `SimulationControl`, `GlobalGeometryRules` seeded. |
| `load_idf(path)` / `load_epjson(path)` | Parse from disk. See [parsing-idf-epjson.md](parsing-idf-epjson.md). |
| `doc.version` | `tuple[int, int, int]` — e.g. `(25, 2, 0)`. |
| `doc.schema` | `EpJSONSchema` for the document's version. |
| `doc[obj_type]` | The `IDFCollection` for the type. Type names are case-insensitive, as they are in EnergyPlus, so `doc["zone"]` and `doc["Zone"]` are the same collection. Never raises: an absent or misspelled type gives an empty collection that is detached from the document, so reading a type never inserts it. |
| `doc.get_collection(obj_type)` | The same operation, typed for dynamic `str` keys. It delegates to `doc[obj_type]`; there is no behavioural difference. |
| `doc.<attr>` | Attribute accessor for any schema type: the `snake_case` plural (`doc.air_loop_hvacs`), singular (`doc.air_loop_hvac`), or raw name (`doc.AirLoopHVAC`, case-insensitive). Hand-written shorthands also resolve (`doc.building_surfaces` → `BuildingSurface:Detailed`, `doc.ideal_loads` → `ZoneHVAC:IdealLoadsAirSystem`), but a name derived from the schema always wins over a shorthand. A typo raises `AttributeError` naming the closest matches. |
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
--8<-- "agent_references/snippets/document-and-objects.py:add-object"
```

Singletons (objects EnergyPlus requires exactly one of, like `Building` or `SimulationControl`) accept a positional name or no name at all; idfkit fills in the type-name where applicable. Objects without a name field (e.g. `GlobalGeometryRules`) accept no name.

## Looking up objects

```python
--8<-- "agent_references/snippets/document-and-objects.py:lookup"
```

Collections support `.first()` (when you know there's a singleton), `.values()`, name-keyed `[name]` access, and `in` membership tests.

Any object type in the schema is also reachable as an attribute — its `snake_case` plural, its singular, or the raw type name. English pluralisation of these names is ambiguous (`Lights` is already plural, `InternalMass` is not), so all three forms resolve and only the canonical spelling shown in errors is fixed. A misspelling raises `AttributeError` naming the closest matches:

```python
--8<-- "agent_references/snippets/document-and-objects.py:accessors"
```

Names are derived from the schema by rule, so object types added in a new EnergyPlus release are reachable with no change to idfkit. Three types the rule cannot split are named explicitly (`Output:SQLite` is `doc.output_sqlite`), and singular nouns ending in `s` get a real plural (`doc.window_material_gases`). The canonical plural of every type, plus the shorthands, appears in `dir(doc)` and in IPython, Jupyter, and editor tab completion. Static type checkers type these accessors as `IDFCollection[IDFObject]`.

Resolution is strict about separators: `doc.z_o_n_e`, `doc.zone_`, and `doc.airloophvacs` all raise rather than guess. Case is loose only for the raw type name, matching `doc["ZONE"]`, and the raw name may use `_` in place of `:` (`doc.Site_Location`). A name owned by a real member wins over any accessor: `doc.version` is the version tuple, and the `Version` objects are `doc.versions`.

## Modifying objects

Field access is via attribute. Setting a value re-validates against the schema and updates the reference graph automatically:

```python
--8<-- "agent_references/snippets/document-and-objects.py:modify"
```

Dict-style access also works and accepts either Python or IDD field names — `zone["x_origin"]`, `zone["X Origin"]`, and `zone.x_origin` are all equivalent. Attribute access is the idiomatic form (better IDE autocomplete and type checking).

Renaming uses `doc.rename()` (or `obj.name = "new"`) so the reference graph cascades the change:

```python
--8<-- "agent_references/snippets/document-and-objects.py:rename"
```

See [reference-tracking.md](reference-tracking.md) for the full reference-graph workflow.

## Extensible fields (repeated groups)

Some object types have repeated field groups — vertices on a surface, branches on a `BranchList`, layers in a `Construction`. idfkit exposes them as `ExtensibleList` accessors:

```python
--8<-- "agent_references/snippets/document-and-objects.py:extensible"
```

`ExtensibleList` supports `append`, `insert`, `extend`, `clear`, `pop`, indexing, iteration, and `as_list()`.

## Iterating the whole model

```python
--8<-- "agent_references/snippets/document-and-objects.py:iterate"
```

## Common mistakes

!!! failure "mutating a list of extensibles in place"

    ```python
    surface._data["vertices"].append({"vertex_x_coordinate": 1.0})  # bypasses validation
    ```

!!! success "use the typed wrapper"

    ```python
    --8<-- "agent_references/snippets/document-and-objects.py:mistake-extensible-good"
    ```

!!! failure "renaming via raw string edits"

    ```python
    # Renames the zone but leaves every BuildingSurface:Detailed.zone_name stale
    zone._data["name"] = "OpenPlanArea"
    ```

!!! success "rename through the document"

    ```python
    --8<-- "agent_references/snippets/document-and-objects.py:mistake-rename-good"
    ```

!!! failure "expecting `shading_building` to mean the detailed type"

    ```python
    # Earlier idfkit releases returned Shading:Building:Detailed for this shorthand.
    # It now returns Shading:Building, matching doc.shading_buildings.
    for shade in doc.shading_building:
        print(shade.vertices)  # wrong type: Shading:Building has no vertices
    ```

!!! success "name the detailed type explicitly"

    ```python
    --8<-- "agent_references/snippets/document-and-objects.py:mistake-shading-good"
    ```

## Related

- [parsing-idf-epjson.md](parsing-idf-epjson.md) — turning files on disk into documents.
- [writing-output.md](writing-output.md) — serializing documents back out.
- [reference-tracking.md](reference-tracking.md) — cross-object references and cascading renames.
- [schema-and-validation.md](schema-and-validation.md) — checking a model is well-formed before simulation.
- API docs: [py.idfkit.com/api/document/](https://py.idfkit.com/api/document/)
