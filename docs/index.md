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

- **O(1) object lookups** -- collections are indexed by name, so
  `doc["Zone"]["Office"]` is a dict lookup, not a linear scan.
- **Automatic reference tracking** -- a live reference graph keeps track of
  every cross-object reference. Renaming an object updates every field that
  pointed to the old name.
- **IDF + epJSON** -- read and write both formats; convert between them in a
  single call.
- **Schema-driven validation** -- validate documents against the official
  EnergyPlus epJSON schema with detailed error messages.
- **Built-in 3D geometry** -- `Vector3D` and `Polygon3D` classes for surface
  area, zone volume, and coordinate transforms without external dependencies.
- **Memory-efficient** -- slot-based objects and gzip-compressed schema bundles
  keep the footprint small.
- **Broad version support** -- bundled schemas for every EnergyPlus release
  from v8.9 through v25.2.
- **eppy compatibility layer** -- methods like `idfobjects`, `newidfobject`,
  and `getsurfaces` work out of the box so migration can be gradual.

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

## What's Next

| Page | Description |
|------|-------------|
| [Getting Started](getting_started.ipynb) | Interactive notebook walking through basic, advanced, and expert usage. |
| [Migrating from eppy](migration.md) | Side-by-side comparison of eppy and idfkit APIs. |
| [Benchmarks](benchmarks.md) | Performance comparison against eppy and other EnergyPlus toolkits. |
| [API Reference](api/document.md) | Full module-by-module API documentation. |
