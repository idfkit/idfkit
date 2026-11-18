"""Creation signatures of generated classes (stub only).

DO NOT EDIT — regenerate with:
    python -m idfkit.codegen.generate_stubs
"""

from __future__ import annotations

from typing import Literal

from typing_extensions import Never

from .. import _generated_types as _g

class AnyBuilding:
    def __call__(
        self,
        name: str = "",
        /,
        *,
        north_axis: float | None = 0,
        terrain: Literal["", "City", "Country", "Ocean", "Suburbs", "Urban"] | None = "Suburbs",
        loads_convergence_tolerance_value: float | None = 0.04,
        temperature_convergence_tolerance_value: float | None = 0.4,
        solar_distribution: Literal[
            "",
            "FullExterior",
            "FullExteriorWithReflections",
            "FullInteriorAndExterior",
            "FullInteriorAndExteriorWithReflections",
            "MinimalShadowing",
        ]
        | None = "FullExterior",
        maximum_number_of_warmup_days: int | None = 25,
        minimum_number_of_warmup_days: int | None = ...,
    ) -> None:
        """Create a new ``Building`` and add it to the document.

        Describes parameters that are used during the simulation of the building. There are necessary correlations between the entries for this object and some entries in the Site:WeatherStation and Site:HeightVariation objects, specifically the Terrain field.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-simulation-parameters/#building
        """

class ZoneAirHeatBalanceAlgorithm:
    def __call__(
        self,
        /,
        *,
        algorithm: Literal["", "AnalyticalSolution", "EulerMethod", "ThirdOrderBackwardDifference"]
        | None = "ThirdOrderBackwardDifference",
        do_space_heat_balance_for_sizing: Literal["", "No", "Yes"] | None = "No",
        do_space_heat_balance_for_simulation: Literal["", "No", "Yes"] | None = "No",
    ) -> None:
        """Create a new ``ZoneAirHeatBalanceAlgorithm`` and add it to the document.

        Controls the zone/space air heat balance.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-simulation-parameters/#zoneairheatbalancealgorithm
        """

class SiteWeatherStation:
    def __call__(
        self,
        /,
        *,
        wind_sensor_height_above_ground: float | None = 10,
        wind_speed_profile_exponent: float | None = 0.14,
        wind_speed_profile_boundary_layer_thickness: float | None = 270,
        air_temperature_sensor_height_above_ground: float | None = 1.5,
    ) -> None:
        """Create a new ``Site:WeatherStation`` and add it to the document.

        This object should only be used for non-standard weather data. Standard weather data such as TMY2, IWEC, and ASHRAE design day data are all measured at the default conditions and do not require this object.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-location-climate-weather-file-access/#siteweatherstation
        """

class SiteSolarAndVisibleSpectrum:
    def __call__(
        self,
        name: str,
        /,
        *,
        spectrum_data_method: Literal["", "Default", "UserDefined"] | None = "Default",
        solar_spectrum_data_object_name: str | None = ...,
        visible_spectrum_data_object_name: str | None = ...,
    ) -> None:
        """Create a new ``Site:SolarAndVisibleSpectrum`` and add it to the document.

        If this object is omitted, the default solar and visible spectrum data will be used.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-location-climate-weather-file-access/#sitesolarandvisiblespectrum
        """

class WindowThermalModelParams:
    def __call__(
        self,
        name: str,
        /,
        *,
        standard: Literal["", "EN673Declared", "EN673Design", "ISO15099"] | None = "ISO15099",
        thermal_model: Literal[
            "",
            "ConvectiveScalarModel_NoSDThickness",
            "ConvectiveScalarModel_withSDThickness",
            "ISO15099",
            "ScaledCavityWidth",
        ]
        | None = "ISO15099",
        sdscalar: float | None = 1,
        deflection_model: Literal["", "MeasuredDeflection", "NoDeflection", "TemperatureAndPressureInput"]
        | None = "NoDeflection",
        vacuum_pressure_limit: float | None = 13.238,
        initial_temperature: float | None = 25,
        initial_pressure: float | None = 101325,
    ) -> None:
        """Create a new ``WindowThermalModel:Params`` and add it to the document.

        object is used to select which thermal model should be used in tarcog simulations

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-surface-construction-elements/#windowthermalmodelparams
        """

class AnyWallAdiabatic:
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
    ) -> None:
        """Create a new ``Wall:Adiabatic`` and add it to the document.

        Allows for simplified entry of interior walls.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-thermal-zone-description-geometry/#walladiabatic
        """

class AnySurfacePropertyConvectionCoefficients:
    def __call__(
        self,
        /,
        *,
        surface_name: str,
        convection_coefficient_1_location: Literal["Inside", "Outside"],
        convection_coefficient_1_type: Literal[
            "ASHRAEVerticalWall",
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

class GroundHeatTransferBasementMatlProps:
    def __call__(
        self,
        /,
        *,
        nmat_number_of_materials_in_this_domain: float,
        density_for_foundation_wall: float | None = 2243,
        density_for_floor_slab: float | None = 2243,
        density_for_ceiling: float | None = 311,
        density_for_soil: float | None = 1500,
        density_for_gravel: float | None = 2000,
        density_for_wood: float | None = 449,
        specific_heat_for_foundation_wall: float | None = 880,
        specific_heat_for_floor_slab: float | None = 880,
        specific_heat_for_ceiling: float | None = 1530,
        specific_heat_for_soil: float | None = 840,
        specific_heat_for_gravel: float | None = 720,
        specific_heat_for_wood: float | None = 1530,
        thermal_conductivity_for_foundation_wall: float | None = 1.4,
        thermal_conductivity_for_floor_slab: float | None = 1.4,
        thermal_conductivity_for_ceiling: float | None = 0.09,
        thermal_conductivity_for_soil: float | None = 1.1,
        thermal_conductivity_for_gravel: float | None = 1.9,
        thermal_conductivity_for_wood: float | None = 0.12,
    ) -> None:
        """Create a new ``GroundHeatTransfer:Basement:MatlProps`` and add it to the document.

        Specifies the material properties for the Basement preprocessor ground heat transfer simulation. Only the Foundation Wall, Floor Slab, Soil, and Gravel properties are currently used.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-detailed-ground-heat-transfer/#groundheattransferbasementmatlprops
        """

class GroundHeatTransferBasementSurfaceProps:
    def __call__(
        self,
        /,
        *,
        albedo_surface_albedo_for_no_snow_conditions: float | None = 0.16,
        albedo_surface_albedo_for_snow_conditions: float | None = 0.4,
        epsln_surface_emissivity_no_snow: float | None = 0.94,
        epsln_surface_emissivity_with_snow: float | None = 0.86,
        veght_surface_roughness_no_snow_conditions: float | None = 6,
        veght_surface_roughness_snow_conditions: float | None = 0.25,
        pet_flag_potential_evapotranspiration_on_: Literal["", "FALSE", "TRUE"] | None = "FALSE",
        pet_flag_potential_evapotranspiration_on: Literal["", "FALSE", "TRUE"] | None = ...,
    ) -> None:
        """Create a new ``GroundHeatTransfer:Basement:SurfaceProps`` and add it to the document.

        Specifies the soil surface properties for the Basement preprocessor ground heat transfer simulation.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-detailed-ground-heat-transfer/#groundheattransferbasementsurfaceprops
        """

class AnyGasEquipment:
    def __call__(
        self,
        name: str,
        /,
        *,
        narrow_with_as_version_first: Never,
        schedule_name: str,
        design_level_calculation_method: Literal[
            "", "EquipmentLevel", "Power/Area", "Power/Person", "Watts/Area", "Watts/Person"
        ]
        | None = "EquipmentLevel",
        design_level: float | None = ...,
        power_per_person: float | None = ...,
        fraction_latent: float | None = 0,
        fraction_radiant: float | None = 0,
        fraction_lost: float | None = 0,
        carbon_dioxide_generation_rate: float | None = 0,
        end_use_subcategory: str | None = "General",
    ) -> None:
        """Create a new ``GasEquipment`` and add it to the document.

        Sets internal gains and contaminant rates for gas equipment in the zone. If a ZoneList, SpaceList, or a Zone comprised of more than one Space is specified then this definition applies to all applicable spaces, and each instance will be named with the Space Name plus this Object Name.

        No call suits every release: narrow the document with ``as_version`` first.
        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-internal-gains-people-lights-other/#gasequipment
        """

class AnyDaylightingReferencePoint:
    def __call__(
        self,
        name: str,
        /,
        *,
        narrow_with_as_version_first: Never,
        x_coordinate_of_reference_point: float,
        y_coordinate_of_reference_point: float,
        z_coordinate_of_reference_point: float | None = 0.8,
    ) -> None:
        """Create a new ``Daylighting:ReferencePoint`` and add it to the document.

        Used by Daylighting:Controls to identify the reference point coordinates for each sensor. Reference points are given in coordinates specified in the GlobalGeometryRules object Daylighting Reference Point CoordinateSystem field.

        No call suits every release: narrow the document with ``as_version`` first.
        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-daylighting/#daylightingreferencepoint
        """

class DaylightingDeviceShelf:
    def __call__(
        self,
        name: str,
        /,
        *,
        window_name: str,
        inside_shelf_name: str | None = ...,
        outside_shelf_name: str | None = ...,
        outside_shelf_construction_name: str | None = ...,
        view_factor_to_outside_shelf: float | None = ...,
    ) -> None:
        """Create a new ``DaylightingDevice:Shelf`` and add it to the document.

        Defines a daylighting which can have an inside shelf, an outside shelf, or both. The inside shelf is defined as a building surface and the outside shelf is defined as a shading surface.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-daylighting/#daylightingdeviceshelf
        """

class ZoneInfiltrationDesignFlowRate:
    def __call__(
        self,
        name: str,
        /,
        *,
        zone_or_zonelist_or_space_or_spacelist_name: str,
        schedule_name: str | None = ...,
        design_flow_rate_calculation_method: Literal[
            "", "AirChanges/Hour", "Flow/Area", "Flow/ExteriorArea", "Flow/ExteriorWallArea", "Flow/Zone"
        ]
        | None = "Flow/Zone",
        design_flow_rate: float | None = ...,
        flow_rate_per_floor_area: float | None = ...,
        flow_rate_per_exterior_surface_area: float | None = ...,
        air_changes_per_hour: float | None = ...,
        constant_term_coefficient: float | None = 1,
        temperature_term_coefficient: float | None = 0,
        velocity_term_coefficient: float | None = 0,
        velocity_squared_term_coefficient: float | None = 0,
        density_basis: Literal["", "Indoor", "Outdoor", "Standard"] | None = "Outdoor",
    ) -> None:
        """Create a new ``ZoneInfiltration:DesignFlowRate`` and add it to the document.

        Infiltration is specified as a design level which is modified by a Schedule fraction, temperature difference and wind speed: Infiltration=Idesign * FSchedule * (A + B*|(Tzone-Todb)| + C*WindSpd + D * WindSpd**2) If a ZoneList, SpaceList, or a Zone comprised of more than one Space is specified then this definition applies to all applicable spaces, and each instance will be named with the Space Name plus this Object Name.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-airflow/#zoneinfiltrationdesignflowrate
        """

class AnyZoneVentilationWindandStackOpenArea:
    def __call__(
        self,
        name: str,
        /,
        *,
        narrow_with_as_version_first: Never,
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

        No call suits every release: narrow the document with ``as_version`` first.
        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-airflow/#zoneventilationwindandstackopenarea
        """

class AnyZoneCrossMixing:
    def __call__(
        self,
        name: str,
        /,
        *,
        narrow_with_as_version_first: Never,
        schedule_name: str,
        design_flow_rate_calculation_method: Literal["", "AirChanges/Hour", "Flow/Area", "Flow/Person", "Flow/Zone"]
        | None = "Flow/Zone",
        design_flow_rate: float | None = ...,
        flow_rate_per_person: float | None = ...,
        air_changes_per_hour: float | None = ...,
        delta_temperature: float | None = 0,
        delta_temperature_schedule_name: str | None = ...,
        minimum_outdoor_temperature_schedule_name: str | None = ...,
        maximum_outdoor_temperature_schedule_name: str | None = ...,
    ) -> None:
        """Create a new ``ZoneCrossMixing`` and add it to the document.

        ZoneCrossMixing exchanges an equal amount of air between two zones or spaces. Note that this statement affects the energy balance of both zones or spaces.

        No call suits every release: narrow the document with ``as_version`` first.
        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-airflow/#zonecrossmixing
        """

class AirflowNetworkSimulationControl:
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
        allow_unsupported_zone_equipment: Literal["", "No", "Yes"] | None = "No",
        do_distribution_duct_sizing_calculation: Literal["", "No", "Yes"] | None = "No",
    ) -> None:
        """Create a new ``AirflowNetwork:SimulationControl`` and add it to the document.

        This object defines the global parameters used in an Airflow Network simulation.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-airflow-network/#airflownetworksimulationcontrol
        """

class AnyHVACTemplateZoneWaterToAirHeatPump:
    def __call__(
        self,
        /,
        *,
        zone_name: str,
        template_thermostat_name: str | None = ...,
        cooling_supply_air_flow_rate: float | Literal["", "Autosize"] | None = "Autosize",
        heating_supply_air_flow_rate: float | Literal["", "Autosize"] | None = "Autosize",
        no_load_supply_air_flow_rate: float | Literal["Autosize"] | None = ...,
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
        supply_fan_operating_mode_schedule_name: str | None = ...,
        supply_fan_placement: Literal["", "BlowThrough", "DrawThrough"] | None = "DrawThrough",
        supply_fan_total_efficiency: float | None = 0.7,
        supply_fan_delta_pressure: float | None = 75,
        supply_fan_motor_efficiency: float | None = 0.9,
        cooling_coil_type: Literal["", "Coil:Cooling:WaterToAirHeatPump:EquationFit"] | None = ...,
        cooling_coil_gross_rated_total_capacity: float | Literal["", "Autosize"] | None = "Autosize",
        cooling_coil_gross_rated_sensible_heat_ratio: float | Literal["", "Autosize"] | None = "Autosize",
        cooling_coil_gross_rated_cop: float | None = 3.5,
        heat_pump_heating_coil_type: Literal["", "Coil:Heating:WaterToAirHeatPump:EquationFit"] | None = ...,
        heat_pump_heating_coil_gross_rated_capacity: float | Literal["", "Autosize"] | None = "Autosize",
        heat_pump_heating_coil_gross_rated_cop: float | None = 4.2,
        supplemental_heating_coil_availability_schedule_name: str | None = ...,
        supplemental_heating_coil_capacity: float | Literal["", "Autosize"] | None = "Autosize",
        maximum_cycling_rate: float | None = 2.5,
        heat_pump_fan_delay_time: float | None = 60,
        dedicated_outdoor_air_system_name: str | None = ...,
        supplemental_heating_coil_type: Literal["", "Electric", "HotWater"] | None = "Electric",
        zone_cooling_design_supply_air_temperature_input_method: Literal[
            "", "SupplyAirTemperature", "TemperatureDifference"
        ]
        | None = "SupplyAirTemperature",
        zone_cooling_design_supply_air_temperature: float | None = 14,
        zone_cooling_design_supply_air_temperature_difference: float | None = 11.11,
        zone_heating_design_supply_air_temperature_input_method: Literal[
            "", "SupplyAirTemperature", "TemperatureDifference"
        ]
        | None = "SupplyAirTemperature",
        zone_heating_design_supply_air_temperature: float | None = 50,
        zone_heating_design_supply_air_temperature_difference: float | None = 30,
        heat_pump_coil_water_flow_mode: Literal["", "Constant", "ConstantOnDemand", "Cycling"] | None = "Cycling",
        design_specification_outdoor_air_object_name: str | None = ...,
        design_specification_zone_air_distribution_object_name: str | None = ...,
        baseboard_heating_type: Literal["", "Electric", "HotWater", "None"] | None = "None",
        baseboard_heating_availability_schedule_name: str | None = ...,
        baseboard_heating_capacity: float | Literal["", "Autosize"] | None = "Autosize",
    ) -> None:
        """Create a new ``HVACTemplate:Zone:WaterToAirHeatPump`` and add it to the document.

        Water to Air Heat Pump to be used with HVACTemplate:Plant:MixedWaterLoop

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/hvac-template-objects/group-hvac-templates/#hvactemplatezonewatertoairheatpump
        """

class HVACTemplateZoneWaterToAirHeatPump:
    def __call__(
        self,
        /,
        *,
        zone_name: str,
        template_thermostat_name: str | None = ...,
        cooling_supply_air_flow_rate: float | Literal["", "Autosize"] | None = "Autosize",
        heating_supply_air_flow_rate: float | Literal["", "Autosize"] | None = "Autosize",
        no_load_supply_air_flow_rate: float | Literal["Autosize"] | None = ...,
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
        supply_fan_operating_mode_schedule_name: str | None = ...,
        supply_fan_placement: Literal["", "BlowThrough", "DrawThrough"] | None = "DrawThrough",
        supply_fan_total_efficiency: float | None = 0.7,
        supply_fan_delta_pressure: float | None = 75,
        supply_fan_motor_efficiency: float | None = 0.9,
        cooling_coil_type: Literal["", "Coil:Cooling:WaterToAirHeatPump:EquationFit"] | None = ...,
        cooling_coil_gross_rated_total_capacity: float | Literal["", "Autosize"] | None = "Autosize",
        cooling_coil_gross_rated_sensible_heat_ratio: float | Literal["", "Autosize"] | None = "Autosize",
        cooling_coil_gross_rated_cop: float | None = 3.5,
        heat_pump_heating_coil_type: Literal["", "Coil:Heating:WaterToAirHeatPump:EquationFit"] | None = ...,
        heat_pump_heating_coil_gross_rated_capacity: float | Literal["", "Autosize"] | None = "Autosize",
        heat_pump_heating_coil_gross_rated_cop: float | None = 4.2,
        supplemental_heating_coil_availability_schedule_name: str | None = ...,
        supplemental_heating_coil_capacity: float | Literal["", "Autosize"] | None = "Autosize",
        maximum_cycling_rate: float | None = 2.5,
        latent_capacity_time_constant: float | None = 60,
        heat_pump_fan_delay_time: float | None = 60,
        dedicated_outdoor_air_system_name: str | None = ...,
        supplemental_heating_coil_type: Literal["", "Electric", "HotWater"] | None = "Electric",
        zone_cooling_design_supply_air_temperature_input_method: Literal[
            "", "SupplyAirTemperature", "TemperatureDifference"
        ]
        | None = "SupplyAirTemperature",
        zone_cooling_design_supply_air_temperature: float | None = 14,
        zone_cooling_design_supply_air_temperature_difference: float | None = 11.11,
        zone_heating_design_supply_air_temperature_input_method: Literal[
            "", "SupplyAirTemperature", "TemperatureDifference"
        ]
        | None = "SupplyAirTemperature",
        zone_heating_design_supply_air_temperature: float | None = 50,
        zone_heating_design_supply_air_temperature_difference: float | None = 30,
        heat_pump_coil_water_flow_mode: Literal["", "Constant", "ConstantOnDemand", "Cycling"] | None = "Cycling",
        design_specification_outdoor_air_object_name: str | None = ...,
        design_specification_zone_air_distribution_object_name: str | None = ...,
        baseboard_heating_type: Literal["", "Electric", "HotWater", "None"] | None = "None",
        baseboard_heating_availability_schedule_name: str | None = ...,
        baseboard_heating_capacity: float | Literal["", "Autosize"] | None = "Autosize",
    ) -> None:
        """Create a new ``HVACTemplate:Zone:WaterToAirHeatPump`` and add it to the document.

        Water to Air Heat Pump to be used with HVACTemplate:Plant:MixedWaterLoop

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/hvac-template-objects/group-hvac-templates/#hvactemplatezonewatertoairheatpump
        """

class HVACTemplateZoneUnitary:
    def __call__(
        self,
        /,
        *,
        zone_name: str,
        template_unitary_system_name: str,
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
            "", "SupplyAirTemperature", "SystemSupplyAirTemperature", "TemperatureDifference"
        ]
        | None = "SystemSupplyAirTemperature",
        zone_heating_design_supply_air_temperature: float | None = 50,
        zone_heating_design_supply_air_temperature_difference: float | None = 30,
        design_specification_outdoor_air_object_name: str | None = ...,
        design_specification_zone_air_distribution_object_name: str | None = ...,
    ) -> None:
        """Create a new ``HVACTemplate:Zone:Unitary`` and add it to the document.

        Zone terminal unit, constant volume, no controls.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/hvac-template-objects/group-hvac-templates/#hvactemplatezoneunitary
        """

class HVACTemplatePlantHotWaterLoop:
    def __call__(
        self,
        name: str,
        /,
        *,
        pump_schedule_name: str | None = ...,
        pump_control_type: Literal["", "Continuous", "Intermittent"] | None = "Intermittent",
        hot_water_plant_operation_scheme_type: Literal["", "Default", "UserDefined"] | None = "Default",
        hot_water_plant_equipment_operation_schemes_name: str | None = ...,
        hot_water_setpoint_schedule_name: str | None = ...,
        hot_water_design_setpoint: float | None = 82,
        hot_water_pump_configuration: Literal["", "ConstantFlow", "VariableFlow"] | None = "ConstantFlow",
        hot_water_pump_rated_head: float | None = 179352,
        hot_water_setpoint_reset_type: Literal["", "None", "OutdoorAirTemperatureReset"] | None = "None",
        hot_water_setpoint_at_outdoor_dry_bulb_low: float | None = 82.2,
        hot_water_reset_outdoor_dry_bulb_low: float | None = -6.7,
        hot_water_setpoint_at_outdoor_dry_bulb_high: float | None = 65.6,
        hot_water_reset_outdoor_dry_bulb_high: float | None = 10,
        hot_water_pump_type: Literal[
            "",
            "FiveHeaderedPumps",
            "FourHeaderedPumps",
            "PumpPerBoiler",
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
        loop_design_delta_temperature: float | None = 11,
        maximum_outdoor_dry_bulb_temperature: float | None = ...,
        load_distribution_scheme: Literal[
            "", "Optimal", "SequentialLoad", "SequentialUniformPLR", "UniformLoad", "UniformPLR"
        ]
        | None = "SequentialLoad",
    ) -> None:
        """Create a new ``HVACTemplate:Plant:HotWaterLoop`` and add it to the document.

        Plant loop to serve all HVACTemplate hot water coils and boilers.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/hvac-template-objects/group-hvac-templates/#hvactemplateplanthotwaterloop
        """

class AirTerminalSingleDuctMixer:
    def __call__(
        self,
        name: str,
        /,
        *,
        zonehvac_unit_object_type: Literal[
            "AirLoopHVAC:UnitarySystem",
            "ZoneHVAC:FourPipeFanCoil",
            "ZoneHVAC:PackagedTerminalAirConditioner",
            "ZoneHVAC:PackagedTerminalHeatPump",
            "ZoneHVAC:TerminalUnit:VariableRefrigerantFlow",
            "ZoneHVAC:UnitVentilator",
            "ZoneHVAC:WaterToAirHeatPump",
        ],
        zonehvac_unit_object_name: str,
        mixer_outlet_node_name: str,
        mixer_primary_air_inlet_node_name: str,
        mixer_secondary_air_inlet_node_name: str,
        mixer_connection_type: Literal["InletSide", "SupplySide"],
        design_specification_outdoor_air_object_name: str | None = ...,
        per_person_ventilation_rate_mode: Literal["", "CurrentOccupancy", "DesignOccupancy"]
        | None = "CurrentOccupancy",
    ) -> None:
        """Create a new ``AirTerminal:SingleDuct:Mixer`` and add it to the document.

        The mixer air terminal unit provides a means of supplying central system air to the air inlet or outlet side of a zoneHVAC equipment such as a four pipe fan coil unit. Normally the central air would be ventilation air from a dedicated outdoor air system (DOAS).

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-air-distribution-equipment/#airterminalsingleductmixer
        """

class CoilCoolingWaterDetailedGeometry:
    def __call__(
        self,
        name: str,
        /,
        *,
        water_inlet_node_name: str,
        water_outlet_node_name: str,
        air_inlet_node_name: str,
        air_outlet_node_name: str,
        availability_schedule_name: str | None = ...,
        maximum_water_flow_rate: float | Literal["", "Autosize"] | None = "Autosize",
        tube_outside_surface_area: float | Literal["", "Autosize"] | None = "Autosize",
        total_tube_inside_area: float | Literal["", "Autosize"] | None = "Autosize",
        fin_surface_area: float | Literal["", "Autosize"] | None = "Autosize",
        minimum_airflow_area: float | Literal["", "Autosize"] | None = "Autosize",
        coil_depth: float | Literal["", "Autosize"] | None = "Autosize",
        fin_diameter: float | Literal["", "Autosize"] | None = "Autosize",
        fin_thickness: float | None = 0.0015,
        tube_inside_diameter: float | None = 0.01445,
        tube_outside_diameter: float | None = 0.0159,
        tube_thermal_conductivity: float | None = 386,
        fin_thermal_conductivity: float | None = 204,
        fin_spacing: float | None = 0.0018,
        tube_depth_spacing: float | None = 0.026,
        number_of_tube_rows: float | None = 4,
        number_of_tubes_per_row: float | Literal["", "Autosize"] | None = "Autosize",
        condensate_collection_water_storage_tank_name: str | None = ...,
        design_water_temperature_difference: float | None = ...,
        design_inlet_water_temperature: float | Literal["", "Autosize"] | None = "Autosize",
    ) -> None:
        """Create a new ``Coil:Cooling:Water:DetailedGeometry`` and add it to the document.

        Chilled water cooling coil, detailed flat fin coil model for continuous plate fins, with inputs for detailed coil geometry specifications.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-heating-and-cooling-coils/#coilcoolingwaterdetailedgeometry
        """

class CoilHeatingWater:
    def __call__(
        self,
        name: str,
        /,
        *,
        water_inlet_node_name: str,
        water_outlet_node_name: str,
        air_inlet_node_name: str,
        air_outlet_node_name: str,
        availability_schedule_name: str | None = ...,
        u_factor_times_area_value: float | Literal["", "Autosize"] | None = "Autosize",
        maximum_water_flow_rate: float | Literal["", "Autosize"] | None = "Autosize",
        performance_input_method: Literal["", "NominalCapacity", "UFactorTimesAreaAndDesignWaterFlowRate"]
        | None = "UFactorTimesAreaAndDesignWaterFlowRate",
        rated_capacity: float | Literal["", "Autosize"] | None = "Autosize",
        rated_inlet_water_temperature: float | None = 82.2,
        rated_inlet_air_temperature: float | None = 16.6,
        rated_outlet_water_temperature: float | None = 71.1,
        rated_outlet_air_temperature: float | None = 32.2,
        rated_ratio_for_air_and_water_convection: float | None = 0.5,
        design_water_temperature_difference: float | None = ...,
    ) -> None:
        """Create a new ``Coil:Heating:Water`` and add it to the document.

        Hot water heating coil, NTU-effectiveness model, assumes a cross-flow heat exchanger. Two options for capacity inputs: UA and water flow rate or capacity and design temperatures.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-heating-and-cooling-coils/#coilheatingwater
        """

class CoilHeatingDesuperheater:
    def __call__(
        self,
        name: str,
        /,
        *,
        air_inlet_node_name: str,
        air_outlet_node_name: str,
        heating_source_object_type: Literal[
            "Coil:Cooling:DX",
            "Coil:Cooling:DX:SingleSpeed",
            "Coil:Cooling:DX:TwoSpeed",
            "Coil:Cooling:DX:TwoStageWithHumidityControlMode",
            "Coil:Cooling:DX:VariableSpeed",
            "Refrigeration:CompressorRack",
            "Refrigeration:Condenser:AirCooled",
            "Refrigeration:Condenser:EvaporativeCooled",
            "Refrigeration:Condenser:WaterCooled",
        ],
        heating_source_name: str,
        availability_schedule_name: str | None = ...,
        heat_reclaim_recovery_efficiency: float | None = ...,
        temperature_setpoint_node_name: str | None = ...,
        on_cycle_parasitic_electric_load: float | None = ...,
    ) -> None:
        """Create a new ``Coil:Heating:Desuperheater`` and add it to the document.

        Desuperheater air heating coil. The heating energy provided by this coil is reclaimed from the superheated refrigerant gas leaving a compressor and does not impact the performance of the compressor. If the coil is located directly in an air loop branch or outdoor air equipment list, then it is controlled on leaving air temperature and the Temperature Setpoint Node Name must be specified. If the coil is contained within another component such as a unitary system, then the coil is controlled by the parent component and the setpoint node name is not entered.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-heating-and-cooling-coils/#coilheatingdesuperheater
        """

class CoilHeatingDXMultiSpeed:
    def __call__(
        self,
        name: str,
        /,
        *,
        air_inlet_node_name: str,
        air_outlet_node_name: str,
        fuel_type: Literal[
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
        crankcase_heater_capacity_function_of_temperature_curve_name: str | None = ...,
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

class AirLoopHVACUnitarySystem:
    def __call__(
        self,
        name: str,
        /,
        *,
        air_inlet_node_name: str,
        air_outlet_node_name: str,
        control_type: Literal["", "Load", "SetPoint", "SingleZoneVAV"] | None = "Load",
        controlling_zone_or_thermostat_location: str | None = ...,
        dehumidification_control_type: Literal["", "CoolReheat", "Multimode", "None"] | None = "None",
        availability_schedule_name: str | None = ...,
        supply_fan_object_type: Literal[
            "Fan:ComponentModel", "Fan:ConstantVolume", "Fan:OnOff", "Fan:SystemModel", "Fan:VariableVolume"
        ]
        | None = ...,
        supply_fan_name: str | None = ...,
        fan_placement: Literal["BlowThrough", "DrawThrough"] | None = ...,
        supply_air_fan_operating_mode_schedule_name: str | None = ...,
        heating_coil_object_type: Literal[
            "Coil:Heating:DX:MultiSpeed",
            "Coil:Heating:DX:SingleSpeed",
            "Coil:Heating:DX:VariableSpeed",
            "Coil:Heating:Desuperheater",
            "Coil:Heating:Electric",
            "Coil:Heating:Electric:MultiStage",
            "Coil:Heating:Fuel",
            "Coil:Heating:Gas:MultiStage",
            "Coil:Heating:Steam",
            "Coil:Heating:Water",
            "Coil:Heating:WaterToAirHeatPump:EquationFit",
            "Coil:Heating:WaterToAirHeatPump:ParameterEstimation",
            "Coil:Heating:WaterToAirHeatPump:VariableSpeedEquationFit",
            "Coil:UserDefined",
        ]
        | None = ...,
        heating_coil_name: str | None = ...,
        dx_heating_coil_sizing_ratio: float | None = 1,
        cooling_coil_object_type: Literal[
            "Coil:Cooling:DX",
            "Coil:Cooling:DX:MultiSpeed",
            "Coil:Cooling:DX:SingleSpeed",
            "Coil:Cooling:DX:SingleSpeed:ThermalStorage",
            "Coil:Cooling:DX:TwoSpeed",
            "Coil:Cooling:DX:TwoStageWithHumidityControlMode",
            "Coil:Cooling:DX:VariableSpeed",
            "Coil:Cooling:Water",
            "Coil:Cooling:Water:DetailedGeometry",
            "Coil:Cooling:WaterToAirHeatPump:EquationFit",
            "Coil:Cooling:WaterToAirHeatPump:ParameterEstimation",
            "Coil:Cooling:WaterToAirHeatPump:VariableSpeedEquationFit",
            "Coil:UserDefined",
            "CoilSystem:Cooling:DX:HeatExchangerAssisted",
            "CoilSystem:Cooling:Water:HeatExchangerAssisted",
        ]
        | None = ...,
        cooling_coil_name: str | None = ...,
        use_doas_dx_cooling_coil: Literal["", "No", "Yes"] | None = "No",
        minimum_supply_air_temperature: float | Literal["", "Autosize"] | None = 2,
        latent_load_control: Literal[
            "",
            "LatentOnlyLoadControl",
            "LatentOrSensibleLoadControl",
            "LatentWithSensibleLoadControl",
            "SensibleOnlyLoadControl",
        ]
        | None = "SensibleOnlyLoadControl",
        supplemental_heating_coil_object_type: Literal[
            "Coil:Heating:Desuperheater",
            "Coil:Heating:Electric",
            "Coil:Heating:Electric:Multistage",
            "Coil:Heating:Fuel",
            "Coil:Heating:Steam",
            "Coil:Heating:Water",
            "Coil:UserDefined",
        ]
        | None = ...,
        supplemental_heating_coil_name: str | None = ...,
        cooling_supply_air_flow_rate_method: Literal[
            "FlowPerCoolingCapacity", "FlowPerFloorArea", "FractionOfAutosizedCoolingValue", "None", "SupplyAirFlowRate"
        ]
        | None = ...,
        cooling_supply_air_flow_rate: float | Literal["Autosize"] | None = ...,
        cooling_supply_air_flow_rate_per_floor_area: float | None = ...,
        cooling_fraction_of_autosized_cooling_supply_air_flow_rate: float | None = ...,
        cooling_supply_air_flow_rate_per_unit_of_capacity: float | None = ...,
        heating_supply_air_flow_rate_method: Literal[
            "FlowPerFloorArea", "FlowPerHeatingCapacity", "FractionOfAutosizedHeatingValue", "None", "SupplyAirFlowRate"
        ]
        | None = ...,
        heating_supply_air_flow_rate: float | Literal["Autosize"] | None = ...,
        heating_supply_air_flow_rate_per_floor_area: float | None = ...,
        heating_fraction_of_autosized_heating_supply_air_flow_rate: float | None = ...,
        heating_supply_air_flow_rate_per_unit_of_capacity: float | None = ...,
        no_load_supply_air_flow_rate_method: Literal[
            "FlowPerCoolingCapacity",
            "FlowPerFloorArea",
            "FlowPerHeatingCapacity",
            "FractionOfAutosizedCoolingValue",
            "FractionOfAutosizedHeatingValue",
            "None",
            "SupplyAirFlowRate",
        ]
        | None = ...,
        no_load_supply_air_flow_rate: float | Literal["Autosize"] | None = ...,
        no_load_supply_air_flow_rate_per_floor_area: float | None = ...,
        no_load_fraction_of_autosized_cooling_supply_air_flow_rate: float | None = ...,
        no_load_fraction_of_autosized_heating_supply_air_flow_rate: float | None = ...,
        no_load_supply_air_flow_rate_per_unit_of_capacity_during_cooling_operation: float | None = ...,
        no_load_supply_air_flow_rate_per_unit_of_capacity_during_heating_operation: float | None = ...,
        no_load_supply_air_flow_rate_control_set_to_low_speed: Literal["", "No", "Yes"] | None = "Yes",
        maximum_supply_air_temperature: float | Literal["", "Autosize"] | None = 80,
        maximum_outdoor_dry_bulb_temperature_for_supplemental_heater_operation: float | None = 21,
        outdoor_dry_bulb_temperature_sensor_node_name: str | None = ...,
        ancillary_on_cycle_electric_power: float | None = 0,
        ancillary_off_cycle_electric_power: float | None = 0,
        design_heat_recovery_water_flow_rate: float | None = 0,
        maximum_temperature_for_heat_recovery: float | None = 80,
        heat_recovery_water_inlet_node_name: str | None = ...,
        heat_recovery_water_outlet_node_name: str | None = ...,
        design_specification_multispeed_object_type: Literal["UnitarySystemPerformance:Multispeed"] | None = ...,
        design_specification_multispeed_object_name: str | None = ...,
    ) -> None:
        """Create a new ``AirLoopHVAC:UnitarySystem`` and add it to the document.

        AirloopHVAC:UnitarySystem is a generic HVAC system type that allows any configuration of coils and/or fan. This object is a replacement of other AirloopHVAC objects. This object can be used in outdoor air systems, outdoor air units, air loops, and as zone equipment if desired.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-unitary-equipment/#airloophvacunitarysystem
        """

class OutdoorAirNodeList:
    def __call__(self, /, *, nodes: list[_g.OutdoorAirNodeListNodesItem] = ...) -> None:
        """Create a new ``OutdoorAir:NodeList`` and add it to the document.

        This object sets the temperature and humidity conditions for an outdoor air node using the weather data values. to vary outdoor air node conditions with height above ground use OutdoorAir:Node instead of this object. This object may be used more than once. The same node name may not appear in both an OutdoorAir:Node object and an OutdoorAir:NodeList object.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-air-distribution/#outdoorairnodelist
        """

class GroundHeatExchangerVerticalProperties:
    def __call__(
        self,
        name: str,
        /,
        *,
        depth_of_top_of_borehole: float,
        borehole_length: float,
        borehole_diameter: float,
        grout_thermal_conductivity: float,
        grout_thermal_heat_capacity: float,
        pipe_thermal_conductivity: float,
        pipe_thermal_heat_capacity: float,
        pipe_outer_diameter: float,
        pipe_thickness: float,
        u_tube_distance: float,
    ) -> None:
        """Create a new ``GroundHeatExchanger:Vertical:Properties`` and add it to the document.

        Properties for vertical ground heat exchanger systems

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-condenser-equipment/#groundheatexchangerverticalproperties
        """

class GroundHeatExchangerVerticalArray:
    def __call__(
        self,
        name: str,
        /,
        *,
        ghe_vertical_properties_object_name: str,
        number_of_boreholes_in_x_direction: int,
        number_of_boreholes_in_y_direction: int,
        borehole_spacing: float,
    ) -> None:
        """Create a new ``GroundHeatExchanger:Vertical:Array`` and add it to the document.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-condenser-equipment/#groundheatexchangerverticalarray
        """

class AnyCondenserEquipmentList:
    def __call__(self, name: str, /) -> None:
        """Create a new ``CondenserEquipmentList`` and add it to the document.

        List condenser equipment in order of operating priority, 1st in list will be used 1st, etc Use only condenser equipment in this list. If no equipment object types and equipment names are specified, then the corresponding PlantEquipmentOperation:* object will assume all available condenser equipment for the loop should be OFF (not operate) within the specified lower/upper limit.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-plant-condenser-control/#condenserequipmentlist
        """

class PlantEquipmentOperationUncontrolled:
    def __call__(self, name: str, /, *, equipment_list_name: str) -> None:
        """Create a new ``PlantEquipmentOperation:Uncontrolled`` and add it to the document.

        Plant equipment operation scheme for uncontrolled operation. Specifies a group of equipment that runs if the loop is active, unless turned off by the loop flow resolver to maintain continuity in the fluid loop.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-plant-condenser-control/#plantequipmentoperationuncontrolled
        """

class EnergyManagementSystemProgram:
    def __call__(self, name: str, /, *, lines: list[_g.EnergyManagementSystemProgramLinesItem]) -> None:
        """Create a new ``EnergyManagementSystem:Program`` and add it to the document.

        This input defines an Erl program Each field after the name is a line of EMS Runtime Language

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-energy-management-system-ems/#energymanagementsystemprogram
        """

class AnyEnergyManagementSystemMeteredOutputVariable:
    def __call__(
        self,
        name: str,
        /,
        *,
        ems_variable_name: str,
        update_frequency: Literal["SystemTimestep", "ZoneTimestep"],
        resource_type: Literal[
            "Coal",
            "CondensateWaterCollected",
            "Diesel",
            "DistrictCooling",
            "Electricity",
            "ElectricityProducedOnSite",
            "EnergyTransfer",
            "Gasoline",
            "MainsWaterSupply",
            "NaturalGas",
            "OnSiteWaterProduced",
            "OtherFuel1",
            "OtherFuel2",
            "Propane",
            "RainWaterCollected",
            "SolarAirHeating",
            "SolarWaterHeating",
            "WaterUse",
            "WellWaterDrawn",
        ],
        group_type: Literal["Building", "HVAC", "Plant", "System"],
        end_use_category: Literal[
            "Baseboard",
            "Boilers",
            "Chillers",
            "Cooling",
            "CoolingCoils",
            "ExteriorEquipment",
            "ExteriorLights",
            "Fans",
            "HeatRecovery",
            "HeatRecoveryForCooling",
            "HeatRecoveryForHeating",
            "HeatRejection",
            "Heating",
            "HeatingCoils",
            "Humidifier",
            "InteriorEquipment",
            "InteriorLights",
            "OnSiteGeneration",
            "Pumps",
            "Refrigeration",
            "WaterSystems",
        ],
        ems_program_or_subroutine_name: str | None = ...,
        end_use_subcategory: str | None = ...,
        units: str | None = ...,
    ) -> None:
        """Create a new ``EnergyManagementSystem:MeteredOutputVariable`` and add it to the document.

        This object sets up an EnergyPlus output variable from an Erl variable

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-energy-management-system-ems/#energymanagementsystemmeteredoutputvariable
        """

class AvailabilityManagerScheduledOff:
    def __call__(self, name: str, /, *, schedule_name: str) -> None:
        """Create a new ``AvailabilityManager:ScheduledOff`` and add it to the document.

        Determines the availability of a loop or system: only controls the turn off action. Schedule overrides fan/pump schedule.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-system-availability-managers/#availabilitymanagerscheduledoff
        """

class AvailabilityManagerHighTemperatureTurnOff:
    def __call__(self, name: str, /, *, sensor_node_name: str, temperature: float) -> None:
        """Create a new ``AvailabilityManager:HighTemperatureTurnOff`` and add it to the document.

        Overrides fan/pump schedules depending on temperature at sensor node.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-system-availability-managers/#availabilitymanagerhightemperatureturnoff
        """

class RefrigerationCompressorList:
    def __call__(self, name: str, /, *, compressors: list[_g.RefrigerationCompressorListCompressorsItem] = ...) -> None:
        """Create a new ``Refrigeration:CompressorList`` and add it to the document.

        List of all the compressors included within a single refrigeration system (Refrigeration:System). Each list must contain at least one compressor. The order in which the individual compressors are listed here will be the order in which the compressors are dispatched to meet the system load. IMPORTANT: List compressor names in the order in which the compressors will be loaded Data is available for many compressors in the RefrigerationCompressor.idf dataset

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-refrigeration/#refrigerationcompressorlist
        """

class RefrigerationWalkIn:
    def __call__(
        self,
        name: str,
        /,
        *,
        rated_coil_cooling_capacity: float,
        operating_temperature: float,
        rated_cooling_source_temperature: float,
        rated_total_heating_power: float,
        rated_total_lighting_power: float,
        defrost_schedule_name: str,
        insulated_floor_surface_area: float,
        availability_schedule_name: str | None = ...,
        heating_power_schedule_name: str | None = ...,
        rated_cooling_coil_fan_power: float | None = 375,
        rated_circulation_fan_power: float | None = 0,
        lighting_schedule_name: str | None = ...,
        defrost_type: Literal["", "Electric", "HotFluid", "None", "OffCycle"] | None = "Electric",
        defrost_control_type: Literal["", "TemperatureTermination", "TimeSchedule"] | None = "TimeSchedule",
        defrost_drip_down_schedule_name: str | None = ...,
        defrost_power: float | None = ...,
        temperature_termination_defrost_fraction_to_ice: float | None = ...,
        restocking_schedule_name: str | None = ...,
        average_refrigerant_charge_inventory: float | None = 0,
        insulated_floor_u_value: float | None = 0.3154,
        zone_data: list[_g.RefrigerationWalkInZoneDataItem] = ...,
    ) -> None:
        """Create a new ``Refrigeration:WalkIn`` and add it to the document.

        Works in conjunction with a compressor rack, a refrigeration system, or a refrigeration secondary system to simulate the performance of a walk-in cooler. The walk-in cooler model uses information at rated conditions along with input descriptions for heat transfer surfaces facing multiple zones to determine performance.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-refrigeration/#refrigerationwalkin
        """

class DemandManagerThermostats:
    def __call__(
        self,
        name: str,
        /,
        *,
        reset_control: Literal["Fixed", "Off"],
        maximum_heating_setpoint_reset: float,
        maximum_cooling_setpoint_reset: float,
        selection_control: Literal["All", "RotateMany", "RotateOne"],
        availability_schedule_name: str | None = ...,
        minimum_reset_duration: int | None = ...,
        reset_step_change: float | None = ...,
        rotation_duration: int | None = ...,
        thermostats: list[_g.DemandManagerThermostatsThermostatsItem] = ...,
    ) -> None:
        """Create a new ``DemandManager:Thermostats`` and add it to the document.

        used for demand limiting ZoneControl:Thermostat objects.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-demand-limiting-controls/#demandmanagerthermostats
        """

class LifeCycleCostNonrecurringCost:
    def __call__(
        self,
        name: str,
        /,
        *,
        category: Literal["", "Construction", "OtherCapital", "Salvage"] | None = "Construction",
        cost: float | None = ...,
        start_of_costs: Literal["", "BasePeriod", "ServicePeriod"] | None = "ServicePeriod",
        years_from_start: int | None = ...,
        months_from_start: int | None = ...,
    ) -> None:
        """Create a new ``LifeCycleCost:NonrecurringCost`` and add it to the document.

        A non-recurring cost happens only once during the study period. For costs that occur more than once during the study period on a regular schedule, use the LifeCycleCost:RecurringCost object.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/energyplus-economics/lifecyclecost-nonrecurringcost/#lifecyclecostnonrecurringcost
        """

class OutputSurfacesList:
    def __call__(
        self,
        /,
        *,
        report_type: Literal[
            "CostInfo",
            "DecayCurvesFromComponentLoadsSummary",
            "Details",
            "DetailsWithVertices",
            "Lines",
            "Vertices",
            "ViewFactorInfo",
        ],
        report_specifications: Literal["IDF"] | None = ...,
    ) -> None:
        """Create a new ``Output:Surfaces:List`` and add it to the document.

        Produces a report summarizing the details of surfaces in the eio output file.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/input-for-output/#outputsurfaceslist
        """
