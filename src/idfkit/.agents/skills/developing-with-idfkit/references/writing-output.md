# Writing output

idfkit serializes `IDFDocument` to both EnergyPlus formats. Pick `write_idf` for `.idf` (what `energyplus` expects by default) or `write_epjson` for the JSON variant.

## When to use

- You've finished editing a document and want to persist it to disk.
- You want an IDF string (without writing to disk) for inspection or testing.
- You're converting between IDF and epJSON.
- You need byte-identical output for unmodified objects (lossless round-trip).

## Quick start

```python
from idfkit import load_idf, write_idf, write_epjson

doc = load_idf("in.idf")
doc["Zone"]["Office"].x_origin = 10.0

# Persist
write_idf(doc, "out.idf")
write_epjson(doc, "out.epJSON")

# Or get a string back (filepath=None)
idf_text = write_idf(doc)
```

## Core API

| Symbol | Purpose |
|---|---|
| `write_idf(doc, filepath=None, encoding="latin-1", output_type="standard", *, preserve_formatting=None)` | Serialize to IDF. Returns `str` if `filepath` is `None`. |
| `write_epjson(doc, filepath=None, indent=2, *, preserve_formatting=None)` | Serialize to epJSON. Returns `str` if `filepath` is `None`. |
| `idfkit.writers.convert_idf_to_epjson(src, dst)` | Convenience converter. |
| `idfkit.writers.convert_epjson_to_idf(src, dst)` | Convenience converter. |
| `IDFWriter(doc, output_type=...)` | Lower-level writer with a `to_string()` method. |
| `EpJSONWriter(doc)` | Lower-level epJSON writer. |

## Output formatting modes

`write_idf(..., output_type=)` mirrors eppy's `idf.outputtype`:

- `"standard"` (default) — full `!- Field Name` comments, one field per line. Best for hand editing.
- `"nocomment"` — one field per line, no comments. Smaller, still diff-friendly.
- `"compressed"` — entire object on one line. Best for parametric runs that produce thousands of files.

```python
write_idf(doc, "out.idf", output_type="compressed")
```

epJSON formatting is controlled by `indent` (default 2; pass `indent=0` for the most compact form).

## Encoding

EnergyPlus expects `latin-1` for IDF files (that's the writer default). Don't override unless you have a downstream tool that requires UTF-8 — many EnergyPlus utilities will choke on non-`latin-1` IDFs.

## Lossless round-trips (IDF only)

To preserve every byte of whitespace, comments, and object ordering for objects you didn't touch, pair `load_idf(..., preserve_formatting=True)` with `write_idf(...)`:

```python
from idfkit import load_idf, write_idf

doc = load_idf("building.idf", preserve_formatting=True)
doc["Zone"]["Office"].x_origin = 10.0
write_idf(doc, "building_modified.idf")
# Only the Zone "Office" block is reformatted; everything else is byte-identical.
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

Pass `filepath=None` (or omit it) to get the serialized string back. Useful for tests:

```python
text = write_idf(doc)
assert "Zone," in text
```

## Format conversion

```python
from idfkit import load_idf, write_epjson

doc = load_idf("building.idf")
write_epjson(doc, "building.epJSON")  # IDF → epJSON
```

Or in the other direction:

```python
from idfkit import load_epjson, write_idf

doc = load_epjson("building.epJSON")
write_idf(doc, "building.idf")  # epJSON → IDF
```

The explicit converters `idfkit.writers.convert_idf_to_epjson` and `convert_epjson_to_idf` skip the round-trip through Python and stream directly between the two formats — use them in scripts that don't need to inspect the document in between.

## Batch writing

If you generate many output files in a loop, reuse the document where you can and prefer the compressed writer to keep disk and I/O down:

```python
from pathlib import Path
from idfkit import load_idf, write_idf

base = load_idf("base.idf")
out_dir = Path("runs")
out_dir.mkdir(exist_ok=True)

for wwr in (0.2, 0.3, 0.4, 0.5):
    doc = base.copy()
    from idfkit import set_wwr

    set_wwr(doc, wwr)
    write_idf(doc, out_dir / f"wwr_{int(wwr * 100)}.idf", output_type="compressed")
```

## Common mistakes

!!! failure "expecting byte-identical output without `preserve_formatting=True` on the loader"

    ```python
    doc = load_idf("building.idf")             # no CST
    write_idf(doc, "out.idf")                  # reformatted, NOT byte-identical
    ```

!!! success "pair load + write"

    ```python
    doc = load_idf("building.idf", preserve_formatting=True)
    write_idf(doc, "out.idf")
    ```

!!! failure "UTF-8 by default for IDF"

    ```python
    write_idf(doc, "out.idf", encoding="utf-8")   # EnergyPlus may reject non-latin-1 bytes
    ```

!!! success "let the default win"

    ```python
    write_idf(doc, "out.idf")  # latin-1
    ```

!!! failure "mixing `output_type="compressed"` with lossless expectations"

    ```python
    doc = load_idf("building.idf", preserve_formatting=True)
    write_idf(doc, "out.idf", output_type="compressed")   # CST is ignored when output_type isn't "standard"
    ```

!!! success "be explicit about your intent"

    ```python
    write_idf(doc, "out.idf", output_type="standard")  # lossless (default)
    # or
    write_idf(doc, "out.idf", output_type="compressed", preserve_formatting=False)
    ```

## Related

- [parsing-idf-epjson.md](parsing-idf-epjson.md) — the loader side, including `preserve_formatting`.
- [document-and-objects.md](document-and-objects.md) — what you write out.
- API docs: [py.idfkit.com/api/writer/](https://py.idfkit.com/api/writer/)
