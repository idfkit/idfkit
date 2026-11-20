"""Tests for the EnergyPlus simulation runner."""

from __future__ import annotations

import logging
import os
import re
import subprocess
from pathlib import Path
from typing import TYPE_CHECKING, Any
from unittest.mock import MagicMock, patch

import pytest
from conftest import (
    REFUSAL_R1,
    REFUSAL_R2,
    InMemoryFileSystem,
    design_day_model,
    ground_heat_model,
    refusal_r3,
    refusal_r4,
    runnable_model,
)

from idfkit import LATEST_VERSION, new_document
from idfkit.exceptions import ExpandObjectsError, SimulationError
from idfkit.simulation.config import EnergyPlusConfig
from idfkit.simulation.runner import _build_command, _ensure_sql_output, _prepare_run_directory, simulate

if TYPE_CHECKING:
    from idfkit import IDFDocument
    from idfkit._generated_types import SimulationControl


@pytest.fixture
def mock_config(tmp_path: Path) -> EnergyPlusConfig:
    """Create a mock EnergyPlusConfig pointing to tmp_path."""
    exe = tmp_path / "energyplus"
    exe.touch()
    exe.chmod(0o755)
    idd = tmp_path / "Energy+.idd"
    idd.write_text("!IDD_Version 24.1.0\n")

    # ExpandObjects
    expand_exe = tmp_path / "ExpandObjects"
    expand_exe.touch()
    expand_exe.chmod(0o755)

    # Slab & Basement preprocessors
    preprocess = tmp_path / "PreProcess" / "GrndTempCalc"
    preprocess.mkdir(parents=True)
    slab_exe = preprocess / "Slab"
    slab_exe.touch()
    slab_exe.chmod(0o755)
    (preprocess / "SlabGHT.idd").write_text("! Slab IDD\n")
    basement_exe = preprocess / "Basement"
    basement_exe.touch()
    basement_exe.chmod(0o755)
    (preprocess / "BasementGHT.idd").write_text("! Basement IDD\n")

    return EnergyPlusConfig(
        executable=exe,
        version=LATEST_VERSION,
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

    def test_without_weather_omits_w(self, mock_config: EnergyPlusConfig, tmp_path: Path) -> None:
        """A command without a weather path drops ``-w <path>`` and keeps every other element in order."""
        common: dict[str, Any] = {
            "config": mock_config,
            "idf_path": tmp_path / "in.idf",
            "output_dir": tmp_path,
            "output_prefix": "eplus",
            "output_suffix": "C",
            "expand_objects": True,
            "annual": False,
            "design_day": True,
            "readvars": False,
            "extra_args": None,
        }
        weather = tmp_path / "w.epw"
        with_weather = _build_command(weather_path=weather, **common)
        without_weather = _build_command(weather_path=None, **common)

        assert "-D" in without_weather
        assert "-w" not in without_weather
        assert not any(arg.endswith(".epw") for arg in without_weather)
        assert without_weather == [arg for arg in with_weather if arg not in ("-w", str(weather))]


# ---------------------------------------------------------------------------
# _ensure_sql_output
# ---------------------------------------------------------------------------


class TestEnsureSqlOutput:
    """Tests for _ensure_sql_output()."""

    def test_adds_when_missing(self) -> None:
        doc = runnable_model()
        assert "Output:SQLite" not in doc
        _ensure_sql_output(doc)
        assert "Output:SQLite" in doc

    def test_no_duplicate(self) -> None:
        doc = runnable_model()
        doc.add("Output:SQLite", option_type="SimpleAndTabular")
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

    def test_stale_weather_copy_replaced(self, tmp_path: Path, weather_file: Path) -> None:
        out = tmp_path / "existing"
        out.mkdir()
        dest = out / weather_file.name
        dest.write_text("existing content")
        _prepare_run_directory(out, weather_file)
        assert dest.read_bytes() == weather_file.read_bytes()

    def test_second_run_with_same_named_weather_uses_new_file(self, tmp_path: Path) -> None:
        """Two runs into one output_dir with different weather files of the same name (#227)."""
        first = tmp_path / "a" / "site.epw"
        second = tmp_path / "b" / "site.epw"
        first.parent.mkdir()
        second.parent.mkdir()
        first.write_text("LOCATION,First\n")
        second.write_text("LOCATION,Second city\n")
        out = tmp_path / "run"

        _prepare_run_directory(out, first)
        assert (out / "site.epw").read_text() == "LOCATION,First\n"
        _prepare_run_directory(out, second)
        assert (out / "site.epw").read_text() == "LOCATION,Second city\n"

    def test_identical_weather_copy_not_rewritten(self, tmp_path: Path, weather_file: Path) -> None:
        out = tmp_path / "run"
        _prepare_run_directory(out, weather_file)
        dest = out / weather_file.name
        os.utime(dest, (0, 0))
        _prepare_run_directory(out, weather_file)
        assert dest.stat().st_mtime == 0

    def test_weather_already_in_output_dir(self, tmp_path: Path) -> None:
        out = tmp_path / "run"
        out.mkdir()
        weather = out / "site.epw"
        weather.write_text("LOCATION,Here\n")
        run_dir = _prepare_run_directory(out, weather)
        assert run_dir == out.resolve()
        assert weather.read_text() == "LOCATION,Here\n"

    def test_without_weather_copies_nothing(self, tmp_path: Path) -> None:
        run_dir = _prepare_run_directory(tmp_path / "run", None)
        assert run_dir.is_dir()
        assert list(run_dir.glob("*.epw")) == []


# ---------------------------------------------------------------------------
# simulate
# ---------------------------------------------------------------------------


class TestSimulate:
    """Tests for simulate()."""

    @patch("idfkit.simulation.runner.run_process")
    def test_success(self, mock_run: MagicMock, mock_config: EnergyPlusConfig, weather_file: Path) -> None:
        mock_run.return_value = MagicMock(returncode=0, stdout="ok", stderr="")
        model = runnable_model()
        result = simulate(model, weather_file, energyplus=mock_config)
        assert result.success
        assert result.exit_code == 0
        mock_run.assert_called_once()

    @patch("idfkit.simulation.runner.run_process")
    def test_failure(self, mock_run: MagicMock, mock_config: EnergyPlusConfig, weather_file: Path) -> None:
        mock_run.return_value = MagicMock(returncode=1, stdout="", stderr="error occurred")
        model = runnable_model()
        result = simulate(model, weather_file, energyplus=mock_config)
        assert not result.success
        assert result.exit_code == 1

    @patch("idfkit.simulation.runner.run_process")
    def test_timeout(self, mock_run: MagicMock, mock_config: EnergyPlusConfig, weather_file: Path) -> None:
        mock_run.side_effect = subprocess.TimeoutExpired(cmd=["energyplus"], timeout=10)
        model = runnable_model()
        with pytest.raises(SimulationError, match="timed out"):
            simulate(model, weather_file, energyplus=mock_config, timeout=10)

    def test_missing_weather(self, mock_config: EnergyPlusConfig) -> None:
        model = runnable_model()
        with pytest.raises(SimulationError, match="Weather file not found"):
            simulate(model, "/nonexistent/weather.epw", energyplus=mock_config)

    @patch("idfkit.simulation.runner.run_process")
    def test_model_not_mutated(self, mock_run: MagicMock, mock_config: EnergyPlusConfig, weather_file: Path) -> None:
        mock_run.return_value = MagicMock(returncode=0, stdout="", stderr="")
        model = runnable_model()
        assert "Output:SQLite" not in model
        simulate(model, weather_file, energyplus=mock_config)
        # Original model should not have Output:SQLite
        assert "Output:SQLite" not in model

    def test_fs_requires_output_dir(self, mock_config: EnergyPlusConfig, weather_file: Path) -> None:
        fs = InMemoryFileSystem()
        model = runnable_model()
        with pytest.raises(ValueError, match="output_dir is required"):
            simulate(model, weather_file, energyplus=mock_config, fs=fs)

    @patch("idfkit.simulation.runner.run_process")
    def test_simulate_with_fs_uploads_results(
        self, mock_run: MagicMock, mock_config: EnergyPlusConfig, weather_file: Path
    ) -> None:
        mock_run.return_value = MagicMock(returncode=0, stdout="ok", stderr="")
        fs = InMemoryFileSystem()
        model = runnable_model()
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
        uploaded = [k for k in fs._files if k.startswith("remote/output/")]
        assert "remote/output/model.idf" in uploaded

    @patch("idfkit.simulation.runner.run_process")
    def test_fs_run_skips_weather_and_deletes_local_dir(
        self, mock_run: MagicMock, mock_config: EnergyPlusConfig, weather_file: Path
    ) -> None:
        """The input weather file is not uploaded, and the local run directory is gone afterwards."""
        mock_run.return_value = MagicMock(returncode=0, stdout="ok", stderr="")
        fs = InMemoryFileSystem()
        simulate(runnable_model(), weather_file, energyplus=mock_config, output_dir="remote/output", fs=fs)
        local_dir = Path(mock_run.call_args.kwargs["cwd"])
        assert not local_dir.exists()
        assert f"remote/output/{weather_file.name}" not in fs._files
        assert "remote/output/model.idf" in fs._files

    @patch("idfkit.simulation.runner.run_process")
    def test_fs_run_skips_symlinked_weather(
        self, mock_run: MagicMock, mock_config: EnergyPlusConfig, weather_file: Path, tmp_path: Path
    ) -> None:
        """A symlinked weather file is copied under its target's name, which the upload still skips."""
        mock_run.return_value = MagicMock(returncode=0, stdout="ok", stderr="")
        link = tmp_path / "link.epw"
        link.symlink_to(weather_file)
        fs = InMemoryFileSystem()
        simulate(runnable_model(), link, energyplus=mock_config, output_dir="remote/output", fs=fs)
        assert not [k for k in fs._files if k.endswith(".epw")]
        assert "remote/output/model.idf" in fs._files

    @patch("idfkit.simulation.runner.run_process")
    def test_fs_run_deletes_local_dir_on_timeout(
        self, mock_run: MagicMock, mock_config: EnergyPlusConfig, weather_file: Path
    ) -> None:
        mock_run.side_effect = subprocess.TimeoutExpired(cmd=["energyplus"], timeout=10)
        fs = InMemoryFileSystem()
        with pytest.raises(SimulationError, match="timed out"):
            simulate(runnable_model(), weather_file, energyplus=mock_config, output_dir="remote/output", fs=fs)
        assert not Path(mock_run.call_args.kwargs["cwd"]).exists()


# ---------------------------------------------------------------------------
# simulate() automatic preprocessing
# ---------------------------------------------------------------------------


class TestSimulatePreprocessing:
    """Tests for automatic ground heat-transfer preprocessing in simulate()."""

    def test_auto_preprocesses_slab_model(self, mock_config: EnergyPlusConfig, weather_file: Path) -> None:
        """simulate() calls _run_preprocessing for models with slab objects."""
        model = runnable_model(version=LATEST_VERSION)
        model.add("GroundHeatTransfer:Slab:Materials", "", {}, validate=False)
        model.add("Zone", "Office", {"x_origin": 0.0})

        preprocessed = runnable_model(version=LATEST_VERSION)
        preprocessed.add("Zone", "Office", {"x_origin": 0.0})

        sim_proc = MagicMock(returncode=0, stdout="ok", stderr="")

        with (
            patch("idfkit.simulation.expand.run_preprocessing", return_value=preprocessed) as mock_preprocess,
            patch("idfkit.simulation.runner.run_process", return_value=sim_proc) as mock_sim_run,
        ):
            result = simulate(model, weather_file, energyplus=mock_config)

        mock_preprocess.assert_called_once()
        # EnergyPlus CLI was called without -x (already expanded)
        sim_cmd = mock_sim_run.call_args[0][0]
        assert "-x" not in sim_cmd
        assert result.success

    def test_auto_preprocesses_basement_model(self, mock_config: EnergyPlusConfig, weather_file: Path) -> None:
        """simulate() calls _run_preprocessing for models with basement objects."""
        model = runnable_model(version=LATEST_VERSION)
        model.add("GroundHeatTransfer:Basement:SimParameters", "", {}, validate=False)
        model.add("Zone", "Office", {"x_origin": 0.0})

        preprocessed = runnable_model(version=LATEST_VERSION)
        preprocessed.add("Zone", "Office", {"x_origin": 0.0})

        sim_proc = MagicMock(returncode=0, stdout="ok", stderr="")

        with (
            patch("idfkit.simulation.expand.run_preprocessing", return_value=preprocessed) as mock_preprocess,
            patch("idfkit.simulation.runner.run_process", return_value=sim_proc) as mock_sim_run,
        ):
            result = simulate(model, weather_file, energyplus=mock_config)

        mock_preprocess.assert_called_once()
        sim_cmd = mock_sim_run.call_args[0][0]
        assert "-x" not in sim_cmd
        assert result.success

    @patch("idfkit.simulation.runner.run_process")
    def test_no_preprocessing_for_plain_model(
        self, mock_run: MagicMock, mock_config: EnergyPlusConfig, weather_file: Path
    ) -> None:
        """simulate() does not run preprocessing for models without GHT objects."""
        mock_run.return_value = MagicMock(returncode=0, stdout="ok", stderr="")
        model = runnable_model(version=LATEST_VERSION)
        model.add("Zone", "Office", {"x_origin": 0.0})

        with patch("idfkit.simulation.expand.run_preprocessing") as mock_preprocess:
            result = simulate(model, weather_file, energyplus=mock_config)

        mock_preprocess.assert_not_called()
        # EnergyPlus CLI called with -x (normal expand)
        sim_cmd = mock_run.call_args[0][0]
        assert "-x" in sim_cmd
        assert result.success

    @patch("idfkit.simulation.runner.run_process")
    def test_no_preprocessing_when_expand_objects_false(
        self, mock_run: MagicMock, mock_config: EnergyPlusConfig, weather_file: Path
    ) -> None:
        """simulate(expand_objects=False) skips preprocessing even with GHT objects."""
        mock_run.return_value = MagicMock(returncode=0, stdout="ok", stderr="")
        model = runnable_model(version=LATEST_VERSION)
        model.add("GroundHeatTransfer:Slab:Materials", "", {}, validate=False)
        model.add("Zone", "Office", {"x_origin": 0.0})

        with patch("idfkit.simulation.expand.run_preprocessing") as mock_preprocess:
            result = simulate(model, weather_file, energyplus=mock_config, expand_objects=False)

        mock_preprocess.assert_not_called()
        sim_cmd = mock_run.call_args[0][0]
        assert "-x" not in sim_cmd
        assert result.success

    def test_preprocessing_error_propagates(self, mock_config: EnergyPlusConfig, weather_file: Path) -> None:
        """ExpandObjectsError from preprocessing propagates through simulate()."""
        model = runnable_model(version=LATEST_VERSION)
        model.add("GroundHeatTransfer:Slab:Materials", "", {}, validate=False)
        model.add("Zone", "Office", {"x_origin": 0.0})

        with (
            patch(
                "idfkit.simulation.expand.run_preprocessing",
                side_effect=ExpandObjectsError("Slab failed", preprocessor="Slab", exit_code=0),
            ),
            pytest.raises(ExpandObjectsError, match="Slab failed"),
        ):
            simulate(model, weather_file, energyplus=mock_config)

    def test_model_not_mutated_with_preprocessing(self, mock_config: EnergyPlusConfig, weather_file: Path) -> None:
        """Original model is not mutated when preprocessing runs."""
        model = runnable_model(version=LATEST_VERSION)
        model.add("GroundHeatTransfer:Slab:Materials", "", {}, validate=False)
        model.add("Zone", "Office", {"x_origin": 0.0})

        original_types = set(model.keys())

        preprocessed = runnable_model(version=LATEST_VERSION)
        preprocessed.add("Zone", "Office", {"x_origin": 0.0})

        sim_proc = MagicMock(returncode=0, stdout="ok", stderr="")

        with (
            patch("idfkit.simulation.expand.run_preprocessing", return_value=preprocessed),
            patch("idfkit.simulation.runner.run_process", return_value=sim_proc),
        ):
            simulate(model, weather_file, energyplus=mock_config)

        assert set(model.keys()) == original_types
        assert "Output:SQLite" not in model


# ---------------------------------------------------------------------------
# _run_simple: OSError path (L248-250)
# ---------------------------------------------------------------------------


class TestRunSimpleOSError:
    """Tests for the OSError exception path in _run_simple()."""

    @patch("idfkit.simulation.runner.run_process")
    def test_os_error_raises_simulation_error(
        self, mock_run: MagicMock, mock_config: EnergyPlusConfig, weather_file: Path
    ) -> None:
        """run_process raising OSError should raise SimulationError."""
        mock_run.side_effect = OSError("No such file or directory")
        model = runnable_model()
        with pytest.raises(SimulationError, match="Failed to start EnergyPlus"):
            simulate(model, weather_file, energyplus=mock_config)


# ---------------------------------------------------------------------------
# resolve_config: auto-discovery path (_common.py L31)
# ---------------------------------------------------------------------------


class TestResolveConfig:
    """Tests for resolve_config() auto-discovery path."""

    def test_auto_discovers_energyplus(self, mock_config: EnergyPlusConfig) -> None:
        """resolve_config(None) calls find_energyplus() when no config is provided."""
        from idfkit.simulation._common import resolve_config  # pyright: ignore[reportPrivateUsage]

        with patch("idfkit.simulation._common.find_energyplus", return_value=mock_config) as mock_find:
            result = resolve_config(None)

        mock_find.assert_called_once()
        assert result is mock_config

    def test_returns_provided_config(self, mock_config: EnergyPlusConfig) -> None:
        """resolve_config(config) returns the config without calling find_energyplus."""
        from idfkit.simulation._common import resolve_config  # pyright: ignore[reportPrivateUsage]

        with patch("idfkit.simulation._common.find_energyplus") as mock_find:
            result = resolve_config(mock_config)

        mock_find.assert_not_called()
        assert result is mock_config


# ---------------------------------------------------------------------------
# simulate() without a weather file
# ---------------------------------------------------------------------------


class TestSimulateWithoutWeather:
    """Tests for simulate() with weather=None on a design-day-only run."""

    @patch("idfkit.simulation.runner.run_process")
    def test_command_has_no_weather(self, mock_run: MagicMock, mock_config: EnergyPlusConfig, tmp_path: Path) -> None:
        mock_run.return_value = MagicMock(returncode=0, stdout="ok", stderr="")
        result = simulate(design_day_model(), design_day=True, energyplus=mock_config, output_dir=tmp_path / "run")
        cmd = mock_run.call_args[0][0]
        assert "-D" in cmd
        assert "-w" not in cmd
        assert result.success
        assert list(result.run_dir.glob("*.epw")) == []

    @patch("idfkit.simulation.runner.run_process")
    def test_positional_none(self, mock_run: MagicMock, mock_config: EnergyPlusConfig, tmp_path: Path) -> None:
        mock_run.return_value = MagicMock(returncode=0, stdout="ok", stderr="")
        result = simulate(
            design_day_model(), None, design_day=True, energyplus=mock_config, output_dir=tmp_path / "run"
        )
        cmd = mock_run.call_args[0][0]
        assert "-D" in cmd
        assert "-w" not in cmd
        assert list(result.run_dir.glob("*.epw")) == []

    @patch("idfkit.simulation.runner.run_process")
    def test_log_states_no_weather(
        self,
        mock_run: MagicMock,
        mock_config: EnergyPlusConfig,
        tmp_path: Path,
        caplog: pytest.LogCaptureFixture,
    ) -> None:
        mock_run.return_value = MagicMock(returncode=0, stdout="ok", stderr="")
        with caplog.at_level(logging.DEBUG, logger="idfkit.simulation"):
            simulate(design_day_model(), design_day=True, energyplus=mock_config, output_dir=tmp_path / "run")
        messages = [record.getMessage() for record in caplog.records]
        assert "Starting simulation without a weather file" in messages
        assert not any("in.epw" in m for m in messages)
        assert not any(str(Path.cwd()) in m for m in messages if "weather" in m.casefold())


class TestWeatherAdmission:
    """Refusals REFUSAL_R1 to R4 and the unchanged missing-file message, raised before any subprocess."""

    def _assert_refused(self, message: str, **kwargs: Any) -> None:
        # Not ``or``: an IDFDocument with no objects is falsy.
        model = kwargs.pop("model", None)
        if model is None:
            model = runnable_model()
        with (
            patch("idfkit.simulation.runner.run_process") as mock_run,
            patch("idfkit.simulation.expand.run_preprocessing") as mock_preprocess,
            pytest.raises(SimulationError, match=re.escape(message)),
        ):
            simulate(model, **kwargs)
        mock_run.assert_not_called()
        mock_preprocess.assert_not_called()

    def test_r1_empty_string(self, mock_config: EnergyPlusConfig) -> None:
        self._assert_refused(REFUSAL_R1, weather="", design_day=True, energyplus=mock_config)

    def test_missing_file_unchanged(self, mock_config: EnergyPlusConfig, tmp_path: Path) -> None:
        missing = tmp_path / "absent.epw"
        self._assert_refused(
            f"Weather file not found: {missing.resolve()}", weather=missing, design_day=True, energyplus=mock_config
        )

    def test_r2_not_design_day(self, mock_config: EnergyPlusConfig) -> None:
        self._assert_refused(REFUSAL_R2, weather=None, design_day=False, energyplus=mock_config)

    def test_r2_design_day_and_annual(self, mock_config: EnergyPlusConfig) -> None:
        self._assert_refused(REFUSAL_R2, weather=None, design_day=True, annual=True, energyplus=mock_config)

    def test_r3_ground_heat_transfer(self, mock_config: EnergyPlusConfig) -> None:
        self._assert_refused(
            refusal_r3("GroundHeatTransfer:Basement:SimParameters, GroundHeatTransfer:Slab:Materials"),
            model=ground_heat_model(),
            weather=None,
            design_day=True,
            energyplus=mock_config,
        )

    def test_r3_lists_only_enabled_types(self, mock_config: EnergyPlusConfig) -> None:
        self._assert_refused(
            refusal_r3("GroundHeatTransfer:Slab:Materials"),
            model=ground_heat_model(slab="Yes", basement="No"),
            weather=None,
            design_day=True,
            energyplus=mock_config,
        )

    @pytest.mark.parametrize(
        ("slab", "basement"),
        [("No", "No"), ("", ""), (None, None)],
        ids=["control-no", "control-blank", "control-absent"],
    )
    def test_r3_not_raised_when_control_disables_preprocessors(
        self, mock_config: EnergyPlusConfig, tmp_path: Path, slab: str | None, basement: str | None
    ) -> None:
        """Without an enabled Slab or Basement solver, only ExpandObjects runs, and it reads no weather file."""
        model = ground_heat_model(slab=slab, basement=basement)
        with (
            patch("idfkit.simulation.runner.run_process") as mock_run,
            patch("idfkit.simulation.expand.run_preprocessing", side_effect=lambda m, **_: m.copy()) as mock_pre,
        ):
            mock_run.return_value = MagicMock(returncode=0, stdout="ok", stderr="")
            result = simulate(model, design_day=True, energyplus=mock_config, output_dir=tmp_path / "run")
        mock_pre.assert_called_once()
        assert mock_pre.call_args.kwargs["weather"] is None
        assert result.success

    def test_annual_without_run_period_refused(self, mock_config: EnergyPlusConfig, weather_file: Path) -> None:
        """EnergyPlus would add a run period, simulate nothing and report success, so the run is refused."""
        with (
            patch("idfkit.simulation.runner.run_process") as mock_run,
            pytest.raises(SimulationError, match="annual=True, but the model has no RunPeriod"),
        ):
            simulate(new_document(), weather_file, annual=True, energyplus=mock_config)
        mock_run.assert_not_called()

    def test_design_day_without_design_days_refused(self, mock_config: EnergyPlusConfig, weather_file: Path) -> None:
        """EnergyPlus would blame the weather data input, so the run is refused and names the fix."""
        model = new_document()
        model.add("RunPeriod", "Annual", begin_month=1, begin_day_of_month=1, end_month=12, end_day_of_month=31)
        with (
            patch("idfkit.simulation.runner.run_process") as mock_run,
            pytest.raises(
                SimulationError, match=r"design_day=True, but the model has no SizingPeriod:DesignDay"
            ) as exc,
        ):
            simulate(model, weather_file, design_day=True, energyplus=mock_config)
        mock_run.assert_not_called()
        assert "apply_to_model" in str(exc.value)
        assert "apply_ashrae_sizing" in str(exc.value)

    def test_design_day_refused_before_energyplus_discovery(self, weather_file: Path) -> None:
        with (
            patch("idfkit.simulation._common.find_energyplus") as mock_find,
            pytest.raises(SimulationError, match="no SizingPeriod:DesignDay"),
        ):
            simulate(runnable_model(), weather_file, design_day=True)
        mock_find.assert_not_called()

    def test_design_day_with_design_day_runs(
        self, mock_config: EnergyPlusConfig, weather_file: Path, tmp_path: Path
    ) -> None:
        with patch("idfkit.simulation.runner.run_process") as mock_run:
            mock_run.return_value = MagicMock(returncode=0, stdout="ok", stderr="")
            result = simulate(
                design_day_model(), weather_file, design_day=True, energyplus=mock_config, output_dir=tmp_path / "run"
            )
        assert result.success
        assert "-D" in mock_run.call_args.args[0]

    def test_annual_with_run_period_runs(
        self, mock_config: EnergyPlusConfig, weather_file: Path, tmp_path: Path
    ) -> None:
        model = new_document()
        model.add("RunPeriod", "Annual", begin_month=1, begin_day_of_month=1, end_month=12, end_day_of_month=31)
        with patch("idfkit.simulation.runner.run_process") as mock_run:
            mock_run.return_value = MagicMock(returncode=0, stdout="ok", stderr="")
            result = simulate(model, weather_file, annual=True, energyplus=mock_config, output_dir=tmp_path / "run")
        assert result.success
        assert "-a" in mock_run.call_args.args[0]

    def test_weather_refused_before_energyplus_discovery(self) -> None:
        """An invalid weather argument is reported even on a machine without EnergyPlus."""
        with (
            patch("idfkit.simulation._common.find_energyplus") as mock_find,
            pytest.raises(SimulationError, match=re.escape(REFUSAL_R2)),
        ):
            simulate(runnable_model(), annual=True)  # pyright: ignore[reportCallIssue]
        mock_find.assert_not_called()

    def test_r3_not_raised_without_expand_objects(self, mock_config: EnergyPlusConfig, tmp_path: Path) -> None:
        with (
            patch("idfkit.simulation.runner.run_process") as mock_run,
            patch("idfkit.simulation.expand.run_preprocessing") as mock_preprocess,
        ):
            mock_run.return_value = MagicMock(returncode=0, stdout="ok", stderr="")
            result = simulate(
                ground_heat_model(),
                design_day=True,
                expand_objects=False,
                energyplus=mock_config,
                output_dir=tmp_path / "run",
            )
        mock_run.assert_called_once()
        mock_preprocess.assert_not_called()
        assert result.success

    def test_r2_takes_precedence_over_r3(self, mock_config: EnergyPlusConfig) -> None:
        self._assert_refused(
            REFUSAL_R2, model=ground_heat_model(), weather=None, design_day=False, energyplus=mock_config
        )

    def test_r4_default_weather_in_run_dir(self, mock_config: EnergyPlusConfig, tmp_path: Path) -> None:
        (tmp_path / "in.epw").write_text("LOCATION,Elsewhere\n")
        self._assert_refused(
            refusal_r4(tmp_path.resolve()), weather=None, design_day=True, energyplus=mock_config, output_dir=tmp_path
        )

    def test_r4_refused_before_cache_lookup(self, mock_config: EnergyPlusConfig, tmp_path: Path) -> None:
        run_dir = tmp_path / "run"
        run_dir.mkdir()
        (run_dir / "in.epw").write_text("LOCATION,Elsewhere\n")
        cache = MagicMock()
        self._assert_refused(
            refusal_r4(run_dir.resolve()),
            weather=None,
            design_day=True,
            energyplus=mock_config,
            output_dir=run_dir,
            cache=cache,
        )
        cache.compute_key.assert_not_called()
        cache.get.assert_not_called()

    def test_r3_not_raised_for_emptied_collection(self, mock_config: EnergyPlusConfig, tmp_path: Path) -> None:
        """A type whose every object was removed leaves an empty collection, which needs no weather file."""
        model = design_day_model(version=LATEST_VERSION)
        slab = model.add("GroundHeatTransfer:Slab:Materials", "", {}, validate=False)
        model.removeidfobject(slab)
        with (
            patch("idfkit.simulation.runner.run_process") as mock_run,
            patch("idfkit.simulation.expand.run_preprocessing") as mock_preprocess,
        ):
            mock_run.return_value = MagicMock(returncode=0, stdout="ok", stderr="")
            result = simulate(model, design_day=True, energyplus=mock_config, output_dir=tmp_path / "run")
        mock_run.assert_called_once()
        mock_preprocess.assert_not_called()
        assert result.success


# ---------------------------------------------------------------------------
# simulate() with a cache and files the model names (#216)
# ---------------------------------------------------------------------------


def _schedule_file_model(file_name: str) -> Any:
    model = runnable_model()
    model.add("Schedule:File", "Staged", file_name=file_name, column_number=1, rows_to_skip_at_top=0, validate=False)
    return model


class TestSimulateCacheCoversExternalFiles:
    """The key hashes every file the model names, so a changed input is a miss and a restored one a hit."""

    @patch("idfkit.simulation.runner.run_process")
    def test_staged_file_in_output_dir(
        self, mock_run: MagicMock, mock_config: EnergyPlusConfig, weather_file: Path, tmp_path: Path
    ) -> None:
        from idfkit.simulation.cache import SimulationCache

        mock_run.return_value = MagicMock(returncode=0, stdout="ok", stderr="")
        cache = SimulationCache(cache_dir=tmp_path / "cache")
        run_dir = tmp_path / "run"
        (run_dir / "data").mkdir(parents=True)
        csv = run_dir / "data" / "hourly.csv"
        model = _schedule_file_model("data/hourly.csv")

        def run() -> bool:
            result = simulate(model, weather_file, energyplus=mock_config, output_dir=run_dir, cache=cache)
            assert result.run_dir == run_dir.resolve()
            return result.cached

        csv.write_text("0.5\n")
        assert not run()
        assert run()  # unchanged CSV: hit
        csv.write_text("1.0\n")
        assert not run()  # changed CSV: miss
        csv.write_text("0.5\n")
        assert run()  # restored CSV: hit on the first entry
        assert mock_run.call_count == 2

    @patch("idfkit.simulation.runner.run_process")
    def test_file_outside_output_dir(
        self, mock_run: MagicMock, mock_config: EnergyPlusConfig, weather_file: Path, tmp_path: Path
    ) -> None:
        from idfkit.simulation.cache import SimulationCache

        mock_run.return_value = MagicMock(returncode=0, stdout="ok", stderr="")
        cache = SimulationCache(cache_dir=tmp_path / "cache")
        csv = tmp_path / "inputs" / "occ.csv"
        csv.parent.mkdir()
        model = _schedule_file_model(str(csv))

        csv.write_text("1\n")
        simulate(model, weather_file, energyplus=mock_config, cache=cache)
        simulate(model, weather_file, energyplus=mock_config, cache=cache)
        assert mock_run.call_count == 1
        csv.write_text("2\n")
        simulate(model, weather_file, energyplus=mock_config, cache=cache)
        assert mock_run.call_count == 2

    @patch("idfkit.simulation.runner.run_process")
    def test_python_plugin_is_never_cached(
        self,
        mock_run: MagicMock,
        mock_config: EnergyPlusConfig,
        weather_file: Path,
        tmp_path: Path,
        caplog: pytest.LogCaptureFixture,
    ) -> None:
        from idfkit.simulation.cache import SimulationCache

        mock_run.return_value = MagicMock(returncode=0, stdout="ok", stderr="")
        cache = SimulationCache(cache_dir=tmp_path / "cache")
        model = runnable_model()
        model.add("PythonPlugin:Instance", "Plugin", python_module_name="plugin", plugin_class_name="P", validate=False)

        with caplog.at_level(logging.WARNING, logger="idfkit.simulation.cache"):
            simulate(model, weather_file, energyplus=mock_config, cache=cache)
            simulate(model, weather_file, energyplus=mock_config, cache=cache)
        assert mock_run.call_count == 2
        assert not (tmp_path / "cache").exists()
        assert "Not using the simulation cache" in caplog.text
        assert "PythonPlugin:Instance" in caplog.text

    @patch("idfkit.simulation.runner.run_process")
    def test_reused_output_dir_still_hits(
        self, mock_run: MagicMock, mock_config: EnergyPlusConfig, weather_file: Path, tmp_path: Path
    ) -> None:
        from idfkit.simulation.cache import SimulationCache

        mock_run.return_value = MagicMock(returncode=0, stdout="ok", stderr="")
        cache = SimulationCache(cache_dir=tmp_path / "cache")
        run_dir = tmp_path / "run"
        model = runnable_model()
        simulate(model, weather_file, energyplus=mock_config, output_dir=run_dir)  # leftovers, no cache
        (run_dir / "notes.txt").write_text("unrelated\n")
        simulate(model, weather_file, energyplus=mock_config, output_dir=run_dir, cache=cache)
        simulate(model, weather_file, energyplus=mock_config, output_dir=run_dir, cache=cache)
        assert mock_run.call_count == 2


class TestSimulateCacheHitLocalOutputDir:
    """A local hit is copied into ``output_dir`` like a fresh run, and says it was cached."""

    @patch("idfkit.simulation.runner.run_process")
    def test_hit_is_copied_into_output_dir(
        self, mock_run: MagicMock, mock_config: EnergyPlusConfig, weather_file: Path, tmp_path: Path
    ) -> None:
        from idfkit.simulation.cache import CACHE_META_FILE, SimulationCache

        mock_run.return_value = MagicMock(returncode=0, stdout="ok", stderr="")
        cache = SimulationCache(cache_dir=tmp_path / "cache")
        model = runnable_model()

        first = simulate(model, weather_file, energyplus=mock_config, output_dir=tmp_path / "a", cache=cache)
        assert not first.cached
        second = simulate(model, weather_file, energyplus=mock_config, output_dir=tmp_path / "b", cache=cache)
        assert mock_run.call_count == 1
        assert second.cached
        assert "cached=True" in repr(second)
        assert second.run_dir == (tmp_path / "b").resolve()
        names_a = {p.name for p in first.run_dir.iterdir()}
        names_b = {p.name for p in second.run_dir.iterdir()}
        assert names_b == names_a
        assert CACHE_META_FILE not in names_b

        # Writing into the hit's run_dir leaves the cache entry intact.
        (second.run_dir / "model.idf").write_text("scribbled")
        third = simulate(model, weather_file, energyplus=mock_config, output_dir=tmp_path / "c", cache=cache)
        assert third.cached
        assert (third.run_dir / "model.idf").read_text() != "scribbled"

    @patch("idfkit.simulation.runner.run_process")
    def test_hit_without_output_dir_reads_the_entry_in_place(
        self, mock_run: MagicMock, mock_config: EnergyPlusConfig, weather_file: Path, tmp_path: Path
    ) -> None:
        """Without output_dir a hit copies nothing, so repeated hits do not fill the temp directory."""
        from idfkit.simulation.cache import SimulationCache

        mock_run.return_value = MagicMock(returncode=0, stdout="ok", stderr="")
        cache = SimulationCache(cache_dir=tmp_path / "cache")
        model = runnable_model()

        simulate(model, weather_file, energyplus=mock_config, cache=cache)
        with patch("idfkit.simulation._common.shutil.copytree") as copytree:
            hit = simulate(model, weather_file, energyplus=mock_config, cache=cache)
        copytree.assert_not_called()
        assert hit.cached
        assert (tmp_path / "cache").resolve() in hit.run_dir.resolve().parents
        assert (hit.run_dir / "model.idf").is_file()


class TestSimulateCacheWithFileSystem:
    """``cache=`` and ``fs=`` together: a miss is stored locally and a hit is uploaded to ``output_dir``."""

    @patch("idfkit.simulation.runner.run_process")
    def test_miss_stores_then_hit_uploads(
        self, mock_run: MagicMock, mock_config: EnergyPlusConfig, weather_file: Path, tmp_path: Path
    ) -> None:
        from idfkit.simulation.cache import CACHE_META_FILE, SimulationCache

        mock_run.return_value = MagicMock(returncode=0, stdout="ok", stderr="")
        cache = SimulationCache(cache_dir=tmp_path / "cache")
        fs = InMemoryFileSystem()
        model = runnable_model()

        first = simulate(model, weather_file, energyplus=mock_config, cache=cache, fs=fs, output_dir="runs/a")
        assert first.run_dir == Path("runs/a")
        assert first.fs is fs
        # The miss was stored from the local staging directory, not the remote path.
        assert len([p for p in (tmp_path / "cache").iterdir() if not p.name.startswith(".")]) == 1

        second = simulate(model, weather_file, energyplus=mock_config, cache=cache, fs=fs, output_dir="runs/b")
        assert mock_run.call_count == 1  # hit
        assert second.success
        assert second.cached
        assert not first.cached
        assert second.run_dir == Path("runs/b")
        assert second.fs is fs
        names_a = {k.removeprefix("runs/a/") for k in fs._files if k.startswith("runs/a/")}
        names_b = {k.removeprefix("runs/b/") for k in fs._files if k.startswith("runs/b/")}
        assert names_b
        assert names_b == names_a
        assert CACHE_META_FILE not in names_b

    @patch("idfkit.simulation.runner.run_process")
    def test_hit_uploads_from_entry_without_local_copy(
        self, mock_run: MagicMock, mock_config: EnergyPlusConfig, weather_file: Path, tmp_path: Path
    ) -> None:
        from idfkit.simulation.cache import SimulationCache

        mock_run.return_value = MagicMock(returncode=0, stdout="ok", stderr="")
        cache = SimulationCache(cache_dir=tmp_path / "cache")
        fs = InMemoryFileSystem()
        model = runnable_model()
        simulate(model, weather_file, energyplus=mock_config, cache=cache, fs=fs, output_dir="runs/a")
        with patch("idfkit.simulation.runner.restore_cached_result", side_effect=AssertionError("local copy")):
            hit = simulate(model, weather_file, energyplus=mock_config, cache=cache, fs=fs, output_dir="runs/b")
        assert hit.cached
        assert "runs/b/model.idf" in fs._files
        assert not [k for k in fs._files if k.endswith(".epw")]

    def test_put_failure_is_logged(self, tmp_path: Path, caplog: pytest.LogCaptureFixture) -> None:
        from idfkit.simulation.cache import CacheKey, SimulationCache
        from idfkit.simulation.result import SimulationResult

        cache = SimulationCache(cache_dir=tmp_path / "cache")
        result = SimulationResult(
            run_dir=tmp_path / "missing", success=True, exit_code=0, stdout="", stderr="", runtime_seconds=1.0
        )
        key = CacheKey(hex_digest="ab" * 32)
        with caplog.at_level(logging.WARNING, logger="idfkit.simulation.cache"):
            cache.put(key, result)
        assert not cache.contains(key)
        assert "Could not cache result" in caplog.text


def _simulation_control(model: IDFDocument) -> SimulationControl:
    control = model["SimulationControl"].first()
    assert control is not None
    return control


class TestDefaultModeAdmission:
    """Without annual or design_day, a model that gives EnergyPlus no environment is refused."""

    def test_new_document_is_refused_before_energyplus_starts(self, weather_file: Path) -> None:
        """new_document() seeds SimulationControl but no RunPeriod or design day: nothing would run."""
        with (
            patch("idfkit.simulation._common.find_energyplus") as mock_find,
            pytest.raises(SimulationError, match="nothing to simulate: it has no RunPeriod") as exc,
        ):
            simulate(new_document(), weather_file)
        mock_find.assert_not_called()
        assert 'model.add("RunPeriod"' in str(exc.value)
        assert "apply_to_model" in str(exc.value)

    @pytest.mark.parametrize("environment", ["RunPeriod", "SizingPeriod:DesignDay"])
    def test_one_environment_is_enough(
        self, environment: str, mock_config: EnergyPlusConfig, weather_file: Path, tmp_path: Path
    ) -> None:
        model = runnable_model() if environment == "RunPeriod" else design_day_model()
        with patch("idfkit.simulation.runner.run_process") as mock_run:
            mock_run.return_value = MagicMock(returncode=0, stdout="ok", stderr="")
            result = simulate(model, weather_file, energyplus=mock_config, output_dir=tmp_path / "run")
        assert result.success

    def test_run_period_turned_off_by_simulation_control(self, weather_file: Path) -> None:
        model = runnable_model()
        _simulation_control(model).update(run_simulation_for_weather_file_run_periods="No")
        with pytest.raises(SimulationError, match="SimulationControl turns off weather-file run periods"):
            simulate(model, weather_file)

    def test_sizing_only_run_is_admitted(self) -> None:
        """Sizing periods with every run flag off still size the HVAC when a sizing calculation is on."""
        from idfkit.simulation._common import admit_environments

        model = design_day_model()
        _simulation_control(model).update(
            do_zone_sizing_calculation="Yes",
            run_simulation_for_sizing_periods="No",
            run_simulation_for_weather_file_run_periods="No",
        )
        admit_environments(model, annual=False, design_day=False)
        _simulation_control(model).update(do_zone_sizing_calculation="No")
        with pytest.raises(SimulationError, match="turns off sizing periods"):
            admit_environments(model, annual=False, design_day=False)


class TestModelAdmission:
    """simulate() names its model argument when given something that is not a document."""

    @pytest.mark.parametrize("model", [None, "model.idf"])
    def test_non_document_raises_type_error(self, model: object, weather_file: Path) -> None:
        with pytest.raises(TypeError, match="model must be an IDFDocument, got"):
            simulate(model, weather_file)  # pyright: ignore[reportArgumentType]

    def test_path_hint(self, weather_file: Path) -> None:
        with pytest.raises(TypeError, match=r"load_idf\(path\)"):
            simulate("model.idf", weather_file)  # pyright: ignore[reportArgumentType]
