# Reference

Reference states facts: what each package contains, how a command behaves, what
a format holds, and which defaults apply. These pages are here to be consulted,
not read cover to cover. When you need a signature, a default, a valid range,
or an exit code, this is where it lives. For a task, see the
[How-to guides](../how-to/index.md); for the reasoning behind the design, see
[Explanation](../explanation/index.md).

The API pages are generated from the source, so they stay faithful to the code.
Pages that describe one language only say so.

## Versions and schema data

- [Supported EnergyPlus versions](versions.md): the 17 releases both libraries
  bundle, how the version written in a file is matched to one of them, and
  which releases have generated static types.
- [Slim schema format](slim-schema-format.md): the reduced schema form
  `@idfkit/schemas` ships, key by key. TypeScript only.

## Python API

Generated from the docstrings in the source. The navigation carries the full
list; these are the entry points:

- **Core**: [Document](../api/document.md), [Objects](../api/objects.md),
  [I/O](../api/io.md), [Schema](../api/schema.md),
  [Validation](../api/validation.md), [Geometry](../api/geometry.md),
  [References](../api/references.md), [Thermal](../api/thermal.md),
  [Visualization](../api/visualization.md), [Exceptions](../api/exceptions.md),
  [Versions](../api/versions.md).
- **Simulation**: [Runner](../api/simulation/runner.md),
  [Async](../api/simulation/async.md), [Results](../api/simulation/results.md),
  [SQL](../api/simulation/sql.md), [Batch](../api/simulation/batch.md),
  [Cache](../api/simulation/cache.md).
- **Weather**: [Station](../api/weather/station.md),
  [Download](../api/weather/download.md),
  [Design days](../api/weather/designday.md).

## TypeScript API

Not published on this site yet. It will be generated from a pinned TypeDoc
artefact and will appear in this section. Until it does, the TSDoc comments it
is generated from are the ones your editor already shows for `@idfkit/core`,
`@idfkit/schemas`, and `@idfkit/weather`.

## CLI and configuration

Both pages describe the Python package. There is no JavaScript CLI, and the
JavaScript packages read no environment variables.

- [`idfkit tmy`](../cli/tmy.md): search for and download weather files.
- [Environment variables](../concepts/environment-variables.md): every variable
  idfkit reads, where it is read, and its default.

The other two commands are documented with the task they serve:
[`idfkit migrate`](../simulation/migrating-versions.md) forward-migrates a model
to a newer EnergyPlus version, and
[`idfkit check`](../concepts/version-compatibility.md) lints source for objects
and fields that do not exist in a target version.
