from __future__ import annotations

from idfkit import IDFDocument
from idfkit.simulation import SimulationResult

model: IDFDocument = ...  # type: ignore[assignment]
result: SimulationResult = ...  # type: ignore[assignment]
# --8<-- [start:example]
# tasks.py
from pathlib import Path

from celery import Celery

from idfkit import load_idf
from idfkit.simulation import simulate

app = Celery("tasks")
app.config_from_object("celeryconfig")


@app.task(bind=True, name="simulate_building")
def simulate_building(
    self,
    idf_path: str,
    weather_path: str,
    output_dir: str,
    design_day: bool = False,
) -> dict:
    """Run a single EnergyPlus simulation and return a result summary."""
    model = load_idf(idf_path)
    result = simulate(
        model,
        weather_path,
        output_dir=output_dir,
        design_day=design_day,
        timeout=14000.0,
    )
    return {
        "success": result.success,
        "runtime": result.runtime_seconds,
        "output_dir": str(Path(result.run_dir).resolve()),
    }


# --8<-- [end:example]
