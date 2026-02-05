"""Tests for the EnergyPlus simulation runner."""

from __future__ import annotations

import subprocess
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
from conftest import InMemoryFileSystem

from idfkit import new_document
from idfkit.exceptions import SimulationError
from idfkit.simulation.config import EnergyPlusConfig
from idfkit.simulation.runner import _build_command, _ensure_sql_output, _prepare_run_directory, simulate


@pytest.fixture
def mock_config(tmp_path: Path) -> EnergyPlusConfig:
    """Create a mock EnergyPlusConfig pointing to tmp_path."""
    exe = tmp_path / "energyplus"
    exe.touch()
    exe.chmod(0o755)
    idd = tmp_path / "Energy+.idd"
    idd.write_text("!IDD_Version 24.1.0\n")
    return EnergyPlusConfig(
        executable=exe,
        version=(24, 1, 0),
        install_dir=tmp_path,
        idd_path=idd,
    )


@pytest.fixture
def weather_file(tmp_path: Path) -> Path:
    """Create a dummy weather file."""
    epw = tmp_path / "weather.epw"
    epw.write_text("LOCATION,Chicago\n")
    return epw


# ---------------------------------------------------------------------------
# _build_command
# ---------------------------------------------------------------------------


class TestBuildCommand:
    """Tests for _build_command()."""

    def test_basic_flags(self, mock_config: EnergyPlusConfig, tmp_path: Path) -> None:
        idf = tmp_path / "in.idf"
        weather = tmp_path / "weather.epw"
        cmd = _build_command(
            config=mock_config,
            idf_path=idf,
            weather_path=weather,
            output_dir=tmp_path,
            output_prefix="eplus",
            output_suffix="C",
            expand_objects=True,
            annual=False,
            design_day=False,
            readvars=False,
            extra_args=None,
        )
        assert str(mock_config.executable) in cmd
        assert "-w" in cmd
        assert "-x" in cmd
        assert "-a" not in cmd
        assert "-D" not in cmd
        assert "-r" not in cmd
        assert cmd[-1] == str(idf)

    def test_annual_flag(self, mock_config: EnergyPlusConfig, tmp_path: Path) -> None:
        cmd = _build_command(
            config=mock_config,
            idf_path=tmp_path / "in.idf",
            weather_path=tmp_path / "w.epw",
            output_dir=tmp_path,
            output_prefix="eplus",
            output_suffix="C",
            expand_objects=False,
            annual=True,
            design_day=False,
            readvars=False,
            extra_args=None,
        )
        assert "-a" in cmd
        assert "-x" not in cmd

    def test_design_day_flag(self, mock_config: EnergyPlusConfig, tmp_path: Path) -> None:
        cmd = _build_command(
            config=mock_config,
            idf_path=tmp_path / "in.idf",
            weather_path=tmp_path / "w.epw",
            output_dir=tmp_path,
            output_prefix="eplus",
            output_suffix="C",
            expand_objects=False,
            annual=False,
            design_day=True,
            readvars=False,
            extra_args=None,
        )
        assert "-D" in cmd

    def test_readvars_flag(self, mock_config: EnergyPlusConfig, tmp_path: Path) -> None:
        cmd = _build_command(
            config=mock_config,
            idf_path=tmp_path / "in.idf",
            weather_path=tmp_path / "w.epw",
            output_dir=tmp_path,
            output_prefix="eplus",
            output_suffix="C",
            expand_objects=False,
            annual=False,
            design_day=False,
            readvars=True,
            extra_args=None,
        )
        assert "-r" in cmd

    def test_extra_args(self, mock_config: EnergyPlusConfig, tmp_path: Path) -> None:
        cmd = _build_command(
            config=mock_config,
            idf_path=tmp_path / "in.idf",
            weather_path=tmp_path / "w.epw",
            output_dir=tmp_path,
            output_prefix="eplus",
            output_suffix="C",
            expand_objects=False,
            annual=False,
            design_day=False,
            readvars=False,
            extra_args=["--custom", "value"],
        )
        assert "--custom" in cmd
        assert "value" in cmd


# ---------------------------------------------------------------------------
# _ensure_sql_output
# ---------------------------------------------------------------------------


class TestEnsureSqlOutput:
    """Tests for _ensure_sql_output()."""

    def test_adds_when_missing(self) -> None:
        doc = new_document()
        assert "Output:SQLite" not in doc
        _ensure_sql_output(doc)
        assert "Output:SQLite" in doc

    def test_no_duplicate(self) -> None:
        doc = new_document()
        doc.add("Output:SQLite", "SimpleAndTabular")
        _ensure_sql_output(doc)
        assert len(doc["Output:SQLite"]) == 1


# ---------------------------------------------------------------------------
# _prepare_run_directory
# ---------------------------------------------------------------------------


class TestPrepareRunDirectory:
    """Tests for _prepare_run_directory()."""

    def test_temp_dir_created(self, weather_file: Path) -> None:
        run_dir = _prepare_run_directory(None, weather_file)
        assert run_dir.is_dir()
        assert (run_dir / weather_file.name).is_file()

    def test_explicit_dir(self, tmp_path: Path, weather_file: Path) -> None:
        out = tmp_path / "my_output"
        run_dir = _prepare_run_directory(out, weather_file)
        assert run_dir == out.resolve()
        assert run_dir.is_dir()
        assert (run_dir / weather_file.name).is_file()

    def test_weather_not_copied_if_exists(self, tmp_path: Path, weather_file: Path) -> None:
        out = tmp_path / "existing"
        out.mkdir()
        dest = out / weather_file.name
        dest.write_text("existing content")
        _prepare_run_directory(out, weather_file)
        assert dest.read_text() == "existing content"


# ---------------------------------------------------------------------------
# simulate
# ---------------------------------------------------------------------------


class TestSimulate:
    """Tests for simulate()."""

    @patch("idfkit.simulation.runner.subprocess.run")
    def test_success(self, mock_run: MagicMock, mock_config: EnergyPlusConfig, weather_file: Path) -> None:
        mock_run.return_value = MagicMock(returncode=0, stdout="ok", stderr="")
        model = new_document()
        result = simulate(model, weather_file, energyplus=mock_config)
        assert result.success
        assert result.exit_code == 0
        mock_run.assert_called_once()

    @patch("idfkit.simulation.runner.subprocess.run")
    def test_failure(self, mock_run: MagicMock, mock_config: EnergyPlusConfig, weather_file: Path) -> None:
        mock_run.return_value = MagicMock(returncode=1, stdout="", stderr="error occurred")
        model = new_document()
        result = simulate(model, weather_file, energyplus=mock_config)
        assert not result.success
        assert result.exit_code == 1

    @patch("idfkit.simulation.runner.subprocess.run")
    def test_timeout(self, mock_run: MagicMock, mock_config: EnergyPlusConfig, weather_file: Path) -> None:
        mock_run.side_effect = subprocess.TimeoutExpired(cmd=["energyplus"], timeout=10)
        model = new_document()
        with pytest.raises(SimulationError, match="timed out"):
            simulate(model, weather_file, energyplus=mock_config, timeout=10)

    def test_missing_weather(self, mock_config: EnergyPlusConfig) -> None:
        model = new_document()
        with pytest.raises(SimulationError, match="Weather file not found"):
            simulate(model, "/nonexistent/weather.epw", energyplus=mock_config)

    @patch("idfkit.simulation.runner.subprocess.run")
    def test_model_not_mutated(self, mock_run: MagicMock, mock_config: EnergyPlusConfig, weather_file: Path) -> None:
        mock_run.return_value = MagicMock(returncode=0, stdout="", stderr="")
        model = new_document()
        assert "Output:SQLite" not in model
        simulate(model, weather_file, energyplus=mock_config)
        # Original model should not have Output:SQLite
        assert "Output:SQLite" not in model

    def test_fs_requires_output_dir(self, mock_config: EnergyPlusConfig, weather_file: Path) -> None:
        fs = InMemoryFileSystem()
        model = new_document()
        with pytest.raises(ValueError, match="output_dir is required"):
            simulate(model, weather_file, energyplus=mock_config, fs=fs)

    @patch("idfkit.simulation.runner.subprocess.run")
    def test_simulate_with_fs_uploads_results(
        self, mock_run: MagicMock, mock_config: EnergyPlusConfig, weather_file: Path
    ) -> None:
        mock_run.return_value = MagicMock(returncode=0, stdout="ok", stderr="")
        fs = InMemoryFileSystem()
        model = new_document()
        result = simulate(
            model,
            weather_file,
            energyplus=mock_config,
            output_dir="remote/output",
            fs=fs,
        )
        assert result.success
        assert result.fs is fs
        assert result.run_dir == Path("remote/output")
        # Verify files were uploaded — at minimum in.idf and weather should be there
        uploaded = [k for k in fs._files if k.startswith("remote/output/")]
        assert len(uploaded) > 0
