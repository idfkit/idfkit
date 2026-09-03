from __future__ import annotations

from idfkit.simulation import S3FileSystem, SimulationResult
from pathlib import Path
from typing import Any

data: Any = ...  # type: ignore[assignment]
s3_fs: S3FileSystem = ...  # type: ignore[assignment]
# --8<-- [start:example]
import tempfile

# Download entire result directory
with tempfile.TemporaryDirectory() as tmp:
    # Copy from S3 to local
    for path in s3_fs.glob("run-001", "*"):
        data = s3_fs.read_bytes(path)
        local_path = Path(tmp) / Path(path).name
        local_path.write_bytes(data)

    # Use local result
    result = SimulationResult.from_directory(tmp)
    # Multiple queries without network calls
# --8<-- [end:example]
