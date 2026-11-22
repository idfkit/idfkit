#!/usr/bin/env python
"""Time ``schedules.values()`` on Schedule:Compact objects in a model with special days.

Builds a model with ten ``RunPeriodControl:SpecialDays`` (the US federal holidays most
commercial prototype models carry) and a set of office-style Schedule:Compact objects that
use Holiday and custom-day rules, then times a year of values for each, hourly and at four
timesteps per hour. Rerun on another commit to compare.

Usage:
    uv run python benchmarks/bench_schedules.py
    uv run python benchmarks/bench_schedules.py -n 50 --repeat 5
"""

from __future__ import annotations

import argparse
import statistics
import time

from idfkit import new_document
from idfkit.objects import IDFObject
from idfkit.schedules import values

SPECIAL_DAYS = [
    ("New Years Day", "January 1", "Holiday"),
    ("Martin Luther King Day", "3rd Monday in January", "Holiday"),
    ("Presidents Day", "3rd Monday in February", "Holiday"),
    ("Memorial Day", "Last Monday in May", "Holiday"),
    ("Independence Day", "July 4", "Holiday"),
    ("Labor Day", "1st Monday in September", "Holiday"),
    ("Columbus Day", "2nd Monday in October", "Holiday"),
    ("Veterans Day", "November 11", "Holiday"),
    ("Thanksgiving Day", "4th Thursday in November", "Holiday"),
    ("Christmas Day", "December 25", "Holiday"),
]


def build(n: int) -> list[IDFObject]:
    """Return *n* Schedule:Compact objects of a model with ten special days."""
    doc = new_document()
    for name, start, kind in SPECIAL_DAYS:
        doc.add(
            "RunPeriodControl:SpecialDays",
            name,
            start_date=start,
            duration=1,
            special_day_type=kind,
            validate=False,
        )
    schedules: list[IDFObject] = []
    for i in range(n):
        occupied = f"{0.5 + i / (2 * n):.4f}"
        fields = [
            "Through: 12/31",
            "For: Weekdays SummerDesignDay",
            "Until: 06:00",
            "0.05",
            "Until: 07:00",
            "0.1",
            "Until: 08:00",
            "0.3",
            "Until: 12:00",
            occupied,
            "Until: 13:00",
            "0.5",
            "Until: 17:00",
            occupied,
            "Until: 18:00",
            "0.3",
            "Until: 24:00",
            "0.05",
            "For: Saturday",
            "Until: 08:00",
            "0.05",
            "Until: 14:00",
            "0.3",
            "Until: 24:00",
            "0.05",
            "For: Sunday Holidays AllOtherDays",
            "Until: 24:00",
            "0.05",
        ]
        schedules.append(
            doc.add("Schedule:Compact", f"Office {i}", validate=False, data=[{"field": f} for f in fields])
        )
    return schedules


def main() -> None:
    """Run the benchmark and print the median time per configuration."""
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("-n", type=int, default=20, help="number of schedules (default 20)")
    parser.add_argument("--repeat", type=int, default=3, help="timed repetitions (default 3)")
    args = parser.parse_args()

    schedules = build(args.n)
    for timestep in (1, 4):
        times: list[float] = []
        for _ in range(args.repeat):
            start = time.perf_counter()
            for schedule in schedules:
                values(schedule, year=2024, timestep=timestep)
            times.append(time.perf_counter() - start)
        median = statistics.median(times)
        print(f"{args.n} schedules, timestep {timestep}: {median:.3f} s ({median / args.n * 1000:.1f} ms per schedule)")


if __name__ == "__main__":
    main()
