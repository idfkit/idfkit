from __future__ import annotations

from idfkit.simulation import SimulationJob, simulate_batch

jobs: list[SimulationJob] = ...  # type: ignore[assignment]
# --8<-- [start:example]
from rich.progress import Progress

with Progress() as progress:
    task = progress.add_task("Simulating...", total=len(jobs))

    def callback(completed, total, label, success):
        progress.update(task, completed=completed)

    batch = simulate_batch(jobs, progress=callback)
# --8<-- [end:example]
