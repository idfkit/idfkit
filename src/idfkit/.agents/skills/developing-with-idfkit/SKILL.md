# Developing with idfkit

idfkit is a fast, modern EnergyPlus IDF/epJSON toolkit for Python. It provides O(1) object lookups, automatic cross-reference tracking, schema-driven validation, geometry helpers, and a simulation runner that wraps EnergyPlus. This skill folder is the entrypoint for agents writing code against idfkit.

## How to use this skill

Read `references/<topic>.md` for focused, task-oriented guidance. Each reference is self-contained and includes runnable code examples mined from the linted `docs/snippets/` directory and the test suite. When in doubt, fetch the smallest reference that covers your task — don't pre-load everything.

## Reference index

| Task | Reference |
|---|---|
| Build, load, query, or modify a model | [document-and-objects.md](references/document-and-objects.md) |
| Parse `.idf` / `.epJSON` files | [parsing-idf-epjson.md](references/parsing-idf-epjson.md) |
| Write `.idf` / `.epJSON` files | [writing-output.md](references/writing-output.md) |
| Validate a model against the schema | [schema-and-validation.md](references/schema-and-validation.md) |
| Find or update cross-references between objects | [reference-tracking.md](references/reference-tracking.md) |
| Compute surface area, zone volume, azimuth, WWR | [geometry-and-surfaces.md](references/geometry-and-surfaces.md) |
| Build a building footprint and zone it | [geometry-builders-and-zoning.md](references/geometry-builders-and-zoning.md) |
| Stand up an HVAC system quickly with `HVACTemplate:*` | [hvac-templates.md](references/hvac-templates.md) |
| Hand-author `AirLoopHVAC` / `PlantLoop` / `CondenserLoop` | [hvac-loops.md](references/hvac-loops.md) |
| Run EnergyPlus simulations (sync, async, batch) | [simulation-execution.md](references/simulation-execution.md) |
| Parse SQL / CSV / ERR simulation output | [result-parsing.md](references/result-parsing.md) |
| Find a weather station, download EPW/DDY, inject design days | [weather-data.md](references/weather-data.md) |
| Evaluate `Schedule:*` objects to time series | [schedule-evaluation.md](references/schedule-evaluation.md) |
| Compute R-value, U-value, SHGC, gas mixture properties | [thermal-properties.md](references/thermal-properties.md) |
| Render building geometry to 3D or SVG | [visualization.md](references/visualization.md) |
| Migrate a model forward across EnergyPlus versions | [version-migration.md](references/version-migration.md) |

## Conventions used in every reference

- **Imports come from `idfkit` directly** unless the symbol lives in a sub-package (`idfkit.simulation`, `idfkit.weather`, `idfkit.schedules`, `idfkit.thermal`, `idfkit.visualization`).
- **Python 3.10+** syntax: `tuple[int, int, int]`, `from __future__ import annotations` in real code.
- **Strict mode is the default**: unknown field names raise `InvalidFieldError`. Pass `strict=False` only as a tolerant migration fallback.
- **EnergyPlus version is part of every document**: `doc.version` is a `tuple[int, int, int]`. The latest supported version is exposed as `idfkit.LATEST_VERSION`.
- **Code snippets in references are mined from `docs/snippets/`** — they are linted with `ruff` and type-checked with `pyright`, so they run as-is.

## Common pitfalls

- `IDFObject` field names use Python-style snake_case (`zone.x_origin`, not `zone["X Origin"]`). The schema's IDD field names map to attribute names automatically.
- Renaming an object via `obj.name = "new"` propagates through the reference graph automatically. **Editing a node-name string elsewhere does not** — see [reference-tracking.md](references/reference-tracking.md).
- `HVACTemplate:*` objects must be expanded before EnergyPlus can simulate them. Either call `doc.expand(...)` explicitly, or pass `expand_objects=True` to `simulate(...)`. See [hvac-templates.md](references/hvac-templates.md).
- Simulations need EnergyPlus installed on the host. idfkit discovers it via `$ENERGYPLUS_DIR`, `$PATH`, or standard install locations. See [simulation-execution.md](references/simulation-execution.md).
