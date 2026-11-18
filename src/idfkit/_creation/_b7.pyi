"""Creation signatures of generated classes (stub only).

DO NOT EDIT — regenerate with:
    python -m idfkit.codegen.generate_stubs
"""

from __future__ import annotations

from typing import Any, Literal

from typing_extensions import Never

class WindowsCalculationEngine:
    def __call__(
        self,
        /,
        *,
        windows_engine: Literal["", "BuiltInWindowsModel", "ExternalWindowsModel"] | None = "BuiltInWindowsModel",
    ) -> None: ...

class WallUnderground:
    def __call__(
        self,
        name: str,
        /,
        *,
        construction_name: str,
        zone_name: str,
        space_name: str | None = ...,
        azimuth_angle: float | None = ...,
        tilt_angle: float | None = 90,
        starting_x_coordinate: float | None = ...,
        starting_y_coordinate: float | None = ...,
        starting_z_coordinate: float | None = ...,
        length: float | None = ...,
        height: float | None = ...,
    ) -> None: ...

class CeilingInterzone:
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
        tilt_angle: float | None = 0,
        starting_x_coordinate: float | None = ...,
        starting_y_coordinate: float | None = ...,
        starting_z_coordinate: float | None = ...,
        length: float | None = ...,
        width: float | None = ...,
    ) -> None: ...

class ShadingBuilding:
    def __call__(
        self,
        name: str,
        /,
        *,
        azimuth_angle: float | None = ...,
        tilt_angle: float | None = 90,
        starting_x_coordinate: float | None = ...,
        starting_y_coordinate: float | None = ...,
        starting_z_coordinate: float | None = ...,
        length: float | None = ...,
        height: float | None = ...,
    ) -> None: ...

class GroundHeatTransferSlabInsulation:
    def __call__(
        self,
        /,
        *,
        rins_r_value_of_under_slab_insulation: float | None = 0,
        dins_width_of_strip_of_under_slab_insulation: float | None = 0,
        rvins_r_value_of_vertical_insulation: float | None = 0,
        zvins_depth_of_vertical_insulation: float | None = 0,
        ivins_flag_is_there_vertical_insulation: Literal[0, 1, ""] | None = 0,
    ) -> None: ...

class ElectricEquipmentITEAirCooledDefinition:
    def __call__(
        self,
        name: str,
        /,
        *,
        cpu_power_input_function_of_loading_and_air_temperature_curve_name: str,
        design_fan_air_flow_rate_per_power_input: float,
        air_flow_function_of_loading_and_air_temperature_curve_name: str,
        fan_power_input_function_of_flow_curve_name: str,
        air_flow_calculation_method: Literal["", "FlowControlWithApproachTemperatures", "FlowFromSystem"]
        | None = "FlowFromSystem",
        design_power_input_calculation_method: Literal["", "EquipmentLevel", "Watts/Area"] | None = "EquipmentLevel",
        watts_per_unit: float | None = ...,
        watts_per_floor_area: float | None = ...,
        design_fan_power_input_fraction: float | None = 0,
        design_entering_air_temperature: float | None = 15,
        environmental_class: Literal["", "A1", "A2", "A3", "A4", "B", "C", "H1", "None"] | None = "None",
        air_inlet_connection_type: Literal["", "AdjustedSupply", "RoomAirModel", "ZoneAirNode"]
        | None = "AdjustedSupply",
        design_recirculation_fraction: float | None = 0,
        recirculation_function_of_loading_and_supply_temperature_curve_name: str | None = ...,
        design_electric_power_supply_efficiency: float | None = 1,
        electric_power_supply_efficiency_function_of_part_load_ratio_curve_name: str | None = ...,
        fraction_of_electric_power_supply_losses_to_zone: float | None = 1,
        supply_temperature_difference: float | None = ...,
        supply_temperature_difference_schedule: str | None = ...,
        return_temperature_difference: float | None = ...,
        return_temperature_difference_schedule: str | None = ...,
    ) -> None: ...

class AirflowNetworkMultiZoneComponentHorizontalOpening:
    def __call__(
        self,
        name: str,
        /,
        *,
        air_mass_flow_coefficient_when_opening_is_closed: float,
        discharge_coefficient: float,
        air_mass_flow_exponent_when_opening_is_closed: float | None = 0.65,
        sloping_plane_angle: float | None = 90,
    ) -> None: ...

class AirflowNetworkDistributionNode:
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
            "Zone",
        ]
        | None = "Other",
        node_height: float | None = 0,
    ) -> None: ...

class DuctLossLeakage:
    def __call__(
        self, name: str, /, *, airloophvac_name: str, airflownetwork_distribution_linkage_name: str
    ) -> None: ...

class AnyZoneControlHumidistat:
    def __call__(self, name: str, /, *, narrow_with_as_version_first: Never, zone_name: str) -> None: ...

class ZoneHVACEvaporativeCoolerUnit:
    def __call__(
        self,
        name: str,
        /,
        *,
        outdoor_air_inlet_node_name: str,
        cooler_outlet_node_name: str,
        supply_air_fan_object_type: Literal[
            "Fan:ComponentModel", "Fan:ConstantVolume", "Fan:OnOff", "Fan:SystemModel", "Fan:VariableVolume"
        ],
        supply_air_fan_name: str,
        design_supply_air_flow_rate: float | Literal["Autosize"],
        fan_placement: Literal["BlowThrough", "DrawThrough"],
        cooler_unit_control_method: Literal[
            "ZoneCoolingLoadOnOffCycling", "ZoneCoolingLoadVariableSpeedFan", "ZoneTemperatureDeadbandOnOffCycling"
        ],
        first_evaporative_cooler_object_type: Literal[
            "EvaporativeCooler:Direct:CelDekPad",
            "EvaporativeCooler:Direct:ResearchSpecial",
            "EvaporativeCooler:Indirect:CelDekPad",
            "EvaporativeCooler:Indirect:ResearchSpecial",
            "EvaporativeCooler:Indirect:WetCoil",
        ],
        first_evaporative_cooler_object_name: str,
        availability_schedule_name: str | None = ...,
        availability_manager_list_name: str | None = ...,
        zone_relief_air_node_name: str | None = ...,
        throttling_range_temperature_difference: float | None = 1,
        cooling_load_control_threshold_heat_transfer_rate: float | None = 100,
        second_evaporative_cooler_object_type: Literal[
            "EvaporativeCooler:Direct:CelDekPad",
            "EvaporativeCooler:Direct:ResearchSpecial",
            "EvaporativeCooler:Indirect:CelDekPad",
            "EvaporativeCooler:Indirect:ResearchSpecial",
            "EvaporativeCooler:Indirect:WetCoil",
        ]
        | None = ...,
        second_evaporative_cooler_name: str | None = ...,
        design_specification_zonehvac_sizing_object_name: str | None = ...,
        shut_off_relative_humidity: float | None = ...,
    ) -> None: ...

class ZoneHVACCoolingPanelRadiantConvectiveWater:
    def __call__(
        self,
        name: str,
        /,
        *,
        availability_schedule_name: str,
        water_inlet_node_name: str,
        water_outlet_node_name: str,
        maximum_chilled_water_flow_rate: float | Literal["Autosize"],
        fraction_radiant: float,
        rated_inlet_water_temperature: float | None = 5,
        rated_inlet_space_temperature: float | None = 24,
        rated_water_mass_flow_rate: float | None = 0.063,
        cooling_design_capacity_method: Literal[
            "", "CapacityPerFloorArea", "CoolingDesignCapacity", "FractionOfAutosizedCoolingCapacity", "None"
        ]
        | None = "CoolingDesignCapacity",
        cooling_design_capacity: float | Literal["Autosize"] | None = ...,
        cooling_design_capacity_per_floor_area: float | None = ...,
        fraction_of_autosized_cooling_design_capacity: float | None = ...,
        control_type: Literal[
            "",
            "MeanAirTemperature",
            "MeanRadiantTemperature",
            "OperativeTemperature",
            "OutdoorDryBulbTemperature",
            "OutdoorWetBulbTemperature",
            "ZoneConvectiveLoad",
            "ZoneTotalLoad",
        ]
        | None = "MeanAirTemperature",
        cooling_control_throttling_range: float | None = 0.5,
        cooling_control_temperature_schedule_name: str | None = ...,
        condensation_control_type: Literal["", "Off", "SimpleOff", "VariableOff"] | None = "SimpleOff",
        condensation_control_dewpoint_offset: float | None = 1,
        fraction_of_radiant_energy_incident_on_people: float | None = ...,
        surface_fractions: list[Any] = ...,
    ) -> None: ...

class CoilHeatingDXSingleSpeed:
    def __call__(
        self,
        name: str,
        /,
        *,
        gross_rated_heating_capacity: float | Literal["Autosize"],
        gross_rated_heating_cop: float,
        rated_air_flow_rate: float | Literal["Autosize"],
        air_inlet_node_name: str,
        air_outlet_node_name: str,
        heating_capacity_function_of_temperature_curve_name: str,
        heating_capacity_function_of_flow_fraction_curve_name: str,
        energy_input_ratio_function_of_temperature_curve_name: str,
        energy_input_ratio_function_of_flow_fraction_curve_name: str,
        part_load_fraction_correlation_curve_name: str,
        availability_schedule_name: str | None = ...,
        defrost_energy_input_ratio_function_of_temperature_curve_name: str | None = ...,
        minimum_outdoor_dry_bulb_temperature_for_compressor_operation: float | None = -8,
        outdoor_dry_bulb_temperature_to_turn_on_compressor: float | None = ...,
        maximum_outdoor_dry_bulb_temperature_for_defrost_operation: float | None = 5,
        crankcase_heater_capacity: float | None = 0,
        crankcase_heater_capacity_function_of_temperature_curve_name: str | None = ...,
        maximum_outdoor_dry_bulb_temperature_for_crankcase_heater_operation: float | None = 10,
        defrost_strategy: Literal["", "Resistive", "ReverseCycle"] | None = "ReverseCycle",
        defrost_control: Literal["", "OnDemand", "Timed"] | None = "Timed",
        defrost_time_period_fraction: float | None = 0.058333,
        resistive_defrost_heater_capacity: float | Literal["", "Autosize"] | None = 0,
        region_number_for_calculating_hspf: int | None = 4,
        evaporator_air_inlet_node_name: str | None = ...,
        zone_name_for_evaporator_placement: str | None = ...,
        secondary_coil_air_flow_rate: float | Literal["Autosize"] | None = ...,
        secondary_coil_fan_flow_scaling_factor: float | None = 1.25,
        nominal_sensible_heat_ratio_of_secondary_coil: float | None = ...,
        sensible_heat_ratio_modifier_function_of_temperature_curve_name: str | None = ...,
        sensible_heat_ratio_modifier_function_of_flow_fraction_curve_name: str | None = ...,
    ) -> None: ...

class AirLoopHVACUnitaryFurnaceHeatCool:
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
        cooling_coil_object_type: Literal[
            "Coil:Cooling:DX:SingleSpeed",
            "Coil:Cooling:DX:VariableSpeed",
            "CoilSystem:Cooling:DX:HeatExchangerAssisted",
        ],
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

class AnyAirLoopHVACOutdoorAirSystem:
    def __call__(self, name: str, /, *, controller_list_name: str, outdoor_air_equipment_list_name: str) -> None: ...

class BranchList:
    def __call__(self, name: str, /, *, branches: list[Any] = ...) -> None: ...

class PipingSystemUndergroundPipeSegment:
    def __call__(
        self,
        name: str,
        /,
        *,
        x_position: float,
        y_position: float,
        flow_direction: Literal["DecreasingZ", "IncreasingZ"],
    ) -> None: ...

class AnyPumpVariableSpeedCondensate:
    def __call__(
        self,
        name: str,
        /,
        *,
        inlet_node_name: str,
        outlet_node_name: str,
        design_steam_volume_flow_rate: float | Literal["Autosize"] | None = ...,
        design_pump_head: float | None = 179352,
        design_power_consumption: float | Literal["Autosize"] | None = ...,
        motor_efficiency: float | None = 0.9,
        fraction_of_motor_inefficiencies_to_fluid_stream: float | None = 0,
        coefficient_1_of_the_part_load_performance_curve: float | None = 0,
        coefficient_2_of_the_part_load_performance_curve: float | None = 1,
        coefficient_3_of_the_part_load_performance_curve: float | None = 0,
        coefficient_4_of_the_part_load_performance_curve: float | None = 0,
        pump_flow_rate_schedule_name: str | None = ...,
        zone_name: str | None = ...,
        skin_loss_radiative_fraction: float | None = ...,
        design_power_sizing_method: Literal["", "PowerPerFlow", "PowerPerFlowPerPressure"]
        | None = "PowerPerFlowPerPressure",
        design_electric_power_per_unit_flow_rate: float | None = 348701.1,
        design_shaft_power_per_unit_flow_rate_per_unit_head: float | None = 1.282051282,
    ) -> None: ...

class AnyChillerElectricEIR:
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
        reference_leaving_chilled_water_temperature: float | None = 6.67,
        reference_entering_condenser_fluid_temperature: float | None = 29.4,
        reference_chilled_water_flow_rate: float | Literal["Autosize"] | None = ...,
        reference_condenser_fluid_flow_rate: float | Literal["Autosize"] | None = ...,
        minimum_part_load_ratio: float | None = 0.1,
        maximum_part_load_ratio: float | None = 1,
        optimum_part_load_ratio: float | None = 1,
        minimum_unloading_ratio: float | None = 0.2,
        condenser_inlet_node_name: str | None = ...,
        condenser_outlet_node_name: str | None = ...,
        condenser_type: Literal["", "AirCooled", "EvaporativelyCooled", "WaterCooled"] | None = "WaterCooled",
        condenser_fan_power_ratio: float | None = 0,
        fraction_of_compressor_electric_consumption_rejected_by_condenser: float | None = 1,
        leaving_chilled_water_lower_temperature_limit: float | None = 2,
        chiller_flow_mode: Literal["", "ConstantFlow", "LeavingSetpointModulated", "NotModulated"]
        | None = "NotModulated",
        design_heat_recovery_water_flow_rate: float | Literal["", "Autosize"] | None = 0,
        heat_recovery_inlet_node_name: str | None = ...,
        heat_recovery_outlet_node_name: str | None = ...,
        sizing_factor: float | None = 1,
        basin_heater_capacity: float | None = 0,
        basin_heater_setpoint_temperature: float | None = 2,
        basin_heater_operating_schedule_name: str | None = ...,
        condenser_heat_recovery_relative_capacity_fraction: float | None = ...,
        heat_recovery_inlet_high_temperature_limit_schedule_name: str | None = ...,
        heat_recovery_leaving_temperature_setpoint_node_name: str | None = ...,
        end_use_subcategory: str | None = "General",
    ) -> None: ...

class ChillerHeaterPerformanceElectricEIR:
    def __call__(
        self,
        name: str,
        /,
        *,
        reference_cooling_mode_evaporator_capacity: float | Literal["Autosize"],
        reference_cooling_mode_cop: float,
        cooling_mode_cooling_capacity_function_of_temperature_curve_name: str,
        cooling_mode_electric_input_to_cooling_output_ratio_function_of_temperature_curve_name: str,
        cooling_mode_electric_input_to_cooling_output_ratio_function_of_part_load_ratio_curve_name: str,
        heating_mode_cooling_capacity_function_of_temperature_curve_name: str,
        heating_mode_electric_input_to_cooling_output_ratio_function_of_temperature_curve_name: str,
        heating_mode_electric_input_to_cooling_output_ratio_function_of_part_load_ratio_curve_name: str,
        reference_cooling_mode_leaving_chilled_water_temperature: float | None = 6.67,
        reference_cooling_mode_entering_condenser_fluid_temperature: float | None = 29.44,
        reference_cooling_mode_leaving_condenser_water_temperature: float | None = 35,
        reference_heating_mode_cooling_capacity_ratio: float | None = 0.75,
        reference_heating_mode_cooling_power_input_ratio: float | None = 1.38,
        reference_heating_mode_leaving_chilled_water_temperature: float | None = 6.67,
        reference_heating_mode_leaving_condenser_water_temperature: float | None = 49,
        reference_heating_mode_entering_condenser_fluid_temperature: float | None = 29.44,
        heating_mode_entering_chilled_water_temperature_low_limit: float | None = 12.22,
        chilled_water_flow_mode_type: Literal["", "ConstantFlow", "VariableFlow"] | None = "ConstantFlow",
        design_chilled_water_flow_rate: float | Literal["Autosize"] | None = ...,
        design_condenser_water_flow_rate: float | Literal["Autosize"] | None = ...,
        design_hot_water_flow_rate: float | None = 0,
        compressor_motor_efficiency: float | None = 1,
        cooling_mode_temperature_curve_condenser_water_independent_variable: Literal[
            "", "EnteringCondenser", "LeavingCondenser"
        ]
        | None = "EnteringCondenser",
        cooling_mode_cooling_capacity_optimum_part_load_ratio: float | None = 1,
        heating_mode_temperature_curve_condenser_water_independent_variable: Literal[
            "", "EnteringCondenser", "LeavingCondenser"
        ]
        | None = "LeavingCondenser",
        heating_mode_cooling_capacity_optimum_part_load_ratio: float | None = 1,
        sizing_factor: float | None = 1,
    ) -> None: ...

class ExternalInterfaceFunctionalMockupUnitImportToSchedule:
    def __call__(
        self,
        name: str,
        /,
        *,
        fmu_file_name: str,
        fmu_instance_name: str,
        fmu_variable_name: str,
        initial_value: float,
        schedule_type_limits_names: str | None = ...,
    ) -> None: ...

class AvailabilityManagerHighTemperatureTurnOn:
    def __call__(self, name: str, /, *, sensor_node_name: str, temperature: float) -> None: ...

class SetpointManagerOutdoorAirReset:
    def __call__(
        self,
        name: str,
        /,
        *,
        setpoint_at_outdoor_low_temperature: float,
        outdoor_low_temperature: float,
        setpoint_at_outdoor_high_temperature: float,
        outdoor_high_temperature: float,
        setpoint_node_or_nodelist_name: str,
        control_variable: Literal["", "MaximumTemperature", "MinimumTemperature", "Temperature"] | None = "Temperature",
        schedule_name: str | None = ...,
        setpoint_at_outdoor_low_temperature_2: float | None = ...,
        outdoor_low_temperature_2: float | None = ...,
        setpoint_at_outdoor_high_temperature_2: float | None = ...,
        outdoor_high_temperature_2: float | None = ...,
    ) -> None: ...

class SetpointManagerSystemNodeResetTemperature:
    def __call__(
        self,
        name: str,
        /,
        *,
        control_variable: Literal["MaximumTemperature", "MinimumTemperature", "Temperature"],
        setpoint_at_low_reference_temperature: float,
        setpoint_at_high_reference_temperature: float,
        low_reference_temperature: float,
        high_reference_temperature: float,
        reference_node_name: str,
        setpoint_node_or_nodelist_name: str,
    ) -> None: ...

class GeneratorPVWatts:
    def __call__(
        self,
        name: str,
        /,
        *,
        dc_system_capacity: float,
        module_type: Literal["Premium", "Standard", "ThinFilm"],
        array_type: Literal["FixedOpenRack", "FixedRoofMounted", "OneAxis", "OneAxisBacktracking", "TwoAxis"],
        pvwatts_version: Literal["5"] | None = ...,
        system_losses: float | None = 0.14,
        array_geometry_type: Literal["", "Surface", "TiltAzimuth"] | None = "TiltAzimuth",
        tilt_angle: float | None = 20,
        azimuth_angle: float | None = 180,
        surface_name: str | None = ...,
        ground_coverage_ratio: float | None = 0.4,
    ) -> None: ...

class MatrixTwoDimension:
    def __call__(
        self, name: str, /, *, number_of_rows: int, number_of_columns: int, values: list[Any] = ...
    ) -> None: ...

class AnyTableLookup:
    def __call__(
        self,
        name: str,
        /,
        *,
        independent_variable_list_name: str,
        normalization_method: Literal["", "AutomaticWithDivisor", "DivisorOnly", "None"] | None = "None",
        normalization_divisor: float | None = 1,
        minimum_output: float | None = ...,
        maximum_output: float | None = ...,
        output_unit_type: Literal["", "Capacity", "Dimensionless", "Power", "Pressure", "Temperature"]
        | None = "Dimensionless",
        external_file_name: str | None = ...,
        external_file_column_number: int | None = ...,
        external_file_starting_row_number: int | None = ...,
        values: list[Any] = ...,
    ) -> None: ...

class AnyEnvironmentalImpactFactors:
    def __call__(
        self,
        /,
        *,
        district_cooling_cop: float | None = 3,
        total_carbon_equivalent_emission_factor_from_n2o: float | None = 80.7272,
        total_carbon_equivalent_emission_factor_from_ch4: float | None = 6.2727,
        total_carbon_equivalent_emission_factor_from_co2: float | None = 0.2727,
    ) -> None: ...

class EnvironmentalImpactFactors:
    def __call__(
        self,
        /,
        *,
        district_heating_water_efficiency: float | None = 0.3,
        district_cooling_cop: float | None = 3,
        district_heating_steam_conversion_efficiency: float | None = 0.25,
        total_carbon_equivalent_emission_factor_from_n2o: float | None = 80.7272,
        total_carbon_equivalent_emission_factor_from_ch4: float | None = 6.2727,
        total_carbon_equivalent_emission_factor_from_co2: float | None = 0.2727,
    ) -> None: ...
