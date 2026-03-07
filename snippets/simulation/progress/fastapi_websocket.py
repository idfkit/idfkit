from __future__ import annotations

from idfkit import IDFDocument
from idfkit.simulation import SimulationResult
from typing import Any

data: Any = ...  # type: ignore[assignment]
model: IDFDocument = ...  # type: ignore[assignment]
result: SimulationResult = ...  # type: ignore[assignment]
websocket: Any = ...  # type: ignore[assignment]
# --8<-- [start:example]
from fastapi import FastAPI, WebSocket
from idfkit import load_idf
from idfkit.simulation import async_simulate, SimulationProgress

app = FastAPI()


@app.websocket("/ws/simulate")
async def simulate_ws(websocket: WebSocket):
    await websocket.accept()
    data = await websocket.receive_json()

    model = load_idf(data["idf_path"])

    async def on_progress(event: SimulationProgress) -> None:
        await websocket.send_json({
            "phase": event.phase,
            "percent": event.percent,
            "message": event.message,
        })

    result = await async_simulate(
        model,
        data["weather_path"],
        on_progress=on_progress,
    )

    await websocket.send_json({
        "phase": "done",
        "success": result.success,
        "runtime": result.runtime_seconds,
    })
    await websocket.close()


# --8<-- [end:example]
