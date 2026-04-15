"""IDF model version migration.

Provides a thin orchestration layer over EnergyPlus's ``IDFVersionUpdater``
transition binaries, exposing a single entry point — [migrate][idfkit.migration.migrate]
— that forward-migrates an [IDFDocument][idfkit.document.IDFDocument] across
one or more EnergyPlus version steps.

The orchestrator handles:

- Planning the ordered chain of transition steps between source and target.
- Invoking each ``Transition-VX-to-VY`` binary in a temporary working directory.
- Capturing per-step stdout / stderr / audit output.
- Re-parsing the final IDF into a fresh [IDFDocument][idfkit.document.IDFDocument].
- Computing a structural [MigrationDiff][idfkit.migration.report.MigrationDiff].
- Emitting progress events via the same callback protocol used by the simulation
  runner.

The actual transformation rules live inside EnergyPlus's compiled Fortran
transition binaries; this module does *not* re-implement them.  Different
backends can be plugged in via the [Migrator][idfkit.migration.protocol.Migrator]
protocol — the default
[SubprocessMigrator][idfkit.migration.subprocess_backend.SubprocessMigrator]
shells out to the binaries shipped with the installed EnergyPlus distribution.

Example:
    ```python
    from idfkit import load_idf
    from idfkit.migration import migrate
    from idfkit.simulation import find_energyplus

    model = load_idf("old.idf")              # v22.1.0
    config = find_energyplus()               # e.g. 25.2.0 installed
    report = migrate(model, target_version=config.version, energyplus=config)
    report.migrated_model  # fresh IDFDocument at 25.2.0
    ```
"""

from __future__ import annotations

from .async_runner import async_migrate
from .async_subprocess_backend import AsyncSubprocessMigrator
from .chain import plan_migration_chain
from .diff import document_diff
from .progress import MigrationProgress
from .protocol import AsyncMigrator, MigrationStepResult, Migrator
from .report import MigrationDiff, MigrationReport, MigrationStep
from .runner import migrate
from .subprocess_backend import SubprocessMigrator

__all__ = [
    "AsyncMigrator",
    "AsyncSubprocessMigrator",
    "MigrationDiff",
    "MigrationProgress",
    "MigrationReport",
    "MigrationStep",
    "MigrationStepResult",
    "Migrator",
    "SubprocessMigrator",
    "async_migrate",
    "document_diff",
    "migrate",
    "plan_migration_chain",
]
