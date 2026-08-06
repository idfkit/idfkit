# Reference

Reference is the technical description of idfkit's machinery: classes,
functions, CLI commands, configuration keys, and their exact behaviour. It's
here to be consulted, not read cover to cover. When you need a fact — a
signature, a default, a valid range, an exit code — this is where it lives.

The bulk of the reference is **generated from docstrings**, so it stays faithful
to the code. For task-oriented walkthroughs, see the
[How-to guides](../how-to/index.md); for the reasoning behind the design, see
[Explanation](../explanation/index.md).

## Configuration & CLI

- [Environment variables](../concepts/environment-variables.md) — every variable
  idfkit reads, where it's read, and its default.
- [`idfkit tmy`](../cli/tmy.md) — the weather-data command-line tool.

## API

The complete API, generated from the source:

- **Core** — [Document](../api/document.md), [Objects](../api/objects.md),
  [I/O](../api/io.md), [Schema](../api/schema.md),
  [Validation](../api/validation.md), [Geometry](../api/geometry.md),
  [References](../api/references.md), [Thermal](../api/thermal.md),
  [Visualization](../api/visualization.md), [Exceptions](../api/exceptions.md),
  [Versions](../api/versions.md).
- **Simulation** — [Runner](../api/simulation/runner.md),
  [Async](../api/simulation/async.md), [Results](../api/simulation/results.md),
  [SQL](../api/simulation/sql.md), [Batch](../api/simulation/batch.md),
  [Cache](../api/simulation/cache.md), and more.
- **Weather** — [Station](../api/weather/station.md),
  [Download](../api/weather/download.md),
  [Design days](../api/weather/designday.md).

See the **API Reference** section in the navigation for the full list.
