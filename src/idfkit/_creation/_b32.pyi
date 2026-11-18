"""Creation signatures of generated classes (stub only).

DO NOT EDIT — regenerate with:
    python -m idfkit.codegen.generate_stubs
"""

from __future__ import annotations

from typing import Literal

from .. import _generated_types as _g

class RoomAirTemperaturePatternConstantGradient:
    def __call__(
        self,
        this_type_has_no_name_field: _g._PassFieldsAsKeywords = ...,
        /,
        *,
        room_air_temperature_pattern_constant_gradient_name: str,
        control_integer_for_pattern_control_schedule_name: int,
        thermostat_offset: float | None = ...,
        return_air_offset: float | None = ...,
        exhaust_air_offset: float | None = ...,
        temperature_gradient: float | None = ...,
    ) -> None:
        """Create a new ``RoomAir:TemperaturePattern:ConstantGradient`` and add it to the document.

        Used to model room air with a fixed temperature gradient in the vertical direction. Used in combination with RoomAir:TemperaturePattern:UserDefined.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-room-air-models/#roomairtemperaturepatternconstantgradient
        """

class AirflowNetworkDistributionComponentReliefAirFlow:
    def __call__(
        self,
        name: str,
        /,
        *,
        outdoor_air_mixer_name: str,
        air_mass_flow_coefficient_when_no_outdoor_air_flow_at_reference_conditions: float,
        air_mass_flow_exponent_when_no_outdoor_air_flow: float | None = 0.65,
        reference_crack_conditions: str | None = ...,
    ) -> None:
        """Create a new ``AirflowNetwork:Distribution:Component:ReliefAirFlow`` and add it to the document.

        This object allows variation of air flow rate to perform pressure.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-airflow-network/#airflownetworkdistributioncomponentreliefairflow
        """

class HVACTemplateZoneVAVFanPowered:
    def __call__(
        self,
        this_type_has_no_name_field: _g._PassFieldsAsKeywords = ...,
        /,
        *,
        zone_name: str,
        template_vav_system_name: str,
        template_thermostat_name: str | None = ...,
        primary_supply_air_maximum_flow_rate: float | Literal["Autosize"] | None = "Autosize",
        zone_heating_sizing_factor: float | None = ...,
        zone_cooling_sizing_factor: float | None = ...,
        primary_supply_air_minimum_flow_fraction: float | Literal["Autosize"] | None = "Autosize",
        secondary_supply_air_maximum_flow_rate: float | Literal["Autosize"] | None = "Autosize",
        flow_type: Literal["Parallel", "ParallelFromPlenum", "Series", "SeriesFromPlenum"] | None = "Parallel",
        parallel_fan_on_flow_fraction: float | Literal["Autosize"] | None = "Autosize",
        outdoor_air_method: Literal["DetailedSpecification", "Flow/Area", "Flow/Person", "Flow/Zone", "Maximum", "Sum"]
        | None = "Flow/Person",
        outdoor_air_flow_rate_per_person: float | None = 0.00944,
        outdoor_air_flow_rate_per_zone_floor_area: float | None = 0,
        outdoor_air_flow_rate_per_zone: float | None = 0,
        reheat_coil_type: Literal["Electric", "Gas", "HotWater"] | None = "Electric",
        reheat_coil_availability_schedule_name: str | None = ...,
        fan_total_efficiency: float | None = 0.7,
        fan_delta_pressure: float | None = 1000,
        fan_motor_efficiency: float | None = 0.9,
        supply_plenum_name: str | None = ...,
        return_plenum_name: str | None = ...,
        baseboard_heating_type: Literal["Electric", "HotWater", "None"] | None = "None",
        baseboard_heating_availability_schedule_name: str | None = ...,
        baseboard_heating_capacity: float | Literal["Autosize"] | None = "Autosize",
        zone_cooling_design_supply_air_temperature_input_method: Literal[
            "SupplyAirTemperature", "SystemSupplyAirTemperature", "TemperatureDifference"
        ]
        | None = "SystemSupplyAirTemperature",
        zone_cooling_design_supply_air_temperature: float | None = 12.8,
        zone_cooling_design_supply_air_temperature_difference: float | None = 11.11,
        zone_heating_design_supply_air_temperature_input_method: Literal[
            "SupplyAirTemperature", "TemperatureDifference"
        ]
        | None = "SupplyAirTemperature",
        zone_heating_design_supply_air_temperature: float | None = 50,
        zone_heating_design_supply_air_temperature_difference: float | None = 30,
        zone_piu_fan_schedule_name: str | None = ...,
        design_specification_outdoor_air_object_name: str | None = ...,
        design_specification_zone_air_distribution_object_name: str | None = ...,
    ) -> None:
        """Create a new ``HVACTemplate:Zone:VAV:FanPowered`` and add it to the document.

        Zone terminal unit, fan powered variable volume, reheat optional. Referenced schedules must be defined elsewhere in the idf.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/hvac-template-objects/group-hvac-templates/#hvactemplatezonevavfanpowered
        """

class AnyHeaderedPumpsConstantSpeed:
    def __call__(
        self,
        name: str,
        /,
        *,
        inlet_node_name: str,
        outlet_node_name: str,
        total_design_flow_rate: float | Literal["Autosize"] | None = ...,
        number_of_pumps_in_bank: int | None = ...,
        flow_sequencing_control_scheme: Literal["Sequential"] | None = "Sequential",
        design_pump_head: float | None = 179352,
        design_power_consumption: float | Literal["Autosize"] | None = ...,
        motor_efficiency: float | None = 0.9,
        fraction_of_motor_inefficiencies_to_fluid_stream: float | None = 0,
        pump_control_type: Literal["Continuous", "Intermittent"] | None = "Continuous",
        pump_flow_rate_schedule_name: str | None = ...,
        zone_name: str | None = ...,
        skin_loss_radiative_fraction: float | None = ...,
        design_power_sizing_method: Literal["PowerPerFlow", "PowerPerFlowPerPressure"]
        | None = "PowerPerFlowPerPressure",
        design_electric_power_per_unit_flow_rate: float | None = 348701.1,
        design_shaft_power_per_unit_flow_rate_per_unit_head: float | None = 1.282051282,
    ) -> None:
        """Create a new ``HeaderedPumps:ConstantSpeed`` and add it to the document.

        This Headered pump object describes a pump bank with more than 1 pump in parallel

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-pumps/#headeredpumpsconstantspeed
        """

class HeaderedPumpsConstantSpeed:
    def __call__(
        self,
        name: str,
        /,
        *,
        inlet_node_name: str,
        outlet_node_name: str,
        total_design_flow_rate: float | Literal["Autosize"] | None = ...,
        number_of_pumps_in_bank: int | None = ...,
        flow_sequencing_control_scheme: Literal["Sequential"] | None = "Sequential",
        design_pump_head: float | None = 179352,
        design_power_consumption: float | Literal["Autosize"] | None = ...,
        motor_efficiency: float | None = 0.9,
        fraction_of_motor_inefficiencies_to_fluid_stream: float | None = 0,
        pump_control_type: Literal["Continuous", "Intermittent"] | None = "Continuous",
        pump_flow_rate_schedule_name: str | None = ...,
        zone_name: str | None = ...,
        skin_loss_radiative_fraction: float | None = ...,
        design_power_sizing_method: Literal["PowerPerFlow", "PowerPerFlowPerPressure"]
        | None = "PowerPerFlowPerPressure",
        design_electric_power_per_unit_flow_rate: float | None = 348701.1,
        design_shaft_power_per_unit_flow_rate_per_unit_head: float | None = 1.282051282,
        end_use_subcategory: str | None = "General",
    ) -> None:
        """Create a new ``HeaderedPumps:ConstantSpeed`` and add it to the document.

        This Headered pump object describes a pump bank with more than 1 pump in parallel

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-pumps/#headeredpumpsconstantspeed
        """

class AnyChillerCombustionTurbine:
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
        fuel_type: Literal["Diesel", "Gasoline", "NaturalGas", "OtherFuel1", "OtherFuel2"] | None = "NaturalGas",
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
