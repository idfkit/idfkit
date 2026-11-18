"""Creation signatures of generated classes (stub only).

DO NOT EDIT — regenerate with:
    python -m idfkit.codegen.generate_stubs
"""

from __future__ import annotations

from collections.abc import Sequence
from typing import Literal

from .. import _generated_types as _g

class SiteGroundTemperatureFCfactorMethod:
    def __call__(
        self,
        this_type_has_no_name_field: _g._PassFieldsAsKeywords = ...,
        /,
        *,
        january_ground_temperature: float | None = 13,
        february_ground_temperature: float | None = 13,
        march_ground_temperature: float | None = 13,
        april_ground_temperature: float | None = 13,
        may_ground_temperature: float | None = 13,
        june_ground_temperature: float | None = 13,
        july_ground_temperature: float | None = 13,
        august_ground_temperature: float | None = 13,
        september_ground_temperature: float | None = 13,
        october_ground_temperature: float | None = 13,
        november_ground_temperature: float | None = 13,
        december_ground_temperature: float | None = 13,
        validate: bool = True,
    ) -> None:
        """Create a new ``Site:GroundTemperature:FCfactorMethod`` and add it to the document.

        These temperatures are specifically for underground walls and ground floors defined with the C-factor and F-factor methods, and should be close to the monthly average outdoor air temperature delayed by 3 months for the location.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-location-climate-weather-file-access/#sitegroundtemperaturefcfactormethod
        """

class WindowMaterialScreenEquivalentLayer:
    def __call__(
        self,
        name: str,
        /,
        *,
        screen_beam_diffuse_solar_transmittance: float,
        screen_beam_diffuse_solar_reflectance: float,
        screen_beam_beam_visible_transmittance: float,
        screen_beam_diffuse_visible_transmittance: float,
        screen_beam_diffuse_visible_reflectance: float,
        screen_beam_beam_solar_transmittance: float | Literal["Autocalculate"] | None = "Autocalculate",
        screen_infrared_transmittance: float | None = 0.02,
        screen_infrared_emissivity: float | None = 0.93,
        screen_wire_spacing: float | None = 0.025,
        screen_wire_diameter: float | None = 0.005,
        validate: bool = True,
    ) -> None:
        """Create a new ``WindowMaterial:Screen:EquivalentLayer`` and add it to the document.

        Equivalent layer window screen physical properties. Can only be located on the exterior side of a window construction.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-surface-construction-elements/#windowmaterialscreenequivalentlayer
        """

class ShadingZoneDetailed:
    def __call__(
        self,
        name: str,
        /,
        *,
        base_surface_name: str,
        transmittance_schedule_name: str | None = ...,
        number_of_vertices: float | Literal["Autocalculate"] | None = "Autocalculate",
        vertices: Sequence[_g.ShadingZoneDetailedVerticesItem | _g.ShadingZoneDetailedVerticesGroup] = ...,
        validate: bool = True,
    ) -> None:
        """Create a new ``Shading:Zone:Detailed`` and add it to the document.

        used For fins, overhangs, elements that shade the building, are attached to the building but are not part of the heat transfer calculations

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/energyplus-economics/cost-estimating/#shadingzonedetailed
        """

class GroundHeatTransferBasementManualGrid:
    def __call__(
        self,
        this_type_has_no_name_field: _g._PassFieldsAsKeywords = ...,
        /,
        *,
        nx_number_of_cells_in_the_x_direction_20_: float,
        ny_number_of_cells_in_the_y_direction_20_: float,
        nzag_number_of_cells_in_the_z_direction_above_grade_4_always_: float,
        nzbg_number_of_cells_in_z_direction_below_grade_10_35_: float,
        ibase_x_direction_cell_indicator_of_slab_edge_5_20_: float,
        jbase_y_direction_cell_indicator_of_slab_edge_5_20_: float,
        kbase_z_direction_cell_indicator_of_the_top_of_the_floor_slab_5_20_: float,
        validate: bool = True,
    ) -> None:
        """Create a new ``GroundHeatTransfer:Basement:ManualGrid`` and add it to the document.

        Manual Grid only necessary using manual gridding (not recommended)

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-detailed-ground-heat-transfer/#groundheattransferbasementmanualgrid
        """

class RoomAirNode:
    def __call__(
        self,
        name: str = "",
        /,
        *,
        node_type: Literal["Ceiling", "Control", "Floor", "Inlet", "MundtRoom", "Return"],
        zone_name: str,
        height_of_nodal_control_volume_center: float,
        surface_1_name: str | None = ...,
        surface_2_name: str | None = ...,
        surface_3_name: str | None = ...,
        surface_4_name: str | None = ...,
        surface_5_name: str | None = ...,
        surface_6_name: str | None = ...,
        surface_7_name: str | None = ...,
        surface_8_name: str | None = ...,
        surface_9_name: str | None = ...,
        surface_10_name: str | None = ...,
        surface_11_name: str | None = ...,
        surface_12_name: str | None = ...,
        surface_13_name: str | None = ...,
        surface_14_name: str | None = ...,
        surface_15_name: str | None = ...,
        surface_16_name: str | None = ...,
        surface_17_name: str | None = ...,
        surface_18_name: str | None = ...,
        surface_19_name: str | None = ...,
        surface_20_name: str | None = ...,
        surface_21_name: str | None = ...,
        validate: bool = True,
    ) -> None:
        """Create a new ``RoomAir:Node`` and add it to the document.

        Define an air node for some types of nodal room air models

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-room-air-models/#roomairnode
        """

class ZoneAirBalanceOutdoorAir:
    def __call__(
        self,
        name: str,
        /,
        *,
        zone_name: str,
        air_balance_method: Literal["None", "Quadrature"] | None = "Quadrature",
        induced_outdoor_air_due_to_unbalanced_duct_leakage: float | None = 0,
        induced_outdoor_air_schedule_name: str | None = ...,
        validate: bool = True,
    ) -> None:
        """Create a new ``ZoneAirBalance:OutdoorAir`` and add it to the document.

        Provide a combined zone outdoor air flow by including interactions between mechanical ventilation, infiltration and duct leakage. This object will combine outdoor flows from all ZoneInfiltration and ZoneVentilation objects in the same zone. Balanced flows will be summed, while unbalanced flows will be added in quadrature.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-airflow/#zoneairbalanceoutdoorair
        """

class AnyAirflowNetworkMultiZoneComponentDetailedOpening:
    def __call__(
        self,
        name: str,
        /,
        *,
        air_mass_flow_coefficient_when_opening_is_closed: float,
        number_of_sets_of_opening_factor_data: int,
        opening_factor_2: float,
        air_mass_flow_exponent_when_opening_is_closed: float | None = 0.65,
        type_of_rectangular_large_vertical_opening_lvo_: Literal["HorizontallyPivoted", "NonPivoted"]
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
        validate: bool = True,
    ) -> None:
        """Create a new ``AirflowNetwork:MultiZone:Component:DetailedOpening`` and add it to the document.

        This object specifies the properties of airflow through windows and doors (window, door and glass door heat transfer subsurfaces) when they are closed or open.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-airflow-network/#airflownetworkmultizonecomponentdetailedopening
        """

class AirflowNetworkDistributionComponentDuct:
    def __call__(
        self,
        name: str,
        /,
        *,
        duct_length: float,
        hydraulic_diameter: float,
        cross_section_area: float,
        surface_roughness: float | None = 0.0009,
        coefficient_for_local_dynamic_loss_due_to_fitting: float | None = 0,
        heat_transmittance_coefficient_u_factor_for_duct_wall_construction: float | None = 0.943,
        overall_moisture_transmittance_coefficient_from_air_to_air: float | None = 0.001,
        outside_convection_coefficient: float | None = ...,
        inside_convection_coefficient: float | None = ...,
        validate: bool = True,
    ) -> None:
        """Create a new ``AirflowNetwork:Distribution:Component:Duct`` and add it to the document.

        This object defines the relationship between pressure and air flow through the duct.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-airflow-network/#airflownetworkdistributioncomponentduct
        """

class HVACTemplateZoneVAVHeatAndCool:
    def __call__(
        self,
        this_type_has_no_name_field: _g._PassFieldsAsKeywords = ...,
        /,
        *,
        zone_name: str,
        template_vav_system_name: str,
        template_thermostat_name: str | None = ...,
        supply_air_maximum_flow_rate: float | Literal["Autosize"] | None = "Autosize",
        zone_heating_sizing_factor: float | None = ...,
        zone_cooling_sizing_factor: float | None = ...,
        constant_minimum_air_flow_fraction: float | None = 0.2,
        outdoor_air_method: Literal["DetailedSpecification", "Flow/Area", "Flow/Person", "Flow/Zone", "Maximum", "Sum"]
        | None = "Flow/Person",
        outdoor_air_flow_rate_per_person: float | None = 0.00944,
        outdoor_air_flow_rate_per_zone_floor_area: float | None = 0,
        outdoor_air_flow_rate_per_zone: float | None = 0,
        design_specification_outdoor_air_object_name_for_sizing: str | None = ...,
        design_specification_zone_air_distribution_object_name: str | None = ...,
        reheat_coil_type: Literal["Electric", "Gas", "HotWater", "None"] | None = "None",
        reheat_coil_availability_schedule_name: str | None = ...,
        maximum_reheat_air_temperature: float | None = ...,
        supply_plenum_name: str | None = ...,
        return_plenum_name: str | None = ...,
        baseboard_heating_type: Literal["Electric", "HotWater", "None"] | None = "None",
        baseboard_heating_availability_schedule_name: str | None = ...,
        baseboard_heating_capacity: float | Literal["Autosize"] | None = "Autosize",
        zone_cooling_design_supply_air_temperature_input_method: Literal[
            "SupplyAirTemperature", "SystemSupplyAirTemperature", "TemperatureDifference"
        ]
        | None = "SystemSupplyAirTemperature",
        zone_cooling_design_supply_air_temperature: float | None = 12.8,
        zone_cooling_design_supply_air_temperature_difference: float | None = 11.11,
        zone_heating_design_supply_air_temperature_input_method: Literal[
            "SupplyAirTemperature", "TemperatureDifference"
        ]
        | None = "SupplyAirTemperature",
        zone_heating_design_supply_air_temperature: float | None = 50,
        zone_heating_design_supply_air_temperature_difference: float | None = 30,
        validate: bool = True,
    ) -> None:
        """Create a new ``HVACTemplate:Zone:VAV:HeatAndCool`` and add it to the document.

        VAV system with VAV for both heating and cooling and optional reheat coil. For heating, this unit increases airflow first, then activates reheat coil.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/hvac-template-objects/group-hvac-templates/#hvactemplatezonevavheatandcool
        """

class SizingSystem:
    def __call__(
        self,
        this_type_has_no_name_field: _g._PassFieldsAsKeywords = ...,
        /,
        *,
        airloop_name: str,
        preheat_design_temperature: float,
        preheat_design_humidity_ratio: float,
        precool_design_temperature: float,
        precool_design_humidity_ratio: float,
        central_cooling_design_supply_air_temperature: float,
        central_heating_design_supply_air_temperature: float,
        type_of_load_to_size_on: Literal["Latent", "Sensible", "Total", "VentilationRequirement"] | None = "Sensible",
        design_outdoor_air_flow_rate: float | Literal["Autosize"] | None = "Autosize",
        central_heating_maximum_system_air_flow_ratio: float | Literal["Autosize"] | None = "Autosize",
        type_of_zone_sum_to_use: Literal["Coincident", "NonCoincident"] | None = "NonCoincident",
        central_cooling_design_supply_air_humidity_ratio: float | None = 0.008,
        central_heating_design_supply_air_humidity_ratio: float | None = 0.008,
        cooling_supply_air_flow_rate_method: Literal[
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
        system_outdoor_air_method: Literal[
            "Standard62.1SimplifiedProcedure", "Standard62.1VentilationRateProcedure", "ZoneSum"
        ]
        | None = "ZoneSum",
        zone_maximum_outdoor_air_fraction: float | None = 1,
        cooling_design_capacity_method: Literal[
            "CapacityPerFloorArea", "CoolingDesignCapacity", "FractionOfAutosizedCoolingCapacity", "None"
        ]
        | None = "CoolingDesignCapacity",
        cooling_design_capacity: float | Literal["Autosize"] | None = "Autosize",
        cooling_design_capacity_per_floor_area: float | None = ...,
        fraction_of_autosized_cooling_design_capacity: float | None = ...,
        heating_design_capacity_method: Literal[
            "CapacityPerFloorArea", "FractionOfAutosizedHeatingCapacity", "HeatingDesignCapacity", "None"
        ]
        | None = "HeatingDesignCapacity",
        heating_design_capacity: float | Literal["Autosize"] | None = "Autosize",
        heating_design_capacity_per_floor_area: float | None = ...,
        fraction_of_autosized_heating_design_capacity: float | None = ...,
        central_cooling_capacity_control_method: Literal["Bypass", "OnOff", "VAV", "VT"] | None = "OnOff",
        occupant_diversity: float | Literal["Autosize"] | None = "Autosize",
        heating_coil_sizing_method: Literal["CoolingCapacity", "GreaterOfHeatingOrCooling", "HeatingCapacity", "None"]
        | None = "None",
        maximum_heating_capacity_to_cooling_capacity_sizing_ratio: float | None = 1,
        validate: bool = True,
    ) -> None:
        """Create a new ``Sizing:System`` and add it to the document.

        Specifies the input needed to perform sizing calculations for a central forced air system. System design air flow, heating capacity, and cooling capacity will be calculated using this input data.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-design-objects/#sizingsystem
        """

class AnyCoilCoolingDXMultiSpeed:
    def __call__(
        self,
        name: str,
        /,
        *,
        air_inlet_node_name: str,
        air_outlet_node_name: str,
        fuel_type: Literal["Diesel", "Electricity", "Gasoline", "NaturalGas", "OtherFuel1", "OtherFuel2", "Propane"],
        number_of_speeds: int,
        speed_1_gross_rated_total_cooling_capacity: float | Literal["Autosize"],
        speed_1_gross_rated_sensible_heat_ratio: float | Literal["Autosize"],
        speed_1_rated_air_flow_rate: float | Literal["Autosize"],
        speed_1_total_cooling_capacity_function_of_temperature_curve_name: str,
        speed_1_total_cooling_capacity_function_of_flow_fraction_curve_name: str,
        speed_1_energy_input_ratio_function_of_temperature_curve_name: str,
        speed_1_energy_input_ratio_function_of_flow_fraction_curve_name: str,
        speed_1_part_load_fraction_correlation_curve_name: str,
        speed_2_gross_rated_total_cooling_capacity: float | Literal["Autosize"],
        speed_2_gross_rated_sensible_heat_ratio: float | Literal["Autosize"],
        speed_2_rated_air_flow_rate: float | Literal["Autosize"],
        speed_2_total_cooling_capacity_function_of_temperature_curve_name: str,
        speed_2_total_cooling_capacity_function_of_flow_fraction_curve_name: str,
        speed_2_energy_input_ratio_function_of_temperature_curve_name: str,
        speed_2_energy_input_ratio_function_of_flow_fraction_curve_name: str,
        speed_2_part_load_fraction_correlation_curve_name: str,
        availability_schedule_name: str | None = ...,
        condenser_air_inlet_node_name: str | None = ...,
        condenser_type: Literal["AirCooled", "EvaporativelyCooled"] | None = "AirCooled",
        minimum_outdoor_dry_bulb_temperature_for_compressor_operation: float | None = -25,
        supply_water_storage_tank_name: str | None = ...,
        condensate_collection_water_storage_tank_name: str | None = ...,
        apply_part_load_fraction_to_speeds_greater_than_1: Literal["No", "Yes"] | None = "No",
        apply_latent_degradation_to_speeds_greater_than_1: Literal["No", "Yes"] | None = "No",
        crankcase_heater_capacity: float | None = 0,
        maximum_outdoor_dry_bulb_temperature_for_crankcase_heater_operation: float | None = 10,
        basin_heater_capacity: float | None = 0,
        basin_heater_setpoint_temperature: float | None = 2,
        basin_heater_operating_schedule_name: str | None = ...,
        speed_1_gross_rated_cooling_cop: float | None = 3,
        speed_1_nominal_time_for_condensate_removal_to_begin: float | None = 0,
        speed_1_ratio_of_initial_moisture_evaporation_rate_and_steady_state_latent_capacity: float | None = 0,
        speed_1_maximum_cycling_rate: float | None = 0,
        speed_1_latent_capacity_time_constant: float | None = 0,
        speed_1_rated_waste_heat_fraction_of_power_input: float | None = 0.2,
        speed_1_waste_heat_function_of_temperature_curve_name: str | None = ...,
        speed_1_evaporative_condenser_effectiveness: float | None = 0.9,
        speed_1_evaporative_condenser_air_flow_rate: float | Literal["Autosize"] | None = ...,
        speed_1_rated_evaporative_condenser_pump_power_consumption: float | Literal["Autosize"] | None = ...,
        speed_2_gross_rated_cooling_cop: float | None = 3,
        speed_2_nominal_time_for_condensate_removal_to_begin: float | None = 0,
        speed_2_ratio_of_initial_moisture_evaporation_rate_and_steady_state_latent_capacity: float | None = 0,
        speed_2_maximum_cycling_rate: float | None = 0,
        speed_2_latent_capacity_time_constant: float | None = 0,
        speed_2_rated_waste_heat_fraction_of_power_input: float | None = 0.2,
        speed_2_waste_heat_function_of_temperature_curve_name: str | None = ...,
        speed_2_evaporative_condenser_effectiveness: float | None = 0.9,
        speed_2_evaporative_condenser_air_flow_rate: float | Literal["Autosize"] | None = ...,
        speed_2_rated_evaporative_condenser_pump_power_consumption: float | Literal["Autosize"] | None = ...,
        speed_3_gross_rated_total_cooling_capacity: float | Literal["Autosize"] | None = ...,
        speed_3_gross_rated_sensible_heat_ratio: float | Literal["Autosize"] | None = ...,
        speed_3_gross_rated_cooling_cop: float | None = 3,
        speed_3_rated_air_flow_rate: float | Literal["Autosize"] | None = ...,
        speed_3_total_cooling_capacity_function_of_temperature_curve_name: str | None = ...,
        speed_3_total_cooling_capacity_function_of_flow_fraction_curve_name: str | None = ...,
        speed_3_energy_input_ratio_function_of_temperature_curve_name: str | None = ...,
        speed_3_energy_input_ratio_function_of_flow_fraction_curve_name: str | None = ...,
        speed_3_part_load_fraction_correlation_curve_name: str | None = ...,
        speed_3_nominal_time_for_condensate_removal_to_begin: float | None = 0,
        speed_3_ratio_of_initial_moisture_evaporation_rate_and_steady_state_latent_capacity: float | None = 0,
        speed_3_maximum_cycling_rate: float | None = 0,
        speed_3_latent_capacity_time_constant: float | None = 0,
        speed_3_rated_waste_heat_fraction_of_power_input: float | None = 0.2,
        speed_3_waste_heat_function_of_temperature_curve_name: str | None = ...,
        speed_3_evaporative_condenser_effectiveness: float | None = 0.9,
        speed_3_evaporative_condenser_air_flow_rate: float | Literal["Autosize"] | None = ...,
        speed_3_rated_evaporative_condenser_pump_power_consumption: float | Literal["Autosize"] | None = ...,
        speed_4_gross_rated_total_cooling_capacity: float | Literal["Autosize"] | None = ...,
        speed_4_gross_rated_sensible_heat_ratio: float | Literal["Autosize"] | None = ...,
        speed_4_gross_rated_cooling_cop: float | None = 3,
        speed_4_rated_air_flow_rate: float | Literal["Autosize"] | None = ...,
        speed_4_total_cooling_capacity_function_of_temperature_curve_name: str | None = ...,
        speed_4_total_cooling_capacity_function_of_flow_fraction_curve_name: str | None = ...,
        speed_4_energy_input_ratio_function_of_temperature_curve_name: str | None = ...,
        speed_4_energy_input_ratio_function_of_flow_fraction_curve_name: str | None = ...,
        speed_4_part_load_fraction_correlation_curve_name: str | None = ...,
        speed_4_nominal_time_for_condensate_removal_to_begin: float | None = 0,
        speed_4_ratio_of_initial_moisture_evaporation_rate_and_steady_state_latent_capacity: float | None = 0,
        speed_4_maximum_cycling_rate: float | None = 0,
        speed_4_latent_capacity_time_constant: float | None = 0,
        speed_4_rated_waste_heat_fraction_of_power_input: float | None = 0.2,
        speed_4_waste_heat_function_of_temperature_curve_name: str | None = ...,
        speed_4_evaporative_condenser_effectiveness: float | None = 0.9,
        speed_4_evaporative_condenser_air_flow_rate: float | Literal["Autosize"] | None = ...,
        speed_4_rated_evaporative_condenser_pump_power_consumption: float | Literal["Autosize"] | None = ...,
        zone_name_for_condenser_placement: str | None = ...,
        validate: bool = True,
    ) -> None:
        """Create a new ``Coil:Cooling:DX:MultiSpeed`` and add it to the document.

        Direct expansion (DX) cooling coil and condensing unit (includes electric or engine-driven compressor and condenser fan), multi-speed (or variable-speed). Optional moisture evaporation from wet coil when compressor cycles off with continuous fan operation. Requires two to four sets of performance data and will interpolate between speeds. Modeled as a single coil (multi-speed compressor or multiple compressors with row split or intertwined coil).

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-heating-and-cooling-coils/#coilcoolingdxmultispeed
        """

class AirLoopHVACDedicatedOutdoorAirSystem:
    def __call__(
        self,
        name: str,
        /,
        *,
        airloophvac_mixer_name: str,
        airloophvac_splitter_name: str,
        preheat_design_temperature: float,
        preheat_design_humidity_ratio: float,
        precool_design_temperature: float,
        precool_design_humidity_ratio: float,
        number_of_airloophvac: int,
        airloophvac_outdoorairsystem_name: str | None = ...,
        availability_schedule_name: str | None = ...,
        airloophvacs: Sequence[
            _g.AirLoopHVACDedicatedOutdoorAirSystemAirloophvacsItem
            | _g.AirLoopHVACDedicatedOutdoorAirSystemAirloophvacsGroup
        ] = ...,
        validate: bool = True,
    ) -> None:
        """Create a new ``AirLoopHVAC:DedicatedOutdoorAirSystem`` and add it to the document.

        Defines a central forced air system to provide dedicated outdoor air to multiple AirLoopHVACs.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-air-path/#airloophvacdedicatedoutdoorairsystem
        """

class HeatPumpAirToWaterFuelFiredCooling:
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
        companion_heating_heat_pump_name: str | None = ...,
        fuel_type: Literal[
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
        nominal_cooling_capacity: float | Literal["Autosize"] | None = ...,
        nominal_cop: float | None = 1,
        design_flow_rate: float | Literal["Autosize"] | None = ...,
        design_supply_temperature: float | None = 7,
        design_temperature_lift: float | Literal["Autosize"] | None = 11.1,
        sizing_factor: float | None = 1,
        flow_mode: Literal["ConstantFlow", "LeavingSetpointModulated", "NotModulated"] | None = "NotModulated",
        outdoor_air_temperature_curve_input_variable: Literal["DryBulb", "WetBulb"] | None = "DryBulb",
        water_temperature_curve_input_variable: Literal["EnteringEvaporator", "LeavingEvaporator"]
        | None = "EnteringEvaporator",
        minimum_part_load_ratio: float | None = 0.1,
        maximum_part_load_ratio: float | None = 1,
        cycling_ratio_factor_curve_name: str | None = ...,
        nominal_auxiliary_electric_power: float | None = ...,
        auxiliary_electric_energy_input_ratio_function_of_temperature_curve_name: str | None = ...,
        auxiliary_electric_energy_input_ratio_function_of_plr_curve_name: str | None = ...,
        standby_electric_power: float | None = 0,
        minimum_unloading_ratio: float | None = 0.25,
        validate: bool = True,
    ) -> None:
        """Create a new ``HeatPump:AirToWater:FuelFired:Cooling`` and add it to the document.

        The object defines a fuel-fired absorption heat pump based on equation-fit models.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-plant-heating-and-cooling-equipment/#heatpumpairtowaterfuelfiredcooling
        """
