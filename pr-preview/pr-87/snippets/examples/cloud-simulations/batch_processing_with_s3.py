from __future__ import annotations

from idfkit import IDFDocument
from idfkit.simulation import BatchResult, S3FileSystem, SimulationJob

batch: BatchResult = ...  # type: ignore[assignment]
fs: S3FileSystem = ...  # type: ignore[assignment]
jobs: list[SimulationJob] = ...  # type: ignore[assignment]
variant: IDFDocument = ...  # type: ignore[assignment]
variants: list[IDFDocument] = ...  # type: ignore[assignment]
# --8<-- [start:example]
from idfkit.simulation import simulate_batch, SimulationJob, S3FileSystem

fs = S3FileSystem(bucket="my-bucket", prefix="batch-42/")

jobs = [
    SimulationJob(
        model=variant,
        weather="weather.epw",
        label=f"case-{i}",
        output_dir=f"case-{i}",
    )
    for i, variant in enumerate(variants)
]

batch = simulate_batch(jobs, max_workers=4, fs=fs)

# All results stored in S3
for i, result in enumerate(batch):
    print(f"Case {i}: s3://my-bucket/batch-42/case-{i}/")
# --8<-- [end:example]
