"""Creation signatures of generated classes (stub only).

DO NOT EDIT — regenerate with:
    python -m idfkit.codegen.generate_stubs
"""

from __future__ import annotations

from typing import Literal

from typing_extensions import Never

from .. import _generated_types as _g

class AnyConvergenceLimits:
    def __call__(
        self,
        /,
        *,
        minimum_system_timestep: int | None = ...,
        maximum_hvac_iterations: int | None = 20,
        minimum_plant_iterations: int | None = 2,
        maximum_plant_iterations: int | None = 8,
    ) -> None: ...

class SitePrecipitation:
    def __call__(
        self,
        /,
        *,
        precipitation_model_type: Literal["ScheduleAndDesignLevel"] | None = ...,
        design_level_for_total_annual_precipitation: float | None = ...,
        precipitation_rates_schedule_name: str | None = ...,
        average_total_annual_precipitation: float | None = ...,
    ) -> None: ...

class SurfacePropertyOtherSideConditionsModel:
    def __call__(
        self,
        name: str,
        /,
        *,
        type_of_modeling: Literal[
            "",
            "ConvectiveUnderwater",
            "GapConvectionRadiation",
            "GroundCoupledSurface",
            "UndergroundPipingSystemSurface",
        ]
        | None = "GapConvectionRadiation",
    ) -> None: ...

class SurfacePropertyUnderwater:
    def __call__(
        self,
        name: str,
        /,
        *,
        distance_from_surface_centroid_to_leading_edge_of_boundary_layer: float,
        free_stream_water_temperature_schedule: str,
        free_stream_water_velocity_schedule: str | None = ...,
    ) -> None: ...

class AnySurfacePropertyConvectionCoefficientsMultipleSurface:
    def __call__(
        self,
        /,
        *,
        surface_type: Literal[
            "AllExteriorFloors",
            "AllExteriorRoofs",
            "AllExteriorSurfaces",
            "AllExteriorWalls",
            "AllExteriorWindows",
            "AllInteriorCeilings",
            "AllInteriorFloors",
            "AllInteriorSurfaces",
            "AllInteriorWalls",
            "AllInteriorWindows",
        ],
        convection_coefficient_1_location: Literal["Inside", "Outside"],
        convection_coefficient_1_type: Literal[
            "ASHRAEVerticalWall",
            "AdaptiveConvectionAlgorithm",
            "AlamdariHammondStableHorizontal",
            "AlamdariHammondUnstableHorizontal",
            "AlamdariHammondVerticalWall",
            "AwbiHattonHeatedFloor",
            "AwbiHattonHeatedWall",
            "BeausoleilMorrisonMixedAssistedWall",
            "BeausoleilMorrisonMixedOpposingWall",
            "BeausoleilMorrisonMixedStableCeiling",
            "BeausoleilMorrisonMixedStableFloor",
            "BeausoleilMorrisonMixedUnstableCeiling",
            "BeausoleilMorrisonMixedUnstableFloor",
            "BlockenWindard",
            "ClearRoof",
            "DOE-2",
            "EmmelRoof",
            "EmmelVertical",
            "FisherPedersenCeilingDiffuserCeiling",
            "FisherPedersenCeilingDiffuserFloor",
            "FisherPedersenCeilingDiffuserWalls",
            "FohannoPolidoriVerticalWall",
            "GoldsteinNovoselacCeilingDiffuserFloor",
            "GoldsteinNovoselacCeilingDiffuserWalls",
            "GoldsteinNovoselacCeilingDiffuserWindow",
            "ISO15099Windows",
            "KaradagChilledCeiling",
            "KhalifaEq3WallAwayFromHeat",
            "KhalifaEq4CeilingAwayFromHeat",
            "KhalifaEq5WallNearHeat",
            "KhalifaEq6NonHeatedWalls",
            "KhalifaEq7Ceiling",
            "McAdams",
            "Mitchell",
            "MoWitt",
            "NusseltJurges",
            "Schedule",
            "Simple",
            "SimpleCombined",
            "TARP",
            "UserCurve",
            "Value",
            "WaltonStableHorizontalOrTilt",
            "WaltonUnstableHorizontalOrTilt",
        ],
        convection_coefficient_1: float | None = ...,
        convection_coefficient_1_schedule_name: str | None = ...,
        convection_coefficient_1_user_curve_name: str | None = ...,
        convection_coefficient_2_location: Literal["Inside", "Outside"] | None = ...,
        convection_coefficient_2_type: Literal[
            "ASHRAEVerticalWall",
            "AdaptiveConvectionAlgorithm",
            "AlamdariHammondStableHorizontal",
            "AlamdariHammondUnstableHorizontal",
            "AlamdariHammondVerticalWall",
            "AwbiHattonHeatedFloor",
            "AwbiHattonHeatedWall",
            "BeausoleilMorrisonMixedAssistedWall",
            "BeausoleilMorrisonMixedOpposingWall",
            "BeausoleilMorrisonMixedStableCeiling",
            "BeausoleilMorrisonMixedStableFloor",
            "BeausoleilMorrisonMixedUnstableCeiling",
            "BeausoleilMorrisonMixedUnstableFloor",
            "BlockenWindard",
            "ClearRoof",
            "DOE-2",
            "EmmelRoof",
            "EmmelVertical",
            "FisherPedersenCeilingDiffuserCeiling",
            "FisherPedersenCeilingDiffuserFloor",
            "FisherPedersenCeilingDiffuserWalls",
            "FohannoPolidoriVerticalWall",
            "GoldsteinNovoselacCeilingDiffuserFloor",
            "GoldsteinNovoselacCeilingDiffuserWalls",
            "GoldsteinNovoselacCeilingDiffuserWindow",
            "ISO15099Windows",
            "KaradagChilledCeiling",
            "KhalifaEq3WallAwayFromHeat",
            "KhalifaEq4CeilingAwayFromHeat",
            "KhalifaEq5WallNearHeat",
            "KhalifaEq6NonHeatedWalls",
            "KhalifaEq7Ceiling",
            "McAdams",
            "Mitchell",
            "MoWitt",
            "NusseltJurges",
            "Schedule",
            "Simple",
            "SimpleCombined",
            "TARP",
            "UserCurve",
            "Value",
            "WaltonStableHorizontalOrTilt",
            "WaltonUnstableHorizontalOrTilt",
        ]
        | None = ...,
        convection_coefficient_2: float | None = 0.1,
        convection_coefficient_2_schedule_name: str | None = ...,
        convection_coefficient_2_user_curve_name: str | None = ...,
    ) -> None: ...

class AnyZoneInfiltrationEffectiveLeakageArea:
    def __call__(
        self,
        name: str,
        /,
        *,
        narrow_with_as_version_first: Never,
        schedule_name: str,
        effective_air_leakage_area: float,
        stack_coefficient: float,
        wind_coefficient: float,
    ) -> None: ...

class ZoneCrossMixing:
    def __call__(
        self,
        name: str,
        /,
        *,
        zone_or_space_name: str,
        source_zone_or_space_name: str,
        schedule_name: str | None = ...,
        design_flow_rate_calculation_method: Literal["", "AirChanges/Hour", "Flow/Area", "Flow/Person", "Flow/Zone"]
        | None = "Flow/Zone",
        design_flow_rate: float | None = ...,
        flow_rate_per_floor_area: float | None = ...,
        flow_rate_per_person: float | None = ...,
        air_changes_per_hour: float | None = ...,
        delta_temperature: float | None = 0,
        delta_temperature_schedule_name: str | None = ...,
        minimum_receiving_temperature_schedule_name: str | None = ...,
        maximum_receiving_temperature_schedule_name: str | None = ...,
        minimum_source_temperature_schedule_name: str | None = ...,
        maximum_source_temperature_schedule_name: str | None = ...,
        minimum_outdoor_temperature_schedule_name: str | None = ...,
        maximum_outdoor_temperature_schedule_name: str | None = ...,
    ) -> None: ...

class AnyZoneCoolTowerShower:
    def __call__(
        self,
        name: str,
        /,
        *,
        narrow_with_as_version_first: Never,
        pump_flow_rate_schedule_name: str,
        maximum_water_flow_rate: float,
        effective_tower_height: float,
        airflow_outlet_area: float,
        maximum_air_flow_rate: float,
        minimum_indoor_temperature: float,
        rated_power_consumption: float,
        availability_schedule_name: str | None = ...,
        water_supply_storage_tank_name: str | None = ...,
        flow_control_type: Literal["", "WaterFlowSchedule", "WindDrivenFlow"] | None = "WindDrivenFlow",
        fraction_of_water_loss: float | None = ...,
        fraction_of_flow_schedule: float | None = ...,
    ) -> None: ...

class AnyAirflowNetworkDistributionNode:
    def __call__(
        self,
        name: str,
        /,
        *,
        component_name_or_node_name: str | None = ...,
        component_object_type_or_node_type: Literal[
            "",
            "AirLoopHVAC:OutdoorAirSystem",
            "AirLoopHVAC:ZoneMixer",
            "AirLoopHVAC:ZoneSplitter",
            "OAMixerOutdoorAirStreamNode",
            "Other",
            "OutdoorAir:Node",
            "OutdoorAir:NodeList",
        ]
        | None = "Other",
        node_height: float | None = 0,
    ) -> None: ...

class ExteriorLights:
    def __call__(
        self,
        name: str,
        /,
        *,
        schedule_name: str,
        design_level: float,
        control_option: Literal["AstronomicalClock", "ScheduleNameOnly"] | None = ...,
        end_use_subcategory: str | None = "General",
    ) -> None: ...

class AnyHVACTemplateSystemVRF:
    def __call__(
        self,
        name: str,
        /,
        *,
        system_availability_schedule_name: str | None = ...,
        gross_rated_total_cooling_capacity: float | Literal["", "Autosize"] | None = "Autosize",
        gross_rated_cooling_cop: float | None = 3.3,
        minimum_outdoor_temperature_in_cooling_mode: float | None = -6,
        maximum_outdoor_temperature_in_cooling_mode: float | None = 43,
        gross_rated_heating_capacity: float | Literal["", "Autosize"] | None = "Autosize",
        rated_heating_capacity_sizing_ratio: float | None = 1,
        gross_rated_heating_cop: float | None = 3.4,
        minimum_outdoor_temperature_in_heating_mode: float | None = -20,
        maximum_outdoor_temperature_in_heating_mode: float | None = 16,
        minimum_heat_pump_part_load_ratio: float | None = 0.15,
        zone_name_for_master_thermostat_location: str | None = ...,
        master_thermostat_priority_control_type: Literal[
            "", "LoadPriority", "MasterThermostatPriority", "Scheduled", "ThermostatOffsetPriority", "ZonePriority"
        ]
        | None = "MasterThermostatPriority",
        thermostat_priority_schedule_name: str | None = ...,
        heat_pump_waste_heat_recovery: Literal["", "No", "Yes"] | None = "No",
        equivalent_piping_length_used_for_piping_correction_factor_in_cooling_mode: float | None = 30,
        vertical_height_used_for_piping_correction_factor: float | None = 10,
        equivalent_piping_length_used_for_piping_correction_factor_in_heating_mode: float | None = 30,
        crankcase_heater_power_per_compressor: float | None = 33,
        number_of_compressors: int | None = 2,
        ratio_of_compressor_size_to_total_compressor_capacity: float | None = 0.5,
        maximum_outdoor_dry_bulb_temperature_for_crankcase_heater: float | None = 5,
        defrost_strategy: Literal["", "Resistive", "ReverseCycle"] | None = "Resistive",
        defrost_control: Literal["", "OnDemand", "Timed"] | None = "Timed",
        defrost_time_period_fraction: float | None = 0.058333,
        resistive_defrost_heater_capacity: float | Literal["", "Autosize"] | None = "Autosize",
        maximum_outdoor_dry_bulb_temperature_for_defrost_operation: float | None = 5,
        condenser_type: Literal["", "AirCooled", "EvaporativelyCooled", "WaterCooled"] | None = "AirCooled",
        water_condenser_volume_flow_rate: float | Literal["", "Autosize"] | None = "Autosize",
        evaporative_condenser_effectiveness: float | None = 0.9,
        evaporative_condenser_air_flow_rate: float | Literal["", "Autosize"] | None = "Autosize",
        evaporative_condenser_pump_rated_power_consumption: float | Literal["", "Autosize"] | None = 0,
        basin_heater_capacity: float | None = 0,
        basin_heater_setpoint_temperature: float | None = 2,
        basin_heater_operating_schedule_name: str | None = ...,
        fuel_type: Literal["", "Diesel", "Electricity", "Gasoline", "NaturalGas", "OtherFuel1", "OtherFuel2"]
        | None = "Electricity",
        minimum_outdoor_temperature_in_heat_recovery_mode: float | None = -15,
        maximum_outdoor_temperature_in_heat_recovery_mode: float | None = 45,
    ) -> None: ...

class OutputControlSizingStyle:
    def __call__(self, /, *, column_separator: Literal["Comma", "Fixed", "Tab"]) -> None: ...

class AnyZoneControlContaminantController:
    def __call__(
        self,
        name: str,
        /,
        *,
        zone_name: str,
        carbon_dioxide_setpoint_schedule_name: str,
        carbon_dioxide_control_availability_schedule_name: str | None = ...,
        minimum_carbon_dioxide_concentration_schedule_name: str | None = ...,
        maximum_carbon_dioxide_concentration_schedule_name: str | None = ...,
        generic_contaminant_control_availability_schedule_name: str | None = ...,
        generic_contaminant_setpoint_schedule_name: str | None = ...,
    ) -> None: ...

class AnyZoneHVACWaterToAirHeatPump:
    def __call__(
        self,
        name: str,
        /,
        *,
        air_inlet_node_name: str,
        air_outlet_node_name: str,
        cooling_supply_air_flow_rate: float | Literal["Autosize"],
        heating_supply_air_flow_rate: float | Literal["Autosize"],
        cooling_outdoor_air_flow_rate: float | Literal["Autosize"],
        heating_outdoor_air_flow_rate: float | Literal["Autosize"],
        supply_air_fan_object_type: Literal["Fan:OnOff", "Fan:SystemModel"],
        supply_air_fan_name: str,
        heating_coil_object_type: Literal[
            "Coil:Heating:WaterToAirHeatPump:EquationFit", "Coil:Heating:WaterToAirHeatPump:VariableSpeedEquationFit"
        ],
        heating_coil_name: str,
        cooling_coil_object_type: Literal[
            "Coil:Cooling:WaterToAirHeatPump:EquationFit", "Coil:Cooling:WaterToAirHeatPump:VariableSpeedEquationFit"
        ],
        cooling_coil_name: str,
        supplemental_heating_coil_object_type: Literal[
            "Coil:Heating:Electric", "Coil:Heating:Fuel", "Coil:Heating:Steam", "Coil:Heating:Water"
        ],
        supplemental_heating_coil_name: str,
        maximum_supply_air_temperature_from_supplemental_heater: float | Literal["Autosize"],
        availability_schedule_name: str | None = ...,
        outdoor_air_mixer_object_type: Literal["OutdoorAir:Mixer"] | None = ...,
        outdoor_air_mixer_name: str | None = ...,
        no_load_supply_air_flow_rate: float | Literal["Autosize"] | None = ...,
        no_load_outdoor_air_flow_rate: float | Literal["Autosize"] | None = ...,
        maximum_outdoor_dry_bulb_temperature_for_supplemental_heater_operation: float | None = 21,
        outdoor_dry_bulb_temperature_sensor_node_name: str | None = ...,
        fan_placement: Literal["", "BlowThrough", "DrawThrough"] | None = "BlowThrough",
        supply_air_fan_operating_mode_schedule_name: str | None = ...,
        availability_manager_list_name: str | None = ...,
        heat_pump_coil_water_flow_mode: Literal["", "Constant", "ConstantOnDemand", "Cycling"] | None = "Cycling",
        design_specification_zonehvac_sizing_object_name: str | None = ...,
    ) -> None: ...

class ZoneHVACWaterToAirHeatPump:
    def __call__(
        self,
        name: str,
        /,
        *,
        air_inlet_node_name: str,
        air_outlet_node_name: str,
        cooling_supply_air_flow_rate: float | Literal["Autosize"],
        heating_supply_air_flow_rate: float | Literal["Autosize"],
        cooling_outdoor_air_flow_rate: float | Literal["Autosize"],
        heating_outdoor_air_flow_rate: float | Literal["Autosize"],
        supply_air_fan_object_type: Literal["Fan:OnOff", "Fan:SystemModel"],
        supply_air_fan_name: str,
        heating_coil_object_type: Literal[
            "Coil:Heating:WaterToAirHeatPump:EquationFit", "Coil:Heating:WaterToAirHeatPump:VariableSpeedEquationFit"
        ],
        heating_coil_name: str,
        cooling_coil_object_type: Literal[
            "Coil:Cooling:WaterToAirHeatPump:EquationFit", "Coil:Cooling:WaterToAirHeatPump:VariableSpeedEquationFit"
        ],
        cooling_coil_name: str,
        supplemental_heating_coil_object_type: Literal[
            "Coil:Heating:Electric", "Coil:Heating:Fuel", "Coil:Heating:Steam", "Coil:Heating:Water"
        ],
        supplemental_heating_coil_name: str,
        availability_schedule_name: str | None = ...,
        outdoor_air_mixer_object_type: Literal["OutdoorAir:Mixer"] | None = ...,
        outdoor_air_mixer_name: str | None = ...,
        no_load_supply_air_flow_rate: float | Literal["Autosize"] | None = ...,
        no_load_supply_air_flow_rate_control_set_to_low_speed: Literal["", "No", "Yes"] | None = "Yes",
        no_load_outdoor_air_flow_rate: float | Literal["Autosize"] | None = ...,
        maximum_supply_air_temperature_from_supplemental_heater: float | Literal["", "Autosize"] | None = "Autosize",
        maximum_outdoor_dry_bulb_temperature_for_supplemental_heater_operation: float | None = 21,
        outdoor_dry_bulb_temperature_sensor_node_name: str | None = ...,
        fan_placement: Literal["", "BlowThrough", "DrawThrough"] | None = "BlowThrough",
        supply_air_fan_operating_mode_schedule_name: str | None = ...,
        availability_manager_list_name: str | None = ...,
        heat_pump_coil_water_flow_mode: Literal["", "Constant", "ConstantOnDemand", "Cycling"] | None = "Cycling",
        design_specification_zonehvac_sizing_object_name: str | None = ...,
        design_specification_multispeed_object_type: Literal["UnitarySystemPerformance:Multispeed"] | None = ...,
        design_specification_multispeed_object_name: str | None = ...,
        dx_heating_coil_sizing_ratio: float | None = 1,
    ) -> None: ...

class ZoneHVACEnergyRecoveryVentilator:
    def __call__(
        self,
        name: str,
        /,
        *,
        heat_exchanger_name: str,
        supply_air_flow_rate: float | Literal["Autosize"],
        exhaust_air_flow_rate: float | Literal["Autosize"],
        supply_air_fan_name: str,
        exhaust_air_fan_name: str,
        availability_schedule_name: str | None = ...,
        controller_name: str | None = ...,
        ventilation_rate_per_unit_floor_area: float | None = ...,
        ventilation_rate_per_occupant: float | None = ...,
        availability_manager_list_name: str | None = ...,
    ) -> None: ...

class AirTerminalSingleDuctVAVReheatVariableSpeedFan:
    def __call__(
        self,
        name: str,
        /,
        *,
        maximum_cooling_air_flow_rate: float | Literal["Autosize"],
        maximum_heating_air_flow_rate: float | Literal["Autosize"],
        zone_minimum_air_flow_fraction: float,
        fan_object_type: Literal["Fan:SystemModel", "Fan:VariableVolume"],
        fan_name: str,
        heating_coil_object_type: Literal[
            "Coil:Heating:Electric", "Coil:Heating:Fuel", "Coil:Heating:Steam", "Coil:Heating:Water"
        ],
        heating_coil_name: str,
        availability_schedule_name: str | None = ...,
        air_inlet_node_name: str | None = ...,
        air_outlet_node_name: str | None = ...,
        maximum_hot_water_or_steam_flow_rate: float | Literal["Autosize"] | None = ...,
        minimum_hot_water_or_steam_flow_rate: float | None = 0,
        heating_convergence_tolerance: float | None = 0.001,
        minimum_air_flow_turndown_schedule_name: str | None = ...,
    ) -> None: ...

class AirTerminalSingleDuctConstantVolumeCooledBeam:
    def __call__(
        self,
        name: str,
        /,
        *,
        cooled_beam_type: Literal["Active", "Passive"],
        supply_air_inlet_node_name: str,
        supply_air_outlet_node_name: str,
        chilled_water_inlet_node_name: str,
        chilled_water_outlet_node_name: str,
        availability_schedule_name: str | None = ...,
        supply_air_volumetric_flow_rate: float | Literal["", "Autosize"] | None = "Autosize",
        maximum_total_chilled_water_volumetric_flow_rate: float | Literal["", "Autosize"] | None = "Autosize",
        number_of_beams: int | Literal["", "Autosize"] | None = "Autosize",
        beam_length: float | Literal["", "Autosize"] | None = "Autosize",
        design_inlet_water_temperature: float | None = 15,
        design_outlet_water_temperature: float | None = 17,
        coil_surface_area_per_coil_length: float | None = 5.422,
        model_parameter_a: float | None = 15.3,
        model_parameter_n1: float | None = 0,
        model_parameter_n2: float | None = 0.84,
        model_parameter_n3: float | None = 0.12,
        model_parameter_a0: float | None = 0.171,
        model_parameter_k1: float | None = 0.0057,
        model_parameter_n: float | None = 0.4,
        coefficient_of_induction_kin: float | Literal["", "Autocalculate"] | None = "Autocalculate",
        leaving_pipe_inside_diameter: float | None = 0.0145,
    ) -> None: ...

class AnyCoilCoolingDXCurveFitPerformance:
    def __call__(
        self,
        name: str,
        /,
        *,
        base_operating_mode: str,
        crankcase_heater_capacity: float | None = 0,
        minimum_outdoor_dry_bulb_temperature_for_compressor_operation: float | None = -25,
        maximum_outdoor_dry_bulb_temperature_for_crankcase_heater_operation: float | None = 10,
        unit_internal_static_air_pressure: float | None = ...,
        capacity_control_method: Literal["", "Continuous", "Discrete"] | None = "Discrete",
        evaporative_condenser_basin_heater_capacity: float | None = 0,
        evaporative_condenser_basin_heater_setpoint_temperature: float | None = 2,
        evaporative_condenser_basin_heater_operating_schedule_name: str | None = ...,
        compressor_fuel_type: Literal[
            "",
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
        | None = "Electricity",
        alternative_operating_mode_1: str | None = ...,
        alternative_operating_mode_2: str | None = ...,
    ) -> None: ...

class EvaporativeCoolerDirectCelDekPad:
    def __call__(
        self,
        name: str = "",
        /,
        *,
        recirculating_water_pump_power_consumption: float,
        air_inlet_node_name: str,
        air_outlet_node_name: str,
        availability_schedule_name: str | None = ...,
        direct_pad_area: float | Literal["", "Autosize"] | None = "Autosize",
        direct_pad_depth: float | Literal["", "Autosize"] | None = "Autosize",
        control_type: str | None = ...,
        water_supply_storage_tank_name: str | None = ...,
    ) -> None: ...

class NodeList:
    def __call__(self, name: str, /, *, nodes: list[_g.NodeListNodesItem] = ...) -> None: ...

class PipingSystemUndergroundDomain:
    def __call__(
        self,
        name: str,
        /,
        *,
        xmax: float,
        ymax: float,
        zmax: float,
        x_direction_mesh_type: Literal["SymmetricGeometric", "Uniform"],
        y_direction_mesh_type: Literal["SymmetricGeometric", "Uniform"],
        z_direction_mesh_type: Literal["SymmetricGeometric", "Uniform"],
        soil_thermal_conductivity: float,
        soil_density: float,
        soil_specific_heat: float,
        undisturbed_ground_temperature_model_type: Literal[
            "Site:GroundTemperature:Undisturbed:FiniteDifference",
            "Site:GroundTemperature:Undisturbed:KusudaAchenbach",
            "Site:GroundTemperature:Undisturbed:Xing",
        ],
        undisturbed_ground_temperature_model_name: str,
        number_of_pipe_circuits_entered_for_this_domain: int,
        x_direction_mesh_density_parameter: int | None = 4,
        x_direction_geometric_coefficient: float | None = 1.3,
        y_direction_mesh_density_parameter: int | None = 4,
        y_direction_geometric_coefficient: float | None = 1.3,
        z_direction_mesh_density_parameter: int | None = 4,
        z_direction_geometric_coefficient: float | None = 1.3,
        soil_moisture_content_volume_fraction: float | None = 30,
        soil_moisture_content_volume_fraction_at_saturation: float | None = 50,
        this_domain_includes_basement_surface_interaction: Literal["", "No", "Yes"] | None = "No",
        width_of_basement_floor_in_ground_domain: float | None = ...,
        depth_of_basement_wall_in_ground_domain: float | None = ...,
        shift_pipe_x_coordinates_by_basement_width: Literal["No", "Yes"] | None = ...,
        name_of_basement_wall_boundary_condition_model: str | None = ...,
        name_of_basement_floor_boundary_condition_model: str | None = ...,
        convergence_criterion_for_the_outer_cartesian_domain_iteration_loop: float | None = 0.001,
        maximum_iterations_in_the_outer_cartesian_domain_iteration_loop: int | None = 500,
        evapotranspiration_ground_cover_parameter: float | None = 0.4,
        pipe_circuits: list[_g.PipingSystemUndergroundDomainPipeCircuitsItem] = ...,
    ) -> None: ...

class BoilerHotWater:
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
        design_water_flow_rate: float | Literal["", "Autosize"] | None = "Autosize",
        minimum_part_load_ratio: float | None = 0,
        maximum_part_load_ratio: float | None = 1,
        optimum_part_load_ratio: float | None = 1,
        water_outlet_upper_temperature_limit: float | None = 99.9,
        boiler_flow_mode: Literal["", "ConstantFlow", "LeavingSetpointModulated", "NotModulated"]
        | None = "NotModulated",
        on_cycle_parasitic_electric_load: float | None = 0,
        sizing_factor: float | None = 1,
        end_use_subcategory: str | None = "General",
        off_cycle_parasitic_fuel_load: float | None = ...,
    ) -> None: ...

class AnyHeatPumpAirToWaterFuelFiredHeating:
    def __call__(
        self,
        name: str,
        /,
        *,
        water_inlet_node_name: str,
        water_outlet_node_name: str,
        normalized_capacity_function_of_temperature_curve_name: str,
        fuel_energy_input_ratio_function_of_temperature_curve_name: str,
        fuel_energy_input_ratio_function_of_plr_curve_name: str,
        air_source_node_name: str | None = ...,
        companion_cooling_heat_pump_name: str | None = ...,
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
        end_use_subcategory: str | None = "General",
        nominal_heating_capacity: float | Literal["Autosize"] | None = ...,
        nominal_cop: float | None = 1,
        design_flow_rate: float | Literal["Autosize"] | None = ...,
        design_supply_temperature: float | None = 60,
        design_temperature_lift: float | Literal["", "Autosize"] | None = 11.1,
        sizing_factor: float | None = 1,
        flow_mode: Literal["", "ConstantFlow", "LeavingSetpointModulated", "NotModulated"] | None = "NotModulated",
        outdoor_air_temperature_curve_input_variable: Literal["", "DryBulb", "WetBulb"] | None = "DryBulb",
        water_temperature_curve_input_variable: Literal["", "EnteringCondenser", "LeavingCondenser"]
        | None = "EnteringCondenser",
        minimum_part_load_ratio: float | None = 0.1,
        maximum_part_load_ratio: float | None = 1,
        defrost_control_type: Literal["", "OnDemand", "Timed"] | None = "Timed",
        defrost_operation_time_fraction: float | None = 0,
        fuel_energy_input_ratio_defrost_adjustment_curve_name: str | None = ...,
        resistive_defrost_heater_capacity: float | None = 0,
        maximum_outdoor_dry_bulb_temperature_for_defrost_operation: float | None = 5,
        cycling_ratio_factor_curve_name: str | None = ...,
        nominal_auxiliary_electric_power: float | None = ...,
        auxiliary_electric_energy_input_ratio_function_of_temperature_curve_name: str | None = ...,
        auxiliary_electric_energy_input_ratio_function_of_plr_curve_name: str | None = ...,
        standby_electric_power: float | None = 0,
    ) -> None: ...

class HeatPumpAirToWaterFuelFiredHeating:
    def __call__(
        self,
        name: str,
        /,
        *,
        water_inlet_node_name: str,
        water_outlet_node_name: str,
        normalized_capacity_function_of_temperature_curve_name: str,
        fuel_energy_input_ratio_function_of_temperature_curve_name: str,
        fuel_energy_input_ratio_function_of_plr_curve_name: str,
        air_source_node_name: str | None = ...,
        companion_cooling_heat_pump_name: str | None = ...,
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
        end_use_subcategory: str | None = "General",
        nominal_heating_capacity: float | Literal["Autosize"] | None = ...,
        nominal_cop: float | None = 1,
        design_flow_rate: float | Literal["Autosize"] | None = ...,
        design_supply_temperature: float | None = 60,
        design_temperature_lift: float | Literal["", "Autosize"] | None = 11.1,
        sizing_factor: float | None = 1,
        flow_mode: Literal["", "ConstantFlow", "LeavingSetpointModulated", "NotModulated"] | None = "NotModulated",
        outdoor_air_temperature_curve_input_variable: Literal["", "DryBulb", "WetBulb"] | None = "DryBulb",
        water_temperature_curve_input_variable: Literal["", "EnteringCondenser", "LeavingCondenser"]
        | None = "EnteringCondenser",
        minimum_part_load_ratio: float | None = 0.1,
        maximum_part_load_ratio: float | None = 1,
        defrost_control_type: Literal["", "OnDemand", "Timed"] | None = "Timed",
        defrost_operation_time_fraction: float | None = 0,
        fuel_energy_input_ratio_defrost_adjustment_curve_name: str | None = ...,
        resistive_defrost_heater_capacity: float | None = 0,
        maximum_outdoor_dry_bulb_temperature_for_defrost_operation: float | None = 5,
        cycling_ratio_factor_curve_name: str | None = ...,
        nominal_auxiliary_electric_power: float | None = ...,
        auxiliary_electric_energy_input_ratio_function_of_temperature_curve_name: str | None = ...,
        auxiliary_electric_energy_input_ratio_function_of_plr_curve_name: str | None = ...,
        standby_electric_power: float | None = 0,
        minimum_unloading_ratio: float | None = 0.25,
    ) -> None: ...

class HeatPumpWaterToWaterParameterEstimationHeating:
    def __call__(
        self,
        name: str,
        /,
        *,
        source_side_inlet_node_name: str,
        source_side_outlet_node_name: str,
        load_side_inlet_node_name: str,
        load_side_outlet_node_name: str,
        nominal_cop: float | None = ...,
        nominal_capacity: float | None = ...,
        minimum_part_load_ratio: float | None = ...,
        maximum_part_load_ratio: float | None = ...,
        optimum_part_load_ratio: float | None = ...,
        load_side_flow_rate: float | None = ...,
        source_side_flow_rate: float | None = ...,
        load_side_heat_transfer_coefficient: float | None = ...,
        source_side_heat_transfer_coefficient: float | None = ...,
        piston_displacement: float | None = ...,
        compressor_clearance_factor: float | None = ...,
        compressor_suction_and_discharge_pressure_drop: float | None = ...,
        superheating: float | None = ...,
        constant_part_of_electromechanical_power_losses: float | None = ...,
        loss_factor: float | None = ...,
        high_pressure_cut_off: float | None = 500000000,
        low_pressure_cut_off: float | None = 0,
    ) -> None: ...

class FluidCoolerTwoSpeed:
    def __call__(
        self,
        name: str,
        /,
        *,
        water_inlet_node_name: str,
        water_outlet_node_name: str,
        design_entering_water_temperature: float,
        design_entering_air_temperature: float,
        design_entering_air_wet_bulb_temperature: float,
        design_water_flow_rate: float | Literal["Autosize"],
        high_fan_speed_air_flow_rate: float | Literal["Autosize"],
        high_fan_speed_fan_power: float | Literal["Autosize"],
        low_fan_speed_air_flow_rate: float | Literal["Autocalculate"],
        low_fan_speed_fan_power: float | Literal["Autocalculate"],
        performance_input_method: Literal["", "NominalCapacity", "UFactorTimesAreaAndDesignWaterFlowRate"]
        | None = "NominalCapacity",
        high_fan_speed_u_factor_times_area_value: float | Literal["Autosize"] | None = ...,
        low_fan_speed_u_factor_times_area_value: float | Literal["Autocalculate"] | None = ...,
        low_fan_speed_u_factor_times_area_sizing_factor: float | None = 0.6,
        high_speed_nominal_capacity: float | None = ...,
        low_speed_nominal_capacity: float | Literal["Autocalculate"] | None = ...,
        low_speed_nominal_capacity_sizing_factor: float | None = 0.5,
        low_fan_speed_air_flow_rate_sizing_factor: float | None = 0.5,
        low_fan_speed_fan_power_sizing_factor: float | None = 0.16,
        outdoor_air_inlet_node_name: str | None = ...,
    ) -> None: ...

class ExternalInterfaceFunctionalMockupUnitImportToVariable:
    def __call__(
        self, name: str, /, *, fmu_file_name: str, fmu_instance_name: str, fmu_variable_name: str, initial_value: float
    ) -> None: ...

class ExternalInterfaceFunctionalMockupUnitExportFromVariable:
    def __call__(
        self, /, *, output_variable_index_key_name: str, output_variable_name: str, fmu_variable_name: str
    ) -> None: ...

class SetpointManagerScheduled:
    def __call__(
        self,
        name: str,
        /,
        *,
        control_variable: Literal[
            "HumidityRatio",
            "MassFlowRate",
            "MaximumHumidityRatio",
            "MaximumMassFlowRate",
            "MaximumTemperature",
            "MinimumHumidityRatio",
            "MinimumMassFlowRate",
            "MinimumTemperature",
            "Temperature",
        ],
        schedule_name: str,
        setpoint_node_or_nodelist_name: str,
    ) -> None: ...

class GeneratorInternalCombustionEngine:
    def __call__(
        self,
        name: str,
        /,
        *,
        rated_power_output: float | None = ...,
        electric_circuit_node_name: str | None = ...,
        minimum_part_load_ratio: float | None = ...,
        maximum_part_load_ratio: float | None = ...,
        optimum_part_load_ratio: float | None = ...,
        shaft_power_curve_name: str | None = ...,
        jacket_heat_recovery_curve_name: str | None = ...,
        lube_heat_recovery_curve_name: str | None = ...,
        total_exhaust_energy_curve_name: str | None = ...,
        exhaust_temperature_curve_name: str | None = ...,
        coefficient_1_of_u_factor_times_area_curve: float | None = ...,
        coefficient_2_of_u_factor_times_area_curve: float | None = ...,
        maximum_exhaust_flow_per_unit_of_power_output: float | None = ...,
        design_minimum_exhaust_temperature: float | None = ...,
        fuel_higher_heating_value: float | None = ...,
        design_heat_recovery_water_flow_rate: float | None = 0,
        heat_recovery_inlet_node_name: str | None = ...,
        heat_recovery_outlet_node_name: str | None = ...,
        fuel_type: Literal[
            "", "Diesel", "FuelOilNo1", "FuelOilNo2", "Gasoline", "NaturalGas", "OtherFuel1", "OtherFuel2", "Propane"
        ]
        | None = "Diesel",
        heat_recovery_maximum_temperature: float | None = 80,
    ) -> None: ...

class ElectricLoadCenterTransformer:
    def __call__(
        self,
        name: str,
        /,
        *,
        availability_schedule_name: str | None = ...,
        transformer_usage: Literal["", "LoadCenterPowerConditioning", "PowerInFromGrid", "PowerOutToGrid"]
        | None = "PowerInFromGrid",
        zone_name: str | None = ...,
        radiative_fraction: float | None = 0,
        rated_capacity: float | None = ...,
        phase: Literal[1, 3, ""] | None = 3,
        conductor_material: Literal["", "Aluminum", "Copper"] | None = "Aluminum",
        full_load_temperature_rise: float | None = 150,
        fraction_of_eddy_current_losses: float | None = 0.1,
        performance_input_method: Literal["", "NominalEfficiency", "RatedLosses"] | None = "RatedLosses",
        rated_no_load_loss: float | None = ...,
        rated_load_loss: float | None = ...,
        nameplate_efficiency: float | None = 0.98,
        per_unit_load_for_nameplate_efficiency: float | None = 0.35,
        reference_temperature_for_nameplate_efficiency: float | None = 75,
        per_unit_load_for_maximum_efficiency: float | None = ...,
        consider_transformer_loss_for_utility_cost: Literal["", "No", "Yes"] | None = "Yes",
        meters: list[_g.ElectricLoadCenterTransformerMetersItem] = ...,
    ) -> None: ...

class FaultModelTemperatureSensorOffsetReturnAir:
    def __call__(
        self,
        name: str,
        /,
        *,
        controller_object_type: Literal["Controller:OutdoorAir"],
        controller_object_name: str,
        availability_schedule_name: str | None = ...,
        severity_schedule_name: str | None = ...,
        temperature_sensor_offset: float | None = 0,
    ) -> None: ...

class CurveBiquadratic:
    def __call__(
        self,
        name: str,
        /,
        *,
        coefficient1_constant: float,
        coefficient2_x: float,
        coefficient3_x_2: float,
        coefficient4_y: float,
        coefficient5_y_2: float,
        coefficient6_x_y: float,
        minimum_value_of_x: float,
        maximum_value_of_x: float,
        minimum_value_of_y: float,
        maximum_value_of_y: float,
        minimum_curve_output: float | None = ...,
        maximum_curve_output: float | None = ...,
        input_unit_type_for_x: Literal[
            "", "Dimensionless", "Distance", "MassFlow", "Power", "Temperature", "VolumetricFlow"
        ]
        | None = "Dimensionless",
        input_unit_type_for_y: Literal[
            "", "Dimensionless", "Distance", "MassFlow", "Power", "Temperature", "VolumetricFlow"
        ]
        | None = "Dimensionless",
        output_unit_type: Literal["", "Capacity", "Dimensionless", "Power", "Pressure", "Temperature"]
        | None = "Dimensionless",
    ) -> None: ...

class CurveRectangularHyperbola2:
    def __call__(
        self,
        name: str,
        /,
        *,
        coefficient1_c1: float,
        coefficient2_c2: float,
        coefficient3_c3: float,
        minimum_value_of_x: float,
        maximum_value_of_x: float,
        minimum_curve_output: float | None = ...,
        maximum_curve_output: float | None = ...,
        input_unit_type_for_x: Literal["", "Dimensionless"] | None = "Dimensionless",
        output_unit_type: Literal["", "Capacity", "Dimensionless", "Power", "Pressure", "Temperature"]
        | None = "Dimensionless",
    ) -> None: ...

class AnyOutputSQLite:
    def __call__(self, /, *, option_type: Literal["Simple", "SimpleAndTabular"] | None = ...) -> None: ...
