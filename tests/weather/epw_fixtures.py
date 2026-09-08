"""Constructed EPW text for the reader's own suite.

The corpus carries the real files and is where the numbers are checked against something neither
library wrote. What belongs here instead is the shape: files small enough to read, and files
deliberately malformed, neither of which any upstream archive publishes.

The leap-year builder is the clearest case for constructing rather than committing. Every archive
published upstream is 8,760 hourly rows from 1 January to 31 December, so there is no leap-year
file to commit and no oracle behind one if there were.

This module is the counterpart of ``idfkit-js/packages/weather/tests/epw-fixtures.ts`` and produces
byte-identical text for the same options, so a difference between the two suites is a difference in
the readers rather than in their inputs.
"""

from __future__ import annotations

from collections.abc import Callable, Sequence
from typing import Final

#: How many days each month holds, January first, on a common year.
DAYS_IN_MONTH: Final = (31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31)

#: The eight header records, with ``%LEAP%`` and ``%CITY%`` still to fill in.
_HEADER: Final = (
    "LOCATION,%CITY%,IL,USA,TMYx,725300,41.98,-87.92,-6.0,201.0",
    "DESIGN CONDITIONS,0",
    "TYPICAL/EXTREME PERIODS,1,Summer - Week Nearest Max Temperature For Period,Extreme,7/13,7/19",
    "GROUND TEMPERATURES,1,.5,,,,-1.89,-3.06,-0.99,2.23,10.68,17.20,21.60,22.94,20.66,15.60,8.83,2.56",
    "HOLIDAYS/DAYLIGHT SAVINGS,%LEAP%,0,0,0",
    "COMMENTS 1,Constructed for the reader test suite. Not an upstream file.",
    "COMMENTS 2, -- no provenance to record",
)


def template_row(year: int, month: int, day: int, hour: int) -> list[str]:
    """One plausible hourly row, as thirty-five fields.

    The values are ordinary readings rather than round numbers, so a column read from the wrong
    position looks wrong instead of looking empty.
    """
    return [
        str(year),
        str(month),
        str(day),
        str(hour),
        "0",
        "?9?9?9?9E0?9?9?9?9?9?9?9?9?9?9?9?9?9?9?9?9?9?9",
        "2.80",
        "-3.30",
        "62",
        "92453",
        "0",
        "0",
        "256",
        "0",
        "0",
        "0",
        "0",
        "0",
        "0",
        "0",
        "160",
        "2.60",
        "0",
        "0",
        "777.7",
        "77777",
        "9",
        "999999999",
        "7",
        "0.0850",
        "0",
        "88",
        "0.195",
        "0.0",
        "0.0",
    ]


def build_epw(
    *,
    city: str = "Chicago Ohare Intl Ap",
    leap_year: bool = False,
    records_per_hour: int = 1,
    line_ending: str = "\n",
    row: Callable[[int, int, int, Sequence[str]], Sequence[str]] | None = None,
) -> str:
    """Build a whole year of EPW text, 1 January to 31 December.

    Args:
        city: The station name written into the LOCATION record.
        leap_year: Whether the file's calendar carries a 29 February.
        records_per_hour: As the DATA PERIODS record declares it.
        line_ending: ``\\n`` by default; pass ``\\r\\n`` for the other convention.
        row: Rewrite one row's fields. Called for every record with its zero-based index, the
            row's month and day, and the 35 fields as strings.

    Returns:
        The file's text, header records and all.
    """
    year = 2016 if leap_year else 2015
    lines = [line.replace("%LEAP%", "Yes" if leap_year else "No").replace("%CITY%", city) for line in _HEADER]
    lines.append(f"DATA PERIODS,1,{records_per_hour},Data,Sunday, 1/ 1,12/31")

    index = 0
    for month in range(1, 13):
        days = DAYS_IN_MONTH[month - 1] + (1 if leap_year and month == 2 else 0)
        for day in range(1, days + 1):
            for hour in range(1, 25):
                for _ in range(records_per_hour):
                    fields = template_row(year, month, day, hour)
                    lines.append(",".join(row(index, month, day, fields) if row else fields))
                    index += 1

    return line_ending.join(lines) + line_ending


def year_row_count(leap_year: bool, records_per_hour: int = 1) -> int:
    """How many records :func:`build_epw` writes for a whole year."""
    return (366 if leap_year else 365) * 24 * records_per_hour
