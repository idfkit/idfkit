from __future__ import annotations

from datetime import datetime
from idfkit import IDFObject
from idfkit.simulation import FileSystem
from pathlib import Path


# --8<-- [start:example]
def evaluate_schedule_file(
    obj: IDFObject,
    dt: datetime,
    fs: FileSystem | None = None,
    base_path: Path | str | None = None,
) -> float:
    """
    Evaluate a Schedule:File at a specific datetime.

    Args:
        obj: The Schedule:File IDF object
        dt: Datetime to evaluate
        fs: FileSystem for reading the CSV (default: LocalFileSystem)
        base_path: Base directory for resolving relative file paths
                   (default: directory containing the IDF)
    """


# --8<-- [end:example]
