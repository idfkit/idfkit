"""Creation signatures of generated classes (stub only).

DO NOT EDIT — regenerate with:
    python -m idfkit.codegen.generate_stubs
"""

from __future__ import annotations

from typing import Any, Literal

class AnyRunPeriod:
    def __call__(
        self,
        name: str = "",
        /,
        *,
        begin_month: int,
        begin_day_of_month: int,
        end_month: int,
        end_day_of_month: int,
        day_of_week_for_start_day: Literal["Friday", "Monday", "Saturday", "Sunday", "Thursday", "Tuesday", "Wednesday"]
        | None = ...,
        use_weather_file_holidays_and_special_days: Literal["", "No", "Yes"] | None = "Yes",
        use_weather_file_daylight_saving_period: Literal["", "No", "Yes"] | None = "Yes",
        apply_weekend_holiday_rule: Literal["", "No", "Yes"] | None = "No",
        use_weather_file_rain_indicators: Literal["", "No", "Yes"] | None = "Yes",
        use_weather_file_snow_indicators: Literal["", "No", "Yes"] | None = "Yes",
    ) -> None: ...

class AnySiteGroundDomainSlab:
    def __call__(
        self,
        name: str,
        /,
        *,
        undisturbed_ground_temperature_model_type: Literal[
            "Site:GroundTemperature:Undisturbed:FiniteDifference",
            "Site:GroundTemperature:Undisturbed:KusudaAchenbach",
            "Site:GroundTemperature:Undisturbed:Xing",
        ],
        undisturbed_ground_temperature_model_name: str,
        slab_boundary_condition_model_name: str,
        slab_location: Literal["InGrade", "OnGrade"],
        ground_domain_depth: float | None = 10,
        aspect_ratio: float | None = 1,
        perimeter_offset: float | None = 5,
        soil_thermal_conductivity: float | None = 1.5,
        soil_density: float | None = 2800,
        soil_specific_heat: float | None = 850,
        soil_moisture_content_volume_fraction: float | None = 30,
        soil_moisture_content_volume_fraction_at_saturation: float | None = 50,
        evapotranspiration_ground_cover_parameter: float | None = 0.4,
        slab_material_name: str | None = ...,
        horizontal_insulation: Literal["", "No", "Yes"] | None = "No",
        horizontal_insulation_material_name: str | None = ...,
        horizontal_insulation_extents: Literal["", "Full", "Perimeter"] | None = "Full",
        perimeter_insulation_width: float | None = ...,
        vertical_insulation: Literal["", "No", "Yes"] | None = "No",
        vertical_insulation_material_name: str | None = ...,
        vertical_insulation_depth: float | None = ...,
        simulation_timestep: Literal["", "Hourly", "Timestep"] | None = "Hourly",
        geometric_mesh_coefficient: float | None = 1.6,
        mesh_density_parameter: int | None = 6,
    ) -> None: ...

class SiteWaterMainsTemperature:
    def __call__(
        self,
        /,
        *,
        calculation_method: Literal["", "Correlation", "CorrelationFromWeatherFile", "Schedule"]
        | None = "CorrelationFromWeatherFile",
        temperature_schedule_name: str | None = ...,
        annual_average_outdoor_air_temperature: float | None = ...,
        maximum_difference_in_monthly_average_outdoor_air_temperatures: float | None = ...,
        temperature_multiplier: float | None = 1,
        temperature_offset: float | None = 0,
    ) -> None: ...

class ScheduleDayInterval:
    def __call__(
        self,
        name: str,
        /,
        *,
        schedule_type_limits_name: str | None = ...,
        interpolate_to_timestep: Literal["", "Average", "Linear", "No"] | None = "No",
        data: list[Any] = ...,
    ) -> None: ...

class WindowMaterialGap:
    def __call__(
        self,
        name: str,
        /,
        *,
        thickness: float,
        gas_or_gas_mixture_: str,
        pressure: float | None = 101325,
        deflection_state: str | None = ...,
        support_pillar: str | None = ...,
        gas_or_gas_mixture: str | None = ...,
    ) -> None: ...

class GlazedDoorInterzone:
    def __call__(
        self,
        name: str,
        /,
        *,
        construction_name: str,
        building_surface_name: str,
        outside_boundary_condition_object: str | None = ...,
        multiplier: float | None = 1,
        starting_x_coordinate: float | None = ...,
        starting_z_coordinate: float | None = ...,
        length: float | None = ...,
        height: float | None = ...,
    ) -> None: ...

class InternalMass:
    def __call__(
        self,
        name: str,
        /,
        *,
        surface_area: float,
        construction_name: str | None = ...,
        zone_or_zonelist_name: str | None = ...,
        space_or_spacelist_name: str | None = ...,
    ) -> None: ...

class GroundHeatTransferSlabMatlProps:
    def __call__(
        self,
        /,
        *,
        rho_slab_material_density: float | None = 2300,
        rho_soil_density: float | None = 1200,
        cp_slab_cp: float | None = 650,
        cp_soil_cp: float | None = 1200,
        tcon_slab_k: float | None = 0.9,
        tcon_soil_k: float | None = 1,
    ) -> None: ...

class GroundHeatTransferSlabYFACE:
    def __call__(self, /) -> None: ...

class AnyRoomAirTemperaturePatternTwoGradient:
    def __call__(
        self,
        /,
        *,
        room_air_temperature_pattern_two_gradient_name: str,
        control_integer_for_pattern_control_schedule_name: int,
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
    ) -> None: ...

class AnyComfortViewFactorAngles:
    def __call__(self, name: str = "", /) -> None: ...

class GasEquipmentInstance:
    def __call__(
        self,
        name: str,
        /,
        *,
        gas_equipment_definition_name: str,
        zone_or_zonelist_or_space_or_spacelist_name: str,
        schedule_name: str,
        multiplier: float | None = 1,
        end_use_subcategory: str | None = "General",
    ) -> None: ...

class AnyIndoorLivingWall:
    def __call__(
        self,
        name: str,
        /,
        *,
        surface_name: str,
        schedule_name: str,
        evapotranspiration_calculation_method: Literal["", "Penman-Monteith", "Stanghellini"]
        | None = "Penman-Monteith",
        lighting_method: Literal["Daylight", "LED", "LED-Daylight"] | None = ...,
        led_intensity_schedule_name: str | None = ...,
        daylighting_control_name: str | None = ...,
        led_daylight_targeted_lighting_intensity_schedule_name: str | None = ...,
        total_leaf_area: float | None = ...,
        led_nominal_intensity: float | None = ...,
        led_nominal_power: float | None = ...,
        radiant_fraction_of_led_lights: float | None = 0.6,
    ) -> None: ...

class DaylightingControls:
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
        number_of_stepped_control_steps: int | None = 1,
        probability_lighting_will_be_reset_when_needed_in_manual_stepped_control: float | None = 1,
        glare_calculation_daylighting_reference_point_name: str | None = ...,
        glare_calculation_azimuth_angle_of_view_direction_clockwise_from_zone_y_axis: float | None = 0,
        maximum_allowable_discomfort_glare_index: float | None = 22,
        delight_gridding_resolution: float | None = ...,
        control_data: list[Any] = ...,
    ) -> None: ...

class AirflowNetworkDistributionComponentConstantPressureDrop:
    def __call__(self, name: str, /, *, pressure_difference_across_the_component: float) -> None: ...

class HVACTemplateThermostat:
    def __call__(
        self,
        name: str,
        /,
        *,
        heating_setpoint_schedule_name: str | None = ...,
        constant_heating_setpoint: float | None = ...,
        cooling_setpoint_schedule_name: str | None = ...,
        constant_cooling_setpoint: float | None = ...,
    ) -> None: ...

class HVACTemplateSystemConstantVolume:
    def __call__(
        self,
        name: str,
        /,
        *,
        system_availability_schedule_name: str | None = ...,
        supply_fan_maximum_flow_rate: float | Literal["", "Autosize"] | None = "Autosize",
        supply_fan_total_efficiency: float | None = 0.7,
        supply_fan_delta_pressure: float | None = 600,
        supply_fan_motor_efficiency: float | None = 0.9,
        supply_fan_motor_in_air_stream_fraction: float | None = 1,
        supply_fan_placement: Literal["", "BlowThrough", "DrawThrough"] | None = "DrawThrough",
        cooling_coil_type: Literal[
            "", "ChilledWater", "ChilledWaterDetailedFlatModel", "HeatExchangerAssistedChilledWater", "None"
        ]
        | None = "ChilledWater",
        cooling_coil_availability_schedule_name: str | None = ...,
        cooling_coil_setpoint_control_type: Literal[
            "", "ControlZone", "FixedSetpoint", "OutdoorAirTemperatureReset", "Scheduled", "Warmest"
        ]
        | None = "FixedSetpoint",
        cooling_coil_control_zone_name: str | None = ...,
        cooling_coil_design_setpoint_temperature: float | None = 12.8,
        cooling_coil_setpoint_schedule_name: str | None = ...,
        cooling_coil_setpoint_at_outdoor_dry_bulb_low: float | None = 15.6,
        cooling_coil_reset_outdoor_dry_bulb_low: float | None = 15.6,
        cooling_coil_setpoint_at_outdoor_dry_bulb_high: float | None = 12.8,
        cooling_coil_reset_outdoor_dry_bulb_high: float | None = 23.3,
        heating_coil_type: Literal["", "Electric", "Gas", "HotWater", "None"] | None = "HotWater",
        heating_coil_availability_schedule_name: str | None = ...,
        heating_coil_setpoint_control_type: Literal[
            "", "ControlZone", "FixedSetpoint", "OutdoorAirTemperatureReset", "Scheduled"
        ]
        | None = "FixedSetpoint",
        heating_coil_control_zone_name: str | None = ...,
        heating_coil_design_setpoint: float | None = 10,
        heating_coil_setpoint_schedule_name: str | None = ...,
        heating_coil_setpoint_at_outdoor_dry_bulb_low: float | None = 15,
        heating_coil_reset_outdoor_dry_bulb_low: float | None = 7.8,
        heating_coil_setpoint_at_outdoor_dry_bulb_high: float | None = 12.2,
        heating_coil_reset_outdoor_dry_bulb_high: float | None = 12.2,
        heating_coil_capacity: float | Literal["", "Autosize"] | None = "Autosize",
        gas_heating_coil_efficiency: float | None = 0.8,
        gas_heating_coil_parasitic_electric_load: float | None = 0,
        preheat_coil_type: Literal["", "Electric", "Gas", "HotWater", "None"] | None = "None",
        preheat_coil_availability_schedule_name: str | None = ...,
        preheat_coil_design_setpoint: float | None = 7.2,
        preheat_coil_setpoint_schedule_name: str | None = ...,
        gas_preheat_coil_efficiency: float | None = 0.8,
        gas_preheat_coil_parasitic_electric_load: float | None = 0,
        maximum_outdoor_air_flow_rate: float | Literal["", "Autosize"] | None = "Autosize",
        minimum_outdoor_air_flow_rate: float | Literal["", "Autosize"] | None = "Autosize",
        minimum_outdoor_air_schedule_name: str | None = ...,
        economizer_type: Literal[
            "",
            "DifferentialDryBulb",
            "DifferentialDryBulbAndEnthalpy",
            "DifferentialEnthalpy",
            "ElectronicEnthalpy",
            "FixedDewPointAndDryBulb",
            "FixedDryBulb",
            "FixedEnthalpy",
            "NoEconomizer",
        ]
        | None = "NoEconomizer",
        economizer_upper_temperature_limit: float | None = ...,
        economizer_lower_temperature_limit: float | None = ...,
        economizer_upper_enthalpy_limit: float | None = ...,
        economizer_maximum_limit_dewpoint_temperature: float | None = ...,
        supply_plenum_name: str | None = ...,
        return_plenum_name: str | None = ...,
        night_cycle_control: Literal["", "CycleOnAny", "CycleOnAnyZoneFansOnly", "CycleOnControlZone", "StayOff"]
        | None = "StayOff",
        night_cycle_control_zone_name: str | None = ...,
        heat_recovery_type: Literal["", "Enthalpy", "None", "Sensible"] | None = "None",
        sensible_heat_recovery_effectiveness: float | None = 0.7,
        latent_heat_recovery_effectiveness: float | None = 0.65,
        heat_recovery_heat_exchanger_type: Literal["", "Plate", "Rotary"] | None = "Plate",
        heat_recovery_frost_control_type: Literal[
            "", "ExhaustAirRecirculation", "ExhaustOnly", "MinimumExhaustTemperature", "None"
        ]
        | None = "None",
        dehumidification_control_type: Literal["", "CoolReheat", "None"] | None = "None",
        dehumidification_control_zone_name: str | None = ...,
        dehumidification_relative_humidity_setpoint: float | None = 60,
        dehumidification_relative_humidity_setpoint_schedule_name: str | None = ...,
        humidifier_type: Literal["", "ElectricSteam", "None"] | None = "None",
        humidifier_availability_schedule_name: str | None = ...,
        humidifier_rated_capacity: float | None = ...,
        humidifier_rated_electric_power: float | Literal["", "Autosize"] | None = "Autosize",
        humidifier_control_zone_name: str | None = ...,
        humidifier_relative_humidity_setpoint: float | None = 30,
        humidifier_relative_humidity_setpoint_schedule_name: str | None = ...,
        return_fan: Literal["", "No", "Yes"] | None = "No",
        return_fan_total_efficiency: float | None = 0.7,
        return_fan_delta_pressure: float | None = 300,
        return_fan_motor_efficiency: float | None = 0.9,
        return_fan_motor_in_air_stream_fraction: float | None = 1,
    ) -> None: ...

class ThermostatSetpointThermalComfortFangerDualSetpoint:
    def __call__(
        self,
        name: str,
        /,
        *,
        fanger_thermal_comfort_heating_schedule_name: str,
        fanger_thermal_comfort_cooling_schedule_name: str,
    ) -> None: ...

class FanConstantVolume:
    def __call__(
        self,
        name: str,
        /,
        *,
        pressure_rise: float,
        air_inlet_node_name: str,
        air_outlet_node_name: str,
        availability_schedule_name: str | None = ...,
        fan_total_efficiency: float | None = 0.7,
        maximum_flow_rate: float | Literal["Autosize"] | None = ...,
        motor_efficiency: float | None = 0.9,
        motor_in_airstream_fraction: float | None = 1,
        end_use_subcategory: str | None = "General",
    ) -> None: ...

class AnyAirLoopHVACUnitaryFurnaceHeatCool:
    def __call__(
        self,
        name: str,
        /,
        *,
        furnace_air_inlet_node_name: str,
        furnace_air_outlet_node_name: str,
        cooling_supply_air_flow_rate: float | Literal["Autosize"],
        heating_supply_air_flow_rate: float | Literal["Autosize"],
        controlling_zone_or_thermostat_location: str,
        supply_fan_object_type: Literal["Fan:ConstantVolume", "Fan:OnOff"],
        supply_fan_name: str,
        heating_coil_object_type: Literal[
            "Coil:Heating:Electric", "Coil:Heating:Fuel", "Coil:Heating:Steam", "Coil:Heating:Water"
        ],
        heating_coil_name: str,
        cooling_coil_object_type: Literal["Coil:Cooling:DX:SingleSpeed", "CoilSystem:Cooling:DX:HeatExchangerAssisted"],
        cooling_coil_name: str,
        availability_schedule_name: str | None = ...,
        supply_air_fan_operating_mode_schedule_name: str | None = ...,
        maximum_supply_air_temperature: float | Literal["", "Autosize"] | None = 80,
        no_load_supply_air_flow_rate: float | Literal["Autosize"] | None = ...,
        fan_placement: Literal["", "BlowThrough", "DrawThrough"] | None = "BlowThrough",
        dehumidification_control_type: Literal["", "CoolReheat", "Multimode", "None"] | None = "None",
        reheat_coil_object_type: Literal[
            "Coil:Heating:Desuperheater",
            "Coil:Heating:Electric",
            "Coil:Heating:Fuel",
            "Coil:Heating:Steam",
            "Coil:Heating:Water",
        ]
        | None = ...,
        reheat_coil_name: str | None = ...,
    ) -> None: ...

class PipeUnderground:
    def __call__(
        self,
        name: str,
        /,
        *,
        construction_name: str,
        fluid_inlet_node_name: str,
        fluid_outlet_node_name: str,
        sun_exposure: Literal["NoSun", "SunExposed"],
        soil_material_name: str,
        undisturbed_ground_temperature_model_type: Literal[
            "Site:GroundTemperature:Undisturbed:FiniteDifference",
            "Site:GroundTemperature:Undisturbed:KusudaAchenbach",
            "Site:GroundTemperature:Undisturbed:Xing",
        ],
        undisturbed_ground_temperature_model_name: str,
        pipe_inside_diameter: float | None = ...,
        pipe_length: float | None = ...,
    ) -> None: ...

class AnyPumpConstantSpeed:
    def __call__(
        self,
        name: str,
        /,
        *,
        inlet_node_name: str,
        outlet_node_name: str,
        design_flow_rate: float | Literal["Autosize"] | None = ...,
        design_pump_head: float | None = 179352,
        design_power_consumption: float | Literal["Autosize"] | None = ...,
        motor_efficiency: float | None = 0.9,
        fraction_of_motor_inefficiencies_to_fluid_stream: float | None = 0,
        pump_control_type: Literal["", "Continuous", "Intermittent"] | None = "Continuous",
        pump_flow_rate_schedule_name: str | None = ...,
        pump_curve_name: str | None = ...,
        impeller_diameter: float | None = ...,
        rotational_speed: float | None = ...,
        zone_name: str | None = ...,
        skin_loss_radiative_fraction: float | None = ...,
        design_power_sizing_method: Literal["", "PowerPerFlow", "PowerPerFlowPerPressure"]
        | None = "PowerPerFlowPerPressure",
        design_electric_power_per_unit_flow_rate: float | None = 348701.1,
        design_shaft_power_per_unit_flow_rate_per_unit_head: float | None = 1.282051282,
    ) -> None: ...

class AnyHeatPumpPlantLoopEIRHeating:
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
        reference_coefficient_of_performance: float | None = ...,
        sizing_factor: float | None = 1,
    ) -> None: ...

class ExternalInterfaceVariable:
    def __call__(self, name: str, /, *, initial_value: float) -> None: ...

class AvailabilityManagerNightVentilation:
    def __call__(
        self,
        name: str,
        /,
        *,
        applicability_schedule_name: str,
        fan_schedule_name: str,
        control_zone_name: str,
        ventilation_temperature_schedule_name: str | None = ...,
        ventilation_temperature_difference: float | None = 2,
        ventilation_temperature_low_limit: float | None = 15,
        night_venting_flow_fraction: float | None = 1,
    ) -> None: ...

class SetpointManagerSystemNodeResetHumidity:
    def __call__(
        self,
        name: str,
        /,
        *,
        control_variable: Literal["HumidityRatio", "MaximumHumidityRatio", "MinimumHumidityRatio"],
        setpoint_at_low_reference_humidity_ratio: float,
        setpoint_at_high_reference_humidity_ratio: float,
        low_reference_humidity_ratio: float,
        high_reference_humidity_ratio: float,
        reference_node_name: str,
        setpoint_node_or_nodelist_name: str,
    ) -> None: ...

class UtilityCostRatchet:
    def __call__(
        self,
        name: str,
        /,
        *,
        tariff_name: str,
        baseline_source_variable: str,
        adjustment_source_variable: str,
        season_from: Literal["Annual", "Fall", "Monthly", "Spring", "Summer", "Winter"] | None = ...,
        season_to: Literal["Annual", "Fall", "Spring", "Summer", "Winter"] | None = ...,
        multiplier_value_or_variable_name: float | str | None = ...,
        offset_value_or_variable_name: float | str | None = ...,
    ) -> None: ...

class OutputConstructions:
    def __call__(
        self,
        /,
        *,
        details_type_1: Literal["Constructions", "Materials"] | None = ...,
        details_type_2: Literal["Constructions", "Materials"] | None = ...,
    ) -> None: ...

class OutputControlSurfaceColorScheme:
    def __call__(
        self,
        name: str,
        /,
        *,
        drawing_element_1_type: Literal[
            "AttachedBuildingShades",
            "DaylightReferencePoint1",
            "DaylightReferencePoint2",
            "DetachedBuildingShades",
            "DetachedFixedShades",
            "Doors",
            "Floors",
            "GlassDoors",
            "Photovoltaics",
            "Roofs",
            "Text",
            "TubularDaylightDiffusers",
            "TubularDaylightDomes",
            "Walls",
            "Windows",
        ]
        | None = ...,
        color_for_drawing_element_1: int | None = ...,
        drawing_element_2_type: Literal[
            "AttachedBuildingShades",
            "DaylightReferencePoint1",
            "DaylightReferencePoint2",
            "DetachedBuildingShades",
            "DetachedFixedShades",
            "Doors",
            "Floors",
            "GlassDoors",
            "Photovoltaics",
            "Roofs",
            "Text",
            "TubularDaylightDiffusers",
            "TubularDaylightDomes",
            "Walls",
            "Windows",
        ]
        | None = ...,
        color_for_drawing_element_2: int | None = ...,
        drawing_element_3_type: Literal[
            "AttachedBuildingShades",
            "DaylightReferencePoint1",
            "DaylightReferencePoint2",
            "DetachedBuildingShades",
            "DetachedFixedShades",
            "Doors",
            "Floors",
            "GlassDoors",
            "Photovoltaics",
            "Roofs",
            "Text",
            "TubularDaylightDiffusers",
            "TubularDaylightDomes",
            "Walls",
            "Windows",
        ]
        | None = ...,
        color_for_drawing_element_3: int | None = ...,
        drawing_element_4_type: Literal[
            "AttachedBuildingShades",
            "DaylightReferencePoint1",
            "DaylightReferencePoint2",
            "DetachedBuildingShades",
            "DetachedFixedShades",
            "Doors",
            "Floors",
            "GlassDoors",
            "Photovoltaics",
            "Roofs",
            "Text",
            "TubularDaylightDiffusers",
            "TubularDaylightDomes",
            "Walls",
            "Windows",
        ]
        | None = ...,
        color_for_drawing_element_4: int | None = ...,
        drawing_element_5_type: Literal[
            "AttachedBuildingShades",
            "DaylightReferencePoint1",
            "DaylightReferencePoint2",
            "DetachedBuildingShades",
            "DetachedFixedShades",
            "Doors",
            "Floors",
            "GlassDoors",
            "Photovoltaics",
            "Roofs",
            "Text",
            "TubularDaylightDiffusers",
            "TubularDaylightDomes",
            "Walls",
            "Windows",
        ]
        | None = ...,
        color_for_drawing_element_5: int | None = ...,
        drawing_element_6_type: Literal[
            "AttachedBuildingShades",
            "DaylightReferencePoint1",
            "DaylightReferencePoint2",
            "DetachedBuildingShades",
            "DetachedFixedShades",
            "Doors",
            "Floors",
            "GlassDoors",
            "Photovoltaics",
            "Roofs",
            "Text",
            "TubularDaylightDiffusers",
            "TubularDaylightDomes",
            "Walls",
            "Windows",
        ]
        | None = ...,
        color_for_drawing_element_6: int | None = ...,
        drawing_element_7_type: Literal[
            "AttachedBuildingShades",
            "DaylightReferencePoint1",
            "DaylightReferencePoint2",
            "DetachedBuildingShades",
            "DetachedFixedShades",
            "Doors",
            "Floors",
            "GlassDoors",
            "Photovoltaics",
            "Roofs",
            "Text",
            "TubularDaylightDiffusers",
            "TubularDaylightDomes",
            "Walls",
            "Windows",
        ]
        | None = ...,
        color_for_drawing_element_7: int | None = ...,
        drawing_element_8_type: Literal[
            "AttachedBuildingShades",
            "DaylightReferencePoint1",
            "DaylightReferencePoint2",
            "DetachedBuildingShades",
            "DetachedFixedShades",
            "Doors",
            "Floors",
            "GlassDoors",
            "Photovoltaics",
            "Roofs",
            "Text",
            "TubularDaylightDiffusers",
            "TubularDaylightDomes",
            "Walls",
            "Windows",
        ]
        | None = ...,
        color_for_drawing_element_8: int | None = ...,
        drawing_element_9_type: Literal[
            "AttachedBuildingShades",
            "DaylightReferencePoint1",
            "DaylightReferencePoint2",
            "DetachedBuildingShades",
            "DetachedFixedShades",
            "Doors",
            "Floors",
            "GlassDoors",
            "Photovoltaics",
            "Roofs",
            "Text",
            "TubularDaylightDiffusers",
            "TubularDaylightDomes",
            "Walls",
            "Windows",
        ]
        | None = ...,
        color_for_drawing_element_9: int | None = ...,
        drawing_element_10_type: Literal[
            "AttachedBuildingShades",
            "DaylightReferencePoint1",
            "DaylightReferencePoint2",
            "DetachedBuildingShades",
            "DetachedFixedShades",
            "Doors",
            "Floors",
            "GlassDoors",
            "Photovoltaics",
            "Roofs",
            "Text",
            "TubularDaylightDiffusers",
            "TubularDaylightDomes",
            "Walls",
            "Windows",
        ]
        | None = ...,
        color_for_drawing_element_10: int | None = ...,
        drawing_element_11_type: Literal[
            "AttachedBuildingShades",
            "DaylightReferencePoint1",
            "DaylightReferencePoint2",
            "DetachedBuildingShades",
            "DetachedFixedShades",
            "Doors",
            "Floors",
            "GlassDoors",
            "Photovoltaics",
            "Roofs",
            "Text",
            "TubularDaylightDiffusers",
            "TubularDaylightDomes",
            "Walls",
            "Windows",
        ]
        | None = ...,
        color_for_drawing_element_11: int | None = ...,
        drawing_element_12_type: Literal[
            "AttachedBuildingShades",
            "DaylightReferencePoint1",
            "DaylightReferencePoint2",
            "DetachedBuildingShades",
            "DetachedFixedShades",
            "Doors",
            "Floors",
            "GlassDoors",
            "Photovoltaics",
            "Roofs",
            "Text",
            "TubularDaylightDiffusers",
            "TubularDaylightDomes",
            "Walls",
            "Windows",
        ]
        | None = ...,
        color_for_drawing_element_12: int | None = ...,
        drawing_element_13_type: Literal[
            "AttachedBuildingShades",
            "DaylightReferencePoint1",
            "DaylightReferencePoint2",
            "DetachedBuildingShades",
            "DetachedFixedShades",
            "Doors",
            "Floors",
            "GlassDoors",
            "Photovoltaics",
            "Roofs",
            "Text",
            "TubularDaylightDiffusers",
            "TubularDaylightDomes",
            "Walls",
            "Windows",
        ]
        | None = ...,
        color_for_drawing_element_13: int | None = ...,
        drawing_element_14_type: Literal[
            "AttachedBuildingShades",
            "DaylightReferencePoint1",
            "DaylightReferencePoint2",
            "DetachedBuildingShades",
            "DetachedFixedShades",
            "Doors",
            "Floors",
            "GlassDoors",
            "Photovoltaics",
            "Roofs",
            "Text",
            "TubularDaylightDiffusers",
            "TubularDaylightDomes",
            "Walls",
            "Windows",
        ]
        | None = ...,
        color_for_drawing_element_14: int | None = ...,
        drawing_element_15_type: Literal[
            "AttachedBuildingShades",
            "DaylightReferencePoint1",
            "DaylightReferencePoint2",
            "DetachedBuildingShades",
            "DetachedFixedShades",
            "Doors",
            "Floors",
            "GlassDoors",
            "Photovoltaics",
            "Roofs",
            "Text",
            "TubularDaylightDiffusers",
            "TubularDaylightDomes",
            "Walls",
            "Windows",
        ]
        | None = ...,
        color_for_drawing_element_15: int | None = ...,
    ) -> None: ...

class AnyOutputMeter:
    def __call__(
        self,
        /,
        *,
        key_name: str,
        reporting_frequency: Literal[
            "", "Annual", "Daily", "Detailed", "Environment", "Hourly", "Monthly", "RunPeriod", "Timestep"
        ]
        | None = "Hourly",
    ) -> None: ...

class OutputEnvironmentalImpactFactors:
    def __call__(
        self,
        /,
        *,
        reporting_frequency: Literal["Annual", "Daily", "Environment", "Hourly", "Monthly", "RunPeriod", "Timestep"]
        | None = ...,
    ) -> None: ...
