# Project: idfkit — Core Python Library

## Summary

**idfkit** is a fast, modern EnergyPlus IDF/epJSON toolkit for Python. It is the foundation of the entire idfkit ecosystem — every other product (Envelop, idfkit-mcp, idfkit-lsp) builds on top of it.

**Repository:** `idfkit/idfkit`
**Language:** Python 3.10+
**License:** MIT
**Build system:** hatchling via uv
**Install:** `pip install idfkit`

## Core Capabilities

### High-Performance Data Model
- **IDFDocument:** Main container class. Dict-like access by object type (`doc["Zone"]`). Attribute access via Python names (`doc.zones`). Holds the schema, version, and reference graph.
- **IDFObject:** Lightweight dict wrapper using `__slots__` (~200 bytes per object). Field access via attributes with automatic IDF-to-Python name conversion.
- **IDFCollection:** Name-indexed collection of IDFObjects for a single type. O(1) lookup by name.
- **O(1) lookups:** Dictionary-based architecture delivers 4,000x faster object lookups than eppy.

### Reference Tracking
- **ReferenceGraph:** Tracks all cross-object references live. Auto-updates on rename. Enables `get_referencing(name)` queries to find all objects that reference a given name.
- Schema-driven: all reference relationships are derived from the bundled epJSON schemas.

### Dual Format Support
- Native IDF (text) and epJSON (structured JSON) parsing and writing.
- Seamless round-tripping between formats.
- Tokenizer-based IDF parser. JSON-based epJSON parser.

### Schema & Validation
- **SchemaManager:** Loads and caches epJSON schemas per EnergyPlus version.
- **Validation:** Document and object validation against schema — field types, required fields, ranges, choices, references.
- **Introspection:** `ObjectDescription` and `FieldDescription` for programmatic schema exploration.

### 3D Geometry
- **Vector3D, Polygon3D:** Geometric primitives for building surfaces.
- Surface area, volume, window-to-wall ratio (WWR) calculations.
- Intersect-match operations for surface adjacency.
- SVG-based 3D visualization output.

### Simulation
- **Sync runner:** Subprocess-based EnergyPlus execution.
- **Async runner:** `async_simulate()` for non-blocking workflows.
- **Batch processing:** Sync and async batch runners for parametric studies.
- **Content-addressed caching:** Deterministic hashing of model + weather + options to avoid redundant simulation runs.
- **Preprocessor support:** Slab, Basement, ExpandObjects integration.
- **Result parsing:** SQL, CSV, ERR, RDD, and HTML output parsers.
- **Progress tracking:** Event-based progress reporting.
- **FileSystem protocol:** Abstraction for local, S3, and in-memory storage.
- **Plotting:** matplotlib and plotly backends for result visualization.

### Weather
- **Station search:** Index of 55,000+ global weather stations with spatial queries.
- **EPW/DDY download:** Cached file download from climate data repositories.
- **Design day parsing:** DDY file parsing and injection into models.
- **Geocoding:** Address-to-coordinates via Nominatim for station search.

### Schedules
- **Evaluation engine:** Handles all 8 EnergyPlus schedule types (Compact, Day:Interval, Day:Hourly, Day:List, Week:Daily, Week:Compact, Year, File:Shading).
- **Time-series output:** Evaluate any schedule to a pandas-compatible time series.

### Thermal Properties
- R/U-value calculations for construction assemblies.
- SHGC (Solar Heat Gain Coefficient) calculations.
- Gas mixture property calculations (conductivity, viscosity, specific heat).

### Migration & Compatibility
- **eppy compatibility layer:** `_compat.py` provides drop-in migration support for users transitioning from eppy.
- Side-by-side migration guide in documentation.

## Architecture

```
src/idfkit/
  __init__.py                # Public API: load_idf, load_epjson, new_document, write_*
  document.py                # IDFDocument
  objects.py                 # IDFObject, IDFCollection
  idf_parser.py              # IDF tokenizer and parser
  epjson_parser.py           # epJSON parser
  writers.py                 # write_idf(), write_epjson()
  schema.py                  # EpJSONSchema, SchemaManager
  validation.py              # Document and object validation
  geometry.py                # Vector3D, Polygon3D, surface/zone calculations
  geometry_builders.py       # Geometry construction helpers
  references.py              # ReferenceGraph
  introspection.py           # ObjectDescription, FieldDescription
  versions.py                # Version registry (8.9.0–25.2.0)
  exceptions.py              # Custom exception hierarchy
  _compat.py                 # eppy compatibility layer
  _compat_object.py          # eppy object compatibility
  schemas/                   # Bundled epJSON schemas (16 versions)
  simulation/                # Simulation execution subsystem
    runner.py, async_runner.py, batch.py, async_batch.py
    config.py, cache.py, expand.py, result.py
    progress.py, progress_bars.py, fs.py, outputs.py, _common.py
    parsers/ (sql, csv, err, rdd, html)
    plotting/ (matplotlib, plotly, visualizations)
  weather/                   # Weather data subsystem
    station.py, download.py, designday.py, geocode.py, spatial.py, index.py
  schedules/                 # Schedule evaluation engine
    compact.py, day.py, week.py, year.py, file.py
    evaluate.py, builder.py, series.py, time_utils.py
    holidays.py, day_types.py, types.py
  thermal/                   # Thermal property calculations
    gas.py, properties.py
  visualization/             # 3D rendering
    model.py, svg.py
```

## Key Design Principles

1. **Schema-driven:** All object types, field names, and references derive from bundled epJSON schemas. Nothing is hardcoded.
2. **Version-aware:** Each document is tied to an EnergyPlus version. Schemas are cached per version.
3. **Zero core dependencies:** No third-party dependencies beyond Python stdlib. Optional extras for simulation, weather, plotting.
4. **Protocol-based I/O:** `FileSystem` and `AsyncFileSystem` protocols abstract storage backends.
5. **Backward compatibility:** Supports EnergyPlus 8.9.0 through 25.2.0 (16 versions). Default test version: 24.1.0.

## Code Quality Standards

- **Type checking:** Pyright strict mode enforced on all code.
- **Line length:** 120 characters.
- **Imports:** `from __future__ import annotations` in every module.
- **Linting:** Ruff with comprehensive rule selection (flake8-bugbear, flake8-bandit, isort, pyupgrade, tryceratops).
- **Testing:** ~45 test modules mirroring source structure. Doctest enabled. Integration tests require EnergyPlus installation.
- **Quality gate:** `make check && make test` (lock validation, pre-commit hooks, ruff, pyright, deptry, pytest with coverage).

## Strategic Role in the Ecosystem

idfkit is the **gravity center** of the ecosystem. Its design decisions cascade to every other product:

- **Envelop** renders idfkit's data model in the browser (schedule evaluation, geometry, HVAC topology).
- **idfkit-mcp** exposes idfkit's operations as MCP tools for AI agents.
- **idfkit-lsp** provides editor intelligence based on idfkit's schema and type system.

Decisions about idfkit's API surface, dependency policy, and version support are **Type 1 decisions** that affect the entire ecosystem.
