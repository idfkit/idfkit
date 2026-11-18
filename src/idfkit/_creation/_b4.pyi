"""Creation signatures of generated classes (stub only).

DO NOT EDIT — regenerate with:
    python -m idfkit.codegen.generate_stubs
"""

from __future__ import annotations

from typing import Any, Literal

class AnyVersion:
    def __call__(self, /, *, version_identifier: str | None = ...) -> None: ...

class AnyMaterial:
    def __call__(
        self,
        name: str,
        /,
        *,
        roughness: Literal["MediumRough", "MediumSmooth", "Rough", "Smooth", "VeryRough", "VerySmooth"],
        thickness: float,
        conductivity: float,
        density: float,
        specific_heat: float,
        thermal_absorptance: float | None = 0.9,
        solar_absorptance: float | None = 0.7,
        visible_absorptance: float | None = 0.7,
    ) -> None: ...

class AnyMaterialPropertyHeatAndMoistureTransferThermalConductivity:
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

class ConstructionPropertyInternalHeatSource:
    def __call__(
        self,
        name: str,
        /,
        *,
        thermal_source_present_after_layer_number: int,
        temperature_calculation_requested_after_layer_number: int,
        dimensions_for_the_ctf_calculation: int,
        tube_spacing: float,
        construction_name: str | None = ...,
        two_dimensional_temperature_calculation_position: float | None = 0,
    ) -> None: ...

class SurfacePropertyExteriorNaturalVentedCavity:
    def __call__(
        self,
        name: str,
        /,
        *,
        boundary_conditions_model_name: str,
        roughness_of_exterior_surface: Literal[
            "MediumRough", "MediumSmooth", "Rough", "Smooth", "VeryRough", "VerySmooth"
        ],
        area_fraction_of_openings: float | None = ...,
        thermal_emissivity_of_exterior_baffle_material: float | None = ...,
        solar_absorbtivity_of_exterior_baffle: float | None = ...,
        height_scale_for_buoyancy_driven_ventilation: float | None = ...,
        effective_thickness_of_cavity_behind_exterior_baffle: float | None = ...,
        ratio_of_actual_surface_area_to_projected_surface_area: float | None = 1,
        effectiveness_for_perforations_with_respect_to_wind: float | None = 0.25,
        discharge_coefficient_for_openings_with_respect_to_buoyancy_driven_flow: float | None = 0.65,
        surface: list[Any] = ...,
    ) -> None: ...

class AnySurfacePropertyLocalEnvironment:
    def __call__(
        self,
        name: str,
        /,
        *,
        exterior_surface_name: str | None = ...,
        surrounding_surfaces_object_name: str | None = ...,
        outdoor_air_node_name: str | None = ...,
    ) -> None: ...

class GroundHeatTransferSlabAutoGrid:
    def __call__(
        self,
        /,
        *,
        slabx_x_dimension_of_the_building_slab: float,
        slaby_y_dimension_of_the_building_slab: float,
        slabdepth_thickness_of_slab_on_grade: float | None = 0.1,
        clearance_distance_from_edge_of_slab_to_domain_edge: float | None = 15,
        zclearance_distance_from_bottom_of_slab_to_domain_bottom: float | None = 15,
    ) -> None: ...

class GroundHeatTransferBasementInsulation:
    def __call__(
        self,
        /,
        *,
        insfull_flag_is_the_wall_fully_insulated_: Literal["FALSE", "TRUE"],
        rext_r_value_of_any_exterior_insulation: float | None = ...,
        insfull_flag_is_the_wall_fully_insulated: Literal["FALSE", "TRUE"] | None = ...,
    ) -> None: ...

class LightsInstance:
    def __call__(
        self,
        name: str,
        /,
        *,
        lights_definition_name: str,
        zone_or_zonelist_or_space_or_spacelist_name: str,
        schedule_name: str,
        fraction_replaceable: float | None = 1,
        multiplier: float | None = 1,
        end_use_subcategory: str | None = "General",
        return_air_heat_gain_node_name: str | None = ...,
        exhaust_air_heat_gain_node_name: str | None = ...,
    ) -> None: ...

class DaylightingDeviceLightWell:
    def __call__(
        self,
        /,
        *,
        exterior_window_name: str,
        height_of_well: float,
        perimeter_of_bottom_of_well: float,
        area_of_bottom_of_well: float,
        visible_reflectance_of_well_walls: float,
    ) -> None: ...

class OutputControlIlluminanceMapStyle:
    def __call__(self, /, *, column_separator: Literal["", "Comma", "Fixed", "Tab"] | None = "Comma") -> None: ...

class DuctLossMakeupAir:
    def __call__(
        self, name: str, /, *, airloophvac_name: str, airflownetwork_distribution_linkage_name: str
    ) -> None: ...

class HVACTemplateSystemUnitaryHeatPumpAirToAir:
    def __call__(
        self,
        name: str,
        /,
        *,
        control_zone_or_thermostat_location_name: str,
        system_availability_schedule_name: str | None = ...,
        cooling_supply_air_flow_rate: float | Literal["", "Autosize"] | None = "Autosize",
        heating_supply_air_flow_rate: float | Literal["", "Autosize"] | None = "Autosize",
        no_load_supply_air_flow_rate: float | Literal["", "Autosize"] | None = "Autosize",
        supply_fan_operating_mode_schedule_name: str | None = ...,
        supply_fan_placement: Literal["", "BlowThrough", "DrawThrough"] | None = "BlowThrough",
        supply_fan_total_efficiency: float | None = 0.7,
        supply_fan_delta_pressure: float | None = 600,
        supply_fan_motor_efficiency: float | None = 0.9,
        supply_fan_motor_in_air_stream_fraction: float | None = 1,
        cooling_coil_type: Literal["", "SingleSpeedDX"] | None = "SingleSpeedDX",
        cooling_coil_availability_schedule_name: str | None = ...,
        cooling_design_supply_air_temperature: float | None = 12.8,
        cooling_coil_gross_rated_total_capacity: float | Literal["", "Autosize"] | None = "Autosize",
        cooling_coil_gross_rated_sensible_heat_ratio: float | Literal["", "Autosize"] | None = "Autosize",
        cooling_coil_gross_rated_cop: float | None = 3,
        heat_pump_heating_coil_type: Literal["", "SingleSpeedDXHeatPump"] | None = "SingleSpeedDXHeatPump",
        heat_pump_heating_coil_availability_schedule_name: str | None = ...,
        heating_design_supply_air_temperature: float | None = 50,
        heat_pump_heating_coil_gross_rated_capacity: float | Literal["", "Autosize"] | None = "Autosize",
        heat_pump_heating_coil_rated_cop: float | None = 2.75,
        heat_pump_heating_minimum_outdoor_dry_bulb_temperature: float | None = -8,
        heat_pump_defrost_maximum_outdoor_dry_bulb_temperature: float | None = 5,
        heat_pump_defrost_strategy: Literal["", "Resistive", "ReverseCycle"] | None = "ReverseCycle",
        heat_pump_defrost_control: Literal["", "OnDemand", "Timed"] | None = "Timed",
        heat_pump_defrost_time_period_fraction: float | None = 0.058333,
        supplemental_heating_coil_type: Literal["", "Electric", "Gas", "HotWater"] | None = "Electric",
        supplemental_heating_coil_availability_schedule_name: str | None = ...,
        supplemental_heating_coil_capacity: float | Literal["", "Autosize"] | None = "Autosize",
        supplemental_heating_coil_maximum_outdoor_dry_bulb_temperature: float | None = 21,
        supplemental_gas_heating_coil_efficiency: float | None = 0.8,
        supplemental_gas_heating_coil_parasitic_electric_load: float | None = 0,
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
        economizer_lockout: Literal["", "LockoutWithCompressor", "LockoutWithHeating", "NoLockout"]
        | None = "NoLockout",
        economizer_maximum_limit_dry_bulb_temperature: float | None = ...,
        economizer_maximum_limit_enthalpy: float | None = ...,
        economizer_maximum_limit_dewpoint_temperature: float | None = ...,
        economizer_minimum_limit_dry_bulb_temperature: float | None = ...,
        supply_plenum_name: str | None = ...,
        return_plenum_name: str | None = ...,
        night_cycle_control: Literal["", "CycleOnAny", "CycleOnControlZone", "StayOff"] | None = "StayOff",
        night_cycle_control_zone_name: str | None = ...,
        heat_recovery_type: Literal["", "Enthalpy", "None", "Sensible"] | None = "None",
        sensible_heat_recovery_effectiveness: float | None = 0.7,
        latent_heat_recovery_effectiveness: float | None = 0.65,
        humidifier_type: Literal["", "ElectricSteam", "None"] | None = "None",
        humidifier_availability_schedule_name: str | None = ...,
        humidifier_rated_capacity: float | None = ...,
        humidifier_rated_electric_power: float | Literal["", "Autosize"] | None = "Autosize",
        humidifier_control_zone_name: str | None = ...,
        humidifier_setpoint: float | None = 30,
        return_fan: Literal["", "No", "Yes"] | None = "No",
        return_fan_total_efficiency: float | None = 0.7,
        return_fan_delta_pressure: float | None = 500,
        return_fan_motor_efficiency: float | None = 0.9,
        return_fan_motor_in_air_stream_fraction: float | None = 1,
    ) -> None: ...

class AnySizingZone:
    def __call__(
        self,
        /,
        *,
        zone_or_zonelist_name: str,
        zone_cooling_design_supply_air_humidity_ratio: float,
        zone_heating_design_supply_air_humidity_ratio: float,
        zone_cooling_design_supply_air_temperature_input_method: Literal[
            "", "SupplyAirTemperature", "TemperatureDifference"
        ]
        | None = "SupplyAirTemperature",
        zone_cooling_design_supply_air_temperature: float | None = ...,
        zone_cooling_design_supply_air_temperature_difference: float | None = ...,
        zone_heating_design_supply_air_temperature_input_method: Literal[
            "", "SupplyAirTemperature", "TemperatureDifference"
        ]
        | None = "SupplyAirTemperature",
        zone_heating_design_supply_air_temperature: float | None = ...,
        zone_heating_design_supply_air_temperature_difference: float | None = ...,
        design_specification_outdoor_air_object_name: str | None = ...,
        zone_heating_sizing_factor: float | None = ...,
        zone_cooling_sizing_factor: float | None = ...,
        cooling_design_air_flow_method: Literal["", "DesignDay", "DesignDayWithLimit", "Flow/Zone"]
        | None = "DesignDay",
        cooling_design_air_flow_rate: float | None = 0,
        cooling_minimum_air_flow_per_zone_floor_area: float | None = 0.000762,
        cooling_minimum_air_flow: float | None = 0,
        cooling_minimum_air_flow_fraction: float | None = 0.2,
        heating_design_air_flow_method: Literal["", "DesignDay", "DesignDayWithLimit", "Flow/Zone"]
        | None = "DesignDay",
        heating_design_air_flow_rate: float | None = 0,
        heating_maximum_air_flow_per_zone_floor_area: float | None = 0.002032,
        heating_maximum_air_flow: float | None = 0.1415762,
        heating_maximum_air_flow_fraction: float | None = 0.3,
        design_specification_zone_air_distribution_object_name: str | None = ...,
        account_for_dedicated_outdoor_air_system: Literal["", "No", "Yes"] | None = "No",
        dedicated_outdoor_air_system_control_strategy: Literal[
            "", "ColdSupplyAir", "NeutralDehumidifiedSupplyAir", "NeutralSupplyAir"
        ]
        | None = "NeutralSupplyAir",
        dedicated_outdoor_air_low_setpoint_temperature_for_design: float | Literal["", "Autosize"] | None = "Autosize",
        dedicated_outdoor_air_high_setpoint_temperature_for_design: float | Literal["", "Autosize"] | None = "Autosize",
    ) -> None: ...

class DesignSpecificationZoneHVACSizing:
    def __call__(
        self,
        name: str,
        /,
        *,
        cooling_supply_air_flow_rate_method: Literal[
            "",
            "FlowPerCoolingCapacity",
            "FlowPerFloorArea",
            "FractionOfAutosizedCoolingAirflow",
            "None",
            "SupplyAirFlowRate",
        ]
        | None = "SupplyAirFlowRate",
        cooling_supply_air_flow_rate: float | Literal["Autosize"] | None = ...,
        cooling_supply_air_flow_rate_per_floor_area: float | None = ...,
        cooling_fraction_of_autosized_cooling_supply_air_flow_rate: float | None = ...,
        cooling_supply_air_flow_rate_per_unit_cooling_capacity: float | None = ...,
        no_load_supply_air_flow_rate_method: Literal[
            "",
            "FlowPerFloorArea",
            "FractionOfAutosizedCoolingAirflow",
            "FractionOfAutosizedHeatingAirflow",
            "None",
            "SupplyAirFlowRate",
        ]
        | None = "SupplyAirFlowRate",
        no_load_supply_air_flow_rate: float | Literal["Autosize"] | None = ...,
        no_load_supply_air_flow_rate_per_floor_area: float | None = ...,
        no_load_fraction_of_cooling_supply_air_flow_rate: float | None = ...,
        no_load_fraction_of_heating_supply_air_flow_rate: float | None = ...,
        heating_supply_air_flow_rate_method: Literal[
            "",
            "FlowPerFloorArea",
            "FlowPerHeatingCapacity",
            "FractionOfAutosizedHeatingAirflow",
            "None",
            "SupplyAirFlowRate",
        ]
        | None = "SupplyAirFlowRate",
        heating_supply_air_flow_rate: float | Literal["Autosize"] | None = ...,
        heating_supply_air_flow_rate_per_floor_area: float | None = ...,
        heating_fraction_of_heating_supply_air_flow_rate: float | None = ...,
        heating_supply_air_flow_rate_per_unit_heating_capacity: float | None = ...,
        cooling_design_capacity_method: Literal[
            "", "CapacityPerFloorArea", "CoolingDesignCapacity", "FractionOfAutosizedCoolingCapacity", "None"
        ]
        | None = "None",
        cooling_design_capacity: float | Literal["Autosize"] | None = ...,
        cooling_design_capacity_per_floor_area: float | None = ...,
        fraction_of_autosized_cooling_design_capacity: float | None = ...,
        heating_design_capacity_method: Literal[
            "", "CapacityPerFloorArea", "FractionOfAutosizedHeatingCapacity", "HeatingDesignCapacity", "None"
        ]
        | None = "None",
        heating_design_capacity: float | Literal["Autosize"] | None = ...,
        heating_design_capacity_per_floor_area: float | None = ...,
        fraction_of_autosized_heating_design_capacity: float | None = ...,
    ) -> None: ...

class AnySizingSystem:
    def __call__(
        self,
        /,
        *,
        airloop_name: str,
        preheat_design_temperature: float,
        preheat_design_humidity_ratio: float,
        precool_design_temperature: float,
        precool_design_humidity_ratio: float,
        central_cooling_design_supply_air_temperature: float,
        central_heating_design_supply_air_temperature: float,
        type_of_load_to_size_on: Literal["", "Sensible", "Total", "VentilationRequirement"] | None = "Sensible",
        design_outdoor_air_flow_rate: float | Literal["", "Autosize"] | None = "Autosize",
        central_heating_maximum_system_air_flow_ratio: float | Literal["", "Autosize"] | None = "Autosize",
        type_of_zone_sum_to_use: Literal["", "Coincident", "NonCoincident"] | None = "NonCoincident",
        central_cooling_design_supply_air_humidity_ratio: float | None = 0.008,
        central_heating_design_supply_air_humidity_ratio: float | None = 0.008,
        cooling_supply_air_flow_rate_method: Literal[
            "",
            "DesignDay",
            "Flow/System",
            "FlowPerCoolingCapacity",
            "FlowPerFloorArea",
            "FractionOfAutosizedCoolingAirflow",
        ]
        | None = "DesignDay",
        cooling_supply_air_flow_rate: float | None = 0,
        cooling_supply_air_flow_rate_per_floor_area: float | None = ...,
        cooling_fraction_of_autosized_cooling_supply_air_flow_rate: float | None = ...,
        cooling_supply_air_flow_rate_per_unit_cooling_capacity: float | None = ...,
        heating_supply_air_flow_rate_method: Literal[
            "",
            "DesignDay",
            "Flow/System",
            "FlowPerFloorArea",
            "FlowPerHeatingCapacity",
            "FractionOfAutosizedCoolingAirflow",
            "FractionOfAutosizedHeatingAirflow",
        ]
        | None = "DesignDay",
        heating_supply_air_flow_rate: float | None = 0,
        heating_supply_air_flow_rate_per_floor_area: float | None = ...,
        heating_fraction_of_autosized_heating_supply_air_flow_rate: float | None = ...,
        heating_fraction_of_autosized_cooling_supply_air_flow_rate: float | None = ...,
        heating_supply_air_flow_rate_per_unit_heating_capacity: float | None = ...,
        system_outdoor_air_method: Literal["", "ZoneSum"] | None = "ZoneSum",
        zone_maximum_outdoor_air_fraction: float | None = 1,
        cooling_design_capacity_method: Literal[
            "", "CapacityPerFloorArea", "CoolingDesignCapacity", "FractionOfAutosizedCoolingCapacity", "None"
        ]
        | None = "CoolingDesignCapacity",
        cooling_design_capacity: float | Literal["", "Autosize"] | None = "Autosize",
        cooling_design_capacity_per_floor_area: float | None = ...,
        fraction_of_autosized_cooling_design_capacity: float | None = ...,
        heating_design_capacity_method: Literal[
            "", "CapacityPerFloorArea", "FractionOfAutosizedHeatingCapacity", "HeatingDesignCapacity", "None"
        ]
        | None = "HeatingDesignCapacity",
        heating_design_capacity: float | Literal["", "Autosize"] | None = "Autosize",
        heating_design_capacity_per_floor_area: float | None = ...,
        fraction_of_autosized_heating_design_capacity: float | None = ...,
        central_cooling_capacity_control_method: Literal["", "Bypass", "OnOff", "VAV", "VT"] | None = "OnOff",
    ) -> None: ...

class ZoneHVACDehumidifierDX:
    def __call__(
        self,
        name: str,
        /,
        *,
        air_inlet_node_name: str,
        air_outlet_node_name: str,
        rated_water_removal: float,
        rated_energy_factor: float,
        rated_air_flow_rate: float,
        water_removal_curve_name: str,
        energy_factor_curve_name: str,
        part_load_fraction_correlation_curve_name: str,
        availability_schedule_name: str | None = ...,
        minimum_dry_bulb_temperature_for_dehumidifier_operation: float | None = 10,
        maximum_dry_bulb_temperature_for_dehumidifier_operation: float | None = 35,
        off_cycle_parasitic_electric_load: float | None = 0,
        condensate_collection_water_storage_tank_name: str | None = ...,
    ) -> None: ...

class AnyZoneHVACBaseboardRadiantConvectiveWater:
    def __call__(
        self,
        name: str,
        /,
        *,
        inlet_node_name: str,
        outlet_node_name: str,
        maximum_water_flow_rate: float | Literal["Autosize"],
        availability_schedule_name: str | None = ...,
        rated_average_water_temperature: float | None = 87.78,
        rated_water_mass_flow_rate: float | None = 0.063,
        heating_design_capacity: float | Literal["", "Autosize"] | None = "Autosize",
        surface_fractions: list[Any] = ...,
    ) -> None: ...

class AnyFanSystemModel:
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
        design_electric_power_consumption: float | Literal["Autosize"] | None = ...,
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

class FanPerformanceNightVentilation:
    def __call__(
        self,
        /,
        *,
        fan_name: str,
        fan_total_efficiency: float,
        pressure_rise: float,
        motor_efficiency: float,
        maximum_flow_rate: float | Literal["Autosize"] | None = ...,
        motor_in_airstream_fraction: float | None = 1,
    ) -> None: ...

class CoilSystemCoolingDXHeatExchangerAssisted:
    def __call__(
        self,
        name: str,
        /,
        *,
        heat_exchanger_object_type: Literal[
            "HeatExchanger:AirToAir:FlatPlate",
            "HeatExchanger:AirToAir:SensibleAndLatent",
            "HeatExchanger:Desiccant:BalancedFlow",
        ],
        heat_exchanger_name: str,
        cooling_coil_object_type: Literal[
            "Coil:Cooling:DX", "Coil:Cooling:DX:SingleSpeed", "Coil:Cooling:DX:VariableSpeed"
        ],
        cooling_coil_name: str,
    ) -> None: ...

class AirLoopHVACControllerList:
    def __call__(
        self,
        name: str,
        /,
        *,
        controller_1_object_type: Literal["Controller:OutdoorAir", "Controller:WaterCoil"],
        controller_1_name: str,
        controller_2_object_type: Literal["Controller:OutdoorAir", "Controller:WaterCoil"] | None = ...,
        controller_2_name: str | None = ...,
        controller_3_object_type: Literal["Controller:OutdoorAir", "Controller:WaterCoil"] | None = ...,
        controller_3_name: str | None = ...,
        controller_4_object_type: Literal["Controller:OutdoorAir", "Controller:WaterCoil"] | None = ...,
        controller_4_name: str | None = ...,
        controller_5_object_type: Literal["Controller:OutdoorAir", "Controller:WaterCoil"] | None = ...,
        controller_5_name: str | None = ...,
        controller_6_object_type: Literal["Controller:OutdoorAir", "Controller:WaterCoil"] | None = ...,
        controller_6_name: str | None = ...,
        controller_7_object_type: Literal["Controller:OutdoorAir", "Controller:WaterCoil"] | None = ...,
        controller_7_name: str | None = ...,
        controller_8_object_type: Literal["Controller:OutdoorAir", "Controller:WaterCoil"] | None = ...,
        controller_8_name: str | None = ...,
    ) -> None: ...

class PipeOutdoor:
    def __call__(
        self,
        name: str,
        /,
        *,
        construction_name: str,
        fluid_inlet_node_name: str,
        fluid_outlet_node_name: str,
        ambient_temperature_outdoor_air_node_name: str | None = ...,
        pipe_inside_diameter: float | None = ...,
        pipe_length: float | None = ...,
    ) -> None: ...

class AnyPipingSystemUndergroundPipeCircuit:
    def __call__(
        self,
        name: str,
        /,
        *,
        pipe_thermal_conductivity: float,
        pipe_density: float,
        pipe_specific_heat: float,
        pipe_inner_diameter: float,
        pipe_outer_diameter: float,
        design_flow_rate: float,
        circuit_inlet_node: str,
        circuit_outlet_node: str,
        radial_thickness_of_inner_radial_near_pipe_mesh_region: float,
        number_of_pipe_segments_entered_for_this_pipe_circuit: int,
        convergence_criterion_for_the_inner_radial_iteration_loop: float | None = 0.001,
        maximum_iterations_in_the_inner_radial_iteration_loop: int | None = 500,
        number_of_soil_nodes_in_the_inner_radial_near_pipe_mesh_region: int | None = 3,
        pipe_segments: list[Any] = ...,
    ) -> None: ...

class PipingSystemUndergroundPipeCircuit:
    def __call__(
        self,
        name: str,
        /,
        *,
        pipe_thermal_conductivity: float,
        pipe_density: float,
        pipe_specific_heat: float,
        pipe_inner_diameter: float,
        pipe_outer_diameter: float,
        design_flow_rate: float,
        circuit_inlet_node: str,
        circuit_outlet_node: str,
        radial_thickness_of_inner_radial_near_pipe_mesh_region: float,
        number_of_pipe_segments_entered_for_this_pipe_circuit: int,
        convergence_criterion_for_the_inner_radial_iteration_loop: float | None = 0.001,
        maximum_iterations_in_the_inner_radial_iteration_loop: int | None = 500,
        number_of_soil_nodes_in_the_inner_radial_near_pipe_mesh_region: int | None = 3,
        pipe_segments: list[Any] = ...,
    ) -> None: ...

class PumpVariableSpeed:
    def __call__(
        self,
        name: str,
        /,
        *,
        inlet_node_name: str,
        outlet_node_name: str,
        design_maximum_flow_rate: float | Literal["Autosize"] | None = ...,
        design_pump_head: float | None = 179352,
        design_power_consumption: float | Literal["Autosize"] | None = ...,
        motor_efficiency: float | None = 0.9,
        fraction_of_motor_inefficiencies_to_fluid_stream: float | None = 0,
        coefficient_1_of_the_part_load_performance_curve: float | None = 0,
        coefficient_2_of_the_part_load_performance_curve: float | None = 1,
        coefficient_3_of_the_part_load_performance_curve: float | None = 0,
        coefficient_4_of_the_part_load_performance_curve: float | None = 0,
        design_minimum_flow_rate: float | Literal["", "Autosize"] | None = "Autosize",
        pump_control_type: Literal["", "Continuous", "Intermittent"] | None = "Continuous",
        pump_flow_rate_schedule_name: str | None = ...,
        pump_curve_name: str | None = ...,
        impeller_diameter: float | None = ...,
        vfd_control_type: Literal["ManualControl", "PressureSetpointControl"] | None = ...,
        pump_rpm_schedule_name: str | None = ...,
        minimum_pressure_schedule: str | None = ...,
        maximum_pressure_schedule: str | None = ...,
        minimum_rpm_schedule: str | None = ...,
        maximum_rpm_schedule: str | None = ...,
        zone_name: str | None = ...,
        skin_loss_radiative_fraction: float | None = ...,
        design_power_sizing_method: Literal["", "PowerPerFlow", "PowerPerFlowPerPressure"]
        | None = "PowerPerFlowPerPressure",
        design_electric_power_per_unit_flow_rate: float | None = 348701.1,
        design_shaft_power_per_unit_flow_rate_per_unit_head: float | None = 1.282051282,
        design_minimum_flow_rate_fraction: float | None = 0,
        end_use_subcategory: str | None = "General",
    ) -> None: ...

class BoilerSteam:
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
        maximum_operating_pressure: float | None = 160000,
        theoretical_efficiency: float | None = 0.8,
        design_outlet_steam_temperature: float | None = 100,
        nominal_capacity: float | Literal["Autosize"] | None = ...,
        minimum_part_load_ratio: float | None = ...,
        maximum_part_load_ratio: float | None = ...,
        optimum_part_load_ratio: float | None = ...,
        coefficient_1_of_fuel_use_function_of_part_load_ratio_curve: float | None = ...,
        coefficient_2_of_fuel_use_function_of_part_load_ratio_curve: float | None = ...,
        coefficient_3_of_fuel_use_function_of_part_load_ratio_curve: float | None = ...,
        water_inlet_node_name: str | None = ...,
        steam_outlet_node_name: str | None = ...,
        sizing_factor: float | None = 1,
        end_use_subcategory: str | None = "General",
    ) -> None: ...

class ChillerHeaterAbsorptionDoubleEffect:
    def __call__(
        self,
        name: str,
        /,
        *,
        chilled_water_inlet_node_name: str,
        chilled_water_outlet_node_name: str,
        condenser_inlet_node_name: str,
        hot_water_inlet_node_name: str,
        hot_water_outlet_node_name: str,
        exhaust_source_object_type: Literal["Generator:MicroTurbine"],
        nominal_cooling_capacity: float | Literal["", "Autosize"] | None = "Autosize",
        heating_to_cooling_capacity_ratio: float | None = 0.8,
        thermal_energy_input_to_cooling_output_ratio: float | None = 0.97,
        thermal_energy_input_to_heating_output_ratio: float | None = 1.25,
        electric_input_to_cooling_output_ratio: float | None = 0.01,
        electric_input_to_heating_output_ratio: float | None = 0,
        condenser_outlet_node_name: str | None = ...,
        minimum_part_load_ratio: float | None = 0.1,
        maximum_part_load_ratio: float | None = 1,
        optimum_part_load_ratio: float | None = 1,
        design_entering_condenser_water_temperature: float | None = 29,
        design_leaving_chilled_water_temperature: float | None = 7,
        design_chilled_water_flow_rate: float | Literal["", "Autosize"] | None = "Autosize",
        design_condenser_water_flow_rate: float | Literal["", "Autosize"] | None = "Autosize",
        design_hot_water_flow_rate: float | Literal["", "Autosize"] | None = "Autosize",
        cooling_capacity_function_of_temperature_curve_name: str | None = ...,
        fuel_input_to_cooling_output_ratio_function_of_temperature_curve_name: str | None = ...,
        fuel_input_to_cooling_output_ratio_function_of_part_load_ratio_curve_name: str | None = ...,
        electric_input_to_cooling_output_ratio_function_of_temperature_curve_name: str | None = ...,
        electric_input_to_cooling_output_ratio_function_of_part_load_ratio_curve_name: str | None = ...,
        heating_capacity_function_of_cooling_capacity_curve_name: str | None = ...,
        fuel_input_to_heat_output_ratio_during_heating_only_operation_curve_name: str | None = ...,
        temperature_curve_input_variable: Literal["", "EnteringCondenser", "LeavingCondenser"]
        | None = "EnteringCondenser",
        condenser_type: Literal["", "AirCooled", "WaterCooled"] | None = "WaterCooled",
        chilled_water_temperature_lower_limit: float | None = 2,
        exhaust_source_object_name: str | None = ...,
        sizing_factor: float | None = 1,
    ) -> None: ...

class HeatPumpWaterToWaterEquationFitCooling:
    def __call__(
        self,
        name: str,
        /,
        *,
        source_side_inlet_node_name: str,
        source_side_outlet_node_name: str,
        load_side_inlet_node_name: str,
        load_side_outlet_node_name: str,
        reference_load_side_flow_rate: float | Literal["Autosize"],
        reference_source_side_flow_rate: float | Literal["Autosize"],
        reference_cooling_capacity: float | Literal["Autosize"],
        reference_cooling_power_consumption: float | Literal["Autosize"],
        cooling_capacity_curve_name: str,
        cooling_compressor_power_curve_name: str,
        reference_coefficient_of_performance: float | None = 8,
        sizing_factor: float | None = 1,
        companion_heating_heat_pump_name: str | None = ...,
    ) -> None: ...

class GroundHeatExchangerSystem:
    def __call__(
        self,
        name: str,
        /,
        *,
        inlet_node_name: str,
        outlet_node_name: str,
        design_flow_rate: float,
        undisturbed_ground_temperature_model_type: Literal[
            "Site:GroundTemperature:Undisturbed:FiniteDifference",
            "Site:GroundTemperature:Undisturbed:KusudaAchenbach",
            "Site:GroundTemperature:Undisturbed:Xing",
        ],
        undisturbed_ground_temperature_model_name: str,
        ground_thermal_conductivity: float,
        ground_thermal_heat_capacity: float,
        ghe_vertical_responsefactors_object_name: str | None = ...,
        g_function_calculation_method: Literal["", "FullDesign", "UBHWTcalc", "UHFcalc"] | None = "UHFcalc",
        ghe_vertical_sizing_object_type: Literal["GroundHeatExchanger:Vertical:Sizing:Rectangle"] | None = ...,
        ghe_vertical_sizing_object_name: str | None = ...,
        ghe_vertical_array_object_name: str | None = ...,
        vertical_well_locations: list[Any] = ...,
    ) -> None: ...

class ThermalStoragePCM:
    def __call__(
        self,
        name: str,
        /,
        *,
        availability_schedule_name: str,
        plant_side_inlet_node_name: str,
        plant_side_outlet_node_name: str,
        use_side_inlet_node_name: str,
        use_side_outlet_node_name: str,
        pcm_material_name: str,
        tank_capacity: float | Literal["Autosize"],
        use_side_design_flow_rate: float | Literal["Autosize"],
        plant_side_design_flow_rate: float | Literal["Autosize"],
        heat_loss_rate: float | None = 0,
    ) -> None: ...

class ThermalStorageSizing:
    def __call__(
        self,
        name: str,
        /,
        *,
        on_peak_period_start_time: float,
        on_peak_period_end_time: float,
        sizing_factor: float | None = 1,
    ) -> None: ...

class EnergyManagementSystemGlobalVariable:
    def __call__(self, /, *, variables: list[Any] = ...) -> None: ...

class AvailabilityManagerHybridVentilation:
    def __call__(
        self,
        name: str,
        /,
        *,
        control_zone_name: str,
        ventilation_control_mode_schedule_name: str,
        hvac_air_loop_name: str | None = ...,
        use_weather_file_rain_indicators: Literal["", "No", "Yes"] | None = "Yes",
        maximum_wind_speed: float | None = 40,
        minimum_outdoor_temperature: float | None = -100,
        maximum_outdoor_temperature: float | None = 100,
        minimum_outdoor_enthalpy: float | None = ...,
        maximum_outdoor_enthalpy: float | None = ...,
        minimum_outdoor_dewpoint: float | None = -100,
        maximum_outdoor_dewpoint: float | None = 100,
        minimum_outdoor_ventilation_air_schedule_name: str | None = ...,
        opening_factor_function_of_wind_speed_curve_name: str | None = ...,
        airflownetwork_control_type_schedule_name: str | None = ...,
        simple_airflow_control_type_schedule_name: str | None = ...,
        zoneventilation_object_name: str | None = ...,
        minimum_hvac_operation_time: float | None = 0,
        minimum_ventilation_time: float | None = 0,
    ) -> None: ...

class SetpointManagerOutdoorAirPretreat:
    def __call__(
        self,
        name: str,
        /,
        *,
        mixed_air_stream_node_name: str,
        outdoor_air_stream_node_name: str,
        return_air_stream_node_name: str,
        setpoint_node_or_nodelist_name: str,
        control_variable: Literal["HumidityRatio", "MaximumHumidityRatio", "MinimumHumidityRatio", "Temperature"]
        | None = ...,
        minimum_setpoint_temperature: float | None = -99,
        maximum_setpoint_temperature: float | None = 99,
        minimum_setpoint_humidity_ratio: float | None = ...,
        maximum_setpoint_humidity_ratio: float | None = 1,
        reference_setpoint_node_name: str | None = ...,
    ) -> None: ...

class SetpointManagerReturnAirBypassFlow:
    def __call__(
        self,
        name: str,
        /,
        *,
        hvac_air_loop_name: str,
        control_variable: Literal["", "Flow"] | None = "Flow",
        temperature_setpoint_schedule_name: str | None = ...,
    ) -> None: ...

class SetpointManagerWarmestTemperatureFlow:
    def __call__(
        self,
        name: str,
        /,
        *,
        hvac_air_loop_name: str,
        setpoint_node_or_nodelist_name: str,
        control_variable: Literal["Temperature"] | None = ...,
        minimum_setpoint_temperature: float | None = 12,
        maximum_setpoint_temperature: float | None = 18,
        strategy: Literal["", "FlowFirst", "TemperatureFirst"] | None = "TemperatureFirst",
        minimum_turndown_ratio: float | None = 0.2,
    ) -> None: ...

class RefrigerationCompressor:
    def __call__(
        self,
        name: str,
        /,
        *,
        refrigeration_compressor_power_curve_name: str,
        refrigeration_compressor_capacity_curve_name: str,
        rated_superheat: float | None = ...,
        rated_return_gas_temperature: float | None = ...,
        rated_liquid_temperature: float | None = ...,
        rated_subcooling: float | None = ...,
        end_use_subcategory: str | None = "General",
        mode_of_operation: Literal["", "Subcritical", "Transcritical"] | None = "Subcritical",
        transcritical_compressor_power_curve_name: str | None = ...,
        transcritical_compressor_capacity_curve_name: str | None = ...,
    ) -> None: ...

class AnyLifeCycleCostUseAdjustment:
    def __call__(
        self,
        name: str,
        /,
        *,
        resource: Literal[
            "Coal",
            "Diesel",
            "Electricity",
            "ElectricityNet",
            "ElectricityProduced",
            "ElectricityPurchased",
            "ElectricitySurplusSold",
            "Gasoline",
            "NaturalGas",
            "OtherFuel1",
            "OtherFuel2",
            "Propane",
            "Water",
        ],
        multipliers: list[Any] = ...,
    ) -> None: ...

class LifeCycleCostUseAdjustment:
    def __call__(
        self,
        name: str,
        /,
        *,
        resource: Literal[
            "Coal",
            "Diesel",
            "DistrictCooling",
            "DistrictHeatingSteam",
            "DistrictHeatingWater",
            "Electricity",
            "ElectricityNet",
            "ElectricityProduced",
            "ElectricityPurchased",
            "ElectricitySurplusSold",
            "FuelOilNo1",
            "FuelOilNo2",
            "Gasoline",
            "NaturalGas",
            "OtherFuel1",
            "OtherFuel2",
            "Propane",
            "Water",
        ],
        multipliers: list[Any] = ...,
    ) -> None: ...

class OutputPreprocessorMessage:
    def __call__(
        self,
        /,
        *,
        preprocessor_name: str | None = ...,
        error_severity: Literal["Fatal", "Information", "Severe", "Warning"] | None = ...,
        message_line_1: str | None = ...,
        message_line_2: str | None = ...,
        message_line_3: str | None = ...,
        message_line_4: str | None = ...,
        message_line_5: str | None = ...,
        message_line_6: str | None = ...,
        message_line_7: str | None = ...,
        message_line_8: str | None = ...,
        message_line_9: str | None = ...,
        message_line_10: str | None = ...,
    ) -> None: ...
