"""Type definitions for schedule evaluation.

This module defines enums and dataclasses used throughout the schedules package.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date, time
from enum import Enum
from typing import Literal


class DayType(Enum):
    """Special day type for schedule evaluation.

    Used to override the calendar day with a design day schedule,
    which is useful for sizing calculations.
    """

    NORMAL = "normal"
    """Use calendar day (weekday, weekend, or holiday based on date)."""

    SUMMER_DESIGN = "summer"
    """Use SummerDesignDay schedule regardless of actual date."""

    WINTER_DESIGN = "winter"
    """Use WinterDesignDay schedule regardless of actual date."""

    HOLIDAY = "holiday"
    """Treat as holiday regardless of actual date."""

    CUSTOM_DAY_1 = "customday1"
    """Use CustomDay1 schedule."""

    CUSTOM_DAY_2 = "customday2"
    """Use CustomDay2 schedule."""


class Interpolation(Enum):
    """Interpolation mode for schedule values.

    Controls how values are computed when the evaluation timestep
    doesn't align with the schedule's native intervals.
    """

    NO = "no"
    """Step function - value at each interval applies until next interval."""

    AVERAGE = "average"
    """Linear interpolation when timestep doesn't align with intervals."""

    LINEAR = "linear"
    """Alias for AVERAGE."""


# Literal types for string parameters - provides IDE autocompletion
DayTypeLiteral = Literal["normal", "summer", "winter", "holiday", "customday1", "customday2"]
InterpolationLiteral = Literal["no", "step", "average", "linear"]

# Union types for flexible parameter acceptance
DayTypeInput = DayType | DayTypeLiteral
InterpolationInput = Interpolation | InterpolationLiteral

# Internal mapping from literal strings to enums
_DAY_TYPE_MAP: dict[DayTypeLiteral, DayType] = {
    "normal": DayType.NORMAL,
    "summer": DayType.SUMMER_DESIGN,
    "winter": DayType.WINTER_DESIGN,
    "holiday": DayType.HOLIDAY,
    "customday1": DayType.CUSTOM_DAY_1,
    "customday2": DayType.CUSTOM_DAY_2,
}

_INTERPOLATION_MAP: dict[InterpolationLiteral, Interpolation] = {
    "no": Interpolation.NO,
    "step": Interpolation.NO,
    "average": Interpolation.AVERAGE,
    "linear": Interpolation.LINEAR,
}


def parse_day_type(value: DayTypeInput | None) -> DayType:
    """Convert string literal or enum to DayType."""
    if value is None:
        return DayType.NORMAL
    if isinstance(value, DayType):
        return value
    return _DAY_TYPE_MAP[value]


def parse_interpolation(value: InterpolationInput | None) -> Interpolation:
    """Convert string literal or enum to Interpolation."""
    if value is None:
        return Interpolation.NO
    if isinstance(value, Interpolation):
        return value
    return _INTERPOLATION_MAP[value]


@dataclass(frozen=True)
class SpecialDay:
    """A special day period from RunPeriodControl:SpecialDays.

    Represents a holiday or custom day type that spans one or more days.
    """

    name: str
    """Name of the special day (e.g., "Christmas")."""

    start_date: date
    """Start date of the special day period."""

    duration: int
    """Number of days this special day spans."""

    day_type: str
    """Day type: "Holiday", "CustomDay1", or "CustomDay2"."""

    def contains(self, d: date) -> bool:
        """Check if a date falls within this special day period."""
        from datetime import timedelta

        end_date = self.start_date + timedelta(days=self.duration - 1)
        return self.start_date <= d <= end_date


@dataclass(frozen=True)
class TimeValue:
    """A time-value pair for interval schedules.

    The value applies from the previous time until this time.
    """

    until_time: time
    """Time until which the value applies."""

    value: float
    """The schedule value."""


@dataclass
class CompactDayRule:
    """A 'For:' block in Schedule:Compact with day types and time-value pairs."""

    day_types: set[str]
    """Day types this rule applies to (e.g., {"Weekdays", "Weekends"})."""

    time_values: list[TimeValue]
    """Time-value pairs defining the schedule for these days."""


@dataclass
class CompactPeriod:
    """A 'Through:' block in Schedule:Compact covering a date range."""

    end_month: int
    """End month of the period (1-12)."""

    end_day: int
    """End day of the period (1-31)."""

    day_rules: list[CompactDayRule]
    """Day rules within this period."""

    def contains(self, d: date) -> bool:
        """Check if a date falls within this period.

        Periods implicitly start from January 1 or the end of the previous period.
        This method only checks the end boundary.
        """
        return (d.month, d.day) <= (self.end_month, self.end_day)


# Day type string constants matching EnergyPlus naming
DAY_TYPE_SUNDAY = "Sunday"
DAY_TYPE_MONDAY = "Monday"
DAY_TYPE_TUESDAY = "Tuesday"
DAY_TYPE_WEDNESDAY = "Wednesday"
DAY_TYPE_THURSDAY = "Thursday"
DAY_TYPE_FRIDAY = "Friday"
DAY_TYPE_SATURDAY = "Saturday"
DAY_TYPE_WEEKDAYS = "Weekdays"
DAY_TYPE_WEEKENDS = "Weekends"
DAY_TYPE_ALLDAYS = "AllDays"
DAY_TYPE_HOLIDAY = "Holiday"
DAY_TYPE_SUMMER_DESIGN = "SummerDesignDay"
DAY_TYPE_WINTER_DESIGN = "WinterDesignDay"
DAY_TYPE_CUSTOM_DAY_1 = "CustomDay1"
DAY_TYPE_CUSTOM_DAY_2 = "CustomDay2"
DAY_TYPE_ALL_OTHER_DAYS = "AllOtherDays"

# Mapping from Python weekday() to EnergyPlus day type
# Python: Monday=0, Sunday=6
# EnergyPlus order: Sunday, Monday, ..., Saturday
WEEKDAY_TO_DAY_TYPE: dict[int, str] = {
    0: DAY_TYPE_MONDAY,
    1: DAY_TYPE_TUESDAY,
    2: DAY_TYPE_WEDNESDAY,
    3: DAY_TYPE_THURSDAY,
    4: DAY_TYPE_FRIDAY,
    5: DAY_TYPE_SATURDAY,
    6: DAY_TYPE_SUNDAY,
}

# Day types that match weekdays (Mon-Fri)
WEEKDAY_TYPES = {DAY_TYPE_MONDAY, DAY_TYPE_TUESDAY, DAY_TYPE_WEDNESDAY, DAY_TYPE_THURSDAY, DAY_TYPE_FRIDAY}

# Day types that match weekends (Sat-Sun)
WEEKEND_TYPES = {DAY_TYPE_SATURDAY, DAY_TYPE_SUNDAY}
