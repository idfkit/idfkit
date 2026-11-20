"""Cancellation of the subprocesses a batch of simulations has started.

[simulate_batch][idfkit.simulation.batch.simulate_batch] runs each job in a
worker thread, and a worker thread cannot be interrupted. When the caller is
interrupted (Ctrl-C, or any exception while the batch waits), the batch kills
the EnergyPlus children its workers have started instead: each worker binds a
[ProcessGroup][idfkit.simulation._cancel.ProcessGroup] for the duration of its
job, and every subprocess started through
[run_process][idfkit.simulation._cancel.run_process] or
[tracked][idfkit.simulation._cancel.tracked] joins the group bound in its
thread. A process started after the group was cancelled is killed at once.
"""

from __future__ import annotations

import contextlib
import subprocess
import threading
from collections.abc import Iterator, Sequence
from contextvars import ContextVar
from pathlib import Path

_active_group: ContextVar[ProcessGroup | None] = ContextVar("idfkit_simulation_process_group", default=None)


class ProcessGroup:
    """The live subprocesses of one batch, killed together by [cancel][idfkit.simulation._cancel.ProcessGroup.cancel]."""

    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._procs: set[subprocess.Popen[str]] = set()
        self._cancelled = False

    @property
    def cancelled(self) -> bool:
        """Whether [cancel][idfkit.simulation._cancel.ProcessGroup.cancel] has been called."""
        return self._cancelled

    def cancel(self) -> None:
        """Kill every live process in the group, and every process that joins it from now on."""
        with self._lock:
            self._cancelled = True
            procs = list(self._procs)
        for proc in procs:
            _kill(proc)

    @contextlib.contextmanager
    def bind(self) -> Iterator[None]:
        """Make this the group that subprocesses started in the current thread join."""
        token = _active_group.set(self)
        try:
            yield
        finally:
            _active_group.reset(token)

    def add(self, proc: subprocess.Popen[str]) -> None:
        """Add *proc* to the group, or kill it if the group is already cancelled."""
        with self._lock:
            if not self._cancelled:
                self._procs.add(proc)
                return
        _kill(proc)

    def discard(self, proc: subprocess.Popen[str]) -> None:
        """Remove *proc* from the group (it has exited)."""
        with self._lock:
            self._procs.discard(proc)


def _kill(proc: subprocess.Popen[str]) -> None:
    with contextlib.suppress(OSError):  # already reaped
        proc.kill()


@contextlib.contextmanager
def tracked(proc: subprocess.Popen[str]) -> Iterator[None]:
    """Register *proc* with the group bound in this thread, if any, while the block runs."""
    group = _active_group.get()
    if group is None:
        yield
        return
    group.add(proc)
    try:
        yield
    finally:
        group.discard(proc)


def run_process(cmd: Sequence[str], *, cwd: Path, timeout: float) -> subprocess.CompletedProcess[str]:
    """Run *cmd* as [subprocess.run][] does with captured text output, as a member of the bound group.

    Raises:
        subprocess.TimeoutExpired: If *cmd* runs longer than *timeout* seconds (it is killed).
        OSError: If *cmd* cannot be started.
    """
    with (
        subprocess.Popen(  # noqa: S603
            list(cmd),
            stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            cwd=str(cwd),
        ) as proc,
        tracked(proc),
    ):
        try:
            stdout, stderr = proc.communicate(timeout=timeout)
        except subprocess.TimeoutExpired:
            proc.kill()
            stdout, stderr = proc.communicate()
            raise subprocess.TimeoutExpired(proc.args, timeout, output=stdout, stderr=stderr) from None
        except BaseException:
            proc.kill()  # Popen.__exit__ reaps it
            raise
        return subprocess.CompletedProcess(list(cmd), proc.returncode, stdout, stderr)
