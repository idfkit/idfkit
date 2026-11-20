"""The garbage-collection safety net for the temporary run directories simulate() creates.

A result that owns an idfkit-created ``idfkit_sim_*`` directory and is dropped without
``cleanup()`` deletes it, with a ``ResourceWarning``, once nothing that could read it is
reachable. A caller's ``output_dir``, a cache entry and an ``fs=`` run are never touched.

Every test points the temp root at ``tmp_path``, so the directories land there.
"""

from __future__ import annotations

import asyncio
import copy
import dataclasses
import gc
import os
import pickle
import subprocess
import sys
import tempfile
import warnings
from collections.abc import Callable, Iterator
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from conftest import InMemoryFileSystem, runnable_model

from idfkit import LATEST_VERSION
from idfkit.exceptions import SimulationError
from idfkit.simulation._run_dir import lease_for, register_temp_run_dir
from idfkit.simulation.async_batch import async_simulate_batch
from idfkit.simulation.async_runner import async_simulate
from idfkit.simulation.batch import BatchResult, SimulationJob, simulate_batch
from idfkit.simulation.cache import SimulationCache
from idfkit.simulation.config import EnergyPlusConfig
from idfkit.simulation.result import SimulationResult
from idfkit.simulation.runner import simulate


@pytest.fixture
def temp_root(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    """Make ``tempfile.mkdtemp`` (and so every ``idfkit_sim_*`` directory) create under ``tmp_path``."""
    root = tmp_path / "tmp"
    root.mkdir()
    monkeypatch.setattr(tempfile, "tempdir", str(root))
    return root


@pytest.fixture
def mock_config(tmp_path: Path) -> EnergyPlusConfig:
    exe = tmp_path / "energyplus"
    exe.touch()
    exe.chmod(0o755)
    idd = tmp_path / "Energy+.idd"
    idd.write_text("!IDD_Version 24.1.0\n")
    return EnergyPlusConfig(executable=exe, version=LATEST_VERSION, install_dir=tmp_path, idd_path=idd)


@pytest.fixture
def weather_file(tmp_path: Path) -> Path:
    epw = tmp_path / "weather.epw"
    epw.write_text("LOCATION,Chicago\n")
    return epw


@pytest.fixture
def mock_run() -> Iterator[MagicMock]:
    with patch("idfkit.simulation.runner.run_process") as mock:
        mock.return_value = MagicMock(returncode=0, stdout="ok", stderr="")
        yield mock


def _resource_warnings(caught: list[warnings.WarningMessage]) -> list[str]:
    """The run-directory warnings idfkit issued, leaving out unrelated ones (an unclosed file elsewhere)."""
    return [
        str(w.message)
        for w in caught
        if issubclass(w.category, ResourceWarning) and Path(w.filename).name == "_run_dir.py"
    ]


class _Recorder:
    """Records every warning raised inside the block, garbage collection included."""

    def __enter__(self) -> list[warnings.WarningMessage]:
        # Collect garbage other tests in this worker left first, so their results do not report here.
        gc.collect()
        self._cm = warnings.catch_warnings(record=True)
        caught = self._cm.__enter__()
        warnings.simplefilter("always")
        return caught

    def __exit__(self, *exc: object) -> None:
        gc.collect()  # so the block sees finalizers of objects dropped in it, on any interpreter
        self._cm.__exit__(*exc)


def _sim_dirs(root: Path) -> list[Path]:
    return sorted(root.glob("idfkit_sim_*"))


@pytest.mark.usefixtures("mock_run")
class TestSimulate:
    def test_dropped_result_deletes_its_dir_and_warns(
        self, temp_root: Path, mock_config: EnergyPlusConfig, weather_file: Path
    ) -> None:
        result = simulate(runnable_model(), weather_file, energyplus=mock_config)
        run_dir = result.run_dir
        assert run_dir.parent == temp_root
        assert run_dir.exists()
        with _Recorder() as caught:
            del result
        assert not run_dir.exists()
        [message] = _resource_warnings(caught)
        assert str(run_dir) in message
        assert "cleanup()" in message

    def test_with_block_does_not_warn(self, temp_root: Path, mock_config: EnergyPlusConfig, weather_file: Path) -> None:
        with _Recorder() as caught, simulate(runnable_model(), weather_file, energyplus=mock_config):
            pass
        assert _resource_warnings(caught) == []
        assert _sim_dirs(temp_root) == []

    def test_cleanup_then_drop_does_not_warn(
        self, temp_root: Path, mock_config: EnergyPlusConfig, weather_file: Path
    ) -> None:
        with _Recorder() as caught:
            result = simulate(runnable_model(), weather_file, energyplus=mock_config)
            result.cleanup()
            del result
        assert _resource_warnings(caught) == []

    def test_failed_run_deletes_its_dir_without_warning(
        self, temp_root: Path, mock_config: EnergyPlusConfig, weather_file: Path, mock_run: MagicMock
    ) -> None:
        mock_run.side_effect = subprocess.TimeoutExpired(cmd="energyplus", timeout=1)
        with _Recorder() as caught, pytest.raises(SimulationError):
            simulate(runnable_model(), weather_file, energyplus=mock_config, timeout=1)
        assert _resource_warnings(caught) == []
        assert _sim_dirs(temp_root) == []

    def test_output_dir_is_never_touched(
        self, temp_root: Path, tmp_path: Path, mock_config: EnergyPlusConfig, weather_file: Path
    ) -> None:
        out = tmp_path / "out"
        with _Recorder() as caught:
            result = simulate(runnable_model(), weather_file, energyplus=mock_config, output_dir=out)
            assert lease_for(result.run_dir) is None
            del result
        assert _resource_warnings(caught) == []
        assert (out / "model.idf").exists()

    def test_cache_hit_is_never_touched(
        self, temp_root: Path, tmp_path: Path, mock_config: EnergyPlusConfig, weather_file: Path
    ) -> None:
        cache = SimulationCache(cache_dir=tmp_path / "cache")
        with simulate(runnable_model(), weather_file, energyplus=mock_config, cache=cache):
            pass
        with _Recorder() as caught:
            hit = simulate(runnable_model(), weather_file, energyplus=mock_config, cache=cache)
            assert hit.cached
            entry = hit.run_dir
            del hit
        assert _resource_warnings(caught) == []
        assert entry.exists()

    def test_fs_run_is_never_touched(self, temp_root: Path, mock_config: EnergyPlusConfig, weather_file: Path) -> None:
        fs = InMemoryFileSystem()
        with _Recorder() as caught:
            result = simulate(runnable_model(), weather_file, energyplus=mock_config, output_dir="remote/out", fs=fs)
            del result
        assert _resource_warnings(caught) == []
        assert fs.exists("remote/out/model.idf")


class TestSharedDirectory:
    """Every copy of a result shares one lease, so the directory outlives all but the last."""

    @staticmethod
    def _owned(temp_root: Path) -> SimulationResult:
        run_dir = Path(tempfile.mkdtemp(prefix="idfkit_sim_"))
        lease = register_temp_run_dir(run_dir)
        result = SimulationResult(
            run_dir=run_dir, success=True, exit_code=0, stdout="", stderr="", runtime_seconds=0.0, owns_run_dir=True
        )
        assert result._run_dir_lease is lease  # pyright: ignore[reportPrivateUsage]
        return result

    def test_copies_keep_the_dir_alive(self, temp_root: Path) -> None:
        result = self._owned(temp_root)
        run_dir = result.run_dir
        copies = [copy.copy(result), copy.deepcopy(result), dataclasses.replace(result, stdout="changed")]
        with _Recorder() as caught:
            del result
            while len(copies) > 1:
                copies.pop()
                gc.collect()
                assert run_dir.exists()
            assert _resource_warnings(caught) == []
            copies.clear()
        assert not run_dir.exists()
        assert len(_resource_warnings(caught)) == 1

    def test_cleanup_of_a_copy_releases_every_copy(self, temp_root: Path) -> None:
        result = self._owned(temp_root)
        other = copy.copy(result)
        with _Recorder() as caught:
            other.cleanup()
            del result, other
        assert _resource_warnings(caught) == []

    def test_pickled_result_is_no_longer_reaped(self, temp_root: Path) -> None:
        result = self._owned(temp_root)
        run_dir = result.run_dir
        with _Recorder() as caught:
            restored = _pickle_roundtrip(result)
            assert restored._run_dir_lease is None  # pyright: ignore[reportPrivateUsage]
            del result
        assert _resource_warnings(caught) == []
        assert run_dir.exists()  # another process may read it through its copy
        assert restored.owns_run_dir
        restored.cleanup()  # still the caller's to delete
        assert not run_dir.exists()

    def test_hand_built_owning_result_is_not_tracked(self, temp_root: Path) -> None:
        run_dir = Path(tempfile.mkdtemp(prefix="idfkit_sim_"))
        with _Recorder() as caught:
            result = SimulationResult(
                run_dir=run_dir, success=True, exit_code=0, stdout="", stderr="", runtime_seconds=0.0, owns_run_dir=True
            )
            assert result._run_dir_lease is None  # pyright: ignore[reportPrivateUsage]
            del result
        assert _resource_warnings(caught) == []
        assert run_dir.exists()

    def test_forked_child_never_deletes(self, temp_root: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        """A lease acts only in the process that made it; a fork inherits it with another pid."""
        result = self._owned(temp_root)
        run_dir = result.run_dir
        real_pid = os.getpid()
        monkeypatch.setattr(os, "getpid", lambda: real_pid + 1)
        with _Recorder() as caught:
            del result
        assert _resource_warnings(caught) == []
        assert run_dir.exists()


@pytest.mark.usefixtures("mock_run")
class TestBatch:
    @staticmethod
    def _jobs(weather_file: Path, n: int = 3) -> list[SimulationJob]:
        return [SimulationJob(model=runnable_model(), weather=weather_file, label=f"j{i}") for i in range(n)]

    def test_dropped_batch_warns_once_and_deletes_every_dir(
        self, temp_root: Path, mock_config: EnergyPlusConfig, weather_file: Path
    ) -> None:
        batch = simulate_batch(self._jobs(weather_file), energyplus=mock_config, max_workers=3)
        assert len(_sim_dirs(temp_root)) == 3
        with _Recorder() as caught:
            for result in batch:  # the reported pattern: read, never clean up
                assert result.success
            del batch, result
        assert _sim_dirs(temp_root) == []
        [message] = _resource_warnings(caught)
        assert "BatchResult with 3 temporary run directories" in message

    def test_kept_member_outlives_its_batch(
        self, temp_root: Path, mock_config: EnergyPlusConfig, weather_file: Path
    ) -> None:
        batch = simulate_batch(self._jobs(weather_file), energyplus=mock_config, max_workers=3)
        kept = batch[1]
        with _Recorder() as caught:
            del batch
            gc.collect()
            assert _sim_dirs(temp_root) == [kept.run_dir]
            del kept
        assert _sim_dirs(temp_root) == []
        assert len(_resource_warnings(caught)) == 1

    def test_with_block_does_not_warn(self, temp_root: Path, mock_config: EnergyPlusConfig, weather_file: Path) -> None:
        with (
            _Recorder() as caught,
            simulate_batch(self._jobs(weather_file), energyplus=mock_config, max_workers=3),
        ):
            pass
        assert _resource_warnings(caught) == []
        assert _sim_dirs(temp_root) == []

    def test_partly_cleaned_batch_counts_the_rest(
        self, temp_root: Path, mock_config: EnergyPlusConfig, weather_file: Path
    ) -> None:
        batch = simulate_batch(self._jobs(weather_file), energyplus=mock_config, max_workers=3)
        batch[0].cleanup()
        with _Recorder() as caught:
            del batch
        [message] = _resource_warnings(caught)
        assert "BatchResult with 2 temporary run directories" in message

    def test_rebuilt_batch_groups_the_same_results(
        self, temp_root: Path, mock_config: EnergyPlusConfig, weather_file: Path
    ) -> None:
        batch = simulate_batch(self._jobs(weather_file, 2), energyplus=mock_config)
        rebuilt = BatchResult(results=batch.results, total_runtime_seconds=0.0)
        with _Recorder() as caught:
            del batch, rebuilt
        assert len(_resource_warnings(caught)) == 1


def _make_mock_process(returncode: int = 0) -> MagicMock:
    proc = MagicMock()
    proc.communicate = AsyncMock(return_value=(b"ok", b""))
    proc.returncode = returncode
    proc.kill = MagicMock()
    proc.wait = AsyncMock()
    return proc


class TestAsync:
    @patch("idfkit.simulation.async_runner.asyncio.create_subprocess_exec")
    def test_dropped_async_result_deletes_its_dir_and_warns(
        self, mock_exec: AsyncMock, temp_root: Path, mock_config: EnergyPlusConfig, weather_file: Path
    ) -> None:
        mock_exec.return_value = _make_mock_process()
        result = asyncio.run(async_simulate(runnable_model(), weather_file, energyplus=mock_config))
        run_dir = result.run_dir
        with _Recorder() as caught:
            del result
        assert not run_dir.exists()
        assert len(_resource_warnings(caught)) == 1

    @patch("idfkit.simulation.async_runner.asyncio.create_subprocess_exec")
    def test_async_cleanup_does_not_warn(
        self, mock_exec: AsyncMock, temp_root: Path, mock_config: EnergyPlusConfig, weather_file: Path
    ) -> None:
        mock_exec.side_effect = lambda *a, **k: _make_mock_process()

        async def run() -> None:
            async with await async_simulate(runnable_model(), weather_file, energyplus=mock_config):
                pass
            jobs = [SimulationJob(model=runnable_model(), weather=weather_file) for _ in range(2)]
            async with await async_simulate_batch(jobs, energyplus=mock_config):
                pass

        with _Recorder() as caught:
            asyncio.run(run())
        assert _resource_warnings(caught) == []
        assert _sim_dirs(temp_root) == []

    @patch("idfkit.simulation.async_runner.asyncio.create_subprocess_exec")
    def test_dropped_async_batch_warns_once(
        self, mock_exec: AsyncMock, temp_root: Path, mock_config: EnergyPlusConfig, weather_file: Path
    ) -> None:
        mock_exec.side_effect = lambda *a, **k: _make_mock_process()
        jobs = [SimulationJob(model=runnable_model(), weather=weather_file) for _ in range(3)]
        batch = asyncio.run(async_simulate_batch(jobs, energyplus=mock_config))
        with _Recorder() as caught:
            del batch
        assert _sim_dirs(temp_root) == []
        assert len(_resource_warnings(caught)) == 1


def test_interpreter_exit_deletes_and_warns(tmp_path: Path) -> None:
    """``weakref.finalize`` also reaps a directory whose result is still alive when the interpreter exits."""
    script = (
        "import tempfile\n"
        "from pathlib import Path\n"
        "from idfkit.simulation._run_dir import register_temp_run_dir\n"
        "from idfkit.simulation.result import SimulationResult\n"
        "d = Path(tempfile.mkdtemp(prefix='idfkit_sim_'))\n"
        "register_temp_run_dir(d)\n"
        "RESULT = SimulationResult(run_dir=d, success=True, exit_code=0, stdout='', stderr='',\n"
        "                          runtime_seconds=0.0, owns_run_dir=True)\n"
        "print(d)\n"
    )
    env = {**os.environ, "TMPDIR": str(tmp_path), "TEMP": str(tmp_path), "TMP": str(tmp_path)}
    proc = subprocess.run(  # noqa: S603
        [sys.executable, "-W", "always::ResourceWarning", "-c", script],
        capture_output=True,
        text=True,
        env=env,
        check=True,
    )
    run_dir = Path(proc.stdout.strip())
    assert run_dir.parent == tmp_path
    assert not run_dir.exists()
    assert "ResourceWarning" in proc.stderr


def _pickle_roundtrip(result: SimulationResult) -> SimulationResult:
    return pickle.loads(pickle.dumps(result))  # noqa: S301


@pytest.mark.parametrize("duplicate", [copy.deepcopy, _pickle_roundtrip], ids=["deepcopy", "pickle"])
def test_duplicated_result_still_knows_what_it_has_not_parsed(
    tmp_path: Path, duplicate: Callable[[SimulationResult], SimulationResult]
) -> None:
    """The "not parsed yet" sentinel survives deepcopy and pickle, so close() and the accessors still work."""
    (tmp_path / "eplusout.err").write_text("Program Version,EnergyPlus\n   ** Warning ** something\n")
    result = SimulationResult(run_dir=tmp_path, success=True, exit_code=0, stdout="", stderr="", runtime_seconds=0.0)
    twin: SimulationResult = duplicate(result)
    twin.close()
    assert twin.errors.warning_count == 1
