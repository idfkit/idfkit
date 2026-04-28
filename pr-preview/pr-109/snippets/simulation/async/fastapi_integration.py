from __future__ import annotations

from idfkit import IDFDocument
from idfkit.simulation import SimulationResult

model: IDFDocument = ...  # type: ignore[assignment]
result: SimulationResult = ...  # type: ignore[assignment]
weather_path: str = ...  # type: ignore[assignment]
# --8<-- [start:example]
from fastapi import FastAPI
from idfkit import load_idf
from idfkit.simulation import async_simulate

app = FastAPI()


@app.post("/simulate")
async def run_simulation(idf_path: str, weather_path: str):
    model = load_idf(idf_path)
    result = await async_simulate(model, weather_path, design_day=True)

    return {
        "success": result.success,
        "runtime": result.runtime_seconds,
        "errors": result.errors.summary(),
    }


# --8<-- [end:example]
