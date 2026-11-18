"""Creation signatures of generated classes (stub only).

DO NOT EDIT — regenerate with:
    python -m idfkit.codegen.generate_stubs
"""

from __future__ import annotations

from collections.abc import Sequence
from typing import Literal

from .. import _generated_types as _g

class OutputControlIlluminanceMapStyle:
    def __call__(
        self,
        this_type_has_no_name_field: _g._PassFieldsAsKeywords = ...,
        /,
        *,
        column_separator: Literal["Comma", "Fixed", "Tab"] | None = "Comma",
        validate: bool = True,
    ) -> None:
        """Create a new ``OutputControl:IlluminanceMap:Style`` and add it to the document.

        default style for the Daylighting Illuminance Map is comma -- this works well for importing into spreadsheet programs such as Excel(tm) but not so well for word processing programs -- there tab may be a better choice. fixed puts spaces between the 'columns'

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-daylighting/#outputcontrolilluminancemapstyle
        """

class AnyFanSystemModel:
    def __call__(
        self,
        name: str,
        /,
        *,
        air_inlet_node_name: str,
        air_outlet_node_name: str,
        design_maximum_air_flow_rate: float | Literal["Autosize"],
        design_pressure_rise: float,
        availability_schedule_name: str | None = ...,
        speed_control_method: Literal["Continuous", "Discrete"] | None = "Discrete",
        electric_power_minimum_flow_rate_fraction: float | None = 0.2,
        motor_efficiency: float | None = 0.9,
        motor_in_air_stream_fraction: float | None = 1,
        design_electric_power_consumption: float | Literal["Autosize"] | None = ...,
        design_power_sizing_method: Literal["PowerPerFlow", "PowerPerFlowPerPressure", "TotalEfficiencyAndPressure"]
        | None = "PowerPerFlowPerPressure",
        electric_power_per_unit_flow_rate: float | None = ...,
        electric_power_per_unit_flow_rate_per_unit_pressure: float | None = 1.66667,
        fan_total_efficiency: float | None = 0.7,
        electric_power_function_of_flow_fraction_curve_name: str | None = ...,
        night_ventilation_mode_pressure_rise: float | None = ...,
        night_ventilation_mode_flow_fraction: float | None = ...,
        motor_loss_zone_name: str | None = ...,
        motor_loss_radiative_fraction: float | None = ...,
        end_use_subcategory: str | None = "General",
        number_of_speeds: int | None = 1,
        speed_fractions: Sequence[_g.FanSystemModelSpeedFractionsItem | _g.FanSystemModelSpeedFractionsGroup] = ...,
        validate: bool = True,
    ) -> None:
        """Create a new ``Fan:SystemModel`` and add it to the document.

        Versatile simple fan that can be used in variable air volume, constant volume, on-off cycling, two-speed or multi-speed applications. Performance at different flow rates, or speed levels, is determined using separate performance curve or table or prescribed power fractions at discrete speed levels for two-speed or multi-speed fans.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-fans/#fansystemmodel
        """

class PumpVariableSpeed:
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
        end_use_subcategory: str | None = "General",
        validate: bool = True,
    ) -> None:
        """Create a new ``Pump:VariableSpeed`` and add it to the document.

        This pump model is described in the ASHRAE secondary HVAC toolkit.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-pumps/#pumpvariablespeed
        """

class ChillerHeaterAbsorptionDoubleEffect:
    def __call__(
        self,
        name: str,
        /,
        *,
        chilled_water_inlet_node_name: str,
        chilled_water_outlet_node_name: str,
        condenser_inlet_node_name: str,
        hot_water_inlet_node_name: str,
        hot_water_outlet_node_name: str,
        exhaust_source_object_type: Literal["Generator:MicroTurbine"],
        nominal_cooling_capacity: float | Literal["Autosize"] | None = "Autosize",
        heating_to_cooling_capacity_ratio: float | None = 0.8,
        thermal_energy_input_to_cooling_output_ratio: float | None = 0.97,
        thermal_energy_input_to_heating_output_ratio: float | None = 1.25,
        electric_input_to_cooling_output_ratio: float | None = 0.01,
        electric_input_to_heating_output_ratio: float | None = 0,
        condenser_outlet_node_name: str | None = ...,
        minimum_part_load_ratio: float | None = 0.1,
        maximum_part_load_ratio: float | None = 1,
        optimum_part_load_ratio: float | None = 1,
        design_entering_condenser_water_temperature: float | None = 29,
        design_leaving_chilled_water_temperature: float | None = 7,
        design_chilled_water_flow_rate: float | Literal["Autosize"] | None = "Autosize",
        design_condenser_water_flow_rate: float | Literal["Autosize"] | None = "Autosize",
        design_hot_water_flow_rate: float | Literal["Autosize"] | None = "Autosize",
        cooling_capacity_function_of_temperature_curve_name: str | None = ...,
        fuel_input_to_cooling_output_ratio_function_of_temperature_curve_name: str | None = ...,
        fuel_input_to_cooling_output_ratio_function_of_part_load_ratio_curve_name: str | None = ...,
        electric_input_to_cooling_output_ratio_function_of_temperature_curve_name: str | None = ...,
        electric_input_to_cooling_output_ratio_function_of_part_load_ratio_curve_name: str | None = ...,
        heating_capacity_function_of_cooling_capacity_curve_name: str | None = ...,
        fuel_input_to_heat_output_ratio_during_heating_only_operation_curve_name: str | None = ...,
        temperature_curve_input_variable: Literal["EnteringCondenser", "LeavingCondenser"] | None = "EnteringCondenser",
        condenser_type: Literal["AirCooled", "WaterCooled"] | None = "WaterCooled",
        chilled_water_temperature_lower_limit: float | None = 2,
        exhaust_source_object_name: str | None = ...,
        sizing_factor: float | None = 1,
        validate: bool = True,
    ) -> None:
        """Create a new ``ChillerHeater:Absorption:DoubleEffect`` and add it to the document.

        Exhaust fired absorption chiller-heater using performance curves similar to DOE-2

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-plant-equipment/#chillerheaterabsorptiondoubleeffect
        """

class GroundHeatExchangerSystem:
    def __call__(
        self,
        name: str,
        /,
        *,
        inlet_node_name: str,
        outlet_node_name: str,
        design_flow_rate: float,
        undisturbed_ground_temperature_model_type: Literal[
            "Site:GroundTemperature:Undisturbed:FiniteDifference",
            "Site:GroundTemperature:Undisturbed:KusudaAchenbach",
            "Site:GroundTemperature:Undisturbed:Xing",
        ],
        undisturbed_ground_temperature_model_name: str,
        ground_thermal_conductivity: float,
        ground_thermal_heat_capacity: float,
        ghe_vertical_responsefactors_object_name: str | None = ...,
        g_function_calculation_method: Literal["FullDesign", "UBHWTcalc", "UHFcalc"] | None = "UHFcalc",
        ghe_vertical_sizing_object_type: Literal["GroundHeatExchanger:Vertical:Sizing:Rectangle"] | None = ...,
        ghe_vertical_sizing_object_name: str | None = ...,
        ghe_vertical_array_object_name: str | None = ...,
        vertical_well_locations: Sequence[
            _g.GroundHeatExchangerSystemVerticalWellLocationsItem
            | _g.GroundHeatExchangerSystemVerticalWellLocationsGroup
        ] = ...,
        validate: bool = True,
    ) -> None:
        """Create a new ``GroundHeatExchanger:System`` and add it to the document.

        Models vertical ground heat exchangers systems using the response factor approach developed by Eskilson. Response factors are calculated using a finite line source model assuming uniform heat flux at the borehole wall if UHFcalc is specified, or uniform borehole wall temperature if UBHWTcalc is specified.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-condenser-equipment/#groundheatexchangersystem
        """

class SetpointManagerOutdoorAirPretreat:
    def __call__(
        self,
        name: str,
        /,
        *,
        mixed_air_stream_node_name: str,
        outdoor_air_stream_node_name: str,
        return_air_stream_node_name: str,
        setpoint_node_or_nodelist_name: str,
        control_variable: Literal["HumidityRatio", "MaximumHumidityRatio", "MinimumHumidityRatio", "Temperature"]
        | None = ...,
        minimum_setpoint_temperature: float | None = -99,
        maximum_setpoint_temperature: float | None = 99,
        minimum_setpoint_humidity_ratio: float | None = ...,
        maximum_setpoint_humidity_ratio: float | None = 1,
        reference_setpoint_node_name: str | None = ...,
        validate: bool = True,
    ) -> None:
        """Create a new ``SetpointManager:OutdoorAirPretreat`` and add it to the document.

        This setpoint manager determines the required conditions at the outdoor air stream node which will produce the reference setpoint condition at the mixed air node when mixed with the return air stream

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-setpoint-managers/#setpointmanageroutdoorairpretreat
        """

class SetpointManagerReturnAirBypassFlow:
    def __call__(
        self,
        name: str,
        /,
        *,
        hvac_air_loop_name: str,
        control_variable: Literal["Flow"] | None = "Flow",
        temperature_setpoint_schedule_name: str | None = ...,
        validate: bool = True,
    ) -> None:
        """Create a new ``SetpointManager:ReturnAirBypassFlow`` and add it to the document.

        This setpoint manager determines the required mass flow rate through a return air bypass duct to meet the specified temperature setpoint

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-setpoint-managers/#setpointmanagerreturnairbypassflow
        """

class AnyLifeCycleCostUseAdjustment:
    def __call__(
        self,
        name: str,
        /,
        *,
        resource: Literal[
            "Coal",
            "Diesel",
            "Electricity",
            "ElectricityNet",
            "ElectricityProduced",
            "ElectricityPurchased",
            "ElectricitySurplusSold",
            "Gasoline",
            "NaturalGas",
            "OtherFuel1",
            "OtherFuel2",
            "Propane",
            "Water",
        ],
        multipliers: Sequence[
            _g.LifeCycleCostUseAdjustmentMultipliersItem | _g.LifeCycleCostUseAdjustmentMultipliersGroup
        ] = ...,
        validate: bool = True,
    ) -> None:
        """Create a new ``LifeCycleCost:UseAdjustment`` and add it to the document.

        Used by advanced users to adjust the energy or water use costs for future years. This should not be used for compensating for inflation but should only be used to increase the costs of energy or water based on assumed changes to the actual usage, such as anticipated changes in the future function of the building. The adjustments begin at the start of the service period.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/energyplus-economics/lifecyclecost-useadjustment/#lifecyclecostuseadjustment
        """

class LifeCycleCostUseAdjustment:
    def __call__(
        self,
        name: str,
        /,
        *,
        resource: Literal[
            "Coal",
            "Diesel",
            "DistrictCooling",
            "DistrictHeatingSteam",
            "DistrictHeatingWater",
            "Electricity",
            "ElectricityNet",
            "ElectricityProduced",
            "ElectricityPurchased",
            "ElectricitySurplusSold",
            "FuelOilNo1",
            "FuelOilNo2",
            "Gasoline",
            "NaturalGas",
            "OtherFuel1",
            "OtherFuel2",
            "Propane",
            "Water",
        ],
        multipliers: Sequence[
            _g.LifeCycleCostUseAdjustmentMultipliersItem | _g.LifeCycleCostUseAdjustmentMultipliersGroup
        ] = ...,
        validate: bool = True,
    ) -> None:
        """Create a new ``LifeCycleCost:UseAdjustment`` and add it to the document.

        Used by advanced users to adjust the energy or water use costs for future years. This should not be used for compensating for inflation but should only be used to increase the costs of energy or water based on assumed changes to the actual usage, such as anticipated changes in the future function of the building. The adjustments begin at the start of the service period.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/energyplus-economics/lifecyclecost-useadjustment/#lifecyclecostuseadjustment
        """
