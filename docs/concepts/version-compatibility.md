# Version Compatibility Checking

idfkit includes a built-in compatibility checker that detects cross-version
breakage in Python scripts caused by EnergyPlus schema changes. This is useful
when migrating models between EnergyPlus versions, or when maintaining code that
must work across multiple versions.

The checker analyses Python source files using the AST (no code execution) and
compares extracted string literals against the bundled epJSON schemas for
different EnergyPlus versions.

## What it detects

| Code | Description |
|------|-------------|
| `C001` | Object type exists in one schema version but not another |
| `C002` | Enumerated choice value for a field exists in one version but not another |

## CLI usage

The `idfkit check-compat` command checks one or more Python files:

### Check migration between two versions

```bash
idfkit check-compat my_model.py --from 24.2 --to 25.1
```

### Check against multiple target versions

```bash
idfkit check-compat my_model.py --targets 24.1,24.2,25.1
```

### Machine-readable JSON output (for CI)

```bash
idfkit check-compat my_model.py --from 24.2 --to 25.1 --json
```

### Exit codes

| Code | Meaning |
|------|---------|
| `0` | No compatibility issues found |
| `1` | One or more compatibility issues found |
| `2` | Usage error (bad arguments, missing file, etc.) |

## Library API

You can also use the checker programmatically:

```python
from idfkit.compat import check_compatibility

source = open("my_script.py").read()
diagnostics = check_compatibility(
    source,
    filename="my_script.py",
    targets=[(24, 2, 0), (25, 1, 0)],
)

for d in diagnostics:
    print(d)
    # my_script.py:12:5: C001 [warning] Object type 'Foo' not found in 25.1.0 (exists in 24.2.0)
```

### Working with schema diffs directly

For lower-level access, use the schema diffing API:

```python
from idfkit.compat import build_schema_index, diff_schemas
from idfkit import get_schema

idx_old = build_schema_index(get_schema((24, 1, 0)))
idx_new = build_schema_index(get_schema((25, 2, 0)))

diff = diff_schemas(idx_old, idx_new)
print(f"Removed types: {diff.removed_types}")
print(f"Added types: {diff.added_types}")

for (obj_type, field), removed in diff.removed_choices.items():
    print(f"  {obj_type}.{field}: removed choices {removed}")
```

## Diagnostic structure

Each diagnostic is a frozen dataclass with these fields:

| Field | Type | Description |
|-------|------|-------------|
| `code` | `str` | Machine-readable code (e.g. `"C001"`) |
| `message` | `str` | Human-readable description |
| `severity` | `CompatSeverity` | `WARNING` or `ERROR` |
| `filename` | `str` | Source file path |
| `line` | `int` | 1-based line number |
| `col` | `int` | 0-based column offset |
| `end_col` | `int` | 0-based end column offset |
| `from_version` | `str` | Version where the literal is valid |
| `to_version` | `str` | Version where the literal is invalid |
| `suggested_fix` | `str \| None` | Optional suggested replacement |

Call `diagnostic.to_dict()` to get a plain dictionary suitable for JSON
serialisation.

## Detected patterns

The checker extracts string literals from these Python AST patterns:

- **`doc.add("ObjectType", ...)`** -- the first positional argument is treated
  as an EnergyPlus object type.
- **`doc.add("ObjectType", field="value")`** -- keyword argument string values
  are checked against the field's enumerated choices in the schema.
- **`doc.add("ObjectType", "Name", {"field": "value"})`** -- string values in a
  dict literal argument are also checked.
- **`doc["ObjectType"]`** -- subscript access is checked when the file imports
  from `idfkit`.

Dynamic strings, f-strings, and variable references are intentionally ignored to
keep false positives low.
