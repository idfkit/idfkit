from __future__ import annotations

from idfkit import IDFDocument
from idfkit.simulation import S3FileSystem, simulate

fs: S3FileSystem = ...  # type: ignore[assignment]
model: IDFDocument = ...  # type: ignore[assignment]
weather: str = ...  # type: ignore[assignment]
# --8<-- [start:example]
from idfkit.simulation import S3FileSystem

fs = S3FileSystem(bucket="my-bucket", prefix="runs/")
result = simulate(
    model,
    weather,
    output_dir="run-001",  # Required with fs
    fs=fs,
)
# --8<-- [end:example]
