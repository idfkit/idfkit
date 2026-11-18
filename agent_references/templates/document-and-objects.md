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
| `doc[obj_type]` | The `IDFCollection` for the type. Type names are case-insensitive, as they are in EnergyPlus, so `doc["zone"]` and `doc["Zone"]` are the same collection. Never raises: an absent or misspelled type gives an empty collection that is detached from the document, so reading a type never inserts it. A name no bundled EnergyPlus release has (a typo, `doc["Zoen"]`) also warns `UnknownObjectTypeWarning`, naming the closest real type. Typed for a literal type name of the document's release, in the schema's spelling (`doc["Zone"]` is `IDFCollection[Zone]`); any other key, a plain `str` variable included, is a type error. |
| `doc.get_collection(obj_type)` | The same operation, typed for dynamic `str` keys: it returns an untyped `IDFCollection[IDFObject]` whatever the name. It delegates to `doc[obj_type]`; there is no behavioural difference. Use it when the name is a variable (`for t in TYPES: doc.get_collection(t)`); for a literal name write `doc["Zone"]`, which is typed and checked. |
| `doc.<attr>` | Typed attribute accessor for any schema type: the `snake_case` plural (`doc.air_loop_hvacs` is `IDFCollection[AirLoopHVAC]`). Hand-written shorthands also resolve and keep their meaning (`doc.building_surfaces` → `BuildingSurface:Detailed`, `doc.ideal_loads` → `ZoneHVAC:IdealLoadsAirSystem`). A typo raises `AttributeError` naming the closest matches. |
| `doc.add(obj_type, name="", **fields)` | Create and insert an object. Returns the new `IDFObject`. Leave `name` empty for a type without a Name field. |
| `doc.<attr>.add("Name", **fields)`, `doc[obj_type].add(...)` | The typed form of `doc.add()`: the same validated object, but the parameters are the type's own (checked by pyright and mypy: the name only for a type with a Name field, the required fields, the others with their schema defaults) and the result is the type's class (`doc.zones.add("Office")` is a `Zone`). The name is positional only, and left out for a type without a Name field: `add(name="Office")` raises `TypeError`. Takes `validate=False` as `doc.add()` does, for unvalidated bulk loading. To add an object you already hold, use `doc.addidfobject(obj)`: `collection.add(obj)` is deprecated (it filed the object in the collection only, unvalidated). |
| `doc.rename(obj_type, old, new)` | Rename + cascade updates through every reference. |
| `doc.removeidfobject(obj)` | Delete an object. |
| `doc.copy()` | Independent deep copy that shares the schema and keeps the preserved formatting of a `preserve_formatting=True` read. The fast way to make an in-process variant. |
| `copy.deepcopy(doc)`, `pickle.dumps(doc)` | Also supported, same result as `doc.copy()` but slower. The schema travels by version, not by content, so a pickled document is small and the unpickled one shares the process-wide schema; this is what hands a document to worker processes (`ProcessPoolExecutor`, joblib). `simulate_batch` uses threads and needs none of this. |
| `doc.all_objects` | Iterator over every object in the model (a property, not a method). |
| `len(doc)` | Total object count. |
| `obj_type in doc` | Does the model hold at least one object of this type? Not whether its release has the type, so a type checker does not narrow the document on it (see [What `"Space" in doc` tells a type checker](#what-space-in-doc-tells-a-type-checker)). |
| `doc.get(...)`, `doc.pop(...)`, `doc.setdefault(...)` | Do not exist: a document is not a `dict`. `doc.update({...})` is the eppy batch update (`"Zone.Office.x_origin"` keys). |

## Adding objects

`doc.add()` is the canonical constructor. Pass field values as keyword arguments using Python snake_case names (`x_origin`, not `"X Origin"`):

```python
--8<-- "agent_references/snippets/document-and-objects.py:add-object"
```

Some types have no Name field: `Output:Meter`, `Output:Variable`, `Output:SQLite`, `Timestep`, `SimulationControl`, `GlobalGeometryRules` and about 160 more. Their first field is a normal field, so pass it by its schema name, never as `name`: `doc.add("Output:Meter", key_name="Electricity:Facility")`, `doc.add("Output:SQLite", option_type="SimpleAndTabular")`. A non-empty name on one of these types raises `InvalidFieldError` naming the field to use, in `add()` (with or without `validate`), on `obj.name = ...` and in the eppy-style `newidfobject`/`copyidfobject`/`addidfobject`, because both writers would drop it. `doc.describe(obj_type).has_name` and `schema.has_name(obj_type)` tell you which kind a type is, and `describe(...).fields` lists the first field of a nameless type (`key_name` for `Output:Meter`). `Output:Table:ReportPeriod` is one of them up to 25.1 (its first field is `name_`) and has a Name field from 25.2.

A keyword that is not a field of the type is refused, never stored, whatever its value: `add()` raises `ValidationFailedError` (code `W003`) by default, and `InvalidFieldError` naming every such key with `validate=False`, which skips value checks but not field names. That includes a spelling an extensible type does not have (`report_1=` on `Output:Table:SummaryReports`; the group is `reports=[{"report_name": ...}]`), a display spelling (`"X Origin"`; use `x_origin`), and `name` passed inside `fields` (pass it as the `name` argument). The groups are checked too, in both modes: a group key the group does not name, or a wrapper value that is not a list of dicts, raises `TypeError`, as `update()` does. Pass a copy of another object's groups (`vertices=wall.vertices.as_list()`), not the live view. `FenestrationSurface:Detailed` has fixed `vertex_N_x_coordinate` fields, not a `vertices` list.

### Typed creation through the collection

`add()` takes the type name and fields as strings, so a type checker checks neither: `doc.add("Zone", "Lab", ceiling_hieght=3.0)` type-checks and fails only when it runs, and the result is a plain `IDFObject`. In type-checked code, add through the collection instead:

```python
--8<-- "agent_references/snippets/document-and-objects.py:typed-collection-add"
```

`doc.zones.add(...)` runs `doc.add("Zone", ...)`, so behaviour, validation errors and reference indexing are the same; the difference is the types. It validates unless passed `validate=False` (keyword-only, a `bool`, after the fields), which skips value, range and required-field checks as `doc.add(..., validate=False)` does but still refuses a key the type does not have (`InvalidFieldError`). The type checker is not relaxed by it: a required field left out is still a type error with `validate=False`. Its parameters come from the class's creation signature, generated from the schema, and an editor's signature help (Pylance, pyright) lists them as `doc.materials.add(` is typed: the name first, positional-only; then the fields the schema requires, with no default (`roughness: Literal[...]`, `thickness: float`, ...); then the others with their schema default (`thermal_absorptance: float | None = 0.9`), or `= ...` where the schema gives none (or one that is not a plain number or string). A shown default is the value EnergyPlus applies to a field left empty: `add()` stores only the fields you pass, so `material.thermal_absorptance` reads `None` until you set it. Leaving out a required field is a type error (`Arguments missing for parameters "roughness", ...`), as it is a `ValidationFailedError` (E001) at run time, and so is passing `None` for one. A type without a Name field takes no name: `doc["Output:SQLite"].add("x")` is a type error naming the parameter `this_type_has_no_name_field` (of type `_PassFieldsAsKeywords`), as it raises `InvalidFieldError`; pass the type's first field as a keyword instead (`doc.output_variables.add(key_value="*", ...)`); a type whose schema requires a name (most) must be given one, and a few (`Building`) default it to `""`. The parameters follow the document's type: through `IDFDocumentV9_4` the fields, value types and required fields are 9.4's, and through `AnyIDFDocument` only fields and values every release accepts, with a field required where any release requires it (so no release refuses a call that type-checks) and a default shown only where every release has it. Where no call suits every release, because a required field was renamed between releases (`People`, `Lights`, `InternalMass`), the signature requires `narrow_with_as_version_first`, which nothing satisfies: the error `Argument missing for parameter "narrow_with_as_version_first"` means narrow the document with `as_version(doc, since=...)` and add through that. A field whose key ends in `_` (`gas_or_gas_mixture_` on `WindowMaterial:Gap`) is offered under that key only. A field whose key is not a Python name (`100_outdoor_air_in_cooling` on `Sizing:System`) cannot be a keyword: set it with `doc.add(...)` or after creation. A collection a type checker cannot narrow (`doc.get_collection(obj_type)`) accepts any name and fields, as `doc.add()` does. Hover and signature help on a typed `add(` show the object type's own documentation rather than a generic one: its schema memo, its EnergyPlus I/O Reference page on docs.idfkit.com, and, where the signature requires `narrow_with_as_version_first`, that note. Per-field docs (units, ranges) are not in the signature help; hover the field on the typed object (`material.thickness`) or use `doc.describe(obj_type)`. Fields are keywords only. A type with no objects yet is read as an empty collection that is not stored in the document, and adding through it stores it, so `zones = doc.zones; zones.add("A")` leaves the zone in `zones`.

Prefer the attribute accessor (`doc.zones`, `doc.output_variables`) or a collection held in a variable when creating many objects in one function: a type checker resolves `doc["Output:Variable"]` through one overload per object type, which costs time for a type listed late in the schema, while an accessor and the collection's `add()` itself cost the same for every type.

## Looking up objects

```python
--8<-- "agent_references/snippets/document-and-objects.py:lookup"
```

Collections support `.first()` (when you know there's a singleton), `.values()`, name-keyed `[name]` access, and `in` membership tests.

Any object type in the schema is also reachable as an attribute, typed like the subscript form: its `snake_case` plural (`doc.zones`), or, for a type a model holds at most one of (`"maxProperties": 1` in the schema: `Building`, `Timestep`, `SimulationControl`, `Output:SQLite`, ...), its singular (`doc.building`, `doc.output_sqlite`). Either way it is the collection, so read a unique object with `.first()` and add through the attribute as for any type. Use the attribute in application code, and `doc["Type:Name"]` when the type name comes from EnergyPlus documentation, an epJSON file or a variable. A misspelling raises `AttributeError` naming the closest matches:

```python
--8<-- "agent_references/snippets/document-and-objects.py:accessors"
```

Names are derived from the schema by rule, so object types added in a new EnergyPlus release are reachable with no change to idfkit. Three types the rule cannot split are named explicitly (`Output:SQLite` is `doc.output_sqlite`, not `doc.output_sq_lite`), and singular nouns ending in `s` get a real plural (`doc.window_material_gases`). Uniqueness is read from each release's schema: a type unique in one release and not in another is singular in the one and plural in the other, so `AnyIDFDocument` declares neither name; use `doc["Type:Name"]` there. The plural of a unique type (`doc.output_sqlites`, `doc.buildings`) still resolves but is deprecated: it raises `DeprecationWarning` at run time and is marked `@deprecated` in the stub, which pyright strict reports as an error. The name of every type, plus the shorthands, is declared in the type stub, so editors complete it and type checkers see `IDFCollection` of the generated class. The same names appear in `dir(doc)` for IPython and Jupyter.

Resolution is strict about separators: `doc.z_o_n_e`, `doc.zone_`, `doc.airloophvacs` and the singular `doc.air_loop_hvac` all raise rather than guess. The raw type name with `_` in place of `:` resolves in any case (`doc.Site_Location`, `doc.ZONE`), as it did before derived names existed, but is untyped. A name owned by a real member wins over any accessor: `doc.version` is the version tuple, and the `Version` object is `doc["Version"]`.

## Typing a document for its EnergyPlus version

The type stubs describe the latest supported release, and every document is typed as one unless you say otherwise: a model's version is read from its file, so a type checker cannot know it. For a model of an older release, state the version with `as_version`, which checks it at run time (`TypeError` if the file is another version) and returns the same document typed for that release. Its object types, field value types and choices, `update()` keywords and accessors are that release's, so editors complete the fields the release has, and a type the release lacks is an error:

```python
--8<-- "agent_references/snippets/document-and-objects.py:versioned"
```

`idfkit.versioned` has one type per supported release, `IDFDocumentV<major>_<minor>` (`IDFDocumentV9_4`, ..., `IDFDocumentV26_2`, which is `IDFDocument`). Annotate a function with `AnyIDFDocument` (from `idfkit.document` or `idfkit.versioned`) to accept a document of any release; through it, a document offers the object types every release has and no object type or field that some release lacks. A field whose value type changed between releases reads as any release's value, since the document can be of any of them, and accepts only a value every release accepts, through assignment and `update()` alike: `heater_fuel_type` reads as `str | None`, `"NaturalGas"` can be written, and `"DistrictHeatingWater"` (rejected by 9.3 to 23.1) and `"Steam"` (rejected from 23.2) cannot. Reaching for something a release lacks is reported against the type that lacks it: on a 9.4 document, pyright reports `doc["Space"]` as `No overloads for "__getitem__"` with `Argument of type "Literal['Space']" cannot be assigned to parameter "obj_type" of type "_NotAnObjectTypeOfEnergyPlus9_4"`. Through `AnyIDFDocument` the type named is `_NotAnObjectTypeOfEveryRelease`, and `doc.spaces` is reported as `Cannot access attribute "spaces" for class "IDFDocumentAllVersions[bool]"`; narrow with `as_version` to use it. mypy reports the lookup as `Invalid index type "str" for "IDFDocumentV9_4[bool]"; expected type "Sequence[_NotAnObjectTypeNameOfEnergyPlus9_4]"`: the `Sequence` is how the stub keeps mypy to that one line, not a hint to pass one. The raw spellings (`doc.Site_Location`) stay an untyped fallback of `IDFDocument` only. idfkit's own functions (`save_idf`, `simulate`, the geometry helpers) take `AnyIDFDocument`, and those that return the document they were given (`expand_objects`, `doc.copy()`) return it with the same type. Field names, value types and `update()` keywords are checked against the release's declaration, as on any typed object (see Modifying objects).

### Which document type to annotate with

| The code works on | Annotate with |
|---|---|
| Models of the latest release (you create them with `new_document()`, or migrated them to it with `migrate(doc, IDFDocument)`) | `IDFDocument` |
| Models of any supported release (a reusable function, a library module) | `AnyIDFDocument`; an object from it as `AnyZone`, `AnyMaterial`, ... |
| Models of one release | `IDFDocumentV9_4` and so on, created with `new_document(IDFDocumentV9_4)` or reached with `as_version` |
| Models of a range of releases (9.6 and later, before 23.2, ...) | `IDFDocumentSince9_6`, `IDFDocumentBefore23_2`, ..., reached with `as_version(doc, since=...)`; a `TypeVar` bound to one returns the caller's type |

### Annotating a parameter with an object class

Every object type of the latest release has two classes to annotate with. `Zone` is the latest release's: a 9.4 zone (`Zone_v8_9_to_v9_4`) and a zone reached through `AnyIDFDocument` are rejected. `AnyZone` is the type as every release that has it declares it, and accepts a zone of any release; through it, fields follow the same rules as through `AnyIDFDocument` (only fields every release has, reads as the union, writes as the intersection), extensible groups included. Every object type has an `Any<Class>`: for a type no release changed it is the latest class itself (`AnyZoneList` is `ZoneList`), so you never need to know which types changed. "Any" is about the object, as in `AnyIDFDocument` it is about the document: `AnySpace` accepts a `Space` of any release that has one (9.6 on, as its docstring says). Such an object is reached only through a document of a release that has the type, so code for any release narrows the document first (`as_version(doc, since="9.6")`, below) and decides what an older model gets; `AnyIDFDocument` itself offers no `Space`.

The classes exist only in the stubs: import them from `idfkit.document` inside `if TYPE_CHECKING:`, with `from __future__ import annotations`. Importing one from `idfkit` instead is reported by recent pyright (`"Zone" is not exported from module "idfkit"`), and importing one outside `TYPE_CHECKING` raises `ImportError` at run time.

```python
--8<-- "agent_references/snippets/document-and-objects.py:typed-object-parameter"
```

An `Any<Class>` covers the releases idfkit supports. When idfkit adopts a release that drops or renames a field, that field leaves `Any<Class>`, and code using it stops type-checking: it would not work on that release either. A type the latest release no longer has, such as `DistrictHeating`, has no `Any<Class>`; annotate with its range class (`DistrictHeating_v8_9_to_v23_1`), imported from `idfkit.versioned` inside `if TYPE_CHECKING:`, since the range classes too exist only in the stubs.

### Reading and writing through `AnyIDFDocument`

Reading a field gives any value some release allows; writing accepts only what every release accepts:

```python
--8<-- "agent_references/snippets/document-and-objects.py:versioned-read-write"
```

### Code for a range of releases

A union of release types accepts exactly those releases. `idfkit.versioned` has one for each range that starts or ends at a release: `IDFDocumentSince9_6` is 9.6 and every later release idfkit supports, `IDFDocumentBefore9_6` every earlier one. Under pyright, a value is accepted only if every release in the union accepts it, by assignment or `update()`; mypy checks `update()` this way but not attribute assignment through a union. Bind a `TypeVar` to the union, so the function returns the caller's own type (unannotated, pyright infers the whole union and mypy infers `Any`):

```python
--8<-- "agent_references/snippets/document-and-objects.py:versioned-range"
```

The annotation is not checked at run time. To narrow a document of unknown release into a range, give `as_version` the range: `since=` the first release (inclusive), `before=` the release it stops before (exclusive), or both. Each bound is a release's number, its document type or its version tuple: `since="9.6"`, `since=IDFDocumentV9_6` and `since=(9, 6, 0)` are the same range. `as_version` returns the document typed as the union of the releases in the range (`IDFDocumentSince9_6` for `since="9.6"`), or raises `TypeError` naming them. pyright and mypy both keep the union exactly. The range is the releases idfkit supports, so it grows when idfkit adds one, and there is no list to keep current. Pass `since=`, not an `IDFDocumentSince9_6` alias: to a type checker an alias is not a class.

A type checker reads a range only from a release's type or a string literal. A bound in a variable (`since=first`), an optional one (`before: str | None`), or a version tuple (`since=doc.version`) is accepted, and types the document as `AnyIDFDocument`; so does a literal no supported release has (`since="27.1"`) or a range with no release in it, both of which raise `ValueError` when the call runs. Name a bound by its release (`"26.2"`, `IDFDocumentV26_2`), not `IDFDocument`: as a bound, `IDFDocument` means the latest release when the code runs, so `since=IDFDocument` stops accepting a 26.2 model once idfkit adopts the next release.

For releases that are not one range, pass `as_version` a tuple of release types, as `isinstance` takes one: `as_version(doc, (IDFDocumentV9_6, IDFDocumentV26_2))` returns the document typed as their union. Under pyright the union is kept exactly; mypy collapses it into what all of the releases share, so lookups still work but a field only those releases have is not offered. Name every release in a tuple by its own type, the latest included: `IDFDocumentV26_2`, not `IDFDocument`. `IDFDocument` stands for whichever release is latest when the code runs. Once idfkit supports a newer release, a tuple that ends in `IDFDocument` no longer covers the release that was latest when it was written, and `as_version` raises `TypeError` on a model of that release. A union written by hand to annotate with has the same flaw (pyright and mypy then reject a model of that release), a flaw the generated `IDFDocumentSince…` aliases do not have.

A narrower range also gives a narrower read type. Through releases that all list a field's choices, the checker can prove a `match` handles every one:

```python
--8<-- "agent_references/snippets/document-and-objects.py:versioned-exhaustive"
```

### A model created for an older release

Pass `new_document` the release's document type: `new_document(IDFDocumentV9_4)` creates a 9.4.0 model typed as `IDFDocumentV9_4`, so the release is named once and the type and the version cannot disagree. For a non-strict model, parametrize the type, `new_document(IDFDocumentV9_4[Literal[False]])`, typed `IDFDocumentV9_4[Literal[False]]`; this form takes no `strict=`. Given a version tuple instead, `new_document` is typed for the latest release whatever the version, so a test fixture built with `new_document(version=(9, 4, 0))` is checked against the wrong release. For the latest release keep `new_document()`: `IDFDocument`, and so the latest release's own type `IDFDocumentV26_2` (which is `IDFDocument`), is refused (`TypeError`, though pyright accepts the call), because it is the run-time class of every document and `new_document(type(doc))` would otherwise create a latest-release model whatever `doc`'s release; `AnyIDFDocument` and unions of release types are refused too (a union, like `IDFDocument`, only when the call runs). A model whose version comes from a file is typed with `as_version`, as above.

```python
--8<-- "agent_references/snippets/document-and-objects.py:versioned-new-document"
```

### A field renamed between releases

`AnyIDFDocument` offers neither name of a renamed field. Branch on `doc.version` and narrow each branch to the releases that use one name, `before=` and `since=` the release that renamed it; each `update()` call is then checked against all of them, under pyright and under mypy (which still rejects the `doc.version` test itself, as below):

```python
--8<-- "agent_references/snippets/document-and-objects.py:versioned-renamed-field"
```

### What `"Space" in doc` tells a type checker

At run time `"Space" in doc` is true when the model holds at least one `Space`. It is false for a release without the type, and equally for a release that has it when the model holds none, so it says nothing about the release, and `doc["Space"]` never raises either way. A type checker therefore leaves the document's type as it was on both sides of the test:

- `if "Space" in doc:` does not make a `Space` lookup legal through `AnyIDFDocument`; `doc["Space"]` stays an error inside it. Branch on `doc.version` and narrow with `as_version` instead.
- `if "Output:SQLite" not in doc:` on a type every release has is an ordinary branch, type-checked like any other: an empty model of any release takes it.
- On a union from `as_version(doc, (A, B, C))`, neither branch of `"Space" in d` drops a member.

```python
--8<-- "agent_references/snippets/document-and-objects.py:versioned-containment"
```

The document types used to be `TypedDict` subclasses to pyright, which narrows those on `in` by its own rules: `"Space" in doc` retyped an `AnyIDFDocument` as the latest release (so a 9.6 or 22.1 model then raised `InvalidFieldError` on `ceiling_height`), and the body of `"Zone" not in doc` was skipped as unreachable.

### Checking: pyright versus `idfkit check`

They catch different mistakes, so code meant for several releases should run both:

- **pyright** (or Pylance, mypy) checks *types*: release-typed lookups (`legacy["Space"]`), attribute reads and assignments (`heater.heater_fuel_type = "Steam"`), `update()` keywords and those of a collection's `add()` (`doc.zones.add(...)`). It cannot see into string-keyed calls: `doc.add("Space", ...)` and its keyword values are untyped, which is why `doc.spaces.add(...)` is the form to use in type-checked code. A misspelled field is reported against `_NotAFieldOfThisObjectType` (`Argument of type "Literal['ceiling_hieght']" cannot be assigned to parameter "key" of type "_NotAFieldOfThisObjectType"`), or as `No parameter named "ceiling_hieght"` in a collection's `add()` or `update()` call.
- **`idfkit check`** lints *string literals* in Python source against the releases you name, with no annotations needed: object type names (rule `C001`, e.g. `doc.add("Space", ...)`, `legacy["Space"]`, `doc.get_collection("Space")`) and choice values in calls (rule `C002`, e.g. `add(..., heater_fuel_type="DistrictHeating")`). An object type, field name or choice value passed to `add()` that no target release accepts, which `add()` raises on, is an error (rule `C006`, with the closest real name: `doc.add("Zoen", "Office")`, `doc.add("Zone", "A", ceiling_hieght=3.0)`, `doc.add("Zone", "A", zone_inside_convection_algorithm="Bogus")`); it is read only in a file that imports idfkit. A field name is read from the keywords and from a dict of fields (`{"ceiling_height": 3.0}`, `fields={...}`), with or without `validate=False` (`add()` refuses an unknown field either way), and accepted as `add()` accepts it: a trailing-underscore field with or without its `_` (`gas_or_gas_mixture`), the extensible wrapper (`vertices=[...]`) and the deprecated flat spellings (`vertex_x_coordinate_2`); it is checked only when every target in scope has the type. `C001` and `C002` report a literal once, naming every release that lacks it (`not found in 8.9.0 to 9.5.0; added in 9.6.0`), and the summary counts findings. An unknown type is reported only on a receiver known to be a document with a schema (`doc = new_document()`, `load_idf(...)`, `as_version(...)`, or a parameter annotated `IDFDocument`, `AnyIDFDocument`, `IDFDocument | None`, ...), since a collection's `add()` takes a name first and a bare `IDFDocument()` accepts any type. A choice value is reported in an `add()` call given more than the type name (so `set.add("x")` is not read), except with `validate=False`, which stores it unchecked; on a collection (`doc["Zone"]`, `doc.zones`, or a name bound to one) it is checked against the collection's type. A document held as `self.building`, `app.window` or `variants["Window"]` is treated as a document, not a collection. It also reads field names in a collection's `add()` (`doc.zones.add("A", ceiling_hieght=3.0)`), which pyright checks too. It does not check attribute assignments, `obj.update(...)`, or a field some targets have and others lack.
- **`get_collection` with a literal name is for `idfkit check`, not pyright.** pyright types it as `IDFCollection[IDFObject]` whatever the name, and checks nothing. `idfkit check`, in a file that imports idfkit, reports a name no target release has (rule `C003`, an error, with the closest real name). At run time a misspelled `get_collection("Zoen")` still returns an empty collection, but warns `idfkit.exceptions.UnknownObjectTypeWarning` with the closest real name (`Did you mean 'Zone'?`), as `doc["Zoen"]`, `doc.idfobjects[...]` and `doc.getobject(...)` do; a name some bundled release has never warns, even one the document's release lacks (`Space` on 9.4), and `"Zoen" in doc` never warns. That covers notebooks and untyped code, which `idfkit check` does not read; to fail on it in tests, run pytest with `-W error::idfkit.exceptions.UnknownObjectTypeWarning`. The opt-in rule `C004` (`--extend-select C004`) also reports every other literal name, suggesting `doc["Zone"]`, which is typed and which pyright checks. Variable names (`doc.get_collection(t)`) are not reported.
- Neither checks item access on an object (`obj["field"]`).

`idfkit check` checks a lookup only against the targets it can run on. It recognises a lookup on `as_version(doc, ...)` (one release type, a tuple or `|` union of them, or `since=`/`before=`), on a name bound once to such a call, and a lookup inside `if doc.version >= (9, 4, 0):` (and the `else` of a test it read completely; `and`, `or`, `not` and chained comparisons against tuples are read). It does not follow early returns, `assert`, `isinstance` or annotations. For a guard it cannot see, silence the line with a comment, which it reports as `C005` once it stops being needed:

```python
if not list(doc.get_collection("Construction:AirBoundary")):  # idfkit: ignore[C001]
    ...
```

Use `# idfkit: ignore[...]`, not `# noqa`: ruff reads `noqa` codes as its own and removes ones it does not know.

To gate CI, put the settings in `pyproject.toml` and run `idfkit check` with no arguments (it exits 1 when it reports anything at or above `fail-on`, 2 on a usage, configuration or syntax error). A pre-commit hook `idfkit-check` reads the same table:

```toml
[tool.idfkit.check]
targets = "all"            # or ["9.4", "26.2"], or since = "9.4" / before = "24.1"
paths = ["src"]
extend-select = ["C004"]
per-file-ignores = { "tests/**" = ["C004"] }
```

```bash
uv run pyright src/
uv run idfkit check                         # settings from [tool.idfkit.check]
uv run idfkit check src/ --since 9.4        # every supported release from 9.4 on
uv run idfkit check src/ --targets all      # --from/--to compares one migration's two releases only
```

mypy sees the document's methods, properties and accessors, but collapses a union of release types into what they share (see Code for a range of releases), and does not check the name of a field that is read (it types `zone.ceiling_hieght` as `object`), so prefer pyright for idfkit code. It reports a misspelled field that is assigned to as `variable has type "_NotAFieldOfThisObjectType"`.

## Reading fields

Reading a field gives its value, or `None` when it is unset. The exception is a field that every release having it requires with no default (`Material.thickness`, `BuildingSurface:Detailed.zone_name`, `Construction.outside_layer`, about 2,700 fields): it reads as its value type, never `None` (`float`, not `float | None`), so arithmetic on it needs no guard. `add()` refuses an object without it, and assigning `None` to it, or passing `None` to `update()`, is a type error. An object can still lack one when it comes from a file EnergyPlus would refuse, or from `doc.add(..., validate=False)`; reading the field then raises `MissingRequiredFieldError`, an `AttributeError` naming the object and the field, instead of returning `None`. To ask whether such a field is set without raising, use `obj.get("thickness")` (or `getattr(obj, "thickness", None)`), and `validate_document(doc)` lists every missing one (`E001`). A field with a schema default reads `None` when blank, not the default: EnergyPlus applies the default, idfkit stores only what was written.

```python
--8<-- "agent_references/snippets/document-and-objects.py:read-required"
```

A blank value is stored as absent wherever it comes from (`add(..., f="")`, `obj.f = ""`, `""` or `null` in epJSON, an empty IDF field), so no field reads `""`, and `""` is not part of any field's type: clear a field with `None` in type-checked code. Choice values are read in the spelling of the file (`"WALL"`, `"hourly"`), which may differ in case from the `Literal` the type lists: compare them with `.casefold()` when the model was loaded from a file.

## Modifying objects

Field access is via attribute. Setting a value re-validates against the schema and updates the reference graph automatically:

```python
--8<-- "agent_references/snippets/document-and-objects.py:modify"
```

Dict-style access also works and accepts either Python or IDD field names — `zone["x_origin"]`, `zone["X Origin"]`, and `zone.x_origin` are all equivalent. Attribute access is the idiomatic form (better IDE autocomplete and type checking). A typed object, such as one from `doc["Lights"]` or `doc.lights`, declares the EnergyPlus 26.2 snake_case names only, and pyright reports any other attribute name, read or assigned. That includes an eppy-style capitalised spelling (`lights.Watts_per_Zone_Floor_Area`) and a field that exists only in an earlier version (`Lights.watts_per_zone_floor_area`, up to 23.2). Both still work at run time; in type-checked code, reach a field missing from 26.2 with item access (`lights["watts_per_zone_floor_area"]`). Objects from `doc.add()`, `doc.get_collection()` and the eppy API are plain `IDFObject` and accept any name; a collection's `add()` (`doc.zones.add(...)`) returns the typed class. A few epJSON keys end in `_` because their IDD name ends in punctuation or a space (`cond_flag_is_the_basement_conditioned_`, `nx_number_of_cells_in_the_x_direction_20_`). At runtime the spelling without the underscore works too, in `add()`, attribute access and `update()`, and is stored under the schema's key; `name` is never such a spelling. The typed `update()` stubs name only the schema's key, so use that key in type-checked code.

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

`ExtensibleList` supports `append`, `insert`, `extend`, `clear`, `pop`, indexing, iteration, and `as_list()`. In type-checked code, a group passed to `add()` or `update()` is a dict typed by the group's item type, a `TypedDict` of the group's fields, all optional: `vertices=[{"vertex_x_coordinate": 0.0, ...}]` takes a sequence of `BuildingSurfaceDetailedVerticesItem`, or of the group objects themselves (`vertices=list(other.vertices)`), so editors complete the keys and a misspelled key or wrong value is a type error. `wall.vertices.as_list()` returns `list[BuildingSurfaceDetailedVerticesItem]`, so a copy passes straight back (`vertices=wall.vertices.as_list()`); its keys are optional, as a blank field is left out, so read one with `.get()`. To build groups ahead of a call, annotate the list with the item type (`points: list[BuildingSurfaceDetailedVerticesItem] = []`, imported from `idfkit.document`); a list typed `list[dict[str, float]]` is not accepted. Each item type is named after its object type and group (`ScheduleWeekCompactDataItem`, `ZoneListZonesItem`).

## Iterating the whole model

```python
--8<-- "agent_references/snippets/document-and-objects.py:iterate"
```

## Common mistakes

!!! failure "guarding a required field against None"

    ```python
    if material.thickness is None:  # pyright strict: reportUnnecessaryComparison; it is a float
        raise ValueError(material.name)
    ```

!!! success "read it; check with get() only when the model may be incomplete"

    ```python
    r = material.thickness / material.conductivity  # raises MissingRequiredFieldError if unset
    if material.get("thickness") is None: ...  # the untyped check, for loaded files
    ```

!!! failure "guarding a release-specific lookup with `in`"

    ```python
    if "Space" in doc:  # true only when the model holds a Space; says nothing about the release
        for space in doc["Space"]:  # a type error through AnyIDFDocument
            space.ceiling_height = 3.0  # 9.6 to 22.1 have Space but not ceiling_height
    ```

!!! success "branch on the release, then narrow"

    ```python
    --8<-- "agent_references/snippets/document-and-objects.py:versioned-containment"
    ```

!!! failure "narrowing with `isinstance(doc, IDFDocument)`"

    ```python
    if isinstance(doc, IDFDocument):  # true for a document of every release at run time
        for space in doc["Space"]:  # pyright now types doc as the latest release here
            space.ceiling_height = 3.0  # raises InvalidFieldError on a 9.6 or 22.1 model
    ```

    `IDFDocument` is the only document class at run time, so every document passes the test, while a type checker narrows to the latest release on it. Use `as_version`, as above.

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
