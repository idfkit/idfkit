from __future__ import annotations

from idfkit import IDFDocument
from typing import Any

model: IDFDocument = ...  # type: ignore[assignment]
websocket: Any = ...  # type: ignore[assignment]
# --8<-- [start:example]
from idfkit.simulation import async_simulate, SimulationProgress


async def on_progress(event: SimulationProgress) -> None:
    """Async callback -- awaited by the runner."""
    await websocket.send_json({
        "phase": event.phase,
        "percent": event.percent,
        "message": event.message,
    })


async def main():
    result = await async_simulate(model, "weather.epw", on_progress=on_progress)


# --8<-- [end:example]
