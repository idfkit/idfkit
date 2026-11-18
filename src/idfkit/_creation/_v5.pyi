"""Creation signatures of generated classes (stub only).

DO NOT EDIT — regenerate with:
    python -m idfkit.codegen.generate_stubs
"""

from __future__ import annotations

class CoilSystemIntegratedHeatPumpAirSource_v8_9_to_v22_1:
    def __call__(
        self,
        name: str,
        /,
        *,
        supply_hot_water_flow_sensor_node_name: str,
        space_cooling_coil_name: str,
        space_heating_coil_name: str | None = ...,
        dedicated_water_heating_coil_name: str | None = ...,
        scwh_coil_name: str | None = ...,
        scdwh_cooling_coil_name: str | None = ...,
        scdwh_water_heating_coil_name: str | None = ...,
        shdwh_heating_coil_name: str | None = ...,
        shdwh_water_heating_coil_name: str | None = ...,
        indoor_temperature_limit_for_scwh_mode: float | None = 20,
        ambient_temperature_limit_for_scwh_mode: float | None = 27,
        indoor_temperature_above_which_wh_has_higher_priority: float | None = 20,
        ambient_temperature_above_which_wh_has_higher_priority: float | None = 20,
        flag_to_indicate_load_control_in_scwh_mode: float | None = 0,
        minimum_speed_level_for_scwh_mode: float | None = 1,
        maximum_water_flow_volume_before_switching_from_scdwh_to_scwh_mode: float | None = 0,
        minimum_speed_level_for_scdwh_mode: float | None = 1,
        maximum_running_time_before_allowing_electric_resistance_heat_use_during_shdwh_mode: float | None = 360,
        minimum_speed_level_for_shdwh_mode: float | None = 1,
        validate: bool = True,
    ) -> None:
        """Create a new ``CoilSystem:IntegratedHeatPump:AirSource`` and add it to the document.

        This object is used for air-source integrated heat pump, a collection of its working modes.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v22.1/io-reference/overview/group-heating-and-cooling-coils/#coilsystemintegratedheatpumpairsource
        """
