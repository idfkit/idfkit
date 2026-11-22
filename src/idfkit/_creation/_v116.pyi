"""Creation signatures of generated classes (stub only).

DO NOT EDIT — regenerate with:
    python -m idfkit.codegen.generate_stubs
"""

from __future__ import annotations

from collections.abc import Sequence
from typing import Literal

from .. import versioned as _vd

class PlantEquipmentOperationThermalEnergyStorage_v8_9_to_v22_1:
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
        validate: bool = True,
    ) -> None:
        """Create a new ``PlantEquipmentOperation:ThermalEnergyStorage`` and add it to the document.

        Plant equipment operation scheme for simpler input to control thermal (ice) energy storage systems. It replaces a host of setpoint managers with simple, single input values. For more complex controls, use the ComponentSetpoint scheme.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v22.1/io-reference/overview/group-plant-condenser-control/#plantequipmentoperationthermalenergystorage
        """

class CoilWaterHeatingAirToWaterHeatPumpVariableSpeed_v8_9_to_v22_1:
    def __call__(
        self,
        name: str,
        /,
        *,
        rated_water_heating_capacity: float,
        evaporator_air_inlet_node_name: str,
        evaporator_air_outlet_node_name: str,
        condenser_water_inlet_node_name: str,
        condenser_water_outlet_node_name: str,
        rated_water_heating_capacity_at_speed_1: float,
        speed_1_reference_unit_rated_air_flow_rate: float,
        speed_1_reference_unit_rated_water_flow_rate: float,
        speed_1_reference_unit_water_pump_input_power_at_rated_conditions: float,
        speed_1_total_wh_capacity_function_of_temperature_curve_name: str,
        speed_1_total_wh_capacity_function_of_air_flow_fraction_curve_name: str,
        speed_1_total_wh_capacity_function_of_water_flow_fraction_curve_name: str,
        speed_1_cop_function_of_temperature_curve_name: str,
        speed_1_cop_function_of_air_flow_fraction_curve_name: str,
        speed_1_cop_function_of_water_flow_fraction_curve_name: str,
        number_of_speeds: float | None = 1,
        nominal_speed_level: float | None = 1,
        rated_evaporator_inlet_air_dry_bulb_temperature: float | None = 19.7,
        rated_evaporator_inlet_air_wet_bulb_temperature: float | None = 13.5,
        rated_condenser_inlet_water_temperature: float | None = 57.5,
        rated_evaporator_air_flow_rate: float | Literal["Autocalculate"] | None = ...,
        rated_condenser_water_flow_rate: float | Literal["Autocalculate"] | None = ...,
        evaporator_fan_power_included_in_rated_cop: Literal["No", "Yes"] | None = "Yes",
        condenser_pump_power_included_in_rated_cop: Literal["No", "Yes"] | None = "No",
        condenser_pump_heat_included_in_rated_heating_capacity_and_rated_cop: Literal["No", "Yes"] | None = "No",
        fraction_of_condenser_pump_heat_to_water: float | None = 0.2,
        crankcase_heater_capacity: float | None = 0,
        maximum_ambient_temperature_for_crankcase_heater_operation: float | None = 10,
        evaporator_air_temperature_type_for_curve_objects: Literal["DryBulbTemperature", "WetBulbTemperature"]
        | None = "WetBulbTemperature",
        part_load_fraction_correlation_curve_name: str | None = ...,
        rated_water_heating_cop_at_speed_1: float | None = 3.2,
        rated_sensible_heat_ratio_at_speed_1: float | None = 0.85,
        rated_water_heating_capacity_at_speed_2: float | None = ...,
        rated_water_heating_cop_at_speed_2: float | None = 3.2,
        rated_sensible_heat_ratio_at_speed_2: float | None = 0.85,
        speed_2_reference_unit_rated_air_flow_rate: float | None = ...,
        speed_2_reference_unit_rated_water_flow_rate: float | None = ...,
        speed_2_reference_unit_water_pump_input_power_at_rated_conditions: float | None = ...,
        speed_2_total_wh_capacity_function_of_temperature_curve_name: str | None = ...,
        speed_2_total_wh_capacity_function_of_air_flow_fraction_curve_name: str | None = ...,
        speed_2_total_wh_capacity_function_of_water_flow_fraction_curve_name: str | None = ...,
        speed_2_cop_function_of_temperature_curve_name: str | None = ...,
        speed_2_cop_function_of_air_flow_fraction_curve_name: str | None = ...,
        speed_2_cop_function_of_water_flow_fraction_curve_name: str | None = ...,
        rated_water_heating_capacity_at_speed_3: float | None = ...,
        rated_water_heating_cop_at_speed_3: float | None = 3.2,
        rated_sensible_heat_ratio_at_speed_3: float | None = 0.85,
        speed_3_reference_unit_rated_air_flow_rate: float | None = ...,
        speed_3_reference_unit_rated_water_flow_rate: float | None = ...,
        speed_3_reference_unit_water_pump_input_power_at_rated_conditions: float | None = ...,
        speed_3_total_wh_capacity_function_of_temperature_curve_name: str | None = ...,
        speed_3_total_wh_capacity_function_of_air_flow_fraction_curve_name: str | None = ...,
        speed_3_total_wh_capacity_function_of_water_flow_fraction_curve_name: str | None = ...,
        speed_3_cop_function_of_temperature_curve_name: str | None = ...,
        speed_3_cop_function_of_air_flow_fraction_curve_name: str | None = ...,
        speed_3_cop_function_of_water_flow_fraction_curve_name: str | None = ...,
        rated_water_heating_capacity_at_speed_4: float | None = ...,
        rated_water_heating_cop_at_speed_4: float | None = 3.2,
        rated_sensible_heat_ratio_at_speed_4: float | None = 0.85,
        speed_4_reference_unit_rated_air_flow_rate: float | None = ...,
        speed_4_reference_unit_rated_water_flow_rate: float | None = ...,
        speed_4_reference_unit_water_pump_input_power_at_rated_conditions: float | None = ...,
        speed_4_total_wh_capacity_function_of_temperature_curve_name: str | None = ...,
        speed_4_total_wh_capacity_function_of_air_flow_fraction_curve_name: str | None = ...,
        speed_4_total_wh_capacity_function_of_water_flow_fraction_curve_name: str | None = ...,
        speed_4_cop_function_of_temperature_curve_name: str | None = ...,
        speed_4_cop_function_of_air_flow_fraction_curve_name: str | None = ...,
        speed_4_cop_function_of_water_flow_fraction_curve_name: str | None = ...,
        rated_water_heating_capacity_at_speed_5: float | None = ...,
        rated_water_heating_cop_at_speed_5: float | None = 3.2,
        rated_sensible_heat_ratio_at_speed_5: float | None = 0.85,
        speed_5_reference_unit_rated_air_flow_rate: float | None = ...,
        speed_5_reference_unit_rated_water_flow_rate: float | None = ...,
        speed_5_reference_unit_water_pump_input_power_at_rated_conditions: float | None = ...,
        speed_5_total_wh_capacity_function_of_temperature_curve_name: str | None = ...,
        speed_5_total_wh_capacity_function_of_air_flow_fraction_curve_name: str | None = ...,
        speed_5_total_wh_capacity_function_of_water_flow_fraction_curve_name: str | None = ...,
        speed_5_cop_function_of_temperature_curve_name: str | None = ...,
        speed_5_cop_function_of_air_flow_fraction_curve_name: str | None = ...,
        speed_5_cop_function_of_water_flow_fraction_curve_name: str | None = ...,
        rated_water_heating_capacity_at_speed_6: float | None = ...,
        rated_water_heating_cop_at_speed_6: float | None = 3.2,
        rated_sensible_heat_ratio_at_speed_6: float | None = 0.85,
        speed_6_reference_unit_rated_air_flow_rate: float | None = ...,
        speed_6_reference_unit_rated_water_flow_rate: float | None = ...,
        speed_6_reference_unit_water_pump_input_power_at_rated_conditions: float | None = ...,
        speed_6_total_wh_capacity_function_of_temperature_curve_name: str | None = ...,
        speed_6_total_wh_capacity_function_of_air_flow_fraction_curve_name: str | None = ...,
        speed_6_total_wh_capacity_function_of_water_flow_fraction_curve_name: str | None = ...,
        speed_6_cop_function_of_temperature_curve_name: str | None = ...,
        speed_6_cop_function_of_air_flow_fraction_curve_name: str | None = ...,
        speed_6_cop_function_of_water_flow_fraction_curve_name: str | None = ...,
        rated_water_heating_capacity_at_speed_7: float | None = ...,
        rated_water_heating_cop_at_speed_7: float | None = 3.2,
        rated_sensible_heat_ratio_at_speed_7: float | None = 0.85,
        speed_7_reference_unit_rated_air_flow_rate: float | None = ...,
        speed_7_reference_unit_rated_water_flow_rate: float | None = ...,
        speed_7_reference_unit_water_pump_input_power_at_rated_conditions: float | None = ...,
        speed_7_total_wh_capacity_function_of_temperature_curve_name: str | None = ...,
        speed_7_total_wh_capacity_function_of_air_flow_fraction_curve_name: str | None = ...,
        speed_7_total_wh_capacity_function_of_water_flow_fraction_curve_name: str | None = ...,
        speed_7_cop_function_of_temperature_curve_name: str | None = ...,
        speed_7_cop_function_of_air_flow_fraction_curve_name: str | None = ...,
        speed_7_cop_function_of_water_flow_fraction_curve_name: str | None = ...,
        rated_water_heating_capacity_at_speed_8: float | None = ...,
        rated_water_heating_cop_at_speed_8: float | None = 3.2,
        rated_sensible_heat_ratio_at_speed_8: float | None = 0.85,
        speed_8_reference_unit_rated_air_flow_rate: float | None = ...,
        speed_8_reference_unit_rated_water_flow_rate: float | None = ...,
        speed_8_reference_unit_water_pump_input_power_at_rated_conditions: float | None = ...,
        speed_8_total_wh_capacity_function_of_temperature_curve_name: str | None = ...,
        speed_8_total_wh_capacity_function_of_air_flow_fraction_curve_name: str | None = ...,
        speed_8_total_wh_capacity_function_of_water_flow_fraction_curve_name: str | None = ...,
        speed_8_cop_function_of_temperature_curve_name: str | None = ...,
        speed_8_cop_function_of_air_flow_fraction_curve_name: str | None = ...,
        speed_8_cop_function_of_water_flow_fraction_curve_name: str | None = ...,
        rated_water_heating_capacity_at_speed_9: float | None = ...,
        rated_water_heating_cop_at_speed_9: float | None = 3.2,
        rated_sensible_heat_ratio_at_speed_9: float | None = 0.85,
        speed_9_reference_unit_rated_air_flow_rate: float | None = ...,
        speed_9_reference_unit_rated_water_flow_rate: float | None = ...,
        speed_9_reference_unit_water_pump_input_power_at_rated_conditions: float | None = ...,
        speed_9_total_wh_capacity_function_of_temperature_curve_name: str | None = ...,
        speed_9_total_wh_capacity_function_of_air_flow_fraction_curve_name: str | None = ...,
        speed_9_total_wh_capacity_function_of_water_flow_fraction_curve_name: str | None = ...,
        speed_9_cop_function_of_temperature_curve_name: str | None = ...,
        speed_9_cop_function_of_air_flow_fraction_curve_name: str | None = ...,
        speed_9_cop_function_of_water_flow_fraction_curve_name: str | None = ...,
        rated_water_heating_capacity_at_speed_10: float | None = ...,
        rated_water_heating_cop_at_speed_10: float | None = 3.2,
        rated_sensible_heat_ratio_at_speed_10: float | None = 0.85,
        speed_10_reference_unit_rated_air_flow_rate: float | None = ...,
        speed_10_reference_unit_rated_water_flow_rate: float | None = ...,
        speed_10_reference_unit_water_pump_input_power_at_rated_conditions: float | None = ...,
        speed_10_total_wh_capacity_function_of_temperature_curve_name: str | None = ...,
        speed_10_total_wh_capacity_function_of_air_flow_fraction_curve_name: str | None = ...,
        speed_10_total_wh_capacity_function_of_water_flow_fraction_curve_name: str | None = ...,
        speed_10_cop_function_of_temperature_curve_name: str | None = ...,
        speed_10_cop_function_of_air_flow_fraction_curve_name: str | None = ...,
        speed_10_cop_function_of_water_flow_fraction_curve_name: str | None = ...,
        validate: bool = True,
    ) -> None:
        """Create a new ``Coil:WaterHeating:AirToWaterHeatPump:VariableSpeed`` and add it to the document.

        vairlable-speed Heat pump water heater (VSHPWH) heating coil, air-to-water direct-expansion (DX) system which includes a variable-speed water heating coil, evaporator air coil, evaporator fan, electric compressor, and water pump. Part of a WaterHeater:HeatPump system.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v22.1/io-reference/overview/group-heating-and-cooling-coils/#coilwaterheatingairtowaterheatpumpvariablespeed
        """

class EvaporativeFluidCoolerSingleSpeed_v8_9_to_v25_1:
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
        design_entering_water_temperature: float | None = ...,
        design_entering_air_temperature: float | None = ...,
        design_entering_air_wet_bulb_temperature: float | None = ...,
        capacity_control: Literal["FanCycling", "FluidBypass"] | None = "FanCycling",
        sizing_factor: float | None = 1,
        evaporation_loss_mode: Literal["LossFactor", "SaturatedExit"] | None = "SaturatedExit",
        evaporation_loss_factor: float | None = ...,
        drift_loss_percent: float | None = 0.008,
        blowdown_calculation_mode: Literal["ConcentrationRatio", "ScheduledRate"] | None = "ConcentrationRatio",
        blowdown_concentration_ratio: float | None = 3,
        blowdown_makeup_water_usage_schedule_name: str | None = ...,
        supply_water_storage_tank_name: str | None = ...,
        validate: bool = True,
    ) -> None:
        """Create a new ``EvaporativeFluidCooler:SingleSpeed`` and add it to the document.

        This model is based on Merkel's theory, which is also the basis for the cooling tower model in EnergyPlus. The Evaporative fluid cooler is modeled as a counter flow heat exchanger.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v25.1/io-reference/overview/group-condenser-equipment/#evaporativefluidcoolersinglespeed
        """

class LifeCycleCostNonrecurringCost_v8_9_to_v22_1:
    def __call__(
        self,
        name: str,
        /,
        *,
        category: Literal["Construction", "OtherCapital", "Salvage"] | None = "Construction",
        cost: float | None = ...,
        start_of_costs: Literal["BasePeriod", "ServicePeriod"] | None = "ServicePeriod",
        years_from_start: float | None = ...,
        months_from_start: float | None = ...,
        validate: bool = True,
    ) -> None:
        """Create a new ``LifeCycleCost:NonrecurringCost`` and add it to the document.

        A non-recurring cost happens only once during the study period. For costs that occur more than once during the study period on a regular schedule, use the LifeCycleCost:RecurringCost object.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v22.1/io-reference/energyplus-economics/lifecyclecost-nonrecurringcost/#lifecyclecostnonrecurringcost
        """

class RoomAirNodeAirflowNetworkHVACEquipment_v8_9_to_v9_2:
    def __call__(
        self,
        name: str = "",
        /,
        *,
        equipment_fractions: Sequence[
            _vd.RoomAirNodeAirflowNetworkHVACEquipmentEquipmentFractionsItem_v8_9_to_v9_2
            | _vd.RoomAirNodeAirflowNetworkHVACEquipmentEquipmentFractionsGroup_v8_9_to_v9_2
        ] = ...,
        validate: bool = True,
    ) -> None:
        """Create a new ``RoomAir:Node:AirflowNetwork:HVACEquipment`` and add it to the document.

        define the zone equipment associated with one particular RoomAir:Node

        ``equipment_fractions`` takes the extensible groups in order, one dict per group:

        ```python
        doc["RoomAir:Node:AirflowNetwork:HVACEquipment"].add(
            "RoomAir Node AirflowNetwork HVACEquipment 1",
            equipment_fractions=[
                {
                    "fraction_of_output_or_supply_air_from_hvac_equipment": 0.0,
                    "fraction_of_input_or_return_air_to_hvac_equipment": 0.0,
                    "zonehvac_or_air_terminal_equipment_object_type": "AirLoopHVACReturnAir",
                    "zonehvac_or_air_terminal_equipment_object_name": "ZoneHVAC or Air Terminal Equipment Object 1",
                },
                {
                    "fraction_of_output_or_supply_air_from_hvac_equipment": 0.0,
                    "fraction_of_input_or_return_air_to_hvac_equipment": 0.0,
                    "zonehvac_or_air_terminal_equipment_object_type": "AirTerminal:DualDuct:ConstantVolume",
                    "zonehvac_or_air_terminal_equipment_object_name": "ZoneHVAC or Air Terminal Equipment Object 2",
                },
            ],
        )
        ```

        EnergyPlus I/O Reference: https://docs.idfkit.com/v9.2/io-reference/overview/group-room-air-models/#roomairnodeairflownetworkhvacequipment
        """
