from __future__ import annotations

from idfkit.simulation import OutputVariableIndex

variables: OutputVariableIndex | None = ...  # type: ignore[assignment]
# --8<-- [start:example]
# By name pattern
temp_vars = [v for v in variables if "Temperature" in v.name]

# By key
zone1_vars = [v for v in variables if v.key_value == "ZONE 1"]
# --8<-- [end:example]
