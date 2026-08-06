from __future__ import annotations

from idfkit.simulation import SimulationJob

jobs: list[SimulationJob] = ...  # type: ignore[assignment]
# --8<-- [start:example]
from rich.progress import Progress
from idfkit.simulation import simulate_batch, SimulationProgress
import threading

lock = threading.Lock()

with Progress() as progress:
    tasks = {}  # job_index -> task_id

    def on_progress(event: SimulationProgress) -> None:
        with lock:
            if event.job_index not in tasks:
                tasks[event.job_index] = progress.add_task(
                    event.job_label or f"Job {event.job_index}",
                    total=100,
                )
            task_id = tasks[event.job_index]
        if event.percent is not None:
            progress.update(task_id, completed=event.percent)
        progress.update(task_id, description=f"{event.job_label}: {event.phase}")

    batch = simulate_batch(jobs, on_progress=on_progress, max_workers=4)
# --8<-- [end:example]
