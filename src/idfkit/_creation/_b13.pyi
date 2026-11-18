"""Creation signatures of generated classes (stub only).

DO NOT EDIT — regenerate with:
    python -m idfkit.codegen.generate_stubs
"""

from __future__ import annotations

from typing import Any, Literal

class AnyPerformancePrecisionTradeoffs:
    def __call__(self, /, *, use_coil_direct_solutions: Literal["", "No", "Yes"] | None = "No") -> None: ...

class SiteGroundTemperatureUndisturbedKusudaAchenbach:
    def __call__(
        self,
        name: str,
        /,
        *,
        soil_thermal_conductivity: float,
        soil_density: float,
        soil_specific_heat: float,
        average_soil_surface_temperature: float | None = ...,
        average_amplitude_of_surface_temperature: float | None = ...,
        phase_shift_of_minimum_surface_temperature: float | None = ...,
    ) -> None: ...

class ScheduleDayList:
    def __call__(
        self,
        name: str,
        /,
        *,
        schedule_type_limits_name: str | None = ...,
        interpolate_to_timestep: Literal["", "Average", "Linear", "No"] | None = "No",
        minutes_per_item: int | None = ...,
        extensions: list[Any] = ...,
    ) -> None: ...

class MaterialNoMass:
    def __call__(
        self,
        name: str,
        /,
        *,
        roughness: Literal["MediumRough", "MediumSmooth", "Rough", "Smooth", "VeryRough", "VerySmooth"],
        thermal_resistance: float,
        thermal_absorptance: float | None = 0.9,
        solar_absorptance: float | None = 0.7,
        visible_absorptance: float | None = 0.7,
        thermal_absorptance_inside_face: float | None = ...,
        solar_absorptance_inside_face: float | None = ...,
        visible_absorptance_inside_face: float | None = ...,
    ) -> None: ...

class MaterialPropertyPhaseChangeHysteresis:
    def __call__(
        self,
        name: str,
        /,
        *,
        latent_heat_during_the_entire_phase_change_process: float,
        liquid_state_thermal_conductivity: float,
        liquid_state_density: float,
        liquid_state_specific_heat: float,
        high_temperature_difference_of_melting_curve: float,
        peak_melting_temperature: float,
        low_temperature_difference_of_melting_curve: float,
        solid_state_thermal_conductivity: float,
        solid_state_density: float,
        solid_state_specific_heat: float,
        high_temperature_difference_of_freezing_curve: float,
        peak_freezing_temperature: float,
        low_temperature_difference_of_freezing_curve: float,
    ) -> None: ...

class AnyWallExterior:
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

class Roof:
    def __call__(
        self,
        name: str,
        /,
        *,
        construction_name: str,
        zone_name: str,
        space_name: str | None = ...,
        azimuth_angle: float | None = ...,
        tilt_angle: float | None = 0,
        starting_x_coordinate: float | None = ...,
        starting_y_coordinate: float | None = ...,
        starting_z_coordinate: float | None = ...,
        length: float | None = ...,
        width: float | None = ...,
    ) -> None: ...

class AnyCeilingAdiabatic:
    def __call__(
        self,
        name: str,
        /,
        *,
        construction_name: str,
        zone_name: str,
        azimuth_angle: float | None = ...,
        tilt_angle: float | None = 0,
        starting_x_coordinate: float | None = ...,
        starting_y_coordinate: float | None = ...,
        starting_z_coordinate: float | None = ...,
        length: float | None = ...,
        width: float | None = ...,
    ) -> None: ...

class FenestrationSurfaceDetailed:
    def __call__(
        self,
        name: str,
        /,
        *,
        surface_type: Literal[
            "Door",
            "FixedWindow",
            "GlassDoor",
            "OperableWindow",
            "OverheadDoor",
            "Skylight",
            "TubularDaylightDiffuser",
            "TubularDaylightDome",
            "Window",
        ],
        building_surface_name: str,
        vertex_1_x_coordinate: float,
        vertex_1_y_coordinate: float,
        vertex_1_z_coordinate: float,
        vertex_2_x_coordinate: float,
        vertex_2_y_coordinate: float,
        vertex_2_z_coordinate: float,
        vertex_3_x_coordinate: float,
        vertex_3_y_coordinate: float,
        vertex_3_z_coordinate: float,
        construction_name: str | None = ...,
        outside_boundary_condition_object: str | None = ...,
        view_factor_to_ground: float | Literal["", "Autocalculate"] | None = "Autocalculate",
        frame_and_divider_name: str | None = ...,
        multiplier: float | None = 1,
        number_of_vertices: float | Literal["", "Autocalculate"] | None = "Autocalculate",
        vertex_4_x_coordinate: float | None = ...,
        vertex_4_y_coordinate: float | None = ...,
        vertex_4_z_coordinate: float | None = ...,
    ) -> None: ...

class DoorInterzone:
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

class SurfacePropertyExposedFoundationPerimeter:
    def __call__(
        self,
        /,
        *,
        surface_name: str,
        exposed_perimeter_calculation_method: Literal["BySegment", "ExposedPerimeterFraction", "TotalExposedPerimeter"],
        total_exposed_perimeter: float | None = ...,
        exposed_perimeter_fraction: float | None = 1,
        surfaces: list[Any] = ...,
    ) -> None: ...

class SurfaceConvectionAlgorithmInsideUserCurve:
    def __call__(
        self,
        name: str = "",
        /,
        *,
        reference_temperature_for_convection_heat_transfer: Literal[
            "AdjacentAirTemperature", "MeanAirTemperature", "SupplyAirTemperature"
        ]
        | None = ...,
        hc_function_of_temperature_difference_curve_name: str | None = ...,
        hc_function_of_temperature_difference_divided_by_height_curve_name: str | None = ...,
        hc_function_of_air_change_rate_curve_name: str | None = ...,
        hc_function_of_air_system_volume_flow_rate_divided_by_zone_perimeter_length_curve_name: str | None = ...,
    ) -> None: ...

class ZoneMRTCalculation:
    def __call__(self, /, *, zone_name: str, people_names: list[Any] = ...) -> None: ...

class DaylightingReferencePoint:
    def __call__(
        self,
        name: str,
        /,
        *,
        zone_or_space_name: str,
        x_coordinate_of_reference_point: float,
        y_coordinate_of_reference_point: float,
        z_coordinate_of_reference_point: float | None = 0.8,
    ) -> None: ...

class OutputDaylightFactors:
    def __call__(self, /, *, reporting_days: Literal["AllShadowCalculationDays", "SizingDays"]) -> None: ...

class AnyHVACTemplateZoneFanCoil:
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
    ) -> None: ...

class HVACTemplatePlantBoilerObjectReference:
    def __call__(
        self,
        name: str,
        /,
        *,
        boiler_name: str,
        boiler_object_type: Literal["", "Boiler:HotWater"] | None = "Boiler:HotWater",
        priority: float | None = ...,
        template_plant_loop_type: Literal["HotWater", "MixedWater"] | None = ...,
    ) -> None: ...

class ThermostatSetpointThermalComfortFangerSingleHeating:
    def __call__(self, name: str, /, *, fanger_thermal_comfort_schedule_name: str) -> None: ...

class ZoneHVACPackagedTerminalAirConditioner:
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
        supply_air_fan_object_type: Literal["Fan:ConstantVolume", "Fan:OnOff", "Fan:SystemModel"],
        supply_air_fan_name: str,
        heating_coil_object_type: Literal[
            "Coil:Heating:Electric", "Coil:Heating:Fuel", "Coil:Heating:Steam", "Coil:Heating:Water"
        ],
        heating_coil_name: str,
        cooling_coil_object_type: Literal[
            "Coil:Cooling:DX",
            "Coil:Cooling:DX:SingleSpeed",
            "Coil:Cooling:DX:VariableSpeed",
            "CoilSystem:Cooling:DX:HeatExchangerAssisted",
        ],
        cooling_coil_name: str,
        availability_schedule_name: str | None = ...,
        outdoor_air_mixer_object_type: Literal["OutdoorAir:Mixer"] | None = ...,
        outdoor_air_mixer_name: str | None = ...,
        no_load_supply_air_flow_rate: float | Literal["Autosize"] | None = ...,
        no_load_supply_air_flow_rate_control_set_to_low_speed: Literal["", "No", "Yes"] | None = "Yes",
        no_load_outdoor_air_flow_rate: float | Literal["Autosize"] | None = ...,
        fan_placement: Literal["", "BlowThrough", "DrawThrough"] | None = "DrawThrough",
        supply_air_fan_operating_mode_schedule_name: str | None = ...,
        availability_manager_list_name: str | None = ...,
        design_specification_zonehvac_sizing_object_name: str | None = ...,
        capacity_control_method: Literal["", "None", "SingleZoneVAV"] | None = "None",
        minimum_supply_air_temperature_in_cooling_mode: float | Literal["", "Autosize"] | None = "Autosize",
        maximum_supply_air_temperature_in_heating_mode: float | Literal["", "Autosize"] | None = "Autosize",
    ) -> None: ...

class ZoneHVACEquipmentConnections:
    def __call__(
        self,
        /,
        *,
        zone_name: str,
        zone_conditioning_equipment_list_name: str,
        zone_air_node_name: str,
        zone_air_inlet_node_or_nodelist_name: str | None = ...,
        zone_air_exhaust_node_or_nodelist_name: str | None = ...,
        zone_return_air_node_or_nodelist_name: str | None = ...,
        zone_return_air_node_1_flow_rate_fraction_schedule_name: str | None = ...,
        zone_return_air_node_1_flow_rate_basis_node_or_nodelist_name: str | None = ...,
    ) -> None: ...

class AnyCoilHeatingDXSingleSpeed:
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

class AnyGroundHeatExchangerHorizontalTrench:
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
        trench_length_in_pipe_axial_direction: float | None = 50,
        number_of_trenches: int | None = 1,
        horizontal_spacing_between_pipes: float | None = 1,
        pipe_inner_diameter: float | None = 0.016,
        pipe_outer_diameter: float | None = 0.026,
        burial_depth: float | None = 1.5,
        soil_thermal_conductivity: float | None = 1.08,
        soil_density: float | None = 962,
        soil_specific_heat: float | None = 2576,
        pipe_thermal_conductivity: float | None = 0.3895,
        pipe_density: float | None = 641,
        pipe_specific_heat: float | None = 2405,
        soil_moisture_content_percent: float | None = 30,
        soil_moisture_content_percent_at_saturation: float | None = 50,
        evapotranspiration_ground_cover_parameter: float | None = 0.4,
    ) -> None: ...

class PlantEquipmentOperationCoolingLoad:
    def __call__(
        self,
        name: str,
        /,
        *,
        load_range_1_lower_limit: float,
        load_range_1_upper_limit: float,
        range_1_equipment_list_name: str | None = ...,
        load_range_2_lower_limit: float | None = ...,
        load_range_2_upper_limit: float | None = ...,
        range_2_equipment_list_name: str | None = ...,
        load_range_3_lower_limit: float | None = ...,
        load_range_3_upper_limit: float | None = ...,
        range_3_equipment_list_name: str | None = ...,
        load_range_4_lower_limit: float | None = ...,
        load_range_4_upper_limit: float | None = ...,
        range_4_equipment_list_name: str | None = ...,
        load_range_5_lower_limit: float | None = ...,
        load_range_5_upper_limit: float | None = ...,
        range_5_equipment_list_name: str | None = ...,
        load_range_6_lower_limit: float | None = ...,
        load_range_6_upper_limit: float | None = ...,
        range_6_equipment_list_name: str | None = ...,
        load_range_7_lower_limit: float | None = ...,
        load_range_7_upper_limit: float | None = ...,
        range_7_equipment_list_name: str | None = ...,
        load_range_8_lower_limit: float | None = ...,
        load_range_8_upper_limit: float | None = ...,
        range_8_equipment_list_name: str | None = ...,
        load_range_9_lower_limit: float | None = ...,
        load_range_9_upper_limit: float | None = ...,
        range_9_equipment_list_name: str | None = ...,
        load_range_10_lower_limit: float | None = ...,
        load_range_10_upper_limit: float | None = ...,
        range_10_equipment_list_name: str | None = ...,
    ) -> None: ...

class ExternalInterfaceSchedule:
    def __call__(self, name: str, /, *, initial_value: float, schedule_type_limits_name: str | None = ...) -> None: ...

class SetpointManagerColdest:
    def __call__(
        self,
        name: str,
        /,
        *,
        hvac_air_loop_name: str,
        setpoint_node_or_nodelist_name: str,
        control_variable: Literal["", "Temperature"] | None = "Temperature",
        minimum_setpoint_temperature: float | None = 20,
        maximum_setpoint_temperature: float | None = 50,
        strategy: Literal["", "MinimumTemperature"] | None = "MinimumTemperature",
    ) -> None: ...

class RefrigerationCaseAndWalkInList:
    def __call__(self, name: str, /, *, cases_and_walkins: list[Any] = ...) -> None: ...

class AnyGeneratorInternalCombustionEngine:
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
        fuel_type: Literal["", "Diesel", "Gasoline", "NaturalGas", "OtherFuel1", "OtherFuel2"] | None = "Diesel",
        heat_recovery_maximum_temperature: float | None = 80,
    ) -> None: ...

class FaultModelTemperatureSensorOffsetCoilSupplyAir:
    def __call__(
        self,
        name: str,
        /,
        *,
        coil_object_type: Literal[
            "AirLoopHVAC:UnitarySystem",
            "Coil:Cooling:Water",
            "Coil:Cooling:Water:Detailedgeometry",
            "Coil:Heating:Desuperheater",
            "Coil:Heating:Electric",
            "Coil:Heating:Gas",
            "Coil:Heating:Steam",
            "Coil:Heating:Water",
            "CoilSystem:Cooling:DX",
            "CoilSystem:Heating:DX",
        ],
        coil_object_name: str,
        availability_schedule_name: str | None = ...,
        severity_schedule_name: str | None = ...,
        water_coil_controller_name: str | None = ...,
        reference_sensor_offset: float | None = 0,
    ) -> None: ...

class FaultModelFoulingBoiler:
    def __call__(
        self,
        name: str,
        /,
        *,
        boiler_object_type: Literal["Boiler:HotWater"],
        boiler_object_name: str,
        availability_schedule_name: str | None = ...,
        severity_schedule_name: str | None = ...,
        fouling_factor: float | None = 1,
    ) -> None: ...

class CurveCubicLinear:
    def __call__(
        self,
        name: str,
        /,
        *,
        coefficient1_constant: float,
        coefficient2_x: float,
        coefficient3_x_2: float,
        coefficient4_x_3: float,
        coefficient5_y: float,
        coefficient6_x_y: float,
        minimum_value_of_x: float,
        maximum_value_of_x: float,
        minimum_value_of_y: float,
        maximum_value_of_y: float,
        minimum_curve_output: float | None = ...,
        maximum_curve_output: float | None = ...,
        input_unit_type_for_x: Literal["", "Dimensionless", "Temperature"] | None = "Dimensionless",
        input_unit_type_for_y: Literal["", "Dimensionless", "Temperature"] | None = "Dimensionless",
        output_unit_type: Literal["", "Capacity", "Dimensionless", "Power", "Pressure", "Temperature"]
        | None = "Dimensionless",
    ) -> None: ...

class TableIndependentVariableList:
    def __call__(self, name: str, /, *, independent_variables: list[Any] = ...) -> None: ...

class ComponentCostReference:
    def __call__(
        self,
        /,
        *,
        reference_building_line_item_costs: float | None = ...,
        reference_building_miscellaneous_cost_per_conditioned_area: float | None = ...,
        reference_building_design_and_engineering_fees: float | None = ...,
        reference_building_contractor_fee: float | None = ...,
        reference_building_contingency: float | None = ...,
        reference_building_permits_bonding_and_insurance: float | None = ...,
        reference_building_commissioning_fee: float | None = ...,
        reference_building_regional_adjustment_factor: float | None = ...,
    ) -> None: ...

class LifeCycleCostParameters:
    def __call__(
        self,
        name: str,
        /,
        *,
        discounting_convention: Literal["", "BeginningOfYear", "EndOfYear", "MidYear"] | None = "EndOfYear",
        inflation_approach: Literal["", "ConstantDollar", "CurrentDollar"] | None = "ConstantDollar",
        real_discount_rate: float | None = ...,
        nominal_discount_rate: float | None = ...,
        inflation: float | None = ...,
        base_date_month: Literal[
            "",
            "April",
            "August",
            "December",
            "February",
            "January",
            "July",
            "June",
            "March",
            "May",
            "November",
            "October",
            "September",
        ]
        | None = "January",
        base_date_year: int | None = ...,
        service_date_month: Literal[
            "",
            "April",
            "August",
            "December",
            "February",
            "January",
            "July",
            "June",
            "March",
            "May",
            "November",
            "October",
            "September",
        ]
        | None = "January",
        service_date_year: int | None = ...,
        length_of_study_period_in_years: int | None = ...,
        tax_rate: float | None = ...,
        depreciation_method: Literal[
            "",
            "ModifiedAcceleratedCostRecoverySystem-10year",
            "ModifiedAcceleratedCostRecoverySystem-15year",
            "ModifiedAcceleratedCostRecoverySystem-20year",
            "ModifiedAcceleratedCostRecoverySystem-3year",
            "ModifiedAcceleratedCostRecoverySystem-5year",
            "ModifiedAcceleratedCostRecoverySystem-7year",
            "None",
            "StraightLine-27year",
            "StraightLine-31year",
            "StraightLine-39year",
            "StraightLine-40year",
        ]
        | None = "None",
    ) -> None: ...

class AnyOutputTableAnnual:
    def __call__(
        self,
        name: str,
        /,
        *,
        filter: str | None = ...,
        schedule_name: str | None = ...,
        variable_details: list[Any] = ...,
    ) -> None: ...
