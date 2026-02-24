# Evaluation: IDFkit Developer Experience in VS Code

## Executive Summary

When Python developers use IDFkit in VS Code, they get no auto-completion for
object fields, no type checking on field values, and no discoverability for the
`doc.zones`-style attribute shortcuts. This is because IDFkit relies heavily on
`__getattr__`/`__setattr__` for dynamic attribute access, making all field
interactions opaque to static analysis tools like Pyright/Pylance.

The primary challenge — **determining the necessary attributes for a specific
IDF object** — is a direct consequence of this design. A developer writing
`model.add("BuildingSurface:Detailed", "Wall_South", ...)` has no way to
discover the 14+ required and optional keyword arguments without consulting
external documentation. VS Code's IntelliSense is silent.

This document evaluates the problem, measures its scope, and proposes concrete
solutions that range from zero-code improvements to schema-driven code
generation.

---

## 1. The Problem: Dynamic Access Defeats Static Analysis

### 1.1 What the developer experiences today

Consider a typical IDFkit workflow in VS Code:

```python
from idfkit import new_document

model = new_document(version=(24, 1, 0))

# (1) No auto-complete for "zones" — Pyright doesn't know this attribute exists
zones = model.zones

# (2) No auto-complete for field names — zone.x_| shows nothing
zone = model["Zone"]["Office"]
x = zone.x_origin  # Pyright infers: Any

# (3) No type checking — this typo is silently accepted, returns None
y = zone.y_origni  # No error, returns None at runtime

# (4) No field discovery for add() — what kwargs does Material accept?
model.add("Material", "Concrete", roughness="MediumRough", ...)  # guessing
```

At every step, Pylance/Pyright sees `Any` and offers no help.

### 1.2 Where the type information is lost

There are six specific code patterns in IDFkit where static type information
is lost. Each one maps to a different user frustration:

#### Pattern 1: `IDFObject.__getattr__` — Field reads return `Any`

**Location:** `src/idfkit/objects.py:143-164`

```python
def __getattr__(self, key: str) -> Any:
    # Tries multiple name forms, returns None if not found
```

**User impact:** `zone.x_origin`, `zone.roughness`, `zone.anything_at_all`
all have type `Any`. No field name completions, no type narrowing, no error
on misspelled field names.

#### Pattern 2: `IDFObject.__setattr__` — Field writes accept anything

**Location:** `src/idfkit/objects.py:166-175`

```python
def __setattr__(self, key: str, value: Any) -> None:
    python_key = to_python_name(key)
    self._data[python_key] = value
```

**User impact:** `zone.thickness = "not a number"` is silently accepted.
No type checking on assignment. No error on assigning to nonexistent fields.

#### Pattern 3: `IDFDocument.__getattr__` — Collection shortcuts are invisible

**Location:** `src/idfkit/document.py:161-183`

```python
def __getattr__(self, name: str) -> IDFCollection:
    obj_type = _PYTHON_TO_IDF.get(name)
    if obj_type:
        return self[obj_type]
```

**User impact:** `model.zones`, `model.materials`, `model.building_surfaces`
and 45 other convenience attributes are completely invisible to Pylance. No
auto-completion when typing `model.zo...`. Pyright may even flag them as
errors in strict mode.

#### Pattern 4: `IDFDocument.add()` — kwargs are untyped

**Location:** `src/idfkit/document.py:244-294`

```python
def add(self, obj_type: str, name: str, data: dict[str, Any] | None = None,
        **kwargs: Any) -> IDFObject:
```

**User impact:** This is the primary pain point. When writing:
```python
model.add("Material", "Concrete_200mm",
    roughness="MediumRough",
    thickness=0.2,
    # ... what other fields exist? Are they required? What types?
)
```
VS Code shows no parameter hints for the available fields. The developer must
consult the EnergyPlus IDD reference, the idfkit docs, or the schema
introspection API to discover that `conductivity`, `density`, and
`specific_heat` are required.

#### Pattern 5: `IDFObject.__getitem__` — Index access returns `Any`

**Location:** `src/idfkit/objects.py:177-186`

```python
def __getitem__(self, key: str | int) -> Any:
```

**User impact:** `zone[0]` is always `str` (the name), but Pyright sees `Any`.
`zone["x_origin"]` also returns `Any`.

#### Pattern 6: `IDFObject.get_field_idd()` — Schema access returns untyped dict

**Location:** `src/idfkit/objects.py:224-229`

```python
def get_field_idd(self, field_name: str) -> dict[str, Any] | None:
```

**User impact:** The schema information *is* accessible at runtime via this
method, but the returned dict is untyped — the developer doesn't get
completion for keys like `"type"`, `"enum"`, `"default"`, `"units"`, etc.

---

## 2. Scale of the Problem

The EnergyPlus v24.1 schema defines:

| Metric | Count |
|---|---|
| Object types | 847 |
| Total fields across all object types | 12,652 |
| Fields with descriptions | 6,055 (47.9%) |
| Fields with default values | 3,764 (29.7%) |
| Fields with enum constraints | 1,505 (11.9%) |
| Fields with units | 4,692 (37.1%) |
| Required fields (across all types) | Varies per type (e.g., Material has 5) |
| Convenience attributes on IDFDocument | 48 (in `_PYTHON_TO_IDF` mapping) |

All 12,652 fields and 48 convenience attributes are currently invisible to
VS Code's type system. A developer working with even 10-20 common object types
must memorize or look up hundreds of field names.

---

## 3. Proposed Solutions

The solutions below are ordered from least to most invasive. They can be
adopted incrementally.

### 3.1 Solution A: Explicit properties on `IDFDocument` for common collections

**What:** Replace the `__getattr__` lookup for the 48 entries in
`_PYTHON_TO_IDF` with explicit `@property` declarations.

**Before:**
```python
# In __getattr__, invisible to Pyright:
_PYTHON_TO_IDF = {"zones": "Zone", "materials": "Material", ...}
```

**After:**
```python
@property
def zones(self) -> IDFCollection:
    """Collection of Zone objects."""
    return self["Zone"]

@property
def materials(self) -> IDFCollection:
    """Collection of Material objects."""
    return self["Material"]

@property
def building_surfaces(self) -> IDFCollection:
    """Collection of BuildingSurface:Detailed objects."""
    return self["BuildingSurface:Detailed"]

# ... for all 48 entries
```

**Impact:**
- `model.zones` auto-completes in VS Code immediately
- `model.zo` triggers suggestion list showing `zones`
- Docstrings appear in hover
- The `__getattr__` fallback remains for dynamic/uncommon types
- No runtime behavior change

**Effort:** Low. The 48 properties can be generated from the existing
`_PYTHON_TO_IDF` dict with a script. The `__getattr__` fallback stays for
backward compatibility and for the remaining ~800 object types.

**Limitation:** The returned `IDFCollection` is still generic — its objects
are `IDFObject` with no field-specific types.

### 3.2 Solution B: `TypedDict` classes for common object types

**What:** Define `TypedDict` classes for the most common object types and use
them in `add()` overloads.

```python
from typing import TypedDict

class ZoneFields(TypedDict, total=False):
    x_origin: float
    y_origin: float
    z_origin: float
    direction_of_relative_north: float
    type: int
    multiplier: int
    ceiling_height: float | str
    volume: float | str
    floor_area: float | str

class MaterialFields(TypedDict, total=False):
    roughness: str  # Literal["Rough", "MediumRough", ...] for stricter checking
    thickness: float
    conductivity: float
    density: float
    specific_heat: float
    thermal_absorptance: float
    solar_absorptance: float
    visible_absorptance: float
```

These can be used in overloaded signatures for `add()`:

```python
from typing import overload, Literal

@overload
def add(self, obj_type: Literal["Zone"], name: str,
        data: ZoneFields | None = None, **kwargs: Unpack[ZoneFields]) -> IDFObject: ...
@overload
def add(self, obj_type: Literal["Material"], name: str,
        data: MaterialFields | None = None, **kwargs: Unpack[MaterialFields]) -> IDFObject: ...
@overload
def add(self, obj_type: str, name: str,
        data: dict[str, Any] | None = None, **kwargs: Any) -> IDFObject: ...
```

**Impact:**
- `model.add("Material", "Concrete", |)` shows `roughness`, `thickness`, etc.
  in the completion list with correct types
- Type errors like `thickness="not a number"` are caught statically
- The generic `str` overload preserves backward compatibility for all 847 types

**Effort:** Medium. The `TypedDict` classes can be auto-generated from the
schema. The overloads must cover the most common types (perhaps 20-30). A
code generation script reading the bundled schema can produce all of them.

**Limitation:** `@overload` with `Literal` string discrimination works with
Pyright but produces long type stubs. Covering all 847 types this way is
impractical in source code — a `.pyi` stub file is more appropriate.

### 3.3 Solution C: Generated `.pyi` type stubs from schema

**What:** Use the EnergyPlus schema to generate a comprehensive `.pyi` stub
file that provides type information to Pyright without changing any runtime
code.

**Generated `src/idfkit/document.pyi`:**
```python
class IDFDocument:
    @property
    def zones(self) -> IDFCollection: ...
    @property
    def materials(self) -> IDFCollection: ...
    @property
    def building_surfaces(self) -> IDFCollection: ...
    # ... all 48 convenience properties

    @overload
    def add(self, obj_type: Literal["Zone"], name: str, data: ZoneFields | None = ...,
            *, x_origin: float = ..., y_origin: float = ..., ...) -> IDFObject: ...
    @overload
    def add(self, obj_type: Literal["Material"], name: str, data: MaterialFields | None = ...,
            *, roughness: str = ..., thickness: float = ..., ...) -> IDFObject: ...
    # ... overloads for top N object types
    @overload
    def add(self, obj_type: str, name: str, data: dict[str, Any] | None = ...,
            **kwargs: Any) -> IDFObject: ...
```

**Generated `src/idfkit/objects.pyi`:**
```python
class IDFObject:
    @property
    def name(self) -> str: ...
    @property
    def obj_type(self) -> str: ...
    @property
    def data(self) -> dict[str, Any]: ...
    @property
    def fieldnames(self) -> list[str]: ...
    @property
    def fieldvalues(self) -> list[Any]: ...
    def get_field_idd(self, field_name: str) -> FieldSchema | None: ...
    # __getattr__ return type stays Any — but typed wrapper classes help
```

**Impact:**
- All 48 document properties auto-complete
- `add()` calls for common types get full field completion and type checking
- Zero runtime changes — stubs only affect static analysis
- Can be regenerated whenever the schema changes

**Effort:** Medium. Requires a code generation script (which can live in
a `scripts/` or `tools/` directory). The script reads the schema and writes
`.pyi` files. Must be re-run when the schema version or API changes.

### 3.4 Solution D: Schema-informed `FieldSchema` TypedDict

**What:** Type the schema introspection return values so developers using
`get_field_idd()` get completion for schema keys.

```python
class FieldSchema(TypedDict, total=False):
    type: str
    enum: list[str]
    default: float | int | str
    minimum: float
    maximum: float
    exclusiveMinimum: float
    exclusiveMaximum: float
    note: str
    units: str
    ip_units: str  # "ip-units" in the JSON, mapped for Python
    object_list: list[str]
    data_type: str
    anyOf: list[dict[str, Any]]
    reference: list[str]
```

**Before:**
```python
field_info = zone.get_field_idd("x_origin")  # dict[str, Any] | None
field_info["type"]  # Any
```

**After:**
```python
field_info = zone.get_field_idd("x_origin")  # FieldSchema | None
field_info["type"]  # str — with auto-complete for "type", "enum", etc.
```

**Impact:** Improves the "expert" workflow where developers introspect the
schema programmatically (as shown in the getting_started notebook Section 3.4).

**Effort:** Low. One `TypedDict` class plus updating the return type annotation
on `get_field_idd()` and `get_field_schema()`.

### 3.5 Solution E: Runtime helper for field discovery

**What:** Add a method to `IDFObject` or `EpJSONSchema` that returns a
structured summary of an object type's fields, designed for interactive
exploration in notebooks and the REPL.

```python
# Possible API
schema.describe("Material")
# Output:
# Material (Surface Construction Elements)
#   * roughness        : str   enum=[Rough, MediumRough, ...]
#   * thickness        : float units=m, >0
#   * conductivity     : float units=W/m-K, >0
#   * density          : float units=kg/m3, >0
#   * specific_heat    : float units=J/kg-K, >=100
#     thermal_absorptance: float default=0.9, (0, 0.99999]
#     solar_absorptance  : float default=0.7, [0, 1]
#     visible_absorptance: float default=0.7, [0, 1]
#   (* = required)

# Or as structured data:
schema.get_fields_summary("Material")
# Returns list of FieldInfo dataclasses with name, type, required, default, etc.
```

**Impact:** Directly addresses the primary challenge. Even without static
typing, developers can quickly discover what fields an object type needs. Works
in Jupyter notebooks (the getting_started notebook already uses schema
introspection, but the output requires manual assembly).

**Effort:** Low-medium. A formatting/presentation layer over existing schema
APIs.

---

## 4. Recommendation: Incremental Adoption Path

These solutions build on each other and can be adopted in phases:

### Phase 1: Quick wins (no code generation required)

1. **Explicit properties on IDFDocument** (Solution A) — Replace the 48
   `_PYTHON_TO_IDF` entries with `@property` methods. This immediately enables
   auto-completion for `model.zones`, `model.materials`, etc. Keep the
   `__getattr__` fallback for dynamic access.

2. **`FieldSchema` TypedDict** (Solution D) — Type the return value of
   `get_field_idd()` and `get_field_schema()`. Small change, immediate benefit
   for schema introspection workflows.

3. **`describe()` helper** (Solution E) — Add a human-readable field summary
   method. Helps notebook users and REPL exploration.

### Phase 2: Schema-driven code generation

4. **TypedDict classes for top 20-30 object types** (Solution B) — Generate
   `TypedDict` classes for `Zone`, `Material`, `Construction`,
   `BuildingSurface:Detailed`, `People`, `Lights`, etc. Use `@overload` on
   `add()` for these types.

5. **Full `.pyi` stub generation** (Solution C) — Build a script that reads the
   schema and generates complete type stubs. Regenerate per EnergyPlus version.
   Ship as part of the package so Pylance picks them up automatically.

### Phase 3: Advanced type narrowing

6. **Generic `IDFCollection[T]`** — Parameterize `IDFCollection` so that
   `model.zones` returns `IDFCollection[ZoneObject]` where `ZoneObject` is a
   protocol or typed class with known fields. This provides end-to-end type
   flow: `model.zones["Office"].x_origin` would infer `float`.

7. **Pyright plugin** (if supported in the future) — Custom type narrowing
   could resolve `model.add("Zone", ...)` to the correct `TypedDict` without
   requiring explicit overloads for all 847 types.

---

## 5. Detailed Analysis: What Each Solution Enables

| User action | Today | Phase 1 | Phase 2 | Phase 3 |
|---|---|---|---|---|
| `model.zo` → auto-complete to `zones` | No | Yes | Yes | Yes |
| `model.zones` → recognized by Pyright | No | Yes | Yes | Yes |
| `model.add("Zone", ...)` → field hints | No | No | Yes (top types) | Yes (all types) |
| `model.add("Material", ..., thickness=)` → type check | No | No | Yes | Yes |
| `zone.x_origin` → inferred as `float` | No | No | No | Yes |
| `zone.x_origni` → flagged as typo | No | No | No | Yes |
| `schema.get_field_schema(...)["type"]` → auto-complete | No | Yes | Yes | Yes |
| `schema.describe("Material")` → field summary | No | Yes | Yes | Yes |

---

## 6. Technical Considerations

### 6.1 Maintaining `__getattr__` for backward compatibility

All solutions preserve the existing `__getattr__` fallback. Explicit
properties take precedence over `__getattr__` in Python's MRO, so adding
properties is non-breaking. The 48 convenience attributes become static
while the remaining ~800 object types still work dynamically.

### 6.2 Code generation vs. hand-written stubs

With 847 object types and 12,652 fields, hand-writing type information is
impractical. A code generation script that reads the bundled EnergyPlus schema
is the correct approach. The script should:

- Read `schemas/V{version}/Energy+.schema.epJSON.gz`
- Extract field names, types, defaults, required flags
- Map EnergyPlus types to Python types: `"number"` → `float`,
  `"integer"` → `int`, `"string"` → `str`
- Handle `anyOf` fields (e.g., `float | Literal["Autocalculate"]`)
- Handle `enum` fields as `Literal` unions
- Generate `.pyi` stubs or inline TypedDict classes

### 6.3 Handling 847 object types in overloads

Python's `@overload` is not designed for 847 variants. Practical options:

- **Top-N overloads in source code:** Cover the 20-30 most common types
  (`Zone`, `Material`, `Construction`, `BuildingSurface:Detailed`, `People`,
  `Lights`, `ElectricEquipment`, `Schedule:Compact`, etc.) with explicit
  overloads. A final `str` overload catches everything else.

- **Full coverage in `.pyi` stubs:** Stubs can be larger without runtime cost.
  Generate an overload per object type in the stub file.

- **Alternative: builder pattern:** Instead of overloading `add()`, provide
  typed builder methods:
  ```python
  model.add_zone("Office", x_origin=0.0, y_origin=0.0)
  model.add_material("Concrete", roughness="MediumRough", thickness=0.2, ...)
  ```
  This gives complete type safety but adds API surface. Could be generated
  for top-N types.

### 6.4 The `__slots__` constraint

`IDFObject` uses `__slots__`, which means properties must be defined on the
class, not on instances. This is compatible with all proposed solutions —
properties and TypedDicts are class-level constructs.

### 6.5 Versioning

The EnergyPlus schema changes between versions (new object types, new fields,
deprecated fields). Type stubs should be generated per schema version. Since
IDFkit supports 16 versions, the stubs could either:

- Target the latest version only (simplest, covers most users)
- Ship version-specific stubs selected by configuration
- Generate a union type covering all versions (most complete but noisier)

The pragmatic choice is to generate stubs for the latest version and document
that earlier versions may have fewer/different fields.

---

## 7. Impact on Existing Notebook and Test Workflows

### 7.1 Getting started notebook

The getting_started notebook (`docs/getting_started.ipynb`) demonstrates
patterns that would immediately benefit:

**Cell 7 — Adding objects with kwargs:**
```python
model.add("Building", "My Office Building", {
    "north_axis": 0,
    "terrain": "City",
    ...
})
```
With Solution B, VS Code would auto-complete the dict keys and validate types.

**Cell 9 — Attribute access on document:**
```python
zones = model.zones  # Currently invisible to Pylance
```
With Solution A, this auto-completes and type-checks.

**Cell 11 — Field access on objects:**
```python
office.x_origin  # Currently Any
```
With Solution C (Phase 3), this would be `float`.

**Cell 53 — Schema introspection:**
```python
field_names = schema.get_field_names("Zone")
required = schema.get_required_fields("Zone")
```
With Solution D, the schema return types are fully typed.

### 7.2 Test suite

The test suite (`tests/`) uses the same patterns. Adding type stubs would
enable Pyright to catch type errors in tests themselves, improving code quality
of both the library and user code.

---

## 8. Conclusion

IDFkit's runtime design is sound — dynamic attribute access provides a clean
API for working with 847 object types without boilerplate. But this dynamism
comes at the cost of VS Code discoverability, which is the primary obstacle
for new users and the root cause of the stated challenge.

The most impactful first step is **Solution A: explicit properties on
IDFDocument**. It is a small, non-breaking change that immediately makes 48
collection shortcuts visible to auto-complete. Combined with **Solution D
(typed schema returns)** and **Solution E (describe helper)**, this addresses
the field discovery problem through both static analysis and runtime
introspection.

For deeper type safety, **schema-driven code generation** (Solutions B and C)
can produce TypedDicts and `.pyi` stubs that give `add()` calls full parameter
completion for the most common object types. This is where the richness of the
EnergyPlus schema (12,652 typed fields with defaults, enums, ranges, and
descriptions) becomes a direct asset — every field definition in the schema
translates to a typed parameter hint in VS Code.
