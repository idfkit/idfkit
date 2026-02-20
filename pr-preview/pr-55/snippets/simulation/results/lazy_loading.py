from __future__ import annotations

from idfkit import IDFDocument
from idfkit.simulation import SimulationResult, simulate

model: IDFDocument = ...  # type: ignore[assignment]
result: SimulationResult = ...  # type: ignore[assignment]
weather: str = ...  # type: ignore[assignment]
# --8<-- [start:example]
result = simulate(model, weather)

# Nothing parsed yet - only metadata stored

result.errors  # NOW parses .err file
result.sql  # NOW opens SQLite database
result.variables  # NOW parses .rdd/.mdd files
result.html  # NOW parses HTML tabular output
# --8<-- [end:example]
