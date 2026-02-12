from __future__ import annotations

from idfkit import IDFDocument
from idfkit.simulation import SimulationResult

model: IDFDocument = ...  # type: ignore[assignment]
result: SimulationResult = ...  # type: ignore[assignment]
# --8<-- [start:example]

from celery import Celery

from idfkit import load_idf
from idfkit.simulation import S3FileSystem, simulate

app = Celery("tasks")
app.config_from_object("celeryconfig")


@app.task(bind=True, name="simulate_to_s3")
def simulate_to_s3(
    self,
    idf_path: str,
    weather_path: str,
    s3_prefix: str,
    design_day: bool = False,
) -> dict:
    """Run a simulation and upload results to S3."""
    model = load_idf(idf_path)

    with S3FileSystem(bucket="my-sim-bucket", prefix=s3_prefix) as fs:
        result = simulate(
            model,
            weather_path,
            output_dir="results",
            design_day=design_day,
            fs=fs,
        )

    return {
        "success": result.success,
        "runtime": result.runtime_seconds,
        "s3_prefix": s3_prefix,
    }


# --8<-- [end:example]
