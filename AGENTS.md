# AGENTS.md

Instructions for AI agents and CI environments working with this repository.

## Quick Start

```bash
# Install all dependencies (dev + optional)
uv sync

# Run full quality gate (required before any commit)
make check && make test
```

## Project Summary

**idfkit** is a Python toolkit for EnergyPlus IDF/epJSON building energy model files. The core package (`src/idfkit/`) parses, manipulates, validates, and writes EnergyPlus input files. Sub-packages handle simulation execution, weather data, schedule evaluation, thermal calculations, and visualization.

The codebase has zero core runtime dependencies. Optional features (plotting, cloud storage, DataFrames, progress bars) are gated behind extras in `pyproject.toml`.

## Repository Layout

| Path | Purpose |
|---|---|
| `src/idfkit/` | Main package source code |
| `src/idfkit/simulation/` | EnergyPlus simulation runner (sync, async, batch, caching) |
| `src/idfkit/weather/` | Weather station search and EPW/DDY download |
| `src/idfkit/schedules/` | Schedule evaluation engine (all 8 schedule types) |
| `src/idfkit/thermal/` | R/U-value, SHGC, gas mixture calculations |
| `src/idfkit/visualization/` | 3D geometry rendering to SVG |
| `src/idfkit/schemas/` | Bundled epJSON schemas (16 EnergyPlus versions) |
| `tests/` | Unit and integration tests (mirrors source structure) |
| `tests/conftest.py` | Shared pytest fixtures |
| `tests/fixtures/` | Test data files |
| `docs/` | MkDocs Material documentation |
| `docs/snippets/` | Code snippets used in docs (linted with ruff/pyright) |
| `benchmarks/` | Performance benchmarks vs eppy/opyplus |
| `scripts/` | Utility scripts (weather index rebuild) |

## Development Workflow

### Quality Gate

Every commit must pass:

```bash
make check    # lock validation, pre-commit (ruff format + lint), pyright strict, deptry
make test     # pytest with coverage (unit tests, doctests)
```

### Running Tests

```bash
# All unit tests (no EnergyPlus needed)
make test

# Single test file
uv run pytest tests/test_document.py -v

# Single test function
uv run pytest tests/test_document.py::test_add_object -v

# Integration tests (requires EnergyPlus)
ENERGYPLUS_DIR=/usr/local/EnergyPlus-24-2-0 uv run pytest -m integration -v
```

Default `pytest` runs doctests from `src/idfkit/` but excludes `simulation/`, `weather/`, `schedules/`, `thermal/`, and `visualization/` modules (they need external dependencies or EnergyPlus).

### Type Checking

```bash
uv run pyright src/ docs/snippets
```

Pyright runs in **strict** mode. Fix typing issues properly rather than adding `# type: ignore` or `# pyright: ignore` comments.

### Linting and Formatting

Handled by **ruff** via pre-commit hooks. Key settings:

- Line length: 120 characters
- Target: Python 3.10
- Auto-fix enabled
- Comprehensive rule set (see `pyproject.toml [tool.ruff.lint]`)

```bash
# Check
uv run ruff check src/ tests/

# Format
uv run ruff format src/ tests/
```

## Code Conventions

- Every module starts with `from __future__ import annotations`
- All functions require full type annotations (parameters + return type)
- Public APIs use Google or NumPy style docstrings
- Use dataclasses or Pydantic for structured data, not raw dicts
- Custom exceptions inherit from `IdfKitError` (see `src/idfkit/exceptions.py`)
- The `IDFObject` class uses `__slots__` for memory efficiency (~200 bytes per instance)
- Schema files under `src/idfkit/schemas/` are auto-generated; do not edit manually

## Key Abstractions

| Class | Module | Role |
|---|---|---|
| `IDFDocument` | `document.py` | Main container for an EnergyPlus model |
| `IDFObject` | `objects.py` | Single EnergyPlus object (thin dict wrapper) |
| `IDFCollection` | `objects.py` | Name-indexed collection of objects of one type |
| `ReferenceGraph` | `references.py` | Live cross-object reference tracking |
| `EpJSONSchema` | `schema.py` | Schema for a specific EnergyPlus version |
| `SchemaManager` | `schema.py` | Cached schema loader |
| `SimulationResult` | `simulation/result.py` | Container for simulation outputs |
| `FileSystem` | `simulation/fs.py` | Protocol for local/S3/async file I/O |

## Test Fixtures

Defined in `tests/conftest.py`:

| Fixture | Description |
|---|---|
| `schema` | v24.1.0 `EpJSONSchema` |
| `empty_doc` | Empty `IDFDocument` (v24.1.0) |
| `simple_doc` | Document with zone, material, construction, surfaces |
| `idf_file` | Temporary `.idf` file on disk |
| `epjson_file` | Temporary `.epJSON` file on disk |
| `reference_graph` | Pre-populated `ReferenceGraph` with sample references |

`InMemoryFileSystem` and `InMemoryAsyncFileSystem` classes are also available in `conftest.py` for testing I/O without touching disk.

## Installing EnergyPlus

EnergyPlus is required to run integration tests (`pytest -m integration`) and to verify simulation tutorials. The project supports EnergyPlus versions 8.9.0 through 25.2.0.

### Download

EnergyPlus releases are hosted on GitHub under the **NatLabRockies** organization (formerly NREL):

```
https://github.com/NatLabRockies/EnergyPlus/releases
```

Pick a version that matches a bundled schema (see `src/idfkit/schemas/` for available versions). Version **24.2.0** is recommended for testing as it is the latest in the 24.x series used by most tutorials.

### Linux (Ubuntu) Installation

```bash
# 1. Download the tar.gz for your Ubuntu version (22.04 or 24.04)
wget https://github.com/NatLabRockies/EnergyPlus/releases/download/v24.2.0/EnergyPlus-24.2.0-e7ecb2d53b-Linux-Ubuntu24.04-x86_64.tar.gz -O /tmp/energyplus.tar.gz

# 2. Extract to the standard installation directory
mkdir -p /usr/local/EnergyPlus-24-2-0
tar xzf /tmp/energyplus.tar.gz -C /usr/local/EnergyPlus-24-2-0 --strip-components=1

# 3. Verify
/usr/local/EnergyPlus-24-2-0/energyplus --version
```

For Ubuntu 22.04, replace `Ubuntu24.04` with `Ubuntu22.04` in the URL.

### Setting the Environment Variable

Set `ENERGYPLUS_DIR` so idfkit can discover the installation:

```bash
export ENERGYPLUS_DIR=/usr/local/EnergyPlus-24-2-0
```

### How idfkit Discovers EnergyPlus

idfkit searches for EnergyPlus in this order (see `src/idfkit/simulation/config.py`):

1. Explicit `path` argument to `find_energyplus(path=...)`
2. `ENERGYPLUS_DIR` environment variable
3. `energyplus` on system `PATH`
4. Platform default directories (newest version first):
   - Linux: `~/.local/EnergyPlus-*`, `~/EnergyPlus-*`, `/usr/local/EnergyPlus-*`, `/opt/EnergyPlus-*`
   - macOS: `~/Applications/EnergyPlus-*`, `/Applications/EnergyPlus-*`
   - Windows: `%ProgramFiles%/EnergyPlus-*`

### Verifying the Installation

```bash
uv run python -c "
from idfkit.simulation import find_energyplus
config = find_energyplus()
print(f'EnergyPlus {config.version[0]}.{config.version[1]}.{config.version[2]}')
print(f'Executable: {config.executable}')
"
```

### Running Integration Tests

```bash
# Run only integration tests (requires EnergyPlus)
ENERGYPLUS_DIR=/usr/local/EnergyPlus-24-2-0 uv run pytest -m integration -v

# Run all tests including integration
ENERGYPLUS_DIR=/usr/local/EnergyPlus-24-2-0 uv run pytest -v
```

### Version Compatibility

The `src/idfkit/versions.py` file lists all supported versions. Each version has a bundled epJSON schema under `src/idfkit/schemas/V{major}-{minor}-{patch}/`.

| Version Range | Notes |
|---|---|
| 24.1.0 - 24.2.0 | Used in most tutorials and examples |
| 25.1.0 - 25.2.0 | Latest supported |
| 8.9.0 - 9.6.0 | Legacy versions |

### Bundled Files

An EnergyPlus installation includes:
- `energyplus` executable
- `Energy+.idd` (schema definition)
- `ExampleFiles/` directory with sample IDF models
- `WeatherData/` directory with sample EPW weather files

The example files are used by `tests/test_simulation_e2e.py` for integration testing.

## CI Pipeline

GitHub Actions workflows in `.github/workflows/`:

| Workflow | Trigger | What it does |
|---|---|---|
| `main.yml` | PR and push to main | Quality checks, test matrix (Python 3.10-3.13), pyright, coverage |
| `deploy-docs.yml` | Push to main | Deploy docs to GitHub Pages |
| `deploy-pr-docs.yml` | Pull requests | Deploy PR preview docs |
| `on-release-main.yml` | Version tag | Release to PyPI |

## Optional Dependency Extras

| Extra | Packages | Purpose |
|---|---|---|
| `weather` | openpyxl | Refresh weather station index from source |
| `pandas` / `dataframes` | pandas | DataFrame result conversion |
| `s3` / `cloud` | boto3 | S3 storage backend |
| `async-s3` | aiobotocore | Async S3 backend |
| `plot` | matplotlib | Static plotting |
| `plotly` | plotly | Interactive charts |
| `progress` | tqdm | Progress bars for simulations |
| `all` | Everything above | All optional features |
