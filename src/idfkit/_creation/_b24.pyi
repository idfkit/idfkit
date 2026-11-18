"""Creation signatures of generated classes (stub only).

DO NOT EDIT — regenerate with:
    python -m idfkit.codegen.generate_stubs
"""

from __future__ import annotations

from collections.abc import Sequence
from typing import Literal

from typing_extensions import Never

from .. import _generated_types as _g

class RunPeriodControlSpecialDays:
    def __call__(
        self,
        name: str,
        /,
        *,
        start_date: str,
        duration: float | None = 1,
        special_day_type: Literal["", "CustomDay1", "CustomDay2", "Holiday", "SummerDesignDay", "WinterDesignDay"]
        | None = "Holiday",
    ) -> None:
        """Create a new ``RunPeriodControl:SpecialDays`` and add it to the document.

        This object sets up holidays/special days to be used during weather file run periods. (These are not used with SizingPeriod:* objects.) Depending on the value in the run period, days on the weather file may also be used. However, the weather file specification will take precedence over any specification shown here. (No error message on duplicate days or overlapping days).

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-location-climate-weather-file-access/#runperiodcontrolspecialdays
        """

class AnyMaterialPropertyPhaseChange:
    def __call__(
        self,
        name: str,
        /,
        *,
        narrow_with_as_version_first: Never,
        temperature_coefficient_for_thermal_conductivity: float | None = 0,
    ) -> None:
        """Create a new ``MaterialProperty:PhaseChange`` and add it to the document.

        Additional properties for temperature dependent thermal conductivity and enthalpy for Phase Change Materials (PCM) Name and temperature coefficient are followed by up to 100 sets of temperature-enthalpy pairs. HeatBalanceAlgorithm = CondFD(ConductionFiniteDifference) solution algorithm only. Constructions with this should use the detailed CondFD process. Has no effect with other HeatBalanceAlgorithm solution algorithms

        No call suits every release: narrow the document with ``as_version`` first.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-surface-construction-elements/#materialpropertyphasechange
        """

class SurfacePropertySurroundingSurfaces:
    def __call__(
        self,
        name: str,
        /,
        *,
        sky_view_factor: float | Literal["", "Autocalculate"] | None = "Autocalculate",
        sky_temperature_schedule_name: str | None = ...,
        ground_view_factor: float | Literal["", "Autocalculate"] | None = "Autocalculate",
        ground_temperature_schedule_name: str | None = ...,
        surfaces: Sequence[
            _g.SurfacePropertySurroundingSurfacesSurfacesItem | _g.SurfacePropertySurroundingSurfacesSurfacesGroup
        ] = ...,
    ) -> None:
        """Create a new ``SurfaceProperty:SurroundingSurfaces`` and add it to the document.

        This object defines a list of surrounding surfaces for an exterior surface.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-advanced-surface-concepts/#surfacepropertysurroundingsurfaces
        """

class HVACTemplatePlantChillerObjectReference:
    def __call__(
        self,
        name: str,
        /,
        *,
        chiller_name: str,
        chiller_object_type: Literal["", "Chiller:Electric:EIR", "Chiller:Electric:ReformulatedEIR"]
        | None = "Chiller:Electric:EIR",
        priority: float | None = ...,
    ) -> None:
        """Create a new ``HVACTemplate:Plant:Chiller:ObjectReference`` and add it to the document.

        This object references a detailed chiller object and adds it to an HVACTemplate:Plant:ChilledWaterLoop. The user must create a complete detailed chiller object with all required curve or performance objects.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/hvac-template-objects/group-hvac-templates/#hvactemplateplantchillerobjectreference
        """

class AnyAirTerminalSingleDuctVAVNoReheat:
    def __call__(
        self,
        name: str,
        /,
        *,
        air_outlet_node_name: str,
        air_inlet_node_name: str,
        maximum_air_flow_rate: float | Literal["Autosize"],
        availability_schedule_name: str | None = ...,
        zone_minimum_air_flow_input_method: Literal["", "Constant", "FixedFlowRate", "Scheduled"] | None = "Constant",
        constant_minimum_air_flow_fraction: float | Literal["", "Autosize"] | None = "Autosize",
        fixed_minimum_air_flow_rate: float | Literal["", "Autosize"] | None = "Autosize",
        minimum_air_flow_fraction_schedule_name: str | None = ...,
        design_specification_outdoor_air_object_name: str | None = ...,
    ) -> None:
        """Create a new ``AirTerminal:SingleDuct:VAV:NoReheat`` and add it to the document.

        Central air system terminal unit, single duct, variable volume, with no reheat coil.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-zone-hvac-air-loop-terminal-units/#airterminalsingleductvavnoreheat
        """

class AnyCoilHeatingDXMultiSpeed:
    def __call__(
        self,
        name: str,
        /,
        *,
        air_inlet_node_name: str,
        air_outlet_node_name: str,
        fuel_type: Literal["Diesel", "Electricity", "Gasoline", "NaturalGas", "OtherFuel1", "OtherFuel2", "Propane"],
        number_of_speeds: int,
        speed_1_gross_rated_heating_capacity: float | Literal["Autosize"],
        speed_1_gross_rated_heating_cop: float,
        speed_1_rated_air_flow_rate: float | Literal["Autosize"],
        speed_1_heating_capacity_function_of_temperature_curve_name: str,
        speed_1_heating_capacity_function_of_flow_fraction_curve_name: str,
        speed_1_energy_input_ratio_function_of_temperature_curve_name: str,
        speed_1_energy_input_ratio_function_of_flow_fraction_curve_name: str,
        speed_1_part_load_fraction_correlation_curve_name: str,
        speed_2_gross_rated_heating_capacity: float | Literal["Autosize"],
        speed_2_gross_rated_heating_cop: float,
        speed_2_rated_air_flow_rate: float | Literal["Autosize"],
        speed_2_heating_capacity_function_of_temperature_curve_name: str,
        speed_2_heating_capacity_function_of_flow_fraction_curve_name: str,
        speed_2_energy_input_ratio_function_of_temperature_curve_name: str,
        speed_2_energy_input_ratio_function_of_flow_fraction_curve_name: str,
        speed_2_part_load_fraction_correlation_curve_name: str,
        availability_schedule_name: str | None = ...,
        minimum_outdoor_dry_bulb_temperature_for_compressor_operation: float | None = -8,
        outdoor_dry_bulb_temperature_to_turn_on_compressor: float | None = ...,
        crankcase_heater_capacity: float | None = 0,
        maximum_outdoor_dry_bulb_temperature_for_crankcase_heater_operation: float | None = 10,
        defrost_energy_input_ratio_function_of_temperature_curve_name: str | None = ...,
        maximum_outdoor_dry_bulb_temperature_for_defrost_operation: float | None = 5,
        defrost_strategy: Literal["", "Resistive", "ReverseCycle"] | None = "ReverseCycle",
        defrost_control: Literal["", "OnDemand", "Timed"] | None = "Timed",
        defrost_time_period_fraction: float | None = 0.058333,
        resistive_defrost_heater_capacity: float | Literal["", "Autosize"] | None = 0,
        apply_part_load_fraction_to_speeds_greater_than_1: Literal["", "No", "Yes"] | None = "No",
        region_number_for_calculating_hspf: int | None = 4,
        speed_1_rated_waste_heat_fraction_of_power_input: float | None = 0.2,
        speed_1_waste_heat_function_of_temperature_curve_name: str | None = ...,
        speed_2_rated_waste_heat_fraction_of_power_input: float | None = 0.2,
        speed_2_waste_heat_function_of_temperature_curve_name: str | None = ...,
        speed_3_gross_rated_heating_capacity: float | Literal["Autosize"] | None = ...,
        speed_3_gross_rated_heating_cop: float | None = ...,
        speed_3_rated_air_flow_rate: float | Literal["Autosize"] | None = ...,
        speed_3_heating_capacity_function_of_temperature_curve_name: str | None = ...,
        speed_3_heating_capacity_function_of_flow_fraction_curve_name: str | None = ...,
        speed_3_energy_input_ratio_function_of_temperature_curve_name: str | None = ...,
        speed_3_energy_input_ratio_function_of_flow_fraction_curve_name: str | None = ...,
        speed_3_part_load_fraction_correlation_curve_name: str | None = ...,
        speed_3_rated_waste_heat_fraction_of_power_input: float | None = 0.2,
        speed_3_waste_heat_function_of_temperature_curve_name: str | None = ...,
        speed_4_gross_rated_heating_capacity: float | Literal["Autosize"] | None = ...,
        speed_4_gross_rated_heating_cop: float | None = ...,
        speed_4_rated_air_flow_rate: float | Literal["Autosize"] | None = ...,
        speed_4_heating_capacity_function_of_temperature_curve_name: str | None = ...,
        speed_4_heating_capacity_function_of_flow_fraction_curve_name: str | None = ...,
        speed_4_energy_input_ratio_function_of_temperature_curve_name: str | None = ...,
        speed_4_energy_input_ratio_function_of_flow_fraction_curve_name: str | None = ...,
        speed_4_part_load_fraction_correlation_curve_name: str | None = ...,
        speed_4_rated_waste_heat_fraction_of_power_input: float | None = 0.2,
        speed_4_waste_heat_function_of_temperature_curve_name: str | None = ...,
        zone_name_for_evaporator_placement: str | None = ...,
        speed_1_secondary_coil_air_flow_rate: float | Literal["Autosize"] | None = ...,
        speed_1_secondary_coil_fan_flow_scaling_factor: float | None = 1.25,
        speed_1_nominal_sensible_heat_ratio_of_secondary_coil: float | None = ...,
        speed_1_sensible_heat_ratio_modifier_function_of_temperature_curve_name: str | None = ...,
        speed_1_sensible_heat_ratio_modifier_function_of_flow_fraction_curve_name: str | None = ...,
        speed_2_secondary_coil_air_flow_rate: float | Literal["Autosize"] | None = ...,
        speed_2_secondary_coil_fan_flow_scaling_factor: float | None = 1.25,
        speed_2_nominal_sensible_heat_ratio_of_secondary_coil: float | None = ...,
        speed_2_sensible_heat_ratio_modifier_function_of_temperature_curve_name: str | None = ...,
        speed_2_sensible_heat_ratio_modifier_function_of_flow_fraction_curve_name: str | None = ...,
        speed_3_secondary_coil_air_flow_rate: float | Literal["Autosize"] | None = ...,
        speed_3_secondary_coil_fan_flow_scaling_factor: float | None = 1.25,
        speed_3_nominal_sensible_heat_ratio_of_secondary_coil: float | None = ...,
        speed_3_sensible_heat_ratio_modifier_function_of_temperature_curve_name: str | None = ...,
        speed_3_sensible_heat_ratio_modifier_function_of_flow_fraction_curve_name: str | None = ...,
        speed_4_secondary_coil_air_flow_rate: float | Literal["Autosize"] | None = ...,
        speed_4_secondary_coil_fan_flow_scaling_factor: float | None = 1.25,
        speed_4_nominal_sensible_heat_ratio_of_secondary_coil: float | None = ...,
        speed_4_sensible_heat_ratio_modifier_function_of_temperature_curve_name: str | None = ...,
        speed_4_sensible_heat_ratio_modifier_function_of_flow_fraction_curve_name: str | None = ...,
    ) -> None:
        """Create a new ``Coil:Heating:DX:MultiSpeed`` and add it to the document.

        Direct expansion (DX) heating coil (air-to-air heat pump) and compressor unit (includes electric or engine-driven compressor and outdoor fan), multi-speed (or variable-speed), with defrost controls. Requires two to four sets of performance data and will interpolate between speeds.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-heating-and-cooling-coils/#coilheatingdxmultispeed
        """

class EnergyManagementSystemSubroutine:
    def __call__(
        self,
        name: str,
        /,
        *,
        lines: Sequence[
            _g.EnergyManagementSystemSubroutineLinesItem | _g.EnergyManagementSystemSubroutineLinesGroup
        ] = ...,
    ) -> None:
        """Create a new ``EnergyManagementSystem:Subroutine`` and add it to the document.

        This input defines an Erl program subroutine Each field after the name is a line of EMS Runtime Language

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-energy-management-system-ems/#energymanagementsystemsubroutine
        """

class OutputVariable:
    def __call__(
        self,
        this_type_has_no_name_field: _g._PassFieldsAsKeywords = ...,
        /,
        *,
        variable_name: str,
        key_value: str | None = "*",
        reporting_frequency: Literal[
            "", "Annual", "Daily", "Detailed", "Environment", "Hourly", "Monthly", "RunPeriod", "Timestep"
        ]
        | None = "Hourly",
        schedule_name: str | None = ...,
    ) -> None:
        """Create a new ``Output:Variable`` and add it to the document.

        each Output:Variable command picks variables to be put onto the standard output file (.eso) some variables may not be reported for every simulation. a list of variables that can be reported are available after a run on the report dictionary file (.rdd) if the Output:VariableDictionary has been requested.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/input-for-output/#outputvariable
        """
