from __future__ import annotations

from idfkit import IDFDocument
from idfkit.simulation import OutputVariableIndex, SimulationResult

model: IDFDocument = ...  # type: ignore[assignment]
result: SimulationResult = ...  # type: ignore[assignment]
variables: OutputVariableIndex | None = ...  # type: ignore[assignment]
# --8<-- [start:example]
variables = result.variables
if variables is not None:
    # Search for variables
    matches = variables.search("Temperature")
    for var in matches:
        print(f"{var.name} [{var.units}]")

    # Add outputs to model for next run
    variables.add_all_to_model(model, filter_pattern="Zone.*Temperature")
# --8<-- [end:example]
