from __future__ import annotations

from idfkit import IDFDocument
from idfkit.simulation import SimulationResult

doc: IDFDocument = ...  # type: ignore[assignment]
result: SimulationResult = ...  # type: ignore[assignment]
# --8<-- [start:example]
from idfkit import validate_document

result = validate_document(doc)
if not result.is_valid:
    for error in result.errors:
        print(error)
# --8<-- [end:example]
