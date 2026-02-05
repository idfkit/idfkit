"""Weather station data model and search result types."""

from __future__ import annotations

from dataclasses import dataclass


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
        source: Dataset source identifier (e.g. ``"SRC-TMYx"``).
        latitude: Decimal degrees, north positive.
        longitude: Decimal degrees, east positive.
        timezone: Hours offset from GMT (e.g. ``-8.0``).
        elevation: Meters above sea level.
        url: Full download URL for the ZIP archive.
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

    def to_dict(self) -> dict[str, str | float]:
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
        }

    @classmethod
    def from_dict(cls, data: dict[str, str | float]) -> WeatherStation:
        """Deserialize from a plain dictionary."""
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
        )

    @property
    def display_name(self) -> str:
        """Human-readable station name with location context.

        Dots in the city name are replaced with spaces for readability.
        """
        name = self.city.replace(".", " ").replace("-", " ")
        parts = [name]
        if self.state:
            parts.append(self.state)
        parts.append(self.country)
        return ", ".join(parts)

    @property
    def dataset_variant(self) -> str:
        """Extract the TMYx dataset variant from the download URL.

        Returns a string like ``"TMYx"``, ``"TMYx.2007-2021"``, or
        ``"TMYx.2009-2023"``.
        """
        # URL ends with e.g. ...722950_TMYx.2009-2023.zip
        filename = self.url.rsplit("/", maxsplit=1)[-1]
        # Remove .zip extension
        stem = filename.removesuffix(".zip")
        # Dataset variant is everything after the last underscore
        # e.g. "USA_CA_Marina.Muni.AP.690070_TMYx" -> "TMYx"
        # e.g. "USA_CA_Twentynine.Palms.SELF.690150_TMYx.2004-2018" -> "TMYx.2004-2018"
        parts = stem.rsplit("_", maxsplit=1)
        if len(parts) == 2:
            return parts[1]
        return stem


@dataclass(frozen=True)
class SearchResult:
    """A text search result with relevance score."""

    station: WeatherStation
    score: float
    """Relevance score from 0.0 to 1.0, higher is better."""
    match_field: str
    """Which field matched: ``"wmo"``, ``"name"``, ``"state"``, ``"country"``."""


@dataclass(frozen=True)
class SpatialResult:
    """A spatial proximity result with great-circle distance."""

    station: WeatherStation
    distance_km: float
    """Great-circle distance in kilometres."""
