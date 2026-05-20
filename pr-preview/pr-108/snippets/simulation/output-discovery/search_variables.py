from __future__ import annotations

from idfkit.simulation import OutputVariableIndex

variables: OutputVariableIndex | None = ...  # type: ignore[assignment]
# --8<-- [start:example]
# Search by name pattern
matches = variables.search("Zone Mean Air Temperature")

# Search with regex
matches = variables.search(r"Zone.*Temperature")

# Case-insensitive
matches = variables.search("temperature")  # Finds all temperature vars
# --8<-- [end:example]
