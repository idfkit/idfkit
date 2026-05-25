# Parsing IDF and epJSON

idfkit reads both EnergyPlus formats — classic `.idf` and `.epJSON` — through a single document model. Pick the loader that matches the file extension. Both return an `IDFDocument` with identical semantics afterwards.

## When to use

- You have a `.idf` or `.epJSON` file on disk and want to query or modify it.
- You need to detect the EnergyPlus version of an existing file.
- You need lossless round-tripping (write the file back byte-identical when unchanged).
- You're migrating off eppy and want a drop-in `IDF(...)` replacement (see `idfkit._compat`).

## Quick start

```python
--8<-- "docs/snippets/agent_references/parsing-idf-epjson.py:quickstart"
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
--8<-- "docs/snippets/agent_references/parsing-idf-epjson.py:strict-mode"
```

Drop to `strict=False` only as a tolerant fallback for legacy or noisy files:

```python
--8<-- "docs/snippets/agent_references/parsing-idf-epjson.py:strict-false"
```

## Strict parsing (the default)

`strict_parsing=True` makes the IDF tokenizer fail fast on malformed objects (missing semicolons, truncated lines, unbalanced quotes) by raising `IDFParseError`. Set `strict_parsing=False` if you need to load a noisy file and inspect the diagnostics:

```python
--8<-- "docs/snippets/agent_references/parsing-idf-epjson.py:strict-parsing"
```

## Version handling

Every document is tied to a specific EnergyPlus version. The parser reads the `Version` object and picks the matching bundled schema (8.9 through 26.1 — see `idfkit.ENERGYPLUS_VERSIONS`).

```python
--8<-- "docs/snippets/agent_references/parsing-idf-epjson.py:version"
```

Override the version when the file is missing or wrong:

```python
--8<-- "docs/snippets/agent_references/parsing-idf-epjson.py:version-override"
```

If the file references a version idfkit doesn't bundle, you'll get `VersionNotFoundError`. To upgrade, see [version-migration.md](version-migration.md).

## Lossless round-trips

For workflows that mutate a handful of objects and want to preserve every byte of whitespace, comments, and formatting elsewhere in the file, pass `preserve_formatting=True`:

```python
--8<-- "docs/snippets/agent_references/parsing-idf-epjson.py:preserve"
```

Internally this builds a Concrete Syntax Tree (CST) at parse time and re-emits the original source for objects you didn't touch. Mutated objects are reformatted using the standard writer. See [writing-output.md](writing-output.md) for the writer side.

## Format conversion

To convert between IDF and epJSON, load with one function and write with the other:

```python
--8<-- "docs/snippets/agent_references/parsing-idf-epjson.py:convert"
```

Or use the explicit converters:

```python
--8<-- "docs/snippets/agent_references/parsing-idf-epjson.py:convert-explicit"
```

## Bulk loading

For batch workflows, preload the schema once and pass it to every `IDFParser` so files of the same version share the cache:

```python
--8<-- "docs/snippets/agent_references/parsing-idf-epjson.py:bulk"
```

## Common mistakes

**BAD — silent typos in non-strict mode**

```python
doc = load_idf("building.idf", strict=False)
zone.x_orign = 10.0                        # silently dropped on the floor
write_idf(doc, "out.idf")                  # x_origin unchanged
```

**GOOD — keep strict mode on for authoring**

```python
--8<-- "docs/snippets/agent_references/parsing-idf-epjson.py:mistake-strict-good"
```

**BAD — guessing the version on legacy files**

```python
doc = load_idf("legacy.idf")               # may raise VersionNotFoundError
```

**GOOD — explicitly migrate before loading**

```python
--8<-- "docs/snippets/agent_references/parsing-idf-epjson.py:mistake-version-good"
```

**BAD — forgetting `preserve_formatting` for the writer side**

```python
doc = load_idf("building.idf")             # no CST → format-only writer
write_idf(doc, "out.idf")                  # not byte-identical, even with no edits
```

**GOOD — pair load + write**

```python
--8<-- "docs/snippets/agent_references/parsing-idf-epjson.py:mistake-preserve-good"
```

## Related

- [document-and-objects.md](document-and-objects.md) — what you do with a document once parsed.
- [writing-output.md](writing-output.md) — serializing back out.
- [version-migration.md](version-migration.md) — upgrading legacy files.
- API docs: [py.idfkit.com/api/parser/](https://py.idfkit.com/api/parser/)
