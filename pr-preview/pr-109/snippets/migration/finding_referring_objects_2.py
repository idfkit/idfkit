from __future__ import annotations

from idfkit import IDFDocument, IDFObject

doc: IDFDocument = ...  # type: ignore[assignment]
zone: IDFObject = ...  # type: ignore[assignment]
# --8<-- [start:example]
zone = doc["Zone"]["Office"]

# eppy-compatible spelling
referrers = zone.getreferingobjs()

# Corrected spelling
referrers = zone.get_referring_objects()

# Optional filters -- by IDD group and/or field name
surfaces = zone.getreferingobjs(
    iddgroups=["Thermal Zones and Surfaces"],
    fields=["zone_name"],
)
# --8<-- [end:example]
