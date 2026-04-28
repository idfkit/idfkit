from __future__ import annotations

from idfkit import IDFDocument
from idfkit.simulation import S3FileSystem

fs: S3FileSystem = ...  # type: ignore[assignment]
job_id: str = ...  # type: ignore[assignment]
model: IDFDocument = ...  # type: ignore[assignment]
weather_path: str = ...  # type: ignore[assignment]
# --8<-- [start:example]
# worker.py (runs on AWS Batch, Kubernetes, etc.)
from idfkit.simulation import simulate, S3FileSystem

fs = S3FileSystem(bucket="simulations", prefix="study-001/")

# Run single job
result = simulate(
    model,
    weather_path,  # Must be local
    output_dir=f"case-{job_id}",
    fs=fs,
)

# Results uploaded to S3 automatically
# --8<-- [end:example]
