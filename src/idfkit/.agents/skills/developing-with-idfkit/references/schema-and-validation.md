# Schema and validation

idfkit bundles the official EnergyPlus epJSON schema for every supported version (8.9 → 26.1). The schema drives field metadata (types, ranges, defaults, references) and on-demand validation. Use it for introspection ("what fields does `Zone` have?") and for catching errors before you hand a model to EnergyPlus.

## When to use

- You're authoring a model and want to know what fields and types an object accepts.
- You've finished editing and want a single pre-flight check before simulating.
- You want to look up the EnergyPlus group, memo, or required fields for an object type.

## Quick start

```python
from idfkit import load_idf, validate_document, get_schema

doc = load_idf("building.idf")
result = validate_document(doc)
if not result.is_valid:
    for err in result.errors:
        print(err)
```

## Core API

| Symbol | Purpose |
|---|---|
| `get_schema(version)` | Load and cache the `EpJSONSchema` for an EnergyPlus version. |
| `get_schema_manager()` | Process-wide schema cache. |
| `EpJSONSchema` | The schema container; see methods below. |
| `validate_document(doc, *, check_references=True, check_required=True, check_types=True, check_ranges=True, check_singletons=True, object_types=None)` | Validate a whole document. Returns `ValidationResult`. |
| `validate_object(obj, schema=None)` | Validate one object. Returns a `list[ValidationError]`. |
| `ValidationResult` | `.errors`, `.warnings`, `.info`, `.is_valid`, `.total_issues`. |
| `ValidationError` | `severity`, `obj_type`, `obj_name`, `field`, `message`, `code`. |
| `Severity` | `ERROR`, `WARNING`, `INFO`. |
| `ObjectDescription` / `FieldDescription` | Schema introspection — see [Introspection](#introspecting-the-schema). |

`doc.schema` is the `EpJSONSchema` already bound to the document's version. You rarely need to pass `schema=` to `validate_document` — the default is `doc.schema`.

## Schema methods worth knowing

```python
from idfkit import get_schema

schema = get_schema((25, 2, 0))

schema.get_object_schema("Zone")           # raw JSON-Schema dict
schema.get_field_names("Zone")             # Python-style field names
schema.get_required_fields("Zone")
schema.get_field_type("Zone", "x_origin")  # "real", "alpha", "choice", ...
schema.get_field_default("Material", "thickness")
schema.get_group("HVACTemplate:Zone:VAV")  # "HVAC Templates"
schema.has_name("Zone")                    # True
schema.is_extensible("BuildingSurface:Detailed")
schema.is_reference_field("Zone", "Floor Area")
schema.get_field_object_list("BuildingSurface:Detailed", "zone_name")
# ['ZoneNames']  — what reference list this field accepts
schema.get_types_providing_reference("ZoneNames")
# ['Zone', 'ZoneList'] — what types satisfy that reference
schema.object_types                        # every registered type
"Zone" in schema                           # bool
```

The reference-list machinery (`get_field_object_list` / `get_types_providing_reference`) is what powers automatic cross-reference tracking. See [reference-tracking.md](reference-tracking.md).

## Validating a document

```python
from idfkit import validate_document

result = validate_document(doc)
print(result)                              # human summary

# Drill in
for err in result.errors:
    print(err.code, err.obj_type, err.obj_name, err.field, err.message)

for warn in result.warnings:
    print(warn)
```

`ValidationResult` is truthy when `is_valid` is `True`. Use it as a gate:

```python
if not validate_document(doc):
    raise SystemExit("Refusing to simulate an invalid model")
```

## Scoping a validation

Skip categories of checks when you're iterating quickly, or restrict to a subset of types:

```python
# Skip range checks during a parametric sweep where you know values are temporarily out of bounds
result = validate_document(doc, check_ranges=False)

# Validate only materials and constructions
result = validate_document(doc, object_types=["Material", "Construction"])

# Skip reference integrity (e.g. before you've finished adding referenced objects)
result = validate_document(doc, check_references=False)
```

## Validating a single object

For tight inner loops or interactive workflows, `validate_object` skips reference checks (which require a whole-document view):

```python
from idfkit import validate_object

zone = doc["Zone"]["Office"]
issues = validate_object(zone)
for issue in issues:
    print(issue)
```

## Error codes

Common codes (see `ValidationError.code`):

- `E001` — required field missing
- `E002` — invalid type
- `E003` — value out of range
- `E004` — unknown reference target
- `E010` — singleton constraint violated (>1 instance of a `maxProperties: 1` type)
- `W001` — schema not available (validator skipped)

These codes are stable; agents and CI checks can filter on them.

## Introspecting the schema

`ObjectDescription` and `FieldDescription` are higher-level views over the raw JSON Schema:

```python
desc = doc.describe("Zone")
print(desc.memo)                           # human description from EnergyPlus docs
for field in desc.fields:
    print(field.name, field.field_type, field.required, field.default, field.range)
```

`doc.describe("Zone")` is shorthand for `ObjectDescription.from_schema(doc.schema, "Zone")`.

## Common mistakes

**BAD — running a simulation without validating first**

```python
result = simulate(doc, "weather.epw")      # may fail mid-simulation with cryptic .err output
```

**GOOD — gate the simulation on validation**

```python
v = validate_document(doc)
if not v.is_valid:
    for err in v.errors:
        print(err)
    raise SystemExit("Fix errors before simulating")
result = simulate(doc, "weather.epw")
```

**BAD — assuming a field exists without checking the schema**

```python
zone.fictional_field = 1.0                 # InvalidFieldError in strict mode
```

**GOOD — ask the schema**

```python
if "fictional_field" in doc.schema.get_field_names("Zone"):
    zone.fictional_field = 1.0
```

**BAD — caching a schema across versions**

```python
schema = get_schema((24, 1, 0))            # cached
doc = load_idf("v25_model.idf")            # version (25, 2, 0)
validate_document(doc, schema=schema)      # wrong schema — false errors
```

**GOOD — let the document carry its own schema**

```python
validate_document(doc)                     # uses doc.schema automatically
```

## Related

- [reference-tracking.md](reference-tracking.md) — the reference machinery built on top of schema metadata.
- [document-and-objects.md](document-and-objects.md) — using schema info to author objects.
- [version-migration.md](version-migration.md) — when the schema changes between versions.
- API docs: [py.idfkit.com/api/validation/](https://py.idfkit.com/api/validation/) and [py.idfkit.com/api/schema/](https://py.idfkit.com/api/schema/)
