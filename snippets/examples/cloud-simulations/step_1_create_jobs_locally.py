from __future__ import annotations

from idfkit import IDFDocument
from idfkit.simulation import SimulationJob

jobs: list[SimulationJob] = ...  # type: ignore[assignment]
model_variants: list[IDFDocument] = ...  # type: ignore[assignment]
variant: IDFDocument = ...  # type: ignore[assignment]
# --8<-- [start:example]
from idfkit.simulation import SimulationJob, S3FileSystem

fs = S3FileSystem(bucket="simulations", prefix="study-001/")

# Create job specifications
jobs = []
for i, variant in enumerate(model_variants):
    jobs.append(
        SimulationJob(
            model=variant,
            weather="weather.epw",
            label=f"case-{i:04d}",
            output_dir=f"case-{i:04d}",
        )
    )

# Save job specs (e.g., as JSON or pickle)
# --8<-- [end:example]
