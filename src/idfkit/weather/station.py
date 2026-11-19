"""Weather station data model and search result types."""

from __future__ import annotations

import re
from collections.abc import Iterable
from dataclasses import dataclass, field
from typing import Any

__all__ = [
    "SearchResult",
    "SpatialResult",
    "WeatherStation",
]

_YEAR_RANGE = re.compile(r"(\d{4})-(\d{4})$")


@dataclass(frozen=True)
class WeatherStation:
    """Metadata for a single weather file entry from climate.onebuilding.org.

    Each instance represents one downloadable weather dataset. The same physical
    station may appear multiple times with different ``source`` or year-range
    variants (e.g. ``TMYx.2007-2021`` vs ``TMYx.2009-2023``).

    Attributes:
        country: ISO 3166 country code (e.g. ``"USA"``).
        state: State or province abbreviation (e.g. ``"CA"``).
        city: City or station name as it appears in the index
            (e.g. ``"Marina.Muni.AP"``).
        wmo: WMO station number as a string to preserve leading zeros
            (e.g. ``"722950"`` or ``"012345"``).
        source: Source tag from the upstream index (e.g. ``"SRC-TMYx"``). To tell
            the datasets of one station apart, read
            [dataset_variant][idfkit.weather.station.WeatherStation.dataset_variant]
            (e.g. ``"TMYx.2009-2023"``) instead.
        latitude: Decimal degrees, north positive.
        longitude: Decimal degrees, east positive.
        timezone: Hours offset from GMT (e.g. ``-8.0``).
        elevation: Meters above sea level.
        url: Full download URL for the ZIP archive.
        ashrae_climate_zone: ASHRAE HOF climate zone label
            (e.g. ``"4A - Mixed - Humid"``).
        heating_design_db_c: 99% heating design dry-bulb temperature in °C.
        cooling_design_db_c: 1% cooling design dry-bulb temperature in °C.
        hdd18: Heating degree-days base 18 °C.
        cdd10: Cooling degree-days base 10 °C.
        design_conditions_source_wmo: When the station inherits design
            conditions from a neighbouring station, this holds that
            station's WMO number; otherwise ``None``.
    """

    country: str
    state: str
    city: str
    wmo: str
    source: str
    latitude: float
    longitude: float
    timezone: float
    elevation: float
    url: str
    ashrae_climate_zone: str
    heating_design_db_c: float
    cooling_design_db_c: float
    hdd18: int
    cdd10: int
    design_conditions_source_wmo: str | None = None

    def to_dict(self) -> dict[str, Any]:
        """Serialize to a plain dictionary for JSON storage."""
        return {
            "country": self.country,
            "state": self.state,
            "city": self.city,
            "wmo": self.wmo,
            "source": self.source,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "timezone": self.timezone,
            "elevation": self.elevation,
            "url": self.url,
            "ashrae_climate_zone": self.ashrae_climate_zone,
            "heating_design_db_c": self.heating_design_db_c,
            "cooling_design_db_c": self.cooling_design_db_c,
            "hdd18": self.hdd18,
            "cdd10": self.cdd10,
            "design_conditions_source_wmo": self.design_conditions_source_wmo,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> WeatherStation:
        """Deserialize from a plain dictionary.

        The required climate fields use ``data[key]`` so a stale or
        corrupt payload fails loudly. ``design_conditions_source_wmo``
        is genuinely optional.
        """
        source_wmo = data.get("design_conditions_source_wmo")
        return cls(
            country=str(data["country"]),
            state=str(data["state"]),
            city=str(data["city"]),
            wmo=str(data["wmo"]),
            source=str(data["source"]),
            latitude=float(data["latitude"]),
            longitude=float(data["longitude"]),
            timezone=float(data["timezone"]),
            elevation=float(data["elevation"]),
            url=str(data["url"]),
            ashrae_climate_zone=str(data["ashrae_climate_zone"]),
            heating_design_db_c=float(data["heating_design_db_c"]),
            cooling_design_db_c=float(data["cooling_design_db_c"]),
            hdd18=int(data["hdd18"]),
            cdd10=int(data["cdd10"]),
            design_conditions_source_wmo=str(source_wmo) if source_wmo is not None else None,
        )

    @property
    def display_name(self) -> str:
        """Human-readable station name with location context.

        Dots in the city name are replaced with spaces for readability.
        """
        name = self.city.replace(".", " ").replace("-", " ").strip()
        parts: list[str] = []
        if name:
            parts.append(name)
        if self.state:
            parts.append(self.state)
        parts.append(self.country)
        return ", ".join(parts)

    @property
    def filename_stem(self) -> str:
        """The canonical EPW filename stem derived from the download URL.

        Returns the ZIP filename without the ``.zip`` extension, e.g.
        ``"USA_IL_Chicago.Ohare.Intl.AP.725300_TMYx.2009-2023"``.
        """
        filename = self.url.rsplit("/", maxsplit=1)[-1]
        return filename.removesuffix(".zip")

    @property
    def dataset_variant(self) -> str:
        """Extract the TMYx dataset variant from the download URL.

        Returns a string like ``"TMYx"``, ``"TMYx.2007-2021"``, or
        ``"TMYx.2009-2023"``.
        """
        # Dataset variant is everything after the last underscore
        # e.g. "USA_CA_Marina.Muni.AP.690070_TMYx" -> "TMYx"
        # e.g. "USA_CA_Twentynine.Palms.SELF.690150_TMYx.2004-2018" -> "TMYx.2004-2018"
        parts = self.filename_stem.rsplit("_", maxsplit=1)
        if len(parts) == 2:
            return parts[1]
        return self.filename_stem

    @property
    def dataset_years(self) -> tuple[int, int] | None:
        """The first and last year of the dataset's period, or ``None`` when it names none.

        ``(2009, 2023)`` for ``"TMYx.2009-2023"``; ``None`` for a plain ``"TMYx"``.
        """
        match = _YEAR_RANGE.search(self.dataset_variant)
        if match is None:
            return None
        return int(match.group(1)), int(match.group(2))

    @property
    def station_key(self) -> str:
        """What every dataset of one physical station shares: the filename stem without its variant.

        ``"USA_IL_Chicago.Ohare.Intl.AP.725300"`` for each of that station's TMYx datasets.
        """
        parts = self.filename_stem.rsplit("_", maxsplit=1)
        return parts[0] if len(parts) == 2 else self.filename_stem

    @property
    def heating_design_db_f(self) -> float:
        """99% heating design dry-bulb temperature in °F."""
        return self.heating_design_db_c * 9 / 5 + 32

    @property
    def cooling_design_db_f(self) -> float:
        """1% cooling design dry-bulb temperature in °F."""
        return self.cooling_design_db_c * 9 / 5 + 32


def newest_first(stations: Iterable[WeatherStation]) -> tuple[WeatherStation, ...]:
    """*stations* ordered newest dataset first.

    Datasets with a year range sort by their last year, then their first, latest first;
    datasets without one (a plain ``"TMYx"``) follow them.
    """

    def recency(station: WeatherStation) -> tuple[int, int, int]:
        years = station.dataset_years
        return (0, 0, 0) if years is None else (1, years[1], years[0])

    return tuple(sorted(stations, key=recency, reverse=True))


@dataclass(frozen=True)
class SearchResult:
    """A text search result with relevance score: one physical station.

    ``station`` is the station's newest dataset; ``variants`` holds every dataset
    of it the search matched (the TMYx year ranges), newest first.
    """

    station: WeatherStation
    score: float
    """Relevance score from 0.0 to 1.0, higher is better."""
    match_field: str
    """Which field matched: ``"wmo"``, ``"name"``, ``"state"``, ``"country"``, or ``"filename"``."""
    variants: tuple[WeatherStation, ...] = field(default=())
    """Every dataset of this station, newest first; ``variants[0]`` is ``station``."""

    def __post_init__(self) -> None:
        # A result built without its variants still lists its station, so code that
        # iterates ``variants`` never drops it.
        if not self.variants:
            object.__setattr__(self, "variants", (self.station,))


@dataclass(frozen=True)
class SpatialResult:
    """A spatial proximity result with great-circle distance: one physical station.

    ``station`` is the station's newest dataset; ``variants`` holds its datasets
    (the TMYx year ranges) at this location, newest first. A station's datasets
    do not always share coordinates, and those lying more than a few kilometres
    from the rest come back as a separate result.
    """

    station: WeatherStation
    distance_km: float
    """Great-circle distance in kilometres to ``station``'s own coordinates."""
    variants: tuple[WeatherStation, ...] = field(default=())
    """This station's datasets at this location, newest first; ``variants[0]`` is ``station``."""

    def __post_init__(self) -> None:
        # A result built without its variants still lists its station, so code that
        # iterates ``variants`` never drops it.
        if not self.variants:
            object.__setattr__(self, "variants", (self.station,))
