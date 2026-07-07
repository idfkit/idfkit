from __future__ import annotations

from idfkit import IDFDocument
from idfkit.simulation import SimulationResult, simulate

model: IDFDocument = ...  # type: ignore[assignment]
result: SimulationResult = ...  # type: ignore[assignment]
weather: str = ...  # type: ignore[assignment]
# --8<-- [start:example]
result = simulate(model, weather)  # Just runs EnergyPlus
result.errors  # Parses ERR file on first access
result.sql  # Opens SQLite database on first access
# --8<-- [end:example]
