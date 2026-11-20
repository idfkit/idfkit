"""Tests for the batch simulation module."""

from __future__ import annotations

import tempfile
import threading
import time
from pathlib import Path
from typing import Any
from unittest.mock import MagicMock, patch

import pytest
from conftest import REFUSAL_R2, InMemoryFileSystem, design_day_model, runnable_model

from idfkit import LATEST_VERSION
from idfkit.exceptions import OutputNotFoundError, SimulationError
from idfkit.simulation._cancel import _active_group  # pyright: ignore[reportPrivateUsage]
from idfkit.simulation.batch import (
    REFUSED_RUN_DIR,
    BatchResult,
    SimulationJob,
    _stopped_result,  # pyright: ignore[reportPrivateUsage]
    cancelled_job_result,
    simulate_batch,
)
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
# SimulationJob
# ---------------------------------------------------------------------------


class TestSimulationJob:
    """Tests for SimulationJob dataclass."""

    def test_frozen(self) -> None:
        model = runnable_model()
        job = SimulationJob(model=model, weather="test.epw")
        with pytest.raises(AttributeError):
            job.label = "changed"  # type: ignore[misc]

    def test_defaults(self) -> None:
        model = runnable_model()
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
        assert job.auto_migrate is False

    def test_custom_fields(self) -> None:
        model = runnable_model()
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

    def test_weather_defaults_to_none(self) -> None:
        assert SimulationJob(model=runnable_model()).weather is None

    def test_positional_weather(self) -> None:
        job = SimulationJob(runnable_model(), "w.epw")
        assert job.weather == "w.epw"

    def test_extra_args_list_stored_as_tuple(self) -> None:
        args = ["--convert"]
        job = SimulationJob(model=runnable_model(), extra_args=args)
        args.append("--later")
        assert job.extra_args == ("--convert",)

    def test_extra_args_string_refused(self) -> None:
        with pytest.raises(TypeError, match="pass \\['--convert'\\]"):
            SimulationJob(model=runnable_model(), extra_args="--convert")  # type: ignore[arg-type]

    @pytest.mark.parametrize("model", ["building.idf", Path("building.idf")])
    def test_path_model_refused(self, model: object) -> None:
        with pytest.raises(TypeError, match="load it with load_idf"):
            SimulationJob(model=model, weather="w.epw")  # type: ignore[arg-type]


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

    def test_cancelled_is_neither_succeeded_nor_failed(self, mixed_results: tuple[SimulationResult, ...]) -> None:
        job = SimulationJob(model=runnable_model(), label="c")
        cancelled = cancelled_job_result(job, "job 'x' failed", started=False)
        br = BatchResult(results=(*mixed_results, cancelled), total_runtime_seconds=3.5)
        assert br.cancelled == (cancelled,)
        assert br.failed == (mixed_results[1],)
        assert len(br.succeeded) == 2
        assert not br.all_succeeded

    def test_cancelled_empty_without_fail_fast(self, mixed_results: tuple[SimulationResult, ...]) -> None:
        assert BatchResult(results=mixed_results, total_runtime_seconds=3.5).cancelled == ()

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

    @patch("idfkit.simulation.runner.run_process")
    def test_single_job(self, mock_run: MagicMock, mock_config: EnergyPlusConfig, weather_file: Path) -> None:
        mock_run.return_value = MagicMock(returncode=0, stdout="ok", stderr="")
        model = runnable_model()
        job = SimulationJob(model=model, weather=weather_file, label="single")
        result = simulate_batch([job], energyplus=mock_config)
        assert len(result) == 1
        assert result[0].success
        assert result.all_succeeded

    @patch("idfkit.simulation.runner.run_process")
    def test_multiple_jobs(self, mock_run: MagicMock, mock_config: EnergyPlusConfig, weather_file: Path) -> None:
        mock_run.return_value = MagicMock(returncode=0, stdout="ok", stderr="")
        jobs = [SimulationJob(model=runnable_model(), weather=weather_file, label=f"job-{i}") for i in range(3)]
        result = simulate_batch(jobs, energyplus=mock_config)
        assert len(result) == 3
        assert result.all_succeeded

    @patch("idfkit.simulation.runner.run_process")
    def test_preserves_order(self, mock_run: MagicMock, mock_config: EnergyPlusConfig, weather_file: Path) -> None:
        """Results should be in the same order as input jobs."""
        call_count = 0

        def side_effect(*_args: object, **_kwargs: object) -> MagicMock:
            nonlocal call_count
            call_count += 1
            return MagicMock(returncode=0, stdout=f"run-{call_count}", stderr="")

        mock_run.side_effect = side_effect
        jobs = [SimulationJob(model=runnable_model(), weather=weather_file, label=f"job-{i}") for i in range(3)]
        result = simulate_batch(jobs, energyplus=mock_config, max_workers=1)
        # With max_workers=1 the order is deterministic
        assert result[0].stdout == "run-1"
        assert result[1].stdout == "run-2"
        assert result[2].stdout == "run-3"

    @patch("idfkit.simulation.runner.run_process")
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

        jobs = [SimulationJob(model=runnable_model(), weather=weather_file, label=f"job-{i}") for i in range(3)]
        result = simulate_batch(jobs, energyplus=mock_config, max_workers=1)
        assert len(result) == 3
        assert not result.all_succeeded
        assert len(result.succeeded) == 2
        assert len(result.failed) == 1

    @patch("idfkit.simulation.runner.run_process")
    def test_fail_fast_without_a_failure_runs_every_job(
        self, mock_run: MagicMock, mock_config: EnergyPlusConfig, weather_file: Path
    ) -> None:
        mock_run.return_value = MagicMock(returncode=0, stdout="ok", stderr="")
        jobs = [SimulationJob(model=runnable_model(), weather=weather_file) for _ in range(3)]
        result = simulate_batch(jobs, energyplus=mock_config, max_workers=1, fail_fast=True)
        assert result.all_succeeded
        assert mock_run.call_count == 3

    @patch("idfkit.simulation.runner.run_process")
    def test_fail_fast_on_the_last_job_cancels_nothing(
        self, mock_run: MagicMock, mock_config: EnergyPlusConfig, weather_file: Path
    ) -> None:
        mock_run.side_effect = [
            MagicMock(returncode=0, stdout="ok", stderr=""),
            MagicMock(returncode=1, stdout="", stderr="failed"),
        ]
        jobs = [SimulationJob(model=runnable_model(), weather=weather_file) for _ in range(2)]
        result = simulate_batch(jobs, energyplus=mock_config, max_workers=1, fail_fast=True)
        assert (len(result.succeeded), len(result.failed), result.cancelled) == (1, 1, ())

    def test_fail_fast_stops_running_and_queued_jobs(self, tmp_path: Path, mock_config: EnergyPlusConfig) -> None:
        """The first failure stops the batch: a running job is stopped, a queued one never starts."""
        running = threading.Event()
        calls: list[str] = []

        def fake_simulate(*, output_dir: Path, **_kwargs: Any) -> SimulationResult:
            name = Path(output_dir).name
            calls.append(name)
            if name == "bad":
                assert running.wait(10)
                return SimulationResult(
                    run_dir=output_dir, success=False, exit_code=1, stdout="", stderr="boom", runtime_seconds=0.1
                )
            if name == "q1":
                running.set()
            group = _active_group.get()
            assert group is not None
            deadline = time.monotonic() + 10
            while not group.cancelled and time.monotonic() < deadline:  # stands in for EnergyPlus until killed
                time.sleep(0.01)
            temp = tmp_path / f"temp-{name}"
            temp.mkdir()
            return SimulationResult(
                run_dir=temp, success=False, exit_code=-9, stdout="", stderr="", runtime_seconds=0.1, owns_run_dir=True
            )

        names = ["bad", "q1", "q2", "q3"]
        jobs = [SimulationJob(model=runnable_model(), label=n, output_dir=tmp_path / n) for n in names]
        progress_calls: list[tuple[int, str, bool]] = []

        def progress(*, completed: int, total: int, label: str, success: bool) -> None:
            progress_calls.append((completed, label, success))

        with patch("idfkit.simulation.batch.simulate", side_effect=fake_simulate):
            result = simulate_batch(jobs, energyplus=mock_config, max_workers=2, fail_fast=True, progress=progress)

        reason = "job 'bad' failed and fail_fast=True stopped the batch"
        assert result.failed == (result[0],)
        assert result.cancelled == (result[1], result[2], result[3])
        assert result[1].refusal == f"stopped while running: {reason}"
        assert result[3].refusal == f"never started: {reason}"
        assert "q3" not in calls
        assert not (tmp_path / "temp-q1").exists()  # the stopped run's temporary directory is deleted
        assert result[1].run_dir == tmp_path / "q1"
        assert progress_calls[0] == (1, "bad", False)
        assert [c[0] for c in progress_calls] == [1, 2, 3, 4]
        assert all(not c[2] for c in progress_calls)

    def test_cancelled_result_repr_summary_and_raise(self) -> None:
        r = cancelled_job_result(SimulationJob(model=runnable_model()), "job 'a' failed", started=True)
        assert r.cancelled
        assert not r.success
        assert repr(r) == f"SimulationResult(cancelled: {r.refusal!r}, run_dir={REFUSED_RUN_DIR!r})"
        assert "cancelled: stopped while running" in r.errors.summary()
        with pytest.raises(SimulationError, match=r"^Simulation cancelled: stopped while running"):
            r.raise_for_status()
        with pytest.raises(OutputNotFoundError, match="this batch job was cancelled"):
            _ = r.sql

    def test_stopped_result_of_a_job_that_never_ran(self) -> None:
        job = SimulationJob(model=runnable_model())
        placeholder = cancelled_job_result(job, "the batch was stopped", started=False)
        r = _stopped_result(job, placeholder, "job 'a' failed")
        assert r.refusal == "never started: job 'a' failed"

    @patch("idfkit.simulation.runner.run_process")
    def test_progress_callback(self, mock_run: MagicMock, mock_config: EnergyPlusConfig, weather_file: Path) -> None:
        mock_run.return_value = MagicMock(returncode=0, stdout="", stderr="")
        progress_calls: list[dict[str, object]] = []

        def on_progress(**kwargs: object) -> None:
            progress_calls.append(kwargs)

        jobs = [SimulationJob(model=runnable_model(), weather=weather_file, label=f"job-{i}") for i in range(2)]
        simulate_batch(jobs, energyplus=mock_config, progress=on_progress, max_workers=1)

        assert len(progress_calls) == 2
        # Both should report total=2
        assert all(c["total"] == 2 for c in progress_calls)
        # completed should be 1 and 2 (in some order)
        completed_values = sorted(c["completed"] for c in progress_calls)
        assert completed_values == [1, 2]
        # All succeeded
        assert all(c["success"] is True for c in progress_calls)

    @patch("idfkit.simulation.runner.run_process")
    def test_progress_callback_with_wrong_signature_refused_before_running(
        self, mock_run: MagicMock, mock_config: EnergyPlusConfig, weather_file: Path
    ) -> None:
        def prog(completed: int, total: int) -> None: ...

        jobs = [SimulationJob(model=runnable_model(), weather=weather_file)]
        with pytest.raises(TypeError, match="cannot take that"):
            simulate_batch(jobs, energyplus=mock_config, progress=prog)  # type: ignore[arg-type]
        mock_run.assert_not_called()

    @patch("idfkit.simulation.runner.run_process")
    def test_cache_integration(
        self, mock_run: MagicMock, mock_config: EnergyPlusConfig, weather_file: Path, tmp_path: Path
    ) -> None:
        """Cache should be passed through to simulate()."""
        mock_run.return_value = MagicMock(returncode=0, stdout="ok", stderr="")
        cache = SimulationCache(cache_dir=tmp_path / "cache")
        model = runnable_model()
        job = SimulationJob(model=model, weather=weather_file, label="cached")

        # First run — miss, then store
        result1 = simulate_batch([job], energyplus=mock_config, cache=cache)
        assert result1[0].success
        assert mock_run.call_count == 1

        # Second run — cache hit, subprocess not called again
        result2 = simulate_batch([job], energyplus=mock_config, cache=cache)
        assert result2[0].success
        assert mock_run.call_count == 1  # no additional call

    @patch("idfkit.simulation.runner.run_process")
    def test_cache_follows_staged_file_content(
        self, mock_run: MagicMock, mock_config: EnergyPlusConfig, weather_file: Path, tmp_path: Path
    ) -> None:
        """A job's staged Schedule:File CSV is part of its cache key (#216)."""
        mock_run.return_value = MagicMock(returncode=0, stdout="ok", stderr="")
        cache = SimulationCache(cache_dir=tmp_path / "cache")
        run_dir = tmp_path / "run"
        run_dir.mkdir()
        csv = run_dir / "hourly.csv"
        model = runnable_model()
        model.add("Schedule:File", "Staged", file_name="hourly.csv", column_number=1, validate=False)
        job = SimulationJob(model=model, weather=weather_file, output_dir=run_dir)

        csv.write_text("1\n")
        simulate_batch([job], energyplus=mock_config, cache=cache)
        simulate_batch([job], energyplus=mock_config, cache=cache)
        assert mock_run.call_count == 1
        csv.write_text("2\n")
        simulate_batch([job], energyplus=mock_config, cache=cache)
        assert mock_run.call_count == 2

    @patch("idfkit.simulation.runner.run_process")
    def test_total_runtime_populated(
        self, mock_run: MagicMock, mock_config: EnergyPlusConfig, weather_file: Path
    ) -> None:
        mock_run.return_value = MagicMock(returncode=0, stdout="", stderr="")
        job = SimulationJob(model=runnable_model(), weather=weather_file)
        result = simulate_batch([job], energyplus=mock_config)
        assert result.total_runtime_seconds >= 0

    @patch("idfkit.simulation.runner.run_process")
    def test_batch_passes_fs_to_simulate(
        self, mock_run: MagicMock, mock_config: EnergyPlusConfig, weather_file: Path
    ) -> None:
        """When fs is passed to simulate_batch, results should carry the fs."""
        mock_run.return_value = MagicMock(returncode=0, stdout="ok", stderr="")
        fs = InMemoryFileSystem()
        job = SimulationJob(model=runnable_model(), weather=weather_file, output_dir="remote/batch/0")
        result = simulate_batch([job], energyplus=mock_config, fs=fs, max_workers=1)
        assert result[0].success
        assert result[0].fs is fs

    def test_job_exception_uses_output_dir(
        self, mock_config: EnergyPlusConfig, weather_file: Path, tmp_path: Path
    ) -> None:
        """When _run_job raises, output_dir is used as run_dir for the failed result."""
        with patch("idfkit.simulation.batch.simulate", side_effect=OSError("boom")):
            out_dir = tmp_path / "out"
            out_dir.mkdir()
            jobs = [SimulationJob(model=runnable_model(), weather=weather_file, output_dir=str(out_dir))]
            result = simulate_batch(jobs, energyplus=mock_config)
        assert not result[0].success
        assert result[0].run_dir == out_dir

    def test_refused_job_ignores_stale_err_in_output_dir(
        self, mock_config: EnergyPlusConfig, weather_file: Path, tmp_path: Path
    ) -> None:
        """A refused job's errors give its reason, not a stale .err left in its output_dir."""
        out_dir = tmp_path / "out"
        out_dir.mkdir()
        (out_dir / "eplusout.err").write_text("   ** Severe  ** stale from an earlier run\n")
        with patch("idfkit.simulation.batch.simulate", side_effect=OSError("boom")):
            jobs = [SimulationJob(model=runnable_model(), weather=weather_file, output_dir=str(out_dir))]
            r = simulate_batch(jobs, energyplus=mock_config)[0]
        assert r.refusal == "boom"
        assert r.err_path is None
        assert r.errors.severe_count == 0
        assert [m.message for m in r.errors.fatal] == ["refused: boom"]

    def test_timeout_after_energyplus_ran_reads_its_err(
        self, mock_config: EnergyPlusConfig, weather_file: Path, tmp_path: Path
    ) -> None:
        """A job that timed out after EnergyPlus wrote its .err is a failed run, not a refusal."""
        out_dir = tmp_path / "out"
        out_dir.mkdir()
        (out_dir / "eplusout.err").write_text("   ** Severe  ** stale from an earlier run\n")

        def run_then_time_out(**_: object) -> SimulationResult:
            (out_dir / "eplusout.err").write_text("   ** Severe  ** from this run\n   ** Severe  ** and another\n")
            msg = "Simulation timed out after 5 seconds"
            raise SimulationError(msg, stderr="partial stderr")

        with patch("idfkit.simulation.batch.simulate", side_effect=run_then_time_out):
            jobs = [SimulationJob(model=runnable_model(), weather=weather_file, output_dir=str(out_dir))]
            r = simulate_batch(jobs, energyplus=mock_config)[0]
        assert r.refusal is None
        assert r.err_path == out_dir / "eplusout.err"
        assert r.errors.severe_count == 2
        assert not repr(r).startswith("SimulationResult(refused")

    def test_refusal_reason_excludes_stderr_tail(
        self, mock_config: EnergyPlusConfig, weather_file: Path, tmp_path: Path
    ) -> None:
        """A SimulationError's stderr appears once in raise_for_status(), not in the refusal reason."""
        exc = SimulationError("Simulation timed out after 5 seconds", exit_code=3, stderr="line1 from eplus\nline2")
        with patch("idfkit.simulation.batch.simulate", side_effect=exc):
            jobs = [SimulationJob(model=runnable_model(), weather=weather_file, output_dir=str(tmp_path / "out"))]
            r = simulate_batch(jobs, energyplus=mock_config)[0]
        assert r.refusal == "Simulation timed out after 5 seconds"
        assert repr(r).startswith("SimulationResult(refused: 'Simulation timed out after 5 seconds', run_dir=")
        with pytest.raises(SimulationError) as info:
            r.raise_for_status()
        assert str(info.value).count("line1 from eplus") == 1
        assert str(info.value).count("(exit code 3)") == 1

    def test_refused_result_repr_summary_and_raise(self, mock_config: EnergyPlusConfig) -> None:
        """A refused job says so in its repr, its error summary and raise_for_status()."""
        r = simulate_batch([SimulationJob(model=runnable_model(), weather="/no/such.epw")], energyplus=mock_config)[0]
        assert r.refusal is not None
        assert "Weather file not found" in r.refusal
        assert repr(r).startswith(f"SimulationResult(refused: {r.refusal!r}")
        assert f"refused: {r.refusal}" in r.errors.summary()
        with pytest.raises(SimulationError, match=r"^Simulation refused: Weather file not found") as info:
            r.raise_for_status()
        assert "EnergyPlus simulation failed" not in str(info.value)

    def test_fs_without_output_dir_raises_up_front(self, mock_config: EnergyPlusConfig, weather_file: Path) -> None:
        """fs= with a job lacking output_dir is a configuration error, raised before any job runs."""
        jobs = [
            SimulationJob(model=runnable_model(), weather=weather_file, output_dir="remote/0"),
            SimulationJob(model=runnable_model(), weather=weather_file, label="no-dir"),
        ]
        with (
            patch("idfkit.simulation.batch.simulate") as mock_simulate,
            pytest.raises(ValueError, match=r"output_dir is required.*missing on: no-dir"),
        ):
            simulate_batch(jobs, energyplus=mock_config, fs=InMemoryFileSystem())
        mock_simulate.assert_not_called()

    def test_auto_migrate_is_forwarded_to_simulate(self, mock_config: EnergyPlusConfig, weather_file: Path) -> None:
        with patch("idfkit.simulation.batch.simulate", side_effect=RuntimeError("stop")) as mock_simulate:
            jobs = [
                SimulationJob(model=runnable_model(), weather=weather_file, auto_migrate=True),
                SimulationJob(model=runnable_model(), weather=weather_file),
            ]
            simulate_batch(jobs, energyplus=mock_config, max_workers=1)
        flags = sorted(call.kwargs["auto_migrate"] for call in mock_simulate.call_args_list)
        assert flags == [False, True]

    def test_progress_cleanup_called_on_error(self, mock_config: EnergyPlusConfig, weather_file: Path) -> None:
        """progress_cleanup is called when simulate_batch raises after resolve_on_progress."""
        cleanup_called = False

        def _cleanup() -> None:
            nonlocal cleanup_called
            cleanup_called = True

        with (
            patch("idfkit.simulation.batch.resolve_on_progress", return_value=(None, _cleanup)),
            patch("idfkit.simulation.batch.simulate", side_effect=RuntimeError("boom")),
        ):
            jobs = [SimulationJob(model=runnable_model(), weather=weather_file)]
            simulate_batch(jobs, energyplus=mock_config)

        assert cleanup_called


class TestSimulateBatchWithoutWeather:
    """Batches that mix jobs with and without a weather file."""

    @patch("idfkit.simulation.runner.run_process")
    def test_mixed_batch(self, mock_run: MagicMock, mock_config: EnergyPlusConfig, weather_file: Path) -> None:
        mock_run.return_value = MagicMock(returncode=0, stdout="ok", stderr="")
        jobs = [
            SimulationJob(model=runnable_model(), weather=weather_file, label="with-weather"),
            SimulationJob(model=design_day_model(), design_day=True, label="design-day"),
        ]
        result = simulate_batch(jobs, energyplus=mock_config, max_workers=1)
        assert result.all_succeeded
        commands = [c[0][0] for c in mock_run.call_args_list]
        assert sorted("-w" in cmd for cmd in commands) == [False, True]

    @patch("idfkit.simulation.runner.run_process")
    def test_annual_job_without_weather_fails_alone(
        self, mock_run: MagicMock, mock_config: EnergyPlusConfig, weather_file: Path
    ) -> None:
        mock_run.return_value = MagicMock(returncode=0, stdout="ok", stderr="")
        jobs = [
            SimulationJob(model=runnable_model(), weather=weather_file, label="with-weather"),
            SimulationJob(model=design_day_model(), design_day=True, label="design-day"),
            SimulationJob(model=runnable_model(), annual=True, label="annual"),
        ]
        result = simulate_batch(jobs, energyplus=mock_config)
        assert result[0].success
        assert result[1].success
        assert not result[2].success
        assert REFUSAL_R2 in result[2].stderr
        assert mock_run.call_count == 2

    def test_refused_job_creates_no_directory(
        self, mock_config: EnergyPlusConfig, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """A job refused before EnergyPlus runs leaves no temporary directory behind (#228)."""
        temp_root = tmp_path / "tmp"
        temp_root.mkdir()
        monkeypatch.setattr(tempfile, "tempdir", str(temp_root))
        jobs = [SimulationJob(model=runnable_model(), annual=True, label=f"annual-{i}") for i in range(3)]
        result = simulate_batch(jobs, energyplus=mock_config)
        assert not any(r.success for r in result)
        assert list(temp_root.iterdir()) == []
        assert all(r.run_dir == REFUSED_RUN_DIR for r in result)
        assert not REFUSED_RUN_DIR.exists()
        assert [m.message for m in result[0].errors.fatal] == [f"refused: {result[0].refusal}"]
        assert result[0].refusal is not None
        assert result[0].refusal.startswith("A weather file is required")

    def test_refused_result_ignores_files_at_placeholder(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        """Files another process put at the shared placeholder path are never read as outputs (#228)."""
        placeholder = tmp_path / "idfkit-refused-job"
        placeholder.mkdir()
        (placeholder / "eplusout.err").write_text("   ** Fatal  ** planted\n")
        monkeypatch.setattr("idfkit.simulation.result.REFUSED_RUN_DIR", placeholder)
        result = SimulationResult(
            run_dir=placeholder, success=False, exit_code=None, stdout="", stderr="refused", runtime_seconds=0.0
        )
        assert result.err_path is None
        assert result.errors.fatal_count == 0
        assert result.sql_path is None
        with pytest.raises(OutputNotFoundError):
            _ = result.sql


class TestBatchResultCleanup:
    """BatchResult.cleanup() and its context manager delete only idfkit-created run directories."""

    @patch("idfkit.simulation.runner.run_process")
    def test_with_block_deletes_temp_dirs_only(
        self, mock_run: MagicMock, mock_config: EnergyPlusConfig, weather_file: Path, tmp_path: Path
    ) -> None:
        mock_run.return_value = MagicMock(returncode=0, stdout="ok", stderr="")
        out = tmp_path / "kept"
        jobs = [
            SimulationJob(model=runnable_model(), weather=weather_file, label="temp"),
            SimulationJob(model=runnable_model(), weather=weather_file, label="kept", output_dir=out),
        ]
        with simulate_batch(jobs, energyplus=mock_config) as batch:
            temp_dir = batch[0].run_dir
            assert batch[0].owns_run_dir
            assert not batch[1].owns_run_dir
        assert not temp_dir.exists()
        assert (out / "model.idf").exists()
        batch.cleanup()  # idempotent

    def test_refused_result_cleanup_is_noop(self) -> None:
        refused = SimulationResult(
            run_dir=REFUSED_RUN_DIR,
            success=False,
            exit_code=None,
            stdout="",
            stderr="",
            runtime_seconds=0.0,
            refusal="no weather",
        )
        BatchResult(results=(refused,), total_runtime_seconds=0.0).cleanup()
