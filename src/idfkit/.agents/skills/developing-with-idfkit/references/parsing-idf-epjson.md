# Parsing IDF and epJSON

idfkit reads both EnergyPlus formats — classic `.idf` and `.epJSON` — through a single document model. Pick the loader that matches the file extension. Both return a document with identical semantics afterwards, typed as `AnyIDFDocument` unless you state its release (see Version handling).

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
| `load_idf(path, version=None, *, as_type=None, since=None, before=None, strict=True, strict_parsing=True, preserve_formatting=False)` | Parse a `.idf` file. Typed `AnyIDFDocument`, or for the release `as_type=` (or the range `since=`/`before=`) names, checked once the file is read. |
| `load_epjson(path, version=None, *, as_type=None, since=None, before=None, strict=True, strict_parsing=True, preserve_formatting=False)` | Parse an `.epJSON` file, typed the same way. |
| `load_idf_with_diagnostics(path, ...)` | `load_idf` that also returns the recoverable parse findings, as a `ParseResult`; takes the same `as_type=`, `since=`, `before=`. |
| `parse_idf(path, ...)` | Lower-level callable used by `load_idf`. |
| `parse_epjson(path, ...)` | Lower-level callable used by `load_epjson`. |
| `get_idf_version(path)` | Read the version from an IDF file without parsing the rest. |
| `IDFParser` | Reusable parser with caching across files of the same version. |

## Strict mode (the default)

`strict=True` makes any attempt to access or set an unknown field name raise `InvalidFieldError`. This is what you want 99% of the time — it catches typos and version-mismatched field names at the call site. On a typed object (`doc["Zone"][...]`) pyright reports an undeclared field name before the code runs, for reading and for assigning.

```python
doc = load_idf("building.idf")  # strict=True by default
zone = doc["Zone"]["Office"]
zone.x_origin  # OK
zone.x_orign  # raises InvalidFieldError, and pyright reports it before the code runs
```

Drop to `strict=False` only as a tolerant fallback for legacy or noisy files:

```python
doc = load_idf("legacy.idf", strict=False)
zone = doc["Zone"]["Office"]
zone.x_orign  # returns None at run time; pyright still reports the name
```

## Strict parsing (the default)

`strict_parsing=True` makes the IDF tokenizer fail fast on malformed objects (missing semicolons, truncated lines, unbalanced quotes) by raising `IDFParseError`. An object missing its `;` before the next object (`Zone, A, 0, 0, 0` then `Material, M;`) is loaded as read, with the next type inside a field, in either mode: a value across two lines is legal IDF. The load logs a warning, and `load_idf_with_diagnostics()` returns a `ParseError` diagnostic at the value's line, `missing ';' ... before 'Material'?`. Set `strict_parsing=False` if you need to load a noisy file and inspect the diagnostics:

```python
from idfkit.exceptions import IDFParseError

try:
    doc = load_idf("noisy.idf", strict_parsing=False)
except IDFParseError as e:
    for d in e.diagnostics:
        print(d.line, d.column, d.message)
```

An object type the schema does not have (`Zonee`) raises `IDFParseError` with the code `UnknownObjectType` from both `load_idf` and `load_epjson`; the epJSON message adds `Did you mean 'Zone'?`. With `strict_parsing=False`, `load_epjson` skips that type and logs a warning.

## Blank fields are unset

A blank IDF field (`, ,`) is an unset field. It is not stored in `obj.data`, it is not written to epJSON, and it reads as `None`, the same as a field cut off by an early semicolon. An explicit `0` is a value and is kept. Assigning `None` or `""` to a field clears it the same way. Writing the document back to IDF and reading it again gives an equal model.

```python
# Zone, Office, 0, 0, 0, 0, , , ;  -- type, multiplier and ceiling height left blank
zone = doc["Zone"]["Office"]
zone.ceiling_height  # None, exactly as if the semicolon had come earlier
"ceiling_height" in zone.data  # False: a blank field is not stored
if zone.ceiling_height is None:
    zone.ceiling_height = "Autocalculate"
```

## Version handling

Every document is tied to a specific EnergyPlus version. The parser reads the `Version` object and picks the matching bundled schema (8.9 through 26.2 — see `idfkit.ENERGYPLUS_VERSIONS`).

```python
from idfkit import get_idf_version

version = get_idf_version("building.idf")  # (25, 2, 0)
```

Override the version when the file is missing or wrong:

```python
doc = load_idf("legacy.idf", version=(9, 6, 0))
```

If the file references a version idfkit doesn't bundle, you'll get `VersionNotFoundError`. To upgrade, see [version-migration.md](version-migration.md).

A type checker cannot read the file, so a loaded document is typed as `AnyIDFDocument`: only the object types, fields and choices every supported release accepts type-check through it, whatever the file's release. To work with a release's own fields and choices, state the release when loading. The loader checks it once the file is read and raises `TypeError`, naming the file, if the file is another release; a malformed target (`since="27.1"`, or both `as_type=` and `since=`) is refused before the file is read:

```python
from idfkit import load_epjson, load_idf, load_idf_with_diagnostics
from idfkit.versioned import IDFDocumentV9_4, IDFDocumentV26_1

model = load_idf("model.idf")  # AnyIDFDocument: what every supported release has
legacy = load_idf("legacy.idf", as_type=IDFDocumentV9_4)  # IDFDocumentV9_4; TypeError unless 9.4
legacy["People"]["Office"].zone_or_zonelist_name = "Office"  # the 9.4 field name
recent = load_epjson("recent.epJSON", since="9.6")  # 9.6 or later: IDFDocumentSince9_6
recent["Space"].first()  # every release from 9.6 on has Space
older = load_idf("older.idf", since="25.2", before="26.2")  # 25.2 or 26.1
result = load_idf_with_diagnostics("hand_edited.idf", as_type=IDFDocumentV26_1)
print(result.document["Zone"].first(), result.diagnostics)  # result.document is IDFDocumentV26_1
```

`as_type=` takes what `as_version` takes: a release's type from `idfkit.versioned` or a tuple of them, whose type argument states the strictness as for `new_document` (`as_type=IDFDocumentV9_4[Literal[False]]` loads a non-strict document); `since=` and `before=` take a release number, its type or a version tuple. The positional `version=` is different: it overrides the release the file is read as, and does not type the document. For a document already loaded, `as_version(doc, IDFDocumentV9_4)` does the same check; see "Typing a document for its EnergyPlus version" in [document-and-objects.md](document-and-objects.md).

## Lossless round-trips

For workflows that mutate a handful of objects and want to preserve every byte of whitespace, comments, and formatting elsewhere in the file, pass `preserve_formatting=True`:

```python
from idfkit import load_idf, save_idf

doc = load_idf("building.idf", preserve_formatting=True)
doc["Zone"]["Office"].x_origin = 10.0
save_idf(doc, "modified.idf")  # unmodified objects render byte-identical
```

Internally this builds a Concrete Syntax Tree (CST) at parse time and re-emits the original source for objects you didn't touch. Mutated objects are reformatted using the standard writer. See [writing-output.md](writing-output.md) for the writer side.

## Format conversion

To convert between IDF and epJSON, load with one function and write with the other:

```python
from idfkit import load_idf, save_epjson

doc = load_idf("building.idf")
save_epjson(doc, "building.epJSON")
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
    save_idf(doc, "out.idf")                   # x_origin unchanged
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
    from idfkit import migrate, load_idf, save_idf

    legacy = load_idf("legacy.idf")
    report = migrate(legacy, target_version=(25, 2, 0))
    if report.success and report.migrated_model is not None:
        doc = report.migrated_model
        save_idf(doc, "legacy_v25.idf")
    ```

!!! failure "testing a blank field against the empty string"

    ```python
    if zone.multiplier == "":                  # never true: a blank field reads as None
        zone.multiplier = 1
    ```

!!! success "test for None"

    ```python
    if zone.multiplier is None:  # blank or never written: both read as None
        ...
    ```

!!! failure "forgetting `preserve_formatting` for the writer side"

    ```python
    doc = load_idf("building.idf")             # no CST → format-only writer
    save_idf(doc, "out.idf")                   # not byte-identical, even with no edits
    ```

!!! success "pair load + save"

    ```python
    doc = load_idf("building.idf", preserve_formatting=True)
    save_idf(doc, "out.idf")  # byte-identical
    ```

## Related

- [document-and-objects.md](document-and-objects.md) — what you do with a document once parsed.
- [writing-output.md](writing-output.md) — serializing back out.
- [version-migration.md](version-migration.md) — upgrading legacy files.
- API docs: [py.idfkit.com/api/parser/](https://py.idfkit.com/api/parser/)
