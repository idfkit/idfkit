from __future__ import annotations

from idfkit.simulation import OutputVariableIndex

variables: OutputVariableIndex | None = ...  # type: ignore[assignment]
# --8<-- [start:example]
# All output variables
for var in variables.variables:
    print(f"Variable: {var.name} [{var.units}]")

# All meters
for meter in variables.meters:
    print(f"Meter: {meter.name} [{meter.units}]")
# --8<-- [end:example]
