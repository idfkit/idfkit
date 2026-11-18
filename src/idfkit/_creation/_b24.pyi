"""Creation signatures of generated classes (stub only).

DO NOT EDIT — regenerate with:
    python -m idfkit.codegen.generate_stubs
"""

from __future__ import annotations

from typing import Literal

from typing_extensions import Never

from .. import _generated_types as _g

class ZoneCapacitanceMultiplierResearchSpecial:
    def __call__(
        self,
        name: str,
        /,
        *,
        zone_or_zonelist_name: str | None = ...,
        temperature_capacity_multiplier: float | None = 1,
        humidity_capacity_multiplier: float | None = 1,
        carbon_dioxide_capacity_multiplier: float | None = 1,
        generic_contaminant_capacity_multiplier: float | None = 1,
    ) -> None:
        """Create a new ``ZoneCapacitanceMultiplier:ResearchSpecial`` and add it to the document.

        Multiplier altering the relative capacitance of the air compared to an empty zone

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-simulation-parameters/#zonecapacitancemultiplierresearchspecial
        """

class RunPeriodControlSpecialDays:
    def __call__(
        self,
        name: str,
        /,
        *,
        start_date: str,
        duration: float | None = 1,
        special_day_type: Literal["", "CustomDay1", "CustomDay2", "Holiday", "SummerDesignDay", "WinterDesignDay"]
        | None = "Holiday",
    ) -> None:
        """Create a new ``RunPeriodControl:SpecialDays`` and add it to the document.

        This object sets up holidays/special days to be used during weather file run periods. (These are not used with SizingPeriod:* objects.) Depending on the value in the run period, days on the weather file may also be used. However, the weather file specification will take precedence over any specification shown here. (No error message on duplicate days or overlapping days).

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-location-climate-weather-file-access/#runperiodcontrolspecialdays
        """

class SiteGroundReflectance:
    def __call__(
        self,
        /,
        *,
        january_ground_reflectance: float | None = 0.2,
        february_ground_reflectance: float | None = 0.2,
        march_ground_reflectance: float | None = 0.2,
        april_ground_reflectance: float | None = 0.2,
        may_ground_reflectance: float | None = 0.2,
        june_ground_reflectance: float | None = 0.2,
        july_ground_reflectance: float | None = 0.2,
        august_ground_reflectance: float | None = 0.2,
        september_ground_reflectance: float | None = 0.2,
        october_ground_reflectance: float | None = 0.2,
        november_ground_reflectance: float | None = 0.2,
        december_ground_reflectance: float | None = 0.2,
    ) -> None:
        """Create a new ``Site:GroundReflectance`` and add it to the document.

        Specifies the ground reflectance values used to calculate ground reflected solar. The ground reflectance can be further modified when snow is on the ground by Site:GroundReflectance:SnowModifier.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-location-climate-weather-file-access/#sitegroundreflectance
        """

class AnyMaterialPropertyPhaseChange:
    def __call__(
        self,
        name: str,
        /,
        *,
        narrow_with_as_version_first: Never,
        temperature_coefficient_for_thermal_conductivity: float | None = 0,
    ) -> None:
        """Create a new ``MaterialProperty:PhaseChange`` and add it to the document.

        Additional properties for temperature dependent thermal conductivity and enthalpy for Phase Change Materials (PCM) Name and temperature coefficient are followed by up to 100 sets of temperature-enthalpy pairs. HeatBalanceAlgorithm = CondFD(ConductionFiniteDifference) solution algorithm only. Constructions with this should use the detailed CondFD process. Has no effect with other HeatBalanceAlgorithm solution algorithms

        No call suits every release: narrow the document with ``as_version`` first.
        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-surface-construction-elements/#materialpropertyphasechange
        """

class ShadingOverhangProjection:
    def __call__(
        self,
        name: str,
        /,
        *,
        window_or_door_name: str,
        height_above_window_or_door: float | None = ...,
        tilt_angle_from_window_door: float | None = 90,
        left_extension_from_window_door_width: float | None = ...,
        right_extension_from_window_door_width: float | None = ...,
        depth_as_fraction_of_window_door_height: float | None = ...,
    ) -> None:
        """Create a new ``Shading:Overhang:Projection`` and add it to the document.

        Overhangs are typically flat shading surfaces that reference a window or door.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-thermal-zone-description-geometry/#shadingoverhangprojection
        """

class SurfacePropertyHeatBalanceSourceTerm:
    def __call__(
        self,
        /,
        *,
        surface_name: str,
        inside_face_heat_source_term_schedule_name: str | None = ...,
        outside_face_heat_source_term_schedule_name: str | None = ...,
    ) -> None:
        """Create a new ``SurfaceProperty:HeatBalanceSourceTerm`` and add it to the document.

        Allows an additional heat source term to be added to the inside or outside surface boundary. A heat source can be added to either or both the inside and outside of the same surface.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-advanced-surface-concepts/#surfacepropertyheatbalancesourceterm
        """

class SurfaceConvectionAlgorithmOutsideUserCurve:
    def __call__(
        self,
        name: str = "",
        /,
        *,
        wind_speed_type_for_curve: Literal[
            "", "HeightAdjust", "ParallelComponent", "ParallelComponentHeightAdjust", "WeatherFile"
        ]
        | None = "HeightAdjust",
        hf_function_of_wind_speed_curve_name: str | None = ...,
        hn_function_of_temperature_difference_curve_name: str | None = ...,
        hn_function_of_temperature_difference_divided_by_height_curve_name: str | None = ...,
    ) -> None:
        """Create a new ``SurfaceConvectionAlgorithm:Outside:UserCurve`` and add it to the document.

        Used to describe a custom model equation for surface convection heat transfer coefficient If more than one curve is referenced they are all used and added together.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-advanced-surface-concepts/#surfaceconvectionalgorithmoutsideusercurve
        """

class AnySurfacePropertySurroundingSurfaces:
    def __call__(
        self,
        name: str,
        /,
        *,
        sky_view_factor: float | None = ...,
        sky_temperature_schedule_name: str | None = ...,
        ground_view_factor: float | None = ...,
        ground_temperature_schedule_name: str | None = ...,
        surfaces: list[_g.SurfacePropertySurroundingSurfacesSurfacesItem] = ...,
    ) -> None:
        """Create a new ``SurfaceProperty:SurroundingSurfaces`` and add it to the document.

        This object defines a list of surrounding surfaces for an exterior surface.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-advanced-surface-concepts/#surfacepropertysurroundingsurfaces
        """

class SurfacePropertySurroundingSurfaces:
    def __call__(
        self,
        name: str,
        /,
        *,
        sky_view_factor: float | Literal["", "Autocalculate"] | None = "Autocalculate",
        sky_temperature_schedule_name: str | None = ...,
        ground_view_factor: float | Literal["", "Autocalculate"] | None = "Autocalculate",
        ground_temperature_schedule_name: str | None = ...,
        surfaces: list[_g.SurfacePropertySurroundingSurfacesSurfacesItem] = ...,
    ) -> None:
        """Create a new ``SurfaceProperty:SurroundingSurfaces`` and add it to the document.

        This object defines a list of surrounding surfaces for an exterior surface.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-advanced-surface-concepts/#surfacepropertysurroundingsurfaces
        """

class RoomAirTemperaturePatternTwoGradient:
    def __call__(
        self,
        /,
        *,
        room_air_temperature_pattern_two_gradient_name: str,
        control_integer_for_pattern_control_schedule_name: int,
        thermostat_height: float | None = ...,
        return_air_height: float | None = ...,
        exhaust_air_height: float | None = ...,
        temperature_gradient_lower_bound: float | None = ...,
        temperature_gradient_upper_bound: float | None = ...,
        gradient_interpolation_mode: Literal[
            "OutdoorDryBulbTemperature",
            "SensibleCoolingLoad",
            "SensibleHeatingLoad",
            "ZoneAndOutdoorTemperatureDifference",
            "ZoneDryBulbTemperature",
        ]
        | None = ...,
        upper_temperature_bound: float | None = ...,
        lower_temperature_bound: float | None = ...,
        upper_heat_rate_bound: float | None = ...,
        lower_heat_rate_bound: float | None = ...,
    ) -> None:
        """Create a new ``RoomAir:TemperaturePattern:TwoGradient`` and add it to the document.

        Used to model room air with two temperature gradients in the vertical direction. Used in combination with RoomAir:TemperaturePattern:UserDefined.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-room-air-models/#roomairtemperaturepatterntwogradient
        """

class RoomAirSettingsUnderFloorAirDistributionInterior:
    def __call__(
        self,
        /,
        *,
        zone_name: str,
        number_of_diffusers: float | Literal["", "Autocalculate"] | None = "Autocalculate",
        power_per_plume: float | Literal["", "Autocalculate"] | None = "Autocalculate",
        design_effective_area_of_diffuser: float | Literal["", "Autocalculate"] | None = "Autocalculate",
        diffuser_slot_angle_from_vertical: float | Literal["", "Autocalculate"] | None = "Autocalculate",
        thermostat_height: float | None = 1.2,
        comfort_height: float | None = 1.1,
        temperature_difference_threshold_for_reporting: float | None = 0.4,
        floor_diffuser_type: Literal["", "Custom", "HorizontalSwirl", "LinearBarGrille", "Swirl", "VariableArea"]
        | None = "Swirl",
        transition_height: float | Literal["", "Autocalculate"] | None = 1.7,
        coefficient_a: float | Literal["", "Autocalculate"] | None = "Autocalculate",
        coefficient_b: float | Literal["", "Autocalculate"] | None = "Autocalculate",
        coefficient_c: float | Literal["", "Autocalculate"] | None = "Autocalculate",
        coefficient_d: float | Literal["", "Autocalculate"] | None = "Autocalculate",
        coefficient_e: float | Literal["", "Autocalculate"] | None = "Autocalculate",
    ) -> None:
        """Create a new ``RoomAirSettings:UnderFloorAirDistributionInterior`` and add it to the document.

        This Room Air Model is applicable to interior spaces that are served by an underfloor air distribution system. The dominant sources of heat gain should be from people, equipment, and other localized sources located in the occupied part of the room. The model should be used with caution in zones which have large heat gains or losses through exterior walls or windows or which have considerable direct solar gain. Used with RoomAirModelType = UnderFloorAirDistributionInterior.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-room-air-models/#roomairsettingsunderfloorairdistributioninterior
        """

class SteamEquipmentInstance:
    def __call__(
        self,
        name: str,
        /,
        *,
        steam_equipment_definition_name: str,
        zone_or_zonelist_or_space_or_spacelist_name: str,
        schedule_name: str,
        multiplier: float | None = 1,
        end_use_subcategory: str | None = "General",
    ) -> None:
        """Create a new ``SteamEquipment:Instance`` and add it to the document.

        Sets internal gains for steam equipment in the zone. The physical characteristics are given by the referenced SteamEquipment:Definition object. If a ZoneList, SpaceList, or a Zone comprised of more than one Space is specified then this definition applies to all applicable spaces, and each instance will be named with the Space Name plus this Object Name.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-internal-gains/#steamequipmentinstance
        """

class ZoneContaminantSourceAndSinkGenericDecaySource:
    def __call__(
        self,
        name: str,
        /,
        *,
        zone_name: str,
        schedule_name: str,
        initial_emission_rate: float | None = ...,
        delay_time_constant: float | None = ...,
    ) -> None:
        """Create a new ``ZoneContaminantSourceAndSink:Generic:DecaySource`` and add it to the document.

        Simulate generic contaminant source driven by the cutoff concentration model.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-internal-gains-people-lights-other/#zonecontaminantsourceandsinkgenericdecaysource
        """

class AnyAirflowNetworkSimulationControl:
    def __call__(
        self,
        name: str,
        /,
        *,
        airflownetwork_control: Literal[
            "",
            "MultizoneWithDistribution",
            "MultizoneWithDistributionOnlyDuringFanOperation",
            "MultizoneWithoutDistribution",
            "NoMultizoneOrDistribution",
        ]
        | None = "NoMultizoneOrDistribution",
        wind_pressure_coefficient_type: Literal["", "Input", "SurfaceAverageCalculation"]
        | None = "SurfaceAverageCalculation",
        height_selection_for_local_wind_pressure_calculation: Literal["", "ExternalNode", "OpeningHeight"]
        | None = "OpeningHeight",
        building_type: Literal["", "HighRise", "LowRise"] | None = "LowRise",
        maximum_number_of_iterations: int | None = 500,
        initialization_type: Literal["", "LinearInitializationMethod", "ZeroNodePressures"]
        | None = "ZeroNodePressures",
        relative_airflow_convergence_tolerance: float | None = 0.0001,
        absolute_airflow_convergence_tolerance: float | None = ...,
        convergence_acceleration_limit: float | None = -0.5,
        azimuth_angle_of_long_axis_of_building: float | None = 0,
        ratio_of_building_width_along_short_axis_to_width_along_long_axis: float | None = 1,
        height_dependence_of_external_node_temperature: Literal["", "No", "Yes"] | None = "No",
        solver: Literal["", "ConjugateGradient", "SkylineLU"] | None = "SkylineLU",
    ) -> None:
        """Create a new ``AirflowNetwork:SimulationControl`` and add it to the document.

        This object defines the global parameters used in an Airflow Network simulation.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-airflow-network/#airflownetworksimulationcontrol
        """

class AirflowNetworkMultiZoneExternalNode:
    def __call__(
        self,
        name: str,
        /,
        *,
        wind_pressure_coefficient_curve_name: str,
        external_node_height: float | None = 0,
        symmetric_wind_pressure_coefficient_curve: Literal["", "No", "Yes"] | None = "No",
        wind_angle_type: Literal["", "Absolute", "Relative"] | None = "Absolute",
    ) -> None:
        """Create a new ``AirflowNetwork:MultiZone:ExternalNode`` and add it to the document.

        This object defines outdoor environmental conditions outside of the building.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-airflow-network/#airflownetworkmultizoneexternalnode
        """

class HVACTemplateSystemPackagedVAV:
    def __call__(
        self,
        name: str,
        /,
        *,
        system_availability_schedule_name: str | None = ...,
        supply_fan_maximum_flow_rate: float | Literal["", "Autosize"] | None = "Autosize",
        supply_fan_minimum_flow_rate: float | Literal["", "Autosize"] | None = "Autosize",
        supply_fan_placement: Literal["", "BlowThrough", "DrawThrough"] | None = "DrawThrough",
        supply_fan_total_efficiency: float | None = 0.7,
        supply_fan_delta_pressure: float | None = 1000,
        supply_fan_motor_efficiency: float | None = 0.9,
        supply_fan_motor_in_air_stream_fraction: float | None = 1,
        cooling_coil_type: Literal["", "TwoSpeedDX", "TwoSpeedHumidControlDX"] | None = "TwoSpeedDX",
        cooling_coil_availability_schedule_name: str | None = ...,
        cooling_coil_setpoint_schedule_name: str | None = ...,
        cooling_coil_design_setpoint: float | None = 12.8,
        cooling_coil_gross_rated_total_capacity: float | Literal["", "Autosize"] | None = "Autosize",
        cooling_coil_gross_rated_sensible_heat_ratio: float | Literal["", "Autosize"] | None = "Autosize",
        cooling_coil_gross_rated_cop: float | None = 3,
        heating_coil_type: Literal["", "Electric", "Gas", "HotWater", "None"] | None = "None",
        heating_coil_availability_schedule_name: str | None = ...,
        heating_coil_setpoint_schedule_name: str | None = ...,
        heating_coil_design_setpoint: float | None = 10,
        heating_coil_capacity: float | Literal["", "Autosize"] | None = "Autosize",
        gas_heating_coil_efficiency: float | None = 0.8,
        gas_heating_coil_parasitic_electric_load: float | None = 0,
        maximum_outdoor_air_flow_rate: float | Literal["", "Autosize"] | None = "Autosize",
        minimum_outdoor_air_flow_rate: float | Literal["", "Autosize"] | None = "Autosize",
        minimum_outdoor_air_control_type: Literal["", "FixedMinimum", "ProportionalMinimum"]
        | None = "ProportionalMinimum",
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
        supply_fan_part_load_power_coefficients: Literal[
            "",
            "ASHRAE90.1-2004AppendixG",
            "InletVaneDampers",
            "OutletDampers",
            "VariableSpeedMotor",
            "VariableSpeedMotorPressureReset",
        ]
        | None = "InletVaneDampers",
        night_cycle_control: Literal["", "CycleOnAny", "CycleOnAnyZoneFansOnly", "CycleOnControlZone", "StayOff"]
        | None = "StayOff",
        night_cycle_control_zone_name: str | None = ...,
        heat_recovery_type: Literal["", "Enthalpy", "None", "Sensible"] | None = "None",
        sensible_heat_recovery_effectiveness: float | None = 0.7,
        latent_heat_recovery_effectiveness: float | None = 0.65,
        cooling_coil_setpoint_reset_type: Literal[
            "", "None", "OutdoorAirTemperatureReset", "Warmest", "WarmestTemperatureFirst"
        ]
        | None = "None",
        heating_coil_setpoint_reset_type: Literal["", "None", "OutdoorAirTemperatureReset"] | None = "None",
        dehumidification_control_type: Literal["", "CoolReheat", "None"] | None = "None",
        dehumidification_control_zone_name: str | None = ...,
        dehumidification_setpoint: float | None = 60,
        humidifier_type: Literal["", "ElectricSteam", "None"] | None = "None",
        humidifier_availability_schedule_name: str | None = ...,
        humidifier_rated_capacity: float | None = ...,
        humidifier_rated_electric_power: float | Literal["", "Autosize"] | None = "Autosize",
        humidifier_control_zone_name: str | None = ...,
        humidifier_setpoint: float | None = 30,
        sizing_option: Literal["", "Coincident", "NonCoincident"] | None = "NonCoincident",
        return_fan: Literal["", "No", "Yes"] | None = "No",
        return_fan_total_efficiency: float | None = 0.7,
        return_fan_delta_pressure: float | None = 500,
        return_fan_motor_efficiency: float | None = 0.9,
        return_fan_motor_in_air_stream_fraction: float | None = 1,
        return_fan_part_load_power_coefficients: Literal[
            "",
            "ASHRAE90.1-2004AppendixG",
            "InletVaneDampers",
            "OutletDampers",
            "VariableSpeedMotor",
            "VariableSpeedMotorPressureReset",
        ]
        | None = "InletVaneDampers",
    ) -> None:
        """Create a new ``HVACTemplate:System:PackagedVAV`` and add it to the document.

        Packaged Variable Air Volume (PVAV) air loop with optional heating coil and optional preheat.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/hvac-template-objects/group-hvac-templates/#hvactemplatesystempackagedvav
        """

class HVACTemplatePlantChillerObjectReference:
    def __call__(
        self,
        name: str,
        /,
        *,
        chiller_name: str,
        chiller_object_type: Literal["", "Chiller:Electric:EIR", "Chiller:Electric:ReformulatedEIR"]
        | None = "Chiller:Electric:EIR",
        priority: float | None = ...,
    ) -> None:
        """Create a new ``HVACTemplate:Plant:Chiller:ObjectReference`` and add it to the document.

        This object references a detailed chiller object and adds it to an HVACTemplate:Plant:ChilledWaterLoop. The user must create a complete detailed chiller object with all required curve or performance objects.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/hvac-template-objects/group-hvac-templates/#hvactemplateplantchillerobjectreference
        """

class AnyZoneHVACCoolingPanelRadiantConvectiveWater:
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
            "ZoneTotalLoad",
            "ZoneConvectiveLoad",
        ]
        | None = "MeanAirTemperature",
        cooling_control_throttling_range: float | None = 0.5,
        cooling_control_temperature_schedule_name: str | None = ...,
        condensation_control_type: Literal["", "Off", "SimpleOff", "VariableOff"] | None = "SimpleOff",
        condensation_control_dewpoint_offset: float | None = 1,
        fraction_of_radiant_energy_incident_on_people: float | None = ...,
        surface_fractions: list[_g.ZoneHVACCoolingPanelRadiantConvectiveWaterSurfaceFractionsItem] = ...,
    ) -> None:
        """Create a new ``ZoneHVAC:CoolingPanel:RadiantConvective:Water`` and add it to the document.

        The number of surfaces can be expanded beyond 100, if necessary, by adding more groups to the end of the list

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-radiative-convective-units/#zonehvaccoolingpanelradiantconvectivewater
        """

class ZoneHVACLowTemperatureRadiantSurfaceGroup:
    def __call__(
        self,
        name: str,
        /,
        *,
        surface_fractions: list[_g.ZoneHVACLowTemperatureRadiantSurfaceGroupSurfaceFractionsItem] = ...,
    ) -> None:
        """Create a new ``ZoneHVAC:LowTemperatureRadiant:SurfaceGroup`` and add it to the document.

        This is used to allow the coordinate control of several radiant system surfaces. Note that the following flow fractions must sum up to 1.0 The number of surfaces can be expanded beyond 100, if necessary, by adding more groups to the end of the list

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-radiative-convective-units/#zonehvaclowtemperatureradiantsurfacegroup
        """

class AnyAirTerminalSingleDuctVAVNoReheat:
    def __call__(
        self,
        name: str,
        /,
        *,
        air_outlet_node_name: str,
        air_inlet_node_name: str,
        maximum_air_flow_rate: float | Literal["Autosize"],
        availability_schedule_name: str | None = ...,
        zone_minimum_air_flow_input_method: Literal["", "Constant", "FixedFlowRate", "Scheduled"] | None = "Constant",
        constant_minimum_air_flow_fraction: float | Literal["", "Autosize"] | None = "Autosize",
        fixed_minimum_air_flow_rate: float | Literal["", "Autosize"] | None = "Autosize",
        minimum_air_flow_fraction_schedule_name: str | None = ...,
        design_specification_outdoor_air_object_name: str | None = ...,
    ) -> None:
        """Create a new ``AirTerminal:SingleDuct:VAV:NoReheat`` and add it to the document.

        Central air system terminal unit, single duct, variable volume, with no reheat coil.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-zone-hvac-air-loop-terminal-units/#airterminalsingleductvavnoreheat
        """

class ZoneHVACAirDistributionUnit:
    def __call__(
        self,
        name: str,
        /,
        *,
        air_distribution_unit_outlet_node_name: str,
        air_terminal_object_type: Literal[
            "AirTerminal:DualDuct:ConstantVolume",
            "AirTerminal:DualDuct:VAV",
            "AirTerminal:DualDuct:VAV:OutdoorAir",
            "AirTerminal:SingleDuct:ConstantVolume:CooledBeam",
            "AirTerminal:SingleDuct:ConstantVolume:FourPipeBeam",
            "AirTerminal:SingleDuct:ConstantVolume:FourPipeInduction",
            "AirTerminal:SingleDuct:ConstantVolume:NoReheat",
            "AirTerminal:SingleDuct:ConstantVolume:Reheat",
            "AirTerminal:SingleDuct:Mixer",
            "AirTerminal:SingleDuct:ParallelPIU:Reheat",
            "AirTerminal:SingleDuct:SeriesPIU:Reheat",
            "AirTerminal:SingleDuct:UserDefined",
            "AirTerminal:SingleDuct:VAV:HeatAndCool:NoReheat",
            "AirTerminal:SingleDuct:VAV:HeatAndCool:Reheat",
            "AirTerminal:SingleDuct:VAV:NoReheat",
            "AirTerminal:SingleDuct:VAV:Reheat",
            "AirTerminal:SingleDuct:VAV:Reheat:VariableSpeedFan",
        ],
        air_terminal_name: str,
        nominal_upstream_leakage_fraction: float | None = 0,
        constant_downstream_leakage_fraction: float | None = 0,
        design_specification_air_terminal_sizing_object_name: str | None = ...,
    ) -> None:
        """Create a new ``ZoneHVAC:AirDistributionUnit`` and add it to the document.

        Central air system air distribution unit, serves as a wrapper for a specific type of air terminal unit. This object is referenced in a ZoneHVAC:EquipmentList.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-zone-equipment/#zonehvacairdistributionunit
        """

class AnyCoilHeatingDXMultiSpeed:
    def __call__(
        self,
        name: str,
        /,
        *,
        air_inlet_node_name: str,
        air_outlet_node_name: str,
        fuel_type: Literal["Diesel", "Electricity", "Gasoline", "NaturalGas", "OtherFuel1", "OtherFuel2", "Propane"],
        number_of_speeds: int,
        speed_1_gross_rated_heating_capacity: float | Literal["Autosize"],
        speed_1_gross_rated_heating_cop: float,
        speed_1_rated_air_flow_rate: float | Literal["Autosize"],
        speed_1_heating_capacity_function_of_temperature_curve_name: str,
        speed_1_heating_capacity_function_of_flow_fraction_curve_name: str,
        speed_1_energy_input_ratio_function_of_temperature_curve_name: str,
        speed_1_energy_input_ratio_function_of_flow_fraction_curve_name: str,
        speed_1_part_load_fraction_correlation_curve_name: str,
        speed_2_gross_rated_heating_capacity: float | Literal["Autosize"],
        speed_2_gross_rated_heating_cop: float,
        speed_2_rated_air_flow_rate: float | Literal["Autosize"],
        speed_2_heating_capacity_function_of_temperature_curve_name: str,
        speed_2_heating_capacity_function_of_flow_fraction_curve_name: str,
        speed_2_energy_input_ratio_function_of_temperature_curve_name: str,
        speed_2_energy_input_ratio_function_of_flow_fraction_curve_name: str,
        speed_2_part_load_fraction_correlation_curve_name: str,
        availability_schedule_name: str | None = ...,
        minimum_outdoor_dry_bulb_temperature_for_compressor_operation: float | None = -8,
        outdoor_dry_bulb_temperature_to_turn_on_compressor: float | None = ...,
        crankcase_heater_capacity: float | None = 0,
        maximum_outdoor_dry_bulb_temperature_for_crankcase_heater_operation: float | None = 10,
        defrost_energy_input_ratio_function_of_temperature_curve_name: str | None = ...,
        maximum_outdoor_dry_bulb_temperature_for_defrost_operation: float | None = 5,
        defrost_strategy: Literal["", "Resistive", "ReverseCycle"] | None = "ReverseCycle",
        defrost_control: Literal["", "OnDemand", "Timed"] | None = "Timed",
        defrost_time_period_fraction: float | None = 0.058333,
        resistive_defrost_heater_capacity: float | Literal["", "Autosize"] | None = 0,
        apply_part_load_fraction_to_speeds_greater_than_1: Literal["", "No", "Yes"] | None = "No",
        region_number_for_calculating_hspf: int | None = 4,
        speed_1_rated_waste_heat_fraction_of_power_input: float | None = 0.2,
        speed_1_waste_heat_function_of_temperature_curve_name: str | None = ...,
        speed_2_rated_waste_heat_fraction_of_power_input: float | None = 0.2,
        speed_2_waste_heat_function_of_temperature_curve_name: str | None = ...,
        speed_3_gross_rated_heating_capacity: float | Literal["Autosize"] | None = ...,
        speed_3_gross_rated_heating_cop: float | None = ...,
        speed_3_rated_air_flow_rate: float | Literal["Autosize"] | None = ...,
        speed_3_heating_capacity_function_of_temperature_curve_name: str | None = ...,
        speed_3_heating_capacity_function_of_flow_fraction_curve_name: str | None = ...,
        speed_3_energy_input_ratio_function_of_temperature_curve_name: str | None = ...,
        speed_3_energy_input_ratio_function_of_flow_fraction_curve_name: str | None = ...,
        speed_3_part_load_fraction_correlation_curve_name: str | None = ...,
        speed_3_rated_waste_heat_fraction_of_power_input: float | None = 0.2,
        speed_3_waste_heat_function_of_temperature_curve_name: str | None = ...,
        speed_4_gross_rated_heating_capacity: float | Literal["Autosize"] | None = ...,
        speed_4_gross_rated_heating_cop: float | None = ...,
        speed_4_rated_air_flow_rate: float | Literal["Autosize"] | None = ...,
        speed_4_heating_capacity_function_of_temperature_curve_name: str | None = ...,
        speed_4_heating_capacity_function_of_flow_fraction_curve_name: str | None = ...,
        speed_4_energy_input_ratio_function_of_temperature_curve_name: str | None = ...,
        speed_4_energy_input_ratio_function_of_flow_fraction_curve_name: str | None = ...,
        speed_4_part_load_fraction_correlation_curve_name: str | None = ...,
        speed_4_rated_waste_heat_fraction_of_power_input: float | None = 0.2,
        speed_4_waste_heat_function_of_temperature_curve_name: str | None = ...,
        zone_name_for_evaporator_placement: str | None = ...,
        speed_1_secondary_coil_air_flow_rate: float | Literal["Autosize"] | None = ...,
        speed_1_secondary_coil_fan_flow_scaling_factor: float | None = 1.25,
        speed_1_nominal_sensible_heat_ratio_of_secondary_coil: float | None = ...,
        speed_1_sensible_heat_ratio_modifier_function_of_temperature_curve_name: str | None = ...,
        speed_1_sensible_heat_ratio_modifier_function_of_flow_fraction_curve_name: str | None = ...,
        speed_2_secondary_coil_air_flow_rate: float | Literal["Autosize"] | None = ...,
        speed_2_secondary_coil_fan_flow_scaling_factor: float | None = 1.25,
        speed_2_nominal_sensible_heat_ratio_of_secondary_coil: float | None = ...,
        speed_2_sensible_heat_ratio_modifier_function_of_temperature_curve_name: str | None = ...,
        speed_2_sensible_heat_ratio_modifier_function_of_flow_fraction_curve_name: str | None = ...,
        speed_3_secondary_coil_air_flow_rate: float | Literal["Autosize"] | None = ...,
        speed_3_secondary_coil_fan_flow_scaling_factor: float | None = 1.25,
        speed_3_nominal_sensible_heat_ratio_of_secondary_coil: float | None = ...,
        speed_3_sensible_heat_ratio_modifier_function_of_temperature_curve_name: str | None = ...,
        speed_3_sensible_heat_ratio_modifier_function_of_flow_fraction_curve_name: str | None = ...,
        speed_4_secondary_coil_air_flow_rate: float | Literal["Autosize"] | None = ...,
        speed_4_secondary_coil_fan_flow_scaling_factor: float | None = 1.25,
        speed_4_nominal_sensible_heat_ratio_of_secondary_coil: float | None = ...,
        speed_4_sensible_heat_ratio_modifier_function_of_temperature_curve_name: str | None = ...,
        speed_4_sensible_heat_ratio_modifier_function_of_flow_fraction_curve_name: str | None = ...,
    ) -> None:
        """Create a new ``Coil:Heating:DX:MultiSpeed`` and add it to the document.

        Direct expansion (DX) heating coil (air-to-air heat pump) and compressor unit (includes electric or engine-driven compressor and outdoor fan), multi-speed (or variable-speed), with defrost controls. Requires two to four sets of performance data and will interpolate between speeds.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-heating-and-cooling-coils/#coilheatingdxmultispeed
        """

class AnyHeatPumpWaterToWaterEquationFitHeating:
    def __call__(
        self,
        name: str,
        /,
        *,
        narrow_with_as_version_first: Never,
        source_side_inlet_node_name: str,
        source_side_outlet_node_name: str,
        load_side_inlet_node_name: str,
        load_side_outlet_node_name: str,
        reference_load_side_flow_rate: float | Literal["Autosize"],
        reference_source_side_flow_rate: float | Literal["Autosize"],
        reference_heating_capacity: float | Literal["Autosize"],
        reference_heating_power_consumption: float | Literal["Autosize"],
        reference_coefficient_of_performance: float | None = 7.5,
        sizing_factor: float | None = 1,
        companion_cooling_heat_pump_name: str | None = ...,
    ) -> None:
        """Create a new ``HeatPump:WaterToWater:EquationFit:Heating`` and add it to the document.

        simple water-water hp curve-fit model

        No call suits every release: narrow the document with ``as_version`` first.
        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-plant-equipment/#heatpumpwatertowaterequationfitheating
        """

class GroundHeatExchangerSlinky:
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

class PlantEquipmentOperationThermalEnergyStorage:
    def __call__(
        self,
        name: str,
        /,
        *,
        on_peak_schedule: str,
        charging_availability_schedule: str,
        non_charging_chilled_water_temperature: float,
        charging_chilled_water_temperature: float,
        component_1_object_type: Literal[
            "Chiller:Absorption",
            "Chiller:Absorption:Indirect",
            "Chiller:CombustionTurbine",
            "Chiller:ConstantCOP",
            "Chiller:Electric",
            "Chiller:Electric:EIR",
            "Chiller:Electric:ReformulatedEIR",
            "Chiller:EngineDriven",
            "ThermalStorage:Ice:Detailed",
            "ThermalStorage:Ice:Simple",
        ],
        component_1_name: str,
        component_1_demand_calculation_node_name: str,
        component_1_setpoint_node_name: str,
        component_1_flow_rate: float | Literal["Autosize"],
        component_1_operation_type: Literal["Cooling", "Dual", "Heating"],
        component_2_object_type: Literal[
            "Chiller:Absorption",
            "Chiller:Absorption:Indirect",
            "Chiller:CombustionTurbine",
            "Chiller:ConstantCOP",
            "Chiller:Electric",
            "Chiller:Electric:EIR",
            "Chiller:Electric:ReformulatedEIR",
            "Chiller:EngineDriven",
            "ThermalStorage:Ice:Detailed",
            "ThermalStorage:Ice:Simple",
        ]
        | None = ...,
        component_2_name: str | None = ...,
        component_2_demand_calculation_node_name: str | None = ...,
        component_2_setpoint_node_name: str | None = ...,
        component_2_flow_rate: float | Literal["Autosize"] | None = ...,
        component_2_operation_type: Literal["Cooling", "Dual", "Heating"] | None = ...,
        component_3_object_type: Literal[
            "Chiller:Absorption",
            "Chiller:Absorption:Indirect",
            "Chiller:CombustionTurbine",
            "Chiller:ConstantCOP",
            "Chiller:Electric",
            "Chiller:Electric:EIR",
            "Chiller:Electric:ReformulatedEIR",
            "Chiller:EngineDriven",
            "ThermalStorage:Ice:Detailed",
            "ThermalStorage:Ice:Simple",
        ]
        | None = ...,
        component_3_name: str | None = ...,
        component_3_demand_calculation_node_name: str | None = ...,
        component_3_setpoint_node_name: str | None = ...,
        component_3_flow_rate: float | Literal["Autosize"] | None = ...,
        component_3_operation_type: Literal["Cooling", "Dual", "Heating"] | None = ...,
        component_4_object_type: Literal[
            "Chiller:Absorption",
            "Chiller:Absorption:Indirect",
            "Chiller:CombustionTurbine",
            "Chiller:ConstantCOP",
            "Chiller:Electric",
            "Chiller:Electric:ASHRAE205",
            "Chiller:Electric:EIR",
            "Chiller:Electric:ReformulatedEIR",
            "Chiller:EngineDriven",
            "ThermalStorage:Ice:Detailed",
            "ThermalStorage:Ice:Simple",
        ]
        | None = ...,
        component_4_name: str | None = ...,
        component_4_demand_calculation_node_name: str | None = ...,
        component_4_setpoint_node_name: str | None = ...,
        component_4_flow_rate: float | Literal["Autosize"] | None = ...,
        component_4_operation_type: Literal["Cooling", "Dual", "Heating"] | None = ...,
        component_5_object_type: Literal[
            "Chiller:Absorption",
            "Chiller:Absorption:Indirect",
            "Chiller:CombustionTurbine",
            "Chiller:ConstantCOP",
            "Chiller:Electric",
            "Chiller:Electric:ASHRAE205",
            "Chiller:Electric:EIR",
            "Chiller:Electric:ReformulatedEIR",
            "Chiller:EngineDriven",
            "ThermalStorage:Ice:Detailed",
            "ThermalStorage:Ice:Simple",
        ]
        | None = ...,
        component_5_name: str | None = ...,
        component_5_demand_calculation_node_name: str | None = ...,
        component_5_setpoint_node_name: str | None = ...,
        component_5_flow_rate: float | Literal["Autosize"] | None = ...,
        component_5_operation_type: Literal["Cooling", "Dual", "Heating"] | None = ...,
        component_6_object_type: Literal[
            "Chiller:Absorption",
            "Chiller:Absorption:Indirect",
            "Chiller:CombustionTurbine",
            "Chiller:ConstantCOP",
            "Chiller:Electric",
            "Chiller:Electric:ASHRAE205",
            "Chiller:Electric:EIR",
            "Chiller:Electric:ReformulatedEIR",
            "Chiller:EngineDriven",
            "ThermalStorage:Ice:Detailed",
            "ThermalStorage:Ice:Simple",
        ]
        | None = ...,
        component_6_name: str | None = ...,
        component_6_demand_calculation_node_name: str | None = ...,
        component_6_setpoint_node_name: str | None = ...,
        component_6_flow_rate: float | Literal["Autosize"] | None = ...,
        component_6_operation_type: Literal["Cooling", "Dual", "Heating"] | None = ...,
        component_7_object_type: Literal[
            "Chiller:Absorption",
            "Chiller:Absorption:Indirect",
            "Chiller:CombustionTurbine",
            "Chiller:ConstantCOP",
            "Chiller:Electric",
            "Chiller:Electric:ASHRAE205",
            "Chiller:Electric:EIR",
            "Chiller:Electric:ReformulatedEIR",
            "Chiller:EngineDriven",
            "ThermalStorage:Ice:Detailed",
            "ThermalStorage:Ice:Simple",
        ]
        | None = ...,
        component_7_name: str | None = ...,
        component_7_demand_calculation_node_name: str | None = ...,
        component_7_setpoint_node_name: str | None = ...,
        component_7_flow_rate: float | Literal["Autosize"] | None = ...,
        component_7_operation_type: Literal["Cooling", "Dual", "Heating"] | None = ...,
        component_8_object_type: Literal[
            "Chiller:Absorption",
            "Chiller:Absorption:Indirect",
            "Chiller:CombustionTurbine",
            "Chiller:ConstantCOP",
            "Chiller:Electric",
            "Chiller:Electric:ASHRAE205",
            "Chiller:Electric:EIR",
            "Chiller:Electric:ReformulatedEIR",
            "Chiller:EngineDriven",
            "ThermalStorage:Ice:Detailed",
            "ThermalStorage:Ice:Simple",
        ]
        | None = ...,
        component_8_name: str | None = ...,
        component_8_demand_calculation_node_name: str | None = ...,
        component_8_setpoint_node_name: str | None = ...,
        component_8_flow_rate: float | Literal["Autosize"] | None = ...,
        component_8_operation_type: Literal["Cooling", "Dual", "Heating"] | None = ...,
        component_9_object_type: Literal[
            "Chiller:Absorption",
            "Chiller:Absorption:Indirect",
            "Chiller:CombustionTurbine",
            "Chiller:ConstantCOP",
            "Chiller:Electric",
            "Chiller:Electric:ASHRAE205",
            "Chiller:Electric:EIR",
            "Chiller:Electric:ReformulatedEIR",
            "Chiller:EngineDriven",
            "ThermalStorage:Ice:Detailed",
            "ThermalStorage:Ice:Simple",
        ]
        | None = ...,
        component_9_name: str | None = ...,
        component_9_demand_calculation_node_name: str | None = ...,
        component_9_setpoint_node_name: str | None = ...,
        component_9_flow_rate: float | Literal["Autosize"] | None = ...,
        component_9_operation_type: Literal["Cooling", "Dual", "Heating"] | None = ...,
        component_10_object_type: Literal[
            "Chiller:Absorption",
            "Chiller:Absorption:Indirect",
            "Chiller:CombustionTurbine",
            "Chiller:ConstantCOP",
            "Chiller:Electric",
            "Chiller:Electric:ASHRAE205",
            "Chiller:Electric:EIR",
            "Chiller:Electric:ReformulatedEIR",
            "Chiller:EngineDriven",
            "ThermalStorage:Ice:Detailed",
            "ThermalStorage:Ice:Simple",
        ]
        | None = ...,
        component_10_name: str | None = ...,
        component_10_demand_calculation_node_name: str | None = ...,
        component_10_setpoint_node_name: str | None = ...,
        component_10_flow_rate: float | Literal["Autosize"] | None = ...,
        component_10_operation_type: Literal["Cooling", "Dual", "Heating"] | None = ...,
    ) -> None:
        """Create a new ``PlantEquipmentOperation:ThermalEnergyStorage`` and add it to the document.

        Plant equipment operation scheme for simpler input to control thermal (ice) energy storage systems. It replaces a host of setpoint managers with simple, single input values. For more complex controls, use the ComponentSetpoint scheme.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-plant-condenser-control/#plantequipmentoperationthermalenergystorage
        """

class EnergyManagementSystemSubroutine:
    def __call__(self, name: str, /, *, lines: list[_g.EnergyManagementSystemSubroutineLinesItem] = ...) -> None:
        """Create a new ``EnergyManagementSystem:Subroutine`` and add it to the document.

        This input defines an Erl program subroutine Each field after the name is a line of EMS Runtime Language

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-energy-management-system-ems/#energymanagementsystemsubroutine
        """

class ExternalInterfaceActuator:
    def __call__(
        self,
        name: str,
        /,
        *,
        actuated_component_unique_name: str,
        actuated_component_type: str,
        actuated_component_control_type: str,
        optional_initial_value: float | None = ...,
    ) -> None:
        """Create a new ``ExternalInterface:Actuator`` and add it to the document.

        Hardware portion of EMS used to set up actuators in the model

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-externalinterface/#externalinterfaceactuator
        """

class AvailabilityManagerScheduledOn:
    def __call__(self, name: str, /, *, schedule_name: str) -> None:
        """Create a new ``AvailabilityManager:ScheduledOn`` and add it to the document.

        Determines the availability of a loop or system: only controls the turn on action. Schedule overrides fan/pump schedule.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-system-availability-managers/#availabilitymanagerscheduledon
        """

class SetpointManagerSingleZoneOneStageHeating:
    def __call__(
        self,
        name: str,
        /,
        *,
        control_zone_name: str,
        setpoint_node_or_nodelist_name: str,
        heating_stage_on_supply_air_setpoint_temperature: float | None = 99,
        heating_stage_off_supply_air_setpoint_temperature: float | None = -99,
    ) -> None:
        """Create a new ``SetpointManager:SingleZone:OneStageHeating`` and add it to the document.

        This object can be used with CoilSystem:Heating:DX, Coil:Heating:Fuel, Coil:Heating:Electric to model on/off cycling control of single stage air systems. Setpoints are modulated to run coil full on or full off depending on zone conditions. Intended for use with ZoneControl:Thermostat:StagedDualSetpoint.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-setpoint-managers/#setpointmanagersinglezoneonestageheating
        """

class RefrigerationSubcooler:
    def __call__(
        self,
        name: str,
        /,
        *,
        subcooler_type: Literal["", "LiquidSuction", "Mechanical"] | None = "LiquidSuction",
        liquid_suction_design_subcooling_temperature_difference: float | None = ...,
        design_liquid_inlet_temperature: float | None = ...,
        design_vapor_inlet_temperature: float | None = ...,
        capacity_providing_system: str | None = ...,
        outlet_control_temperature: float | None = ...,
    ) -> None:
        """Create a new ``Refrigeration:Subcooler`` and add it to the document.

        Two types of subcoolers are modeled by the detailed refrigeration system. The liquid suction heat exchanger uses cool suction gas to subcool the hot condensate after it leaves the condenser and before it reaches the thermal expansion valve. A mechanical subcooler is used to transfer cooling capacity from one refrigeration system to another.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-refrigeration/#refrigerationsubcooler
        """

class GeneratorFuelCellWaterSupply:
    def __call__(
        self,
        name: str,
        /,
        *,
        reformer_water_flow_rate_function_of_fuel_rate_curve_name: str | None = ...,
        reformer_water_pump_power_function_of_fuel_rate_curve_name: str | None = ...,
        pump_heat_loss_factor: float | None = ...,
        water_temperature_modeling_mode: Literal[
            "MainsWaterTemperature", "TemperatureFromAirNode", "TemperatureFromSchedule", "TemperatureFromWaterNode"
        ]
        | None = ...,
        water_temperature_reference_node_name: str | None = ...,
        water_temperature_schedule_name: str | None = ...,
    ) -> None:
        """Create a new ``Generator:FuelCell:WaterSupply`` and add it to the document.

        Used to provide details of the water supply subsystem for a fuel cell power generator. This water is used for steam reforming of the fuel and is not the same as the water used for thermal heat recovery.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-electric-load-center-generator/#generatorfuelcellwatersupply
        """

class GeneratorFuelCellInverter:
    def __call__(
        self,
        name: str,
        /,
        *,
        inverter_efficiency_calculation_mode: Literal["Constant", "Quadratic"] | None = ...,
        inverter_efficiency: float | None = ...,
        efficiency_function_of_dc_power_curve_name: str | None = ...,
    ) -> None:
        """Create a new ``Generator:FuelCell:Inverter`` and add it to the document.

        Used to describe the power condition unit subsystem of a fuel cell power generator. This object models an inverter system contained within a fuel cell system that converts from direct current (DC) to alternating current (AC).

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-electric-load-center-generator/#generatorfuelcellinverter
        """

class ComponentCostAdjustments:
    def __call__(
        self,
        /,
        *,
        miscellaneous_cost_per_conditioned_area: float | None = ...,
        design_and_engineering_fees: float | None = ...,
        contractor_fee: float | None = ...,
        contingency: float | None = ...,
        permits_bonding_and_insurance: float | None = ...,
        commissioning_fee: float | None = ...,
        regional_adjustment_factor: float | None = ...,
    ) -> None:
        """Create a new ``ComponentCost:Adjustments`` and add it to the document.

        Used to perform various modifications to the construction costs to arrive at an estimate for total project costs. This object allows extending the line item model so that the overall costs of the project will reflect various profit and fees.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/energyplus-economics/cost-estimating/#componentcostadjustments
        """

class OutputControlResilienceSummaries:
    def __call__(self, /, *, heat_index_algorithm: Literal["", "Extended", "Simplified"] | None = "Simplified") -> None:
        """Create a new ``OutputControl:ResilienceSummaries`` and add it to the document.

        Specifies methods for resilience reporting variables

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/input-for-output/#outputcontrolresiliencesummaries
        """

class OutputVariable:
    def __call__(
        self,
        /,
        *,
        variable_name: str,
        key_value: str | None = "*",
        reporting_frequency: Literal[
            "", "Annual", "Daily", "Detailed", "Environment", "Hourly", "Monthly", "RunPeriod", "Timestep"
        ]
        | None = "Hourly",
        schedule_name: str | None = ...,
    ) -> None:
        """Create a new ``Output:Variable`` and add it to the document.

        each Output:Variable command picks variables to be put onto the standard output file (.eso) some variables may not be reported for every simulation. a list of variables that can be reported are available after a run on the report dictionary file (.rdd) if the Output:VariableDictionary has been requested.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/input-for-output/#outputvariable
        """
