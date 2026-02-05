"""Tests for the batch simulation module."""

from __future__ import annotations

from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
from conftest import InMemoryFileSystem

from idfkit import new_document
from idfkit.simulation.batch import BatchResult, SimulationJob, simulate_batch
from idfkit.simulation.cache import SimulationCache
from idfkit.simulation.config import EnergyPlusConfig
from idfkit.simulation.result import SimulationResult

# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


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
# SimulationJob
# ---------------------------------------------------------------------------


class TestSimulationJob:
    """Tests for SimulationJob dataclass."""

    def test_frozen(self) -> None:
        model = new_document()
        job = SimulationJob(model=model, weather="test.epw")
        with pytest.raises(AttributeError):
            job.label = "changed"  # type: ignore[misc]

    def test_defaults(self) -> None:
        model = new_document()
        job = SimulationJob(model=model, weather="test.epw")
        assert job.label == ""
        assert job.output_dir is None
        assert job.expand_objects is True
        assert job.annual is False
        assert job.design_day is False
        assert job.output_prefix == "eplus"
        assert job.output_suffix == "C"
        assert job.readvars is False
        assert job.timeout == 3600.0
        assert job.extra_args is None

    def test_custom_fields(self) -> None:
        model = new_document()
        job = SimulationJob(
            model=model,
            weather="/path/to/w.epw",
            label="test-job",
            annual=True,
            extra_args=("--custom",),
        )
        assert job.label == "test-job"
        assert job.annual is True
        assert job.extra_args == ("--custom",)


# ---------------------------------------------------------------------------
# BatchResult
# ---------------------------------------------------------------------------


class TestBatchResult:
    """Tests for BatchResult dataclass."""

    @pytest.fixture
    def mixed_results(self, tmp_path: Path) -> tuple[SimulationResult, SimulationResult, SimulationResult]:
        ok1 = SimulationResult(
            run_dir=tmp_path / "r1", success=True, exit_code=0, stdout="", stderr="", runtime_seconds=1.0
        )
        fail = SimulationResult(
            run_dir=tmp_path / "r2", success=False, exit_code=1, stdout="", stderr="err", runtime_seconds=0.5
        )
        ok2 = SimulationResult(
            run_dir=tmp_path / "r3", success=True, exit_code=0, stdout="", stderr="", runtime_seconds=2.0
        )
        return ok1, fail, ok2

    def test_succeeded(self, mixed_results: tuple[SimulationResult, ...]) -> None:
        br = BatchResult(results=mixed_results, total_runtime_seconds=3.5)
        assert len(br.succeeded) == 2

    def test_failed(self, mixed_results: tuple[SimulationResult, ...]) -> None:
        br = BatchResult(results=mixed_results, total_runtime_seconds=3.5)
        assert len(br.failed) == 1

    def test_all_succeeded_false(self, mixed_results: tuple[SimulationResult, ...]) -> None:
        br = BatchResult(results=mixed_results, total_runtime_seconds=3.5)
        assert not br.all_succeeded

    def test_all_succeeded_true(self, tmp_path: Path) -> None:
        r = SimulationResult(run_dir=tmp_path, success=True, exit_code=0, stdout="", stderr="", runtime_seconds=1.0)
        br = BatchResult(results=(r,), total_runtime_seconds=1.0)
        assert br.all_succeeded

    def test_len(self, mixed_results: tuple[SimulationResult, ...]) -> None:
        br = BatchResult(results=mixed_results, total_runtime_seconds=3.5)
        assert len(br) == 3

    def test_getitem(self, mixed_results: tuple[SimulationResult, ...]) -> None:
        br = BatchResult(results=mixed_results, total_runtime_seconds=3.5)
        assert br[0] is mixed_results[0]
        assert br[1] is mixed_results[1]
        assert br[2] is mixed_results[2]


# ---------------------------------------------------------------------------
# simulate_batch
# ---------------------------------------------------------------------------


class TestSimulateBatch:
    """Tests for simulate_batch()."""

    def test_empty_jobs_raises(self) -> None:
        with pytest.raises(ValueError, match="jobs must not be empty"):
            simulate_batch([])

    @patch("idfkit.simulation.runner.subprocess.run")
    def test_single_job(self, mock_run: MagicMock, mock_config: EnergyPlusConfig, weather_file: Path) -> None:
        mock_run.return_value = MagicMock(returncode=0, stdout="ok", stderr="")
        model = new_document()
        job = SimulationJob(model=model, weather=weather_file, label="single")
        result = simulate_batch([job], energyplus=mock_config)
        assert len(result) == 1
        assert result[0].success
        assert result.all_succeeded

    @patch("idfkit.simulation.runner.subprocess.run")
    def test_multiple_jobs(self, mock_run: MagicMock, mock_config: EnergyPlusConfig, weather_file: Path) -> None:
        mock_run.return_value = MagicMock(returncode=0, stdout="ok", stderr="")
        jobs = [SimulationJob(model=new_document(), weather=weather_file, label=f"job-{i}") for i in range(3)]
        result = simulate_batch(jobs, energyplus=mock_config)
        assert len(result) == 3
        assert result.all_succeeded

    @patch("idfkit.simulation.runner.subprocess.run")
    def test_preserves_order(self, mock_run: MagicMock, mock_config: EnergyPlusConfig, weather_file: Path) -> None:
        """Results should be in the same order as input jobs."""
        call_count = 0

        def side_effect(*_args: object, **_kwargs: object) -> MagicMock:
            nonlocal call_count
            call_count += 1
            return MagicMock(returncode=0, stdout=f"run-{call_count}", stderr="")

        mock_run.side_effect = side_effect
        jobs = [SimulationJob(model=new_document(), weather=weather_file, label=f"job-{i}") for i in range(3)]
        result = simulate_batch(jobs, energyplus=mock_config, max_workers=1)
        # With max_workers=1 the order is deterministic
        assert result[0].stdout == "run-1"
        assert result[1].stdout == "run-2"
        assert result[2].stdout == "run-3"

    @patch("idfkit.simulation.runner.subprocess.run")
    def test_failed_job_does_not_cancel_others(
        self, mock_run: MagicMock, mock_config: EnergyPlusConfig, weather_file: Path
    ) -> None:
        """A single job failure should not prevent other jobs from running."""
        returns = [
            MagicMock(returncode=0, stdout="ok", stderr=""),
            MagicMock(returncode=1, stdout="", stderr="failed"),
            MagicMock(returncode=0, stdout="ok", stderr=""),
        ]
        mock_run.side_effect = returns

        jobs = [SimulationJob(model=new_document(), weather=weather_file, label=f"job-{i}") for i in range(3)]
        result = simulate_batch(jobs, energyplus=mock_config, max_workers=1)
        assert len(result) == 3
        assert not result.all_succeeded
        assert len(result.succeeded) == 2
        assert len(result.failed) == 1

    @patch("idfkit.simulation.runner.subprocess.run")
    def test_progress_callback(self, mock_run: MagicMock, mock_config: EnergyPlusConfig, weather_file: Path) -> None:
        mock_run.return_value = MagicMock(returncode=0, stdout="", stderr="")
        progress_calls: list[dict[str, object]] = []

        def on_progress(**kwargs: object) -> None:
            progress_calls.append(kwargs)

        jobs = [SimulationJob(model=new_document(), weather=weather_file, label=f"job-{i}") for i in range(2)]
        simulate_batch(jobs, energyplus=mock_config, progress=on_progress, max_workers=1)

        assert len(progress_calls) == 2
        # Both should report total=2
        assert all(c["total"] == 2 for c in progress_calls)
        # completed should be 1 and 2 (in some order)
        completed_values = sorted(c["completed"] for c in progress_calls)
        assert completed_values == [1, 2]
        # All succeeded
        assert all(c["success"] is True for c in progress_calls)

    @patch("idfkit.simulation.runner.subprocess.run")
    def test_cache_integration(
        self, mock_run: MagicMock, mock_config: EnergyPlusConfig, weather_file: Path, tmp_path: Path
    ) -> None:
        """Cache should be passed through to simulate()."""
        mock_run.return_value = MagicMock(returncode=0, stdout="ok", stderr="")
        cache = SimulationCache(cache_dir=tmp_path / "cache")
        model = new_document()
        job = SimulationJob(model=model, weather=weather_file, label="cached")

        # First run — miss, then store
        result1 = simulate_batch([job], energyplus=mock_config, cache=cache)
        assert result1[0].success
        assert mock_run.call_count == 1

        # Second run — cache hit, subprocess not called again
        result2 = simulate_batch([job], energyplus=mock_config, cache=cache)
        assert result2[0].success
        assert mock_run.call_count == 1  # no additional call

    @patch("idfkit.simulation.runner.subprocess.run")
    def test_total_runtime_populated(
        self, mock_run: MagicMock, mock_config: EnergyPlusConfig, weather_file: Path
    ) -> None:
        mock_run.return_value = MagicMock(returncode=0, stdout="", stderr="")
        job = SimulationJob(model=new_document(), weather=weather_file)
        result = simulate_batch([job], energyplus=mock_config)
        assert result.total_runtime_seconds >= 0

    @patch("idfkit.simulation.runner.subprocess.run")
    def test_batch_passes_fs_to_simulate(
        self, mock_run: MagicMock, mock_config: EnergyPlusConfig, weather_file: Path
    ) -> None:
        """When fs is passed to simulate_batch, results should carry the fs."""
        mock_run.return_value = MagicMock(returncode=0, stdout="ok", stderr="")
        fs = InMemoryFileSystem()
        job = SimulationJob(model=new_document(), weather=weather_file, output_dir="remote/batch/0")
        result = simulate_batch([job], energyplus=mock_config, fs=fs, max_workers=1)
        assert result[0].success
        assert result[0].fs is fs
