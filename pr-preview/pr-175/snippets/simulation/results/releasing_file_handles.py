from __future__ import annotations

import tempfile
from pathlib import Path

from idfkit import IDFDocument
from idfkit.simulation import SimulationResult, simulate

model: IDFDocument = ...  # type: ignore[assignment]
result: SimulationResult = ...  # type: ignore[assignment]
weather: str = ...  # type: ignore[assignment]
# --8<-- [start:example]
# The result context exits first - closing the SQLite connection - then
# TemporaryDirectory cleans up, so rmtree succeeds even on Windows.
with tempfile.TemporaryDirectory() as tmp, simulate(model, weather, output_dir=Path(tmp) / "run") as result:
    temps = result.sql.get_timeseries("Zone Mean Air Temperature", "ZONE 1")

# Equivalent without a context manager:
result = simulate(model, weather)
try:
    temps = result.sql.get_timeseries("Zone Mean Air Temperature", "ZONE 1")
finally:
    result.close()  # idempotent; reopens lazily if you touch result.sql again
# --8<-- [end:example]
