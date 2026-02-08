"""Built-in progress bar factories for simulation callbacks.

Provides :func:`tqdm_progress`, a context manager that yields a ready-to-use
``on_progress`` callback powered by `tqdm <https://tqdm.github.io/>`_.
Install the optional dependency with::

    pip install idfkit[progress]

The :func:`resolve_on_progress` helper is used internally by the runners
to accept ``on_progress="tqdm"`` as a convenience shorthand.
"""

from __future__ import annotations

from collections.abc import Callable, Iterator
from contextlib import contextmanager
from typing import Any

from .progress import SimulationProgress


@contextmanager
def tqdm_progress(
    *,
    desc: str = "Simulating",
    bar_format: str = "{l_bar}{bar}| {n:.0f}/{total_fmt}% [{elapsed}<{remaining}]",
    leave: bool = True,
    position: int | None = None,
    file: Any = None,
    **tqdm_kwargs: Any,
) -> Iterator[Callable[[SimulationProgress], None]]:
    """Context manager that yields a tqdm-based ``on_progress`` callback.

    The progress bar is automatically closed when the context exits,
    even if an exception is raised.

    Args:
        desc: Progress bar description (left label).
        bar_format: tqdm bar format string.  The default shows percentage,
            elapsed and estimated remaining time.
        leave: Whether the bar remains visible after completion.
        position: Line position for the bar (useful for nested bars).
        file: Output stream (default: ``sys.stderr``).
        **tqdm_kwargs: Extra keyword arguments forwarded to :class:`tqdm.tqdm`.

    Yields:
        A callback suitable for the ``on_progress`` parameter.

    Raises:
        ImportError: If tqdm is not installed.

    Example::

        from idfkit.simulation import simulate
        from idfkit.simulation.progress_bars import tqdm_progress

        with tqdm_progress(desc="Annual run") as cb:
            result = simulate(model, "weather.epw", annual=True, on_progress=cb)
    """
    tqdm_cls = _import_tqdm()
    bar = tqdm_cls(
        total=100,
        desc=desc,
        unit="%",
        bar_format=bar_format,
        leave=leave,
        position=position,
        file=file,
        **tqdm_kwargs,
    )

    def _callback(event: SimulationProgress) -> None:
        if event.percent is not None:
            bar.n = event.percent
        bar.set_postfix_str(event.phase, refresh=False)
        bar.refresh()

    error = True
    try:
        yield _callback
        error = False
    finally:
        if not error:
            bar.n = 100
            bar.refresh()
        bar.close()


def resolve_on_progress(
    on_progress: Callable[[SimulationProgress], Any] | str | None,
) -> tuple[Callable[[SimulationProgress], Any] | None, Callable[[], None] | None]:
    """Resolve an ``on_progress`` value into a concrete callback.

    Used internally by runners.  Users should not call this directly.

    Accepts:
    - ``None`` -- no progress tracking.
    - A callable -- used directly.
    - ``"tqdm"`` -- creates a tqdm progress bar (requires ``idfkit[progress]``).

    Returns:
        A ``(callback, cleanup)`` pair.  *cleanup* is ``None`` unless a
        tqdm bar was created, in which case it must be called after the
        simulation to close the bar.

    Raises:
        ImportError: If ``"tqdm"`` is requested but tqdm is not installed.
        ValueError: If the string value is not ``"tqdm"``.
    """
    if on_progress is None:
        return None, None

    if isinstance(on_progress, str):
        if on_progress != "tqdm":
            msg = f"on_progress must be 'tqdm', a callable, or None -- got {on_progress!r}"
            raise ValueError(msg)
        # Manually enter the context manager so runners can clean up
        # in their own try/finally without requiring `with` syntax.
        cm = tqdm_progress()
        cb = cm.__enter__()

        def _cleanup() -> None:
            cm.__exit__(None, None, None)

        return cb, _cleanup

    if callable(on_progress):
        return on_progress, None

    msg = f"on_progress must be 'tqdm', a callable, or None -- got {type(on_progress).__name__}"
    raise TypeError(msg)


def _import_tqdm() -> type:
    """Import tqdm, raising a helpful error if unavailable."""
    try:
        from tqdm.auto import tqdm  # type: ignore[import-not-found]
    except ImportError:
        msg = "tqdm is required for built-in progress bars. Install it with: pip install idfkit[progress]"
        raise ImportError(msg) from None
    return tqdm  # type: ignore[no-any-return]
