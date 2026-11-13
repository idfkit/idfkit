"""A lock that a forked child gets back unheld.

A child forked while some thread holds a ``threading.Lock`` inherits the lock still held, by a
thread the child does not have, so the child's first ``acquire`` waits forever. Every
process-wide lock in idfkit is a :class:`ForkSafeLock`, and one ``os.register_at_fork`` hook
hands each of them a fresh lock in the child, the way the standard library's ``logging``
re-initialises its handler locks.

Code takes the lock as ``with owner._lock.lock:``. The attribute is read when the ``with``
starts, so a ``with`` that is still open in the forking thread releases the lock it acquired,
not the replacement.
"""

from __future__ import annotations

import os
import threading
import weakref


class ForkSafeLock:
    """A ``threading.Lock`` (or ``RLock``) replaced by a fresh, unheld one in a forked child."""

    __slots__ = ("__weakref__", "lock", "reentrant")

    def __init__(self, *, reentrant: bool = False) -> None:
        self.reentrant = reentrant
        self.lock: threading.Lock | threading.RLock = threading.RLock() if reentrant else threading.Lock()
        _live_locks.add(self)

    def __reduce__(self) -> tuple[type[ForkSafeLock], tuple[()], dict[str, bool]]:
        """Pickle and copy as a fresh, unheld lock: a lock cannot be pickled, and a copy needs its own."""
        return (ForkSafeLock, (), {"reentrant": self.reentrant})

    def __setstate__(self, state: dict[str, bool]) -> None:
        """Restore the lock kind of a pickled or copied lock."""
        self.reentrant = state["reentrant"]
        self.reset()

    def reset(self) -> None:
        """Replace the lock. Only for a forked child, where it may be held by a thread the child lacks."""
        self.lock = threading.RLock() if self.reentrant else threading.Lock()


# Every fork-safe lock alive in this process.
_live_locks: weakref.WeakSet[ForkSafeLock] = weakref.WeakSet()


def _reset_locks_after_fork() -> None:
    """Replace, in a forked child, every lock the parent may have held at the moment of the fork."""
    for lock in _live_locks:
        lock.reset()


if hasattr(os, "register_at_fork"):  # POSIX only; Windows has no fork
    os.register_at_fork(after_in_child=_reset_locks_after_fork)
