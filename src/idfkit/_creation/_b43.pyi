"""Creation signatures of generated classes (stub only).

DO NOT EDIT — regenerate with:
    python -m idfkit.codegen.generate_stubs
"""

from __future__ import annotations

from collections.abc import Sequence
from typing import Literal

from .. import _generated_types as _g

class GroundHeatTransferSlabXFACE:
    def __call__(self, /) -> None:
        """Create a new ``GroundHeatTransfer:Slab:XFACE`` and add it to the document.

        This is only needed when using manual gridding (not recommended) XFACE: X Direction cell face coordinates: m

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-detailed-ground-heat-transfer/#groundheattransferslabxface
        """

class AnyAirflowNetworkDistributionComponentCoil:
    def __call__(
        self,
        /,
        *,
        coil_name: str,
        coil_object_type: Literal[
            "Coil:Cooling:DX:MultiSpeed",
            "Coil:Cooling:DX:SingleSpeed",
            "Coil:Cooling:DX:TwoSpeed",
            "Coil:Cooling:DX:TwoStageWithHumidityControlMode",
            "Coil:Cooling:Water",
            "Coil:Cooling:Water:DetailedGeometry",
            "Coil:Heating:DX:MultiSpeed",
            "Coil:Heating:DX:SingleSpeed",
            "Coil:Heating:Desuperheater",
            "Coil:Heating:Electric",
            "Coil:Heating:Fuel",
            "Coil:Heating:Water",
        ],
        air_path_length: float,
        air_path_hydraulic_diameter: float,
    ) -> None:
        """Create a new ``AirflowNetwork:Distribution:Component:Coil`` and add it to the document.

        This object defines the name of a coil used in an air loop.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-airflow-network/#airflownetworkdistributioncomponentcoil
        """

class AnyAirTerminalSingleDuctVAVReheatVariableSpeedFan:
    def __call__(
        self,
        name: str,
        /,
        *,
        maximum_cooling_air_flow_rate: float | Literal["Autosize"],
        maximum_heating_air_flow_rate: float | Literal["Autosize"],
        zone_minimum_air_flow_fraction: float,
        fan_object_type: Literal["Fan:SystemModel", "Fan:VariableVolume"],
        fan_name: str,
        heating_coil_object_type: Literal[
            "Coil:Heating:Electric", "Coil:Heating:Fuel", "Coil:Heating:Steam", "Coil:Heating:Water"
        ],
        heating_coil_name: str,
        availability_schedule_name: str | None = ...,
        air_inlet_node_name: str | None = ...,
        air_outlet_node_name: str | None = ...,
        maximum_hot_water_or_steam_flow_rate: float | Literal["Autosize"] | None = ...,
        minimum_hot_water_or_steam_flow_rate: float | None = 0,
        heating_convergence_tolerance: float | None = 0.001,
    ) -> None:
        """Create a new ``AirTerminal:SingleDuct:VAV:Reheat:VariableSpeedFan`` and add it to the document.

        Central air system terminal unit, single duct, variable volume, with reheat coil (hot water, electric, gas, or steam) and variable-speed fan. These units are usually employed in underfloor air distribution (UFAD) systems where the air is supplied at low static pressure through an underfloor plenum. The fan is used to control the flow of conditioned air that enters the space.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-air-distribution-equipment/#airterminalsingleductvavreheatvariablespeedfan
        """

class AnyCoilCoolingDXSingleSpeed:
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
        condenser_type: Literal["AirCooled", "EvaporativelyCooled"] | None = "AirCooled",
        evaporative_condenser_effectiveness: float | None = 0.9,
        evaporative_condenser_air_flow_rate: float | Literal["Autosize"] | None = ...,
        evaporative_condenser_pump_rated_power_consumption: float | Literal["Autosize"] | None = 0,
        crankcase_heater_capacity: float | None = 0,
        maximum_outdoor_dry_bulb_temperature_for_crankcase_heater_operation: float | None = 10,
        supply_water_storage_tank_name: str | None = ...,
        condensate_collection_water_storage_tank_name: str | None = ...,
        basin_heater_capacity: float | None = 0,
        basin_heater_setpoint_temperature: float | None = 2,
        basin_heater_operating_schedule_name: str | None = ...,
        sensible_heat_ratio_function_of_temperature_curve_name: str | None = ...,
        sensible_heat_ratio_function_of_flow_fraction_curve_name: str | None = ...,
        report_ashrae_standard_127_performance_ratings: Literal["No", "Yes"] | None = "No",
        zone_name_for_condenser_placement: str | None = ...,
    ) -> None:
        """Create a new ``Coil:Cooling:DX:SingleSpeed`` and add it to the document.

        Direct expansion (DX) cooling coil and condensing unit (includes electric compressor and condenser fan), single-speed. Optional inputs for moisture evaporation from wet coil when compressor cycles off with continuous fan operation.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-heating-and-cooling-coils/#coilcoolingdxsinglespeed
        """

class CoilWaterHeatingAirToWaterHeatPumpPumped:
    def __call__(
        self,
        name: str,
        /,
        *,
        rated_heating_capacity: float,
        evaporator_air_inlet_node_name: str,
        evaporator_air_outlet_node_name: str,
        condenser_water_inlet_node_name: str,
        condenser_water_outlet_node_name: str,
        availability_schedule_name: str | None = ...,
        rated_cop: float | None = 3.2,
        rated_sensible_heat_ratio: float | None = 0.85,
        rated_evaporator_inlet_air_dry_bulb_temperature: float | None = 19.7,
        rated_evaporator_inlet_air_wet_bulb_temperature: float | None = 13.5,
        rated_condenser_inlet_water_temperature: float | None = 57.5,
        rated_evaporator_air_flow_rate: float | Literal["Autocalculate"] | None = ...,
        rated_condenser_water_flow_rate: float | Literal["Autocalculate"] | None = ...,
        evaporator_fan_power_included_in_rated_cop: Literal["No", "Yes"] | None = "Yes",
        condenser_pump_power_included_in_rated_cop: Literal["No", "Yes"] | None = "No",
        condenser_pump_heat_included_in_rated_heating_capacity_and_rated_cop: Literal["No", "Yes"] | None = "No",
        condenser_water_pump_power: float | None = 0,
        fraction_of_condenser_pump_heat_to_water: float | None = 0.2,
        crankcase_heater_capacity: float | None = 0,
        crankcase_heater_capacity_function_of_temperature_curve_name: str | None = ...,
        maximum_ambient_temperature_for_crankcase_heater_operation: float | None = 10,
        evaporator_air_temperature_type_for_curve_objects: Literal["DryBulbTemperature", "WetBulbTemperature"]
        | None = "WetBulbTemperature",
        heating_capacity_function_of_temperature_curve_name: str | None = ...,
        heating_capacity_function_of_air_flow_fraction_curve_name: str | None = ...,
        heating_capacity_function_of_water_flow_fraction_curve_name: str | None = ...,
        heating_cop_function_of_temperature_curve_name: str | None = ...,
        heating_cop_function_of_air_flow_fraction_curve_name: str | None = ...,
        heating_cop_function_of_water_flow_fraction_curve_name: str | None = ...,
        part_load_fraction_correlation_curve_name: str | None = ...,
    ) -> None:
        """Create a new ``Coil:WaterHeating:AirToWaterHeatPump:Pumped`` and add it to the document.

        Heat pump water heater (HPWH) heating coil, air-to-water direct-expansion (DX) system which includes a water heating coil, evaporator air coil, evaporator fan, electric compressor, and water pump. Part of a WaterHeater:HeatPump:PumpedCondenser system.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-heating-and-cooling-coils/#coilwaterheatingairtowaterheatpumppumped
        """

class HeatExchangerFluidToFluid:
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
            "FreeCooling", "HeatRecoveryForCooling", "HeatRecoveryForHeating", "HeatRejection", "LoopToLoop"
        ]
        | None = "LoopToLoop",
        component_override_loop_supply_side_inlet_node_name: str | None = ...,
        component_override_loop_demand_side_inlet_node_name: str | None = ...,
        component_override_cooling_control_temperature_mode: Literal["DryBulbTemperature", "Loop", "WetBulbTemperature"]
        | None = "Loop",
        sizing_factor: float | None = 1,
        operation_minimum_temperature_limit: float | None = ...,
        operation_maximum_temperature_limit: float | None = ...,
    ) -> None:
        """Create a new ``HeatExchanger:FluidToFluid`` and add it to the document.

        A fluid/fluid heat exchanger designed to couple the supply side of one loop to the demand side of another loop Loops can be either plant or condenser loops but no air side connections are allowed

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-condenser-equipment/#heatexchangerfluidtofluid
        """

class AnyWaterHeaterMixed:
    def __call__(
        self,
        name: str,
        /,
        *,
        setpoint_temperature_schedule_name: str,
        heater_fuel_type: Literal[
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
        ],
        heater_thermal_efficiency: float,
        ambient_temperature_indicator: Literal["Outdoors", "Schedule", "Zone"],
        tank_volume: float | Literal["Autosize"] | None = 0,
        deadband_temperature_difference: float | None = 0,
        maximum_temperature_limit: float | None = ...,
        heater_control_type: Literal["Cycle", "Modulate"] | None = "Cycle",
        heater_maximum_capacity: float | Literal["Autosize"] | None = ...,
        heater_minimum_capacity: float | None = ...,
        heater_ignition_minimum_flow_rate: float | None = 0,
        heater_ignition_delay: float | None = 0,
        part_load_factor_curve_name: str | None = ...,
        off_cycle_parasitic_fuel_consumption_rate: float | None = 0,
        off_cycle_parasitic_fuel_type: Literal[
            "Coal", "Diesel", "Electricity", "Gasoline", "NaturalGas", "OtherFuel1", "OtherFuel2"
        ]
        | None = ...,
        off_cycle_parasitic_heat_fraction_to_tank: float | None = 0,
        on_cycle_parasitic_fuel_consumption_rate: float | None = 0,
        on_cycle_parasitic_fuel_type: Literal[
            "Coal", "Diesel", "Electricity", "Gasoline", "NaturalGas", "OtherFuel1", "OtherFuel2"
        ]
        | None = ...,
        on_cycle_parasitic_heat_fraction_to_tank: float | None = 0,
        ambient_temperature_schedule_name: str | None = ...,
        ambient_temperature_zone_name: str | None = ...,
        ambient_temperature_outdoor_air_node_name: str | None = ...,
        off_cycle_loss_coefficient_to_ambient_temperature: float | None = ...,
        off_cycle_loss_fraction_to_zone: float | None = 1,
        on_cycle_loss_coefficient_to_ambient_temperature: float | None = ...,
        on_cycle_loss_fraction_to_zone: float | None = 1,
        peak_use_flow_rate: float | None = ...,
        use_flow_rate_fraction_schedule_name: str | None = ...,
        cold_water_supply_temperature_schedule_name: str | None = ...,
        use_side_inlet_node_name: str | None = ...,
        use_side_outlet_node_name: str | None = ...,
        use_side_effectiveness: float | None = 1,
        source_side_inlet_node_name: str | None = ...,
        source_side_outlet_node_name: str | None = ...,
        source_side_effectiveness: float | None = 1,
        use_side_design_flow_rate: float | Literal["Autosize"] | None = "Autosize",
        source_side_design_flow_rate: float | Literal["Autosize"] | None = "Autosize",
        indirect_water_heating_recovery_time: float | None = 1.5,
        source_side_flow_control_mode: Literal[
            "IndirectHeatAlternateSetpoint", "IndirectHeatPrimarySetpoint", "StorageTank"
        ]
        | None = "IndirectHeatPrimarySetpoint",
        indirect_alternate_setpoint_temperature_schedule_name: str | None = ...,
        end_use_subcategory: str | None = "General",
    ) -> None:
        """Create a new ``WaterHeater:Mixed`` and add it to the document.

        Water heater with well-mixed, single-node water tank. May be used to model a tankless water heater (small tank volume), a hot water storage tank (zero heater capacity), or a heat pump water heater (see WaterHeater:HeatPump:PumpedCondenser.)

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-water-heaters/#waterheatermixed
        """

class GeneratorFuelCellExhaustGasToWaterHeatExchanger:
    def __call__(
        self,
        name: str,
        /,
        *,
        heat_recovery_water_inlet_node_name: str | None = ...,
        heat_recovery_water_outlet_node_name: str | None = ...,
        heat_recovery_water_maximum_flow_rate: float | None = ...,
        exhaust_outlet_air_node_name: str | None = ...,
        heat_exchanger_calculation_method: Literal[
            "Condensing", "EmpiricalUAeff", "FixedEffectiveness", "FundementalUAeff"
        ]
        | None = ...,
        method_1_heat_exchanger_effectiveness: float | None = ...,
        method_2_parameter_hxs0: float | None = ...,
        method_2_parameter_hxs1: float | None = ...,
        method_2_parameter_hxs2: float | None = ...,
        method_2_parameter_hxs3: float | None = ...,
        method_2_parameter_hxs4: float | None = ...,
        method_3_h0gas_coefficient: float | None = ...,
        method_3_ndotgasref_coefficient: float | None = ...,
        method_3_n_coefficient: float | None = ...,
        method_3_gas_area: float | None = ...,
        method_3_h0_water_coefficient: float | None = ...,
        method_3_n_dot_water_ref_coefficient: float | None = ...,
        method_3_m_coefficient: float | None = ...,
        method_3_water_area: float | None = ...,
        method_3_f_adjustment_factor: float | None = ...,
        method_4_hxl1_coefficient: float | None = ...,
        method_4_hxl2_coefficient: float | None = ...,
        method_4_condensation_threshold: float | None = ...,
    ) -> None:
        """Create a new ``Generator:FuelCell:ExhaustGasToWaterHeatExchanger`` and add it to the document.

        Describes the exhaust gas heat exchanger subsystem of a fuel cell power generator used to recovery thermal energy

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-electric-load-center-generator/#generatorfuelcellexhaustgastowaterheatexchanger
        """

class WaterUseConnections:
    def __call__(
        self,
        name: str,
        /,
        *,
        inlet_node_name: str | None = ...,
        outlet_node_name: str | None = ...,
        supply_water_storage_tank_name: str | None = ...,
        reclamation_water_storage_tank_name: str | None = ...,
        hot_water_supply_temperature_schedule_name: str | None = ...,
        cold_water_supply_temperature_schedule_name: str | None = ...,
        drain_water_heat_exchanger_type: Literal["CounterFlow", "CrossFlow", "Ideal", "None"] | None = "None",
        drain_water_heat_exchanger_destination: Literal["Equipment", "Plant", "PlantAndEquipment"] | None = "Plant",
        drain_water_heat_exchanger_u_factor_times_area: float | None = ...,
        connections: Sequence[_g.WaterUseConnectionsConnectionsItem | _g.WaterUseConnectionsConnectionsGroup] = ...,
    ) -> None:
        """Create a new ``WaterUse:Connections`` and add it to the document.

        A subsystem that groups together multiple WaterUse:Equipment components. As its name suggests, the object provides connections that are shared by these components, including: 1. Inlet node and outlet node connections to a plant loop 2. Connections to WaterUse:Storage objects to store and draw reclaimed water 3. Internal connections to simulate drainwater heat recovery.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-water-systems/#wateruseconnections
        """

class CurveRectangularHyperbola1:
    def __call__(
        self,
        name: str,
        /,
        *,
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
        """Create a new ``Curve:RectangularHyperbola1`` and add it to the document.

        Rectangular hyperbola type 1 curve with one independent variable. Input consists of the curve name, the three coefficients, and the maximum and minimum valid independent variable values. Optional inputs for the curve minimum and maximum may be used to limit the output of the performance curve. curve = ((C1*x)/(C2+x))+C3

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-performance-curves/#curverectangularhyperbola1
        """

class FluidPropertiesSuperheated:
    def __call__(
        self,
        /,
        *,
        fluid_name: str | None = ...,
        fluid_property_type: Literal["Density", "Enthalpy"] | None = ...,
        temperature_values_name: str | None = ...,
        pressure: float | None = ...,
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
        """Create a new ``FluidProperties:Superheated`` and add it to the document.

        fluid properties for the superheated region

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-fluid-properties/#fluidpropertiessuperheated
        """
