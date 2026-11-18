"""Creation signatures of generated classes (stub only).

DO NOT EDIT — regenerate with:
    python -m idfkit.codegen.generate_stubs
"""

from __future__ import annotations

from typing import Literal

from typing_extensions import Never

from .. import _generated_types as _g

class SiteGroundReflectanceSnowModifier:
    def __call__(
        self,
        /,
        *,
        ground_reflected_solar_modifier: float | None = 1,
        daylighting_ground_reflected_solar_modifier: float | None = 1,
    ) -> None:
        """Create a new ``Site:GroundReflectance:SnowModifier`` and add it to the document.

        Specifies ground reflectance multipliers when snow resident on the ground. These multipliers are applied to the 'normal' ground reflectances specified in Site:GroundReflectance.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-location-climate-weather-file-access/#sitegroundreflectancesnowmodifier
        """

class RoofIrrigation:
    def __call__(
        self,
        /,
        *,
        irrigation_model_type: Literal["Schedule", "SmartSchedule"] | None = ...,
        irrigation_rate_schedule_name: str | None = ...,
        irrigation_maximum_saturation_threshold: float | None = 40,
    ) -> None:
        """Create a new ``RoofIrrigation`` and add it to the document.

        Used to describe the amount of irrigation on the ecoroof surface over the course of the simulation runperiod.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-location-climate-weather-file-access/#roofirrigation
        """

class WindowGapSupportPillar:
    def __call__(self, name: str, /, *, spacing: float | None = 0.04, radius: float | None = 0.0004) -> None:
        """Create a new ``WindowGap:SupportPillar`` and add it to the document.

        used to define pillar geometry for support pillars

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-surface-construction-elements/#windowgapsupportpillar
        """

class AnyMaterialPropertyVariableThermalConductivity:
    def __call__(self, name: str, /, *, narrow_with_as_version_first: Never) -> None:
        """Create a new ``MaterialProperty:VariableThermalConductivity`` and add it to the document.

        Additional properties for temperature dependent thermal conductivity using piecewise linear temperature-conductivity function. Name is followed by up to 100 sets of temperature-conductivity pairs. HeatBalanceAlgorithm = CondFD(ConductionFiniteDifference) solution algorithm only. Has no effect with other HeatBalanceAlgorithm solution algorithms

        No call suits every release: narrow the document with ``as_version`` first.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-surface-construction-elements/#materialpropertyvariablethermalconductivity
        """

class CeilingAdiabatic:
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
    ) -> None:
        """Create a new ``Ceiling:Adiabatic`` and add it to the document.

        Allows for simplified entry of interior ceilings.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-thermal-zone-description-geometry/#ceilingadiabatic
        """

class WindowInterzone:
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
    ) -> None:
        """Create a new ``Window:Interzone`` and add it to the document.

        Allows for simplified entry of interzone windows (adjacent to other zones).

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-thermal-zone-description-geometry/#windowinterzone
        """

class WindowShadingControl:
    def __call__(
        self,
        name: str,
        /,
        *,
        zone_name: str,
        shading_type: Literal[
            "BetweenGlassBlind",
            "BetweenGlassShade",
            "ExteriorBlind",
            "ExteriorScreen",
            "ExteriorShade",
            "InteriorBlind",
            "InteriorShade",
            "SwitchableGlazing",
        ],
        shading_control_type: Literal[
            "AlwaysOff",
            "AlwaysOn",
            "MeetDaylightIlluminanceSetpoint",
            "OffNightAndOnDayIfCoolingAndHighSolarOnWindow",
            "OnIfHighGlare",
            "OnIfHighHorizontalSolar",
            "OnIfHighOutdoorAirTempAndHighHorizontalSolar",
            "OnIfHighOutdoorAirTempAndHighSolarOnWindow",
            "OnIfHighOutdoorAirTemperature",
            "OnIfHighSolarOnWindow",
            "OnIfHighSolarOrHighLuminanceTillMidnight",
            "OnIfHighSolarOrHighLuminanceTillNextMorning",
            "OnIfHighSolarOrHighLuminanceTillSunset",
            "OnIfHighZoneAirTempAndHighHorizontalSolar",
            "OnIfHighZoneAirTempAndHighSolarOnWindow",
            "OnIfHighZoneAirTemperature",
            "OnIfHighZoneCooling",
            "OnIfScheduleAllows",
            "OnNightAndOnDayIfCoolingAndHighSolarOnWindow",
            "OnNightIfHeatingAndOffDay",
            "OnNightIfHeatingAndOnDayIfCooling",
            "OnNightIfLowInsideTempAndOffDay",
            "OnNightIfLowOutdoorTempAndOffDay",
            "OnNightIfLowOutdoorTempAndOnDayIfCooling",
        ],
        shading_control_sequence_number: int | None = 1,
        construction_with_shading_name: str | None = ...,
        schedule_name: str | None = ...,
        setpoint: float | None = ...,
        shading_control_is_scheduled: Literal["", "No", "Yes"] | None = "No",
        glare_control_is_active: Literal["", "No", "Yes"] | None = "No",
        shading_device_material_name: str | None = ...,
        type_of_slat_angle_control_for_blinds: Literal["", "BlockBeamSolar", "FixedSlatAngle", "ScheduledSlatAngle"]
        | None = "FixedSlatAngle",
        slat_angle_schedule_name: str | None = ...,
        setpoint_2: float | None = ...,
        daylighting_control_object_name: str | None = ...,
        multiple_surface_control_type: Literal["", "Group", "Sequential"] | None = "Sequential",
        fenestration_surfaces: list[_g.WindowShadingControlFenestrationSurfacesItem] = ...,
    ) -> None:
        """Create a new ``WindowShadingControl`` and add it to the document.

        Specifies the type, location, and controls for window shades, window blinds, and switchable glazing. Referencing the surface objects for exterior windows and glass doors (ref: FenestrationSurface:Detailed, Window, and GlazedDoor).

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-thermal-zone-description-geometry/#windowshadingcontrol
        """

class SurfacePropertyHeatTransferAlgorithm:
    def __call__(
        self,
        /,
        *,
        surface_name: str,
        algorithm: Literal[
            "",
            "CombinedHeatAndMoistureFiniteElement",
            "ConductionFiniteDifference",
            "ConductionTransferFunction",
            "MoisturePenetrationDepthConductionTransferFunction",
        ]
        | None = "ConductionTransferFunction",
    ) -> None:
        """Create a new ``SurfaceProperty:HeatTransferAlgorithm`` and add it to the document.

        Determines which Heat Balance Algorithm will be used for a specific surface Allows selectively overriding the global setting in HeatBalanceAlgorithm CTF (Conduction Transfer Functions), EMPD (Effective Moisture Penetration Depth with Conduction Transfer Functions). Advanced/Research Usage: CondFD (Conduction Finite Difference) Advanced/Research Usage: HAMT (Combined Heat And Moisture Finite Element)

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-advanced-surface-concepts/#surfacepropertyheattransferalgorithm
        """

class SurfacePropertyConvectionCoefficients:
    def __call__(
        self,
        /,
        *,
        surface_name: str,
        convection_coefficient_1_location: Literal["Inside", "Outside"],
        convection_coefficient_1_type: Literal[
            "ASHRAEVerticalWall",
            "ASTMC1340",
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
            "ASTMC1340",
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
    ) -> None:
        """Create a new ``SurfaceProperty:ConvectionCoefficients`` and add it to the document.

        Allow user settable interior and/or exterior convection coefficients. Note that some other factors may limit the lower bounds for these values, such as for windows, the interior convection coefficient must be >.28, for trombe wall algorithm selection (zone), the interior convection coefficient must be >.1 for TARP interior convection, the lower limit is also .1 Minimum and maximum limits are set in HeatBalanceAlgorithm object. Defaults in HeatBalanceAlgorithm object are [.1,1000].

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-advanced-surface-concepts/#surfacepropertyconvectioncoefficients
        """

class SurfacePropertiesVaporCoefficients:
    def __call__(
        self,
        /,
        *,
        surface_name: str,
        constant_external_vapor_transfer_coefficient: Literal["", "No", "Yes"] | None = "No",
        external_vapor_coefficient_value: float | None = 0,
        constant_internal_vapor_transfer_coefficient: Literal["", "No", "Yes"] | None = "No",
        internal_vapor_coefficient_value: float | None = 0,
    ) -> None:
        """Create a new ``SurfaceProperties:VaporCoefficients`` and add it to the document.

        The interior and external vapor transfer coefficients. Normally these value are calculated using the heat convection coefficient values. Use this object to used fixed constant values. Units are kg/Pa.s.m2 This will only work with the CombinedHeatAndMoistureFiniteElement algorithm for surfaces. Other algorithms will ignore these coefficients

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-advanced-surface-concepts/#surfacepropertiesvaporcoefficients
        """

class SurfacePropertyIncidentSolarMultiplier:
    def __call__(
        self,
        /,
        *,
        surface_name: str,
        incident_solar_multiplier: float | None = 1,
        incident_solar_multiplier_schedule_name: str | None = ...,
    ) -> None:
        """Create a new ``SurfaceProperty:IncidentSolarMultiplier`` and add it to the document.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-advanced-surface-concepts/#surfacepropertyincidentsolarmultiplier
        """

class People:
    def __call__(
        self,
        name: str,
        /,
        *,
        zone_or_zonelist_or_space_or_spacelist_name: str,
        number_of_people_schedule_name: str,
        activity_level_schedule_name: str,
        number_of_people_calculation_method: Literal["", "Area/Person", "People", "People/Area"] | None = "People",
        number_of_people: float | None = ...,
        people_per_floor_area: float | None = ...,
        floor_area_per_person: float | None = ...,
        fraction_radiant: float | None = 0.3,
        sensible_heat_fraction: float | Literal["", "Autocalculate"] | None = "Autocalculate",
        carbon_dioxide_generation_rate: float | None = ...,
        enable_ashrae_55_comfort_warnings: Literal["", "No", "Yes"] | None = "No",
        mean_radiant_temperature_calculation_type: Literal["", "AngleFactor", "EnclosureAveraged", "SurfaceWeighted"]
        | None = "EnclosureAveraged",
        surface_name_angle_factor_list_name: str | None = ...,
        work_efficiency_schedule_name: str | None = ...,
        clothing_insulation_calculation_method: Literal[
            "", "CalculationMethodSchedule", "ClothingInsulationSchedule", "DynamicClothingModelASHRAE55"
        ]
        | None = "ClothingInsulationSchedule",
        clothing_insulation_calculation_method_schedule_name: str | None = ...,
        clothing_insulation_schedule_name: str | None = ...,
        air_velocity_schedule_name: str | None = ...,
        thermal_comfort_model_1_type: Literal[
            "AdaptiveASH55", "AdaptiveCEN15251", "AnkleDraftASH55", "CoolingEffectASH55", "Fanger", "KSU", "Pierce"
        ]
        | None = ...,
        thermal_comfort_model_2_type: Literal[
            "AdaptiveASH55", "AdaptiveCEN15251", "AnkleDraftASH55", "CoolingEffectASH55", "Fanger", "KSU", "Pierce"
        ]
        | None = ...,
        thermal_comfort_model_3_type: Literal[
            "AdaptiveASH55", "AdaptiveCEN15251", "AnkleDraftASH55", "CoolingEffectASH55", "Fanger", "KSU", "Pierce"
        ]
        | None = ...,
        thermal_comfort_model_4_type: Literal[
            "AdaptiveASH55", "AdaptiveCEN15251", "AnkleDraftASH55", "CoolingEffectASH55", "Fanger", "KSU", "Pierce"
        ]
        | None = ...,
        thermal_comfort_model_5_type: Literal[
            "AdaptiveASH55", "AdaptiveCEN15251", "AnkleDraftASH55", "CoolingEffectASH55", "Fanger", "KSU", "Pierce"
        ]
        | None = ...,
        thermal_comfort_model_6_type: Literal[
            "AdaptiveASH55", "AdaptiveCEN15251", "AnkleDraftASH55", "CoolingEffectASH55", "Fanger", "KSU", "Pierce"
        ]
        | None = ...,
        thermal_comfort_model_7_type: Literal[
            "AdaptiveASH55", "AdaptiveCEN15251", "AnkleDraftASH55", "CoolingEffectASH55", "Fanger", "KSU", "Pierce"
        ]
        | None = ...,
        ankle_level_air_velocity_schedule_name: str | None = ...,
        cold_stress_temperature_threshold: float | None = 15.56,
        heat_stress_temperature_threshold: float | None = 30,
    ) -> None:
        """Create a new ``People`` and add it to the document.

        Sets internal gains and contaminant rates for occupants in the zone. If a ZoneList, SpaceList, or a Zone comprised of more than one Space is specified then this definition applies to all applicable spaces, and each instance will be named with the Space Name plus this Object Name.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-internal-gains-people-lights-other/#people
        """

class HotWaterEquipmentInstance:
    def __call__(
        self,
        name: str,
        /,
        *,
        hot_water_equipment_definition_name: str,
        zone_or_zonelist_or_space_or_spacelist_name: str,
        schedule_name: str,
        multiplier: float | None = 1,
        end_use_subcategory: str | None = "General",
    ) -> None:
        """Create a new ``HotWaterEquipment:Instance`` and add it to the document.

        Sets internal gains for hot water equipment in the zone. The physical characteristics are given by the referenced HotWaterEquipment:Definition object. If a ZoneList, SpaceList, or a Zone comprised of more than one Space is specified then this definition applies to all applicable spaces, and each instance will be named with the Space Name plus this Object Name.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-internal-gains/#hotwaterequipmentinstance
        """

class SurfaceContaminantSourceAndSinkGenericBoundaryLayerDiffusion:
    def __call__(
        self,
        name: str,
        /,
        *,
        surface_name: str,
        schedule_name: str,
        mass_transfer_coefficient: float | None = ...,
        henry_adsorption_constant_or_partition_coefficient: float | None = ...,
    ) -> None:
        """Create a new ``SurfaceContaminantSourceAndSink:Generic:BoundaryLayerDiffusion`` and add it to the document.

        Simulate generic contaminant source driven by the boundary layer diffusion controlled model.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-internal-gains-people-lights-other/#surfacecontaminantsourceandsinkgenericboundarylayerdiffusion
        """

class ZoneEarthtube:
    def __call__(
        self,
        /,
        *,
        zone_name: str,
        schedule_name: str,
        design_flow_rate: float,
        minimum_zone_temperature_when_cooling: float,
        maximum_zone_temperature_when_heating: float,
        delta_temperature: float,
        average_soil_surface_temperature: float,
        amplitude_of_soil_surface_temperature: float,
        phase_constant_of_soil_surface_temperature: float,
        earthtube_type: Literal["", "Exhaust", "Intake", "Natural"] | None = "Natural",
        fan_pressure_rise: float | None = 0,
        fan_total_efficiency: float | None = 1,
        pipe_radius: float | None = 1,
        pipe_thickness: float | None = 0.2,
        pipe_length: float | None = 15,
        pipe_thermal_conductivity: float | None = 200,
        pipe_depth_under_ground_surface: float | None = 3,
        soil_condition: Literal["", "HeavyAndDamp", "HeavyAndDry", "HeavyAndSaturated", "LightAndDry"]
        | None = "HeavyAndDamp",
        constant_term_flow_coefficient: float | None = 1,
        temperature_term_flow_coefficient: float | None = 0,
        velocity_term_flow_coefficient: float | None = 0,
        velocity_squared_term_flow_coefficient: float | None = 0,
        earth_tube_model_type: Literal["", "Basic", "Vertical"] | None = "Basic",
        earth_tube_model_parameters: str | None = ...,
    ) -> None:
        """Create a new ``ZoneEarthtube`` and add it to the document.

        Earth Tube is specified as a design level which is modified by a Schedule fraction, temperature difference and wind speed: Earthtube=Edesign * Fschedule * (A + B*|(Tzone-Todb)| + C*WindSpd + D * WindSpd**2)

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-airflow/#zoneearthtube
        """

class AnyZoneThermalChimney:
    def __call__(
        self,
        name: str,
        /,
        *,
        narrow_with_as_version_first: Never,
        zone_name: str,
        width_of_the_absorber_wall: float,
        cross_sectional_area_of_air_channel_outlet: float,
        distance_from_top_of_thermal_chimney_to_inlet_1: float,
        cross_sectional_areas_of_air_channel_inlet_1: float,
        availability_schedule_name: str | None = ...,
        discharge_coefficient: float | None = 0.8,
        distance_from_top_of_thermal_chimney_to_inlet_2: float | None = ...,
        cross_sectional_areas_of_air_channel_inlet_2: float | None = ...,
        distance_from_top_of_thermal_chimney_to_inlet_3: float | None = ...,
        cross_sectional_areas_of_air_channel_inlet_3: float | None = ...,
        distance_from_top_of_thermal_chimney_to_inlet_4: float | None = ...,
        cross_sectional_areas_of_air_channel_inlet_4: float | None = ...,
        distance_from_top_of_thermal_chimney_to_inlet_5: float | None = ...,
        cross_sectional_areas_of_air_channel_inlet_5: float | None = ...,
        distance_from_top_of_thermal_chimney_to_inlet_6: float | None = ...,
        cross_sectional_areas_of_air_channel_inlet_6: float | None = ...,
        distance_from_top_of_thermal_chimney_to_inlet_7: float | None = ...,
        cross_sectional_areas_of_air_channel_inlet_7: float | None = ...,
        distance_from_top_of_thermal_chimney_to_inlet_8: float | None = ...,
        cross_sectional_areas_of_air_channel_inlet_8: float | None = ...,
        distance_from_top_of_thermal_chimney_to_inlet_9: float | None = ...,
        cross_sectional_areas_of_air_channel_inlet_9: float | None = ...,
        distance_from_top_of_thermal_chimney_to_inlet_10: float | None = ...,
        cross_sectional_areas_of_air_channel_inlet_10: float | None = ...,
        distance_from_top_of_thermal_chimney_to_inlet_11: float | None = ...,
        cross_sectional_areas_of_air_channel_inlet_11: float | None = ...,
        distance_from_top_of_thermal_chimney_to_inlet_12: float | None = ...,
        cross_sectional_areas_of_air_channel_inlet_12: float | None = ...,
        distance_from_top_of_thermal_chimney_to_inlet_13: float | None = ...,
        cross_sectional_areas_of_air_channel_inlet_13: float | None = ...,
        distance_from_top_of_thermal_chimney_to_inlet_14: float | None = ...,
        cross_sectional_areas_of_air_channel_inlet_14: float | None = ...,
        distance_from_top_of_thermal_chimney_to_inlet_15: float | None = ...,
        cross_sectional_areas_of_air_channel_inlet_15: float | None = ...,
        distance_from_top_of_thermal_chimney_to_inlet_16: float | None = ...,
        cross_sectional_areas_of_air_channel_inlet_16: float | None = ...,
        distance_from_top_of_thermal_chimney_to_inlet_17: float | None = ...,
        cross_sectional_areas_of_air_channel_inlet_17: float | None = ...,
        distance_from_top_of_thermal_chimney_to_inlet_18: float | None = ...,
        cross_sectional_areas_of_air_channel_inlet_18: float | None = ...,
        distance_from_top_of_thermal_chimney_to_inlet_19: float | None = ...,
        cross_sectional_areas_of_air_channel_inlet_19: float | None = ...,
        distance_from_top_of_thermal_chimney_to_inlet_20: float | None = ...,
        cross_sectional_areas_of_air_channel_inlet_20: float | None = ...,
    ) -> None:
        """Create a new ``ZoneThermalChimney`` and add it to the document.

        A thermal chimney is a vertical shaft utilizing solar radiation to enhance natural ventilation. It consists of an absorber wall, air gap and glass cover with high solar transmissivity.

        No call suits every release: narrow the document with ``as_version`` first.
        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-airflow/#zonethermalchimney
        """

class AirflowNetworkMultiZoneSurface:
    def __call__(
        self,
        /,
        *,
        surface_name: str,
        leakage_component_name: str,
        external_node_name: str | None = ...,
        window_door_opening_factor_or_crack_factor: float | None = 1,
        ventilation_control_mode: Literal[
            "",
            "ASHRAE55Adaptive",
            "AdjacentEnthalpy",
            "AdjacentTemperature",
            "CEN15251Adaptive",
            "Constant",
            "Enthalpy",
            "NoVent",
            "Temperature",
            "ZoneLevel",
        ]
        | None = "ZoneLevel",
        ventilation_control_zone_temperature_setpoint_schedule_name: str | None = ...,
        minimum_venting_open_factor: float | None = 0,
        indoor_and_outdoor_temperature_difference_lower_limit_for_maximum_venting_open_factor: float | None = 0,
        indoor_and_outdoor_temperature_difference_upper_limit_for_minimum_venting_open_factor: float | None = 100,
        indoor_and_outdoor_enthalpy_difference_lower_limit_for_maximum_venting_open_factor: float | None = 0,
        indoor_and_outdoor_enthalpy_difference_upper_limit_for_minimum_venting_open_factor: float | None = 300000,
        venting_availability_schedule_name: str | None = ...,
        occupant_ventilation_control_name: str | None = ...,
        equivalent_rectangle_method: Literal["", "BaseSurfaceAspectRatio", "PolygonHeight", "UserDefinedAspectRatio"]
        | None = "PolygonHeight",
        equivalent_rectangle_aspect_ratio: float | None = 1,
    ) -> None:
        """Create a new ``AirflowNetwork:MultiZone:Surface`` and add it to the document.

        This object specifies the properties of a surface linkage through which air flows. Airflow Report: Node 1 as an inside face zone; Node 2 as an outside face zone or external node.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-airflow-network/#airflownetworkmultizonesurface
        """

class HVACTemplateZoneFanCoil:
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
        cooling_coil_type: Literal[
            "", "ChilledWater", "ChilledWaterDetailedFlatModel", "HeatExchangerAssistedChilledWater"
        ]
        | None = "ChilledWater",
        cooling_coil_availability_schedule_name: str | None = ...,
        cooling_coil_design_setpoint: float | None = 14,
        heating_coil_type: Literal["", "Electric", "HotWater"] | None = "HotWater",
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
            "ASHRAE90VariableFan",
            "ConstantFanVariableFlow",
            "CyclingFan",
            "MultiSpeedFan",
            "VariableFanConstantFlow",
            "VariableFanVariableFlow",
        ]
        | None = ...,
        low_speed_supply_air_flow_ratio: float | None = 0.33,
        medium_speed_supply_air_flow_ratio: float | None = 0.66,
        outdoor_air_schedule_name: str | None = ...,
        baseboard_heating_type: Literal["", "Electric", "HotWater", "None"] | None = "None",
        baseboard_heating_availability_schedule_name: str | None = ...,
        baseboard_heating_capacity: float | Literal["", "Autosize"] | None = "Autosize",
    ) -> None:
        """Create a new ``HVACTemplate:Zone:FanCoil`` and add it to the document.

        4 pipe fan coil unit with optional outdoor air.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/hvac-template-objects/group-hvac-templates/#hvactemplatezonefancoil
        """

class ZoneHVACPackagedTerminalHeatPump:
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
        heating_coil_object_type: Literal["Coil:Heating:DX:SingleSpeed", "Coil:Heating:DX:VariableSpeed"],
        heating_coil_name: str,
        cooling_coil_object_type: Literal[
            "Coil:Cooling:DX",
            "Coil:Cooling:DX:SingleSpeed",
            "Coil:Cooling:DX:VariableSpeed",
            "CoilSystem:Cooling:DX:HeatExchangerAssisted",
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
        no_load_supply_air_flow_rate_control_set_to_low_speed: Literal["", "No", "Yes"] | None = "Yes",
        no_load_outdoor_air_flow_rate: float | Literal["Autosize"] | None = ...,
        heating_convergence_tolerance: float | None = 0.001,
        cooling_convergence_tolerance: float | None = 0.001,
        maximum_outdoor_dry_bulb_temperature_for_supplemental_heater_operation: float | None = 21,
        fan_placement: Literal["", "BlowThrough", "DrawThrough"] | None = "DrawThrough",
        supply_air_fan_operating_mode_schedule_name: str | None = ...,
        availability_manager_list_name: str | None = ...,
        design_specification_zonehvac_sizing_object_name: str | None = ...,
        capacity_control_method: Literal["", "None", "SingleZoneVAV"] | None = "None",
        minimum_supply_air_temperature_in_cooling_mode: float | Literal["", "Autosize"] | None = "Autosize",
        maximum_supply_air_temperature_in_heating_mode: float | Literal["", "Autosize"] | None = "Autosize",
        dx_heating_coil_sizing_ratio: float | None = 1,
    ) -> None:
        """Create a new ``ZoneHVAC:PackagedTerminalHeatPump`` and add it to the document.

        Packaged terminal heat pump (PTHP). Forced-convection heating-cooling unit with supply fan, direct expansion (DX) cooling coil, DX heating coil (air-to-air heat pump), supplemental heating coil (gas, electric, hot water, or steam), and fixed-position outdoor air mixer.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-zone-forced-air-units/#zonehvacpackagedterminalheatpump
        """

class ZoneHVACUnitVentilator:
    def __call__(
        self,
        name: str,
        /,
        *,
        maximum_supply_air_flow_rate: float | Literal["Autosize"],
        outdoor_air_control_type: Literal["FixedAmount", "FixedTemperature", "VariablePercent"],
        minimum_outdoor_air_flow_rate: float | Literal["Autosize"],
        minimum_outdoor_air_schedule_name: str,
        maximum_outdoor_air_flow_rate: float | Literal["Autosize"],
        maximum_outdoor_air_fraction_or_temperature_schedule_name: str,
        air_inlet_node_name: str,
        air_outlet_node_name: str,
        supply_air_fan_object_type: Literal["Fan:ConstantVolume", "Fan:OnOff", "Fan:SystemModel", "Fan:VariableVolume"],
        supply_air_fan_name: str,
        coil_option: Literal["Cooling", "Heating", "HeatingAndCooling", "None"],
        availability_schedule_name: str | None = ...,
        outdoor_air_node_name: str | None = ...,
        exhaust_air_node_name: str | None = ...,
        mixed_air_node_name: str | None = ...,
        supply_air_fan_operating_mode_schedule_name: str | None = ...,
        heating_coil_object_type: Literal[
            "Coil:Heating:Electric", "Coil:Heating:Fuel", "Coil:Heating:Steam", "Coil:Heating:Water"
        ]
        | None = ...,
        heating_coil_name: str | None = ...,
        heating_convergence_tolerance: float | None = 0.001,
        cooling_coil_object_type: Literal[
            "Coil:Cooling:Water",
            "Coil:Cooling:Water:DetailedGeometry",
            "CoilSystem:Cooling:Water:HeatExchangerAssisted",
        ]
        | None = ...,
        cooling_coil_name: str | None = ...,
        cooling_convergence_tolerance: float | None = 0.001,
        availability_manager_list_name: str | None = ...,
        design_specification_zonehvac_sizing_object_name: str | None = ...,
    ) -> None:
        """Create a new ``ZoneHVAC:UnitVentilator`` and add it to the document.

        Unit ventilator. Forced-convection ventilation unit with supply fan (constant-volume or variable-volume), optional chilled water cooling coil, optional heating coil (gas, electric, hot water, or steam) and controllable outdoor air mixer.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-zone-forced-air-units/#zonehvacunitventilator
        """

class ZoneHVACBaseboardRadiantConvectiveWater:
    def __call__(
        self,
        name: str,
        /,
        *,
        design_object: str,
        inlet_node_name: str,
        outlet_node_name: str,
        maximum_water_flow_rate: float | Literal["Autosize"],
        availability_schedule_name: str | None = ...,
        rated_average_water_temperature: float | None = 87.78,
        rated_water_mass_flow_rate: float | None = 0.063,
        heating_design_capacity: float | Literal["", "Autosize"] | None = "Autosize",
        surface_fractions: list[_g.ZoneHVACBaseboardRadiantConvectiveWaterSurfaceFractionsItem] = ...,
    ) -> None:
        """Create a new ``ZoneHVAC:Baseboard:RadiantConvective:Water`` and add it to the document.

        The number of surfaces can be expanded beyond 100, if necessary, by adding more groups to the end of the list

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-radiative-convective-units/#zonehvacbaseboardradiantconvectivewater
        """

class AirTerminalSingleDuctConstantVolumeFourPipeBeam:
    def __call__(
        self,
        name: str,
        /,
        *,
        primary_air_inlet_node_name: str,
        primary_air_outlet_node_name: str,
        primary_air_availability_schedule_name: str | None = ...,
        cooling_availability_schedule_name: str | None = ...,
        heating_availability_schedule_name: str | None = ...,
        chilled_water_inlet_node_name: str | None = ...,
        chilled_water_outlet_node_name: str | None = ...,
        hot_water_inlet_node_name: str | None = ...,
        hot_water_outlet_node_name: str | None = ...,
        design_primary_air_volume_flow_rate: float | Literal["", "Autosize"] | None = "Autosize",
        design_chilled_water_volume_flow_rate: float | Literal["", "Autosize"] | None = "Autosize",
        design_hot_water_volume_flow_rate: float | Literal["", "Autosize"] | None = "Autosize",
        zone_total_beam_length: float | Literal["", "Autosize"] | None = "Autosize",
        rated_primary_air_flow_rate_per_beam_length: float | None = 0.035,
        beam_rated_cooling_capacity_per_beam_length: float | None = 600,
        beam_rated_cooling_room_air_chilled_water_temperature_difference: float | None = 10,
        beam_rated_chilled_water_volume_flow_rate_per_beam_length: float | None = ...,
        beam_cooling_capacity_temperature_difference_modification_factor_curve_name: str | None = ...,
        beam_cooling_capacity_air_flow_modification_factor_curve_name: str | None = ...,
        beam_cooling_capacity_chilled_water_flow_modification_factor_curve_name: str | None = ...,
        beam_rated_heating_capacity_per_beam_length: float | None = 1500,
        beam_rated_heating_room_air_hot_water_temperature_difference: float | None = 27.8,
        beam_rated_hot_water_volume_flow_rate_per_beam_length: float | None = ...,
        beam_heating_capacity_temperature_difference_modification_factor_curve_name: str | None = ...,
        beam_heating_capacity_air_flow_modification_factor_curve_name: str | None = ...,
        beam_heating_capacity_hot_water_flow_modification_factor_curve_name: str | None = ...,
    ) -> None:
        """Create a new ``AirTerminal:SingleDuct:ConstantVolume:FourPipeBeam`` and add it to the document.

        Central air system terminal unit, single duct, constant volume, with heating and/or cooling. Operates as two-pipe unit if heating or cooling water is omitted. Heating and/or cooling can be scheduled off for dedicated ventilation.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-air-distribution-equipment/#airterminalsingleductconstantvolumefourpipebeam
        """

class AnyCoilCoolingDXTwoStageWithHumidityControlMode:
    def __call__(
        self,
        name: str,
        /,
        *,
        air_inlet_node_name: str,
        air_outlet_node_name: str,
        normal_mode_stage_1_coil_performance_object_type: Literal["CoilPerformance:DX:Cooling"],
        normal_mode_stage_1_coil_performance_name: str,
        availability_schedule_name: str | None = ...,
        crankcase_heater_capacity: float | None = 0,
        maximum_outdoor_dry_bulb_temperature_for_crankcase_heater_operation: float | None = 10,
        number_of_capacity_stages: int | None = 1,
        number_of_enhanced_dehumidification_modes: int | None = 0,
        normal_mode_stage_1_2_coil_performance_object_type: Literal["CoilPerformance:DX:Cooling"] | None = ...,
        normal_mode_stage_1_2_coil_performance_name: str | None = ...,
        dehumidification_mode_1_stage_1_coil_performance_object_type: Literal["CoilPerformance:DX:Cooling"]
        | None = ...,
        dehumidification_mode_1_stage_1_coil_performance_name: str | None = ...,
        dehumidification_mode_1_stage_1_2_coil_performance_object_type: Literal["CoilPerformance:DX:Cooling"]
        | None = ...,
        dehumidification_mode_1_stage_1_2_coil_performance_name: str | None = ...,
        supply_water_storage_tank_name: str | None = ...,
        condensate_collection_water_storage_tank_name: str | None = ...,
        minimum_outdoor_dry_bulb_temperature_for_compressor_operation: float | None = -25,
        basin_heater_capacity: float | None = 0,
        basin_heater_setpoint_temperature: float | None = 2,
        basin_heater_operating_schedule_name: str | None = ...,
    ) -> None:
        """Create a new ``Coil:Cooling:DX:TwoStageWithHumidityControlMode`` and add it to the document.

        Direct expansion (DX) cooling coil and condensing unit (includes electric compressor and condenser fan), two-stage with humidity control mode (e.g. sub-cool or hot gas reheat). Optional inputs for moisture evaporation from wet coil when compressor cycles off with continuous fan operation. Requires two to four sets of performance data, see CoilPerformance:DX:Cooling. Stages are modeled as a face-split coil.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-heating-and-cooling-coils/#coilcoolingdxtwostagewithhumiditycontrolmode
        """

class AnyCoilCoolingWaterToAirHeatPumpParameterEstimation:
    def __call__(
        self,
        name: str,
        /,
        *,
        narrow_with_as_version_first: Never,
        compressor_type: Literal["Reciprocating", "Rotary", "Scroll"],
        design_source_side_flow_rate: float,
        nominal_cooling_coil_capacity: float,
        high_pressure_cutoff: float,
        low_pressure_cutoff: float,
        water_inlet_node_name: str,
        water_outlet_node_name: str,
        air_inlet_node_name: str,
        air_outlet_node_name: str,
        load_side_total_heat_transfer_coefficient: float,
        load_side_outside_surface_heat_transfer_coefficient: float,
        superheat_temperature_at_the_evaporator_outlet: float,
        compressor_power_losses: float,
        compressor_efficiency: float,
        refrigerant_type: str | None = "R22",
        nominal_time_for_condensate_removal_to_begin: float | None = 0,
        ratio_of_initial_moisture_evaporation_rate_and_steady_state_latent_capacity: float | None = 0,
        compressor_piston_displacement: float | None = ...,
        compressor_suction_discharge_pressure_drop: float | None = ...,
        compressor_clearance_factor: float | None = ...,
        refrigerant_volume_flow_rate: float | None = ...,
        volume_ratio: float | None = ...,
        leak_rate_coefficient: float | None = ...,
        source_side_heat_transfer_coefficient: float | None = ...,
        source_side_heat_transfer_resistance1: float | None = ...,
        source_side_heat_transfer_resistance2: float | None = ...,
    ) -> None:
        """Create a new ``Coil:Cooling:WaterToAirHeatPump:ParameterEstimation`` and add it to the document.

        Direct expansion (DX) cooling coil for water-to-air heat pump (includes electric compressor), single-speed, parameter estimation model. Optional inputs for moisture evaporation from wet coil when compressor cycles off with continuous fan operation. Parameter estimation model is a deterministic model that requires a consistent set of parameters to describe the operating conditions of the heat pump components.

        No call suits every release: narrow the document with ``as_version`` first.
        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-heating-and-cooling-coils/#coilcoolingwatertoairheatpumpparameterestimation
        """

class CoilCoolingWaterToAirHeatPumpParameterEstimation:
    def __call__(
        self,
        name: str,
        /,
        *,
        compressor_type: Literal["Reciprocating", "Rotary", "Scroll"],
        design_source_side_flow_rate: float,
        nominal_cooling_coil_capacity: float,
        high_pressure_cutoff: float,
        low_pressure_cutoff: float,
        water_inlet_node_name: str,
        water_outlet_node_name: str,
        air_inlet_node_name: str,
        air_outlet_node_name: str,
        load_side_total_heat_transfer_coefficient: float,
        load_side_outside_surface_heat_transfer_coefficient: float,
        superheat_temperature_at_the_evaporator_outlet: float,
        compressor_power_losses: float,
        compressor_efficiency: float,
        part_load_fraction_correlation_curve_name: str,
        availability_schedule_name: str | None = ...,
        refrigerant_type: str | None = "R22",
        nominal_time_for_condensate_removal_to_begin: float | None = 0,
        ratio_of_initial_moisture_evaporation_rate_and_steady_state_latent_capacity: float | None = 0,
        compressor_piston_displacement: float | None = ...,
        compressor_suction_discharge_pressure_drop: float | None = ...,
        compressor_clearance_factor: float | None = ...,
        refrigerant_volume_flow_rate: float | None = ...,
        volume_ratio: float | None = ...,
        leak_rate_coefficient: float | None = ...,
        source_side_heat_transfer_coefficient: float | None = ...,
        source_side_heat_transfer_resistance1: float | None = ...,
        source_side_heat_transfer_resistance2: float | None = ...,
        maximum_cycling_rate: float | None = 0,
        latent_capacity_time_constant: float | None = 0,
        fan_delay_time: float | None = 60,
    ) -> None:
        """Create a new ``Coil:Cooling:WaterToAirHeatPump:ParameterEstimation`` and add it to the document.

        Direct expansion (DX) cooling coil for water-to-air heat pump (includes electric compressor), single-speed, parameter estimation model. Optional inputs for moisture evaporation from wet coil when compressor cycles off with continuous fan operation. Parameter estimation model is a deterministic model that requires a consistent set of parameters to describe the operating conditions of the heat pump components.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-heating-and-cooling-coils/#coilcoolingwatertoairheatpumpparameterestimation
        """

class DehumidifierDesiccantNoFans:
    def __call__(
        self,
        name: str,
        /,
        *,
        availability_schedule_name: str | None = ...,
        process_air_inlet_node_name: str | None = ...,
        process_air_outlet_node_name: str | None = ...,
        regeneration_air_inlet_node_name: str | None = ...,
        regeneration_fan_inlet_node_name: str | None = ...,
        control_type: Literal["LeavingMaximumHumidityRatioSetpoint", "SystemNodeMaximumHumidityRatioSetpoint"]
        | None = ...,
        leaving_maximum_humidity_ratio_setpoint: float | None = ...,
        nominal_process_air_flow_rate: float | None = ...,
        nominal_process_air_velocity: float | None = ...,
        rotor_power: float | None = ...,
        regeneration_coil_object_type: Literal[
            "Coil:Heating:Electric", "Coil:Heating:Fuel", "Coil:Heating:Steam", "Coil:Heating:Water"
        ]
        | None = ...,
        regeneration_coil_name: str | None = ...,
        regeneration_fan_object_type: Literal["Fan:ConstantVolume", "Fan:SystemModel", "Fan:VariableVolume"]
        | None = ...,
        regeneration_fan_name: str | None = ...,
        performance_model_type: Literal["Default", "UserCurves"] | None = ...,
        leaving_dry_bulb_function_of_entering_dry_bulb_and_humidity_ratio_curve_name: str | None = ...,
        leaving_dry_bulb_function_of_air_velocity_curve_name: str | None = ...,
        leaving_humidity_ratio_function_of_entering_dry_bulb_and_humidity_ratio_curve_name: str | None = ...,
        leaving_humidity_ratio_function_of_air_velocity_curve_name: str | None = ...,
        regeneration_energy_function_of_entering_dry_bulb_and_humidity_ratio_curve_name: str | None = ...,
        regeneration_energy_function_of_air_velocity_curve_name: str | None = ...,
        regeneration_velocity_function_of_entering_dry_bulb_and_humidity_ratio_curve_name: str | None = ...,
        regeneration_velocity_function_of_air_velocity_curve_name: str | None = ...,
        nominal_regeneration_temperature: float | None = ...,
    ) -> None:
        """Create a new ``Dehumidifier:Desiccant:NoFans`` and add it to the document.

        This object models a solid desiccant dehumidifier. The process air stream is the air which is dehumidified. The regeneration air stream is the air which is heated to regenerate the desiccant. This object determines the process air outlet conditions, the load on the regeneration heating coil, the electric power consumption for the wheel rotor motor, and the regeneration air fan mass flow rate. All other heat exchangers are modeled as separate objects connected to the inlet and outlet nodes of the dehumidifier. The solid desiccant dehumidifier is typically used in an AirLoopHVAC:OutdoorAirSystem, but can also be specified in any AirLoopHVAC.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-humidifiers-and-dehumidifiers/#dehumidifierdesiccantnofans
        """

class AirLoopHVACUnitaryHeatOnly:
    def __call__(
        self,
        name: str,
        /,
        *,
        unitary_system_air_inlet_node_name: str,
        unitary_system_air_outlet_node_name: str,
        heating_supply_air_flow_rate: float | Literal["Autosize"],
        controlling_zone_or_thermostat_location: str,
        supply_fan_object_type: Literal["Fan:ConstantVolume", "Fan:OnOff"],
        supply_fan_name: str,
        heating_coil_object_type: Literal[
            "Coil:Heating:Electric", "Coil:Heating:Fuel", "Coil:Heating:Steam", "Coil:Heating:Water"
        ],
        heating_coil_name: str,
        availability_schedule_name: str | None = ...,
        supply_air_fan_operating_mode_schedule_name: str | None = ...,
        maximum_supply_air_temperature: float | Literal["", "Autosize"] | None = 80,
        fan_placement: Literal["", "BlowThrough", "DrawThrough"] | None = "BlowThrough",
    ) -> None:
        """Create a new ``AirLoopHVAC:UnitaryHeatOnly`` and add it to the document.

        Unitary system, heating-only with constant volume supply fan (continuous or cycling) and heating coil (gas, electric, hot water, or steam). Identical to AirLoopHVAC:Unitary:Furnace:HeatOnly.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-unitary-equipment/#airloophvacunitaryheatonly
        """

class AnyHeaderedPumpsVariableSpeed:
    def __call__(
        self,
        name: str,
        /,
        *,
        inlet_node_name: str,
        outlet_node_name: str,
        total_design_flow_rate: float | Literal["Autosize"] | None = ...,
        number_of_pumps_in_bank: int | None = ...,
        flow_sequencing_control_scheme: Literal["", "Sequential"] | None = "Sequential",
        design_pump_head: float | None = 179352,
        design_power_consumption: float | Literal["Autosize"] | None = ...,
        motor_efficiency: float | None = 0.9,
        fraction_of_motor_inefficiencies_to_fluid_stream: float | None = 0,
        coefficient_1_of_the_part_load_performance_curve: float | None = 0,
        coefficient_2_of_the_part_load_performance_curve: float | None = 1,
        coefficient_3_of_the_part_load_performance_curve: float | None = 0,
        coefficient_4_of_the_part_load_performance_curve: float | None = 0,
        minimum_flow_rate_fraction: float | None = 0,
        pump_control_type: Literal["", "Continuous", "Intermittent"] | None = "Continuous",
        pump_flow_rate_schedule_name: str | None = ...,
        zone_name: str | None = ...,
        skin_loss_radiative_fraction: float | None = ...,
        design_power_sizing_method: Literal["", "PowerPerFlow", "PowerPerFlowPerPressure"]
        | None = "PowerPerFlowPerPressure",
        design_electric_power_per_unit_flow_rate: float | None = 348701.1,
        design_shaft_power_per_unit_flow_rate_per_unit_head: float | None = 1.282051282,
    ) -> None:
        """Create a new ``HeaderedPumps:VariableSpeed`` and add it to the document.

        This Headered pump object describes a pump bank with more than 1 pump in parallel

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-pumps/#headeredpumpsvariablespeed
        """

class HeaderedPumpsVariableSpeed:
    def __call__(
        self,
        name: str,
        /,
        *,
        inlet_node_name: str,
        outlet_node_name: str,
        total_design_flow_rate: float | Literal["Autosize"] | None = ...,
        number_of_pumps_in_bank: int | None = ...,
        flow_sequencing_control_scheme: Literal["", "Sequential"] | None = "Sequential",
        design_pump_head: float | None = 179352,
        design_power_consumption: float | Literal["Autosize"] | None = ...,
        motor_efficiency: float | None = 0.9,
        fraction_of_motor_inefficiencies_to_fluid_stream: float | None = 0,
        coefficient_1_of_the_part_load_performance_curve: float | None = 0,
        coefficient_2_of_the_part_load_performance_curve: float | None = 1,
        coefficient_3_of_the_part_load_performance_curve: float | None = 0,
        coefficient_4_of_the_part_load_performance_curve: float | None = 0,
        minimum_flow_rate_fraction: float | None = 0,
        pump_control_type: Literal["", "Continuous", "Intermittent"] | None = "Continuous",
        pump_flow_rate_schedule_name: str | None = ...,
        zone_name: str | None = ...,
        skin_loss_radiative_fraction: float | None = ...,
        design_power_sizing_method: Literal["", "PowerPerFlow", "PowerPerFlowPerPressure"]
        | None = "PowerPerFlowPerPressure",
        design_electric_power_per_unit_flow_rate: float | None = 348701.1,
        design_shaft_power_per_unit_flow_rate_per_unit_head: float | None = 1.282051282,
        end_use_subcategory: str | None = "General",
    ) -> None:
        """Create a new ``HeaderedPumps:VariableSpeed`` and add it to the document.

        This Headered pump object describes a pump bank with more than 1 pump in parallel

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-pumps/#headeredpumpsvariablespeed
        """

class AnyGroundHeatExchangerSlinky:
    def __call__(
        self,
        name: str,
        /,
        *,
        inlet_node_name: str,
        outlet_node_name: str,
        undisturbed_ground_temperature_model_type: Literal[
            "Site:GroundTemperature:Undisturbed:FiniteDifference",
            "Site:GroundTemperature:Undisturbed:KusudaAchenbach",
            "Site:GroundTemperature:Undisturbed:Xing",
        ],
        undisturbed_ground_temperature_model_name: str,
        design_flow_rate: float | None = 0.002,
        soil_thermal_conductivity: float | None = 1.08,
        soil_density: float | None = 962,
        soil_specific_heat: float | None = 2576,
        pipe_thermal_conductivity: float | None = 0.4,
        pipe_density: float | None = 641,
        pipe_specific_heat: float | None = 2405,
        pipe_outer_diameter: float | None = 0.02667,
        pipe_thickness: float | None = 0.002413,
        heat_exchanger_configuration: Literal["Horizontal", "Vertical"] | None = ...,
        coil_diameter: float | None = 1,
        coil_pitch: float | None = 0.2,
        trench_depth: float | None = 1.8,
        trench_length: float | None = 10,
        number_of_trenches: int | None = 1,
        horizontal_spacing_between_pipes: float | None = 2,
        maximum_length_of_simulation: float | None = ...,
    ) -> None:
        """Create a new ``GroundHeatExchanger:Slinky`` and add it to the document.

        This models a slinky horizontal heat exchanger placed in a series of trenches The model uses the model developed by: Xiong, Z., D.E. Fisher, and J.D. Spitler. 2015. Development and Validation of a Slinky Ground Heat Exchanger Model. Applied Energy 141: 57-69.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-condenser-equipment/#groundheatexchangerslinky
        """

class AvailabilityManagerNightCycle:
    def __call__(
        self,
        name: str,
        /,
        *,
        applicability_schedule_name: str,
        fan_schedule_name: str,
        control_type: Literal[
            "",
            "CycleOnAny",
            "CycleOnAnyCoolingOrHeatingZone",
            "CycleOnAnyCoolingZone",
            "CycleOnAnyHeatingZone",
            "CycleOnAnyHeatingZoneFansOnly",
            "CycleOnAnyZoneFansOnly",
            "CycleOnControlZone",
            "StayOff",
        ]
        | None = "StayOff",
        thermostat_tolerance: float | None = 1,
        cycling_run_time_control_type: Literal["", "FixedRunTime", "Thermostat", "ThermostatWithMinimumRunTime"]
        | None = "FixedRunTime",
        cycling_run_time: float | None = 3600,
        control_zone_or_zone_list_name: str | None = ...,
        cooling_control_zone_or_zone_list_name: str | None = ...,
        heating_control_zone_or_zone_list_name: str | None = ...,
        heating_zone_fans_only_zone_or_zone_list_name: str | None = ...,
    ) -> None:
        """Create a new ``AvailabilityManager:NightCycle`` and add it to the document.

        Determines the availability of a loop or system: whether it is on or off. Depending on zone temperatures, overrides Schedules and forces system Fans on.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-system-availability-managers/#availabilitymanagernightcycle
        """

class DemandManagerAssignmentList:
    def __call__(
        self,
        name: str,
        /,
        *,
        meter_name: str,
        demand_limit_safety_fraction: float,
        demand_window_length: int,
        demand_manager_priority: Literal["All", "Sequential"],
        demand_limit_schedule_name: str | None = ...,
        billing_period_schedule_name: str | None = ...,
        peak_period_schedule_name: str | None = ...,
        manager_data: list[_g.DemandManagerAssignmentListManagerDataItem] = ...,
    ) -> None:
        """Create a new ``DemandManagerAssignmentList`` and add it to the document.

        A high level control that makes demand limiting decisions based on a list of possible demand limiting strategies.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-demand-limiting-controls/#demandmanagerassignmentlist
        """

class AnyPhotovoltaicPerformanceSandia:
    def __call__(
        self,
        name: str,
        /,
        *,
        active_area: float | None = 1,
        number_of_cells_in_series: int | None = 1,
        number_of_cells_in_parallel: int | None = 1,
        short_circuit_current: float | None = ...,
        open_circuit_voltage: float | None = ...,
        current_at_maximum_power_point: float | None = ...,
        voltage_at_maximum_power_point: float | None = ...,
        sandia_database_parameter_aisc: float | None = ...,
        sandia_database_parameter_aimp: float | None = ...,
        sandia_database_parameter_c0: float | None = ...,
        sandia_database_parameter_c1: float | None = ...,
        sandia_database_parameter_bvoc0: float | None = ...,
        sandia_database_parameter_mbvoc: float | None = ...,
        sandia_database_parameter_bvmp0: float | None = ...,
        sandia_database_parameter_mbvmp: float | None = ...,
        diode_factor: float | None = ...,
        sandia_database_parameter_c2: float | None = ...,
        sandia_database_parameter_c3: float | None = ...,
        sandia_database_parameter_a0: float | None = ...,
        sandia_database_parameter_a1: float | None = ...,
        sandia_database_parameter_a2: float | None = ...,
        sandia_database_parameter_a3: float | None = ...,
        sandia_database_parameter_a4: float | None = ...,
        sandia_database_parameter_b0: float | None = ...,
        sandia_database_parameter_b1: float | None = ...,
        sandia_database_parameter_b2: float | None = ...,
        sandia_database_parameter_b3: float | None = ...,
        sandia_database_parameter_b4: float | None = ...,
        sandia_database_parameter_b5: float | None = ...,
        sandia_database_parameter_delta_tc_: float | None = ...,
        sandia_database_parameter_fd: float | None = ...,
        sandia_database_parameter_a: float | None = ...,
        sandia_database_parameter_b: float | None = ...,
        sandia_database_parameter_c4: float | None = ...,
        sandia_database_parameter_c5: float | None = ...,
        sandia_database_parameter_ix0: float | None = ...,
        sandia_database_parameter_ixx0: float | None = ...,
        sandia_database_parameter_c6: float | None = ...,
        sandia_database_parameter_c7: float | None = ...,
        sandia_database_parameter_delta_tc: float | None = ...,
    ) -> None:
        """Create a new ``PhotovoltaicPerformance:Sandia`` and add it to the document.

        Describes performance input data needed for specific makes and models of production PV panels using the empirical coefficients assembled by Sandia National Laboratory.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-electric-load-center-generator/#photovoltaicperformancesandia
        """

class GeneratorWindTurbine:
    def __call__(
        self,
        name: str,
        /,
        *,
        rated_rotor_speed: float,
        rotor_diameter: float,
        overall_height: float,
        rated_power: float,
        rated_wind_speed: float,
        cut_in_wind_speed: float,
        cut_out_wind_speed: float,
        availability_schedule_name: str | None = ...,
        rotor_type: Literal["", "HorizontalAxisWindTurbine", "VerticalAxisWindTurbine"]
        | None = "HorizontalAxisWindTurbine",
        power_control: Literal[
            "",
            "FixedSpeedFixedPitch",
            "FixedSpeedVariablePitch",
            "VariableSpeedFixedPitch",
            "VariableSpeedVariablePitch",
        ]
        | None = "VariableSpeedVariablePitch",
        number_of_blades: float | None = 3,
        fraction_system_efficiency: float | None = 0.835,
        maximum_tip_speed_ratio: float | None = 5,
        maximum_power_coefficient: float | None = 0.25,
        annual_local_average_wind_speed: float | None = ...,
        height_for_local_average_wind_speed: float | None = 50,
        blade_chord_area: float | None = ...,
        blade_drag_coefficient: float | None = 0.9,
        blade_lift_coefficient: float | None = 0.05,
        power_coefficient_c1: float | None = 0.5176,
        power_coefficient_c2: float | None = 116,
        power_coefficient_c3: float | None = 0.4,
        power_coefficient_c4: float | None = 0,
        power_coefficient_c5: float | None = 5,
        power_coefficient_c6: float | None = 21,
    ) -> None:
        """Create a new ``Generator:WindTurbine`` and add it to the document.

        Wind turbine generator.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-electric-load-center-generator/#generatorwindturbine
        """

class AnyElectricLoadCenterStorageLiIonNMCBattery:
    def __call__(
        self,
        name: str,
        /,
        *,
        number_of_cells_in_series: int,
        number_of_strings_in_parallel: int,
        battery_mass: float,
        battery_surface_area: float,
        availability_schedule_name: str | None = ...,
        zone_name: str | None = ...,
        radiative_fraction: float | None = 0,
        lifetime_model: Literal["", "KandlerSmith", "None"] | None = "KandlerSmith",
        initial_fractional_state_of_charge: float | None = 0.5,
        dc_to_dc_charging_efficiency: float | None = 0.95,
        battery_specific_heat_capacity: float | None = 1500,
        heat_transfer_coefficient_between_battery_and_ambient: float | None = 7.5,
        fully_charged_cell_voltage: float | None = 4.2,
        cell_voltage_at_end_of_exponential_zone: float | None = 3.53,
        cell_voltage_at_end_of_nominal_zone: float | None = 3.342,
        default_nominal_cell_voltage: float | None = 3.342,
        fully_charged_cell_capacity: float | None = 3.2,
        fraction_of_cell_capacity_removed_at_the_end_of_exponential_zone: float | None = 0.8075,
        fraction_of_cell_capacity_removed_at_the_end_of_nominal_zone: float | None = 0.976875,
        charge_rate_at_which_voltage_vs_capacity_curve_was_generated: float | None = 1,
        battery_cell_internal_electrical_resistance: float | None = 0.09,
    ) -> None:
        """Create a new ``ElectricLoadCenter:Storage:LiIonNMCBattery`` and add it to the document.

        Uses Lithium Ion NMC model to simulate rechargeable battery banks in an electrical load center. The battery bank is a collection of one or more individual battery modules. Given the surplus or deficit power from the electrical system and the state of charge from the previous time step, this object can model the voltage, current, and energy losses with charging and discharging during each time step. The cumulative battery damage can be also modeled and reported at the end of each simulation run.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-electric-load-center-generator/#electricloadcenterstorageliionnmcbattery
        """

class UtilityCostTariff:
    def __call__(
        self,
        name: str,
        /,
        *,
        output_meter_name: str,
        conversion_factor_choice: Literal[
            "CCF", "MCF", "MJ", "MMBtu", "Therm", "UserDefined", "gal", "kBtu", "kWh", "kgal", "m3"
        ]
        | None = ...,
        energy_conversion_factor: float | None = ...,
        demand_conversion_factor: float | None = ...,
        time_of_use_period_schedule_name: str | None = ...,
        season_schedule_name: str | None = ...,
        month_schedule_name: str | None = ...,
        demand_window_length: Literal["Day", "FullHour", "HalfHour", "QuarterHour", "Week"] | None = ...,
        monthly_charge_or_variable_name: float | str | None = ...,
        minimum_monthly_charge_or_variable_name: float | str | None = ...,
        real_time_pricing_charge_schedule_name: str | None = ...,
        customer_baseline_load_schedule_name: str | None = ...,
        group_name: str | None = ...,
        buy_or_sell: Literal["", "BuyFromUtility", "NetMetering", "SellToUtility"] | None = "BuyFromUtility",
    ) -> None:
        """Create a new ``UtilityCost:Tariff`` and add it to the document.

        Defines the name of a utility cost tariff, the type of tariff, and other details about the overall tariff. Each other object that is part of the tariff model references the tariff name. See UtilityCost:Charge:Simple, UtilityCost:Charge:Block, UtilityCost:Ratchet, UtilityCost:Qualify, UtilityCost:Variable and UtilityCost:Computation objects.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/energyplus-economics/utilitycost-tariff/#utilitycosttariff
        """

class AnyLifeCycleCostParameters:
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
    ) -> None:
        """Create a new ``LifeCycleCost:Parameters`` and add it to the document.

        Provides inputs related to the overall life-cycle analysis. It establishes many of the assumptions used in computing the present value. It is important that when comparing the results of multiple simulations that the fields in the LifeCycleCost:Parameters objects are the same for all the simulations. When this object is present the tabular report file will contain the Life-Cycle Cost Report.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/energyplus-economics/lifecyclecost-parameters/#lifecyclecostparameters
        """

class OutputJSON:
    def __call__(
        self,
        /,
        *,
        option_type: Literal["TimeSeries", "TimeSeriesAndTabular"],
        output_json: Literal["", "No", "Yes"] | None = "Yes",
        output_cbor: Literal["", "No", "Yes"] | None = "No",
        output_messagepack: Literal["", "No", "Yes"] | None = "No",
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
        """Create a new ``Output:JSON`` and add it to the document.

        Output from EnergyPlus can be written to JSON format files.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/input-for-output/#outputjson
        """
