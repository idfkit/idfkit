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
| `doc[obj_type]` | The `IDFCollection` for the type. Type names are case-insensitive, as they are in EnergyPlus, so `doc["zone"]` and `doc["Zone"]` are the same collection. Never raises: an absent or misspelled type gives an empty collection that is detached from the document, so reading a type never inserts it. Typed for a literal type name of the document's release, in the schema's spelling (`doc["Zone"]` is `IDFCollection[Zone]`); any other key, a plain `str` variable included, is a type error. |
| `doc.get_collection(obj_type)` | The same operation, typed for dynamic `str` keys: it returns an untyped `IDFCollection[IDFObject]` whatever the name. It delegates to `doc[obj_type]`; there is no behavioural difference. Use it when the name is a variable (`for t in TYPES: doc.get_collection(t)`); for a literal name write `doc["Zone"]`, which is typed and checked. |
| `doc.<attr>` | Typed attribute accessor for any schema type: the `snake_case` plural (`doc.air_loop_hvacs` is `IDFCollection[AirLoopHVAC]`). Hand-written shorthands also resolve and keep their meaning (`doc.building_surfaces` → `BuildingSurface:Detailed`, `doc.ideal_loads` → `ZoneHVAC:IdealLoadsAirSystem`). A typo raises `AttributeError` naming the closest matches. |
| `doc.add(obj_type, name="", **fields)` | Create and insert an object. Returns the new `IDFObject`. Leave `name` empty for a type without a Name field. |
| `doc.<attr>.add("Name", **fields)`, `doc[obj_type].add(...)` | The typed form of `doc.add()`: the same validated object, but the parameters are the type's own (checked by pyright and mypy: the name only for a type with a Name field, the required fields, the others with their schema defaults) and the result is the type's class (`doc.zones.add("Office")` is a `Zone`). The name is positional only, and left out for a type without a Name field: `add(name="Office")` raises `TypeError`. Always validates; use `doc.add(..., validate=False)` for unvalidated bulk loading. To add an object you already hold, use `doc.addidfobject(obj)`: `collection.add(obj)` is deprecated (it filed the object in the collection only, unvalidated). |
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

### Typed creation through the collection

`add()` takes the type name and fields as strings, so a type checker checks neither: `doc.add("Zone", "Lab", ceiling_hieght=3.0)` type-checks and fails only when it runs, and the result is a plain `IDFObject`. In type-checked code, add through the collection instead:

```python
# Through the collection: the parameters are the type's own, checked by the type checker, and the
# result is the type's class (Zone, Material, ...), not a plain IDFObject. Signature help shows the
# required fields with no default and the others with the schema's default.
office_zone = doc.zones.add("Office", x_origin=0.0, ceiling_height=3.0)
office_zone.multiplier = 2  # typed: an int, checked on assignment

insulation = doc["Material"].add(
    "XPS_25mm",
    roughness="Rough",
    thickness=0.025,
    conductivity=0.034,
    density=35.0,
    specific_heat=1400.0,
)
doc["Output:SQLite"].add(option_type="SimpleAndTabular")  # a type without a Name field: no name

# doc.zones.add("Lab", ceiling_hieght=3.0)                       # error: No parameter named "ceiling_hieght"
# doc.zones.add("Lab", zone_inside_convection_algorithm="Bogus")  # error: not one of the field's choices
# doc["Material"].add("XPS_50mm", thickness=0.05)                 # error: Arguments missing for parameters
#                                                                 #   "roughness", "conductivity", "density", ...
# doc["Output:SQLite"].add("Out", option_type="Simple")          # error: parameter "this_type_has_no_name_field"
```

`doc.zones.add(...)` runs `doc.add("Zone", ...)` with validation on, so behaviour, validation errors and reference indexing are the same; the difference is the types. Its parameters come from the class's creation signature, generated from the schema, and an editor's signature help (Pylance, pyright) lists them as `doc.materials.add(` is typed: the name first, positional-only; then the fields the schema requires, with no default (`roughness: Literal[...]`, `thickness: float`, ...); then the others with their schema default (`thermal_absorptance: float | None = 0.9`), or `= ...` where the schema gives none (or one that is not a plain number or string). A shown default is the value EnergyPlus applies to a field left empty: `add()` stores only the fields you pass, so `material.thermal_absorptance` reads `None` until you set it. Leaving out a required field is a type error (`Arguments missing for parameters "roughness", ...`), as it is a `ValidationFailedError` (E001) at run time, and so is passing `None` for one. A type without a Name field takes no name: `doc["Output:SQLite"].add("x")` is a type error naming the parameter `this_type_has_no_name_field` (of type `_PassFieldsAsKeywords`), as it raises `InvalidFieldError`; pass the type's first field as a keyword instead (`doc.output_variables.add(key_value="*", ...)`); a type whose schema requires a name (most) must be given one, and a few (`Building`) default it to `""`. The parameters follow the document's type: through `IDFDocumentV9_4` the fields, value types and required fields are 9.4's, and through `AnyIDFDocument` only fields and values every release accepts, with a field required where any release requires it (so no release refuses a call that type-checks) and a default shown only where every release has it. Where no call suits every release, because a required field was renamed between releases (`People`, `Lights`, `InternalMass`), the signature requires `narrow_with_as_version_first`, which nothing satisfies: the error `Argument missing for parameter "narrow_with_as_version_first"` means narrow the document with `as_version(doc, since=...)` and add through that. A field whose key ends in `_` (`gas_or_gas_mixture_` on `WindowMaterial:Gap`) is offered under that key only. A field whose key is not a Python name (`100_outdoor_air_in_cooling` on `Sizing:System`) cannot be a keyword: set it with `doc.add(...)` or after creation. A collection a type checker cannot narrow (`doc.get_collection(obj_type)`) accepts any name and fields, as `doc.add()` does. Hover and signature help on a typed `add(` show the object type's own documentation rather than a generic one: its schema memo, its EnergyPlus I/O Reference page on docs.idfkit.com, and, where the signature requires `narrow_with_as_version_first`, that note. Per-field docs (units, ranges) are not in the signature help; hover the field on the typed object (`material.thickness`) or use `doc.describe(obj_type)`. Fields are keywords only. A type with no objects yet is read as an empty collection that is not stored in the document, and adding through it stores it, so `zones = doc.zones; zones.add("A")` leaves the zone in `zones`.

Prefer the attribute accessor (`doc.zones`, `doc.output_variables`) or a collection held in a variable when creating many objects in one function: a type checker resolves `doc["Output:Variable"]` through one overload per object type, which costs time for a type listed late in the schema, while an accessor and the collection's `add()` itself cost the same for every type.

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
from typing import TYPE_CHECKING

if TYPE_CHECKING:  # the classes exist only in the stubs; importing them at run time fails
    # From idfkit.document, not idfkit: recent pyright reports "not exported" for the latter.
    from idfkit.document import AnyBuildingSurfaceDetailed, AnyZone, Zone


def latest_ceiling(zone: Zone) -> float | None:
    """A latest-release Zone only: a 9.4 zone (Zone_v8_9_to_v9_4) is rejected."""
    height = zone.ceiling_height
    return height if isinstance(height, float) else None


def any_ceiling(zone: AnyZone) -> float | None:
    """A Zone of any release: the latest one, a 9.4 one, or one reached through AnyIDFDocument."""
    height = zone.ceiling_height
    return height if isinstance(height, float) else None


def vertex_count(surface: AnyBuildingSurfaceDetailed) -> int:
    """Extensible groups are typed too: vertices exist in every release."""
    return sum(1 for vertex in surface.vertices if vertex.vertex_x_coordinate is not None)


any_ceiling(doc["Zone"]["Office"])
any_ceiling(as_version(load_idf("legacy.idf"), IDFDocumentV9_4)["Zone"]["Office"])
```

An `Any<Class>` covers the releases idfkit supports. When idfkit adopts a release that drops or renames a field, that field leaves `Any<Class>`, and code using it stops type-checking: it would not work on that release either. A type the latest release no longer has, such as `DistrictHeating`, has no `Any<Class>`; annotate with its range class (`DistrictHeating_v8_9_to_v23_1`), imported from `idfkit.versioned` inside `if TYPE_CHECKING:`, since the range classes too exist only in the stubs.

### Reading and writing through `AnyIDFDocument`

Reading a field gives any value some release allows; writing accepts only what every release accepts:

```python
def use_natural_gas(doc: AnyIDFDocument) -> None:
    for heater in doc["WaterHeater:Mixed"]:
        fuel = heater.heater_fuel_type  # reads as str | None: any release's value can be in the file
        print(fuel)
        heater.heater_fuel_type = "NaturalGas"  # accepted: every release accepts it
        heater.update(heater_fuel_type="Electricity")  # update() is typed the same way
        # heater.heater_fuel_type = "DistrictHeatingWater"  # error: 9.3 to 23.1 reject it
        # heater.heater_fuel_type = "Steam"                 # error: 23.2 on rejects it


```

### Code for a range of releases

A union of release types accepts exactly those releases. `idfkit.versioned` has one for each range that starts or ends at a release: `IDFDocumentSince9_6` is 9.6 and every later release idfkit supports, `IDFDocumentBefore9_6` every earlier one. Under pyright, a value is accepted only if every release in the union accepts it, by assignment or `update()`; mypy checks `update()` this way but not attribute assignment through a union. Bind a `TypeVar` to the union, so the function returns the caller's own type (unannotated, pyright infers the whole union and mypy infers `Any`):

```python
from typing import TypeVar

from idfkit.versioned import IDFDocumentSince26_1, IDFDocumentV26_1

# A function for 26.1 and later. IDFDocumentSince26_1 is IDFDocumentV26_1 | IDFDocumentV26_2, and
# grows when idfkit adds a release. The TypeVar hands the caller's own type back: a plain
# load_idf() result (IDFDocument, which is IDFDocumentV26_2) comes back as IDFDocument.
Since26_1 = TypeVar("Since26_1", bound=IDFDocumentSince26_1)


def use_district_steam(doc: Since26_1) -> Since26_1:
    for heater in doc["WaterHeater:Mixed"]:
        heater.heater_fuel_type = "DistrictHeatingSteam"  # both releases accept it
    return doc


latest = use_district_steam(load_idf("model.idf"))  # IDFDocument
older = use_district_steam(as_version(load_idf("older.idf"), IDFDocumentV26_1))  # IDFDocumentV26_1
# use_district_steam(legacy)  # error: a 9.4 document is not in the range
```

The annotation is not checked at run time. To narrow a document of unknown release into a range, give `as_version` the range: `since=` the first release (inclusive), `before=` the release it stops before (exclusive), or both. Each bound is a release's number, its document type or its version tuple: `since="9.6"`, `since=IDFDocumentV9_6` and `since=(9, 6, 0)` are the same range. `as_version` returns the document typed as the union of the releases in the range (`IDFDocumentSince9_6` for `since="9.6"`), or raises `TypeError` naming them. pyright and mypy both keep the union exactly. The range is the releases idfkit supports, so it grows when idfkit adds one, and there is no list to keep current. Pass `since=`, not an `IDFDocumentSince9_6` alias: to a type checker an alias is not a class.

A type checker reads a range only from a release's type or a string literal. A bound in a variable (`since=first`), an optional one (`before: str | None`), or a version tuple (`since=doc.version`) is accepted, and types the document as `AnyIDFDocument`; so does a literal no supported release has (`since="27.1"`) or a range with no release in it, both of which raise `ValueError` when the call runs. Name a bound by its release (`"26.2"`, `IDFDocumentV26_2`), not `IDFDocument`: as a bound, `IDFDocument` means the latest release when the code runs, so `since=IDFDocument` stops accepting a 26.2 model once idfkit adopts the next release.

For releases that are not one range, pass `as_version` a tuple of release types, as `isinstance` takes one: `as_version(doc, (IDFDocumentV9_6, IDFDocumentV26_2))` returns the document typed as their union. Under pyright the union is kept exactly; mypy collapses it into what all of the releases share, so lookups still work but a field only those releases have is not offered. Name every release in a tuple by its own type, the latest included: `IDFDocumentV26_2`, not `IDFDocument`. `IDFDocument` stands for whichever release is latest when the code runs. Once idfkit supports a newer release, a tuple that ends in `IDFDocument` no longer covers the release that was latest when it was written, and `as_version` raises `TypeError` on a model of that release. A union written by hand to annotate with has the same flaw (pyright and mypy then reject a model of that release), a flaw the generated `IDFDocumentSince…` aliases do not have.

A narrower range also gives a narrower read type. Through releases that all list a field's choices, the checker can prove a `match` handles every one. Choices are read in the schema's spelling by default, so this holds on files that write them in another case (see Choice values are read in the schema's spelling):

```python
from typing_extensions import assert_never

from idfkit.versioned import IDFDocumentSince23_2


# Through this range heater_fuel_type reads as 12 known choices (or None), so the checker can
# prove every one is handled. Through AnyIDFDocument it reads as str | None (8.9 to 9.2 accept any
# string), and no match over it can be exhaustive.
def is_district_heated(doc: IDFDocumentSince23_2, heater_name: str) -> bool:
    fuel = doc["WaterHeater:Mixed"][heater_name].heater_fuel_type
    match fuel:
        case "DistrictHeatingWater" | "DistrictHeatingSteam":
            return True
        case (
            "Coal"
            | "Diesel"
            | "Electricity"
            | "FuelOilNo1"
            | "FuelOilNo2"
            | "Gasoline"
            | "NaturalGas"
            | "OtherFuel1"
            | "OtherFuel2"
            | "Propane"
            | None
        ):
            return False
        case _:
            assert_never(fuel)  # reported if a choice is left unhandled


```

### A model created for an older release

Pass `new_document` the release's document type: `new_document(IDFDocumentV9_4)` creates a 9.4.0 model typed as `IDFDocumentV9_4`, so the release is named once and the type and the version cannot disagree. For a non-strict model, parametrize the type, `new_document(IDFDocumentV9_4[Literal[False]])`, typed `IDFDocumentV9_4[Literal[False]]`; this form takes no `strict=`. Given a version tuple instead, `new_document` is typed for the latest release whatever the version, so a test fixture built with `new_document(version=(9, 4, 0))` is checked against the wrong release. For the latest release keep `new_document()`: `IDFDocument`, and so the latest release's own type `IDFDocumentV26_2` (which is `IDFDocument`), is refused (`TypeError`, though pyright accepts the call), because it is the run-time class of every document and `new_document(type(doc))` would otherwise create a latest-release model whatever `doc`'s release; `AnyIDFDocument` and unions of release types are refused too (a union, like `IDFDocument`, only when the call runs). A model whose version comes from a file is typed with `as_version`, as above.

```python
from typing import Literal

from idfkit import new_document

blank_94 = new_document(IDFDocumentV9_4)  # version (9, 4, 0), typed IDFDocumentV9_4
blank_94["People"]  # 9.4's People, with zone_or_zonelist_name
lax_94 = new_document(IDFDocumentV9_4[Literal[False]])  # non-strict, typed IDFDocumentV9_4[Literal[False]]
```

### A field renamed between releases

`AnyIDFDocument` offers neither name of a renamed field. Branch on `doc.version` and narrow each branch to the releases that use one name, `before=` and `since=` the release that renamed it; each `update()` call is then checked against all of them, under pyright and under mypy (which still rejects the `doc.version` test itself, as below):

```python
def set_people_zone(doc: AnyIDFDocument, people: str, zone: str) -> None:
    """Set a People object's zone, whatever the model's release.

    The field was renamed in 9.6, so AnyIDFDocument offers neither name. Each branch narrows the
    model to the releases that use one name, and update() is checked against all of them. The
    ranges are the releases idfkit supports, so since="9.6" takes every later release as it is added.
    """
    if doc.version < (9, 6, 0):
        as_version(doc, before="9.6")["People"][people].update(zone_or_zonelist_name=zone)
    else:
        as_version(doc, since="9.6")["People"][people].update(zone_or_zonelist_or_space_or_spacelist_name=zone)


```

### What `"Space" in doc` tells a type checker

At run time `"Space" in doc` is true when the model holds at least one `Space`. It is false for a release without the type, and equally for a release that has it when the model holds none, so it says nothing about the release, and `doc["Space"]` never raises either way. A type checker therefore leaves the document's type as it was on both sides of the test:

- `if "Space" in doc:` does not make a `Space` lookup legal through `AnyIDFDocument`; `doc["Space"]` stays an error inside it. Branch on `doc.version` and narrow with `as_version` instead.
- `if "Output:SQLite" not in doc:` on a type every release has is an ordinary branch, type-checked like any other: an empty model of any release takes it.
- On a union from `as_version(doc, (A, B, C))`, neither branch of `"Space" in d` drops a member.

```python
def ensure_sqlite_output(doc: AnyIDFDocument) -> None:
    """Add Output:SQLite unless the model already holds one.

    "Output:SQLite" in doc asks whether the model holds such an object, so it is False for an
    empty model of any release, and the body below is type-checked.
    """
    if "Output:SQLite" not in doc:
        doc.add("Output:SQLite", option_type="SimpleAndTabular")


def set_ceiling_heights(doc: AnyIDFDocument, height: float) -> None:
    """Branch on the release, not on "Space" in doc, then narrow with as_version.

    Space arrived in 9.6 and its ceiling_height field in 22.2. since="22.2" is every release from
    22.2 on, and grows when idfkit adopts a new one; a hand-written tuple of release types would not.
    """
    if doc.version < (22, 2, 0):
        return
    for space in as_version(doc, since="22.2")["Space"]:
        space.ceiling_height = height


```

The document types used to be `TypedDict` subclasses to pyright, which narrows those on `in` by its own rules: `"Space" in doc` retyped an `AnyIDFDocument` as the latest release (so a 9.6 or 22.1 model then raised `InvalidFieldError` on `ceiling_height`), and the body of `"Zone" not in doc` was skipped as unreachable.

### Checking: pyright versus `idfkit check`

They catch different mistakes, so code meant for several releases should run both:

- **pyright** (or Pylance, mypy) checks *types*: release-typed lookups (`legacy["Space"]`), attribute reads and assignments (`heater.heater_fuel_type = "Steam"`), `update()` keywords and those of a collection's `add()` (`doc.zones.add(...)`). It cannot see into string-keyed calls: `doc.add("Space", ...)` and its keyword values are untyped, which is why `doc.spaces.add(...)` is the form to use in type-checked code. A misspelled field is reported against `_NotAFieldOfThisObjectType` (`Argument of type "Literal['ceiling_hieght']" cannot be assigned to parameter "key" of type "_NotAFieldOfThisObjectType"`), or as `No parameter named "ceiling_hieght"` in a collection's `add()` or `update()` call.
- **`idfkit check`** lints *string literals* in Python source against the releases you name, with no annotations needed: object type names (rule `C001`, e.g. `doc.add("Space", ...)`, `legacy["Space"]`, `doc.get_collection("Space")`) and choice values in calls (rule `C002`, e.g. `add(..., heater_fuel_type="DistrictHeating")`). An object type, field name or choice value passed to `add()` that no target release accepts, which `add()` raises on, is an error (rule `C006`, with the closest real name: `doc.add("Zoen", "Office")`, `doc.add("Zone", "A", ceiling_hieght=3.0)`, `doc.add("Zone", "A", zone_inside_convection_algorithm="Bogus")`); it is read only in a file that imports idfkit. A field name is read from the keywords and from a dict of fields (`{"ceiling_height": 3.0}`, `fields={...}`), with or without `validate=False` (`add()` refuses an unknown field either way), and accepted as `add()` accepts it: a trailing-underscore field with or without its `_` (`gas_or_gas_mixture`), the extensible wrapper (`vertices=[...]`) and the deprecated flat spellings (`vertex_x_coordinate_2`); it is checked only when every target in scope has the type. `C001` and `C002` report a literal once, naming every release that lacks it (`not found in 8.9.0 to 9.5.0; added in 9.6.0`), and the summary counts findings. An unknown type is reported only on a receiver known to be a document with a schema (`doc = new_document()`, `load_idf(...)`, `as_version(...)`, or a parameter annotated `IDFDocument`, `AnyIDFDocument`, `IDFDocument | None`, ...), since a collection's `add()` takes a name first and a bare `IDFDocument()` accepts any type. A choice value is reported in an `add()` call given more than the type name (so `set.add("x")` is not read), except with `validate=False`, which stores it unchecked; on a collection (`doc["Zone"]`, `doc.zones`, or a name bound to one) it is checked against the collection's type. A document held as `self.building`, `app.window` or `variants["Window"]` is treated as a document, not a collection. It also reads field names in a collection's `add()` (`doc.zones.add("A", ceiling_hieght=3.0)`), which pyright checks too. It does not check attribute assignments, `obj.update(...)`, or a field some targets have and others lack.
- **`get_collection` with a literal name is for `idfkit check`, not pyright.** pyright types it as `IDFCollection[IDFObject]` whatever the name, and checks nothing. `idfkit check`, in a file that imports idfkit, reports a name no target release has (rule `C003`, an error, with the closest real name: at run time a misspelled `get_collection("Zoen")` silently returns an empty collection). The opt-in rule `C004` (`--extend-select C004`) also reports every other literal name, suggesting `doc["Zone"]`, which is typed and which pyright checks. Variable names (`doc.get_collection(t)`) are not reported.
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
from idfkit import MissingRequiredFieldError

if TYPE_CHECKING:
    from idfkit.document import AnyMaterial


def r_value(mat: AnyMaterial) -> float:
    """thickness and conductivity are required in every release: they read as float, no guard."""
    return mat.thickness / mat.conductivity


absorptance = doc.materials["Concrete"].thermal_absorptance  # float | None: it has a default
effective = absorptance if absorptance is not None else 0.9  # the value EnergyPlus applies

legacy = load_idf("hand_written.idf")  # a file EnergyPlus would refuse may lack a required field
for mat in legacy.materials:
    if mat.get("thickness") is None:  # the untyped check: None when unset, never raises
        print(f"{mat.name} has no thickness")
        continue
    print(r_value(mat))
try:
    print(legacy.materials["Brick"].thickness)
except MissingRequiredFieldError as err:  # an AttributeError naming the object and the field
    print(err.obj_type, err.obj_name, err.field_name)
```

A blank value is stored as absent wherever it comes from (`add(..., f="")`, `obj.f = ""`, `""` or `null` in epJSON, an empty IDF field), so no field reads `""`, and `""` is not part of any field's type: clear a field with `None` in type-checked code.

### Choice values are read in the schema's spelling

A choice field reads in the spelling its schema declares, whatever case the source used: a surface the file calls `WALL` reads `surface_type == "Wall"`, the spelling its `Literal["Wall", "Floor", "Ceiling", "Roof"]` type lists. This holds for IDF and epJSON files, for values given to `doc.add()`, `update()` or assignment in another case (`doc.add("Material", "M", roughness="ROUGH", ...)` stores `"Rough"`; on a typed object only the `Literal` spelling type-checks anyway), for extensible groups, and for the sizing keywords of a numeric field (`AUTOSIZE` reads `"Autosize"`). A value that is no listed choice is kept as written, for `validate_document` to report. EnergyPlus reads choices case-insensitively, so this changes no simulation. A `preserve_formatting=True` load still writes every unmodified object byte for byte; an object you change is written with its choices in the schema's spelling. So an exhaustive `match` over a choice field is sound on models you did not write:

```python
from collections import Counter

from typing_extensions import assert_never

from idfkit import load_idf

# 5ZoneAirCooled.idf writes WALL, FLOOR, CEILING and ROOF. Each choice is read in the spelling the
# schema declares, so the Literal type holds and the match is exhaustive on a file of any case.
model = load_idf("5ZoneAirCooled.idf")
counts: Counter[str] = Counter()
for srf in model.building_surfaces:
    match srf.surface_type:
        case "Wall" | "Floor" | "Ceiling" | "Roof":
            counts[srf.surface_type] += 1
        case _:
            assert_never(srf.surface_type)

# Opt out to keep the file's own text. The Literal type then does not hold: compare with casefold().
raw = load_idf("5ZoneAirCooled.idf", normalize_choices=False)
walls = [s for s in raw.building_surfaces if s.surface_type.casefold() == "wall"]
assert raw.normalize_choices is False
```

To keep the source's text, pass `normalize_choices=False` to `load_idf`, `load_epjson`, `load_idf_with_diagnostics` or `new_document`; `doc.normalize_choices` reports the setting, and `doc.copy()`, `migrate()` and `expand_objects()` keep it. It is independent of `strict` and `preserve_formatting`. The stubs do not change with it: on such a document a choice field still has its `Literal` type but can hold any case, so compare with `.casefold()` and do not rely on an exhaustive `match`.

## Modifying objects

Field access is via attribute. Setting a value re-validates against the schema and updates the reference graph automatically:

```python
zone = doc["Zone"]["Office"]
zone.ceiling_height = 3.5  # plain field
zone.direction_of_relative_north = 90.0
```

Dict-style access also works and accepts either Python or IDD field names — `zone["x_origin"]`, `zone["X Origin"]`, and `zone.x_origin` are all equivalent. Attribute access is the idiomatic form (better IDE autocomplete and type checking). A typed object, such as one from `doc["Lights"]` or `doc.lights`, declares the EnergyPlus 26.2 snake_case names only, and pyright reports any other attribute name, read or assigned. That includes an eppy-style capitalised spelling (`lights.Watts_per_Zone_Floor_Area`) and a field that exists only in an earlier version (`Lights.watts_per_zone_floor_area`, up to 23.2). Both still work at run time; in type-checked code, reach a field missing from 26.2 with item access (`lights["watts_per_zone_floor_area"]`). Objects from `doc.add()`, `doc.get_collection()` and the eppy API are plain `IDFObject` and accept any name; a collection's `add()` (`doc.zones.add(...)`) returns the typed class. A few epJSON keys end in `_` because their IDD name ends in punctuation or a space (`cond_flag_is_the_basement_conditioned_`, `nx_number_of_cells_in_the_x_direction_20_`). At runtime the spelling without the underscore works too, in `add()`, attribute access and `update()`, and is stored under the schema's key; `name` is never such a spelling. The typed `update()` stubs name only the schema's key, so use that key in type-checked code.

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

`ExtensibleList` supports `append`, `insert`, `extend`, `clear`, `pop`, indexing, iteration, and `as_list()`. In type-checked code, a group passed to `add()` or `update()` is a dict typed by the group's item type, a `TypedDict` of the group's fields, all optional: `vertices=[{"vertex_x_coordinate": 0.0, ...}]` takes a sequence of `BuildingSurfaceDetailedVerticesItem`, or of the group objects themselves (`vertices=list(other.vertices)`), so editors complete the keys and a misspelled key or wrong value is a type error. `wall.vertices.as_list()` returns `list[BuildingSurfaceDetailedVerticesItem]`, so a copy passes straight back (`vertices=wall.vertices.as_list()`); its keys are optional, as a blank field is left out, so read one with `.get()`. To build groups ahead of a call, annotate the list with the item type (`points: list[BuildingSurfaceDetailedVerticesItem] = []`, imported from `idfkit.document`); a list typed `list[dict[str, float]]` is not accepted. Each item type is named after its object type and group (`ScheduleWeekCompactDataItem`, `ZoneListZonesItem`).

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
    def ensure_sqlite_output(doc: AnyIDFDocument) -> None:
        """Add Output:SQLite unless the model already holds one.

        "Output:SQLite" in doc asks whether the model holds such an object, so it is False for an
        empty model of any release, and the body below is type-checked.
        """
        if "Output:SQLite" not in doc:
            doc.add("Output:SQLite", option_type="SimpleAndTabular")


    def set_ceiling_heights(doc: AnyIDFDocument, height: float) -> None:
        """Branch on the release, not on "Space" in doc, then narrow with as_version.

        Space arrived in 9.6 and its ceiling_height field in 22.2. since="22.2" is every release from
        22.2 on, and grows when idfkit adopts a new one; a hand-written tuple of release types would not.
        """
        if doc.version < (22, 2, 0):
            return
        for space in as_version(doc, since="22.2")["Space"]:
            space.ceiling_height = height


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
