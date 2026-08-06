from __future__ import annotations

from idfkit import IDFDocument
from idfkit.simulation import SimulationResult

model: IDFDocument = ...  # type: ignore[assignment]
result: SimulationResult = ...  # type: ignore[assignment]
weather: str = ...  # type: ignore[assignment]
# --8<-- [start:example]
from idfkit.simulation import simulate

result = simulate(model, weather)

# Basic info
print(f"Success: {result.success}")
print(f"Exit code: {result.exit_code}")
print(f"Runtime: {result.runtime_seconds:.1f}s")
print(f"Output dir: {result.run_dir}")

# Parsed outputs (lazy-loaded)
result.errors  # ErrorReport from .err file
result.sql  # SQLResult from .sql database
result.variables  # OutputVariableIndex from .rdd/.mdd
result.csv  # CSVResult from .csv file
result.html  # HTMLResult from HTML tabular output
# --8<-- [end:example]
