from __future__ import annotations

from datetime import datetime
from idfkit import IDFObject
from idfkit.schedules import Interpolation, ScheduleFileCache
from idfkit.simulation import FileSystem
from pathlib import Path


# --8<-- [start:example]
def evaluate_schedule_file(
    obj: IDFObject,
    dt: datetime,
    fs: FileSystem | None = None,
    base_path: Path | str | None = None,
    cache: ScheduleFileCache | None = None,
    interpolation: Interpolation = Interpolation.NO,
) -> float:
    """
    Evaluate a Schedule:File at a specific datetime.

    Args:
        obj: The Schedule:File IDF object
        dt: Datetime to evaluate
        fs: FileSystem for reading the CSV (default: LocalFileSystem)
        base_path: Base directory for resolving relative file paths
                   (default: directory containing the IDF)
        cache: Reuses parsed CSV columns across calls, so evaluating a full
               year doesn't re-read the file 8,760 times
        interpolation: Whether to interpolate between sub-hourly items
    """


# --8<-- [end:example]
