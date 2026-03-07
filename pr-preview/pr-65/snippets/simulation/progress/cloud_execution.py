from __future__ import annotations

from idfkit import IDFDocument
from idfkit.simulation import S3FileSystem

fs: S3FileSystem = ...  # type: ignore[assignment]
model: IDFDocument = ...  # type: ignore[assignment]
# --8<-- [start:example]
from idfkit.simulation import simulate, S3FileSystem, SimulationProgress

fs = S3FileSystem(bucket="my-bucket", prefix="runs/")


def on_progress(event: SimulationProgress) -> None:
    # This fires during local execution, before upload
    print(f"{event.phase}: {event.percent}")


result = simulate(
    model,
    "weather.epw",
    output_dir="run-001",
    fs=fs,
    on_progress=on_progress,
)
# --8<-- [end:example]
