"""Creation signatures of generated classes (stub only).

DO NOT EDIT — regenerate with:
    python -m idfkit.codegen.generate_stubs
"""

from __future__ import annotations

from typing import Literal

from .. import _generated_types as _g

class SurfaceConvectionAlgorithmInside:
    def __call__(
        self,
        /,
        *,
        algorithm: Literal["", "ASTMC1340", "AdaptiveConvectionAlgorithm", "CeilingDiffuser", "Simple", "TARP"]
        | None = "TARP",
    ) -> None: ...

class SiteGroundTemperatureBuildingSurface:
    def __call__(
        self,
        /,
        *,
        january_ground_temperature: float | None = 18,
        february_ground_temperature: float | None = 18,
        march_ground_temperature: float | None = 18,
        april_ground_temperature: float | None = 18,
        may_ground_temperature: float | None = 18,
        june_ground_temperature: float | None = 18,
        july_ground_temperature: float | None = 18,
        august_ground_temperature: float | None = 18,
        september_ground_temperature: float | None = 18,
        october_ground_temperature: float | None = 18,
        november_ground_temperature: float | None = 18,
        december_ground_temperature: float | None = 18,
    ) -> None: ...

class MaterialAirGap:
    def __call__(self, name: str, /, *, thermal_resistance: float) -> None: ...

class WindowMaterialScreen:
    def __call__(
        self,
        name: str,
        /,
        *,
        diffuse_solar_reflectance: float,
        diffuse_visible_reflectance: float,
        screen_material_spacing: float,
        screen_material_diameter: float,
        reflected_beam_transmittance_accounting_method: Literal["", "DoNotModel", "ModelAsDiffuse", "ModelAsDirectBeam"]
        | None = "ModelAsDiffuse",
        thermal_hemispherical_emissivity: float | None = 0.9,
        conductivity: float | None = 221,
        screen_to_glass_distance: float | None = 0.025,
        top_opening_multiplier: float | None = 0,
        bottom_opening_multiplier: float | None = 0,
        left_side_opening_multiplier: float | None = 0,
        right_side_opening_multiplier: float | None = 0,
        angle_of_resolution_for_screen_transmittance_output_map: Literal[0, 1, 2, 3, 5, ""] | None = 0,
    ) -> None: ...

class WindowMaterialGapEquivalentLayer:
    def __call__(
        self,
        name: str,
        /,
        *,
        gas_type: Literal["AIR", "ARGON", "CUSTOM", "KRYPTON", "XENON"],
        thickness: float,
        gap_vent_type: Literal["Sealed", "VentedIndoor", "VentedOutdoor"],
        conductivity_coefficient_a: float | None = ...,
        conductivity_coefficient_b: float | None = ...,
        conductivity_coefficient_c: float | None = ...,
        viscosity_coefficient_a: float | None = ...,
        viscosity_coefficient_b: float | None = ...,
        viscosity_coefficient_c: float | None = ...,
        specific_heat_coefficient_a: float | None = ...,
        specific_heat_coefficient_b: float | None = ...,
        specific_heat_coefficient_c: float | None = ...,
        molecular_weight: float | None = ...,
        specific_heat_ratio: float | None = ...,
    ) -> None: ...

class MaterialPropertyHeatAndMoistureTransferThermalConductivity:
    def __call__(
        self,
        /,
        *,
        material_name: str,
        number_of_thermal_coordinates: int,
        moisture_content_1: float,
        thermal_conductivity_1: float,
        moisture_content_2: float | None = ...,
        thermal_conductivity_2: float | None = ...,
        moisture_content_3: float | None = ...,
        thermal_conductivity_3: float | None = ...,
        moisture_content_4: float | None = ...,
        thermal_conductivity_4: float | None = ...,
        moisture_content_5: float | None = ...,
        thermal_conductivity_5: float | None = ...,
        moisture_content_6: float | None = ...,
        thermal_conductivity_6: float | None = ...,
        moisture_content_7: float | None = ...,
        thermal_conductivity_7: float | None = ...,
        moisture_content_8: float | None = ...,
        thermal_conductivity_8: float | None = ...,
        moisture_content_9: float | None = ...,
        thermal_conductivity_9: float | None = ...,
        moisture_content_10: float | None = ...,
        thermal_conductivity_10: float | None = ...,
        moisture_content_11: float | None = ...,
        thermal_conductivity_11: float | None = ...,
        moisture_content_12: float | None = ...,
        thermal_conductivity_12: float | None = ...,
        moisture_content_13: float | None = ...,
        thermal_conductivity_13: float | None = ...,
        moisture_content_14: float | None = ...,
        thermal_conductivity_14: float | None = ...,
        moisture_content_15: float | None = ...,
        thermal_conductivity_15: float | None = ...,
        moisture_content_16: float | None = ...,
        thermal_conductivity_16: float | None = ...,
        moisture_content_17: float | None = ...,
        thermal_conductivity_17: float | None = ...,
        moisture_content_18: float | None = ...,
        thermal_conductivity_18: float | None = ...,
        moisture_content_19: float | None = ...,
        thermal_conductivity_19: float | None = ...,
        moisture_content_20: float | None = ...,
        thermal_conductivity_20: float | None = ...,
        moisture_content_21: float | None = ...,
        thermal_conductivity_21: float | None = ...,
        moisture_content_22: float | None = ...,
        thermal_conductivity_22: float | None = ...,
        moisture_content_23: float | None = ...,
        thermal_conductivity_23: float | None = ...,
        moisture_content_24: float | None = ...,
        thermal_conductivity_24: float | None = ...,
        moisture_content_25: float | None = ...,
        thermal_conductivity_25: float | None = ...,
    ) -> None: ...

class GlazedDoor:
    def __call__(
        self,
        name: str,
        /,
        *,
        construction_name: str,
        building_surface_name: str,
        frame_and_divider_name: str | None = ...,
        multiplier: float | None = 1,
        starting_x_coordinate: float | None = ...,
        starting_z_coordinate: float | None = ...,
        length: float | None = ...,
        height: float | None = ...,
    ) -> None: ...

class AnyWindowShadingControl:
    def __call__(
        self,
        name: str,
        /,
        *,
        zone_name: str,
        shading_type: Literal[
            "BetweenGlassBlind",
            "BetweenGlassShade",
            "ExteriorBlind",
            "ExteriorScreen",
            "ExteriorShade",
            "InteriorBlind",
            "InteriorShade",
            "SwitchableGlazing",
        ],
        shading_control_type: Literal[
            "AlwaysOff",
            "AlwaysOn",
            "MeetDaylightIlluminanceSetpoint",
            "OffNightAndOnDayIfCoolingAndHighSolarOnWindow",
            "OnIfHighGlare",
            "OnIfHighHorizontalSolar",
            "OnIfHighOutdoorAirTempAndHighHorizontalSolar",
            "OnIfHighOutdoorAirTempAndHighSolarOnWindow",
            "OnIfHighOutdoorAirTemperature",
            "OnIfHighSolarOnWindow",
            "OnIfHighZoneAirTempAndHighHorizontalSolar",
            "OnIfHighZoneAirTempAndHighSolarOnWindow",
            "OnIfHighZoneAirTemperature",
            "OnIfHighZoneCooling",
            "OnIfScheduleAllows",
            "OnNightAndOnDayIfCoolingAndHighSolarOnWindow",
            "OnNightIfHeatingAndOffDay",
            "OnNightIfHeatingAndOnDayIfCooling",
            "OnNightIfLowInsideTempAndOffDay",
            "OnNightIfLowOutdoorTempAndOffDay",
            "OnNightIfLowOutdoorTempAndOnDayIfCooling",
        ],
        shading_control_sequence_number: int | None = 1,
        construction_with_shading_name: str | None = ...,
        schedule_name: str | None = ...,
        setpoint: float | None = ...,
        shading_control_is_scheduled: Literal["", "No", "Yes"] | None = "No",
        glare_control_is_active: Literal["", "No", "Yes"] | None = "No",
        shading_device_material_name: str | None = ...,
        type_of_slat_angle_control_for_blinds: Literal["", "BlockBeamSolar", "FixedSlatAngle", "ScheduledSlatAngle"]
        | None = "FixedSlatAngle",
        slat_angle_schedule_name: str | None = ...,
        setpoint_2: float | None = ...,
        daylighting_control_object_name: str | None = ...,
        multiple_surface_control_type: Literal["", "Group", "Sequential"] | None = "Sequential",
        fenestration_surfaces: list[_g.WindowShadingControlFenestrationSurfacesItem] = ...,
    ) -> None: ...

class WindowPropertyFrameAndDivider:
    def __call__(
        self,
        name: str,
        /,
        *,
        frame_width: float | None = 0,
        frame_outside_projection: float | None = 0,
        frame_inside_projection: float | None = 0,
        frame_conductance: float | None = 0,
        ratio_of_frame_edge_glass_conductance_to_center_of_glass_conductance: float | None = 1,
        frame_solar_absorptance: float | None = 0.7,
        frame_visible_absorptance: float | None = 0.7,
        frame_thermal_hemispherical_emissivity: float | None = 0.9,
        divider_type: Literal["", "DividedLite", "Suspended"] | None = "DividedLite",
        divider_width: float | None = 0,
        number_of_horizontal_dividers: int | None = 0,
        number_of_vertical_dividers: int | None = 0,
        divider_outside_projection: float | None = 0,
        divider_inside_projection: float | None = 0,
        divider_conductance: float | None = 0,
        ratio_of_divider_edge_glass_conductance_to_center_of_glass_conductance: float | None = 1,
        divider_solar_absorptance: float | None = 0,
        divider_visible_absorptance: float | None = 0,
        divider_thermal_hemispherical_emissivity: float | None = 0.9,
        outside_reveal_solar_absorptance: float | None = 0,
        inside_sill_depth: float | None = 0,
        inside_sill_solar_absorptance: float | None = 0,
        inside_reveal_depth: float | None = 0,
        inside_reveal_solar_absorptance: float | None = 0,
        nfrc_product_type_for_assembly_calculations: Literal[
            "",
            "CasementDouble",
            "CasementSingle",
            "CurtainWall",
            "DoorSidelite",
            "DoorTransom",
            "DualAction",
            "Fixed",
            "Garage",
            "Greenhouse",
            "HingedEscape",
            "HorizontalSlider",
            "Jal",
            "Pivoted",
            "ProjectingDual",
            "ProjectingSingle",
            "SideHingedDoor",
            "Skylight",
            "SlidingPatioDoor",
            "SpandrelPanel",
            "TropicalAwning",
            "TubularDaylightingDevice",
            "VerticalSlider",
        ]
        | None = "CurtainWall",
    ) -> None: ...

class WindowPropertyStormWindow:
    def __call__(
        self,
        /,
        *,
        window_name: str,
        storm_glass_layer_name: str,
        month_that_storm_glass_layer_is_put_on: int,
        day_of_month_that_storm_glass_layer_is_put_on: int,
        month_that_storm_glass_layer_is_taken_off: int,
        day_of_month_that_storm_glass_layer_is_taken_off: int,
        distance_between_storm_glass_layer_and_adjacent_glass: float | None = 0.05,
    ) -> None: ...

class FoundationKivaSettings:
    def __call__(
        self,
        /,
        *,
        soil_conductivity: float | None = 1.73,
        soil_density: float | None = 1842,
        soil_specific_heat: float | None = 419,
        ground_solar_absorptivity: float | None = 0.9,
        ground_thermal_absorptivity: float | None = 0.9,
        ground_surface_roughness: float | None = 0.03,
        far_field_width: float | None = 40,
        deep_ground_boundary_condition: Literal["", "Autoselect", "GroundWater", "ZeroFlux"] | None = "Autoselect",
        deep_ground_depth: float | Literal["", "Autocalculate"] | None = "Autocalculate",
        minimum_cell_dimension: float | None = 0.02,
        maximum_cell_growth_coefficient: float | None = 1.5,
        simulation_timestep: Literal["", "Hourly", "Timestep"] | None = "Hourly",
    ) -> None: ...

class AnyRoomAirTemperaturePatternSurfaceMapping:
    def __call__(
        self,
        name: str,
        /,
        *,
        control_integer_for_pattern_control_schedule_name: int,
        thermostat_offset: float | None = ...,
        return_air_offset: float | None = ...,
        exhaust_air_offset: float | None = ...,
        surface_deltas: list[_g.RoomAirTemperaturePatternSurfaceMappingSurfaceDeltasItem] = ...,
    ) -> None: ...

class AirflowNetworkMultiZoneWindPressureCoefficientArray:
    def __call__(
        self,
        name: str,
        /,
        *,
        wind_direction_1: float,
        wind_direction_2: float,
        wind_direction_3: float | None = ...,
        wind_direction_4: float | None = ...,
        wind_direction_5: float | None = ...,
        wind_direction_6: float | None = ...,
        wind_direction_7: float | None = ...,
        wind_direction_8: float | None = ...,
        wind_direction_9: float | None = ...,
        wind_direction_10: float | None = ...,
        wind_direction_11: float | None = ...,
        wind_direction_12: float | None = ...,
        wind_direction_13: float | None = ...,
        wind_direction_14: float | None = ...,
        wind_direction_15: float | None = ...,
        wind_direction_16: float | None = ...,
        wind_direction_17: float | None = ...,
        wind_direction_18: float | None = ...,
        wind_direction_19: float | None = ...,
        wind_direction_20: float | None = ...,
        wind_direction_21: float | None = ...,
        wind_direction_22: float | None = ...,
        wind_direction_23: float | None = ...,
        wind_direction_24: float | None = ...,
        wind_direction_25: float | None = ...,
        wind_direction_26: float | None = ...,
        wind_direction_27: float | None = ...,
        wind_direction_28: float | None = ...,
        wind_direction_29: float | None = ...,
        wind_direction_30: float | None = ...,
        wind_direction_31: float | None = ...,
        wind_direction_32: float | None = ...,
        wind_direction_33: float | None = ...,
        wind_direction_34: float | None = ...,
        wind_direction_35: float | None = ...,
        wind_direction_36: float | None = ...,
    ) -> None: ...

class AirflowNetworkDistributionComponentLeak:
    def __call__(
        self, name: str, /, *, air_mass_flow_coefficient: float, air_mass_flow_exponent: float | None = 0.65
    ) -> None: ...

class AirflowNetworkDistributionComponentLeakageRatio:
    def __call__(
        self,
        name: str,
        /,
        *,
        maximum_flow_rate: float,
        reference_pressure_difference: float,
        effective_leakage_ratio: float | None = ...,
        air_mass_flow_exponent: float | None = 0.65,
    ) -> None: ...

class AnyDesignSpecificationOutdoorAir:
    def __call__(
        self,
        name: str,
        /,
        *,
        outdoor_air_method: Literal[
            "",
            "AirChanges/Hour",
            "Flow/Area",
            "Flow/Person",
            "Flow/Zone",
            "IndoorAirQualityProcedure",
            "Maximum",
            "ProportionalControlBasedOnDesignOccupancy",
            "Sum",
        ]
        | None = "Flow/Person",
        outdoor_air_flow_per_person: float | None = 0.00944,
        outdoor_air_flow_per_zone_floor_area: float | None = 0,
        outdoor_air_flow_per_zone: float | None = 0,
        outdoor_air_flow_air_changes_per_hour: float | None = 0,
        outdoor_air_schedule_name: str | None = ...,
        proportional_control_minimum_outdoor_air_flow_rate_schedule_name: str | None = ...,
    ) -> None: ...

class ThermostatSetpointSingleHeating:
    def __call__(self, name: str, /, *, setpoint_temperature_schedule_name: str | None = ...) -> None: ...

class CoilCoolingDXVariableRefrigerantFlowFluidTemperatureControl:
    def __call__(
        self,
        name: str,
        /,
        *,
        coil_air_inlet_node: str,
        coil_air_outlet_node: str,
        rated_total_cooling_capacity: float | Literal["Autosize"],
        rated_sensible_heat_ratio: float | Literal["Autosize"],
        indoor_unit_evaporating_temperature_function_of_superheating_curve_name: str,
        availability_schedule_name: str | None = ...,
        indoor_unit_reference_superheating: float | None = 5,
        name_of_water_storage_tank_for_condensate_collection: str | None = ...,
    ) -> None: ...

class AnyCoilSystemCoolingDX:
    def __call__(
        self,
        name: str,
        /,
        *,
        dx_cooling_coil_system_inlet_node_name: str,
        dx_cooling_coil_system_outlet_node_name: str,
        dx_cooling_coil_system_sensor_node_name: str,
        cooling_coil_object_type: Literal[
            "Coil:Cooling:DX:SingleSpeed",
            "Coil:Cooling:DX:SingleSpeed:ThermalStorage",
            "Coil:Cooling:DX:TwoSpeed",
            "Coil:Cooling:DX:TwoStageWithHumidityControlMode",
            "Coil:Cooling:DX:VariableSpeed",
            "CoilSystem:Cooling:DX:HeatExchangerAssisted",
        ],
        cooling_coil_name: str,
        availability_schedule_name: str | None = ...,
        dehumidification_control_type: Literal["", "CoolReheat", "Multimode", "None"] | None = "None",
        run_on_sensible_load: Literal["", "No", "Yes"] | None = "Yes",
        run_on_latent_load: Literal["", "No", "Yes"] | None = "No",
        use_outdoor_air_dx_cooling_coil: Literal["", "No", "Yes"] | None = "No",
        outdoor_air_dx_cooling_coil_leaving_minimum_air_temperature: float | None = 2,
    ) -> None: ...

class EvaporativeCoolerDirectResearchSpecial:
    def __call__(
        self,
        name: str = "",
        /,
        *,
        air_inlet_node_name: str,
        air_outlet_node_name: str,
        sensor_node_name: str,
        availability_schedule_name: str | None = ...,
        cooler_design_effectiveness: float | None = ...,
        effectiveness_flow_ratio_modifier_curve_name: str | None = ...,
        primary_air_design_flow_rate: float | Literal["", "Autosize"] | None = "Autosize",
        recirculating_water_pump_design_power: float | Literal["", "Autosize"] | None = "Autosize",
        water_pump_power_sizing_factor: float | None = 90,
        water_pump_power_modifier_curve_name: str | None = ...,
        water_supply_storage_tank_name: str | None = ...,
        drift_loss_fraction: float | None = ...,
        blowdown_concentration_ratio: float | None = ...,
        evaporative_operation_minimum_drybulb_temperature: float | None = ...,
        evaporative_operation_maximum_limit_wetbulb_temperature: float | None = ...,
        evaporative_operation_maximum_limit_drybulb_temperature: float | None = ...,
    ) -> None: ...

class AnyAirConditionerVariableRefrigerantFlowFluidTemperatureControl:
    def __call__(
        self,
        /,
        *,
        heat_pump_name: str,
        zone_terminal_unit_list_name: str,
        outdoor_unit_evaporating_temperature_function_of_superheating_curve_name: str,
        outdoor_unit_condensing_temperature_function_of_subcooling_curve_name: str,
        availability_schedule_name: str | None = ...,
        refrigerant_type: str | None = "R410A",
        rated_evaporative_capacity: float | Literal["", "Autosize"] | None = 40000,
        rated_compressor_power_per_unit_of_rated_evaporative_capacity: float | None = 0.35,
        minimum_outdoor_air_temperature_in_cooling_mode: float | None = -6,
        maximum_outdoor_air_temperature_in_cooling_mode: float | None = 43,
        minimum_outdoor_air_temperature_in_heating_mode: float | None = -20,
        maximum_outdoor_air_temperature_in_heating_mode: float | None = 16,
        reference_outdoor_unit_superheating: float | None = 3,
        reference_outdoor_unit_subcooling: float | None = 5,
        refrigerant_temperature_control_algorithm_for_indoor_unit: Literal["", "ConstantTemp", "VariableTemp"]
        | None = "VariableTemp",
        reference_evaporating_temperature_for_indoor_unit: float | None = 6,
        reference_condensing_temperature_for_indoor_unit: float | None = 44,
        variable_evaporating_temperature_minimum_for_indoor_unit: float | None = 4,
        variable_evaporating_temperature_maximum_for_indoor_unit: float | None = 13,
        variable_condensing_temperature_minimum_for_indoor_unit: float | None = 42,
        variable_condensing_temperature_maximum_for_indoor_unit: float | None = 46,
        outdoor_unit_fan_power_per_unit_of_rated_evaporative_capacity: float | None = 0.00425,
        outdoor_unit_fan_flow_rate_per_unit_of_rated_evaporative_capacity: float | None = ...,
        diameter_of_main_pipe_connecting_outdoor_unit_to_the_first_branch_joint: float | None = 0.0762,
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
        compressor_maximum_delta_pressure: float | None = 4500000,
        number_of_compressor_loading_index_entries: int | None = 2,
        loading_indices: list[_g.AirConditionerVariableRefrigerantFlowFluidTemperatureControlLoadingIndicesItem] = ...,
    ) -> None: ...

class AnyControllerMechanicalVentilation:
    def __call__(
        self,
        name: str,
        /,
        *,
        availability_schedule_name: str | None = ...,
        demand_controlled_ventilation: Literal["", "No", "Yes"] | None = "No",
        system_outdoor_air_method: Literal[
            "",
            "IndoorAirQualityProcedure",
            "IndoorAirQualityProcedureCombined",
            "IndoorAirQualityProcedureGenericContaminant",
            "ProportionalControlBasedOnDesignOARate",
            "ProportionalControlBasedOnDesignOccupancy",
            "ZoneSum",
        ]
        | None = ...,
        zone_maximum_outdoor_air_fraction: float | None = 1,
        zone_specifications: list[_g.AnyControllerMechanicalVentilationZoneSpecificationsItem] = ...,
    ) -> None: ...

class OutdoorAirNode:
    def __call__(
        self,
        name: str,
        /,
        *,
        height_above_ground: float | None = -1,
        drybulb_temperature_schedule_name: str | None = ...,
        wetbulb_temperature_schedule_name: str | None = ...,
        wind_speed_schedule_name: str | None = ...,
        wind_direction_schedule_name: str | None = ...,
        wind_pressure_coefficient_curve_name: str | None = ...,
        symmetric_wind_pressure_coefficient_curve: Literal["", "No", "Yes"] | None = "No",
        wind_angle_type: Literal["", "Absolute", "Relative"] | None = "Absolute",
    ) -> None: ...

class PumpConstantSpeed:
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
        end_use_subcategory: str | None = "General",
    ) -> None: ...

class AnyChillerElectricReformulatedEIR:
    def __call__(
        self,
        name: str,
        /,
        *,
        reference_capacity: float | Literal["Autosize"],
        reference_cop: float,
        cooling_capacity_function_of_temperature_curve_name: str,
        electric_input_to_cooling_output_ratio_function_of_temperature_curve_name: str,
        electric_input_to_cooling_output_ratio_function_of_part_load_ratio_curve_name: str,
        chilled_water_inlet_node_name: str,
        chilled_water_outlet_node_name: str,
        condenser_inlet_node_name: str,
        condenser_outlet_node_name: str,
        reference_leaving_chilled_water_temperature: float | None = 6.67,
        reference_leaving_condenser_water_temperature: float | None = 35,
        reference_chilled_water_flow_rate: float | Literal["Autosize"] | None = ...,
        reference_condenser_water_flow_rate: float | Literal["Autosize"] | None = ...,
        electric_input_to_cooling_output_ratio_function_of_part_load_ratio_curve_type: Literal[
            "", "LeavingCondenserWaterTemperature", "Lift"
        ]
        | None = "LeavingCondenserWaterTemperature",
        minimum_part_load_ratio: float | None = 0.1,
        maximum_part_load_ratio: float | None = 1,
        optimum_part_load_ratio: float | None = 1,
        minimum_unloading_ratio: float | None = 0.2,
        fraction_of_compressor_electric_consumption_rejected_by_condenser: float | None = 1,
        leaving_chilled_water_lower_temperature_limit: float | None = 2,
        chiller_flow_mode_type: Literal["", "ConstantFlow", "LeavingSetpointModulated", "NotModulated"]
        | None = "NotModulated",
        design_heat_recovery_water_flow_rate: float | Literal["", "Autosize"] | None = 0,
        heat_recovery_inlet_node_name: str | None = ...,
        heat_recovery_outlet_node_name: str | None = ...,
        sizing_factor: float | None = 1,
        condenser_heat_recovery_relative_capacity_fraction: float | None = ...,
        heat_recovery_inlet_high_temperature_limit_schedule_name: str | None = ...,
        heat_recovery_leaving_temperature_setpoint_node_name: str | None = ...,
        end_use_subcategory: str | None = "General",
    ) -> None: ...

class ChillerAbsorptionIndirect:
    def __call__(
        self,
        name: str,
        /,
        *,
        nominal_capacity: float | Literal["Autosize"],
        nominal_pumping_power: float | Literal["Autosize"],
        chilled_water_inlet_node_name: str,
        chilled_water_outlet_node_name: str,
        condenser_inlet_node_name: str,
        condenser_outlet_node_name: str,
        generator_heat_input_function_of_part_load_ratio_curve_name: str,
        minimum_part_load_ratio: float | None = ...,
        maximum_part_load_ratio: float | None = ...,
        optimum_part_load_ratio: float | None = ...,
        design_condenser_inlet_temperature: float | None = 30,
        condenser_inlet_temperature_lower_limit: float | None = 15,
        chilled_water_outlet_temperature_lower_limit: float | None = 5,
        design_chilled_water_flow_rate: float | Literal["", "Autosize"] | None = "Autosize",
        design_condenser_water_flow_rate: float | Literal["", "Autosize"] | None = "Autosize",
        chiller_flow_mode: Literal["", "ConstantFlow", "LeavingSetpointModulated", "NotModulated"]
        | None = "NotModulated",
        pump_electric_input_function_of_part_load_ratio_curve_name: str | None = ...,
        generator_inlet_node_name: str | None = ...,
        generator_outlet_node_name: str | None = ...,
        capacity_correction_function_of_condenser_temperature_curve_name: str | None = ...,
        capacity_correction_function_of_chilled_water_temperature_curve_name: str | None = ...,
        capacity_correction_function_of_generator_temperature_curve_name: str | None = ...,
        generator_heat_input_correction_function_of_condenser_temperature_curve_name: str | None = ...,
        generator_heat_input_correction_function_of_chilled_water_temperature_curve_name: str | None = ...,
        generator_heat_source_type: Literal["", "HotWater", "Steam"] | None = "Steam",
        design_generator_fluid_flow_rate: float | Literal["Autosize"] | None = ...,
        temperature_lower_limit_generator_inlet: float | None = 0,
        degree_of_subcooling_in_steam_generator: float | None = 1,
        degree_of_subcooling_in_steam_condensate_loop: float | None = 0,
        sizing_factor: float | None = 1,
    ) -> None: ...

class PlantLoop:
    def __call__(
        self,
        name: str,
        /,
        *,
        plant_equipment_operation_scheme_name: str,
        loop_temperature_setpoint_node_name: str,
        maximum_loop_temperature: float,
        minimum_loop_temperature: float,
        maximum_loop_flow_rate: float | Literal["Autosize"],
        plant_side_inlet_node_name: str,
        plant_side_outlet_node_name: str,
        plant_side_branch_list_name: str,
        demand_side_inlet_node_name: str,
        demand_side_outlet_node_name: str,
        demand_side_branch_list_name: str,
        fluid_type: Literal["", "Steam", "UserDefinedFluidType", "Water"] | None = "Water",
        user_defined_fluid_type: str | None = ...,
        minimum_loop_flow_rate: float | None = 0,
        plant_loop_volume: float | Literal["", "Autocalculate"] | None = "Autocalculate",
        plant_side_connector_list_name: str | None = ...,
        demand_side_connector_list_name: str | None = ...,
        load_distribution_scheme: Literal[
            "", "Optimal", "SequentialLoad", "SequentialUniformPLR", "UniformLoad", "UniformPLR"
        ]
        | None = "SequentialLoad",
        availability_manager_list_name: str | None = ...,
        plant_loop_demand_calculation_scheme: Literal["", "DualSetpointDeadband", "SingleSetpoint"]
        | None = "SingleSetpoint",
        common_pipe_simulation: Literal["", "CommonPipe", "None", "TwoWayCommonPipe"] | None = "None",
        pressure_simulation_type: Literal["", "LoopFlowCorrection", "None", "PumpPowerCorrection"] | None = "None",
        loop_circulation_time: float | None = 2,
    ) -> None: ...

class CondenserLoop:
    def __call__(
        self,
        name: str,
        /,
        *,
        condenser_equipment_operation_scheme_name: str,
        condenser_loop_temperature_setpoint_node_name: str,
        maximum_loop_temperature: float,
        minimum_loop_temperature: float,
        maximum_loop_flow_rate: float | Literal["Autosize"],
        condenser_side_inlet_node_name: str,
        condenser_side_outlet_node_name: str,
        condenser_side_branch_list_name: str,
        condenser_side_connector_list_name: str,
        demand_side_inlet_node_name: str,
        demand_side_outlet_node_name: str,
        condenser_demand_side_branch_list_name: str,
        condenser_demand_side_connector_list_name: str,
        fluid_type: Literal["", "UserDefinedFluidType", "Water"] | None = "Water",
        user_defined_fluid_type: str | None = ...,
        minimum_loop_flow_rate: float | None = 0,
        condenser_loop_volume: float | Literal["", "Autocalculate"] | None = "Autocalculate",
        load_distribution_scheme: Literal[
            "", "Optimal", "SequentialLoad", "SequentialUniformPLR", "UniformLoad", "UniformPLR"
        ]
        | None = "SequentialLoad",
        pressure_simulation_type: Literal["", "LoopFlowCorrection", "None", "PumpPowerCorrection"] | None = "None",
        loop_circulation_time: float | None = 2,
    ) -> None: ...

class PlantEquipmentOperationOutdoorDryBulb:
    def __call__(
        self,
        name: str,
        /,
        *,
        dry_bulb_temperature_range_1_lower_limit: float,
        dry_bulb_temperature_range_1_upper_limit: float,
        range_1_equipment_list_name: str,
        dry_bulb_temperature_range_2_lower_limit: float | None = ...,
        dry_bulb_temperature_range_2_upper_limit: float | None = ...,
        range_2_equipment_list_name: str | None = ...,
        dry_bulb_temperature_range_3_lower_limit: float | None = ...,
        dry_bulb_temperature_range_3_upper_limit: float | None = ...,
        range_3_equipment_list_name: str | None = ...,
        dry_bulb_temperature_range_4_lower_limit: float | None = ...,
        dry_bulb_temperature_range_4_upper_limit: float | None = ...,
        range_4_equipment_list_name: str | None = ...,
        dry_bulb_temperature_range_5_lower_limit: float | None = ...,
        dry_bulb_temperature_range_5_upper_limit: float | None = ...,
        range_5_equipment_list_name: str | None = ...,
        dry_bulb_temperature_range_6_lower_limit: float | None = ...,
        dry_bulb_temperature_range_6_upper_limit: float | None = ...,
        range_6_equipment_list_name: str | None = ...,
        dry_bulb_temperature_range_7_lower_limit: float | None = ...,
        dry_bulb_temperature_range_7_upper_limit: float | None = ...,
        range_7_equipment_list_name: str | None = ...,
        dry_bulb_temperature_range_8_lower_limit: float | None = ...,
        dry_bulb_temperature_range_8_upper_limit: float | None = ...,
        range_8_equipment_list_name: str | None = ...,
        dry_bulb_temperature_range_9_lower_limit: float | None = ...,
        dry_bulb_temperature_range_9_upper_limit: float | None = ...,
        range_9_equipment_list_name: str | None = ...,
        dry_bulb_temperature_range_10_lower_limit: float | None = ...,
        dry_bulb_temperature_range_10_upper_limit: float | None = ...,
        range_10_equipment_list_name: str | None = ...,
    ) -> None: ...

class PlantEquipmentOperationUserDefined:
    def __call__(
        self,
        name: str,
        /,
        *,
        main_model_program_calling_manager_name: str,
        initialization_program_calling_manager_name: str | None = ...,
        equipment_1_object_type: str | None = ...,
        equipment_1_name: str | None = ...,
        equipment_2_object_type: str | None = ...,
        equipment_2_name: str | None = ...,
        equipment_3_object_type: str | None = ...,
        equipment_3_name: str | None = ...,
        equipment_4_object_type: str | None = ...,
        equipment_4_name: str | None = ...,
        equipment_5_object_type: str | None = ...,
        equipment_5_name: str | None = ...,
        equipment_6_object_type: str | None = ...,
        equipment_6_name: str | None = ...,
        equipment_7_object_type: str | None = ...,
        equipment_7_name: str | None = ...,
        equipment_8_object_type: str | None = ...,
        equipment_8_name: str | None = ...,
        equipment_9_object_type: str | None = ...,
        equipment_9_name: str | None = ...,
        equipment_10_object_type: str | None = ...,
        equipment_10_name: str | None = ...,
    ) -> None: ...

class SetpointManagerMultiZoneCoolingAverage:
    def __call__(
        self,
        name: str,
        /,
        *,
        hvac_air_loop_name: str,
        setpoint_node_or_nodelist_name: str,
        minimum_setpoint_temperature: float | None = 12,
        maximum_setpoint_temperature: float | None = 18,
    ) -> None: ...

class GeneratorMicroTurbine:
    def __call__(
        self,
        name: str,
        /,
        *,
        reference_electrical_power_output: float,
        reference_electrical_efficiency_using_lower_heating_value: float,
        electrical_power_function_of_temperature_and_elevation_curve_name: str,
        electrical_efficiency_function_of_temperature_curve_name: str,
        electrical_efficiency_function_of_part_load_ratio_curve_name: str,
        minimum_full_load_electrical_power_output: float | None = 0,
        maximum_full_load_electrical_power_output: float | None = ...,
        reference_combustion_air_inlet_temperature: float | None = 15,
        reference_combustion_air_inlet_humidity_ratio: float | None = 0.00638,
        reference_elevation: float | None = 0,
        fuel_type: Literal[
            "",
            "Coal",
            "Diesel",
            "FuelOilNo1",
            "FuelOilNo2",
            "Gasoline",
            "NaturalGas",
            "OtherFuel1",
            "OtherFuel2",
            "Propane",
        ]
        | None = "NaturalGas",
        fuel_higher_heating_value: float | None = 50000,
        fuel_lower_heating_value: float | None = 45450,
        standby_power: float | None = 0,
        ancillary_power: float | None = 0,
        ancillary_power_function_of_fuel_input_curve_name: str | None = ...,
        heat_recovery_water_inlet_node_name: str | None = ...,
        heat_recovery_water_outlet_node_name: str | None = ...,
        reference_thermal_efficiency_using_lower_heat_value: float | None = 0,
        reference_inlet_water_temperature: float | None = ...,
        heat_recovery_water_flow_operating_mode: Literal["", "InternalControl", "PlantControl"] | None = "PlantControl",
        reference_heat_recovery_water_flow_rate: float | None = ...,
        heat_recovery_water_flow_rate_function_of_temperature_and_power_curve_name: str | None = ...,
        thermal_efficiency_function_of_temperature_and_elevation_curve_name: str | None = ...,
        heat_recovery_rate_function_of_part_load_ratio_curve_name: str | None = ...,
        heat_recovery_rate_function_of_inlet_water_temperature_curve_name: str | None = ...,
        heat_recovery_rate_function_of_water_flow_rate_curve_name: str | None = ...,
        minimum_heat_recovery_water_flow_rate: float | None = 0,
        maximum_heat_recovery_water_flow_rate: float | None = 0,
        maximum_heat_recovery_water_temperature: float | None = ...,
        combustion_air_inlet_node_name: str | None = ...,
        combustion_air_outlet_node_name: str | None = ...,
        reference_exhaust_air_mass_flow_rate: float | None = ...,
        exhaust_air_flow_rate_function_of_temperature_curve_name: str | None = ...,
        exhaust_air_flow_rate_function_of_part_load_ratio_curve_name: str | None = ...,
        nominal_exhaust_air_outlet_temperature: float | None = ...,
        exhaust_air_temperature_function_of_temperature_curve_name: str | None = ...,
        exhaust_air_temperature_function_of_part_load_ratio_curve_name: str | None = ...,
    ) -> None: ...

class ElectricLoadCenterDistribution:
    def __call__(
        self,
        name: str,
        /,
        *,
        generator_list_name: str | None = ...,
        generator_operation_scheme_type: Literal[
            "Baseload",
            "DemandLimit",
            "FollowThermal",
            "FollowThermalLimitElectrical",
            "TrackElectrical",
            "TrackMeter",
            "TrackSchedule",
        ]
        | None = ...,
        generator_demand_limit_scheme_purchased_electric_demand_limit: float | None = ...,
        generator_track_schedule_name_scheme_schedule_name: str | None = ...,
        generator_track_meter_scheme_meter_name: str | None = ...,
        electrical_buss_type: Literal[
            "",
            "AlternatingCurrent",
            "AlternatingCurrentWithStorage",
            "DirectCurrentWithInverter",
            "DirectCurrentWithInverterACStorage",
            "DirectCurrentWithInverterDCStorage",
        ]
        | None = "AlternatingCurrent",
        inverter_name: str | None = ...,
        electrical_storage_object_name: str | None = ...,
        transformer_object_name: str | None = ...,
        storage_operation_scheme: Literal[
            "",
            "FacilityDemandLeveling",
            "TrackChargeDischargeSchedules",
            "TrackFacilityElectricDemandStoreExcessOnSite",
            "TrackMeterDemandStoreExcessOnSite",
        ]
        | None = ...,
        storage_control_track_meter_name: str | None = ...,
        storage_converter_object_name: str | None = ...,
        maximum_storage_state_of_charge_fraction: float | None = 1,
        minimum_storage_state_of_charge_fraction: float | None = 0,
        design_storage_control_charge_power: float | None = ...,
        storage_charge_power_fraction_schedule_name: str | None = ...,
        design_storage_control_discharge_power: float | None = ...,
        storage_discharge_power_fraction_schedule_name: str | None = ...,
        storage_control_utility_demand_target: float | None = ...,
        storage_control_utility_demand_target_fraction_schedule_name: str | None = ...,
    ) -> None: ...

class AnyHybridModelZone:
    def __call__(
        self,
        name: str,
        /,
        *,
        zone_name: str,
        zone_measured_air_temperature_schedule_name: str,
        begin_month: int,
        begin_day_of_month: int,
        end_month: int,
        end_day_of_month: int,
        calculate_zone_internal_thermal_mass: Literal["", "No", "Yes"] | None = "No",
        calculate_zone_air_infiltration_rate: Literal["", "No", "Yes"] | None = "No",
    ) -> None: ...

class CurveFanPressureRise:
    def __call__(
        self,
        name: str,
        /,
        *,
        coefficient1_c1: float,
        coefficient2_c2: float,
        coefficient3_c3: float,
        coefficient4_c4: float,
        minimum_value_of_qfan: float,
        maximum_value_of_qfan: float,
        minimum_value_of_psm: float,
        maximum_value_of_psm: float,
        minimum_curve_output: float | None = ...,
        maximum_curve_output: float | None = ...,
    ) -> None: ...

class ParametricRunControl:
    def __call__(self, name: str = "", /, *, runs: list[_g.ParametricRunControlRunsItem] = ...) -> None: ...

class AnyOutputControlTableStyle:
    def __call__(
        self,
        /,
        *,
        column_separator: Literal[
            "", "All", "Comma", "CommaAndHTML", "CommaAndXML", "Fixed", "HTML", "Tab", "TabAndHTML", "XML", "XMLandHTML"
        ]
        | None = "Comma",
        unit_conversion: Literal["", "InchPound", "JtoGJ", "JtoKWH", "JtoMJ", "None"] | None = "None",
    ) -> None: ...

class OutputControlReportingTolerances:
    def __call__(
        self,
        /,
        *,
        tolerance_for_time_heating_setpoint_not_met: float | None = 0.2,
        tolerance_for_time_cooling_setpoint_not_met: float | None = 0.2,
    ) -> None: ...

class OutputMeterCumulativeMeterFileOnly:
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
