"""Structured reporting dataclasses for migration runs."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import TYPE_CHECKING, Generic

if TYPE_CHECKING:
    # ``default=`` is in ``typing.TypeVar`` only from Python 3.13; type checkers always have
    # ``typing_extensions``, and the run-time type variable below needs no default.
    from typing import Any

    from typing_extensions import TypeVar

    from ..document import AnyIDFDocument

    DocumentT_co = TypeVar(
        "DocumentT_co",
        bound=AnyIDFDocument[Any],
        covariant=True,
        default=AnyIDFDocument,
    )
    """The type of a report's ``migrated_model``: the target release's document type when the
    caller named it, else ``AnyIDFDocument``. A bare ``MigrationReport`` means any of them."""
else:
    from typing import TypeVar

    DocumentT_co = TypeVar("DocumentT_co", covariant=True)


def _empty_count_delta() -> dict[str, int]:
    return {}


def _empty_field_changes() -> dict[str, FieldDelta]:
    return {}


@dataclass(frozen=True, slots=True)
class MigrationStep:
    """Record of a single transition step.

    Attributes:
        from_version: Source version for this step.
        to_version: Target version for this step.
        success: Whether the step completed without error.
        binary: Path to the transition binary that was invoked, if any. ``None``
            for pure-Python backends or steps that were skipped.
        stdout: Captured standard output (may be empty).
        stderr: Captured standard error (may be empty).
        audit_text: Contents of the per-step ``.audit`` file if produced,
            else ``None``.
        runtime_seconds: Wall-clock runtime of the step.
    """

    from_version: tuple[int, int, int]
    to_version: tuple[int, int, int]
    success: bool
    binary: Path | None = None
    stdout: str = ""
    stderr: str = ""
    audit_text: str | None = None
    runtime_seconds: float = 0.0


@dataclass(frozen=True, slots=True)
class FieldDelta:
    """Per-object-type summary of field changes introduced by the migration.

    Attributes:
        added: Field names present in *to_version* schema but not in *from_version*.
        removed: Field names present in *from_version* schema but not in *to_version*.
    """

    added: tuple[str, ...] = ()
    removed: tuple[str, ...] = ()


@dataclass(frozen=True, slots=True)
class MigrationDiff:
    """Structural diff between pre- and post-migration documents.

    Attributes:
        added_object_types: Types present after migration but not before.
        removed_object_types: Types present before migration but not after.
        object_count_delta: Per-type signed change in object count.
            Includes only types with a nonzero delta.
        field_changes: Per-type schema-level field changes (only types present
            in both the before and after schemas are included).
    """

    added_object_types: tuple[str, ...] = ()
    removed_object_types: tuple[str, ...] = ()
    object_count_delta: dict[str, int] = field(default_factory=_empty_count_delta)
    field_changes: dict[str, FieldDelta] = field(default_factory=_empty_field_changes)

    @property
    def is_empty(self) -> bool:
        """``True`` when the migration produced no observable structural change."""
        return (
            not self.added_object_types
            and not self.removed_object_types
            and not self.object_count_delta
            and not self.field_changes
        )


@dataclass(frozen=True, slots=True)
class MigrationReport(Generic[DocumentT_co]):
    """Result of a full migration run.

    Generic in the type of ``migrated_model``. [migrate][idfkit.migration.migrate]
    given a document type as its target, such as ``IDFDocumentV24_1`` from
    [idfkit.versioned][], returns a report typed for that release;
    given a version tuple or string, whose release a type checker cannot know,
    it returns one typed with ``AnyIDFDocument``, as a bare ``MigrationReport``
    annotation also is.

    Attributes:
        migrated_model: The new document, at ``target_version`` (``None``
            only on a no-op migration where source equals target — in that
            case the caller's original model is the result).
        source_version: The version the model started at.
        target_version: The version the model was migrated to. On a partial
            failure this is the last successfully reached version, which may
            be earlier than the originally-requested target.
        requested_target: The originally-requested target version.
        steps: Ordered record of every transition step that ran.
        diff: Structural diff computed after migration. Empty when no
            steps ran (source == target).
    """

    migrated_model: DocumentT_co | None
    source_version: tuple[int, int, int]
    target_version: tuple[int, int, int]
    requested_target: tuple[int, int, int]
    steps: tuple[MigrationStep, ...] = ()
    diff: MigrationDiff = field(default_factory=MigrationDiff)

    @property
    def success(self) -> bool:
        """``True`` when every transition step succeeded (or none ran)."""
        return all(s.success for s in self.steps)

    @property
    def completed_steps(self) -> tuple[MigrationStep, ...]:
        """Steps that completed successfully, in order."""
        return tuple(s for s in self.steps if s.success)

    @property
    def failed_step(self) -> MigrationStep | None:
        """The first step that failed, if any."""
        for s in self.steps:
            if not s.success:
                return s
        return None

    def summary(self) -> str:
        """Return a short multi-line summary suitable for logs or CLI output."""
        s_ver = ".".join(str(x) for x in self.source_version)
        t_ver = ".".join(str(x) for x in self.target_version)
        lines = [
            f"Migration: {s_ver} -> {t_ver}"
            + (
                ""
                if self.target_version == self.requested_target
                else f" (requested {'.'.join(str(x) for x in self.requested_target)})"
            ),
            f"Steps: {len(self.completed_steps)}/{len(self.steps)} succeeded",
        ]
        if self.diff.added_object_types:
            lines.append(f"  + object types: {', '.join(self.diff.added_object_types)}")
        if self.diff.removed_object_types:
            lines.append(f"  - object types: {', '.join(self.diff.removed_object_types)}")
        return "\n".join(lines)
