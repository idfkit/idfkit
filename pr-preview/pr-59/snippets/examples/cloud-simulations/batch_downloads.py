from __future__ import annotations

from idfkit import IDFObject
from idfkit.simulation import S3FileSystem, SimulationResult
from typing import Any

data: Any = ...  # type: ignore[assignment]
fs: S3FileSystem = ...  # type: ignore[assignment]
obj: IDFObject = ...  # type: ignore[assignment]
# --8<-- [start:example]
import tempfile
from pathlib import Path

with tempfile.TemporaryDirectory() as tmp:
    # Download all files for a run
    for obj in fs.glob("run-001", "*"):
        data = fs.read_bytes(obj)
        local_path = Path(tmp) / Path(obj).name
        local_path.write_bytes(data)

    # Now use local result
    result = SimulationResult.from_directory(tmp)
    # Multiple queries without network calls
# --8<-- [end:example]
