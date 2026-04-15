"""Backend protocol for single-step IDF version transitions.

A [Migrator][idfkit.migration.protocol.Migrator] knows how to migrate an IDF
text from one EnergyPlus version to the next adjacent version. The top-level
[migrate()][idfkit.migration.runner.migrate] function chains these single-step
calls together according to a plan produced by
[plan_migration_chain()][idfkit.migration.chain.plan_migration_chain].

The default implementation,
[SubprocessMigrator][idfkit.migration.subprocess_backend.SubprocessMigrator],
invokes the ``Transition-VX-to-VY`` binaries shipped in
``PreProcess/IDFVersionUpdater`` of an EnergyPlus installation. Other backends
(e.g. vendored binaries, a pure-Python port) can be plugged in without
changing the public API.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Protocol, runtime_checkable


@dataclass(frozen=True, slots=True)
class MigrationStepResult:
    """Result of a single-step migration.

    Attributes:
        idf_text: The migrated IDF source text.
        stdout: Captured standard output (may be empty).
        stderr: Captured standard error (may be empty).
        audit_text: Contents of the per-step ``.audit`` file if produced by
            the backend, else ``None``.
    """

    idf_text: str
    stdout: str = ""
    stderr: str = ""
    audit_text: str | None = None


@runtime_checkable
class Migrator(Protocol):
    """Protocol implemented by backends that migrate IDF text one version at a time."""

    def migrate_step(
        self,
        idf_text: str,
        from_version: tuple[int, int, int],
        to_version: tuple[int, int, int],
        *,
        work_dir: Path,
    ) -> MigrationStepResult:
        """Migrate *idf_text* from *from_version* to *to_version*.

        Args:
            idf_text: The source IDF text.
            from_version: The source version; the migrator should assume the
                IDF conforms to this version's IDD.
            to_version: The target version; the migrator must emit IDF text
                that conforms to this version's IDD.
            work_dir: A clean working directory the backend may use for
                intermediate files. Caller owns cleanup.

        Returns:
            The [MigrationStepResult][idfkit.migration.protocol.MigrationStepResult]
            for this single step.

        Raises:
            idfkit.exceptions.MigrationError: If the migration fails.
        """
        ...


@runtime_checkable
class AsyncMigrator(Protocol):
    """Async counterpart to [Migrator][idfkit.migration.protocol.Migrator].

    Implementations perform a single version-step migration without blocking
    the event loop. The default implementation,
    [AsyncSubprocessMigrator][idfkit.migration.async_subprocess_backend.AsyncSubprocessMigrator],
    uses [asyncio.create_subprocess_exec][] to drive the ``Transition-VX-to-VY``
    binaries shipped with EnergyPlus.
    """

    async def migrate_step(
        self,
        idf_text: str,
        from_version: tuple[int, int, int],
        to_version: tuple[int, int, int],
        *,
        work_dir: Path,
    ) -> MigrationStepResult:
        """Async counterpart to [Migrator.migrate_step][idfkit.migration.protocol.Migrator.migrate_step]."""
        ...
