# Parsing IDF and epJSON

idfkit reads both EnergyPlus formats — classic `.idf` and `.epJSON` — through a single document model. Pick the loader that matches the file extension. Both return an `IDFDocument` with identical semantics afterwards.

## When to use

- You have a `.idf` or `.epJSON` file on disk and want to query or modify it.
- You need to detect the EnergyPlus version of an existing file.
- You need lossless round-tripping (write the file back byte-identical when unchanged).
- You're migrating off eppy and want a drop-in `IDF(...)` replacement (see `idfkit._compat`).

## Quick start

```python
from idfkit import load_idf, load_epjson

doc = load_idf("building.idf")
doc = load_epjson("building.epJSON")
print(doc.version)  # e.g. (25, 2, 0)
print(len(doc), "objects")
```

## Core API

| Symbol | Purpose |
|---|---|
| `load_idf(path, *, strict=True, strict_parsing=True, preserve_formatting=False)` | Parse a `.idf` file. |
| `load_epjson(path, *, strict=True, preserve_formatting=False)` | Parse an `.epJSON` file. |
| `parse_idf(path, ...)` | Lower-level callable used by `load_idf`. |
| `parse_epjson(path, ...)` | Lower-level callable used by `load_epjson`. |
| `get_idf_version(path)` | Read the version from an IDF file without parsing the rest. |
| `IDFParser` | Reusable parser with caching across files of the same version. |

## Strict mode (the default)

`strict=True` makes any attempt to access or set an unknown field name raise `InvalidFieldError`. This is what you want 99% of the time — it catches typos and version-mismatched field names at the call site.

```python
doc = load_idf("building.idf")  # strict=True by default
zone = doc["Zone"]["Office"]
zone.x_origin  # OK
zone.x_orign  # raises InvalidFieldError
```

Drop to `strict=False` only as a tolerant fallback for legacy or noisy files:

```python
doc = load_idf("legacy.idf", strict=False)
zone.x_orign  # returns None, no error
```

## Strict parsing (the default)

`strict_parsing=True` makes the IDF tokenizer fail fast on malformed objects (missing semicolons, truncated lines, unbalanced quotes) by raising `IDFParseError`. Set `strict_parsing=False` if you need to load a noisy file and inspect the diagnostics:

```python
from idfkit.exceptions import IDFParseError

try:
    doc = load_idf("noisy.idf", strict_parsing=False)
except IDFParseError as e:
    for d in e.diagnostics:
        print(d.line, d.column, d.message)
```

## Version handling

Every document is tied to a specific EnergyPlus version. The parser reads the `Version` object and picks the matching bundled schema (8.9 through 26.1 — see `idfkit.ENERGYPLUS_VERSIONS`).

```python
from idfkit import get_idf_version

version = get_idf_version("building.idf")  # (25, 2, 0)
```

Override the version when the file is missing or wrong:

```python
doc = load_idf("legacy.idf", version=(9, 6, 0))
```

If the file references a version idfkit doesn't bundle, you'll get `VersionNotFoundError`. To upgrade, see [version-migration.md](version-migration.md).

## Lossless round-trips

For workflows that mutate a handful of objects and want to preserve every byte of whitespace, comments, and formatting elsewhere in the file, pass `preserve_formatting=True`:

```python
from idfkit import load_idf, write_idf

doc = load_idf("building.idf", preserve_formatting=True)
doc["Zone"]["Office"].x_origin = 10.0
write_idf(doc, "modified.idf")  # unmodified objects render byte-identical
```

Internally this builds a Concrete Syntax Tree (CST) at parse time and re-emits the original source for objects you didn't touch. Mutated objects are reformatted using the standard writer. See [writing-output.md](writing-output.md) for the writer side.

## Format conversion

To convert between IDF and epJSON, load with one function and write with the other:

```python
from idfkit import load_idf, write_epjson

doc = load_idf("building.idf")
write_epjson(doc, "building.epJSON")
```

Or use the explicit converters:

```python
from idfkit.writers import convert_idf_to_epjson, convert_epjson_to_idf

convert_idf_to_epjson("building.idf", "building.epJSON")
convert_epjson_to_idf("building.epJSON", "building.idf")
```

## Bulk loading

For batch workflows, preload the schema once and pass it to every `IDFParser` so files of the same version share the cache:

```python
from idfkit import IDFParser
from idfkit.schema import get_schema

schema = get_schema((25, 2, 0))
docs = [IDFParser(Path(p), schema=schema).parse() for p in input_paths]
```

## Common mistakes

!!! failure "silent typos in non-strict mode"

    ```python
    doc = load_idf("building.idf", strict=False)
    zone.x_orign = 10.0                        # silently dropped on the floor
    write_idf(doc, "out.idf")                  # x_origin unchanged
    ```

!!! success "keep strict mode on for authoring"

    ```python
    doc = load_idf("building.idf")  # strict=True
    zone.x_origin = 10.0
    ```

!!! failure "guessing the version on legacy files"

    ```python
    doc = load_idf("legacy.idf")               # may raise VersionNotFoundError
    ```

!!! success "explicitly migrate before loading"

    ```python
    from idfkit import migrate, load_idf, write_idf

    legacy = load_idf("legacy.idf")
    report = migrate(legacy, target_version=(25, 2, 0))
    if report.success and report.migrated_model is not None:
        doc = report.migrated_model
        write_idf(doc, "legacy_v25.idf")
    ```

!!! failure "forgetting `preserve_formatting` for the writer side"

    ```python
    doc = load_idf("building.idf")             # no CST → format-only writer
    write_idf(doc, "out.idf")                  # not byte-identical, even with no edits
    ```

!!! success "pair load + write"

    ```python
    doc = load_idf("building.idf", preserve_formatting=True)
    write_idf(doc, "out.idf")  # byte-identical
    ```

## Related

- [document-and-objects.md](document-and-objects.md) — what you do with a document once parsed.
- [writing-output.md](writing-output.md) — serializing back out.
- [version-migration.md](version-migration.md) — upgrading legacy files.
- API docs: [py.idfkit.com/api/parser/](https://py.idfkit.com/api/parser/)
