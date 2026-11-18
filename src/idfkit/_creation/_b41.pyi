"""Creation signatures of generated classes (stub only).

DO NOT EDIT — regenerate with:
    python -m idfkit.codegen.generate_stubs
"""

from __future__ import annotations

from collections.abc import Sequence
from typing import Literal

from .. import _generated_types as _g

class AnyHVACSystemRootFindingAlgorithm:
    def __call__(
        self,
        this_type_has_no_name_field: _g._PassFieldsAsKeywords = ...,
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

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-simulation-parameters/#hvacsystemrootfindingalgorithm
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

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-internal-gains-people-lights-other/#electricequipment
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

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-airflow-network/#airflownetworkmultizonecomponentsimpleopening
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

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-air-distribution-equipment/#airterminalsingleductconstantvolumefourpipeinduction
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

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-heating-and-cooling-coils/#coilcoolingdxsinglespeedthermalstorage
        """

class Branch:
    def __call__(
        self,
        name: str,
        /,
        *,
        pressure_drop_curve_name: str | None = ...,
        components: Sequence[_g.BranchComponentsItem | _g.BranchComponentsGroup] = ...,
    ) -> None:
        """Create a new ``Branch`` and add it to the document.

        List components on the branch in simulation and connection order Note: this should NOT include splitters or mixers which define endpoints of branches

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-node-branch-management/#branch
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

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-refrigeration/#refrigerationairchiller
        """

class OutputControlTableStyle:
    def __call__(
        self,
        this_type_has_no_name_field: _g._PassFieldsAsKeywords = ...,
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

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/standard-output-reports/outputcontrol-table-style/#outputcontroltablestyle
        """

class AnyPythonPluginVariables:
    def __call__(self, name: str, /) -> None:
        """Create a new ``PythonPlugin:Variables`` and add it to the document.

        This object defines name identifiers for custom Python Plugin variable data that should be shared among all running Python Plugins.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-python-plugins/#pythonpluginvariables
        """
