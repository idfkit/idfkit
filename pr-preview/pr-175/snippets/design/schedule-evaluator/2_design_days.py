from __future__ import annotations

from datetime import datetime
from enum import Enum
from pathlib import Path
from idfkit import IDFDocument, IDFObject
from idfkit.schedules import DayTypeInput
from idfkit.simulation import FileSystem


# --8<-- [start:example]
class DayType(Enum):
    """Special day type for schedule evaluation."""

    NORMAL = "normal"  # Use the calendar day
    SUMMER_DESIGN = "summer"  # Use the SummerDesignDay schedule
    WINTER_DESIGN = "winter"  # Use the WinterDesignDay schedule
    HOLIDAY = "holiday"  # Treat as a holiday regardless of date
    CUSTOM_DAY_1 = "customday1"  # Use the CustomDay1 schedule
    CUSTOM_DAY_2 = "customday2"  # Use the CustomDay2 schedule


def evaluate(
    schedule: IDFObject,
    dt: datetime,
    document: IDFDocument | None = None,
    day_type: DayTypeInput | None = None,
    fs: FileSystem | None = None,
    base_path: Path | str | None = None,
) -> float:
    """
    Get schedule value at a specific datetime.

    Args:
        day_type: Override the calendar day with a design day, holiday, or
                  custom day schedule. Accepts a DayType or its string value
                  ("summer", "holiday", ...). Used for sizing calculations.
        fs: FileSystem used to read Schedule:File CSVs.
        base_path: Base directory for resolving relative Schedule:File paths.
    """


# --8<-- [end:example]
