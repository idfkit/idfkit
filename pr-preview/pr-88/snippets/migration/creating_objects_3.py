from __future__ import annotations

from idfkit import IDFDocument

doc: IDFDocument = ...  # type: ignore[assignment]
# --8<-- [start:example]
zone = doc.newidfobject("Zone", Name="Office", X_Origin=0.0)
# --8<-- [end:example]
