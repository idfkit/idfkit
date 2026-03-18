from __future__ import annotations

from idfkit import IDFDocument
from idfkit.simulation import BatchResult, SimulationJob, SimulationResult

batch: BatchResult = ...  # type: ignore[assignment]
jobs: list[SimulationJob] = ...  # type: ignore[assignment]
model1: IDFDocument = ...  # type: ignore[assignment]
model2: IDFDocument = ...  # type: ignore[assignment]
result: SimulationResult = ...  # type: ignore[assignment]
# --8<-- [start:example]
import asyncio
from idfkit.simulation import async_simulate_batch, SimulationJob


async def main():
    jobs = [
        SimulationJob(model=model1, weather="weather.epw", label="baseline"),
        SimulationJob(model=model2, weather="weather.epw", label="improved"),
    ]

    batch = await async_simulate_batch(jobs, max_concurrent=4)

    print(f"Completed: {len(batch.succeeded)}/{len(batch)}")
    for i, result in enumerate(batch):
        print(f"  Job {i}: {'Success' if result.success else 'Failed'}")


asyncio.run(main())
# --8<-- [end:example]
