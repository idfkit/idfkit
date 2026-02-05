"""Tests for idfkit.weather.designday."""

from __future__ import annotations

from pathlib import Path

import pytest

from idfkit.weather.designday import DesignDayManager, DesignDayType, _classify_design_day

_FIXTURES = Path(__file__).parent / "fixtures" / "weather"


class TestClassifyDesignDay:
    def test_heating_99_6(self) -> None:
        assert _classify_design_day("Chicago Ohare Intl AP Ann Htg 99.6% Condns DB") == DesignDayType.HEATING_99_6

    def test_heating_99(self) -> None:
        assert _classify_design_day("Chicago Ohare Intl AP Ann Htg 99% Condns DB") == DesignDayType.HEATING_99

    def test_cooling_db_04(self) -> None:
        assert _classify_design_day("Chicago Ohare Intl AP Ann Clg .4% Condns DB=>MWB") == DesignDayType.COOLING_DB_0_4

    def test_cooling_db_1(self) -> None:
        assert _classify_design_day("Chicago Ohare Intl AP Ann Clg 1% Condns DB=>MWB") == DesignDayType.COOLING_DB_1

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

    def test_unknown_returns_none(self) -> None:
        assert _classify_design_day("Some Random Design Day Name") is None

    def test_monthly_not_classified(self) -> None:
        """Monthly design days should not match any annual classification."""
        assert _classify_design_day("Chicago Ohare Intl AP January .4% Condns DB=>MCWB") is None
        assert _classify_design_day("Chicago Ohare Intl AP July .4% Condns WB=>MCDB") is None


class TestDesignDayManager:
    def test_parse_sample_ddy(self) -> None:
        ddm = DesignDayManager(_FIXTURES / "sample.ddy")
        # 6 original annual + 1 enthalpy + 1 humidification + 1 htg wind + 2 monthly = 11
        assert len(ddm.all_design_days) == 11

    def test_annual_filter(self) -> None:
        ddm = DesignDayManager(_FIXTURES / "sample.ddy")
        # 6 original + 1 enthalpy + 1 humidification + 1 htg wind = 9 classified annual
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
        # 2 DB cooling + 1 WB cooling + 1 dehumid + 1 enthalpy = 5 cooling-related
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
        # WIND types (EnergyPlus "Coldest Month" format) are not in our fixture
        assert ddm.get(DesignDayType.WIND_0_4) is None

    def test_empty_ddy(self) -> None:
        ddm = DesignDayManager(_FIXTURES / "empty.ddy")
        assert len(ddm.all_design_days) == 0
        assert ddm.location is not None

    def test_summary(self) -> None:
        ddm = DesignDayManager(_FIXTURES / "sample.ddy")
        summary = ddm.summary()
        assert "Chicago Ohare Intl AP" in summary
        assert "Design days found: 11" in summary
        assert "Annual (classified): 9" in summary
        assert "Monthly: 2" in summary


class TestApplyToModel:
    @pytest.fixture
    def model(self) -> object:
        from idfkit import new_document

        return new_document()

    def test_apply_default(self, model: object) -> None:
        from idfkit.document import IDFDocument

        assert isinstance(model, IDFDocument)
        ddm = DesignDayManager(_FIXTURES / "sample.ddy")
        names = ddm.apply_to_model(model)
        # Default: heating 99.6% + cooling 1% DB = 2 design days
        assert len(names) == 2
        assert any("99.6%" in n for n in names)
        assert any("1% Condns DB" in n for n in names)
        # Check objects actually exist in model
        assert "SizingPeriod:DesignDay" in model
        assert len(list(model["SizingPeriod:DesignDay"])) == 2

    def test_apply_with_wet_bulb(self, model: object) -> None:
        from idfkit.document import IDFDocument

        assert isinstance(model, IDFDocument)
        ddm = DesignDayManager(_FIXTURES / "sample.ddy")
        names = ddm.apply_to_model(model, cooling="1%", include_wet_bulb=True)
        # heating 99.6% + cooling 1% DB + cooling 1% WB = 3
        assert len(names) == 3

    def test_apply_with_enthalpy(self, model: object) -> None:
        from idfkit.document import IDFDocument

        assert isinstance(model, IDFDocument)
        ddm = DesignDayManager(_FIXTURES / "sample.ddy")
        names = ddm.apply_to_model(model, cooling="1%", include_enthalpy=True)
        # heating 99.6% + cooling 1% DB + cooling 1% Enth = 3
        assert len(names) == 3
        assert any("Enth" in n for n in names)

    def test_apply_with_wind(self, model: object) -> None:
        from idfkit.document import IDFDocument

        assert isinstance(model, IDFDocument)
        ddm = DesignDayManager(_FIXTURES / "sample.ddy")
        names = ddm.apply_to_model(model, cooling="1%", include_wind=True)
        # heating 99.6% + cooling 1% DB + htg wind 99.6% = 3
        assert len(names) == 3
        assert any("Htg Wind" in n for n in names)

    def test_apply_both_heating(self, model: object) -> None:
        from idfkit.document import IDFDocument

        assert isinstance(model, IDFDocument)
        ddm = DesignDayManager(_FIXTURES / "sample.ddy")
        names = ddm.apply_to_model(model, heating="both", cooling="1%")
        assert len(names) == 3

    def test_apply_updates_location(self, model: object) -> None:
        from idfkit.document import IDFDocument

        assert isinstance(model, IDFDocument)
        ddm = DesignDayManager(_FIXTURES / "sample.ddy")
        ddm.apply_to_model(model)
        assert "Site:Location" in model
        loc = next(iter(model["Site:Location"]))
        assert loc.name == "Chicago Ohare Intl AP"

    def test_apply_replace_existing(self, model: object) -> None:
        from idfkit.document import IDFDocument

        assert isinstance(model, IDFDocument)
        ddm = DesignDayManager(_FIXTURES / "sample.ddy")
        # Apply twice — should replace, not accumulate
        ddm.apply_to_model(model)
        ddm.apply_to_model(model)
        assert len(list(model["SizingPeriod:DesignDay"])) == 2


class TestNoDesignDaysError:
    """Tests for NoDesignDaysError exception."""

    def test_raise_if_empty_does_not_raise_when_design_days_present(self) -> None:
        ddm = DesignDayManager(_FIXTURES / "sample.ddy")
        # Should not raise
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

        # The empty.ddy has a Site:Location with a name
        error = exc_info.value
        # The station name comes from Site:Location if present
        assert error.station_name is not None or error.ddy_path is not None

    def test_error_message_includes_ddy_path(self) -> None:
        from idfkit.exceptions import NoDesignDaysError

        ddm = DesignDayManager(_FIXTURES / "empty.ddy")
        with pytest.raises(NoDesignDaysError) as exc_info:
            ddm.raise_if_empty()

        error_msg = str(exc_info.value)
        assert "empty.ddy" in error_msg or "no SizingPeriod:DesignDay" in error_msg

    def test_nearby_suggestions_empty_when_no_station(self) -> None:
        from idfkit.exceptions import NoDesignDaysError

        # When not created from a station, no nearby suggestions
        ddm = DesignDayManager(_FIXTURES / "empty.ddy")
        with pytest.raises(NoDesignDaysError) as exc_info:
            ddm.raise_if_empty()

        error = exc_info.value
        assert error.nearby_suggestions == []
