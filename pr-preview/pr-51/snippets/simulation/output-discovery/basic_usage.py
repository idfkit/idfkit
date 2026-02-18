from __future__ import annotations

from idfkit import IDFDocument
from idfkit.simulation import OutputVariableIndex, SimulationResult

model: IDFDocument = ...  # type: ignore[assignment]
result: SimulationResult = ...  # type: ignore[assignment]
variables: OutputVariableIndex | None = ...  # type: ignore[assignment]
weather: str = ...  # type: ignore[assignment]
# --8<-- [start:example]
from idfkit.simulation import simulate

result = simulate(model, weather)

variables = result.variables
if variables is not None:
    # Search for temperature-related outputs
    matches = variables.search("Temperature")
    for var in matches[:10]:
        print(f"{var.name} [{var.units}]")
# --8<-- [end:example]
