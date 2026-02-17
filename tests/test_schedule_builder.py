"""Tests for the schedule builder module."""

from __future__ import annotations

import calendar

import pytest

from idfkit import new_document
from idfkit.schedules import values
from idfkit.schedules.builder import (
    create_compact_schedule_from_values,
    create_constant_schedule,
    create_schedule_type_limits,
)

_TOL = 1e-6


class TestCreateScheduleTypeLimits:
    def test_creates_object(self) -> None:
        doc = new_document()
        obj = create_schedule_type_limits(doc, "Fraction")
        assert obj.obj_type == "ScheduleTypeLimits"
        assert obj.name == "Fraction"

    def test_fields_set_correctly(self) -> None:
        doc = new_document()
        obj = create_schedule_type_limits(
            doc, "Temperature", lower=-50, upper=100, numeric_type="Continuous", unit_type="Temperature"
        )
        assert obj.lower_limit_value == -50
        assert obj.upper_limit_value == 100
        assert obj.numeric_type == "Continuous"
        assert obj.unit_type == "Temperature"

    def test_unit_type_omitted_when_empty(self) -> None:
        doc = new_document()
        obj = create_schedule_type_limits(doc, "Fraction")
        assert obj.get("Unit Type") is None


class TestCreateConstantSchedule:
    def test_creates_constant(self) -> None:
        doc = new_document()
        obj = create_constant_schedule(doc, "AlwaysOn", 1.0)
        assert obj.obj_type == "Schedule:Constant"
        assert obj.name == "AlwaysOn"
        assert obj.hourly_value == 1.0

    def test_with_type_limits(self) -> None:
        doc = new_document()
        create_schedule_type_limits(doc, "Fraction")
        obj = create_constant_schedule(doc, "AlwaysOn", 1.0, type_limits="Fraction")
        assert obj.schedule_type_limits_name == "Fraction"

    def test_evaluates_correctly(self) -> None:
        doc = new_document()
        obj = create_constant_schedule(doc, "Half", 0.5)
        hourly = values(obj, year=2024)
        assert len(hourly) == 8784  # 2024 is a leap year
        assert all(abs(v - 0.5) < _TOL for v in hourly)


class TestCreateCompactScheduleFromValues:
    def test_constant_8760(self) -> None:
        """All same value produces a compact schedule with minimal fields."""
        doc = new_document()
        vals = [0.75] * 8760
        obj = create_compact_schedule_from_values(doc, "Const", vals, year=2023)
        assert obj.obj_type == "Schedule:Compact"
        # Should have Through: 12/31, For: AllDays, Until: 24:00, 0.75
        assert obj.field_1 == "Through: 12/31"
        assert obj.field_2 == "For: AllDays"
        assert obj.field_3 == "Until: 24:00"
        assert obj.field_4 == "0.75"

    def test_binary_on_off(self) -> None:
        """Daytime on / nighttime off pattern compresses Until blocks."""
        doc = new_document()
        # Every day: off 0-8, on 8-18, off 18-24
        day_profile = [0.0] * 8 + [1.0] * 10 + [0.0] * 6
        vals = day_profile * 365
        obj = create_compact_schedule_from_values(doc, "Office", vals, year=2023)
        assert obj.obj_type == "Schedule:Compact"
        # Should produce: Through: 12/31, For: AllDays,
        # Until: 08:00, 0, Until: 18:00, 1, Until: 24:00, 0
        assert obj.field_1 == "Through: 12/31"
        assert obj.field_2 == "For: AllDays"
        assert obj.field_3 == "Until: 08:00"
        assert obj.field_4 == "0"
        assert obj.field_5 == "Until: 18:00"
        assert obj.field_6 == "1"
        assert obj.field_7 == "Until: 24:00"
        assert obj.field_8 == "0"

    def test_two_different_day_profiles(self) -> None:
        """Two distinct day profiles produce two Through blocks."""
        doc = new_document()
        # First 31 days (January): constant 1.0
        profile_a = [1.0] * 24
        # Remaining 334 days: constant 0.5
        profile_b = [0.5] * 24
        vals = profile_a * 31 + profile_b * 334
        assert len(vals) == 8760
        obj = create_compact_schedule_from_values(doc, "TwoPhase", vals, year=2023)
        # First Through block ends 1/31, second ends 12/31
        assert obj.field_1 == "Through: 1/31"
        assert obj.field_5 == "Through: 12/31"

    def test_unique_daily_profiles(self) -> None:
        """Each day having a unique profile produces 365 Through blocks."""
        doc = new_document()
        # Each day gets a slightly different constant value
        vals: list[float] = []
        for d in range(365):
            vals.extend([float(d)] * 24)
        assert len(vals) == 8760
        obj = create_compact_schedule_from_values(doc, "Unique", vals, year=2023)
        # Should have 365 Through blocks, each with 4 fields → 1460 fields total
        assert obj.get("Field 1460") is not None
        assert obj.get("Field 1461") is None

    def test_leap_year_8784(self) -> None:
        doc = new_document()
        vals = [1.0] * 8784
        obj = create_compact_schedule_from_values(doc, "Leap", vals, year=2024)
        assert obj.obj_type == "Schedule:Compact"
        assert obj.field_1 == "Through: 12/31"

    def test_non_leap_8760(self) -> None:
        doc = new_document()
        vals = [1.0] * 8760
        obj = create_compact_schedule_from_values(doc, "NonLeap", vals, year=2023)
        assert obj.obj_type == "Schedule:Compact"

    def test_wrong_length_raises(self) -> None:
        doc = new_document()
        with pytest.raises(ValueError, match="Expected 8760"):
            create_compact_schedule_from_values(doc, "Bad", [1.0] * 100, year=2023)

    def test_wrong_length_leap_raises(self) -> None:
        doc = new_document()
        with pytest.raises(ValueError, match="Expected 8784"):
            create_compact_schedule_from_values(doc, "Bad", [1.0] * 8760, year=2024)

    def test_roundtrip_constant(self) -> None:
        """Create from constant values, evaluate back, values must match."""
        doc = new_document()
        year = 2023
        input_vals = [0.42] * 8760
        obj = create_compact_schedule_from_values(doc, "RT", input_vals, year=year)
        output_vals = values(obj, year=year)
        assert len(output_vals) == 8760
        for i, (inp, out) in enumerate(zip(input_vals, output_vals)):
            assert abs(inp - out) < _TOL, f"Mismatch at hour {i}: {inp} vs {out}"

    def test_roundtrip_binary_pattern(self) -> None:
        """Create from binary on/off pattern, evaluate back, values must match."""
        doc = new_document()
        year = 2023
        day_profile = [0.0] * 8 + [1.0] * 10 + [0.0] * 6
        input_vals = day_profile * 365
        obj = create_compact_schedule_from_values(doc, "RT_Binary", input_vals, year=year)
        output_vals = values(obj, year=year)
        assert len(output_vals) == 8760
        for i, (inp, out) in enumerate(zip(input_vals, output_vals)):
            assert abs(inp - out) < _TOL, f"Mismatch at hour {i}: {inp} vs {out}"

    def test_roundtrip_monthly_varying(self) -> None:
        """Create from monthly-varying daily profiles, evaluate back, values must match.

        Uses 12 unique daily profiles (one per month) so the generated
        Schedule:Compact has ~100 fields, well within the parser's limit.
        """
        doc = new_document()
        year = 2023
        # Build 12 unique monthly profiles: each month has a different on/off pattern
        monthly_profiles: list[list[float]] = []
        for m in range(12):
            base = (m + 1) / 12.0
            profile = [0.0] * 24
            # On-hours shift by month: month 0 → hours 6-18, month 11 → hours 1-13
            start_h = 6 - (m % 6)
            end_h = start_h + 12
            for h in range(start_h, min(end_h, 24)):
                profile[h] = base
            monthly_profiles.append(profile)

        # Assign profiles by month
        input_vals: list[float] = []
        for m in range(1, 13):
            days_in_month = calendar.monthrange(year, m)[1]
            for _ in range(days_in_month):
                input_vals.extend(monthly_profiles[m - 1])
        assert len(input_vals) == 8760

        obj = create_compact_schedule_from_values(doc, "RT_Monthly", input_vals, year=year)
        output_vals = values(obj, year=year)
        assert len(output_vals) == 8760
        for i, (inp, out) in enumerate(zip(input_vals, output_vals)):
            assert abs(inp - out) < _TOL, f"Mismatch at hour {i}: {inp} vs {out}"

    def test_roundtrip_leap_year(self) -> None:
        """Roundtrip test for leap year (8784 values)."""
        doc = new_document()
        year = 2024
        assert calendar.isleap(year)
        num_days = 366
        day_profile = [0.0] * 6 + [0.5] * 6 + [1.0] * 6 + [0.5] * 6
        input_vals = day_profile * num_days
        assert len(input_vals) == 8784
        obj = create_compact_schedule_from_values(doc, "RT_Leap", input_vals, year=year)
        output_vals = values(obj, year=year)
        assert len(output_vals) == 8784
        for i, (inp, out) in enumerate(zip(input_vals, output_vals)):
            assert abs(inp - out) < _TOL, f"Mismatch at hour {i}: {inp} vs {out}"

    def test_with_type_limits(self) -> None:
        doc = new_document()
        create_schedule_type_limits(doc, "Fraction")
        obj = create_compact_schedule_from_values(
            doc, "Sched", [0.5] * 8760, year=2023, type_limits="Fraction"
        )
        assert obj.schedule_type_limits_name == "Fraction"

    def test_compact_field_count_constant(self) -> None:
        """A constant schedule should have minimal fields (4)."""
        doc = new_document()
        obj = create_compact_schedule_from_values(doc, "Min", [1.0] * 8760, year=2023)
        # Through: 12/31, For: AllDays, Until: 24:00, 1
        assert obj.get("Field 4") is not None
        assert obj.get("Field 5") is None
