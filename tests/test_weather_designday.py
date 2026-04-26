"""Tests for idfkit.weather.designday."""

from __future__ import annotations

from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from idfkit.weather.designday import (
    DesignDayManager,
    DesignDayType,
    _classify_design_day,  # pyright: ignore[reportPrivateUsage]
    apply_ashrae_sizing,
)
from idfkit.weather.station import WeatherStation

_FIXTURES = Path(__file__).parent / "fixtures" / "weather"


def _make_station(
    *,
    wmo: str = "725300",
    latitude: float = 41.98,
    longitude: float = -87.92,
) -> WeatherStation:
    return WeatherStation(
        country="USA",
        state="IL",
        city="Chicago.Ohare.Intl.AP",
        wmo=wmo,
        source="TMYx.2009-2023",
        latitude=latitude,
        longitude=longitude,
        timezone=-6.0,
        elevation=201.0,
        url="https://example.com/USA_IL_Chicago.Ohare.Intl.AP.725300_TMYx.2009-2023.zip",
        ashrae_climate_zone="5A - Cool - Humid",
        heating_design_db_c=-17.4,
        cooling_design_db_c=32.5,
        hdd18=3454,
        cdd10=2103,
    )


class TestClassifyDesignDay:
    def test_heating_99_6(self) -> None:
        assert _classify_design_day("Chicago Ohare Intl AP Ann Htg 99.6% Condns DB") == DesignDayType.HEATING_99_6

    def test_heating_99(self) -> None:
        assert _classify_design_day("Chicago Ohare Intl AP Ann Htg 99% Condns DB") == DesignDayType.HEATING_99

    def test_cooling_db_04(self) -> None:
        assert _classify_design_day("Chicago Ohare Intl AP Ann Clg .4% Condns DB=>MWB") == DesignDayType.COOLING_DB_0_4

    def test_cooling_db_1(self) -> None:
        assert _classify_design_day("Chicago Ohare Intl AP Ann Clg 1% Condns DB=>MWB") == DesignDayType.COOLING_DB_1

    def test_cooling_db_2(self) -> None:
        assert _classify_design_day("Chicago Ohare Intl AP Ann Clg 2% Condns DB=>MWB") == DesignDayType.COOLING_DB_2

    def test_cooling_wb_1(self) -> None:
        assert _classify_design_day("Chicago Ohare Intl AP Ann Clg 1% Condns WB=>MDB") == DesignDayType.COOLING_WB_1

    def test_cooling_enth_04(self) -> None:
        assert (
            _classify_design_day("Chicago Ohare Intl AP Ann Clg .4% Condns Enth=>MDB") == DesignDayType.COOLING_ENTH_0_4
        )

    def test_cooling_enth_1(self) -> None:
        assert _classify_design_day("Chicago Ohare Intl AP Ann Clg 1% Condns Enth=>MDB") == DesignDayType.COOLING_ENTH_1

    def test_dehumid_1(self) -> None:
        assert _classify_design_day("Chicago Ohare Intl AP Ann Clg 1% Condns DP=>MDB") == DesignDayType.DEHUMID_1

    def test_humidification_99_6(self) -> None:
        assert (
            _classify_design_day("Chicago Ohare Intl AP Ann Hum_n 99.6% Condns DP=>MCDB")
            == DesignDayType.HUMIDIFICATION_99_6
        )

    def test_humidification_99(self) -> None:
        assert (
            _classify_design_day("Chicago Ohare Intl AP Ann Hum_n 99% Condns DP=>MCDB")
            == DesignDayType.HUMIDIFICATION_99
        )

    def test_htg_wind_99_6(self) -> None:
        assert (
            _classify_design_day("Chicago Ohare Intl AP Ann Htg Wind 99.6% Condns WS=>MCDB")
            == DesignDayType.HTG_WIND_99_6
        )

    def test_htg_wind_99(self) -> None:
        assert (
            _classify_design_day("Chicago Ohare Intl AP Ann Htg Wind 99% Condns WS=>MCDB") == DesignDayType.HTG_WIND_99
        )

    def test_wind_04(self) -> None:
        assert _classify_design_day("Coldest Month WS/MDB 0.4%") == DesignDayType.WIND_0_4

    def test_wind_1(self) -> None:
        assert _classify_design_day("Coldest Month WS/MDB 1%") == DesignDayType.WIND_1

    def test_unknown_returns_none(self) -> None:
        assert _classify_design_day("Some Random Design Day Name") is None

    def test_monthly_not_classified(self) -> None:
        assert _classify_design_day("Chicago Ohare Intl AP January .4% Condns DB=>MCWB") is None
        assert _classify_design_day("Chicago Ohare Intl AP July .4% Condns WB=>MCDB") is None


class TestDesignDayManager:
    def test_parse_sample_ddy(self) -> None:
        ddm = DesignDayManager(_FIXTURES / "sample.ddy")
        assert len(ddm.all_design_days) == 11

    def test_annual_filter(self) -> None:
        ddm = DesignDayManager(_FIXTURES / "sample.ddy")
        assert len(ddm.annual) == 9

    def test_monthly_filter(self) -> None:
        ddm = DesignDayManager(_FIXTURES / "sample.ddy")
        assert len(ddm.monthly) == 2
        names = [dd.name for dd in ddm.monthly]
        assert any("January" in n for n in names)
        assert any("July" in n for n in names)

    def test_heating_filter(self) -> None:
        ddm = DesignDayManager(_FIXTURES / "sample.ddy")
        assert len(ddm.heating) == 2

    def test_cooling_filter(self) -> None:
        ddm = DesignDayManager(_FIXTURES / "sample.ddy")
        assert len(ddm.cooling) == 5

    def test_location(self) -> None:
        ddm = DesignDayManager(_FIXTURES / "sample.ddy")
        assert ddm.location is not None
        assert ddm.location.name == "Chicago Ohare Intl AP"

    def test_get_specific_type(self) -> None:
        ddm = DesignDayManager(_FIXTURES / "sample.ddy")
        dd = ddm.get(DesignDayType.HEATING_99_6)
        assert dd is not None
        assert "99.6%" in dd.name

    def test_get_enthalpy(self) -> None:
        ddm = DesignDayManager(_FIXTURES / "sample.ddy")
        dd = ddm.get(DesignDayType.COOLING_ENTH_1)
        assert dd is not None
        assert "Enth" in dd.name

    def test_get_humidification(self) -> None:
        ddm = DesignDayManager(_FIXTURES / "sample.ddy")
        dd = ddm.get(DesignDayType.HUMIDIFICATION_99_6)
        assert dd is not None
        assert "Hum_n" in dd.name

    def test_get_htg_wind(self) -> None:
        ddm = DesignDayManager(_FIXTURES / "sample.ddy")
        dd = ddm.get(DesignDayType.HTG_WIND_99_6)
        assert dd is not None
        assert "Htg Wind" in dd.name

    def test_get_missing_type_returns_none(self) -> None:
        ddm = DesignDayManager(_FIXTURES / "sample.ddy")
        assert ddm.get(DesignDayType.WIND_0_4) is None

    def test_empty_ddy(self) -> None:
        ddm = DesignDayManager(_FIXTURES / "empty.ddy")
        assert len(ddm.all_design_days) == 0
        assert ddm.location is not None

    def test_parse_no_location_no_design_days(self, tmp_path: Path) -> None:
        """DDY with no Site:Location and no SizingPeriod:DesignDay (lines 148->154, 150->154)."""
        ddy = tmp_path / "bare.ddy"
        ddy.write_text("\n Version,\n    25.2;\n")
        ddm = DesignDayManager(ddy)
        assert ddm.location is None
        assert ddm.all_design_days == []

    def test_summary(self) -> None:
        ddm = DesignDayManager(_FIXTURES / "sample.ddy")
        summary = ddm.summary()
        assert "Chicago Ohare Intl AP" in summary
        assert "Design days found: 11" in summary
        assert "Annual (classified): 9" in summary
        assert "Monthly: 2" in summary

    def test_summary_no_location(self, tmp_path: Path) -> None:
        """Summary without location (line 395->397)."""
        ddy = tmp_path / "nosite.ddy"
        ddy.write_text("\n Version,\n    25.2;\n")
        ddm = DesignDayManager(ddy)
        summary = ddm.summary()
        assert "Location:" not in summary

    def test_summary_no_monthly(self, tmp_path: Path) -> None:
        """Summary omits monthly line when no monthly design days (line 399->401)."""
        ddy = tmp_path / "annual_only.ddy"
        ddy.write_text(
            "\n Version,\n    25.2;\n\n"
            " SizingPeriod:DesignDay,\n"
            "    Test Ann Htg 99.6% Condns DB,\n"
            "    1, 21, WinterDesignDay, -20.6, 0.0, DefaultMultipliers,\n"
            "    , Wetbulb, -20.6, , , , , 98934., 4.9, 270,\n"
            "    No, No, No, SummerOrWinter, , , , , 0.00;\n"
        )
        ddm = DesignDayManager(ddy)
        summary = ddm.summary()
        assert "Monthly:" not in summary

    def test_from_station(self) -> None:
        """from_station downloads DDY and creates manager (lines 176-184)."""
        station = _make_station()
        mock_downloader = MagicMock()
        mock_downloader.get_ddy.return_value = _FIXTURES / "sample.ddy"

        with patch("idfkit.weather.download.WeatherDownloader", return_value=mock_downloader):
            ddm = DesignDayManager.from_station(station)

        assert len(ddm.all_design_days) == 11
        mock_downloader.get_ddy.assert_called_once_with(station)


class TestApplyToModel:
    @pytest.fixture()
    def model(self) -> object:
        from idfkit import new_document

        return new_document()

    def test_apply_default(self, model: object) -> None:
        from idfkit.document import IDFDocument

        assert isinstance(model, IDFDocument)
        ddm = DesignDayManager(_FIXTURES / "sample.ddy")
        names = ddm.apply_to_model(model)
        assert len(names) == 2
        assert any("99.6%" in n for n in names)
        assert any("1% Condns DB" in n for n in names)
        assert "SizingPeriod:DesignDay" in model
        assert len(list(model["SizingPeriod:DesignDay"])) == 2

    def test_apply_with_wet_bulb(self, model: object) -> None:
        from idfkit.document import IDFDocument

        assert isinstance(model, IDFDocument)
        ddm = DesignDayManager(_FIXTURES / "sample.ddy")
        names = ddm.apply_to_model(model, cooling="1%", include_wet_bulb=True)
        assert len(names) == 3

    def test_apply_with_enthalpy(self, model: object) -> None:
        from idfkit.document import IDFDocument

        assert isinstance(model, IDFDocument)
        ddm = DesignDayManager(_FIXTURES / "sample.ddy")
        names = ddm.apply_to_model(model, cooling="1%", include_enthalpy=True)
        assert len(names) == 3
        assert any("Enth" in n for n in names)

    def test_apply_with_dehumidification(self, model: object) -> None:
        """Include dehumidification design days (lines 316-318)."""
        from idfkit.document import IDFDocument

        assert isinstance(model, IDFDocument)
        ddm = DesignDayManager(_FIXTURES / "sample.ddy")
        names = ddm.apply_to_model(model, cooling="1%", include_dehumidification=True)
        assert len(names) == 3
        assert any("DP" in n for n in names)

    def test_apply_with_wind(self, model: object) -> None:
        from idfkit.document import IDFDocument

        assert isinstance(model, IDFDocument)
        ddm = DesignDayManager(_FIXTURES / "sample.ddy")
        names = ddm.apply_to_model(model, cooling="1%", include_wind=True)
        assert len(names) == 3
        assert any("Htg Wind" in n for n in names)

    def test_apply_both_heating(self, model: object) -> None:
        """Both heating percentiles (line 292->294)."""
        from idfkit.document import IDFDocument

        assert isinstance(model, IDFDocument)
        ddm = DesignDayManager(_FIXTURES / "sample.ddy")
        names = ddm.apply_to_model(model, heating="both", cooling="1%")
        assert len(names) == 3

    def test_apply_heating_99(self, model: object) -> None:
        """Single 99% heating percentile yields exactly 2 design days (heating 99% DB + cooling 1% DB)."""
        from idfkit.document import IDFDocument

        assert isinstance(model, IDFDocument)
        ddm = DesignDayManager(_FIXTURES / "sample.ddy")
        names = ddm.apply_to_model(model, heating="99%", cooling="1%")
        assert len(names) == 2
        assert any("99% Condns DB" in n for n in names)
        assert any("1% Condns DB" in n for n in names)

    def test_apply_updates_location(self, model: object) -> None:
        from idfkit.document import IDFDocument

        assert isinstance(model, IDFDocument)
        ddm = DesignDayManager(_FIXTURES / "sample.ddy")
        ddm.apply_to_model(model)
        assert "Site:Location" in model
        loc = next(iter(model["Site:Location"]))
        assert loc.name == "Chicago Ohare Intl AP"

    def test_apply_replaces_existing_location(self, model: object) -> None:
        """Replace existing Site:Location (lines 383->389)."""
        from idfkit.document import IDFDocument

        assert isinstance(model, IDFDocument)
        # Add a dummy location first
        model.newidfobject("Site:Location", Name="Old Location")
        ddm = DesignDayManager(_FIXTURES / "sample.ddy")
        ddm.apply_to_model(model)
        locs = list(model["Site:Location"])
        assert len(locs) == 1
        assert locs[0].name == "Chicago Ohare Intl AP"

    def test_apply_no_update_location(self, model: object) -> None:
        """update_location=False should skip location injection (line 383->389)."""
        from idfkit.document import IDFDocument

        assert isinstance(model, IDFDocument)
        ddm = DesignDayManager(_FIXTURES / "sample.ddy")
        ddm.apply_to_model(model, update_location=False)
        assert "Site:Location" not in model

    def test_apply_replace_existing(self, model: object) -> None:
        from idfkit.document import IDFDocument

        assert isinstance(model, IDFDocument)
        ddm = DesignDayManager(_FIXTURES / "sample.ddy")
        ddm.apply_to_model(model)
        ddm.apply_to_model(model)
        assert len(list(model["SizingPeriod:DesignDay"])) == 2

    def test_apply_no_replace_existing(self, model: object) -> None:
        """replace_existing=False should not remove existing design days.

        Note: Cannot add the exact same named objects twice (DuplicateObjectError),
        so we apply different selections to verify accumulation.
        """
        from idfkit.document import IDFDocument

        assert isinstance(model, IDFDocument)
        ddm = DesignDayManager(_FIXTURES / "sample.ddy")
        # First: heating 99.6% + cooling 1% DB = 2
        ddm.apply_to_model(model, heating="99.6%", cooling="1%")
        assert len(list(model["SizingPeriod:DesignDay"])) == 2
        # Second: add 99% heating (different name) without replacing
        ddm.apply_to_model(model, heating="99%", cooling="0.4%", replace_existing=False)
        # Should now have 2 + 2 = 4 (99%, 0.4% are different names)
        assert len(list(model["SizingPeriod:DesignDay"])) == 4


class TestNoDesignDaysError:
    def test_raise_if_empty_does_not_raise_when_design_days_present(self) -> None:
        ddm = DesignDayManager(_FIXTURES / "sample.ddy")
        ddm.raise_if_empty()

    def test_raise_if_empty_raises_for_empty_ddy(self) -> None:
        from idfkit.exceptions import NoDesignDaysError

        ddm = DesignDayManager(_FIXTURES / "empty.ddy")
        with pytest.raises(NoDesignDaysError) as exc_info:
            ddm.raise_if_empty()

        error = exc_info.value
        assert "no SizingPeriod:DesignDay objects" in str(error)
        assert error.ddy_path is not None
        assert "empty.ddy" in error.ddy_path

    def test_error_includes_station_name_from_location(self) -> None:
        from idfkit.exceptions import NoDesignDaysError

        ddm = DesignDayManager(_FIXTURES / "empty.ddy")
        with pytest.raises(NoDesignDaysError) as exc_info:
            ddm.raise_if_empty()

        error = exc_info.value
        assert error.station_name is not None or error.ddy_path is not None

    def test_station_name_from_station_object(self, tmp_path: Path) -> None:
        """When no Site:Location, station name comes from WeatherStation (lines 245-246)."""
        from idfkit.exceptions import NoDesignDaysError

        ddy = tmp_path / "bare.ddy"
        ddy.write_text("\n Version,\n    25.2;\n")
        station = _make_station()
        ddm = DesignDayManager(ddy, station=station)
        with pytest.raises(NoDesignDaysError) as exc_info:
            ddm.raise_if_empty()

        error = exc_info.value
        assert error.station_name == station.display_name

    def test_nearby_suggestions_with_station(self, tmp_path: Path) -> None:
        """When station is set, nearby suggestions are looked up (lines 250-267)."""
        from idfkit.exceptions import NoDesignDaysError
        from idfkit.weather.index import StationIndex
        from idfkit.weather.station import SpatialResult

        ddy = tmp_path / "bare.ddy"
        ddy.write_text("\n Version,\n    25.2;\n")
        station = _make_station(wmo="999999")

        # Create mock spatial results with 7 nearby stations (self + 6 others)
        # so the loop hits len(nearby) >= 5 and triggers `break` on line 265
        nearby_stations = [
            SpatialResult(station=station, distance_km=0.0),  # self — skipped
        ]
        for i in range(6):
            nearby_stations.append(SpatialResult(station=_make_station(wmo=str(100000 + i)), distance_km=float(10 + i)))

        mock_index = MagicMock(spec=StationIndex)
        mock_index.nearest.return_value = nearby_stations

        with patch("idfkit.weather.index.StationIndex") as mock_cls:
            mock_cls.load.return_value = mock_index
            ddm = DesignDayManager(ddy, station=station)
            with pytest.raises(NoDesignDaysError) as exc_info:
                ddm.raise_if_empty()

        error = exc_info.value
        assert len(error.nearby_suggestions) == 5  # capped at 5

    def test_nearby_suggestions_handles_load_failure(self, tmp_path: Path) -> None:
        """If StationIndex.load() fails, nearby suggestions are empty (line 266)."""
        from idfkit.exceptions import NoDesignDaysError

        ddy = tmp_path / "bare.ddy"
        ddy.write_text("\n Version,\n    25.2;\n")
        station = _make_station()

        with patch("idfkit.weather.index.StationIndex") as mock_cls:
            mock_cls.load.side_effect = FileNotFoundError("no index")
            ddm = DesignDayManager(ddy, station=station)
            with pytest.raises(NoDesignDaysError) as exc_info:
                ddm.raise_if_empty()

        assert exc_info.value.nearby_suggestions == []

    def test_nearby_suggestions_empty_when_no_station(self) -> None:
        from idfkit.exceptions import NoDesignDaysError

        ddm = DesignDayManager(_FIXTURES / "empty.ddy")
        with pytest.raises(NoDesignDaysError) as exc_info:
            ddm.raise_if_empty()

        error = exc_info.value
        assert error.nearby_suggestions == []

    def test_error_message_includes_ddy_path(self) -> None:
        from idfkit.exceptions import NoDesignDaysError

        ddm = DesignDayManager(_FIXTURES / "empty.ddy")
        with pytest.raises(NoDesignDaysError) as exc_info:
            ddm.raise_if_empty()

        error_msg = str(exc_info.value)
        assert "empty.ddy" in error_msg or "no SizingPeriod:DesignDay" in error_msg


class TestApplyAshraeSizing:
    def test_general_preset(self) -> None:
        """apply_ashrae_sizing with general preset (lines 438-442)."""
        from idfkit import new_document

        model = new_document()
        station = _make_station()

        mock_downloader = MagicMock()
        mock_downloader.get_ddy.return_value = _FIXTURES / "sample.ddy"

        with patch("idfkit.weather.download.WeatherDownloader", return_value=mock_downloader):
            names = apply_ashrae_sizing(model, station, standard="general")

        assert len(names) == 2
        assert any("99.6%" in n for n in names)
        assert any("Clg" in n and "DB" in n for n in names)

    def test_90_1_preset(self) -> None:
        """apply_ashrae_sizing with 90.1 preset (lines 440-441)."""
        from idfkit import new_document

        model = new_document()
        station = _make_station()

        mock_downloader = MagicMock()
        mock_downloader.get_ddy.return_value = _FIXTURES / "sample.ddy"

        with patch("idfkit.weather.download.WeatherDownloader", return_value=mock_downloader):
            names = apply_ashrae_sizing(model, station, standard="90.1")

        assert len(names) == 3
        assert any("99.6%" in n for n in names)
        assert any("WB" in n for n in names)

    def test_raises_for_empty_ddy(self, tmp_path: Path) -> None:
        """apply_ashrae_sizing raises NoDesignDaysError for empty DDY."""
        from idfkit import new_document
        from idfkit.exceptions import NoDesignDaysError

        model = new_document()
        station = _make_station()

        ddy = tmp_path / "empty.ddy"
        ddy.write_text("\n Version,\n    25.2;\n")

        mock_downloader = MagicMock()
        mock_downloader.get_ddy.return_value = ddy

        with (
            patch("idfkit.weather.download.WeatherDownloader", return_value=mock_downloader),
            pytest.raises(NoDesignDaysError),
        ):
            apply_ashrae_sizing(model, station)
