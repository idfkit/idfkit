# Logging

idfkit uses Python's standard `logging` module throughout the library.
Every module logs through a namespaced logger (e.g. `idfkit.idf_parser`,
`idfkit.simulation.runner`), so you can control verbosity per subsystem
using normal Python logging configuration.

By default, **no output is produced** — idfkit never calls
`logging.basicConfig()` or installs handlers, following the
[library logging best practice](https://docs.python.org/3/howto/logging.html#configuring-logging-for-a-library).
You opt in to log output by configuring handlers in your own application.

## Quick Start

The simplest way to see idfkit logs is to enable `basicConfig`:

```python
--8<-- "docs/snippets/concepts/logging/basic_setup.py:example"
```

## Log Levels

idfkit uses three log levels:

| Level | What Gets Logged |
|-------|-----------------|
| **`DEBUG`** | Diagnostic details — file paths, version detection, mmap usage, cache key computation, command lines, candidate paths |
| **`INFO`** | Operational milestones — parsing/writing completion with timing, simulation start/finish, batch progress, schema loading, weather downloads |
| **`WARNING`** | Potential problems — unknown object types skipped during parsing, non-zero EnergyPlus exit codes |

Errors are raised as exceptions (not logged), so there is no `ERROR`-level output.

## Logger Hierarchy

All loggers live under the `idfkit` namespace:

```
idfkit
├── idfkit.schema              # Schema loading and caching
├── idfkit.idf_parser          # IDF file parsing
├── idfkit.epjson_parser       # epJSON file parsing
├── idfkit.writers             # IDF/epJSON file writing
├── idfkit.document            # Object add/remove/rename
├── idfkit.validation          # Schema validation
├── idfkit.geometry            # Geometry operations (WWR, intersect_match)
├── idfkit.simulation
│   ├── idfkit.simulation.config       # EnergyPlus discovery
│   ├── idfkit.simulation.runner       # Simulation execution
│   ├── idfkit.simulation.async_runner # Async simulation
│   ├── idfkit.simulation.batch        # Batch processing
│   ├── idfkit.simulation.async_batch  # Async batch processing
│   ├── idfkit.simulation.cache        # Simulation result caching
│   └── idfkit.simulation.expand       # Preprocessors (ExpandObjects, Slab, Basement)
└── idfkit.weather
    ├── idfkit.weather.download        # EPW/DDY downloads
    └── idfkit.weather.index           # Station index loading
```

Setting a level on a parent logger applies to all children. For example,
`logging.getLogger("idfkit.simulation").setLevel(logging.DEBUG)` enables
debug output for the runner, cache, batch, and all other simulation loggers.

## Targeted Logging

Enable verbose output only for the subsystems you care about:

```python
--8<-- "docs/snippets/concepts/logging/targeted_loggers.py:example"
```

## Logging to a File

Write all idfkit output to a log file while keeping your console clean:

```python
--8<-- "docs/snippets/concepts/logging/file_handler.py:example"
```

## Debugging Simulations

When a simulation fails or produces unexpected results, enable `DEBUG` on
the simulation subsystem to see every step — EnergyPlus discovery, cache
lookups, the exact command line, and timing:

```python
--8<-- "docs/snippets/concepts/logging/debug_simulation.py:example"
```

## Integrating with Your Application

idfkit's loggers coexist naturally with your own application logging.
Configure them together:

```python
--8<-- "docs/snippets/concepts/logging/app_integration.py:example"
```

### Django

Use Django's `LOGGING` dict to configure idfkit loggers:

```python
--8<-- "docs/snippets/concepts/logging/django_integration.py:example"
```

## Structured / JSON Logging

For production environments or log aggregation pipelines, attach a custom
formatter to emit structured output:

```python
--8<-- "docs/snippets/concepts/logging/structured_logging.py:example"
```

## Silencing All Output

Suppress all idfkit logging entirely:

```python
--8<-- "docs/snippets/concepts/logging/silence.py:example"
```

## Key Log Messages

Here are some representative messages you will see at each level:

### INFO

| Logger | Message |
|--------|---------|
| `idfkit.idf_parser` | `Parsed 850 objects from model.idf in 0.142s` |
| `idfkit.schema` | `Loaded schema for version 24.1.0 (480 object types) in 0.523s` |
| `idfkit.simulation.runner` | `Starting simulation with weather weather.epw` |
| `idfkit.simulation.runner` | `Simulation completed successfully in 12.3s` |
| `idfkit.simulation.batch` | `Starting batch of 50 jobs with 8 workers` |
| `idfkit.validation` | `Validation complete: 0 errors, 2 warnings, 1 info` |
| `idfkit.weather.download` | `Downloading weather data for Chicago-OHare (WMO 725300)` |

### DEBUG

| Logger | Message |
|--------|---------|
| `idfkit.simulation.runner` | `Cache miss for key a1b2c3d4e5f6` |
| `idfkit.simulation.runner` | `Command: /usr/local/.../energyplus -w weather.epw -d ...` |
| `idfkit.simulation.config` | `Trying candidate /usr/local/EnergyPlus-24-2-0` |
| `idfkit.simulation.cache` | `Computed cache key a1b2c3d4e5f6` |
| `idfkit.idf_parser` | `Using mmap for large file (52428800 bytes)` |
| `idfkit.document` | `Added Zone 'Office'` |

### WARNING

| Logger | Message |
|--------|---------|
| `idfkit.idf_parser` | `Skipping unknown object type 'FooBar'` |
| `idfkit.simulation.runner` | `Simulation exited with code 1 in 5.2s` |

## See Also

- [Error Handling](../simulation/errors.md) — Handling simulation failures
- [Caching Strategy](caching.md) — Cache hit/miss diagnostics
- [Troubleshooting](../troubleshooting/errors.md) — Common error solutions
