"""Tests for the ESO/MTR parser.

The fixtures (``sample.eso``, ``sample.mtr``, ``sample_truncated.eso``) are real
EnergyPlus output, produced by ``tests/fixtures/simulation/generate_eso_fixtures.py``
from a two-day run of the bundled ``1ZoneUncontrolled.idf`` example. Expected
values below were cross-checked against the matching ``.sql`` output.
"""

from __future__ import annotations

import dataclasses
from datetime import datetime
from pathlib import Path

import pytest

from idfkit.simulation.parsers.eso import ESOColumn, ESOEnvironment, ESOResult, ESOVariable

FIXTURES = Path(__file__).parent / "fixtures" / "simulation"
SAMPLE_ESO = FIXTURES / "sample.eso"
SAMPLE_MTR = FIXTURES / "sample.mtr"
SAMPLE_TRUNCATED = FIXTURES / "sample_truncated.eso"

# A representative hourly site variable present in the run period (last env).
_OAT = "Site Outdoor Air Drybulb Temperature"
_OAT_FIRST5 = (-4.5, -3.0, -3.625, -2.75, -2.0)


@pytest.fixture
def eso() -> ESOResult:
    return ESOResult.from_file(SAMPLE_ESO)


class TestDictionary:
    """Parsing of the data-dictionary section."""

    def test_program_version(self, eso: ESOResult) -> None:
        assert eso.program_version.startswith("Program Version,EnergyPlus")

    def test_variable_count(self, eso: ESOResult) -> None:
        assert len(eso.variables) == 169

    def test_markers_excluded(self, eso: ESOResult) -> None:
        # Reserved time/environment markers (ids 1-6) are not user variables.
        assert all(v.report_id >= 7 for v in eso.variables)

    def test_get_variable_metadata(self, eso: ESOResult) -> None:
        var = eso.get_variable(_OAT, "Environment")
        assert var is not None
        assert var.units == "C"
        assert var.frequency == "Hourly"
        assert var.num_values == 1

    def test_daily_variable_num_values(self, eso: ESOResult) -> None:
        var = eso.get_variable("Site Daylight Saving Time Status")
        assert var is not None
        assert var.frequency == "Daily"
        # Daily aggregated records carry value + min/max with their times.
        assert var.num_values == 7

    def test_monthly_variable(self, eso: ESOResult) -> None:
        var = eso.get_variable("Other Equipment Total Heating Energy", "TEST 352A")
        assert var is not None
        assert var.frequency == "Monthly"


class TestEnvironments:
    """Environment-period parsing."""

    def test_environment_count(self, eso: ESOResult) -> None:
        assert len(eso.environments) == 3

    def test_environment_titles(self, eso: ESOResult) -> None:
        titles = [e.title for e in eso.environments]
        assert titles[-1] == "RUN PERIOD 1"
        assert "ANN HTG 99% CONDNS DB" in titles[0]

    def test_environment_site_data(self, eso: ESOResult) -> None:
        env = eso.environments[-1]
        assert env.index == 2
        assert env.latitude == pytest.approx(39.74)
        assert env.elevation == pytest.approx(1829.0)


class TestGetColumn:
    """Lazy, targeted variable extraction."""

    def test_default_returns_last_environment(self, eso: ESOResult) -> None:
        col = eso.get_column(_OAT)
        assert col is not None
        assert col.environment_index == 2  # the run period
        assert len(col.values) == 48  # two days, hourly

    def test_values(self, eso: ESOResult) -> None:
        col = eso.get_column(_OAT, "Environment")
        assert col is not None
        assert col.values[:5] == pytest.approx(_OAT_FIRST5)

    def test_case_insensitive(self, eso: ESOResult) -> None:
        col = eso.get_column(_OAT.lower(), "environment")
        assert col is not None
        assert len(col.values) == 48

    def test_zone_variable_values(self, eso: ESOResult) -> None:
        col = eso.get_column("Zone Mean Air Temperature", "ZONE ONE")
        assert col is not None
        assert col.values[:3] == pytest.approx((-0.6373729597, -0.6606436058, -0.7104918716))

    def test_explicit_environment_index(self, eso: ESOResult) -> None:
        col = eso.get_column(_OAT, "Environment", environment_index=0)
        assert col is not None
        assert col.environment_index == 0
        assert len(col.values) == 24  # a one-day design day

    def test_wrong_key_returns_none(self, eso: ESOResult) -> None:
        assert eso.get_column(_OAT, "NotAKey") is None

    def test_unknown_variable_returns_none(self, eso: ESOResult) -> None:
        assert eso.get_column("No Such Variable") is None

    def test_unknown_environment_index_returns_none(self, eso: ESOResult) -> None:
        assert eso.get_column(_OAT, "Environment", environment_index=99) is None


class TestEager:
    """Full materialization and parity with the lazy path."""

    def test_columns_populated(self) -> None:
        eager = ESOResult.from_file(SAMPLE_ESO, eager=True)
        assert len(eager.columns) == 507

    def test_eager_matches_lazy(self) -> None:
        lazy = ESOResult.from_file(SAMPLE_ESO)
        eager = ESOResult.from_file(SAMPLE_ESO, eager=True)
        mismatches = 0
        for col in eager.columns:
            ref = lazy.get_column(
                col.variable.variable_name,
                col.variable.key_value or None,
                col.variable.frequency,
                environment_index=col.environment_index,
            )
            if ref is None or ref.values != col.values or ref.timestamps != col.timestamps:
                mismatches += 1
        assert mismatches == 0


class TestTimestamps:
    """Timestamp construction and the hour-24 rollover."""

    def test_reference_year_and_bounds(self, eso: ESOResult) -> None:
        col = eso.get_column(_OAT)
        assert col is not None
        assert col.timestamps[0] == datetime(2017, 1, 1, 1, 0)
        assert col.timestamps[-1] == datetime(2017, 1, 3, 0, 0)

    def test_hour_24_rolls_to_next_day(self, eso: ESOResult) -> None:
        col = eso.get_column(_OAT)
        assert col is not None
        # Hour 24 of Jan 1 is reported as midnight of Jan 2.
        assert datetime(2017, 1, 2, 0, 0) in col.timestamps

    def test_daily_timestamps(self, eso: ESOResult) -> None:
        col = eso.get_column("Site Daylight Saving Time Status")
        assert col is not None
        assert all(ts.hour == 0 for ts in col.timestamps)


class TestDataFrame:
    """pandas conversion (optional dependency)."""

    def test_to_dataframe(self, eso: ESOResult) -> None:
        pytest.importorskip("pandas")
        df = eso.to_dataframe(_OAT, "Environment")
        assert df.index.name == "timestamp"
        assert list(df.columns) == [_OAT]
        assert len(df) == 48
        assert df[_OAT].iloc[0] == pytest.approx(_OAT_FIRST5[0])

    def test_to_dataframe_missing_variable_raises(self, eso: ESOResult) -> None:
        pytest.importorskip("pandas")
        with pytest.raises(KeyError):
            eso.to_dataframe("No Such Variable")


class TestFrozen:
    """The value dataclasses are immutable."""

    def test_variable_frozen(self, eso: ESOResult) -> None:
        with pytest.raises(dataclasses.FrozenInstanceError):
            eso.variables[0].report_id = 1  # type: ignore[misc]

    def test_environment_frozen(self) -> None:
        env = ESOEnvironment(0, "x", 0.0, 0.0, 0.0, 0.0)
        with pytest.raises(dataclasses.FrozenInstanceError):
            env.title = "y"  # type: ignore[misc]

    def test_column_frozen(self, eso: ESOResult) -> None:
        col = eso.get_column(_OAT)
        assert col is not None
        with pytest.raises(dataclasses.FrozenInstanceError):
            col.environment_index = 5  # type: ignore[misc]


class TestMeterFile:
    """The .mtr meter file parses through the same reader."""

    def test_meters_have_empty_key(self) -> None:
        mtr = ESOResult.from_file(SAMPLE_MTR)
        assert len(mtr.variables) >= 1
        assert all(v.key_value == "" for v in mtr.variables)

    def test_get_meter_column(self) -> None:
        mtr = ESOResult.from_file(SAMPLE_MTR)
        col = mtr.get_column("ExteriorLights:Electricity")
        assert col is not None
        assert len(col.values) == 48


class TestEdgeCases:
    """Empty, dictionary-only, truncated, and alternate-encoding inputs."""

    def test_empty_string(self) -> None:
        result = ESOResult.from_string("")
        assert result.variables == ()
        assert result.environments == ()
        assert result.columns == ()

    def test_dictionary_only(self) -> None:
        # Derive a dictionary-only file from the real fixture: header + a
        # terminator and no data records.
        raw = SAMPLE_ESO.read_bytes()
        header_end = raw.find(b"End of Data Dictionary")
        dict_only = raw[:header_end] + b"End of Data Dictionary\nEnd of Data\n"
        result = ESOResult.from_bytes(dict_only)
        assert len(result.variables) == 169
        assert result.columns == ()
        assert result.environments == ()

    def test_truncated_file_parses_without_raising(self) -> None:
        result = ESOResult.from_file(SAMPLE_TRUNCATED)
        assert len(result.variables) == 169
        # Whatever was parsed cleanly is available; nothing raises.
        col = result.get_column(_OAT)
        if col is not None:
            assert all(isinstance(v, float) for v in col.values)
        assert isinstance(result.columns, tuple)

    def test_unknown_report_id_is_skipped(self) -> None:
        raw = SAMPLE_ESO.read_bytes()
        injected = raw.replace(b"End of Data\n", b"99999,42.0\nEnd of Data\n", 1)
        result = ESOResult.from_bytes(injected)
        # Injecting an undeclared id must not break parsing of declared ones.
        col = result.get_column(_OAT)
        assert col is not None
        assert len(col.values) == 48

    def test_crlf_line_endings(self) -> None:
        raw = SAMPLE_ESO.read_bytes().replace(b"\n", b"\r\n")
        result = ESOResult.from_bytes(raw)
        col = result.get_column(_OAT)
        assert col is not None
        assert col.values[:5] == pytest.approx(_OAT_FIRST5)


class TestConstructors:
    """from_file / from_string / from_bytes agree."""

    def test_from_string_matches_from_file(self) -> None:
        text = SAMPLE_ESO.read_text(encoding="latin-1")
        from_str = ESOResult.from_string(text)
        from_file = ESOResult.from_file(SAMPLE_ESO)
        assert from_str.get_column(_OAT).values == from_file.get_column(_OAT).values  # type: ignore[union-attr]

    def test_caching_returns_same_object(self, eso: ESOResult) -> None:
        first = eso.get_column(_OAT)
        second = eso.get_column(_OAT)
        assert first is second  # second lookup hits the per-id scan cache


class TestTypes:
    """Spot-check the public type surface."""

    def test_exported_types(self, eso: ESOResult) -> None:
        assert isinstance(eso.variables[0], ESOVariable)
        assert isinstance(eso.environments[0], ESOEnvironment)
        assert isinstance(eso.get_column(_OAT), ESOColumn)
