from __future__ import annotations

from idfkit import IDFDocument, write_idf
from idfkit.migration import (
    AsyncMigrator,
    AsyncSubprocessMigrator,
    MigrationDiff,
    MigrationProgress,
    MigrationReport,
    MigrationStep,
    Migrator,
    SubprocessMigrator,
)
from idfkit.simulation import SimulationResult, simulate

doc: IDFDocument = ...  # type: ignore[assignment]
old_doc: IDFDocument = ...  # type: ignore[assignment]
new_doc: IDFDocument = ...  # type: ignore[assignment]
doc_v22: IDFDocument = ...  # type: ignore[assignment]
doc_v25: IDFDocument = ...  # type: ignore[assignment]
report: MigrationReport = ...  # type: ignore[assignment]
diff: MigrationDiff = ...  # type: ignore[assignment]
step: MigrationStep = ...  # type: ignore[assignment]
change: object = ...  # type: ignore[assignment]
chain: list[MigrationStep] = ...  # type: ignore[assignment]
result: SimulationResult = ...  # type: ignore[assignment]
migrator: Migrator = ...  # type: ignore[assignment]
async_migrator: AsyncMigrator = ...  # type: ignore[assignment]
subprocess_migrator: SubprocessMigrator = ...  # type: ignore[assignment]
async_subprocess_migrator: AsyncSubprocessMigrator = ...  # type: ignore[assignment]

# --8<-- [start:quickstart]
from idfkit import load_idf
from idfkit.migration import migrate
from idfkit.simulation import find_energyplus

doc = load_idf("legacy_v22.idf")  # version (22, 1, 0)
config = find_energyplus()  # e.g. (25, 2, 0)

report = migrate(doc, target_version=config.version, energyplus=config)
new_doc = report.migrated_model  # fresh IDFDocument at (25, 2, 0)
# --8<-- [end:quickstart]


# --8<-- [start:core-api]
from idfkit.migration import (
    migrate,  # sync entrypoint
    async_migrate,  # asyncio entrypoint
    MigrationReport,
    MigrationStep,
    MigrationDiff,
    MigrationProgress,
    Migrator,  # protocol (sync)
    AsyncMigrator,  # protocol (async)
    SubprocessMigrator,  # default backend
    AsyncSubprocessMigrator,
    plan_migration_chain,  # planning without execution
    document_diff,  # structural diff between two docs
)
# --8<-- [end:core-api]


# --8<-- [start:chain]
from idfkit.migration import plan_migration_chain

chain = plan_migration_chain(
    source=(22, 1, 0),
    target=(25, 2, 0),
)
for step in chain:
    print(step.from_version, "->", step.to_version, step.binary)
# --8<-- [end:chain]


# --8<-- [start:report]
report = migrate(doc, target_version=(25, 2, 0))

report.migrated_model  # IDFDocument
report.source_version  # (22, 1, 0)
report.target_version  # (25, 2, 0)
report.steps  # list[MigrationStep]
report.diff  # MigrationDiff (structural changes)
report.summary()  # human-readable rollup

for step in report.steps:
    print(step.from_version, "->", step.to_version)
    print(step.stdout)
    print(step.stderr)
    print(step.audit_text)  # contents of the transition audit file
    print(step.runtime_seconds)
# --8<-- [end:report]


# --8<-- [start:inspect-diff]
diff = report.diff
print(f"Added object types: {diff.added_object_types}")  # tuple[str, ...]
print(f"Removed object types: {diff.removed_object_types}")  # tuple[str, ...]
print(f"Object count changes: {diff.object_count_delta}")  # {type: signed delta}

# Per-type schema-level field renames (FieldDelta has .added / .removed)
for obj_type, delta in diff.field_changes.items():
    print(obj_type, "added fields:", delta.added, "removed fields:", delta.removed)
# --8<-- [end:inspect-diff]


# --8<-- [start:progress]
def on_progress(event: MigrationProgress) -> None:
    print(event.step_index, event.total_steps, event.from_version, "->", event.to_version, event.phase)


migrate(doc, target_version=(25, 2, 0), on_progress=on_progress)
# --8<-- [end:progress]


# --8<-- [start:async]
import asyncio
from idfkit.migration import async_migrate


async def main():
    report = await async_migrate(doc, target_version=(25, 2, 0))
    return report.migrated_model


new_doc = asyncio.run(main())
# --8<-- [end:async]


# --8<-- [start:custom-backend]
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
    ) -> (
        MigrationStepResult
    ): ...  # invoke a binary, return MigrationStepResult(idf_text=..., stdout=..., stderr=..., audit_text=...)


migrate(doc, target_version=(25, 2, 0), migrator=MyMigrator())
# --8<-- [end:custom-backend]


# --8<-- [start:document-diff]
from idfkit.migration import document_diff

diff = document_diff(old_doc, new_doc)
if diff.is_empty:
    print("No structural changes")
else:
    print("Added types:", diff.added_object_types)
    print("Removed types:", diff.removed_object_types)
    print("Count deltas:", diff.object_count_delta)
# --8<-- [end:document-diff]


# --8<-- [start:mistake-reversible-good]
doc_v22 = load_idf("legacy_v22.idf")  # keep this on disk
doc_v25 = migrate(doc_v22, target_version=(25, 2, 0)).migrated_model
# --8<-- [end:mistake-reversible-good]


# --8<-- [start:mistake-energyplus-good]
config = find_energyplus(version=(25, 2, 0))  # explicitly pick a newer install
migrate(doc, target_version=(25, 2, 0), energyplus=config)
# --8<-- [end:mistake-energyplus-good]


# --8<-- [start:mistake-automigrate-good]
report = migrate(doc, target_version=config.version)
new_doc = report.migrated_model  # IDFDocument at the target version
write_idf(new_doc, "migrated.idf")
result = simulate(new_doc, "weather.epw")
# --8<-- [end:mistake-automigrate-good]
