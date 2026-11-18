"""Creation signatures of generated classes (stub only).

DO NOT EDIT — regenerate with:
    python -m idfkit.codegen.generate_stubs
"""

from __future__ import annotations

from typing import Any, Literal

from typing_extensions import Never

class AnySurfaceConvectionAlgorithmInside:
    def __call__(
        self,
        /,
        *,
        algorithm: Literal["", "AdaptiveConvectionAlgorithm", "CeilingDiffuser", "Simple", "TARP"] | None = "TARP",
    ) -> None: ...

class SiteLocation:
    def __call__(
        self,
        name: str,
        /,
        *,
        latitude: float | None = 0,
        longitude: float | None = 0,
        time_zone: float | None = 0,
        elevation: float | None = 0,
        keep_site_location_information: Literal["", "No", "Yes"] | None = "No",
    ) -> None: ...

class SiteVariableLocation:
    def __call__(
        self,
        name: str,
        /,
        *,
        building_location_latitude_schedule: str | None = ...,
        building_location_longitude_schedule: str | None = ...,
        building_location_orientation_schedule: str | None = ...,
    ) -> None: ...

class AnySiteWaterMainsTemperature:
    def __call__(
        self,
        /,
        *,
        calculation_method: Literal["Correlation", "Schedule"],
        temperature_schedule_name: str | None = ...,
        annual_average_outdoor_air_temperature: float | None = ...,
        maximum_difference_in_monthly_average_outdoor_air_temperatures: float | None = ...,
    ) -> None: ...

class AnyMaterialPropertyHeatAndMoistureTransferDiffusion:
    def __call__(
        self,
        /,
        *,
        material_name: str,
        number_of_data_pairs: int,
        relative_humidity_fraction_1: float,
        water_vapor_diffusion_resistance_factor_1: float,
        relative_humidity_fraction_2: float | None = ...,
        water_vapor_diffusion_resistance_factor_2: float | None = ...,
        relative_humidity_fraction_3: float | None = ...,
        water_vapor_diffusion_resistance_factor_3: float | None = ...,
        relative_humidity_fraction_4: float | None = ...,
        water_vapor_diffusion_resistance_factor_4: float | None = ...,
        relative_humidity_fraction_5: float | None = ...,
        water_vapor_diffusion_resistance_factor_5: float | None = ...,
        relative_humidity_fraction_6: float | None = ...,
        water_vapor_diffusion_resistance_factor_6: float | None = ...,
        relative_humidity_fraction_7: float | None = ...,
        water_vapor_diffusion_resistance_factor_7: float | None = ...,
        relative_humidity_fraction_8: float | None = ...,
        water_vapor_diffusion_resistance_factor_8: float | None = ...,
        relative_humidity_fraction_9: float | None = ...,
        water_vapor_diffusion_resistance_factor_9: float | None = ...,
        relative_humidity_fraction_10: float | None = ...,
        water_vapor_diffusion_resistance_factor_10: float | None = ...,
        relative_humidity_fraction_11: float | None = ...,
        water_vapor_diffusion_resistance_factor_11: float | None = ...,
        relative_humidity_fraction_12: float | None = ...,
        water_vapor_diffusion_resistance_factor_12: float | None = ...,
        relative_humidity_fraction_13: float | None = ...,
        water_vapor_diffusion_resistance_factor_13: float | None = ...,
        relative_humidity_fraction_14: float | None = ...,
        water_vapor_diffusion_resistance_factor_14: float | None = ...,
        relative_humidity_fraction_15: float | None = ...,
        water_vapor_diffusion_resistance_factor_15: float | None = ...,
        relative_humidity_fraction_16: float | None = ...,
        water_vapor_diffusion_resistance_factor_16: float | None = ...,
        relative_humidity_fraction_17: float | None = ...,
        water_vapor_diffusion_resistance_factor_17: float | None = ...,
        relative_humidity_fraction_18: float | None = ...,
        water_vapor_diffusion_resistance_factor_18: float | None = ...,
        relative_humidity_fraction_19: float | None = ...,
        water_vapor_diffusion_resistance_factor_19: float | None = ...,
        relative_humidity_fraction_20: float | None = ...,
        water_vapor_diffusion_resistance_factor_20: float | None = ...,
        relative_humidity_fraction_21: float | None = ...,
        water_vapor_diffusion_resistance_factor_21: float | None = ...,
        relative_humidity_fraction_22: float | None = ...,
        water_vapor_diffusion_resistance_factor_22: float | None = ...,
        relative_humidity_fraction_23: float | None = ...,
        water_vapor_diffusion_resistance_factor_23: float | None = ...,
        relative_humidity_fraction_24: float | None = ...,
        water_vapor_diffusion_resistance_factor_24: float | None = ...,
        relative_humidity_fraction_25: float | None = ...,
        water_vapor_diffusion_resistance_factor_25: float | None = ...,
    ) -> None: ...

class MaterialPropertyHeatAndMoistureTransferDiffusion:
    def __call__(
        self,
        /,
        *,
        material_name: str,
        number_of_data_pairs: int,
        relative_humidity_fraction_1: float,
        water_vapor_diffusion_resistance_factor_1: float,
        relative_humidity_fraction_2: float | None = ...,
        water_vapor_diffusion_resistance_factor_2: float | None = ...,
        relative_humidity_fraction_3: float | None = ...,
        water_vapor_diffusion_resistance_factor_3: float | None = ...,
        relative_humidity_fraction_4: float | None = ...,
        water_vapor_diffusion_resistance_factor_4: float | None = ...,
        relative_humidity_fraction_5: float | None = ...,
        water_vapor_diffusion_resistance_factor_5: float | None = ...,
        relative_humidity_fraction_6: float | None = ...,
        water_vapor_diffusion_resistance_factor_6: float | None = ...,
        relative_humidity_fraction_7: float | None = ...,
        water_vapor_diffusion_resistance_factor_7: float | None = ...,
        relative_humidity_fraction_8: float | None = ...,
        water_vapor_diffusion_resistance_factor_8: float | None = ...,
        relative_humidity_fraction_9: float | None = ...,
        water_vapor_diffusion_resistance_factor_9: float | None = ...,
        relative_humidity_fraction_10: float | None = ...,
        water_vapor_diffusion_resistance_factor_10: float | None = ...,
        relative_humidity_fraction_11: float | None = ...,
        water_vapor_diffusion_resistance_factor_11: float | None = ...,
        relative_humidity_fraction_12: float | None = ...,
        water_vapor_diffusion_resistance_factor_12: float | None = ...,
        relative_humidity_fraction_13: float | None = ...,
        water_vapor_diffusion_resistance_factor_13: float | None = ...,
        relative_humidity_fraction_14: float | None = ...,
        water_vapor_diffusion_resistance_factor_14: float | None = ...,
        relative_humidity_fraction_15: float | None = ...,
        water_vapor_diffusion_resistance_factor_15: float | None = ...,
        relative_humidity_fraction_16: float | None = ...,
        water_vapor_diffusion_resistance_factor_16: float | None = ...,
        relative_humidity_fraction_17: float | None = ...,
        water_vapor_diffusion_resistance_factor_17: float | None = ...,
        relative_humidity_fraction_18: float | None = ...,
        water_vapor_diffusion_resistance_factor_18: float | None = ...,
        relative_humidity_fraction_19: float | None = ...,
        water_vapor_diffusion_resistance_factor_19: float | None = ...,
        relative_humidity_fraction_20: float | None = ...,
        water_vapor_diffusion_resistance_factor_20: float | None = ...,
        relative_humidity_fraction_21: float | None = ...,
        water_vapor_diffusion_resistance_factor_21: float | None = ...,
        relative_humidity_fraction_22: float | None = ...,
        water_vapor_diffusion_resistance_factor_22: float | None = ...,
        relative_humidity_fraction_23: float | None = ...,
        water_vapor_diffusion_resistance_factor_23: float | None = ...,
        relative_humidity_fraction_24: float | None = ...,
        water_vapor_diffusion_resistance_factor_24: float | None = ...,
        relative_humidity_fraction_25: float | None = ...,
        water_vapor_diffusion_resistance_factor_25: float | None = ...,
    ) -> None: ...

class BuildingSurfaceDetailed:
    def __call__(
        self,
        name: str,
        /,
        *,
        surface_type: Literal["Ceiling", "Floor", "Roof", "Wall"],
        zone_name: str,
        outside_boundary_condition: Literal[
            "Adiabatic",
            "Foundation",
            "Ground",
            "GroundBasementPreprocessorAverageFloor",
            "GroundBasementPreprocessorAverageWall",
            "GroundBasementPreprocessorLowerWall",
            "GroundBasementPreprocessorUpperWall",
            "GroundFCfactorMethod",
            "GroundSlabPreprocessorAverage",
            "GroundSlabPreprocessorCore",
            "GroundSlabPreprocessorPerimeter",
            "OtherSideCoefficients",
            "OtherSideConditionsModel",
            "Outdoors",
            "Space",
            "Surface",
            "Zone",
        ],
        construction_name: str | None = ...,
        space_name: str | None = ...,
        outside_boundary_condition_object: str | None = ...,
        sun_exposure: Literal["", "NoSun", "SunExposed"] | None = "SunExposed",
        wind_exposure: Literal["", "NoWind", "WindExposed"] | None = "WindExposed",
        view_factor_to_ground: float | Literal["", "Autocalculate"] | None = "Autocalculate",
        number_of_vertices: float | Literal["", "Autocalculate"] | None = "Autocalculate",
        vertices: list[Any] = ...,
    ) -> None: ...

class AnyWallDetailed:
    def __call__(
        self,
        name: str,
        /,
        *,
        construction_name: str,
        zone_name: str,
        outside_boundary_condition: Literal[
            "Adiabatic",
            "Foundation",
            "Ground",
            "GroundBasementPreprocessorAverageFloor",
            "GroundBasementPreprocessorAverageWall",
            "GroundBasementPreprocessorLowerWall",
            "GroundBasementPreprocessorUpperWall",
            "GroundFCfactorMethod",
            "GroundSlabPreprocessorAverage",
            "GroundSlabPreprocessorCore",
            "GroundSlabPreprocessorPerimeter",
            "OtherSideCoefficients",
            "OtherSideConditionsModel",
            "Outdoors",
            "Surface",
            "Zone",
        ],
        outside_boundary_condition_object: str | None = ...,
        sun_exposure: Literal["", "NoSun", "SunExposed"] | None = "SunExposed",
        wind_exposure: Literal["", "NoWind", "WindExposed"] | None = "WindExposed",
        view_factor_to_ground: float | Literal["", "Autocalculate"] | None = "Autocalculate",
        number_of_vertices: float | Literal["", "Autocalculate"] | None = "Autocalculate",
        vertices: list[Any] = ...,
    ) -> None: ...

class AnyFloorDetailed:
    def __call__(
        self,
        name: str,
        /,
        *,
        construction_name: str,
        zone_name: str,
        outside_boundary_condition: Literal[
            "Adiabatic",
            "Foundation",
            "Ground",
            "GroundBasementPreprocessorAverageFloor",
            "GroundBasementPreprocessorAverageWall",
            "GroundBasementPreprocessorLowerWall",
            "GroundBasementPreprocessorUpperWall",
            "GroundFCfactorMethod",
            "GroundSlabPreprocessorAverage",
            "GroundSlabPreprocessorCore",
            "GroundSlabPreprocessorPerimeter",
            "OtherSideCoefficients",
            "OtherSideConditionsModel",
            "Outdoors",
            "Surface",
            "Zone",
        ],
        outside_boundary_condition_object: str | None = ...,
        sun_exposure: Literal["", "NoSun", "SunExposed"] | None = "SunExposed",
        wind_exposure: Literal["", "NoWind", "WindExposed"] | None = "WindExposed",
        view_factor_to_ground: float | Literal["", "Autocalculate"] | None = "Autocalculate",
        number_of_vertices: float | Literal["", "Autocalculate"] | None = "Autocalculate",
        vertices: list[Any] = ...,
    ) -> None: ...

class AnyWallUnderground:
    def __call__(
        self,
        name: str,
        /,
        *,
        construction_name: str,
        zone_name: str,
        azimuth_angle: float | None = ...,
        tilt_angle: float | None = 90,
        starting_x_coordinate: float | None = ...,
        starting_y_coordinate: float | None = ...,
        starting_z_coordinate: float | None = ...,
        length: float | None = ...,
        height: float | None = ...,
    ) -> None: ...

class AnyFloorGroundContact:
    def __call__(
        self,
        name: str,
        /,
        *,
        construction_name: str,
        zone_name: str,
        azimuth_angle: float | None = ...,
        tilt_angle: float | None = 180,
        starting_x_coordinate: float | None = ...,
        starting_y_coordinate: float | None = ...,
        starting_z_coordinate: float | None = ...,
        length: float | None = ...,
        width: float | None = ...,
    ) -> None: ...

class AnyWindow:
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

class Door:
    def __call__(
        self,
        name: str,
        /,
        *,
        construction_name: str,
        building_surface_name: str,
        multiplier: float | None = 1,
        starting_x_coordinate: float | None = ...,
        starting_z_coordinate: float | None = ...,
        length: float | None = ...,
        height: float | None = ...,
    ) -> None: ...

class WindowPropertyAirflowControl:
    def __call__(
        self,
        name: str,
        /,
        *,
        airflow_source: Literal["", "IndoorAir", "OutdoorAir"] | None = "IndoorAir",
        airflow_destination: Literal["", "IndoorAir", "OutdoorAir", "ReturnAir"] | None = "OutdoorAir",
        maximum_flow_rate: float | None = 0,
        airflow_control_type: Literal["", "AlwaysOff", "AlwaysOnAtMaximumFlow", "ScheduledOnly"]
        | None = "AlwaysOnAtMaximumFlow",
        airflow_is_scheduled: Literal["", "No", "Yes"] | None = "No",
        airflow_multiplier_schedule_name: str | None = ...,
        airflow_return_air_node_name: str | None = ...,
    ) -> None: ...

class ShadingOverhang:
    def __call__(
        self,
        name: str,
        /,
        *,
        window_or_door_name: str,
        height_above_window_or_door: float | None = ...,
        tilt_angle_from_window_door: float | None = 90,
        left_extension_from_window_door_width: float | None = ...,
        right_extension_from_window_door_width: float | None = ...,
        depth: float | None = ...,
    ) -> None: ...

class GroundHeatTransferBasementInterior:
    def __call__(
        self,
        /,
        *,
        cond_flag_is_the_basement_conditioned_: Literal["", "FALSE", "TRUE"] | None = "TRUE",
        hin_downward_convection_only_heat_transfer_coefficient: float | None = 0.92,
        hin_upward_convection_only_heat_transfer_coefficient: float | None = 4.04,
        hin_horizontal_convection_only_heat_transfer_coefficient: float | None = 3.08,
        hin_downward_combined_convection_and_radiation_heat_transfer_coefficient: float | None = 6.13,
        hin_upward_combined_convection_and_radiation_heat_transfer_coefficient: float | None = 9.26,
        hin_horizontal_combined_convection_and_radiation_heat_transfer_coefficient: float | None = 8.29,
        cond_flag_is_the_basement_conditioned: Literal["", "FALSE", "TRUE"] | None = ...,
    ) -> None: ...

class RoomAirNodeAirflowNetworkInternalGains:
    def __call__(self, name: str = "", /, *, gains: list[Any] = ...) -> None: ...

class AnyZoneBaseboardOutdoorTemperatureControlled:
    def __call__(
        self,
        name: str,
        /,
        *,
        narrow_with_as_version_first: Never,
        schedule_name: str,
        capacity_at_low_temperature: float,
        low_temperature: float,
        capacity_at_high_temperature: float,
        high_temperature: float,
        fraction_radiant: float | None = 0,
        end_use_subcategory: str | None = "General",
    ) -> None: ...

class AnyZoneInfiltrationDesignFlowRate:
    def __call__(
        self,
        name: str,
        /,
        *,
        narrow_with_as_version_first: Never,
        schedule_name: str,
        design_flow_rate_calculation_method: Literal[
            "", "AirChanges/Hour", "Flow/Area", "Flow/ExteriorArea", "Flow/ExteriorWallArea", "Flow/Zone"
        ]
        | None = "Flow/Zone",
        design_flow_rate: float | None = ...,
        air_changes_per_hour: float | None = ...,
        constant_term_coefficient: float | None = 1,
        temperature_term_coefficient: float | None = 0,
        velocity_term_coefficient: float | None = 0,
        velocity_squared_term_coefficient: float | None = 0,
    ) -> None: ...

class AnyZoneMixing:
    def __call__(
        self,
        name: str,
        /,
        *,
        narrow_with_as_version_first: Never,
        schedule_name: str,
        design_flow_rate_calculation_method: Literal["", "AirChanges/Hour", "Flow/Area", "Flow/Person", "Flow/Zone"]
        | None = "Flow/Zone",
        design_flow_rate: float | None = ...,
        flow_rate_per_person: float | None = ...,
        air_changes_per_hour: float | None = ...,
        delta_temperature: float | None = 0,
        delta_temperature_schedule_name: str | None = ...,
        minimum_outdoor_temperature_schedule_name: str | None = ...,
        maximum_outdoor_temperature_schedule_name: str | None = ...,
    ) -> None: ...

class DesignSpecificationAirTerminalSizing:
    def __call__(
        self,
        name: str,
        /,
        *,
        fraction_of_design_cooling_load: float | None = 1,
        cooling_design_supply_air_temperature_difference_ratio: float | None = 1,
        fraction_of_design_heating_load: float | None = 1,
        heating_design_supply_air_temperature_difference_ratio: float | None = 1,
        fraction_of_minimum_outdoor_air_flow: float | None = 1,
    ) -> None: ...

class ZoneHVACWindowAirConditioner:
    def __call__(
        self,
        name: str,
        /,
        *,
        maximum_supply_air_flow_rate: float | Literal["Autosize"],
        maximum_outdoor_air_flow_rate: float | Literal["Autosize"],
        air_inlet_node_name: str,
        air_outlet_node_name: str,
        outdoor_air_mixer_object_type: Literal["OutdoorAir:Mixer"],
        outdoor_air_mixer_name: str,
        supply_air_fan_object_type: Literal["Fan:ConstantVolume", "Fan:OnOff", "Fan:SystemModel"],
        supply_air_fan_name: str,
        cooling_coil_object_type: Literal[
            "Coil:Cooling:DX:SingleSpeed",
            "Coil:Cooling:DX:VariableSpeed",
            "CoilSystem:Cooling:DX:HeatExchangerAssisted",
        ],
        dx_cooling_coil_name: str,
        fan_placement: Literal["BlowThrough", "DrawThrough"],
        availability_schedule_name: str | None = ...,
        supply_air_fan_operating_mode_schedule_name: str | None = ...,
        cooling_convergence_tolerance: float | None = 0.001,
        availability_manager_list_name: str | None = ...,
        design_specification_zonehvac_sizing_object_name: str | None = ...,
    ) -> None: ...

class AirTerminalDualDuctVAV:
    def __call__(
        self,
        name: str,
        /,
        *,
        air_outlet_node_name: str,
        hot_air_inlet_node_name: str,
        cold_air_inlet_node_name: str,
        maximum_damper_air_flow_rate: float | Literal["Autosize"],
        availability_schedule_name: str | None = ...,
        zone_minimum_air_flow_fraction: float | None = 0.2,
        design_specification_outdoor_air_object_name: str | None = ...,
        minimum_air_flow_turndown_schedule_name: str | None = ...,
    ) -> None: ...

class EvaporativeCoolerIndirectResearchSpecial:
    def __call__(
        self,
        name: str = "",
        /,
        *,
        cooler_wetbulb_design_effectiveness: float,
        primary_air_inlet_node_name: str,
        primary_air_outlet_node_name: str,
        secondary_air_inlet_node_name: str,
        secondary_air_outlet_node_name: str,
        sensor_node_name: str,
        availability_schedule_name: str | None = ...,
        wetbulb_effectiveness_flow_ratio_modifier_curve_name: str | None = ...,
        cooler_drybulb_design_effectiveness: float | None = ...,
        drybulb_effectiveness_flow_ratio_modifier_curve_name: str | None = ...,
        recirculating_water_pump_design_power: float | Literal["", "Autosize"] | None = "Autosize",
        water_pump_power_sizing_factor: float | None = 90,
        water_pump_power_modifier_curve_name: str | None = ...,
        secondary_air_design_flow_rate: float | Literal["", "Autosize"] | None = "Autosize",
        secondary_air_flow_scaling_factor: float | None = 1,
        secondary_air_fan_design_power: float | Literal["", "Autosize"] | None = "Autosize",
        secondary_air_fan_sizing_specific_power: float | None = 250,
        secondary_air_fan_power_modifier_curve_name: str | None = ...,
        primary_air_design_flow_rate: float | Literal["", "Autosize"] | None = "Autosize",
        dewpoint_effectiveness_factor: float | None = ...,
        relief_air_inlet_node_name: str | None = ...,
        water_supply_storage_tank_name: str | None = ...,
        drift_loss_fraction: float | None = 0,
        blowdown_concentration_ratio: float | None = ...,
        evaporative_operation_minimum_limit_secondary_air_drybulb_temperature: float | None = ...,
        evaporative_operation_maximum_limit_outdoor_wetbulb_temperature: float | None = ...,
        dry_operation_maximum_limit_outdoor_drybulb_temperature: float | None = ...,
    ) -> None: ...

class AnyBoilerHotWater:
    def __call__(
        self,
        name: str,
        /,
        *,
        fuel_type: Literal[
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
        ],
        nominal_thermal_efficiency: float,
        boiler_water_inlet_node_name: str,
        boiler_water_outlet_node_name: str,
        nominal_capacity: float | Literal["Autosize"] | None = ...,
        efficiency_curve_temperature_evaluation_variable: Literal["EnteringBoiler", "LeavingBoiler"] | None = ...,
        normalized_boiler_efficiency_curve_name: str | None = ...,
        design_water_flow_rate: float | Literal["Autosize"] | None = ...,
        minimum_part_load_ratio: float | None = 0,
        maximum_part_load_ratio: float | None = 1,
        optimum_part_load_ratio: float | None = 1,
        water_outlet_upper_temperature_limit: float | None = 99.9,
        boiler_flow_mode: Literal["", "ConstantFlow", "LeavingSetpointModulated", "NotModulated"]
        | None = "NotModulated",
        sizing_factor: float | None = 1,
        end_use_subcategory: str | None = "General",
    ) -> None: ...

class HeatPumpPlantLoopEIRCooling:
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
        heat_recovery_inlet_node_name: str | None = ...,
        heat_recovery_outlet_node_name: str | None = ...,
        companion_heat_pump_name: str | None = ...,
        load_side_reference_flow_rate: float | Literal["", "Autosize"] | None = "Autosize",
        source_side_reference_flow_rate: float | Literal["", "Autosize"] | None = "Autosize",
        heat_recovery_reference_flow_rate: float | Literal["", "Autosize"] | None = "Autosize",
        reference_capacity: float | Literal["", "Autosize"] | None = "Autosize",
        reference_coefficient_of_performance: float | None = 3,
        sizing_factor: float | None = 1,
        control_type: Literal["", "Load", "Setpoint"] | None = "Load",
        flow_mode: Literal["", "ConstantFlow", "VariableSpeedPumping"] | None = "ConstantFlow",
        minimum_part_load_ratio: float | None = 0,
        minimum_source_inlet_temperature: float | None = -100,
        maximum_source_inlet_temperature: float | None = 100,
        minimum_supply_water_temperature_curve_name: str | None = ...,
        maximum_supply_water_temperature_curve_name: str | None = ...,
        maximum_heat_recovery_outlet_temperature: float | None = 60,
        heat_recovery_capacity_modifier_function_of_temperature_curve_name: str | None = ...,
        heat_recovery_electric_input_to_output_ratio_modifier_function_of_temperature_curve_name: str | None = ...,
        thermosiphon_capacity_fraction_curve_name: str | None = ...,
        thermosiphon_minimum_temperature_difference: float | None = 0,
    ) -> None: ...

class AnyCoolingTowerVariableSpeedMerkel:
    def __call__(
        self,
        name: str,
        /,
        *,
        water_inlet_node_name: str,
        water_outlet_node_name: str,
        design_water_flow_rate: float | Literal["Autosize"],
        design_air_flow_rate: float | Literal["Autocalculate"],
        design_fan_power: float | Literal["Autocalculate"],
        fan_power_modifier_function_of_air_flow_rate_ratio_curve_name: str,
        u_factor_times_area_modifier_function_of_air_flow_ratio_curve_name: str,
        u_factor_times_area_modifier_function_of_wetbulb_temperature_difference_curve_name: str,
        u_factor_times_area_modifier_function_of_water_flow_ratio_curve_name: str,
        performance_input_method: Literal["", "NominalCapacity", "UFactorTimesAreaAndDesignWaterFlowRate"]
        | None = "NominalCapacity",
        heat_rejection_capacity_and_nominal_capacity_sizing_ratio: float | None = 1.25,
        nominal_capacity: float | Literal["Autosize"] | None = ...,
        free_convection_nominal_capacity: float | Literal["Autocalculate"] | None = ...,
        free_convection_nominal_capacity_sizing_factor: float | None = 0.1,
        design_water_flow_rate_per_unit_of_nominal_capacity: float | None = ...,
        design_air_flow_rate_per_unit_of_nominal_capacity: float | None = ...,
        minimum_air_flow_rate_ratio: float | None = 0.2,
        design_fan_power_per_unit_of_nominal_capacity: float | None = 0.0105,
        free_convection_regime_air_flow_rate: float | Literal["", "Autocalculate"] | None = 0,
        free_convection_regime_air_flow_rate_sizing_factor: float | None = 0.1,
        design_air_flow_rate_u_factor_times_area_value: float | Literal["Autosize"] | None = ...,
        free_convection_regime_u_factor_times_area_value: float | Literal["", "Autocalculate"] | None = 0,
        free_convection_u_factor_times_area_value_sizing_factor: float | None = 0.1,
        design_inlet_air_dry_bulb_temperature: float | None = 35,
        design_inlet_air_wet_bulb_temperature: float | None = 25.6,
        design_approach_temperature: float | Literal["", "Autosize"] | None = "Autosize",
        design_range_temperature: float | Literal["", "Autosize"] | None = "Autosize",
        basin_heater_capacity: float | None = 0,
        basin_heater_setpoint_temperature: float | None = 2,
        basin_heater_operating_schedule_name: str | None = ...,
        evaporation_loss_mode: Literal["LossFactor", "SaturatedExit"] | None = ...,
        evaporation_loss_factor: float | None = 0.2,
        drift_loss_percent: float | None = 0.008,
        blowdown_calculation_mode: Literal["ConcentrationRatio", "ScheduledRate"] | None = ...,
        blowdown_concentration_ratio: float | None = 3,
        blowdown_makeup_water_usage_schedule_name: str | None = ...,
        supply_water_storage_tank_name: str | None = ...,
        outdoor_air_inlet_node_name: str | None = ...,
        number_of_cells: int | None = 1,
        cell_control: Literal["", "MaximalCell", "MinimalCell"] | None = ...,
        cell_minimum_water_flow_rate_fraction: float | None = 0.33,
        cell_maximum_water_flow_rate_fraction: float | None = 2.5,
        sizing_factor: float | None = 1,
        end_use_subcategory: str | None = "General",
    ) -> None: ...

class WaterHeaterSizing:
    def __call__(
        self,
        /,
        *,
        waterheater_name: str,
        design_mode: Literal[
            "PeakDraw", "PerFloorArea", "PerPerson", "PerSolarCollectorArea", "PerUnit", "ResidentialHUD-FHAMinimum"
        ]
        | None = ...,
        time_storage_can_meet_peak_draw: float | None = ...,
        time_for_tank_recovery: float | None = ...,
        nominal_tank_volume_for_autosizing_plant_connections: float | None = ...,
        number_of_bedrooms: int | None = ...,
        number_of_bathrooms: int | None = ...,
        storage_capacity_per_person: float | None = ...,
        recovery_capacity_per_person: float | None = ...,
        storage_capacity_per_floor_area: float | None = ...,
        recovery_capacity_per_floor_area: float | None = ...,
        number_of_units: float | None = ...,
        storage_capacity_per_unit: float | None = ...,
        recovery_capacity_perunit: float | None = ...,
        storage_capacity_per_collector_area: float | None = ...,
        height_aspect_ratio: float | None = ...,
    ) -> None: ...

class WaterHeaterHeatPumpWrappedCondenser:
    def __call__(
        self,
        name: str,
        /,
        *,
        compressor_setpoint_temperature_schedule_name: str,
        condenser_top_location: float,
        inlet_air_configuration: Literal["OutdoorAirOnly", "Schedule", "ZoneAirOnly", "ZoneAndOutdoorAir"],
        tank_name: str,
        dx_coil_name: str,
        compressor_location: Literal["Outdoors", "Schedule", "Zone"],
        fan_name: str,
        availability_schedule_name: str | None = ...,
        dead_band_temperature_difference: float | None = 5,
        condenser_bottom_location: float | None = 0,
        evaporator_air_flow_rate: float | Literal["Autocalculate"] | None = ...,
        air_inlet_node_name: str | None = ...,
        air_outlet_node_name: str | None = ...,
        outdoor_air_node_name: str | None = ...,
        exhaust_air_node_name: str | None = ...,
        inlet_air_temperature_schedule_name: str | None = ...,
        inlet_air_humidity_schedule_name: str | None = ...,
        inlet_air_zone_name: str | None = ...,
        tank_object_type: Literal["", "WaterHeater:Stratified"] | None = "WaterHeater:Stratified",
        tank_use_side_inlet_node_name: str | None = ...,
        tank_use_side_outlet_node_name: str | None = ...,
        dx_coil_object_type: Literal["", "Coil:WaterHeating:AirToWaterHeatPump:Wrapped"] | None = ...,
        minimum_inlet_air_temperature_for_compressor_operation: float | None = 10,
        maximum_inlet_air_temperature_for_compressor_operation: float | None = 48.88888888889,
        compressor_ambient_temperature_schedule_name: str | None = ...,
        fan_object_type: Literal["", "Fan:OnOff", "Fan:SystemModel"] | None = "Fan:OnOff",
        fan_placement: Literal["", "BlowThrough", "DrawThrough"] | None = "DrawThrough",
        on_cycle_parasitic_electric_load: float | None = 0,
        off_cycle_parasitic_electric_load: float | None = 0,
        parasitic_heat_rejection_location: Literal["", "Outdoors", "Zone"] | None = "Outdoors",
        inlet_air_mixer_node_name: str | None = ...,
        outlet_air_splitter_node_name: str | None = ...,
        inlet_air_mixer_schedule_name: str | None = ...,
        tank_element_control_logic: Literal["", "MutuallyExclusive", "Simultaneous"] | None = "Simultaneous",
        control_sensor_1_height_in_stratified_tank: float | None = ...,
        control_sensor_1_weight: float | None = 1,
        control_sensor_2_height_in_stratified_tank: float | None = ...,
    ) -> None: ...

class EnergyManagementSystemSensor:
    def __call__(
        self,
        name: str,
        /,
        *,
        output_variable_or_output_meter_name: str,
        output_variable_or_output_meter_index_key_name: str | None = ...,
    ) -> None: ...

class EnergyManagementSystemActuator:
    def __call__(
        self,
        name: str,
        /,
        *,
        actuated_component_unique_name: str,
        actuated_component_type: str,
        actuated_component_control_type: str,
    ) -> None: ...

class EnergyManagementSystemConstructionIndexVariable:
    def __call__(self, name: str, /, *, construction_object_name: str) -> None: ...

class AnyExternalInterfaceFunctionalMockupUnitExportToSchedule:
    def __call__(
        self,
        /,
        *,
        schedule_name: str,
        fmu_variable_name: str,
        initial_value: float,
        schedule_type_limits_names: str | None = ...,
    ) -> None: ...

class SetpointManagerScheduledDualSetpoint:
    def __call__(
        self,
        name: str,
        /,
        *,
        high_setpoint_schedule_name: str,
        low_setpoint_schedule_name: str,
        setpoint_node_or_nodelist_name: str,
        control_variable: Literal["", "Temperature"] | None = "Temperature",
    ) -> None: ...

class SetpointManagerSingleZoneCooling:
    def __call__(
        self,
        name: str,
        /,
        *,
        control_zone_name: str,
        zone_node_name: str,
        zone_inlet_node_name: str,
        setpoint_node_or_nodelist_name: str,
        control_variable: Literal["", "Temperature"] | None = "Temperature",
        minimum_supply_air_temperature: float | None = -99,
        maximum_supply_air_temperature: float | None = 99,
    ) -> None: ...

class SetpointManagerSingleZoneHumidityMinimum:
    def __call__(
        self, name: str, /, *, setpoint_node_or_nodelist_name: str, control_zone_air_node_name: str
    ) -> None: ...

class SetpointManagerMixedAir:
    def __call__(
        self,
        name: str,
        /,
        *,
        reference_setpoint_node_name: str,
        fan_inlet_node_name: str,
        fan_outlet_node_name: str,
        setpoint_node_or_nodelist_name: str,
        control_variable: Literal["", "Temperature"] | None = "Temperature",
        cooling_coil_inlet_node_name: str | None = ...,
        cooling_coil_outlet_node_name: str | None = ...,
        minimum_temperature_at_cooling_coil_outlet_node: float | None = 7.2,
    ) -> None: ...

class RefrigerationTranscriticalSystem:
    def __call__(
        self,
        name: str,
        /,
        *,
        system_type: Literal["SingleStage", "TwoStage"],
        medium_temperature_refrigerated_case_or_walkin_or_caseandwalkinlist_name: str,
        refrigeration_gas_cooler_name: str,
        high_pressure_compressor_or_compressorlist_name: str,
        refrigeration_system_working_fluid_type: str,
        low_temperature_refrigerated_case_or_walkin_or_caseandwalkinlist_name: str | None = ...,
        low_pressure_compressor_or_compressorlist_name: str | None = ...,
        receiver_pressure: float | None = 4000000,
        subcooler_effectiveness: float | None = 0.4,
        sum_ua_suction_piping_for_medium_temperature_loads: float | None = 0,
        medium_temperature_suction_piping_zone_name: str | None = ...,
        sum_ua_suction_piping_for_low_temperature_loads: float | None = 0,
        low_temperature_suction_piping_zone_name: str | None = ...,
        end_use_subcategory: str | None = "General",
    ) -> None: ...

class AnyRefrigerationSecondarySystem:
    def __call__(
        self,
        name: str,
        /,
        *,
        refrigerated_case_or_walkin_or_caseandwalkinlist_name: str,
        circulating_fluid_type: Literal["FluidAlwaysLiquid", "FluidPhaseChange"],
        circulating_fluid_name: str,
        evaporator_evaporating_temperature: float,
        evaporator_approach_temperature_difference: float,
        evaporator_capacity: float | None = ...,
        evaporator_flow_rate_for_secondary_fluid: float | None = ...,
        evaporator_range_temperature_difference: float | None = ...,
        number_of_pumps_in_loop: int | None = 1,
        total_pump_flow_rate: float | None = ...,
        total_pump_power: float | None = ...,
        total_pump_head: float | None = ...,
        phasechange_circulating_rate: float | None = 2.5,
        pump_drive_type: Literal["", "Constant", "Variable"] | None = "Constant",
        variable_speed_pump_cubic_curve_name: str | None = ...,
        pump_motor_heat_to_fluid: float | None = 0.85,
        sum_ua_distribution_piping: float | None = 0,
        distribution_piping_zone_name: str | None = ...,
        sum_ua_receiver_separator_shell: float | None = 0,
        receiver_separator_zone_name: str | None = ...,
        evaporator_refrigerant_inventory: float | None = 0,
        end_use_subcategory: str | None = "General",
    ) -> None: ...

class DemandManagerLights:
    def __call__(
        self,
        name: str,
        /,
        *,
        limit_control: Literal["Fixed", "Off"],
        selection_control: Literal["All", "RotateMany", "RotateOne"],
        availability_schedule_name: str | None = ...,
        minimum_limit_duration: int | None = ...,
        maximum_limit_fraction: float | None = ...,
        limit_step_change: float | None = ...,
        rotation_duration: int | None = ...,
        lights: list[Any] = ...,
    ) -> None: ...

class FaultModelHumiditySensorOffsetOutdoorAir:
    def __call__(
        self,
        name: str,
        /,
        *,
        controller_object_type: Literal["Controller:OutdoorAir"],
        controller_object_name: str,
        availability_schedule_name: str | None = ...,
        severity_schedule_name: str | None = ...,
        humidity_sensor_offset: float | None = 0,
    ) -> None: ...

class CurveQuadLinear:
    def __call__(
        self,
        name: str,
        /,
        *,
        coefficient1_constant: float,
        coefficient2_w: float,
        coefficient3_x: float,
        coefficient4_y: float,
        coefficient5_z: float,
        minimum_value_of_w: float,
        maximum_value_of_w: float,
        minimum_value_of_x: float,
        maximum_value_of_x: float,
        minimum_value_of_y: float,
        maximum_value_of_y: float,
        minimum_value_of_z: float,
        maximum_value_of_z: float,
        minimum_curve_output: float | None = ...,
        maximum_curve_output: float | None = ...,
        input_unit_type_for_w: Literal[
            "",
            "Dimensionless",
            "Distance",
            "MassFlow",
            "Power",
            "Temperature",
            "VolumetricFlow",
            "VolumetricFlowPerPower",
        ]
        | None = "Dimensionless",
        input_unit_type_for_x: Literal[
            "",
            "Dimensionless",
            "Distance",
            "MassFlow",
            "Power",
            "Temperature",
            "VolumetricFlow",
            "VolumetricFlowPerPower",
        ]
        | None = "Dimensionless",
        input_unit_type_for_y: Literal[
            "",
            "Dimensionless",
            "Distance",
            "MassFlow",
            "Power",
            "Temperature",
            "VolumetricFlow",
            "VolumetricFlowPerPower",
        ]
        | None = "Dimensionless",
        input_unit_type_for_z: Literal[
            "",
            "Dimensionless",
            "Distance",
            "MassFlow",
            "Power",
            "Temperature",
            "VolumetricFlow",
            "VolumetricFlowPerPower",
        ]
        | None = "Dimensionless",
    ) -> None: ...

class UtilityCostComputation:
    def __call__(
        self,
        name: str,
        /,
        *,
        tariff_name: str,
        compute_step_1: str | None = ...,
        compute_step_2: str | None = ...,
        compute_step_3: str | None = ...,
        compute_step_4: str | None = ...,
        compute_step_5: str | None = ...,
        compute_step_6: str | None = ...,
        compute_step_7: str | None = ...,
        compute_step_8: str | None = ...,
        compute_step_9: str | None = ...,
        compute_step_10: str | None = ...,
        compute_step_11: str | None = ...,
        compute_step_12: str | None = ...,
        compute_step_13: str | None = ...,
        compute_step_14: str | None = ...,
        compute_step_15: str | None = ...,
        compute_step_16: str | None = ...,
        compute_step_17: str | None = ...,
        compute_step_18: str | None = ...,
        compute_step_19: str | None = ...,
        compute_step_20: str | None = ...,
        compute_step_21: str | None = ...,
        compute_step_22: str | None = ...,
        compute_step_23: str | None = ...,
        compute_step_24: str | None = ...,
        compute_step_25: str | None = ...,
        compute_step_26: str | None = ...,
        compute_step_27: str | None = ...,
        compute_step_28: str | None = ...,
        compute_step_29: str | None = ...,
        compute_step_30: str | None = ...,
    ) -> None: ...

class OutputVariableDictionary:
    def __call__(
        self,
        /,
        *,
        key_field: Literal["", "IDF", "regular"] | None = "regular",
        sort_option: Literal["Name", "Unsorted"] | None = ...,
    ) -> None: ...

class OutputTableTimeBins:
    def __call__(
        self,
        /,
        *,
        variable_name: str,
        key_value: str | None = "*",
        interval_start: float | None = ...,
        interval_size: float | None = ...,
        interval_count: int | None = ...,
        schedule_name: str | None = ...,
        variable_type: Literal["Energy", "Power", "Temperature", "VolumetricFlow"] | None = ...,
    ) -> None: ...

class AnyMeterCustomDecrement:
    def __call__(self, name: str, /, *, source_meter_name: str, variable_details: list[Any] = ...) -> None: ...

class PythonPluginSearchPaths:
    def __call__(
        self,
        name: str,
        /,
        *,
        add_current_working_directory_to_search_path: Literal["", "No", "Yes"] | None = "Yes",
        add_input_file_directory_to_search_path: Literal["", "No", "Yes"] | None = "Yes",
        add_epin_environment_variable_to_search_path: Literal["", "No", "Yes"] | None = "Yes",
        py_search_paths: list[Any] = ...,
    ) -> None: ...
