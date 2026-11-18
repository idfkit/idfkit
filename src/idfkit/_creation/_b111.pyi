"""Creation signatures of generated classes (stub only).

DO NOT EDIT — regenerate with:
    python -m idfkit.codegen.generate_stubs
"""

from __future__ import annotations

from typing import Literal

from .. import _generated_types as _g

class SurfaceConvectionAlgorithmOutside:
    def __call__(
        self,
        this_type_has_no_name_field: _g._PassFieldsAsKeywords = ...,
        /,
        *,
        algorithm: Literal["AdaptiveConvectionAlgorithm", "DOE-2", "MoWiTT", "SimpleCombined", "TARP"] | None = "DOE-2",
    ) -> None:
        """Create a new ``SurfaceConvectionAlgorithm:Outside`` and add it to the document.

        Default outside surface heat transfer convection algorithm to be used for all zones

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-simulation-parameters/#surfaceconvectionalgorithmoutside
        """

class HVACTemplateSystemVAV:
    def __call__(
        self,
        name: str,
        /,
        *,
        system_availability_schedule_name: str | None = ...,
        supply_fan_maximum_flow_rate: float | Literal["Autosize"] | None = "Autosize",
        supply_fan_minimum_flow_rate: float | Literal["Autosize"] | None = "Autosize",
        supply_fan_total_efficiency: float | None = 0.7,
        supply_fan_delta_pressure: float | None = 1000,
        supply_fan_motor_efficiency: float | None = 0.9,
        supply_fan_motor_in_air_stream_fraction: float | None = 1,
        cooling_coil_type: Literal["ChilledWater", "ChilledWaterDetailedFlatModel"] | None = "ChilledWater",
        cooling_coil_availability_schedule_name: str | None = ...,
        cooling_coil_setpoint_schedule_name: str | None = ...,
        cooling_coil_design_setpoint: float | None = 12.8,
        heating_coil_type: Literal["Electric", "Gas", "HotWater", "None"] | None = "None",
        heating_coil_availability_schedule_name: str | None = ...,
        heating_coil_setpoint_schedule_name: str | None = ...,
        heating_coil_design_setpoint: float | None = 10,
        gas_heating_coil_efficiency: float | None = 0.8,
        gas_heating_coil_parasitic_electric_load: float | None = 0,
        preheat_coil_type: Literal["Electric", "Gas", "HotWater", "None"] | None = "None",
        preheat_coil_availability_schedule_name: str | None = ...,
        preheat_coil_setpoint_schedule_name: str | None = ...,
        preheat_coil_design_setpoint: float | None = 7.2,
        gas_preheat_coil_efficiency: float | None = 0.8,
        gas_preheat_coil_parasitic_electric_load: float | None = 0,
        maximum_outdoor_air_flow_rate: float | Literal["Autosize"] | None = "Autosize",
        minimum_outdoor_air_flow_rate: float | Literal["Autosize"] | None = "Autosize",
        minimum_outdoor_air_control_type: Literal["FixedMinimum", "ProportionalMinimum"] | None = "ProportionalMinimum",
        minimum_outdoor_air_schedule_name: str | None = ...,
        economizer_type: Literal[
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
        economizer_lockout: Literal["NoLockout"] | None = "NoLockout",
        economizer_upper_temperature_limit: float | None = ...,
        economizer_lower_temperature_limit: float | None = ...,
        economizer_upper_enthalpy_limit: float | None = ...,
        economizer_maximum_limit_dewpoint_temperature: float | None = ...,
        supply_plenum_name: str | None = ...,
        return_plenum_name: str | None = ...,
        supply_fan_placement: Literal["BlowThrough", "DrawThrough"] | None = "DrawThrough",
        supply_fan_part_load_power_coefficients: Literal[
            "ASHRAE90.1-2004AppendixG",
            "InletVaneDampers",
            "OutletDampers",
            "VariableSpeedMotor",
            "VariableSpeedMotorPressureReset",
        ]
        | None = "InletVaneDampers",
        night_cycle_control: Literal["CycleOnAny", "CycleOnAnyZoneFansOnly", "CycleOnControlZone", "StayOff"]
        | None = "StayOff",
        night_cycle_control_zone_name: str | None = ...,
        heat_recovery_type: Literal["Enthalpy", "None", "Sensible"] | None = "None",
        sensible_heat_recovery_effectiveness: float | None = 0.7,
        latent_heat_recovery_effectiveness: float | None = 0.65,
        cooling_coil_setpoint_reset_type: Literal[
            "None", "OutdoorAirTemperatureReset", "Warmest", "WarmestTemperatureFirst"
        ]
        | None = "None",
        heating_coil_setpoint_reset_type: Literal["None", "OutdoorAirTemperatureReset"] | None = "None",
        dehumidification_control_type: Literal["CoolReheat", "None"] | None = "None",
        dehumidification_control_zone_name: str | None = ...,
        dehumidification_setpoint: float | None = 60,
        humidifier_type: Literal["ElectricSteam", "None"] | None = "None",
        humidifier_availability_schedule_name: str | None = ...,
        humidifier_rated_capacity: float | None = ...,
        humidifier_rated_electric_power: float | Literal["Autosize"] | None = "Autosize",
        humidifier_control_zone_name: str | None = ...,
        humidifier_setpoint: float | None = 30,
        sizing_option: Literal["Coincident", "NonCoincident"] | None = "NonCoincident",
        return_fan: Literal["No", "Yes"] | None = "No",
        return_fan_total_efficiency: float | None = 0.7,
        return_fan_delta_pressure: float | None = 500,
        return_fan_motor_efficiency: float | None = 0.9,
        return_fan_motor_in_air_stream_fraction: float | None = 1,
        return_fan_part_load_power_coefficients: Literal[
            "ASHRAE90.1-2004AppendixG",
            "InletVaneDampers",
            "OutletDampers",
            "VariableSpeedMotor",
            "VariableSpeedMotorPressureReset",
        ]
        | None = "InletVaneDampers",
    ) -> None:
        """Create a new ``HVACTemplate:System:VAV`` and add it to the document.

        Variable Air Volume (VAV) air loop with optional heating coil and optional preheat.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/hvac-template-objects/group-hvac-templates/#hvactemplatesystemvav
        """

class AnySizingParameters:
    def __call__(
        self,
        this_type_has_no_name_field: _g._PassFieldsAsKeywords = ...,
        /,
        *,
        heating_sizing_factor: float | None = 1,
        cooling_sizing_factor: float | None = 1,
        timesteps_in_averaging_window: int | None = ...,
    ) -> None:
        """Create a new ``Sizing:Parameters`` and add it to the document.

        Specifies global heating and cooling sizing factors/ratios. These ratios are applied at the zone level to all of the zone heating and cooling loads and air flow rates. Then these new loads and air flow rates are used to calculate the system level flow rates and capacities and are used in all component sizing calculations. Specifies the width (in load timesteps) of a moving average window which is used to smooth the peak load across more than one timestep.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-design-objects/#sizingparameters
        """

class ZoneHVACLowTemperatureRadiantConstantFlowDesign:
    def __call__(
        self,
        name: str,
        /,
        *,
        fluid_to_radiant_surface_heat_transfer_model: Literal["ConvectionOnly", "ISOStandard"]
        | None = "ConvectionOnly",
        hydronic_tubing_inside_diameter: float | None = 0.013,
        hydronic_tubing_outside_diameter: float | None = 0.016,
        hydronic_tubing_conductivity: float | None = 0.35,
        temperature_control_type: Literal[
            "MeanAirTemperature",
            "MeanRadiantTemperature",
            "OperativeTemperature",
            "OutdoorDryBulbTemperature",
            "OutdoorWetBulbTemperature",
            "RunningMeanOutdoorDryBulbTemperature",
            "SurfaceFaceTemperature",
            "SurfaceInteriorTemperature",
        ]
        | None = "MeanAirTemperature",
        running_mean_outdoor_dry_bulb_temperature_weighting_factor: float | None = 0.8,
        motor_efficiency: float | None = 0.9,
        fraction_of_motor_inefficiencies_to_fluid_stream: float | None = 0,
        condensation_control_type: Literal["Off", "SimpleOff", "VariableOff"] | None = "SimpleOff",
        condensation_control_dewpoint_offset: float | None = 1,
        changeover_delay_time_period_schedule: str | None = ...,
    ) -> None:
        """Create a new ``ZoneHVAC:LowTemperatureRadiant:ConstantFlow:Design`` and add it to the document.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-radiative-convective-units/#zonehvaclowtemperatureradiantconstantflowdesign
        """

class ControllerOutdoorAir:
    def __call__(
        self,
        name: str,
        /,
        *,
        relief_air_outlet_node_name: str,
        return_air_node_name: str,
        mixed_air_node_name: str,
        actuator_node_name: str,
        minimum_outdoor_air_flow_rate: float | Literal["Autosize"],
        maximum_outdoor_air_flow_rate: float | Literal["Autosize"],
        economizer_control_type: Literal[
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
        economizer_control_action_type: Literal["MinimumFlowWithBypass", "ModulateFlow"] | None = "ModulateFlow",
        economizer_maximum_limit_dry_bulb_temperature: float | None = ...,
        economizer_maximum_limit_enthalpy: float | None = ...,
        economizer_maximum_limit_dewpoint_temperature: float | None = ...,
        electronic_enthalpy_limit_curve_name: str | None = ...,
        economizer_minimum_limit_dry_bulb_temperature: float | None = ...,
        lockout_type: Literal["LockoutWithCompressor", "LockoutWithHeating", "NoLockout"] | None = "NoLockout",
        minimum_limit_type: Literal["FixedMinimum", "ProportionalMinimum"] | None = "ProportionalMinimum",
        minimum_outdoor_air_schedule_name: str | None = ...,
        minimum_fraction_of_outdoor_air_schedule_name: str | None = ...,
        maximum_fraction_of_outdoor_air_schedule_name: str | None = ...,
        mechanical_ventilation_controller_name: str | None = ...,
        time_of_day_economizer_control_schedule_name: str | None = ...,
        high_humidity_control: Literal["No", "Yes"] | None = "No",
        humidistat_control_zone_name: str | None = ...,
        high_humidity_outdoor_air_flow_ratio: float | None = 1,
        control_high_indoor_humidity_based_on_outdoor_humidity_ratio: Literal["No", "Yes"] | None = "Yes",
        heat_recovery_bypass_control_type: Literal[
            "BypassWhenOAFlowGreaterThanMinimum", "BypassWhenWithinEconomizerLimits"
        ]
        | None = "BypassWhenWithinEconomizerLimits",
        economizer_operation_staging: Literal["EconomizerFirst", "InterlockedWithMechanicalCooling"]
        | None = "InterlockedWithMechanicalCooling",
    ) -> None:
        """Create a new ``Controller:OutdoorAir`` and add it to the document.

        Controller to set the outdoor air flow rate for an air loop. Control options include fixed, proportional, scheduled, economizer, and demand-controlled ventilation.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-controllers/#controlleroutdoorair
        """

class AnyEvaporativeFluidCoolerTwoSpeed:
    def __call__(
        self,
        name: str,
        /,
        *,
        water_inlet_node_name: str,
        water_outlet_node_name: str,
        high_fan_speed_air_flow_rate: float | Literal["Autosize"],
        high_fan_speed_fan_power: float | Literal["Autosize"],
        low_fan_speed_air_flow_rate: float | Literal["Autocalculate"],
        low_fan_speed_fan_power: float | Literal["Autocalculate"],
        design_spray_water_flow_rate: float,
        performance_input_method: Literal[
            "StandardDesignCapacity", "UFactorTimesAreaAndDesignWaterFlowRate", "UserSpecifiedDesignCapacity"
        ],
        low_fan_speed_air_flow_rate_sizing_factor: float | None = 0.5,
        low_fan_speed_fan_power_sizing_factor: float | None = 0.16,
        outdoor_air_inlet_node_name: str | None = ...,
        heat_rejection_capacity_and_nominal_capacity_sizing_ratio: float | None = 1.25,
        high_speed_standard_design_capacity: float | None = ...,
        low_speed_standard_design_capacity: float | Literal["Autocalculate"] | None = ...,
        low_speed_standard_capacity_sizing_factor: float | None = 0.5,
        high_fan_speed_u_factor_times_area_value: float | Literal["Autosize"] | None = ...,
        low_fan_speed_u_factor_times_area_value: float | Literal["Autocalculate"] | None = ...,
        low_fan_speed_u_factor_times_area_sizing_factor: float | None = 0.6,
        design_water_flow_rate: float | Literal["Autosize"] | None = ...,
        high_speed_user_specified_design_capacity: float | None = ...,
        low_speed_user_specified_design_capacity: float | Literal["Autocalculate"] | None = ...,
        low_speed_user_specified_design_capacity_sizing_factor: float | None = 0.5,
        design_entering_water_temperature: float | None = ...,
        design_entering_air_temperature: float | None = ...,
        design_entering_air_wet_bulb_temperature: float | None = ...,
        high_speed_sizing_factor: float | None = 1,
        evaporation_loss_mode: Literal["LossFactor", "SaturatedExit"] | None = "SaturatedExit",
        evaporation_loss_factor: float | None = ...,
        drift_loss_percent: float | None = 0.008,
        blowdown_calculation_mode: Literal["ConcentrationRatio", "ScheduledRate"] | None = "ConcentrationRatio",
        blowdown_concentration_ratio: float | None = 3,
        blowdown_makeup_water_usage_schedule_name: str | None = ...,
        supply_water_storage_tank_name: str | None = ...,
    ) -> None:
        """Create a new ``EvaporativeFluidCooler:TwoSpeed`` and add it to the document.

        This model is based on Merkel's theory, which is also the basis for the cooling tower model in EnergyPlus. The Evaporative fluid cooler is modeled as a counter flow heat exchanger.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-condenser-equipment/#evaporativefluidcoolertwospeed
        """

class ElectricLoadCenterInverterLookUpTable:
    def __call__(
        self,
        name: str = "",
        /,
        *,
        availability_schedule_name: str | None = ...,
        zone_name: str | None = ...,
        radiative_fraction: float | None = ...,
        rated_maximum_continuous_output_power: float | None = ...,
        night_tare_loss_power: float | None = ...,
        nominal_voltage_input: float | None = ...,
        efficiency_at_10_power_and_nominal_voltage: float | None = ...,
        efficiency_at_20_power_and_nominal_voltage: float | None = ...,
        efficiency_at_30_power_and_nominal_voltage: float | None = ...,
        efficiency_at_50_power_and_nominal_voltage: float | None = ...,
        efficiency_at_75_power_and_nominal_voltage: float | None = ...,
        efficiency_at_100_power_and_nominal_voltage: float | None = ...,
    ) -> None:
        """Create a new ``ElectricLoadCenter:Inverter:LookUpTable`` and add it to the document.

        California Energy Commission tests and publishes data on inverters This inverter model interpolates using CEC test data Input data are at http://www.gosolarcalifornia.org/equipment/inverter_tests/summaries

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-electric-load-center-generator/#electricloadcenterinverterlookuptable
        """

class UtilityCostChargeBlock:
    def __call__(
        self,
        this_type_has_no_name_field: _g._PassFieldsAsKeywords = ...,
        /,
        *,
        utility_cost_charge_block_name: str,
        tariff_name: str,
        source_variable: str,
        category_variable_name: Literal[
            "Adjustment",
            "Basis",
            "DemandCharges",
            "EnergyCharges",
            "NotIncluded",
            "ServiceCharges",
            "Subtotal",
            "Surcharge",
            "Taxes",
            "Total",
        ],
        season: Literal["Annual", "Fall", "Spring", "Summer", "Winter"] | None = ...,
        remaining_into_variable: str | None = ...,
        block_size_multiplier_value_or_variable_name: float | str | None = ...,
        block_size_1_value_or_variable_name: float | str | None = ...,
        block_1_cost_per_unit_value_or_variable_name: float | str | None = ...,
        block_size_2_value_or_variable_name: float | str | None = ...,
        block_2_cost_per_unit_value_or_variable_name: float | str | None = ...,
        block_size_3_value_or_variable_name: float | str | None = ...,
        block_3_cost_per_unit_value_or_variable_name: float | str | None = ...,
        block_size_4_value_or_variable_name: float | str | None = ...,
        block_4_cost_per_unit_value_or_variable_name: float | str | None = ...,
        block_size_5_value_or_variable_name: float | str | None = ...,
        block_5_cost_per_unit_value_or_variable_name: float | str | None = ...,
        block_size_6_value_or_variable_name: float | str | None = ...,
        block_6_cost_per_unit_value_or_variable_name: float | str | None = ...,
        block_size_7_value_or_variable_name: float | str | None = ...,
        block_7_cost_per_unit_value_or_variable_name: float | str | None = ...,
        block_size_8_value_or_variable_name: float | str | None = ...,
        block_8_cost_per_unit_value_or_variable_name: float | str | None = ...,
        block_size_9_value_or_variable_name: float | str | None = ...,
        block_9_cost_per_unit_value_or_variable_name: float | str | None = ...,
        block_size_10_value_or_variable_name: float | str | None = ...,
        block_10_cost_per_unit_value_or_variable_name: float | str | None = ...,
        block_size_11_value_or_variable_name: float | str | None = ...,
        block_11_cost_per_unit_value_or_variable_name: float | str | None = ...,
        block_size_12_value_or_variable_name: float | str | None = ...,
        block_12_cost_per_unit_value_or_variable_name: float | str | None = ...,
        block_size_13_value_or_variable_name: float | str | None = ...,
        block_13_cost_per_unit_value_or_variable_name: float | str | None = ...,
        block_size_14_value_or_variable_name: float | str | None = ...,
        block_14_cost_per_unit_value_or_variable_name: float | str | None = ...,
        block_size_15_value_or_variable_name: float | str | None = ...,
        block_15_cost_per_unit_value_or_variable_name: float | str | None = ...,
    ) -> None:
        """Create a new ``UtilityCost:Charge:Block`` and add it to the document.

        Used to compute energy and demand charges (or any other charges) that are structured in blocks of charges. Multiple UtilityCost:Charge:Block objects may be defined for a single tariff and they will be added together.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/energyplus-economics/utilitycost-charge-block/#utilitycostchargeblock
        """
