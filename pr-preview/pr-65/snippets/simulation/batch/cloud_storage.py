from __future__ import annotations

from idfkit import IDFDocument
from idfkit.simulation import S3FileSystem, SimulationJob, simulate_batch

fs: S3FileSystem = ...  # type: ignore[assignment]
jobs: list[SimulationJob] = ...  # type: ignore[assignment]
variant: IDFDocument = ...  # type: ignore[assignment]
variants: list[IDFDocument] = ...  # type: ignore[assignment]
# --8<-- [start:example]
from idfkit.simulation import S3FileSystem

fs = S3FileSystem(bucket="my-bucket", prefix="study-001/")

# Each job needs an explicit output_dir
jobs = [
    SimulationJob(
        model=variant,
        weather="weather.epw",
        label=f"case-{i}",
        output_dir=f"case-{i}",  # Required with fs
    )
    for i, variant in enumerate(variants)
]

batch = simulate_batch(jobs, fs=fs)
# --8<-- [end:example]
