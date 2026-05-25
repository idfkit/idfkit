# Version migration

`idfkit.migration` is a thin orchestration layer over EnergyPlus's `IDFVersionUpdater` transition binaries. Use it to forward-migrate an IDF (or `IDFDocument`) from an older EnergyPlus version to a newer one. Backward migration is **not** supported (EnergyPlus's binaries are one-way).

## When to use

- You have an old IDF and want to simulate it against a newer EnergyPlus installation.
- You're maintaining a fleet of models and want them all on the same version.
- You need to surface what transition steps changed during migration.

## Quick start

```python
--8<-- "docs/snippets/agent_references/version-migration.py:quickstart"
```

The same path is wired into `simulate(..., auto_migrate=True)` — see [simulation-execution.md](simulation-execution.md). Use the explicit `migrate(...)` form when you want to inspect or persist the migrated model independently of running a simulation.

## Core API

```python
--8<-- "docs/snippets/agent_references/version-migration.py:core-api"
```

`migrate` always takes a parsed `IDFDocument` and returns a `MigrationReport` whose `migrated_model` attribute is the new document. The input is never mutated.

## Top-level signature

```text
migrate(
    model: IDFDocument,
    target_version: tuple[int, int, int] | str,
    *,
    energyplus: EnergyPlusConfig | None = None,   # default: auto-discover
    migrator: Migrator | None = None,             # plug a custom backend
    on_progress: Callable[[MigrationProgress], None] | None = None,
    work_dir: str | Path | None = None,           # default: a fresh tempdir
    keep_work_dir: bool = False,
) -> MigrationReport
```

`async_migrate` mirrors this signature.

## The migration chain

EnergyPlus ships one `Transition-VX-to-VY` binary per version step. idfkit plans a sequence of binaries to walk from source → target. Inspect the plan without executing:

```python
--8<-- "docs/snippets/agent_references/version-migration.py:chain"
```

A four-step chain (22.1 → 22.2 → 23.1 → 23.2 → 24.1 → 24.2 → 25.1 → 25.2) is normal — each step is a separate binary invocation.

## What `MigrationReport` contains

```python
--8<-- "docs/snippets/agent_references/version-migration.py:report"
```

`MigrationDiff` surfaces what changed structurally: `added_object_types` and `removed_object_types` (tuples of type names), `object_count_delta` (per-type count changes), and `field_changes` (per-type `FieldDelta`s recording added/removed fields). Its `is_empty` property is `True` when nothing changed.

## Inspecting changes

```python
--8<-- "docs/snippets/agent_references/version-migration.py:inspect-diff"
```

## Progress events

```python
--8<-- "docs/snippets/agent_references/version-migration.py:progress"
```

## Async

```python
--8<-- "docs/snippets/agent_references/version-migration.py:async"
```

## Plugging a custom backend

```python
--8<-- "docs/snippets/agent_references/version-migration.py:custom-backend"
```

The default `SubprocessMigrator` shells out to the binaries shipped with the installed EnergyPlus. Custom backends are useful for containerised or remote migration services.

## Diffing two arbitrary documents

`document_diff` is exposed independently — useful for change reports outside migration:

```python
--8<-- "docs/snippets/agent_references/version-migration.py:document-diff"
```

## Common mistakes

!!! failure "assuming migration is reversible"

    ```python
    report = migrate(doc, target_version=(22, 1, 0))   # MigrationError: backward migration not supported
    ```

!!! success "keep the original and migrate forward"

    ```python
    --8<-- "docs/snippets/agent_references/version-migration.py:mistake-reversible-good"
    ```

!!! failure "running migrate without `energyplus` when the installed version is older"

    ```python
    # Installed: 24.1; doc is 25.2 → no transition binaries exist to migrate forward
    migrate(doc, target_version=(25, 2, 0))    # MigrationError
    ```

!!! success "install a newer EnergyPlus, or migrate using one that has the binaries"

    ```python
    --8<-- "docs/snippets/agent_references/version-migration.py:mistake-energyplus-good"
    ```

!!! failure "assuming `simulate(auto_migrate=True)` persists the migrated model"

    ```python
    result = simulate(doc, "weather.epw", auto_migrate=True)
    # doc is unchanged; the migrated model was used for the simulation only.
    ```

!!! success "call `migrate` explicitly and persist if you need it later"

    ```python
    --8<-- "docs/snippets/agent_references/version-migration.py:mistake-automigrate-good"
    ```

## Related

- [simulation-execution.md](simulation-execution.md) — `auto_migrate=True` for transparent migration.
- [parsing-idf-epjson.md](parsing-idf-epjson.md) — explicit version override at load time.
- CLI: `idfkit migrate <input.idf> <target_version>` migrates from the shell.
- API docs: [py.idfkit.com/api/migration/](https://py.idfkit.com/api/migration/)
