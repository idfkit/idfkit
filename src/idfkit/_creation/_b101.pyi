"""Creation signatures of generated classes (stub only).

DO NOT EDIT — regenerate with:
    python -m idfkit.codegen.generate_stubs
"""

from __future__ import annotations

from collections.abc import Sequence
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

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-simulation-parameters/#building
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

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-thermal-zone-description-geometry/#walladiabatic
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

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-airflow-network/#airflownetworksimulationcontrol
        """

class HVACTemplateZoneWaterToAirHeatPump:
    def __call__(
        self,
        this_type_has_no_name_field: _g._PassFieldsAsKeywords = ...,
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

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/hvac-template-objects/group-hvac-templates/#hvactemplatezonewatertoairheatpump
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

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-heating-and-cooling-coils/#coilcoolingwaterdetailedgeometry
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

class EnergyManagementSystemProgram:
    def __call__(
        self,
        name: str,
        /,
        *,
        lines: Sequence[_g.EnergyManagementSystemProgramLinesItem | _g.EnergyManagementSystemProgramLinesGroup],
    ) -> None:
        """Create a new ``EnergyManagementSystem:Program`` and add it to the document.

        This input defines an Erl program Each field after the name is a line of EMS Runtime Language

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-energy-management-system-ems/#energymanagementsystemprogram
        """

class RefrigerationCompressorList:
    def __call__(
        self,
        name: str,
        /,
        *,
        compressors: Sequence[
            _g.RefrigerationCompressorListCompressorsItem | _g.RefrigerationCompressorListCompressorsGroup
        ] = ...,
    ) -> None:
        """Create a new ``Refrigeration:CompressorList`` and add it to the document.

        List of all the compressors included within a single refrigeration system (Refrigeration:System). Each list must contain at least one compressor. The order in which the individual compressors are listed here will be the order in which the compressors are dispatched to meet the system load. IMPORTANT: List compressor names in the order in which the compressors will be loaded Data is available for many compressors in the RefrigerationCompressor.idf dataset

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-refrigeration/#refrigerationcompressorlist
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
        thermostats: Sequence[
            _g.DemandManagerThermostatsThermostatsItem | _g.DemandManagerThermostatsThermostatsGroup
        ] = ...,
    ) -> None:
        """Create a new ``DemandManager:Thermostats`` and add it to the document.

        used for demand limiting ZoneControl:Thermostat objects.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-demand-limiting-controls/#demandmanagerthermostats
        """

class OutputSurfacesList:
    def __call__(
        self,
        this_type_has_no_name_field: _g._PassFieldsAsKeywords = ...,
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
