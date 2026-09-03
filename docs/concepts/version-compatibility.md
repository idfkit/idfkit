# How to work across EnergyPlus versions

idfkit supports 17 EnergyPlus releases, and their schemas disagree: object types
come and go, and enumerated choice values are renamed under you. A viewer, a
converter, or anything else that opens files it did not write cannot hard-code
`26.1.0`, and code that runs against more than one release cannot assume the
names it was written with still exist.

Neither failure is loud. Reading an IDF against the wrong schema does not throw,
because IDF is positional: a field-order difference mis-maps values into
neighbouring slots and the parse "succeeds" with a corrupted model. A choice
value that was removed two releases ago is just a string until EnergyPlus
rejects it.

This guide covers both defences. At load time, let the library resolve the
version out of the file. Before you ship or migrate, lint your source against
the versions you claim to support.

!!! tip "Linting is not migration"
    Everything here is static or read-only: it tells you what would break. To
    actually upgrade a model, see [how to migrate models between
    versions](../simulation/migrating-versions.md), which covers the sibling
    `idfkit migrate` CLI and the `idfkit.migrate()` API, both driving the
    `IDFVersionUpdater` transition binaries.

## Let the loader read the version out of the file

The loading entry points detect the version themselves, resolve it against the
schemas they have, and fail with a useful message when there is no match. For a
file on disk, this is the whole story.

=== "Python"

    ```python
    from idfkit import load_idf

    model = load_idf("whatever.idf")
    model.version  # (9, 0, 1), say
    ```

=== "TypeScript"

    ```ts
    --8<-- "docs/snippets/js/concepts/version-compatibility/let_the_loader_read_the_version_out_of_the_file.ts:example"
    ```

The version each library reports is spelled the way its ecosystem spells
versions: a `(major, minor, patch)` tuple in Python, a string in TypeScript.
`idfkit.version_string()` renders the tuple when you need the string form.

What happens to a version that is not one of the 17 also differs, and the
difference is worth knowing before you rely on either. Python falls back to the
newest supported release at or below the detected one, so a file claiming
`24.1.5` is read with the `24.1.0` schema, and only a version older than every
bundled schema raises `SchemaNotFoundError`. TypeScript's `resolveVersion`
matches on major and minor and takes the newest patch, and returns nothing at
all when no release shares that major and minor, so the load throws rather than
guessing.

## Detect, resolve, and load text you obtained some other way

Text fetched over the network, pulled out of a database, or pasted into an
editor never reaches a loader that could read it off disk. In TypeScript, take
the three steps yourself, because each fails differently:

```ts
--8<-- "docs/snippets/js/concepts/version-compatibility/detect_resolve_and_load_text_you_obtained_some_other_way.ts:example"
```

`resolveVersion` exists because IDF files write `Version, 9.0;` while schemas are
keyed `9.0.1`. In Node, `schemaFor` is the same three steps behind one call:

```ts
--8<-- "docs/snippets/js/concepts/version-compatibility/detect_resolve_and_load_text_you_obtained_some_other_way_2.ts:example"
```

Python has no equivalent, because it has nothing to resolve. Its parsers take a
path, `get_schema(version)` returns the schema synchronously from the package's
own files, and `load_idf()` already chains the two. Write the text to a file and
load it.

## Files with no `Version` object

Fragments, snippets, and hand-written test inputs often carry none. Pass the
version explicitly:

=== "Python"

    ```python
    from idfkit import load_idf

    model = load_idf("fragment.idf", version=(26, 1, 0))
    ```

=== "TypeScript"

    ```ts
    --8<-- "docs/snippets/js/concepts/version-compatibility/files_with_no_version_object.ts:example"
    ```

An explicit version overrides detection entirely, so it doubles as a "parse this
as if it were 26.1" escape hatch. Use it knowingly: that is precisely the
mis-mapping the resolution logic exists to prevent. Python rejects a version
that is not a known EnergyPlus release with `UnsupportedVersionError`, and
raises `VersionNotFoundError` when detection finds nothing and you passed
nothing; TypeScript's `getIdfVersion` returns `undefined` for the same input,
leaving the decision to the caller.

## epJSON works the same way, with its own detector

=== "Python"

    ```python
    from idfkit import load_epjson

    model = load_epjson("whatever.epJSON")
    ```

=== "TypeScript"

    ```ts
    --8<-- "docs/snippets/js/concepts/version-compatibility/epjson_works_the_same_way_with_its_own_detector.ts:example"
    ```

## Hold one schema source when you work across versions

A document is bound to one version for its lifetime. There is no
version-agnostic mode, because field order and reference lists genuinely differ
between releases, so working across versions means holding several documents,
not one flexible one.

Keep a single schema source for all of them. Python's `get_schema()` goes
through a process-wide `SchemaManager` that caches every version it has loaded,
so repeat calls are free. TypeScript's `SchemaBundle` shares one blob store
across versions: loading a second version pays only for the definitions it does
not already share with the first, and the definitions common to both are the
same frozen object. Hold one bundle for the lifetime of the process rather than
constructing one per file. See [Content-addressed
schemas](../explanation/content-addressed-schemas.md) for why that works.

## Lint your source before you migrate

The rest of this page is Python only. `idfkit check` statically analyses Python
source and reports literals that will not survive a move to another EnergyPlus
version. It parses with the AST and executes nothing, then compares the string
literals it extracted against the bundled epJSON schemas for the versions you
name. There is no TypeScript counterpart: generated type packages such as
`@idfkit/types-v26-1` catch the same class of mistake at compile time instead.

### What it detects

| Code | Description |
|------|-------------|
| `C001` | Object type exists in one schema version but not another |
| `C002` | Enumerated choice value for a field exists in one version but not another |

The linter extracts string literals from these AST patterns:

- `doc.add("ObjectType", ...)`: the first positional argument is treated as an
  EnergyPlus object type.
- `doc.add("ObjectType", field="value")`: keyword argument string values are
  checked against the field's enumerated choices in the schema.
- `doc.add("ObjectType", "Name", {"field": "value"})`: string values in a dict
  literal argument are also checked.
- `doc["ObjectType"]`: subscript access is checked when the file imports from
  `idfkit`.

Dynamic strings, f-strings, and variable references are ignored on purpose, to
keep false positives low.

### Lint between two versions, or against several

```bash
# One migration
idfkit check my_model.py --from 24.2 --to 25.1

# Several target versions at once
idfkit check my_model.py --targets 24.1,24.2,25.1
```

### Emit machine-readable output for CI

```bash
idfkit check my_model.py --from 24.2 --to 25.1 --json
idfkit check my_model.py --from 24.2 --to 25.1 --sarif
```

SARIF (Static Analysis Results Interchange Format) 2.1.0 output is consumed by:

- **GitHub Code Scanning**, uploaded via `github/codeql-action/upload-sarif`
- **VS Code**, with the [SARIF
  Viewer](https://marketplace.visualstudio.com/items?itemName=MS-SarifVSCode.sarif-viewer)
  extension
- any other SARIF 2.1.0-compatible tool

### Narrow what gets reported

`--select` and `--ignore` control which rules fire, the way ruff's do:

```bash
# Only report object-type issues
idfkit check my_model.py --from 24.2 --to 25.1 --select C001

# Suppress choice-value warnings
idfkit check my_model.py --from 24.2 --to 25.1 --ignore C002
```

EnergyPlus object types are organised into IDD groups (*Thermal Zones and
Surfaces*, *Surface Construction Elements*, *HVAC Templates*, and so on), which
scope the linter further:

```bash
# Only lint HVAC-related objects
idfkit check my_model.py --from 24.2 --to 25.1 \
    --group "HVAC Templates,HVAC Design Objects"

# Skip detailed ground heat transfer objects
idfkit check my_model.py --from 24.2 --to 25.1 \
    --exclude-group "Detailed Ground Heat Transfer"
```

By default every diagnostic is reported. `--severity` sets a minimum:

```bash
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

### Run the linter on every commit

idfkit ships a [pre-commit](https://pre-commit.com/) hook. Add it to your
`.pre-commit-config.yaml`, then `pre-commit install`:

```yaml
repos:
  - repo: https://github.com/idfkit/idfkit
    rev: v0.1.0  # pin to a release tag
    hooks:
      - id: idfkit-check
        args: ["--from", "24.2", "--to", "25.1"]
```

Any CLI flag above goes in `args`, and the standard pre-commit `files` filter
restricts which paths are linted. The hook runs on Python files by default.

```yaml
hooks:
  - id: idfkit-check
    args:
      - "--targets"
      - "24.1,24.2,25.1,25.2,26.1"
      - "--ignore"
      - "C002"
      - "--group"
      - "Thermal Zones and Surfaces"
    files: ^src/.*\.py$
```

For GitHub Actions, upload the SARIF results to Code Scanning:

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

### Call the linter from Python

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

Group filtering and SARIF formatting are available the same way:

```python
from idfkit.compat import check_compatibility, format_sarif

diagnostics = check_compatibility(
    source,
    filename="my_script.py",
    targets=[(24, 2, 0), (25, 1, 0)],
    include_groups={"Thermal Zones and Surfaces"},
)
sarif_json = format_sarif(diagnostics)
```

Each diagnostic is a frozen dataclass:

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
| `suggested_fix` | <code>str &#124; None</code> | Optional suggested replacement |

Call `diagnostic.to_dict()` for a plain dictionary suitable for JSON
serialisation.

### Diff two schemas directly

For lower-level access, skip the linter and compare the schemas:

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

## See also

- [How to migrate models between EnergyPlus versions](../simulation/migrating-versions.md)
  for upgrading an existing model rather than checking one
- [Supported versions](../reference/versions.md) for the 17 releases and how a
  file's version is matched to a schema
- [Content-addressed schemas](../explanation/content-addressed-schemas.md) for
  why holding several versions at once is cheap
- [Type safety](type-safety.md) for catching the same class of mistake in an
  editor
