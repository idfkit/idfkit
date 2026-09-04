# Writing output

idfkit serializes `IDFDocument` to both EnergyPlus formats. Each format has a pair of functions: `write_*` returns the serialized text, `save_*` puts it on disk. Pick the `idf` pair for `.idf` (what `energyplus` expects by default) or the `epjson` pair for the JSON variant.

## When to use

- You've finished editing a document and want to persist it to disk.
- You want an IDF string (without writing to disk) for inspection or testing.
- You're converting between IDF and epJSON.
- You need byte-identical output for unmodified objects (lossless round-trip).

## Quick start

```python
--8<-- "agent_references/snippets/writing-output.py:quickstart"
```

## Core API

| Symbol | Purpose |
|---|---|
| `write_idf(doc, output_type="standard", *, preserve_formatting=None)` | Serialize to IDF and return the text. Never touches the disk. |
| `save_idf(doc, path, encoding="latin-1", output_type="standard", *, preserve_formatting=None)` | Serialize to IDF and write it to `path`. |
| `write_epjson(doc, indent=2, *, preserve_formatting=None)` | Serialize to epJSON and return the text. Never touches the disk. |
| `save_epjson(doc, path, indent=2, *, preserve_formatting=None)` | Serialize to epJSON and write it to `path`. |
| `idfkit.writers.convert_idf_to_epjson(src, dst)` | Convenience converter. |
| `idfkit.writers.convert_epjson_to_idf(src, dst)` | Convenience converter. |
| `IDFWriter(doc, output_type=...)` | Lower-level writer with a `to_string()` method. |
| `EpJSONWriter(doc)` | Lower-level epJSON writer. |

## Output formatting modes

`output_type=` on `write_idf` and `save_idf` mirrors eppy's `idf.outputtype`:

- `"standard"` (default) — full `!- Field Name` comments, one field per line. Best for hand editing.
- `"nocomment"` — one field per line, no comments. Smaller, still diff-friendly.
- `"compressed"` — entire object on one line. Best for parametric runs that produce thousands of files.

```python
--8<-- "agent_references/snippets/writing-output.py:output-type"
```

epJSON formatting is controlled by `indent` (default 2; pass `indent=0` for the most compact form).

## Encoding

EnergyPlus expects `latin-1` for IDF files (that's the `save_idf` default). Don't override unless you have a downstream tool that requires UTF-8 — many EnergyPlus utilities will choke on non-`latin-1` IDFs.

## Lossless round-trips (IDF only)

To preserve every byte of whitespace, comments, and object ordering for objects you didn't touch, pair `load_idf(..., preserve_formatting=True)` with `save_idf(...)`:

```python
--8<-- "agent_references/snippets/writing-output.py:preserve"
```

When `preserve_formatting=None` (the default) and the document has a CST attached (i.e. parsed with `preserve_formatting=True`), the writer auto-detects and uses lossless mode. Setting `output_type="nocomment"` or `"compressed"` disables lossless mode because those modes intentionally reformat every object.

For epJSON, lossless is all-or-nothing: any mutation falls back to the standard writer.

## Mode interactions

| `preserve_formatting` | `output_type` | Behaviour |
|---|---|---|
| `None` (default) | `"standard"` | Lossless if a CST is attached, otherwise standard formatting. |
| `None` (default) | `"nocomment"` / `"compressed"` | Always standard formatting (lossless suppressed). |
| `True` | `"standard"` | Lossless. Raises if no CST is attached. |
| `False` | any | Always standard formatting. |

## Strings vs. files

`write_idf` and `write_epjson` return the serialized string and never touch the disk. Useful for tests:

```python
--8<-- "agent_references/snippets/writing-output.py:string"
```

## Format conversion

```python
--8<-- "agent_references/snippets/writing-output.py:convert"
```

Or in the other direction:

```python
--8<-- "agent_references/snippets/writing-output.py:convert-back"
```

The explicit converters `idfkit.writers.convert_idf_to_epjson` and `convert_epjson_to_idf` skip the round-trip through Python and stream directly between the two formats — use them in scripts that don't need to inspect the document in between.

## Batch writing

If you generate many output files in a loop, reuse the document where you can and prefer the compressed writer to keep disk and I/O down:

```python
--8<-- "agent_references/snippets/writing-output.py:batch"
```

## Common mistakes

!!! failure "expecting byte-identical output without `preserve_formatting=True` on the loader"

    ```python
    doc = load_idf("building.idf")             # no CST
    save_idf(doc, "out.idf")                   # reformatted, NOT byte-identical
    ```

!!! success "pair load + save"

    ```python
    --8<-- "agent_references/snippets/writing-output.py:mistake-preserve-good"
    ```

!!! failure "UTF-8 by default for IDF"

    ```python
    save_idf(doc, "out.idf", encoding="utf-8")    # EnergyPlus may reject non-latin-1 bytes
    ```

!!! success "let the default win"

    ```python
    --8<-- "agent_references/snippets/writing-output.py:mistake-encoding-good"
    ```

!!! failure "mixing `output_type="compressed"` with lossless expectations"

    ```python
    doc = load_idf("building.idf", preserve_formatting=True)
    save_idf(doc, "out.idf", output_type="compressed")    # CST is ignored when output_type isn't "standard"
    ```

!!! success "be explicit about your intent"

    ```python
    --8<-- "agent_references/snippets/writing-output.py:mistake-compressed-good"
    ```

## Related

- [parsing-idf-epjson.md](parsing-idf-epjson.md) — the loader side, including `preserve_formatting`.
- [document-and-objects.md](document-and-objects.md) — what you write out.
- API docs: [py.idfkit.com/api/writer/](https://py.idfkit.com/api/writer/)
