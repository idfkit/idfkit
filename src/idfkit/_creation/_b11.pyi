"""Creation signatures of generated classes (stub only).

DO NOT EDIT — regenerate with:
    python -m idfkit.codegen.generate_stubs
"""

from __future__ import annotations

from typing import Literal

class AnySiteLocation:
    def __call__(
        self,
        name: str,
        /,
        *,
        latitude: float | None = 0,
        longitude: float | None = 0,
        time_zone: float | None = 0,
        elevation: float | None = 0,
    ) -> None:
        """Create a new ``Site:Location`` and add it to the document.

        Specifies the building's location. Only one location is allowed. Weather data file location, if it exists, will override this object.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-location-climate-weather-file-access/#sitelocation
        """

class CoilHeatingDXVariableRefrigerantFlowFluidTemperatureControl:
    def __call__(
        self,
        name: str,
        /,
        *,
        coil_air_inlet_node: str,
        coil_air_outlet_node: str,
        rated_total_heating_capacity: float | Literal["Autosize"],
        indoor_unit_condensing_temperature_function_of_subcooling_curve_name: str,
        availability_schedule: str | None = ...,
        indoor_unit_reference_subcooling: float | None = 5,
    ) -> None:
        """Create a new ``Coil:Heating:DX:VariableRefrigerantFlow:FluidTemperatureControl`` and add it to the document.

        This is a key object in the new physics based VRF model applicable for Fluid Temperature Control. It describes the the indoor unit coil of the system at heating mode. Used with ZoneHVAC:TerminalUnit:VariableRefrigerantFlow. Outdoor unit is modeled separately, see AirConditioner:VariableRefrigerantFlow:FluidTemperatureControl or AirConditioner:VariableRefrigerantFlow:FluidTemperatureControl:HR

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-heating-and-cooling-coils/#coilheatingdxvariablerefrigerantflowfluidtemperaturecontrol
        """

class AirLoopHVACUnitaryHeatPumpAirToAirMultiSpeed:
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
        dx_heating_coil_sizing_ratio: float | None = 1,
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

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-unitary-equipment/#airloophvacunitaryheatpumpairtoairmultispeed
        """

class AnyPumpVariableSpeed:
    def __call__(
        self,
        name: str,
        /,
        *,
        inlet_node_name: str,
        outlet_node_name: str,
        design_maximum_flow_rate: float | Literal["Autosize"] | None = ...,
        design_pump_head: float | None = 179352,
        design_power_consumption: float | Literal["Autosize"] | None = ...,
        motor_efficiency: float | None = 0.9,
        fraction_of_motor_inefficiencies_to_fluid_stream: float | None = 0,
        coefficient_1_of_the_part_load_performance_curve: float | None = 0,
        coefficient_2_of_the_part_load_performance_curve: float | None = 1,
        coefficient_3_of_the_part_load_performance_curve: float | None = 0,
        coefficient_4_of_the_part_load_performance_curve: float | None = 0,
        design_minimum_flow_rate: float | Literal["Autosize"] | None = "Autosize",
        pump_control_type: Literal["Continuous", "Intermittent"] | None = "Continuous",
        pump_flow_rate_schedule_name: str | None = ...,
        pump_curve_name: str | None = ...,
        impeller_diameter: float | None = ...,
        vfd_control_type: Literal["ManualControl", "PressureSetpointControl"] | None = ...,
        pump_rpm_schedule_name: str | None = ...,
        minimum_pressure_schedule: str | None = ...,
        maximum_pressure_schedule: str | None = ...,
        minimum_rpm_schedule: str | None = ...,
        maximum_rpm_schedule: str | None = ...,
        zone_name: str | None = ...,
        skin_loss_radiative_fraction: float | None = ...,
        design_power_sizing_method: Literal["PowerPerFlow", "PowerPerFlowPerPressure"]
        | None = "PowerPerFlowPerPressure",
        design_electric_power_per_unit_flow_rate: float | None = 348701.1,
        design_shaft_power_per_unit_flow_rate_per_unit_head: float | None = 1.282051282,
        design_minimum_flow_rate_fraction: float | None = 0,
    ) -> None:
        """Create a new ``Pump:VariableSpeed`` and add it to the document.

        This pump model is described in the ASHRAE secondary HVAC toolkit.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-pumps/#pumpvariablespeed
        """

class PlantEquipmentOperationOutdoorDryBulbDifference:
    def __call__(
        self,
        name: str,
        /,
        *,
        reference_temperature_node_name: str,
        dry_bulb_temperature_difference_range_1_lower_limit: float,
        dry_bulb_temperature_difference_range_1_upper_limit: float,
        range_1_equipment_list_name: str,
        dry_bulb_temperature_difference_range_2_lower_limit: float | None = ...,
        dry_bulb_temperature_difference_range_2_upper_limit: float | None = ...,
        range_2_equipment_list_name: str | None = ...,
        dry_bulb_temperature_difference_range_3_lower_limit: float | None = ...,
        dry_bulb_temperature_difference_range_3_upper_limit: float | None = ...,
        range_3_equipment_list_name: str | None = ...,
        dry_bulb_temperature_difference_range_4_lower_limit: float | None = ...,
        dry_bulb_temperature_difference_range_4_upper_limit: float | None = ...,
        range_4_equipment_list_name: str | None = ...,
        dry_bulb_temperature_difference_range_5_lower_limit: float | None = ...,
        dry_bulb_temperature_difference_range_5_upper_limit: float | None = ...,
        range_5_equipment_list_name: str | None = ...,
        dry_bulb_temperature_difference_range_6_lower_limit: float | None = ...,
        dry_bulb_temperature_difference_range_6_upper_limit: float | None = ...,
        range_6_equipment_list_name: str | None = ...,
        dry_bulb_temperature_difference_range_7_lower_limit: float | None = ...,
        dry_bulb_temperature_difference_range_7_upper_limit: float | None = ...,
        range_7_equipment_list_name: str | None = ...,
        dry_bulb_temperature_difference_range_8_lower_limit: float | None = ...,
        dry_bulb_temperature_difference_range_8_upper_limit: float | None = ...,
        range_8_equipment_list_name: str | None = ...,
        dry_bulb_temperature_difference_range_9_lower_limit: float | None = ...,
        dry_bulb_temperature_difference_range_9_upper_limit: float | None = ...,
        range_9_equipment_list_name: str | None = ...,
        dry_bulb_temperature_difference_range_10_lower_limit: float | None = ...,
        dry_bulb_temperature_difference_range_10_upper_limit: float | None = ...,
        range_10_equipment_list_name: str | None = ...,
    ) -> None:
        """Create a new ``PlantEquipmentOperation:OutdoorDryBulbDifference`` and add it to the document.

        Plant equipment operation scheme for outdoor dry-bulb temperature difference operation. Specifies one or more groups of equipment which are available to operate for successive ranges based the difference between a reference node temperature and the outdoor dry-bulb temperature.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-plant-condenser-control/#plantequipmentoperationoutdoordrybulbdifference
        """

class SetpointManagerCondenserEnteringResetIdeal:
    def __call__(
        self,
        name: str,
        /,
        *,
        setpoint_node_or_nodelist_name: str,
        control_variable: Literal["Temperature"] | None = "Temperature",
        minimum_lift: float | None = 11.1,
        maximum_condenser_entering_water_temperature: float | None = 32,
    ) -> None:
        """Create a new ``SetpointManager:CondenserEnteringReset:Ideal`` and add it to the document.

        This setpoint manager determine the ideal optimum condenser entering water temperature setpoint for a given timestep.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-setpoint-managers/#setpointmanagercondenserenteringresetideal
        """

class FaultModelFoulingCoil:
    def __call__(
        self,
        name: str,
        /,
        *,
        coil_name: str,
        availability_schedule_name: str | None = ...,
        severity_schedule_name: str | None = ...,
        fouling_input_method: Literal["FouledUARated", "FoulingFactor"] | None = "FouledUARated",
        uafouled: float | None = ...,
        water_side_fouling_factor: float | None = 0,
        air_side_fouling_factor: float | None = 0,
        outside_coil_surface_area: float | None = ...,
        inside_to_outside_coil_surface_area_ratio: float | None = 0.07,
    ) -> None:
        """Create a new ``FaultModel:Fouling:Coil`` and add it to the document.

        This object describes fouling water heating or cooling coils

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-operational-faults/#faultmodelfoulingcoil
        """

class CurveFunctionalPressureDrop:
    def __call__(
        self,
        name: str,
        /,
        *,
        diameter: float,
        minor_loss_coefficient: float | None = ...,
        length: float | None = ...,
        roughness: float | None = ...,
        fixed_friction_factor: float | None = ...,
    ) -> None:
        """Create a new ``Curve:Functional:PressureDrop`` and add it to the document.

        Sets up curve information for minor loss and/or friction calculations in plant pressure simulations Expression: DeltaP = {K + f*(L/D)} * (rho * V^2) / 2

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-performance-curves/#curvefunctionalpressuredrop
        """
