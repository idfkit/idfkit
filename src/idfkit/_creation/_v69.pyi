"""Creation signatures of generated classes (stub only).

DO NOT EDIT — regenerate with:
    python -m idfkit.codegen.generate_stubs
"""

from __future__ import annotations

class WallInterzone_v8_9_to_v9_5:
    def __call__(
        self,
        name: str,
        /,
        *,
        construction_name: str,
        zone_name: str,
        outside_boundary_condition_object: str,
        azimuth_angle: float | None = ...,
        tilt_angle: float | None = 90,
        starting_x_coordinate: float | None = ...,
        starting_y_coordinate: float | None = ...,
        starting_z_coordinate: float | None = ...,
        length: float | None = ...,
        height: float | None = ...,
        validate: bool = True,
    ) -> None:
        """Create a new ``Wall:Interzone`` and add it to the document.

        Allows for simplified entry of interzone walls (walls between zones).

        EnergyPlus I/O Reference: https://docs.idfkit.com/v9.5/io-reference/overview/group-thermal-zone-description-geometry/#wallinterzone
        """
