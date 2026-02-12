from __future__ import annotations

from idfkit import IDFDocument
from idfkit.simulation import SimulationResult

model: IDFDocument = ...  # type: ignore[assignment]
result: SimulationResult = ...  # type: ignore[assignment]
# --8<-- [start:example]
from pathlib import Path

from celery import Celery

from idfkit import load_idf
from idfkit.simulation import SimulationProgress, simulate

app = Celery("tasks")
app.config_from_object("celeryconfig")


@app.task(bind=True, name="simulate_with_progress")
def simulate_with_progress(
    self,
    idf_path: str,
    weather_path: str,
    output_dir: str,
) -> dict:
    """Report EnergyPlus progress back to Celery task state."""

    def report_progress(progress: SimulationProgress) -> None:
        self.update_state(
            state="SIMULATING",
            meta={
                "environment": progress.environment,
                "percent": progress.percent,
            },
        )

    model = load_idf(idf_path)
    result = simulate(
        model,
        weather_path,
        output_dir=output_dir,
        on_progress=report_progress,
    )

    return {
        "success": result.success,
        "runtime": result.runtime_seconds,
        "output_dir": str(Path(result.run_dir).resolve()),
    }


# --8<-- [end:example]
