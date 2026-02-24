# Version Compatibility Linting

idfkit includes a built-in **compatibility linter** that statically analyses
Python source files and detects cross-version breakage caused by EnergyPlus
schema changes. This is useful when migrating models between EnergyPlus
versions, or when maintaining code that must work across multiple versions.

The linter parses Python source files using the AST (no code execution) and
compares extracted string literals against the bundled epJSON schemas for
different EnergyPlus versions.

## What it detects

| Code | Description |
|------|-------------|
| `C001` | Object type exists in one schema version but not another |
| `C002` | Enumerated choice value for a field exists in one version but not another |

## CLI usage

The `idfkit check` command lints one or more Python files.

### Lint migration between two versions

```bash
idfkit check my_model.py --from 24.2 --to 25.1
```

### Lint against multiple target versions

```bash
idfkit check my_model.py --targets 24.1,24.2,25.1
```

### Machine-readable JSON output (for CI)

```bash
idfkit check my_model.py --from 24.2 --to 25.1 --json
```

### SARIF output (for GitHub Code Scanning / VS Code)

```bash
idfkit check my_model.py --from 24.2 --to 25.1 --sarif
```

SARIF (Static Analysis Results Interchange Format) output can be consumed by:

- **GitHub Code Scanning** — upload via `github/codeql-action/upload-sarif`
- **VS Code** — install the [SARIF Viewer](https://marketplace.visualstudio.com/items?itemName=MS-SarifVSCode.sarif-viewer) extension
- Any SARIF 2.1.0-compatible tool

### Rule selection

Use `--select` and `--ignore` to control which lint rules are reported, similar
to ruff's rule selection:

```bash
# Only report object-type issues
idfkit check my_model.py --from 24.2 --to 25.1 --select C001

# Suppress choice-value warnings
idfkit check my_model.py --from 24.2 --to 25.1 --ignore C002
```

### Group filtering

EnergyPlus object types are organised into IDD groups (e.g. *Thermal Zones
and Surfaces*, *Surface Construction Elements*, *HVAC Templates*). You can
scope the linter to specific groups or exclude groups you don't care about:

```bash
# Only lint HVAC-related objects
idfkit check my_model.py --from 24.2 --to 25.1 \
    --group "HVAC Templates,HVAC Design Objects"

# Skip detailed ground heat transfer objects
idfkit check my_model.py --from 24.2 --to 25.1 \
    --exclude-group "Detailed Ground Heat Transfer"
```

### Severity filtering

By default all diagnostics are reported. Use `--severity` to set a minimum
threshold:

```bash
# Only report errors, suppress warnings
idfkit check my_model.py --from 24.2 --to 25.1 --severity error
```

### Exit codes

| Code | Meaning |
|------|---------|
| `0` | No compatibility issues found |
| `1` | One or more compatibility issues found |
| `2` | Usage error (bad arguments, missing file, etc.) |

### Complete flag reference

| Flag | Description |
|------|-------------|
| `FILE ...` | Python file(s) to lint (positional, required) |
| `--from VERSION` | Source EnergyPlus version (e.g. `24.2`) |
| `--to VERSION` | Target EnergyPlus version (required with `--from`) |
| `--targets VERSIONS` | Comma-separated target versions (alternative to `--from`/`--to`) |
| `--json` | Output diagnostics as JSON |
| `--sarif` | Output diagnostics as SARIF 2.1.0 |
| `--select CODES` | Only report these lint rule codes (e.g. `C001,C002`) |
| `--ignore CODES` | Suppress these lint rule codes (e.g. `C002`) |
| `--group GROUPS` | Only lint object types in these IDD groups |
| `--exclude-group GROUPS` | Exclude object types in these IDD groups |
| `--severity LEVEL` | Minimum severity: `warning` or `error` |

## Pre-commit integration

idfkit ships a [pre-commit](https://pre-commit.com/) hook so you can run the
compatibility linter automatically on every commit.

### Setup

Add the following to your `.pre-commit-config.yaml`:

```yaml
repos:
  - repo: https://github.com/samuelduchesne/idfkit
    rev: v0.1.0  # pin to a release tag
    hooks:
      - id: idfkit-check
        args: ["--from", "24.2", "--to", "25.1"]
```

Then install the hook:

```bash
pre-commit install
```

### Customising the hook

You can pass any of the CLI flags described above via the `args` key:

```yaml
hooks:
  - id: idfkit-check
    args:
      - "--targets"
      - "24.1,24.2,25.1,25.2"
      - "--ignore"
      - "C002"
      - "--group"
      - "Thermal Zones and Surfaces"
```

The hook runs on Python files by default. To restrict it to specific paths, use
the standard pre-commit `files` filter:

```yaml
hooks:
  - id: idfkit-check
    args: ["--from", "24.2", "--to", "25.1"]
    files: ^src/.*\.py$
```

### CI usage with SARIF

For GitHub Actions, you can upload SARIF results to Code Scanning:

```yaml
# .github/workflows/lint.yml
jobs:
  compat-lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: astral-sh/setup-uv@v5
      - run: uv sync
      - run: uv run idfkit check src/ --from 24.2 --to 25.1 --sarif > results.sarif
        continue-on-error: true
      - uses: github/codeql-action/upload-sarif@v3
        with:
          sarif_file: results.sarif
```

## Library API

You can also use the linter programmatically:

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

### Group filtering via the library API

```python
diagnostics = check_compatibility(
    source,
    filename="my_script.py",
    targets=[(24, 2, 0), (25, 1, 0)],
    include_groups={"Thermal Zones and Surfaces"},
)
```

### SARIF output via the library API

```python
from idfkit.compat import check_compatibility, format_sarif

diagnostics = check_compatibility(source, "my_script.py", targets=[(24, 2, 0), (25, 1, 0)])
sarif_json = format_sarif(diagnostics)
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

The linter extracts string literals from these Python AST patterns:

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
