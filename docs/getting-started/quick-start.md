# Common tasks

Quick recipes for the operations you'll use every day, in both languages where both have
them and with the difference stated where they do not. Each section is
self-contained — jump to the one you need. If you're brand new to idfkit, work
through [Build your first model](../tutorials/first-model.md) first, then come
back here.

## Load a Model

=== "Python"

    ```python
    --8<-- "docs/snippets/getting-started/quick-start/load_a_model.py:example"
    ```

=== "TypeScript"

    ```ts
    --8<-- "docs/snippets/js/getting-started/quick-start/load_a_model.ts:example"
    ```

`load_idf()` uses strict parsing by default (`strict_parsing=True`) and raises
`IDFParseError` for malformed objects. Use `strict_parsing=False` only as a
migration/compatibility fallback for legacy or noisy files.

## Query Objects

Access objects with O(1) dictionary lookups:

=== "Python"

    ```python
    --8<-- "docs/snippets/getting-started/quick-start/query_objects.py:example"
    ```

=== "TypeScript"

    ```ts
    --8<-- "docs/snippets/js/getting-started/quick-start/query_objects.ts:example"
    ```

## Modify Fields

Change field values with attribute assignment:

=== "Python"

    ```python
    --8<-- "docs/snippets/getting-started/quick-start/modify_fields.py:example"
    ```

=== "TypeScript"

    ```ts
    --8<-- "docs/snippets/js/getting-started/quick-start/modify_fields.ts:example"
    ```

## Discover Available Fields

Not sure what fields an object type has? Use `describe()` to see all available fields:

=== "Python"

    ```python
    --8<-- "docs/snippets/getting-started/quick-start/discover_available_fields.py:example"
    ```

=== "TypeScript"

    ```ts
    --8<-- "docs/snippets/js/getting-started/quick-start/discover_available_fields.ts:example"
    ```

In REPL/Jupyter, use tab completion to explore object fields:

```text
>>> zone = model["Zone"]["Office"]
>>> zone.<TAB>
x_origin, y_origin, z_origin, multiplier, ...
```

Both libraries catch a misspelled field name. They catch it at different moments,
and the difference is the one thing worth knowing about the two type systems:
Python validates when the object is built, TypeScript when the file is compiled.

=== "Python"

    ```python
    --8<-- "docs/snippets/getting-started/quick-start/discover_available_fields_3.py:example"
    ```

=== "TypeScript"

    ```ts
    --8<-- "docs/snippets/js/getting-started/quick-start/discover_available_fields_3.ts:example"
    ```

!!! tip "IDE Support"
    idfkit ships type stubs for all 858 EnergyPlus object types — your IDE
    will autocomplete field names, show inline documentation, and catch typos.
    See [Type-Safe Development](../concepts/type-safety.md) for details.

## Create a New Model

=== "Python"

    ```python
    --8<-- "docs/snippets/getting-started/quick-start/create_a_new_model.py:example"
    ```

=== "TypeScript"

    ```ts
    --8<-- "docs/snippets/js/getting-started/quick-start/create_a_new_model.ts:example"
    ```

## Write Output

=== "Python"

    ```python
    --8<-- "docs/snippets/getting-started/quick-start/write_output.py:example"
    ```

=== "TypeScript"

    ```ts
    --8<-- "docs/snippets/js/getting-started/quick-start/write_output.ts:example"
    ```

## Run a Simulation

=== "Python"

    ```python
    --8<-- "docs/snippets/getting-started/quick-start/run_a_simulation.py:example"
    ```

{{ parity("local-simulation") }}

## Query Results

=== "Python"

    ```python
    --8<-- "docs/snippets/getting-started/quick-start/query_results.py:example"
    ```

{{ parity("local-simulation") }}

## Find Weather Stations

=== "Python"

    ```python
    --8<-- "docs/snippets/getting-started/quick-start/find_weather_stations.py:example"
    ```

=== "TypeScript"

    ```ts
    --8<-- "docs/snippets/js/getting-started/quick-start/find_weather_stations.ts:example"
    ```

## Apply Design Days

=== "Python"

    ```python
    --8<-- "docs/snippets/getting-started/quick-start/apply_design_days.py:example"
    ```

{{ parity("design-day-sizing") }}

## Lossless Round-Trip

Pass `preserve_formatting=True` to build a Concrete Syntax Tree (CST) so that
`write_idf` and `save_idf` reproduce the original formatting, comments, and whitespace for
unmodified objects:

=== "Python"

    ```python
    --8<-- "docs/snippets/getting-started/quick-start/lossless_roundtrip.py:example"
    ```

{{ parity("lossless-round-trip") }}

## Next Steps

- [Core Tutorial](core-tutorial.ipynb) - Complete interactive walkthrough
- [Simulation Guide](../simulation/index.md) - Deep dive into simulation features
- [How to migrate models between EnergyPlus versions](../simulation/migrating-versions.md) - Move models forward across EnergyPlus releases
- [Weather Guide](../weather/index.md) - Weather station search and design days
- [API Reference](../api/document.md) - Full API documentation
