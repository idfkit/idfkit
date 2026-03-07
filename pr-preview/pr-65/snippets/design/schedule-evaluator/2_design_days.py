from __future__ import annotations

from datetime import datetime
from enum import Enum
from idfkit import IDFDocument, IDFObject


# --8<-- [start:example]
class DayType(Enum):
    """Special day type for evaluation."""

    NORMAL = "normal"  # Use calendar day
    SUMMER_DESIGN = "summer"  # Use SummerDesignDay schedule
    WINTER_DESIGN = "winter"  # Use WinterDesignDay schedule


def evaluate(
    schedule: IDFObject,
    dt: datetime,
    document: IDFDocument | None = None,
    day_type: DayType = DayType.NORMAL,
) -> float:
    """
    Get schedule value at a specific datetime.

    Args:
        day_type: Override calendar day with design day schedule.
                  Used for sizing calculations.
    """


# --8<-- [end:example]
