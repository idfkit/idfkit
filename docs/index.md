# idfkit

[![Release](https://img.shields.io/github/v/release/samuelduchesne/idfkit)](https://img.shields.io/github/v/release/samuelduchesne/idfkit)
[![Build status](https://img.shields.io/github/actions/workflow/status/samuelduchesne/idfkit/main.yml?branch=main)](https://github.com/samuelduchesne/idfkit/actions/workflows/main.yml?query=branch%3Amain)
[![Commit activity](https://img.shields.io/github/commit-activity/m/samuelduchesne/idfkit)](https://img.shields.io/github/commit-activity/m/samuelduchesne/idfkit)
[![License](https://img.shields.io/github/license/samuelduchesne/idfkit)](https://img.shields.io/github/license/samuelduchesne/idfkit)

**A fast, modern EnergyPlus IDF/epJSON toolkit for Python.**

idfkit lets you load, create, query, and modify EnergyPlus models with an
intuitive Python API. It is designed as a drop-in replacement for
[eppy](https://github.com/santoshphilip/eppy) with better performance,
built-in reference tracking, and native support for both IDF and epJSON
formats.

## Key Features

- **O(1) object lookups** — Collections are indexed by name, so
  `doc["Zone"]["Office"]` is a dict lookup, not a linear scan.
- **Automatic reference tracking** — A live reference graph keeps track of
  every cross-object reference. Renaming an object updates every field that
  pointed to the old name.
- **IDF + epJSON** — Read and write both formats; convert between them in a
  single call.
- **Schema-driven validation** — Validate documents against the official
  EnergyPlus epJSON schema with detailed error messages.
- **Built-in 3D geometry** — `Vector3D` and `Polygon3D` classes for surface
  area, zone volume, and coordinate transforms without external dependencies.
- **EnergyPlus simulation** — Run simulations as subprocesses with structured
  result parsing, batch processing, and content-addressed caching.
- **Weather data** — Search 55,000+ weather stations, download EPW/DDY files,
  and apply ASHRAE design day conditions.
- **Broad version support** — Bundled schemas for every EnergyPlus release
  from v8.9 through v25.2.

## Installation

```bash
pip install idfkit
```

Or with [uv](https://docs.astral.sh/uv/):

```bash
uv add idfkit
```

## Quick Example

```python
from idfkit import load_idf, write_idf

# Load an existing IDF file
doc = load_idf("in.idf")

# Query objects with O(1) lookups
zone = doc["Zone"]["Office"]
print(zone.x_origin, zone.y_origin)

# Modify a field
zone.x_origin = 10.0

# See what references the zone
for obj in doc.get_referencing("Office"):
    print(obj.obj_type, obj.name)

# Write back to IDF (or epJSON)
write_idf(doc, "out.idf")
```

## Run Simulations

```python
from idfkit.simulation import simulate

result = simulate(doc, "weather.epw", design_day=True)

# Query results
ts = result.sql.get_timeseries(
    variable_name="Zone Mean Air Temperature",
    key_value="Office",
)
print(f"Max temp: {max(ts.values):.1f}°C")
```

## Find Weather Stations

```python
from idfkit.weather import StationIndex, geocode

index = StationIndex.load()
results = index.nearest(*geocode("Chicago, IL"))
print(results[0].station.display_name)
```

## Documentation

<div class="grid cards" markdown>

-   :material-rocket-launch:{ .lg .middle } **Get Started**

    ---

    Installation, quick start guide, and interactive tutorial.

    [:octicons-arrow-right-24: Get Started](getting-started/installation.md)

-   :material-school:{ .lg .middle } **Concepts**

    ---

    Architecture decisions, caching strategy, and design principles.

    [:octicons-arrow-right-24: Concepts](concepts/simulation-architecture.md)

-   :material-play-circle:{ .lg .middle } **Simulation**

    ---

    Run EnergyPlus, parse results, batch processing, and caching.

    [:octicons-arrow-right-24: Simulation Guide](simulation/index.md)

-   :material-weather-cloudy:{ .lg .middle } **Weather**

    ---

    Station search, downloads, design days, and geocoding.

    [:octicons-arrow-right-24: Weather Guide](weather/index.md)

-   :material-flask:{ .lg .middle } **Examples**

    ---

    Parametric studies, sizing workflows, and cloud simulations.

    [:octicons-arrow-right-24: Examples](examples/parametric-study.ipynb)

-   :material-api:{ .lg .middle } **API Reference**

    ---

    Complete API documentation for all modules.

    [:octicons-arrow-right-24: API Reference](api/document.md)

</div>

## More Resources

| Page | Description |
|------|-------------|
| [Core Tutorial](getting-started/core-tutorial.ipynb) | Interactive notebook covering basic, advanced, and expert usage |
| [Migrating from eppy](migration.md) | Side-by-side comparison of eppy and idfkit APIs |
| [Benchmarks](benchmarks.md) | Performance comparison against eppy and other tools |
| [Troubleshooting](troubleshooting/errors.md) | Common errors and solutions |
