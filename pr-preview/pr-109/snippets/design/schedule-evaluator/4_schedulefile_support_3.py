from __future__ import annotations

from idfkit import IDFObject
from idfkit.simulation import FileSystem
from pathlib import Path


# --8<-- [start:example]
class ScheduleFileCache:
    """Cache for Schedule:File CSV data."""

    _cache: dict[str, list[float]]  # file_path -> values

    def get_values(
        self,
        obj: IDFObject,
        fs: FileSystem,
        base_path: Path,
    ) -> list[float]:
        """Get cached values or read from file."""


# --8<-- [end:example]
