"""Tests for the simulation progress parser and callback wiring."""

from __future__ import annotations

import textwrap
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from idfkit import new_document
from idfkit.exceptions import SimulationError
from idfkit.simulation.async_runner import async_simulate
from idfkit.simulation.batch import SimulationJob, simulate_batch
from idfkit.simulation.config import EnergyPlusConfig
from idfkit.simulation.progress import (
    ProgressParser,
    SimulationProgress,
    _date_to_day_of_year,
    _day_span,
)
from idfkit.simulation.runner import simulate

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
# Helper: sample EnergyPlus stdout
# ---------------------------------------------------------------------------

ANNUAL_STDOUT = textwrap.dedent("""\
    EnergyPlus, Version 24.1.0-87b2e308c0
    Initializing New Environment Parameters
    Warming up {1}
    Warming up {2}
    Warming up {3}
    Warmup Complete
    Starting Simulation at 01/01/2017 for CHICAGO AnnualRun from 01/01/2017 to 12/31/2017
    Continuing Simulation at 02/01/2017 for CHICAGO AnnualRun
    Continuing Simulation at 03/01/2017 for CHICAGO AnnualRun
    Continuing Simulation at 04/01/2017 for CHICAGO AnnualRun
    Continuing Simulation at 06/01/2017 for CHICAGO AnnualRun
    Continuing Simulation at 12/01/2017 for CHICAGO AnnualRun
    Writing tabular output file results using comma format.
    Writing final SQL reports
    EnergyPlus Completed Successfully.
""")

DESIGN_DAY_STDOUT = textwrap.dedent("""\
    EnergyPlus, Version 24.1.0-87b2e308c0
    Initializing New Environment Parameters
    Warming up {1}
    Warming up {2}
    Warmup Complete
    Starting Simulation at 07/21 for CHICAGO_IL_USA ANNUAL COOLING 1% DESIGN CONDITIONS
    Writing tabular output file results using comma format.
    EnergyPlus Completed Successfully.
""")

MULTI_ENV_STDOUT = textwrap.dedent("""\
    EnergyPlus, Version 24.1.0-87b2e308c0
    Initializing New Environment Parameters
    Warming up {1}
    Warmup Complete
    Starting Simulation at 01/21 for CHICAGO WINTER DESIGN DAY
    Initializing New Environment Parameters
    Warming up {1}
    Warming up {2}
    Warmup Complete
    Starting Simulation at 07/21 for CHICAGO SUMMER DESIGN DAY
    Writing tabular output file results using comma format.
    EnergyPlus Completed Successfully.
""")


# ---------------------------------------------------------------------------
# _date_to_day_of_year
# ---------------------------------------------------------------------------


class TestDateToDayOfYear:
    """Tests for _date_to_day_of_year helper."""

    def test_jan_1(self) -> None:
        assert _date_to_day_of_year("01/01") == 1

    def test_jan_31(self) -> None:
        assert _date_to_day_of_year("01/31") == 31

    def test_feb_1(self) -> None:
        assert _date_to_day_of_year("02/01") == 32

    def test_mar_1(self) -> None:
        assert _date_to_day_of_year("03/01") == 60

    def test_jul_21(self) -> None:
        # 31+28+31+30+31+30+21 = 202
        assert _date_to_day_of_year("07/21") == 202

    def test_dec_31(self) -> None:
        assert _date_to_day_of_year("12/31") == 365

    def test_with_year(self) -> None:
        assert _date_to_day_of_year("01/01/2017") == 1
        assert _date_to_day_of_year("12/31/2017") == 365

    def test_invalid_returns_1(self) -> None:
        assert _date_to_day_of_year("invalid") == 1
        assert _date_to_day_of_year("") == 1
        assert _date_to_day_of_year("xx/yy") == 1


# ---------------------------------------------------------------------------
# _day_span
# ---------------------------------------------------------------------------


class TestDaySpan:
    """Tests for _day_span helper."""

    def test_same_day(self) -> None:
        assert _day_span(1, 1) == 1

    def test_full_year(self) -> None:
        assert _day_span(1, 365) == 365

    def test_single_month(self) -> None:
        assert _day_span(1, 31) == 31

    def test_wrap_around(self) -> None:
        # Oct 1 (274) to Jan 31 (31) = 92+31 = 123
        assert _day_span(274, 31) == 123


# ---------------------------------------------------------------------------
# ProgressParser
# ---------------------------------------------------------------------------


class TestProgressParser:
    """Tests for ProgressParser."""

    def test_empty_line_returns_none(self) -> None:
        parser = ProgressParser()
        assert parser.parse_line("") is None
        assert parser.parse_line("   ") is None

    def test_unrecognized_line_returns_none(self) -> None:
        parser = ProgressParser()
        assert parser.parse_line("Some random EnergyPlus output") is None

    def test_warmup(self) -> None:
        parser = ProgressParser()
        event = parser.parse_line("Warming up {1}")
        assert event is not None
        assert event.phase == "warmup"
        assert event.warmup_day == 1
        assert event.percent is None

    def test_warmup_increments(self) -> None:
        parser = ProgressParser()
        parser.parse_line("Warming up {1}")
        event = parser.parse_line("Warming up {5}")
        assert event is not None
        assert event.warmup_day == 5

    def test_initializing(self) -> None:
        parser = ProgressParser()
        event = parser.parse_line("Initializing New Environment Parameters")
        assert event is not None
        assert event.phase == "initializing"

    def test_start_simulation_with_period(self) -> None:
        parser = ProgressParser()
        event = parser.parse_line(
            "Starting Simulation at 01/01/2017 for CHICAGO AnnualRun from 01/01/2017 to 12/31/2017"
        )
        assert event is not None
        assert event.phase == "simulating"
        assert event.environment == "CHICAGO AnnualRun"
        assert event.sim_day == 1
        assert event.sim_total_days == 365
        assert event.percent == 0.0  # First day of 365

    def test_start_simulation_without_period(self) -> None:
        parser = ProgressParser()
        event = parser.parse_line("Starting Simulation at 07/21 for CHICAGO SUMMER DESIGN DAY")
        assert event is not None
        assert event.phase == "simulating"
        assert event.environment == "CHICAGO SUMMER DESIGN DAY"
        assert event.sim_day == 202
        assert event.percent is None  # No period info, can't estimate

    def test_continue_simulation_with_percentage(self) -> None:
        parser = ProgressParser()
        # First establish the simulation period
        parser.parse_line("Starting Simulation at 01/01/2017 for AnnualRun from 01/01/2017 to 12/31/2017")
        # Now continue
        event = parser.parse_line("Continuing Simulation at 07/01/2017 for AnnualRun")
        assert event is not None
        assert event.phase == "simulating"
        assert event.sim_day == 182  # July 1
        assert event.sim_total_days == 365
        assert event.percent is not None
        # 181 elapsed days / 365 total * 100
        assert abs(event.percent - (181 / 365 * 100)) < 0.1

    def test_continue_simulation_tracks_environment(self) -> None:
        parser = ProgressParser()
        parser.parse_line("Starting Simulation at 01/01 for WINTER RUN from 01/01 to 01/31")
        event = parser.parse_line("Continuing Simulation at 01/15 for WINTER RUN")
        assert event is not None
        assert event.environment == "WINTER RUN"

    def test_warmup_complete(self) -> None:
        parser = ProgressParser()
        parser.parse_line("Warming up {3}")
        event = parser.parse_line("Warmup Complete")
        assert event is not None
        assert event.phase == "warmup"
        assert event.warmup_day == 3

    def test_writing_tabular(self) -> None:
        parser = ProgressParser()
        event = parser.parse_line("Writing tabular output file results using comma format.")
        assert event is not None
        assert event.phase == "postprocessing"

    def test_writing_sql(self) -> None:
        parser = ProgressParser()
        event = parser.parse_line("Writing final SQL reports")
        assert event is not None
        assert event.phase == "postprocessing"

    def test_completed(self) -> None:
        parser = ProgressParser()
        event = parser.parse_line("EnergyPlus Completed Successfully.")
        assert event is not None
        assert event.phase == "complete"
        assert event.percent == 100.0

    def test_full_annual_stdout_parse(self) -> None:
        """Parse a full annual simulation stdout and check event sequence."""
        parser = ProgressParser()
        events: list[SimulationProgress] = []
        for line in ANNUAL_STDOUT.splitlines():
            event = parser.parse_line(line)
            if event is not None:
                events.append(event)

        # Check phase sequence
        phases = [e.phase for e in events]
        assert phases[0] == "initializing"
        assert phases[1] == "warmup"  # {1}
        assert phases[2] == "warmup"  # {2}
        assert phases[3] == "warmup"  # {3}
        assert phases[4] == "warmup"  # Warmup Complete
        assert phases[5] == "simulating"  # Starting
        assert phases[6] == "simulating"  # Continuing Feb
        assert phases[7] == "simulating"  # Continuing Mar
        assert phases[8] == "simulating"  # Continuing Apr
        assert phases[9] == "simulating"  # Continuing Jun
        assert phases[10] == "simulating"  # Continuing Dec
        assert phases[11] == "postprocessing"
        assert phases[12] == "postprocessing"
        assert phases[13] == "complete"

        # The starting event should have 0% (day 1 of 365)
        assert events[5].percent == 0.0
        # December should be close to 100%
        assert events[10].percent is not None
        assert events[10].percent > 90.0
        # Completed should be 100%
        assert events[13].percent == 100.0

    def test_multi_environment_resets(self) -> None:
        """Initializing New Environment resets warmup counter."""
        parser = ProgressParser()
        events: list[SimulationProgress] = []
        for line in MULTI_ENV_STDOUT.splitlines():
            event = parser.parse_line(line)
            if event is not None:
                events.append(event)

        # Should see two initializing phases
        init_events = [e for e in events if e.phase == "initializing"]
        assert len(init_events) == 2

        # After second init, warmup should restart at 1.
        # Filter to "Warming up {1}" lines (exclude "Warmup Complete"
        # which also carries the last warmup_day from its env).
        warmup_start_events = [
            e for e in events if e.phase == "warmup" and e.warmup_day == 1 and "Warming up" in e.message
        ]
        assert len(warmup_start_events) == 2  # one per environment

    def test_job_context_not_set_by_default(self) -> None:
        parser = ProgressParser()
        event = parser.parse_line("Warming up {1}")
        assert event is not None
        assert event.job_index is None
        assert event.job_label is None

    def test_set_job_context(self) -> None:
        parser = ProgressParser()
        parser.set_job_context(index=3, label="test-job")
        event = parser.parse_line("Warming up {1}")
        assert event is not None
        assert event.job_index == 3
        assert event.job_label == "test-job"

    def test_percent_clamped_to_100(self) -> None:
        """Percentage should never exceed 100.0."""
        parser = ProgressParser()
        # Set up a very short simulation period
        parser.parse_line("Starting Simulation at 01/01 for SHORT from 01/01 to 01/05")
        # Simulate a date after the end date
        event = parser.parse_line("Continuing Simulation at 01/10 for SHORT")
        assert event is not None
        assert event.percent is not None
        assert event.percent <= 100.0

    def test_sim_total_days_reset_on_new_environment(self) -> None:
        """_sim_total_days must reset when a new environment starts."""
        parser = ProgressParser()

        # First environment: annual run with known date range
        parser.parse_line("Initializing New Environment Parameters")
        parser.parse_line("Warming up {1}")
        parser.parse_line("Warmup Complete")
        e1 = parser.parse_line("Starting Simulation at 01/01/2017 for AnnualRun from 01/01/2017 to 12/31/2017")
        assert e1 is not None
        assert e1.sim_total_days == 365
        assert e1.percent is not None  # has a percentage

        # Second environment: design day with NO date range
        parser.parse_line("Initializing New Environment Parameters")
        parser.parse_line("Warming up {1}")
        parser.parse_line("Warmup Complete")
        e2 = parser.parse_line("Starting Simulation at 07/21 for SummerDesignDay")
        assert e2 is not None
        # Must NOT inherit the previous 365-day total
        assert e2.sim_total_days is None
        assert e2.percent is None

    def test_sim_total_days_none_without_date_range(self) -> None:
        """Starting Simulation without from/to must set sim_total_days to None."""
        parser = ProgressParser()
        parser.parse_line("Initializing New Environment Parameters")
        event = parser.parse_line("Starting Simulation at 01/01 for DesignDay")
        assert event is not None
        assert event.sim_total_days is None
        assert event.percent is None


# ---------------------------------------------------------------------------
# SimulationProgress dataclass
# ---------------------------------------------------------------------------


class TestSimulationProgress:
    """Tests for SimulationProgress dataclass."""

    def test_frozen(self) -> None:
        event = SimulationProgress(phase="warmup", message="Warming up {1}")
        with pytest.raises(AttributeError):
            event.phase = "simulating"  # type: ignore[misc]

    def test_defaults(self) -> None:
        event = SimulationProgress(phase="warmup", message="test")
        assert event.percent is None
        assert event.environment is None
        assert event.warmup_day is None
        assert event.sim_day is None
        assert event.sim_total_days is None
        assert event.job_index is None
        assert event.job_label is None

    def test_all_fields(self) -> None:
        event = SimulationProgress(
            phase="simulating",
            message="Continuing at 07/01",
            percent=50.0,
            environment="AnnualRun",
            sim_day=182,
            sim_total_days=365,
            job_index=2,
            job_label="baseline",
        )
        assert event.phase == "simulating"
        assert event.percent == 50.0
        assert event.environment == "AnnualRun"
        assert event.sim_day == 182
        assert event.sim_total_days == 365
        assert event.job_index == 2
        assert event.job_label == "baseline"


# ---------------------------------------------------------------------------
# simulate() with on_progress callback
# ---------------------------------------------------------------------------


class TestSimulateWithProgress:
    """Tests for simulate() on_progress callback wiring."""

    @patch("idfkit.simulation.runner.subprocess.Popen")
    def test_on_progress_called(self, mock_popen: MagicMock, mock_config: EnergyPlusConfig, weather_file: Path) -> None:
        """on_progress callback receives SimulationProgress events."""
        proc = MagicMock()
        proc.stdout = iter(["Warming up {1}\n", "EnergyPlus Completed Successfully.\n"])
        proc.stderr = iter([])
        proc.wait.return_value = 0
        proc.returncode = 0
        mock_popen.return_value = proc

        events: list[SimulationProgress] = []
        model = new_document()
        simulate(model, weather_file, energyplus=mock_config, on_progress=events.append)

        assert len(events) == 2
        assert events[0].phase == "warmup"
        assert events[0].warmup_day == 1
        assert events[1].phase == "complete"
        assert events[1].percent == 100.0

    @patch("idfkit.simulation.runner.subprocess.Popen")
    def test_on_progress_full_annual_sequence(
        self, mock_popen: MagicMock, mock_config: EnergyPlusConfig, weather_file: Path
    ) -> None:
        """on_progress fires for each recognized stdout line."""
        proc = MagicMock()
        proc.stdout = iter(line + "\n" for line in ANNUAL_STDOUT.splitlines())
        proc.stderr = iter([])
        proc.wait.return_value = 0
        proc.returncode = 0
        mock_popen.return_value = proc

        events: list[SimulationProgress] = []
        model = new_document()
        simulate(model, weather_file, energyplus=mock_config, on_progress=events.append)

        phases = [e.phase for e in events]
        assert "initializing" in phases
        assert "warmup" in phases
        assert "simulating" in phases
        assert "postprocessing" in phases
        assert "complete" in phases

    @patch("idfkit.simulation.runner.subprocess.run")
    def test_no_progress_uses_subprocess_run(
        self, mock_run: MagicMock, mock_config: EnergyPlusConfig, weather_file: Path
    ) -> None:
        """Without on_progress, simulate() uses subprocess.run (original path)."""
        mock_run.return_value = MagicMock(returncode=0, stdout="ok", stderr="")
        model = new_document()
        result = simulate(model, weather_file, energyplus=mock_config)
        assert result.success
        mock_run.assert_called_once()

    @patch("idfkit.simulation.runner.subprocess.Popen")
    def test_stdout_captured_with_progress(
        self, mock_popen: MagicMock, mock_config: EnergyPlusConfig, weather_file: Path
    ) -> None:
        """All stdout is still captured in result.stdout when using on_progress."""
        stdout_lines = ["line one\n", "Warming up {1}\n", "line three\n"]
        proc = MagicMock()
        proc.stdout = iter(stdout_lines)
        proc.stderr = iter([])
        proc.wait.return_value = 0
        proc.returncode = 0
        mock_popen.return_value = proc

        model = new_document()
        result = simulate(model, weather_file, energyplus=mock_config, on_progress=lambda _: None)

        assert "line one" in result.stdout
        assert "Warming up {1}" in result.stdout
        assert "line three" in result.stdout


# ---------------------------------------------------------------------------
# async_simulate() with on_progress callback
# ---------------------------------------------------------------------------


def _make_mock_process_with_stdout(
    stdout_lines: list[bytes],
    returncode: int = 0,
    stderr: bytes = b"",
) -> MagicMock:
    """Create a mock asyncio.subprocess.Process with line-by-line stdout."""
    proc = MagicMock()
    proc.returncode = returncode
    proc.kill = MagicMock()
    proc.wait = AsyncMock()

    # For the simple path (no on_progress)
    full_stdout = b"".join(stdout_lines)
    proc.communicate = AsyncMock(return_value=(full_stdout, stderr))

    # For the progress path: simulate readline behavior
    line_iter = iter([*stdout_lines, b""])  # b"" signals EOF

    async def readline() -> bytes:
        return next(line_iter)

    proc.stdout = MagicMock()
    proc.stdout.readline = readline

    # stderr.read() for the progress path
    async def read_stderr() -> bytes:
        return stderr

    proc.stderr = MagicMock()
    proc.stderr.read = read_stderr

    return proc


class TestAsyncSimulateWithProgress:
    """Tests for async_simulate() on_progress callback wiring."""

    @pytest.mark.asyncio
    @patch("idfkit.simulation.async_runner.asyncio.create_subprocess_exec")
    async def test_sync_callback(self, mock_exec: AsyncMock, mock_config: EnergyPlusConfig, weather_file: Path) -> None:
        """Sync on_progress callback works with async_simulate."""
        proc = _make_mock_process_with_stdout([
            b"Warming up {1}\n",
            b"EnergyPlus Completed Successfully.\n",
        ])
        mock_exec.return_value = proc

        events: list[SimulationProgress] = []
        model = new_document()
        result = await async_simulate(model, weather_file, energyplus=mock_config, on_progress=events.append)

        assert result.success
        assert len(events) == 2
        assert events[0].phase == "warmup"
        assert events[1].phase == "complete"

    @pytest.mark.asyncio
    @patch("idfkit.simulation.async_runner.asyncio.create_subprocess_exec")
    async def test_async_callback(
        self, mock_exec: AsyncMock, mock_config: EnergyPlusConfig, weather_file: Path
    ) -> None:
        """Async on_progress callback is awaited."""
        proc = _make_mock_process_with_stdout([
            b"Warming up {1}\n",
            b"EnergyPlus Completed Successfully.\n",
        ])
        mock_exec.return_value = proc

        events: list[SimulationProgress] = []

        async def async_cb(event: SimulationProgress) -> None:
            events.append(event)

        model = new_document()
        result = await async_simulate(model, weather_file, energyplus=mock_config, on_progress=async_cb)

        assert result.success
        assert len(events) == 2

    @pytest.mark.asyncio
    @patch("idfkit.simulation.async_runner.asyncio.create_subprocess_exec")
    async def test_no_progress_uses_communicate(
        self, mock_exec: AsyncMock, mock_config: EnergyPlusConfig, weather_file: Path
    ) -> None:
        """Without on_progress, uses proc.communicate() (original path)."""
        proc = _make_mock_process_with_stdout([b"ok\n"])
        mock_exec.return_value = proc

        model = new_document()
        result = await async_simulate(model, weather_file, energyplus=mock_config)

        assert result.success
        proc.communicate.assert_called_once()


# ---------------------------------------------------------------------------
# simulate_batch() with on_progress callback
# ---------------------------------------------------------------------------


class TestBatchWithProgress:
    """Tests for simulate_batch() on_progress wiring."""

    @patch("idfkit.simulation.runner.subprocess.Popen")
    def test_on_progress_includes_job_context(
        self, mock_popen: MagicMock, mock_config: EnergyPlusConfig, weather_file: Path
    ) -> None:
        """Events from batch carry job_index and job_label."""
        proc = MagicMock()
        proc.stdout = iter(["Warming up {1}\n", "EnergyPlus Completed Successfully.\n"])
        proc.stderr = iter([])
        proc.wait.return_value = 0
        proc.returncode = 0
        mock_popen.return_value = proc

        events: list[SimulationProgress] = []
        jobs = [
            SimulationJob(model=new_document(), weather=weather_file, label="run-0"),
        ]
        simulate_batch(jobs, energyplus=mock_config, on_progress=events.append, max_workers=1)

        assert len(events) >= 1
        assert events[0].job_index == 0
        assert events[0].job_label == "run-0"

    @patch("idfkit.simulation.runner.subprocess.Popen")
    def test_both_progress_and_on_progress(
        self, mock_popen: MagicMock, mock_config: EnergyPlusConfig, weather_file: Path
    ) -> None:
        """Both job-level progress and sim-level on_progress callbacks fire."""
        proc = MagicMock()
        proc.stdout = iter(["Warming up {1}\n", "EnergyPlus Completed Successfully.\n"])
        proc.stderr = iter([])
        proc.wait.return_value = 0
        proc.returncode = 0
        mock_popen.return_value = proc

        sim_events: list[SimulationProgress] = []
        job_events: list[dict[str, object]] = []

        def job_cb(**kwargs: object) -> None:
            job_events.append(kwargs)

        jobs = [SimulationJob(model=new_document(), weather=weather_file, label="run-0")]
        simulate_batch(
            jobs,
            energyplus=mock_config,
            on_progress=sim_events.append,
            progress=job_cb,
            max_workers=1,
        )

        # sim-level events should fire during simulation
        assert len(sim_events) >= 1
        # job-level progress fires after completion
        assert len(job_events) == 1
        assert job_events[0]["completed"] == 1


# ---------------------------------------------------------------------------
# Sync runner: stderr thread joined on timeout, stderr in error
# ---------------------------------------------------------------------------


class TestSyncRunnerStderrOnTimeout:
    """Ensure the stderr thread is joined and stderr is included in timeout errors."""

    @patch("idfkit.simulation.runner.subprocess.Popen")
    def test_stderr_included_in_timeout_error(
        self, mock_popen: MagicMock, mock_config: EnergyPlusConfig, weather_file: Path
    ) -> None:
        """Timeout error should contain partial stderr."""
        from idfkit.exceptions import SimulationError

        proc = MagicMock()
        # stdout blocks indefinitely (simulating a hung process)
        proc.stdout = iter(["Warming up {1}\n"])
        proc.stderr = iter(["some stderr output\n"])
        proc.wait.return_value = -9
        proc.returncode = -9
        proc.kill = MagicMock()
        mock_popen.return_value = proc

        model = new_document()
        with pytest.raises(SimulationError, match="timed out") as exc_info:
            simulate(
                model,
                weather_file,
                energyplus=mock_config,
                on_progress=lambda _: None,
                timeout=0.0,  # Immediate timeout
            )

        # stderr should be captured despite the timeout
        assert exc_info.value.stderr is not None
        assert "some stderr output" in exc_info.value.stderr

    @patch("idfkit.simulation.runner.subprocess.Popen")
    def test_stderr_thread_joined_on_callback_error(
        self, mock_popen: MagicMock, mock_config: EnergyPlusConfig, weather_file: Path
    ) -> None:
        """stderr is captured when callback raises."""
        from idfkit.exceptions import SimulationError

        proc = MagicMock()
        proc.stdout = iter(["Warming up {1}\n"])
        proc.stderr = iter(["warning: something\n"])
        proc.wait.return_value = 0
        proc.returncode = 0
        proc.kill = MagicMock()
        mock_popen.return_value = proc

        def bad_callback(event: SimulationProgress) -> None:
            raise RuntimeError("boom")

        model = new_document()
        with pytest.raises(SimulationError, match="boom") as exc_info:
            simulate(model, weather_file, energyplus=mock_config, on_progress=bad_callback)

        # stderr should be present despite the error
        assert exc_info.value.stderr is not None
        assert "warning: something" in exc_info.value.stderr


# ---------------------------------------------------------------------------
# Async runner: subprocess killed on callback error
# ---------------------------------------------------------------------------


class TestAsyncRunnerSubprocessCleanup:
    """Ensure EnergyPlus subprocess is killed when callback raises."""

    @pytest.mark.asyncio
    @patch("idfkit.simulation.async_runner.asyncio.create_subprocess_exec")
    async def test_process_killed_on_callback_error(
        self, mock_exec: AsyncMock, mock_config: EnergyPlusConfig, weather_file: Path
    ) -> None:
        """If on_progress raises, the subprocess must be killed."""
        proc = _make_mock_process_with_stdout([
            b"Warming up {1}\n",
            b"EnergyPlus Completed Successfully.\n",
        ])
        mock_exec.return_value = proc

        def bad_callback(event: SimulationProgress) -> None:
            raise RuntimeError("boom")

        model = new_document()
        with pytest.raises(SimulationError, match="boom"):
            await async_simulate(model, weather_file, energyplus=mock_config, on_progress=bad_callback)

        # Subprocess must have been killed
        proc.kill.assert_called()
