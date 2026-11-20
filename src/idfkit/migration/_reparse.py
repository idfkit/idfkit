"""Re-parse a migration's final IDF into the document the report hands back."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pathlib import Path

    from ..document import IDFDocument
    from ._typing import DocumentT


def parse_migrated_idf(
    path: Path, *, version: tuple[int, int, int], strict: bool, normalize_choices: bool = True
) -> IDFDocument:
    """Parse the migrated IDF at *path*, detached from the file it was read from.

    *path* lives in the migration's work directory, which is normally a temporary directory
    removed as soon as the run ends. ``parse_idf`` records *path* as the document's ``filepath``,
    so a bare ``doc.save()`` would write into a directory that no longer exists, or overwrite
    the scratch file when the caller passed ``work_dir``. The source model's path is no better:
    the migrated document is at another EnergyPlus version, and saving over the original would
    destroy it. So the result has no ``filepath`` and must be saved to a path the caller names.
    """
    from ..idf_parser import parse_idf

    doc = parse_idf(path, version=version, strict=strict, normalize_choices=normalize_choices)
    doc.filepath = None
    return doc


def unmigrated_copy(model: DocumentT, target: tuple[int, int, int]) -> DocumentT:
    """The report's document for a no-op migration (source equals target): a copy of *model*.

    A copy, not *model* itself, so that ``migrated_model`` is always a document the caller can
    edit without touching the input, and has no ``filepath``, as a migrated document has none.
    Its version is *target*, as a migrated document's is: a file headed ``Version, 9.0;``
    loads as ``(9, 0, 0)``, but its release, and the report's ``target_version``, is 9.0.1.
    """
    doc = model.copy()
    doc.filepath = None
    # The stub declares no setter for ``version``: only this no-op stands in for a re-parse at *target*.
    object.__setattr__(doc, "_version", target)
    return doc
