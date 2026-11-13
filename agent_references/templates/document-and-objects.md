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
--8<-- "agent_references/snippets/document-and-objects.py:add-object"
```

Some types have no Name field: `Output:Meter`, `Output:Variable`, `Output:SQLite`, `Timestep`, `SimulationControl`, `GlobalGeometryRules` and about 160 more. Their first field is a normal field, so pass it by its schema name, never as `name`: `doc.add("Output:Meter", key_name="Electricity:Facility")`, `doc.add("Output:SQLite", option_type="SimpleAndTabular")`. A non-empty name on one of these types raises `InvalidFieldError` naming the field to use, in `add()` (with or without `validate`), on `obj.name = ...` and in the eppy-style `newidfobject`/`copyidfobject`/`addidfobject`, because both writers would drop it. `doc.describe(obj_type).has_name` and `schema.has_name(obj_type)` tell you which kind a type is, and `describe(...).fields` lists the first field of a nameless type (`key_name` for `Output:Meter`). `Output:Table:ReportPeriod` is one of them up to 25.1 (its first field is `name_`) and has a Name field from 25.2.

A keyword that is not a field of the type is refused, never stored, whatever its value: `add()` raises `ValidationFailedError` (code `W003`) by default, and `InvalidFieldError` naming every such key with `validate=False`, which skips value checks but not field names. That includes a spelling an extensible type does not have (`report_1=` on `Output:Table:SummaryReports`; the group is `reports=[{"report_name": ...}]`), a display spelling (`"X Origin"`; use `x_origin`), and `name` passed inside `fields` (pass it as the `name` argument). The groups are checked too, in both modes: a group key the group does not name, or a wrapper value that is not a list of dicts, raises `TypeError`, as `update()` does. Pass a copy of another object's groups (`vertices=wall.vertices.as_list()`), not the live view. `FenestrationSurface:Detailed` has fixed `vertex_N_x_coordinate` fields, not a `vertices` list.

## Looking up objects

```python
--8<-- "agent_references/snippets/document-and-objects.py:lookup"
```

Collections support `.first()` (when you know there's a singleton), `.values()`, name-keyed `[name]` access, and `in` membership tests.

Any object type in the schema is also reachable as an attribute: its `snake_case` plural, typed like the subscript form. Use the attribute in application code, and `doc["Type:Name"]` when the type name comes from EnergyPlus documentation, an epJSON file or a variable. A misspelling raises `AttributeError` naming the closest matches:

```python
--8<-- "agent_references/snippets/document-and-objects.py:accessors"
```

Names are derived from the schema by rule, so object types added in a new EnergyPlus release are reachable with no change to idfkit. Three types the rule cannot split are named explicitly (`Output:SQLite` is `doc.output_sqlite`), and singular nouns ending in `s` get a real plural (`doc.window_material_gases`). The plural of every type, plus the shorthands, is declared in the type stub, so editors complete it and type checkers see `IDFCollection` of the generated class. The same names appear in `dir(doc)` for IPython and Jupyter.

Resolution is strict about separators: `doc.z_o_n_e`, `doc.zone_`, `doc.airloophvacs` and the singular `doc.air_loop_hvac` all raise rather than guess. The raw type name with `_` in place of `:` resolves in any case (`doc.Site_Location`, `doc.ZONE`), as it did before derived names existed, but is untyped. A name owned by a real member wins over any accessor: `doc.version` is the version tuple, and the `Version` objects are `doc.versions`.

## Typing a document for its EnergyPlus version

The type stubs describe the latest supported release, and every document is typed as one unless you say otherwise: a model's version is read from its file, so a type checker cannot know it. For a model of an older release, state the version with `as_version`, which checks it at run time (`TypeError` if the file is another version) and returns the same document typed for that release. Its object types, field value types and choices, `update()` keywords and accessors are that release's, so editors complete the fields the release has, and a type the release lacks is an error:

```python
--8<-- "agent_references/snippets/document-and-objects.py:versioned"
```

`idfkit.versioned` has one type per supported release, `IDFDocumentV<major>_<minor>` (`IDFDocumentV9_4`, ..., `IDFDocumentV26_2`, which is `IDFDocument`). Annotate a function with `AnyIDFDocument` (from `idfkit.document` or `idfkit.versioned`) to accept a document of any release; through it, a document offers the object types every release has and no object type or field that some release lacks. A field whose value type changed between releases reads as any release's value, since the document can be of any of them, and accepts only a value every release accepts, through assignment and `update()` alike: `heater_fuel_type` reads as `str | None`, `"NaturalGas"` can be written, and `"DistrictHeatingWater"` (rejected before 23.2) and `"Steam"` (rejected from 23.2) cannot. Reaching for something a release lacks is reported against the type that lacks it: `"Space" is not a defined key in "IDFDocumentV9_4[bool]"`. Through `AnyIDFDocument`, `doc["Space"]` is reported as `"Space" is not a defined key in "IDFDocumentAllVersions[bool]"` and `doc.spaces` as `Cannot access attribute "spaces" for class "IDFDocumentAllVersions[bool]"`; narrow with `as_version` to use it. The raw spellings (`doc.Site_Location`) stay an untyped fallback of `IDFDocument` only. idfkit's own functions (`save_idf`, `simulate`, the geometry helpers) take `AnyIDFDocument`, and those that return the document they were given (`expand_objects`, `doc.copy()`) return it with the same type. Field names, value types and `update()` keywords are checked against the release's declaration, as on any typed object (see Modifying objects).

### Which document type to annotate with

| The code works on | Annotate with |
|---|---|
| Models of the latest release (you create them with `new_document()`, or migrated them to it) | `IDFDocument` |
| Models of any supported release (a reusable function, a library module) | `AnyIDFDocument` |
| Models of one release | `IDFDocumentV9_4` and so on, reached with `as_version` |
| Models of a range of releases (9.6 and later, before 23.2, ...) | a union of release types, with a `TypeVar` to return the caller's type |

### Reading and writing through `AnyIDFDocument`

Reading a field gives any value some release allows; writing accepts only what every release accepts:

```python
--8<-- "agent_references/snippets/document-and-objects.py:versioned-read-write"
```

### Code for a range of releases

A union of release types accepts exactly those releases. Under pyright, a value is accepted only if every release in the union accepts it, by assignment or `update()`; mypy checks `update()` this way but not attribute assignment through a union. Bind a `TypeVar` to the union, so the function returns the caller's own type (unannotated, pyright infers the whole union and mypy infers `Any`):

```python
--8<-- "agent_references/snippets/document-and-objects.py:versioned-range"
```

The annotation is not checked at run time. To narrow a document of unknown release, call `as_version` with one release type; it does not take a union.

A narrower range also gives a narrower read type. Through releases that all list a field's choices, the checker can prove a `match` handles every one:

```python
--8<-- "agent_references/snippets/document-and-objects.py:versioned-exhaustive"
```

### A model created for an older release

`new_document(version=...)` is typed for the latest release, whatever version it is given. Type it for its release with `as_version`, as for a loaded model; a test fixture that skips this is checked against the wrong release:

```python
--8<-- "agent_references/snippets/document-and-objects.py:versioned-new-document"
```

### A field renamed between releases

`AnyIDFDocument` offers neither name of a renamed field. Branch on `doc.version` and type each branch with `as_version`, one release at a time; item access is the unchecked fallback:

```python
--8<-- "agent_references/snippets/document-and-objects.py:versioned-renamed-field"
```

### Checking: pyright versus `idfkit check`

They catch different mistakes, so code meant for several releases should run both:

- **pyright** (or Pylance, mypy) checks *types*: release-typed lookups (`legacy["Space"]`), attribute reads and assignments (`heater.heater_fuel_type = "Steam"`), `update()` keywords. It cannot see into string-keyed calls: `doc.add("Space", ...)` and its keyword values are untyped.
- **`idfkit check`** lints *string literals* in Python source against the releases you name, with no annotations needed: object type names (rule `C001`, e.g. `doc.add("Space", ...)`, `legacy["Space"]`) and choice values in calls (rule `C002`, e.g. `add(..., heater_fuel_type="DistrictHeating")`). It does not check attribute assignments.
- Neither checks `doc.get_collection("Space")` or item access (`obj["field"]`).

```bash
uv run pyright src/
uv run idfkit check --targets 9.4,23.2,26.2 src/my_module.py
```

mypy does not see the document's own methods and properties (it reports `add` and `version` as missing on a document), so prefer pyright for idfkit code.

## Modifying objects

Field access is via attribute. Setting a value re-validates against the schema and updates the reference graph automatically:

```python
--8<-- "agent_references/snippets/document-and-objects.py:modify"
```

Dict-style access also works and accepts either Python or IDD field names — `zone["x_origin"]`, `zone["X Origin"]`, and `zone.x_origin` are all equivalent. Attribute access is the idiomatic form (better IDE autocomplete and type checking). A typed object, such as one from `doc["Lights"]` or `doc.lights`, declares the EnergyPlus 26.2 snake_case names only, and pyright reports any other attribute name, read or assigned. That includes an eppy-style capitalised spelling (`lights.Watts_per_Zone_Floor_Area`) and a field that exists only in an earlier version (`Lights.watts_per_zone_floor_area`, up to 23.2). Both still work at run time; in type-checked code, reach a field missing from 26.2 with item access (`lights["watts_per_zone_floor_area"]`). Objects from `doc.add()`, `doc.get_collection()` and the eppy API are plain `IDFObject` and accept any name. A few epJSON keys end in `_` because their IDD name ends in punctuation or a space (`cond_flag_is_the_basement_conditioned_`, `nx_number_of_cells_in_the_x_direction_20_`). At runtime the spelling without the underscore works too, in `add()`, attribute access and `update()`, and is stored under the schema's key; `name` is never such a spelling. The typed `update()` stubs name only the schema's key, so use that key in type-checked code.

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

## Related

- [parsing-idf-epjson.md](parsing-idf-epjson.md) — turning files on disk into documents.
- [writing-output.md](writing-output.md) — serializing documents back out.
- [reference-tracking.md](reference-tracking.md) — cross-object references and cascading renames.
- [schema-and-validation.md](schema-and-validation.md) — checking a model is well-formed before simulation.
- API docs: [py.idfkit.com/api/document/](https://py.idfkit.com/api/document/)
