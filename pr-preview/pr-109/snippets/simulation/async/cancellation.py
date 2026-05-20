from __future__ import annotations

from asyncio import asyncio
from idfkit import IDFDocument
from idfkit.simulation import async_simulate

model: IDFDocument = ...  # type: ignore[assignment]


# --8<-- [start:example]
async def run_with_timeout():
    task = asyncio.create_task(async_simulate(model, "weather.epw"))

    try:
        result = await asyncio.wait_for(task, timeout=120)
    except asyncio.TimeoutError:
        print("Simulation cancelled after 120s")


# --8<-- [end:example]
