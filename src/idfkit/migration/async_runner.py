"""Async counterpart to [migrate()][idfkit.migration.runner.migrate].

Drives an [AsyncMigrator][idfkit.migration.protocol.AsyncMigrator] through the
planned chain without blocking the event loop. Accepts both sync and async
``on_progress`` callbacks, mirroring
[async_simulate][idfkit.simulation.async_runner.async_simulate].
"""

from __future__ import annotations

import asyncio
import inspect
import logging
import shutil
import tempfile
import time
from collections.abc import Awaitable, Callable
from pathlib import Path
from typing import TYPE_CHECKING, Any

from ..exceptions import EnergyPlusNotFoundError, MigrationError
from .async_subprocess_backend import AsyncSubprocessMigrator
from .chain import normalize_target, plan_migration_chain
from .diff import document_diff, verify_migration_output
from .progress import MigrationProgress
from .report import MigrationDiff, MigrationReport, MigrationStep

if TYPE_CHECKING:
    from ..document import IDFDocument
    from ..simulation.config import EnergyPlusConfig
    from .protocol import AsyncMigrator

logger = logging.getLogger(__name__)

OnMigrationProgress = Callable[[MigrationProgress], Any] | Callable[[MigrationProgress], Awaitable[Any]]


async def async_migrate(
    model: IDFDocument,
    target_version: tuple[int, int, int] | str,
    *,
    energyplus: EnergyPlusConfig | None = None,
    migrator: AsyncMigrator | None = None,
    on_progress: OnMigrationProgress | None = None,
    work_dir: str | Path | None = None,
    keep_work_dir: bool = False,
) -> MigrationReport:
    """Async counterpart to [migrate()][idfkit.migration.runner.migrate].

    Same semantics as the sync version; the only difference is that each
    transition step is driven via [asyncio.create_subprocess_exec][] (or a
    caller-supplied [AsyncMigrator][idfkit.migration.protocol.AsyncMigrator]),
    and progress callbacks may be async.

    Args:
        model: The document to migrate.
        target_version: Target version (tuple or dotted string).
        energyplus: EnergyPlus installation. Ignored when *migrator* is set.
        migrator: Optional [AsyncMigrator][idfkit.migration.protocol.AsyncMigrator].
            When ``None``, defaults to an
            [AsyncSubprocessMigrator][idfkit.migration.async_subprocess_backend.AsyncSubprocessMigrator]
            rooted at the installed EnergyPlus's IDFVersionUpdater directory.
        on_progress: Optional sync or async callback receiving
            [MigrationProgress][idfkit.migration.progress.MigrationProgress]
            events.
        work_dir: Directory in which to stage per-step working directories.
            Defaults to a newly-created temporary directory that is removed
            after the migration unless *keep_work_dir* is ``True``.
        keep_work_dir: Preserve intermediate files for inspection.

    Returns:
        A [MigrationReport][idfkit.migration.report.MigrationReport].

    Raises:
        idfkit.exceptions.UnsupportedVersionError: For an unsupported version.
        ValueError: If the target is older than ``model.version``.
        idfkit.exceptions.MigrationError: On any transition-step failure; the
            exception's ``completed_steps`` records the prefix that succeeded.
        idfkit.exceptions.EnergyPlusNotFoundError: If *migrator* is ``None``
            and no EnergyPlus installation can be discovered.
    """
    target = normalize_target(target_version)
    source = model.version

    await _emit(on_progress, MigrationProgress(phase="planning", message="Planning migration chain"))
    chain = plan_migration_chain(source, target)

    if not chain:
        await _emit(
            on_progress,
            MigrationProgress(phase="complete", message="Source equals target; nothing to do", percent=100.0),
        )
        return MigrationReport(
            migrated_model=None,
            source_version=source,
            target_version=target,
            requested_target=target,
            steps=(),
            diff=MigrationDiff(),
        )

    resolved_migrator = await asyncio.to_thread(_resolve_async_migrator, migrator, energyplus)
    total_steps = len(chain)
    await _emit(
        on_progress,
        MigrationProgress(
            phase="preparing",
            message=f"Running {total_steps} transition step{'s' if total_steps != 1 else ''}",
            total_steps=total_steps,
        ),
    )

    owned_work_dir = work_dir is None
    root = Path(tempfile.mkdtemp(prefix="idfkit_migrate_")) if owned_work_dir else Path(work_dir).resolve()
    if not owned_work_dir:
        root.mkdir(parents=True, exist_ok=True)

    try:
        report = await _run_chain_async(
            model=model,
            chain=chain,
            migrator=resolved_migrator,
            work_root=root,
            on_progress=on_progress,
            source=source,
            target=target,
        )
    finally:
        if owned_work_dir and not keep_work_dir:
            await asyncio.to_thread(shutil.rmtree, root, True)

    return report


async def _run_chain_async(
    *,
    model: IDFDocument,
    chain: tuple[tuple[tuple[int, int, int], tuple[int, int, int]], ...],
    migrator: AsyncMigrator,
    work_root: Path,
    on_progress: OnMigrationProgress | None,
    source: tuple[int, int, int],
    target: tuple[int, int, int],
) -> MigrationReport:
    """Drive every step in *chain* through an async migrator."""
    from ..idf_parser import parse_idf
    from ..writers import write_idf

    initial_idf = work_root / "step_0_input.idf"
    await asyncio.to_thread(write_idf, model, initial_idf)
    current_text = await asyncio.to_thread(initial_idf.read_text, "latin-1")

    steps: list[MigrationStep] = []
    completed_pairs: list[tuple[tuple[int, int, int], tuple[int, int, int]]] = []

    for idx, (a, b) in enumerate(chain):
        await _emit(
            on_progress,
            MigrationProgress(
                phase="transitioning",
                message=f"Transitioning {_vstr(a)} -> {_vstr(b)}",
                step_index=idx,
                total_steps=len(chain),
                from_version=a,
                to_version=b,
                percent=100.0 * idx / len(chain),
            ),
        )

        step_dir = work_root / f"step_{idx + 1}_{_vstr(a)}_to_{_vstr(b)}"
        start = time.monotonic()
        try:
            step_result = await migrator.migrate_step(current_text, a, b, work_dir=step_dir)
        except MigrationError as exc:
            steps.append(
                MigrationStep(
                    from_version=a,
                    to_version=b,
                    success=False,
                    binary=_infer_binary(migrator, a, b),
                    stdout="",
                    stderr=exc.stderr or "",
                    audit_text=None,
                    runtime_seconds=time.monotonic() - start,
                )
            )
            raise MigrationError(
                str(exc),
                from_version=a,
                to_version=b,
                exit_code=exc.exit_code,
                stderr=exc.stderr,
                completed_steps=tuple(completed_pairs),
            ) from exc

        elapsed = time.monotonic() - start
        steps.append(
            MigrationStep(
                from_version=a,
                to_version=b,
                success=True,
                binary=_infer_binary(migrator, a, b),
                stdout=step_result.stdout,
                stderr=step_result.stderr,
                audit_text=step_result.audit_text,
                runtime_seconds=elapsed,
            )
        )
        completed_pairs.append((a, b))
        current_text = step_result.idf_text

    await _emit(
        on_progress,
        MigrationProgress(
            phase="reparsing",
            message="Re-parsing migrated IDF",
            total_steps=len(chain),
            percent=100.0,
        ),
    )
    final_idf = work_root / "migrated.idf"
    await asyncio.to_thread(final_idf.write_text, current_text, "latin-1")
    migrated = await asyncio.to_thread(parse_idf, final_idf, version=target)
    verify_migration_output(
        model,
        migrated,
        target_version=target,
        completed_steps=tuple(completed_pairs),
    )

    await _emit(on_progress, MigrationProgress(phase="diffing", message="Computing structural diff"))
    diff = await asyncio.to_thread(document_diff, model, migrated)

    await _emit(on_progress, MigrationProgress(phase="complete", message="Migration complete", percent=100.0))

    return MigrationReport(
        migrated_model=migrated,
        source_version=source,
        target_version=target,
        requested_target=target,
        steps=tuple(steps),
        diff=diff,
    )


def _resolve_async_migrator(
    migrator: AsyncMigrator | None,
    energyplus: EnergyPlusConfig | None,
) -> AsyncMigrator:
    """Resolve the async migrator, falling back to AsyncSubprocessMigrator."""
    if migrator is not None:
        return migrator

    config: EnergyPlusConfig
    if energyplus is not None:
        config = energyplus
    else:
        from ..simulation.config import find_energyplus

        config = find_energyplus()

    updater_dir = config.version_updater_dir
    if updater_dir is None:
        raise EnergyPlusNotFoundError(
            [str(config.install_dir / "PreProcess" / "IDFVersionUpdater")],
        )
    return AsyncSubprocessMigrator(version_updater_dir=updater_dir)


def _infer_binary(
    migrator: AsyncMigrator,
    from_version: tuple[int, int, int],
    to_version: tuple[int, int, int],
) -> Path | None:
    """Return the transition binary path for a step, when the migrator exposes one."""
    locate = getattr(migrator, "locate_binary", None)
    if locate is None:
        return None
    try:
        return locate(from_version, to_version)
    except MigrationError:
        return None


async def _emit(
    on_progress: OnMigrationProgress | None,
    event: MigrationProgress,
) -> None:
    """Dispatch *event* to *on_progress*, supporting sync or async callbacks.

    Exceptions raised by the callback are logged and swallowed so they don't
    poison the migration run.
    """
    if on_progress is None:
        return
    try:
        if inspect.iscoroutinefunction(on_progress):
            await on_progress(event)
        else:
            result = on_progress(event)
            if inspect.isawaitable(result):
                await result
    except Exception:
        logger.warning("on_progress callback raised; ignoring", exc_info=True)


def _vstr(v: tuple[int, int, int]) -> str:
    return f"{v[0]}.{v[1]}.{v[2]}"
