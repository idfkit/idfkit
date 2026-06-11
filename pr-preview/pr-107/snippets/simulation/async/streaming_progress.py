from __future__ import annotations

from idfkit import IDFDocument
from idfkit.simulation import SimulationJob

jobs: list[SimulationJob] = ...  # type: ignore[assignment]
variant: IDFDocument = ...  # type: ignore[assignment]
variants: list[IDFDocument] = ...  # type: ignore[assignment]
# --8<-- [start:example]
import asyncio
from idfkit.simulation import async_simulate_batch_stream, SimulationJob


async def main():
    jobs = [
        SimulationJob(model=variant, weather="weather.epw", label=f"case-{i}") for i, variant in enumerate(variants)
    ]

    async for event in async_simulate_batch_stream(jobs, max_concurrent=4):
        status = "OK" if event.result.success else "FAIL"
        print(f"[{event.completed}/{event.total}] {event.label}: {status}")


asyncio.run(main())
# --8<-- [end:example]
