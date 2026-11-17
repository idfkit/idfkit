"""Re-parse a migration's final IDF into the document the report hands back."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pathlib import Path

    from ..document import IDFDocument


def parse_migrated_idf(path: Path, *, version: tuple[int, int, int], strict: bool) -> IDFDocument:
    """Parse the migrated IDF at *path*, detached from the file it was read from.

    *path* lives in the migration's work directory, which is normally a temporary directory
    removed as soon as the run ends. ``parse_idf`` records *path* as the document's ``filepath``,
    so a bare ``doc.save()`` would write into a directory that no longer exists, or overwrite
    the scratch file when the caller passed ``work_dir``. The source model's path is no better:
    the migrated document is at another EnergyPlus version, and saving over the original would
    destroy it. So the result has no ``filepath`` and must be saved to a path the caller names.
    """
    from ..idf_parser import parse_idf

    doc = parse_idf(path, version=version, strict=strict)
    doc.filepath = None
    return doc
