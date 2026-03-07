from __future__ import annotations

from idfkit import IDFDocument
from idfkit.simulation import SimulationResult
from typing import Any

model: IDFDocument = ...  # type: ignore[assignment]
result: SimulationResult = ...  # type: ignore[assignment]
weather: str = ...  # type: ignore[assignment]
websocket: Any = ...  # type: ignore[assignment]
# --8<-- [start:example]
import json
from idfkit.simulation import async_simulate, SimulationProgress


async def run_with_websocket(model, weather, websocket):
    """Run a simulation and forward progress over WebSocket."""

    async def on_progress(event: SimulationProgress) -> None:
        await websocket.send_text(
            json.dumps({
                "type": "simulation_progress",
                "phase": event.phase,
                "percent": event.percent,
                "message": event.message,
                "environment": event.environment,
            })
        )

    result = await async_simulate(model, weather, on_progress=on_progress)
    await websocket.send_text(
        json.dumps({
            "type": "simulation_complete",
            "success": result.success,
            "runtime": result.runtime_seconds,
        })
    )
    return result


# --8<-- [end:example]
