from __future__ import annotations

from idfkit import IDFDocument, ValidationResult

model: IDFDocument = ...  # type: ignore[assignment]
validation: ValidationResult = ...  # type: ignore[assignment]
# --8<-- [start:example]
from idfkit import validate_document

validation = validate_document(model)
if not validation.is_valid:
    for err in validation.errors:
        print(err)
# --8<-- [end:example]
