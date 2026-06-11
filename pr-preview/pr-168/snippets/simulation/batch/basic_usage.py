from __future__ import annotations

from idfkit import IDFDocument
from idfkit.simulation import BatchResult, SimulationJob, SimulationResult

batch: BatchResult = ...  # type: ignore[assignment]
jobs: list[SimulationJob] = ...  # type: ignore[assignment]
model1: IDFDocument = ...  # type: ignore[assignment]
model2: IDFDocument = ...  # type: ignore[assignment]
result: SimulationResult = ...  # type: ignore[assignment]
# --8<-- [start:example]
from idfkit.simulation import simulate_batch, SimulationJob

# Create jobs
jobs = [
    SimulationJob(model=model1, weather="weather.epw", label="baseline"),
    SimulationJob(model=model2, weather="weather.epw", label="improved"),
]

# Run in parallel
batch = simulate_batch(jobs, max_workers=4)

print(f"Completed: {len(batch.succeeded)}/{len(batch)}")
for i, result in enumerate(batch):
    print(f"  Job {i}: {'Success' if result.success else 'Failed'}")
# --8<-- [end:example]
