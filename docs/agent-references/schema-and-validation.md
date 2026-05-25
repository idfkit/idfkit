# Schema and validation

idfkit bundles the official EnergyPlus epJSON schema for every supported version (8.9 → 26.1). The schema drives field metadata (types, ranges, defaults, references) and on-demand validation. Use it for introspection ("what fields does `Zone` have?") and for catching errors before you hand a model to EnergyPlus.

## When to use

- You're authoring a model and want to know what fields and types an object accepts.
- You've finished editing and want a single pre-flight check before simulating.
- You want to look up the EnergyPlus group, memo, or required fields for an object type.

## Quick start

```python
--8<-- "docs/snippets/agent_references/schema-and-validation.py:quickstart"
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
--8<-- "docs/snippets/agent_references/schema-and-validation.py:schema-methods"
```

The reference-list machinery (`get_field_object_list` / `get_types_providing_reference`) is what powers automatic cross-reference tracking. See [reference-tracking.md](reference-tracking.md).

## Validating a document

```python
--8<-- "docs/snippets/agent_references/schema-and-validation.py:validate"
```

`ValidationResult` is truthy when `is_valid` is `True`. Use it as a gate:

```python
--8<-- "docs/snippets/agent_references/schema-and-validation.py:validate-gate"
```

## Scoping a validation

Skip categories of checks when you're iterating quickly, or restrict to a subset of types:

```python
--8<-- "docs/snippets/agent_references/schema-and-validation.py:scope"
```

## Validating a single object

For tight inner loops or interactive workflows, `validate_object` skips reference checks (which require a whole-document view):

```python
--8<-- "docs/snippets/agent_references/schema-and-validation.py:validate-object"
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
--8<-- "docs/snippets/agent_references/schema-and-validation.py:introspect"
```

`FieldDescription` exposes `name, field_type, required, default, units, enum_values, minimum, maximum, exclusive_minimum, exclusive_maximum, note, is_reference, object_list`. There is no `range` aggregate — pull `minimum`/`maximum` (and the `exclusive_*` variants for open intervals) directly.

## Common mistakes

**BAD — running a simulation without validating first**

```python
result = simulate(doc, "weather.epw")      # may fail mid-simulation with cryptic .err output
```

**GOOD — gate the simulation on validation**

```python
--8<-- "docs/snippets/agent_references/schema-and-validation.py:mistake-validate-good"
```

**BAD — assuming a field exists without checking the schema**

```python
zone.fictional_field = 1.0                 # InvalidFieldError in strict mode
```

**GOOD — ask the schema**

```python
--8<-- "docs/snippets/agent_references/schema-and-validation.py:mistake-schema-good"
```

**BAD — caching a schema across versions**

```python
schema = get_schema((24, 1, 0))            # cached
doc = load_idf("v25_model.idf")            # version (25, 2, 0)
validate_document(doc, schema=schema)      # wrong schema — false errors
```

**GOOD — let the document carry its own schema**

```python
--8<-- "docs/snippets/agent_references/schema-and-validation.py:mistake-version-good"
```

## Related

- [reference-tracking.md](reference-tracking.md) — the reference machinery built on top of schema metadata.
- [document-and-objects.md](document-and-objects.md) — using schema info to author objects.
- [version-migration.md](version-migration.md) — when the schema changes between versions.
- API docs: [py.idfkit.com/api/validation/](https://py.idfkit.com/api/validation/) and [py.idfkit.com/api/schema/](https://py.idfkit.com/api/schema/)
