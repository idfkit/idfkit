# Migrating Versions

EnergyPlus ships a new release roughly twice a year, and each release can
rename objects, drop fields, or alter defaults. idfkit's
[`migrate()`][idfkit.migration.runner.migrate] orchestrates the
`Transition-VX-to-VY` binaries shipped in `PreProcess/IDFVersionUpdater` to
forward-migrate an IDF model across one or more version steps in a single
call.

There are two ways to migrate a model:

| Approach | When to use |
|----------|-------------|
| Explicit `migrate(model, target_version=...)` | You want to inspect the migrated model, the structural diff, or per-step diagnostics before doing anything else. |
| `simulate(model, ..., auto_migrate=True)` | You want to run a simulation against the installed EnergyPlus and don't care about the intermediate steps. |

!!! note "Forward only"
    EnergyPlus does not ship reverse transition binaries. Asking to migrate
    *backwards* (target older than source) always raises
    [`VersionMismatchError`][idfkit.exceptions.VersionMismatchError] with
    `direction == "backward"`.

## Explicit Migration

Call [`migrate()`][idfkit.migration.runner.migrate] directly when you need
the migrated [`IDFDocument`][idfkit.document.IDFDocument] in hand:

```python
--8<-- "docs/snippets/migration_versions/quick_start.py:example"
```

The returned [`MigrationReport`][idfkit.migration.report.MigrationReport]
exposes:

| Attribute | Description |
|-----------|-------------|
| `migrated_model` | The migrated `IDFDocument` (`None` on a no-op migration where source equals target). |
| `source_version` / `target_version` | The version range actually traversed. |
| `requested_target` | The version originally requested — differs from `target_version` only on partial failures. |
| `steps` | Ordered tuple of [`MigrationStep`][idfkit.migration.report.MigrationStep] records with stdout/stderr/audit per binary invocation. |
| `diff` | Structural [`MigrationDiff`][idfkit.migration.report.MigrationDiff] — added/removed object types, count deltas, and per-type field changes. |
| `success` | `True` only when every step succeeded. |
| `summary()` | Short human-readable summary suitable for logs or CLI. |

## CLI

The `idfkit migrate` subcommand is a thin wrapper over `migrate()` for shell
users. It loads the input IDF, forward-migrates it through the installed
`IDFVersionUpdater` transition binaries, and writes the result to disk.

### Basic usage

```bash
# Migrate to the latest supported version; writes old-v25-2-0.idf next to input
idfkit migrate old.idf

# Explicit target and output path
idfkit migrate old.idf --to 25.2 -o new.idf

# Machine-readable report (suppresses stderr progress output)
idfkit migrate old.idf --to 25.2 --json
```

When `--to` is omitted the target is the latest supported version. When
`--output` is omitted the result is written to `<stem>-v<major>-<minor>-<patch>.idf`
next to the input.

### Exit codes

| Code | Meaning |
|------|---------|
| `0` | Migration succeeded (or source version equals target — no-op) |
| `1` | Migration runtime failure (a transition binary exited non-zero) |
| `2` | Argument or configuration error (bad version, missing input, EnergyPlus not found) |

### Flag reference

| Flag | Description |
|------|-------------|
| `INPUT` | Path to the source IDF file (positional, required) |
| `-o`, `--output OUTPUT` | Output IDF path. Defaults to `<stem>-v<target>.idf` next to the input. |
| `--to VERSION` | Target EnergyPlus version (e.g. `25.2`). Defaults to the latest supported. |
| `--energyplus PATH` | Path to the EnergyPlus install or executable. Auto-discovered via `$ENERGYPLUS_DIR`, `PATH`, and platform defaults when omitted. |
| `--work-dir DIR` | Directory in which to stage per-step transition output. Defaults to a temporary directory. |
| `--keep-work-dir` | Preserve intermediate files for inspection (only meaningful with the default temp directory). |
| `--json` | Emit a JSON report on stdout instead of the human-readable summary. Also suppresses stderr progress output. |
| `-q`, `--quiet` | Suppress progress output. |

## Transparent Migration During `simulate()`

When you only want a simulation result, pass `auto_migrate=True` and
`simulate()` will forward-migrate the model on your behalf if the
installed EnergyPlus version differs:

```python
--8<-- "docs/snippets/migration_versions/auto_migrate_simulate.py:example"
```

The resulting [`SimulationResult.migration_report`][idfkit.simulation.result.SimulationResult.migration_report]
is populated whenever a migration ran, and `None` otherwise. Without
`auto_migrate=True`, a version mismatch raises
[`VersionMismatchError`][idfkit.exceptions.VersionMismatchError] before the
simulation starts.

## Async Migration

Both APIs have async counterparts with identical semantics:

- [`async_migrate()`][idfkit.migration.async_runner.async_migrate] — non-blocking
  equivalent of `migrate()`, useful inside FastAPI handlers or other async
  contexts where you want only the migration.
- [`async_simulate(..., auto_migrate=True)`][idfkit.simulation.async_runner.async_simulate]
  — accepts the same `auto_migrate` flag and populates `migration_report`
  on the returned `SimulationResult`.

## Partial Failures

If a transition step fails midway,
[`MigrationError`][idfkit.exceptions.MigrationError] is raised. The
exception carries `from_version`, `to_version`, the binary's `exit_code`
and `stderr`, and `completed_steps` — the prefix of `(from, to)` pairs that
ran successfully — so you can recover partial progress or report exactly
which transition broke.

## See Also

- [Migration API](../api/migration.md) — full reference for `migrate`, `MigrationReport`, and the `Migrator` protocol.
- [Version Compatibility](../concepts/version-compatibility.md) — the sibling `idfkit check` subcommand for *statically* linting your Python code for cross-version breakage before you migrate.
- [Running Simulations](running.md) — full `simulate()` parameter reference.
- [Error Handling](errors.md) — handling `VersionMismatchError` from `simulate()`.
