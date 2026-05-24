# Version migration

`idfkit.migration` is a thin orchestration layer over EnergyPlus's `IDFVersionUpdater` transition binaries. Use it to forward-migrate an IDF (or `IDFDocument`) from an older EnergyPlus version to a newer one. Backward migration is **not** supported (EnergyPlus's binaries are one-way).

## When to use

- You have an old IDF and want to simulate it against a newer EnergyPlus installation.
- You're maintaining a fleet of models and want them all on the same version.
- You need to surface what transition steps changed during migration.

## Quick start

```python
from idfkit import load_idf
from idfkit.migration import migrate
from idfkit.simulation import find_energyplus

doc = load_idf("legacy_v22.idf")           # version (22, 1, 0)
config = find_energyplus()                 # e.g. (25, 2, 0)

report = migrate(doc, target_version=config.version, energyplus=config)
new_doc = report.migrated_model            # fresh IDFDocument at (25, 2, 0)
```

The same path is wired into `simulate(..., auto_migrate=True)` — see [simulation-execution.md](simulation-execution.md). Use the explicit `migrate(...)` form when you want to inspect or persist the migrated model independently of running a simulation.

## Core API

```python
from idfkit.migration import (
    migrate,                  # sync entrypoint
    async_migrate,            # asyncio entrypoint
    MigrationReport,
    MigrationStep,
    MigrationDiff,
    MigrationProgress,
    Migrator,                 # protocol (sync)
    AsyncMigrator,            # protocol (async)
    SubprocessMigrator,       # default backend
    AsyncSubprocessMigrator,
    plan_migration_chain,     # planning without execution
    document_diff,            # structural diff between two docs
)
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
from idfkit.migration import plan_migration_chain

chain = plan_migration_chain(
    source=(22, 1, 0),
    target=(25, 2, 0),
)
for step in chain:
    print(step.from_version, "->", step.to_version, step.binary)
```

A four-step chain (22.1 → 22.2 → 23.1 → 23.2 → 24.1 → 24.2 → 25.1 → 25.2) is normal — each step is a separate binary invocation.

## What `MigrationReport` contains

```python
report = migrate(doc, target_version=(25, 2, 0))

report.migrated_model                      # IDFDocument
report.source_version                      # (22, 1, 0)
report.target_version                      # (25, 2, 0)
report.steps                               # list[MigrationStep]
report.diff                                # MigrationDiff (structural changes)
report.summary()                           # human-readable rollup

for step in report.steps:
    print(step.from_version, "->", step.to_version)
    print(step.stdout)
    print(step.stderr)
    print(step.audit_text)                 # contents of the transition audit file
    print(step.runtime_seconds)
```

`MigrationDiff` surfaces what types/objects changed: added, removed, renamed (object-type rename, e.g. `HVACTemplate:Plant:ChilledWaterLoop` getting a new field), and modified.

## Inspecting changes

```python
diff = report.diff
print(f"Added: {len(diff.added)}")
print(f"Removed: {len(diff.removed)}")
print(f"Modified: {len(diff.modified)}")

for change in diff.modified[:5]:
    print(change.obj_type, change.name, change.field_changes)
```

## Progress events

```python
def on_progress(event: MigrationProgress) -> None:
    print(event.step_index, event.total_steps, event.from_version, "->", event.to_version, event.phase)

migrate(doc, target_version=(25, 2, 0), on_progress=on_progress)
```

## Async

```python
import asyncio
from idfkit.migration import async_migrate

async def main():
    report = await async_migrate(doc, target_version=(25, 2, 0))
    return report.migrated_model

new_doc = asyncio.run(main())
```

## Plugging a custom backend

```python
from pathlib import Path
from idfkit.migration import MigrationStepResult

class MyMigrator:
    def migrate_step(
        self,
        idf_text: str,
        from_version: tuple[int, int, int],
        to_version: tuple[int, int, int],
        *,
        work_dir: Path,
    ) -> MigrationStepResult:
        ...   # invoke a binary, return MigrationStepResult(idf_text=..., stdout=..., stderr=..., audit_text=...)

migrate(doc, target_version=(25, 2, 0), migrator=MyMigrator())
```

The default `SubprocessMigrator` shells out to the binaries shipped with the installed EnergyPlus. Custom backends are useful for containerised or remote migration services.

## Diffing two arbitrary documents

`document_diff` is exposed independently — useful for change reports outside migration:

```python
from idfkit.migration import document_diff

diff = document_diff(old_doc, new_doc)
print(diff.summary())
```

## Common mistakes

**BAD — assuming migration is reversible**

```python
report = migrate(doc, target_version=(22, 1, 0))   # MigrationError: backward migration not supported
```

**GOOD — keep the original and migrate forward**

```python
doc_v22 = load_idf("legacy_v22.idf")       # keep this on disk
doc_v25 = migrate(doc_v22, target_version=(25, 2, 0)).migrated_model
```

**BAD — running migrate without `energyplus` when the installed version is older**

```python
# Installed: 24.1; doc is 25.2 → no transition binaries exist to migrate forward
migrate(doc, target_version=(25, 2, 0))    # MigrationError
```

**GOOD — install a newer EnergyPlus, or migrate using one that has the binaries**

```python
config = find_energyplus(version=(25, 2, 0))   # explicitly pick a newer install
migrate(doc, target_version=(25, 2, 0), energyplus=config)
```

**BAD — assuming `simulate(auto_migrate=True)` persists the migrated model**

```python
result = simulate(doc, "weather.epw", auto_migrate=True)
# doc is unchanged; the migrated model was used for the simulation only.
```

**GOOD — call `migrate` explicitly and persist if you need it later**

```python
report = migrate(doc, target_version=config.version)
write_idf(report.migrated_model, "migrated.idf")
result = simulate(report.migrated_model, "weather.epw")
```

## Related

- [simulation-execution.md](simulation-execution.md) — `auto_migrate=True` for transparent migration.
- [parsing-idf-epjson.md](parsing-idf-epjson.md) — explicit version override at load time.
- CLI: `idfkit migrate <input.idf> <target_version>` migrates from the shell.
- API docs: [py.idfkit.com/api/migration/](https://py.idfkit.com/api/migration/)
