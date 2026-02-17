"""Schedule construction helpers.

Provides high-level functions for creating EnergyPlus schedule objects
from simple Python inputs (constant values, hourly arrays).  These are
the inverse of the schedule *evaluation* functions in the sibling modules.

The main entry point for 8760-value arrays is
:func:`create_compact_schedule_from_values`, which produces a single
``Schedule:Compact`` object using the EnergyPlus Compact DSL.
"""

from __future__ import annotations

import calendar
from collections.abc import Sequence
from datetime import date
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from ..document import IDFDocument
    from ..objects import IDFObject


def create_schedule_type_limits(
    doc: IDFDocument,
    name: str,
    lower: float = 0.0,
    upper: float = 1.0,
    numeric_type: str = "Continuous",
    unit_type: str = "",
) -> IDFObject:
    """Create a ``ScheduleTypeLimits`` object.

    Args:
        doc: The document to add the object to.
        name: Name for the type limits (e.g. ``"Fraction"``).
        lower: Lower limit value.
        upper: Upper limit value.
        numeric_type: ``"Continuous"`` or ``"Discrete"``.
        unit_type: Unit type string (e.g. ``"Dimensionless"``).

    Returns:
        The created ``ScheduleTypeLimits`` object.
    """
    kwargs: dict[str, Any] = {
        "lower_limit_value": lower,
        "upper_limit_value": upper,
        "numeric_type": numeric_type,
    }
    if unit_type:
        kwargs["unit_type"] = unit_type
    return doc.add("ScheduleTypeLimits", name, **kwargs)


def create_constant_schedule(
    doc: IDFDocument,
    name: str,
    value: float,
    type_limits: str = "",
) -> IDFObject:
    """Create a ``Schedule:Constant``.

    Args:
        doc: The document to add the object to.
        name: Schedule name.
        value: The constant hourly value.
        type_limits: Name of an existing ``ScheduleTypeLimits`` object.
            Pass empty string to omit.

    Returns:
        The created ``Schedule:Constant`` object.
    """
    kwargs: dict[str, Any] = {"hourly_value": value}
    if type_limits:
        kwargs["schedule_type_limits_name"] = type_limits
    return doc.add("Schedule:Constant", name, **kwargs)


def create_compact_schedule_from_values(
    doc: IDFDocument,
    name: str,
    values: Sequence[float],
    year: int = 2024,
    type_limits: str = "",
    *,
    tolerance: float = 1e-6,
) -> IDFObject:
    """Create a ``Schedule:Compact`` from hourly values.

    Takes 8760 (or 8784 for a leap year) hourly values and produces a
    single ``Schedule:Compact`` object that encodes the same data using
    the EnergyPlus Compact DSL (``Through`` / ``For`` / ``Until`` /
    value syntax).

    Consecutive days that share the same 24-hour profile are merged into
    a single ``Through:`` block, and consecutive hours with the same
    value are merged into a single ``Until:`` entry.

    Args:
        doc: Document to add the schedule to.
        name: Schedule name.
        values: Hourly schedule values.  Must be exactly 8760 (non-leap)
            or 8784 (leap year) elements.
        year: Calendar year for day counting (default 2024).
        type_limits: Name of a ``ScheduleTypeLimits`` to assign.
            Pass empty string to omit.
        tolerance: Float comparison tolerance for profile grouping
            (default 1e-6).

    Returns:
        The created ``Schedule:Compact`` object.

    Raises:
        ValueError: If ``len(values)`` does not match the year.
    """
    is_leap = calendar.isleap(year)
    expected = 8784 if is_leap else 8760
    if len(values) != expected:
        msg = f"Expected {expected} hourly values for year {year}, got {len(values)}"
        raise ValueError(msg)

    num_days = 366 if is_leap else 365

    # 1. Split into daily profiles
    daily_profiles: list[tuple[float, ...]] = []
    for d in range(num_days):
        start = d * 24
        daily_profiles.append(tuple(values[start : start + 24]))

    # 2. Group consecutive days with identical profiles into date ranges.
    #    Each range is (start_day_index, end_day_index, profile).
    ranges: list[tuple[int, int, tuple[float, ...]]] = []
    run_start = 0
    for d in range(1, num_days):
        if not _profiles_equal(daily_profiles[d], daily_profiles[run_start], tolerance):
            ranges.append((run_start, d - 1, daily_profiles[run_start]))
            run_start = d
    ranges.append((run_start, num_days - 1, daily_profiles[run_start]))

    # 3. Build Compact DSL fields.
    jan1 = date(year, 1, 1)
    fields: list[str] = []

    for _, end_day, profile in ranges:
        end_date = date.fromordinal(jan1.toordinal() + end_day)
        fields.append(f"Through: {end_date.month}/{end_date.day}")
        fields.append("For: AllDays")
        fields.extend(_profile_to_until_fields(profile))

    # 4. Create the Schedule:Compact object.
    kwargs: dict[str, Any] = {}
    if type_limits:
        kwargs["schedule_type_limits_name"] = type_limits
    for i, field_val in enumerate(fields, 1):
        kwargs[f"field_{i}"] = field_val

    return doc.add("Schedule:Compact", name, validate=False, **kwargs)


# ---------------------------------------------------------------------------
# Private helpers
# ---------------------------------------------------------------------------


def _profiles_equal(a: tuple[float, ...], b: tuple[float, ...], tol: float) -> bool:
    """Compare two 24-value daily profiles within tolerance."""
    return len(a) == len(b) and all(abs(x - y) <= tol for x, y in zip(a, b, strict=True))


def _profile_to_until_fields(profile: Sequence[float]) -> list[str]:
    """Convert a 24-value hourly profile to Until/Value field pairs.

    Merges consecutive hours with the same value to produce compact output.
    For a constant-value day, this returns just ``["Until: 24:00", "value"]``.

    Note: Uses exact float equality for intra-day hour merging (not the
    tolerance used for inter-day profile grouping).  This is correct because
    the values within a single day come from the same input array and are
    compared to themselves, not to values from a different day.
    """
    fields: list[str] = []
    prev_value = profile[0]
    run_end_hour = 1

    for h in range(1, 24):
        if profile[h] != prev_value:
            fields.append(f"Until: {run_end_hour:02d}:00")
            fields.append(_format_value(prev_value))
            prev_value = profile[h]
            run_end_hour = h + 1
        else:
            run_end_hour = h + 1

    # Final hour block
    fields.append(f"Until: {run_end_hour:02d}:00")
    fields.append(_format_value(prev_value))

    return fields


def _format_value(v: float) -> str:
    """Format a numeric value for Compact DSL, dropping trailing zeros."""
    # Using :.15g handles integers (1.0 → "1"), floats, inf, and nan
    # without the OverflowError risk of int(v) on non-finite values.
    return f"{v:.15g}"
