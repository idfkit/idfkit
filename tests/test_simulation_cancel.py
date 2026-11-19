"""Interrupting a run kills the EnergyPlus processes it started.

A stand-in ``energyplus`` shell script records its PID in its run directory and
then sleeps, unless the run directory's name contains ``fast``.
"""

from __future__ import annotations

import asyncio
import contextlib
import os
import subprocess
import sys
import threading
import time
from pathlib import Path
from typing import Any

import pytest
from conftest import runnable_model

from idfkit import LATEST_VERSION
from idfkit.exceptions import MigrationError
from idfkit.migration.subprocess_backend import SubprocessMigrator
from idfkit.simulation._cancel import ProcessGroup, run_process
from idfkit.simulation.async_batch import async_simulate_batch_stream
from idfkit.simulation.async_runner import async_simulate
from idfkit.simulation.batch import SimulationJob, simulate_batch
from idfkit.simulation.config import EnergyPlusConfig

pytestmark = pytest.mark.skipif(sys.platform == "win32", reason="the stand-in EnergyPlus is a POSIX shell script")

_SCRIPT = """#!/bin/sh
echo $$ > "$PWD/pid"
case "$PWD" in *fast*) exit 0 ;; esac
exec sleep 60
"""


@pytest.fixture
def sleepy_config(tmp_path: Path) -> EnergyPlusConfig:
    exe = tmp_path / "bin" / "energyplus"
    exe.parent.mkdir()
    exe.write_text(_SCRIPT)
    exe.chmod(0o755)
    idd = tmp_path / "bin" / "Energy+.idd"
    idd.write_text("!IDD_Version 24.1.0\n")
    return EnergyPlusConfig(executable=exe, version=LATEST_VERSION, install_dir=exe.parent, idd_path=idd)


@pytest.fixture
def weather_file(tmp_path: Path) -> Path:
    epw = tmp_path / "weather.epw"
    epw.write_text("LOCATION,Chicago\n")
    return epw


def _alive(pid: int) -> bool:
    try:
        os.kill(pid, 0)
    except ProcessLookupError:
        return False
    # A zombie still answers signal 0; reap it if it is our child.
    with contextlib.suppress(ChildProcessError):
        done, _ = os.waitpid(pid, os.WNOHANG)
        return done == 0
    return True


def _started_pids(run_dirs: list[Path]) -> list[int]:
    """The PIDs the stand-in recorded (a process killed while writing leaves an empty file)."""
    texts = [(d / "pid").read_text().strip() for d in run_dirs if (d / "pid").is_file()]
    return [int(text) for text in texts if text]


async def _wait_for_pid(run_dir: Path) -> int:
    for _ in range(200):
        if (run_dir / "pid").is_file() and (run_dir / "pid").read_text().strip():
            return int((run_dir / "pid").read_text())
        await asyncio.sleep(0.02)
    msg = f"the stand-in EnergyPlus never started in {run_dir}"
    raise AssertionError(msg)


def _wait_for_pid_sync(pid_file: Path) -> int:
    for _ in range(500):
        if pid_file.is_file() and pid_file.read_text().strip():
            return int(pid_file.read_text())
        time.sleep(0.02)
    msg = f"the stand-in process never wrote {pid_file}"
    raise AssertionError(msg)


class _Stop(Exception):
    pass


class TestProcessGroup:
    def test_cancel_kills_a_running_process(self, tmp_path: Path) -> None:
        group = ProcessGroup()
        proc = subprocess.Popen([sys.executable, "-c", "import time; time.sleep(60)"], text=True)  # noqa: S603
        group.add(proc)
        group.cancel()
        assert proc.wait(timeout=10) != 0
        assert group.cancelled

    def test_process_started_after_cancel_is_killed(self, tmp_path: Path) -> None:
        group = ProcessGroup()
        group.cancel()
        start = time.monotonic()
        with group.bind():
            done = run_process([sys.executable, "-c", "import time; time.sleep(60)"], cwd=tmp_path, timeout=60)
        assert done.returncode != 0
        assert time.monotonic() - start < 30

    def test_run_process_without_a_group(self, tmp_path: Path) -> None:
        done = run_process([sys.executable, "-c", "print('hi')"], cwd=tmp_path, timeout=60)
        assert (done.returncode, done.stdout.strip()) == (0, "hi")

    def test_run_process_timeout(self, tmp_path: Path) -> None:
        with pytest.raises(subprocess.TimeoutExpired):
            run_process([sys.executable, "-c", "import time; time.sleep(60)"], cwd=tmp_path, timeout=0.2)


class TestSimulateBatchInterrupted:
    def test_exception_in_caller_cancels_queue_and_kills_running(
        self, tmp_path: Path, sleepy_config: EnergyPlusConfig, weather_file: Path
    ) -> None:
        run_dirs = [tmp_path / "fast0", *(tmp_path / f"slow{i}" for i in range(1, 8))]
        jobs = [SimulationJob(model=runnable_model(), weather=weather_file, output_dir=d) for d in run_dirs]

        def stop(*, completed: int, total: int, label: str, success: bool) -> None:
            raise _Stop

        start = time.monotonic()
        with pytest.raises(_Stop):
            simulate_batch(jobs, energyplus=sleepy_config, max_workers=2, progress=stop)
        assert time.monotonic() - start < 30

        pids = _started_pids(run_dirs)
        assert 1 <= len(pids) <= 3  # the fast job, and at most the two that had a worker; the rest never started
        assert not any(_alive(pid) for pid in pids)

    def test_with_on_progress_kills_running(
        self, tmp_path: Path, sleepy_config: EnergyPlusConfig, weather_file: Path
    ) -> None:
        run_dirs = [tmp_path / "fast0", tmp_path / "slow1", tmp_path / "slow2"]
        jobs = [SimulationJob(model=runnable_model(), weather=weather_file, output_dir=d) for d in run_dirs]

        def stop(*, completed: int, total: int, label: str, success: bool) -> None:
            raise _Stop

        with pytest.raises(_Stop):
            simulate_batch(jobs, energyplus=sleepy_config, max_workers=2, progress=stop, on_progress=lambda _p: None)
        assert not any(_alive(pid) for pid in _started_pids(run_dirs))


class TestAsyncCancellation:
    @pytest.mark.asyncio
    @pytest.mark.parametrize("with_progress", [False, True])
    async def test_cancelled_async_simulate_kills_energyplus(
        self, tmp_path: Path, sleepy_config: EnergyPlusConfig, weather_file: Path, with_progress: bool
    ) -> None:
        run_dir = tmp_path / "slow"
        task = asyncio.create_task(
            async_simulate(
                runnable_model(),
                weather_file,
                energyplus=sleepy_config,
                output_dir=run_dir,
                on_progress=(lambda _p: None) if with_progress else None,
            )
        )
        pid = await _wait_for_pid(run_dir)
        task.cancel()
        with pytest.raises(asyncio.CancelledError):
            await task
        assert not _alive(pid)

    @pytest.mark.asyncio
    async def test_closing_the_stream_kills_running_jobs(
        self, tmp_path: Path, sleepy_config: EnergyPlusConfig, weather_file: Path
    ) -> None:
        run_dirs = [tmp_path / "fast0", tmp_path / "slow1", tmp_path / "slow2"]
        jobs = [SimulationJob(model=runnable_model(), weather=weather_file, output_dir=d) for d in run_dirs]
        async with contextlib.aclosing(async_simulate_batch_stream(jobs, energyplus=sleepy_config)) as stream:
            async for _event in stream:
                break
        pids = _started_pids(run_dirs)
        assert len(pids) >= 1
        assert not any(_alive(pid) for pid in pids)


class TestMigrationStepKilled:
    def test_cancelling_the_group_kills_a_running_transition(self, tmp_path: Path) -> None:
        updater = tmp_path / "IDFVersionUpdater"
        updater.mkdir()
        binary = updater / "Transition-V24-1-0-to-V24-2-0"
        binary.write_text(_SCRIPT)
        binary.chmod(0o755)
        work = tmp_path / "work"
        migrator = SubprocessMigrator(version_updater_dir=updater, step_timeout=60)
        group = ProcessGroup()
        errors: list[BaseException] = []

        def step() -> None:
            with group.bind():
                try:
                    migrator.migrate_step("Version,24.1;\n", (24, 1, 0), (24, 2, 0), work_dir=work)
                except BaseException as exc:
                    errors.append(exc)

        thread = threading.Thread(target=step)
        start = time.monotonic()
        thread.start()
        pid = _wait_for_pid_sync(work / "pid")
        group.cancel()
        thread.join(timeout=30)
        assert not thread.is_alive()
        assert time.monotonic() - start < 30
        assert len(errors) == 1
        assert isinstance(errors[0], MigrationError)
        assert not _alive(pid)


class TestAsyncPreprocessCancelled:
    @pytest.mark.asyncio
    async def test_cancelling_async_simulate_kills_the_preprocessor(
        self,
        tmp_path: Path,
        sleepy_config: EnergyPlusConfig,
        weather_file: Path,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        pre_dir = tmp_path / "preprocess"
        pre_dir.mkdir()
        script = pre_dir / "slab"
        script.write_text(_SCRIPT)
        script.chmod(0o755)

        def slow_preprocess(model: Any, *_args: Any) -> tuple[Any, bool]:
            # Stands in for a long Slab/Basement/ExpandObjects run, which goes through run_process.
            run_process([str(script)], cwd=pre_dir, timeout=60)
            return model, False

        monkeypatch.setattr("idfkit.simulation.async_runner.maybe_preprocess", slow_preprocess)
        task = asyncio.create_task(
            async_simulate(runnable_model(), weather_file, energyplus=sleepy_config, output_dir=tmp_path / "slow")
        )
        pid = await _wait_for_pid(pre_dir)
        start = time.monotonic()
        task.cancel()
        with pytest.raises(asyncio.CancelledError):
            await task
        assert time.monotonic() - start < 30
        assert not _alive(pid)
        assert not (tmp_path / "slow" / "pid").exists()  # EnergyPlus itself never started
