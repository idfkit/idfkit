"""Creation signatures of generated classes (stub only).

DO NOT EDIT — regenerate with:
    python -m idfkit.codegen.generate_stubs
"""

from __future__ import annotations

from collections.abc import Sequence
from typing import Literal

from .. import _generated_types as _g

class DuctLossLeakage:
    def __call__(
        self,
        name: str,
        /,
        *,
        airloophvac_name: str,
        airflownetwork_distribution_linkage_name: str,
        validate: bool = True,
    ) -> None:
        """Create a new ``Duct:Loss:Leakage`` and add it to the document.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-airflow-network/#ductlossleakage
        """

class ZoneHVACEvaporativeCoolerUnit:
    def __call__(
        self,
        name: str,
        /,
        *,
        outdoor_air_inlet_node_name: str,
        cooler_outlet_node_name: str,
        supply_air_fan_object_type: Literal[
            "Fan:ComponentModel", "Fan:ConstantVolume", "Fan:OnOff", "Fan:SystemModel", "Fan:VariableVolume"
        ],
        supply_air_fan_name: str,
        design_supply_air_flow_rate: float | Literal["Autosize"],
        fan_placement: Literal["BlowThrough", "DrawThrough"],
        cooler_unit_control_method: Literal[
            "ZoneCoolingLoadOnOffCycling", "ZoneCoolingLoadVariableSpeedFan", "ZoneTemperatureDeadbandOnOffCycling"
        ],
        first_evaporative_cooler_object_type: Literal[
            "EvaporativeCooler:Direct:CelDekPad",
            "EvaporativeCooler:Direct:ResearchSpecial",
            "EvaporativeCooler:Indirect:CelDekPad",
            "EvaporativeCooler:Indirect:ResearchSpecial",
            "EvaporativeCooler:Indirect:WetCoil",
        ],
        first_evaporative_cooler_object_name: str,
        availability_schedule_name: str | None = ...,
        availability_manager_list_name: str | None = ...,
        zone_relief_air_node_name: str | None = ...,
        throttling_range_temperature_difference: float | None = 1,
        cooling_load_control_threshold_heat_transfer_rate: float | None = 100,
        second_evaporative_cooler_object_type: Literal[
            "EvaporativeCooler:Direct:CelDekPad",
            "EvaporativeCooler:Direct:ResearchSpecial",
            "EvaporativeCooler:Indirect:CelDekPad",
            "EvaporativeCooler:Indirect:ResearchSpecial",
            "EvaporativeCooler:Indirect:WetCoil",
        ]
        | None = ...,
        second_evaporative_cooler_name: str | None = ...,
        design_specification_zonehvac_sizing_object_name: str | None = ...,
        shut_off_relative_humidity: float | None = ...,
        validate: bool = True,
    ) -> None:
        """Create a new ``ZoneHVAC:EvaporativeCoolerUnit`` and add it to the document.

        Zone evaporative cooler. Forced-convection cooling-only unit with supply fan, 100% outdoor air supply. Optional relief exhaust node

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-zone-forced-air-units/#zonehvacevaporativecoolerunit
        """

class AirLoopHVACUnitaryFurnaceHeatCool:
    def __call__(
        self,
        name: str,
        /,
        *,
        furnace_air_inlet_node_name: str,
        furnace_air_outlet_node_name: str,
        cooling_supply_air_flow_rate: float | Literal["Autosize"],
        heating_supply_air_flow_rate: float | Literal["Autosize"],
        controlling_zone_or_thermostat_location: str,
        supply_fan_object_type: Literal["Fan:ConstantVolume", "Fan:OnOff"],
        supply_fan_name: str,
        heating_coil_object_type: Literal[
            "Coil:Heating:Electric", "Coil:Heating:Fuel", "Coil:Heating:Steam", "Coil:Heating:Water"
        ],
        heating_coil_name: str,
        cooling_coil_object_type: Literal[
            "Coil:Cooling:DX:SingleSpeed",
            "Coil:Cooling:DX:VariableSpeed",
            "CoilSystem:Cooling:DX:HeatExchangerAssisted",
        ],
        cooling_coil_name: str,
        availability_schedule_name: str | None = ...,
        supply_air_fan_operating_mode_schedule_name: str | None = ...,
        maximum_supply_air_temperature: float | Literal["Autosize"] | None = 80,
        no_load_supply_air_flow_rate: float | Literal["Autosize"] | None = ...,
        fan_placement: Literal["BlowThrough", "DrawThrough"] | None = "BlowThrough",
        dehumidification_control_type: Literal["CoolReheat", "Multimode", "None"] | None = "None",
        reheat_coil_object_type: Literal[
            "Coil:Heating:Desuperheater",
            "Coil:Heating:Electric",
            "Coil:Heating:Fuel",
            "Coil:Heating:Steam",
            "Coil:Heating:Water",
        ]
        | None = ...,
        reheat_coil_name: str | None = ...,
        validate: bool = True,
    ) -> None:
        """Create a new ``AirLoopHVAC:Unitary:Furnace:HeatCool`` and add it to the document.

        Unitary system, heating and cooling with constant volume supply fan (continuous or cycling), direct expansion (DX) cooling coil, heating coil (gas, electric, hot water, or steam), and optional reheat coil for dehumidification control. Identical to AirLoopHVAC:UnitaryHeatCool.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-unitary-equipment/#airloophvacunitaryfurnaceheatcool
        """

class AnyPumpVariableSpeedCondensate:
    def __call__(
        self,
        name: str,
        /,
        *,
        inlet_node_name: str,
        outlet_node_name: str,
        design_steam_volume_flow_rate: float | Literal["Autosize"] | None = ...,
        design_pump_head: float | None = 179352,
        design_power_consumption: float | Literal["Autosize"] | None = ...,
        motor_efficiency: float | None = 0.9,
        fraction_of_motor_inefficiencies_to_fluid_stream: float | None = 0,
        coefficient_1_of_the_part_load_performance_curve: float | None = 0,
        coefficient_2_of_the_part_load_performance_curve: float | None = 1,
        coefficient_3_of_the_part_load_performance_curve: float | None = 0,
        coefficient_4_of_the_part_load_performance_curve: float | None = 0,
        pump_flow_rate_schedule_name: str | None = ...,
        zone_name: str | None = ...,
        skin_loss_radiative_fraction: float | None = ...,
        design_power_sizing_method: Literal["PowerPerFlow", "PowerPerFlowPerPressure"]
        | None = "PowerPerFlowPerPressure",
        design_electric_power_per_unit_flow_rate: float | None = 348701.1,
        design_shaft_power_per_unit_flow_rate_per_unit_head: float | None = 1.282051282,
        validate: bool = True,
    ) -> None:
        """Create a new ``Pump:VariableSpeed:Condensate`` and add it to the document.

        This pump model is described in the ASHRAE secondary HVAC toolkit. Variable Speed Condensate pump for Steam Systems

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-pumps/#pumpvariablespeedcondensate
        """

class ExternalInterfaceFunctionalMockupUnitImportToSchedule:
    def __call__(
        self,
        name: str,
        /,
        *,
        fmu_file_name: str,
        fmu_instance_name: str,
        fmu_variable_name: str,
        initial_value: float,
        schedule_type_limits_names: str | None = ...,
        validate: bool = True,
    ) -> None:
        """Create a new ``ExternalInterface:FunctionalMockupUnitImport:To:Schedule`` and add it to the document.

        This objects contains only one value, which is used during the first call of EnergyPlus

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-externalinterface/#externalinterfacefunctionalmockupunitimporttoschedule
        """

class AvailabilityManagerHighTemperatureTurnOn:
    def __call__(self, name: str, /, *, sensor_node_name: str, temperature: float, validate: bool = True) -> None:
        """Create a new ``AvailabilityManager:HighTemperatureTurnOn`` and add it to the document.

        Overrides fan/pump schedules depending on temperature at sensor node.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-system-availability-managers/#availabilitymanagerhightemperatureturnon
        """

class SetpointManagerSystemNodeResetTemperature:
    def __call__(
        self,
        name: str,
        /,
        *,
        control_variable: Literal["MaximumTemperature", "MinimumTemperature", "Temperature"],
        setpoint_at_low_reference_temperature: float,
        setpoint_at_high_reference_temperature: float,
        low_reference_temperature: float,
        high_reference_temperature: float,
        reference_node_name: str,
        setpoint_node_or_nodelist_name: str,
        validate: bool = True,
    ) -> None:
        """Create a new ``SetpointManager:SystemNodeReset:Temperature`` and add it to the document.

        This Setpoint Manager is used to place a temperature setpoint on a system node according to the reference (e.g., return) temperature using a reset rule. The temperature setpoint is obtained by retrieving the temperature of the user specified reference system node.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-setpoint-managers/#setpointmanagersystemnoderesettemperature
        """

class MatrixTwoDimension:
    def __call__(
        self,
        name: str,
        /,
        *,
        number_of_rows: int,
        number_of_columns: int,
        values: Sequence[_g.MatrixTwoDimensionValuesItem | _g.MatrixTwoDimensionValuesGroup] = ...,
        validate: bool = True,
    ) -> None:
        """Create a new ``Matrix:TwoDimension`` and add it to the document.

        matrix data in row-major order list each row keeping the columns in order number of values must equal N1 x N2

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-surface-construction-elements/#matrixtwodimension
        """
