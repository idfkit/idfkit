# Version migration

`idfkit.migration` is a thin orchestration layer over EnergyPlus's `IDFVersionUpdater` transition binaries. Use it to forward-migrate an IDF (or `IDFDocument`) from an older EnergyPlus version to a newer one. Backward migration is **not** supported (EnergyPlus's binaries are one-way).

## When to use

- You have an old IDF and want to simulate it against a newer EnergyPlus installation.
- You're maintaining a fleet of models and want them all on the same version.
- You need to surface what transition steps changed during migration.

To keep editing an old model in its own release instead, type it for that release with `as_version` (see "Typing a document for its EnergyPlus version" in [document-and-objects.md](document-and-objects.md)). After migrating, `report.migrated_model` is typed for the release you name as the target (see [Typing the migrated document](#typing-the-migrated-document)).

## Quick start

```python
--8<-- "agent_references/snippets/version-migration.py:quickstart"
```

The same path is wired into `simulate(..., auto_migrate=True)` — see [simulation-execution.md](simulation-execution.md). Use the explicit `migrate(...)` form when you want to inspect or persist the migrated model independently of running a simulation.

## Core API

```python
--8<-- "agent_references/snippets/version-migration.py:core-api"
```

`migrate` always takes a parsed `IDFDocument` and returns a `MigrationReport` whose `migrated_model` attribute is the new document (a copy of the input when it is already at the target). The input is never mutated. The migrated document has no `filepath` (it is `None`), so a bare `new_doc.save()` raises `ValueError`: save it to a path you name, with `save_idf(new_doc, path)` or `new_doc.save(path)`. It is not tied to the source's path, because a bare save would overwrite the original file with a model at another version.

## Top-level signature

```text
migrate(
    model: IDFDocument,
    target_version: tuple[int, int, int] | str | type[IDFDocumentV...],
    *,
    energyplus: EnergyPlusConfig | None = None,   # default: auto-discover
    migrator: Migrator | None = None,             # plug a custom backend
    on_progress: Callable[[MigrationProgress], None] | None = None,
    work_dir: str | Path | None = None,           # default: a fresh tempdir
    keep_work_dir: bool = False,
    cache: bool = True,                           # reuse an earlier identical migration (not with work_dir/keep_work_dir)
) -> MigrationReport[...]
```

`async_migrate` mirrors this signature.

## Typing the migrated document

`MigrationReport` is generic in the type of `migrated_model`. Name the target as a document type from `idfkit.versioned` (`IDFDocumentV24_1`, or `IDFDocument` for the latest) and the report is typed for that release; a tuple or string target gives `AnyIDFDocument`, because a type checker cannot know which release a value names:

```python
--8<-- "agent_references/snippets/version-migration.py:typed-result"
```

The document type is also the target at run time: `migrate(doc, IDFDocumentV24_1)` migrates to 24.1.0. A migration reaches one release, so `AnyIDFDocument` and a union or tuple of document types raise `TypeError`; pyright and mypy reject `AnyIDFDocument`, and mypy rejects a union too, but pyright accepts a union (it tries each member against the overloads), so the run-time error is the one that catches it there. The migrated document keeps the source's `strict` setting, and a tuple or string target carries it into the type: `AnyIDFDocument[Literal[True]]` for a document from `load_idf`. A bare `MigrationReport` annotation accepts a report of any release. `migrated_model` is never `None`: on a no-op migration (the model is already at the target, `report.steps == ()`) it is a copy of the input, so `doc = migrate(doc, target_version=config.version).migrated_model` is safe whatever `doc`'s version. Under mypy the overloads resolve the same way, but mypy does not see a document's own properties, so prefer pyright (see [document-and-objects.md](document-and-objects.md)).

To write your own function generic over one release, as `migrate` is, use `ReleaseDocumentT` from `idfkit.versioned`: a type variable constrained to the release types, so `type[ReleaseDocumentT]` takes one release's type and refuses `AnyIDFDocument`.

## The migration chain

EnergyPlus ships one `Transition-VX-to-VY` binary per version step. idfkit plans a sequence of binaries to walk from source → target. Inspect the plan without executing:

```python
--8<-- "agent_references/snippets/version-migration.py:chain"
```

A seven-step chain (22.1 → 22.2 → 23.1 → 23.2 → 24.1 → 24.2 → 25.1 → 25.2) is normal — each step is a separate binary invocation.

Each step also renames output variables and meters (`Output:Variable`, `Output:Meter`, EMS sensors) from the `Report Variables <from> to <to>.csv` table next to the binary, so `Other Equipment FuelOil#1 Rate` becomes `Other Equipment FuelOilNo1 Rate` on 9.3 → 9.4. When an install lacks that table the binary skips the renames and still succeeds; idfkit logs a warning on the `idfkit.migration` logger, and the step's `stdout` says `... not found`.

## What `MigrationReport` contains

```python
--8<-- "agent_references/snippets/version-migration.py:report"
```

`MigrationDiff` surfaces what changed structurally: `added_object_types` and `removed_object_types` (tuples of type names), `object_count_delta` (per-type count changes), and `field_changes` (per-type `FieldDelta`s recording added/removed fields). Its `is_empty` property is `True` when nothing changed.

## Inspecting changes

```python
--8<-- "agent_references/snippets/version-migration.py:inspect-diff"
```

## Speed: migrate once, then batch

Each transition binary spends several seconds loading its IDDs, so a multi-step migration takes tens of seconds even for a tiny model. `migrate` and `async_migrate` remember the last 32 migrations in memory for the process, keyed by the source IDF's content, the steps and the EnergyPlus install. Migrating the same content again (as repeated `simulate(..., auto_migrate=True)` runs of one model do) only re-parses the result, and `report.from_cache` is `True`. Concurrent identical migrations run the binaries once.

The memo cannot help a parametric batch whose variants all differ: each `SimulationJob(auto_migrate=True)` migrates its own content. Migrate the seed once, then build the variants from the migrated model:

```python
--8<-- "agent_references/snippets/version-migration.py:migrate-once"
```

A custom backend is cached only when it has a `cache_key` string attribute; the bundled backends use their `IDFVersionUpdater` directory.

## Progress events

```python
--8<-- "agent_references/snippets/version-migration.py:progress"
```

## Async

```python
--8<-- "agent_references/snippets/version-migration.py:async"
```

## Plugging a custom backend

```python
--8<-- "agent_references/snippets/version-migration.py:custom-backend"
```

The default `SubprocessMigrator` shells out to the binaries shipped with the installed EnergyPlus. Custom backends are useful for containerised or remote migration services.

## Diffing two arbitrary documents

`document_diff` is exposed independently — useful for change reports outside migration:

```python
--8<-- "agent_references/snippets/version-migration.py:document-diff"
```

## Common mistakes

!!! failure "assuming migration is reversible"

    ```python
    report = migrate(doc, target_version=(22, 1, 0))   # MigrationError: backward migration not supported
    ```

!!! success "keep the original and migrate forward"

    ```python
    --8<-- "agent_references/snippets/version-migration.py:mistake-reversible-good"
    ```

!!! failure "running migrate without `energyplus` when the installed version is older"

    ```python
    # Installed: 24.1; doc is 25.2 → no transition binaries exist to migrate forward
    migrate(doc, target_version=(25, 2, 0))    # MigrationError
    ```

!!! success "install a newer EnergyPlus, or migrate using one that has the binaries"

    ```python
    --8<-- "agent_references/snippets/version-migration.py:mistake-energyplus-good"
    ```

!!! failure "assuming `simulate(auto_migrate=True)` persists the migrated model"

    ```python
    result = simulate(doc, "weather.epw", auto_migrate=True)
    # doc is unchanged; the migrated model was used for the simulation only.
    ```

!!! success "call `migrate` explicitly and persist if you need it later"

    ```python
    --8<-- "agent_references/snippets/version-migration.py:mistake-automigrate-good"
    ```

## Related

- [simulation-execution.md](simulation-execution.md) — `auto_migrate=True` for transparent migration.
- [parsing-idf-epjson.md](parsing-idf-epjson.md) — explicit version override at load time.
- CLI: `idfkit migrate <input.idf> [--to VERSION] [--energyplus PATH]` migrates from the shell. Without `--to` it targets the version of the EnergyPlus installation it uses, the newest that installation can simulate and migrate to. A chain with a step the installation has no transition binary for fails before any step runs.
- API docs: [py.idfkit.com/api/migration/](https://py.idfkit.com/api/migration/)
