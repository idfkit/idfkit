"""Read an EPW weather file: the eight header records, and the hourly table as columns.

The text is what :meth:`WeatherDownloader.download` already puts on disk, so this is the step
between retrieving a station's weather and computing anything from it. Nothing here touches the
network, the clock or any global state, and :func:`parse_epw` touches no filesystem either.

The hour convention, stated once
--------------------------------

The ``hour`` column runs 1 to 24, and hour 24 is the last hour of its **own** day rather than
hour 0 of the next. A chart that treats 24 as midnight of the following day is off by one for
every day of the year, and discovers it late. This is the format's convention, not a choice made
here.

The shape of a column
---------------------

Every numeric field is one packed :class:`array.array` of doubles, and absence is ``nan``. Both
halves of that are load-bearing and are settled in the feature's contract rather than here:

* **Packed**, because thirty-five columns of 8,760 doubles is 2.45 MB, which is the arithmetic
  width of packed doubles and is reachable no other way. A list of ``float | None`` costs three
  to four times as much.
* **Doubles rather than floats, and this is forced.** The two libraries must return the same
  values within a relative tolerance of 1e-12, and single precision carries about 1e-7. Halving
  the width is the first optimisation anyone looking at 2.45 MB will reach for; every test in
  this repository would still pass and the thing it breaks is agreement with the JavaScript
  library, which only the shared corpus can see. It is a correctness constraint wearing the
  costume of a performance trade.
* **``nan`` for absence**, because no physical quantity in this format can be nan and no EPW can
  express one, so it is not a value the file could have carried. It is distinguishable from a
  real zero, and it propagates loudly through arithmetic rather than quietly biasing a result.

What is exported
----------------

Four names are registered for this capability in the naming register: ``parse_epw``,
``load_epw``, ``WeatherFile`` and ``monthly_means``, and those are what
:mod:`idfkit.weather` re-exports. The record types below are named for readability and reachable
through this module; they are not a second set of registered concepts.
"""

from __future__ import annotations

import math
import re
from array import array
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Final

from ._epw_sentinels import MISSING_VALUES

__all__ = ["WeatherFile", "load_epw", "monthly_means", "parse_epw"]


# ---------------------------------------------------------------------------
# The hourly table's columns
# ---------------------------------------------------------------------------
#
# Positions are how the reader finds a field. No caller counts to one, which is what "access is by
# name" means. The order below IS the file's field order and the two text positions sit in it
# rather than beside it, so a reader of this list can check it against the data dictionary line by
# line.

COLUMN_NAMES: Final[tuple[str, ...]] = (
    "year",
    "month",
    "day",
    "hour",
    "minute",
    "source_and_uncertainty_flags",
    "dry_bulb_temperature",
    "dew_point_temperature",
    "relative_humidity",
    "atmospheric_station_pressure",
    "extraterrestrial_horizontal_radiation",
    "extraterrestrial_direct_normal_radiation",
    "horizontal_infrared_radiation_intensity_from_sky",
    "global_horizontal_radiation",
    "direct_normal_radiation",
    "diffuse_horizontal_radiation",
    "global_horizontal_illuminance",
    "direct_normal_illuminance",
    "diffuse_horizontal_illuminance",
    "zenith_luminance",
    "wind_direction",
    "wind_speed",
    "total_sky_cover",
    "opaque_sky_cover",
    "visibility",
    "ceiling_height",
    "present_weather_observation",
    "present_weather_codes",
    "precipitable_water",
    "aerosol_optical_depth",
    "snow_depth",
    "days_since_last_snowfall",
    "albedo",
    "liquid_precipitation_depth",
    "liquid_precipitation_quantity",
)

#: The two text columns.
#:
#: Position 5 is obviously text. Position 27 is not: it holds a nine-digit code such as
#: ``999999999``, which is nine single-digit observations written side by side and not the number
#: nine hundred and ninety-nine million. Coercing it yields a column of meaningless integers, so it
#: is text and is never parsed.
TEXT_POSITIONS: Final[frozenset[int]] = frozenset({5, 27})

#: How many comma-separated fields an hourly row must have.
FIELD_COUNT: Final = len(COLUMN_NAMES)

#: Per position, the values that mean the measurement was not made.
#:
#: Read from the generated table rather than written here, and applied PER FIELD AND PER VALUE
#: rather than as a rule about magnitude. 99 is missing for total sky cover and an ordinary reading
#: for relative humidity; 77777 in ceiling height is an unlimited ceiling and stays a number. A
#: reader that blanked large numbers would blank 55% of the ceiling column in the sampled corpus
#: and report a real sky condition as unmeasured.
_MISSING_AT_POSITION: Final[dict[int, frozenset[float]]] = {
    position: frozenset(values) for position, values in MISSING_VALUES
}


# ---------------------------------------------------------------------------
# The header records
# ---------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class EpwLocation:
    """Where the station is. The one header record a caller reads routinely."""

    city: str
    state_province_region: str
    country: str
    data_source: str
    wmo_number: str
    #: Degrees north, negative south.
    latitude: float
    #: Degrees east, negative west.
    longitude: float
    #: Hours from UTC, negative west.
    time_zone: float
    #: Metres above sea level.
    elevation: float


@dataclass(frozen=True, slots=True)
class EpwPeriod:
    """One named period from the ``TYPICAL/EXTREME PERIODS`` record."""

    name: str
    #: ``Typical`` or ``Extreme``, as the file spells it.
    kind: str
    #: ``month/day``, as the file spells it.
    start: str
    end: str


@dataclass(frozen=True, slots=True)
class EpwGroundTemperatures:
    """One depth's worth of the ``GROUND TEMPERATURES`` record."""

    #: Metres below grade.
    depth: float
    #: Absent in every file sampled, and optional in the format.
    soil_conductivity: float | None
    soil_density: float | None
    soil_specific_heat: float | None
    #: Twelve monthly values, January first.
    monthly: tuple[float, ...]


@dataclass(frozen=True, slots=True)
class EpwSpecialDay:
    """One entry of the ``HOLIDAYS/DAYLIGHT SAVINGS`` record's named-day list."""

    name: str
    kind: str
    start: str
    duration: int


@dataclass(frozen=True, slots=True)
class EpwHolidays:
    """The ``HOLIDAYS/DAYLIGHT SAVINGS`` record."""

    #: Whether the file's calendar has a 29 February.
    #:
    #: Read, and used to say which calendar the data period's month/day dates are read against. It
    #: is not itself what decides the row count: the declared period is, and a partial period holds
    #: what its own extent holds whatever this says.
    leap_year_observed: bool
    daylight_saving_start: str
    daylight_saving_end: str
    special_days: tuple[EpwSpecialDay, ...]


@dataclass(frozen=True, slots=True)
class EpwDataPeriod:
    """The ``DATA PERIODS`` record, which is load-bearing.

    It declares the interval and the extent, and the row count is taken from it rather than from a
    constant of 8,760. A file whose rows disagree with its own declaration fails rather than being
    truncated or padded.
    """

    #: How many periods the record declares. One in every file sampled.
    period_count: int
    records_per_hour: int
    name: str
    start_day_of_week: str
    #: ``month/day``, as the file spells it.
    start_date: str
    end_date: str


@dataclass(frozen=True, slots=True)
class HourlyTable:
    """The hourly table, as columns rather than rows.

    One entry per record of the declared period, in file order. Every numeric column is a packed
    ``array('d')`` carrying ``nan`` where the file said the measurement was not taken; the two
    text columns are tuples of strings.

    Columns are reached by name, which is the whole point of the reader::

        table.dry_bulb_temperature[0]
    """

    #: How many records the table holds. Equal to every column's length.
    row_count: int
    year: array[float]
    month: array[float]
    day: array[float]
    hour: array[float]
    minute: array[float]
    source_and_uncertainty_flags: tuple[str, ...]
    dry_bulb_temperature: array[float]
    dew_point_temperature: array[float]
    relative_humidity: array[float]
    atmospheric_station_pressure: array[float]
    extraterrestrial_horizontal_radiation: array[float]
    extraterrestrial_direct_normal_radiation: array[float]
    horizontal_infrared_radiation_intensity_from_sky: array[float]
    global_horizontal_radiation: array[float]
    direct_normal_radiation: array[float]
    diffuse_horizontal_radiation: array[float]
    global_horizontal_illuminance: array[float]
    direct_normal_illuminance: array[float]
    diffuse_horizontal_illuminance: array[float]
    zenith_luminance: array[float]
    wind_direction: array[float]
    wind_speed: array[float]
    total_sky_cover: array[float]
    opaque_sky_cover: array[float]
    visibility: array[float]
    ceiling_height: array[float]
    present_weather_observation: array[float]
    present_weather_codes: tuple[str, ...]
    precipitable_water: array[float]
    aerosol_optical_depth: array[float]
    snow_depth: array[float]
    days_since_last_snowfall: array[float]
    albedo: array[float]
    liquid_precipitation_depth: array[float]
    liquid_precipitation_quantity: array[float]
    #: How many records of each numeric column are present, meaning not absent.
    #:
    #: Carried rather than recomputed: a caller that needed it would otherwise rescan the column,
    #: and :func:`monthly_means` needs it anyway.
    present_count: Mapping[str, int]


@dataclass(frozen=True, slots=True)
class WeatherFile:
    """One station's typical year, as read from EPW text.

    Not to be confused with :class:`~idfkit.weather.download.WeatherFiles`, plural, which is what
    retrieval hands back: the EPW, DDY and STAT members of one archive. This is what reading ONE
    of those members produces. The two names are one character apart, which is a hazard worth
    naming here rather than discovering in review.
    """

    location: EpwLocation
    #: The ``DESIGN CONDITIONS`` record as it stands, uninterpreted.
    #:
    #: Retained rather than parsed. A caller who wants design conditions is sent to the DDY member
    #: of the same archive, which :class:`DesignDayManager` already reads.
    design_conditions: str
    typical_periods: tuple[EpwPeriod, ...]
    ground_temperatures: tuple[EpwGroundTemperatures, ...]
    holidays: EpwHolidays
    #: The two ``COMMENTS`` records, as text. They carry provenance and no structure worth imposing.
    comments: tuple[str, str]
    data_period: EpwDataPeriod
    hours: HourlyTable


@dataclass(frozen=True, slots=True)
class MonthlyMean:
    """One month's mean of one column, and how many hours went into it."""

    #: 1 to 12.
    month: int
    #: The mean of the hours that were present, or ``nan`` when none was.
    mean: float
    #: How many hours went into it. Zero when the whole month is absent.
    count: int


# ---------------------------------------------------------------------------
# Header parsing
# ---------------------------------------------------------------------------

#: The eight header records, in the order the format fixes them.
_HEADER_KEYWORDS: Final = (
    "LOCATION",
    "DESIGN CONDITIONS",
    "TYPICAL/EXTREME PERIODS",
    "GROUND TEMPERATURES",
    "HOLIDAYS/DAYLIGHT SAVINGS",
    "COMMENTS 1",
    "COMMENTS 2",
    "DATA PERIODS",
)


def _fields(line: str) -> list[str]:
    """Split a header record on commas. Header records carry no escaped commas outside quotes."""
    return [field.strip() for field in line.split(",")]


def _remainder(line: str) -> str:
    """Everything after the first comma. Used for records kept as text."""
    _, separator, rest = line.partition(",")
    return rest if separator else ""


#: The grammar of a number in this format, shared with the JavaScript reader verbatim.
#:
#: Neither language's built-in conversion is used on its own, because the two disagree about what
#: text is a number and the disagreement is silent. ``float`` accepts ``nan``, ``inf`` and
#: ``1_0``; ``Number`` rejects all three and accepts ``0x10`` as sixteen. A file carrying ``nan``
#: in dry bulb would read as one absent hour here and raise there, and no fixture in the corpus
#: carries one to catch it. Both readers therefore match this grammar first and convert second.
_NUMBER: Final = re.compile(r"[+-]?(?:\d+\.?\d*|\.\d+)(?:[eE][+-]?\d+)?")

#: The same, for a field that counts rather than measures. ``1.5`` records per hour is a corrupt
#: declaration, not a rounding problem, and this reader refuses what it cannot represent.
_INTEGER: Final = re.compile(r"[+-]?\d+")


def _to_number(raw: str) -> float | None:
    """The number ``raw`` spells, or ``None`` when it spells none."""
    text = raw.strip()
    return float(text) if _NUMBER.fullmatch(text) else None


def _to_integer(raw: str) -> int | None:
    """The whole number ``raw`` spells, or ``None`` when it spells none."""
    text = raw.strip()
    return int(text) if _INTEGER.fullmatch(text) else None


def _number_at(parts: Sequence[str], index: int, what: str) -> float:
    if index >= len(parts) or parts[index] == "":
        msg = f"EPW header: {what} is missing from the {parts[0] if parts else 'header'} record"
        raise ValueError(msg)
    value = _to_number(parts[index])
    if value is None:
        msg = f'EPW header: {what} is "{parts[index]}", which is not a number'
        raise ValueError(msg)
    return value


def _integer_at(parts: Sequence[str], index: int, what: str) -> int:
    if index >= len(parts) or parts[index] == "":
        msg = f"EPW header: {what} is missing from the {parts[0] if parts else 'header'} record"
        raise ValueError(msg)
    value = _to_integer(parts[index])
    if value is None:
        msg = f'EPW header: {what} is "{parts[index]}", which is not a whole number'
        raise ValueError(msg)
    return value


def _optional_number_at(parts: Sequence[str], index: int) -> float | None:
    if index >= len(parts) or parts[index] == "":
        return None
    return _to_number(parts[index])


def _parse_location(line: str) -> EpwLocation:
    parts = _fields(line)
    if len(parts) < 10:
        msg = f"EPW header: the LOCATION record has {len(parts) - 1} fields, expected 9"
        raise ValueError(msg)
    return EpwLocation(
        city=parts[1],
        state_province_region=parts[2],
        country=parts[3],
        data_source=parts[4],
        wmo_number=parts[5],
        latitude=_number_at(parts, 6, "latitude"),
        longitude=_number_at(parts, 7, "longitude"),
        time_zone=_number_at(parts, 8, "time zone"),
        elevation=_number_at(parts, 9, "elevation"),
    )


def _parse_typical_periods(line: str) -> tuple[EpwPeriod, ...]:
    parts = _fields(line)
    declared = int(_optional_number_at(parts, 1) or 0)
    periods: list[EpwPeriod] = []
    for index in range(declared):
        at = 2 + index * 4
        if len(parts) < at + 4:
            msg = f"EPW header: TYPICAL/EXTREME PERIODS declares {declared} periods and carries {index}"
            raise ValueError(msg)
        periods.append(EpwPeriod(name=parts[at], kind=parts[at + 1], start=parts[at + 2], end=parts[at + 3]))
    return tuple(periods)


def _parse_ground_temperatures(line: str) -> tuple[EpwGroundTemperatures, ...]:
    parts = _fields(line)
    declared = int(_optional_number_at(parts, 1) or 0)
    sets: list[EpwGroundTemperatures] = []
    at = 2
    for index in range(declared):
        if len(parts) < at + 16:
            msg = f"EPW header: GROUND TEMPERATURES declares {declared} sets and carries {index}"
            raise ValueError(msg)
        monthly = tuple(
            _number_at(parts, at + 4 + month, f"ground temperature month {month + 1}") for month in range(12)
        )
        sets.append(
            EpwGroundTemperatures(
                depth=_number_at(parts, at, "ground temperature depth"),
                soil_conductivity=_optional_number_at(parts, at + 1),
                soil_density=_optional_number_at(parts, at + 2),
                soil_specific_heat=_optional_number_at(parts, at + 3),
                monthly=monthly,
            )
        )
        at += 16
    return tuple(sets)


def _parse_holidays(line: str) -> EpwHolidays:
    parts = _fields(line)
    declared = int(_optional_number_at(parts, 4) or 0)
    special_days: list[EpwSpecialDay] = []
    for index in range(declared):
        at = 5 + index * 4
        if len(parts) < at + 4:
            break
        special_days.append(
            EpwSpecialDay(
                name=parts[at],
                kind=parts[at + 1],
                start=parts[at + 2],
                duration=int(_optional_number_at(parts, at + 3) or 0),
            )
        )
    return EpwHolidays(
        leap_year_observed=len(parts) > 1 and parts[1].lower().startswith("y"),
        daylight_saving_start=parts[2] if len(parts) > 2 else "0",
        daylight_saving_end=parts[3] if len(parts) > 3 else "0",
        special_days=tuple(special_days),
    )


def _parse_data_period(line: str) -> EpwDataPeriod:
    parts = _fields(line)
    if len(parts) < 7:
        msg = f"EPW header: the DATA PERIODS record has {len(parts) - 1} fields, expected at least 6"
        raise ValueError(msg)
    period_count = _integer_at(parts, 1, "the number of data periods")
    if period_count != 1:
        msg = (
            f"EPW header: DATA PERIODS declares {period_count} periods. This reader reads a "
            f"single-period file, and refuses what it cannot represent rather than guessing"
        )
        raise ValueError(msg)
    return EpwDataPeriod(
        period_count=period_count,
        records_per_hour=_integer_at(parts, 2, "records per hour"),
        name=parts[3],
        start_day_of_week=parts[4],
        start_date=parts[5],
        end_date=parts[6],
    )


# ---------------------------------------------------------------------------
# How many records the declaration asks for
# ---------------------------------------------------------------------------

_DAYS_IN_MONTH: Final = (31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31)


def _parse_month_day(text: str, what: str) -> tuple[int, int]:
    """``1/ 1``, `` 1/1``, ``1/1/2016``. A written year is ignored: the calendar comes from the flag."""
    parts = [part.strip() for part in text.split("/")]
    month = _to_integer(parts[0]) if len(parts) > 0 else None
    day = _to_integer(parts[1]) if len(parts) > 1 else None
    if month is None or day is None:
        msg = f'EPW header: the data period\'s {what} is "{text}", which is not a month/day date'
        raise ValueError(msg)
    if not 1 <= month <= 12 or day < 1:
        msg = f'EPW header: the data period\'s {what} is "{text}", which is not a month/day date'
        raise ValueError(msg)
    return month, day


def _day_of_year(month: int, day: int, leap: bool) -> int:
    """Day of the year, 1-based, on the calendar the leap flag selects."""
    return day + sum(_DAYS_IN_MONTH[m - 1] + (1 if leap and m == 2 else 0) for m in range(1, month))


def _declared_row_count(period: EpwDataPeriod, leap_year_observed: bool) -> int:
    """How many records the declared period asks for.

    FR-004: taken from the declaration, never from a constant. The leap flag says which calendar
    the declared month/day dates are read against, which is how a leap-year file declaring 1/1 to
    12/31 asks for 8,784 records rather than 8,760. That is the period's own extent, not a flag
    overriding it.
    """
    start_month, start_day = _parse_month_day(period.start_date, "start date")
    end_month, end_day = _parse_month_day(period.end_date, "end date")
    first = _day_of_year(start_month, start_day, leap_year_observed)
    last = _day_of_year(end_month, end_day, leap_year_observed)
    year_length = 366 if leap_year_observed else 365
    # A period may wrap the end of the year, which the format permits.
    days = last - first + 1 if last >= first else year_length - first + 1 + last
    if period.records_per_hour < 1:
        msg = f"EPW header: the data period declares {period.records_per_hour} records per hour, which is not a count"
        raise ValueError(msg)
    return days * 24 * period.records_per_hour


# ---------------------------------------------------------------------------
# The reader
# ---------------------------------------------------------------------------


def parse_epw(text: str) -> WeatherFile:
    """Read an EPW weather file from text.

    The primary form. Synchronous, pure, and free of input and output: no network, no filesystem,
    no clock, no global state.

    Args:
        text: The file's decoded text. Decode it as the weather formats are written, which is
            latin-1 and not UTF-8; :func:`load_epw` does.

    Returns:
        The header records and the hourly table as columns.

    Raises:
        ValueError: If the header is short of its eight records, if a row has the wrong field
            count, or if the file disagrees with its own declared data period. Nothing partial is
            ever returned: a short or partly populated table is the failure this refuses to hand
            back.

    Example:
        ```python
        from idfkit.weather import parse_epw

        epw = parse_epw(Path("chicago.epw").read_text(encoding="latin-1"))
        epw.hours.dry_bulb_temperature[0]  # the first hour's dry bulb, in C
        ```
    """
    lines = text.replace("\r\n", "\n").replace("\r", "\n").split("\n")
    # A final newline is a line terminator, not an empty record.
    while lines and lines[-1].strip() == "":
        lines.pop()

    if len(lines) < len(_HEADER_KEYWORDS):
        msg = f"EPW: the file has {len(lines)} lines, which is short of the {len(_HEADER_KEYWORDS)} header records"
        raise ValueError(msg)

    for index, keyword in enumerate(_HEADER_KEYWORDS):
        if not lines[index].upper().startswith(keyword):
            msg = f'EPW: line {index + 1} should be the {keyword} record and starts "{lines[index][:32]}"'
            raise ValueError(msg)
    header = lines[: len(_HEADER_KEYWORDS)]

    holidays = _parse_holidays(header[4])
    data_period = _parse_data_period(header[7])
    expected = _declared_row_count(data_period, holidays.leap_year_observed)
    present = len(lines) - len(_HEADER_KEYWORDS)
    if present != expected:
        msg = (
            f"EPW: the data period declares {data_period.start_date} to {data_period.end_date} at "
            f"{data_period.records_per_hour} record(s) per hour, which is {expected} records, "
            f"and the file carries {present}"
        )
        raise ValueError(msg)

    return WeatherFile(
        location=_parse_location(header[0]),
        design_conditions=_remainder(header[1]),
        typical_periods=_parse_typical_periods(header[2]),
        ground_temperatures=_parse_ground_temperatures(header[3]),
        holidays=holidays,
        comments=(_remainder(header[5]), _remainder(header[6])),
        data_period=data_period,
        hours=_read_table(lines, len(_HEADER_KEYWORDS), expected),
    )


def _read_table(lines: Sequence[str], offset: int, row_count: int) -> HourlyTable:
    """Fill one packed column per numeric field, and one tuple per text field."""
    numeric: dict[int, array[float]] = {
        position: array("d", bytes(8 * row_count)) for position in range(FIELD_COUNT) if position not in TEXT_POSITIONS
    }
    text: dict[int, list[str]] = {position: [""] * row_count for position in TEXT_POSITIONS}

    for row in range(row_count):
        line = lines[offset + row]
        parts = line.split(",")
        if len(parts) != FIELD_COUNT:
            msg = (
                f"EPW: line {offset + row + 1}, which is row {row + 1} of the hourly table, has "
                f"{len(parts)} fields and the format has {FIELD_COUNT}"
            )
            raise ValueError(msg)
        for position, raw in enumerate(parts):
            if position in TEXT_POSITIONS:
                text[position][row] = raw
                continue
            value = _to_number(raw)
            if value is None:
                msg = (
                    f"EPW: line {offset + row + 1}, which is row {row + 1} of the hourly table, "
                    f'holds "{raw}" at field {position + 1} ({COLUMN_NAMES[position]}), '
                    f"which is not a number"
                )
                raise ValueError(msg)
            # A value the field reserves for "not measured" becomes absent here, and absence is
            # nan: out of the domain the field can take, distinguishable from a real zero, and
            # loud rather than quiet in later arithmetic.
            missing = _MISSING_AT_POSITION.get(position)
            numeric[position][row] = math.nan if missing is not None and value in missing else value

    columns: dict[str, object] = {}
    present_count: dict[str, int] = {}
    for position, name in enumerate(COLUMN_NAMES):
        if position in TEXT_POSITIONS:
            columns[name] = tuple(text[position])
            continue
        column = numeric[position]
        columns[name] = column
        present_count[name] = sum(1 for value in column if not math.isnan(value))

    return HourlyTable(row_count=row_count, present_count=present_count, **columns)  # type: ignore[arg-type]


def load_epw(path: str | Path) -> WeatherFile:
    """Read an EPW weather file from a path.

    A convenience over :func:`parse_epw` and nothing more: it reads the bytes, decodes them
    latin-1, which is how the weather formats are written and how the downloader stores them, and
    hands the text on. Every rule about what is read, what is absent and what fails belongs to
    :func:`parse_epw`.

    Args:
        path: The ``.epw`` file to read.
    """
    return parse_epw(Path(path).read_text(encoding="latin-1"))


# ---------------------------------------------------------------------------
# Monthly aggregates
# ---------------------------------------------------------------------------


def monthly_means(file: WeatherFile, field: str) -> list[MonthlyMean]:
    """The monthly means of one numeric column, each carrying the count of hours it included.

    **Absent hours are excluded from the sum AND from the divisor**, so the result is the mean of
    the values that exist rather than their sum spread over hours that do not. Fusing the two
    yields a number biased towards zero in proportion to how much is absent, which looks plausible
    rather than wrong and which no committed fixture can detect.

    The month's extent and the divisor are different numbers. February in a leap year holds 696
    records rather than 672; that decides which records belong to the month, and it is not what the
    mean divides by.

    **The count is part of the answer rather than derivable from it.** Without it a caller cannot
    tell a mean over 744 hours from a mean over three, and both look like numbers.

    Args:
        file: A weather file, as :func:`parse_epw` returned it.
        field: Which numeric column to aggregate, by its name on the hourly table.

    Returns:
        Twelve entries, January first.

    Example:
        ```python
        january = monthly_means(epw, "dry_bulb_temperature")[0]
        january.mean   # nan when the month held no measurement at all
        january.count  # and 0 beside it, which says why
        ```
    """
    # `present_count` holds exactly the numeric columns, so this also rejects the two text ones.
    if field not in file.hours.present_count:
        msg = f"{field!r} is not a numeric column of the hourly table"
        raise ValueError(msg)

    values: array[float] = getattr(file.hours, field)
    months: array[float] = file.hours.month
    sums = [0.0] * 12
    counts = [0] * 12

    for row in range(file.hours.row_count):
        value = values[row]
        if math.isnan(value):
            continue
        # Skipped rather than truncated when it is not a whole month, so a row carrying 1.5 falls
        # out of every bucket here as it does in the JavaScript reader, instead of landing in
        # January in one language and nowhere in the other.
        month = months[row]
        if not month.is_integer() or not 1 <= month <= 12:
            continue
        index = int(month)
        sums[index - 1] += value
        counts[index - 1] += 1

    # A month with no present hour is absent, not zero, and the count says which.
    return [
        MonthlyMean(
            month=month + 1,
            mean=math.nan if counts[month] == 0 else sums[month] / counts[month],
            count=counts[month],
        )
        for month in range(12)
    ]
