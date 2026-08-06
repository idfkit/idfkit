from __future__ import annotations

from idfkit.simulation import OutputVariableIndex

variables: OutputVariableIndex | None = ...  # type: ignore[assignment]
# --8<-- [start:example]
# Get all temperature variables (°C)
temp_vars = variables.filter_by_units("C")

# Get all energy variables
energy_vars = variables.filter_by_units("J")
# --8<-- [end:example]
