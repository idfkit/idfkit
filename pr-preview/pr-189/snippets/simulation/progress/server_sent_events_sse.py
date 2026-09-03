from __future__ import annotations

from idfkit import IDFDocument
from idfkit.simulation import SimulationResult
from typing import Any

data: Any = ...  # type: ignore[assignment]
model: IDFDocument = ...  # type: ignore[assignment]
result: SimulationResult = ...  # type: ignore[assignment]
weather_path: str = ...  # type: ignore[assignment]
# --8<-- [start:example]
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from idfkit import load_idf
from idfkit.simulation import async_simulate, SimulationProgress
import asyncio
import json

app = FastAPI()


@app.get("/api/simulate/stream")
async def simulate_stream(idf_path: str, weather_path: str):
    queue: asyncio.Queue[str] = asyncio.Queue()

    async def on_progress(event: SimulationProgress) -> None:
        data = json.dumps({
            "phase": event.phase,
            "percent": event.percent,
            "message": event.message,
        })
        await queue.put(f"data: {data}\n\n")

    async def generate():
        model = load_idf(idf_path)
        task = asyncio.create_task(async_simulate(model, weather_path, on_progress=on_progress))
        while not task.done():
            try:
                chunk = await asyncio.wait_for(queue.get(), timeout=0.5)
                yield chunk
            except asyncio.TimeoutError:
                yield ": keepalive\n\n"
        result = await task
        yield f"data: {json.dumps({'phase': 'done', 'success': result.success})}\n\n"

    return StreamingResponse(generate(), media_type="text/event-stream")


# --8<-- [end:example]
