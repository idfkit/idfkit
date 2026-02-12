"""Tests for the async EnergyPlus simulation runner and batch modules."""

from __future__ import annotations

import asyncio
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from conftest import InMemoryAsyncFileSystem, InMemoryFileSystem

from idfkit import new_document
from idfkit.exceptions import SimulationError
from idfkit.simulation.async_batch import SimulationEvent, async_simulate_batch, async_simulate_batch_stream
from idfkit.simulation.async_runner import async_simulate
from idfkit.simulation.batch import SimulationJob
from idfkit.simulation.cache import SimulationCache
from idfkit.simulation.config import EnergyPlusConfig


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
