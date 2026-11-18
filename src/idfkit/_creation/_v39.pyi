"""Creation signatures of generated classes (stub only).

DO NOT EDIT — regenerate with:
    python -m idfkit.codegen.generate_stubs
"""

from __future__ import annotations

from collections.abc import Sequence
from typing import Literal

from .. import _generated_types as _g

class FenestrationSurfaceDetailed_v8_9:
    def __call__(
        self,
        name: str,
        /,
        *,
        surface_type: Literal["Door", "GlassDoor", "TubularDaylightDiffuser", "TubularDaylightDome", "Window"],
        construction_name: str,
        building_surface_name: str,
        vertex_1_x_coordinate: float,
        vertex_1_y_coordinate: float,
        vertex_1_z_coordinate: float,
        vertex_2_x_coordinate: float,
        vertex_2_y_coordinate: float,
        vertex_2_z_coordinate: float,
        vertex_3_x_coordinate: float,
        vertex_3_y_coordinate: float,
        vertex_3_z_coordinate: float,
        outside_boundary_condition_object: str | None = ...,
        view_factor_to_ground: float | Literal["Autocalculate"] | None = "Autocalculate",
        shading_control_name: str | None = ...,
        frame_and_divider_name: str | None = ...,
        multiplier: float | None = 1,
        number_of_vertices: float | Literal["Autocalculate"] | None = "Autocalculate",
        vertex_4_x_coordinate: float | None = ...,
        vertex_4_y_coordinate: float | None = ...,
        vertex_4_z_coordinate: float | None = ...,
    ) -> None:
        """Create a new ``FenestrationSurface:Detailed`` and add it to the document.

        Allows for detailed entry of subsurfaces (windows, doors, glass doors, tubular daylighting devices).

        EnergyPlus I/O Reference: https://docs.idfkit.com/v8.9/io-reference/overview/group-thermal-zone-description-geometry/#fenestrationsurfacedetailed
        """

class DemandManagerElectricEquipment_v8_9_to_v22_1:
    def __call__(
        self,
        name: str,
        /,
        *,
        limit_control: Literal["Fixed", "Off"],
        selection_control: Literal["All", "RotateMany", "RotateOne"],
        availability_schedule_name: str | None = ...,
        minimum_limit_duration: float | None = ...,
        maximum_limit_fraction: float | None = ...,
        limit_step_change: float | None = ...,
        rotation_duration: float | None = ...,
        equipment: Sequence[
            _g.DemandManagerElectricEquipmentEquipmentItem | _g.DemandManagerElectricEquipmentEquipmentGroup
        ] = ...,
    ) -> None:
        """Create a new ``DemandManager:ElectricEquipment`` and add it to the document.

        used for demand limiting ElectricEquipment objects.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v22.1/io-reference/overview/group-demand-limiting-controls/#demandmanagerelectricequipment
        """
