"""Creation signatures of generated classes (stub only).

DO NOT EDIT — regenerate with:
    python -m idfkit.codegen.generate_stubs
"""

from __future__ import annotations

from collections.abc import Sequence

from .. import _generated_types as _g

class RoomAirTemperaturePatternSurfaceMapping_v8_9_to_v22_1:
    def __call__(
        self,
        name: str,
        /,
        *,
        control_integer_for_pattern_control_schedule_name: float,
        thermostat_offset: float | None = ...,
        return_air_offset: float | None = ...,
        exhaust_air_offset: float | None = ...,
        surface_deltas: Sequence[
            _g.RoomAirTemperaturePatternSurfaceMappingSurfaceDeltasItem
            | _g.RoomAirTemperaturePatternSurfaceMappingSurfaceDeltasGroup
        ] = ...,
    ) -> None:
        """Create a new ``RoomAir:TemperaturePattern:SurfaceMapping`` and add it to the document.

        Defines a distribution pattern for the air temperatures adjacent to individual surfaces. This allows controlling the adjacent air temperature on a surface-by-surface basis rather than by height. This allows modeling different adjacent air temperatures on the opposite sides of the zone. Used in combination with RoomAir:TemperaturePattern:UserDefined.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v22.1/io-reference/overview/group-room-air-models/#roomairtemperaturepatternsurfacemapping
        """
