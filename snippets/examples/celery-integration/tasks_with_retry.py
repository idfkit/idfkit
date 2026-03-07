from __future__ import annotations

from idfkit import IDFDocument
from idfkit.simulation import SimulationResult

model: IDFDocument = ...  # type: ignore[assignment]
result: SimulationResult = ...  # type: ignore[assignment]
# --8<-- [start:example]
from pathlib import Path

from celery import Celery

from idfkit import load_idf
from idfkit.exceptions import SimulationError
from idfkit.simulation import simulate

app = Celery("tasks")
app.config_from_object("celeryconfig")


@app.task(
    bind=True,
    name="simulate_with_retry",
    autoretry_for=(SimulationError, OSError),
    retry_backoff=60,
    retry_backoff_max=600,
    max_retries=3,
)
def simulate_with_retry(
    self,
    idf_path: str,
    weather_path: str,
    output_dir: str,
) -> dict:
    """Simulate with automatic retry on transient failures."""
    model = load_idf(idf_path)
    result = simulate(model, weather_path, output_dir=output_dir, design_day=True)

    if not result.success:
        # Raise to trigger retry for EnergyPlus errors that may be transient
        raise SimulationError(
            f"Simulation failed (attempt {self.request.retries + 1})",
            exit_code=1,
        )

    return {
        "success": True,
        "runtime": result.runtime_seconds,
        "output_dir": str(Path(result.run_dir).resolve()),
        "retries": self.request.retries,
    }


# --8<-- [end:example]
