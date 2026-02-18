from __future__ import annotations


from idfkit import IDFDocument
from idfkit.simulation import SimulationResult

model: IDFDocument = ...  # type: ignore[assignment]
result: SimulationResult = ...  # type: ignore[assignment]
# --8<-- [start:example]
# tasks.py — parametric task that builds variants on the worker
from pathlib import Path

from celery import Celery

from idfkit import load_idf
from idfkit.simulation import simulate

app = Celery("tasks")
app.config_from_object("celeryconfig")


@app.task(bind=True, name="run_parametric_case")
def run_parametric_case(
    self,
    base_idf_path: str,
    weather_path: str,
    output_dir: str,
    wall_conductivity: float | None = None,
    window_u_factor: float | None = None,
    infiltration_rate: float | None = None,
    label: str = "",
) -> dict:
    """Apply parameter overrides to a base model and simulate."""
    model = load_idf(base_idf_path)

    # Apply overrides
    if wall_conductivity is not None:
        for mat in model["Material"]:
            if "wall" in mat.name.lower():
                mat.conductivity = wall_conductivity

    if window_u_factor is not None:
        for win in model["WindowMaterial:SimpleGlazingSystem"]:
            win.u_factor = window_u_factor

    if infiltration_rate is not None:
        for inf in model["ZoneInfiltration:DesignFlowRate"]:
            inf.design_flow_rate = infiltration_rate

    result = simulate(model, weather_path, output_dir=output_dir, design_day=True)
    return {
        "label": label,
        "success": result.success,
        "runtime": result.runtime_seconds,
        "output_dir": str(Path(result.run_dir).resolve()),
    }


# --8<-- [end:example]
