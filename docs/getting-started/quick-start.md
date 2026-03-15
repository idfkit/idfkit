# Quick Start

Get up and running with idfkit in 5 minutes. This guide covers the essential
operations you'll use every day.

## Load a Model

```python
--8<-- "docs/snippets/getting-started/quick-start/load_a_model.py:example"
```

`load_idf()` uses strict parsing by default (`strict=True`) and raises
`IDFParseError` for malformed objects. Use `strict=False` only as a
migration/compatibility fallback for legacy or noisy files.

## Query Objects

Access objects with O(1) dictionary lookups:

```python
--8<-- "docs/snippets/getting-started/quick-start/query_objects.py:example"
```

## Modify Fields

Change field values with attribute assignment:

```python
--8<-- "docs/snippets/getting-started/quick-start/modify_fields.py:example"
```

## Discover Available Fields

Not sure what fields an object type has? Use `describe()` to see all available fields:

```python
--8<-- "docs/snippets/getting-started/quick-start/discover_available_fields.py:example"
```

In REPL/Jupyter, use tab completion to explore object fields:

```python
zone = model["Zone"]["Office"]
zone.<TAB>  # Shows: x_origin, y_origin, z_origin, multiplier, ...
```

Validation is enabled by default, so typos are caught immediately:

```python
--8<-- "docs/snippets/getting-started/quick-start/discover_available_fields_3.py:example"
```

!!! tip "IDE Support"
    idfkit ships type stubs for all 858 EnergyPlus object types — your IDE
    will autocomplete field names, show inline documentation, and catch typos.
    See [Type-Safe Development](../concepts/type-safety.md) for details.

## Create a New Model

```python
--8<-- "docs/snippets/getting-started/quick-start/create_a_new_model.py:example"
```

## Write Output

```python
--8<-- "docs/snippets/getting-started/quick-start/write_output.py:example"
```

## Run a Simulation

```python
--8<-- "docs/snippets/getting-started/quick-start/run_a_simulation.py:example"
```

## Query Results

```python
--8<-- "docs/snippets/getting-started/quick-start/query_results.py:example"
```

## Find Weather Stations

```python
--8<-- "docs/snippets/getting-started/quick-start/find_weather_stations.py:example"
```

## Apply Design Days

```python
--8<-- "docs/snippets/getting-started/quick-start/apply_design_days.py:example"
```

## Next Steps

- [Core Tutorial](core-tutorial.ipynb) - Complete interactive walkthrough
- [Simulation Guide](../simulation/index.md) - Deep dive into simulation features
- [Weather Guide](../weather/index.md) - Weather station search and design days
- [API Reference](../api/document.md) - Full API documentation
