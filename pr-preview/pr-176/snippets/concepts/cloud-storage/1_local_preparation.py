from __future__ import annotations

from idfkit import IDFDocument
from idfkit.simulation import S3FileSystem

fs: S3FileSystem = ...  # type: ignore[assignment]
variant: IDFDocument = ...  # type: ignore[assignment]
variants: list[IDFDocument] = ...  # type: ignore[assignment]
# --8<-- [start:example]
from idfkit.simulation import SimulationJob, S3FileSystem

fs = S3FileSystem(bucket="simulations", prefix="study-001/")

jobs = [
    SimulationJob(
        model=variant,
        weather="weather.epw",
        label=f"case-{i}",
        output_dir=f"case-{i}",
        fs=fs,
    )
    for i, variant in enumerate(variants)
]
# --8<-- [end:example]
