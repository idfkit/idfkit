"""Creation signatures of generated classes (stub only).

DO NOT EDIT — regenerate with:
    python -m idfkit.codegen.generate_stubs
"""

from __future__ import annotations

from typing import Literal

from .. import _generated_types as _g
from .. import versioned as _vd

class SimulationControl_v8_9_to_v22_1:
    def __call__(
        self,
        /,
        *,
        do_zone_sizing_calculation: Literal["", "No", "Yes"] | None = "No",
        do_system_sizing_calculation: Literal["", "No", "Yes"] | None = "No",
        do_plant_sizing_calculation: Literal["", "No", "Yes"] | None = "No",
        run_simulation_for_sizing_periods: Literal["", "No", "Yes"] | None = "Yes",
        run_simulation_for_weather_file_run_periods: Literal["", "No", "Yes"] | None = "Yes",
        do_hvac_sizing_simulation_for_sizing_periods: Literal["", "No", "Yes"] | None = "No",
        maximum_number_of_hvac_sizing_simulation_passes: float | None = 1,
    ) -> None:
        """Create a new ``SimulationControl`` and add it to the document.

        Note that the following 3 fields are related to the Sizing:Zone, Sizing:System, and Sizing:Plant objects. Having these fields set to Yes but no corresponding Sizing object will not cause the sizing to be done. However, having any of these fields set to No, the corresponding Sizing object is ignored. Note also, if you want to do system sizing, you must also do zone sizing in the same run or an error will result.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v22.1/io-reference/overview/group-simulation-parameters/#simulationcontrol
        """

class AirflowNetworkDistributionNode_v8_9_to_v25_1:
    def __call__(
        self,
        name: str,
        /,
        *,
        component_name_or_node_name: str | None = ...,
        component_object_type_or_node_type: Literal[
            "",
            "AirLoopHVAC:OutdoorAirSystem",
            "AirLoopHVAC:ZoneMixer",
            "AirLoopHVAC:ZoneSplitter",
            "OAMixerOutdoorAirStreamNode",
            "Other",
            "OutdoorAir:Node",
            "OutdoorAir:NodeList",
        ]
        | None = "Other",
        node_height: float | None = 0,
    ) -> None:
        """Create a new ``AirflowNetwork:Distribution:Node`` and add it to the document.

        This object represents an air distribution node in the AirflowNetwork model.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v25.1/io-reference/overview/group-airflow-network/#airflownetworkdistributionnode
        """

class CoilSystemCoolingDXHeatExchangerAssisted_v8_9_to_v22_1:
    def __call__(
        self,
        name: str,
        /,
        *,
        heat_exchanger_object_type: Literal[
            "HeatExchanger:AirToAir:FlatPlate",
            "HeatExchanger:AirToAir:SensibleAndLatent",
            "HeatExchanger:Desiccant:BalancedFlow",
        ],
        heat_exchanger_name: str,
        cooling_coil_object_type: Literal["Coil:Cooling:DX:SingleSpeed", "Coil:Cooling:DX:VariableSpeed"],
        cooling_coil_name: str,
    ) -> None:
        """Create a new ``CoilSystem:Cooling:DX:HeatExchangerAssisted`` and add it to the document.

        Virtual component consisting of a direct expansion (DX) cooling coil and an air-to-air heat exchanger. The air-to-air heat exchanger precools the air entering the cooling coil and reuses this energy to reheat the supply air leaving the cooling coil. This heat exchange process improves the latent removal performance of the cooling coil (lower sensible heat ratio).

        EnergyPlus I/O Reference: https://docs.idfkit.com/v22.1/io-reference/overview/group-heating-and-cooling-coils/#coilsystemcoolingdxheatexchangerassisted
        """

class MaterialPropertyPhaseChange_v8_9_to_v24_1:
    def __call__(
        self,
        name: str,
        /,
        *,
        temperature_1: float,
        enthalpy_1: float,
        temperature_2: float,
        enthalpy_2: float,
        temperature_3: float,
        enthalpy_3: float,
        temperature_coefficient_for_thermal_conductivity: float | None = 0,
        temperature_4: float | None = ...,
        enthalpy_4: float | None = ...,
        temperature_5: float | None = ...,
        enthalpy_5: float | None = ...,
        temperature_6: float | None = ...,
        enthalpy_6: float | None = ...,
        temperature_7: float | None = ...,
        enthalpy_7: float | None = ...,
        temperature_8: float | None = ...,
        enthalpy_8: float | None = ...,
        temperature_9: float | None = ...,
        enthalpy_9: float | None = ...,
        temperature_10: float | None = ...,
        enthalpy_10: float | None = ...,
        temperature_11: float | None = ...,
        enthalpy_11: float | None = ...,
        temperature_12: float | None = ...,
        enthalpy_12: float | None = ...,
        temperature_13: float | None = ...,
        enthalpy_13: float | None = ...,
        temperature_14: float | None = ...,
        enthalpy_14: float | None = ...,
        temperature_15: float | None = ...,
        enthalpy_15: float | None = ...,
        temperature_16: float | None = ...,
        enthalpy_16: float | None = ...,
    ) -> None:
        """Create a new ``MaterialProperty:PhaseChange`` and add it to the document.

        Additional properties for temperature dependent thermal conductivity and enthalpy for Phase Change Materials (PCM) HeatBalanceAlgorithm = CondFD(ConductionFiniteDifference) solution algorithm only. Constructions with this should use the detailed CondFD process. Has no effect with other HeatBalanceAlgorithm solution algorithms

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v24.1/io-reference/overview/group-surface-construction-elements/#materialpropertyphasechange
        """

class ScheduleYear_v9_0_to_v22_1:
    def __call__(
        self,
        name: str,
        /,
        *,
        schedule_type_limits_name: str | None = ...,
        schedule_weeks: list[_vd.ScheduleYearScheduleWeeksItem_v9_0_to_v22_1] = ...,
    ) -> None:
        """Create a new ``Schedule:Year`` and add it to the document.

        A Schedule:Year contains from 1 to 52 week schedules

        EnergyPlus I/O Reference: https://docs.idfkit.com/v22.1/io-reference/overview/group-schedules/#scheduleyear
        """

class ZoneCoolTowerShower_v8_9_to_v24_1:
    def __call__(
        self,
        name: str,
        /,
        *,
        zone_name: str,
        pump_flow_rate_schedule_name: str,
        maximum_water_flow_rate: float,
        effective_tower_height: float,
        airflow_outlet_area: float,
        maximum_air_flow_rate: float,
        minimum_indoor_temperature: float,
        rated_power_consumption: float,
        availability_schedule_name: str | None = ...,
        water_supply_storage_tank_name: str | None = ...,
        flow_control_type: Literal["", "WaterFlowSchedule", "WindDrivenFlow"] | None = "WindDrivenFlow",
        fraction_of_water_loss: float | None = ...,
        fraction_of_flow_schedule: float | None = ...,
    ) -> None:
        """Create a new ``ZoneCoolTower:Shower`` and add it to the document.

        A cooltower (sometimes referred to as a wind tower or a shower cooling tower) models passive downdraught evaporative cooling (PDEC) that is designed to capture the wind at the top of a tower and cool the outdoor air using water evaporation before delivering it to a space.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v24.1/io-reference/overview/group-airflow/#zonecooltowershower
        """

class CoilHeatingWaterToAirHeatPumpEquationFit_v9_5_to_v22_1:
    def __call__(
        self,
        name: str,
        /,
        *,
        water_inlet_node_name: str,
        water_outlet_node_name: str,
        air_inlet_node_name: str,
        air_outlet_node_name: str,
        rated_air_flow_rate: float | Literal["Autosize"],
        rated_water_flow_rate: float | Literal["Autosize"],
        gross_rated_heating_capacity: float | Literal["Autosize"],
        gross_rated_heating_cop: float,
        heating_capacity_curve_name: str,
        heating_power_consumption_curve_name: str,
    ) -> None:
        """Create a new ``Coil:Heating:WaterToAirHeatPump:EquationFit`` and add it to the document.

        Direct expansion (DX) heating coil for water-to-air heat pump (includes electric compressor), single-speed, equation-fit model. Equation-fit model uses normalized curves to describe the heat pump performance.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v22.1/io-reference/overview/group-heating-and-cooling-coils/#coilheatingwatertoairheatpumpequationfit
        """

class CoilHeatingWaterToAirHeatPumpEquationFit_v22_2_to_v23_1:
    def __call__(
        self,
        name: str,
        /,
        *,
        water_inlet_node_name: str,
        water_outlet_node_name: str,
        air_inlet_node_name: str,
        air_outlet_node_name: str,
        rated_air_flow_rate: float | Literal["Autosize"],
        rated_water_flow_rate: float | Literal["Autosize"],
        gross_rated_heating_capacity: float | Literal["Autosize"],
        gross_rated_heating_cop: float,
        heating_capacity_curve_name: str,
        heating_power_consumption_curve_name: str,
        rated_entering_water_temperature: float | None = 20,
        rated_entering_air_dry_bulb_temperature: float | None = 20,
        ratio_of_rated_heating_capacity_to_rated_cooling_capacity: float | None = 1,
    ) -> None:
        """Create a new ``Coil:Heating:WaterToAirHeatPump:EquationFit`` and add it to the document.

        Direct expansion (DX) heating coil for water-to-air heat pump (includes electric compressor), single-speed, equation-fit model. Equation-fit model uses normalized curves to describe the heat pump performance.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v23.1/io-reference/overview/group-heating-and-cooling-coils/#coilheatingwatertoairheatpumpequationfit
        """

class CoilHeatingDXSingleSpeed_v8_9_to_v22_1:
    def __call__(
        self,
        name: str,
        /,
        *,
        gross_rated_heating_capacity: float | Literal["Autosize"],
        gross_rated_heating_cop: float,
        rated_air_flow_rate: float | Literal["Autosize"],
        air_inlet_node_name: str,
        air_outlet_node_name: str,
        heating_capacity_function_of_temperature_curve_name: str,
        heating_capacity_function_of_flow_fraction_curve_name: str,
        energy_input_ratio_function_of_temperature_curve_name: str,
        energy_input_ratio_function_of_flow_fraction_curve_name: str,
        part_load_fraction_correlation_curve_name: str,
        availability_schedule_name: str | None = ...,
        rated_supply_fan_power_per_volume_flow_rate: float | None = 773.3,
        defrost_energy_input_ratio_function_of_temperature_curve_name: str | None = ...,
        minimum_outdoor_dry_bulb_temperature_for_compressor_operation: float | None = -8,
        outdoor_dry_bulb_temperature_to_turn_on_compressor: float | None = ...,
        maximum_outdoor_dry_bulb_temperature_for_defrost_operation: float | None = 5,
        crankcase_heater_capacity: float | None = 0,
        maximum_outdoor_dry_bulb_temperature_for_crankcase_heater_operation: float | None = 10,
        defrost_strategy: Literal["", "Resistive", "ReverseCycle"] | None = "ReverseCycle",
        defrost_control: Literal["", "OnDemand", "Timed"] | None = "Timed",
        defrost_time_period_fraction: float | None = 0.058333,
        resistive_defrost_heater_capacity: float | Literal["", "Autosize"] | None = 0,
        region_number_for_calculating_hspf: float | None = 4,
        evaporator_air_inlet_node_name: str | None = ...,
        zone_name_for_evaporator_placement: str | None = ...,
        secondary_coil_air_flow_rate: float | Literal["Autosize"] | None = ...,
        secondary_coil_fan_flow_scaling_factor: float | None = 1.25,
        nominal_sensible_heat_ratio_of_secondary_coil: float | None = ...,
        sensible_heat_ratio_modifier_function_of_temperature_curve_name: str | None = ...,
        sensible_heat_ratio_modifier_function_of_flow_fraction_curve_name: str | None = ...,
    ) -> None:
        """Create a new ``Coil:Heating:DX:SingleSpeed`` and add it to the document.

        Direct expansion (DX) heating coil (air-to-air heat pump) and compressor unit (includes electric compressor and outdoor fan), single-speed, with defrost controls.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v22.1/io-reference/overview/group-heating-and-cooling-coils/#coilheatingdxsinglespeed
        """

class CoilHeatingDXSingleSpeed_v22_2_to_v23_1:
    def __call__(
        self,
        name: str,
        /,
        *,
        gross_rated_heating_capacity: float | Literal["Autosize"],
        gross_rated_heating_cop: float,
        rated_air_flow_rate: float | Literal["Autosize"],
        air_inlet_node_name: str,
        air_outlet_node_name: str,
        heating_capacity_function_of_temperature_curve_name: str,
        heating_capacity_function_of_flow_fraction_curve_name: str,
        energy_input_ratio_function_of_temperature_curve_name: str,
        energy_input_ratio_function_of_flow_fraction_curve_name: str,
        part_load_fraction_correlation_curve_name: str,
        availability_schedule_name: str | None = ...,
        defrost_energy_input_ratio_function_of_temperature_curve_name: str | None = ...,
        minimum_outdoor_dry_bulb_temperature_for_compressor_operation: float | None = -8,
        outdoor_dry_bulb_temperature_to_turn_on_compressor: float | None = ...,
        maximum_outdoor_dry_bulb_temperature_for_defrost_operation: float | None = 5,
        crankcase_heater_capacity: float | None = 0,
        maximum_outdoor_dry_bulb_temperature_for_crankcase_heater_operation: float | None = 10,
        defrost_strategy: Literal["", "Resistive", "ReverseCycle"] | None = "ReverseCycle",
        defrost_control: Literal["", "OnDemand", "Timed"] | None = "Timed",
        defrost_time_period_fraction: float | None = 0.058333,
        resistive_defrost_heater_capacity: float | Literal["", "Autosize"] | None = 0,
        region_number_for_calculating_hspf: int | None = 4,
        evaporator_air_inlet_node_name: str | None = ...,
        zone_name_for_evaporator_placement: str | None = ...,
        secondary_coil_air_flow_rate: float | Literal["Autosize"] | None = ...,
        secondary_coil_fan_flow_scaling_factor: float | None = 1.25,
        nominal_sensible_heat_ratio_of_secondary_coil: float | None = ...,
        sensible_heat_ratio_modifier_function_of_temperature_curve_name: str | None = ...,
        sensible_heat_ratio_modifier_function_of_flow_fraction_curve_name: str | None = ...,
    ) -> None:
        """Create a new ``Coil:Heating:DX:SingleSpeed`` and add it to the document.

        Direct expansion (DX) heating coil (air-to-air heat pump) and compressor unit (includes electric compressor and outdoor fan), single-speed, with defrost controls.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v23.1/io-reference/overview/group-heating-and-cooling-coils/#coilheatingdxsinglespeed
        """

class FuelFactors_v9_3_to_v22_1:
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
        units_of_measure: str | None = ...,
        energy_per_unit_factor: float | None = ...,
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

        EnergyPlus I/O Reference: https://docs.idfkit.com/v22.1/io-reference/input-for-output/#fuelfactors
        """

class MeterCustomDecrement_v9_4_to_v23_1:
    def __call__(
        self,
        name: str,
        /,
        *,
        source_meter_name: str,
        resource_type: Literal[
            "Coal",
            "Diesel",
            "DistrictCooling",
            "DistrictHeating",
            "Electricity",
            "FuelOilNo1",
            "FuelOilNo2",
            "Gasoline",
            "Generic",
            "NaturalGas",
            "OtherFuel1",
            "OtherFuel2",
            "Propane",
            "Steam",
            "Water",
        ]
        | None = ...,
        variable_details: list[_g.MeterCustomDecrementVariableDetailsItem] = ...,
    ) -> None:
        """Create a new ``Meter:CustomDecrement`` and add it to the document.

        Used to allow users to combine specific variables and/or meters into 'custom' meter configurations. To access these meters by name, one must first run a simulation to generate the RDD/MDD files and names.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v23.1/io-reference/overview/group-simulation-parameters/#metercustomdecrement
        """

class CoilHeatingDesuperheater_v22_2_to_v23_1:
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
        parasitic_electric_load: float | None = ...,
    ) -> None:
        """Create a new ``Coil:Heating:Desuperheater`` and add it to the document.

        Desuperheater air heating coil. The heating energy provided by this coil is reclaimed from the superheated refrigerant gas leaving a compressor and does not impact the performance of the compressor. If the coil is located directly in an air loop branch or outdoor air equipment list, then it is controlled on leaving air temperature and the Temperature Setpoint Node Name must be specified. If the coil is contained within another component such as a unitary system, then the coil is controlled by the parent component and the setpoint node name is not entered.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v23.1/io-reference/overview/group-heating-and-cooling-coils/#coilheatingdesuperheater
        """

class MaterialPropertyHeatAndMoistureTransferSuction_v8_9_to_v22_1:
    def __call__(
        self,
        /,
        *,
        material_name: str,
        number_of_suction_points: float,
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
        """Create a new ``MaterialProperty:HeatAndMoistureTransfer:Suction`` and add it to the document.

        HeatBalanceAlgorithm = CombinedHeatAndMoistureFiniteElement solution algorithm only. Relationship between liquid suction transport coefficient and moisture content Has no effect with other HeatBalanceAlgorithm solution algorithms

        EnergyPlus I/O Reference: https://docs.idfkit.com/v22.1/io-reference/overview/group-surface-construction-elements/#materialpropertyheatandmoisturetransfersuction
        """

class AirTerminalSingleDuctSeriesPIUReheat_v24_2_to_v25_2:
    def __call__(
        self,
        name: str,
        /,
        *,
        maximum_air_flow_rate: float | Literal["Autosize"],
        maximum_primary_air_flow_rate: float | Literal["Autosize"],
        minimum_primary_air_flow_fraction: float | Literal["Autosize"],
        reheat_coil_object_type: Literal[
            "Coil:Heating:Electric", "Coil:Heating:Fuel", "Coil:Heating:Steam", "Coil:Heating:Water"
        ],
        reheat_coil_name: str,
        availability_schedule_name: str | None = ...,
        supply_air_inlet_node_name: str | None = ...,
        secondary_air_inlet_node_name: str | None = ...,
        outlet_node_name: str | None = ...,
        reheat_coil_air_inlet_node_name: str | None = ...,
        zone_mixer_name: str | None = ...,
        fan_name: str | None = ...,
        maximum_hot_water_or_steam_flow_rate: float | Literal["Autosize"] | None = ...,
        minimum_hot_water_or_steam_flow_rate: float | None = 0,
        convergence_tolerance: float | None = 0.001,
        fan_control_type: Literal["", "ConstantSpeed", "VariableSpeed"] | None = "ConstantSpeed",
        minimum_fan_turn_down_ratio: float | None = 0.3,
        heating_control_type: Literal["Modulated", "Staged"] | None = ...,
        design_heating_discharge_air_temperature: float | None = 32.1,
        high_limit_heating_discharge_air_temperature: float | None = 37.7,
    ) -> None:
        """Create a new ``AirTerminal:SingleDuct:SeriesPIU:Reheat`` and add it to the document.

        Central air system terminal unit, single duct, variable volume, series powered induction unit (PIU), with reheat coil (hot water, electric, gas, or steam).

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v25.2/io-reference/overview/group-zone-hvac-air-loop-terminal-units/#airterminalsingleductseriespiureheat
        """

class AirLoopHVACUnitarySystem_v8_9_to_v9_2:
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
        maximum_supply_air_temperature: float | Literal["", "Autosize"] | None = 80,
        maximum_outdoor_dry_bulb_temperature_for_supplemental_heater_operation: float | None = 21,
        outdoor_dry_bulb_temperature_sensor_node_name: str | None = ...,
        maximum_cycling_rate: float | None = 2.5,
        heat_pump_time_constant: float | None = 60,
        fraction_of_on_cycle_power_use: float | None = 0.01,
        heat_pump_fan_delay_time: float | None = 60,
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

        EnergyPlus I/O Reference: https://docs.idfkit.com/v9.2/io-reference/overview/group-unitary-equipment/#airloophvacunitarysystem
        """

class AirLoopHVACUnitaryHeatPumpAirToAirMultiSpeed_v22_2_to_v25_1:
    def __call__(
        self,
        name: str,
        /,
        *,
        air_inlet_node_name: str,
        air_outlet_node_name: str,
        controlling_zone_or_thermostat_location: str,
        supply_air_fan_object_type: Literal["Fan:ConstantVolume", "Fan:OnOff"],
        supply_air_fan_name: str,
        supply_air_fan_placement: Literal["BlowThrough", "DrawThrough"],
        heating_coil_object_type: Literal[
            "Coil:Heating:DX:MultiSpeed",
            "Coil:Heating:Electric:MultiStage",
            "Coil:Heating:Gas:MultiStage",
            "Coil:Heating:Steam",
            "Coil:Heating:Water",
        ],
        heating_coil_name: str,
        cooling_coil_object_type: Literal["Coil:Cooling:DX:MultiSpeed"],
        cooling_coil_name: str,
        number_of_speeds_for_heating: int,
        number_of_speeds_for_cooling: int,
        heating_speed_1_supply_air_flow_rate: float | Literal["Autosize"],
        cooling_speed_1_supply_air_flow_rate: float | Literal["Autosize"],
        cooling_speed_2_supply_air_flow_rate: float | Literal["Autosize"],
        availability_schedule_name: str | None = ...,
        supply_air_fan_operating_mode_schedule_name: str | None = ...,
        minimum_outdoor_dry_bulb_temperature_for_compressor_operation: float | None = -8,
        supplemental_heating_coil_object_type: Literal[
            "Coil:Heating:Electric", "Coil:Heating:Fuel", "Coil:Heating:Steam", "Coil:Heating:Water"
        ]
        | None = ...,
        supplemental_heating_coil_name: str | None = ...,
        maximum_supply_air_temperature_from_supplemental_heater: float | Literal["Autosize"] | None = ...,
        maximum_outdoor_dry_bulb_temperature_for_supplemental_heater_operation: float | None = 21,
        auxiliary_on_cycle_electric_power: float | None = 0,
        auxiliary_off_cycle_electric_power: float | None = 0,
        design_heat_recovery_water_flow_rate: float | None = 0,
        maximum_temperature_for_heat_recovery: float | None = 80,
        heat_recovery_water_inlet_node_name: str | None = ...,
        heat_recovery_water_outlet_node_name: str | None = ...,
        no_load_supply_air_flow_rate: float | Literal["Autosize"] | None = ...,
        heating_speed_2_supply_air_flow_rate: float | Literal["Autosize"] | None = ...,
        heating_speed_3_supply_air_flow_rate: float | Literal["Autosize"] | None = ...,
        heating_speed_4_supply_air_flow_rate: float | Literal["Autosize"] | None = ...,
        cooling_speed_3_supply_air_flow_rate: float | Literal["Autosize"] | None = ...,
        cooling_speed_4_supply_air_flow_rate: float | Literal["Autosize"] | None = ...,
    ) -> None:
        """Create a new ``AirLoopHVAC:UnitaryHeatPump:AirToAir:MultiSpeed`` and add it to the document.

        Unitary system, heating and cooling, multi-speed with constant volume supply fan (continuous or cycling), direct expansion (DX) cooling coil, heating coil (DX air-to-air heat pump, gas, electric, hot water, or steam), and supplemental heating coil (gas, electric, hot water, or steam).

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v25.1/io-reference/overview/group-unitary-equipment/#airloophvacunitaryheatpumpairtoairmultispeed
        """

class MeterCustom_v9_4_to_v23_1:
    def __call__(
        self,
        name: str,
        /,
        *,
        resource_type: Literal[
            "Coal",
            "Diesel",
            "DistrictCooling",
            "DistrictHeating",
            "Electricity",
            "FuelOilNo1",
            "FuelOilNo2",
            "Gasoline",
            "Generic",
            "NaturalGas",
            "OtherFuel1",
            "OtherFuel2",
            "Propane",
            "Steam",
            "Water",
        ]
        | None = ...,
        variable_details: list[_g.MeterCustomVariableDetailsItem] = ...,
    ) -> None:
        """Create a new ``Meter:Custom`` and add it to the document.

        Used to allow users to combine specific variables and/or meters into 'custom' meter configurations. To access these meters by name, one must first run a simulation to generate the RDD/MDD files and names. A Meter:Custom cannot reference another Meter:Custom.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v23.1/io-reference/overview/group-simulation-parameters/#metercustom
        """

class ExternalInterfaceFunctionalMockupUnitExportToActuator_v8_9_to_v25_1:
    def __call__(
        self,
        name: str,
        /,
        *,
        actuated_component_unique_name: str,
        actuated_component_type: str,
        actuated_component_control_type: str,
        fmu_variable_name: str,
        initial_value: float,
    ) -> None:
        """Create a new ``ExternalInterface:FunctionalMockupUnitExport:To:Actuator`` and add it to the document.

        Hardware portion of EMS used to set up actuators in the model that are dynamically updated from the FMU.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v25.1/io-reference/overview/group-externalinterface/#externalinterfacefunctionalmockupunitexporttoactuator
        """
