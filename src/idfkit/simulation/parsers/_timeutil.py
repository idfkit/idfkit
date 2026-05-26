"""Shared time helpers for EnergyPlus output parsers.

EnergyPlus encodes timestamps without a calendar year and uses ``Hour=24`` to
mean midnight of the following day. These helpers centralize that handling so
the SQL, ESO, and other time-series parsers agree on a single representation.
"""

from __future__ import annotations

from datetime import datetime, timedelta

# EnergyPlus uses a fixed reference year for timestamps. 2017 is the canonical
# non-leap year used by convention.
REFERENCE_YEAR = 2017

# Mapping from EnergyPlus ReportingFrequency string to a readable label.
# Keys cover both the SQLite spelling ("Run Period") and the ESO ``!Frequency``
# token spelling ("RunPeriod", "TimeStep", "Each Call").
FREQUENCY_MAP: dict[str, str] = {
    "Each Call": "Timestep",
    "EachCall": "Timestep",
    "Detailed": "Timestep",
    "TimeStep": "Timestep",
    "Timestep": "Timestep",
    "Hourly": "Hourly",
    "Daily": "Daily",
    "Monthly": "Monthly",
    "Run Period": "RunPeriod",
    "RunPeriod": "RunPeriod",
    "Annual": "Annual",
}


def make_timestamp(year: int, month: int, day: int, hour: int, minute: int) -> datetime:
    """Build a datetime from EnergyPlus time components.

    EnergyPlus stores Hour=24 to mean midnight of the next day. This function
    handles that edge case, rolling over to the next day at hour 0.

    Args:
        year: Year value from the database (or ``REFERENCE_YEAR`` fallback).
        month: Month (1-12).
        day: Day of month.
        hour: Hour (0-24, where 24 means next day hour 0).
        minute: Minute (0-59).

    Returns:
        A datetime for the given time components.
    """
    if hour == 24:
        return datetime(year, month, day, 0, minute) + timedelta(days=1)
    return datetime(year, month, day, hour, minute)
