"""Type-check fixture for ``SimulationJob`` and ``simulate_batch`` (never called; checked by ``make check``).

``SimulationJob.model`` is a loaded document, so a path fails type-checking instead of failing the job at
run time. ``extra_args`` takes any sequence of strings, as ``simulate(extra_args=...)`` does. The
``progress=`` callback must take the four keywords ``simulate_batch`` calls it with, so a callback that
does not is caught here rather than after every job has run.

Each seeded error below carries a ``pyright: ignore`` naming the rule it must trigger, and this file
turns on ``reportUnnecessaryTypeIgnoreComment``, so the fixture proves the errors are caught rather than
merely tolerated.
"""

# pyright: strict, reportUnnecessaryTypeIgnoreComment=true

from __future__ import annotations

from typing_extensions import assert_type

from idfkit import new_document
from idfkit.simulation import SimulationJob, SimulationResult, simulate_batch
from idfkit.versioned import AnyIDFDocument


def _full(*, completed: int, total: int, label: str, success: bool) -> None: ...


def _positional_or_keyword(completed: int, total: int, label: str, success: bool) -> None: ...


def _kwargs(**kwargs: object) -> None: ...


def _too_few(completed: int, total: int) -> None: ...


def correct_calls() -> None:
    job = SimulationJob(model=new_document(), weather="w.epw", extra_args=["--convert"])
    assert_type(job.model, AnyIDFDocument)
    SimulationJob(model=new_document(), extra_args=("--convert",))
    simulate_batch([job], progress=_full)
    simulate_batch([job], progress=_positional_or_keyword)
    simulate_batch([job], progress=_kwargs)
    stopped = simulate_batch([job], fail_fast=True)
    assert_type(stopped.cancelled, tuple[SimulationResult, ...])


def seeded_errors() -> None:
    SimulationJob(model="building.idf", weather="w.epw")  # pyright: ignore[reportArgumentType]
    job = SimulationJob(model=new_document())
    simulate_batch([job], progress=_too_few)  # pyright: ignore[reportArgumentType]
