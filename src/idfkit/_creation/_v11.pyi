"""Creation signatures of generated classes (stub only).

DO NOT EDIT — regenerate with:
    python -m idfkit.codegen.generate_stubs
"""

from __future__ import annotations

from typing import Literal

from .. import _generated_types as _g

class RoomAirTemperaturePatternConstantGradient_v8_9_to_v22_1:
    def __call__(
        self,
        /,
        *,
        room_air_temperature_pattern_constant_gradient_name: str,
        control_integer_for_pattern_control_schedule_name: float,
        thermostat_offset: float | None = ...,
        return_air_offset: float | None = ...,
        exhaust_air_offset: float | None = ...,
        temperature_gradient: float | None = ...,
    ) -> None:
        """Create a new ``RoomAir:TemperaturePattern:ConstantGradient`` and add it to the document.

        Used to model room air with a fixed temperature gradient in the vertical direction. Used in combination with RoomAir:TemperaturePattern:UserDefined.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v22.1/io-reference/overview/group-room-air-models/#roomairtemperaturepatternconstantgradient
        """

class ZoneRefrigerationDoorMixing_v8_9_to_v24_1:
    def __call__(
        self,
        name: str,
        /,
        *,
        zone_1_name: str,
        zone_2_name: str,
        schedule_name: str,
        door_height: float | None = 3,
        door_area: float | None = 9,
        door_protection_type: Literal["", "AirCurtain", "None", "StripCurtain"] | None = "None",
    ) -> None:
        """Create a new ``ZoneRefrigerationDoorMixing`` and add it to the document.

        Refrigeration Door Mixing is used for an opening between two zones that are at the same elevation but have different air temperatures. In this case, the mixing air flow between the two zones is determined by the density difference between the two zones. This would typically be used between two zones in a refrigerated warehouse that are controlled at different temperatures. It could also be used to model a door to a walk-in refrigerated space if that space were modeled as a zone instead of using the object Refrigeration:WalkIn.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v24.1/io-reference/overview/group-airflow/#zonerefrigerationdoormixing
        """

class ZoneHVACTerminalUnitVariableRefrigerantFlow_v8_9_to_v9_1:
    def __call__(
        self,
        name: str = "",
        /,
        *,
        terminal_unit_air_inlet_node_name: str,
        terminal_unit_air_outlet_node_name: str,
        supply_air_fan_operating_mode_schedule_name: str,
        supply_air_fan_object_name: str,
        terminal_unit_availability_schedule: str | None = ...,
        cooling_supply_air_flow_rate: float | Literal["Autosize"] | None = ...,
        no_cooling_supply_air_flow_rate: float | Literal["Autosize"] | None = ...,
        heating_supply_air_flow_rate: float | Literal["Autosize"] | None = ...,
        no_heating_supply_air_flow_rate: float | Literal["Autosize"] | None = ...,
        cooling_outdoor_air_flow_rate: float | Literal["Autosize"] | None = ...,
        heating_outdoor_air_flow_rate: float | Literal["Autosize"] | None = ...,
        no_load_outdoor_air_flow_rate: float | Literal["Autosize"] | None = ...,
        supply_air_fan_placement: Literal["", "BlowThrough", "DrawThrough"] | None = "BlowThrough",
        supply_air_fan_object_type: Literal[
            "", "Fan:ConstantVolume", "Fan:OnOff", "Fan:SystemModel", "Fan:VariableVolume"
        ]
        | None = "Fan:ConstantVolume",
        outside_air_mixer_object_type: Literal["OutdoorAir:Mixer"] | None = ...,
        outside_air_mixer_object_name: str | None = ...,
        cooling_coil_object_type: Literal[
            "Coil:Cooling:DX:VariableRefrigerantFlow", "Coil:Cooling:DX:VariableRefrigerantFlow:FluidTemperatureControl"
        ]
        | None = ...,
        cooling_coil_object_name: str | None = ...,
        heating_coil_object_type: Literal[
            "Coil:Heating:DX:VariableRefrigerantFlow", "Coil:Heating:DX:VariableRefrigerantFlow:FluidTemperatureControl"
        ]
        | None = ...,
        heating_coil_object_name: str | None = ...,
        zone_terminal_unit_on_parasitic_electric_energy_use: float | None = 0,
        zone_terminal_unit_off_parasitic_electric_energy_use: float | None = 0,
        rated_heating_capacity_sizing_ratio: float | None = 1,
        availability_manager_list_name: str | None = ...,
        design_specification_zonehvac_sizing_object_name: str | None = ...,
    ) -> None:
        """Create a new ``ZoneHVAC:TerminalUnit:VariableRefrigerantFlow`` and add it to the document.

        Zone terminal unit with variable refrigerant flow (VRF) DX cooling and heating coils (air-to-air heat pump). The VRF terminal units are served by an AirConditioner:VariableRefrigerantFlow system.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v9.1/io-reference/overview/group-zone-forced-air-units/#zonehvacterminalunitvariablerefrigerantflow
        """

class WaterHeaterStratified_v9_3_to_v22_1:
    def __call__(
        self,
        name: str,
        /,
        *,
        tank_volume: float | Literal["Autosize"],
        tank_height: float | Literal["Autosize"],
        heater_1_setpoint_temperature_schedule_name: str,
        heater_2_setpoint_temperature_schedule_name: str,
        heater_fuel_type: Literal[
            "Coal",
            "Diesel",
            "DistrictHeating",
            "Electricity",
            "FuelOilNo1",
            "FuelOilNo2",
            "Gasoline",
            "NaturalGas",
            "OtherFuel1",
            "OtherFuel2",
            "Propane",
            "Steam",
        ],
        heater_thermal_efficiency: float,
        ambient_temperature_indicator: Literal["Outdoors", "Schedule", "Zone"],
        end_use_subcategory: str | None = "General",
        tank_shape: Literal["", "HorizontalCylinder", "Other", "VerticalCylinder"] | None = "VerticalCylinder",
        tank_perimeter: float | None = ...,
        maximum_temperature_limit: float | None = ...,
        heater_priority_control: Literal["", "MasterSlave", "Simultaneous"] | None = "MasterSlave",
        heater_1_deadband_temperature_difference: float | None = 0,
        heater_1_capacity: float | Literal["Autosize"] | None = ...,
        heater_1_height: float | None = ...,
        heater_2_deadband_temperature_difference: float | None = 0,
        heater_2_capacity: float | None = ...,
        heater_2_height: float | None = ...,
        off_cycle_parasitic_fuel_consumption_rate: float | None = 0,
        off_cycle_parasitic_fuel_type: Literal[
            "Coal",
            "Diesel",
            "DistrictHeating",
            "Electricity",
            "FuelOilNo1",
            "FuelOilNo2",
            "Gasoline",
            "NaturalGas",
            "OtherFuel1",
            "OtherFuel2",
            "Propane",
            "Steam",
        ]
        | None = ...,
        off_cycle_parasitic_heat_fraction_to_tank: float | None = 0,
        off_cycle_parasitic_height: float | None = 0,
        on_cycle_parasitic_fuel_consumption_rate: float | None = 0,
        on_cycle_parasitic_fuel_type: Literal[
            "Coal",
            "Diesel",
            "DistrictHeating",
            "Electricity",
            "FuelOilNo1",
            "FuelOilNo2",
            "Gasoline",
            "NaturalGas",
            "OtherFuel1",
            "OtherFuel2",
            "Propane",
            "Steam",
        ]
        | None = ...,
        on_cycle_parasitic_heat_fraction_to_tank: float | None = 0,
        on_cycle_parasitic_height: float | None = 0,
        ambient_temperature_schedule_name: str | None = ...,
        ambient_temperature_zone_name: str | None = ...,
        ambient_temperature_outdoor_air_node_name: str | None = ...,
        uniform_skin_loss_coefficient_per_unit_area_to_ambient_temperature: float | None = ...,
        skin_loss_fraction_to_zone: float | None = 1,
        off_cycle_flue_loss_coefficient_to_ambient_temperature: float | None = ...,
        off_cycle_flue_loss_fraction_to_zone: float | None = 1,
        peak_use_flow_rate: float | None = ...,
        use_flow_rate_fraction_schedule_name: str | None = ...,
        cold_water_supply_temperature_schedule_name: str | None = ...,
        use_side_inlet_node_name: str | None = ...,
        use_side_outlet_node_name: str | None = ...,
        use_side_effectiveness: float | None = 1,
        use_side_inlet_height: float | None = 0,
        use_side_outlet_height: float | Literal["", "Autocalculate"] | None = "Autocalculate",
        source_side_inlet_node_name: str | None = ...,
        source_side_outlet_node_name: str | None = ...,
        source_side_effectiveness: float | None = 1,
        source_side_inlet_height: float | Literal["", "Autocalculate"] | None = "Autocalculate",
        source_side_outlet_height: float | None = 0,
        inlet_mode: Literal["", "Fixed", "Seeking"] | None = "Fixed",
        use_side_design_flow_rate: float | Literal["", "Autosize"] | None = "Autosize",
        source_side_design_flow_rate: float | Literal["", "Autosize"] | None = "Autosize",
        indirect_water_heating_recovery_time: float | None = 1.5,
        number_of_nodes: float | None = 1,
        additional_destratification_conductivity: float | None = 0,
        node_1_additional_loss_coefficient: float | None = 0,
        node_2_additional_loss_coefficient: float | None = 0,
        node_3_additional_loss_coefficient: float | None = 0,
        node_4_additional_loss_coefficient: float | None = 0,
        node_5_additional_loss_coefficient: float | None = 0,
        node_6_additional_loss_coefficient: float | None = 0,
        node_7_additional_loss_coefficient: float | None = 0,
        node_8_additional_loss_coefficient: float | None = 0,
        node_9_additional_loss_coefficient: float | None = 0,
        node_10_additional_loss_coefficient: float | None = 0,
        node_11_additional_loss_coefficient: float | None = 0,
        node_12_additional_loss_coefficient: float | None = 0,
        source_side_flow_control_mode: Literal[
            "", "IndirectHeatAlternateSetpoint", "IndirectHeatPrimarySetpoint", "StorageTank"
        ]
        | None = "IndirectHeatPrimarySetpoint",
        indirect_alternate_setpoint_temperature_schedule_name: str | None = ...,
    ) -> None:
        """Create a new ``WaterHeater:Stratified`` and add it to the document.

        Water heater with stratified, multi-node water tank. May be used to model a tankless water heater (small tank volume), a hot water storage tank (zero heater capacity), or a heat pump water heater (see WaterHeater:HeatPump:*.)

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v22.1/io-reference/overview/group-water-heaters/#waterheaterstratified
        """

class HeaderedPumpsVariableSpeed_v8_9_to_v9_0:
    def __call__(
        self,
        name: str,
        /,
        *,
        inlet_node_name: str,
        outlet_node_name: str,
        total_design_flow_rate: float | Literal["Autosize"] | None = ...,
        number_of_pumps_in_bank: float | None = ...,
        flow_sequencing_control_scheme: Literal["", "Sequential"] | None = "Sequential",
        design_pump_head: float | None = 179352,
        design_power_consumption: float | Literal["Autosize"] | None = ...,
        motor_efficiency: float | None = 0.9,
        fraction_of_motor_inefficiencies_to_fluid_stream: float | None = 0,
        coefficient_1_of_the_part_load_performance_curve: float | None = 0,
        coefficient_2_of_the_part_load_performance_curve: float | None = 1,
        coefficient_3_of_the_part_load_performance_curve: float | None = 0,
        coefficient_4_of_the_part_load_performance_curve: float | None = 0,
        minimum_flow_rate_fraction: float | None = 0,
        pump_control_type: Literal["", "Continuous", "Intermittent"] | None = "Continuous",
        pump_flow_rate_schedule_name: str | None = ...,
        zone_name: str | None = ...,
        skin_loss_radiative_fraction: float | None = ...,
        design_power_sizing_method: Literal["", "PowerPerFlow", "PowerPerFlowPerPressure"]
        | None = "PowerPerFlowPerPressure",
        design_electric_power_per_unit_flow_rate: float | None = 348701.1,
        design_shaft_power_per_unit_flow_rate_per_unit_head: float | None = 1.282051282,
    ) -> None:
        """Create a new ``HeaderedPumps:VariableSpeed`` and add it to the document.

        This Headered pump object describes a pump bank with more than 1 pump in parallel

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v9.0/io-reference/overview/group-pumps/#headeredpumpsvariablespeed
        """

class HybridModelZone_v8_9_to_v9_0:
    def __call__(
        self,
        name: str,
        /,
        *,
        zone_name: str,
        zone_measured_air_temperature_schedule_name: str,
        begin_month: float,
        begin_day_of_month: float,
        end_month: float,
        end_day_of_month: float,
        calculate_zone_internal_thermal_mass: Literal["", "No", "Yes"] | None = "No",
        calculate_zone_air_infiltration_rate: Literal["", "No", "Yes"] | None = "No",
    ) -> None:
        """Create a new ``HybridModel:Zone`` and add it to the document.

        Zones with measured air temperature data and a range of dates. If the range of temperature measurement dates includes a leap day, the weather data should include a leap day.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v9.0/io-reference/overview/group-hybrid-model/#hybridmodelzone
        """

class CoilWaterHeatingDesuperheater_v8_9_to_v9_1:
    def __call__(
        self,
        name: str,
        /,
        *,
        setpoint_temperature_schedule_name: str,
        rated_inlet_water_temperature: float,
        rated_outdoor_air_temperature: float,
        maximum_inlet_water_temperature_for_heat_reclaim: float,
        water_inlet_node_name: str,
        water_outlet_node_name: str,
        tank_name: str,
        heating_source_object_type: Literal[
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
        water_flow_rate: float,
        availability_schedule_name: str | None = ...,
        dead_band_temperature_difference: float | None = 5,
        rated_heat_reclaim_recovery_efficiency: float | None = ...,
        heat_reclaim_efficiency_function_of_temperature_curve_name: str | None = ...,
        tank_object_type: Literal["", "WaterHeater:Mixed"] | None = "WaterHeater:Mixed",
        water_pump_power: float | None = 0,
        fraction_of_pump_heat_to_water: float | None = 0.2,
        on_cycle_parasitic_electric_load: float | None = 0,
        off_cycle_parasitic_electric_load: float | None = 0,
    ) -> None:
        """Create a new ``Coil:WaterHeating:Desuperheater`` and add it to the document.

        Desuperheater air heating coil. The heating energy provided by this coil is reclaimed from the superheated refrigerant gas leaving a compressor and does not impact the performance of the compressor. This coil must be used with a water heater tank, see Water Heater:Mixed.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v9.1/io-reference/overview/group-heating-and-cooling-coils/#coilwaterheatingdesuperheater
        """

class CoilWaterHeatingDesuperheater_v22_2_to_v24_2:
    def __call__(
        self,
        name: str,
        /,
        *,
        setpoint_temperature_schedule_name: str,
        rated_inlet_water_temperature: float,
        rated_outdoor_air_temperature: float,
        maximum_inlet_water_temperature_for_heat_reclaim: float,
        water_inlet_node_name: str,
        water_outlet_node_name: str,
        tank_name: str,
        heating_source_object_type: Literal[
            "Coil:Cooling:DX",
            "Coil:Cooling:DX:MultiSpeed",
            "Coil:Cooling:DX:SingleSpeed",
            "Coil:Cooling:DX:TwoSpeed",
            "Coil:Cooling:DX:TwoStageWithHumidityControlMode",
            "Coil:Cooling:DX:VariableSpeed",
            "Coil:Cooling:WaterToAirHeatPump:EquationFit",
            "Refrigeration:CompressorRack",
            "Refrigeration:Condenser:AirCooled",
            "Refrigeration:Condenser:EvaporativeCooled",
            "Refrigeration:Condenser:WaterCooled",
        ],
        heating_source_name: str,
        water_flow_rate: float,
        availability_schedule_name: str | None = ...,
        dead_band_temperature_difference: float | None = 5,
        rated_heat_reclaim_recovery_efficiency: float | None = ...,
        heat_reclaim_efficiency_function_of_temperature_curve_name: str | None = ...,
        tank_object_type: Literal["", "WaterHeater:Mixed", "WaterHeater:Stratified"] | None = "WaterHeater:Mixed",
        water_pump_power: float | None = 0,
        fraction_of_pump_heat_to_water: float | None = 0.2,
        on_cycle_parasitic_electric_load: float | None = 0,
        off_cycle_parasitic_electric_load: float | None = 0,
    ) -> None:
        """Create a new ``Coil:WaterHeating:Desuperheater`` and add it to the document.

        Desuperheater air heating coil. The heating energy provided by this coil is reclaimed from the superheated refrigerant gas leaving a compressor and does not impact the performance of the compressor. This coil must be used with a water heater tank, see Water Heater:Mixed.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v24.2/io-reference/overview/group-heating-and-cooling-coils/#coilwaterheatingdesuperheater
        """

class ZoneHVACWaterToAirHeatPump_v9_2_to_v23_1:
    def __call__(
        self,
        name: str,
        /,
        *,
        air_inlet_node_name: str,
        air_outlet_node_name: str,
        cooling_supply_air_flow_rate: float | Literal["Autosize"],
        heating_supply_air_flow_rate: float | Literal["Autosize"],
        cooling_outdoor_air_flow_rate: float | Literal["Autosize"],
        heating_outdoor_air_flow_rate: float | Literal["Autosize"],
        supply_air_fan_object_type: Literal["Fan:OnOff", "Fan:SystemModel"],
        supply_air_fan_name: str,
        heating_coil_object_type: Literal[
            "Coil:Heating:WaterToAirHeatPump:EquationFit", "Coil:Heating:WaterToAirHeatPump:VariableSpeedEquationFit"
        ],
        heating_coil_name: str,
        cooling_coil_object_type: Literal[
            "Coil:Cooling:WaterToAirHeatPump:EquationFit", "Coil:Cooling:WaterToAirHeatPump:VariableSpeedEquationFit"
        ],
        cooling_coil_name: str,
        supplemental_heating_coil_object_type: Literal[
            "Coil:Heating:Electric", "Coil:Heating:Fuel", "Coil:Heating:Steam", "Coil:Heating:Water"
        ],
        supplemental_heating_coil_name: str,
        availability_schedule_name: str | None = ...,
        outdoor_air_mixer_object_type: Literal["OutdoorAir:Mixer"] | None = ...,
        outdoor_air_mixer_name: str | None = ...,
        no_load_supply_air_flow_rate: float | Literal["Autosize"] | None = ...,
        no_load_outdoor_air_flow_rate: float | Literal["Autosize"] | None = ...,
        maximum_cycling_rate: float | None = 2.5,
        heat_pump_time_constant: float | None = 60,
        fraction_of_on_cycle_power_use: float | None = 0.01,
        heat_pump_fan_delay_time: float | None = 60,
        maximum_supply_air_temperature_from_supplemental_heater: float | Literal["", "Autosize"] | None = "Autosize",
        maximum_outdoor_dry_bulb_temperature_for_supplemental_heater_operation: float | None = 21,
        outdoor_dry_bulb_temperature_sensor_node_name: str | None = ...,
        fan_placement: Literal["", "BlowThrough", "DrawThrough"] | None = "BlowThrough",
        supply_air_fan_operating_mode_schedule_name: str | None = ...,
        availability_manager_list_name: str | None = ...,
        heat_pump_coil_water_flow_mode: Literal["", "Constant", "ConstantOnDemand", "Cycling"] | None = "Cycling",
        design_specification_zonehvac_sizing_object_name: str | None = ...,
    ) -> None:
        """Create a new ``ZoneHVAC:WaterToAirHeatPump`` and add it to the document.

        Water-to-air heat pump. Forced-convection heating-cooling unit with supply fan, water-to-air cooling and heating coils, supplemental heating coil (gas, electric, hot water, or steam), and fixed-position outdoor air mixer.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v23.1/io-reference/overview/group-zone-forced-air-units/#zonehvacwatertoairheatpump
        """

class HVACTemplateSystemUnitarySystem_v8_9_to_v22_1:
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
        number_of_speeds_for_cooling: float | None = 1,
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
        number_of_speeds_or_stages_for_heating: float | None = 1,
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

        EnergyPlus I/O Reference: https://docs.idfkit.com/v22.1/io-reference/hvac-template-objects/group-hvac-templates/#hvactemplatesystemunitarysystem
        """

class AirLoopHVACUnitaryHeatPumpAirToAirMultiSpeed_v8_9_to_v22_1:
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
        number_of_speeds_for_heating: float,
        number_of_speeds_for_cooling: float,
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

        EnergyPlus I/O Reference: https://docs.idfkit.com/v22.1/io-reference/overview/group-unitary-equipment/#airloophvacunitaryheatpumpairtoairmultispeed
        """

class CoilHeatingFuel_v9_4_to_v23_1:
    def __call__(
        self,
        name: str,
        /,
        *,
        air_inlet_node_name: str,
        air_outlet_node_name: str,
        availability_schedule_name: str | None = ...,
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
        burner_efficiency: float | None = 0.8,
        nominal_capacity: float | Literal["Autosize"] | None = ...,
        temperature_setpoint_node_name: str | None = ...,
        parasitic_electric_load: float | None = ...,
        part_load_fraction_correlation_curve_name: str | None = ...,
        parasitic_fuel_load: float | None = ...,
    ) -> None:
        """Create a new ``Coil:Heating:Fuel`` and add it to the document.

        Gas or other fuel heating coil. If the coil is located directly in an air loop branch or outdoor air equipment list, then it is controlled on leaving air temperature and the Temperature Setpoint Node Name must be specified. If the coil is contained within another component such as an air terminal unit, zone HVAC equipment, or unitary system, then the coil is controlled by the parent component and the setpoint node name is not entered.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v23.1/io-reference/energyplus-economics/cost-estimating/#coilheatingfuel
        """

class ZoneHVACLowTemperatureRadiantConstantFlow_v8_9_to_v9_3:
    def __call__(
        self,
        name: str,
        /,
        *,
        availability_schedule_name: str | None = ...,
        zone_name: str | None = ...,
        surface_name_or_radiant_surface_group_name: str | None = ...,
        hydronic_tubing_inside_diameter: float | None = 0.013,
        hydronic_tubing_length: float | Literal["", "Autosize"] | None = "Autosize",
        temperature_control_type: Literal[
            "",
            "MeanAirTemperature",
            "MeanRadiantTemperature",
            "OperativeTemperature",
            "OutdoorDryBulbTemperature",
            "OutdoorWetBulbTemperature",
        ]
        | None = "MeanAirTemperature",
        rated_flow_rate: float | Literal["Autosize"] | None = ...,
        pump_flow_rate_schedule_name: str | None = ...,
        rated_pump_head: float | None = 179352,
        rated_power_consumption: float | None = ...,
        motor_efficiency: float | None = 0.9,
        fraction_of_motor_inefficiencies_to_fluid_stream: float | None = 0,
        heating_water_inlet_node_name: str | None = ...,
        heating_water_outlet_node_name: str | None = ...,
        heating_high_water_temperature_schedule_name: str | None = ...,
        heating_low_water_temperature_schedule_name: str | None = ...,
        heating_high_control_temperature_schedule_name: str | None = ...,
        heating_low_control_temperature_schedule_name: str | None = ...,
        cooling_water_inlet_node_name: str | None = ...,
        cooling_water_outlet_node_name: str | None = ...,
        cooling_high_water_temperature_schedule_name: str | None = ...,
        cooling_low_water_temperature_schedule_name: str | None = ...,
        cooling_high_control_temperature_schedule_name: str | None = ...,
        cooling_low_control_temperature_schedule_name: str | None = ...,
        condensation_control_type: Literal["", "Off", "SimpleOff", "VariableOff"] | None = "SimpleOff",
        condensation_control_dewpoint_offset: float | None = 1,
        number_of_circuits: Literal["", "CalculateFromCircuitLength", "OnePerSurface"] | None = "OnePerSurface",
        circuit_length: float | None = 106.7,
    ) -> None:
        """Create a new ``ZoneHVAC:LowTemperatureRadiant:ConstantFlow`` and add it to the document.

        Low temperature hydronic radiant heating and/or cooling system embedded in a building surface (wall, ceiling, or floor). Controlled by varying the hot or chilled water temperature circulating through the unit.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v9.3/io-reference/overview/group-radiative-convective-units/#zonehvaclowtemperatureradiantconstantflow
        """

class CurveDoubleExponentialDecay_v8_9_to_v9_3:
    def __call__(
        self,
        name: str,
        /,
        *,
        coefficient1_c1: float,
        coefficient2_c2: float,
        coefficient3_c3: float,
        coefficient3_c4: float,
        coefficient3_c5: float,
        minimum_value_of_x: float,
        maximum_value_of_x: float,
        minimum_curve_output: float | None = ...,
        maximum_curve_output: float | None = ...,
        input_unit_type_for_x: Literal["", "Dimensionless"] | None = "Dimensionless",
        output_unit_type: Literal["", "Capacity", "Dimensionless", "Power", "Pressure", "Temperature"]
        | None = "Dimensionless",
    ) -> None:
        """Create a new ``Curve:DoubleExponentialDecay`` and add it to the document.

        Double exponential decay curve with one independent variable. Input consists of the curve name, the five coefficients, and the maximum and minimum valid independent variable values. Optional inputs for the curve minimum and maximum may be used to limit the output of the performance curve. curve = C1+C2*exp(C3*x)+C4*exp(C5*x)

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v9.3/io-reference/overview/group-performance-curves/#curvedoubleexponentialdecay
        """

class CoilCoolingWaterToAirHeatPumpVariableSpeedEquationFit_v22_2_to_v23_1:
    def __call__(
        self,
        name: str,
        /,
        *,
        water_to_refrigerant_hx_water_inlet_node_name: str,
        water_to_refrigerant_hx_water_outlet_node_name: str,
        indoor_air_inlet_node_name: str,
        indoor_air_outlet_node_name: str,
        energy_part_load_fraction_curve_name: str,
        speed_1_reference_unit_gross_rated_total_cooling_capacity: float,
        speed_1_reference_unit_gross_rated_sensible_heat_ratio: float,
        speed_1_reference_unit_gross_rated_cooling_cop: float,
        speed_1_reference_unit_rated_air_flow_rate: float,
        speed_1_reference_unit_rated_water_flow_rate: float,
        speed_1_total_cooling_capacity_function_of_temperature_curve_name: str,
        speed_1_total_cooling_capacity_function_of_air_flow_fraction_curve_name: str,
        speed_1_total_cooling_capacity_function_of_water_flow_fraction_curve_name: str,
        speed_1_energy_input_ratio_function_of_temperature_curve_name: str,
        speed_1_energy_input_ratio_function_of_air_flow_fraction_curve_name: str,
        speed_1_energy_input_ratio_function_of_water_flow_fraction_curve_name: str,
        speed_1_reference_unit_waste_heat_fraction_of_input_power_at_rated_conditions: float,
        speed_1_waste_heat_function_of_temperature_curve_name: str,
        number_of_speeds: int | None = 2,
        nominal_speed_level: int | None = 2,
        gross_rated_total_cooling_capacity_at_selected_nominal_speed_level: float
        | Literal["", "Autosize"]
        | None = "Autosize",
        rated_air_flow_rate_at_selected_nominal_speed_level: float | Literal["", "Autosize"] | None = "Autosize",
        rated_water_flow_rate_at_selected_nominal_speed_level: float | Literal["", "Autosize"] | None = "Autosize",
        nominal_time_for_condensate_to_begin_leaving_the_coil: float | None = 0,
        initial_moisture_evaporation_rate_divided_by_steady_state_ac_latent_capacity: float | None = 0,
        flag_for_using_hot_gas_reheat_0_or_1: float | None = 0,
        speed_2_reference_unit_gross_rated_total_cooling_capacity: float | None = ...,
        speed_2_reference_unit_gross_rated_sensible_heat_ratio: float | None = ...,
        speed_2_reference_unit_gross_rated_cooling_cop: float | None = ...,
        speed_2_reference_unit_rated_air_flow_rate: float | None = ...,
        speed_2_reference_unit_rated_water_flow_rate: float | None = ...,
        speed_2_total_cooling_capacity_function_of_temperature_curve_name: str | None = ...,
        speed_2_total_cooling_capacity_function_of_air_flow_fraction_curve_name: str | None = ...,
        speed_2_total_cooling_capacity_function_of_water_flow_fraction_curve_name: str | None = ...,
        speed_2_energy_input_ratio_function_of_temperature_curve_name: str | None = ...,
        speed_2_energy_input_ratio_function_of_air_flow_fraction_curve_name: str | None = ...,
        speed_2_energy_input_ratio_function_of_water_flow_fraction_curve_name: str | None = ...,
        speed_2_reference_unit_waste_heat_fraction_of_input_power_at_rated_conditions: float | None = ...,
        speed_2_waste_heat_function_of_temperature_curve_name: str | None = ...,
        speed_3_reference_unit_gross_rated_total_cooling_capacity: float | None = ...,
        speed_3_reference_unit_gross_rated_sensible_heat_ratio: float | None = ...,
        speed_3_reference_unit_gross_rated_cooling_cop: float | None = ...,
        speed_3_reference_unit_rated_air_flow_rate: float | None = ...,
        speed_3_reference_unit_rated_water_flow_rate: float | None = ...,
        speed_3_total_cooling_capacity_function_of_temperature_curve_name: str | None = ...,
        speed_3_total_cooling_capacity_function_of_air_flow_fraction_curve_name: str | None = ...,
        speed_3_total_cooling_capacity_function_of_water_flow_fraction_curve_name: str | None = ...,
        speed_3_energy_input_ratio_function_of_temperature_curve_name: str | None = ...,
        speed_3_energy_input_ratio_function_of_air_flow_fraction_curve_name: str | None = ...,
        speed_3_energy_input_ratio_function_of_water_flow_fraction_curve_name: str | None = ...,
        speed_3_reference_unit_waste_heat_fraction_of_input_power_at_rated_conditions: float | None = ...,
        speed_3_waste_heat_function_of_temperature_curve_name: str | None = ...,
        speed_4_reference_unit_gross_rated_total_cooling_capacity: float | None = ...,
        speed_4_reference_unit_gross_rated_sensible_heat_ratio: float | None = ...,
        speed_4_reference_unit_gross_rated_cooling_cop: float | None = ...,
        speed_4_reference_unit_rated_air_flow_rate: float | None = ...,
        speed_4_reference_unit_rated_water_flow_rate: float | None = ...,
        speed_4_total_cooling_capacity_function_of_temperature_curve_name: str | None = ...,
        speed_4_total_cooling_capacity_function_of_air_flow_fraction_curve_name: str | None = ...,
        speed_4_total_cooling_capacity_function_of_water_flow_fraction_curve_name: str | None = ...,
        speed_4_energy_input_ratio_function_of_temperature_curve_name: str | None = ...,
        speed_4_energy_input_ratio_function_of_air_flow_fraction_curve_name: str | None = ...,
        speed_4_energy_input_ratio_function_of_water_flow_fraction_curve_name: str | None = ...,
        speed_4_reference_unit_waste_heat_fraction_of_input_power_at_rated_conditions: float | None = ...,
        speed_4_waste_heat_function_of_temperature_curve_name: str | None = ...,
        speed_5_reference_unit_gross_rated_total_cooling_capacity: float | None = ...,
        speed_5_reference_unit_gross_rated_sensible_heat_ratio: float | None = ...,
        speed_5_reference_unit_gross_rated_cooling_cop: float | None = ...,
        speed_5_reference_unit_rated_air_flow_rate: float | None = ...,
        speed_5_reference_unit_rated_water_flow_rate: float | None = ...,
        speed_5_total_cooling_capacity_function_of_temperature_curve_name: str | None = ...,
        speed_5_total_cooling_capacity_function_of_air_flow_fraction_curve_name: str | None = ...,
        speed_5_total_cooling_capacity_function_of_water_flow_fraction_curve_name: str | None = ...,
        speed_5_energy_input_ratio_function_of_temperature_curve_name: str | None = ...,
        speed_5_energy_input_ratio_function_of_air_flow_fraction_curve_name: str | None = ...,
        speed_5_energy_input_ratio_function_of_water_flow_fraction_curve_name: str | None = ...,
        speed_5_reference_unit_waste_heat_fraction_of_input_power_at_rated_conditions: float | None = ...,
        speed_5_waste_heat_function_of_temperature_curve_name: str | None = ...,
        speed_6_reference_unit_gross_rated_total_cooling_capacity: float | None = ...,
        speed_6_reference_unit_gross_rated_sensible_heat_ratio: float | None = ...,
        speed_6_reference_unit_gross_rated_cooling_cop: float | None = ...,
        speed_6_reference_unit_rated_air_flow_rate: float | None = ...,
        speed_6_reference_unit_rated_water_flow_rate: float | None = ...,
        speed_6_total_cooling_capacity_function_of_temperature_curve_name: str | None = ...,
        speed_6_total_cooling_capacity_function_of_air_flow_fraction_curve_name: str | None = ...,
        speed_6_total_cooling_capacity_function_of_water_flow_fraction_curve_name: str | None = ...,
        speed_6_energy_input_ratio_function_of_temperature_curve_name: str | None = ...,
        speed_6_energy_input_ratio_function_of_air_flow_fraction_curve_name: str | None = ...,
        speed_6_energy_input_ratio_function_of_water_flow_fraction_curve_name: str | None = ...,
        speed_6_reference_unit_waste_heat_fraction_of_input_power_at_rated_conditions: float | None = ...,
        speed_6_waste_heat_function_of_temperature_curve_name: str | None = ...,
        speed_7_reference_unit_gross_rated_total_cooling_capacity: float | None = ...,
        speed_7_reference_unit_gross_rated_sensible_heat_ratio: float | None = ...,
        speed_7_reference_unit_gross_rated_cooling_cop: float | None = ...,
        speed_7_reference_unit_rated_air_flow_rate: float | None = ...,
        speed_7_reference_unit_rated_water_flow_rate: float | None = ...,
        speed_7_total_cooling_capacity_function_of_temperature_curve_name: str | None = ...,
        speed_7_total_cooling_capacity_function_of_air_flow_fraction_curve_name: str | None = ...,
        speed_7_total_cooling_capacity_function_of_water_flow_fraction_curve_name: str | None = ...,
        speed_7_energy_input_ratio_function_of_temperature_curve_name: str | None = ...,
        speed_7_energy_input_ratio_function_of_air_flow_fraction_curve_name: str | None = ...,
        speed_7_energy_input_ratio_function_of_water_flow_fraction_curve_name: str | None = ...,
        speed_7_reference_unit_waste_heat_fraction_of_input_power_at_rated_conditions: float | None = ...,
        speed_7_waste_heat_function_of_temperature_curve_name: str | None = ...,
        speed_8_reference_unit_gross_rated_total_cooling_capacity: float | None = ...,
        speed_8_reference_unit_gross_rated_sensible_heat_ratio: float | None = ...,
        speed_8_reference_unit_gross_rated_cooling_cop: float | None = ...,
        speed_8_reference_unit_rated_air_flow_rate: float | None = ...,
        speed_8_reference_unit_rated_water_flow_rate: float | None = ...,
        speed_8_total_cooling_capacity_function_of_temperature_curve_name: str | None = ...,
        speed_8_total_cooling_capacity_function_of_air_flow_fraction_curve_name: str | None = ...,
        speed_8_total_cooling_capacity_function_of_water_flow_fraction_curve_name: str | None = ...,
        speed_8_energy_input_ratio_function_of_temperature_curve_name: str | None = ...,
        speed_8_energy_input_ratio_function_of_air_flow_fraction_curve_name: str | None = ...,
        speed_8_energy_input_ratio_function_of_water_flow_fraction_curve_name: str | None = ...,
        speed_8_reference_unit_waste_heat_fraction_of_input_power_at_rated_conditions: float | None = ...,
        speed_8_waste_heat_function_of_temperature_curve_name: str | None = ...,
        speed_9_reference_unit_gross_rated_total_cooling_capacity: float | None = ...,
        speed_9_reference_unit_gross_rated_sensible_heat_ratio: float | None = ...,
        speed_9_reference_unit_gross_rated_cooling_cop: float | None = ...,
        speed_9_reference_unit_rated_air_flow_rate: float | None = ...,
        speed_9_reference_unit_rated_water_flow_rate: float | None = ...,
        speed_9_total_cooling_capacity_function_of_temperature_curve_name: str | None = ...,
        speed_9_total_cooling_capacity_function_of_air_flow_fraction_curve_name: str | None = ...,
        speed_9_total_cooling_capacity_function_of_water_flow_fraction_curve_name: str | None = ...,
        speed_9_energy_input_ratio_function_of_temperature_curve_name: str | None = ...,
        speed_9_energy_input_ratio_function_of_air_flow_fraction_curve_name: str | None = ...,
        speed_9_energy_input_ratio_function_of_water_flow_fraction_curve_name: str | None = ...,
        speed_9_reference_unit_waste_heat_fraction_of_input_power_at_rated_conditions: float | None = ...,
        speed_9_waste_heat_function_of_temperature_curve_name: str | None = ...,
        speed_10_reference_unit_gross_rated_total_cooling_capacity: float | None = ...,
        speed_10_reference_unit_gross_rated_sensible_heat_ratio: float | None = ...,
        speed_10_reference_unit_gross_rated_cooling_cop: float | None = ...,
        speed_10_reference_unit_rated_air_flow_rate: float | None = ...,
        speed_10_reference_unit_rated_water_flow_rate: float | None = ...,
        speed_10_total_cooling_capacity_function_of_temperature_curve_name: str | None = ...,
        speed_10_total_cooling_capacity_function_of_air_flow_fraction_curve_name: str | None = ...,
        speed_10_total_cooling_capacity_function_of_water_flow_fraction_curve_name: str | None = ...,
        speed_10_energy_input_ratio_function_of_temperature_curve_name: str | None = ...,
        speed_10_energy_input_ratio_function_of_air_flow_fraction_curve_name: str | None = ...,
        speed_10_energy_input_ratio_function_of_water_flow_fraction_curve_name: str | None = ...,
        speed_10_reference_unit_waste_heat_fraction_of_input_power_at_rated_conditions: float | None = ...,
        speed_10_waste_heat_function_of_temperature_curve_name: str | None = ...,
    ) -> None:
        """Create a new ``Coil:Cooling:WaterToAirHeatPump:VariableSpeedEquationFit`` and add it to the document.

        Direct expansion (DX) cooling coil for water-to-air heat pump (includes electric compressor), variable-speed, equation-fit model. Optional inputs for moisture evaporation from wet coil when compressor cycles off with continuous fan operation. Equation-fit model uses normalized curves to describe the heat pump performance. Requires two to ten sets of performance data and will interpolate between speeds. Modeled as a single coil with variable-speed compressor.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v23.1/io-reference/overview/group-heating-and-cooling-coils/#coilcoolingwatertoairheatpumpvariablespeedequationfit
        """

class OutputControlFiles_v24_2_to_v25_1:
    def __call__(
        self,
        /,
        *,
        output_csv: Literal["", "No", "Yes"] | None = "No",
        output_mtr: Literal["", "No", "Yes"] | None = "Yes",
        output_eso: Literal["", "No", "Yes"] | None = "Yes",
        output_eio: Literal["", "No", "Yes"] | None = "Yes",
        output_tabular: Literal["", "No", "Yes"] | None = "Yes",
        output_sqlite: Literal["", "No", "Yes"] | None = "Yes",
        output_json: Literal["", "No", "Yes"] | None = "Yes",
        output_audit: Literal["", "No", "Yes"] | None = "Yes",
        output_space_sizing: Literal["", "No", "Yes"] | None = "Yes",
        output_zone_sizing: Literal["", "No", "Yes"] | None = "Yes",
        output_system_sizing: Literal["", "No", "Yes"] | None = "Yes",
        output_dxf: Literal["", "No", "Yes"] | None = "Yes",
        output_bnd: Literal["", "No", "Yes"] | None = "Yes",
        output_rdd: Literal["", "No", "Yes"] | None = "Yes",
        output_mdd: Literal["", "No", "Yes"] | None = "Yes",
        output_mtd: Literal["", "No", "Yes"] | None = "Yes",
        output_end: Literal["", "No", "Yes"] | None = "Yes",
        output_shd: Literal["", "No", "Yes"] | None = "Yes",
        output_dfs: Literal["", "No", "Yes"] | None = "Yes",
        output_glhe: Literal["", "No", "Yes"] | None = "Yes",
        output_delightin: Literal["", "No", "Yes"] | None = "Yes",
        output_delighteldmp: Literal["", "No", "Yes"] | None = "Yes",
        output_delightdfdmp: Literal["", "No", "Yes"] | None = "Yes",
        output_edd: Literal["", "No", "Yes"] | None = "Yes",
        output_dbg: Literal["", "No", "Yes"] | None = "Yes",
        output_perflog: Literal["", "No", "Yes"] | None = "Yes",
        output_sln: Literal["", "No", "Yes"] | None = "Yes",
        output_sci: Literal["", "No", "Yes"] | None = "Yes",
        output_wrl: Literal["", "No", "Yes"] | None = "Yes",
        output_screen: Literal["", "No", "Yes"] | None = "Yes",
        output_extshd: Literal["", "No", "Yes"] | None = "Yes",
        output_tarcog: Literal["", "No", "Yes"] | None = "Yes",
    ) -> None:
        """Create a new ``OutputControl:Files`` and add it to the document.

        Conditionally turn on/off output from EnergyPlus.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v25.1/io-reference/input-for-output/#outputcontrolfiles
        """

class IndoorLivingWall_v24_1:
    def __call__(
        self,
        name: str,
        /,
        *,
        surface_name: str,
        schedule_name: str,
        evapotranspiration_calculation_method: Literal["", "Penman-Monteith", "Stanghellini"]
        | None = "Penman-Monteith",
        lighting_method: Literal["Daylight", "LED", "LED-Daylight"] | None = ...,
        led_intensity_schedule_name_: str | None = ...,
        daylighting_control_name: str | None = ...,
        led_daylight_targeted_lighting_intensity_schedule_name: str | None = ...,
        total_leaf_area: float | None = ...,
        led_nominal_intensity_: float | None = ...,
        led_nominal_power: float | None = ...,
        radiant_fraction_of_led_lights: float | None = 0.6,
        led_intensity_schedule_name: str | None = ...,
        led_nominal_intensity: float | None = ...,
    ) -> None:
        """Create a new ``IndoorLivingWall`` and add it to the document.

        Indoor greenery systems such as indoor living walls are panels of plants, which grow hydroponically or from substrates. The living wall structures can be either free-standing or attached to walls. The IndoorLivingWall module directly connects with inside surface heat balance, zone air heat balance, and zone air moisture balance.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v24.1/io-reference/overview/group-internal-gains-people-lights-other/#indoorlivingwall
        """

class PhotovoltaicPerformanceEquivalentOneDiode_v22_2_to_v25_2:
    def __call__(
        self,
        name: str = "",
        /,
        *,
        cell_type: Literal["AmorphousSilicon", "CrystallineSilicon"] | None = ...,
        number_of_cells_in_series: int | None = 36,
        active_area: float | None = 0.89,
        transmittance_absorptance_product: float | None = 0.95,
        semiconductor_bandgap: float | None = 1.12,
        shunt_resistance: float | None = 1000000,
        short_circuit_current: float | None = 6.5,
        open_circuit_voltage: float | None = 21.6,
        reference_temperature: float | None = 25,
        reference_insolation: float | None = 1000,
        module_current_at_maximum_power: float | None = 5.9,
        module_voltage_at_maximum_power: float | None = 17,
        temperature_coefficient_of_short_circuit_current: float | None = 0.02,
        temperature_coefficient_of_open_circuit_voltage: float | None = -0.079,
        nominal_operating_cell_temperature_test_ambient_temperature: float | None = 20,
        nominal_operating_cell_temperature_test_cell_temperature: float | None = 40,
        nominal_operating_cell_temperature_test_insolation: float | None = 800,
        module_heat_loss_coefficient: float | None = 30,
        total_heat_capacity: float | None = 50000,
    ) -> None:
        """Create a new ``PhotovoltaicPerformance:EquivalentOne-Diode`` and add it to the document.

        Describes the performance characteristics of Photovoltaic (PV) modules to be modeled using an equivalent one-diode circuit. This model is also known as the 4- or 5-parameter TRNSYS model for photovoltaics.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v25.2/io-reference/overview/group-electric-load-center-generator/#photovoltaicperformanceequivalentone-diode
        """

class ZoneHVACHighTemperatureRadiant_v8_9_to_v25_1:
    def __call__(
        self,
        name: str,
        /,
        *,
        zone_name: str,
        fuel_type: Literal["Electricity", "NaturalGas"],
        availability_schedule_name: str | None = ...,
        heating_design_capacity_method: Literal[
            "", "CapacityPerFloorArea", "FractionOfAutosizedHeatingCapacity", "HeatingDesignCapacity"
        ]
        | None = "HeatingDesignCapacity",
        heating_design_capacity: float | Literal["", "Autosize"] | None = "Autosize",
        heating_design_capacity_per_floor_area: float | None = ...,
        fraction_of_autosized_heating_design_capacity: float | None = 1,
        combustion_efficiency: float | None = 0.9,
        fraction_of_input_converted_to_radiant_energy: float | None = 0.7,
        fraction_of_input_converted_to_latent_energy: float | None = 0,
        fraction_of_input_that_is_lost: float | None = 0,
        temperature_control_type: Literal[
            "",
            "MeanAirTemperature",
            "MeanAirTemperatureSetpoint",
            "MeanRadiantTemperature",
            "MeanRadiantTemperatureSetpoint",
            "OperativeTemperature",
            "OperativeTemperatureSetpoint",
        ]
        | None = "OperativeTemperature",
        heating_throttling_range: float | None = 2,
        heating_setpoint_temperature_schedule_name: str | None = ...,
        fraction_of_radiant_energy_incident_on_people: float | None = ...,
        surface_fractions: list[_g.ZoneHVACHighTemperatureRadiantSurfaceFractionsItem] = ...,
    ) -> None:
        """Create a new ``ZoneHVAC:HighTemperatureRadiant`` and add it to the document.

        The number of surfaces can be expanded beyond 100, if necessary, by adding more groups to the end of the list

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v25.1/io-reference/overview/group-radiative-convective-units/#zonehvachightemperatureradiant
        """
