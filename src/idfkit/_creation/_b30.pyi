"""Creation signatures of generated classes (stub only).

DO NOT EDIT — regenerate with:
    python -m idfkit.codegen.generate_stubs
"""

from __future__ import annotations

from collections.abc import Sequence
from typing import Literal

from .. import _generated_types as _g

class ScheduleWeekRule:
    def __call__(
        self,
        name: str,
        /,
        *,
        schedule_year_rules_name: str,
        rule_priority_order: int,
        day_schedule_name: str,
        apply_sunday: Literal["No", "Yes"] | None = "No",
        apply_monday: Literal["No", "Yes"] | None = "No",
        apply_tuesday: Literal["No", "Yes"] | None = "No",
        apply_wednesday: Literal["No", "Yes"] | None = "No",
        apply_thursday: Literal["No", "Yes"] | None = "No",
        apply_friday: Literal["No", "Yes"] | None = "No",
        apply_saturday: Literal["No", "Yes"] | None = "No",
        date_ranges: Sequence[_g.ScheduleWeekRuleDateRangesItem | _g.ScheduleWeekRuleDateRangesGroup] = ...,
        validate: bool = True,
    ) -> None:
        """Create a new ``Schedule:Week:Rule`` and add it to the document.

        A Schedule:Week:Rule defines one override rule for a Schedule:Year:Rules. Rules are evaluated in ascending Rule Priority Order; the first matching rule wins. A rule matches a day if: (a) the day falls within the specified date ranges, AND (b) the corresponding Apply <DayOfWeek> field is Yes.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-schedules/#scheduleweekrule
        """

class AnyConstructionAirBoundary:
    def __call__(
        self,
        name: str,
        /,
        *,
        air_exchange_method: Literal["None", "SimpleMixing"] | None = "None",
        simple_mixing_air_changes_per_hour: float | None = 0.5,
        simple_mixing_schedule_name: str | None = ...,
        validate: bool = True,
    ) -> None:
        """Create a new ``Construction:AirBoundary`` and add it to the document.

        Indicates an open boundary between two zones. It may be used for base surfaces and fenestration surfaces. The two adjacent zones are grouped together for solar, daylighting and radiant exchange. When this construction type is used, the Outside Boundary Condition of the surface (or the base surface of a fenestration surface) must be either Surface or Zone. A base surface with Construction:AirBoundary cannot hold any fenestration surfaces.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-surface-construction-elements/#constructionairboundary
        """

class HumidifierSteamElectric:
    def __call__(
        self,
        name: str,
        /,
        *,
        availability_schedule_name: str | None = ...,
        rated_capacity: float | Literal["Autosize"] | None = ...,
        rated_power: float | Literal["Autosize"] | None = ...,
        rated_fan_power: float | None = ...,
        standby_power: float | None = ...,
        air_inlet_node_name: str | None = ...,
        air_outlet_node_name: str | None = ...,
        water_storage_tank_name: str | None = ...,
        validate: bool = True,
    ) -> None:
        """Create a new ``Humidifier:Steam:Electric`` and add it to the document.

        Electrically heated steam humidifier with fan.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-humidifiers-and-dehumidifiers/#humidifiersteamelectric
        """

class HeatExchangerDesiccantBalancedFlowPerformanceDataType1:
    def __call__(
        self,
        name: str,
        /,
        *,
        nominal_air_face_velocity: float | Literal["Autosize"],
        temperature_equation_coefficient_1: float,
        temperature_equation_coefficient_2: float,
        temperature_equation_coefficient_3: float,
        temperature_equation_coefficient_4: float,
        temperature_equation_coefficient_5: float,
        temperature_equation_coefficient_6: float,
        temperature_equation_coefficient_7: float,
        temperature_equation_coefficient_8: float,
        minimum_regeneration_inlet_air_humidity_ratio_for_temperature_equation: float,
        maximum_regeneration_inlet_air_humidity_ratio_for_temperature_equation: float,
        minimum_regeneration_inlet_air_temperature_for_temperature_equation: float,
        maximum_regeneration_inlet_air_temperature_for_temperature_equation: float,
        minimum_process_inlet_air_humidity_ratio_for_temperature_equation: float,
        maximum_process_inlet_air_humidity_ratio_for_temperature_equation: float,
        minimum_process_inlet_air_temperature_for_temperature_equation: float,
        maximum_process_inlet_air_temperature_for_temperature_equation: float,
        minimum_regeneration_air_velocity_for_temperature_equation: float,
        maximum_regeneration_air_velocity_for_temperature_equation: float,
        minimum_regeneration_outlet_air_temperature_for_temperature_equation: float,
        maximum_regeneration_outlet_air_temperature_for_temperature_equation: float,
        minimum_regeneration_inlet_air_relative_humidity_for_temperature_equation: float,
        maximum_regeneration_inlet_air_relative_humidity_for_temperature_equation: float,
        minimum_process_inlet_air_relative_humidity_for_temperature_equation: float,
        maximum_process_inlet_air_relative_humidity_for_temperature_equation: float,
        humidity_ratio_equation_coefficient_1: float,
        humidity_ratio_equation_coefficient_2: float,
        humidity_ratio_equation_coefficient_3: float,
        humidity_ratio_equation_coefficient_4: float,
        humidity_ratio_equation_coefficient_5: float,
        humidity_ratio_equation_coefficient_6: float,
        humidity_ratio_equation_coefficient_7: float,
        humidity_ratio_equation_coefficient_8: float,
        minimum_regeneration_inlet_air_humidity_ratio_for_humidity_ratio_equation: float,
        maximum_regeneration_inlet_air_humidity_ratio_for_humidity_ratio_equation: float,
        minimum_regeneration_inlet_air_temperature_for_humidity_ratio_equation: float,
        maximum_regeneration_inlet_air_temperature_for_humidity_ratio_equation: float,
        minimum_process_inlet_air_humidity_ratio_for_humidity_ratio_equation: float,
        maximum_process_inlet_air_humidity_ratio_for_humidity_ratio_equation: float,
        minimum_process_inlet_air_temperature_for_humidity_ratio_equation: float,
        maximum_process_inlet_air_temperature_for_humidity_ratio_equation: float,
        minimum_regeneration_air_velocity_for_humidity_ratio_equation: float,
        maximum_regeneration_air_velocity_for_humidity_ratio_equation: float,
        minimum_regeneration_outlet_air_humidity_ratio_for_humidity_ratio_equation: float,
        maximum_regeneration_outlet_air_humidity_ratio_for_humidity_ratio_equation: float,
        minimum_regeneration_inlet_air_relative_humidity_for_humidity_ratio_equation: float,
        maximum_regeneration_inlet_air_relative_humidity_for_humidity_ratio_equation: float,
        minimum_process_inlet_air_relative_humidity_for_humidity_ratio_equation: float,
        maximum_process_inlet_air_relative_humidity_for_humidity_ratio_equation: float,
        nominal_air_flow_rate: float | Literal["Autosize"] | None = ...,
        nominal_electric_power: float | None = 0,
        validate: bool = True,
    ) -> None:
        """Create a new ``HeatExchanger:Desiccant:BalancedFlow:PerformanceDataType1`` and add it to the document.

        RTO = B1 + B2*RWI + B3*RTI + B4*(RWI/RTI) + B5*PWI + B6*PTI + B7*(PWI/PTI) + B8*RFV RWO = C1 + C2*RWI + C3*RTI + C4*(RWI/RTI) + C5*PWI + C6*PTI + C7*(PWI/PTI) + C8*RFV where, RTO = Dry-bulb temperature of the regeneration outlet air (C) RWO = Humidity ratio of the regeneration outlet air (kgWater/kgDryAir) RWI = Humidity ratio of the regeneration inlet air (kgWater/kgDryAir) RTI = Dry-bulb temperature of the regeneration inlet air (C) PWI = Humidity ratio of the process inlet air (kgWater/kgDryAir) PTI = Dry-bulb temperature of the process inlet air (C) RFV = Regeneration Face Velocity (m/s)

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-heat-recovery/#heatexchangerdesiccantbalancedflowperformancedatatype1
        """

class HeatPumpPlantLoopEIRHeating:
    def __call__(
        self,
        name: str,
        /,
        *,
        load_side_inlet_node_name: str,
        load_side_outlet_node_name: str,
        source_side_inlet_node_name: str,
        source_side_outlet_node_name: str,
        capacity_modifier_function_of_temperature_curve_name: str,
        electric_input_to_output_ratio_modifier_function_of_temperature_curve_name: str,
        electric_input_to_output_ratio_modifier_function_of_part_load_ratio_curve_name: str,
        condenser_type: Literal["AirSource", "WaterSource"] | None = "WaterSource",
        heat_recovery_inlet_node_name: str | None = ...,
        heat_recovery_outlet_node_name: str | None = ...,
        companion_heat_pump_name: str | None = ...,
        load_side_reference_flow_rate: float | Literal["Autosize"] | None = "Autosize",
        source_side_reference_flow_rate: float | Literal["Autosize"] | None = "Autosize",
        heat_recovery_reference_flow_rate: float | Literal["Autosize"] | None = "Autosize",
        reference_capacity: float | Literal["Autosize"] | None = "Autosize",
        reference_coefficient_of_performance: float | None = 3,
        sizing_factor: float | None = 1,
        heating_to_cooling_capacity_sizing_ratio: float | None = 1,
        heat_pump_sizing_method: Literal["CoolingCapacity", "GreaterOfHeatingOrCooling", "HeatingCapacity"]
        | None = "CoolingCapacity",
        control_type: Literal["Load", "Setpoint"] | None = "Load",
        flow_mode: Literal["ConstantFlow", "VariableSpeedPumping"] | None = "ConstantFlow",
        minimum_part_load_ratio: float | None = 0,
        minimum_source_inlet_temperature: float | None = -100,
        maximum_source_inlet_temperature: float | None = 100,
        minimum_supply_water_temperature_curve_name: str | None = ...,
        maximum_supply_water_temperature_curve_name: str | None = ...,
        dry_outdoor_correction_factor_curve_name: str | None = ...,
        maximum_outdoor_dry_bulb_temperature_for_defrost_operation: float | None = 10,
        heat_pump_defrost_control: Literal["None", "OnDemand", "Timed", "TimedEmpirical"] | None = ...,
        heat_pump_defrost_time_period_fraction: float | None = 0.058333,
        defrost_energy_input_ratio_function_of_temperature_curve_name: str | None = ...,
        timed_empirical_defrost_frequency_curve_name: str | None = ...,
        timed_empirical_defrost_heat_load_penalty_curve_name: str | None = ...,
        timed_empirical_defrost_heat_input_energy_fraction_curve_name: str | None = ...,
        minimum_heat_recovery_outlet_temperature: float | None = 4.5,
        heat_recovery_capacity_modifier_function_of_temperature_curve_name: str | None = ...,
        heat_recovery_electric_input_to_output_ratio_modifier_function_of_temperature_curve_name: str | None = ...,
        validate: bool = True,
    ) -> None:
        """Create a new ``HeatPump:PlantLoop:EIR:Heating`` and add it to the document.

        An EIR formulated water to water heat pump model, heating operation

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-plant-equipment/#heatpumpplantloopeirheating
        """

class GroundHeatExchangerResponseFactors:
    def __call__(
        self,
        name: str,
        /,
        *,
        ghe_vertical_properties_object_name: str,
        number_of_boreholes: int,
        g_function_reference_ratio: float | None = 0.0005,
        g_functions: Sequence[
            _g.GroundHeatExchangerResponseFactorsGFunctionsItem | _g.GroundHeatExchangerResponseFactorsGFunctionsGroup
        ] = ...,
        validate: bool = True,
    ) -> None:
        """Create a new ``GroundHeatExchanger:ResponseFactors`` and add it to the document.

        Response factor definitions from third-party tool, commonly referred to a 'g-functions'

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-condenser-equipment/#groundheatexchangerresponsefactors
        """

class PhotovoltaicPerformanceSandia:
    def __call__(
        self,
        name: str,
        /,
        *,
        active_area: float | None = 1,
        number_of_cells_in_series: int | None = 1,
        number_of_cells_in_parallel: int | None = 1,
        short_circuit_current: float | None = ...,
        open_circuit_voltage: float | None = ...,
        current_at_maximum_power_point: float | None = ...,
        voltage_at_maximum_power_point: float | None = ...,
        sandia_database_parameter_aisc: float | None = ...,
        sandia_database_parameter_aimp: float | None = ...,
        sandia_database_parameter_c0: float | None = ...,
        sandia_database_parameter_c1: float | None = ...,
        sandia_database_parameter_bvoc0: float | None = ...,
        sandia_database_parameter_mbvoc: float | None = ...,
        sandia_database_parameter_bvmp0: float | None = ...,
        sandia_database_parameter_mbvmp: float | None = ...,
        diode_factor: float | None = ...,
        sandia_database_parameter_c2: float | None = ...,
        sandia_database_parameter_c3: float | None = ...,
        sandia_database_parameter_a0: float | None = ...,
        sandia_database_parameter_a1: float | None = ...,
        sandia_database_parameter_a2: float | None = ...,
        sandia_database_parameter_a3: float | None = ...,
        sandia_database_parameter_a4: float | None = ...,
        sandia_database_parameter_b0: float | None = ...,
        sandia_database_parameter_b1: float | None = ...,
        sandia_database_parameter_b2: float | None = ...,
        sandia_database_parameter_b3: float | None = ...,
        sandia_database_parameter_b4: float | None = ...,
        sandia_database_parameter_b5: float | None = ...,
        sandia_database_parameter_delta_tc_: float | None = ...,
        sandia_database_parameter_fd: float | None = ...,
        sandia_database_parameter_a: float | None = ...,
        sandia_database_parameter_b: float | None = ...,
        sandia_database_parameter_c4: float | None = ...,
        sandia_database_parameter_c5: float | None = ...,
        sandia_database_parameter_ix0: float | None = ...,
        sandia_database_parameter_ixx0: float | None = ...,
        sandia_database_parameter_c6: float | None = ...,
        sandia_database_parameter_c7: float | None = ...,
        validate: bool = True,
    ) -> None:
        """Create a new ``PhotovoltaicPerformance:Sandia`` and add it to the document.

        Describes performance input data needed for specific makes and models of production PV panels using the empirical coefficients assembled by Sandia National Laboratory.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-electric-load-center-generator/#photovoltaicperformancesandia
        """
