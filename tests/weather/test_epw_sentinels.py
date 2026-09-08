"""A measurement that was not taken does not become a number.

The counterpart of ``idfkit-js/packages/weather/tests/epw-sentinels.test.ts``, assertion for
assertion.

THE TWO SOURCES OF EVIDENCE, AND WHY BOTH.

The corpus holds the real sentinel-bearing file, a TMY3 from the other common producer, and the
counts below are that file's. It is not committed here: it belongs to the corpus, where the
cross-language claim is made, and copying it would give the same bytes two homes. So the corpus
assertions run when a corpus checkout is reachable and are skipped when it is not.

The constructed assertions run always. They are what makes this a guard rather than a courtesy:
``make test`` on a bare checkout still fails a reader that ignores the table.
"""

from __future__ import annotations

import gzip
import math
import os
from collections.abc import Sequence
from pathlib import Path

import pytest

from idfkit.weather import monthly_means, parse_epw

from .epw_fixtures import build_epw

_REPO = Path(__file__).resolve().parents[2]
_SENTINEL_FIXTURE = "USA_IL_Chicago-OHare.Intl.AP.725300_TMY3.epw.gz"


def _corpus_sentinel_fixture() -> str | None:
    """The sentinel-bearing fixture, or ``None`` when no corpus checkout is at hand."""
    candidates = [
        os.environ.get("IDFKIT_CONFORMANCE_DIR"),
        _REPO / "conformance",
        _REPO.parent / "idfkit-conformance",
    ]
    for candidate in candidates:
        if candidate is None:
            continue
        path = Path(candidate) / "checks" / "weather-monthly" / "fixtures" / _SENTINEL_FIXTURE
        if path.is_file():
            with gzip.open(path, "rt", encoding="latin-1") as handle:
                return handle.read()
    return None


CORPUS_TEXT = _corpus_sentinel_fixture()


@pytest.mark.skipif(CORPUS_TEXT is None, reason="no idfkit-conformance checkout to read the fixture from")
class TestCorpusSentinelFixture:
    @pytest.fixture(scope="class")
    def epw(self):
        assert CORPUS_TEXT is not None
        return parse_epw(CORPUS_TEXT)

    def test_reads_the_precipitation_sentinels_as_absent(self, epw) -> None:
        assert epw.hours.row_count == 8760
        assert epw.hours.row_count - epw.hours.present_count["liquid_precipitation_depth"] == 8041
        assert epw.hours.row_count - epw.hours.present_count["liquid_precipitation_quantity"] == 8041

    def test_reads_the_albedo_sentinel_as_absent(self, epw) -> None:
        assert epw.hours.row_count - epw.hours.present_count["albedo"] == 8040

    def test_leaves_the_unlimited_ceiling_rows_alone(self, epw) -> None:
        unlimited = [value for value in epw.hours.ceiling_height if value == 77777]
        assert len(unlimited) == 4244
        # Not one ceiling reading in this file is missing, though more than half of the column
        # carries a reserved value. A rule about magnitude blanks all 4,244.
        assert epw.hours.present_count["ceiling_height"] == 8760

    def test_reads_the_observation_flag_as_absent_where_no_observation_was_made(self, epw) -> None:
        # Every row of this file carries 9, which the dictionary defines as "not made".
        assert epw.hours.present_count["present_weather_observation"] == 0

    def test_does_not_blank_a_column_the_file_measured(self, epw) -> None:
        assert epw.hours.present_count["dry_bulb_temperature"] == 8760
        assert epw.hours.present_count["relative_humidity"] == 8760
        assert epw.hours.present_count["wind_speed"] == 8760


def _with_field(position: int, value: str, only_month: int | None = None) -> str:
    """Rewrite one field of every row."""

    def row(index: int, month: int, day: int, fields: Sequence[str]) -> list[str]:
        if only_month is not None and month != only_month:
            return list(fields)
        changed = list(fields)
        changed[position] = value
        return changed

    return build_epw(row=row)


class TestReservedValues:
    """Per field and per value, never as a rule about magnitude."""

    def test_maps_a_fields_own_missing_value_to_absent(self) -> None:
        hours = parse_epw(_with_field(32, "999.000")).hours
        assert hours.present_count["albedo"] == 0
        assert math.isnan(hours.albedo[0])

    def test_leaves_a_reserved_value_that_is_an_observation_alone(self) -> None:
        # 77777 is an unlimited ceiling, not a missing measurement. This is the case that separates
        # a per-value table from a rule about magnitude.
        hours = parse_epw(_with_field(25, "77777")).hours
        assert hours.present_count["ceiling_height"] == hours.row_count
        assert hours.ceiling_height[0] == 77777

        # 88888 is a cirroform ceiling. It appears in none of the thirty-five sampled files, is in
        # the table anyway because the table is read from the document rather than derived from the
        # evidence, and is asserted here for that reason.
        cirroform = parse_epw(_with_field(25, "88888")).hours
        assert cirroform.present_count["ceiling_height"] == cirroform.row_count
        assert cirroform.ceiling_height[0] == 88888

        # 99999 in the same field is missing.
        assert parse_epw(_with_field(25, "99999")).hours.present_count["ceiling_height"] == 0

    def test_reads_a_missing_value_only_in_the_field_that_reserves_it(self) -> None:
        # 99 is missing for total sky cover and an ordinary reading for relative humidity.
        hours = parse_epw(_with_field(8, "99")).hours
        assert hours.present_count["relative_humidity"] == hours.row_count
        assert hours.relative_humidity[0] == 99

        assert parse_epw(_with_field(22, "99")).hours.present_count["total_sky_cover"] == 0

    def test_keeps_a_real_zero(self) -> None:
        hours = parse_epw(_with_field(13, "0")).hours
        assert hours.present_count["global_horizontal_radiation"] == hours.row_count
        assert hours.global_horizontal_radiation[0] == 0
        assert not math.isnan(hours.global_horizontal_radiation[0])

    def test_distinguishes_an_absence_from_a_failure(self) -> None:
        # A reserved value is a well-formed file saying a measurement was not taken.
        parse_epw(_with_field(32, "999.000"))
        # A field that is not a number at all is not a file saying anything.
        with pytest.raises(ValueError, match="not a number"):
            parse_epw(_with_field(32, ""))

    def test_reads_the_observation_flag_both_ways(self) -> None:
        assert parse_epw(_with_field(26, "0")).hours.present_count["present_weather_observation"] == 8760
        assert parse_epw(_with_field(26, "9")).hours.present_count["present_weather_observation"] == 0


class TestMonthlyMeansOverAPartlyAbsentColumn:
    def test_returns_absent_not_zero_for_a_month_with_no_present_hour(self) -> None:
        means = monthly_means(parse_epw(_with_field(32, "999.000", only_month=1)), "albedo")

        assert math.isnan(means[0].mean)
        assert means[0].count == 0
        # February measured its albedo, so it is a number.
        assert means[1].count == 28 * 24
        assert means[1].mean == pytest.approx(0.195)

    def test_is_distinguishable_from_a_month_whose_mean_is_genuinely_zero(self) -> None:
        def row(index: int, month: int, day: int, fields: Sequence[str]) -> list[str]:
            changed = list(fields)
            changed[32] = "0.000" if month == 1 else "999.000"
            return changed

        means = monthly_means(parse_epw(build_epw(row=row)), "albedo")

        assert means[0].mean == 0
        assert means[0].count == 31 * 24
        assert math.isnan(means[1].mean)
        assert means[1].count == 0

    def test_divides_by_the_hours_that_are_present(self) -> None:
        """Three hours of every January day measured, and twenty-one absent.

        The mean of what exists is 0.01; the sum spread over the month's own extent is one eighth
        of that.

        WHY THIS IS CONSTRUCTED AND NOT COMMITTED. In every sampled file, from both producers, a
        field is either absent for a whole month or absent in exactly one hour of it. A one-hour
        difference is about 0.14%, which falls inside the summary's own rounding, so the corpus
        oracle cannot separate the two divisors and this requirement has to carry its own guard.
        """

        def row(index: int, month: int, day: int, fields: Sequence[str]) -> list[str]:
            if month != 1:
                return list(fields)
            changed = list(fields)
            changed[32] = "0.010" if int(fields[3]) <= 3 else "999.000"
            return changed

        january = monthly_means(parse_epw(build_epw(row=row)), "albedo")[0]

        assert january.count == 31 * 3
        assert january.mean == pytest.approx(0.01, abs=1e-10)
        # The divisor bug produces this instead, and it looks like a number rather than an error.
        assert january.mean != pytest.approx(0.01 * 31 * 3 / (31 * 24), abs=1e-10)
