from __future__ import annotations

from idfkit import IDFDocument, IDFObject

doc: IDFDocument = ...  # type: ignore[assignment]
surface: IDFObject = ...  # type: ignore[assignment]
# --8<-- [start:example]
from idfkit.geometry import (
    calculate_surface_area,
    calculate_surface_tilt,
    calculate_surface_azimuth,
    calculate_zone_volume,
    calculate_zone_height,
    calculate_zone_ceiling_area,
)

for surface in doc["BuildingSurface:Detailed"]:
    area = calculate_surface_area(surface)
    tilt = calculate_surface_tilt(surface)  # 0=up, 90=vertical, 180=down
    azimuth = calculate_surface_azimuth(surface)  # 0=north, 90=east, 180=south
    print(f"{surface.name}: {area:.1f} m2, tilt={tilt:.0f}, azimuth={azimuth:.0f}")

print("Zone volume:", calculate_zone_volume(doc, "Office"))
print("Zone height:", calculate_zone_height(doc, "Office"))
print("Ceiling area:", calculate_zone_ceiling_area(doc, "Office"))
# --8<-- [end:example]
