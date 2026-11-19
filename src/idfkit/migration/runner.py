"""Top-level migration orchestration.

``migrate()`` plans a chain of transition steps, drives a [Migrator][idfkit.migration.protocol.Migrator]
through each step, captures per-step diagnostics, re-parses the final IDF, and
returns a structured [MigrationReport][idfkit.migration.report.MigrationReport].
"""

from __future__ import annotations

import logging
import shutil
import tempfile
import time
from collections.abc import Callable
from pathlib import Path
from typing import TYPE_CHECKING, Any, overload

from ..exceptions import EnergyPlusNotFoundError, MigrationError
from . import cache as migration_cache
from ._reparse import parse_migrated_idf, unmigrated_copy
from ._typing import StrictT
from .chain import check_chain_binaries, normalize_target, plan_migration_chain, resolve_source_version
from .diff import document_diff, verify_migration_output
from .progress import MigrationProgress
from .report import MigrationDiff, MigrationReport, MigrationStep
from .subprocess_backend import SubprocessMigrator

if TYPE_CHECKING:
    from typing import TypedDict

    from typing_extensions import Unpack

    from ..document import AnyIDFDocument
    from ..simulation.config import EnergyPlusConfig
    from ..versioned import ReleaseDocumentT
    from .protocol import Migrator

logger = logging.getLogger(__name__)

OnMigrationProgress = Callable[[MigrationProgress], Any]


if TYPE_CHECKING:

    class _MigrateOptions(TypedDict, total=False):
        """The keyword options of [migrate()][idfkit.migration.migrate], declared once for its overloads."""

        energyplus: EnergyPlusConfig | None
        migrator: Migrator | None
        on_progress: OnMigrationProgress | None
        work_dir: str | Path | None
        keep_work_dir: bool
        cache: bool


@overload
def migrate(
    model: AnyIDFDocument,
    target_version: type[ReleaseDocumentT],
    **options: Unpack[_MigrateOptions],
) -> MigrationReport[ReleaseDocumentT]: ...
@overload
def migrate(
    model: AnyIDFDocument[StrictT],
    target_version: tuple[int, int, int] | str,
    **options: Unpack[_MigrateOptions],
) -> MigrationReport[AnyIDFDocument[StrictT]]: ...
def migrate(
    model: AnyIDFDocument,
    target_version: tuple[int, int, int] | str | type[AnyIDFDocument[Any]],
    *,
    energyplus: EnergyPlusConfig | None = None,
    migrator: Migrator | None = None,
    on_progress: OnMigrationProgress | None = None,
    work_dir: str | Path | None = None,
    keep_work_dir: bool = False,
    cache: bool = True,
) -> MigrationReport[AnyIDFDocument[Any]]:
    """Forward-migrate *model* to *target_version* through EnergyPlus transition binaries.

    Plans the chain of transition steps between ``model.version`` and
    *target_version*, runs each one in sequence via the supplied *migrator*
    (defaulting to a [SubprocessMigrator][idfkit.migration.subprocess_backend.SubprocessMigrator]
    rooted at the EnergyPlus installation's ``PreProcess/IDFVersionUpdater``
    directory), re-parses the final IDF into a fresh
    [IDFDocument][idfkit.document.IDFDocument], and returns a structured
    [MigrationReport][idfkit.migration.report.MigrationReport].

    The input *model* is never mutated.

    Args:
        model: The document to migrate. Its ``version`` defines the source.
        target_version: A ``(major, minor, patch)`` tuple, a dotted string
            (e.g. ``"25.2.0"``), or the document type of the target release,
            such as ``IDFDocumentV24_1`` from ``idfkit.versioned`` or
            ``IDFDocument`` for the latest. A document type also types the
            report: ``migrated_model`` is then typed for that release, while a
            tuple or string, whose release a type checker cannot know, gives
            ``AnyIDFDocument``.
        energyplus: Pre-configured EnergyPlus installation. Ignored when
            *migrator* is provided. When neither is supplied,
            [find_energyplus()][idfkit.simulation.config.find_energyplus] is used
            to discover an installation automatically.
        migrator: Custom backend implementing
            [Migrator][idfkit.migration.protocol.Migrator]. Overrides
            *energyplus* when provided.
        on_progress: Optional callback invoked with
            [MigrationProgress][idfkit.migration.progress.MigrationProgress]
            events on every phase transition.
        work_dir: Directory in which to stage per-step work subdirectories.
            Defaults to a newly-created temporary directory. The directory is
            removed after migration unless *keep_work_dir* is ``True``.
        keep_work_dir: Set ``True`` to preserve intermediate files for
            inspection.
        cache: Reuse the result of an earlier migration of the same IDF
            content along the same steps with the same EnergyPlus install,
            kept in memory for this process (see
            [idfkit.migration.cache][idfkit.migration.cache]). The transition
            binaries take seconds per step, so this is what makes repeated
            ``simulate(..., auto_migrate=True)`` runs of one model cheap. The
            report's ``from_cache`` says whether the binaries ran. Set
            ``False`` to always run them. Ignored when *work_dir* or
            *keep_work_dir* is given: those ask for the per-step files, so the
            binaries always run.

    Returns:
        A [MigrationReport][idfkit.migration.report.MigrationReport] whose
        ``migrated_model`` is the document at the target version. On a no-op
        migration (source equals target) no step runs and it is a copy of
        *model*, so ``migrate(doc, version).migrated_model`` is a document
        whatever *doc*'s version.
        The migrated document has no ``filepath`` (it is ``None``): it was
        read from a scratch file in the work directory, and the source's path
        would make a bare ``save()`` overwrite the original with a model at
        another version. Save it to an explicit path, e.g.
        ``save_idf(report.migrated_model, path)`` or
        ``report.migrated_model.save(path)``.

    Raises:
        idfkit.exceptions.UnsupportedVersionError: If the target version is
            not in `ENERGYPLUS_VERSIONS`, or no supported release shares the
            model's major and minor version. A two-component version read from
            a file (``Version, 9.0;`` as ``(9, 0, 0)``) resolves to its
            release (9.0.1), as schema selection does.
        TypeError: If *target_version* is a type that names no single release,
            such as ``AnyIDFDocument`` or a union or tuple of document types,
            or is neither a version nor a type.
        ValueError: If *target_version* is older than ``model.version``
            (backward migration is not supported).
        idfkit.exceptions.MigrationError: If any transition step fails. The
            exception's ``completed_steps`` attribute records the prefix of
            steps that succeeded; inspect it to recover partial progress.
            A step the migrator has no transition binary for is reported
            before any step runs.
        idfkit.exceptions.EnergyPlusNotFoundError: If *migrator* is ``None``
            and no EnergyPlus installation can be discovered.
    """
    target = normalize_target(target_version)
    source = resolve_source_version(model.version)

    _emit(on_progress, MigrationProgress(phase="planning", message="Planning migration chain"))
    chain = plan_migration_chain(source, target)

    if not chain:
        _emit(
            on_progress,
            MigrationProgress(phase="complete", message="Source equals target; nothing to do", percent=100.0),
        )
        return MigrationReport(
            migrated_model=unmigrated_copy(model, target),
            source_version=source,
            target_version=target,
            requested_target=target,
            steps=(),
            diff=MigrationDiff(),
        )

    resolved_migrator = _resolve_migrator(migrator, energyplus)
    check_chain_binaries(resolved_migrator, chain)
    total_steps = len(chain)
    _emit(
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
        report = _run_chain(
            model=model,
            chain=chain,
            migrator=resolved_migrator,
            work_root=root,
            on_progress=on_progress,
            source=source,
            target=target,
            # Asking for the work directory means asking to inspect the per-step files,
            # which a cache hit would not write.
            use_cache=cache and work_dir is None and not keep_work_dir,
        )
    finally:
        if owned_work_dir and not keep_work_dir:
            shutil.rmtree(root, ignore_errors=True)

    return report


def _run_chain(
    *,
    model: AnyIDFDocument,
    chain: tuple[tuple[tuple[int, int, int], tuple[int, int, int]], ...],
    migrator: Migrator,
    work_root: Path,
    on_progress: OnMigrationProgress | None,
    source: tuple[int, int, int],
    target: tuple[int, int, int],
    use_cache: bool = True,
) -> MigrationReport[AnyIDFDocument[bool]]:
    """Run every step in *chain*, returning a complete report.

    On failure, raises :class:`~idfkit.exceptions.MigrationError` carrying the
    prefix of successfully-completed steps.
    """
    from ..writers import save_idf

    initial_idf = work_root / "step_0_input.idf"
    save_idf(model, initial_idf)
    input_text = initial_idf.read_text(encoding="latin-1")

    key = migration_cache.cache_key(input_text, chain, migrator) if use_cache else None
    if key is None:
        steps, final_text = _run_steps(input_text, chain, migrator, work_root, on_progress)
        from_cache = False
    else:
        with migration_cache.in_flight(key):
            cached = migration_cache.get(key)
            if cached is None:
                steps, final_text = _run_steps(input_text, chain, migrator, work_root, on_progress)
                migration_cache.put(key, migration_cache.CachedMigration(final_text, steps))
                from_cache = False
            else:
                _emit(on_progress, migration_cache.cached_progress_event(chain))
                steps, final_text = cached.steps, cached.idf_text
                from_cache = True

    _emit(
        on_progress,
        MigrationProgress(
            phase="reparsing",
            message="Re-parsing migrated IDF",
            total_steps=len(chain),
            percent=100.0,
        ),
    )
    final_idf = work_root / "migrated.idf"
    final_idf.write_text(final_text, encoding="latin-1")
    migrated = parse_migrated_idf(
        final_idf, version=target, strict=model.strict, normalize_choices=model.normalize_choices
    )
    verify_migration_output(
        model,
        migrated,
        target_version=target,
        completed_steps=chain,
    )

    _emit(
        on_progress,
        MigrationProgress(phase="diffing", message="Computing structural diff"),
    )
    diff = document_diff(model, migrated)

    _emit(
        on_progress,
        MigrationProgress(phase="complete", message="Migration complete", percent=100.0),
    )

    return MigrationReport(
        migrated_model=migrated,
        source_version=source,
        target_version=target,
        requested_target=target,
        steps=steps,
        diff=diff,
        from_cache=from_cache,
    )


def _run_steps(
    current_text: str,
    chain: tuple[tuple[tuple[int, int, int], tuple[int, int, int]], ...],
    migrator: Migrator,
    work_root: Path,
    on_progress: OnMigrationProgress | None,
) -> tuple[tuple[MigrationStep, ...], str]:
    """Run the transition binaries of *chain* on *current_text*: the step records and the final text."""
    steps: list[MigrationStep] = []
    completed_pairs: list[tuple[tuple[int, int, int], tuple[int, int, int]]] = []

    for idx, (a, b) in enumerate(chain):
        _emit(
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
            step_result = migrator.migrate_step(current_text, a, b, work_dir=step_dir)
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
                exc.reason,
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

    return tuple(steps), current_text


def _resolve_migrator(
    migrator: Migrator | None,
    energyplus: EnergyPlusConfig | None,
) -> Migrator:
    """Pick the migrator to use, falling back to a SubprocessMigrator."""
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
    return SubprocessMigrator(version_updater_dir=updater_dir)


def _infer_binary(
    migrator: Migrator,
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


def _emit(
    on_progress: OnMigrationProgress | None,
    event: MigrationProgress,
) -> None:
    """Invoke *on_progress*, swallowing exceptions to avoid poisoning the migration."""
    if on_progress is None:
        return
    try:
        on_progress(event)
    except Exception:
        logger.warning("on_progress callback raised; ignoring", exc_info=True)


def _vstr(v: tuple[int, int, int]) -> str:
    return f"{v[0]}.{v[1]}.{v[2]}"
