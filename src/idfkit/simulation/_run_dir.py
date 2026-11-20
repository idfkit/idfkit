"""The garbage-collection safety net for the temporary run directories idfkit creates.

``simulate()`` and ``async_simulate()`` without an ``output_dir`` run EnergyPlus in a new
``idfkit_sim_*`` temporary directory. The returned result reads its files from that directory
lazily, so it cannot be deleted while the result is in use; ``cleanup()`` and ``with`` delete it
when the caller is done. A caller who never does left it behind, silently.

Each such directory gets one [RunDirLease][idfkit.simulation._run_dir.RunDirLease]. Every
[SimulationResult][idfkit.simulation.result.SimulationResult] that owns the directory holds the
same lease: the result ``simulate()`` returned, a ``dataclasses.replace()`` of it (looked up again
by path here), a ``copy.copy`` and a ``copy.deepcopy`` (the lease copies as itself), and the batch
that holds it. The lease is only garbage-collected once none of them is reachable any more, so no
object that could still read the directory exists, and then its finalizer deletes the directory
and emits a ``ResourceWarning``, like ``tempfile.TemporaryDirectory``. ``weakref.finalize`` also
runs it at interpreter exit for results still alive then.

What the net never touches:

* A caller's ``output_dir``, a remote ``fs=`` directory and a cache entry: no lease is made for them.
* A directory already deleted by ``cleanup()``: cleaning up releases the lease.
* A pickled result: another process may read the directory through its copy, and idfkit cannot
  tell when the last copy is gone, so pickling releases the lease and the directory is the
  caller's to delete again, as before. An unpickled result holds no lease.
* A forked child: it inherits the parent's leases, but the finalizer acts only in the process that
  created the lease, so a child exiting never deletes the parent's directories.

A result that is part of a [BatchResult][idfkit.simulation.batch.BatchResult] warns once per batch
rather than once per job: the batch holds its results, so a member's lease can only die once the
batch is unreachable too, and the first member to go reports for all of them.
"""

from __future__ import annotations

import os
import shutil
import warnings
import weakref
from collections.abc import Iterable
from pathlib import Path

from .._forksafe import ForkSafeLock

# Reentrant: garbage collection can run a lease's finalizer, which takes this lock, on whatever thread
# allocates, including one that already holds it inside lease_for() or register_temp_run_dir().
_lock = ForkSafeLock(reentrant=True)

# The live lease of every temporary run directory, by path, so that a copy of a result made
# through its constructor (``dataclasses.replace``) finds the lease of the original.
_leases: weakref.WeakValueDictionary[str, RunDirLease] = weakref.WeakValueDictionary()


class _Batch:
    """The leases of one batch, which report a leak once between them."""

    __slots__ = ("states", "warned")

    def __init__(self, states: list[_LeaseState]) -> None:
        self.states = states
        self.warned = False


class _LeaseState:
    """What the finalizer of one lease needs; kept apart from the lease so it can outlive it."""

    __slots__ = ("batch", "path", "pid", "released")

    def __init__(self, path: Path) -> None:
        self.path = path
        self.pid = os.getpid()
        self.released = False
        self.batch: _Batch | None = None


class RunDirLease:
    """Deletes one idfkit-created temporary run directory, with a warning, once nothing refers to it."""

    __slots__ = ("__weakref__", "_finalizer", "state")

    def __init__(self, path: Path) -> None:
        self.state = _LeaseState(path)
        self._finalizer = weakref.finalize(self, _reap, self.state)

    @property
    def path(self) -> Path:
        """The directory this lease deletes."""
        return self.state.path

    @property
    def active(self) -> bool:
        """Whether garbage collection would still delete the directory."""
        return not self.state.released

    def release(self) -> None:
        """Stop tracking the directory: it was deleted, or is no longer idfkit's to delete."""
        self.state.released = True
        self._finalizer.detach()
        key = os.fspath(self.state.path)
        with _lock.lock:
            if _leases.get(key) is self:
                del _leases[key]

    def __copy__(self) -> RunDirLease:
        return self

    def __deepcopy__(self, memo: dict[int, object]) -> RunDirLease:
        return self

    def __reduce__(self) -> tuple[object, tuple[()]]:
        """Release the lease and pickle as no lease; see the module docstring."""
        self.release()
        return (_no_lease, ())


def _no_lease() -> None:
    """What a pickled lease unpickles as."""
    return None


def register_temp_run_dir(path: Path) -> RunDirLease:
    """Make the lease of a temporary run directory idfkit just created at *path*."""
    lease = RunDirLease(path)
    with _lock.lock:
        _leases[os.fspath(path)] = lease
    return lease


def lease_for(path: Path) -> RunDirLease | None:
    """The live lease of the temporary run directory *path*, or ``None`` when idfkit tracks none there."""
    with _lock.lock:
        return _leases.get(os.fspath(path))


def group_batch(leases: Iterable[RunDirLease | None]) -> None:
    """Make the leases of one batch's results report a leak once, as a batch."""
    states = list({id(lease.state): lease.state for lease in leases if lease is not None and lease.active}.values())
    if not states:
        return
    batch = _Batch(states)
    for state in states:
        state.batch = batch


def _reap(state: _LeaseState) -> None:
    """Finalizer of a lease: delete its directory and warn, unless it was released or forked."""
    if state.released or state.pid != os.getpid():
        return
    batch = state.batch
    with _lock.lock:
        report = batch is None or not batch.warned
        leaked = 1 if batch is None else sum(1 for s in batch.states if not s.released)
        if batch is not None:
            batch.warned = True
        state.released = True
    shutil.rmtree(state.path, ignore_errors=True)
    if not report:
        return
    if batch is None:
        message = (
            f"idfkit deleted the temporary run directory {state.path} of a SimulationResult that was "
            "garbage-collected without cleanup(). Use `with simulate(...) as result:` or call "
            "result.cleanup() when done; pass output_dir to keep the files."
        )
    else:
        message = (
            f"A BatchResult with {leaked} temporary run director{'y' if leaked == 1 else 'ies'} "
            "was garbage-collected without cleanup(); idfkit deletes each once no result refers to it. "
            "Use `with simulate_batch(...) as batch:` or call batch.cleanup() when done; give each job "
            "an output_dir to keep the files."
        )
    warnings.warn(message, ResourceWarning, stacklevel=1)
