"""The shape of what the reader returns.

The counterpart of ``idfkit-js/packages/weather/tests/epw.test.ts``, assertion for assertion.
"""

from __future__ import annotations

import math
from array import array
from pathlib import Path

import pytest

from idfkit.weather import load_epw, monthly_means, parse_epw

from .epw_fixtures import build_epw, year_row_count


class TestParseEpw:
    def test_reads_the_header_records(self) -> None:
        epw = parse_epw(build_epw())

        assert epw.location.city == "Chicago Ohare Intl Ap"
        assert epw.location.country == "USA"
        assert epw.location.latitude == pytest.approx(41.98)
        assert epw.location.time_zone == -6
        assert epw.location.elevation == 201

        assert len(epw.typical_periods) == 1
        assert epw.typical_periods[0].kind == "Extreme"
        assert len(epw.ground_temperatures) == 1
        assert epw.ground_temperatures[0].depth == pytest.approx(0.5)
        assert len(epw.ground_temperatures[0].monthly) == 12
        assert epw.holidays.leap_year_observed is False
        assert epw.data_period.records_per_hour == 1
        assert "Constructed for the reader test suite" in epw.comments[0]

    def test_takes_the_row_count_from_the_declared_data_period(self) -> None:
        assert parse_epw(build_epw()).hours.row_count == year_row_count(False)
        assert parse_epw(build_epw(leap_year=True)).hours.row_count == year_row_count(True)

    def test_exposes_every_numeric_field_as_a_named_column(self) -> None:
        hours = parse_epw(build_epw()).hours

        assert isinstance(hours.dry_bulb_temperature, array)
        assert hours.dry_bulb_temperature.typecode == "d"
        assert len(hours.dry_bulb_temperature) == year_row_count(False)
        assert hours.dry_bulb_temperature[0] == pytest.approx(2.8)
        assert hours.dew_point_temperature[0] == pytest.approx(-3.3)
        assert hours.relative_humidity[0] == 62
        assert hours.atmospheric_station_pressure[0] == 92453
        assert hours.wind_speed[0] == pytest.approx(2.6)
        assert hours.wind_direction[0] == 160
        assert hours.horizontal_infrared_radiation_intensity_from_sky[0] == 256
        assert hours.visibility[0] == pytest.approx(777.7)

    def test_keeps_the_two_text_fields_as_text(self) -> None:
        hours = parse_epw(build_epw()).hours

        assert isinstance(hours.source_and_uncertainty_flags[0], str)
        # Nine single-digit observations side by side, not nine hundred and ninety-nine million.
        assert hours.present_weather_codes[0] == "999999999"

    def test_runs_the_hour_column_1_to_24(self) -> None:
        hours = parse_epw(build_epw()).hours

        assert hours.hour[0] == 1
        assert hours.hour[23] == 24
        # Hour 24 belongs to 1 January, not to 2 January.
        assert hours.day[23] == 1
        assert hours.hour[24] == 1
        assert hours.day[24] == 2

    def test_reads_both_line_ending_conventions_and_a_mixture_identically(self) -> None:
        lf = parse_epw(build_epw(line_ending="\n"))
        crlf = parse_epw(build_epw(line_ending="\r\n"))

        assert crlf.hours.row_count == lf.hours.row_count
        assert crlf.location.city == lf.location.city
        assert list(crlf.hours.dry_bulb_temperature) == list(lf.hours.dry_bulb_temperature)
        assert crlf.hours.present_weather_codes[0] == lf.hours.present_weather_codes[0]

        # A file whose lines do not agree with each other, which is what a hand-edited file looks like.
        mixed = "\n".join(
            f"{line}\r" if index % 3 == 0 else line
            for index, line in enumerate(build_epw(line_ending="\n").split("\n"))
        )
        parsed = parse_epw(mixed)
        assert parsed.hours.row_count == lf.hours.row_count
        assert list(parsed.hours.dry_bulb_temperature) == list(lf.hours.dry_bulb_temperature)

    def test_keeps_a_station_name_outside_ascii(self) -> None:
        assert parse_epw(build_epw(city="Montréal-Trudeau")).location.city == "Montréal-Trudeau"


class TestParseEpwRefusals:
    """It refuses a file it cannot read, and returns nothing at all."""

    def test_on_a_header_short_of_its_eight_records(self) -> None:
        truncated = "\n".join(build_epw().split("\n")[:5])
        with pytest.raises(ValueError, match="header"):
            parse_epw(truncated)

    def test_on_a_header_record_out_of_order(self) -> None:
        lines = build_epw().split("\n")
        lines[2], lines[3] = lines[3], lines[2]
        with pytest.raises(ValueError, match=r"TYPICAL/EXTREME PERIODS"):
            parse_epw("\n".join(lines))

    def test_on_a_row_with_the_wrong_field_count_naming_the_row(self) -> None:
        text = build_epw(row=lambda index, month, day, fields: fields[:34] if index == 41 else fields)
        # Line 50 of the file is row 42 of the table: eight header records come first.
        with pytest.raises(ValueError, match=r"line 50, which is row 42 .* has 34 fields and the format has 35"):
            parse_epw(text)

    def test_on_a_numeric_field_that_is_not_a_number(self) -> None:
        def broken(index: int, month: int, day: int, fields: list[str]) -> list[str]:
            if index != 0:
                return fields
            changed = list(fields)
            changed[6] = "warm"
            return changed

        with pytest.raises(ValueError, match=r'row 1 .*"warm".*dry_bulb_temperature'):
            parse_epw(build_epw(row=broken))

    def test_on_a_file_truncated_part_way_through_the_year(self) -> None:
        truncated = "\n".join(build_epw().split("\n")[:4000])
        with pytest.raises(ValueError, match=r"which is 8760 records, and the file carries 3992"):
            parse_epw(truncated)

    def test_on_a_file_longer_than_its_own_declaration(self) -> None:
        lines = build_epw().rstrip("\n").split("\n")
        lines.append(lines[-1])
        with pytest.raises(ValueError, match=r"8760 records, and the file carries 8761"):
            parse_epw("\n".join(lines))


class TestMonthlyMeans:
    def test_returns_twelve_entries_january_first_each_carrying_its_count(self) -> None:
        means = monthly_means(parse_epw(build_epw()), "dry_bulb_temperature")

        assert len(means) == 12
        assert [entry.month for entry in means] == list(range(1, 13))
        assert means[0].count == 31 * 24
        assert means[1].count == 28 * 24
        assert means[0].mean == pytest.approx(2.8)

    def test_takes_a_month_extent_from_the_calendar(self) -> None:
        means = monthly_means(parse_epw(build_epw(leap_year=True)), "dry_bulb_temperature")
        assert means[1].count == 696

    def test_is_the_mean_of_the_values_that_exist(self) -> None:
        def alternating(index: int, month: int, day: int, fields: list[str]) -> list[str]:
            if month != 1:
                return fields
            changed = list(fields)
            changed[6] = "10.0" if index % 2 == 0 else "20.0"
            return changed

        january = monthly_means(parse_epw(build_epw(row=alternating)), "dry_bulb_temperature")[0]
        assert january.mean == pytest.approx(15)
        assert january.count == 31 * 24

    def test_refuses_a_column_that_is_not_numeric(self) -> None:
        with pytest.raises(ValueError, match="not a numeric column"):
            monthly_means(parse_epw(build_epw()), "present_weather_codes")


class TestLoadEpw:
    def test_reads_a_path_decoding_as_the_weather_formats_are_written(self, tmp_path: Path) -> None:
        path = tmp_path / "accented.epw"
        # Latin-1 on the way out, which is how the downloader stores these files. Read as UTF-8 the
        # é is a lone high byte and the decode fails outright.
        path.write_text(build_epw(city="Montréal-Trudeau"), encoding="latin-1")

        epw = load_epw(path)
        assert epw.location.city == "Montréal-Trudeau"
        assert epw.hours.row_count == year_row_count(False)


class TestLeapYear:
    """A constructed leap-year file, which no upstream archive publishes.

    Kept out of the corpus because a file neither EnergyPlus nor the Weather Converter produced has
    no oracle behind it. This is the month's extent, not a mean's divisor: those are different
    numbers and fusing them is the defect the sentinel suite guards.
    """

    def test_reads_8784_rows_and_a_february_of_696(self) -> None:
        epw = parse_epw(build_epw(leap_year=True))

        assert epw.hours.row_count == 8784
        assert epw.holidays.leap_year_observed is True
        february = [row for row in range(epw.hours.row_count) if epw.hours.month[row] == 2]
        assert len(february) == 696
        assert max(epw.hours.day[row] for row in february) == 29

    def test_a_common_year_february_holds_672(self) -> None:
        epw = parse_epw(build_epw())
        assert epw.hours.row_count == 8760
        assert sum(1 for row in range(epw.hours.row_count) if epw.hours.month[row] == 2) == 672

    def test_a_leap_year_file_declaring_a_common_year_extent_fails(self) -> None:
        # The declaration and the file have to agree, and a leap file whose header says otherwise
        # is exactly the disagreement FR-004 refuses to paper over.
        text = build_epw(leap_year=True).replace("HOLIDAYS/DAYLIGHT SAVINGS,Yes", "HOLIDAYS/DAYLIGHT SAVINGS,No")
        with pytest.raises(ValueError, match=r"which is 8760 records, and the file carries 8784"):
            parse_epw(text)


def test_absence_is_nan_and_not_a_number_the_file_could_have_carried() -> None:
    hours = parse_epw(build_epw(row=lambda i, m, d, f: [*f[:32], "999.000", *f[33:]])).hours
    assert hours.present_count["albedo"] == 0
    assert math.isnan(hours.albedo[0])
