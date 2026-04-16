"""Progress events emitted during a migration.

Mirrors the shape of [SimulationProgress][idfkit.simulation.progress.SimulationProgress]
so callers can use the same ``on_progress`` callback style (including ``"tqdm"``).
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

MigrationPhase = Literal[
    "planning",
    "preparing",
    "transitioning",
    "reparsing",
    "diffing",
    "complete",
]


@dataclass(frozen=True, slots=True)
class MigrationProgress:
    """Progress event emitted during a migration run.

    Attributes:
        phase: Current migration phase.
        message: Short human-readable description of the current step.
        step_index: 0-based index of the current transition step
            (only set during the ``"transitioning"`` phase).
        total_steps: Total number of transition steps in the chain
            (only set once the chain has been planned).
        from_version: Source version of the current step, if known.
        to_version: Target version of the current step, if known.
        percent: Estimated completion percentage (``0.0`` to ``100.0``) or
            ``None`` when progress is indeterminate.
    """

    phase: MigrationPhase
    message: str
    step_index: int | None = None
    total_steps: int | None = None
    from_version: tuple[int, int, int] | None = None
    to_version: tuple[int, int, int] | None = None
    percent: float | None = None
