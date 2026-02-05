# Installation

idfkit is available on PyPI and can be installed with pip or uv.

## Basic Installation

=== "pip"

    ```bash
    pip install idfkit
    ```

=== "uv"

    ```bash
    uv add idfkit
    ```

This installs the core package with support for:

- Loading and writing IDF/epJSON files
- O(1) object lookups and reference tracking
- Schema validation
- 3D geometry calculations
- Running EnergyPlus simulations

## Optional Dependencies

idfkit provides optional extras for additional functionality:

### Weather Station Index

Refresh the bundled weather station index from climate.onebuilding.org:

=== "pip"

    ```bash
    pip install idfkit[weather]
    ```

=== "uv"

    ```bash
    uv add idfkit[weather]
    ```

!!! note
    The bundled station index works without this extra. Only install `[weather]`
    if you need to refresh the index with `StationIndex.refresh()`.

### DataFrame Support

Convert simulation results to pandas DataFrames:

=== "pip"

    ```bash
    pip install idfkit[dataframes]
    ```

=== "uv"

    ```bash
    uv add idfkit[dataframes]
    ```

### Plotting

Visualize simulation results with matplotlib or plotly:

=== "pip"

    ```bash
    # Matplotlib backend
    pip install idfkit[plot]

    # Plotly backend
    pip install idfkit[plotly]
    ```

=== "uv"

    ```bash
    # Matplotlib backend
    uv add idfkit[plot]

    # Plotly backend
    uv add idfkit[plotly]
    ```

### Cloud Storage (S3)

Store simulation results in Amazon S3:

=== "pip"

    ```bash
    pip install idfkit[s3]
    ```

=== "uv"

    ```bash
    uv add idfkit[s3]
    ```

### Install Everything

Install all optional dependencies at once:

=== "pip"

    ```bash
    pip install idfkit[all]
    ```

=== "uv"

    ```bash
    uv add idfkit[all]
    ```

## EnergyPlus Installation

To run simulations, you need EnergyPlus installed on your system.

### Automatic Discovery

idfkit automatically discovers EnergyPlus using this priority:

1. **Explicit path** passed to `find_energyplus(path=...)`
2. **Environment variable** `ENERGYPLUS_DIR`
3. **System PATH** (looks for `energyplus` executable)
4. **Platform defaults**:
    - macOS: `/Applications/EnergyPlus-*/`
    - Linux: `/usr/local/EnergyPlus-*/`
    - Windows: `C:\EnergyPlusV*/`

### Download EnergyPlus

Download from the official EnergyPlus website:

- [EnergyPlus Downloads](https://energyplus.net/downloads)

### Verify Installation

```python
from idfkit.simulation import find_energyplus

config = find_energyplus()
print(f"EnergyPlus {config.version[0]}.{config.version[1]}.{config.version[2]}")
print(f"Executable: {config.executable}")
```

## Development Installation

To contribute to idfkit, clone the repository and install with development dependencies:

```bash
git clone https://github.com/samuelduchesne/idfkit.git
cd idfkit
uv sync
```

Run the test suite:

```bash
make test
```

Run all quality checks:

```bash
make check
```

## Requirements

- Python 3.10 or later
- EnergyPlus 8.9 or later (for simulation features)

## Next Steps

- [Quick Start](quick-start.md) - Get up and running in 5 minutes
- [Core Tutorial](core-tutorial.ipynb) - In-depth interactive tutorial
