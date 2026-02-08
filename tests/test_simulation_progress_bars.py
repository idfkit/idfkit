"""Tests for the built-in tqdm progress bar context manager and resolve_on_progress."""

from __future__ import annotations

from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from idfkit import new_document
from idfkit.simulation.config import EnergyPlusConfig
from idfkit.simulation.progress import SimulationProgress
from idfkit.simulation.progress_bars import resolve_on_progress, tqdm_progress

# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def mock_config(tmp_path: Path) -> EnergyPlusConfig:
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
    epw = tmp_path / "weather.epw"
    epw.write_text("LOCATION,Chicago\n")
    return epw


# ---------------------------------------------------------------------------
# resolve_on_progress
# ---------------------------------------------------------------------------


class TestResolveOnProgress:
    """Tests for resolve_on_progress."""

    def test_none_returns_none(self) -> None:
        cb, cleanup = resolve_on_progress(None)
        assert cb is None
        assert cleanup is None

    def test_callable_returned_directly(self) -> None:
        def my_cb(event: SimulationProgress) -> None:
            pass

        cb, cleanup = resolve_on_progress(my_cb)
        assert cb is my_cb
        assert cleanup is None

    def test_lambda_returned_directly(self) -> None:
        fn = lambda e: None
        cb, cleanup = resolve_on_progress(fn)
        assert cb is fn
        assert cleanup is None

    @patch("idfkit.simulation.progress_bars._import_tqdm")
    def test_tqdm_string_creates_bar(self, mock_import: MagicMock) -> None:
        mock_tqdm_cls = MagicMock()
        mock_bar = MagicMock()
        mock_tqdm_cls.return_value = mock_bar
        mock_import.return_value = mock_tqdm_cls

        cb, cleanup = resolve_on_progress("tqdm")
        assert cb is not None
        assert cleanup is not None
        assert callable(cb)
        assert callable(cleanup)

    @patch("idfkit.simulation.progress_bars._import_tqdm")
    def test_tqdm_cleanup_closes_bar(self, mock_import: MagicMock) -> None:
        mock_tqdm_cls = MagicMock()
        mock_bar = MagicMock()
        mock_tqdm_cls.return_value = mock_bar
        mock_import.return_value = mock_tqdm_cls

        _cb, cleanup = resolve_on_progress("tqdm")
        assert cleanup is not None
        cleanup()
        mock_bar.close.assert_called_once()

    def test_invalid_string_raises(self) -> None:
        with pytest.raises(ValueError, match="on_progress must be 'tqdm'"):
            resolve_on_progress("invalid")

    def test_invalid_type_raises(self) -> None:
        with pytest.raises(TypeError, match="on_progress must be 'tqdm'"):
            resolve_on_progress(42)  # type: ignore[arg-type]


# ---------------------------------------------------------------------------
# tqdm_progress (context manager)
# ---------------------------------------------------------------------------


class TestTqdmProgress:
    """Tests for tqdm_progress context manager."""

    @patch("idfkit.simulation.progress_bars._import_tqdm")
    def test_yields_callable(self, mock_import: MagicMock) -> None:
        mock_tqdm_cls = MagicMock()
        mock_bar = MagicMock()
        mock_tqdm_cls.return_value = mock_bar
        mock_import.return_value = mock_tqdm_cls

        with tqdm_progress() as cb:
            assert callable(cb)

    @patch("idfkit.simulation.progress_bars._import_tqdm")
    def test_callback_updates_bar_with_percent(self, mock_import: MagicMock) -> None:
        mock_tqdm_cls = MagicMock()
        mock_bar = MagicMock()
        mock_tqdm_cls.return_value = mock_bar
        mock_import.return_value = mock_tqdm_cls

        with tqdm_progress() as cb:
            event = SimulationProgress(phase="simulating", message="test", percent=42.5)
            cb(event)

            assert mock_bar.n == 42.5
            mock_bar.set_postfix_str.assert_called_with("simulating", refresh=False)
            mock_bar.refresh.assert_called()

    @patch("idfkit.simulation.progress_bars._import_tqdm")
    def test_callback_handles_none_percent(self, mock_import: MagicMock) -> None:
        mock_tqdm_cls = MagicMock()
        mock_bar = MagicMock()
        mock_bar.n = 0
        mock_tqdm_cls.return_value = mock_bar
        mock_import.return_value = mock_tqdm_cls

        with tqdm_progress() as cb:
            event = SimulationProgress(phase="warmup", message="Warming up {1}", percent=None)
            cb(event)

            assert mock_bar.n == 0
            mock_bar.set_postfix_str.assert_called_with("warmup", refresh=False)

    @patch("idfkit.simulation.progress_bars._import_tqdm")
    def test_bar_closed_on_exit(self, mock_import: MagicMock) -> None:
        mock_tqdm_cls = MagicMock()
        mock_bar = MagicMock()
        mock_tqdm_cls.return_value = mock_bar
        mock_import.return_value = mock_tqdm_cls

        with tqdm_progress():
            pass

        assert mock_bar.n == 100
        mock_bar.close.assert_called_once()

    @patch("idfkit.simulation.progress_bars._import_tqdm")
    def test_bar_closed_on_exception(self, mock_import: MagicMock) -> None:
        mock_tqdm_cls = MagicMock()
        mock_bar = MagicMock()
        mock_bar.n = 42
        mock_tqdm_cls.return_value = mock_bar
        mock_import.return_value = mock_tqdm_cls

        with pytest.raises(RuntimeError), tqdm_progress():
            raise RuntimeError("boom")

        mock_bar.close.assert_called_once()
        # Bar should NOT be set to 100% on error
        assert mock_bar.n == 42

    @patch("idfkit.simulation.progress_bars._import_tqdm")
    def test_custom_desc(self, mock_import: MagicMock) -> None:
        mock_tqdm_cls = MagicMock()
        mock_bar = MagicMock()
        mock_tqdm_cls.return_value = mock_bar
        mock_import.return_value = mock_tqdm_cls

        with tqdm_progress(desc="My Run"):
            pass

        call_kwargs = mock_tqdm_cls.call_args[1]
        assert call_kwargs["desc"] == "My Run"

    def test_import_error_without_tqdm(self) -> None:
        with (
            patch.dict("sys.modules", {"tqdm": None, "tqdm.auto": None}),
            pytest.raises(ImportError, match="pip install idfkit\\[progress\\]"),
            tqdm_progress(),
        ):
            pass


# ---------------------------------------------------------------------------
# simulate() with on_progress="tqdm"
# ---------------------------------------------------------------------------


class TestSimulateWithTqdm:
    """Tests for simulate() accepting on_progress='tqdm'."""

    @patch("idfkit.simulation.progress_bars._import_tqdm")
    @patch("idfkit.simulation.runner.subprocess.Popen")
    def test_tqdm_string_creates_progress_bar(
        self,
        mock_popen: MagicMock,
        mock_import: MagicMock,
        mock_config: EnergyPlusConfig,
        weather_file: Path,
    ) -> None:
        mock_tqdm_cls = MagicMock()
        mock_bar = MagicMock()
        mock_tqdm_cls.return_value = mock_bar
        mock_import.return_value = mock_tqdm_cls

        proc = MagicMock()
        proc.stdout = iter(["Warming up {1}\n", "EnergyPlus Completed Successfully.\n"])
        proc.stderr = iter([])
        proc.wait.return_value = 0
        proc.returncode = 0
        mock_popen.return_value = proc

        from idfkit.simulation.runner import simulate

        model = new_document()
        result = simulate(model, weather_file, energyplus=mock_config, on_progress="tqdm")

        assert result.success
        mock_tqdm_cls.assert_called_once()
        mock_bar.close.assert_called_once()

    @patch("idfkit.simulation.progress_bars._import_tqdm")
    @patch("idfkit.simulation.runner.subprocess.Popen")
    def test_tqdm_bar_closed_on_error(
        self,
        mock_popen: MagicMock,
        mock_import: MagicMock,
        mock_config: EnergyPlusConfig,
        weather_file: Path,
    ) -> None:
        """tqdm bar is closed even if simulation raises."""
        mock_tqdm_cls = MagicMock()
        mock_bar = MagicMock()
        mock_tqdm_cls.return_value = mock_bar
        mock_import.return_value = mock_tqdm_cls

        mock_popen.side_effect = OSError("fake error")

        from idfkit.exceptions import SimulationError
        from idfkit.simulation.runner import simulate

        model = new_document()
        with pytest.raises(SimulationError):
            simulate(model, weather_file, energyplus=mock_config, on_progress="tqdm")

        mock_bar.close.assert_called_once()


# ---------------------------------------------------------------------------
# Batch runners reject on_progress="tqdm"
# ---------------------------------------------------------------------------


class TestBatchTqdmRejection:
    """Batch runners must reject on_progress='tqdm' with a clear error."""

    def test_sync_batch_rejects_tqdm(self, mock_config: EnergyPlusConfig, weather_file: Path) -> None:
        from idfkit.simulation.batch import SimulationJob, simulate_batch

        model = new_document()
        jobs = [SimulationJob(model=model, weather=weather_file, label="j0")]
        with pytest.raises(ValueError, match="not supported for batch"):
            simulate_batch(jobs, energyplus=mock_config, on_progress="tqdm")  # type: ignore[arg-type]

    @pytest.mark.asyncio
    async def test_async_batch_rejects_tqdm(self, mock_config: EnergyPlusConfig, weather_file: Path) -> None:
        from idfkit.simulation.async_batch import async_simulate_batch
        from idfkit.simulation.batch import SimulationJob

        model = new_document()
        jobs = [SimulationJob(model=model, weather=weather_file, label="j0")]
        with pytest.raises(ValueError, match="not supported for batch"):
            await async_simulate_batch(jobs, energyplus=mock_config, on_progress="tqdm")  # type: ignore[arg-type]


# ---------------------------------------------------------------------------
# tqdm bar cleaned up on early errors (before simulation starts)
# ---------------------------------------------------------------------------


class TestTqdmCleanupOnEarlyError:
    """tqdm bar is closed even when errors occur before the simulation subprocess starts."""

    @patch("idfkit.simulation.progress_bars._import_tqdm")
    def test_tqdm_cleaned_up_on_missing_weather(self, mock_import: MagicMock, mock_config: EnergyPlusConfig) -> None:
        """Bar is closed when weather file doesn't exist (error before subprocess)."""
        mock_tqdm_cls = MagicMock()
        mock_bar = MagicMock()
        mock_tqdm_cls.return_value = mock_bar
        mock_import.return_value = mock_tqdm_cls

        from idfkit.exceptions import SimulationError
        from idfkit.simulation.runner import simulate

        model = new_document()
        with pytest.raises(SimulationError, match="Weather file not found"):
            simulate(model, "/nonexistent/weather.epw", energyplus=mock_config, on_progress="tqdm")

        mock_bar.close.assert_called_once()
