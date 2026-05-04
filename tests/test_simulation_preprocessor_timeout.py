"""Tests for the preprocessor_timeout parameter and IDFKIT_PREPROCESSOR_TIMEOUT env var.

Covers the resolution helper plus the forwarding through ``simulate()``,
``async_simulate()``, and the batch entry points.
"""

from __future__ import annotations

import asyncio
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from idfkit import LATEST_VERSION, new_document
from idfkit.simulation._common import (
    DEFAULT_PREPROCESSOR_TIMEOUT,
    PREPROCESSOR_TIMEOUT_ENV,
    resolve_preprocessor_timeout,
)
from idfkit.simulation.async_runner import async_simulate
from idfkit.simulation.batch import SimulationJob, simulate_batch
from idfkit.simulation.config import EnergyPlusConfig
from idfkit.simulation.runner import simulate


@pytest.fixture
def mock_config(tmp_path: Path) -> EnergyPlusConfig:
    """Mock EnergyPlusConfig with the executables required for preprocessing."""
    exe = tmp_path / "energyplus"
    exe.touch()
    exe.chmod(0o755)
    idd = tmp_path / "Energy+.idd"
    idd.write_text("!IDD_Version 24.1.0\n")

    expand_exe = tmp_path / "ExpandObjects"
    expand_exe.touch()
    expand_exe.chmod(0o755)

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
    epw = tmp_path / "weather.epw"
    epw.write_text("LOCATION,Test,US,Test,USA_TX,12345,30.0,-95.0,-6.0,10.0\n")
    return epw


@pytest.fixture
def slab_model():
    model = new_document(version=LATEST_VERSION)
    model.add("GroundHeatTransfer:Slab:Materials", "", {}, validate=False)
    model.add("Zone", "Office", {"x_origin": 0.0})
    return model


# ---------------------------------------------------------------------------
# resolve_preprocessor_timeout()
# ---------------------------------------------------------------------------


class TestResolvePreprocessorTimeout:
    def test_explicit_value_wins(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv(PREPROCESSOR_TIMEOUT_ENV, "999")
        assert resolve_preprocessor_timeout(42.0) == 42.0

    def test_falls_back_to_env_var(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv(PREPROCESSOR_TIMEOUT_ENV, "300")
        assert resolve_preprocessor_timeout(None) == 300.0

    def test_default_when_unset(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.delenv(PREPROCESSOR_TIMEOUT_ENV, raising=False)
        assert resolve_preprocessor_timeout(None) == DEFAULT_PREPROCESSOR_TIMEOUT

    def test_default_when_env_empty(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv(PREPROCESSOR_TIMEOUT_ENV, "")
        assert resolve_preprocessor_timeout(None) == DEFAULT_PREPROCESSOR_TIMEOUT

    def test_invalid_env_raises(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv(PREPROCESSOR_TIMEOUT_ENV, "not-a-number")
        with pytest.raises(ValueError, match=PREPROCESSOR_TIMEOUT_ENV):
            resolve_preprocessor_timeout(None)

    def test_non_positive_env_raises(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv(PREPROCESSOR_TIMEOUT_ENV, "0")
        with pytest.raises(ValueError, match="positive"):
            resolve_preprocessor_timeout(None)

    def test_explicit_value_bypasses_invalid_env(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Explicit caller value is returned even if env var is malformed (never read)."""
        monkeypatch.setenv(PREPROCESSOR_TIMEOUT_ENV, "garbage")
        assert resolve_preprocessor_timeout(60.0) == 60.0


# ---------------------------------------------------------------------------
# Forwarding through simulate()
# ---------------------------------------------------------------------------


class TestSimulateForwarding:
    def test_explicit_timeout_forwarded(self, mock_config: EnergyPlusConfig, weather_file: Path, slab_model) -> None:
        preprocessed = new_document(version=LATEST_VERSION)
        preprocessed.add("Zone", "Office", {"x_origin": 0.0})
        sim_proc = MagicMock(returncode=0, stdout="ok", stderr="")

        with (
            patch("idfkit.simulation.expand.run_preprocessing", return_value=preprocessed) as mock_pp,
            patch("idfkit.simulation.runner.subprocess.run", return_value=sim_proc),
        ):
            simulate(slab_model, weather_file, energyplus=mock_config, preprocessor_timeout=300.0)

        assert mock_pp.call_args.kwargs["timeout"] == 300.0

    def test_env_var_used_when_param_omitted(
        self,
        mock_config: EnergyPlusConfig,
        weather_file: Path,
        slab_model,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        monkeypatch.setenv(PREPROCESSOR_TIMEOUT_ENV, "450")
        preprocessed = new_document(version=LATEST_VERSION)
        preprocessed.add("Zone", "Office", {"x_origin": 0.0})
        sim_proc = MagicMock(returncode=0, stdout="ok", stderr="")

        with (
            patch("idfkit.simulation.expand.run_preprocessing", return_value=preprocessed) as mock_pp,
            patch("idfkit.simulation.runner.subprocess.run", return_value=sim_proc),
        ):
            simulate(slab_model, weather_file, energyplus=mock_config)

        assert mock_pp.call_args.kwargs["timeout"] == 450.0

    def test_default_when_unset(
        self,
        mock_config: EnergyPlusConfig,
        weather_file: Path,
        slab_model,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        monkeypatch.delenv(PREPROCESSOR_TIMEOUT_ENV, raising=False)
        preprocessed = new_document(version=LATEST_VERSION)
        preprocessed.add("Zone", "Office", {"x_origin": 0.0})
        sim_proc = MagicMock(returncode=0, stdout="ok", stderr="")

        with (
            patch("idfkit.simulation.expand.run_preprocessing", return_value=preprocessed) as mock_pp,
            patch("idfkit.simulation.runner.subprocess.run", return_value=sim_proc),
        ):
            simulate(slab_model, weather_file, energyplus=mock_config)

        assert mock_pp.call_args.kwargs["timeout"] == DEFAULT_PREPROCESSOR_TIMEOUT


# ---------------------------------------------------------------------------
# Forwarding through async_simulate()
# ---------------------------------------------------------------------------


class TestAsyncSimulateForwarding:
    def test_explicit_timeout_forwarded(self, mock_config: EnergyPlusConfig, weather_file: Path, slab_model) -> None:
        preprocessed = new_document(version=LATEST_VERSION)
        preprocessed.add("Zone", "Office", {"x_origin": 0.0})

        async def fake_simple(_cmd: list[str], _cwd: Path, _timeout: float):
            return "ok", "", 0

        with (
            patch("idfkit.simulation.expand.run_preprocessing", return_value=preprocessed) as mock_pp,
            patch("idfkit.simulation.async_runner._run_simple", side_effect=fake_simple),
        ):
            asyncio.run(async_simulate(slab_model, weather_file, energyplus=mock_config, preprocessor_timeout=222.0))

        assert mock_pp.call_args.kwargs["timeout"] == 222.0


# ---------------------------------------------------------------------------
# Forwarding through SimulationJob / simulate_batch()
# ---------------------------------------------------------------------------


class TestBatchForwarding:
    def test_simulationjob_default_is_none(self) -> None:
        model = new_document(version=LATEST_VERSION)
        job = SimulationJob(model=model, weather="weather.epw")
        assert job.preprocessor_timeout is None

    def test_batch_forwards_per_job_timeout(
        self, mock_config: EnergyPlusConfig, weather_file: Path, slab_model
    ) -> None:
        preprocessed = new_document(version=LATEST_VERSION)
        preprocessed.add("Zone", "Office", {"x_origin": 0.0})
        sim_proc = MagicMock(returncode=0, stdout="ok", stderr="")
        job = SimulationJob(model=slab_model, weather=weather_file, preprocessor_timeout=180.0)

        with (
            patch("idfkit.simulation.expand.run_preprocessing", return_value=preprocessed) as mock_pp,
            patch("idfkit.simulation.runner.subprocess.run", return_value=sim_proc),
        ):
            simulate_batch([job], energyplus=mock_config, max_workers=1)

        assert mock_pp.call_args.kwargs["timeout"] == 180.0
