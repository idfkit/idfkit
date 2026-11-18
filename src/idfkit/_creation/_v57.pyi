"""Creation signatures of generated classes (stub only).

DO NOT EDIT — regenerate with:
    python -m idfkit.codegen.generate_stubs
"""

from __future__ import annotations

from typing import Literal

from .. import _generated_types as _g

class CeilingInterzone_v8_9_to_v9_5:
    def __call__(
        self,
        name: str,
        /,
        *,
        construction_name: str,
        zone_name: str,
        outside_boundary_condition_object: str,
        azimuth_angle: float | None = ...,
        tilt_angle: float | None = 0,
        starting_x_coordinate: float | None = ...,
        starting_y_coordinate: float | None = ...,
        starting_z_coordinate: float | None = ...,
        length: float | None = ...,
        width: float | None = ...,
    ) -> None:
        """Create a new ``Ceiling:Interzone`` and add it to the document.

        Allows for simplified entry of ceilings using adjacent zone (interzone) heat transfer - adjacent surface should be a floor

        EnergyPlus I/O Reference: https://docs.idfkit.com/v9.5/io-reference/overview/group-thermal-zone-description-geometry/#ceilinginterzone
        """

class ZoneHVACTerminalUnitVariableRefrigerantFlow_v9_3_to_v23_1:
    def __call__(
        self,
        name: str = "",
        /,
        *,
        terminal_unit_air_inlet_node_name: str,
        terminal_unit_air_outlet_node_name: str,
        terminal_unit_availability_schedule: str | None = ...,
        cooling_supply_air_flow_rate: float | Literal["Autosize"] | None = ...,
        no_cooling_supply_air_flow_rate: float | Literal["Autosize"] | None = ...,
        heating_supply_air_flow_rate: float | Literal["Autosize"] | None = ...,
        no_heating_supply_air_flow_rate: float | Literal["Autosize"] | None = ...,
        cooling_outdoor_air_flow_rate: float | Literal["Autosize"] | None = ...,
        heating_outdoor_air_flow_rate: float | Literal["Autosize"] | None = ...,
        no_load_outdoor_air_flow_rate: float | Literal["Autosize"] | None = ...,
        supply_air_fan_operating_mode_schedule_name: str | None = ...,
        supply_air_fan_placement: Literal["", "BlowThrough", "DrawThrough"] | None = "BlowThrough",
        supply_air_fan_object_type: Literal[
            "", "Fan:ConstantVolume", "Fan:OnOff", "Fan:SystemModel", "Fan:VariableVolume"
        ]
        | None = "Fan:ConstantVolume",
        supply_air_fan_object_name: str | None = ...,
        outside_air_mixer_object_type: Literal["OutdoorAir:Mixer"] | None = ...,
        outside_air_mixer_object_name: str | None = ...,
        cooling_coil_object_type: Literal[
            "Coil:Cooling:DX:VariableRefrigerantFlow", "Coil:Cooling:DX:VariableRefrigerantFlow:FluidTemperatureControl"
        ]
        | None = ...,
        cooling_coil_object_name: str | None = ...,
        heating_coil_object_type: Literal[
            "Coil:Heating:DX:VariableRefrigerantFlow", "Coil:Heating:DX:VariableRefrigerantFlow:FluidTemperatureControl"
        ]
        | None = ...,
        heating_coil_object_name: str | None = ...,
        zone_terminal_unit_on_parasitic_electric_energy_use: float | None = 0,
        zone_terminal_unit_off_parasitic_electric_energy_use: float | None = 0,
        rated_heating_capacity_sizing_ratio: float | None = 1,
        availability_manager_list_name: str | None = ...,
        design_specification_zonehvac_sizing_object_name: str | None = ...,
        supplemental_heating_coil_object_type: Literal[
            "Coil:Heating:Electric", "Coil:Heating:Fuel", "Coil:Heating:Steam", "Coil:Heating:Water"
        ]
        | None = ...,
        supplemental_heating_coil_name: str | None = ...,
        maximum_supply_air_temperature_from_supplemental_heater: float | Literal["", "Autosize"] | None = "Autosize",
        maximum_outdoor_dry_bulb_temperature_for_supplemental_heater_operation: float | None = 21,
        controlling_zone_or_thermostat_location: str | None = ...,
    ) -> None:
        """Create a new ``ZoneHVAC:TerminalUnit:VariableRefrigerantFlow`` and add it to the document.

        A terminal unit with variable refrigerant flow (VRF) DX cooling and heating coils (air-to-air heat pump). The VRF terminal units are served by an AirConditioner:VariableRefrigerantFlow or AirConditioner:VariableRefrigerantFlow:FluidTemperatureControl:* system. Terminal units can be configured as zone, air loop or outside air system equipment.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v23.1/io-reference/overview/group-zone-forced-air-units/#zonehvacterminalunitvariablerefrigerantflow
        """

class GroundHeatExchangerSlinky_v8_9_to_v22_1:
    def __call__(
        self,
        name: str,
        /,
        *,
        inlet_node_name: str,
        outlet_node_name: str,
        undisturbed_ground_temperature_model_type: Literal[
            "Site:GroundTemperature:Undisturbed:FiniteDifference",
            "Site:GroundTemperature:Undisturbed:KusudaAchenbach",
            "Site:GroundTemperature:Undisturbed:Xing",
        ],
        undisturbed_ground_temperature_model_name: str,
        design_flow_rate: float | None = 0.002,
        soil_thermal_conductivity: float | None = 1.08,
        soil_density: float | None = 962,
        soil_specific_heat: float | None = 2576,
        pipe_thermal_conductivity: float | None = 0.4,
        pipe_density: float | None = 641,
        pipe_specific_heat: float | None = 2405,
        pipe_outer_diameter: float | None = 0.02667,
        pipe_thickness: float | None = 0.002413,
        heat_exchanger_configuration: Literal["Horizontal", "Vertical"] | None = ...,
        coil_diameter: float | None = 1,
        coil_pitch: float | None = 0.2,
        trench_depth: float | None = 1.8,
        trench_length: float | None = 10,
        number_of_trenches: float | None = 1,
        horizontal_spacing_between_pipes: float | None = 2,
        maximum_length_of_simulation: float | None = ...,
    ) -> None:
        """Create a new ``GroundHeatExchanger:Slinky`` and add it to the document.

        This models a slinky horizontal heat exchanger placed in a series of trenches The model uses the model developed by: Xiong, Z., D.E. Fisher, and J.D. Spitler. 2015. Development and Validation of a Slinky Ground Heat Exchanger Model. Applied Energy 141: 57-69.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v22.1/io-reference/overview/group-condenser-equipment/#groundheatexchangerslinky
        """

class RoomAirTemperaturePatternTwoGradient_v8_9_to_v22_1:
    def __call__(
        self,
        this_type_has_no_name_field: _g._PassFieldsAsKeywords = ...,
        /,
        *,
        room_air_temperature_pattern_two_gradient_name: str,
        control_integer_for_pattern_control_schedule_name: float,
        thermostat_height: float | None = ...,
        return_air_height: float | None = ...,
        exhaust_air_height: float | None = ...,
        temperature_gradient_lower_bound: float | None = ...,
        temperature_gradient_upper_bound: float | None = ...,
        gradient_interpolation_mode: Literal[
            "OutdoorDryBulbTemperature",
            "SensibleCoolingLoad",
            "SensibleHeatingLoad",
            "ZoneAndOutdoorTemperatureDifference",
            "ZoneDryBulbTemperature",
        ]
        | None = ...,
        upper_temperature_bound: float | None = ...,
        lower_temperature_bound: float | None = ...,
        upper_heat_rate_bound: float | None = ...,
        lower_heat_rate_bound: float | None = ...,
    ) -> None:
        """Create a new ``RoomAir:TemperaturePattern:TwoGradient`` and add it to the document.

        Used to model room air with two temperature gradients in the vertical direction. Used in combination with RoomAir:TemperaturePattern:UserDefined.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v22.1/io-reference/overview/group-room-air-models/#roomairtemperaturepatterntwogradient
        """

class CoilCoolingWaterToAirHeatPumpEquationFit_v23_2_to_v25_1:
    def __call__(
        self,
        name: str,
        /,
        *,
        water_inlet_node_name: str,
        water_outlet_node_name: str,
        air_inlet_node_name: str,
        air_outlet_node_name: str,
        rated_air_flow_rate: float | Literal["Autosize"],
        rated_water_flow_rate: float | Literal["Autosize"],
        gross_rated_total_cooling_capacity: float | Literal["Autosize"],
        gross_rated_sensible_cooling_capacity: float | Literal["Autosize"],
        gross_rated_cooling_cop: float,
        total_cooling_capacity_curve_name: str,
        sensible_cooling_capacity_curve_name: str,
        cooling_power_consumption_curve_name: str,
        part_load_fraction_correlation_curve_name: str,
        rated_entering_water_temperature: float | None = 30,
        rated_entering_air_dry_bulb_temperature: float | None = 27,
        rated_entering_air_wet_bulb_temperature: float | None = 19,
        nominal_time_for_condensate_removal_to_begin: float | None = 0,
        ratio_of_initial_moisture_evaporation_rate_and_steady_state_latent_capacity: float | None = 0,
        maximum_cycling_rate: float | None = 0,
        latent_capacity_time_constant: float | None = 0,
        fan_delay_time: float | None = 60,
    ) -> None:
        """Create a new ``Coil:Cooling:WaterToAirHeatPump:EquationFit`` and add it to the document.

        Direct expansion (DX) cooling coil for water-to-air heat pump (includes electric compressor), single-speed, equation-fit model. Optional inputs for moisture evaporation from wet coil when compressor cycles off with continuous fan operation. Equation-fit model uses normalized curves to describe the heat pump performance.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v25.1/io-reference/overview/group-heating-and-cooling-coils/#coilcoolingwatertoairheatpumpequationfit
        """
