from __future__ import annotations

from idfkit import IDFDocument
from idfkit.simulation import OutputVariableIndex

model: IDFDocument = ...  # type: ignore[assignment]
variables: OutputVariableIndex | None = ...  # type: ignore[assignment]
# --8<-- [start:example]
variables.add_all_to_model(
    model,
    filter_pattern="Temperature",
    reporting_frequency="Hourly",
)
# --8<-- [end:example]
