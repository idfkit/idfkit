from __future__ import annotations

from idfkit import IDFDocument, IDFObject
from idfkit.schedules import DayType, Interpolation
from idfkit.simulation import FileSystem


# --8<-- [start:example]
def values(
    schedule: IDFObject,
    year: int = 2024,
    timestep: int = 1,  # per hour
    start_date: tuple[int, int] = (1, 1),  # (month, day)
    end_date: tuple[int, int] = (12, 31),
    document: IDFDocument | None = None,
    day_type: DayType = DayType.NORMAL,
    interpolation: Interpolation = Interpolation.NO,
    fs: FileSystem | None = None,
) -> list[float]:
    """
    Generate schedule values for a date range.

    Returns one value per timestep for the entire period.
    Default: 8760 hourly values for a full year.

    Args:
        timestep: Values per hour (1, 2, 4, 6, 12, or 60)
        interpolation: How to handle sub-hourly alignment
        day_type: Use design day schedule for all days
    """


# --8<-- [end:example]
