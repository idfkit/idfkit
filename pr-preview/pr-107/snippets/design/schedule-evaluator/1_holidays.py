from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from idfkit import IDFDocument


# --8<-- [start:example]
@dataclass
class SpecialDay:
    """A special day period from RunPeriodControl:SpecialDays."""

    name: str
    start_date: date  # Parsed from "January 1" or "1/1" etc.
    duration: int  # Days
    day_type: str  # "Holiday", "CustomDay1", "CustomDay2", etc.


def extract_special_days(doc: IDFDocument) -> list[SpecialDay]:
    """Parse all RunPeriodControl:SpecialDays objects."""
    ...


def get_holidays(doc: IDFDocument, year: int) -> set[date]:
    """Get all dates marked as Holiday for a given year."""
    ...


# --8<-- [end:example]
