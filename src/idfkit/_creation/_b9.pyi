"""Creation signatures of generated classes (stub only).

DO NOT EDIT — regenerate with:
    python -m idfkit.codegen.generate_stubs
"""

from __future__ import annotations

from typing import Literal

from .. import _generated_types as _g

class ZoneAirContaminantBalance:
    def __call__(
        self,
        /,
        *,
        carbon_dioxide_concentration: Literal["", "No", "Yes"] | None = "No",
        outdoor_carbon_dioxide_schedule_name: str | None = ...,
        generic_contaminant_concentration: Literal["", "No", "Yes"] | None = "No",
        outdoor_generic_contaminant_schedule_name: str | None = ...,
    ) -> None:
        """Create a new ``ZoneAirContaminantBalance`` and add it to the document.

        Determines which contaminant concentration will be simulates.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-simulation-parameters/#zoneaircontaminantbalance
        """

class AnyHVACSystemRootFindingAlgorithm:
    def __call__(
        self,
        /,
        *,
        algorithm: Literal[
            "", "Alternation", "Bisection", "BisectionThenRegulaFalsi", "RegulaFalsi", "RegulaFalsiThenBisection"
        ]
        | None = "RegulaFalsi",
        number_of_iterations_before_algorithm_switch: int | None = 5,
    ) -> None:
        """Create a new ``HVACSystemRootFindingAlgorithm`` and add it to the document.

        Specifies a HVAC system solver algorithm to find a root

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-simulation-parameters/#hvacsystemrootfindingalgorithm
        """

class RunPeriod:
    def __call__(
        self,
        name: str,
        /,
        *,
        begin_month: int,
        begin_day_of_month: int,
        end_month: int,
        end_day_of_month: int,
        begin_year: float | None = ...,
        end_year: float | None = ...,
        day_of_week_for_start_day: Literal["Friday", "Monday", "Saturday", "Sunday", "Thursday", "Tuesday", "Wednesday"]
        | None = ...,
        use_weather_file_holidays_and_special_days: Literal["", "No", "Yes"] | None = "Yes",
        use_weather_file_daylight_saving_period: Literal["", "No", "Yes"] | None = "Yes",
        apply_weekend_holiday_rule: Literal["", "No", "Yes"] | None = "No",
        use_weather_file_rain_indicators: Literal["", "No", "Yes"] | None = "Yes",
        use_weather_file_snow_indicators: Literal["", "No", "Yes"] | None = "Yes",
        treat_weather_as_actual: Literal["", "No", "Yes"] | None = "No",
        first_hour_interpolation_starting_values: Literal["", "Hour1", "Hour24"] | None = "Hour24",
    ) -> None:
        """Create a new ``RunPeriod`` and add it to the document.

        Specify a range of dates and other parameters for a simulation. Multiple run periods may be input, but they may not overlap.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-location-climate-weather-file-access/#runperiod
        """

class SiteGroundTemperatureUndisturbedXing:
    def __call__(
        self,
        name: str,
        /,
        *,
        soil_thermal_conductivity: float,
        soil_density: float,
        soil_specific_heat: float,
        average_soil_surface_temperature: float,
        soil_surface_temperature_amplitude_1: float,
        soil_surface_temperature_amplitude_2: float,
        phase_shift_of_temperature_amplitude_1: float,
        phase_shift_of_temperature_amplitude_2: float,
    ) -> None:
        """Create a new ``Site:GroundTemperature:Undisturbed:Xing`` and add it to the document.

        Undisturbed ground temperature object using the Xing 2014 2 harmonic parameter model.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-location-climate-weather-file-access/#sitegroundtemperatureundisturbedxing
        """

class AnySiteGroundDomainBasement:
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

class WindowMaterialBlind:
    def __call__(
        self,
        name: str,
        /,
        *,
        slat_width: float,
        slat_separation: float,
        front_side_slat_beam_solar_reflectance: float,
        back_side_slat_beam_solar_reflectance: float,
        front_side_slat_diffuse_solar_reflectance: float,
        back_side_slat_diffuse_solar_reflectance: float,
        slat_beam_visible_transmittance: float,
        slat_orientation: Literal["", "Horizontal", "Vertical"] | None = "Horizontal",
        slat_thickness: float | None = 0.00025,
        slat_angle: float | None = 45,
        slat_conductivity: float | None = 221,
        slat_beam_solar_transmittance: float | None = 0,
        slat_diffuse_solar_transmittance: float | None = 0,
        front_side_slat_beam_visible_reflectance: float | None = ...,
        back_side_slat_beam_visible_reflectance: float | None = ...,
        slat_diffuse_visible_transmittance: float | None = 0,
        front_side_slat_diffuse_visible_reflectance: float | None = ...,
        back_side_slat_diffuse_visible_reflectance: float | None = ...,
        slat_infrared_hemispherical_transmittance: float | None = 0,
        front_side_slat_infrared_hemispherical_emissivity: float | None = 0.9,
        back_side_slat_infrared_hemispherical_emissivity: float | None = 0.9,
        blind_to_glass_distance: float | None = 0.05,
        blind_top_opening_multiplier: float | None = 0.5,
        blind_bottom_opening_multiplier: float | None = 0,
        blind_left_side_opening_multiplier: float | None = 0.5,
        blind_right_side_opening_multiplier: float | None = 0.5,
        minimum_slat_angle: float | None = 0,
        maximum_slat_angle: float | None = 180,
    ) -> None:
        """Create a new ``WindowMaterial:Blind`` and add it to the document.

        Window blind thermal properties

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-surface-construction-elements/#windowmaterialblind
        """

class SurfacePropertyHeatTransferAlgorithmMultipleSurface:
    def __call__(
        self,
        name: str,
        /,
        *,
        surface_type: Literal[
            "AllExteriorFloors",
            "AllExteriorRoofs",
            "AllExteriorSurfaces",
            "AllExteriorWalls",
            "AllGroundContactSurfaces",
            "AllInteriorCeilings",
            "AllInteriorFloors",
            "AllInteriorSurfaces",
            "AllInteriorWalls",
        ],
        algorithm: Literal[
            "",
            "CombinedHeatAndMoistureFiniteElement",
            "ConductionFiniteDifference",
            "ConductionTransferFunction",
            "MoisturePenetrationDepthConductionTransferFunction",
        ]
        | None = "ConductionTransferFunction",
    ) -> None:
        """Create a new ``SurfaceProperty:HeatTransferAlgorithm:MultipleSurface`` and add it to the document.

        Determines which Heat Balance Algorithm will be used for a group of surface types Allows selectively overriding the global setting in HeatBalanceAlgorithm CTF (Conduction Transfer Functions), EMPD (Effective Moisture Penetration Depth with Conduction Transfer Functions). Advanced/Research Usage: CondFD (Conduction Finite Difference) Advanced/Research Usage: HAMT (Combined Heat And Moisture Finite Element)

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-advanced-surface-concepts/#surfacepropertyheattransferalgorithmmultiplesurface
        """

class SurfacePropertyHeatTransferAlgorithmConstruction:
    def __call__(
        self,
        name: str = "",
        /,
        *,
        construction_name: str,
        algorithm: Literal[
            "",
            "CombinedHeatAndMoistureFiniteElement",
            "ConductionFiniteDifference",
            "ConductionTransferFunction",
            "MoisturePenetrationDepthConductionTransferFunction",
        ]
        | None = "ConductionTransferFunction",
    ) -> None:
        """Create a new ``SurfaceProperty:HeatTransferAlgorithm:Construction`` and add it to the document.

        Determines which Heat Balance Algorithm will be used for surfaces that have a specific type of construction Allows selectively overriding the global setting in HeatBalanceAlgorithm CTF (Conduction Transfer Functions), EMPD (Effective Moisture Penetration Depth with Conduction Transfer Functions). Advanced/Research Usage: CondFD (Conduction Finite Difference) Advanced/Research Usage: HAMT (Combined Heat And Moisture Finite Element)

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-advanced-surface-concepts/#surfacepropertyheattransferalgorithmconstruction
        """

class GroundHeatTransferSlabEquivalentSlab:
    def __call__(
        self,
        /,
        *,
        apratio_the_area_to_perimeter_ratio_for_this_slab: float,
        slabdepth_thickness_of_slab_on_grade: float | None = 0.1,
        clearance_distance_from_edge_of_slab_to_domain_edge: float | None = 15,
        zclearance_distance_from_bottom_of_slab_to_domain_bottom: float | None = 15,
    ) -> None:
        """Create a new ``GroundHeatTransfer:Slab:EquivalentSlab`` and add it to the document.

        Using an equivalent slab allows non-rectangular shapes to be modeled accurately. Object uses the area - perimeter (area/perimeter) ratio to determine the size of an equivalent rectangular slab. EnergyPlus users normally use this option.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-detailed-ground-heat-transfer/#groundheattransferslabequivalentslab
        """

class PeopleInstance:
    def __call__(
        self,
        name: str,
        /,
        *,
        people_definition_name: str,
        zone_or_zonelist_or_space_or_spacelist_name: str,
        number_of_people_schedule_name: str,
        activity_level_schedule_name: str,
        surface_name_angle_factor_list_name: str | None = ...,
        work_efficiency_schedule_name: str | None = ...,
        clothing_insulation_calculation_method: Literal[
            "", "CalculationMethodSchedule", "ClothingInsulationSchedule", "DynamicClothingModelASHRAE55"
        ]
        | None = "ClothingInsulationSchedule",
        clothing_insulation_calculation_method_schedule_name: str | None = ...,
        clothing_insulation_schedule_name: str | None = ...,
        air_velocity_schedule_name: str | None = ...,
        multiplier: float | None = 1,
        ankle_level_air_velocity_schedule_name: str | None = ...,
        cold_stress_temperature_threshold: float | None = 15.56,
        heat_stress_temperature_threshold: float | None = 30,
    ) -> None:
        """Create a new ``People:Instance`` and add it to the document.

        Sets internal gains and contaminant rates for occupants in the zone. The physical characteristics are given by the referenced People:Definition object. If a ZoneList, SpaceList, or a Zone comprised of more than one Space is specified then this definition applies to all applicable spaces, and each instance will be named with the Space Name plus this Object Name.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-internal-gains/#peopleinstance
        """

class ElectricEquipment:
    def __call__(
        self,
        name: str,
        /,
        *,
        zone_or_zonelist_or_space_or_spacelist_name: str,
        schedule_name: str,
        design_level_calculation_method: Literal["", "EquipmentLevel", "Watts/Area", "Watts/Person"]
        | None = "EquipmentLevel",
        design_level: float | None = ...,
        watts_per_floor_area: float | None = ...,
        watts_per_person: float | None = ...,
        fraction_latent: float | None = 0,
        fraction_radiant: float | None = 0,
        fraction_lost: float | None = 0,
        end_use_subcategory: str | None = "General",
    ) -> None:
        """Create a new ``ElectricEquipment`` and add it to the document.

        Sets internal gains for electric equipment in the zone. If a ZoneList, SpaceList, or a Zone comprised of more than one Space is specified then this definition applies to all applicable spaces, and each instance will be named with the Space Name plus this Object Name.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-internal-gains-people-lights-other/#electricequipment
        """

class ZoneVentilationWindandStackOpenArea:
    def __call__(
        self,
        name: str,
        /,
        *,
        zone_or_space_name: str,
        opening_area: float | None = 0,
        opening_area_fraction_schedule_name: str | None = ...,
        opening_effectiveness: float | Literal["", "Autocalculate"] | None = "Autocalculate",
        effective_angle: float | None = 0,
        height_difference: float | None = 0,
        discharge_coefficient_for_opening: float | Literal["", "Autocalculate"] | None = "Autocalculate",
        minimum_indoor_temperature: float | None = -100,
        minimum_indoor_temperature_schedule_name: str | None = ...,
        maximum_indoor_temperature: float | None = 100,
        maximum_indoor_temperature_schedule_name: str | None = ...,
        delta_temperature: float | None = -100,
        delta_temperature_schedule_name: str | None = ...,
        minimum_outdoor_temperature: float | None = -100,
        minimum_outdoor_temperature_schedule_name: str | None = ...,
        maximum_outdoor_temperature: float | None = 100,
        maximum_outdoor_temperature_schedule_name: str | None = ...,
        maximum_wind_speed: float | None = 40,
    ) -> None:
        """Create a new ``ZoneVentilation:WindandStackOpenArea`` and add it to the document.

        This object is specified as natural ventilation driven by wind and stack effect only: Ventilation Wind = Cw * Opening Area * Schedule * WindSpd Ventilation Stack = Cd * Opening Area * Schedule * SQRT(2*g*DH*(|(Tzone-Todb)|/Tzone)) Total Ventilation = SQRT((Ventilation Wind)^2 + (Ventilation Stack)^2) If a Zone comprised of more than one Space is specified then this definition applies to all applicable spaces, and each instance will be named with the Space Name plus this Object Name.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-airflow/#zoneventilationwindandstackopenarea
        """

class ZoneMixing:
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
    ) -> None:
        """Create a new ``ZoneMixing`` and add it to the document.

        ZoneMixing is a simple air exchange from one zone or space to another. Note that this statement only affects the energy balance of the 'receiving' zone or space and will not produce any effect on the 'source' zone. Mixing statements can be complementary and include multiple zones, but the balancing of flows between zones is left to the user's discretion.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-airflow/#zonemixing
        """

class ZoneRefrigerationDoorMixing:
    def __call__(
        self,
        name: str,
        /,
        *,
        zone_or_space_name_1: str,
        zone_or_space_name_2: str,
        schedule_name: str,
        door_height: float | None = 3,
        door_area: float | None = 9,
        door_protection_type: Literal["", "AirCurtain", "None", "StripCurtain"] | None = "None",
    ) -> None:
        """Create a new ``ZoneRefrigerationDoorMixing`` and add it to the document.

        Refrigeration Door Mixing is used for an opening between two zones (or spaces) that are at the same elevation but have different air temperatures. In this case, the mixing air flow between the two zones is determined by the density difference between the two zones. This would typically be used between two zones in a refrigerated warehouse that are controlled at different temperatures. It could also be used to model a door to a walk-in refrigerated space if that space were modeled as a zone instead of using the object Refrigeration:WalkIn.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-airflow/#zonerefrigerationdoormixing
        """

class AirflowNetworkMultiZoneComponentSimpleOpening:
    def __call__(
        self,
        name: str,
        /,
        *,
        air_mass_flow_coefficient_when_opening_is_closed: float,
        minimum_density_difference_for_two_way_flow: float,
        discharge_coefficient: float,
        air_mass_flow_exponent_when_opening_is_closed: float | None = 0.65,
    ) -> None:
        """Create a new ``AirflowNetwork:MultiZone:Component:SimpleOpening`` and add it to the document.

        This object specifies the properties of air flow through windows and doors (window, door and glass door heat transfer subsurfaces) when they are closed or open.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-airflow-network/#airflownetworkmultizonecomponentsimpleopening
        """

class HVACTemplatePlantTowerObjectReference:
    def __call__(
        self,
        name: str,
        /,
        *,
        cooling_tower_name: str,
        cooling_tower_object_type: Literal[
            "", "CoolingTower:SingleSpeed", "CoolingTower:TwoSpeed", "CoolingTower:VariableSpeed"
        ]
        | None = "CoolingTower:SingleSpeed",
        priority: float | None = ...,
        template_plant_loop_type: Literal["ChilledWater", "MixedWater"] | None = ...,
    ) -> None:
        """Create a new ``HVACTemplate:Plant:Tower:ObjectReference`` and add it to the document.

        This object references a detailed cooling tower object and adds it to an HVACTemplate:Plant:ChilledWaterLoop or MixedWaterLoop. The user must create a complete detailed cooling tower object with all required curve or performance objects.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/hvac-template-objects/group-hvac-templates/#hvactemplateplanttowerobjectreference
        """

class ZoneHVACUnitHeater:
    def __call__(
        self,
        name: str,
        /,
        *,
        supply_air_fan_object_type: Literal["Fan:ConstantVolume", "Fan:OnOff", "Fan:SystemModel", "Fan:VariableVolume"],
        supply_air_fan_name: str,
        maximum_supply_air_flow_rate: float | Literal["Autosize"],
        heating_coil_object_type: Literal[
            "Coil:Heating:Electric", "Coil:Heating:Fuel", "Coil:Heating:Steam", "Coil:Heating:Water"
        ],
        heating_coil_name: str,
        supply_air_fan_operation_during_no_heating: Literal["No", "Yes"],
        availability_schedule_name: str | None = ...,
        air_inlet_node_name: str | None = ...,
        air_outlet_node_name: str | None = ...,
        supply_air_fan_operating_mode_schedule_name: str | None = ...,
        maximum_hot_water_or_steam_flow_rate: float | Literal["Autosize"] | None = ...,
        minimum_hot_water_or_steam_flow_rate: float | None = 0,
        heating_convergence_tolerance: float | None = 0.001,
        availability_manager_list_name: str | None = ...,
        design_specification_zonehvac_sizing_object_name: str | None = ...,
    ) -> None:
        """Create a new ``ZoneHVAC:UnitHeater`` and add it to the document.

        Unit heater. Forced-convection heating-only unit with supply fan, heating coil (gas, electric, hot water, or steam) and fixed-position outdoor air mixer.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-zone-forced-air-units/#zonehvacunitheater
        """

class AnyZoneHVACEvaporativeCoolerUnit:
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
    ) -> None:
        """Create a new ``ZoneHVAC:EvaporativeCoolerUnit`` and add it to the document.

        Zone evaporative cooler. Forced-convection cooling-only unit with supply fan, 100% outdoor air supply. Optional relief exhaust node

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-zone-forced-air-units/#zonehvacevaporativecoolerunit
        """

class AirTerminalSingleDuctConstantVolumeFourPipeInduction:
    def __call__(
        self,
        name: str,
        /,
        *,
        maximum_total_air_flow_rate: float | Literal["Autosize"],
        supply_air_inlet_node_name: str,
        induced_air_inlet_node_name: str,
        air_outlet_node_name: str,
        heating_coil_object_type: Literal["Coil:Heating:Water"],
        heating_coil_name: str,
        zone_mixer_name: str,
        availability_schedule_name: str | None = ...,
        induction_ratio: float | None = 2.5,
        maximum_hot_water_flow_rate: float | Literal["Autosize"] | None = ...,
        minimum_hot_water_flow_rate: float | None = 0,
        heating_convergence_tolerance: float | None = 0.001,
        cooling_coil_object_type: Literal["Coil:Cooling:Water", "Coil:Cooling:Water:DetailedGeometry"] | None = ...,
        cooling_coil_name: str | None = ...,
        maximum_cold_water_flow_rate: float | Literal["Autosize"] | None = ...,
        minimum_cold_water_flow_rate: float | None = 0,
        cooling_convergence_tolerance: float | None = 0.001,
    ) -> None:
        """Create a new ``AirTerminal:SingleDuct:ConstantVolume:FourPipeInduction`` and add it to the document.

        Central air system terminal unit, single duct, variable volume, induction unit with hot water reheat coil and chilled water recool coil.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-air-distribution-equipment/#airterminalsingleductconstantvolumefourpipeinduction
        """

class AnyCoilWaterHeatingAirToWaterHeatPumpWrapped:
    def __call__(
        self,
        name: str,
        /,
        *,
        rated_heating_capacity: float,
        evaporator_air_inlet_node_name: str,
        evaporator_air_outlet_node_name: str,
        rated_cop: float | None = 3.2,
        rated_sensible_heat_ratio: float | None = 0.85,
        rated_evaporator_inlet_air_dry_bulb_temperature: float | None = 19.7,
        rated_evaporator_inlet_air_wet_bulb_temperature: float | None = 13.5,
        rated_condenser_water_temperature: float | None = 57.5,
        rated_evaporator_air_flow_rate: float | Literal["Autocalculate"] | None = ...,
        evaporator_fan_power_included_in_rated_cop: Literal["", "No", "Yes"] | None = "Yes",
        crankcase_heater_capacity: float | None = 0,
        maximum_ambient_temperature_for_crankcase_heater_operation: float | None = 10,
        evaporator_air_temperature_type_for_curve_objects: Literal["", "DryBulbTemperature", "WetBulbTemperature"]
        | None = "WetBulbTemperature",
        heating_capacity_function_of_temperature_curve_name: str | None = ...,
        heating_capacity_function_of_air_flow_fraction_curve_name: str | None = ...,
        heating_cop_function_of_temperature_curve_name: str | None = ...,
        heating_cop_function_of_air_flow_fraction_curve_name: str | None = ...,
        part_load_fraction_correlation_curve_name: str | None = ...,
    ) -> None:
        """Create a new ``Coil:WaterHeating:AirToWaterHeatPump:Wrapped`` and add it to the document.

        Heat pump water heater (HPWH) heating coil, air-to-water direct-expansion (DX) system which includes a water heating coil, evaporator air coil, evaporator fan, electric compressor, and water pump. Part of a WaterHeater:HeatPump:WrappedCondenser system.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-heating-and-cooling-coils/#coilwaterheatingairtowaterheatpumpwrapped
        """

class CoilSystemCoolingDX:
    def __call__(
        self,
        name: str,
        /,
        *,
        dx_cooling_coil_system_inlet_node_name: str,
        dx_cooling_coil_system_outlet_node_name: str,
        dx_cooling_coil_system_sensor_node_name: str,
        cooling_coil_object_type: Literal[
            "Coil:Cooling:DX",
            "Coil:Cooling:DX:SingleSpeed",
            "Coil:Cooling:DX:SingleSpeed:ThermalStorage",
            "Coil:Cooling:DX:TwoSpeed",
            "Coil:Cooling:DX:TwoStageWithHumidityControlMode",
            "Coil:Cooling:DX:VariableSpeed",
            "CoilSystem:Cooling:DX:HeatExchangerAssisted",
        ],
        cooling_coil_name: str,
        availability_schedule_name: str | None = ...,
        dehumidification_control_type: Literal["", "CoolReheat", "Multimode", "None"] | None = "None",
        run_on_sensible_load: Literal["", "No", "Yes"] | None = "Yes",
        run_on_latent_load: Literal["", "No", "Yes"] | None = "No",
        use_outdoor_air_dx_cooling_coil: Literal["", "No", "Yes"] | None = "No",
        outdoor_air_dx_cooling_coil_leaving_minimum_air_temperature: float | None = 2,
    ) -> None:
        """Create a new ``CoilSystem:Cooling:DX`` and add it to the document.

        Virtual container component that consists of a DX cooling coil and its associated controls. This control object supports several different types of DX cooling coils and may be placed directly in an air loop branch or outdoor air equipment list.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-heating-and-cooling-coils/#coilsystemcoolingdx
        """

class CoilCoolingDXSingleSpeedThermalStorage:
    def __call__(
        self,
        name: str,
        /,
        *,
        operating_mode_control_method: Literal["EMSControlled", "ScheduledModes"],
        storage_type: Literal["Ice", "UserDefinedFluidType", "Water"],
        storage_tank_ambient_temperature_node_name: str,
        storage_tank_to_ambient_u_value_times_area_heat_transfer_coefficient: float,
        rated_evaporator_air_flow_rate: float | Literal["Autosize"],
        evaporator_air_inlet_node_name: str,
        evaporator_air_outlet_node_name: str,
        cooling_only_mode_available: Literal["No", "Yes"],
        cooling_and_charge_mode_available: Literal["No", "Yes"],
        cooling_and_discharge_mode_available: Literal["No", "Yes"],
        charge_only_mode_available: Literal["No", "Yes"],
        discharge_only_mode_available: Literal["No", "Yes"],
        condenser_air_inlet_node_name: str,
        condenser_air_outlet_node_name: str,
        condenser_design_air_flow_rate: float | Literal["Autocalculate"],
        availability_schedule_name: str | None = ...,
        operation_mode_control_schedule_name: str | None = ...,
        user_defined_fluid_type: str | None = ...,
        fluid_storage_volume: float | Literal["Autocalculate"] | None = ...,
        ice_storage_capacity: float | Literal["Autocalculate"] | None = ...,
        storage_capacity_sizing_factor: float | None = ...,
        fluid_storage_tank_rating_temperature: float | None = ...,
        cooling_only_mode_rated_total_evaporator_cooling_capacity: float | Literal["Autosize"] | None = ...,
        cooling_only_mode_rated_sensible_heat_ratio: float | None = 0.7,
        cooling_only_mode_rated_cop: float | None = 3,
        cooling_only_mode_total_evaporator_cooling_capacity_function_of_temperature_curve_name: str | None = ...,
        cooling_only_mode_total_evaporator_cooling_capacity_function_of_flow_fraction_curve_name: str | None = ...,
        cooling_only_mode_energy_input_ratio_function_of_temperature_curve_name: str | None = ...,
        cooling_only_mode_energy_input_ratio_function_of_flow_fraction_curve_name: str | None = ...,
        cooling_only_mode_part_load_fraction_correlation_curve_name: str | None = ...,
        cooling_only_mode_sensible_heat_ratio_function_of_temperature_curve_name: str | None = ...,
        cooling_only_mode_sensible_heat_ratio_function_of_flow_fraction_curve_name: str | None = ...,
        cooling_and_charge_mode_rated_total_evaporator_cooling_capacity: float | Literal["Autocalculate"] | None = ...,
        cooling_and_charge_mode_capacity_sizing_factor: float | None = 0.5,
        cooling_and_charge_mode_rated_storage_charging_capacity: float | Literal["Autocalculate"] | None = ...,
        cooling_and_charge_mode_storage_capacity_sizing_factor: float | None = 0.5,
        cooling_and_charge_mode_rated_sensible_heat_ratio: float | None = 0.7,
        cooling_and_charge_mode_cooling_rated_cop: float | None = 3,
        cooling_and_charge_mode_charging_rated_cop: float | None = 3,
        cooling_and_charge_mode_total_evaporator_cooling_capacity_function_of_temperature_curve_name: str | None = ...,
        cooling_and_charge_mode_total_evaporator_cooling_capacity_function_of_flow_fraction_curve_name: str
        | None = ...,
        cooling_and_charge_mode_evaporator_energy_input_ratio_function_of_temperature_curve_name: str | None = ...,
        cooling_and_charge_mode_evaporator_energy_input_ratio_function_of_flow_fraction_curve_name: str | None = ...,
        cooling_and_charge_mode_evaporator_part_load_fraction_correlation_curve_name: str | None = ...,
        cooling_and_charge_mode_storage_charge_capacity_function_of_temperature_curve_name: str | None = ...,
        cooling_and_charge_mode_storage_charge_capacity_function_of_total_evaporator_plr_curve_name: str | None = ...,
        cooling_and_charge_mode_storage_energy_input_ratio_function_of_temperature_curve_name: str | None = ...,
        cooling_and_charge_mode_storage_energy_input_ratio_function_of_flow_fraction_curve_name: str | None = ...,
        cooling_and_charge_mode_storage_energy_part_load_fraction_correlation_curve_name: str | None = ...,
        cooling_and_charge_mode_sensible_heat_ratio_function_of_temperature_curve_name: str | None = ...,
        cooling_and_charge_mode_sensible_heat_ratio_function_of_flow_fraction_curve_name: str | None = ...,
        cooling_and_discharge_mode_rated_total_evaporator_cooling_capacity: float
        | Literal["Autocalculate"]
        | None = ...,
        cooling_and_discharge_mode_evaporator_capacity_sizing_factor: float | None = 1,
        cooling_and_discharge_mode_rated_storage_discharging_capacity: float | Literal["Autocalculate"] | None = ...,
        cooling_and_discharge_mode_storage_discharge_capacity_sizing_factor: float | None = 1,
        cooling_and_discharge_mode_rated_sensible_heat_ratio: float | None = 0.7,
        cooling_and_discharge_mode_cooling_rated_cop: float | None = 3,
        cooling_and_discharge_mode_discharging_rated_cop: float | None = 3,
        cooling_and_discharge_mode_total_evaporator_cooling_capacity_function_of_temperature_curve_name: str
        | None = ...,
        cooling_and_discharge_mode_total_evaporator_cooling_capacity_function_of_flow_fraction_curve_name: str
        | None = ...,
        cooling_and_discharge_mode_evaporator_energy_input_ratio_function_of_temperature_curve_name: str | None = ...,
        cooling_and_discharge_mode_evaporator_energy_input_ratio_function_of_flow_fraction_curve_name: str | None = ...,
        cooling_and_discharge_mode_evaporator_part_load_fraction_correlation_curve_name: str | None = ...,
        cooling_and_discharge_mode_storage_discharge_capacity_function_of_temperature_curve_name: str | None = ...,
        cooling_and_discharge_mode_storage_discharge_capacity_function_of_flow_fraction_curve_name: str | None = ...,
        cooling_and_discharge_mode_storage_discharge_capacity_function_of_total_evaporator_plr_curve_name: str
        | None = ...,
        cooling_and_discharge_mode_storage_energy_input_ratio_function_of_temperature_curve_name: str | None = ...,
        cooling_and_discharge_mode_storage_energy_input_ratio_function_of_flow_fraction_curve_name: str | None = ...,
        cooling_and_discharge_mode_storage_energy_part_load_fraction_correlation_curve_name: str | None = ...,
        cooling_and_discharge_mode_sensible_heat_ratio_function_of_temperature_curve_name: str | None = ...,
        cooling_and_discharge_mode_sensible_heat_ratio_function_of_flow_fraction_curve_name: str | None = ...,
        charge_only_mode_rated_storage_charging_capacity: float | Literal["Autocalculate"] | None = ...,
        charge_only_mode_capacity_sizing_factor: float | None = 1,
        charge_only_mode_charging_rated_cop: float | None = 3,
        charge_only_mode_storage_charge_capacity_function_of_temperature_curve_name: str | None = ...,
        charge_only_mode_storage_energy_input_ratio_function_of_temperature_curve_name: str | None = ...,
        discharge_only_mode_rated_storage_discharging_capacity: float | Literal["Autocalculate"] | None = ...,
        discharge_only_mode_capacity_sizing_factor: float | None = 1,
        discharge_only_mode_rated_sensible_heat_ratio: float | None = ...,
        discharge_only_mode_rated_cop: float | None = 3,
        discharge_only_mode_storage_discharge_capacity_function_of_temperature_curve_name: str | None = ...,
        discharge_only_mode_storage_discharge_capacity_function_of_flow_fraction_curve_name: str | None = ...,
        discharge_only_mode_energy_input_ratio_function_of_temperature_curve_name: str | None = ...,
        discharge_only_mode_energy_input_ratio_function_of_flow_fraction_curve_name: str | None = ...,
        discharge_only_mode_part_load_fraction_correlation_curve_name: str | None = ...,
        discharge_only_mode_sensible_heat_ratio_function_of_temperature_curve_name: str | None = ...,
        discharge_only_mode_sensible_heat_ratio_function_of_flow_fraction_curve_name: str | None = ...,
        ancillary_electric_power: float | None = ...,
        cold_weather_operation_minimum_outdoor_air_temperature: float | None = ...,
        cold_weather_operation_ancillary_power: float | None = ...,
        condenser_air_flow_sizing_factor: float | None = 1,
        condenser_type: Literal["", "AirCooled", "EvaporativelyCooled"] | None = "AirCooled",
        evaporative_condenser_effectiveness: float | None = 0.7,
        evaporative_condenser_pump_rated_power_consumption: float | Literal["", "Autosize"] | None = 0,
        basin_heater_capacity: float | None = 0,
        basin_heater_setpoint_temperature: float | None = 2,
        basin_heater_availability_schedule_name: str | None = ...,
        supply_water_storage_tank_name: str | None = ...,
        condensate_collection_water_storage_tank_name: str | None = ...,
        storage_tank_plant_connection_inlet_node_name: str | None = ...,
        storage_tank_plant_connection_outlet_node_name: str | None = ...,
        storage_tank_plant_connection_design_flow_rate: float | None = ...,
        storage_tank_plant_connection_heat_transfer_effectiveness: float | None = 0.7,
        storage_tank_minimum_operating_limit_fluid_temperature: float | None = ...,
        storage_tank_maximum_operating_limit_fluid_temperature: float | None = ...,
    ) -> None:
        """Create a new ``Coil:Cooling:DX:SingleSpeed:ThermalStorage`` and add it to the document.

        Direct expansion (DX) cooling coil and condensing unit (includes electric compressor and condenser fan), single-speed with packaged integrated thermal storage for cooling.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-heating-and-cooling-coils/#coilcoolingdxsinglespeedthermalstorage
        """

class ControllerMechanicalVentilation:
    def __call__(
        self,
        name: str,
        /,
        *,
        availability_schedule_name: str | None = ...,
        demand_controlled_ventilation: Literal["", "No", "Yes"] | None = "No",
        system_outdoor_air_method: Literal[
            "",
            "IndoorAirQualityProcedure",
            "IndoorAirQualityProcedureCombined",
            "IndoorAirQualityProcedureGenericContaminant",
            "ProportionalControlBasedOnDesignOARate",
            "ProportionalControlBasedOnDesignOccupancy",
            "ProportionalControlBasedOnOccupancySchedule",
            "Standard62.1VentilationRateProcedure",
            "Standard62.1VentilationRateProcedureWithLimit",
            "ZoneSum",
        ]
        | None = "Standard62.1VentilationRateProcedure",
        zone_maximum_outdoor_air_fraction: float | None = 1,
        zone_specifications: list[_g.ControllerMechanicalVentilationZoneSpecificationsItem] = ...,
    ) -> None:
        """Create a new ``Controller:MechanicalVentilation`` and add it to the document.

        This object is used in conjunction with Controller:OutdoorAir to specify outdoor ventilation air based on outdoor air specified in the DesignSpecification:OutdoorAir object The Controller:OutdoorAir object is associated with a specific air loop, so the outdoor air flow rates specified in Controller:MechanicalVentilation correspond to the zones attached to that specific air loop. Duplicate groups of Zone name, Design Specification Outdoor Air Object Name, and Design Specification Zone Air Distribution Object Name to increase allowable number of entries

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-controllers/#controllermechanicalventilation
        """

class Branch:
    def __call__(
        self,
        name: str,
        /,
        *,
        pressure_drop_curve_name: str | None = ...,
        components: list[_g.BranchComponentsItem] = ...,
    ) -> None:
        """Create a new ``Branch`` and add it to the document.

        List components on the branch in simulation and connection order Note: this should NOT include splitters or mixers which define endpoints of branches

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-node-branch-management/#branch
        """

class AnySolarCollectorPerformanceIntegralCollectorStorage:
    def __call__(
        self,
        name: str,
        /,
        *,
        ics_collector_type: Literal["", "RectangularTank"] | None = "RectangularTank",
        gross_area: float | None = ...,
        collector_water_volume: float | None = ...,
        bottom_heat_loss_conductance: float | None = 0.4,
        side_heat_loss_conductance: float | None = 0.6,
        aspect_ratio: float | None = 0.8,
        collector_side_height: float | None = 0.2,
        thermal_mass_of_absorber_plate: float | None = 0,
        number_of_covers: int | None = 2,
        cover_spacing: float | None = 0.05,
        refractive_index_of_outer_cover: float | None = 1.526,
        extinction_coefficient_times_thickness_of_outer_cover: float | None = 0.045,
        emissivity_of_outer_cover: float | None = 0.88,
        refractive_index_of_inner_cover: float | None = 1.37,
        extinction_coefficient_times_thickness_of_the_inner_cover: float | None = 0.008,
        emissivity_of_inner_cover: float | None = 0.88,
        absorptance_of_absorber_plate: float | None = 0.96,
        emissivity_of_absorber_plate: float | None = 0.3,
    ) -> None:
        """Create a new ``SolarCollectorPerformance:IntegralCollectorStorage`` and add it to the document.

        Thermal and optical performance parameters for a single glazed solar collector with integral storage unit.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-solar-collectors/#solarcollectorperformanceintegralcollectorstorage
        """

class ChillerElectricASHRAE205:
    def __call__(
        self,
        name: str,
        /,
        *,
        representation_file_name: str,
        ambient_temperature_indicator: Literal["Outdoors", "Schedule", "Zone"],
        chilled_water_inlet_node_name: str,
        chilled_water_outlet_node_name: str,
        performance_interpolation_method: Literal["", "Cubic", "Linear"] | None = "Linear",
        rated_capacity: float | Literal["", "Autosize"] | None = "Autosize",
        sizing_factor: float | None = 1,
        ambient_temperature_schedule_name: str | None = ...,
        ambient_temperature_zone_name: str | None = ...,
        ambient_temperature_outdoor_air_node_name: str | None = ...,
        chilled_water_maximum_requested_flow_rate: float | Literal["", "Autosize"] | None = "Autosize",
        condenser_inlet_node_name: str | None = ...,
        condenser_outlet_node_name: str | None = ...,
        condenser_maximum_requested_flow_rate: float | Literal["", "Autosize"] | None = "Autosize",
        chiller_flow_mode: Literal["", "ConstantFlow", "LeavingSetpointModulated", "NotModulated"]
        | None = "NotModulated",
        oil_cooler_inlet_node_name: str | None = ...,
        oil_cooler_outlet_node_name: str | None = ...,
        oil_cooler_design_flow_rate: float | None = ...,
        auxiliary_inlet_node_name: str | None = ...,
        auxiliary_outlet_node_name: str | None = ...,
        auxiliary_cooling_design_flow_rate: float | None = ...,
        heat_recovery_inlet_node_name: str | None = ...,
        heat_recovery_outlet_node_name: str | None = ...,
        end_use_subcategory: str | None = "General",
    ) -> None:
        """Create a new ``Chiller:Electric:ASHRAE205`` and add it to the document.

        This chiller model utilizes ASHRAE Standard 205 compliant representations for chillers (Representation Specification RS0001).

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-plant-equipment/#chillerelectricashrae205
        """

class HeatPumpWaterToWaterEquationFitHeating:
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
        reference_heating_capacity: float | Literal["Autosize"],
        reference_heating_power_consumption: float | Literal["Autosize"],
        heating_capacity_curve_name: str,
        heating_compressor_power_curve_name: str,
        reference_coefficient_of_performance: float | None = 7.5,
        sizing_factor: float | None = 1,
        companion_cooling_heat_pump_name: str | None = ...,
    ) -> None:
        """Create a new ``HeatPump:WaterToWater:EquationFit:Heating`` and add it to the document.

        simple water-water hp curve-fit model

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-plant-equipment/#heatpumpwatertowaterequationfitheating
        """

class DistrictHeatingWater:
    def __call__(
        self,
        name: str,
        /,
        *,
        hot_water_inlet_node_name: str,
        hot_water_outlet_node_name: str,
        nominal_capacity: float | Literal["Autosize"] | None = ...,
        capacity_fraction_schedule_name: str | None = ...,
    ) -> None:
        """Create a new ``DistrictHeating:Water`` and add it to the document.

        Centralized source of hot water, such as a district heating system.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-plant-equipment/#districtheatingwater
        """

class CoolingTowerPerformanceYorkCalc:
    def __call__(
        self,
        name: str,
        /,
        *,
        minimum_inlet_air_wet_bulb_temperature: float,
        maximum_inlet_air_wet_bulb_temperature: float,
        minimum_range_temperature: float,
        maximum_range_temperature: float,
        minimum_approach_temperature: float,
        maximum_approach_temperature: float,
        minimum_water_flow_rate_ratio: float,
        maximum_water_flow_rate_ratio: float,
        maximum_liquid_to_gas_ratio: float,
        coefficient_1: float,
        coefficient_2: float,
        coefficient_3: float,
        coefficient_4: float,
        coefficient_5: float,
        coefficient_6: float,
        coefficient_7: float,
        coefficient_8: float,
        coefficient_9: float,
        coefficient_10: float,
        coefficient_11: float,
        coefficient_12: float,
        coefficient_13: float,
        coefficient_14: float,
        coefficient_15: float,
        coefficient_16: float,
        coefficient_17: float,
        coefficient_18: float,
        coefficient_19: float,
        coefficient_20: float,
        coefficient_21: float,
        coefficient_22: float,
        coefficient_23: float,
        coefficient_24: float,
        coefficient_25: float,
        coefficient_26: float,
        coefficient_27: float,
    ) -> None:
        """Create a new ``CoolingTowerPerformance:YorkCalc`` and add it to the document.

        This object is used to define coefficients for the approach temperature correlation for a variable speed cooling tower when tower Model Type is specified as YorkCalcUserDefined in the object CoolingTower:VariableSpeed.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-condenser-equipment/#coolingtowerperformanceyorkcalc
        """

class EvaporativeFluidCoolerSingleSpeed:
    def __call__(
        self,
        name: str,
        /,
        *,
        water_inlet_node_name: str,
        water_outlet_node_name: str,
        design_air_flow_rate: float | Literal["Autosize"],
        design_air_flow_rate_fan_power: float | Literal["Autosize"],
        design_spray_water_flow_rate: float,
        performance_input_method: Literal[
            "StandardDesignCapacity", "UFactorTimesAreaAndDesignWaterFlowRate", "UserSpecifiedDesignCapacity"
        ],
        outdoor_air_inlet_node_name: str | None = ...,
        heat_rejection_capacity_and_nominal_capacity_sizing_ratio: float | None = 1.25,
        standard_design_capacity: float | None = ...,
        design_air_flow_rate_u_factor_times_area_value: float | Literal["Autosize"] | None = ...,
        design_water_flow_rate: float | Literal["Autosize"] | None = ...,
        user_specified_design_capacity: float | None = ...,
        design_entering_water_temperature: float | Literal["", "Autosize"] | None = "Autosize",
        design_entering_air_temperature: float | None = 35,
        design_entering_air_wet_bulb_temperature: float | None = 25.6,
        capacity_control: Literal["", "FanCycling", "FluidBypass"] | None = "FanCycling",
        sizing_factor: float | None = 1,
        evaporation_loss_mode: Literal["", "LossFactor", "SaturatedExit"] | None = "SaturatedExit",
        evaporation_loss_factor: float | None = ...,
        drift_loss_percent: float | None = 0.008,
        blowdown_calculation_mode: Literal["", "ConcentrationRatio", "ScheduledRate"] | None = "ConcentrationRatio",
        blowdown_concentration_ratio: float | None = 3,
        blowdown_makeup_water_usage_schedule_name: str | None = ...,
        supply_water_storage_tank_name: str | None = ...,
    ) -> None:
        """Create a new ``EvaporativeFluidCooler:SingleSpeed`` and add it to the document.

        This model is based on Merkel's theory, which is also the basis for the cooling tower model in EnergyPlus. The Evaporative fluid cooler is modeled as a counter flow heat exchanger.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-condenser-equipment/#evaporativefluidcoolersinglespeed
        """

class AnyThermalStorageChilledWaterStratified:
    def __call__(
        self,
        name: str,
        /,
        *,
        tank_volume: float,
        tank_height: float,
        ambient_temperature_indicator: Literal["Outdoors", "Schedule", "Zone"],
        tank_shape: Literal["", "HorizontalCylinder", "Other", "VerticalCylinder"] | None = "VerticalCylinder",
        tank_perimeter: float | None = ...,
        setpoint_temperature_schedule_name: str | None = ...,
        deadband_temperature_difference: float | None = ...,
        temperature_sensor_height: float | None = ...,
        minimum_temperature_limit: float | None = ...,
        nominal_cooling_capacity: float | None = ...,
        ambient_temperature_schedule_name: str | None = ...,
        ambient_temperature_zone_name: str | None = ...,
        ambient_temperature_outdoor_air_node_name: str | None = ...,
        uniform_skin_loss_coefficient_per_unit_area_to_ambient_temperature: float | None = ...,
        use_side_inlet_node_name: str | None = ...,
        use_side_outlet_node_name: str | None = ...,
        use_side_heat_transfer_effectiveness: float | None = 1,
        use_side_availability_schedule_name: str | None = ...,
        use_side_inlet_height: float | Literal["", "Autocalculate"] | None = "Autocalculate",
        use_side_outlet_height: float | None = 0,
        use_side_design_flow_rate: float | Literal["", "Autosize"] | None = "Autosize",
        source_side_inlet_node_name: str | None = ...,
        source_side_outlet_node_name: str | None = ...,
        source_side_heat_transfer_effectiveness: float | None = 1,
        source_side_availability_schedule_name: str | None = ...,
        source_side_inlet_height: float | None = 0,
        source_side_outlet_height: float | Literal["", "Autocalculate"] | None = "Autocalculate",
        source_side_design_flow_rate: float | Literal["", "Autosize"] | None = "Autosize",
        tank_recovery_time: float | None = 4,
        inlet_mode: Literal["", "Fixed", "Seeking"] | None = "Fixed",
        number_of_nodes: int | None = 1,
        additional_destratification_conductivity: float | None = 0,
        node_1_additional_loss_coefficient: float | None = 0,
        node_2_additional_loss_coefficient: float | None = 0,
        node_3_additional_loss_coefficient: float | None = 0,
        node_4_additional_loss_coefficient: float | None = 0,
        node_5_additional_loss_coefficient: float | None = 0,
        node_6_additional_loss_coefficient: float | None = 0,
        node_7_additional_loss_coefficient: float | None = 0,
        node_8_additional_loss_coefficient: float | None = 0,
        node_9_additional_loss_coefficient: float | None = 0,
        node_10_additional_loss_coefficient: float | None = 0,
    ) -> None:
        """Create a new ``ThermalStorage:ChilledWater:Stratified`` and add it to the document.

        Chilled water storage with a stratified, multi-node tank. The chilled water is 'used' by drawing from the 'Use Side' of the water tank. The tank is indirectly charged by circulating cold water through the 'Source Side' of the water tank.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-water-heaters/#thermalstoragechilledwaterstratified
        """

class CondenserEquipmentOperationSchemes:
    def __call__(
        self,
        name: str,
        /,
        *,
        control_scheme_1_object_type: Literal[
            "PlantEquipmentOperation:CoolingLoad",
            "PlantEquipmentOperation:HeatingLoad",
            "PlantEquipmentOperation:OutdoorDewpoint",
            "PlantEquipmentOperation:OutdoorDewpointDifference",
            "PlantEquipmentOperation:OutdoorDryBulb",
            "PlantEquipmentOperation:OutdoorDryBulbDifference",
            "PlantEquipmentOperation:OutdoorRelativeHumidity",
            "PlantEquipmentOperation:OutdoorWetBulb",
            "PlantEquipmentOperation:OutdoorWetBulbDifference",
            "PlantEquipmentOperation:Uncontrolled",
            "PlantEquipmentOperation:UserDefined",
        ],
        control_scheme_1_name: str,
        control_scheme_1_schedule_name: str,
        control_scheme_2_object_type: Literal[
            "PlantEquipmentOperation:CoolingLoad",
            "PlantEquipmentOperation:HeatingLoad",
            "PlantEquipmentOperation:OutdoorDewpoint",
            "PlantEquipmentOperation:OutdoorDewpointDifference",
            "PlantEquipmentOperation:OutdoorDryBulb",
            "PlantEquipmentOperation:OutdoorDryBulbDifference",
            "PlantEquipmentOperation:OutdoorRelativeHumidity",
            "PlantEquipmentOperation:OutdoorWetBulb",
            "PlantEquipmentOperation:OutdoorWetBulbDifference",
            "PlantEquipmentOperation:Uncontrolled",
            "PlantEquipmentOperation:UserDefined",
        ]
        | None = ...,
        control_scheme_2_name: str | None = ...,
        control_scheme_2_schedule_name: str | None = ...,
        control_scheme_3_object_type: Literal[
            "PlantEquipmentOperation:CoolingLoad",
            "PlantEquipmentOperation:HeatingLoad",
            "PlantEquipmentOperation:OutdoorDewpoint",
            "PlantEquipmentOperation:OutdoorDewpointDifference",
            "PlantEquipmentOperation:OutdoorDryBulb",
            "PlantEquipmentOperation:OutdoorDryBulbDifference",
            "PlantEquipmentOperation:OutdoorRelativeHumidity",
            "PlantEquipmentOperation:OutdoorWetBulb",
            "PlantEquipmentOperation:OutdoorWetBulbDifference",
            "PlantEquipmentOperation:Uncontrolled",
            "PlantEquipmentOperation:UserDefined",
        ]
        | None = ...,
        control_scheme_3_name: str | None = ...,
        control_scheme_3_schedule_name: str | None = ...,
        control_scheme_4_object_type: Literal[
            "PlantEquipmentOperation:CoolingLoad",
            "PlantEquipmentOperation:HeatingLoad",
            "PlantEquipmentOperation:OutdoorDewpoint",
            "PlantEquipmentOperation:OutdoorDewpointDifference",
            "PlantEquipmentOperation:OutdoorDryBulb",
            "PlantEquipmentOperation:OutdoorDryBulbDifference",
            "PlantEquipmentOperation:OutdoorRelativeHumidity",
            "PlantEquipmentOperation:OutdoorWetBulb",
            "PlantEquipmentOperation:OutdoorWetBulbDifference",
            "PlantEquipmentOperation:Uncontrolled",
            "PlantEquipmentOperation:UserDefined",
        ]
        | None = ...,
        control_scheme_4_name: str | None = ...,
        control_scheme_4_schedule_name: str | None = ...,
        control_scheme_5_object_type: Literal[
            "PlantEquipmentOperation:CoolingLoad",
            "PlantEquipmentOperation:HeatingLoad",
            "PlantEquipmentOperation:OutdoorDewpoint",
            "PlantEquipmentOperation:OutdoorDewpointDifference",
            "PlantEquipmentOperation:OutdoorDryBulb",
            "PlantEquipmentOperation:OutdoorDryBulbDifference",
            "PlantEquipmentOperation:OutdoorRelativeHumidity",
            "PlantEquipmentOperation:OutdoorWetBulb",
            "PlantEquipmentOperation:OutdoorWetBulbDifference",
            "PlantEquipmentOperation:Uncontrolled",
            "PlantEquipmentOperation:UserDefined",
        ]
        | None = ...,
        control_scheme_5_name: str | None = ...,
        control_scheme_5_schedule_name: str | None = ...,
        control_scheme_6_object_type: Literal[
            "PlantEquipmentOperation:CoolingLoad",
            "PlantEquipmentOperation:HeatingLoad",
            "PlantEquipmentOperation:OutdoorDewpoint",
            "PlantEquipmentOperation:OutdoorDewpointDifference",
            "PlantEquipmentOperation:OutdoorDryBulb",
            "PlantEquipmentOperation:OutdoorDryBulbDifference",
            "PlantEquipmentOperation:OutdoorRelativeHumidity",
            "PlantEquipmentOperation:OutdoorWetBulb",
            "PlantEquipmentOperation:OutdoorWetBulbDifference",
            "PlantEquipmentOperation:Uncontrolled",
            "PlantEquipmentOperation:UserDefined",
        ]
        | None = ...,
        control_scheme_6_name: str | None = ...,
        control_scheme_6_schedule_name: str | None = ...,
        control_scheme_7_object_type: Literal[
            "PlantEquipmentOperation:CoolingLoad",
            "PlantEquipmentOperation:HeatingLoad",
            "PlantEquipmentOperation:OutdoorDewpoint",
            "PlantEquipmentOperation:OutdoorDewpointDifference",
            "PlantEquipmentOperation:OutdoorDryBulb",
            "PlantEquipmentOperation:OutdoorDryBulbDifference",
            "PlantEquipmentOperation:OutdoorRelativeHumidity",
            "PlantEquipmentOperation:OutdoorWetBulb",
            "PlantEquipmentOperation:OutdoorWetBulbDifference",
            "PlantEquipmentOperation:Uncontrolled",
            "PlantEquipmentOperation:UserDefined",
        ]
        | None = ...,
        control_scheme_7_name: str | None = ...,
        control_scheme_7_schedule_name: str | None = ...,
        control_scheme_8_object_type: Literal[
            "PlantEquipmentOperation:CoolingLoad",
            "PlantEquipmentOperation:HeatingLoad",
            "PlantEquipmentOperation:OutdoorDewpoint",
            "PlantEquipmentOperation:OutdoorDewpointDifference",
            "PlantEquipmentOperation:OutdoorDryBulb",
            "PlantEquipmentOperation:OutdoorDryBulbDifference",
            "PlantEquipmentOperation:OutdoorRelativeHumidity",
            "PlantEquipmentOperation:OutdoorWetBulb",
            "PlantEquipmentOperation:OutdoorWetBulbDifference",
            "PlantEquipmentOperation:Uncontrolled",
            "PlantEquipmentOperation:UserDefined",
        ]
        | None = ...,
        control_scheme_8_name: str | None = ...,
        control_scheme_8_schedule_name: str | None = ...,
    ) -> None:
        """Create a new ``CondenserEquipmentOperationSchemes`` and add it to the document.

        Operation schemes are listed in 'priority' order. Note that each scheme must address the entire load and/or condition ranges for the simulation. The actual one selected for use will be the first that is 'Scheduled' on. That is, if control scheme 1 is not 'on' and control scheme 2 is -- then control scheme 2 is selected. Only condenser equipment should be listed on a Control Scheme for this item.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-plant-condenser-control/#condenserequipmentoperationschemes
        """

class PlantComponentUserDefined:
    def __call__(
        self,
        name: str,
        /,
        *,
        number_of_plant_loop_connections: int,
        plant_connection_1_inlet_node_name: str,
        plant_connection_1_outlet_node_name: str,
        plant_connection_1_loading_mode: Literal[
            "DemandsLoad",
            "MeetsLoadWithNominalCapacity",
            "MeetsLoadWithNominalCapacityHiOutLimit",
            "MeetsLoadWithNominalCapacityLowOutLimit",
            "MeetsLoadWithPassiveCapacity",
        ],
        plant_connection_1_loop_flow_request_mode: Literal[
            "NeedsFlowAndTurnsLoopOn", "NeedsFlowIfLoopOn", "ReceivesWhateverFlowAvailable"
        ],
        main_model_program_calling_manager_name: str | None = ...,
        plant_connection_1_initialization_program_calling_manager_name: str | None = ...,
        plant_connection_1_simulation_program_calling_manager_name: str | None = ...,
        plant_connection_2_inlet_node_name: str | None = ...,
        plant_connection_2_outlet_node_name: str | None = ...,
        plant_connection_2_loading_mode: Literal[
            "DemandsLoad",
            "MeetLoadWithNominalCapacity",
            "MeetLoadWithNominalCapacityHiOutLimit",
            "MeetLoadWithNominalCapacityLowOutLimit",
            "MeetLoadWithPassiveCapacity",
        ]
        | None = ...,
        plant_connection_2_loop_flow_request_mode: Literal[
            "NeedsFlowAndTurnsLoopOn", "NeedsFlowIfLoopOn", "ReceivesWhateverFlowAvailable"
        ]
        | None = ...,
        plant_connection_2_initialization_program_calling_manager_name: str | None = ...,
        plant_connection_2_simulation_program_calling_manager_name: str | None = ...,
        plant_connection_3_inlet_node_name: str | None = ...,
        plant_connection_3_outlet_node_name: str | None = ...,
        plant_connection_3_loading_mode: Literal[
            "DemandsLoad",
            "MeetLoadWithNominalCapacity",
            "MeetLoadWithNominalCapacityHiOutLimit",
            "MeetLoadWithNominalCapacityLowOutLimit",
            "MeetLoadWithPassiveCapacity",
        ]
        | None = ...,
        plant_connection_3_loop_flow_request_mode: Literal[
            "NeedsFlowAndTurnsLoopOn", "NeedsFlowIfLoopOn", "ReceivesWhateverFlowAvailable"
        ]
        | None = ...,
        plant_connection_3_initialization_program_calling_manager_name: str | None = ...,
        plant_connection_3_simulation_program_calling_manager_name: str | None = ...,
        plant_connection_4_inlet_node_name: str | None = ...,
        plant_connection_4_outlet_node_name: str | None = ...,
        plant_connection_4_loading_mode: Literal[
            "DemandsLoad",
            "MeetLoadWithNominalCapacity",
            "MeetLoadWithNominalCapacityHiOutLimit",
            "MeetLoadWithNominalCapacityLowOutLimit",
            "MeetLoadWithPassiveCapacity",
        ]
        | None = ...,
        plant_connection_4_loop_flow_request_mode: Literal[
            "NeedsFlowAndTurnsLoopOn", "NeedsFlowIfLoopOn", "ReceivesWhateverFlowAvailable"
        ]
        | None = ...,
        plant_connection_4_initialization_program_calling_manager_name: str | None = ...,
        plant_connection_4_simulation_program_calling_manager_name: str | None = ...,
        air_connection_inlet_node_name: str | None = ...,
        air_connection_outlet_node_name: str | None = ...,
        supply_inlet_water_storage_tank_name: str | None = ...,
        collection_outlet_water_storage_tank_name: str | None = ...,
        ambient_zone_name: str | None = ...,
    ) -> None:
        """Create a new ``PlantComponent:UserDefined`` and add it to the document.

        Defines a generic plant component for custom modeling using Energy Management System or External Interface

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-user-defined-hvac-and-plant-component/#plantcomponentuserdefined
        """

class SetpointManagerWarmest:
    def __call__(
        self,
        name: str,
        /,
        *,
        hvac_air_loop_name: str,
        setpoint_node_or_nodelist_name: str,
        control_variable: Literal["", "Temperature"] | None = "Temperature",
        minimum_setpoint_temperature: float | None = 12,
        maximum_setpoint_temperature: float | None = 18,
        strategy: Literal["", "MaximumTemperature"] | None = "MaximumTemperature",
    ) -> None:
        """Create a new ``SetpointManager:Warmest`` and add it to the document.

        This SetpointManager resets the cooling supply air temperature of a central forced air HVAC system according to the cooling demand of the warmest zone.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-setpoint-managers/#setpointmanagerwarmest
        """

class RefrigerationAirChiller:
    def __call__(
        self,
        name: str,
        /,
        *,
        capacity_rating_type: Literal[
            "CapacityTotalSpecificConditions",
            "EuropeanSC1NominalWet",
            "EuropeanSC1Standard",
            "EuropeanSC2NominalWet",
            "EuropeanSC2Standard",
            "EuropeanSC3NominalWet",
            "EuropeanSC3Standard",
            "EuropeanSC4NominalWet",
            "EuropeanSC4Standard",
            "EuropeanSC5NominalWet",
            "EuropeanSC5Standard",
            "FixedLinear",
            "UnitLoadFactorSensibleOnly",
        ],
        rated_cooling_source_temperature: float,
        rated_temperature_difference_dt1: float,
        rated_total_heating_power: float,
        rated_air_flow: float,
        defrost_schedule_name: str,
        availability_schedule_name: str | None = ...,
        rated_unit_load_factor: float | None = ...,
        rated_capacity: float | None = ...,
        rated_relative_humidity: float | None = 85,
        maximum_temperature_difference_between_inlet_air_and_evaporating_temperature: float | None = ...,
        coil_material_correction_factor: float | None = 1,
        refrigerant_correction_factor: float | None = 1,
        capacity_correction_curve_type: Literal["European", "LinearSHR60", "QuadraticSHR", "TabularRHxDT1xTRoom"]
        | None = ...,
        capacity_correction_curve_name: str | None = ...,
        shr60_correction_factor: float | None = 1.48,
        heating_power_schedule_name: str | None = ...,
        fan_speed_control_type: Literal["", "Fixed", "FixedLinear", "TwoSpeed", "VariableSpeed"] | None = "Fixed",
        rated_fan_power: float | None = 375,
        minimum_fan_air_flow_ratio: float | None = 0.2,
        defrost_type: Literal["", "Electric", "HotFluid", "None", "OffCycle"] | None = "Electric",
        defrost_control_type: Literal["", "TemperatureTermination", "TimeSchedule"] | None = "TimeSchedule",
        defrost_drip_down_schedule_name: str | None = ...,
        defrost_power: float | None = ...,
        temperature_termination_defrost_fraction_to_ice: float | None = ...,
        vertical_location: Literal["", "Ceiling", "Floor", "Middle"] | None = "Middle",
        average_refrigerant_charge_inventory: float | None = 0,
    ) -> None:
        """Create a new ``Refrigeration:AirChiller`` and add it to the document.

        Works in conjunction with a refrigeration chiller set, compressor rack, a refrigeration system, or a refrigeration secondary system to simulate the performance of an air chiller, similar to one found in a refrigerated warehouse. Energy use for fans and heaters is modeled based on inputs for nominal power, schedules, and control type. The air chiller model accounts for the sensible and latent heat exchange with the surrounding environment.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-refrigeration/#refrigerationairchiller
        """

class GeneratorFuelCellPowerModule:
    def __call__(
        self,
        name: str,
        /,
        *,
        efficiency_curve_name: str,
        efficiency_curve_mode: Literal["Annex42", "Normalized"] | None = ...,
        nominal_efficiency: float | None = ...,
        nominal_electrical_power: float | None = ...,
        number_of_stops_at_start_of_simulation: float | None = ...,
        cycling_performance_degradation_coefficient: float | None = ...,
        number_of_run_hours_at_beginning_of_simulation: float | None = ...,
        accumulated_run_time_degradation_coefficient: float | None = ...,
        run_time_degradation_initiation_time_threshold: float | None = ...,
        power_up_transient_limit: float | None = ...,
        power_down_transient_limit: float | None = ...,
        start_up_time: float | None = ...,
        start_up_fuel: float | None = ...,
        start_up_electricity_consumption: float | None = ...,
        start_up_electricity_produced: float | None = ...,
        shut_down_time: float | None = ...,
        shut_down_fuel: float | None = ...,
        shut_down_electricity_consumption: float | None = ...,
        ancillary_electricity_constant_term: float | None = ...,
        ancillary_electricity_linear_term: float | None = ...,
        skin_loss_calculation_mode: Literal["ConstantRate", "QuadraticFunctionOfFuelRate", "UAForProcessGasTemperature"]
        | None = ...,
        zone_name: str | None = ...,
        skin_loss_radiative_fraction: float | None = ...,
        constant_skin_loss_rate: float | None = ...,
        skin_loss_u_factor_times_area_term: float | None = ...,
        skin_loss_quadratic_curve_name: str | None = ...,
        dilution_air_flow_rate: float | None = ...,
        stack_heat_loss_to_dilution_air: float | None = ...,
        dilution_inlet_air_node_name: str | None = ...,
        dilution_outlet_air_node_name: str | None = ...,
        minimum_operating_point: float | None = ...,
        maximum_operating_point: float | None = ...,
    ) -> None:
        """Create a new ``Generator:FuelCell:PowerModule`` and add it to the document.

        Describe the core power module subsystem of a fuel cell power generator. This includes the fuel cell stack, fuel reformer, and whatever ancillary devices are included inside. If the model has multiple FC generators that are of the exact same type, then only one of these objects is needed and all the Generator:FuelCell objects can reference it.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-electric-load-center-generator/#generatorfuelcellpowermodule
        """

class ElectricLoadCenterStorageSimple:
    def __call__(
        self,
        name: str = "",
        /,
        *,
        availability_schedule_name: str | None = ...,
        zone_name: str | None = ...,
        radiative_fraction_for_zone_heat_gains: float | None = ...,
        nominal_energetic_efficiency_for_charging: float | None = ...,
        nominal_discharging_energetic_efficiency: float | None = ...,
        maximum_storage_capacity: float | None = ...,
        maximum_power_for_discharging: float | None = ...,
        maximum_power_for_charging: float | None = ...,
        initial_state_of_charge: float | None = ...,
    ) -> None:
        """Create a new ``ElectricLoadCenter:Storage:Simple`` and add it to the document.

        Used to model storage of electricity in an electric load center. This is a simple model that does not attempt to represent any of the characteristics of a real storage device such as a battery. The type of power, AC or DC, depends on the configuration chosen as the Electrical Buss Type in the ElectricLoadCenter:Distribution object.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-electric-load-center-generator/#electricloadcenterstoragesimple
        """

class AnyElectricLoadCenterStorageBattery:
    def __call__(
        self,
        name: str,
        /,
        *,
        availability_schedule_name: str | None = ...,
        zone_name: str | None = ...,
        radiative_fraction: float | None = 0,
        number_of_battery_modules_in_parallel: int | None = 1,
        number_of_battery_modules_in_series: int | None = 1,
        maximum_module_capacity: float | None = ...,
        initial_fractional_state_of_charge: float | None = 1,
        fraction_of_available_charge_capacity: float | None = ...,
        change_rate_from_bound_charge_to_available_charge: float | None = ...,
        fully_charged_module_open_circuit_voltage: float | None = ...,
        fully_discharged_module_open_circuit_voltage: float | None = ...,
        voltage_change_curve_name_for_charging: str | None = ...,
        voltage_change_curve_name_for_discharging: str | None = ...,
        module_internal_electrical_resistance: float | None = ...,
        maximum_module_discharging_current: float | None = ...,
        module_cut_off_voltage: float | None = ...,
        module_charge_rate_limit: float | None = 1,
        battery_life_calculation: Literal["", "No", "Yes"] | None = "No",
        number_of_cycle_bins: int | None = 10,
        battery_life_curve_name: str | None = ...,
    ) -> None:
        """Create a new ``ElectricLoadCenter:Storage:Battery`` and add it to the document.

        Uses the kinetic battery model (KiBaM) to simulate rechargeable battery banks in an electrical load center. The battery bank is a collection of one or more individual battery modules. Given the surplus or deficit power from the electrical system and the state of charge from the previous time step, this object can model the voltage, current, and energy losses with charging and discharging during each time step. The cumulative battery damage can be also modeled and reported at the end of each simulation run.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-electric-load-center-generator/#electricloadcenterstoragebattery
        """

class ElectricLoadCenterStorageConverter:
    def __call__(
        self,
        name: str = "",
        /,
        *,
        availability_schedule_name: str | None = ...,
        power_conversion_efficiency_method: Literal["", "FunctionOfPower", "SimpleFixed"] | None = "SimpleFixed",
        simple_fixed_efficiency: float | None = 0.95,
        design_maximum_continuous_input_power: float | None = ...,
        efficiency_function_of_power_curve_name: str | None = ...,
        ancillary_power_consumed_in_standby: float | None = ...,
        zone_name: str | None = ...,
        radiative_fraction: float | None = ...,
    ) -> None:
        """Create a new ``ElectricLoadCenter:Storage:Converter`` and add it to the document.

        This model is for converting AC to DC for grid-supplied charging of DC storage

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-electric-load-center-generator/#electricloadcenterstorageconverter
        """

class CurveQuadraticLinear:
    def __call__(
        self,
        name: str,
        /,
        *,
        coefficient1_constant: float,
        coefficient2_x: float,
        coefficient3_x_2: float,
        coefficient4_y: float,
        coefficient5_x_y: float,
        coefficient6_x_2_y: float,
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
    ) -> None:
        """Create a new ``Curve:QuadraticLinear`` and add it to the document.

        Quadratic-linear curve with two independent variables. Input consists of the curve name, the six coefficients, and min and max values for each of the independent variables. Optional inputs for curve minimum and maximum may be used to limit the output of the performance curve. curve = (C1 + C2*x + C3*x**2) + (C4 + C5*x + C6*x**2)*y

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-performance-curves/#curvequadraticlinear
        """

class ComponentCostLineItem:
    def __call__(
        self,
        name: str = "",
        /,
        *,
        line_item_type: Literal[
            "Chiller:Electric",
            "Coil:Cooling:DX",
            "Coil:Cooling:DX:SingleSpeed",
            "Coil:DX",
            "Coil:Heating:Fuel",
            "Construction",
            "Daylighting:Controls",
            "General",
            "Generator:Photovoltaic",
            "Lights",
            "Shading:Zone:Detailed",
        ],
        item_name: str,
        type: str | None = ...,
        object_end_use_key: str | None = ...,
        cost_per_each: float | None = ...,
        cost_per_area: float | None = ...,
        cost_per_unit_of_output_capacity: float | None = ...,
        cost_per_unit_of_output_capacity_per_cop: float | None = ...,
        cost_per_volume: float | None = ...,
        cost_per_volume_rate: float | None = ...,
        cost_per_energy_per_temperature_difference: float | None = ...,
        quantity: float | None = ...,
    ) -> None:
        """Create a new ``ComponentCost:LineItem`` and add it to the document.

        Each instance of this object creates a cost line item and will contribute to the total for a cost estimate.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/energyplus-economics/cost-estimating/#componentcostlineitem
        """

class OutputControlTableStyle:
    def __call__(
        self,
        /,
        *,
        column_separator: Literal[
            "", "All", "Comma", "CommaAndHTML", "CommaAndXML", "Fixed", "HTML", "Tab", "TabAndHTML", "XML", "XMLandHTML"
        ]
        | None = "Comma",
        unit_conversion: Literal["", "InchPound", "InchPoundExceptElectricity", "JtoGJ", "JtoKWH", "JtoMJ", "None"]
        | None = "None",
        format_numeric_values: Literal["", "No", "Yes"] | None = "Yes",
    ) -> None:
        """Create a new ``OutputControl:Table:Style`` and add it to the document.

        default style for the OutputControl:Table:Style is comma -- this works well for importing into spreadsheet programs such as Excel(tm) but not so well for word processing programs -- there tab may be a better choice. fixed puts spaces between the 'columns'. HTML produces tables in HTML. XML produces an XML file. note - if no OutputControl:Table:Style is included, the defaults are comma and None.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/standard-output-reports/outputcontrol-table-style/#outputcontroltablestyle
        """

class OutputSQLite:
    def __call__(
        self,
        /,
        *,
        option_type: Literal["Simple", "SimpleAndTabular"] | None = ...,
        unit_conversion_for_tabular_data: Literal[
            "",
            "InchPound",
            "InchPoundExceptElectricity",
            "JtoGJ",
            "JtoKWH",
            "JtoMJ",
            "None",
            "UseOutputControlTableStyle",
        ]
        | None = "UseOutputControlTableStyle",
        format_numeric_values_for_tabular_data: Literal["", "No", "Yes"] | None = "Yes",
    ) -> None:
        """Create a new ``Output:SQLite`` and add it to the document.

        Output from EnergyPlus can be written to an SQLite format file.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/input-for-output/#outputsqlite
        """

class AnyPythonPluginVariables:
    def __call__(self, name: str, /) -> None:
        """Create a new ``PythonPlugin:Variables`` and add it to the document.

        This object defines name identifiers for custom Python Plugin variable data that should be shared among all running Python Plugins.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-python-plugins/#pythonpluginvariables
        """
