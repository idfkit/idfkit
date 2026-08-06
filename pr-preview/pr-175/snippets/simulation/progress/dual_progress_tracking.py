from __future__ import annotations

from idfkit import IDFDocument
from idfkit.simulation import SimulationJob

jobs: list[SimulationJob] = ...  # type: ignore[assignment]
variant: IDFDocument = ...  # type: ignore[assignment]
variants: list[IDFDocument] = ...  # type: ignore[assignment]
# --8<-- [start:example]
from idfkit.simulation import simulate_batch, SimulationJob, SimulationProgress

jobs = [SimulationJob(model=variant, weather="weather.epw", label=f"case-{i}") for i, variant in enumerate(variants)]


def on_sim_progress(event: SimulationProgress) -> None:
    """Fires during each simulation (warmup, simulating, etc.)."""
    if event.percent is not None:
        print(f"  Job {event.job_index} ({event.job_label}): {event.percent:.0f}%")


def on_job_complete(completed, total, label, success):
    """Fires when each job finishes."""
    status = "OK" if success else "FAIL"
    print(f"[{completed}/{total}] {label}: {status}")


batch = simulate_batch(
    jobs,
    on_progress=on_sim_progress,
    progress=on_job_complete,
    max_workers=4,
)
# --8<-- [end:example]
