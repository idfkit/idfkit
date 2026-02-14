# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**idfkit** is a fast, modern EnergyPlus IDF/epJSON toolkit for Python. It provides high-performance parsing and manipulation of EnergyPlus building energy simulation input files, with O(1) object lookups, automatic reference tracking, and native support for both IDF and epJSON formats.

Key capabilities: IDF/epJSON parsing and writing, schema-driven validation, 3D geometry operations, EnergyPlus simulation execution (sync/async/batch), weather data search and download, schedule evaluation, thermal property calculations, and 3D visualization.

**Python:** 3.10+ | **License:** MIT | **Build:** hatchling via uv

## Common Commands

```bash
# Install dependencies
uv sync

# Run all quality checks (lint, format, type check, deptry)
make check

# Run tests (unit tests only, no EnergyPlus required)
make test

# Run a single test
uv run pytest tests/test_file.py::test_function -v

# Run integration tests (requires EnergyPlus installation)
ENERGYPLUS_DIR=/usr/local/EnergyPlus-24-2-0 uv run pytest -m integration -v

# Type check
uv run pyright src/ docs/snippets

# Lint and format
uv run ruff check src/ tests/
uv run ruff format src/ tests/

# Serve documentation locally
make docs

# Build wheel
make build
```

## Project Structure

```
src/idfkit/                  # Main package
  __init__.py                # Public API: load_idf, load_epjson, new_document, write_*
  document.py                # IDFDocument - main container class for EnergyPlus models
  objects.py                 # IDFObject (thin dict wrapper) and IDFCollection (indexed by name)
  idf_parser.py              # IDF format tokenizer and parser
  epjson_parser.py           # epJSON format parser
  writers.py                 # write_idf() and write_epjson()
  schema.py                  # EpJSONSchema loading and SchemaManager (cached by version)
  validation.py              # Document and object validation against schema
  geometry.py                # Vector3D, Polygon3D, surface/zone calculations, WWR, intersect_match
  references.py              # ReferenceGraph - live cross-object reference tracking
  introspection.py           # ObjectDescription, FieldDescription for schema introspection
  versions.py                # Version registry (8.9.0 through 25.2.0), compatibility helpers
  exceptions.py              # Custom exception hierarchy (all inherit IdfKitError)
  _compat.py                 # eppy compatibility layer (drop-in migration support)
  schemas/                   # Bundled epJSON schemas for 16 EnergyPlus versions
  simulation/                # EnergyPlus simulation execution
    runner.py                # Subprocess-based simulation runner
    async_runner.py          # async_simulate()
    batch.py, async_batch.py # Batch processing (sync and async)
    config.py                # EnergyPlus installation discovery
    cache.py                 # Content-addressed simulation caching
    expand.py                # Preprocessor support (Slab, Basement, ExpandObjects)
    result.py                # SimulationResult container
    progress.py              # Event-based progress tracking
    fs.py                    # FileSystem protocol (local, S3, async)
    parsers/                 # Result parsers: sql.py, csv.py, err.py, rdd.py, html.py
    plotting/                # matplotlib and plotly backends
  weather/                   # Weather data module
    station.py               # Station index search (~17k stations)
    download.py              # EPW/DDY file download with local caching
    designday.py             # DDY parsing and injection into models
    geocode.py               # Address-to-coordinates via Nominatim
    spatial.py               # Nearby station queries
  schedules/                 # Schedule evaluation engine (all 8 EnergyPlus schedule types)
  thermal/                   # R/U-value, SHGC, gas mixture property calculations
  visualization/             # 3D building geometry rendering (SVG output)

tests/                       # Test suite (~45 test modules, mirrors source structure)
  conftest.py                # Shared fixtures: schema, empty_doc, simple_doc, InMemoryFileSystem
  fixtures/                  # Test data files (IDF, epJSON, simulation outputs, weather)

docs/                        # MkDocs Material documentation
  snippets/                  # Code snippets (linted with ruff and pyright)

benchmarks/                  # Performance benchmarks vs eppy/opyplus
```

## Architecture

### Core Data Model

- **IDFDocument**: Main container. Dict-like access by object type (`doc["Zone"]`). Attribute access via Python names (`doc.zones`). Holds the schema, version, and reference graph.
- **IDFObject**: Lightweight dict wrapper using `__slots__` (~200 bytes). Field access via attributes with automatic IDF-to-Python name conversion.
- **IDFCollection**: Name-indexed collection of IDFObjects for a single type. O(1) lookup by name.
- **ReferenceGraph**: Tracks all cross-object references. Auto-updates on rename. Enables `get_referencing(name)` queries.
- **EpJSONSchema**: Loaded from bundled JSON schema files. Drives validation, field metadata, and reference resolution.

### Key Design Patterns

- Schema-driven: All object types, field names, and references come from the bundled epJSON schemas
- Version-aware: Each document is tied to an EnergyPlus version; schemas are cached per version
- Protocol-based I/O: `FileSystem` and `AsyncFileSystem` protocols abstract local/S3/in-memory storage
- Zero core dependencies: The main package has no third-party dependencies beyond Python stdlib

## Code Style

- **Line length**: 120 characters
- **Imports**: Always include `from __future__ import annotations` at the top of every module
- **Type hints**: Required on all functions (parameters and return types). Pyright strict mode is enforced.
- **Docstrings**: Google or NumPy style for public APIs
- **Data models**: Use dataclasses or Pydantic instead of raw dicts
- **Ruff rules**: Comprehensive selection including flake8-bugbear, flake8-bandit, isort, pyupgrade, tryceratops (see `pyproject.toml [tool.ruff.lint]`)

## Testing

Tests live in `tests/` and mirror the source structure. Doctest is enabled for modules in `src/idfkit/`.

When adding new functionality:

1. Create test file: `tests/test_<module_name>.py`
2. Write tests before or alongside implementation
3. Run tests: `uv run pytest tests/test_<module_name>.py -v`
4. Verify all tests pass: `make test`

Use pytest fixtures (in `conftest.py`) for shared test setup. Key fixtures:
- `schema` - v24.1.0 EpJSONSchema
- `empty_doc` - Empty IDFDocument
- `simple_doc` - Document with zone, material, construction, and surfaces
- `idf_file` / `epjson_file` - Temporary test files
- `reference_graph` - Pre-populated ReferenceGraph

Tests marked `@pytest.mark.integration` require an EnergyPlus installation.

Note: Doctest modules for `simulation/`, `weather/`, `schedules/`, `thermal/`, and `visualization/` are excluded from default test runs (they require external dependencies or EnergyPlus).

## Type Checking

This project uses **pyright** in strict mode. **ALWAYS** try to fix typing issues with a proper solution rather than adding an ignore statement.

```bash
uv run pyright src/ docs/snippets
```

Ensure all new code is fully typed. The configuration is in `pyproject.toml`. Note the relaxed pyright rules for `docs/snippets/` (documentation code fragments).

## Before Committing

Always run the full quality gate before proposing changes:

```bash
make check && make test
```

This runs: lock file validation, pre-commit hooks (ruff format + lint, JSON formatting, trailing whitespace), pyright, deptry (unused dependency detection), and pytest with coverage.

## EnergyPlus Version Support

Bundled schemas cover EnergyPlus 8.9.0 through 25.2.0 (16 versions). The latest supported version is 25.2.0. Version 24.1.0 is used as the default in test fixtures. See `src/idfkit/versions.py` for the full list.
