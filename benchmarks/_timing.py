"""Stdlib timing helpers for the performance budget gate (R-21).

Used by ``tests/test_perf_budgets.py`` and by ad hoc benchmark scripts. Nothing here imports a
third-party package: the gate must run wherever the library runs.

- :func:`best_of` times a callable with :func:`time.perf_counter` and keeps the fastest run, the
  figure least disturbed by a busy machine.
- :func:`peak_memory` measures the peak memory a callable allocates, with :mod:`tracemalloc`.
- :func:`reference_model_path` and :func:`load_reference_model` give the vendored reference model,
  ``fixtures/HospitalLowEnergy.idf.gz``, the largest EnergyPlus example file.
"""

from __future__ import annotations

import gzip
import tempfile
import time
import tracemalloc
from collections.abc import Callable
from pathlib import Path
from typing import TypeVar

from idfkit import IDFDocument, load_idf

T = TypeVar("T")

FIXTURES_DIR = Path(__file__).resolve().parent / "fixtures"
"""Directory holding the vendored benchmark inputs."""

REFERENCE_MODEL_GZ = FIXTURES_DIR / "HospitalLowEnergy.idf.gz"
"""The reference model, gzip-compressed. See ``fixtures/README.md`` for its source."""


def best_of(fn: Callable[[], object], n: int = 5) -> float:
    """Return the fastest of ``n`` timed calls of ``fn``, in seconds.

    Args:
        fn: The callable to time. It is called with no arguments, ``n`` times.
        n: How many runs to take the minimum over. Must be at least 1.

    Returns:
        The shortest wall-clock duration of a single call, in seconds.
    """
    if n < 1:
        msg = f"n must be at least 1, got {n}"
        raise ValueError(msg)
    best = float("inf")
    for _ in range(n):
        start = time.perf_counter()
        fn()
        elapsed = time.perf_counter() - start
        best = min(best, elapsed)
    return best


def peak_memory(fn: Callable[[], T]) -> tuple[T, int]:
    """Call ``fn`` once and return its result with the peak memory it allocated, in bytes.

    The peak is measured by :mod:`tracemalloc` relative to the moment ``fn`` starts, so memory
    already held by the caller is not counted. Tracing slows the call down; never time a call
    and measure its memory in the same run.

    Args:
        fn: The callable to measure. It is called once, with no arguments.

    Returns:
        ``(result, peak_bytes)``: what ``fn`` returned, and the peak traced allocation above the
        starting point while it ran.
    """
    was_tracing = tracemalloc.is_tracing()
    if not was_tracing:
        tracemalloc.start()
    try:
        tracemalloc.reset_peak()
        baseline, _ = tracemalloc.get_traced_memory()
        result = fn()
        _, peak = tracemalloc.get_traced_memory()
    finally:
        if not was_tracing:
            tracemalloc.stop()
    return result, max(peak - baseline, 0)


def reference_model_path(directory: Path | None = None) -> Path:
    """Decompress the reference model to ``directory`` and return the path of the IDF file.

    :func:`idfkit.load_idf` reads from a path, not from text, so timing it needs the file on
    disk. Decompressing once, before timing, keeps the gzip cost out of the measurement.

    Args:
        directory: Where to write ``HospitalLowEnergy.idf``. A new temporary directory when
            ``None``; the caller then owns its cleanup.

    Returns:
        The path of the decompressed IDF file.
    """
    target_dir = Path(tempfile.mkdtemp(prefix="idfkit-bench-")) if directory is None else directory
    target = target_dir / "HospitalLowEnergy.idf"
    target.write_bytes(gzip.decompress(REFERENCE_MODEL_GZ.read_bytes()))
    return target


def load_reference_model(directory: Path | None = None) -> IDFDocument:
    """Load the vendored reference model into an :class:`~idfkit.IDFDocument`.

    Args:
        directory: Where to decompress the file first. When ``None``, a temporary directory
            that is removed once the model is loaded.

    Returns:
        The parsed reference model.
    """
    if directory is not None:
        return load_idf(str(reference_model_path(directory)))
    with tempfile.TemporaryDirectory(prefix="idfkit-bench-") as tmp:
        return load_idf(str(reference_model_path(Path(tmp))))
