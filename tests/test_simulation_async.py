"""Tests for the async EnergyPlus simulation runner and batch modules."""

from __future__ import annotations

import asyncio
import logging
import re
import tempfile
from pathlib import Path
from typing import TYPE_CHECKING, Any
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from conftest import (
    REFUSAL_R1,
    REFUSAL_R2,
    InMemoryAsyncFileSystem,
    InMemoryFileSystem,
    ground_heat_model,
    refusal_r3,
    refusal_r4,
)

from idfkit import LATEST_VERSION, new_document
from idfkit.exceptions import SimulationError
from idfkit.simulation.async_batch import SimulationEvent, async_simulate_batch, async_simulate_batch_stream
from idfkit.simulation.async_runner import async_simulate
from idfkit.simulation.batch import REFUSED_RUN_DIR, SimulationJob
from idfkit.simulation.cache import SimulationCache
from idfkit.simulation.config import EnergyPlusConfig

if TYPE_CHECKING:
    pass


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


def _make_mock_process(returncode: int = 0, stdout: bytes = b"ok", stderr: bytes = b"") -> MagicMock:
    """Create a mock asyncio.subprocess.Process."""
    proc = MagicMock()
    proc.communicate = AsyncMock(return_value=(stdout, stderr))
    proc.returncode = returncode
    proc.kill = MagicMock()
    proc.wait = AsyncMock()
    return proc


# ---------------------------------------------------------------------------
# async_simulate
# ---------------------------------------------------------------------------


class TestAsyncSimulate:
    """Tests for async_simulate()."""

    @pytest.mark.asyncio
    @patch("idfkit.simulation.async_runner.asyncio.create_subprocess_exec")
    async def test_success(self, mock_exec: AsyncMock, mock_config: EnergyPlusConfig, weather_file: Path) -> None:
        mock_exec.return_value = _make_mock_process(returncode=0)
        model = new_document()
        result = await async_simulate(model, weather_file, energyplus=mock_config)
        assert result.success
        assert result.exit_code == 0
        mock_exec.assert_called_once()

    @pytest.mark.asyncio
    @patch("idfkit.simulation.async_runner.asyncio.create_subprocess_exec")
    async def test_failure(self, mock_exec: AsyncMock, mock_config: EnergyPlusConfig, weather_file: Path) -> None:
        mock_exec.return_value = _make_mock_process(returncode=1, stderr=b"error occurred")
        model = new_document()
        result = await async_simulate(model, weather_file, energyplus=mock_config)
        assert not result.success
        assert result.exit_code == 1

    @pytest.mark.asyncio
    @patch("idfkit.simulation.async_runner.asyncio.create_subprocess_exec")
    async def test_timeout(self, mock_exec: AsyncMock, mock_config: EnergyPlusConfig, weather_file: Path) -> None:
        proc = _make_mock_process()
        proc.communicate = AsyncMock(side_effect=asyncio.TimeoutError)
        mock_exec.return_value = proc
        model = new_document()

        with pytest.raises(SimulationError, match="timed out"):
            await async_simulate(model, weather_file, energyplus=mock_config, timeout=10)

        proc.kill.assert_called_once()

    @pytest.mark.asyncio
    async def test_missing_weather(self, mock_config: EnergyPlusConfig) -> None:
        model = new_document()
        with pytest.raises(SimulationError, match="Weather file not found"):
            await async_simulate(model, "/nonexistent/weather.epw", energyplus=mock_config)

    @pytest.mark.asyncio
    @patch("idfkit.simulation.async_runner.asyncio.create_subprocess_exec")
    async def test_model_not_mutated(
        self, mock_exec: AsyncMock, mock_config: EnergyPlusConfig, weather_file: Path
    ) -> None:
        mock_exec.return_value = _make_mock_process()
        model = new_document()
        assert "Output:SQLite" not in model
        await async_simulate(model, weather_file, energyplus=mock_config)
        assert "Output:SQLite" not in model

    @pytest.mark.asyncio
    async def test_fs_requires_output_dir(self, mock_config: EnergyPlusConfig, weather_file: Path) -> None:
        fs = InMemoryFileSystem()
        model = new_document()
        with pytest.raises(ValueError, match="output_dir is required"):
            await async_simulate(model, weather_file, energyplus=mock_config, fs=fs)

    @pytest.mark.asyncio
    @patch("idfkit.simulation.async_runner.asyncio.create_subprocess_exec")
    async def test_simulate_with_fs_uploads_results(
        self, mock_exec: AsyncMock, mock_config: EnergyPlusConfig, weather_file: Path
    ) -> None:
        mock_exec.return_value = _make_mock_process()
        fs = InMemoryFileSystem()
        model = new_document()
        result = await async_simulate(
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
        assert len(uploaded) > 0

    @pytest.mark.asyncio
    @patch("idfkit.simulation.async_runner.asyncio.create_subprocess_exec")
    async def test_stdout_stderr_captured(
        self, mock_exec: AsyncMock, mock_config: EnergyPlusConfig, weather_file: Path
    ) -> None:
        mock_exec.return_value = _make_mock_process(returncode=0, stdout=b"simulation output", stderr=b"some warnings")
        model = new_document()
        result = await async_simulate(model, weather_file, energyplus=mock_config)
        assert result.stdout == "simulation output"
        assert result.stderr == "some warnings"

    @pytest.mark.asyncio
    @patch("idfkit.simulation.async_runner.asyncio.create_subprocess_exec")
    async def test_runtime_tracked(
        self, mock_exec: AsyncMock, mock_config: EnergyPlusConfig, weather_file: Path
    ) -> None:
        mock_exec.return_value = _make_mock_process()
        model = new_document()
        result = await async_simulate(model, weather_file, energyplus=mock_config)
        assert result.runtime_seconds >= 0


# ---------------------------------------------------------------------------
# async_simulate_batch
# ---------------------------------------------------------------------------


class TestAsyncSimulateBatch:
    """Tests for async_simulate_batch()."""

    @pytest.mark.asyncio
    async def test_empty_jobs_raises(self) -> None:
        with pytest.raises(ValueError, match="jobs must not be empty"):
            await async_simulate_batch([])

    @pytest.mark.asyncio
    @patch("idfkit.simulation.async_runner.asyncio.create_subprocess_exec")
    async def test_single_job(self, mock_exec: AsyncMock, mock_config: EnergyPlusConfig, weather_file: Path) -> None:
        mock_exec.return_value = _make_mock_process()
        model = new_document()
        job = SimulationJob(model=model, weather=weather_file, label="single")
        result = await async_simulate_batch([job], energyplus=mock_config)
        assert len(result) == 1
        assert result[0].success
        assert result.all_succeeded

    @pytest.mark.asyncio
    @patch("idfkit.simulation.async_runner.asyncio.create_subprocess_exec")
    async def test_multiple_jobs(self, mock_exec: AsyncMock, mock_config: EnergyPlusConfig, weather_file: Path) -> None:
        mock_exec.return_value = _make_mock_process()
        jobs = [SimulationJob(model=new_document(), weather=weather_file, label=f"job-{i}") for i in range(3)]
        result = await async_simulate_batch(jobs, energyplus=mock_config)
        assert len(result) == 3
        assert result.all_succeeded

    @pytest.mark.asyncio
    @patch("idfkit.simulation.async_runner.asyncio.create_subprocess_exec")
    async def test_preserves_order(
        self, mock_exec: AsyncMock, mock_config: EnergyPlusConfig, weather_file: Path
    ) -> None:
        """Results should be in the same order as input jobs."""
        call_count = 0

        async def make_proc(*_args: object, **_kwargs: object) -> MagicMock:
            nonlocal call_count
            call_count += 1
            return _make_mock_process(stdout=f"run-{call_count}".encode())

        mock_exec.side_effect = make_proc
        jobs = [SimulationJob(model=new_document(), weather=weather_file, label=f"job-{i}") for i in range(3)]
        result = await async_simulate_batch(jobs, energyplus=mock_config, max_concurrent=1)
        assert result[0].stdout == "run-1"
        assert result[1].stdout == "run-2"
        assert result[2].stdout == "run-3"

    @pytest.mark.asyncio
    @patch("idfkit.simulation.async_runner.asyncio.create_subprocess_exec")
    async def test_failed_job_does_not_cancel_others(
        self, mock_exec: AsyncMock, mock_config: EnergyPlusConfig, weather_file: Path
    ) -> None:
        call_count = 0

        async def make_proc(*_args: object, **_kwargs: object) -> MagicMock:
            nonlocal call_count
            call_count += 1
            if call_count == 2:
                return _make_mock_process(returncode=1, stderr=b"failed")
            return _make_mock_process()

        mock_exec.side_effect = make_proc
        jobs = [SimulationJob(model=new_document(), weather=weather_file, label=f"job-{i}") for i in range(3)]
        result = await async_simulate_batch(jobs, energyplus=mock_config, max_concurrent=1)
        assert len(result) == 3
        assert not result.all_succeeded
        assert len(result.succeeded) == 2
        assert len(result.failed) == 1

    @pytest.mark.asyncio
    @patch("idfkit.simulation.async_runner.asyncio.create_subprocess_exec")
    async def test_total_runtime_populated(
        self, mock_exec: AsyncMock, mock_config: EnergyPlusConfig, weather_file: Path
    ) -> None:
        mock_exec.return_value = _make_mock_process()
        job = SimulationJob(model=new_document(), weather=weather_file)
        result = await async_simulate_batch([job], energyplus=mock_config)
        assert result.total_runtime_seconds >= 0

    @pytest.mark.asyncio
    async def test_refused_job_creates_no_directory(
        self, mock_config: EnergyPlusConfig, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """A job refused before EnergyPlus runs leaves no temporary directory behind (#228)."""
        temp_root = tmp_path / "tmp"
        temp_root.mkdir()
        monkeypatch.setattr(tempfile, "tempdir", str(temp_root))
        jobs = [SimulationJob(model=new_document(), annual=True, label=f"annual-{i}") for i in range(3)]
        result = await async_simulate_batch(jobs, energyplus=mock_config)
        assert not any(r.success for r in result)
        assert list(temp_root.iterdir()) == []
        assert all(r.run_dir == REFUSED_RUN_DIR for r in result)
        assert not REFUSED_RUN_DIR.exists()
        assert (await result[0].async_errors()).fatal_count == 0

    @pytest.mark.asyncio
    @patch("idfkit.simulation.async_runner.asyncio.create_subprocess_exec")
    async def test_cache_integration(
        self, mock_exec: AsyncMock, mock_config: EnergyPlusConfig, weather_file: Path, tmp_path: Path
    ) -> None:
        mock_exec.return_value = _make_mock_process()
        cache = SimulationCache(cache_dir=tmp_path / "cache")
        model = new_document()
        job = SimulationJob(model=model, weather=weather_file, label="cached")

        # First run — miss, then store
        result1 = await async_simulate_batch([job], energyplus=mock_config, cache=cache)
        assert result1[0].success
        assert mock_exec.call_count == 1

        # Second run — cache hit, subprocess not called again
        result2 = await async_simulate_batch([job], energyplus=mock_config, cache=cache)
        assert result2[0].success
        assert mock_exec.call_count == 1  # no additional call


class TestAsyncSimulateCacheCoversExternalFiles:
    """async_simulate hashes the files the model names into the cache key (#216)."""

    @pytest.mark.asyncio
    @patch("idfkit.simulation.async_runner.asyncio.create_subprocess_exec")
    async def test_staged_file_in_output_dir(
        self, mock_exec: AsyncMock, mock_config: EnergyPlusConfig, weather_file: Path, tmp_path: Path
    ) -> None:
        mock_exec.return_value = _make_mock_process()
        cache = SimulationCache(cache_dir=tmp_path / "cache")
        run_dir = tmp_path / "run"
        run_dir.mkdir()
        csv = run_dir / "hourly.csv"
        model = new_document()
        model.add("Schedule:File", "Staged", file_name="hourly.csv", column_number=1, validate=False)

        async def run() -> None:
            await async_simulate(model, weather_file, energyplus=mock_config, output_dir=run_dir, cache=cache)

        csv.write_text("1\n")
        await run()
        await run()
        assert mock_exec.call_count == 1
        csv.write_text("2\n")
        await run()
        assert mock_exec.call_count == 2

    @pytest.mark.asyncio
    @patch("idfkit.simulation.async_runner.asyncio.create_subprocess_exec")
    async def test_batch_job_with_cosimulation_is_never_cached(
        self, mock_exec: AsyncMock, mock_config: EnergyPlusConfig, weather_file: Path, tmp_path: Path
    ) -> None:
        mock_exec.return_value = _make_mock_process()
        cache = SimulationCache(cache_dir=tmp_path / "cache")
        model = new_document()
        model.add("ExternalInterface", "", name_of_external_interface="PtolemyServer", validate=False)
        job = SimulationJob(model=model, weather=weather_file)

        await async_simulate_batch([job], energyplus=mock_config, cache=cache)
        await async_simulate_batch([job], energyplus=mock_config, cache=cache)
        assert mock_exec.call_count == 2


# ---------------------------------------------------------------------------
# async_simulate_batch_stream
# ---------------------------------------------------------------------------


class TestAsyncSimulateBatchStream:
    """Tests for async_simulate_batch_stream()."""

    @pytest.mark.asyncio
    async def test_empty_jobs_raises(self) -> None:
        with pytest.raises(ValueError, match="jobs must not be empty"):
            async for _ in async_simulate_batch_stream([]):
                pass  # pragma: no cover

    @pytest.mark.asyncio
    @patch("idfkit.simulation.async_runner.asyncio.create_subprocess_exec")
    async def test_yields_all_events(
        self, mock_exec: AsyncMock, mock_config: EnergyPlusConfig, weather_file: Path
    ) -> None:
        mock_exec.return_value = _make_mock_process()
        jobs = [SimulationJob(model=new_document(), weather=weather_file, label=f"job-{i}") for i in range(3)]
        events: list[SimulationEvent] = []
        async for event in async_simulate_batch_stream(jobs, energyplus=mock_config):
            events.append(event)

        assert len(events) == 3
        # Each event should have correct total
        assert all(e.total == 3 for e in events)
        # Completed counts should reach 3
        completed_values = sorted(e.completed for e in events)
        assert completed_values == [1, 2, 3]
        # All indices should be present
        assert sorted(e.index for e in events) == [0, 1, 2]

    @pytest.mark.asyncio
    @patch("idfkit.simulation.async_runner.asyncio.create_subprocess_exec")
    async def test_event_contains_result(
        self, mock_exec: AsyncMock, mock_config: EnergyPlusConfig, weather_file: Path
    ) -> None:
        mock_exec.return_value = _make_mock_process()
        job = SimulationJob(model=new_document(), weather=weather_file, label="test-stream")
        events: list[SimulationEvent] = []
        async for event in async_simulate_batch_stream([job], energyplus=mock_config):
            events.append(event)

        assert len(events) == 1
        assert events[0].label == "test-stream"
        assert events[0].result.success
        assert events[0].index == 0
        assert events[0].completed == 1
        assert events[0].total == 1

    @pytest.mark.asyncio
    @patch("idfkit.simulation.async_runner.asyncio.create_subprocess_exec")
    async def test_early_break_cancels_remaining(
        self, mock_exec: AsyncMock, mock_config: EnergyPlusConfig, weather_file: Path
    ) -> None:
        """Breaking out of the stream should cancel remaining tasks."""
        call_count = 0

        async def slow_proc(*_args: object, **_kwargs: object) -> MagicMock:
            nonlocal call_count
            call_count += 1
            proc = _make_mock_process()
            if call_count > 1:
                # Make subsequent calls slow so they're still pending when we break
                original_communicate = proc.communicate

                async def slow_communicate() -> tuple[bytes, bytes]:
                    await asyncio.sleep(10)
                    return await original_communicate()

                proc.communicate = slow_communicate
            return proc

        mock_exec.side_effect = slow_proc
        jobs = [SimulationJob(model=new_document(), weather=weather_file, label=f"job-{i}") for i in range(5)]

        events: list[SimulationEvent] = []
        async for event in async_simulate_batch_stream(jobs, energyplus=mock_config, max_concurrent=1):
            events.append(event)
            break  # Only take the first result

        # Should have gotten exactly one event
        assert len(events) == 1


# ---------------------------------------------------------------------------
# SimulationEvent
# ---------------------------------------------------------------------------


class TestSimulationEvent:
    """Tests for SimulationEvent dataclass."""

    def test_frozen(self, tmp_path: Path) -> None:
        result = MagicMock()
        event = SimulationEvent(index=0, label="test", result=result, completed=1, total=1)
        with pytest.raises(AttributeError):
            event.label = "changed"  # type: ignore[misc]

    def test_fields(self, tmp_path: Path) -> None:
        result = MagicMock()
        event = SimulationEvent(index=2, label="my-sim", result=result, completed=3, total=5)
        assert event.index == 2
        assert event.label == "my-sim"
        assert event.result is result
        assert event.completed == 3
        assert event.total == 5


# ---------------------------------------------------------------------------
# AsyncFileSystem integration
# ---------------------------------------------------------------------------


class TestAsyncFileSystem:
    """Tests for async file system support in async_simulate()."""

    @pytest.mark.asyncio
    @patch("idfkit.simulation.async_runner.asyncio.create_subprocess_exec")
    async def test_simulate_with_async_fs_uploads_results(
        self, mock_exec: AsyncMock, mock_config: EnergyPlusConfig, weather_file: Path
    ) -> None:
        """async_simulate with an AsyncFileSystem should upload without blocking."""
        mock_exec.return_value = _make_mock_process()
        fs = InMemoryAsyncFileSystem()
        model = new_document()
        result = await async_simulate(
            model,
            weather_file,
            energyplus=mock_config,
            output_dir="remote/output",
            fs=fs,
        )
        assert result.success
        assert result.async_fs is fs
        assert result.fs is None
        assert result.run_dir == Path("remote/output")
        uploaded = [k for k in fs._files if k.startswith("remote/output/")]
        assert len(uploaded) > 0

    @pytest.mark.asyncio
    @patch("idfkit.simulation.async_runner.asyncio.create_subprocess_exec")
    async def test_simulate_with_sync_fs_wraps_in_thread(
        self, mock_exec: AsyncMock, mock_config: EnergyPlusConfig, weather_file: Path
    ) -> None:
        """async_simulate with a sync FileSystem should wrap upload in to_thread."""
        mock_exec.return_value = _make_mock_process()
        fs = InMemoryFileSystem()
        model = new_document()
        result = await async_simulate(
            model,
            weather_file,
            energyplus=mock_config,
            output_dir="remote/output",
            fs=fs,
        )
        assert result.success
        assert result.fs is fs
        assert result.async_fs is None
        assert result.run_dir == Path("remote/output")
        uploaded = [k for k in fs._files if k.startswith("remote/output/")]
        assert len(uploaded) > 0

    @pytest.mark.asyncio
    @patch("idfkit.simulation.async_runner.asyncio.create_subprocess_exec")
    async def test_async_fs_result_has_async_accessors(
        self, mock_exec: AsyncMock, mock_config: EnergyPlusConfig, weather_file: Path
    ) -> None:
        """SimulationResult from async fs should support async_errors() etc."""
        mock_exec.return_value = _make_mock_process()
        fs = InMemoryAsyncFileSystem()
        model = new_document()
        result = await async_simulate(
            model,
            weather_file,
            energyplus=mock_config,
            output_dir="remote/output",
            fs=fs,
        )
        # async_errors should not raise (even if no .err file exists)
        errors = await result.async_errors()
        assert errors is not None

    @pytest.mark.asyncio
    @patch("idfkit.simulation.async_runner.asyncio.create_subprocess_exec")
    async def test_async_batch_with_async_fs(
        self, mock_exec: AsyncMock, mock_config: EnergyPlusConfig, weather_file: Path
    ) -> None:
        """async_simulate_batch should accept an AsyncFileSystem."""
        mock_exec.return_value = _make_mock_process()
        fs = InMemoryAsyncFileSystem()
        jobs = [
            SimulationJob(model=new_document(), weather=weather_file, label="job-0", output_dir="batch/run-0"),
            SimulationJob(model=new_document(), weather=weather_file, label="job-1", output_dir="batch/run-1"),
        ]
        result = await async_simulate_batch(jobs, energyplus=mock_config, fs=fs)
        assert len(result) == 2
        assert result.all_succeeded
        # Both should have used the async fs
        for r in result.results:
            assert r.async_fs is fs

    @pytest.mark.asyncio
    async def test_sync_property_raises_when_only_async_fs_set(self) -> None:
        """Accessing sync properties on an async_fs-only result should raise."""
        from idfkit.simulation.result import SimulationResult

        fs = InMemoryAsyncFileSystem()
        result = SimulationResult(
            run_dir=Path("remote/output"),
            success=True,
            exit_code=0,
            stdout="",
            stderr="",
            runtime_seconds=0.0,
            async_fs=fs,
        )
        with pytest.raises(RuntimeError, match="async accessors"):
            _ = result.errors
        with pytest.raises(RuntimeError, match="async accessors"):
            _ = result.sql

    @pytest.mark.asyncio
    async def test_async_errors_with_actual_data(self) -> None:
        """async_errors should parse .err content from an async fs."""
        from idfkit.simulation.result import SimulationResult

        fs = InMemoryAsyncFileSystem()
        await fs.write_text(
            "run/eplusout.err",
            "Program Version,EnergyPlus, 24.1\n   ************* EnergyPlus Completed Successfully.\n",
        )
        result = SimulationResult(
            run_dir=Path("run"),
            success=True,
            exit_code=0,
            stdout="",
            stderr="",
            runtime_seconds=0.0,
            async_fs=fs,
        )
        errors = await result.async_errors()
        assert "completed successfully" in errors.summary()

    @pytest.mark.asyncio
    async def test_async_csv_with_actual_data(self) -> None:
        """async_csv should parse .csv content from an async fs."""
        from idfkit.simulation.result import SimulationResult

        fs = InMemoryAsyncFileSystem()
        csv_content = "Date/Time,Zone Mean Air Temperature [C](TimeStep)\n 01/01  01:00:00,21.5\n"
        await fs.write_text("run/eplusout.csv", csv_content)
        result = SimulationResult(
            run_dir=Path("run"),
            success=True,
            exit_code=0,
            stdout="",
            stderr="",
            runtime_seconds=0.0,
            async_fs=fs,
        )
        csv_result = await result.async_csv()
        assert csv_result is not None
        assert len(csv_result.columns) > 0

    @pytest.mark.asyncio
    async def test_async_variables_with_actual_data(self) -> None:
        """async_variables should parse .rdd content from an async fs."""
        from idfkit.simulation.result import SimulationResult

        fs = InMemoryAsyncFileSystem()
        rdd_content = "! Program Version,EnergyPlus, 24.1\nOutput:Variable,*,Zone Mean Air Temperature,hourly; !- [C]\n"
        await fs.write_text("run/eplusout.rdd", rdd_content)
        result = SimulationResult(
            run_dir=Path("run"),
            success=True,
            exit_code=0,
            stdout="",
            stderr="",
            runtime_seconds=0.0,
            async_fs=fs,
        )
        variables = await result.async_variables()
        assert variables is not None
        assert len(variables.variables) == 1

    @pytest.mark.asyncio
    async def test_async_html_with_actual_data(self) -> None:
        """async_html should parse HTML content from an async fs."""
        from idfkit.simulation.result import SimulationResult

        fs = InMemoryAsyncFileSystem()
        html_content = (
            "<html><body>"
            "<b>Report:</b><b>Test Report</b>"
            "<table><tr><td>Zone</td><td>Value</td></tr>"
            "<tr><td>Zone1</td><td>21.5</td></tr></table>"
            "</body></html>"
        )
        await fs.write_text("run/eplusoutTable.html", html_content)
        result = SimulationResult(
            run_dir=Path("run"),
            success=True,
            exit_code=0,
            stdout="",
            stderr="",
            runtime_seconds=0.0,
            async_fs=fs,
        )
        html_result = await result.async_html()
        assert html_result is not None

    @pytest.mark.asyncio
    async def test_from_directory_with_async_fs(self) -> None:
        """from_directory should accept async_fs and populate it on the result."""
        from idfkit.simulation.result import SimulationResult

        fs = InMemoryAsyncFileSystem()
        await fs.write_text(
            "run/eplusout.err",
            "Program Version,EnergyPlus, 24.1\n   ************* EnergyPlus Completed Successfully.\n",
        )
        result = SimulationResult.from_directory("run", async_fs=fs)
        assert result.async_fs is fs
        assert result.fs is None
        errors = await result.async_errors()
        assert "completed successfully" in errors.summary()

    def test_both_fs_and_async_fs_raises(self) -> None:
        """Setting both fs and async_fs should raise ValueError."""
        from idfkit.simulation.result import SimulationResult

        with pytest.raises(ValueError, match="mutually exclusive"):
            SimulationResult(
                run_dir=Path("run"),
                success=True,
                exit_code=0,
                stdout="",
                stderr="",
                runtime_seconds=0.0,
                fs=InMemoryFileSystem(),
                async_fs=InMemoryAsyncFileSystem(),
            )


# ---------------------------------------------------------------------------
# Low-level async runner helpers
# ---------------------------------------------------------------------------


class TestAsyncRunnerHelpers:
    """Tests for internal async runner helper functions."""

    @pytest.mark.asyncio
    async def test_run_simple_os_error(self, mock_config: EnergyPlusConfig, weather_file: Path, tmp_path: Path) -> None:
        """_run_simple raises SimulationError when subprocess.exec raises OSError."""
        from idfkit.simulation.async_runner import _run_simple  # pyright: ignore[reportPrivateUsage]

        with (
            patch("idfkit.simulation.async_runner.asyncio.create_subprocess_exec", side_effect=OSError("no such exe")),
            pytest.raises(SimulationError, match="Failed to start EnergyPlus"),
        ):
            await _run_simple(["nonexistent"], tmp_path, 10.0)

    @pytest.mark.asyncio
    async def test_start_process_os_error(self, tmp_path: Path) -> None:
        """_start_process raises SimulationError when subprocess start fails."""
        from idfkit.simulation.async_runner import _start_process  # pyright: ignore[reportPrivateUsage]

        with (
            patch("idfkit.simulation.async_runner.asyncio.create_subprocess_exec", side_effect=OSError("bad")),
            pytest.raises(SimulationError, match="Failed to start EnergyPlus"),
        ):
            await _start_process(["nonexistent"], tmp_path)

    @pytest.mark.asyncio
    async def test_gather_with_timeout_raises_simulation_error(self) -> None:
        """_gather_with_timeout raises SimulationError on asyncio.TimeoutError."""
        from idfkit.simulation.async_runner import _gather_with_timeout  # pyright: ignore[reportPrivateUsage]

        proc = MagicMock()
        proc.kill = MagicMock()
        proc.wait = AsyncMock()

        async def slow_stdout() -> None:
            await asyncio.sleep(10)

        async def quick_stderr() -> bytes:
            return b"some stderr"

        with pytest.raises(SimulationError, match="timed out"):
            await _gather_with_timeout(proc, slow_stdout(), quick_stderr(), timeout=0.01)

        proc.kill.assert_called_once()

    @pytest.mark.asyncio
    async def test_gather_with_timeout_cancelled_error(self) -> None:
        """_gather_with_timeout propagates CancelledError after killing the process."""
        from idfkit.simulation.async_runner import _gather_with_timeout  # pyright: ignore[reportPrivateUsage]

        proc = MagicMock()
        proc.kill = MagicMock()
        proc.wait = AsyncMock()

        async def cancellable_stdout() -> None:
            await asyncio.sleep(10)

        async def quick_stderr() -> bytes:
            return b""

        gather_coro = _gather_with_timeout(proc, cancellable_stdout(), quick_stderr(), timeout=10.0)
        task = asyncio.create_task(gather_coro)
        # Give it a moment to start, then cancel
        await asyncio.sleep(0)
        task.cancel()
        with pytest.raises(asyncio.CancelledError):
            await task

        proc.kill.assert_called()

    def test_get_stderr_result_not_done(self) -> None:
        """_get_stderr_result returns b'' when task is not done."""
        from idfkit.simulation.async_runner import _get_stderr_result  # pyright: ignore[reportPrivateUsage]

        task: asyncio.Task[bytes] = MagicMock(spec=asyncio.Task)
        task.done.return_value = False
        task.cancelled.return_value = False
        result = _get_stderr_result(task)
        assert result == b""

    def test_get_stderr_result_exception(self) -> None:
        """_get_stderr_result returns b'' when task.result() raises."""
        from idfkit.simulation.async_runner import _get_stderr_result  # pyright: ignore[reportPrivateUsage]

        task: asyncio.Task[bytes] = MagicMock(spec=asyncio.Task)
        task.done.return_value = True
        task.cancelled.return_value = False
        task.result.side_effect = RuntimeError("task failed")
        result = _get_stderr_result(task)
        assert result == b""

    def test_decode_stderr_non_empty(self) -> None:
        """_decode_stderr returns a decoded string for non-empty bytes."""
        from idfkit.simulation.async_runner import _decode_stderr  # pyright: ignore[reportPrivateUsage]

        result = _decode_stderr(b"some error text")
        assert result == "some error text"

    def test_decode_stderr_empty(self) -> None:
        """_decode_stderr returns None for empty bytes."""
        from idfkit.simulation.async_runner import _decode_stderr  # pyright: ignore[reportPrivateUsage]

        result = _decode_stderr(b"")
        assert result is None

    @pytest.mark.asyncio
    @patch("idfkit.simulation.async_runner.asyncio.create_subprocess_exec")
    async def test_progress_cleanup_called_on_error(
        self, mock_exec: AsyncMock, mock_config: EnergyPlusConfig, weather_file: Path
    ) -> None:
        """progress_cleanup is called even when simulation raises early."""
        cleanup_called = False

        def _cleanup() -> None:
            nonlocal cleanup_called
            cleanup_called = True

        with patch("idfkit.simulation.async_runner.resolve_on_progress", return_value=(None, _cleanup)):
            mock_exec.side_effect = OSError("won't be reached anyway")
            model = new_document()
            with pytest.raises(SimulationError):
                await async_simulate(model, "/nonexistent/weather.epw", energyplus=mock_config)

        assert cleanup_called

    @pytest.mark.asyncio
    @patch("idfkit.simulation.async_runner.asyncio.create_subprocess_exec")
    async def test_run_with_progress_non_event_line(
        self, mock_exec: AsyncMock, mock_config: EnergyPlusConfig, weather_file: Path, tmp_path: Path
    ) -> None:
        """Lines that don't parse to a progress event are collected but don't invoke callback."""
        from idfkit.simulation.async_runner import _run_with_progress  # pyright: ignore[reportPrivateUsage]

        proc = MagicMock()
        # "EnergyPlus starting..." is not a recognised progress line — parser returns None
        stdout_lines = [b"EnergyPlus starting non-progress line\n", b""]
        line_iter = iter(stdout_lines)

        async def readline() -> bytes:
            return next(line_iter)

        proc.returncode = 0
        proc.kill = MagicMock()
        proc.wait = AsyncMock()
        proc.stdout = MagicMock()
        proc.stdout.readline = readline
        proc.stderr = MagicMock()
        proc.stderr.read = AsyncMock(return_value=b"")
        mock_exec.return_value = proc

        events: list[object] = []

        def sync_cb(event: object) -> None:
            events.append(event)

        _stdout, _stderr, rc = await _run_with_progress(["ep"], tmp_path, 60.0, sync_cb)
        assert rc == 0
        # The non-progress line is captured in stdout but doesn't generate an event
        assert len(events) == 0


# ---------------------------------------------------------------------------
# async_batch: progress_cleanup and on_progress callback paths
# ---------------------------------------------------------------------------


class TestAsyncBatchProgressCallback:
    """Tests for async_simulate_batch on_progress callback wiring."""

    @pytest.mark.asyncio
    @patch("idfkit.simulation.async_runner.asyncio.create_subprocess_exec")
    async def test_on_progress_async_callback_stamped(
        self, mock_exec: AsyncMock, mock_config: EnergyPlusConfig, weather_file: Path
    ) -> None:
        """Async on_progress receives events stamped with job_index and job_label for each job."""
        from idfkit.simulation.async_batch import async_simulate_batch
        from idfkit.simulation.progress import SimulationProgress

        def _make_progress_proc() -> MagicMock:
            proc = MagicMock()
            lines = [b"Warming up {1}\n", b"EnergyPlus Completed Successfully.\n", b""]
            it = iter(lines)

            async def readline() -> bytes:
                return next(it)

            proc.returncode = 0
            proc.kill = MagicMock()
            proc.wait = AsyncMock()
            proc.communicate = AsyncMock(return_value=(b"ok", b""))
            proc.stdout = MagicMock()
            proc.stdout.readline = readline
            proc.stderr = MagicMock()
            proc.stderr.read = AsyncMock(return_value=b"")
            return proc

        mock_exec.side_effect = lambda *a, **kw: _make_progress_proc()

        events: list[object] = []

        async def async_cb(event: object) -> None:
            events.append(event)

        jobs = [
            SimulationJob(model=new_document(), weather=weather_file, label="job-0"),
            SimulationJob(model=new_document(), weather=weather_file, label="job-1"),
        ]
        await async_simulate_batch(jobs, energyplus=mock_config, on_progress=async_cb)

        progress_events = [e for e in events if isinstance(e, SimulationProgress)]
        assert len(progress_events) > 0
        job0_events = [e for e in progress_events if e.job_index == 0]
        job1_events = [e for e in progress_events if e.job_index == 1]
        assert len(job0_events) > 0
        assert all(e.job_label == "job-0" for e in job0_events)
        assert len(job1_events) > 0
        assert all(e.job_label == "job-1" for e in job1_events)

    @pytest.mark.asyncio
    @patch("idfkit.simulation.async_runner.asyncio.create_subprocess_exec")
    async def test_batch_progress_cleanup_called(
        self, mock_exec: AsyncMock, mock_config: EnergyPlusConfig, weather_file: Path
    ) -> None:
        """async_simulate_batch calls progress_cleanup in finally block."""
        from idfkit.simulation.async_batch import async_simulate_batch

        cleanup_called = False

        def _cleanup() -> None:
            nonlocal cleanup_called
            cleanup_called = True

        mock_exec.return_value = _make_mock_process()

        with patch("idfkit.simulation.async_batch.resolve_on_progress", return_value=(None, _cleanup)):
            jobs = [SimulationJob(model=new_document(), weather=weather_file)]
            await async_simulate_batch(jobs, energyplus=mock_config)

        assert cleanup_called

    @pytest.mark.asyncio
    async def test_batch_stream_tqdm_rejected(self) -> None:
        """async_simulate_batch_stream rejects on_progress='tqdm'."""
        from idfkit.simulation.async_batch import async_simulate_batch_stream

        jobs = [SimulationJob(model=new_document(), weather="/fake.epw")]
        with pytest.raises(ValueError, match="not supported for batch"):
            async for _ in async_simulate_batch_stream(jobs, on_progress="tqdm"):  # type: ignore[arg-type]
                pass

    @pytest.mark.asyncio
    @patch("idfkit.simulation.async_runner.asyncio.create_subprocess_exec")
    async def test_batch_stream_progress_cleanup_called(
        self, mock_exec: AsyncMock, mock_config: EnergyPlusConfig, weather_file: Path
    ) -> None:
        """async_simulate_batch_stream calls progress_cleanup in finally block."""
        from idfkit.simulation.async_batch import async_simulate_batch_stream

        cleanup_called = False

        def _cleanup() -> None:
            nonlocal cleanup_called
            cleanup_called = True

        mock_exec.return_value = _make_mock_process()

        with patch("idfkit.simulation.async_batch.resolve_on_progress", return_value=(None, _cleanup)):
            jobs = [SimulationJob(model=new_document(), weather=weather_file)]
            async for _ in async_simulate_batch_stream(jobs, energyplus=mock_config):
                pass

        assert cleanup_called

    @pytest.mark.asyncio
    @patch("idfkit.simulation.async_runner.asyncio.create_subprocess_exec")
    async def test_async_run_job_exception_uses_output_dir(
        self, mock_exec: AsyncMock, mock_config: EnergyPlusConfig, weather_file: Path, tmp_path: Path
    ) -> None:
        """When a job fails, output_dir is used as run_dir in the failed result."""
        from idfkit.simulation.async_batch import async_simulate_batch

        mock_exec.side_effect = OSError("boom")
        out_dir = tmp_path / "out"
        out_dir.mkdir()
        jobs = [SimulationJob(model=new_document(), weather=weather_file, output_dir=str(out_dir))]
        result = await async_simulate_batch(jobs, energyplus=mock_config)
        assert not result[0].success
        assert result[0].run_dir == out_dir

    @pytest.mark.asyncio
    @patch("idfkit.simulation.async_runner.asyncio.create_subprocess_exec")
    async def test_on_progress_sync_callback_stamped(
        self, mock_exec: AsyncMock, mock_config: EnergyPlusConfig, weather_file: Path
    ) -> None:
        """Sync on_progress receives events stamped with job_index and job_label for each job."""
        from idfkit.simulation.async_batch import async_simulate_batch
        from idfkit.simulation.progress import SimulationProgress

        def _make_progress_proc() -> MagicMock:
            proc = MagicMock()
            lines = [b"Warming up {1}\n", b"EnergyPlus Completed Successfully.\n", b""]
            it = iter(lines)

            async def readline() -> bytes:
                return next(it)

            proc.returncode = 0
            proc.kill = MagicMock()
            proc.wait = AsyncMock()
            proc.communicate = AsyncMock(return_value=(b"ok", b""))
            proc.stdout = MagicMock()
            proc.stdout.readline = readline
            proc.stderr = MagicMock()
            proc.stderr.read = AsyncMock(return_value=b"")
            return proc

        mock_exec.side_effect = lambda *a, **kw: _make_progress_proc()

        events: list[object] = []

        def sync_cb(event: object) -> None:
            events.append(event)

        jobs = [
            SimulationJob(model=new_document(), weather=weather_file, label="sync-0"),
            SimulationJob(model=new_document(), weather=weather_file, label="sync-1"),
        ]
        await async_simulate_batch(jobs, energyplus=mock_config, on_progress=sync_cb)
        progress_events = [e for e in events if isinstance(e, SimulationProgress)]
        assert len(progress_events) > 0
        job0_events = [e for e in progress_events if e.job_index == 0]
        job1_events = [e for e in progress_events if e.job_index == 1]
        assert len(job0_events) > 0
        assert all(e.job_label == "sync-0" for e in job0_events)
        assert len(job1_events) > 0
        assert all(e.job_label == "sync-1" for e in job1_events)


# ---------------------------------------------------------------------------
# async_simulate without a weather file
# ---------------------------------------------------------------------------


class TestAsyncSimulateWithoutWeather:
    """Tests for async_simulate() with weather=None on a design-day-only run."""

    @pytest.mark.asyncio
    @patch("idfkit.simulation.async_runner.asyncio.create_subprocess_exec")
    async def test_command_has_no_weather(
        self, mock_exec: AsyncMock, mock_config: EnergyPlusConfig, tmp_path: Path
    ) -> None:
        mock_exec.return_value = _make_mock_process()
        result = await async_simulate(
            new_document(), design_day=True, energyplus=mock_config, output_dir=tmp_path / "run"
        )
        cmd = mock_exec.call_args[0]
        assert "-D" in cmd
        assert "-w" not in cmd
        assert result.success
        assert list(result.run_dir.glob("*.epw")) == []

    @pytest.mark.asyncio
    @patch("idfkit.simulation.async_runner.asyncio.create_subprocess_exec")
    async def test_positional_none(self, mock_exec: AsyncMock, mock_config: EnergyPlusConfig, tmp_path: Path) -> None:
        mock_exec.return_value = _make_mock_process()
        result = await async_simulate(
            new_document(), None, design_day=True, energyplus=mock_config, output_dir=tmp_path / "run"
        )
        cmd = mock_exec.call_args[0]
        assert "-D" in cmd
        assert "-w" not in cmd
        assert list(result.run_dir.glob("*.epw")) == []

    @pytest.mark.asyncio
    @patch("idfkit.simulation.async_runner.asyncio.create_subprocess_exec")
    async def test_log_states_no_weather(
        self,
        mock_exec: AsyncMock,
        mock_config: EnergyPlusConfig,
        tmp_path: Path,
        caplog: pytest.LogCaptureFixture,
    ) -> None:
        mock_exec.return_value = _make_mock_process()
        with caplog.at_level(logging.DEBUG, logger="idfkit.simulation"):
            await async_simulate(new_document(), design_day=True, energyplus=mock_config, output_dir=tmp_path / "run")
        messages = [record.getMessage() for record in caplog.records]
        assert "Starting async simulation without a weather file" in messages
        assert not any("in.epw" in m for m in messages)
        assert not any(str(Path.cwd()) in m for m in messages if "weather" in m.casefold())


class TestAsyncBatchWithoutWeather:
    """Async batches that mix jobs with and without a weather file."""

    @staticmethod
    def _jobs(weather_file: Path) -> list[SimulationJob]:
        return [
            SimulationJob(model=new_document(), weather=weather_file, label="with-weather"),
            SimulationJob(model=new_document(), design_day=True, label="design-day"),
        ]

    @pytest.mark.asyncio
    @patch("idfkit.simulation.async_runner.asyncio.create_subprocess_exec")
    async def test_mixed_batch(self, mock_exec: AsyncMock, mock_config: EnergyPlusConfig, weather_file: Path) -> None:
        mock_exec.return_value = _make_mock_process()
        result = await async_simulate_batch(self._jobs(weather_file), energyplus=mock_config)
        assert result.all_succeeded
        commands = [c[0] for c in mock_exec.call_args_list]
        assert sorted("-w" in cmd for cmd in commands) == [False, True]

    @pytest.mark.asyncio
    @patch("idfkit.simulation.async_runner.asyncio.create_subprocess_exec")
    async def test_mixed_batch_stream(
        self, mock_exec: AsyncMock, mock_config: EnergyPlusConfig, weather_file: Path
    ) -> None:
        mock_exec.return_value = _make_mock_process()
        events = [e async for e in async_simulate_batch_stream(self._jobs(weather_file), energyplus=mock_config)]
        assert len(events) == 2
        assert all(e.result.success for e in events)
        commands = [c[0] for c in mock_exec.call_args_list]
        assert sorted("-w" in cmd for cmd in commands) == [False, True]

    @pytest.mark.asyncio
    @patch("idfkit.simulation.async_runner.asyncio.create_subprocess_exec")
    async def test_annual_job_without_weather_fails_alone(
        self, mock_exec: AsyncMock, mock_config: EnergyPlusConfig, weather_file: Path
    ) -> None:
        mock_exec.return_value = _make_mock_process()
        jobs = [*self._jobs(weather_file), SimulationJob(model=new_document(), annual=True, label="annual")]
        result = await async_simulate_batch(jobs, energyplus=mock_config)
        assert result[0].success
        assert result[1].success
        assert not result[2].success
        assert REFUSAL_R2 in result[2].stderr
        assert mock_exec.call_count == 2


class TestAsyncFileSystemWithoutWeather:
    @pytest.mark.asyncio
    @patch("idfkit.simulation.async_runner.asyncio.create_subprocess_exec")
    async def test_async_fs_without_weather(self, mock_exec: AsyncMock, mock_config: EnergyPlusConfig) -> None:
        mock_exec.return_value = _make_mock_process()
        fs = InMemoryAsyncFileSystem()
        result = await async_simulate(
            new_document(),
            design_day=True,
            energyplus=mock_config,
            output_dir="remote/output",
            fs=fs,
        )
        assert result.success
        uploaded = [k for k in fs._files if k.startswith("remote/output/")]
        assert len(uploaded) > 0
        assert not any(k.endswith(".epw") for k in uploaded)


class TestAsyncWeatherAdmission:
    """Refusals REFUSAL_R1 to R4 and the unchanged missing-file message, raised before any subprocess."""

    async def _assert_refused(self, message: str, **kwargs: Any) -> None:
        # Not ``or``: an IDFDocument with no objects is falsy.
        model = kwargs.pop("model", None)
        if model is None:
            model = new_document()
        with (
            patch("idfkit.simulation.async_runner.asyncio.create_subprocess_exec") as mock_exec,
            patch("idfkit.simulation.expand.run_preprocessing") as mock_preprocess,
            pytest.raises(SimulationError, match=re.escape(message)),
        ):
            await async_simulate(model, **kwargs)
        mock_exec.assert_not_called()
        mock_preprocess.assert_not_called()

    @pytest.mark.asyncio
    async def test_r1_empty_string(self, mock_config: EnergyPlusConfig) -> None:
        await self._assert_refused(REFUSAL_R1, weather="", design_day=True, energyplus=mock_config)

    @pytest.mark.asyncio
    async def test_missing_file_unchanged(self, mock_config: EnergyPlusConfig, tmp_path: Path) -> None:
        missing = tmp_path / "absent.epw"
        await self._assert_refused(
            f"Weather file not found: {missing.resolve()}", weather=missing, design_day=True, energyplus=mock_config
        )

    @pytest.mark.asyncio
    async def test_r2_not_design_day(self, mock_config: EnergyPlusConfig) -> None:
        await self._assert_refused(REFUSAL_R2, weather=None, design_day=False, energyplus=mock_config)

    @pytest.mark.asyncio
    async def test_r2_design_day_and_annual(self, mock_config: EnergyPlusConfig) -> None:
        await self._assert_refused(REFUSAL_R2, weather=None, design_day=True, annual=True, energyplus=mock_config)

    @pytest.mark.asyncio
    async def test_r3_ground_heat_transfer(self, mock_config: EnergyPlusConfig) -> None:
        await self._assert_refused(
            refusal_r3("GroundHeatTransfer:Basement:SimParameters, GroundHeatTransfer:Slab:Materials"),
            model=ground_heat_model(),
            weather=None,
            design_day=True,
            energyplus=mock_config,
        )

    @pytest.mark.asyncio
    async def test_r3_lists_only_enabled_types(self, mock_config: EnergyPlusConfig) -> None:
        await self._assert_refused(
            refusal_r3("GroundHeatTransfer:Basement:SimParameters"),
            model=ground_heat_model(slab="No", basement="Yes"),
            weather=None,
            design_day=True,
            energyplus=mock_config,
        )

    @pytest.mark.asyncio
    async def test_r3_not_raised_when_control_absent(self, mock_config: EnergyPlusConfig, tmp_path: Path) -> None:
        model = ground_heat_model(slab=None, basement=None)
        with (
            patch("idfkit.simulation.async_runner.asyncio.create_subprocess_exec") as mock_exec,
            patch("idfkit.simulation.expand.run_preprocessing", side_effect=lambda m, **_: m.copy()) as mock_pre,
        ):
            mock_exec.return_value = _make_mock_process()
            result = await async_simulate(model, design_day=True, energyplus=mock_config, output_dir=tmp_path / "run")
        mock_pre.assert_called_once()
        assert result.success

    @pytest.mark.asyncio
    async def test_weather_refused_before_energyplus_discovery(self) -> None:
        with (
            patch("idfkit.simulation._common.find_energyplus") as mock_find,
            pytest.raises(SimulationError, match=re.escape(REFUSAL_R2)),
        ):
            await async_simulate(new_document(), annual=True)  # pyright: ignore[reportCallIssue]
        mock_find.assert_not_called()

    @pytest.mark.asyncio
    async def test_r3_not_raised_without_expand_objects(self, mock_config: EnergyPlusConfig, tmp_path: Path) -> None:
        with (
            patch("idfkit.simulation.async_runner.asyncio.create_subprocess_exec") as mock_exec,
            patch("idfkit.simulation.expand.run_preprocessing") as mock_preprocess,
        ):
            mock_exec.return_value = _make_mock_process()
            result = await async_simulate(
                ground_heat_model(),
                design_day=True,
                expand_objects=False,
                energyplus=mock_config,
                output_dir=tmp_path / "run",
            )
        mock_exec.assert_called_once()
        mock_preprocess.assert_not_called()
        assert result.success

    @pytest.mark.asyncio
    async def test_r2_takes_precedence_over_r3(self, mock_config: EnergyPlusConfig) -> None:
        await self._assert_refused(
            REFUSAL_R2, model=ground_heat_model(), weather=None, design_day=False, energyplus=mock_config
        )

    @pytest.mark.asyncio
    async def test_r4_default_weather_in_run_dir(self, mock_config: EnergyPlusConfig, tmp_path: Path) -> None:
        (tmp_path / "in.epw").write_text("LOCATION,Elsewhere\n")
        await self._assert_refused(
            refusal_r4(tmp_path.resolve()), weather=None, design_day=True, energyplus=mock_config, output_dir=tmp_path
        )
