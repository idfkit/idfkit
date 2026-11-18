"""Creation signatures of generated classes (stub only).

DO NOT EDIT — regenerate with:
    python -m idfkit.codegen.generate_stubs
"""

from __future__ import annotations

from typing import Literal

from typing_extensions import Never

from .. import _generated_types as _g

class WeatherPropertySkyTemperature:
    def __call__(
        self,
        name: str = "",
        /,
        *,
        calculation_type: Literal[
            "",
            "BerdahlMartin",
            "Brunt",
            "ClarkAllen",
            "DifferenceScheduleDewPointValue",
            "DifferenceScheduleDryBulbValue",
            "Idso",
            "ScheduleValue",
        ]
        | None = "ClarkAllen",
        schedule_name: str | None = ...,
        use_weather_file_horizontal_ir: Literal["", "No", "Yes"] | None = "Yes",
    ) -> None:
        """Create a new ``WeatherProperty:SkyTemperature`` and add it to the document.

        This object is used to override internal sky temperature calculations.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-location-climate-weather-file-access/#weatherpropertyskytemperature
        """

class SiteGroundTemperatureDeep:
    def __call__(
        self,
        /,
        *,
        january_deep_ground_temperature: float | None = 16,
        february_deep_ground_temperature: float | None = 16,
        march_deep_ground_temperature: float | None = 16,
        april_deep_ground_temperature: float | None = 16,
        may_deep_ground_temperature: float | None = 16,
        june_deep_ground_temperature: float | None = 16,
        july_deep_ground_temperature: float | None = 16,
        august_deep_ground_temperature: float | None = 16,
        september_deep_ground_temperature: float | None = 16,
        october_deep_ground_temperature: float | None = 16,
        november_deep_ground_temperature: float | None = 16,
        december_deep_ground_temperature: float | None = 16,
    ) -> None:
        """Create a new ``Site:GroundTemperature:Deep`` and add it to the document.

        These temperatures are specifically for the ground heat exchangers that would use 'deep' (3-4 m depth) ground temperatures for their heat source. They are not used in other models.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-location-climate-weather-file-access/#sitegroundtemperaturedeep
        """

class SiteSpectrumData:
    def __call__(
        self,
        name: str,
        /,
        *,
        spectrum_data_type: Literal["Solar", "Visible"],
        wavelength: float | None = ...,
        spectrum: float | None = ...,
        wavelength_1: float | None = ...,
        spectrum_2: float | None = ...,
        extensions: list[_g.SiteSpectrumDataExtensionsItem] = ...,
    ) -> None:
        """Create a new ``Site:SpectrumData`` and add it to the document.

        Spectrum Data Type is followed by up to 107 sets of normal-incidence measured values of [wavelength, spectrum] for wavelengths covering the solar (0.25 to 2.5 microns) or visible spectrum (0.38 to 0.78 microns)

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-location-climate-weather-file-access/#sitespectrumdata
        """

class ScheduleYear:
    def __call__(
        self,
        name: str,
        /,
        *,
        schedule_type_limits_name: str | None = ...,
        schedule_weeks: list[_g.ScheduleYearScheduleWeeksItem] = ...,
    ) -> None:
        """Create a new ``Schedule:Year`` and add it to the document.

        A Schedule:Year contains from 1 to 52 week schedules

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-schedules/#scheduleyear
        """

class ScheduleCompact:
    def __call__(
        self, name: str, /, *, schedule_type_limits_name: str | None = ..., data: list[_g.ScheduleCompactDataItem] = ...
    ) -> None:
        """Create a new ``Schedule:Compact`` and add it to the document.

        Irregular object. Does not follow the usual definition for fields. Fields A3... are: Through: Date For: Applicable days (ref: Schedule:Week:Compact) Interpolate: Average/Linear/No (ref: Schedule:Day:Interval) -- optional, if not used will be 'No' Until: <Time> (ref: Schedule:Day:Interval) <numeric value> words 'Through','For','Interpolate','Until' must be included.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-schedules/#schedulecompact
        """

class WindowMaterialGas:
    def __call__(
        self,
        name: str,
        /,
        *,
        gas_type: Literal["Air", "Argon", "Custom", "Krypton", "Xenon"],
        thickness: float,
        conductivity_coefficient_a: float | None = ...,
        conductivity_coefficient_b: float | None = ...,
        conductivity_coefficient_c: float | None = ...,
        viscosity_coefficient_a: float | None = ...,
        viscosity_coefficient_b: float | None = ...,
        viscosity_coefficient_c: float | None = ...,
        specific_heat_coefficient_a: float | None = ...,
        specific_heat_coefficient_b: float | None = ...,
        specific_heat_coefficient_c: float | None = ...,
        molecular_weight: float | None = ...,
        specific_heat_ratio: float | None = ...,
    ) -> None:
        """Create a new ``WindowMaterial:Gas`` and add it to the document.

        Gas material properties that are used in Windows or Glass Doors

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-surface-construction-elements/#windowmaterialgas
        """

class AnyGlobalGeometryRules:
    def __call__(
        self,
        /,
        *,
        starting_vertex_position: Literal["LowerLeftCorner", "LowerRightCorner", "UpperLeftCorner", "UpperRightCorner"],
        vertex_entry_direction: Literal["Clockwise", "Counterclockwise"],
        coordinate_system: Literal["Relative", "World"],
        daylighting_reference_point_coordinate_system: Literal["", "Relative", "World"] | None = "Relative",
        rectangular_surface_coordinate_system: Literal["", "Relative", "World"] | None = "Relative",
    ) -> None:
        """Create a new ``GlobalGeometryRules`` and add it to the document.

        Specifies the geometric rules used to describe the input of surface vertices and daylighting reference points.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-thermal-zone-description-geometry/#globalgeometryrules
        """

class RoofCeilingDetailed:
    def __call__(
        self,
        name: str,
        /,
        *,
        construction_name: str,
        zone_name: str,
        outside_boundary_condition: Literal[
            "Adiabatic",
            "Ground",
            "GroundBasementPreprocessorAverageFloor",
            "GroundBasementPreprocessorAverageWall",
            "GroundBasementPreprocessorLowerWall",
            "GroundBasementPreprocessorUpperWall",
            "GroundSlabPreprocessorAverage",
            "GroundSlabPreprocessorCore",
            "GroundSlabPreprocessorPerimeter",
            "OtherSideCoefficients",
            "OtherSideConditionsModel",
            "Outdoors",
            "Space",
            "Surface",
            "Zone",
        ],
        space_name: str | None = ...,
        outside_boundary_condition_object: str | None = ...,
        sun_exposure: Literal["", "NoSun", "SunExposed"] | None = "SunExposed",
        wind_exposure: Literal["", "NoWind", "WindExposed"] | None = "WindExposed",
        view_factor_to_ground: float | Literal["", "Autocalculate"] | None = "Autocalculate",
        number_of_vertices: float | Literal["", "Autocalculate"] | None = "Autocalculate",
        vertices: list[_g.RoofCeilingDetailedVerticesItem] = ...,
    ) -> None:
        """Create a new ``RoofCeiling:Detailed`` and add it to the document.

        Allows for detailed entry of roof/ceiling heat transfer surfaces.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-thermal-zone-description-geometry/#roofceilingdetailed
        """

class RoomAirNodeAirflowNetwork:
    def __call__(
        self,
        name: str = "",
        /,
        *,
        zone_name: str,
        fraction_of_zone_air_volume: float | None = ...,
        roomair_node_airflownetwork_adjacentsurfacelist_name: str | None = ...,
        roomair_node_airflownetwork_internalgains_name: str | None = ...,
        roomair_node_airflownetwork_hvacequipment_name: str | None = ...,
    ) -> None:
        """Create a new ``RoomAir:Node:AirflowNetwork`` and add it to the document.

        define an air node for some types of nodal air models

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-room-air-models/#roomairnodeairflownetwork
        """

class RoomAirNodeAirflowNetworkAdjacentSurfaceList:
    def __call__(
        self, name: str = "", /, *, surfaces: list[_g.RoomAirNodeAirflowNetworkAdjacentSurfaceListSurfacesItem] = ...
    ) -> None:
        """Create a new ``RoomAir:Node:AirflowNetwork:AdjacentSurfaceList`` and add it to the document.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-room-air-models/#roomairnodeairflownetworkadjacentsurfacelist
        """

class AnyZoneVentilationDesignFlowRate:
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
        ventilation_type: Literal["", "Balanced", "Exhaust", "Intake", "Natural"] | None = "Natural",
        fan_pressure_rise: float | None = 0,
        fan_total_efficiency: float | None = 1,
        constant_term_coefficient: float | None = 1,
        temperature_term_coefficient: float | None = 0,
        velocity_term_coefficient: float | None = 0,
        velocity_squared_term_coefficient: float | None = 0,
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
        """Create a new ``ZoneVentilation:DesignFlowRate`` and add it to the document.

        Ventilation is specified as a design level which is modified by a schedule fraction, temperature difference and wind speed: Ventilation=Vdesign * Fschedule * (A + B*|(Tzone-Todb)| + C*WindSpd + D * WindSpd**2) If a ZoneList, SpaceList, or a Zone comprised of more than one Space is specified then this definition applies to all applicable spaces, and each instance will be named with the Space Name plus this Object Name.

        No call suits every release: narrow the document with ``as_version`` first.
        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-airflow/#zoneventilationdesignflowrate
        """

class AnyAirflowNetworkDistributionComponentOutdoorAirFlow:
    def __call__(
        self,
        name: str,
        /,
        *,
        narrow_with_as_version_first: Never,
        air_mass_flow_coefficient_when_no_outdoor_air_flow_at_reference_conditions: float,
        air_mass_flow_exponent_when_no_outdoor_air_flow: float | None = 0.65,
        reference_crack_conditions: str | None = ...,
    ) -> None:
        """Create a new ``AirflowNetwork:Distribution:Component:OutdoorAirFlow`` and add it to the document.

        This object includes the outdoor air flow rate set by the Controller:OutdoorAir object in the airflow network.

        No call suits every release: narrow the document with ``as_version`` first.
        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-airflow-network/#airflownetworkdistributioncomponentoutdoorairflow
        """

class AirflowNetworkDistributionDuctSizing:
    def __call__(
        self,
        name: str,
        /,
        *,
        duct_sizing_method: Literal["", "MaximumVelocity", "PressureLoss", "PressureLossWithMaximumVelocity"]
        | None = "MaximumVelocity",
        duct_sizing_factor: float | None = 1,
        maximum_airflow_velocity: float | None = 5,
        total_pressure_loss_across_supply_trunk: float | None = ...,
        total_pressure_loss_across_supply_branch: float | None = ...,
        total_pressure_loss_across_return_trunk: float | None = ...,
        total_pressure_loss_across_return_branch: float | None = ...,
    ) -> None:
        """Create a new ``AirflowNetwork:Distribution:DuctSizing`` and add it to the document.

        This object defines required parameters for duct sizing in an Airflow Network simulation. To activate duct sizing, see AirflowNetwork:SimulationControl Do Distribution Duct Sizing Calculation.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-airflow-network/#airflownetworkdistributionductsizing
        """

class HVACTemplateSystemUnitarySystem:
    def __call__(
        self,
        name: str,
        /,
        *,
        system_availability_schedule_name: str | None = ...,
        control_type: Literal["", "Load", "SetPoint"] | None = "Load",
        control_zone_or_thermostat_location_name: str | None = ...,
        cooling_supply_air_flow_rate: float | Literal["", "Autosize"] | None = "Autosize",
        heating_supply_air_flow_rate: float | Literal["", "Autosize"] | None = "Autosize",
        no_load_supply_air_flow_rate: float | Literal["", "Autosize"] | None = "Autosize",
        supply_fan_operating_mode_schedule_name: str | None = ...,
        supply_fan_placement: Literal["", "BlowThrough", "DrawThrough"] | None = "BlowThrough",
        supply_fan_total_efficiency: float | None = 0.7,
        supply_fan_delta_pressure: float | None = 600,
        supply_fan_motor_efficiency: float | None = 0.9,
        supply_fan_motor_in_air_stream_fraction: float | None = 1,
        cooling_coil_type: Literal[
            "",
            "ChilledWater",
            "ChilledWaterDetailedFlatModel",
            "HeatExchangerAssistedChilledWater",
            "HeatExchangerAssistedDX",
            "MultiSpeedDX",
            "None",
            "SingleSpeedDX",
            "SingleSpeedDXWaterCooled",
            "TwoSpeedDX",
            "TwoStageDX",
            "TwoStageHumidityControlDX",
        ]
        | None = "SingleSpeedDX",
        number_of_speeds_for_cooling: int | None = 1,
        cooling_coil_availability_schedule_name: str | None = ...,
        cooling_design_supply_air_temperature: float | None = 12.8,
        dx_cooling_coil_gross_rated_total_capacity: float | Literal["", "Autosize"] | None = "Autosize",
        dx_cooling_coil_gross_rated_sensible_heat_ratio: float | Literal["", "Autosize"] | None = "Autosize",
        dx_cooling_coil_gross_rated_cop: float | None = 3,
        heating_coil_type: Literal[
            "",
            "Electric",
            "Gas",
            "HotWater",
            "MultiSpeedDXHeatPumpAirSource",
            "MultiStageElectric",
            "MultiStageGas",
            "None",
            "SingleSpeedDXHeatPumpAirSource",
            "SingleSpeedDXHeatPumpWaterSource",
        ]
        | None = "Gas",
        number_of_speeds_or_stages_for_heating: int | None = 1,
        heating_coil_availability_schedule_name: str | None = ...,
        heating_design_supply_air_temperature: float | None = 50,
        heating_coil_gross_rated_capacity: float | Literal["", "Autosize"] | None = "Autosize",
        gas_heating_coil_efficiency: float | None = 0.8,
        gas_heating_coil_parasitic_electric_load: float | None = 0,
        heat_pump_heating_coil_gross_rated_cop: float | None = 2.75,
        heat_pump_heating_minimum_outdoor_dry_bulb_temperature: float | None = -8,
        heat_pump_defrost_maximum_outdoor_dry_bulb_temperature: float | None = 5,
        heat_pump_defrost_strategy: Literal["", "Resistive", "ReverseCycle"] | None = "ReverseCycle",
        heat_pump_defrost_control: Literal["", "OnDemand", "Timed"] | None = "Timed",
        heat_pump_defrost_time_period_fraction: float | None = 0.058333,
        supplemental_heating_or_reheat_coil_type: Literal["", "DesuperHeater", "Electric", "Gas", "HotWater", "None"]
        | None = "None",
        supplemental_heating_or_reheat_coil_availability_schedule_name: str | None = ...,
        supplemental_heating_or_reheat_coil_capacity: float | Literal["", "Autosize"] | None = "Autosize",
        supplemental_heating_or_reheat_coil_maximum_outdoor_dry_bulb_temperature: float | None = 21,
        supplemental_gas_heating_or_reheat_coil_efficiency: float | None = 0.8,
        supplemental_gas_heating_or_reheat_coil_parasitic_electric_load: float | None = 0,
        maximum_outdoor_air_flow_rate: float | Literal["", "Autosize"] | None = "Autosize",
        minimum_outdoor_air_flow_rate: float | Literal["", "Autosize"] | None = "Autosize",
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
        heat_recovery_type: Literal["", "Enthalpy", "None", "Sensible"] | None = "None",
        sensible_heat_recovery_effectiveness: float | None = 0.7,
        latent_heat_recovery_effectiveness: float | None = 0.65,
        heat_recovery_heat_exchanger_type: Literal["", "Plate", "Rotary"] | None = "Plate",
        heat_recovery_frost_control_type: Literal[
            "", "ExhaustAirRecirculation", "ExhaustOnly", "MinimumExhaustTemperature", "None"
        ]
        | None = "None",
        dehumidification_control_type: Literal["", "CoolReheat", "Multimode", "None"] | None = "None",
        dehumidification_relative_humidity_setpoint: float | None = 60,
        dehumidification_relative_humidity_setpoint_schedule_name: str | None = ...,
        humidifier_type: Literal["", "ElectricSteam", "None"] | None = "None",
        humidifier_availability_schedule_name: str | None = ...,
        humidifier_rated_capacity: float | None = ...,
        humidifier_rated_electric_power: float | Literal["", "Autosize"] | None = "Autosize",
        humidifier_control_zone_name: str | None = ...,
        humidifier_relative_humidity_setpoint: float | None = 30,
        humidifier_relative_humidity_setpoint_schedule_name: str | None = ...,
        sizing_option: Literal["", "Coincident", "NonCoincident"] | None = "NonCoincident",
        return_fan: Literal["", "No", "Yes"] | None = "No",
        return_fan_total_efficiency: float | None = 0.7,
        return_fan_delta_pressure: float | None = 300,
        return_fan_motor_efficiency: float | None = 0.9,
        return_fan_motor_in_air_stream_fraction: float | None = 1,
    ) -> None:
        """Create a new ``HVACTemplate:System:UnitarySystem`` and add it to the document.

        Unitary HVAC system with optional cooling and heating. Supports DX and chilled water, cooling, gas, electric, and hot water heating, air-to-air and water-to-air heat pumps.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/hvac-template-objects/group-hvac-templates/#hvactemplatesystemunitarysystem
        """

class AirTerminalSingleDuctConstantVolumeReheat:
    def __call__(
        self,
        name: str,
        /,
        *,
        air_outlet_node_name: str,
        air_inlet_node_name: str,
        maximum_air_flow_rate: float | Literal["Autosize"],
        reheat_coil_object_type: Literal[
            "Coil:Heating:Electric", "Coil:Heating:Fuel", "Coil:Heating:Steam", "Coil:Heating:Water"
        ],
        reheat_coil_name: str,
        availability_schedule_name: str | None = ...,
        maximum_hot_water_or_steam_flow_rate: float | Literal["Autosize"] | None = ...,
        minimum_hot_water_or_steam_flow_rate: float | None = 0,
        convergence_tolerance: float | None = 0.001,
        maximum_reheat_air_temperature: float | None = ...,
    ) -> None:
        """Create a new ``AirTerminal:SingleDuct:ConstantVolume:Reheat`` and add it to the document.

        Central air system terminal unit, single duct, constant volume, with reheat coil (hot water, electric, gas, or steam).

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-air-distribution-equipment/#airterminalsingleductconstantvolumereheat
        """

class FanOnOff:
    def __call__(
        self,
        name: str,
        /,
        *,
        pressure_rise: float,
        air_inlet_node_name: str,
        air_outlet_node_name: str,
        availability_schedule_name: str | None = ...,
        fan_total_efficiency: float | None = 0.6,
        maximum_flow_rate: float | Literal["Autosize"] | None = ...,
        motor_efficiency: float | None = 0.8,
        motor_in_airstream_fraction: float | None = 1,
        fan_power_ratio_function_of_speed_ratio_curve_name: str | None = ...,
        fan_efficiency_ratio_function_of_speed_ratio_curve_name: str | None = ...,
        end_use_subcategory: str | None = "General",
    ) -> None:
        """Create a new ``Fan:OnOff`` and add it to the document.

        Constant volume fan that is intended to cycle on and off based on cooling/heating load or other control signals. This fan can also operate continuously like Fan:ConstantVolume.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-fans/#fanonoff
        """

class CoilCoolingDXSingleSpeed:
    def __call__(
        self,
        name: str,
        /,
        *,
        gross_rated_total_cooling_capacity: float | Literal["Autosize"],
        gross_rated_sensible_heat_ratio: float | Literal["Autosize"],
        rated_air_flow_rate: float | Literal["Autosize"],
        air_inlet_node_name: str,
        air_outlet_node_name: str,
        total_cooling_capacity_function_of_temperature_curve_name: str,
        total_cooling_capacity_function_of_flow_fraction_curve_name: str,
        energy_input_ratio_function_of_temperature_curve_name: str,
        energy_input_ratio_function_of_flow_fraction_curve_name: str,
        part_load_fraction_correlation_curve_name: str,
        availability_schedule_name: str | None = ...,
        gross_rated_cooling_cop: float | None = 3,
        minimum_outdoor_dry_bulb_temperature_for_compressor_operation: float | None = -25,
        nominal_time_for_condensate_removal_to_begin: float | None = 0,
        ratio_of_initial_moisture_evaporation_rate_and_steady_state_latent_capacity: float | None = 0,
        maximum_cycling_rate: float | None = 0,
        latent_capacity_time_constant: float | None = 0,
        condenser_air_inlet_node_name: str | None = ...,
        condenser_type: Literal["", "AirCooled", "EvaporativelyCooled"] | None = "AirCooled",
        evaporative_condenser_effectiveness: float | None = 0.9,
        evaporative_condenser_air_flow_rate: float | Literal["Autosize"] | None = ...,
        evaporative_condenser_pump_rated_power_consumption: float | Literal["", "Autosize"] | None = 0,
        crankcase_heater_capacity: float | None = 0,
        crankcase_heater_capacity_function_of_temperature_curve_name: str | None = ...,
        maximum_outdoor_dry_bulb_temperature_for_crankcase_heater_operation: float | None = 10,
        supply_water_storage_tank_name: str | None = ...,
        condensate_collection_water_storage_tank_name: str | None = ...,
        basin_heater_capacity: float | None = 0,
        basin_heater_setpoint_temperature: float | None = 2,
        basin_heater_operating_schedule_name: str | None = ...,
        sensible_heat_ratio_function_of_temperature_curve_name: str | None = ...,
        sensible_heat_ratio_function_of_flow_fraction_curve_name: str | None = ...,
        report_ashrae_standard_127_performance_ratings: Literal["", "No", "Yes"] | None = "No",
        zone_name_for_condenser_placement: str | None = ...,
    ) -> None:
        """Create a new ``Coil:Cooling:DX:SingleSpeed`` and add it to the document.

        Direct expansion (DX) cooling coil and condensing unit (includes electric compressor and condenser fan), single-speed. Optional inputs for moisture evaporation from wet coil when compressor cycles off with continuous fan operation.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-heating-and-cooling-coils/#coilcoolingdxsinglespeed
        """

class CoilCoolingDXMultiSpeed:
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
        condenser_type: Literal["", "AirCooled", "EvaporativelyCooled"] | None = "AirCooled",
        minimum_outdoor_dry_bulb_temperature_for_compressor_operation: float | None = -25,
        supply_water_storage_tank_name: str | None = ...,
        condensate_collection_water_storage_tank_name: str | None = ...,
        apply_part_load_fraction_to_speeds_greater_than_1: Literal["", "No", "Yes"] | None = "No",
        apply_latent_degradation_to_speeds_greater_than_1: Literal["", "No", "Yes"] | None = "No",
        crankcase_heater_capacity: float | None = 0,
        crankcase_heater_capacity_function_of_temperature_curve_name: str | None = ...,
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
    ) -> None:
        """Create a new ``Coil:Cooling:DX:MultiSpeed`` and add it to the document.

        Direct expansion (DX) cooling coil and condensing unit (includes electric or engine-driven compressor and condenser fan), multi-speed (or variable-speed). Optional moisture evaporation from wet coil when compressor cycles off with continuous fan operation. Requires two to four sets of performance data and will interpolate between speeds. Modeled as a single coil (multi-speed compressor or multiple compressors with row split or intertwined coil).

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-heating-and-cooling-coils/#coilcoolingdxmultispeed
        """

class CoilCoolingDXVariableRefrigerantFlow:
    def __call__(
        self,
        name: str,
        /,
        *,
        gross_rated_total_cooling_capacity: float | Literal["Autosize"],
        gross_rated_sensible_heat_ratio: float | Literal["Autosize"],
        rated_air_flow_rate: float | Literal["Autosize"],
        cooling_capacity_ratio_modifier_function_of_temperature_curve_name: str,
        cooling_capacity_modifier_curve_function_of_flow_fraction_name: str,
        coil_air_inlet_node: str,
        coil_air_outlet_node: str,
        availability_schedule_name: str | None = ...,
        name_of_water_storage_tank_for_condensate_collection: str | None = ...,
    ) -> None:
        """Create a new ``Coil:Cooling:DX:VariableRefrigerantFlow`` and add it to the document.

        Variable refrigerant flow (VRF) direct expansion (DX) cooling coil. Used with ZoneHVAC:TerminalUnit:VariableRefrigerantFlow. Condensing unit is modeled separately, see AirConditioner:VariableRefrigerantFlow.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-heating-and-cooling-coils/#coilcoolingdxvariablerefrigerantflow
        """

class AirLoopHVACUnitaryHeatPumpWaterToAir:
    def __call__(
        self,
        name: str,
        /,
        *,
        air_inlet_node_name: str,
        air_outlet_node_name: str,
        supply_air_flow_rate: float | Literal["Autosize"],
        controlling_zone_or_thermostat_location: str,
        supply_air_fan_object_type: Literal["Fan:OnOff"],
        supply_air_fan_name: str,
        heating_coil_object_type: Literal[
            "Coil:Heating:WaterToAirHeatPump:EquationFit",
            "Coil:Heating:WaterToAirHeatPump:ParameterEstimation",
            "Coil:Heating:WaterToAirHeatPump:VariableSpeedEquationFit",
        ],
        heating_coil_name: str,
        cooling_coil_object_type: Literal[
            "Coil:Cooling:WaterToAirHeatPump:EquationFit",
            "Coil:Cooling:WaterToAirHeatPump:ParameterEstimation",
            "Coil:Cooling:WaterToAirHeatPump:VariableSpeedEquationFit",
        ],
        cooling_coil_name: str,
        supplemental_heating_coil_object_type: Literal[
            "Coil:Heating:Electric", "Coil:Heating:Fuel", "Coil:Heating:Steam", "Coil:Heating:Water"
        ],
        supplemental_heating_coil_name: str,
        maximum_supply_air_temperature_from_supplemental_heater: float | Literal["Autosize"],
        availability_schedule_name: str | None = ...,
        heating_convergence: float | None = 0.001,
        cooling_convergence: float | None = 0.001,
        maximum_outdoor_dry_bulb_temperature_for_supplemental_heater_operation: float | None = 21,
        outdoor_dry_bulb_temperature_sensor_node_name: str | None = ...,
        fan_placement: Literal["", "BlowThrough", "DrawThrough"] | None = "BlowThrough",
        supply_air_fan_operating_mode_schedule_name: str | None = ...,
        dehumidification_control_type: Literal["", "CoolReheat", "None"] | None = "None",
        heat_pump_coil_water_flow_mode: Literal["", "Constant", "ConstantOnDemand", "Cycling"] | None = "Cycling",
        dx_heating_coil_sizing_ratio: float | None = 1,
    ) -> None:
        """Create a new ``AirLoopHVAC:UnitaryHeatPump:WaterToAir`` and add it to the document.

        Unitary heat pump system, heating and cooling, single-speed with constant volume supply fan (continuous or cycling), direct expansion (DX) cooling coil, DX heating coil (water-to-air heat pump), and supplemental heating coil (gas, electric, hot water, or steam).

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-unitary-equipment/#airloophvacunitaryheatpumpwatertoair
        """

class SolarCollectorFlatPlatePhotovoltaicThermal:
    def __call__(
        self,
        name: str = "",
        /,
        *,
        surface_name: str,
        photovoltaic_thermal_model_performance_name: str | None = ...,
        photovoltaic_name: str | None = ...,
        thermal_working_fluid_type: Literal["Air", "Water"] | None = ...,
        water_inlet_node_name: str | None = ...,
        water_outlet_node_name: str | None = ...,
        air_inlet_node_name: str | None = ...,
        air_outlet_node_name: str | None = ...,
        design_flow_rate: float | Literal["Autosize"] | None = ...,
    ) -> None:
        """Create a new ``SolarCollector:FlatPlate:PhotovoltaicThermal`` and add it to the document.

        Models hybrid photovoltaic-thermal (PVT) solar collectors that convert incident solar energy into both electricity and useful thermal energy by heating air or water.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-solar-collectors/#solarcollectorflatplatephotovoltaicthermal
        """

class HeatPumpAirToWater:
    def __call__(
        self,
        name: str,
        /,
        *,
        air_inlet_node_name: str,
        air_outlet_node_name: str,
        availability_schedule_name_heating: str | None = ...,
        availability_schedule_name_cooling: str | None = ...,
        operating_mode_control_method: Literal["", "EMSControlled", "Load", "ScheduledModes"] | None = "Load",
        operating_mode_control_option_for_multiple_unit: Literal[
            "", "Balanced", "CoolingPriority", "HeatingPriority", "SingleMode"
        ]
        | None = "SingleMode",
        operating_mode_control_schedule_name: str | None = ...,
        minimum_part_load_ratio: float | None = 0,
        rated_inlet_air_temperature_in_heating_mode: float | None = 8,
        rated_air_flow_rate_in_heating_mode: float | Literal["", "Autosize"] | None = "Autosize",
        rated_leaving_water_temperature_in_heating_mode: float | None = 40,
        rated_water_flow_rate_in_heating_mode: float | Literal["", "Autosize"] | None = "Autosize",
        minimum_outdoor_air_temperature_in_heating_mode: float | None = -30,
        maximum_outdoor_air_temperature_in_heating_mode: float | None = 100,
        minimum_leaving_water_temperature_curve_name_in_heating_mode: str | None = ...,
        maximum_leaving_water_temperature_curve_name_in_heating_mode: str | None = ...,
        sizing_factor_for_heating: float | None = 1,
        rated_inlet_air_temperature_in_cooling_mode: float | None = 30,
        rated_air_flow_rate_in_cooling_mode: float | Literal["", "Autosize"] | None = "Autosize",
        rated_leaving_water_temperature_in_cooling_mode: float | None = 8,
        rated_water_flow_rate_in_cooling_mode: float | Literal["", "Autosize"] | None = "Autosize",
        minimum_outdoor_air_temperature_in_cooling_mode: float | None = -30,
        maximum_outdoor_air_temperature_in_cooling_mode: float | None = 100,
        minimum_leaving_water_temperature_curve_name_in_cooling_mode: str | None = ...,
        maximum_leaving_water_temperature_curve_name_in_cooling_mode: str | None = ...,
        sizing_factor_for_cooling: float | None = 1,
        hot_water_inlet_node_name: str | None = ...,
        hot_water_outlet_node_name: str | None = ...,
        chilled_water_inlet_node_name: str | None = ...,
        chilled_water_outlet_node_name: str | None = ...,
        maximum_outdoor_dry_bulb_temperature_for_defrost_operation: float | None = 10,
        heat_pump_defrost_control: Literal["", "None", "OnDemand", "Timed", "TimedEmpirical"] | None = "None",
        heat_pump_defrost_time_period_fraction: float | None = 0.058333,
        resistive_defrost_heater_capacity: float | None = 0,
        defrost_energy_input_ratio_function_of_temperature_curve_name: str | None = ...,
        heat_pump_multiplier: int | None = 1,
        control_type: Literal["", "FixedSpeed", "VariableSpeed"] | None = "VariableSpeed",
        crankcase_heater_capacity: float | None = 0,
        crankcase_heater_capacity_function_of_temperature_curve_name: str | None = ...,
        maximum_ambient_temperature_for_crankcase_heater_operation: float | None = 10,
        number_of_speeds_for_heating: int | None = 1,
        rated_heating_capacity_at_speed_1: float | Literal["", "Autosize"] | None = "Autosize",
        rated_cop_for_heating_at_speed_1: float | None = 3,
        normalized_heating_capacity_function_of_temperature_curve_name_at_speed_1: str | None = ...,
        heating_energy_input_ratio_function_of_temperature_curve_name_at_speed_1: str | None = ...,
        heating_energy_input_ratio_function_of_plr_curve_name_at_speed_1: str | None = ...,
        rated_heating_capacity_at_speed_2: float | Literal["", "Autosize"] | None = "Autosize",
        rated_cop_for_heating_at_speed_2: float | None = ...,
        normalized_heating_capacity_function_of_temperature_curve_name_at_speed_2: str | None = ...,
        heating_energy_input_ratio_function_of_temperature_curve_name_at_speed_2: str | None = ...,
        heating_energy_input_ratio_function_of_plr_curve_name_at_speed_2: str | None = ...,
        rated_heating_capacity_at_speed_3: float | Literal["", "Autosize"] | None = "Autosize",
        rated_cop_for_heating_at_speed_3: float | None = ...,
        normalized_heating_capacity_function_of_temperature_curve_name_at_speed_3: str | None = ...,
        heating_energy_input_ratio_function_of_temperature_curve_name_at_speed_3: str | None = ...,
        heating_energy_input_ratio_function_of_plr_curve_name_at_speed_3: str | None = ...,
        rated_heating_capacity_at_speed_4: float | Literal["", "Autosize"] | None = "Autosize",
        rated_cop_for_heating_at_speed_4: float | None = ...,
        normalized_heating_capacity_function_of_temperature_curve_name_at_speed_4: str | None = ...,
        heating_energy_input_ratio_function_of_temperature_curve_name_at_speed_4: str | None = ...,
        heating_energy_input_ratio_function_of_plr_curve_name_at_speed_4: str | None = ...,
        rated_heating_capacity_at_speed_5: float | Literal["", "Autosize"] | None = "Autosize",
        rated_cop_for_heating_at_speed_5: float | None = ...,
        normalized_heating_capacity_function_of_temperature_curve_name_at_speed_5: str | None = ...,
        heating_energy_input_ratio_function_of_temperature_curve_name_at_speed_5: str | None = ...,
        heating_energy_input_ratio_function_of_plr_curve_name_at_speed_5: str | None = ...,
        booster_mode_on_heating: Literal["", "No", "Yes"] | None = "No",
        rated_heating_capacity_in_booster_mode: float | None = ...,
        rated_heating_cop_in_booster_mode: float | None = 3,
        normalized_heating_capacity_function_of_temperature_curve_name_in_booster_mode: str | None = ...,
        heating_energy_input_ratio_function_of_temperature_curve_name_in_booster_mode: str | None = ...,
        heating_energy_input_ratio_function_of_plr_curve_name_in_booster_mode: str | None = ...,
        number_of_speeds_for_cooling: int | None = 1,
        rated_cooling_capacity_at_speed_1: float | Literal["", "Autosize"] | None = "Autosize",
        rated_cop_for_cooling_at_speed_1: float | None = 3,
        normalized_cooling_capacity_function_of_temperature_curve_name_at_speed_1: str | None = ...,
        cooling_energy_input_ratio_function_of_temperature_curve_name_at_speed_1: str | None = ...,
        cooling_energy_input_ratio_function_of_plr_curve_name_at_speed_1: str | None = ...,
        rated_cooling_capacity_at_speed_2: float | Literal["", "Autosize"] | None = "Autosize",
        rated_cop_for_cooling_at_speed_2: float | None = ...,
        normalized_cooling_capacity_function_of_temperature_curve_name_at_speed_2: str | None = ...,
        cooling_energy_input_ratio_function_of_temperature_curve_name_at_speed_2: str | None = ...,
        cooling_energy_input_ratio_function_of_plr_curve_name_at_speed_2: str | None = ...,
        rated_cooling_capacity_at_speed_3: float | Literal["", "Autosize"] | None = "Autosize",
        rated_cop_for_cooling_at_speed_3: float | None = ...,
        normalized_cooling_capacity_function_of_temperature_curve_name_at_speed_3: str | None = ...,
        cooling_energy_input_ratio_function_of_temperature_curve_name_at_speed_3: str | None = ...,
        cooling_energy_input_ratio_function_of_plr_curve_name_at_speed_3: str | None = ...,
        rated_cooling_capacity_at_speed_4: float | Literal["", "Autosize"] | None = "Autosize",
        rated_cop_for_cooling_at_speed_4: float | None = ...,
        normalized_cooling_capacity_function_of_temperature_curve_name_at_speed_4: str | None = ...,
        cooling_energy_input_ratio_function_of_temperature_curve_name_at_speed_4: str | None = ...,
        cooling_energy_input_ratio_function_of_plr_curve_name_at_speed_4: str | None = ...,
        rated_cooling_capacity_at_speed_5: float | Literal["", "Autosize"] | None = "Autosize",
        rated_cop_for_cooling_at_speed_5: float | None = ...,
        normalized_cooling_capacity_function_of_temperature_curve_name_at_speed_5: str | None = ...,
        cooling_energy_input_ratio_function_of_temperature_curve_name_at_speed_5: str | None = ...,
        cooling_energy_input_ratio_function_of_plr_curve_name_at_speed_5: str | None = ...,
        booster_mode_on_cooling: Literal["", "No", "Yes"] | None = "No",
        rated_cooling_capacity_in_booster_mode: float | None = ...,
        rated_cooling_cop_in_booster_mode: float | None = 3,
        normalized_cooling_capacity_function_of_temperature_curve_name_in_booster_mode: str | None = ...,
        cooling_energy_input_ratio_function_of_temperature_curve_name_in_booster_mode: str | None = ...,
        cooling_energy_input_ratio_function_of_plr_curve_name_in_booster_mode: str | None = ...,
    ) -> None:
        """Create a new ``HeatPump:AirToWater`` and add it to the document.

        air-to-water heat pump system which provides either chilled or hot water with single- or variable speed compressors.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-plant-equipment/#heatpumpairtowater
        """

class AnyGroundHeatExchangerSurface:
    def __call__(
        self,
        name: str,
        /,
        *,
        construction_name: str,
        fluid_inlet_node_name: str,
        fluid_outlet_node_name: str,
        hydronic_tubing_inside_diameter: float | None = ...,
        number_of_tubing_circuits: int | None = ...,
        hydronic_tube_spacing: float | None = ...,
        surface_length: float | None = ...,
        surface_width: float | None = ...,
        lower_surface_environment: Literal["", "Exposed", "Ground"] | None = "Ground",
    ) -> None:
        """Create a new ``GroundHeatExchanger:Surface`` and add it to the document.

        A hydronic surface/panel consisting of a multi-layer construction with embedded rows of tubes. Typically used in hybrid geothermal systems and included in the condenser loop. This component may also be used as a simple solar collector. The bottom surface may be defined as ground-coupled or exposed to wind (eg. bridge deck).

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-condenser-equipment/#groundheatexchangersurface
        """

class GroundHeatExchangerSurface:
    def __call__(
        self,
        name: str,
        /,
        *,
        construction_name: str,
        fluid_inlet_node_name: str,
        fluid_outlet_node_name: str,
        hydronic_tubing_inside_diameter: float | None = ...,
        number_of_tubing_circuits: int | None = ...,
        hydronic_tube_spacing: float | None = ...,
        surface_length: float | None = ...,
        surface_width: float | None = ...,
        lower_surface_environment: Literal["", "Exposed", "Ground"] | None = "Ground",
    ) -> None:
        """Create a new ``GroundHeatExchanger:Surface`` and add it to the document.

        A hydronic surface/panel consisting of a multi-layer construction with embedded rows of tubes. Typically used in hybrid geothermal systems and included in the condenser loop. This component may also be used as a simple solar collector. The bottom surface may be defined as ground-coupled or exposed to wind (eg. bridge deck).

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-condenser-equipment/#groundheatexchangersurface
        """

class GroundHeatExchangerHorizontalTrench:
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
    ) -> None:
        """Create a new ``GroundHeatExchanger:HorizontalTrench`` and add it to the document.

        This models a horizontal heat exchanger placed in a series of trenches The model uses the PipingSystem:Underground underlying algorithms, but provides a more usable input interface.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-condenser-equipment/#groundheatexchangerhorizontaltrench
        """

class PlantEquipmentOperationSchemes:
    def __call__(
        self,
        name: str,
        /,
        *,
        control_scheme_1_object_type: Literal[
            "PlantEquipmentOperation:ChillerHeaterChangeover",
            "PlantEquipmentOperation:ComponentSetpoint",
            "PlantEquipmentOperation:CoolingLoad",
            "PlantEquipmentOperation:HeatingLoad",
            "PlantEquipmentOperation:OutdoorDewpoint",
            "PlantEquipmentOperation:OutdoorDewpointDifference",
            "PlantEquipmentOperation:OutdoorDryBulb",
            "PlantEquipmentOperation:OutdoorDryBulbDifference",
            "PlantEquipmentOperation:OutdoorRelativeHumidity",
            "PlantEquipmentOperation:OutdoorWetBulb",
            "PlantEquipmentOperation:OutdoorWetBulbDifference",
            "PlantEquipmentOperation:ThermalEnergyStorage",
            "PlantEquipmentOperation:Uncontrolled",
            "PlantEquipmentOperation:UserDefined",
        ],
        control_scheme_1_name: str,
        control_scheme_1_schedule_name: str,
        control_scheme_2_object_type: Literal[
            "PlantEquipmentOperation:ChillerHeaterChangeover",
            "PlantEquipmentOperation:ComponentSetpoint",
            "PlantEquipmentOperation:CoolingLoad",
            "PlantEquipmentOperation:HeatingLoad",
            "PlantEquipmentOperation:OutdoorDewpoint",
            "PlantEquipmentOperation:OutdoorDewpointDifference",
            "PlantEquipmentOperation:OutdoorDryBulb",
            "PlantEquipmentOperation:OutdoorDryBulbDifference",
            "PlantEquipmentOperation:OutdoorRelativeHumidity",
            "PlantEquipmentOperation:OutdoorWetBulb",
            "PlantEquipmentOperation:OutdoorWetBulbDifference",
            "PlantEquipmentOperation:ThermalEnergyStorage",
            "PlantEquipmentOperation:Uncontrolled",
            "PlantEquipmentOperation:UserDefined",
        ]
        | None = ...,
        control_scheme_2_name: str | None = ...,
        control_scheme_2_schedule_name: str | None = ...,
        control_scheme_3_object_type: Literal[
            "PlantEquipmentOperation:ChillerHeaterChangeover",
            "PlantEquipmentOperation:ComponentSetpoint",
            "PlantEquipmentOperation:CoolingLoad",
            "PlantEquipmentOperation:HeatingLoad",
            "PlantEquipmentOperation:OutdoorDewpoint",
            "PlantEquipmentOperation:OutdoorDewpointDifference",
            "PlantEquipmentOperation:OutdoorDryBulb",
            "PlantEquipmentOperation:OutdoorDryBulbDifference",
            "PlantEquipmentOperation:OutdoorRelativeHumidity",
            "PlantEquipmentOperation:OutdoorWetBulb",
            "PlantEquipmentOperation:OutdoorWetBulbDifference",
            "PlantEquipmentOperation:ThermalEnergyStorage",
            "PlantEquipmentOperation:Uncontrolled",
            "PlantEquipmentOperation:UserDefined",
        ]
        | None = ...,
        control_scheme_3_name: str | None = ...,
        control_scheme_3_schedule_name: str | None = ...,
        control_scheme_4_object_type: Literal[
            "PlantEquipmentOperation:ChillerHeaterChangeover",
            "PlantEquipmentOperation:ComponentSetpoint",
            "PlantEquipmentOperation:CoolingLoad",
            "PlantEquipmentOperation:HeatingLoad",
            "PlantEquipmentOperation:OutdoorDewpoint",
            "PlantEquipmentOperation:OutdoorDewpointDifference",
            "PlantEquipmentOperation:OutdoorDryBulb",
            "PlantEquipmentOperation:OutdoorDryBulbDifference",
            "PlantEquipmentOperation:OutdoorRelativeHumidity",
            "PlantEquipmentOperation:OutdoorWetBulb",
            "PlantEquipmentOperation:OutdoorWetBulbDifference",
            "PlantEquipmentOperation:ThermalEnergyStorage",
            "PlantEquipmentOperation:Uncontrolled",
            "PlantEquipmentOperation:UserDefined",
        ]
        | None = ...,
        control_scheme_4_name: str | None = ...,
        control_scheme_4_schedule_name: str | None = ...,
        control_scheme_5_object_type: Literal[
            "PlantEquipmentOperation:ChillerHeaterChangeover",
            "PlantEquipmentOperation:ComponentSetpoint",
            "PlantEquipmentOperation:CoolingLoad",
            "PlantEquipmentOperation:HeatingLoad",
            "PlantEquipmentOperation:OutdoorDewpoint",
            "PlantEquipmentOperation:OutdoorDewpointDifference",
            "PlantEquipmentOperation:OutdoorDryBulb",
            "PlantEquipmentOperation:OutdoorDryBulbDifference",
            "PlantEquipmentOperation:OutdoorRelativeHumidity",
            "PlantEquipmentOperation:OutdoorWetBulb",
            "PlantEquipmentOperation:OutdoorWetBulbDifference",
            "PlantEquipmentOperation:ThermalEnergyStorage",
            "PlantEquipmentOperation:Uncontrolled",
            "PlantEquipmentOperation:UserDefined",
        ]
        | None = ...,
        control_scheme_5_name: str | None = ...,
        control_scheme_5_schedule_name: str | None = ...,
        control_scheme_6_object_type: Literal[
            "PlantEquipmentOperation:ChillerHeaterChangeover",
            "PlantEquipmentOperation:ComponentSetpoint",
            "PlantEquipmentOperation:CoolingLoad",
            "PlantEquipmentOperation:HeatingLoad",
            "PlantEquipmentOperation:OutdoorDewpoint",
            "PlantEquipmentOperation:OutdoorDewpointDifference",
            "PlantEquipmentOperation:OutdoorDryBulb",
            "PlantEquipmentOperation:OutdoorDryBulbDifference",
            "PlantEquipmentOperation:OutdoorRelativeHumidity",
            "PlantEquipmentOperation:OutdoorWetBulb",
            "PlantEquipmentOperation:OutdoorWetBulbDifference",
            "PlantEquipmentOperation:ThermalEnergyStorage",
            "PlantEquipmentOperation:Uncontrolled",
            "PlantEquipmentOperation:UserDefined",
        ]
        | None = ...,
        control_scheme_6_name: str | None = ...,
        control_scheme_6_schedule_name: str | None = ...,
        control_scheme_7_object_type: Literal[
            "PlantEquipmentOperation:ChillerHeaterChangeover",
            "PlantEquipmentOperation:ComponentSetpoint",
            "PlantEquipmentOperation:CoolingLoad",
            "PlantEquipmentOperation:HeatingLoad",
            "PlantEquipmentOperation:OutdoorDewpoint",
            "PlantEquipmentOperation:OutdoorDewpointDifference",
            "PlantEquipmentOperation:OutdoorDryBulb",
            "PlantEquipmentOperation:OutdoorDryBulbDifference",
            "PlantEquipmentOperation:OutdoorRelativeHumidity",
            "PlantEquipmentOperation:OutdoorWetBulb",
            "PlantEquipmentOperation:OutdoorWetBulbDifference",
            "PlantEquipmentOperation:ThermalEnergyStorage",
            "PlantEquipmentOperation:Uncontrolled",
            "PlantEquipmentOperation:UserDefined",
        ]
        | None = ...,
        control_scheme_7_name: str | None = ...,
        control_scheme_7_schedule_name: str | None = ...,
        control_scheme_8_object_type: Literal[
            "PlantEquipmentOperation:ChillerHeaterChangeover",
            "PlantEquipmentOperation:ComponentSetpoint",
            "PlantEquipmentOperation:CoolingLoad",
            "PlantEquipmentOperation:HeatingLoad",
            "PlantEquipmentOperation:OutdoorDewpoint",
            "PlantEquipmentOperation:OutdoorDewpointDifference",
            "PlantEquipmentOperation:OutdoorDryBulb",
            "PlantEquipmentOperation:OutdoorDryBulbDifference",
            "PlantEquipmentOperation:OutdoorRelativeHumidity",
            "PlantEquipmentOperation:OutdoorWetBulb",
            "PlantEquipmentOperation:OutdoorWetBulbDifference",
            "PlantEquipmentOperation:ThermalEnergyStorage",
            "PlantEquipmentOperation:Uncontrolled",
            "PlantEquipmentOperation:UserDefined",
        ]
        | None = ...,
        control_scheme_8_name: str | None = ...,
        control_scheme_8_schedule_name: str | None = ...,
    ) -> None:
        """Create a new ``PlantEquipmentOperationSchemes`` and add it to the document.

        Operation schemes are listed in 'priority' order. Note that each scheme must address the entire load and/or condition ranges for the simulation. The actual one selected for use will be the first that is 'Scheduled' on. That is, if control scheme 1 is not 'on' and control scheme 2 is -- then control scheme 2 is selected. Only plant equipment should be listed on a Control Scheme for this item.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-plant-condenser-control/#plantequipmentoperationschemes
        """

class ZoneHVACForcedAirUserDefined:
    def __call__(
        self,
        name: str,
        /,
        *,
        primary_air_inlet_node_name: str,
        primary_air_outlet_node_name: str,
        number_of_plant_loop_connections: int,
        overall_model_simulation_program_calling_manager_name: str | None = ...,
        model_setup_and_sizing_program_calling_manager_name: str | None = ...,
        secondary_air_inlet_node_name: str | None = ...,
        secondary_air_outlet_node_name: str | None = ...,
        plant_connection_1_inlet_node_name: str | None = ...,
        plant_connection_1_outlet_node_name: str | None = ...,
        plant_connection_2_inlet_node_name: str | None = ...,
        plant_connection_2_outlet_node_name: str | None = ...,
        plant_connection_3_inlet_node_name: str | None = ...,
        plant_connection_3_outlet_node_name: str | None = ...,
        supply_inlet_water_storage_tank_name: str | None = ...,
        collection_outlet_water_storage_tank_name: str | None = ...,
        ambient_zone_name: str | None = ...,
    ) -> None:
        """Create a new ``ZoneHVAC:ForcedAir:UserDefined`` and add it to the document.

        Defines a generic zone air unit for custom modeling using Energy Management System or External Interface

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-user-defined-hvac-and-plant-component/#zonehvacforcedairuserdefined
        """

class AnyPlantComponentUserDefined:
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

class SetpointManagerFollowGroundTemperature:
    def __call__(
        self,
        name: str,
        /,
        *,
        setpoint_node_or_nodelist_name: str,
        control_variable: Literal["", "MaximumTemperature", "MinimumTemperature", "Temperature"] | None = "Temperature",
        reference_ground_temperature_object_type: Literal[
            "Site:GroundTemperature:BuildingSurface",
            "Site:GroundTemperature:Deep",
            "Site:GroundTemperature:FCfactorMethod",
            "Site:GroundTemperature:Shallow",
        ]
        | None = ...,
        offset_temperature_difference: float | None = ...,
        maximum_setpoint_temperature: float | None = ...,
        minimum_setpoint_temperature: float | None = ...,
    ) -> None:
        """Create a new ``SetpointManager:FollowGroundTemperature`` and add it to the document.

        This setpoint manager is used to place a temperature setpoint on a system node that is derived from a current ground temperature. The ground temperatures are specified in different Site:GroundTemperature:* objects and used during the simulation. This setpoint manager is primarily intended for condenser or plant loops using some type of ground heat exchanger.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-setpoint-managers/#setpointmanagerfollowgroundtemperature
        """

class RefrigerationCondenserWaterCooled:
    def __call__(
        self,
        name: str,
        /,
        *,
        rated_condensing_temperature: float,
        rated_water_inlet_temperature: float,
        rated_effective_total_heat_rejection_rate: float | None = ...,
        rated_subcooling_temperature_difference: float | None = 0,
        water_inlet_node_name: str | None = ...,
        water_outlet_node_name: str | None = ...,
        water_cooled_loop_flow_type: Literal["", "ConstantFlow", "VariableFlow"] | None = "VariableFlow",
        water_outlet_temperature_schedule_name: str | None = ...,
        water_design_flow_rate: float | None = ...,
        water_maximum_flow_rate: float | None = ...,
        water_maximum_water_outlet_temperature: float | None = 55,
        water_minimum_water_inlet_temperature: float | None = 10,
        end_use_subcategory: str | None = "General",
        condenser_refrigerant_operating_charge_inventory: float | None = ...,
        condensate_receiver_refrigerant_inventory: float | None = ...,
        condensate_piping_refrigerant_inventory: float | None = ...,
    ) -> None:
        """Create a new ``Refrigeration:Condenser:WaterCooled`` and add it to the document.

        Water cooled condenser for a refrigeration system (Refrigeration:System).

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-refrigeration/#refrigerationcondenserwatercooled
        """

class AnyGeneratorCombustionTurbine:
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
        part_load_based_fuel_input_curve_name: str | None = ...,
        temperature_based_fuel_input_curve_name: str | None = ...,
        exhaust_flow_curve_name: str | None = ...,
        part_load_based_exhaust_temperature_curve_name: str | None = ...,
        temperature_based_exhaust_temperature_curve_name: str | None = ...,
        heat_recovery_lube_energy_curve_name: str | None = ...,
        coefficient_1_of_u_factor_times_area_curve: float | None = ...,
        coefficient_2_of_u_factor_times_area_curve: float | None = ...,
        maximum_exhaust_flow_per_unit_of_power_output: float | None = ...,
        design_minimum_exhaust_temperature: float | None = ...,
        design_air_inlet_temperature: float | None = ...,
        fuel_higher_heating_value: float | None = ...,
        design_heat_recovery_water_flow_rate: float | None = 0,
        heat_recovery_inlet_node_name: str | None = ...,
        heat_recovery_outlet_node_name: str | None = ...,
        fuel_type: Literal["", "Diesel", "Gasoline", "NaturalGas", "OtherFuel1", "OtherFuel2"] | None = "NaturalGas",
        heat_recovery_maximum_temperature: float | None = 80,
        outdoor_air_inlet_node_name: str | None = ...,
    ) -> None:
        """Create a new ``Generator:CombustionTurbine`` and add it to the document.

        This generator model is the empirical model from the Building Loads and System Thermodynamics (BLAST) program. Generator performance curves are generated by fitting catalog data to second order polynomial equations. Three sets of coefficients are required.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-electric-load-center-generator/#generatorcombustionturbine
        """

class GeneratorCombustionTurbine:
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
        part_load_based_fuel_input_curve_name: str | None = ...,
        temperature_based_fuel_input_curve_name: str | None = ...,
        exhaust_flow_curve_name: str | None = ...,
        part_load_based_exhaust_temperature_curve_name: str | None = ...,
        temperature_based_exhaust_temperature_curve_name: str | None = ...,
        heat_recovery_lube_energy_curve_name: str | None = ...,
        coefficient_1_of_u_factor_times_area_curve: float | None = ...,
        coefficient_2_of_u_factor_times_area_curve: float | None = ...,
        maximum_exhaust_flow_per_unit_of_power_output: float | None = ...,
        design_minimum_exhaust_temperature: float | None = ...,
        design_air_inlet_temperature: float | None = ...,
        fuel_higher_heating_value: float | None = ...,
        design_heat_recovery_water_flow_rate: float | None = 0,
        heat_recovery_inlet_node_name: str | None = ...,
        heat_recovery_outlet_node_name: str | None = ...,
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
        heat_recovery_maximum_temperature: float | None = 80,
        outdoor_air_inlet_node_name: str | None = ...,
    ) -> None:
        """Create a new ``Generator:CombustionTurbine`` and add it to the document.

        This generator model is the empirical model from the Building Loads and System Thermodynamics (BLAST) program. Generator performance curves are generated by fitting catalog data to second order polynomial equations. Three sets of coefficients are required.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-electric-load-center-generator/#generatorcombustionturbine
        """

class PhotovoltaicPerformanceSimple:
    def __call__(
        self,
        name: str,
        /,
        *,
        fraction_of_surface_area_with_active_solar_cells: float,
        conversion_efficiency_input_mode: Literal["Fixed", "Scheduled"] | None = ...,
        value_for_cell_efficiency_if_fixed: float | None = ...,
        efficiency_schedule_name: str | None = ...,
    ) -> None:
        """Create a new ``PhotovoltaicPerformance:Simple`` and add it to the document.

        Describes a simple model of photovoltaics that may be useful for early phase design analysis. In this model the user has direct access to the efficiency with which surfaces convert incident solar radiation to electricity and need not specify arrays of specific modules.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-electric-load-center-generator/#photovoltaicperformancesimple
        """

class ElectricLoadCenterStorageLiIonNMCBattery:
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

class AnyComponentCostLineItem:
    def __call__(
        self,
        name: str = "",
        /,
        *,
        line_item_type: Literal[
            "Chiller:Electric",
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

class UtilityCostChargeSimple:
    def __call__(
        self,
        /,
        *,
        utility_cost_charge_simple_name: str,
        tariff_name: str,
        source_variable: str,
        category_variable_name: Literal[
            "Adjustment",
            "Basis",
            "DemandCharges",
            "EnergyCharges",
            "NotIncluded",
            "ServiceCharges",
            "Subtotal",
            "Surcharge",
            "Taxes",
            "Total",
        ],
        cost_per_unit_value_or_variable_name: float | str,
        season: Literal["Annual", "Fall", "Spring", "Summer", "Winter"] | None = ...,
    ) -> None:
        """Create a new ``UtilityCost:Charge:Simple`` and add it to the document.

        UtilityCost:Charge:Simple is one of the most often used objects for tariff calculation. It is used to compute energy and demand charges that are very simple. It may also be used for taxes, surcharges and any other charges that occur on a utility bill. Multiple UtilityCost:Charge:Simple objects may be defined for a single tariff and they will be added together.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/energyplus-economics/utilitycost-charge-simple/#utilitycostchargesimple
        """

class OutputTableMonthly:
    def __call__(
        self,
        name: str,
        /,
        *,
        digits_after_decimal: int | None = 2,
        variable_details: list[_g.OutputTableMonthlyVariableDetailsItem] = ...,
    ) -> None:
        """Create a new ``Output:Table:Monthly`` and add it to the document.

        Provides a generic method of setting up tables of monthly results. The report has multiple columns that are each defined using a repeated group of fields for any number of columns. A single Output:Table:Monthly object often produces multiple tables in the output. A table is produced for every instance of a particular output variable. For example, a table defined with zone variables will be produced once for every zone.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/standard-output-reports/output-table-monthly/#outputtablemonthly
        """

class AnyOutputTableReportPeriod:
    def __call__(
        self,
        name: str,
        /,
        *,
        narrow_with_as_version_first: Never,
        begin_month: int,
        begin_day_of_month: int,
        begin_hour_of_day: int,
        end_month: int,
        end_day_of_month: int,
        end_hour_of_day: int,
        report_name: Literal[
            "AllResilienceSummaries", "CO2ResilienceSummary", "ThermalResilienceSummary", "VisualResilienceSummary"
        ]
        | None = ...,
        begin_year: int | None = ...,
        end_year: int | None = ...,
    ) -> None:
        """Create a new ``Output:Table:ReportPeriod`` and add it to the document.

        This object allows the user to generate the resilience tabular reports over a subset of a run period. When it is defined, a series of reporting-period-specific resilience summary tables will be generated at the end of all tabular reports. Multiple reporting periods may be input.

        No call suits every release: narrow the document with ``as_version`` first.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/standard-output-reports/output-table-reportperiod/#outputtablereportperiod
        """

class AnyFuelFactors:
    def __call__(
        self,
        /,
        *,
        existing_fuel_resource_name: Literal[
            "Coal",
            "Diesel",
            "Electricity",
            "FuelOilNo1",
            "FuelOilNo2",
            "Gasoline",
            "NaturalGas",
            "OtherFuel1",
            "OtherFuel2",
            "Propane",
        ]
        | None = ...,
        source_energy_factor: float | None = ...,
        source_energy_schedule_name: str | None = ...,
        co2_emission_factor: float | None = ...,
        co2_emission_factor_schedule_name: str | None = ...,
        co_emission_factor: float | None = ...,
        co_emission_factor_schedule_name: str | None = ...,
        ch4_emission_factor: float | None = ...,
        ch4_emission_factor_schedule_name: str | None = ...,
        nox_emission_factor: float | None = ...,
        nox_emission_factor_schedule_name: str | None = ...,
        n2o_emission_factor: float | None = ...,
        n2o_emission_factor_schedule_name: str | None = ...,
        so2_emission_factor: float | None = ...,
        so2_emission_factor_schedule_name: str | None = ...,
        pm_emission_factor: float | None = ...,
        pm_emission_factor_schedule_name: str | None = ...,
        pm10_emission_factor: float | None = ...,
        pm10_emission_factor_schedule_name: str | None = ...,
        pm2_5_emission_factor: float | None = ...,
        pm2_5_emission_factor_schedule_name: str | None = ...,
        nh3_emission_factor: float | None = ...,
        nh3_emission_factor_schedule_name: str | None = ...,
        nmvoc_emission_factor: float | None = ...,
        nmvoc_emission_factor_schedule_name: str | None = ...,
        hg_emission_factor: float | None = ...,
        hg_emission_factor_schedule_name: str | None = ...,
        pb_emission_factor: float | None = ...,
        pb_emission_factor_schedule_name: str | None = ...,
        water_emission_factor: float | None = ...,
        water_emission_factor_schedule_name: str | None = ...,
        nuclear_high_level_emission_factor: float | None = ...,
        nuclear_high_level_emission_factor_schedule_name: str | None = ...,
        nuclear_low_level_emission_factor: float | None = ...,
        nuclear_low_level_emission_factor_schedule_name: str | None = ...,
    ) -> None:
        """Create a new ``FuelFactors`` and add it to the document.

        Provides Fuel Factors for Emissions as well as Source=>Site conversions. OtherFuel1, OtherFuel2 provide options for users who want to create and use fuels that may not be mainstream (biomass, wood, pellets).

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/input-for-output/#fuelfactors
        """

class PythonPluginVariables:
    def __call__(self, name: str, /, *, global_py_vars: list[_g.PythonPluginVariablesGlobalPyVarsItem] = ...) -> None:
        """Create a new ``PythonPlugin:Variables`` and add it to the document.

        This object defines name identifiers for custom Python Plugin variable data that should be shared among all running Python Plugins.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-python-plugins/#pythonpluginvariables
        """
