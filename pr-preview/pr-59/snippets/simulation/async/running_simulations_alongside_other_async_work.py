from __future__ import annotations

from idfkit import IDFDocument
from idfkit.simulation import SimulationResult
from typing import Any

model: IDFDocument = ...  # type: ignore[assignment]
result: SimulationResult = ...  # type: ignore[assignment]
weather_meta: dict[str, Any] = ...  # type: ignore[assignment]
# --8<-- [start:example]
import asyncio
from idfkit.simulation import async_simulate


async def fetch_weather_data(station_id: str) -> dict:
    """Fetch weather metadata from a remote API."""
    ...


async def main():
    # Run a simulation and an API call concurrently
    sim_task = async_simulate(model, "weather.epw", design_day=True)
    api_task = fetch_weather_data("725300")

    result, weather_meta = await asyncio.gather(sim_task, api_task)

    print(f"Simulation: {result.runtime_seconds:.1f}s")
    print(f"Weather station: {weather_meta}")


asyncio.run(main())
# --8<-- [end:example]
