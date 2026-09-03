from __future__ import annotations

from idfkit import IDFDocument
from idfkit.simulation import BatchResult, SimulationJob, SimulationResult, TimeSeriesResult

batch: BatchResult = ...  # type: ignore[assignment]
job: SimulationJob = ...  # type: ignore[assignment]
jobs: list[SimulationJob] = ...  # type: ignore[assignment]
model: IDFDocument = ...  # type: ignore[assignment]
result: SimulationResult = ...  # type: ignore[assignment]
ts: TimeSeriesResult = ...  # type: ignore[assignment]
variant: IDFDocument = ...  # type: ignore[assignment]
# --8<-- [start:example]
import asyncio
from idfkit.simulation import async_simulate_batch, SimulationJob


async def main():
    # Create variants
    jobs = []
    for insulation in [0.05, 0.10, 0.15, 0.20]:
        variant = model.copy()
        variant["Material"]["Insulation"].thickness = insulation
        jobs.append(
            SimulationJob(
                model=variant,
                weather="weather.epw",
                label=f"insulation-{insulation}m",
                design_day=True,
            )
        )

    # Run all variants
    batch = await async_simulate_batch(jobs, max_concurrent=4)

    # Analyze results
    for job, result in zip(jobs, batch):
        if result.success:
            ts = result.sql.get_timeseries(
                "Zone Mean Air Temperature",
                "ZONE 1",
            )
            print(f"{job.label}: Max temp {max(ts.values):.1f}°C")


asyncio.run(main())
# --8<-- [end:example]
