from __future__ import annotations

from idfkit.simulation import SimulationJob

jobs: list[SimulationJob] = ...  # type: ignore[assignment]
# --8<-- [start:example]
from tqdm import tqdm
from idfkit.simulation import simulate_batch, SimulationProgress

jobs = [...]

# Job-level progress bar
overall = tqdm(total=len(jobs), desc="Batch", position=0)

# Sim-level progress bar (resets per job)
current = tqdm(total=100, desc="Current", position=1, leave=False)


def on_progress(event: SimulationProgress) -> None:
    if event.percent is not None:
        current.n = event.percent
        current.refresh()
    current.set_postfix_str(event.job_label or "")


def on_job_complete(completed, total, label, success):
    overall.update(1)
    current.n = 0
    current.refresh()


batch = simulate_batch(
    jobs,
    on_progress=on_progress,
    progress=on_job_complete,
    max_workers=4,
)

overall.close()
current.close()
# --8<-- [end:example]
