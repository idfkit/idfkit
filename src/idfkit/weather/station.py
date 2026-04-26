"""Weather station data model and search result types."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


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
        source: Dataset source identifier (e.g. ``"TMYx.2009-2023"``).
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
    def heating_design_db_f(self) -> float:
        """99% heating design dry-bulb temperature in °F."""
        return self.heating_design_db_c * 9 / 5 + 32

    @property
    def cooling_design_db_f(self) -> float:
        """1% cooling design dry-bulb temperature in °F."""
        return self.cooling_design_db_c * 9 / 5 + 32


@dataclass(frozen=True)
class SearchResult:
    """A text search result with relevance score."""

    station: WeatherStation
    score: float
    """Relevance score from 0.0 to 1.0, higher is better."""
    match_field: str
    """Which field matched: ``"wmo"``, ``"name"``, ``"state"``, ``"country"``, or ``"filename"``."""


@dataclass(frozen=True)
class SpatialResult:
    """A spatial proximity result with great-circle distance."""

    station: WeatherStation
    distance_km: float
    """Great-circle distance in kilometres."""
