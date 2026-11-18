"""Creation signatures of generated classes (stub only).

DO NOT EDIT — regenerate with:
    python -m idfkit.codegen.generate_stubs
"""

from __future__ import annotations

from collections.abc import Sequence
from typing import Literal

from typing_extensions import Never

from .. import _generated_types as _g

class AnySiteGroundTemperatureUndisturbedXing:
    def __call__(
        self,
        name: str,
        /,
        *,
        narrow_with_as_version_first: Never,
        soil_thermal_conductivity: float,
        soil_density: float,
        soil_specific_heat: float,
        soil_surface_temperature_amplitude_1: float,
        soil_surface_temperature_amplitude_2: float,
        phase_shift_of_temperature_amplitude_1: float,
        phase_shift_of_temperature_amplitude_2: float,
    ) -> None:
        """Create a new ``Site:GroundTemperature:Undisturbed:Xing`` and add it to the document.

        Undisturbed ground temperature object using the Xing 2014 2 harmonic parameter model.

        No call suits every release: narrow the document with ``as_version`` first.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-location-climate-weather-file-access/#sitegroundtemperatureundisturbedxing
        """

class ScheduleWeekCompact:
    def __call__(
        self, name: str, /, *, data: Sequence[_g.ScheduleWeekCompactDataItem | _g.ScheduleWeekCompactDataGroup] = ...
    ) -> None:
        """Create a new ``Schedule:Week:Compact`` and add it to the document.

        Compact definition for Schedule:Day:List

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-schedules/#scheduleweekcompact
        """

class AnyMaterialPropertyHeatAndMoistureTransferRedistribution:
    def __call__(
        self,
        /,
        *,
        material_name: str,
        number_of_redistribution_points: int,
        moisture_content_1: float,
        liquid_transport_coefficient_1: float,
        moisture_content_2: float | None = ...,
        liquid_transport_coefficient_2: float | None = ...,
        moisture_content_3: float | None = ...,
        liquid_transport_coefficient_3: float | None = ...,
        moisture_content_4: float | None = ...,
        liquid_transport_coefficient_4: float | None = ...,
        moisture_content_5: float | None = ...,
        liquid_transport_coefficient_5: float | None = ...,
        moisture_content_6: float | None = ...,
        liquid_transport_coefficient_6: float | None = ...,
        moisture_content_7: float | None = ...,
        liquid_transport_coefficient_7: float | None = ...,
        moisture_content_8: float | None = ...,
        liquid_transport_coefficient_8: float | None = ...,
        moisture_content_9: float | None = ...,
        liquid_transport_coefficient_9: float | None = ...,
        moisture_content_10: float | None = ...,
        liquid_transport_coefficient_10: float | None = ...,
        moisture_content_11: float | None = ...,
        liquid_transport_coefficient_11: float | None = ...,
        moisture_content_12: float | None = ...,
        liquid_transport_coefficient_12: float | None = ...,
        moisture_content_13: float | None = ...,
        liquid_transport_coefficient_13: float | None = ...,
        moisture_content_14: float | None = ...,
        liquid_transport_coefficient_14: float | None = ...,
        moisture_content_15: float | None = ...,
        liquid_transport_coefficient_15: float | None = ...,
        moisture_content_16: float | None = ...,
        liquid_transport_coefficient_16: float | None = ...,
        moisture_content_17: float | None = ...,
        liquid_transport_coefficient_17: float | None = ...,
        moisture_content_18: float | None = ...,
        liquid_transport_coefficient_18: float | None = ...,
        moisture_content_19: float | None = ...,
        liquid_transport_coefficient_19: float | None = ...,
        moisture_content_20: float | None = ...,
        liquid_transport_coefficient_20: float | None = ...,
        moisture_content_21: float | None = ...,
        liquid_transport_coefficient_21: float | None = ...,
        moisture_content_22: float | None = ...,
        liquid_transport_coefficient_22: float | None = ...,
        moisture_content_23: float | None = ...,
        liquid_transport_coefficient_23: float | None = ...,
        moisture_content_24: float | None = ...,
        liquid_transport_coefficient_24: float | None = ...,
        moisture_content_25: float | None = ...,
        liquid_transport_coefficient_25: float | None = ...,
    ) -> None:
        """Create a new ``MaterialProperty:HeatAndMoistureTransfer:Redistribution`` and add it to the document.

        HeatBalanceAlgorithm = CombinedHeatAndMoistureFiniteElement solution algorithm only. Relationship between liquid transport coefficient and moisture content Has no effect with other HeatBalanceAlgorithm solution algorithms

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-surface-construction-elements/#materialpropertyheatandmoisturetransferredistribution
        """

class AnySwimmingPoolIndoor:
    def __call__(
        self,
        name: str,
        /,
        *,
        surface_name: str,
        average_depth: float,
        activity_factor_schedule_name: str,
        make_up_water_supply_schedule_name: str,
        cover_schedule_name: str,
        pool_water_inlet_node: str,
        pool_water_outlet_node: str,
        setpoint_temperature_schedule: str,
        maximum_number_of_people: float,
        cover_evaporation_factor: float | None = 0,
        cover_convection_factor: float | None = 0,
        cover_short_wavelength_radiation_factor: float | None = 0,
        cover_long_wavelength_radiation_factor: float | None = 0,
        pool_heating_system_maximum_water_flow_rate: float | None = ...,
        pool_miscellaneous_equipment_power: float | None = ...,
        people_schedule: str | None = ...,
        people_heat_gain_schedule: str | None = ...,
    ) -> None:
        """Create a new ``SwimmingPool:Indoor`` and add it to the document.

        Specifies an indoor swimming pools linked to a floor surface. The pool is assumed to cover the entire floor to which it is linked.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-internal-gains-people-lights-other/#swimmingpoolindoor
        """

class ZoneHVACHybridUnitaryHVAC:
    def __call__(
        self,
        name: str,
        /,
        *,
        return_air_node_name: str,
        outdoor_air_node_name: str,
        supply_air_node_name: str,
        availability_schedule_name: str | None = ...,
        availability_manager_list_name: str | None = ...,
        minimum_supply_air_temperature_schedule_name: str | None = ...,
        maximum_supply_air_temperature_schedule_name: str | None = ...,
        minimum_supply_air_humidity_ratio_schedule_name: str | None = ...,
        maximum_supply_air_humidity_ratio_schedule_name: str | None = ...,
        method_to_choose_controlled_inputs_and_part_runtime_fraction: Literal["Automatic", "User Defined"]
        | None = "Automatic",
        relief_node_name: str | None = ...,
        system_maximum_supply_air_flow_rate: float | None = ...,
        external_static_pressure_at_system_maximum_supply_air_flow_rate: float | None = ...,
        fan_heat_included_in_lookup_tables: Literal["No", "Yes"] | None = "No",
        fan_heat_gain_location: Literal["MixedAirStream", "SupplyAirStream"] | None = "SupplyAirStream",
        fan_heat_in_air_stream_fraction: float | None = 1,
        scaling_factor: float | None = 1,
        minimum_time_between_mode_change: float | None = 10,
        first_fuel_type: Literal[
            "Coal",
            "Diesel",
            "DistrictCooling",
            "DistrictHeatingSteam",
            "DistrictHeatingWater",
            "Electricity",
            "FuelOilNo1",
            "FuelOilNo2",
            "Gasoline",
            "NaturalGas",
            "None",
            "OtherFuel1",
            "OtherFuel2",
            "Propane",
        ]
        | None = "Electricity",
        second_fuel_type: Literal[
            "Coal",
            "Diesel",
            "DistrictCooling",
            "DistrictHeatingSteam",
            "DistrictHeatingWater",
            "Electricity",
            "FuelOilNo1",
            "FuelOilNo2",
            "Gasoline",
            "NaturalGas",
            "None",
            "OtherFuel1",
            "OtherFuel2",
            "Propane",
        ]
        | None = "None",
        third_fuel_type: Literal[
            "Coal",
            "Diesel",
            "DistrictCooling",
            "DistrictHeatingSteam",
            "DistrictHeatingWater",
            "Electricity",
            "FuelOilNo1",
            "FuelOilNo2",
            "Gasoline",
            "NaturalGas",
            "None",
            "OtherFuel1",
            "OtherFuel2",
            "Propane",
        ]
        | None = "None",
        objective_function_to_minimize: Literal["Electricity Use", "Second Fuel Use", "Third Fuel Use", "Water Use"]
        | None = "Electricity Use",
        design_specification_outdoor_air_object_name: str | None = ...,
        mode_0_name: str | None = ...,
        mode_0_supply_air_temperature_lookup_table_name: str | None = ...,
        mode_0_supply_air_humidity_ratio_lookup_table_name: str | None = ...,
        mode_0_system_electric_power_lookup_table_name: str | None = ...,
        mode_0_supply_fan_electric_power_lookup_table_name: str | None = ...,
        mode_0_external_static_pressure_lookup_table_name: str | None = ...,
        mode_0_system_second_fuel_consumption_lookup_table_name: str | None = ...,
        mode_0_system_third_fuel_consumption_lookup_table_name: str | None = ...,
        mode_0_system_water_use_lookup_table_name: str | None = ...,
        mode_0_outdoor_air_fraction: float | None = 0,
        mode_0_supply_air_mass_flow_rate_ratio: float | None = 0,
        modes: Sequence[_g.ZoneHVACHybridUnitaryHVACModesItem | _g.ZoneHVACHybridUnitaryHVACModesGroup] = ...,
    ) -> None:
        """Create a new ``ZoneHVAC:HybridUnitaryHVAC`` and add it to the document.

        Hybrid Unitary HVAC. A black box model for multi-mode packaged forced air equipment. Independent variables include outdoor air conditions and indoor air conditions. Controlled inputs include operating mode, supply air flow rate, and outdoor air faction. Empirical lookup tables are required to map supply air temperature supply air humidity, electricity use, fuel uses, water use, fan electricity use, and external static pressure as a function of each independent variable and each controlled input. In each timestep the model will choose one or more combinations of settings for mode, supply air flow rate, outdoor air faction, and part runtime fraction so as to satisfy zone requests for sensible cooling, heating, ventilation, and/or dehumidification with the least resource consumption. Equipment in this class may consume electricity, water, and up to two additional fuel types.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-zone-forced-air-units/#zonehvachybridunitaryhvac
        """

class AnyUnitarySystemPerformanceMultispeed:
    def __call__(
        self,
        name: str,
        /,
        *,
        number_of_speeds_for_heating: int,
        number_of_speeds_for_cooling: int,
        single_mode_operation: Literal["No", "Yes"] | None = "No",
        no_load_supply_air_flow_rate_ratio: float | None = 1,
        flow_ratios: Sequence[
            _g.UnitarySystemPerformanceMultispeedFlowRatiosItem | _g.UnitarySystemPerformanceMultispeedFlowRatiosGroup
        ] = ...,
    ) -> None:
        """Create a new ``UnitarySystemPerformance:Multispeed`` and add it to the document.

        The UnitarySystemPerformance object is used to specify the air flow ratio at each operating speed. This object is primarily used for multispeed DX and water coils to allow operation at alternate flow rates different from those specified in the coil object.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-unitary-equipment/#unitarysystemperformancemultispeed
        """

class ChillerCombustionTurbine:
    def __call__(
        self,
        name: str,
        /,
        *,
        nominal_capacity: float | Literal["Autosize"],
        nominal_cop: float,
        chilled_water_inlet_node_name: str,
        chilled_water_outlet_node_name: str,
        temperature_rise_coefficient: float,
        condenser_type: Literal["AirCooled", "EvaporativelyCooled", "WaterCooled"] | None = "AirCooled",
        condenser_inlet_node_name: str | None = ...,
        condenser_outlet_node_name: str | None = ...,
        minimum_part_load_ratio: float | None = ...,
        maximum_part_load_ratio: float | None = ...,
        optimum_part_load_ratio: float | None = ...,
        design_condenser_inlet_temperature: float | None = ...,
        design_chilled_water_outlet_temperature: float | None = ...,
        design_chilled_water_flow_rate: float | Literal["Autosize"] | None = ...,
        design_condenser_water_flow_rate: float | Literal["Autosize"] | None = ...,
        coefficient_1_of_capacity_ratio_curve: float | None = ...,
        coefficient_2_of_capacity_ratio_curve: float | None = ...,
        coefficient_3_of_capacity_ratio_curve: float | None = ...,
        coefficient_1_of_power_ratio_curve: float | None = ...,
        coefficient_2_of_power_ratio_curve: float | None = ...,
        coefficient_3_of_power_ratio_curve: float | None = ...,
        coefficient_1_of_full_load_ratio_curve: float | None = ...,
        coefficient_2_of_full_load_ratio_curve: float | None = ...,
        coefficient_3_of_full_load_ratio_curve: float | None = ...,
        chilled_water_outlet_temperature_lower_limit: float | None = ...,
        coefficient_1_of_fuel_input_curve: float | None = ...,
        coefficient_2_of_fuel_input_curve: float | None = ...,
        coefficient_3_of_fuel_input_curve: float | None = ...,
        coefficient_1_of_temperature_based_fuel_input_curve: float | None = ...,
        coefficient_2_of_temperature_based_fuel_input_curve: float | None = ...,
        coefficient_3_of_temperature_based_fuel_input_curve: float | None = ...,
        coefficient_1_of_exhaust_flow_curve: float | None = ...,
        coefficient_2_of_exhaust_flow_curve: float | None = ...,
        coefficient_3_of_exhaust_flow_curve: float | None = ...,
        coefficient_1_of_exhaust_gas_temperature_curve: float | None = ...,
        coefficient_2_of_exhaust_gas_temperature_curve: float | None = ...,
        coefficient_3_of_exhaust_gas_temperature_curve: float | None = ...,
        coefficient_1_of_temperature_based_exhaust_gas_temperature_curve: float | None = ...,
        coefficient_2_of_temperature_based_exhaust_gas_temperature_curve: float | None = ...,
        coefficient_3_of_temperature_based_exhaust_gas_temperature_curve: float | None = ...,
        coefficient_1_of_recovery_lube_heat_curve: float | None = ...,
        coefficient_2_of_recovery_lube_heat_curve: float | None = ...,
        coefficient_3_of_recovery_lube_heat_curve: float | None = ...,
        coefficient_1_of_u_factor_times_area_curve: float | None = ...,
        coefficient_2_of_u_factor_times_area_curve: float | None = ...,
        gas_turbine_engine_capacity: float | Literal["Autosize"] | None = ...,
        maximum_exhaust_flow_per_unit_of_power_output: float | None = ...,
        design_steam_saturation_temperature: float | None = ...,
        fuel_higher_heating_value: float | None = ...,
        design_heat_recovery_water_flow_rate: float | Literal["Autosize"] | None = 0,
        heat_recovery_inlet_node_name: str | None = ...,
        heat_recovery_outlet_node_name: str | None = ...,
        chiller_flow_mode: Literal["ConstantFlow", "LeavingSetpointModulated", "NotModulated"] | None = "NotModulated",
        fuel_type: Literal[
            "Diesel", "FuelOilNo1", "FuelOilNo2", "Gasoline", "NaturalGas", "OtherFuel1", "OtherFuel2", "Propane"
        ]
        | None = "NaturalGas",
        heat_recovery_maximum_temperature: float | None = 80,
        sizing_factor: float | None = 1,
        basin_heater_capacity: float | None = 0,
        basin_heater_setpoint_temperature: float | None = 2,
        basin_heater_operating_schedule_name: str | None = ...,
        condenser_heat_recovery_relative_capacity_fraction: float | None = ...,
        turbine_engine_efficiency: float | None = 0.35,
    ) -> None:
        """Create a new ``Chiller:CombustionTurbine`` and add it to the document.

        This chiller model is the empirical model from the Building Loads and System Thermodynamics (BLAST) program. Chiller performance curves are generated by fitting catalog data to third order polynomial equations. Three sets of coefficients are required.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-plant-equipment/#chillercombustionturbine
        """

class ThermalStorageIceSimple:
    def __call__(
        self,
        name: str,
        /,
        *,
        ice_storage_type: Literal["IceOnCoilExternal", "IceOnCoilInternal"],
        capacity: float | Literal["Autosize"],
        inlet_node_name: str,
        outlet_node_name: str,
        thermal_storage_sizing_object_name: str | None = ...,
    ) -> None:
        """Create a new ``ThermalStorage:Ice:Simple`` and add it to the document.

        This ice storage model is a simplified model It requires a setpoint placed on the Chilled Water Side Outlet Node It should be placed in the chilled water supply side outlet branch followed by a pipe. Use the PlantEquipmentOperation:ComponentSetpoint plant operation scheme.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-water-heaters/#thermalstorageicesimple
        """

class AnyCurveDoubleExponentialDecay:
    def __call__(
        self,
        name: str,
        /,
        *,
        narrow_with_as_version_first: Never,
        coefficient1_c1: float,
        coefficient2_c2: float,
        coefficient3_c3: float,
        minimum_value_of_x: float,
        maximum_value_of_x: float,
        minimum_curve_output: float | None = ...,
        maximum_curve_output: float | None = ...,
        input_unit_type_for_x: Literal["Dimensionless"] | None = "Dimensionless",
        output_unit_type: Literal["Capacity", "Dimensionless", "Power", "Pressure", "Temperature"]
        | None = "Dimensionless",
    ) -> None:
        """Create a new ``Curve:DoubleExponentialDecay`` and add it to the document.

        Double exponential decay curve with one independent variable. Input consists of the curve name, the five coefficients, and the maximum and minimum valid independent variable values. Optional inputs for the curve minimum and maximum may be used to limit the output of the performance curve. curve = C1+C2*exp(C3*x)+C4*exp(C5*x)

        No call suits every release: narrow the document with ``as_version`` first.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-performance-curves/#curvedoubleexponentialdecay
        """

class AnyPythonPluginTrendVariable:
    def __call__(
        self, name: str, /, *, name_of_a_python_plugin_variable: str, number_of_timesteps_to_be_logged: int
    ) -> None:
        """Create a new ``PythonPlugin:TrendVariable`` and add it to the document.

        This object sets up a Python plugin trend variable from an Python plugin variable A trend variable logs values across timesteps

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-python-plugins/#pythonplugintrendvariable
        """
