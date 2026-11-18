"""Creation signatures of generated classes (stub only).

DO NOT EDIT — regenerate with:
    python -m idfkit.codegen.generate_stubs
"""

from __future__ import annotations

from typing import Literal

from typing_extensions import Never

from .. import _generated_types as _g

class ShadowCalculation:
    def __call__(
        self,
        /,
        *,
        shading_calculation_method: Literal["", "Imported", "PixelCounting", "PolygonClipping", "Scheduled"]
        | None = "PolygonClipping",
        shading_calculation_update_frequency_method: Literal["", "Periodic", "Timestep"] | None = "Periodic",
        shading_calculation_update_frequency: int | None = 20,
        maximum_figures_in_shadow_overlap_calculations: int | None = 15000,
        polygon_clipping_algorithm: Literal[
            "", "ConvexWeilerAtherton", "SlaterBarskyandSutherlandHodgman", "SutherlandHodgman"
        ]
        | None = "SutherlandHodgman",
        pixel_counting_resolution: int | None = 512,
        sky_diffuse_modeling_algorithm: Literal["", "DetailedSkyDiffuseModeling", "SimpleSkyDiffuseModeling"]
        | None = "SimpleSkyDiffuseModeling",
        output_external_shading_calculation_results: Literal["", "No", "Yes"] | None = "No",
        disable_self_shading_within_shading_zone_groups: Literal["", "No", "Yes"] | None = "No",
        disable_self_shading_from_shading_zone_groups_to_other_zones: Literal["", "No", "Yes"] | None = "No",
        shading_zone_groups: list[_g.ShadowCalculationShadingZoneGroupsItem] = ...,
    ) -> None: ...

class Timestep:
    def __call__(self, /, *, number_of_timesteps_per_hour: int | None = 6) -> None: ...

class MaterialRoofVegetation:
    def __call__(
        self,
        name: str,
        /,
        *,
        height_of_plants: float | None = 0.2,
        leaf_area_index: float | None = 1,
        leaf_reflectivity: float | None = 0.22,
        leaf_emissivity: float | None = 0.95,
        minimum_stomatal_resistance: float | None = 180,
        soil_layer_name: str | None = "Green Roof Soil",
        roughness: Literal["", "MediumRough", "MediumSmooth", "Rough", "Smooth", "VeryRough", "VerySmooth"]
        | None = "MediumRough",
        thickness: float | None = 0.1,
        conductivity_of_dry_soil: float | None = 0.35,
        density_of_dry_soil: float | None = 1100,
        specific_heat_of_dry_soil: float | None = 1200,
        thermal_absorptance: float | None = 0.9,
        solar_absorptance: float | None = 0.7,
        visible_absorptance: float | None = 0.75,
        saturation_volumetric_moisture_content_of_the_soil_layer: float | None = 0.3,
        residual_volumetric_moisture_content_of_the_soil_layer: float | None = 0.01,
        initial_volumetric_moisture_content_of_the_soil_layer: float | None = 0.1,
        moisture_diffusion_calculation_method: Literal["", "Advanced", "Simple"] | None = "Advanced",
    ) -> None: ...

class MaterialPropertyVariableThermalConductivity:
    def __call__(
        self, name: str, /, *, values: list[_g.MaterialPropertyVariableThermalConductivityValuesItem] = ...
    ) -> None: ...

class AnyCeilingInterzone:
    def __call__(
        self,
        name: str,
        /,
        *,
        construction_name: str,
        zone_name: str,
        outside_boundary_condition_object: str,
        azimuth_angle: float | None = ...,
        tilt_angle: float | None = 0,
        starting_x_coordinate: float | None = ...,
        starting_y_coordinate: float | None = ...,
        starting_z_coordinate: float | None = ...,
        length: float | None = ...,
        width: float | None = ...,
    ) -> None: ...

class AnyWindowPropertyFrameAndDivider:
    def __call__(
        self,
        name: str,
        /,
        *,
        frame_width: float | None = 0,
        frame_outside_projection: float | None = 0,
        frame_inside_projection: float | None = 0,
        frame_conductance: float | None = ...,
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
    ) -> None: ...

class AirflowNetworkMultiZoneComponentDetailedOpening:
    def __call__(
        self,
        name: str,
        /,
        *,
        air_mass_flow_coefficient_when_opening_is_closed: float,
        number_of_sets_of_opening_factor_data: int,
        opening_factor_2: float,
        air_mass_flow_exponent_when_opening_is_closed: float | None = 0.65,
        type_of_rectangular_large_vertical_opening_lvo_: Literal["", "HorizontallyPivoted", "NonPivoted"]
        | None = "NonPivoted",
        extra_crack_length_or_height_of_pivoting_axis: float | None = 0,
        opening_factor_1: float | None = 0,
        discharge_coefficient_for_opening_factor_1: float | None = 0.001,
        width_factor_for_opening_factor_1: float | None = 0,
        height_factor_for_opening_factor_1: float | None = 0,
        start_height_factor_for_opening_factor_1: float | None = 0,
        discharge_coefficient_for_opening_factor_2: float | None = 1,
        width_factor_for_opening_factor_2: float | None = 1,
        height_factor_for_opening_factor_2: float | None = 1,
        start_height_factor_for_opening_factor_2: float | None = 0,
        opening_factor_3: float | None = ...,
        discharge_coefficient_for_opening_factor_3: float | None = 0,
        width_factor_for_opening_factor_3: float | None = 0,
        height_factor_for_opening_factor_3: float | None = 0,
        start_height_factor_for_opening_factor_3: float | None = 0,
        opening_factor_4: float | None = ...,
        discharge_coefficient_for_opening_factor_4: float | None = 0,
        width_factor_for_opening_factor_4: float | None = 0,
        height_factor_for_opening_factor_4: float | None = 0,
        start_height_factor_for_opening_factor_4: float | None = 0,
        type_of_rectangular_large_vertical_opening_lvo: Literal["", "HorizontallyPivoted", "NonPivoted"] | None = ...,
    ) -> None: ...

class DuctLossConduction:
    def __call__(
        self,
        name: str,
        /,
        *,
        airloophvac_name: str,
        airflownetwork_distribution_linkage_name: str,
        environment_type: Literal["", "Schedule", "Zone"] | None = "Zone",
        ambient_zone_name: str | None = ...,
        ambient_temperature_schedule_name: str | None = ...,
        ambient_humidity_ratio_schedule_name: str | None = ...,
    ) -> None: ...

class HVACTemplateZoneVAV:
    def __call__(
        self,
        /,
        *,
        zone_name: str,
        template_vav_system_name: str,
        template_thermostat_name: str | None = ...,
        supply_air_maximum_flow_rate: float | Literal["", "Autosize"] | None = "Autosize",
        zone_heating_sizing_factor: float | None = ...,
        zone_cooling_sizing_factor: float | None = ...,
        zone_minimum_air_flow_input_method: Literal["", "Constant", "FixedFlowRate", "Scheduled"] | None = "Constant",
        constant_minimum_air_flow_fraction: float | None = 0.2,
        fixed_minimum_air_flow_rate: float | None = ...,
        minimum_air_flow_fraction_schedule_name: str | None = ...,
        outdoor_air_method: Literal[
            "", "DetailedSpecification", "Flow/Area", "Flow/Person", "Flow/Zone", "Maximum", "Sum"
        ]
        | None = "Flow/Person",
        outdoor_air_flow_rate_per_person: float | None = 0.00944,
        outdoor_air_flow_rate_per_zone_floor_area: float | None = 0,
        outdoor_air_flow_rate_per_zone: float | None = 0,
        reheat_coil_type: Literal["", "Electric", "Gas", "HotWater", "None"] | None = "None",
        reheat_coil_availability_schedule_name: str | None = ...,
        damper_heating_action: Literal["", "Normal", "Reverse"] | None = "Reverse",
        maximum_flow_per_zone_floor_area_during_reheat: float | Literal["Autocalculate"] | None = ...,
        maximum_flow_fraction_during_reheat: float | Literal["Autocalculate"] | None = ...,
        maximum_reheat_air_temperature: float | None = ...,
        design_specification_outdoor_air_object_name_for_control: str | None = ...,
        supply_plenum_name: str | None = ...,
        return_plenum_name: str | None = ...,
        baseboard_heating_type: Literal["", "Electric", "HotWater", "None"] | None = "None",
        baseboard_heating_availability_schedule_name: str | None = ...,
        baseboard_heating_capacity: float | Literal["", "Autosize"] | None = "Autosize",
        zone_cooling_design_supply_air_temperature_input_method: Literal[
            "", "SupplyAirTemperature", "SystemSupplyAirTemperature", "TemperatureDifference"
        ]
        | None = "SystemSupplyAirTemperature",
        zone_cooling_design_supply_air_temperature: float | None = 12.8,
        zone_cooling_design_supply_air_temperature_difference: float | None = 11.11,
        zone_heating_design_supply_air_temperature_input_method: Literal[
            "", "SupplyAirTemperature", "TemperatureDifference"
        ]
        | None = "SupplyAirTemperature",
        zone_heating_design_supply_air_temperature: float | None = 50,
        zone_heating_design_supply_air_temperature_difference: float | None = 30,
        design_specification_outdoor_air_object_name_for_sizing: str | None = ...,
        design_specification_zone_air_distribution_object_name: str | None = ...,
    ) -> None: ...

class DesignSpecificationOutdoorAir:
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
            "ProportionalControlBasedOnOccupancySchedule",
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

class ZoneControlThermostatStagedDualSetpoint:
    def __call__(
        self,
        name: str,
        /,
        *,
        zone_or_zonelist_name: str,
        number_of_heating_stages: int,
        stage_1_heating_temperature_offset: float,
        number_of_cooling_stages: int,
        stage_1_cooling_temperature_offset: float,
        heating_temperature_setpoint_schedule_name: str | None = ...,
        heating_throttling_temperature_range: float | None = 1.1,
        stage_2_heating_temperature_offset: float | None = ...,
        stage_3_heating_temperature_offset: float | None = ...,
        stage_4_heating_temperature_offset: float | None = ...,
        cooling_temperature_setpoint_base_schedule_name: str | None = ...,
        cooling_throttling_temperature_range: float | None = 1.1,
        stage_2_cooling_temperature_offset: float | None = ...,
        stage_3_cooling_temperature_offset: float | None = ...,
        stage_4_cooling_temperature_offset: float | None = ...,
    ) -> None: ...

class ZoneHVACIdealLoadsAirSystem:
    def __call__(
        self,
        name: str,
        /,
        *,
        zone_supply_air_node_name: str,
        availability_schedule_name: str | None = ...,
        zone_exhaust_air_node_name: str | None = ...,
        system_inlet_air_node_name: str | None = ...,
        maximum_heating_supply_air_temperature: float | None = 50,
        minimum_cooling_supply_air_temperature: float | None = 13,
        maximum_heating_supply_air_humidity_ratio: float | None = 0.0156,
        minimum_cooling_supply_air_humidity_ratio: float | None = 0.0077,
        heating_limit: Literal["", "LimitCapacity", "LimitFlowRate", "LimitFlowRateAndCapacity", "NoLimit"]
        | None = "NoLimit",
        maximum_heating_air_flow_rate: float | Literal["Autosize"] | None = ...,
        maximum_sensible_heating_capacity: float | Literal["Autosize"] | None = ...,
        cooling_limit: Literal["", "LimitCapacity", "LimitFlowRate", "LimitFlowRateAndCapacity", "NoLimit"]
        | None = "NoLimit",
        maximum_cooling_air_flow_rate: float | Literal["Autosize"] | None = ...,
        maximum_total_cooling_capacity: float | Literal["Autosize"] | None = ...,
        heating_availability_schedule_name: str | None = ...,
        cooling_availability_schedule_name: str | None = ...,
        dehumidification_control_type: Literal[
            "", "ConstantSensibleHeatRatio", "ConstantSupplyHumidityRatio", "Humidistat", "None"
        ]
        | None = "ConstantSensibleHeatRatio",
        cooling_sensible_heat_ratio: float | None = 0.7,
        humidification_control_type: Literal["", "ConstantSupplyHumidityRatio", "Humidistat", "None"] | None = "None",
        design_specification_outdoor_air_object_name: str | None = ...,
        outdoor_air_inlet_node_name: str | None = ...,
        demand_controlled_ventilation_type: Literal["", "CO2Setpoint", "None", "OccupancySchedule"] | None = "None",
        outdoor_air_economizer_type: Literal["", "DifferentialDryBulb", "DifferentialEnthalpy", "NoEconomizer"]
        | None = "NoEconomizer",
        heat_recovery_type: Literal["", "Enthalpy", "None", "Sensible"] | None = "None",
        sensible_heat_recovery_effectiveness: float | None = 0.7,
        latent_heat_recovery_effectiveness: float | None = 0.65,
        design_specification_zonehvac_sizing_object_name: str | None = ...,
        heating_fuel_efficiency_schedule_name: str | None = ...,
        heating_fuel_type: Literal[
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
            "OtherFuel1",
            "OtherFuel2",
            "Propane",
        ]
        | None = "DistrictHeatingWater",
        cooling_fuel_efficiency_schedule_name: str | None = ...,
        cooling_fuel_type: Literal[
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
            "OtherFuel1",
            "OtherFuel2",
            "Propane",
        ]
        | None = "DistrictCooling",
    ) -> None: ...

class ZoneHVACOutdoorAirUnit:
    def __call__(
        self,
        name: str,
        /,
        *,
        zone_name: str,
        outdoor_air_flow_rate: float | Literal["Autosize"],
        outdoor_air_schedule_name: str,
        supply_fan_name: str,
        outdoor_air_node_name: str,
        airoutlet_node_name: str,
        supply_fanoutlet_node_name: str,
        outdoor_air_unit_list_name: str,
        availability_schedule_name: str | None = ...,
        supply_fan_placement: Literal["", "BlowThrough", "DrawThrough"] | None = "DrawThrough",
        exhaust_fan_name: str | None = ...,
        exhaust_air_flow_rate: float | Literal["Autosize"] | None = ...,
        exhaust_air_schedule_name: str | None = ...,
        unit_control_type: Literal["", "NeutralControl", "TemperatureControl"] | None = "NeutralControl",
        high_air_control_temperature_schedule_name: str | None = ...,
        low_air_control_temperature_schedule_name: str | None = ...,
        airinlet_node_name: str | None = ...,
        availability_manager_list_name: str | None = ...,
    ) -> None: ...

class AnyZoneHVACHighTemperatureRadiant:
    def __call__(
        self,
        name: str,
        /,
        *,
        zone_name: str,
        fuel_type: Literal["Electricity", "NaturalGas"],
        heating_setpoint_temperature_schedule_name: str,
        availability_schedule_name: str | None = ...,
        heating_design_capacity_method: Literal[
            "", "CapacityPerFloorArea", "FractionOfAutosizedHeatingCapacity", "HeatingDesignCapacity"
        ]
        | None = "HeatingDesignCapacity",
        heating_design_capacity: float | Literal["", "Autosize"] | None = "Autosize",
        heating_design_capacity_per_floor_area: float | None = ...,
        fraction_of_autosized_heating_design_capacity: float | None = 1,
        combustion_efficiency: float | None = 0.9,
        fraction_of_input_converted_to_radiant_energy: float | None = 0.7,
        fraction_of_input_converted_to_latent_energy: float | None = 0,
        fraction_of_input_that_is_lost: float | None = 0,
        temperature_control_type: Literal[
            "",
            "MeanAirTemperature",
            "MeanAirTemperatureSetpoint",
            "MeanRadiantTemperature",
            "MeanRadiantTemperatureSetpoint",
            "OperativeTemperature",
            "OperativeTemperatureSetpoint",
        ]
        | None = "OperativeTemperature",
        heating_throttling_range: float | None = 2,
        fraction_of_radiant_energy_incident_on_people: float | None = ...,
        surface_fractions: list[_g.ZoneHVACHighTemperatureRadiantSurfaceFractionsItem] = ...,
    ) -> None: ...

class CoilHeatingFuel:
    def __call__(
        self,
        name: str,
        /,
        *,
        air_inlet_node_name: str,
        air_outlet_node_name: str,
        availability_schedule_name: str | None = ...,
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
        burner_efficiency: float | None = 0.8,
        nominal_capacity: float | Literal["Autosize"] | None = ...,
        temperature_setpoint_node_name: str | None = ...,
        on_cycle_parasitic_electric_load: float | None = ...,
        part_load_fraction_correlation_curve_name: str | None = ...,
        off_cycle_parasitic_fuel_load: float | None = ...,
    ) -> None: ...

class AnyCoilHeatingWaterToAirHeatPumpVariableSpeedEquationFit:
    def __call__(
        self,
        name: str,
        /,
        *,
        narrow_with_as_version_first: Never,
        water_to_refrigerant_hx_water_inlet_node_name: str,
        water_to_refrigerant_hx_water_outlet_node_name: str,
        indoor_air_inlet_node_name: str,
        indoor_air_outlet_node_name: str,
        energy_part_load_fraction_curve_name: str,
        speed_1_reference_unit_gross_rated_heating_capacity: float,
        speed_1_reference_unit_gross_rated_heating_cop: float,
        speed_1_reference_unit_rated_water_flow_rate: float,
        speed_1_heating_capacity_function_of_temperature_curve_name: str,
        speed_1_total_heating_capacity_function_of_air_flow_fraction_curve_name: str,
        speed_1_heating_capacity_function_of_water_flow_fraction_curve_name: str,
        speed_1_energy_input_ratio_function_of_temperature_curve_name: str,
        speed_1_energy_input_ratio_function_of_air_flow_fraction_curve_name: str,
        speed_1_energy_input_ratio_function_of_water_flow_fraction_curve_name: str,
        speed_1_reference_unit_waste_heat_fraction_of_input_power_at_rated_conditions: float,
        speed_1_waste_heat_function_of_temperature_curve_name: str,
        number_of_speeds: int | None = 2,
        nominal_speed_level: int | None = 2,
        rated_heating_capacity_at_selected_nominal_speed_level: float | Literal["", "Autosize"] | None = "Autosize",
        rated_air_flow_rate_at_selected_nominal_speed_level: float | Literal["", "Autosize"] | None = "Autosize",
        rated_water_flow_rate_at_selected_nominal_speed_level: float | Literal["", "Autosize"] | None = "Autosize",
        speed_2_reference_unit_gross_rated_heating_capacity: float | None = ...,
        speed_2_reference_unit_gross_rated_heating_cop: float | None = ...,
        speed_2_reference_unit_rated_air_flow_rate: float | None = ...,
        speed_2_reference_unit_rated_water_flow_rate: float | None = ...,
        speed_2_heating_capacity_function_of_temperature_curve_name: str | None = ...,
        speed_2_total_heating_capacity_function_of_air_flow_fraction_curve_name: str | None = ...,
        speed_2_heating_capacity_function_of_water_flow_fraction_curve_name: str | None = ...,
        speed_2_energy_input_ratio_function_of_temperature_curve_name: str | None = ...,
        speed_2_energy_input_ratio_function_of_air_flow_fraction_curve_name: str | None = ...,
        speed_2_energy_input_ratio_function_of_water_flow_fraction_curve_name: str | None = ...,
        speed_2_reference_unit_waste_heat_fraction_of_input_power_at_rated_conditions: float | None = ...,
        speed_2_waste_heat_function_of_temperature_curve_name: str | None = ...,
        speed_3_reference_unit_gross_rated_heating_capacity: float | None = ...,
        speed_3_reference_unit_gross_rated_heating_cop: float | None = ...,
        speed_3_reference_unit_rated_air_flow_rate: float | None = ...,
        speed_3_reference_unit_rated_water_flow_rate: float | None = ...,
        speed_3_heating_capacity_function_of_temperature_curve_name: str | None = ...,
        speed_3_total_heating_capacity_function_of_air_flow_fraction_curve_name: str | None = ...,
        speed_3_heating_capacity_function_of_water_flow_fraction_curve_name: str | None = ...,
        speed_3_energy_input_ratio_function_of_temperature_curve_name: str | None = ...,
        speed_3_energy_input_ratio_function_of_air_flow_fraction_curve_name: str | None = ...,
        speed_3_energy_input_ratio_function_of_water_flow_fraction_curve_name: str | None = ...,
        speed_3_reference_unit_waste_heat_fraction_of_input_power_at_rated_conditions: float | None = ...,
        speed_3_waste_heat_function_of_temperature_curve_name: str | None = ...,
        speed_4_reference_unit_gross_rated_heating_capacity: float | None = ...,
        speed_4_reference_unit_gross_rated_heating_cop: float | None = ...,
        speed_4_reference_unit_rated_air_flow_rate: float | None = ...,
        speed_4_reference_unit_rated_water_flow_rate: float | None = ...,
        speed_4_heating_capacity_function_of_temperature_curve_name: str | None = ...,
        speed_4_total_heating_capacity_function_of_air_flow_fraction_curve_name: str | None = ...,
        speed_4_heating_capacity_function_of_water_flow_fraction_curve_name: str | None = ...,
        speed_4_energy_input_ratio_function_of_temperature_curve_name: str | None = ...,
        speed_4_energy_input_ratio_function_of_air_flow_fraction_curve_name: str | None = ...,
        speed_4_energy_input_ratio_function_of_water_flow_fraction_curve_name: str | None = ...,
        speed_4_reference_unit_waste_heat_fraction_of_input_power_at_rated_conditions: float | None = ...,
        speed_4_waste_heat_function_of_temperature_curve_name: str | None = ...,
        speed_5_reference_unit_gross_rated_heating_capacity: float | None = ...,
        speed_5_reference_unit_gross_rated_heating_cop: float | None = ...,
        speed_5_reference_unit_rated_air_flow_rate: float | None = ...,
        speed_5_reference_unit_rated_water_flow_rate: float | None = ...,
        speed_5_heating_capacity_function_of_temperature_curve_name: str | None = ...,
        speed_5_total_heating_capacity_function_of_air_flow_fraction_curve_name: str | None = ...,
        speed_5_heating_capacity_function_of_water_flow_fraction_curve_name: str | None = ...,
        speed_5_energy_input_ratio_function_of_temperature_curve_name: str | None = ...,
        speed_5_energy_input_ratio_function_of_air_flow_fraction_curve_name: str | None = ...,
        speed_5_energy_input_ratio_function_of_water_flow_fraction_curve_name: str | None = ...,
        speed_5_reference_unit_waste_heat_fraction_of_input_power_at_rated_conditions: float | None = ...,
        speed_5_waste_heat_function_of_temperature_curve_name: str | None = ...,
        speed_6_reference_unit_gross_rated_heating_capacity: float | None = ...,
        speed_6_reference_unit_gross_rated_heating_cop: float | None = ...,
        speed_6_reference_unit_rated_air_flow_rate: float | None = ...,
        speed_6_reference_unit_rated_water_flow_rate: float | None = ...,
        speed_6_heating_capacity_function_of_temperature_curve_name: str | None = ...,
        speed_6_total_heating_capacity_function_of_air_flow_fraction_curve_name: str | None = ...,
        speed_6_heating_capacity_function_of_water_flow_fraction_curve_name: str | None = ...,
        speed_6_energy_input_ratio_function_of_temperature_curve_name: str | None = ...,
        speed_6_energy_input_ratio_function_of_air_flow_fraction_curve_name: str | None = ...,
        speed_6_energy_input_ratio_function_of_water_flow_fraction_curve_name: str | None = ...,
        speed_6_reference_unit_waste_heat_fraction_of_input_power_at_rated_conditions: float | None = ...,
        speed_6_waste_heat_function_of_temperature_curve_name: str | None = ...,
        speed_7_reference_unit_gross_rated_heating_capacity: float | None = ...,
        speed_7_reference_unit_gross_rated_heating_cop: float | None = ...,
        speed_7_reference_unit_rated_air_flow_rate: float | None = ...,
        speed_7_reference_unit_rated_water_flow_rate: float | None = ...,
        speed_7_heating_capacity_function_of_temperature_curve_name: str | None = ...,
        speed_7_total_heating_capacity_function_of_air_flow_fraction_curve_name: str | None = ...,
        speed_7_heating_capacity_function_of_water_flow_fraction_curve_name: str | None = ...,
        speed_7_energy_input_ratio_function_of_temperature_curve_name: str | None = ...,
        speed_7_energy_input_ratio_function_of_air_flow_fraction_curve_name: str | None = ...,
        speed_7_energy_input_ratio_function_of_water_flow_fraction_curve_name: str | None = ...,
        speed_7_reference_unit_waste_heat_fraction_of_input_power_at_rated_conditions: float | None = ...,
        speed_7_waste_heat_function_of_temperature_curve_name: str | None = ...,
        speed_8_reference_unit_gross_rated_heating_capacity: float | None = ...,
        speed_8_reference_unit_gross_rated_heating_cop: float | None = ...,
        speed_8_reference_unit_rated_air_flow_rate: float | None = ...,
        speed_8_reference_unit_rated_water_flow_rate: float | None = ...,
        speed_8_heating_capacity_function_of_temperature_curve_name: str | None = ...,
        speed_8_total_heating_capacity_function_of_air_flow_fraction_curve_name: str | None = ...,
        speed_8_heating_capacity_function_of_water_flow_fraction_curve_name: str | None = ...,
        speed_8_energy_input_ratio_function_of_temperature_curve_name: str | None = ...,
        speed_8_energy_input_ratio_function_of_air_flow_fraction_curve_name: str | None = ...,
        speed_8_energy_input_ratio_function_of_water_flow_fraction_curve_name: str | None = ...,
        speed_8_reference_unit_waste_heat_fraction_of_input_power_at_rated_conditions: float | None = ...,
        speed_8_waste_heat_function_of_temperature_curve_name: str | None = ...,
        speed_9_reference_unit_gross_rated_heating_capacity: float | None = ...,
        speed_9_reference_unit_gross_rated_heating_cop: float | None = ...,
        speed_9_reference_unit_rated_air_flow_rate: float | None = ...,
        speed_9_reference_unit_rated_water_flow_rate: float | None = ...,
        speed_9_heating_capacity_function_of_temperature_curve_name: str | None = ...,
        speed_9_total_heating_capacity_function_of_air_flow_fraction_curve_name: str | None = ...,
        speed_9_heating_capacity_function_of_water_flow_fraction_curve_name: str | None = ...,
        speed_9_energy_input_ratio_function_of_temperature_curve_name: str | None = ...,
        speed_9_energy_input_ratio_function_of_air_flow_fraction_curve_name: str | None = ...,
        speed_9_energy_input_ratio_function_of_water_flow_fraction_curve_name: str | None = ...,
        speed_9_reference_unit_waste_heat_fraction_of_input_power_at_rated_conditions: float | None = ...,
        speed_9_waste_heat_function_of_temperature_curve_name: str | None = ...,
        speed_10_reference_unit_gross_rated_heating_capacity: float | None = ...,
        speed_10_reference_unit_gross_rated_heating_cop: float | None = ...,
        speed_10_reference_unit_rated_air_flow_rate: float | None = ...,
        speed_10_reference_unit_rated_water_flow_rate: float | None = ...,
        speed_10_heating_capacity_function_of_temperature_curve_name: str | None = ...,
        speed_10_total_heating_capacity_function_of_air_flow_fraction_curve_name: str | None = ...,
        speed_10_heating_capacity_function_of_water_flow_fraction_curve_name: str | None = ...,
        speed_10_energy_input_ratio_function_of_temperature_curve_name: str | None = ...,
        speed_10_energy_input_ratio_function_of_air_flow_fraction_curve_name: str | None = ...,
        speed_10_energy_input_ratio_function_of_water_flow_fraction_curve_name: str | None = ...,
        speed_10_reference_unit_waste_heat_fraction_of_input_power_at_rated_conditions: float | None = ...,
        speed_10_waste_heat_function_of_temperature_curve_name: str | None = ...,
    ) -> None: ...

class AnyCoilWaterHeatingAirToWaterHeatPumpPumped:
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
    ) -> None: ...

class AirLoopHVAC:
    def __call__(
        self,
        name: str,
        /,
        *,
        branch_list_name: str,
        supply_side_inlet_node_name: str,
        demand_side_inlet_node_names: str,
        supply_side_outlet_node_names: str,
        controller_list_name: str | None = ...,
        availability_manager_list_name: str | None = ...,
        design_supply_air_flow_rate: float | Literal["", "Autosize"] | None = 0,
        connector_list_name: str | None = ...,
        demand_side_outlet_node_name: str | None = ...,
        design_return_air_flow_fraction_of_supply_air_flow: float | None = 1,
    ) -> None: ...

class TemperingValve:
    def __call__(
        self,
        name: str,
        /,
        *,
        inlet_node_name: str,
        outlet_node_name: str,
        stream_2_source_node_name: str,
        temperature_setpoint_node_name: str,
        pump_outlet_node_name: str,
    ) -> None: ...

class SolarCollectorPerformancePhotovoltaicThermalSimple:
    def __call__(
        self,
        name: str = "",
        /,
        *,
        fraction_of_surface_area_with_active_thermal_collector: float,
        thermal_conversion_efficiency_input_mode_type: Literal["Fixed", "Scheduled"] | None = ...,
        value_for_thermal_conversion_efficiency_if_fixed: float | None = ...,
        thermal_conversion_efficiency_schedule_name: str | None = ...,
        front_surface_emittance: float | None = 0.84,
    ) -> None: ...

class AnyChillerElectric:
    def __call__(
        self,
        name: str,
        /,
        *,
        nominal_capacity: float | Literal["Autosize"],
        nominal_cop: float,
        chilled_water_inlet_node_name: str,
        chilled_water_outlet_node_name: str,
        temperature_rise_coefficient: float,
        condenser_type: Literal["", "AirCooled", "EvaporativelyCooled", "WaterCooled"] | None = "AirCooled",
        condenser_inlet_node_name: str | None = ...,
        condenser_outlet_node_name: str | None = ...,
        minimum_part_load_ratio: float | None = ...,
        maximum_part_load_ratio: float | None = ...,
        optimum_part_load_ratio: float | None = ...,
        design_condenser_inlet_temperature: float | None = ...,
        design_chilled_water_outlet_temperature: float | None = ...,
        design_chilled_water_flow_rate: float | Literal["Autosize"] | None = ...,
        design_condenser_fluid_flow_rate: float | Literal["Autosize"] | None = ...,
        coefficient_1_of_capacity_ratio_curve: float | None = ...,
        coefficient_2_of_capacity_ratio_curve: float | None = ...,
        coefficient_3_of_capacity_ratio_curve: float | None = ...,
        coefficient_1_of_power_ratio_curve: float | None = ...,
        coefficient_2_of_power_ratio_curve: float | None = ...,
        coefficient_3_of_power_ratio_curve: float | None = ...,
        coefficient_1_of_full_load_ratio_curve: float | None = ...,
        coefficient_2_of_full_load_ratio_curve: float | None = ...,
        coefficient_3_of_full_load_ratio_curve: float | None = ...,
        chilled_water_outlet_temperature_lower_limit: float | None = ...,
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

class PlantComponentTemperatureSource:
    def __call__(
        self,
        name: str,
        /,
        *,
        inlet_node: str,
        outlet_node: str,
        design_volume_flow_rate: float | Literal["Autosize"],
        temperature_specification_type: Literal["Constant", "Scheduled"] | None = ...,
        source_temperature: float | None = ...,
        source_temperature_schedule_name: str | None = ...,
    ) -> None: ...

class EnergyManagementSystemInternalVariable:
    def __call__(
        self, name: str, /, *, internal_data_type: str, internal_data_index_key_name: str | None = ...
    ) -> None: ...

class RefrigerationSecondarySystem:
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

class DemandManagerExteriorLights:
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
        lights: list[_g.DemandManagerExteriorLightsLightsItem] = ...,
    ) -> None: ...

class GeneratorFuelCellElectricalStorage:
    def __call__(
        self,
        name: str,
        /,
        *,
        choice_of_model: Literal["SimpleEfficiencyWithConstraints"] | None = ...,
        nominal_charging_energetic_efficiency: float | None = ...,
        nominal_discharging_energetic_efficiency: float | None = ...,
        simple_maximum_capacity: float | None = ...,
        simple_maximum_power_draw: float | None = ...,
        simple_maximum_power_store: float | None = ...,
        initial_charge_state: float | None = ...,
    ) -> None: ...

class WaterUseWell:
    def __call__(
        self,
        name: str,
        /,
        *,
        storage_tank_name: str,
        pump_depth: float | None = ...,
        pump_rated_flow_rate: float | None = ...,
        pump_rated_head: float | None = ...,
        pump_rated_power_consumption: float | None = ...,
        pump_efficiency: float | None = ...,
        well_recovery_rate: float | None = ...,
        nominal_well_storage_volume: float | None = ...,
        water_table_depth_mode: Literal["Constant", "Scheduled"] | None = ...,
        water_table_depth: float | None = ...,
        water_table_depth_schedule_name: str | None = ...,
    ) -> None: ...

class FaultModelFoulingChiller:
    def __call__(
        self,
        name: str,
        /,
        *,
        chiller_object_type: Literal[
            "Chiller:CombustionTurbine",
            "Chiller:ConstantCOP",
            "Chiller:Electric",
            "Chiller:Electric:EIR",
            "Chiller:Electric:ReformulatedEIR",
            "Chiller:EngineDriven",
        ],
        chiller_object_name: str,
        availability_schedule_name: str | None = ...,
        severity_schedule_name: str | None = ...,
        fouling_factor: float | None = 1,
    ) -> None: ...

class MeterCustom:
    def __call__(
        self,
        name: str,
        /,
        *,
        resource_type: Literal[
            "Coal",
            "Diesel",
            "DistrictCooling",
            "DistrictHeatingSteam",
            "DistrictHeatingWater",
            "Electricity",
            "FuelOilNo1",
            "FuelOilNo2",
            "Gasoline",
            "Generic",
            "NaturalGas",
            "OtherFuel1",
            "OtherFuel2",
            "Propane",
            "Water",
        ]
        | None = ...,
        variable_details: list[_g.MeterCustomVariableDetailsItem] = ...,
    ) -> None: ...
