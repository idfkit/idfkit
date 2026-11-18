"""Creation signatures of generated classes (stub only).

DO NOT EDIT — regenerate with:
    python -m idfkit.codegen.generate_stubs
"""

from __future__ import annotations

from typing import Any, Literal

from typing_extensions import Never

from .. import _generated_types as _g

class PerformancePrecisionTradeoffs:
    def __call__(
        self,
        /,
        *,
        use_coil_direct_solutions: Literal["", "No", "Yes"] | None = "No",
        zone_radiant_exchange_algorithm: Literal["", "CarrollMRT", "ScriptF"] | None = "ScriptF",
        override_mode: Literal[
            "", "Advanced", "Mode01", "Mode02", "Mode03", "Mode04", "Mode05", "Mode06", "Mode07", "Mode08", "Normal"
        ]
        | None = "Normal",
        maxzonetempdiff: float | None = 0.3,
        maxalloweddeltemp: float | None = 0.002,
        use_representative_surfaces_for_calculations: Literal["", "No", "Yes"] | None = "No",
    ) -> None:
        """Create a new ``PerformancePrecisionTradeoffs`` and add it to the document.

        This object enables users to choose certain options that speed up EnergyPlus simulation, but may lead to small decreases in accuracy of results.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-simulation-parameters/#performanceprecisiontradeoffs
        """

class SiteHeightVariation:
    def __call__(
        self,
        /,
        *,
        wind_speed_profile_exponent: float | None = 0.22,
        wind_speed_profile_boundary_layer_thickness: float | None = 370,
        air_temperature_gradient_coefficient: float | None = 0.0065,
    ) -> None:
        """Create a new ``Site:HeightVariation`` and add it to the document.

        This object is used if the user requires advanced control over height-dependent variations in wind speed and temperature. When this object is not present, the default model for temperature dependence on height is used, and the wind speed is modeled according to the Terrain field of the BUILDING object.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-location-climate-weather-file-access/#siteheightvariation
        """

class SiteGroundDomainBasement:
    def __call__(
        self,
        name: str,
        /,
        *,
        undisturbed_ground_temperature_model_type: Literal[
            "Site:GroundTemperature:Undisturbed:FiniteDifference",
            "Site:GroundTemperature:Undisturbed:KusudaAchenbach",
            "Site:GroundTemperature:Undisturbed:Xing",
        ],
        undisturbed_ground_temperature_model_name: str,
        basement_floor_boundary_condition_model_name: str,
        basement_wall_boundary_condition_model_name: str,
        ground_domain_depth: float | None = 10,
        aspect_ratio: float | None = 1,
        perimeter_offset: float | None = 5,
        soil_thermal_conductivity: float | None = 1.5,
        soil_density: float | None = 2800,
        soil_specific_heat: float | None = 850,
        soil_moisture_content_volume_fraction: float | None = 30,
        soil_moisture_content_volume_fraction_at_saturation: float | None = 50,
        evapotranspiration_ground_cover_parameter: float | None = 0.4,
        horizontal_insulation: Literal["", "No", "Yes"] | None = "No",
        horizontal_insulation_material_name: str | None = ...,
        horizontal_insulation_extents: Literal["", "Full", "Perimeter"] | None = "Full",
        perimeter_horizontal_insulation_width: float | None = ...,
        basement_wall_depth: float | None = ...,
        vertical_insulation: Literal["", "No", "Yes"] | None = "No",
        basement_wall_vertical_insulation_material_name: str | None = ...,
        vertical_insulation_depth: float | None = ...,
        simulation_timestep: Literal["", "Hourly", "Timestep"] | None = "Hourly",
        mesh_density_parameter: int | None = 4,
    ) -> None:
        """Create a new ``Site:GroundDomain:Basement`` and add it to the document.

        Ground-coupled basement model for simulating basements or other underground zones.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-location-climate-weather-file-access/#sitegrounddomainbasement
        """

class Material:
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
        thermal_absorptance_inside_face: float | None = ...,
        solar_absorptance_inside_face: float | None = ...,
        visible_absorptance_inside_face: float | None = ...,
    ) -> None:
        """Create a new ``Material`` and add it to the document.

        Regular materials described with full set of thermal properties

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-surface-construction-elements/#material
        """

class WindowMaterialShadeEquivalentLayer:
    def __call__(
        self,
        name: str,
        /,
        *,
        front_side_shade_beam_diffuse_solar_transmittance: float,
        back_side_shade_beam_diffuse_solar_transmittance: float,
        front_side_shade_beam_diffuse_solar_reflectance: float,
        back_side_shade_beam_diffuse_solar_reflectance: float,
        shade_beam_beam_solar_transmittance: float | None = 0,
        shade_beam_beam_visible_transmittance_at_normal_incidence: float | None = ...,
        shade_beam_diffuse_visible_transmittance_at_normal_incidence: float | None = ...,
        shade_beam_diffuse_visible_reflectance_at_normal_incidence: float | None = ...,
        shade_material_infrared_transmittance: float | None = 0.05,
        front_side_shade_material_infrared_emissivity: float | None = 0.91,
        back_side_shade_material_infrared_emissivity: float | None = 0.91,
    ) -> None:
        """Create a new ``WindowMaterial:Shade:EquivalentLayer`` and add it to the document.

        Specifies the properties of equivalent layer window shade material Shades are considered to be perfect diffusers (all transmitted and reflected radiation is hemispherically-diffuse) independent of angle of incidence. Shade represents roller blinds.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-surface-construction-elements/#windowmaterialshadeequivalentlayer
        """

class MaterialPropertyVariableAbsorptance:
    def __call__(
        self,
        name: str,
        /,
        *,
        reference_material_name: str,
        control_signal: Literal[
            "", "Scheduled", "SpaceHeatingCoolingMode", "SurfaceReceivedSolarRadiation", "SurfaceTemperature"
        ]
        | None = "SurfaceTemperature",
        thermal_absorptance_function_name: str | None = ...,
        thermal_absorptance_schedule_name: str | None = ...,
        solar_absorptance_function_name: str | None = ...,
        solar_absorptance_schedule_name: str | None = ...,
        control_signal_inside_face: Literal[
            "Scheduled", "SpaceHeatingCoolingMode", "SurfaceReceivedSolarRadiation", "SurfaceTemperature"
        ]
        | None = ...,
        thermal_absorptance_function_name_inside_face: str | None = ...,
        thermal_absorptance_schedule_name_inside_face: str | None = ...,
        solar_absorptance_function_name_inside_face: str | None = ...,
        solar_absorptance_schedule_name_inside_face: str | None = ...,
    ) -> None:
        """Create a new ``MaterialProperty:VariableAbsorptance`` and add it to the document.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-surface-construction-elements/#materialpropertyvariableabsorptance
        """

class ConstructionAirBoundary:
    def __call__(
        self,
        name: str,
        /,
        *,
        air_exchange_method: Literal["", "None", "SimpleMixing"] | None = "None",
        simple_mixing_air_changes_per_hour: float | None = 0.5,
        simple_mixing_schedule_name: str | None = ...,
    ) -> None:
        """Create a new ``Construction:AirBoundary`` and add it to the document.

        Indicates an open boundary between two zones. It may be used for base surfaces and fenestration surfaces. The two adjacent zones are grouped together for solar, daylighting and radiant exchange. When this construction type is used, the Outside Boundary Condition of the surface (or the base surface of a fenestration surface) must be either Surface or Zone. A base surface with Construction:AirBoundary cannot hold any fenestration surfaces.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-surface-construction-elements/#constructionairboundary
        """

class ConstructionComplexFenestrationState:
    def __call__(
        self,
        name: str,
        /,
        *,
        window_thermal_model: str,
        basis_matrix_name: str,
        solar_optical_complex_front_transmittance_matrix_name: str,
        solar_optical_complex_back_reflectance_matrix_name: str,
        visible_optical_complex_front_transmittance_matrix_name: str,
        visible_optical_complex_back_transmittance_matrix_name: str,
        outside_layer_name: str,
        outside_layer_directional_front_absorptance_matrix_name: str,
        outside_layer_directional_back_absorptance_matrix_name: str,
        basis_type: Literal["", "LBNLWINDOW", "UserDefined"] | None = "LBNLWINDOW",
        basis_symmetry_type: Literal["", "Axisymmetric", "None"] | None = "None",
        gap_1_name: str | None = ...,
        cfs_gap_1_directional_front_absorptance_matrix_name: str | None = ...,
        cfs_gap_1_directional_back_absorptance_matrix_name: str | None = ...,
        layer_2_name: str | None = ...,
        layer_2_directional_front_absorptance_matrix_name: str | None = ...,
        layer_2_directional_back_absorptance_matrix_name: str | None = ...,
        gap_2_name: str | None = ...,
        gap_2_directional_front_absorptance_matrix_name: str | None = ...,
        gap_2_directional_back_absorptance_matrix_name: str | None = ...,
        layer_3_name: str | None = ...,
        layer_3_directional_front_absorptance_matrix_name: str | None = ...,
        layer_3_directional_back_absorptance_matrix_name: str | None = ...,
        gap_3_name: str | None = ...,
        gap_3_directional_front_absorptance_matrix_name: str | None = ...,
        gap_3_directional_back_absorptance_matrix_name: str | None = ...,
        layer_4_name: str | None = ...,
        layer_4_directional_front_absorptance_matrix_name: str | None = ...,
        layer_4_directional_back_absorptance_matrix_name: str | None = ...,
        gap_4_name: str | None = ...,
        gap_4_directional_front_absorptance_matrix_name: str | None = ...,
        gap_4_directional_back_absorptance_matrix_name: str | None = ...,
        layer_5_name: str | None = ...,
        layer_5_directional_front_absorptance_matrix_name: str | None = ...,
        layer_5_directional_back_absorptance_matrix_name: str | None = ...,
    ) -> None:
        """Create a new ``Construction:ComplexFenestrationState`` and add it to the document.

        Describes one state for a complex glazing system These input objects are typically generated by using WINDOW software and export to IDF syntax

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-surface-construction-elements/#constructioncomplexfenestrationstate
        """

class AnyInternalMass:
    def __call__(
        self, name: str, /, *, narrow_with_as_version_first: Never, construction_name: str, surface_area: float
    ) -> None:
        """Create a new ``InternalMass`` and add it to the document.

        Used to describe internal zone surface area that does not need to be part of geometric representation. This should be the total surface area exposed to the zone air. If you use a ZoneList in the Zone or ZoneList name field then this definition applies to all the zones in the ZoneList. Likewise for SpaceList.

        No call suits every release: narrow the document with ``as_version`` first.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-thermal-zone-description-geometry/#internalmass
        """

class ZonePropertyLocalEnvironment:
    def __call__(self, name: str, /, *, zone_name: str | None = ..., outdoor_air_node_name: str | None = ...) -> None:
        """Create a new ``ZoneProperty:LocalEnvironment`` and add it to the document.

        This object defines the local environment properties of a zone object. A corresponding outdoor air node should be defined and linked to the zone object.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-advanced-surface-concepts/#zonepropertylocalenvironment
        """

class AnyRoomAirTemperaturePatternNondimensionalHeight:
    def __call__(
        self,
        name: str,
        /,
        *,
        control_integer_for_pattern_control_schedule_name: int,
        thermostat_offset: float | None = ...,
        return_air_offset: float | None = ...,
        exhaust_air_offset: float | None = ...,
        pairs: list[_g.RoomAirTemperaturePatternNondimensionalHeightPairsItem] = ...,
    ) -> None:
        """Create a new ``RoomAir:TemperaturePattern:NondimensionalHeight`` and add it to the document.

        Defines a distribution pattern for air temperatures relative to the current mean air temperature as a function of height. The height, referred to as Zeta, is nondimensional by normalizing with the zone ceiling height. Used in combination with RoomAir:TemperaturePattern:UserDefined.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-room-air-models/#roomairtemperaturepatternnondimensionalheight
        """

class RoomAirSettingsUnderFloorAirDistributionExterior:
    def __call__(
        self,
        /,
        *,
        zone_name: str,
        number_of_diffusers_per_zone: float | Literal["", "Autocalculate"] | None = "Autocalculate",
        power_per_plume: float | Literal["", "Autocalculate"] | None = "Autocalculate",
        design_effective_area_of_diffuser: float | Literal["", "Autocalculate"] | None = "Autocalculate",
        diffuser_slot_angle_from_vertical: float | Literal["", "Autocalculate"] | None = "Autocalculate",
        thermostat_height: float | None = 1.2,
        comfort_height: float | None = 1.1,
        temperature_difference_threshold_for_reporting: float | None = 0.4,
        floor_diffuser_type: Literal["", "Custom", "HorizontalSwirl", "LinearBarGrille", "Swirl", "VariableArea"]
        | None = "Swirl",
        transition_height: float | Literal["", "Autocalculate"] | None = 1.7,
        coefficient_a_in_formula_kc_a_gamma_b_c_d_gamma_e_gamma_2: float
        | Literal["", "Autocalculate"]
        | None = "Autocalculate",
        coefficient_b_in_formula_kc_a_gamma_b_c_d_gamma_e_gamma_2: float
        | Literal["", "Autocalculate"]
        | None = "Autocalculate",
        coefficient_c_in_formula_kc_a_gamma_b_c_d_gamma_e_gamma_2: float
        | Literal["", "Autocalculate"]
        | None = "Autocalculate",
        coefficient_d_in_formula_kc_a_gamma_b_c_d_gamma_e_gamma_2: float
        | Literal["", "Autocalculate"]
        | None = "Autocalculate",
        coefficient_e_in_formula_kc_a_gamma_b_c_d_gamma_e_gamma_2: float
        | Literal["", "Autocalculate"]
        | None = "Autocalculate",
    ) -> None:
        """Create a new ``RoomAirSettings:UnderFloorAirDistributionExterior`` and add it to the document.

        Applicable to exterior spaces that are served by an underfloor air distribution system. The dominant sources of heat gain should be from people, equipment, and other localized sources located in the occupied part of the room, as well as convective gain coming from a warm window. Used with RoomAirModelType = CrossVentilation.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-room-air-models/#roomairsettingsunderfloorairdistributionexterior
        """

class SteamEquipmentDefinition:
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
    ) -> None:
        """Create a new ``SteamEquipment:Definition`` and add it to the document.

        Defines the physical characteristics (design level and heat gain fractions) for steam equipment. Referenced by one or more SteamEquipment:Instance objects.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-internal-gains/#steamequipmentdefinition
        """

class ZoneContaminantSourceAndSinkCarbonDioxide:
    def __call__(
        self, name: str, /, *, zone_name: str, schedule_name: str, design_generation_rate: float | None = ...
    ) -> None:
        """Create a new ``ZoneContaminantSourceAndSink:CarbonDioxide`` and add it to the document.

        Represents internal CO2 gains and sinks in the zone.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-internal-gains-people-lights-other/#zonecontaminantsourceandsinkcarbondioxide
        """

class AirflowNetworkDistributionDuctViewFactors:
    def __call__(
        self,
        /,
        *,
        linkage_name: str,
        duct_surface_exposure_fraction: float | None = 0,
        duct_surface_emittance: float | None = 0.9,
        surfaces: list[_g.AirflowNetworkDistributionDuctViewFactorsSurfacesItem] = ...,
    ) -> None:
        """Create a new ``AirflowNetwork:Distribution:DuctViewFactors`` and add it to the document.

        This object is used to allow user-defined view factors to be used for duct-surface radiation calculations. All surfaces must be in the same enclosure.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-airflow-network/#airflownetworkdistributionductviewfactors
        """

class AirflowNetworkOccupantVentilationControl:
    def __call__(
        self,
        name: str,
        /,
        *,
        minimum_opening_time: float | None = 0,
        minimum_closing_time: float | None = 0,
        thermal_comfort_low_temperature_curve_name: str | None = ...,
        thermal_comfort_temperature_boundary_point: float | None = 10,
        thermal_comfort_high_temperature_curve_name: str | None = ...,
        maximum_threshold_for_persons_dissatisfied_ppd: float | None = 10,
        occupancy_check: Literal["", "No", "Yes"] | None = "No",
        opening_probability_schedule_name: str | None = ...,
        closing_probability_schedule_name: str | None = ...,
    ) -> None:
        """Create a new ``AirflowNetwork:OccupantVentilationControl`` and add it to the document.

        This object is used to provide advanced thermal comfort control of window opening and closing for both exterior and interior windows.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-airflow-network/#airflownetworkoccupantventilationcontrol
        """

class HVACTemplateZoneConstantVolume:
    def __call__(
        self,
        /,
        *,
        zone_name: str,
        template_constant_volume_system_name: str,
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
        design_specification_outdoor_air_object_name: str | None = ...,
        design_specification_zone_air_distribution_object_name: str | None = ...,
        reheat_coil_type: Literal["", "Electric", "Gas", "HotWater", "None"] | None = "None",
        reheat_coil_availability_schedule_name: str | None = ...,
        maximum_reheat_air_temperature: float | None = ...,
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
    ) -> None:
        """Create a new ``HVACTemplate:Zone:ConstantVolume`` and add it to the document.

        Zone terminal unit, constant volume, reheat optional. Referenced schedules must be defined elsewhere in the idf.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/hvac-template-objects/group-hvac-templates/#hvactemplatezoneconstantvolume
        """

class HVACTemplatePlantMixedWaterLoop:
    def __call__(
        self,
        name: str,
        /,
        *,
        pump_schedule_name: str | None = ...,
        pump_control_type: Literal["", "Continuous", "Intermittent"] | None = "Intermittent",
        operation_scheme_type: Literal["", "Default", "UserDefined"] | None = "Default",
        equipment_operation_schemes_name: str | None = ...,
        high_temperature_setpoint_schedule_name: str | None = ...,
        high_temperature_design_setpoint: float | None = 33,
        low_temperature_setpoint_schedule_name: str | None = ...,
        low_temperature_design_setpoint: float | None = 20,
        water_pump_configuration: Literal["", "ConstantFlow", "VariableFlow"] | None = "ConstantFlow",
        water_pump_rated_head: float | None = 179352,
        water_pump_type: Literal[
            "",
            "FiveHeaderedPumps",
            "FourHeaderedPumps",
            "PumpPerTowerOrBoiler",
            "SinglePump",
            "ThreeHeaderedPumps",
            "TwoHeaderedPumps",
        ]
        | None = "SinglePump",
        supply_side_bypass_pipe: Literal["", "No", "Yes"] | None = "Yes",
        demand_side_bypass_pipe: Literal["", "No", "Yes"] | None = "Yes",
        fluid_type: Literal[
            "",
            "EthyleneGlycol30",
            "EthyleneGlycol40",
            "EthyleneGlycol50",
            "EthyleneGlycol60",
            "PropyleneGlycol30",
            "PropyleneGlycol40",
            "PropyleneGlycol50",
            "PropyleneGlycol60",
            "Water",
        ]
        | None = "Water",
        loop_design_delta_temperature: float | None = 5.6,
        load_distribution_scheme: Literal[
            "", "Optimal", "SequentialLoad", "SequentialUniformPLR", "UniformLoad", "UniformPLR"
        ]
        | None = "SequentialLoad",
    ) -> None:
        """Create a new ``HVACTemplate:Plant:MixedWaterLoop`` and add it to the document.

        Central plant loop portion of a water source heat pump system.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/hvac-template-objects/group-hvac-templates/#hvactemplateplantmixedwaterloop
        """

class ZoneHVACLowTemperatureRadiantElectric:
    def __call__(
        self,
        name: str,
        /,
        *,
        heating_setpoint_temperature_schedule_name: str,
        availability_schedule_name: str | None = ...,
        zone_name: str | None = ...,
        surface_name_or_radiant_surface_group_name: str | None = ...,
        heating_design_capacity_method: Literal[
            "", "CapacityPerFloorArea", "FractionOfAutosizedHeatingCapacity", "HeatingDesignCapacity"
        ]
        | None = "HeatingDesignCapacity",
        heating_design_capacity: float | Literal["", "Autosize"] | None = "Autosize",
        heating_design_capacity_per_floor_area: float | None = ...,
        fraction_of_autosized_heating_design_capacity: float | None = 1,
        temperature_control_type: Literal[
            "",
            "MeanAirTemperature",
            "MeanRadiantTemperature",
            "OperativeTemperature",
            "OutdoorDryBulbTemperature",
            "OutdoorWetBulbTemperature",
            "SurfaceFaceTemperature",
            "SurfaceInteriorTemperature",
        ]
        | None = "MeanAirTemperature",
        setpoint_control_type: Literal["", "HalfFlowPower", "ZeroFlowPower"] | None = "HalfFlowPower",
        heating_throttling_range: float | None = 0,
    ) -> None:
        """Create a new ``ZoneHVAC:LowTemperatureRadiant:Electric`` and add it to the document.

        Electric resistance low temperature radiant system

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-radiative-convective-units/#zonehvaclowtemperatureradiantelectric
        """

class ZoneHVACEquipmentList:
    def __call__(
        self,
        name: str,
        /,
        *,
        load_distribution_scheme: Literal["", "SequentialLoad", "SequentialUniformPLR", "UniformLoad", "UniformPLR"]
        | None = "SequentialLoad",
        equipment: list[_g.ZoneHVACEquipmentListEquipmentItem] = ...,
    ) -> None:
        """Create a new ``ZoneHVAC:EquipmentList`` and add it to the document.

        List equipment in simulation order. Note that an ZoneHVAC:AirDistributionUnit object must be listed in this statement if there is a forced air system serving the zone from the air loop. Equipment is simulated in the order specified by Zone Equipment Cooling Sequence and Zone Equipment Heating or No-Load Sequence, depending on the thermostat request. For equipment of similar type, assign sequence 1 to the first system intended to serve that type of load. For situations where one or more equipment types has limited capacity or limited control, order the sequence so that the most controllable piece of equipment runs last. For example, with a dedicated outdoor air system (DOAS), the air terminal for the DOAS should be assigned Heating Sequence = 1 and Cooling Sequence = 1. Any other equipment should be assigned sequence 2 or higher so that it will see the net load after the DOAS air is added to the zone.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-zone-equipment/#zonehvacequipmentlist
        """

class CoilSystemCoolingWaterHeatExchangerAssisted:
    def __call__(
        self,
        name: str,
        /,
        *,
        heat_exchanger_object_type: Literal[
            "HeatExchanger:AirToAir:FlatPlate", "HeatExchanger:AirToAir:SensibleAndLatent"
        ],
        heat_exchanger_name: str,
        cooling_coil_object_type: Literal["Coil:Cooling:Water", "Coil:Cooling:Water:DetailedGeometry"],
        cooling_coil_name: str,
    ) -> None:
        """Create a new ``CoilSystem:Cooling:Water:HeatExchangerAssisted`` and add it to the document.

        Virtual component consisting of a chilled-water cooling coil and an air-to-air heat exchanger. The air-to-air heat exchanger precools the air entering the cooling coil and reuses this energy to reheat the supply air leaving the cooling coil. This heat exchange process improves the latent removal performance of the cooling coil (lower sensible heat ratio).

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-heating-and-cooling-coils/#coilsystemcoolingwaterheatexchangerassisted
        """

class HeatExchangerAirToAirFlatPlate:
    def __call__(
        self,
        name: str,
        /,
        *,
        nominal_supply_air_inlet_temperature: float,
        nominal_supply_air_outlet_temperature: float,
        nominal_secondary_air_flow_rate: float | Literal["Autosize"],
        nominal_secondary_air_inlet_temperature: float,
        supply_air_inlet_node_name: str,
        supply_air_outlet_node_name: str,
        secondary_air_inlet_node_name: str,
        secondary_air_outlet_node_name: str,
        availability_schedule_name: str | None = ...,
        flow_arrangement_type: Literal["CounterFlow", "CrossFlowBothUnmixed", "ParallelFlow"] | None = ...,
        economizer_lockout: Literal["", "No", "Yes"] | None = "Yes",
        ratio_of_supply_to_secondary_ha_values: float | None = ...,
        nominal_supply_air_flow_rate: float | Literal["", "Autosize"] | None = "Autosize",
        nominal_electric_power: float | None = ...,
    ) -> None:
        """Create a new ``HeatExchanger:AirToAir:FlatPlate`` and add it to the document.

        Flat plate air-to-air heat exchanger, typically used for exhaust or relief air heat recovery.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-heat-recovery/#heatexchangerairtoairflatplate
        """

class AirLoopHVACReturnPath:
    def __call__(
        self,
        name: str,
        /,
        *,
        return_air_path_outlet_node_name: str,
        components: list[_g.AirLoopHVACReturnPathComponentsItem] = ...,
    ) -> None:
        """Create a new ``AirLoopHVAC:ReturnPath`` and add it to the document.

        A return air path can only contain one AirLoopHVAC:ZoneMixer and one or more AirLoopHVAC:ReturnPlenum objects.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-air-path/#airloophvacreturnpath
        """

class ConnectorSplitter:
    def __call__(
        self, name: str, /, *, inlet_branch_name: str, branches: list[_g.ConnectorSplitterBranchesItem] = ...
    ) -> None:
        """Create a new ``Connector:Splitter`` and add it to the document.

        Split one air/water stream into N outlet streams. Branch names cannot be duplicated within a single Splitter list.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-node-branch-management/#connectorsplitter
        """

class PipeAdiabaticSteam:
    def __call__(self, name: str, /, *, inlet_node_name: str, outlet_node_name: str) -> None:
        """Create a new ``Pipe:Adiabatic:Steam`` and add it to the document.

        Passes Inlet Node state variables to Outlet Node state variables

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-node-branch-management/#pipeadiabaticsteam
        """

class SolarCollectorFlatPlateWater:
    def __call__(
        self,
        name: str,
        /,
        *,
        solarcollectorperformance_name: str,
        surface_name: str,
        inlet_node_name: str,
        outlet_node_name: str,
        maximum_flow_rate: float | None = ...,
    ) -> None:
        """Create a new ``SolarCollector:FlatPlate:Water`` and add it to the document.

        Flat plate water solar collector (single glazed, unglazed, or evacuated tube). Thermal and optical properties are taken from the referenced SolarCollectorPerformance:FlatPlate object. Collector tilt, azimuth, and gross area are taken from the referenced building surface or shading surface. The collector surface participates normally in all shading calculations.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-solar-collectors/#solarcollectorflatplatewater
        """

class AnyBoilerSteam:
    def __call__(
        self,
        name: str,
        /,
        *,
        fuel_type: Literal["Coal", "Diesel", "Electricity", "Gasoline", "NaturalGas", "OtherFuel1", "OtherFuel2"],
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
    ) -> None:
        """Create a new ``Boiler:Steam`` and add it to the document.

        This boiler model is an adaptation of the empirical model from the Building Loads and System Thermodynamics (BLAST) program. Boiler performance curves are generated by fitting catalog data to third order polynomial equations. A constant efficiency boiler is modeled by setting the fuel use coefficients as follows: N9=1, N10=0, N11=0

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-plant-equipment/#boilersteam
        """

class DistrictCooling:
    def __call__(
        self,
        name: str,
        /,
        *,
        chilled_water_inlet_node_name: str,
        chilled_water_outlet_node_name: str,
        nominal_capacity: float | Literal["Autosize"] | None = ...,
        capacity_fraction_schedule_name: str | None = ...,
    ) -> None:
        """Create a new ``DistrictCooling`` and add it to the document.

        Centralized source of chilled water, such as a district cooling system.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-plant-equipment/#districtcooling
        """

class AnyCentralHeatPumpSystem:
    def __call__(
        self,
        name: str,
        /,
        *,
        cooling_loop_inlet_node_name: str,
        cooling_loop_outlet_node_name: str,
        source_loop_inlet_node_name: str,
        source_loop_outlet_node_name: str,
        heating_loop_inlet_node_name: str,
        heating_loop_outlet_node_name: str,
        chiller_heater_modules_performance_component_object_type_1: Literal["ChillerHeaterPerformance:Electric:EIR"],
        chiller_heater_modules_performance_component_name_1: str,
        chiller_heater_modules_control_schedule_name_1: str,
        ancillary_power: float | None = 0,
        ancillary_operation_schedule_name: str | None = ...,
        number_of_chiller_heater_modules_1: int | None = 1,
        chiller_heater_modules_performance_component_object_type_2: Literal["ChillerHeaterPerformance:Electric:EIR"]
        | None = ...,
        chiller_heater_modules_performance_component_name_2: str | None = ...,
        chiller_heater_modules_control_schedule_name_2: str | None = ...,
        number_of_chiller_heater_modules_2: int | None = 1,
        chiller_heater_performance_component_object_type_3: Literal["ChillerHeaterPerformance:Electric:EIR"]
        | None = ...,
        chiller_heater_performance_component_name_3: str | None = ...,
        chiller_heater_modules_control_schedule_name_3: str | None = ...,
        number_of_chiller_heater_modules_3: int | None = 1,
        chiller_heater_modules_performance_component_object_type_4: Literal["ChillerHeaterPerformance:Electric:EIR"]
        | None = ...,
        chiller_heater_modules_performance_component_name_4: str | None = ...,
        chiller_heater_modules_control_schedule_name_4: str | None = ...,
        number_of_chiller_heater_modules_4: int | None = 1,
        chiller_heater_modules_performance_component_object_type_5: Literal["ChillerHeaterPerformance:Electric:EIR"]
        | None = ...,
        chiller_heater_models_performance_component_name_5: str | None = ...,
        chiller_heater_modules_control_schedule_name_5: str | None = ...,
        number_of_chiller_heater_modules_5: int | None = 1,
        chiller_heater_modules_performance_component_object_type_6: Literal["ChillerHeaterPerformance:Electric:EIR"]
        | None = ...,
        chiller_heater_modules_performance_component_name_6: str | None = ...,
        chiller_heater_modules_control_schedule_name_6: str | None = ...,
        number_of_chiller_heater_modules_6: int | None = 1,
        chiller_heater_modules_performance_component_object_type_7: Literal["ChillerHeaterPerformance:Electric:EIR"]
        | None = ...,
        chiller_heater_modules_performance_component_name_7: str | None = ...,
        chiller_heater_modules_control_schedule_name_7: str | None = ...,
        number_of_chiller_heater_modules_7: int | None = 1,
        chiller_heater_modules_performance_component_object_type_8: Literal["ChillerHeaterPerformance:Electric:EIR"]
        | None = ...,
        chiller_heater_modules_performance_component_name_8: str | None = ...,
        chiller_heater_modules_control_schedule_name_8: str | None = ...,
        number_of_chiller_heater_modules_8: int | None = 1,
        chiller_heater_modules_performance_component_object_type_9: Literal["ChillerHeaterPerformance:Electric:EIR"]
        | None = ...,
        chiller_heater_modules_performance_component_name_9: str | None = ...,
        chiller_heater_modules_control_schedule_name_9: str | None = ...,
        number_of_chiller_heater_modules_9: int | None = 1,
        chiller_heater_modules_performance_component_object_type_10: Literal["ChillerHeaterPerformance:Electric:EIR"]
        | None = ...,
        chiller_heater_modules_performance_component_name_10: str | None = ...,
        chiller_heater_modules_control_schedule_name_10: str | None = ...,
        number_of_chiller_heater_modules_10: int | None = 1,
        chiller_heater_modules_performance_component_object_type_11: Literal["ChillerHeaterPerformance:Electric:EIR"]
        | None = ...,
        chiller_heater_modules_performance_component_name_11: str | None = ...,
        chiller_heater_module_control_schedule_name_11: str | None = ...,
        number_of_chiller_heater_modules_11: int | None = 1,
        chiller_heater_modules_performance_component_object_type_12: Literal["ChillerHeaterPerformance:Electric:EIR"]
        | None = ...,
        chiller_heater_modules_performance_component_name_12: str | None = ...,
        chiller_heater_modules_control_schedule_name_12: str | None = ...,
        number_of_chiller_heater_modules_12: int | None = 1,
        chiller_heater_modules_performance_component_object_type_13: Literal["ChillerHeaterPerformance:Electric:EIR"]
        | None = ...,
        chiller_heater_modules_performance_component_name_13: str | None = ...,
        chiller_heater_modules_control_schedule_name_13: str | None = ...,
        number_of_chiller_heater_modules_13: int | None = 1,
        chiller_heater_modules_performance_component_object_type_14: Literal["ChillerHeaterPerformance:Electric:EIR"]
        | None = ...,
        chiller_heater_modules_performance_component_name_14: str | None = ...,
        chiller_heater_modules_control_schedule_name_14: str | None = ...,
        number_of_chiller_heater_modules_14: int | None = 1,
        chiller_heater_modules_performance_component_object_type_15: Literal["ChillerHeaterPerformance:Electric:EIR"]
        | None = ...,
        chiller_heater_modules_performance_component_name_15: str | None = ...,
        chiller_heater_modules_control_schedule_name_15: str | None = ...,
        number_of_chiller_heater_modules_15: int | None = 1,
        chiller_heater_modules_performance_component_object_type_16: Literal["ChillerHeaterPerformance:Electric:EIR"]
        | None = ...,
        chiller_heater_modules_performance_component_name_16: str | None = ...,
        chiller_heater_modules_control_schedule_name_16: str | None = ...,
        number_of_chiller_heater_modules_16: int | None = 1,
        chiller_heater_modules_performance_component_object_type_17: Literal["ChillerHeaterPerformance:Electric:EIR"]
        | None = ...,
        chiller_heater_modules_performance_component_name_17: str | None = ...,
        chiller_heater_modules_control_schedule_name_17: str | None = ...,
        number_of_chiller_heater_modules_17: int | None = 1,
        chiller_heater_modules_performance_component_object_type_18: Literal["ChillerHeaterPerformance:Electric:EIR"]
        | None = ...,
        chiller_heater_modules_performance_component_name_18: str | None = ...,
        chiller_heater_modules_control_control_schedule_name_18: str | None = ...,
        number_of_chiller_heater_modules_18: int | None = 1,
        chiller_heater_modules_performance_component_object_type_19: Literal["ChillerHeaterPerformance:Electric:EIR"]
        | None = ...,
        chiller_heater_modules_performance_component_name_19: str | None = ...,
        chiller_heater_modules_control_schedule_name_19: str | None = ...,
        number_of_chiller_heater_modules_19: int | None = 1,
        chiller_heater_modules_performance_component_object_type_20: Literal["ChillerHeaterPerformance:Electric:EIR"]
        | None = ...,
        chiller_heater_modules_performance_component_name_20: str | None = ...,
        chiller_heater_modules_control_schedule_name_20: str | None = ...,
        number_of_chiller_heater_modules_20: int | None = 1,
    ) -> None:
        """Create a new ``CentralHeatPumpSystem`` and add it to the document.

        This chiller bank can contain multiple chiller heaters and heat pump performance objects. Its function is to encapsulate the extra controls needed to turn individual modules on/off and whether they are to operate in cooling-only, heating-only or simultaneous cooling/heating mode and whether to connect the source water to the evaporator or condenser side.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-plant-equipment/#centralheatpumpsystem
        """

class CoolingTowerSingleSpeed:
    def __call__(
        self,
        name: str,
        /,
        *,
        water_inlet_node_name: str,
        water_outlet_node_name: str,
        design_air_flow_rate: float | Literal["Autosize"],
        design_fan_power: float | Literal["Autosize"],
        design_water_flow_rate: float | Literal["Autosize"] | None = ...,
        design_u_factor_times_area_value: float | Literal["Autosize"] | None = ...,
        free_convection_regime_air_flow_rate: float | Literal["", "Autocalculate"] | None = 0,
        free_convection_regime_air_flow_rate_sizing_factor: float | None = 0.1,
        free_convection_regime_u_factor_times_area_value: float | Literal["", "Autocalculate"] | None = 0,
        free_convection_u_factor_times_area_value_sizing_factor: float | None = 0.1,
        performance_input_method: Literal["", "NominalCapacity", "UFactorTimesAreaAndDesignWaterFlowRate"]
        | None = "UFactorTimesAreaAndDesignWaterFlowRate",
        heat_rejection_capacity_and_nominal_capacity_sizing_ratio: float | None = 1.25,
        nominal_capacity: float | None = ...,
        free_convection_capacity: float | Literal["Autocalculate"] | None = ...,
        free_convection_nominal_capacity_sizing_factor: float | None = 0.1,
        design_inlet_air_dry_bulb_temperature: float | None = 35,
        design_inlet_air_wet_bulb_temperature: float | None = 25.6,
        design_approach_temperature: float | Literal["", "Autosize"] | None = "Autosize",
        design_range_temperature: float | Literal["", "Autosize"] | None = "Autosize",
        basin_heater_capacity: float | None = 0,
        basin_heater_setpoint_temperature: float | None = 2,
        basin_heater_operating_schedule_name: str | None = ...,
        evaporation_loss_mode: Literal["", "LossFactor", "SaturatedExit"] | None = "SaturatedExit",
        evaporation_loss_factor: float | None = 0.2,
        drift_loss_percent: float | None = 0.008,
        blowdown_calculation_mode: Literal["", "ConcentrationRatio", "ScheduledRate"] | None = "ConcentrationRatio",
        blowdown_concentration_ratio: float | None = 3,
        blowdown_makeup_water_usage_schedule_name: str | None = ...,
        supply_water_storage_tank_name: str | None = ...,
        outdoor_air_inlet_node_name: str | None = ...,
        capacity_control: Literal["", "FanCycling", "FluidBypass"] | None = "FanCycling",
        number_of_cells: int | None = 1,
        cell_control: Literal["", "MaximalCell", "MinimalCell"] | None = "MaximalCell",
        cell_minimum_water_flow_rate_fraction: float | None = 0.33,
        cell_maximum_water_flow_rate_fraction: float | None = 2.5,
        sizing_factor: float | None = 1,
        end_use_subcategory: str | None = "General",
    ) -> None:
        """Create a new ``CoolingTower:SingleSpeed`` and add it to the document.

        This tower model is based on Merkel's theory, which is also the basis for the tower model in ASHRAE's HVAC1 Toolkit. The open wet cooling tower is modeled as a counter flow heat exchanger with a single-speed fan drawing air through the tower (induced-draft configuration). Added fluid bypass as an additional capacity control. 8/2008. For a multi-cell tower, the capacity and air/water flow rate inputs are for the entire tower.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-condenser-equipment/#coolingtowersinglespeed
        """

class AnyHeatExchangerFluidToFluid:
    def __call__(
        self,
        name: str,
        /,
        *,
        loop_demand_side_inlet_node_name: str,
        loop_demand_side_outlet_node_name: str,
        loop_demand_side_design_flow_rate: float | Literal["Autosize"],
        loop_supply_side_inlet_node_name: str,
        loop_supply_side_outlet_node_name: str,
        loop_supply_side_design_flow_rate: float | Literal["Autosize"],
        heat_exchanger_u_factor_times_area_value: float | Literal["Autosize"],
        availability_schedule_name: str | None = ...,
        heat_exchange_model_type: Literal[
            "",
            "CounterFlow",
            "CrossFlowBothMixed",
            "CrossFlowBothUnMixed",
            "CrossFlowSupplyMixedDemandUnMixed",
            "CrossFlowSupplyUnMixedDemandMixed",
            "Ideal",
            "ParallelFlow",
        ]
        | None = "Ideal",
        control_type: Literal[
            "",
            "CoolingDifferentialOnOff",
            "CoolingSetpointModulated",
            "CoolingSetpointOnOff",
            "CoolingSetpointOnOffWithComponentOverride",
            "DualDeadbandSetpointModulated",
            "DualDeadbandSetpointOnOff",
            "HeatingSetpointModulated",
            "HeatingSetpointOnOff",
            "OperationSchemeModulated",
            "OperationSchemeOnOff",
            "UncontrolledOn",
        ]
        | None = "UncontrolledOn",
        heat_exchanger_setpoint_node_name: str | None = ...,
        minimum_temperature_difference_to_activate_heat_exchanger: float | None = 0.01,
        heat_transfer_metering_end_use_type: Literal[
            "", "FreeCooling", "HeatRecoveryForCooling", "HeatRecoveryForHeating", "HeatRejection", "LoopToLoop"
        ]
        | None = "LoopToLoop",
        component_override_loop_supply_side_inlet_node_name: str | None = ...,
        component_override_loop_demand_side_inlet_node_name: str | None = ...,
        component_override_cooling_control_temperature_mode: Literal[
            "", "DryBulbTemperature", "Loop", "WetBulbTemperature"
        ]
        | None = "Loop",
        sizing_factor: float | None = 1,
        operation_minimum_temperature_limit: float | None = ...,
        operation_maximum_temperature_limit: float | None = ...,
    ) -> None:
        """Create a new ``HeatExchanger:FluidToFluid`` and add it to the document.

        A fluid/fluid heat exchanger designed to couple the supply side of one loop to the demand side of another loop Loops can be either plant or condenser loops but no air side connections are allowed

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-condenser-equipment/#heatexchangerfluidtofluid
        """

class EnergyManagementSystemOutputVariable:
    def __call__(
        self,
        name: str,
        /,
        *,
        ems_variable_name: str,
        type_of_data_in_variable: Literal["Averaged", "Summed"],
        update_frequency: Literal["SystemTimestep", "ZoneTimestep"],
        ems_program_or_subroutine_name: str | None = ...,
        units: str | None = ...,
    ) -> None:
        """Create a new ``EnergyManagementSystem:OutputVariable`` and add it to the document.

        This object sets up an EnergyPlus output variable from an Erl variable

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-energy-management-system-ems/#energymanagementsystemoutputvariable
        """

class GeneratorFuelSupply:
    def __call__(
        self,
        name: str,
        /,
        *,
        fuel_temperature_modeling_mode: Literal["Scheduled", "TemperatureFromAirNode"] | None = ...,
        fuel_temperature_reference_node_name: str | None = ...,
        fuel_temperature_schedule_name: str | None = ...,
        compressor_power_multiplier_function_of_fuel_rate_curve_name: str | None = ...,
        compressor_heat_loss_factor: float | None = ...,
        fuel_type: Literal["GaseousConstituents", "LiquidGeneric"] | None = ...,
        liquid_generic_fuel_lower_heating_value: float | None = ...,
        liquid_generic_fuel_higher_heating_value: float | None = ...,
        liquid_generic_fuel_molecular_weight: float | None = ...,
        liquid_generic_fuel_co2_emission_factor: float | None = ...,
        number_of_constituents_in_gaseous_constituent_fuel_supply: float | None = ...,
        constituent_1_name: Literal[
            "Argon",
            "Butane",
            "CarbonDioxide",
            "Ethane",
            "Ethanol",
            "Hexane",
            "Hydrogen",
            "Methane",
            "Methanol",
            "Nitrogen",
            "Oxygen",
            "Pentane",
            "Propane",
            "Water",
        ]
        | None = ...,
        constituent_1_molar_fraction: float | None = ...,
        constituent_2_name: Literal[
            "Argon",
            "Butane",
            "CarbonDioxide",
            "Ethane",
            "Ethanol",
            "Hexane",
            "Hydrogen",
            "Methane",
            "Methanol",
            "Nitrogen",
            "Oxygen",
            "Pentane",
            "Propane",
            "Water",
        ]
        | None = ...,
        constituent_2_molar_fraction: float | None = ...,
        constituent_3_name: Literal[
            "Argon",
            "Butane",
            "CarbonDioxide",
            "Ethane",
            "Ethanol",
            "Hexane",
            "Hydrogen",
            "Methane",
            "Methanol",
            "Nitrogen",
            "Oxygen",
            "Pentane",
            "Propane",
            "Water",
        ]
        | None = ...,
        constituent_3_molar_fraction: float | None = ...,
        constituent_4_name: Literal[
            "Argon",
            "Butane",
            "CarbonDioxide",
            "Ethane",
            "Ethanol",
            "Hexane",
            "Hydrogen",
            "Methane",
            "Methanol",
            "Nitrogen",
            "Oxygen",
            "Pentane",
            "Propane",
            "Water",
        ]
        | None = ...,
        constituent_4_molar_fraction: float | None = ...,
        constituent_5_name: Literal[
            "Argon",
            "Butane",
            "CarbonDioxide",
            "Ethane",
            "Ethanol",
            "Hexane",
            "Hydrogen",
            "Methane",
            "Methanol",
            "Nitrogen",
            "Oxygen",
            "Pentane",
            "Propane",
            "Water",
        ]
        | None = ...,
        constituent_5_molar_fraction: float | None = ...,
        constituent_6_name: Literal[
            "Argon",
            "Butane",
            "CarbonDioxide",
            "Ethane",
            "Ethanol",
            "Hexane",
            "Hydrogen",
            "Methane",
            "Methanol",
            "Nitrogen",
            "Oxygen",
            "Pentane",
            "Propane",
            "Water",
        ]
        | None = ...,
        constituent_6_molar_fraction: float | None = ...,
        constituent_7_name: Literal[
            "Butane", "Ethane", "Ethanol", "Hexane", "Hydrogen", "Methane", "Methanol", "Pentane", "Propane"
        ]
        | None = ...,
        constituent_7_molar_fraction: float | None = ...,
        constituent_8_name: Literal[
            "Argon",
            "Butane",
            "CarbonDioxide",
            "Ethane",
            "Ethanol",
            "Hexane",
            "Hydrogen",
            "Methane",
            "Methanol",
            "Nitrogen",
            "Oxygen",
            "Pentane",
            "Propane",
            "Water",
        ]
        | None = ...,
        constituent_8_molar_fraction: float | None = ...,
        constituent_9_name: Literal[
            "Argon",
            "Butane",
            "CarbonDioxide",
            "Ethane",
            "Ethanol",
            "Hexane",
            "Hydrogen",
            "Methane",
            "Methanol",
            "Nitrogen",
            "Oxygen",
            "Pentane",
            "Propane",
            "Water",
        ]
        | None = ...,
        constituent_9_molar_fraction: float | None = ...,
        constituent_10_name: Literal[
            "Argon",
            "Butane",
            "CarbonDioxide",
            "Ethane",
            "Ethanol",
            "Hexane",
            "Hydrogen",
            "Methane",
            "Methanol",
            "Nitrogen",
            "Oxygen",
            "Pentane",
            "Propane",
            "Water",
        ]
        | None = ...,
        constituent_10_molar_fraction: float | None = ...,
        constituent_11_name: Literal[
            "Argon",
            "Butane",
            "CarbonDioxide",
            "Ethane",
            "Ethanol",
            "Hexane",
            "Hydrogen",
            "Methane",
            "Methanol",
            "Nitrogen",
            "Oxygen",
            "Pentane",
            "Propane",
            "Water",
        ]
        | None = ...,
        constituent_11_molar_fraction: float | None = ...,
        constituent_12_name: Literal[
            "Argon",
            "Butane",
            "CarbonDioxide",
            "Ethane",
            "Ethanol",
            "Hexane",
            "Hydrogen",
            "Methane",
            "Methanol",
            "Nitrogen",
            "Oxygen",
            "Pentane",
            "Propane",
            "Water",
        ]
        | None = ...,
        constituent_12_molar_fraction: float | None = ...,
    ) -> None:
        """Create a new ``Generator:FuelSupply`` and add it to the document.

        Used only with Generator:FuelCell and Generator:MicroCHP

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-electric-load-center-generator/#generatorfuelsupply
        """

class WaterUseRainCollector:
    def __call__(
        self,
        name: str,
        /,
        *,
        storage_tank_name: str,
        loss_factor_mode: Literal["Constant", "Scheduled"] | None = ...,
        collection_loss_factor: float | None = ...,
        collection_loss_factor_schedule_name: str | None = ...,
        maximum_collection_rate: float | None = ...,
        surfaces: list[_g.WaterUseRainCollectorSurfacesItem] = ...,
    ) -> None:
        """Create a new ``WaterUse:RainCollector`` and add it to the document.

        Used for harvesting rainwater falling on building surfaces. The rainwater is sent to a WaterUse:Storage object. In versions up till Version 9.6, it is necessary to also include a Site:Precipitation object to describe the rates of rainfall, in order to use this object. In later versions, if the Site:Precipitation is not present, precipitation depth in the weather input .epw will be used instead. When this is the case, please make sure the precipitation in the .epw is accurate.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-water-systems/#wateruseraincollector
        """

class FaultModelTemperatureSensorOffsetOutdoorAir:
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
    ) -> None:
        """Create a new ``FaultModel:TemperatureSensorOffset:OutdoorAir`` and add it to the document.

        This object describes outdoor air temperature sensor offset

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-operational-faults/#faultmodeltemperaturesensoroffsetoutdoorair
        """

class CurveQuintLinear:
    def __call__(
        self,
        name: str,
        /,
        *,
        coefficient1_constant: float,
        coefficient2_v: float,
        coefficient3_w: float,
        coefficient4_x: float,
        coefficient5_y: float,
        coefficient6_z: float,
        minimum_value_of_v: float,
        maximum_value_of_v: float,
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
        input_unit_type_for_v: Literal[
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
    ) -> None:
        """Create a new ``Curve:QuintLinear`` and add it to the document.

        Linear curve with five independent variables. Input for the linear curve consists of a curve name, the two coefficients, and the maximum and minimum valid independent variable values. Optional inputs for curve minimum and maximum may be used to limit the output of the performance curve. curve = C1 + C2*v + C3*w + C4*x + C5*y + C6*z

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-performance-curves/#curvequintlinear
        """

class FluidPropertiesSaturated:
    def __call__(
        self,
        /,
        *,
        fluid_name: str | None = ...,
        fluid_property_type: Literal["Density", "Enthalpy", "Pressure", "SpecificHeat"] | None = ...,
        fluid_phase: Literal["Fluid", "FluidGas"] | None = ...,
        temperature_values_name: str | None = ...,
        property_value_1: float | None = ...,
        property_value_2: float | None = ...,
        property_value_3: float | None = ...,
        property_value_4: float | None = ...,
        property_value_5: float | None = ...,
        property_value_6: float | None = ...,
        property_value_7: float | None = ...,
        property_value_8: float | None = ...,
        property_value_9: float | None = ...,
        property_value_10: float | None = ...,
        property_value_11: float | None = ...,
        property_value_12: float | None = ...,
        property_value_13: float | None = ...,
        property_value_14: float | None = ...,
        property_value_15: float | None = ...,
        property_value_16: float | None = ...,
        property_value_17: float | None = ...,
        property_value_18: float | None = ...,
        property_value_19: float | None = ...,
        property_value_20: float | None = ...,
        property_value_21: float | None = ...,
        property_value_22: float | None = ...,
        property_value_23: float | None = ...,
        property_value_24: float | None = ...,
        property_value_25: float | None = ...,
        property_value_26: float | None = ...,
        property_value_27: float | None = ...,
        property_value_28: float | None = ...,
        property_value_29: float | None = ...,
        property_value_30: float | None = ...,
        property_value_31: float | None = ...,
        property_value_32: float | None = ...,
        property_value_33: float | None = ...,
        property_value_34: float | None = ...,
        property_value_35: float | None = ...,
        property_value_36: float | None = ...,
        property_value_37: float | None = ...,
        property_value_38: float | None = ...,
        property_value_39: float | None = ...,
        property_value_40: float | None = ...,
        property_value_41: float | None = ...,
        property_value_42: float | None = ...,
        property_value_43: float | None = ...,
        property_value_44: float | None = ...,
        property_value_45: float | None = ...,
        property_value_46: float | None = ...,
        property_value_47: float | None = ...,
        property_value_48: float | None = ...,
        property_value_49: float | None = ...,
        property_value_50: float | None = ...,
        property_value_51: float | None = ...,
        property_value_52: float | None = ...,
        property_value_53: float | None = ...,
        property_value_54: float | None = ...,
        property_value_55: float | None = ...,
        property_value_56: float | None = ...,
        property_value_57: float | None = ...,
        property_value_58: float | None = ...,
        property_value_59: float | None = ...,
        property_value_60: float | None = ...,
        property_value_61: float | None = ...,
        property_value_62: float | None = ...,
        property_value_63: float | None = ...,
        property_value_64: float | None = ...,
        property_value_65: float | None = ...,
        property_value_66: float | None = ...,
        property_value_67: float | None = ...,
        property_value_68: float | None = ...,
        property_value_69: float | None = ...,
        property_value_70: float | None = ...,
        property_value_71: float | None = ...,
        property_value_72: float | None = ...,
        property_value_73: float | None = ...,
        property_value_74: float | None = ...,
        property_value_75: float | None = ...,
        property_value_76: float | None = ...,
        property_value_77: float | None = ...,
        property_value_78: float | None = ...,
        property_value_79: float | None = ...,
        property_value_80: float | None = ...,
        property_value_81: float | None = ...,
        property_value_82: float | None = ...,
        property_value_83: float | None = ...,
        property_value_84: float | None = ...,
        property_value_85: float | None = ...,
        property_value_86: float | None = ...,
        property_value_87: float | None = ...,
        property_value_88: float | None = ...,
        property_value_89: float | None = ...,
        property_value_90: float | None = ...,
        property_value_91: float | None = ...,
        property_value_92: float | None = ...,
        property_value_93: float | None = ...,
        property_value_94: float | None = ...,
        property_value_95: float | None = ...,
        property_value_96: float | None = ...,
        property_value_97: float | None = ...,
        property_value_98: float | None = ...,
        property_value_99: float | None = ...,
        property_value_100: float | None = ...,
        property_value_101: float | None = ...,
        property_value_102: float | None = ...,
        property_value_103: float | None = ...,
        property_value_104: float | None = ...,
        property_value_105: float | None = ...,
        property_value_106: float | None = ...,
        property_value_107: float | None = ...,
        property_value_108: float | None = ...,
        property_value_109: float | None = ...,
        property_value_110: float | None = ...,
        property_value_111: float | None = ...,
        property_value_112: float | None = ...,
        property_value_113: float | None = ...,
        property_value_114: float | None = ...,
        property_value_115: float | None = ...,
        property_value_116: float | None = ...,
        property_value_117: float | None = ...,
        property_value_118: float | None = ...,
        property_value_119: float | None = ...,
        property_value_120: float | None = ...,
        property_value_121: float | None = ...,
        property_value_122: float | None = ...,
        property_value_123: float | None = ...,
        property_value_124: float | None = ...,
        property_value_125: float | None = ...,
        property_value_126: float | None = ...,
        property_value_127: float | None = ...,
        property_value_128: float | None = ...,
        property_value_129: float | None = ...,
        property_value_130: float | None = ...,
        property_value_131: float | None = ...,
        property_value_132: float | None = ...,
        property_value_133: float | None = ...,
        property_value_134: float | None = ...,
        property_value_135: float | None = ...,
        property_value_136: float | None = ...,
        property_value_137: float | None = ...,
        property_value_138: float | None = ...,
        property_value_139: float | None = ...,
        property_value_140: float | None = ...,
        property_value_141: float | None = ...,
        property_value_142: float | None = ...,
        property_value_143: float | None = ...,
        property_value_144: float | None = ...,
        property_value_145: float | None = ...,
        property_value_146: float | None = ...,
        property_value_147: float | None = ...,
        property_value_148: float | None = ...,
        property_value_149: float | None = ...,
        property_value_150: float | None = ...,
        property_value_151: float | None = ...,
        property_value_152: float | None = ...,
        property_value_153: float | None = ...,
        property_value_154: float | None = ...,
        property_value_155: float | None = ...,
        property_value_156: float | None = ...,
        property_value_157: float | None = ...,
        property_value_158: float | None = ...,
        property_value_159: float | None = ...,
        property_value_160: float | None = ...,
        property_value_161: float | None = ...,
        property_value_162: float | None = ...,
        property_value_163: float | None = ...,
        property_value_164: float | None = ...,
        property_value_165: float | None = ...,
        property_value_166: float | None = ...,
        property_value_167: float | None = ...,
        property_value_168: float | None = ...,
        property_value_169: float | None = ...,
        property_value_170: float | None = ...,
        property_value_171: float | None = ...,
        property_value_172: float | None = ...,
        property_value_173: float | None = ...,
        property_value_174: float | None = ...,
        property_value_175: float | None = ...,
        property_value_176: float | None = ...,
        property_value_177: float | None = ...,
        property_value_178: float | None = ...,
        property_value_179: float | None = ...,
        property_value_180: float | None = ...,
        property_value_181: float | None = ...,
        property_value_182: float | None = ...,
        property_value_183: float | None = ...,
        property_value_184: float | None = ...,
        property_value_185: float | None = ...,
        property_value_186: float | None = ...,
        property_value_187: float | None = ...,
        property_value_188: float | None = ...,
        property_value_189: float | None = ...,
        property_value_190: float | None = ...,
        property_value_191: float | None = ...,
        property_value_192: float | None = ...,
        property_value_193: float | None = ...,
        property_value_194: float | None = ...,
        property_value_195: float | None = ...,
        property_value_196: float | None = ...,
        property_value_197: float | None = ...,
        property_value_198: float | None = ...,
        property_value_199: float | None = ...,
        property_value_200: float | None = ...,
        property_value_201: float | None = ...,
        property_value_202: float | None = ...,
        property_value_203: float | None = ...,
        property_value_204: float | None = ...,
        property_value_205: float | None = ...,
        property_value_206: float | None = ...,
        property_value_207: float | None = ...,
        property_value_208: float | None = ...,
        property_value_209: float | None = ...,
        property_value_210: float | None = ...,
        property_value_211: float | None = ...,
        property_value_212: float | None = ...,
        property_value_213: float | None = ...,
        property_value_214: float | None = ...,
        property_value_215: float | None = ...,
        property_value_216: float | None = ...,
        property_value_217: float | None = ...,
        property_value_218: float | None = ...,
        property_value_219: float | None = ...,
        property_value_220: float | None = ...,
        property_value_221: float | None = ...,
        property_value_222: float | None = ...,
        property_value_223: float | None = ...,
        property_value_224: float | None = ...,
        property_value_225: float | None = ...,
        property_value_226: float | None = ...,
        property_value_227: float | None = ...,
        property_value_228: float | None = ...,
        property_value_229: float | None = ...,
        property_value_230: float | None = ...,
        property_value_231: float | None = ...,
        property_value_232: float | None = ...,
        property_value_233: float | None = ...,
        property_value_234: float | None = ...,
        property_value_235: float | None = ...,
        property_value_236: float | None = ...,
        property_value_237: float | None = ...,
        property_value_238: float | None = ...,
        property_value_239: float | None = ...,
        property_value_240: float | None = ...,
        property_value_241: float | None = ...,
        property_value_242: float | None = ...,
        property_value_243: float | None = ...,
        property_value_244: float | None = ...,
        property_value_245: float | None = ...,
        property_value_246: float | None = ...,
        property_value_247: float | None = ...,
        property_value_248: float | None = ...,
        property_value_249: float | None = ...,
        property_value_250: float | None = ...,
    ) -> None:
        """Create a new ``FluidProperties:Saturated`` and add it to the document.

        fluid properties for the saturated region

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-fluid-properties/#fluidpropertiessaturated
        """

class OutputMeterCumulative:
    def __call__(
        self,
        /,
        *,
        key_name: str,
        reporting_frequency: Literal[
            "", "Annual", "Daily", "Detailed", "Environment", "Hourly", "Monthly", "RunPeriod", "Timestep"
        ]
        | None = "Hourly",
    ) -> None:
        """Create a new ``Output:Meter:Cumulative`` and add it to the document.

        Each Output:Meter:Cumulative command picks meters to be reported cumulatively onto the standard output file (.eso) and meter file (.mtr). Not all meters are reported in every simulation. a list of meters that can be reported are available after a run on the meter dictionary file (.mdd) if the Output:VariableDictionary has been requested.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-output-reporting/#outputmetercumulative
        """
