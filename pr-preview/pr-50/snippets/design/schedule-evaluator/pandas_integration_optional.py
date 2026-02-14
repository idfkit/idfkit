from __future__ import annotations

from idfkit import IDFDocument, IDFObject
from idfkit.schedules import DayType, Interpolation
from idfkit.simulation import FileSystem
from typing import Any

pd: Any = ...  # type: ignore[assignment]


# --8<-- [start:example]
def to_series(
    schedule: IDFObject,
    year: int = 2024,
    freq: str = "h",  # hourly
    start_date: tuple[int, int] = (1, 1),
    end_date: tuple[int, int] = (12, 31),
    document: IDFDocument | None = None,
    day_type: DayType = DayType.NORMAL,
    interpolation: Interpolation = Interpolation.NO,
    fs: FileSystem | None = None,
) -> pd.Series:
    """
    Convert schedule to pandas Series with DatetimeIndex.

    Requires: pandas (optional dependency)
    """


# --8<-- [end:example]
