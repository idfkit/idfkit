# Document and objects

The `IDFDocument` is the in-memory representation of an EnergyPlus model. Every workflow — loading, creating, querying, mutating, simulating — starts from a document. This reference covers the four core types you interact with: `IDFDocument`, `IDFCollection`, `IDFObject`, and `ExtensibleList`.

## When to use

- You are loading a model, looking up objects, adding new objects, or modifying existing ones.
- You need to iterate the model by type or by individual object.
- You want O(1) lookups by name (`doc["Zone"]["Office"]`) rather than linear scans.

## Quick start

```python
from idfkit import load_idf, new_document, save_idf

# Create or load
doc = new_document()  # blank model at LATEST_VERSION
doc = load_idf("building.idf")  # from disk

# Add an object — keyword args use Python snake_case field names
zone = doc.add("Zone", "Office", x_origin=0.0, y_origin=0.0, ceiling_height=3.0)

# Look up by type, then by name (both are O(1))
zone = doc["Zone"]["Office"]
print(zone.ceiling_height)  # 3.0

# Mutate fields by attribute
zone.ceiling_height = 3.5

# Persist
save_idf(doc, "out.idf")
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
| `doc.<attr>` | Typed attribute accessor for any schema type: the `snake_case` plural (`doc.air_loop_hvacs` is `IDFCollection[AirLoopHVAC]`). Hand-written shorthands also resolve and keep their meaning (`doc.building_surfaces` → `BuildingSurface:Detailed`, `doc.ideal_loads` → `ZoneHVAC:IdealLoadsAirSystem`). A typo raises `AttributeError` naming the closest matches. |
| `doc.add(obj_type, name="", **fields)` | Create and insert an object. Returns the new `IDFObject`. Leave `name` empty for a type without a Name field. |
| `doc.rename(obj_type, old, new)` | Rename + cascade updates through every reference. |
| `doc.removeidfobject(obj)` | Delete an object. |
| `doc.copy()` | Independent deep copy that shares the schema and keeps the preserved formatting of a `preserve_formatting=True` read. The fast way to make an in-process variant. |
| `copy.deepcopy(doc)`, `pickle.dumps(doc)` | Also supported, same result as `doc.copy()` but slower. The schema travels by version, not by content, so a pickled document is small and the unpickled one shares the process-wide schema; this is what hands a document to worker processes (`ProcessPoolExecutor`, joblib). `simulate_batch` uses threads and needs none of this. |
| `doc.all_objects` | Iterator over every object in the model (a property, not a method). |
| `len(doc)` | Total object count. |
| `obj_type in doc` | Is this type present (and non-empty)? |

## Adding objects

`doc.add()` is the canonical constructor. Pass field values as keyword arguments using Python snake_case names (`x_origin`, not `"X Origin"`):

```python
material = doc.add(
    "Material",
    "XPS_50mm",
    roughness="Rough",
    thickness=0.05,
    conductivity=0.034,
    density=35.0,
    specific_heat=1400.0,
)
```

Some types have no Name field: `Output:Meter`, `Output:Variable`, `Output:SQLite`, `Timestep`, `SimulationControl`, `GlobalGeometryRules` and about 160 more. Their first field is a normal field, so pass it by its schema name, never as `name`: `doc.add("Output:Meter", key_name="Electricity:Facility")`, `doc.add("Output:SQLite", option_type="SimpleAndTabular")`. A non-empty name on one of these types raises `InvalidFieldError` naming the field to use, in `add()` (with or without `validate`), on `obj.name = ...` and in the eppy-style `newidfobject`/`copyidfobject`/`addidfobject`, because both writers would drop it. `doc.describe(obj_type).has_name` and `schema.has_name(obj_type)` tell you which kind a type is, and `describe(...).fields` lists the first field of a nameless type (`key_name` for `Output:Meter`). `Output:Table:ReportPeriod` is one of them up to 25.1 (its first field is `name_`) and has a Name field from 25.2.

A keyword that is not a field of the type is refused, never stored, whatever its value: `add()` raises `ValidationFailedError` (code `W003`) by default, and `InvalidFieldError` naming every such key with `validate=False`, which skips value checks but not field names. That includes a spelling an extensible type does not have (`report_1=` on `Output:Table:SummaryReports`; the group is `reports=[{"report_name": ...}]`), a display spelling (`"X Origin"`; use `x_origin`), and `name` passed inside `fields` (pass it as the `name` argument). The groups are checked too, in both modes: a group key the group does not name, or a wrapper value that is not a list of dicts, raises `TypeError`, as `update()` does. Pass a copy of another object's groups (`vertices=wall.vertices.as_list()`), not the live view. `FenestrationSurface:Detailed` has fixed `vertex_N_x_coordinate` fields, not a `vertices` list.

## Looking up objects

```python
# By type → collection
zones = doc["Zone"]
print(len(zones))  # how many zones

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

Any object type in the schema is also reachable as an attribute: its `snake_case` plural, typed like the subscript form. Use the attribute in application code, and `doc["Type:Name"]` when the type name comes from EnergyPlus documentation, an epJSON file or a variable. A misspelling raises `AttributeError` naming the closest matches:

```python
# Any type in the schema is reachable as a typed attribute, not only common ones.
loops = doc.air_loop_hvacs  # IDFCollection[AirLoopHVAC]
coils = doc.coil_cooling_dx_single_speeds  # Coil:Cooling:DX:SingleSpeed
also_loops = doc["AirLoopHVAC"]  # equivalent
shades = doc.shading_building_detaileds  # Shading:Building:Detailed

# A typo names the closest matches and their object types:
#   >>> doc.shading_bulding
#   AttributeError: 'IDFDocument' object has no attribute 'shading_bulding'.
#   Did you mean:
#     shading_building   (Shading:Building:Detailed)
#     shading_buildings  (Shading:Building)
#     shading_fins       (Shading:Fin)
```

Names are derived from the schema by rule, so object types added in a new EnergyPlus release are reachable with no change to idfkit. Three types the rule cannot split are named explicitly (`Output:SQLite` is `doc.output_sqlite`), and singular nouns ending in `s` get a real plural (`doc.window_material_gases`). The plural of every type, plus the shorthands, is declared in the type stub, so editors complete it and type checkers see `IDFCollection` of the generated class. The same names appear in `dir(doc)` for IPython and Jupyter.

Resolution is strict about separators: `doc.z_o_n_e`, `doc.zone_`, `doc.airloophvacs` and the singular `doc.air_loop_hvac` all raise rather than guess. The raw type name with `_` in place of `:` resolves in any case (`doc.Site_Location`, `doc.ZONE`), as it did before derived names existed, but is untyped. A name owned by a real member wins over any accessor: `doc.version` is the version tuple, and the `Version` objects are `doc.versions`.

## Typing a document for its EnergyPlus version

The type stubs describe the latest supported release, and every document is typed as one unless you say otherwise: a model's version is read from its file, so a type checker cannot know it. For a model of an older release, state the version with `as_version`, which checks it at run time (`TypeError` if the file is another version) and returns the same document typed for that release. Its object types, field value types and choices, `update()` keywords and accessors are that release's, so editors complete the fields the release has, and a type the release lacks is an error:

```python
from idfkit import load_idf
from idfkit.document import AnyIDFDocument
from idfkit.versioned import IDFDocumentV9_4, as_version

legacy = as_version(load_idf("legacy.idf"), IDFDocumentV9_4)  # TypeError unless the file is 9.4
people = legacy["People"]["Office"]
people.update(zone_or_zonelist_name="Office")  # the 9.4 name; 9.6 renamed it, and the new name is an error here


def count_people(doc: AnyIDFDocument) -> int:
    """Accept a document of any supported release."""
    return len(doc["People"])


```

`idfkit.versioned` has one type per supported release, `IDFDocumentV<major>_<minor>` (`IDFDocumentV9_4`, ..., `IDFDocumentV26_2`, which is `IDFDocument`). Annotate a function with `AnyIDFDocument` (import it from `idfkit.document`; importing from `idfkit.versioned` also works but makes the type checker read that module's every-release stub) to accept a document of any release; through it, a document offers the object types every release has, each field typed to admit every release's values, and no field that some release lacks. Reaching for something a release lacks is reported against the type that lacks it: `"Space" is not a defined key in "IDFDocumentV9_4[bool]"`. Through `AnyIDFDocument`, `doc["Space"]` is reported as `"Space" is not a required key in "IDFDocumentAllVersions[bool]", so access may result in runtime exception` and stays typed, and `doc.spaces` as `Cannot access attribute "spaces" for class "IDFDocumentAllVersions[bool]"`; narrow with `as_version` to use it. The raw spellings (`doc.Site_Location`) stay an untyped fallback of `IDFDocument` only. idfkit's own functions (`save_idf`, `simulate`, the geometry helpers) take `AnyIDFDocument`, and those that return the document they were given (`expand_objects`, `doc.copy()`) return it with the same type. As everywhere in idfkit, reading or setting an unknown field name is not a type error (fields resolve at run time); value types and `update()` keywords are checked.

## Modifying objects

Field access is via attribute. Setting a value re-validates against the schema and updates the reference graph automatically:

```python
zone = doc["Zone"]["Office"]
zone.ceiling_height = 3.5  # plain field
zone.direction_of_relative_north = 90.0
```

Dict-style access also works and accepts either Python or IDD field names — `zone["x_origin"]`, `zone["X Origin"]`, and `zone.x_origin` are all equivalent. Attribute access is the idiomatic form (better IDE autocomplete and type checking). A typed object, such as one from `doc["Lights"]` or `doc.lights`, declares the EnergyPlus 26.2 snake_case names only, and pyright reports any other attribute name, read or assigned. That includes an eppy-style capitalised spelling (`lights.Watts_per_Zone_Floor_Area`) and a field that exists only in an earlier version (`Lights.watts_per_zone_floor_area`, up to 23.2). Both still work at run time; in type-checked code, reach a field missing from 26.2 with item access (`lights["watts_per_zone_floor_area"]`). Objects from `doc.add()`, `doc.get_collection()` and the eppy API are plain `IDFObject` and accept any name. A few epJSON keys end in `_` because their IDD name ends in punctuation or a space (`cond_flag_is_the_basement_conditioned_`, `nx_number_of_cells_in_the_x_direction_20_`). At runtime the spelling without the underscore works too, in `add()`, attribute access and `update()`, and is stored under the schema's key; `name` is never such a spelling. The typed `update()` stubs name only the schema's key, so use that key in type-checked code.

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
    "BuildingSurface:Detailed",
    "South Wall",
    surface_type="Wall",
    construction_name="ExtWall",
    zone_name="Office",
    outside_boundary_condition="Outdoors",
)
surface.vertices.append(vertex_x_coordinate=0.0, vertex_y_coordinate=0.0, vertex_z_coordinate=3.0)
surface.vertices.append(vertex_x_coordinate=10.0, vertex_y_coordinate=0.0, vertex_z_coordinate=3.0)
# ...
print(len(surface.vertices))  # 4
```

`ExtensibleList` supports `append`, `insert`, `extend`, `clear`, `pop`, indexing, iteration, and `as_list()`.

## Iterating the whole model

```python
# Every type, in schema-defined order
for obj_type, collection in doc.objects_by_type():
    print(obj_type, len(collection))

# Every individual object
for obj in doc.all_objects:
    if obj.obj_type.startswith("Zone"):
        print(obj.name)
```

## Common mistakes

!!! failure "mutating a list of extensibles in place"

    ```python
    surface._data["vertices"].append({"vertex_x_coordinate": 1.0})  # bypasses validation
    ```

!!! success "use the typed wrapper"

    ```python
    surface.vertices.append(vertex_x_coordinate=1.0, vertex_y_coordinate=0.0, vertex_z_coordinate=3.0)
    ```

!!! failure "renaming via raw string edits"

    ```python
    # Renames the zone but leaves every BuildingSurface:Detailed.zone_name stale
    zone._data["name"] = "OpenPlanArea"
    ```

!!! success "rename through the document"

    ```python
    doc.rename("Zone", "Office", "OpenPlanArea")  # or zone.name = "OpenPlanArea"
    ```

## Related

- [parsing-idf-epjson.md](parsing-idf-epjson.md) — turning files on disk into documents.
- [writing-output.md](writing-output.md) — serializing documents back out.
- [reference-tracking.md](reference-tracking.md) — cross-object references and cascading renames.
- [schema-and-validation.md](schema-and-validation.md) — checking a model is well-formed before simulation.
- API docs: [py.idfkit.com/api/document/](https://py.idfkit.com/api/document/)
