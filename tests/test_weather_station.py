"""Tests for idfkit.weather.station."""

from __future__ import annotations

import pytest

from idfkit.weather.station import SearchResult, SpatialResult, WeatherStation


def _make_station(**kwargs: object) -> WeatherStation:
    defaults: dict[str, object] = {
        "country": "USA",
        "state": "IL",
        "city": "Chicago.Ohare.Intl.AP",
        "wmo": "725300",
        "source": "TMYx.2009-2023",
        "latitude": 41.98,
        "longitude": -87.92,
        "timezone": -6.0,
        "elevation": 201.0,
        "url": "https://climate.onebuilding.org/WMO_Region_4/USA_IL_Chicago.Ohare.Intl.AP.725300_TMYx.2009-2023.zip",
        "ashrae_climate_zone": "5A - Cool - Humid",
        "heating_design_db_c": -17.4,
        "cooling_design_db_c": 32.5,
        "hdd18": 3454,
        "cdd10": 2103,
    }
    defaults.update(kwargs)
    return WeatherStation(**defaults)  # type: ignore[arg-type]


class TestWeatherStation:
    def test_display_name(self) -> None:
        s = _make_station()
        assert s.display_name == "Chicago Ohare Intl AP, IL, USA"

    def test_display_name_no_state(self) -> None:
        s = _make_station(state="")
        assert s.display_name == "Chicago Ohare Intl AP, USA"

    def test_display_name_empty_city_skips_name(self) -> None:
        """81->83: city is empty after stripping → name is falsy, not appended."""
        s = _make_station(city="")
        assert s.display_name == "IL, USA"

    def test_dataset_variant_with_year_range(self) -> None:
        s = _make_station()
        assert s.dataset_variant == "TMYx.2009-2023"

    def test_dataset_variant_without_year_range(self) -> None:
        s = _make_station(
            url="https://climate.onebuilding.org/WMO_Region_4/USA_IL_Chicago.Ohare.Intl.AP.725300_TMYx.zip"
        )
        assert s.dataset_variant == "TMYx"

    def test_frozen(self) -> None:
        s = _make_station()
        with pytest.raises(AttributeError):
            s.wmo = "999999"  # type: ignore[misc]


class TestSerialization:
    def test_to_dict_round_trip(self) -> None:
        s = _make_station()
        d = s.to_dict()
        restored = WeatherStation.from_dict(d)
        assert restored == s

    def test_to_dict_keys(self) -> None:
        s = _make_station()
        d = s.to_dict()
        expected_keys = {
            "country",
            "state",
            "city",
            "wmo",
            "source",
            "latitude",
            "longitude",
            "timezone",
            "elevation",
            "url",
            "ashrae_climate_zone",
            "heating_design_db_c",
            "cooling_design_db_c",
            "hdd18",
            "cdd10",
            "design_conditions_source_wmo",
        }
        assert set(d.keys()) == expected_keys

    def test_from_dict_type_coercion(self) -> None:
        """Ensure from_dict coerces string values to correct types."""
        d = {
            "country": "USA",
            "state": "IL",
            "city": "Test",
            "wmo": "725300",
            "source": "TMYx",
            "latitude": "41.98",
            "longitude": "-87.92",
            "timezone": "-6.0",
            "elevation": "201.0",
            "url": "https://example.com/test.zip",
            "ashrae_climate_zone": "5A - Cool - Humid",
            "heating_design_db_c": "-17.4",
            "cooling_design_db_c": "32.5",
            "hdd18": "3454",
            "cdd10": "2103",
        }
        s = WeatherStation.from_dict(d)  # type: ignore[arg-type]
        assert isinstance(s.wmo, str)
        assert isinstance(s.latitude, float)
        assert s.wmo == "725300"
        assert s.latitude == 41.98
        assert isinstance(s.heating_design_db_c, float)
        assert s.heating_design_db_c == -17.4
        assert isinstance(s.hdd18, int)
        assert s.hdd18 == 3454

    def test_alternate_wmo_round_trip(self) -> None:
        """The optional alternate-WMO field survives a serialization round-trip."""
        s = _make_station(design_conditions_source_wmo="911900")
        restored = WeatherStation.from_dict(s.to_dict())
        assert restored.design_conditions_source_wmo == "911900"

    def test_fahrenheit_properties(self) -> None:
        s = _make_station(heating_design_db_c=0.0, cooling_design_db_c=100.0)
        assert s.heating_design_db_f == pytest.approx(32.0)
        assert s.cooling_design_db_f == pytest.approx(212.0)


class TestFilenameStem:
    def test_us_station_with_year_range(self) -> None:
        s = _make_station()
        assert s.filename_stem == "USA_IL_Chicago.Ohare.Intl.AP.725300_TMYx.2009-2023"

    def test_us_station_without_year_range(self) -> None:
        s = _make_station(
            url="https://climate.onebuilding.org/WMO_Region_4/USA_IL_Chicago.Ohare.Intl.AP.725300_TMYx.zip"
        )
        assert s.filename_stem == "USA_IL_Chicago.Ohare.Intl.AP.725300_TMYx"

    def test_non_us_station_with_leading_zero_wmo(self) -> None:
        s = _make_station(
            country="GBR",
            state="",
            city="London.Heathrow.AP",
            wmo="37720",
            url="https://climate.onebuilding.org/WMO_Region_6/GBR_London.Heathrow.AP.037720_TMYx.zip",
        )
        assert s.filename_stem == "GBR_London.Heathrow.AP.037720_TMYx"


class TestSearchResult:
    def test_fields(self) -> None:
        s = _make_station()
        r = SearchResult(station=s, score=0.95, match_field="name")
        assert r.score == 0.95
        assert r.match_field == "name"


class TestSpatialResult:
    def test_fields(self) -> None:
        s = _make_station()
        r = SpatialResult(station=s, distance_km=12.5)
        assert r.distance_km == 12.5


class TestDatasetVariantFallback:
    def test_no_underscore_in_stem_returns_full_stem(self) -> None:
        """When the filename stem has no underscore, return the full stem (line 111)."""
        s = _make_station(url="https://climate.onebuilding.org/test/noseparator.zip")
        assert s.dataset_variant == "noseparator"
