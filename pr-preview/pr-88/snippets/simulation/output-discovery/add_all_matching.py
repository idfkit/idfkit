from __future__ import annotations

from idfkit import IDFDocument
from idfkit.simulation import OutputVariableIndex

model: IDFDocument = ...  # type: ignore[assignment]
variables: OutputVariableIndex | None = ...  # type: ignore[assignment]
# --8<-- [start:example]
# Add all temperature outputs
count = variables.add_all_to_model(
    model,
    filter_pattern="Zone.*Temperature",
)
print(f"Added {count} output requests")
# --8<-- [end:example]
