from __future__ import annotations

from idfkit import IDFObject
from idfkit.simulation import S3FileSystem
from typing import Any

dt: Any = ...  # type: ignore[assignment]
fs: S3FileSystem = ...  # type: ignore[assignment]
schedule: IDFObject = ...  # type: ignore[assignment]
# --8<-- [start:example]
from idfkit.simulation.fs import S3FileSystem
from idfkit.schedules import evaluate

# Configure S3 storage
fs = S3FileSystem(bucket="my-bucket", prefix="schedules/")

# Evaluate Schedule:File reading from S3
value = evaluate(schedule, dt, fs=fs, base_path="")
# --8<-- [end:example]
