from __future__ import annotations

from idfkit import IDFDocument
from idfkit.simulation import SimulationJob

jobs: list[SimulationJob] = ...  # type: ignore[assignment]
variant: IDFDocument = ...  # type: ignore[assignment]
variants: list[IDFDocument] = ...  # type: ignore[assignment]
# --8<-- [start:example]
import asyncio
from idfkit.simulation import (
    async_simulate_batch_stream,
    SimulationJob,
    SimulationProgress,
)


async def main():
    jobs = [
        SimulationJob(model=variant, weather="weather.epw", label=f"case-{i}") for i, variant in enumerate(variants)
    ]

    def on_sim_progress(event: SimulationProgress) -> None:
        if event.percent is not None:
            print(f"  [{event.job_label}] {event.percent:.0f}%")

    async for event in async_simulate_batch_stream(
        jobs,
        max_concurrent=4,
        on_progress=on_sim_progress,
    ):
        status = "OK" if event.result.success else "FAIL"
        print(f"[{event.completed}/{event.total}] {event.label}: {status}")


asyncio.run(main())
# --8<-- [end:example]
