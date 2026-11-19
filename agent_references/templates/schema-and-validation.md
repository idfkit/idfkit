# Schema and validation

idfkit bundles the official EnergyPlus epJSON schema for every supported version (8.9 → 26.2). The schema drives field metadata (types, ranges, defaults, references) and on-demand validation. Use it for introspection ("what fields does `Zone` have?") and for catching errors before you hand a model to EnergyPlus.

## When to use

- You're authoring a model and want to know what fields and types an object accepts.
- You've finished editing and want a single pre-flight check before simulating.
- You want to look up the EnergyPlus group, memo, or required fields for an object type.

## Quick start

```python
--8<-- "agent_references/snippets/schema-and-validation.py:quickstart"
```

## Core API

| Symbol | Purpose |
|---|---|
| `get_schema(version)` | Load and cache the `EpJSONSchema` for an EnergyPlus version. |
| `get_schema_manager()` | Process-wide schema cache. |
| `EpJSONSchema` | The schema container; see methods below. |
| `validate_document(doc, *, check_references=True, check_required=True, check_types=True, check_ranges=True, check_singletons=True, object_types=None, check_geometry=True)` | Validate a whole document. Returns `ValidationResult`. |
| `validate_object(obj, schema=None)` | Validate one object. Returns a `list[ValidationError]`. |
| `ValidationResult` | `.errors`, `.warnings`, `.info`, `.is_valid`, `.total_issues`. |
| `ValidationError` | `severity`, `obj_type`, `obj_name`, `field`, `message`, `code`, and `obj`: the `IDFObject` itself (`None` for a document-level issue). |
| `Severity` | `ERROR`, `WARNING`, `INFO`. |
| `ObjectDescription` / `FieldDescription` | Schema introspection — see [Introspection](#introspecting-the-schema). |

`doc.schema` is the `EpJSONSchema` already bound to the document's version. You rarely need to pass `schema=` to `validate_document` — the default is `doc.schema`.

## Schema methods worth knowing

```python
--8<-- "agent_references/snippets/schema-and-validation.py:schema-methods"
```

The reference-list machinery (`get_field_object_list` / `get_types_providing_reference`) is what powers automatic cross-reference tracking. See [reference-tracking.md](reference-tracking.md).

## Validating a document

```python
--8<-- "agent_references/snippets/schema-and-validation.py:validate"
```

`ValidationResult` is truthy when `is_valid` is `True`. Use it as a gate:

```python
--8<-- "agent_references/snippets/schema-and-validation.py:validate-gate"
```

## Scoping a validation

Skip categories of checks when you're iterating quickly, or restrict to a subset of types:

```python
--8<-- "agent_references/snippets/schema-and-validation.py:scope"
```

## Validating a single object

For tight inner loops or interactive workflows, `validate_object` skips reference checks (which require a whole-document view):

```python
--8<-- "agent_references/snippets/schema-and-validation.py:validate-object"
```

## Error codes

Common codes (see `ValidationError.code`):

- `E001` — required field missing or blank
- `E002` — value matches none of a field's permitted types
- `E003` — type mismatch on a single-typed field
- `E004` — value not among a field's permitted values
- `E005` — below the minimum; `E006` — not above an exclusive minimum
- `E007` — above the maximum; `E008` — not below an exclusive maximum
- `E009` — reference to a name no object declares. The message quotes the value as typed, the reference list it was looked up in and the closest declared names: `Reference to non-existent object 'Opaqe' (looked up in ConstructionNames). Did you mean 'Opaque'?` A name that exists but is the wrong type for the field is `E009` too: `Reference to 'Office', which is a Zone, not in ScheduleNames`. A related type EnergyPlus also accepts there (a window where the list is `SurfaceNames`) passes. A part or a grouping of the accepted type does not: a `Schedule:Day:*` or `Schedule:Week:*` where the list is `ScheduleNames`, or a `ZoneList` where it is `ZoneNames`.
- `E010` — singleton constraint violated (>1 instance of a `maxProperties: 1` type)
- `E011` — a `Schedule:Compact` that does not cover the year through `12/31`, or a day through `Until: 24:00`; EnergyPlus stops on it
- `E012` — a `Schedule:Compact` or `Schedule:Constant` value outside the lower or upper limit of its `ScheduleTypeLimits` (reported with `check_ranges`); EnergyPlus stops on it
- `E013` — a window, glass door or tubular daylighting surface (`FenestrationSurface:Detailed` other than a `Door`, including one with no surface type, `Window`, `GlazedDoor`, `Window:Interzone`, `GlazedDoor:Interzone`) whose `Construction` has only opaque layers and no `WindowMaterial:*` layer (reported with `check_references`); EnergyPlus stops on it
- `W002` — unknown object type; `W003` — unknown field
- `W004` — an `Output:Diagnostics`, `Output:Table:SummaryReports`, `OutdoorAir:NodeList` or `EnergyManagementSystem:GlobalVariable` with no entries, or only blank ones: it does nothing in EnergyPlus, and its IDF (`Type,;`) is read as one blank entry. Reported by `validate_document` only, so `add()` still accepts one to fill in later.

- `W005` — a floor whose vertex order makes it face up, or a roof or ceiling that faces down (reported with `check_geometry`), read under `GlobalGeometryRules`' entry direction. Its vertices are reversed, as a clockwise footprint extruded by hand gives; EnergyPlus runs it with only an "upside down" warning and a wrong zone volume.

These codes are stable; agents and CI checks can filter on them.

Types without a Name field (`HVACTemplate:Zone:*`, `Output:Variable`, `Timestep`, ...) have an empty `obj_name`. Use `err.obj` to find, highlight or fix the object; `str(err)` and `repr(obj)` name it by its first set field, `HVACTemplate:Zone:IdealLoadsAirSystem(zone_name='B')`:

```python
--8<-- "agent_references/snippets/schema-and-validation.py:nameless-issue"
```

A field yields at most one finding. Where a field admits several types, for example a number or the
literal `Autosize`, the value is judged against each permitted form in turn: it is accepted as soon
as one form fits completely, and otherwise the finding describes the closest form's failure. So an
out-of-range number reports `E007` rather than `E002`, which would only say that a number is not a
number.

## Introspecting the schema

`ObjectDescription` and `FieldDescription` are higher-level views over the raw JSON Schema:

```python
--8<-- "agent_references/snippets/schema-and-validation.py:introspect"
```

`FieldDescription` exposes `name, field_type, required, default, units, enum_values, minimum, maximum, exclusive_minimum, exclusive_maximum, note, is_reference, object_list`. There is no `range` aggregate — pull `minimum`/`maximum` (and the `exclusive_*` variants for open intervals) directly.

## Common mistakes

!!! failure "running a simulation without validating first"

    ```python
    result = simulate(doc, "weather.epw")      # may fail mid-simulation with cryptic .err output
    ```

!!! success "gate the simulation on validation"

    ```python
    --8<-- "agent_references/snippets/schema-and-validation.py:mistake-validate-good"
    ```

!!! failure "assuming a field exists without checking the schema"

    ```python
    zone.fictional_field = 1.0                 # InvalidFieldError in strict mode; a type error too
    ```

!!! success "ask the schema, then use item access for a name chosen at run time"

    ```python
    --8<-- "agent_references/snippets/schema-and-validation.py:mistake-schema-good"
    ```

!!! failure "caching a schema across versions"

    ```python
    schema = get_schema((24, 1, 0))            # cached
    doc = load_idf("v25_model.idf")            # version (25, 2, 0)
    validate_document(doc, schema=schema)      # wrong schema — false errors
    ```

!!! success "let the document carry its own schema"

    ```python
    --8<-- "agent_references/snippets/schema-and-validation.py:mistake-version-good"
    ```

## Related

- [reference-tracking.md](reference-tracking.md) — the reference machinery built on top of schema metadata.
- [document-and-objects.md](document-and-objects.md) — using schema info to author objects.
- [version-migration.md](version-migration.md) — when the schema changes between versions.
- API docs: [py.idfkit.com/api/validation/](https://py.idfkit.com/api/validation/) and [py.idfkit.com/api/schema/](https://py.idfkit.com/api/schema/)
