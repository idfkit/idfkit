"""Creation signatures of generated classes (stub only).

DO NOT EDIT — regenerate with:
    python -m idfkit.codegen.generate_stubs
"""

from __future__ import annotations

from typing import Literal

from .. import versioned as _vd

class ScheduleFile_v8_9_to_v9_1:
    def __call__(
        self,
        name: str,
        /,
        *,
        file_name: str,
        column_number: float,
        rows_to_skip_at_top: float,
        schedule_type_limits_name: str | None = ...,
        number_of_hours_of_data: float | None = 8760,
        column_separator: Literal["", "Comma", "Fixed", "Semicolon", "Tab"] | None = "Comma",
        interpolate_to_timestep: Literal["", "No", "Yes"] | None = "No",
        minutes_per_item: float | None = ...,
    ) -> None:
        """Create a new ``Schedule:File`` and add it to the document.

        A Schedule:File points to a text computer file that has 8760-8784 hours of data.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v9.1/io-reference/overview/group-schedules/#schedulefile
        """

class DaylightingControls_v9_6_to_v22_1:
    def __call__(
        self,
        name: str,
        /,
        *,
        zone_or_space_name: str,
        daylighting_method: Literal["", "DElight", "SplitFlux"] | None = "SplitFlux",
        availability_schedule_name: str | None = ...,
        lighting_control_type: Literal["", "Continuous", "ContinuousOff", "Stepped"] | None = "Continuous",
        minimum_input_power_fraction_for_continuous_or_continuousoff_dimming_control: float | None = 0.3,
        minimum_light_output_fraction_for_continuous_or_continuousoff_dimming_control: float | None = 0.2,
        number_of_stepped_control_steps: float | None = 1,
        probability_lighting_will_be_reset_when_needed_in_manual_stepped_control: float | None = 1,
        glare_calculation_daylighting_reference_point_name: str | None = ...,
        glare_calculation_azimuth_angle_of_view_direction_clockwise_from_zone_y_axis: float | None = 0,
        maximum_allowable_discomfort_glare_index: float | None = 22,
        delight_gridding_resolution: float | None = ...,
        control_data: list[_vd.DaylightingControlsControlDataItem_v9_6_to_v22_1] = ...,
    ) -> None:
        """Create a new ``Daylighting:Controls`` and add it to the document.

        Dimming of overhead electric lighting is determined from each reference point. Glare from daylighting is also calculated.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v22.1/io-reference/energyplus-economics/cost-estimating/#daylightingcontrols
        """

class Zone_v9_5_to_v22_1:
    def __call__(
        self,
        name: str,
        /,
        *,
        direction_of_relative_north: float | None = 0,
        x_origin: float | None = 0,
        y_origin: float | None = 0,
        z_origin: float | None = 0,
        type: float | None = 1,
        multiplier: float | None = 1,
        ceiling_height: float | Literal["", "Autocalculate"] | None = "Autocalculate",
        volume: float | Literal["", "Autocalculate"] | None = "Autocalculate",
        floor_area: float | Literal["", "Autocalculate"] | None = "Autocalculate",
        zone_inside_convection_algorithm: Literal[
            "", "ASTMC1340", "AdaptiveConvectionAlgorithm", "CeilingDiffuser", "Simple", "TARP", "TrombeWall"
        ]
        | None = ...,
        zone_outside_convection_algorithm: Literal[
            "", "AdaptiveConvectionAlgorithm", "DOE-2", "MoWiTT", "SimpleCombined", "TARP"
        ]
        | None = ...,
        part_of_total_floor_area: Literal["", "No", "Yes"] | None = "Yes",
    ) -> None:
        """Create a new ``Zone`` and add it to the document.

        Defines a thermal zone of the building. Every zone contains one or more Spaces. Space is an optional input. If a Zone has no Space(s) specified in input then a default Space named <Zone Name> will be created. If some surfaces in a Zone are assigned to a space and some are not, then a default Space named <Zone Name>-Remainder will be created. Input references to Space Names must have a matching Space object (default space names may not be referenced except in output variable keys).

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v22.1/io-reference/overview/group-thermal-zone-description-geometry/#zone
        """

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
    ) -> None:
        """Create a new ``CoilSystem:IntegratedHeatPump:AirSource`` and add it to the document.

        This object is used for air-source integrated heat pump, a collection of its working modes.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v22.1/io-reference/overview/group-heating-and-cooling-coils/#coilsystemintegratedheatpumpairsource
        """

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
    ) -> None:
        """Create a new ``Wall:Interzone`` and add it to the document.

        Allows for simplified entry of interzone walls (walls between zones).

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v9.5/io-reference/overview/group-thermal-zone-description-geometry/#wallinterzone
        """

class HVACTemplateZoneFanCoil_v8_9:
    def __call__(
        self,
        /,
        *,
        zone_name: str,
        template_thermostat_name: str | None = ...,
        supply_air_maximum_flow_rate: float | Literal["", "Autosize"] | None = "Autosize",
        zone_heating_sizing_factor: float | None = ...,
        zone_cooling_sizing_factor: float | None = ...,
        outdoor_air_method: Literal[
            "", "DetailedSpecification", "Flow/Area", "Flow/Person", "Flow/Zone", "Maximum", "Sum"
        ]
        | None = "Flow/Person",
        outdoor_air_flow_rate_per_person: float | None = 0.00944,
        outdoor_air_flow_rate_per_zone_floor_area: float | None = 0,
        outdoor_air_flow_rate_per_zone: float | None = 0,
        system_availability_schedule_name: str | None = ...,
        supply_fan_total_efficiency: float | None = 0.7,
        supply_fan_delta_pressure: float | None = 75,
        supply_fan_motor_efficiency: float | None = 0.9,
        supply_fan_motor_in_air_stream_fraction: float | None = 1,
        cooling_coil_type: Literal["", "ChilledWater", "ChilledWaterDetailedFlatModel"] | None = "ChilledWater",
        cooling_coil_availability_schedule_name: str | None = ...,
        cooling_coil_design_setpoint: float | None = 14,
        heating_coil_type: Literal["", "HotWater"] | None = "HotWater",
        heating_coil_availability_schedule_name: str | None = ...,
        heating_coil_design_setpoint: float | None = 50,
        dedicated_outdoor_air_system_name: str | None = ...,
        zone_cooling_design_supply_air_temperature_input_method: Literal[
            "", "SupplyAirTemperature", "TemperatureDifference"
        ]
        | None = "SupplyAirTemperature",
        zone_cooling_design_supply_air_temperature_difference: float | None = 11.11,
        zone_heating_design_supply_air_temperature_input_method: Literal[
            "", "SupplyAirTemperature", "TemperatureDifference"
        ]
        | None = "SupplyAirTemperature",
        zone_heating_design_supply_air_temperature_difference: float | None = 30,
        design_specification_outdoor_air_object_name: str | None = ...,
        design_specification_zone_air_distribution_object_name: str | None = ...,
        capacity_control_method: Literal[
            "ConstantFanVariableFlow", "CyclingFan", "VariableFanConstantFlow", "VariableFanVariableFlow"
        ]
        | None = ...,
        low_speed_supply_air_flow_ratio: float | None = 0.33,
        medium_speed_supply_air_flow_ratio: float | None = 0.66,
        outdoor_air_schedule_name: str | None = ...,
        baseboard_heating_type: Literal["", "Electric", "HotWater", "None"] | None = "None",
        baseboard_heating_availability_schedule_name: str | None = ...,
        baseboard_heating_capacity: float | Literal["", "Autosize"] | None = "Autosize",
    ) -> None:
        """Create a new ``HVACTemplate:Zone:FanCoil`` and add it to the document.

        4 pipe fan coil unit with optional outdoor air.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v8.9/io-reference/hvac-template-objects/group-hvac-templates/#hvactemplatezonefancoil
        """

class ElectricLoadCenterStorageBattery_v8_9_to_v22_1:
    def __call__(
        self,
        name: str,
        /,
        *,
        availability_schedule_name: str | None = ...,
        zone_name: str | None = ...,
        radiative_fraction: float | None = 0,
        number_of_battery_modules_in_parallel: float | None = 1,
        number_of_battery_modules_in_series: float | None = 1,
        maximum_module_capacity: float | None = ...,
        initial_fractional_state_of_charge: float | None = 1,
        fraction_of_available_charge_capacity: float | None = ...,
        change_rate_from_bound_charge_to_available_charge: float | None = ...,
        fully_charged_module_open_circuit_voltage: float | None = ...,
        fully_discharged_module_open_circuit_voltage: float | None = ...,
        voltage_change_curve_name_for_charging: str | None = ...,
        voltage_change_curve_name_for_discharging: str | None = ...,
        module_internal_electrical_resistance: float | None = ...,
        maximum_module_discharging_current: float | None = ...,
        module_cut_off_voltage: float | None = ...,
        module_charge_rate_limit: float | None = 1,
        battery_life_calculation: Literal["", "No", "Yes"] | None = "No",
        number_of_cycle_bins: float | None = 10,
        battery_life_curve_name: str | None = ...,
    ) -> None:
        """Create a new ``ElectricLoadCenter:Storage:Battery`` and add it to the document.

        Uses the kinetic battery model (KiBaM) to simulate rechargeable battery banks in an electrical load center. The battery bank is a collection of one or more individual battery modules. Given the surplus or deficit power from the electrical system and the state of charge from the previous time step, this object can model the voltage, current, and energy losses with charging and discharging during each time step. The cumulative battery damage can be also modeled and reported at the end of each simulation run.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v22.1/io-reference/overview/group-electric-load-center-generator/#electricloadcenterstoragebattery
        """

class CoilWaterHeatingAirToWaterHeatPumpPumped_v23_2_to_v25_1:
    def __call__(
        self,
        name: str,
        /,
        *,
        rated_heating_capacity: float,
        evaporator_air_inlet_node_name: str,
        evaporator_air_outlet_node_name: str,
        condenser_water_inlet_node_name: str,
        condenser_water_outlet_node_name: str,
        rated_cop: float | None = 3.2,
        rated_sensible_heat_ratio: float | None = 0.85,
        rated_evaporator_inlet_air_dry_bulb_temperature: float | None = 19.7,
        rated_evaporator_inlet_air_wet_bulb_temperature: float | None = 13.5,
        rated_condenser_inlet_water_temperature: float | None = 57.5,
        rated_evaporator_air_flow_rate: float | Literal["Autocalculate"] | None = ...,
        rated_condenser_water_flow_rate: float | Literal["Autocalculate"] | None = ...,
        evaporator_fan_power_included_in_rated_cop: Literal["", "No", "Yes"] | None = "Yes",
        condenser_pump_power_included_in_rated_cop: Literal["", "No", "Yes"] | None = "No",
        condenser_pump_heat_included_in_rated_heating_capacity_and_rated_cop: Literal["", "No", "Yes"] | None = "No",
        condenser_water_pump_power: float | None = 0,
        fraction_of_condenser_pump_heat_to_water: float | None = 0.2,
        crankcase_heater_capacity: float | None = 0,
        crankcase_heater_capacity_function_of_temperature_curve_name: str | None = ...,
        maximum_ambient_temperature_for_crankcase_heater_operation: float | None = 10,
        evaporator_air_temperature_type_for_curve_objects: Literal["", "DryBulbTemperature", "WetBulbTemperature"]
        | None = "WetBulbTemperature",
        heating_capacity_function_of_temperature_curve_name: str | None = ...,
        heating_capacity_function_of_air_flow_fraction_curve_name: str | None = ...,
        heating_capacity_function_of_water_flow_fraction_curve_name: str | None = ...,
        heating_cop_function_of_temperature_curve_name: str | None = ...,
        heating_cop_function_of_air_flow_fraction_curve_name: str | None = ...,
        heating_cop_function_of_water_flow_fraction_curve_name: str | None = ...,
        part_load_fraction_correlation_curve_name: str | None = ...,
    ) -> None:
        """Create a new ``Coil:WaterHeating:AirToWaterHeatPump:Pumped`` and add it to the document.

        Heat pump water heater (HPWH) heating coil, air-to-water direct-expansion (DX) system which includes a water heating coil, evaporator air coil, evaporator fan, electric compressor, and water pump. Part of a WaterHeater:HeatPump:PumpedCondenser system.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v25.1/io-reference/overview/group-heating-and-cooling-coils/#coilwaterheatingairtowaterheatpumppumped
        """

class ZoneBaseboardOutdoorTemperatureControlled_v8_9_to_v9_5:
    def __call__(
        self,
        name: str,
        /,
        *,
        zone_name: str,
        schedule_name: str,
        capacity_at_low_temperature: float,
        low_temperature: float,
        capacity_at_high_temperature: float,
        high_temperature: float,
        fraction_radiant: float | None = 0,
        end_use_subcategory: str | None = "General",
    ) -> None:
        """Create a new ``ZoneBaseboard:OutdoorTemperatureControlled`` and add it to the document.

        Specifies outside temperature-controlled electric baseboard heating.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v9.5/io-reference/overview/group-internal-gains-people-lights-other/#zonebaseboardoutdoortemperaturecontrolled
        """

class HeatPumpPlantLoopEIRHeating_v9_3_to_v23_1:
    def __call__(
        self,
        name: str,
        /,
        *,
        load_side_inlet_node_name: str,
        load_side_outlet_node_name: str,
        source_side_inlet_node_name: str,
        source_side_outlet_node_name: str,
        capacity_modifier_function_of_temperature_curve_name: str,
        electric_input_to_output_ratio_modifier_function_of_temperature_curve_name: str,
        electric_input_to_output_ratio_modifier_function_of_part_load_ratio_curve_name: str,
        condenser_type: Literal["", "AirSource", "WaterSource"] | None = "WaterSource",
        companion_heat_pump_name: str | None = ...,
        load_side_reference_flow_rate: float | Literal["", "Autosize"] | None = "Autosize",
        source_side_reference_flow_rate: float | Literal["", "Autosize"] | None = "Autosize",
        reference_capacity: float | Literal["", "Autosize"] | None = "Autosize",
        reference_coefficient_of_performance: float | None = 7.5,
        sizing_factor: float | None = 1,
    ) -> None:
        """Create a new ``HeatPump:PlantLoop:EIR:Heating`` and add it to the document.

        An EIR formulated water to water heat pump model, heating operation

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v23.1/io-reference/overview/group-plant-equipment/#heatpumpplantloopeirheating
        """
