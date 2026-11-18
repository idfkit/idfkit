"""Creation signatures of generated classes (stub only).

DO NOT EDIT — regenerate with:
    python -m idfkit.codegen.generate_stubs
"""

from __future__ import annotations

from collections.abc import Sequence
from typing import Literal

from .. import _generated_types as _g

class ShadowCalculation:
    def __call__(
        self,
        this_type_has_no_name_field: _g._PassFieldsAsKeywords = ...,
        /,
        *,
        shading_calculation_method: Literal["Imported", "PixelCounting", "PolygonClipping", "Scheduled"]
        | None = "PolygonClipping",
        shading_calculation_update_frequency_method: Literal["Periodic", "Timestep"] | None = "Periodic",
        shading_calculation_update_frequency: int | None = 20,
        maximum_figures_in_shadow_overlap_calculations: int | None = 15000,
        polygon_clipping_algorithm: Literal[
            "ConvexWeilerAtherton", "SlaterBarskyandSutherlandHodgman", "SutherlandHodgman"
        ]
        | None = "SutherlandHodgman",
        pixel_counting_resolution: int | None = 512,
        sky_diffuse_modeling_algorithm: Literal["DetailedSkyDiffuseModeling", "SimpleSkyDiffuseModeling"]
        | None = "SimpleSkyDiffuseModeling",
        output_external_shading_calculation_results: Literal["No", "Yes"] | None = "No",
        disable_self_shading_within_shading_zone_groups: Literal["No", "Yes"] | None = "No",
        disable_self_shading_from_shading_zone_groups_to_other_zones: Literal["No", "Yes"] | None = "No",
        shading_zone_groups: Sequence[
            _g.ShadowCalculationShadingZoneGroupsItem | _g.ShadowCalculationShadingZoneGroupsGroup
        ] = ...,
        validate: bool = True,
    ) -> None:
        """Create a new ``ShadowCalculation`` and add it to the document.

        This object is used to control details of the solar, shading, and daylighting models

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-simulation-parameters/#shadowcalculation
        """

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
        roughness: Literal["MediumRough", "MediumSmooth", "Rough", "Smooth", "VeryRough", "VerySmooth"]
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
        moisture_diffusion_calculation_method: Literal["Advanced", "Simple"] | None = "Advanced",
        validate: bool = True,
    ) -> None:
        """Create a new ``Material:RoofVegetation`` and add it to the document.

        EcoRoof model, plant layer plus soil layer Implemented by Portland State University (Sailor et al., January, 2007) only one material must be referenced per simulation though the same EcoRoof material could be used in multiple constructions. New moisture redistribution scheme (2010) requires higher number of timesteps per hour (minimum 12 recommended).

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-surface-construction-elements/#materialroofvegetation
        """

class MaterialPropertyVariableThermalConductivity:
    def __call__(
        self,
        name: str,
        /,
        *,
        values: Sequence[
            _g.MaterialPropertyVariableThermalConductivityValuesItem
            | _g.MaterialPropertyVariableThermalConductivityValuesGroup
        ] = ...,
        validate: bool = True,
    ) -> None:
        """Create a new ``MaterialProperty:VariableThermalConductivity`` and add it to the document.

        Additional properties for temperature dependent thermal conductivity using piecewise linear temperature-conductivity function. Name is followed by up to 100 sets of temperature-conductivity pairs. HeatBalanceAlgorithm = CondFD(ConductionFiniteDifference) solution algorithm only. Has no effect with other HeatBalanceAlgorithm solution algorithms

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-surface-construction-elements/#materialpropertyvariablethermalconductivity
        """

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

class HVACTemplateZoneVAV:
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
        zone_minimum_air_flow_input_method: Literal["Constant", "FixedFlowRate", "Scheduled"] | None = "Constant",
        constant_minimum_air_flow_fraction: float | None = 0.2,
        fixed_minimum_air_flow_rate: float | None = ...,
        minimum_air_flow_fraction_schedule_name: str | None = ...,
        outdoor_air_method: Literal["DetailedSpecification", "Flow/Area", "Flow/Person", "Flow/Zone", "Maximum", "Sum"]
        | None = "Flow/Person",
        outdoor_air_flow_rate_per_person: float | None = 0.00944,
        outdoor_air_flow_rate_per_zone_floor_area: float | None = 0,
        outdoor_air_flow_rate_per_zone: float | None = 0,
        reheat_coil_type: Literal["Electric", "Gas", "HotWater", "None"] | None = "None",
        reheat_coil_availability_schedule_name: str | None = ...,
        damper_heating_action: Literal["Normal", "Reverse"] | None = "Reverse",
        maximum_flow_per_zone_floor_area_during_reheat: float | Literal["Autocalculate"] | None = ...,
        maximum_flow_fraction_during_reheat: float | Literal["Autocalculate"] | None = ...,
        maximum_reheat_air_temperature: float | None = ...,
        design_specification_outdoor_air_object_name_for_control: str | None = ...,
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
        design_specification_outdoor_air_object_name_for_sizing: str | None = ...,
        design_specification_zone_air_distribution_object_name: str | None = ...,
        validate: bool = True,
    ) -> None:
        """Create a new ``HVACTemplate:Zone:VAV`` and add it to the document.

        Zone terminal unit, variable volume, reheat optional. For heating, this unit activates reheat coil first, then increases airflow (if reverse action specified).

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/hvac-template-objects/group-hvac-templates/#hvactemplatezonevav
        """

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
        validate: bool = True,
    ) -> None:
        """Create a new ``Coil:Heating:Fuel`` and add it to the document.

        Gas or other fuel heating coil. If the coil is located directly in an air loop branch or outdoor air equipment list, then it is controlled on leaving air temperature and the Temperature Setpoint Node Name must be specified. If the coil is contained within another component such as an air terminal unit, zone HVAC equipment, or unitary system, then the coil is controlled by the parent component and the setpoint node name is not entered.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/energyplus-economics/cost-estimating/#coilheatingfuel
        """

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
        validate: bool = True,
    ) -> None:
        """Create a new ``SolarCollectorPerformance:PhotovoltaicThermal:Simple`` and add it to the document.

        Thermal performance parameters for a hybrid photovoltaic-thermal (PVT) solar collector.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-solar-collectors/#solarcollectorperformancephotovoltaicthermalsimple
        """

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
        pump_drive_type: Literal["Constant", "Variable"] | None = "Constant",
        variable_speed_pump_cubic_curve_name: str | None = ...,
        pump_motor_heat_to_fluid: float | None = 0.85,
        sum_ua_distribution_piping: float | None = 0,
        distribution_piping_zone_name: str | None = ...,
        sum_ua_receiver_separator_shell: float | None = 0,
        receiver_separator_zone_name: str | None = ...,
        evaporator_refrigerant_inventory: float | None = 0,
        end_use_subcategory: str | None = "General",
        validate: bool = True,
    ) -> None:
        """Create a new ``Refrigeration:SecondarySystem`` and add it to the document.

        Works in conjunction with refrigerated cases and walkins to simulate the performance of a secondary loop supermarket refrigeration system. Heat from the refrigeration loads served by the secondary loop is absorbed by a primary refrigeration system (Refrigeration:System). The SecondarySystem object simulates a heat exchanger that is an evaporator, or refrigeration load, on the primary refrigeration system.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-refrigeration/#refrigerationsecondarysystem
        """
