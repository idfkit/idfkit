"""Creation signatures of generated classes (stub only).

DO NOT EDIT — regenerate with:
    python -m idfkit.codegen.generate_stubs
"""

from __future__ import annotations

from typing import Any, Literal

class RunPeriodControlDaylightSavingTime:
    def __call__(self, /, *, start_date: str, end_date: str) -> None: ...

class ScheduleFile:
    def __call__(
        self,
        name: str,
        /,
        *,
        file_name: str,
        column_number: int,
        rows_to_skip_at_top: int,
        schedule_type_limits_name: str | None = ...,
        number_of_hours_of_data: float | None = 8760,
        column_separator: Literal["", "Comma", "Semicolon", "Space", "Tab"] | None = "Comma",
        interpolate_to_timestep: Literal["", "No", "Yes"] | None = "No",
        minutes_per_item: int | None = 60,
        adjust_schedule_for_daylight_savings: Literal["", "No", "Yes"] | None = "Yes",
    ) -> None: ...

class WindowMaterialGlazingGroupThermochromic:
    def __call__(self, name: str, /, *, temperature_data: list[Any] = ...) -> None: ...

class WindowMaterialBlindEquivalentLayer:
    def __call__(
        self,
        name: str,
        /,
        *,
        slat_width: float,
        slat_separation: float,
        front_side_slat_beam_diffuse_solar_reflectance: float,
        back_side_slat_beam_diffuse_solar_reflectance: float,
        front_side_slat_diffuse_diffuse_solar_reflectance: float,
        back_side_slat_diffuse_diffuse_solar_reflectance: float,
        slat_orientation: Literal["", "Horizontal", "Vertical"] | None = "Horizontal",
        slat_crown: float | None = 0.0015,
        slat_angle: float | None = 45,
        front_side_slat_beam_diffuse_solar_transmittance: float | None = 0,
        back_side_slat_beam_diffuse_solar_transmittance: float | None = 0,
        front_side_slat_beam_diffuse_visible_transmittance: float | None = 0,
        back_side_slat_beam_diffuse_visible_transmittance: float | None = 0,
        front_side_slat_beam_diffuse_visible_reflectance: float | None = ...,
        back_side_slat_beam_diffuse_visible_reflectance: float | None = ...,
        slat_diffuse_diffuse_solar_transmittance: float | None = 0,
        slat_diffuse_diffuse_visible_transmittance: float | None = ...,
        front_side_slat_diffuse_diffuse_visible_reflectance: float | None = ...,
        back_side_slat_diffuse_diffuse_visible_reflectance: float | None = ...,
        slat_infrared_transmittance: float | None = 0,
        front_side_slat_infrared_emissivity: float | None = 0.9,
        back_side_slat_infrared_emissivity: float | None = 0.9,
        slat_angle_control: Literal["", "BlockBeamSolar", "FixedSlatAngle", "MaximizeSolar"] | None = "FixedSlatAngle",
    ) -> None: ...

class MaterialPropertyHeatAndMoistureTransferSorptionIsotherm:
    def __call__(
        self,
        /,
        *,
        material_name: str,
        number_of_isotherm_coordinates: int,
        relative_humidity_fraction_1: float,
        moisture_content_1: float,
        relative_humidity_fraction_2: float | None = ...,
        moisture_content_2: float | None = ...,
        relative_humidity_fraction_3: float | None = ...,
        moisture_content_3: float | None = ...,
        relative_humidity_fraction_4: float | None = ...,
        moisture_content_4: float | None = ...,
        relative_humidity_fraction_5: float | None = ...,
        moisture_content_5: float | None = ...,
        relative_humidity_fraction_6: float | None = ...,
        moisture_content_6: float | None = ...,
        relative_humidity_fraction_7: float | None = ...,
        moisture_content_7: float | None = ...,
        relative_humidity_fraction_8: float | None = ...,
        moisture_content_8: float | None = ...,
        relative_humidity_fraction_9: float | None = ...,
        moisture_content_9: float | None = ...,
        relative_humidity_fraction_10: float | None = ...,
        moisture_content_10: float | None = ...,
        relative_humidity_fraction_11: float | None = ...,
        moisture_content_11: float | None = ...,
        relative_humidity_fraction_12: float | None = ...,
        moisture_content_12: float | None = ...,
        relative_humidity_fraction_13: float | None = ...,
        moisture_content_13: float | None = ...,
        relative_humidity_fraction_14: float | None = ...,
        moisture_content_14: float | None = ...,
        relative_humidity_fraction_15: float | None = ...,
        moisture_content_15: float | None = ...,
        relative_humidity_fraction_16: float | None = ...,
        moisture_content_16: float | None = ...,
        relative_humidity_fraction_17: float | None = ...,
        moisture_content_17: float | None = ...,
        relative_humidity_fraction_18: float | None = ...,
        moisture_content_18: float | None = ...,
        relative_humidity_fraction_19: float | None = ...,
        moisture_content_19: float | None = ...,
        relative_humidity_fraction_20: float | None = ...,
        moisture_content_20: float | None = ...,
        relative_humidity_fraction_21: float | None = ...,
        moisture_content_21: float | None = ...,
        relative_humidity_fraction_22: float | None = ...,
        moisture_content_22: float | None = ...,
        relative_humidity_fraction_23: float | None = ...,
        moisture_content_23: float | None = ...,
        relative_humidity_fraction_24: float | None = ...,
        moisture_content_24: float | None = ...,
        relative_humidity_fraction_25: float | None = ...,
        moisture_content_25: float | None = ...,
    ) -> None: ...

class ConstructionCfactorUndergroundWall:
    def __call__(self, name: str, /, *, c_factor: float, height: float) -> None: ...

class ZoneList:
    def __call__(self, name: str, /, *, zones: list[Any] = ...) -> None: ...

class SurfaceControlMovableInsulation:
    def __call__(
        self,
        /,
        *,
        insulation_type: Literal["Inside", "Outside"],
        surface_name: str,
        material_name: str,
        schedule_name: str,
    ) -> None: ...

class GroundHeatTransferBasementAutoGrid:
    def __call__(
        self,
        /,
        *,
        slabx_x_dimension_of_the_building_slab: float,
        slaby_y_dimension_of_the_building_slab: float,
        clearance_distance_from_outside_of_wall_to_edge_: float | None = 15,
        concagheight_height_of_the_foundation_wall_above_grade: float | None = 0,
        slabdepth_thickness_of_the_floor_slab: float | None = 0.1,
        basedepth_depth_of_the_basement_wall_below_grade: float | None = 2,
        clearance_distance_from_outside_of_wall_to_edge: float | None = ...,
    ) -> None: ...

class ComfortViewFactorAngles:
    def __call__(self, name: str = "", /, *, angles: list[Any] = ...) -> None: ...

class AnyLights:
    def __call__(
        self,
        name: str,
        /,
        *,
        schedule_name: str,
        design_level_calculation_method: Literal["", "LightingLevel", "Watts/Area", "Watts/Person"]
        | None = "LightingLevel",
        lighting_level: float | None = ...,
        watts_per_person: float | None = ...,
        return_air_fraction: float | None = 0,
        fraction_radiant: float | None = 0,
        fraction_visible: float | None = 0,
        fraction_replaceable: float | None = 1,
        end_use_subcategory: str | None = "General",
        return_air_fraction_calculated_from_plenum_temperature: Literal["", "No", "Yes"] | None = "No",
        return_air_fraction_function_of_plenum_temperature_coefficient_1: float | None = 0,
        return_air_fraction_function_of_plenum_temperature_coefficient_2: float | None = 0,
        return_air_heat_gain_node_name: str | None = ...,
    ) -> None: ...

class AnyElectricEquipment:
    def __call__(
        self,
        name: str,
        /,
        *,
        schedule_name: str,
        design_level_calculation_method: Literal["", "EquipmentLevel", "Watts/Area", "Watts/Person"]
        | None = "EquipmentLevel",
        design_level: float | None = ...,
        watts_per_person: float | None = ...,
        fraction_latent: float | None = 0,
        fraction_radiant: float | None = 0,
        fraction_lost: float | None = 0,
        end_use_subcategory: str | None = "General",
    ) -> None: ...

class OtherEquipmentInstance:
    def __call__(
        self,
        name: str,
        /,
        *,
        other_equipment_definition_name: str,
        zone_or_zonelist_or_space_or_spacelist_name: str,
        schedule_name: str,
        fuel_type: Literal[
            "",
            "Coal",
            "Diesel",
            "DistrictCooling",
            "DistrictHeatingSteam",
            "DistrictHeatingWater",
            "Electricity",
            "FuelOilNo1",
            "FuelOilNo2",
            "Gasoline",
            "NaturalGas",
            "None",
            "OtherFuel1",
            "OtherFuel2",
            "Propane",
        ]
        | None = "None",
        multiplier: float | None = 1,
        end_use_subcategory: str | None = "General",
    ) -> None: ...

class IndoorLivingWall:
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

class ElectricEquipmentITEAirCooled:
    def __call__(
        self,
        name: str,
        /,
        *,
        zone_or_space_name: str,
        cpu_power_input_function_of_loading_and_air_temperature_curve_name: str,
        design_fan_air_flow_rate_per_power_input: float,
        air_flow_function_of_loading_and_air_temperature_curve_name: str,
        fan_power_input_function_of_flow_curve_name: str,
        air_flow_calculation_method: Literal["", "FlowControlWithApproachTemperatures", "FlowFromSystem"]
        | None = "FlowFromSystem",
        design_power_input_calculation_method: Literal["", "Watts/Area", "Watts/Unit"] | None = "Watts/Unit",
        watts_per_unit: float | None = ...,
        number_of_units: float | None = 1,
        watts_per_floor_area: float | None = ...,
        design_power_input_schedule_name: str | None = ...,
        cpu_loading_schedule_name: str | None = ...,
        design_fan_power_input_fraction: float | None = 0,
        design_entering_air_temperature: float | None = 15,
        environmental_class: Literal["", "A1", "A2", "A3", "A4", "B", "C", "H1", "None"] | None = "None",
        air_inlet_connection_type: Literal["", "AdjustedSupply", "RoomAirModel", "ZoneAirNode"]
        | None = "AdjustedSupply",
        air_inlet_room_air_model_node_name: str | None = ...,
        air_outlet_room_air_model_node_name: str | None = ...,
        supply_air_node_name: str | None = ...,
        design_recirculation_fraction: float | None = 0,
        recirculation_function_of_loading_and_supply_temperature_curve_name: str | None = ...,
        design_electric_power_supply_efficiency: float | None = 1,
        electric_power_supply_efficiency_function_of_part_load_ratio_curve_name: str | None = ...,
        fraction_of_electric_power_supply_losses_to_zone: float | None = 1,
        cpu_end_use_subcategory: str | None = "ITE-CPU",
        fan_end_use_subcategory: str | None = "ITE-Fans",
        electric_power_supply_end_use_subcategory: str | None = "ITE-UPS",
        supply_temperature_difference: float | None = ...,
        supply_temperature_difference_schedule: str | None = ...,
        return_temperature_difference: float | None = ...,
        return_temperature_difference_schedule: str | None = ...,
    ) -> None: ...

class AnyDaylightingControls:
    def __call__(
        self,
        name: str,
        /,
        *,
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

class HVACTemplatePlantTower:
    def __call__(
        self,
        name: str,
        /,
        *,
        tower_type: Literal["SingleSpeed", "TwoSpeed"],
        high_speed_nominal_capacity: float | Literal["", "Autosize"] | None = "Autosize",
        high_speed_fan_power: float | Literal["", "Autosize"] | None = "Autosize",
        low_speed_nominal_capacity: float | Literal["", "Autosize"] | None = "Autosize",
        low_speed_fan_power: float | Literal["", "Autosize"] | None = "Autosize",
        free_convection_capacity: float | Literal["", "Autosize"] | None = "Autosize",
        priority: str | None = ...,
        sizing_factor: float | None = 1,
        template_plant_loop_type: Literal["ChilledWater", "MixedWater"] | None = ...,
    ) -> None: ...

class DesignSpecificationOutdoorAirSpaceList:
    def __call__(self, name: str, /, *, space_specs: list[Any] = ...) -> None: ...

class ZoneControlThermostat:
    def __call__(
        self,
        name: str,
        /,
        *,
        zone_or_zonelist_name: str,
        control_type_schedule_name: str,
        control_1_object_type: Literal[
            "ThermostatSetpoint:DualSetpoint",
            "ThermostatSetpoint:SingleCooling",
            "ThermostatSetpoint:SingleHeating",
            "ThermostatSetpoint:SingleHeatingOrCooling",
        ],
        control_1_name: str,
        control_2_object_type: Literal[
            "ThermostatSetpoint:DualSetpoint",
            "ThermostatSetpoint:SingleCooling",
            "ThermostatSetpoint:SingleHeating",
            "ThermostatSetpoint:SingleHeatingOrCooling",
        ]
        | None = ...,
        control_2_name: str | None = ...,
        control_3_object_type: Literal[
            "ThermostatSetpoint:DualSetpoint",
            "ThermostatSetpoint:SingleCooling",
            "ThermostatSetpoint:SingleHeating",
            "ThermostatSetpoint:SingleHeatingOrCooling",
        ]
        | None = ...,
        control_3_name: str | None = ...,
        control_4_object_type: Literal[
            "ThermostatSetpoint:DualSetpoint",
            "ThermostatSetpoint:SingleCooling",
            "ThermostatSetpoint:SingleHeating",
            "ThermostatSetpoint:SingleHeatingOrCooling",
        ]
        | None = ...,
        control_4_name: str | None = ...,
        temperature_difference_between_cutout_and_setpoint: float | None = 0,
    ) -> None: ...

class ThermostatSetpointSingleHeatingOrCooling:
    def __call__(self, name: str, /, *, setpoint_temperature_schedule_name: str | None = ...) -> None: ...

class AnyZoneHVACTerminalUnitVariableRefrigerantFlow:
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
        supply_air_fan_object_type: Literal["", "Fan:ConstantVolume", "Fan:OnOff", "Fan:SystemModel"]
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
    ) -> None: ...

class AirTerminalSingleDuctVAVHeatAndCoolReheat:
    def __call__(
        self,
        name: str,
        /,
        *,
        damper_air_outlet_node_name: str,
        air_inlet_node_name: str,
        maximum_air_flow_rate: float | Literal["Autosize"],
        zone_minimum_air_flow_fraction: float,
        reheat_coil_object_type: Literal[
            "Coil:Heating:Electric", "Coil:Heating:Fuel", "Coil:Heating:Steam", "Coil:Heating:Water"
        ],
        reheat_coil_name: str,
        air_outlet_node_name: str,
        availability_schedule_name: str | None = ...,
        maximum_hot_water_or_steam_flow_rate: float | Literal["Autosize"] | None = ...,
        minimum_hot_water_or_steam_flow_rate: float | None = 0,
        convergence_tolerance: float | None = 0.001,
        maximum_reheat_air_temperature: float | None = ...,
        minimum_air_flow_turndown_schedule_name: str | None = ...,
    ) -> None: ...

class AirTerminalSingleDuctParallelPIUReheat:
    def __call__(
        self,
        name: str,
        /,
        *,
        maximum_primary_air_flow_rate: float | Literal["Autosize"],
        maximum_secondary_air_flow_rate: float | Literal["Autosize"],
        minimum_primary_air_flow_fraction: float | Literal["Autosize"],
        fan_on_flow_fraction: float | Literal["Autosize"],
        reheat_coil_object_type: Literal[
            "Coil:Heating:Electric", "Coil:Heating:Fuel", "Coil:Heating:Steam", "Coil:Heating:Water"
        ],
        reheat_coil_name: str,
        availability_schedule_name: str | None = ...,
        supply_air_inlet_node_name: str | None = ...,
        secondary_air_inlet_node_name: str | None = ...,
        outlet_node_name: str | None = ...,
        zone_mixer_name: str | None = ...,
        fan_name: str | None = ...,
        maximum_hot_water_or_steam_flow_rate: float | Literal["Autosize"] | None = ...,
        minimum_hot_water_or_steam_flow_rate: float | None = 0,
        convergence_tolerance: float | None = 0.001,
        fan_control_type: Literal["", "ConstantSpeed", "VariableSpeed"] | None = "ConstantSpeed",
        minimum_fan_turn_down_ratio: float | None = 0.3,
        heating_control_type: Literal["Modulated", "Staged"] | None = ...,
        design_heating_discharge_air_temperature: float | None = 32.1,
        high_limit_heating_discharge_air_temperature: float | None = 37.7,
        backdraft_damper_leakage_fraction_curve_name: str | None = ...,
        backdraft_damper_leakage_zone_name: str | None = ...,
    ) -> None: ...

class FanSystemModel:
    def __call__(
        self,
        name: str,
        /,
        *,
        air_inlet_node_name: str,
        air_outlet_node_name: str,
        design_maximum_air_flow_rate: float | Literal["Autosize"],
        design_pressure_rise: float,
        availability_schedule_name: str | None = ...,
        speed_control_method: Literal["", "Continuous", "Discrete"] | None = "Discrete",
        electric_power_minimum_flow_rate_fraction: float | None = 0.2,
        motor_efficiency: float | None = 0.9,
        motor_in_air_stream_fraction: float | None = 1,
        design_electric_power_consumption: float | Literal["", "Autosize"] | None = "Autosize",
        design_power_sizing_method: Literal["", "PowerPerFlow", "PowerPerFlowPerPressure", "TotalEfficiencyAndPressure"]
        | None = "PowerPerFlowPerPressure",
        electric_power_per_unit_flow_rate: float | None = ...,
        electric_power_per_unit_flow_rate_per_unit_pressure: float | None = 1.66667,
        fan_total_efficiency: float | None = 0.7,
        electric_power_function_of_flow_fraction_curve_name: str | None = ...,
        night_ventilation_mode_pressure_rise: float | None = ...,
        night_ventilation_mode_flow_fraction: float | None = ...,
        motor_loss_zone_name: str | None = ...,
        motor_loss_radiative_fraction: float | None = ...,
        end_use_subcategory: str | None = "General",
        number_of_speeds: int | None = 1,
        speed_fractions: list[Any] = ...,
    ) -> None: ...

class AnyCoilHeatingElectricMultiStage:
    def __call__(
        self,
        name: str,
        /,
        *,
        air_inlet_node_name: str,
        air_outlet_node_name: str,
        number_of_stages: int,
        stage_1_efficiency: float,
        stage_1_nominal_capacity: float | Literal["Autosize"],
        availability_schedule_name: str | None = ...,
        temperature_setpoint_node_name: str | None = ...,
        stage_2_efficiency: float | None = ...,
        stage_2_nominal_capacity: float | Literal["Autosize"] | None = ...,
        stage_3_efficiency: float | None = ...,
        stage_3_nominal_capacity: float | Literal["Autosize"] | None = ...,
        stage_4_efficiency: float | None = ...,
        stage_4_nominal_capacity: float | Literal["Autosize"] | None = ...,
    ) -> None: ...

class AnyCoilCoolingWaterToAirHeatPumpEquationFit:
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
        nominal_time_for_condensate_removal_to_begin: float | None = 0,
        ratio_of_initial_moisture_evaporation_rate_and_steady_state_latent_capacity: float | None = 0,
    ) -> None: ...

class CoilWaterHeatingDesuperheater:
    def __call__(
        self,
        name: str,
        /,
        *,
        setpoint_temperature_schedule_name: str,
        rated_inlet_water_temperature: float,
        rated_outdoor_air_temperature: float,
        maximum_inlet_water_temperature_for_heat_reclaim: float,
        water_inlet_node_name: str,
        water_outlet_node_name: str,
        tank_name: str,
        heating_source_object_type: Literal[
            "Coil:Cooling:DX",
            "Coil:Cooling:DX:MultiSpeed",
            "Coil:Cooling:DX:SingleSpeed",
            "Coil:Cooling:DX:TwoSpeed",
            "Coil:Cooling:DX:TwoStageWithHumidityControlMode",
            "Coil:Cooling:DX:VariableSpeed",
            "Coil:Cooling:WaterToAirHeatPump:EquationFit",
            "Coil:Cooling:WaterToAirHeatPump:VariableSpeedEquationFit",
            "Refrigeration:CompressorRack",
            "Refrigeration:Condenser:AirCooled",
            "Refrigeration:Condenser:EvaporativeCooled",
            "Refrigeration:Condenser:WaterCooled",
        ],
        heating_source_name: str,
        water_flow_rate: float,
        availability_schedule_name: str | None = ...,
        dead_band_temperature_difference: float | None = 5,
        rated_heat_reclaim_recovery_efficiency: float | None = ...,
        heat_reclaim_efficiency_function_of_temperature_curve_name: str | None = ...,
        tank_object_type: Literal["", "WaterHeater:Mixed", "WaterHeater:Stratified"] | None = "WaterHeater:Mixed",
        water_pump_power: float | None = 0,
        fraction_of_pump_heat_to_water: float | None = 0.2,
        on_cycle_parasitic_electric_load: float | None = 0,
        off_cycle_parasitic_electric_load: float | None = 0,
    ) -> None: ...

class AirConditionerVariableRefrigerantFlowFluidTemperatureControlHR:
    def __call__(
        self,
        name: str,
        /,
        *,
        zone_terminal_unit_list_name: str,
        outdoor_unit_evaporating_temperature_function_of_superheating_curve_name: str,
        outdoor_unit_condensing_temperature_function_of_subcooling_curve_name: str,
        availability_schedule_name: str | None = ...,
        refrigerant_type: str | None = "R410A",
        rated_evaporative_capacity: float | Literal["", "Autosize"] | None = 40000,
        rated_compressor_power_per_unit_of_rated_evaporative_capacity: float | None = 0.35,
        minimum_outdoor_air_temperature_in_cooling_only_mode: float | None = -6,
        maximum_outdoor_air_temperature_in_cooling_only_mode: float | None = 43,
        minimum_outdoor_air_temperature_in_heating_only_mode: float | None = -20,
        maximum_outdoor_air_temperature_in_heating_only_mode: float | None = 16,
        minimum_outdoor_temperature_in_heat_recovery_mode: float | None = -20,
        maximum_outdoor_temperature_in_heat_recovery_mode: float | None = 43,
        refrigerant_temperature_control_algorithm_for_indoor_unit: Literal["", "ConstantTemp", "VariableTemp"]
        | None = "VariableTemp",
        reference_evaporating_temperature_for_indoor_unit: float | None = 6,
        reference_condensing_temperature_for_indoor_unit: float | None = 44,
        variable_evaporating_temperature_minimum_for_indoor_unit: float | None = 4,
        variable_evaporating_temperature_maximum_for_indoor_unit: float | None = 13,
        variable_condensing_temperature_minimum_for_indoor_unit: float | None = 42,
        variable_condensing_temperature_maximum_for_indoor_unit: float | None = 46,
        outdoor_unit_evaporator_reference_superheating: float | None = 3,
        outdoor_unit_condenser_reference_subcooling: float | None = 5,
        outdoor_unit_evaporator_rated_bypass_factor: float | None = 0.4,
        outdoor_unit_condenser_rated_bypass_factor: float | None = 0.2,
        difference_between_outdoor_unit_evaporating_temperature_and_outdoor_air_temperature_in_heat_recovery_mode: float
        | None = 5,
        outdoor_unit_heat_exchanger_capacity_ratio: float | None = 0.3,
        outdoor_unit_fan_power_per_unit_of_rated_evaporative_capacity: float | None = 0.00425,
        outdoor_unit_fan_flow_rate_per_unit_of_rated_evaporative_capacity: float | None = ...,
        diameter_of_main_pipe_for_suction_gas: float | None = 0.0762,
        diameter_of_main_pipe_for_discharge_gas: float | None = 0.0762,
        length_of_main_pipe_connecting_outdoor_unit_to_the_first_branch_joint: float | None = 30,
        equivalent_length_of_main_pipe_connecting_outdoor_unit_to_the_first_branch_joint: float | None = 36,
        height_difference_between_outdoor_unit_and_indoor_units: float | None = 5,
        main_pipe_insulation_thickness: float | None = 0.02,
        main_pipe_insulation_thermal_conductivity: float | None = 0.032,
        crankcase_heater_power_per_compressor: float | None = 33,
        number_of_compressors: int | None = 2,
        ratio_of_compressor_size_to_total_compressor_capacity: float | None = 0.5,
        maximum_outdoor_dry_bulb_temperature_for_crankcase_heater: float | None = 5,
        defrost_strategy: Literal["", "Resistive", "ReverseCycle"] | None = "Resistive",
        defrost_control: Literal["", "OnDemand", "Timed"] | None = "Timed",
        defrost_energy_input_ratio_modifier_function_of_temperature_curve_name: str | None = ...,
        defrost_time_period_fraction: float | None = 0.058333,
        resistive_defrost_heater_capacity: float | Literal["", "Autosize"] | None = 0,
        maximum_outdoor_dry_bulb_temperature_for_defrost_operation: float | None = 5,
        initial_heat_recovery_cooling_capacity_fraction: float | None = 1,
        heat_recovery_cooling_capacity_time_constant: float | None = 0,
        initial_heat_recovery_cooling_energy_fraction: float | None = 1,
        heat_recovery_cooling_energy_time_constant: float | None = 0,
        initial_heat_recovery_heating_capacity_fraction: float | None = 1,
        heat_recovery_heating_capacity_time_constant: float | None = 0,
        initial_heat_recovery_heating_energy_fraction: float | None = 1,
        heat_recovery_heating_energy_time_constant: float | None = 0,
        compressor_maximum_delta_pressure: float | None = 4500000,
        compressor_inverter_efficiency: float | None = 0.95,
        compressor_evaporative_capacity_correction_factor: float | None = 1,
        number_of_compressor_loading_index_entries: int | None = 2,
        loading_indices: list[Any] = ...,
    ) -> None: ...

class AnyWaterHeaterStratified:
    def __call__(
        self,
        name: str,
        /,
        *,
        tank_volume: float | Literal["Autosize"],
        tank_height: float | Literal["Autosize"],
        heater_1_setpoint_temperature_schedule_name: str,
        heater_2_setpoint_temperature_schedule_name: str,
        heater_fuel_type: Literal[
            "Coal", "Diesel", "Electricity", "Gasoline", "NaturalGas", "OtherFuel1", "OtherFuel2"
        ],
        heater_thermal_efficiency: float,
        ambient_temperature_indicator: Literal["Outdoors", "Schedule", "Zone"],
        end_use_subcategory: str | None = "General",
        tank_shape: Literal["", "HorizontalCylinder", "Other", "VerticalCylinder"] | None = "VerticalCylinder",
        tank_perimeter: float | None = ...,
        maximum_temperature_limit: float | None = ...,
        heater_priority_control: Literal["", "MasterSlave", "Simultaneous"] | None = "MasterSlave",
        heater_1_deadband_temperature_difference: float | None = 0,
        heater_1_capacity: float | Literal["Autosize"] | None = ...,
        heater_1_height: float | None = ...,
        heater_2_deadband_temperature_difference: float | None = 0,
        heater_2_capacity: float | None = ...,
        heater_2_height: float | None = ...,
        off_cycle_parasitic_fuel_consumption_rate: float | None = 0,
        off_cycle_parasitic_fuel_type: Literal[
            "Coal", "Diesel", "Electricity", "Gasoline", "NaturalGas", "OtherFuel1", "OtherFuel2"
        ]
        | None = ...,
        off_cycle_parasitic_heat_fraction_to_tank: float | None = 0,
        off_cycle_parasitic_height: float | None = 0,
        on_cycle_parasitic_fuel_consumption_rate: float | None = 0,
        on_cycle_parasitic_fuel_type: Literal[
            "Coal", "Diesel", "Electricity", "Gasoline", "NaturalGas", "OtherFuel1", "OtherFuel2"
        ]
        | None = ...,
        on_cycle_parasitic_heat_fraction_to_tank: float | None = 0,
        on_cycle_parasitic_height: float | None = 0,
        ambient_temperature_schedule_name: str | None = ...,
        ambient_temperature_zone_name: str | None = ...,
        ambient_temperature_outdoor_air_node_name: str | None = ...,
        uniform_skin_loss_coefficient_per_unit_area_to_ambient_temperature: float | None = ...,
        skin_loss_fraction_to_zone: float | None = 1,
        off_cycle_flue_loss_coefficient_to_ambient_temperature: float | None = ...,
        off_cycle_flue_loss_fraction_to_zone: float | None = 1,
        peak_use_flow_rate: float | None = ...,
        use_flow_rate_fraction_schedule_name: str | None = ...,
        cold_water_supply_temperature_schedule_name: str | None = ...,
        use_side_inlet_node_name: str | None = ...,
        use_side_outlet_node_name: str | None = ...,
        use_side_effectiveness: float | None = 1,
        use_side_inlet_height: float | None = 0,
        use_side_outlet_height: float | Literal["", "Autocalculate"] | None = "Autocalculate",
        source_side_inlet_node_name: str | None = ...,
        source_side_outlet_node_name: str | None = ...,
        source_side_effectiveness: float | None = 1,
        source_side_inlet_height: float | Literal["", "Autocalculate"] | None = "Autocalculate",
        source_side_outlet_height: float | None = 0,
        inlet_mode: Literal["", "Fixed", "Seeking"] | None = "Fixed",
        use_side_design_flow_rate: float | Literal["", "Autosize"] | None = "Autosize",
        source_side_design_flow_rate: float | Literal["", "Autosize"] | None = "Autosize",
        indirect_water_heating_recovery_time: float | None = 1.5,
        number_of_nodes: int | None = 1,
        additional_destratification_conductivity: float | None = 0,
        node_1_additional_loss_coefficient: float | None = 0,
        node_2_additional_loss_coefficient: float | None = 0,
        node_3_additional_loss_coefficient: float | None = 0,
        node_4_additional_loss_coefficient: float | None = 0,
        node_5_additional_loss_coefficient: float | None = 0,
        node_6_additional_loss_coefficient: float | None = 0,
        node_7_additional_loss_coefficient: float | None = 0,
        node_8_additional_loss_coefficient: float | None = 0,
        node_9_additional_loss_coefficient: float | None = 0,
        node_10_additional_loss_coefficient: float | None = 0,
        node_11_additional_loss_coefficient: float | None = 0,
        node_12_additional_loss_coefficient: float | None = 0,
        source_side_flow_control_mode: Literal[
            "", "IndirectHeatAlternateSetpoint", "IndirectHeatPrimarySetpoint", "StorageTank"
        ]
        | None = "IndirectHeatPrimarySetpoint",
        indirect_alternate_setpoint_temperature_schedule_name: str | None = ...,
    ) -> None: ...

class ThermalStorageIceDetailed:
    def __call__(
        self,
        name: str,
        /,
        *,
        capacity: float | Literal["Autosize"],
        inlet_node_name: str,
        outlet_node_name: str,
        discharging_curve_variable_specifications: Literal[
            "FractionChargedLMTD", "FractionDischargedLMTD", "LMTDFractionCharged", "LMTDMassFlow"
        ],
        discharging_curve_name: str,
        charging_curve_variable_specifications: Literal[
            "FractionChargedLMTD", "FractionDischargedLMTD", "LMTDFractionCharged", "LMTDMassFlow"
        ],
        charging_curve_name: str,
        availability_schedule_name: str | None = ...,
        timestep_of_the_curve_data: float | None = ...,
        parasitic_electric_load_during_discharging: float | None = ...,
        parasitic_electric_load_during_charging: float | None = ...,
        tank_loss_coefficient: float | None = ...,
        freezing_temperature_of_storage_medium: float | None = 0,
        thaw_process_indicator: Literal["", "InsideMelt", "OutsideMelt"] | None = "OutsideMelt",
        thermal_storage_sizing_object_name: str | None = ...,
    ) -> None: ...

class AnyPlantEquipmentList:
    def __call__(self, name: str, /) -> None: ...

class EnergyManagementSystemProgramCallingManager:
    def __call__(
        self,
        name: str,
        /,
        *,
        energyplus_model_calling_point: Literal[
            "AfterComponentInputReadIn",
            "AfterNewEnvironmentWarmUpIsComplete",
            "AfterPredictorAfterHVACManagers",
            "AfterPredictorBeforeHVACManagers",
            "BeginNewEnvironment",
            "BeginTimestepBeforePredictor",
            "BeginZoneTimestepAfterInitHeatBalance",
            "BeginZoneTimestepBeforeInitHeatBalance",
            "BeginZoneTimestepBeforeSetCurrentWeather",
            "EndOfSystemSizing",
            "EndOfSystemTimestepAfterHVACReporting",
            "EndOfSystemTimestepBeforeHVACReporting",
            "EndOfZoneSizing",
            "EndOfZoneTimestepAfterZoneReporting",
            "EndOfZoneTimestepBeforeZoneReporting",
            "InsideHVACSystemIterationLoop",
            "UnitarySystemSizing",
            "UserDefinedComponentModel",
        ]
        | None = ...,
        programs: list[Any] = ...,
    ) -> None: ...

class AnyExternalInterfaceFunctionalMockupUnitImport:
    def __call__(
        self, /, *, fmu_file_name: str, fmu_timeout: float | None = 0, fmu_loggingon: int | None = 0
    ) -> None: ...

class AnyExternalInterfaceFunctionalMockupUnitExportToActuator:
    def __call__(
        self,
        name: str,
        /,
        *,
        actuated_component_unique_name: str,
        actuated_component_type: str,
        actuated_component_control_type: str,
        fmu_variable_name: str,
        initial_value: float | None = ...,
    ) -> None: ...

class AvailabilityManagerScheduled:
    def __call__(self, name: str, /, *, schedule_name: str) -> None: ...

class AvailabilityManagerLowTemperatureTurnOff:
    def __call__(
        self, name: str, /, *, sensor_node_name: str, temperature: float, applicability_schedule_name: str | None = ...
    ) -> None: ...

class SetpointManagerMultiZoneMinimumHumidityAverage:
    def __call__(
        self,
        name: str,
        /,
        *,
        hvac_air_loop_name: str,
        setpoint_node_or_nodelist_name: str,
        minimum_setpoint_humidity_ratio: float | None = 0.005,
        maximum_setpoint_humidity_ratio: float | None = 0.012,
    ) -> None: ...

class ElectricLoadCenterInverterSimple:
    def __call__(
        self,
        name: str = "",
        /,
        *,
        availability_schedule_name: str | None = ...,
        zone_name: str | None = ...,
        radiative_fraction: float | None = ...,
        inverter_efficiency: float | None = ...,
    ) -> None: ...

class FaultModelEnthalpySensorOffsetReturnAir:
    def __call__(
        self,
        name: str,
        /,
        *,
        controller_object_type: Literal["Controller:OutdoorAir"],
        controller_object_name: str,
        availability_schedule_name: str | None = ...,
        severity_schedule_name: str | None = ...,
        enthalpy_sensor_offset: float | None = 0,
    ) -> None: ...

class FaultModelFoulingCoolingTower:
    def __call__(
        self,
        name: str,
        /,
        *,
        cooling_tower_object_type: Literal[
            "CoolingTower:SingleSpeed", "CoolingTower:TwoSpeed", "CoolingTower:VariableSpeed:MERKEL"
        ],
        cooling_tower_object_name: str,
        availability_schedule_name: str | None = ...,
        severity_schedule_name: str | None = ...,
        reference_ua_reduction_factor: float | None = ...,
    ) -> None: ...

class UtilityCostQualify:
    def __call__(
        self,
        /,
        *,
        utility_cost_qualify_name: str,
        tariff_name: str,
        variable_name: str,
        threshold_value_or_variable_name: float | str,
        qualify_type: Literal["", "Maximum", "Minimum"] | None = "Maximum",
        season: Literal["Annual", "Fall", "Spring", "Summer", "Winter"] | None = ...,
        threshold_test: Literal["", "Consecutive", "Count"] | None = "Consecutive",
        number_of_months: float | None = ...,
    ) -> None: ...

class AnyOutputControlSurfaceColorScheme:
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

class OutputTableSummaryReports:
    def __call__(self, /, *, reports: list[Any] = ...) -> None: ...

class FuelFactors:
    def __call__(
        self,
        /,
        *,
        existing_fuel_resource_name: Literal[
            "Coal",
            "Diesel",
            "Electricity",
            "FuelOilNo1",
            "FuelOilNo2",
            "Gasoline",
            "NaturalGas",
            "OtherFuel1",
            "OtherFuel2",
            "Propane",
        ]
        | None = ...,
        source_energy_factor: float | None = ...,
        source_energy_schedule_name: str | None = ...,
        co2_emission_factor: float | None = ...,
        co2_emission_factor_schedule_name: str | None = ...,
        co_emission_factor: float | None = ...,
        co_emission_factor_schedule_name: str | None = ...,
        ch4_emission_factor: float | None = ...,
        ch4_emission_factor_schedule_name: str | None = ...,
        nox_emission_factor: float | None = ...,
        nox_emission_factor_schedule_name: str | None = ...,
        n2o_emission_factor: float | None = ...,
        n2o_emission_factor_schedule_name: str | None = ...,
        so2_emission_factor: float | None = ...,
        so2_emission_factor_schedule_name: str | None = ...,
        pm_emission_factor: float | None = ...,
        pm_emission_factor_schedule_name: str | None = ...,
        pm10_emission_factor: float | None = ...,
        pm10_emission_factor_schedule_name: str | None = ...,
        pm2_5_emission_factor: float | None = ...,
        pm2_5_emission_factor_schedule_name: str | None = ...,
        nh3_emission_factor: float | None = ...,
        nh3_emission_factor_schedule_name: str | None = ...,
        nmvoc_emission_factor: float | None = ...,
        nmvoc_emission_factor_schedule_name: str | None = ...,
        hg_emission_factor: float | None = ...,
        hg_emission_factor_schedule_name: str | None = ...,
        pb_emission_factor: float | None = ...,
        pb_emission_factor_schedule_name: str | None = ...,
        water_emission_factor: float | None = ...,
        water_emission_factor_schedule_name: str | None = ...,
        nuclear_high_level_emission_factor: float | None = ...,
        nuclear_high_level_emission_factor_schedule_name: str | None = ...,
        nuclear_low_level_emission_factor: float | None = ...,
        nuclear_low_level_emission_factor_schedule_name: str | None = ...,
    ) -> None: ...
