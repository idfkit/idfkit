from __future__ import annotations

from dataclasses import dataclass
from datetime import time
from idfkit import IDFObject


# --8<-- [start:example]
@dataclass
class CompactPeriod:
    """A 'Through:' block covering a date range."""

    end_month: int
    end_day: int
    day_rules: list[CompactDayRule]


@dataclass
class CompactDayRule:
    """A 'For:' block with day types and time-value pairs."""

    day_types: set[str]  # {"Weekdays", "Weekends", "Holidays", ...}
    time_values: list[tuple[time, float]]  # [(08:00, 0.0), (18:00, 1.0), ...]


def parse_compact(obj: IDFObject) -> list[CompactPeriod]:
    """Parse Schedule:Compact fields into structured data."""


# --8<-- [end:example]
