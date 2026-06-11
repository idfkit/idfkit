from __future__ import annotations

from idfkit import IDFDocument
from idfkit.simulation import SimulationResult, simulate

model: IDFDocument = ...  # type: ignore[assignment]
result: SimulationResult = ...  # type: ignore[assignment]
weather: str = ...  # type: ignore[assignment]
# --8<-- [start:example]
result = simulate(model, weather)  # Fast: just runs EnergyPlus

# These are lazy — parsed on first access:
result.errors  # Parses ERR file
result.sql  # Opens SQLite database
result.variables  # Parses RDD file
# --8<-- [end:example]
