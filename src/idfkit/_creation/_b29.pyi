"""Creation signatures of generated classes (stub only).

DO NOT EDIT — regenerate with:
    python -m idfkit.codegen.generate_stubs
"""

from __future__ import annotations

from typing import Any, Literal

class AnySimulationControl:
    def __call__(
        self,
        /,
        *,
        do_zone_sizing_calculation: Literal["", "No", "Yes"] | None = "No",
        do_system_sizing_calculation: Literal["", "No", "Yes"] | None = "No",
        do_plant_sizing_calculation: Literal["", "No", "Yes"] | None = "No",
        run_simulation_for_sizing_periods: Literal["", "No", "Yes"] | None = "Yes",
        run_simulation_for_weather_file_run_periods: Literal["", "No", "Yes"] | None = "Yes",
        do_hvac_sizing_simulation_for_sizing_periods: Literal["", "No", "Yes"] | None = "No",
        maximum_number_of_hvac_sizing_simulation_passes: int | None = 1,
    ) -> None: ...

class AnyTimestep:
    def __call__(self, /, *, number_of_timesteps_per_hour: int | None = 6) -> None: ...

class WindowMaterialGlazing:
    def __call__(
        self,
        name: str,
        /,
        *,
        optical_data_type: Literal["BSDF", "Spectral", "SpectralAndAngle", "SpectralAverage"],
        thickness: float,
        window_glass_spectral_data_set_name: str | None = ...,
        solar_transmittance_at_normal_incidence: float | None = ...,
        front_side_solar_reflectance_at_normal_incidence: float | None = ...,
        back_side_solar_reflectance_at_normal_incidence: float | None = ...,
        visible_transmittance_at_normal_incidence: float | None = ...,
        front_side_visible_reflectance_at_normal_incidence: float | None = ...,
        back_side_visible_reflectance_at_normal_incidence: float | None = ...,
        infrared_transmittance_at_normal_incidence: float | None = 0,
        front_side_infrared_hemispherical_emissivity: float | None = 0.84,
        back_side_infrared_hemispherical_emissivity: float | None = 0.84,
        conductivity: float | None = 0.9,
        dirt_correction_factor_for_solar_and_visible_transmittance: float | None = 1,
        solar_diffusing: Literal["", "No", "Yes"] | None = "No",
        young_s_modulus: float | None = 72000000000,
        poisson_s_ratio: float | None = 0.22,
        window_glass_spectral_and_incident_angle_transmittance_data_set_table_name: str | None = ...,
        window_glass_spectral_and_incident_angle_front_reflectance_data_set_table_name: str | None = ...,
        window_glass_spectral_and_incident_angle_back_reflectance_data_set_table_name: str | None = ...,
    ) -> None: ...

class MaterialPropertyPhaseChange:
    def __call__(
        self,
        name: str,
        /,
        *,
        temperature_coefficient_for_thermal_conductivity: float | None = 0,
        values: list[Any] = ...,
    ) -> None: ...

class MaterialPropertyHeatAndMoistureTransferSettings:
    def __call__(
        self, /, *, material_name: str, porosity: float, initial_water_content_ratio: float | None = 0.2
    ) -> None: ...

class ConstructionFfactorGroundFloor:
    def __call__(self, name: str, /, *, f_factor: float, area: float, perimeterexposed: float) -> None: ...

class SubSurfaceConstructionAssignments:
    def __call__(
        self,
        name: str,
        /,
        *,
        fixed_window_construction_name: str | None = ...,
        operable_window_construction_name: str | None = ...,
        door_construction_name: str | None = ...,
        glass_door_construction_name: str | None = ...,
        overhead_door_construction_name: str | None = ...,
        skylight_construction_name: str | None = ...,
        tubular_daylight_dome_construction_name: str | None = ...,
        tubular_daylight_diffuser_construction_name: str | None = ...,
    ) -> None: ...

class WallInterzone:
    def __call__(
        self,
        name: str,
        /,
        *,
        construction_name: str,
        zone_name: str,
        outside_boundary_condition_object: str,
        space_name: str | None = ...,
        azimuth_angle: float | None = ...,
        tilt_angle: float | None = 90,
        starting_x_coordinate: float | None = ...,
        starting_y_coordinate: float | None = ...,
        starting_z_coordinate: float | None = ...,
        length: float | None = ...,
        height: float | None = ...,
    ) -> None: ...

class ZonePropertyUserViewFactorsBySurfaceName:
    def __call__(
        self, /, *, zone_or_zonelist_or_space_or_spacelist_name: str | None = ..., view_factors: list[Any] = ...
    ) -> None: ...

class GasEquipment:
    def __call__(
        self,
        name: str,
        /,
        *,
        zone_or_zonelist_or_space_or_spacelist_name: str,
        schedule_name: str,
        design_level_calculation_method: Literal[
            "", "EquipmentLevel", "Power/Area", "Power/Person", "Watts/Area", "Watts/Person"
        ]
        | None = "EquipmentLevel",
        design_level: float | None = ...,
        power_per_floor_area: float | None = ...,
        power_per_person: float | None = ...,
        fraction_latent: float | None = 0,
        fraction_radiant: float | None = 0,
        fraction_lost: float | None = 0,
        carbon_dioxide_generation_rate: float | None = 0,
        end_use_subcategory: str | None = "General",
    ) -> None: ...

class HotWaterEquipmentDefinition:
    def __call__(
        self,
        name: str,
        /,
        *,
        design_level_calculation_method: Literal[
            "", "EquipmentLevel", "Power/Area", "Power/Person", "Watts/Area", "Watts/Person"
        ]
        | None = "EquipmentLevel",
        design_level: float | None = ...,
        power_per_floor_area: float | None = ...,
        power_per_person: float | None = ...,
        fraction_latent: float | None = 0,
        fraction_radiant: float | None = 0,
        fraction_lost: float | None = 0,
    ) -> None: ...

class SteamEquipment:
    def __call__(
        self,
        name: str,
        /,
        *,
        zone_or_zonelist_or_space_or_spacelist_name: str,
        schedule_name: str,
        design_level_calculation_method: Literal[
            "", "EquipmentLevel", "Power/Area", "Power/Person", "Watts/Area", "Watts/Person"
        ]
        | None = "EquipmentLevel",
        design_level: float | None = ...,
        power_per_floor_area: float | None = ...,
        power_per_person: float | None = ...,
        fraction_latent: float | None = 0,
        fraction_radiant: float | None = 0,
        fraction_lost: float | None = 0,
        end_use_subcategory: str | None = "General",
    ) -> None: ...

class ZoneContaminantSourceAndSinkGenericConstant:
    def __call__(
        self,
        name: str,
        /,
        *,
        zone_name: str,
        generation_schedule_name: str,
        removal_schedule_name: str,
        design_generation_rate: float | None = ...,
        design_removal_coefficient: float | None = ...,
    ) -> None: ...

class AnyExteriorFuelEquipment:
    def __call__(
        self,
        name: str,
        /,
        *,
        fuel_use_type: Literal[
            "Coal",
            "Diesel",
            "DistrictCooling",
            "Electricity",
            "Gasoline",
            "NaturalGas",
            "OtherFuel1",
            "OtherFuel2",
            "Water",
        ],
        schedule_name: str,
        design_level: float,
        end_use_subcategory: str | None = "General",
    ) -> None: ...

class AnyHVACTemplateZonePTAC:
    def __call__(
        self,
        /,
        *,
        zone_name: str,
        template_thermostat_name: str | None = ...,
        cooling_supply_air_flow_rate: float | Literal["", "Autosize"] | None = "Autosize",
        heating_supply_air_flow_rate: float | Literal["", "Autosize"] | None = "Autosize",
        no_load_supply_air_flow_rate: float | Literal["Autosize"] | None = ...,
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
        supply_fan_operating_mode_schedule_name: str | None = ...,
        supply_fan_placement: Literal["", "BlowThrough", "DrawThrough"] | None = "DrawThrough",
        supply_fan_total_efficiency: float | None = 0.7,
        supply_fan_delta_pressure: float | None = 75,
        supply_fan_motor_efficiency: float | None = 0.9,
        cooling_coil_type: Literal["", "SingleSpeedDX"] | None = "SingleSpeedDX",
        cooling_coil_availability_schedule_name: str | None = ...,
        cooling_coil_gross_rated_total_capacity: float | Literal["", "Autosize"] | None = "Autosize",
        cooling_coil_gross_rated_sensible_heat_ratio: float | Literal["", "Autosize"] | None = "Autosize",
        cooling_coil_gross_rated_cooling_cop: float | None = 3,
        heating_coil_type: Literal["", "Electric", "Gas", "HotWater"] | None = "Electric",
        heating_coil_availability_schedule_name: str | None = ...,
        heating_coil_capacity: float | Literal["", "Autosize"] | None = "Autosize",
        gas_heating_coil_efficiency: float | None = 0.8,
        gas_heating_coil_parasitic_electric_load: float | None = 0,
        dedicated_outdoor_air_system_name: str | None = ...,
        zone_cooling_design_supply_air_temperature_input_method: Literal[
            "", "SupplyAirTemperature", "TemperatureDifference"
        ]
        | None = "SupplyAirTemperature",
        zone_cooling_design_supply_air_temperature: float | None = 14,
        zone_cooling_design_supply_air_temperature_difference: float | None = 11.11,
        zone_heating_design_supply_air_temperature_input_method: Literal[
            "", "SupplyAirTemperature", "TemperatureDifference"
        ]
        | None = "SupplyAirTemperature",
        zone_heating_design_supply_air_temperature: float | None = 50,
        zone_heating_design_supply_air_temperature_difference: float | None = 30,
        design_specification_outdoor_air_object_name: str | None = ...,
        design_specification_zone_air_distribution_object_name: str | None = ...,
        baseboard_heating_type: Literal["", "Electric", "HotWater", "None"] | None = "None",
        baseboard_heating_availability_schedule_name: str | None = ...,
        baseboard_heating_capacity: float | Literal["", "Autosize"] | None = "Autosize",
    ) -> None: ...

class ZoneHVACVentilatedSlabSlabGroup:
    def __call__(self, name: str, /, *, data: list[Any] = ...) -> None: ...

class AirTerminalSingleDuctVAVHeatAndCoolNoReheat:
    def __call__(
        self,
        name: str,
        /,
        *,
        air_outlet_node_name: str,
        air_inlet_node_name: str,
        maximum_air_flow_rate: float | Literal["Autosize"],
        zone_minimum_air_flow_fraction: float,
        availability_schedule_name: str | None = ...,
        minimum_air_flow_turndown_schedule_name: str | None = ...,
    ) -> None: ...

class SpaceHVACZoneEquipmentSplitter:
    def __call__(
        self,
        name: str,
        /,
        *,
        zone_name: str,
        zone_equipment_object_type: Literal[
            "AirLoopHVAC:UnitarySystem",
            "HeatExchanger:AirToAir:FlatPlate",
            "WaterHeater:HeatPump:PumpedCondenser",
            "WaterHeater:HeatPump:WrappedCondenser",
            "ZoneHVAC:AirDistributionUnit",
            "ZoneHVAC:Baseboard:Convective:Electric",
            "ZoneHVAC:Baseboard:Convective:Water",
            "ZoneHVAC:Baseboard:RadiantConvective:Electric",
            "ZoneHVAC:Baseboard:RadiantConvective:Steam",
            "ZoneHVAC:Baseboard:RadiantConvective:Water",
            "ZoneHVAC:CoolingPanel:RadiantConvective:Water",
            "ZoneHVAC:Dehumidifier:DX",
            "ZoneHVAC:EnergyRecoveryVentilator",
            "ZoneHVAC:EvaporativeCoolerUnit",
            "ZoneHVAC:ForcedAir:UserDefined",
            "ZoneHVAC:FourPipeFanCoil",
            "ZoneHVAC:HighTemperatureRadiant",
            "ZoneHVAC:HybridUnitaryHVAC",
            "ZoneHVAC:IdealLoadsAirSystem",
            "ZoneHVAC:LowTemperatureRadiant:ConstantFlow",
            "ZoneHVAC:LowTemperatureRadiant:Electric",
            "ZoneHVAC:LowTemperatureRadiant:VariableFlow",
            "ZoneHVAC:OutdoorAirUnit",
            "ZoneHVAC:PackagedTerminalAirConditioner",
            "ZoneHVAC:PackagedTerminalHeatPump",
            "ZoneHVAC:RefrigerationChillerSet",
            "ZoneHVAC:TerminalUnit:VariableRefrigerantFlow",
            "ZoneHVAC:UnitHeater",
            "ZoneHVAC:UnitVentilator",
            "ZoneHVAC:VentilatedSlab",
            "ZoneHVAC:WaterToAirHeatPump",
            "ZoneHVAC:WindowAirConditioner",
        ],
        zone_equipment_name: str,
        zone_equipment_outlet_node_name: str | None = ...,
        thermostat_control_method: Literal["", "Ideal", "Maximum", "SingleSpace"] | None = "SingleSpace",
        control_space_name: str | None = ...,
        space_fraction_method: Literal[
            "", "DesignCoolingLoad", "DesignHeatingLoad", "FloorArea", "PerimeterLength", "Volume"
        ]
        | None = "DesignCoolingLoad",
        spaces: list[Any] = ...,
    ) -> None: ...

class CoilHeatingWaterToAirHeatPumpEquationFit:
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
        gross_rated_heating_capacity: float | Literal["Autosize"],
        gross_rated_heating_cop: float,
        heating_capacity_curve_name: str,
        heating_power_consumption_curve_name: str,
        part_load_fraction_correlation_curve_name: str,
        availability_schedule_name: str | None = ...,
        rated_entering_water_temperature: float | None = 20,
        rated_entering_air_dry_bulb_temperature: float | None = 20,
        ratio_of_rated_heating_capacity_to_rated_cooling_capacity: float | None = 1,
    ) -> None: ...

class AirLoopHVACReturnPlenum:
    def __call__(
        self,
        name: str,
        /,
        *,
        zone_name: str,
        zone_node_name: str,
        outlet_node_name: str,
        induced_air_outlet_node_or_nodelist_name: str | None = ...,
        nodes: list[Any] = ...,
    ) -> None: ...

class AnyLoadProfilePlant:
    def __call__(
        self,
        name: str,
        /,
        *,
        inlet_node_name: str,
        outlet_node_name: str,
        load_schedule_name: str,
        peak_flow_rate: float,
        flow_rate_fraction_schedule_name: str,
    ) -> None: ...

class SolarCollectorUnglazedTranspiredMultisystem:
    def __call__(self, /, *, solar_collector_name: str, systems: list[Any] = ...) -> None: ...

class ThermalStorageChilledWaterMixed:
    def __call__(
        self,
        name: str,
        /,
        *,
        ambient_temperature_indicator: Literal["Outdoors", "Schedule", "Zone"],
        tank_volume: float | None = 0.1,
        setpoint_temperature_schedule_name: str | None = ...,
        deadband_temperature_difference: float | None = 0.5,
        minimum_temperature_limit: float | None = ...,
        nominal_cooling_capacity: float | None = ...,
        ambient_temperature_schedule_name: str | None = ...,
        ambient_temperature_zone_name: str | None = ...,
        ambient_temperature_outdoor_air_node_name: str | None = ...,
        heat_gain_coefficient_from_ambient_temperature: float | None = ...,
        use_side_inlet_node_name: str | None = ...,
        use_side_outlet_node_name: str | None = ...,
        use_side_heat_transfer_effectiveness: float | None = 1,
        use_side_availability_schedule_name: str | None = ...,
        use_side_design_flow_rate: float | Literal["", "Autosize"] | None = "Autosize",
        source_side_inlet_node_name: str | None = ...,
        source_side_outlet_node_name: str | None = ...,
        source_side_heat_transfer_effectiveness: float | None = 1,
        source_side_availability_schedule_name: str | None = ...,
        source_side_design_flow_rate: float | Literal["", "Autosize"] | None = "Autosize",
        tank_recovery_time: float | None = 4,
    ) -> None: ...

class ExternalInterfaceFunctionalMockupUnitExportToVariable:
    def __call__(self, name: str, /, *, fmu_variable_name: str, initial_value: float) -> None: ...

class AnyAvailabilityManagerOptimumStart:
    def __call__(
        self,
        name: str,
        /,
        *,
        applicability_schedule_name: str,
        fan_schedule_name: str,
        control_type: Literal["", "ControlZone", "MaximumofZoneList", "StayOff"] | None = "ControlZone",
        control_zone_name: str | None = ...,
        zone_list_name: str | None = ...,
        maximum_value_for_optimum_start_time: float | None = 6,
        control_algorithm: Literal[
            "", "AdaptiveASHRAE", "AdaptiveTemperatureGradient", "ConstantStartTime", "ConstantTemperatureGradient"
        ]
        | None = "AdaptiveASHRAE",
        constant_temperature_gradient_during_cooling: float | None = ...,
        constant_temperature_gradient_during_heating: float | None = ...,
        initial_temperature_gradient_during_cooling: float | None = ...,
        initial_temperature_gradient_during_heating: float | None = ...,
        constant_start_time: float | None = ...,
        number_of_previous_days: int | None = 2,
    ) -> None: ...

class SetpointManagerFollowOutdoorAirTemperature:
    def __call__(
        self,
        name: str,
        /,
        *,
        setpoint_node_or_nodelist_name: str,
        control_variable: Literal["", "MaximumTemperature", "MinimumTemperature", "Temperature"] | None = "Temperature",
        reference_temperature_type: Literal["", "OutdoorAirDryBulb", "OutdoorAirWetBulb"] | None = "OutdoorAirWetBulb",
        offset_temperature_difference: float | None = ...,
        maximum_setpoint_temperature: float | None = ...,
        minimum_setpoint_temperature: float | None = ...,
    ) -> None: ...

class WaterUseStorage:
    def __call__(
        self,
        name: str,
        /,
        *,
        water_temperature_schedule_name: str,
        water_quality_subcategory: str | None = ...,
        maximum_capacity: float | None = ...,
        initial_volume: float | None = ...,
        design_in_flow_rate: float | None = ...,
        design_out_flow_rate: float | None = ...,
        overflow_destination: str | None = ...,
        type_of_supply_controlled_by_float_valve: Literal["GroundwaterWell", "Mains", "None", "OtherTank"] | None = ...,
        float_valve_on_capacity: float | None = ...,
        float_valve_off_capacity: float | None = ...,
        backup_mains_capacity: float | None = ...,
        other_tank_name: str | None = ...,
        water_thermal_mode: Literal["ScheduledTemperature", "ThermalModel"] | None = ...,
        ambient_temperature_indicator: Literal["Outdoors", "Schedule", "Zone"] | None = ...,
        ambient_temperature_schedule_name: str | None = ...,
        zone_name: str | None = ...,
        tank_surface_area: float | None = ...,
        tank_u_value: float | None = ...,
        tank_outside_surface_material_name: str | None = ...,
    ) -> None: ...

class FaultModelTemperatureSensorOffsetCondenserSupplyWater:
    def __call__(
        self,
        name: str,
        /,
        *,
        cooling_tower_object_type: Literal[
            "CoolingTower:SingleSpeed",
            "CoolingTower:TwoSpeed",
            "CoolingTower:VariableSpeed",
            "CoolingTower:VariableSpeed:MERKEL",
        ],
        cooling_tower_object_name: str,
        availability_schedule_name: str | None = ...,
        severity_schedule_name: str | None = ...,
        reference_sensor_offset: float | None = 0,
    ) -> None: ...

class AnyMeterCustom:
    def __call__(self, name: str, /, *, variable_details: list[Any] = ...) -> None: ...
