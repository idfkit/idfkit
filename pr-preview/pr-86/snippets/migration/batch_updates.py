from __future__ import annotations

from idfkit import IDFDocument

idf: IDFDocument = ...  # type: ignore[assignment]
# --8<-- [start:example]
from eppy import json_functions

json_functions.updateidf(idf, {"Zone.Office.x_origin": 10.0})
# --8<-- [end:example]
