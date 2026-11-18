"""Creation signatures of generated classes (stub only).

DO NOT EDIT — regenerate with:
    python -m idfkit.codegen.generate_stubs
"""

from __future__ import annotations

from collections.abc import Sequence
from typing import Literal

from typing_extensions import Never

from .. import _generated_types as _g

class ScheduleYearRules:
    def __call__(
        self,
        name: str,
        /,
        *,
        default_day_schedule_name: str,
        schedule_type_limits_name: str | None = ...,
        summer_design_day_schedule_name: str | None = ...,
        winter_design_day_schedule_name: str | None = ...,
        holiday_schedule_name: str | None = ...,
        custom_day_1_schedule_name: str | None = ...,
        custom_day_2_schedule_name: str | None = ...,
    ) -> None:
        """Create a new ``Schedule:Year:Rules`` and add it to the document.

        A Schedule:Year:Rules defines a yearly schedule using a default day profile and a prioritized list of override rules (Schedule:Week:Rule objects). Rules are evaluated in ascending Rule Priority Order; the first matching rule for a given day is used. If no rule matches, the Default Day Schedule is used. Exception: if no rule date range includes February 29, February 29 inherits February 28.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-schedules/#scheduleyearrules
        """

class SurfaceConvectionAlgorithmOutsideAdaptiveModelSelections:
    def __call__(
        self,
        name: str = "",
        /,
        *,
        wind_convection_windward_vertical_wall_equation_source: Literal[
            "BlockenWindward",
            "DOE2Windward",
            "EmmelVertical",
            "McAdams",
            "Mitchell",
            "MoWiTTWindward",
            "NusseltJurges",
            "SimpleCombined",
            "TARPWindward",
            "UserCurve",
        ]
        | None = "TARPWindward",
        wind_convection_windward_equation_vertical_wall_user_curve_name: str | None = ...,
        wind_convection_leeward_vertical_wall_equation_source: Literal[
            "DOE2Leeward",
            "EmmelVertical",
            "McAdams",
            "Mitchell",
            "MoWiTTLeeward",
            "NusseltJurges",
            "SimpleCombined",
            "TARPLeeward",
            "UserCurve",
        ]
        | None = "TARPLeeward",
        wind_convection_leeward_vertical_wall_equation_user_curve_name: str | None = ...,
        wind_convection_horizontal_roof_equation_source: Literal[
            "BlockenWindward",
            "ClearRoof",
            "DOE2Windward",
            "EmmelRoof",
            "McAdams",
            "Mitchell",
            "MoWiTTWindward",
            "NusseltJurges",
            "SimpleCombined",
            "TARPWindward",
            "UserCurve",
        ]
        | None = "ClearRoof",
        wind_convection_horizontal_roof_user_curve_name: str | None = ...,
        natural_convection_vertical_wall_equation_source: Literal[
            "ASHRAEVerticalWall",
            "AlamdariHammondVerticalWall",
            "FohannoPolidoriVerticalWall",
            "ISO15099Windows",
            "None",
            "UserCurve",
        ]
        | None = "ASHRAEVerticalWall",
        natural_convection_vertical_wall_equation_user_curve_name: str | None = ...,
        natural_convection_stable_horizontal_equation_source: Literal[
            "AlamdariHammondStableHorizontal", "None", "UserCurve", "WaltonStableHorizontalOrTilt"
        ]
        | None = "WaltonStableHorizontalOrTilt",
        natural_convection_stable_horizontal_equation_user_curve_name: str | None = ...,
        natural_convection_unstable_horizontal_equation_source: Literal[
            "AlamdariHammondUnstableHorizontal", "None", "UserCurve", "WaltonUnstableHorizontalOrTilt"
        ]
        | None = "WaltonUnstableHorizontalOrTilt",
        natural_convection_unstable_horizontal_equation_user_curve_name: str | None = ...,
    ) -> None:
        """Create a new ``SurfaceConvectionAlgorithm:Outside:AdaptiveModelSelections`` and add it to the document.

        Options to change the individual convection model equations for dynamic selection when using AdaptiveConvectiongAlgorithm This object is only needed to make changes to the default model selections for any or all of the surface categories. This object is for the outside face, the side of the surface facing away from the thermal zone.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-advanced-surface-concepts/#surfaceconvectionalgorithmoutsideadaptivemodelselections
        """

class AnyAirflowNetworkDistributionComponentFan:
    def __call__(
        self,
        this_type_has_no_name_field: _g._PassFieldsAsKeywords = ...,
        /,
        *,
        fan_name: str,
        supply_fan_object_type: Literal["Fan:ConstantVolume", "Fan:OnOff", "Fan:VariableVolume"]
        | None = "Fan:ConstantVolume",
    ) -> None:
        """Create a new ``AirflowNetwork:Distribution:Component:Fan`` and add it to the document.

        This object defines the name of the supply Air Fan used in an Air loop.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-airflow-network/#airflownetworkdistributioncomponentfan
        """

class AirflowNetworkDistributionComponentHeatExchanger:
    def __call__(
        self,
        this_type_has_no_name_field: _g._PassFieldsAsKeywords = ...,
        /,
        *,
        heatexchanger_name: str,
        heatexchanger_object_type: Literal[
            "HeatExchanger:AirToAir:FlatPlate",
            "HeatExchanger:AirToAir:SensibleAndLatent",
            "HeatExchanger:Desiccant:BalancedFlow",
        ],
        air_path_length: float,
        air_path_hydraulic_diameter: float,
    ) -> None:
        """Create a new ``AirflowNetwork:Distribution:Component:HeatExchanger`` and add it to the document.

        This object defines the name of an air-to-air heat exchanger used in an air loop.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-airflow-network/#airflownetworkdistributioncomponentheatexchanger
        """

class HVACTemplateZonePTHP:
    def __call__(
        self,
        this_type_has_no_name_field: _g._PassFieldsAsKeywords = ...,
        /,
        *,
        zone_name: str,
        template_thermostat_name: str | None = ...,
        cooling_supply_air_flow_rate: float | Literal["Autosize"] | None = "Autosize",
        heating_supply_air_flow_rate: float | Literal["Autosize"] | None = "Autosize",
        no_load_supply_air_flow_rate: float | Literal["Autosize"] | None = ...,
        zone_heating_sizing_factor: float | None = ...,
        zone_cooling_sizing_factor: float | None = ...,
        outdoor_air_method: Literal["DetailedSpecification", "Flow/Area", "Flow/Person", "Flow/Zone", "Maximum", "Sum"]
        | None = "Flow/Person",
        outdoor_air_flow_rate_per_person: float | None = 0.00944,
        outdoor_air_flow_rate_per_zone_floor_area: float | None = 0,
        outdoor_air_flow_rate_per_zone: float | None = 0,
        system_availability_schedule_name: str | None = ...,
        supply_fan_operating_mode_schedule_name: str | None = ...,
        supply_fan_placement: Literal["BlowThrough", "DrawThrough"] | None = "DrawThrough",
        supply_fan_total_efficiency: float | None = 0.7,
        supply_fan_delta_pressure: float | None = 75,
        supply_fan_motor_efficiency: float | None = 0.9,
        cooling_coil_type: Literal["SingleSpeedDX"] | None = "SingleSpeedDX",
        cooling_coil_availability_schedule_name: str | None = ...,
        cooling_coil_gross_rated_total_capacity: float | Literal["Autosize"] | None = "Autosize",
        cooling_coil_gross_rated_sensible_heat_ratio: float | Literal["Autosize"] | None = "Autosize",
        cooling_coil_gross_rated_cop: float | None = 3,
        heat_pump_heating_coil_type: Literal["SingleSpeedDXHeatPump"] | None = "SingleSpeedDXHeatPump",
        heat_pump_heating_coil_availability_schedule_name: str | None = ...,
        heat_pump_heating_coil_gross_rated_capacity: float | Literal["Autosize"] | None = "Autosize",
        heat_pump_heating_coil_gross_rated_cop: float | None = 2.75,
        heat_pump_heating_minimum_outdoor_dry_bulb_temperature: float | None = -8,
        heat_pump_defrost_maximum_outdoor_dry_bulb_temperature: float | None = 5,
        heat_pump_defrost_strategy: Literal["Resistive", "ReverseCycle"] | None = "ReverseCycle",
        heat_pump_defrost_control: Literal["OnDemand", "Timed"] | None = "Timed",
        heat_pump_defrost_time_period_fraction: float | None = 0.058333,
        supplemental_heating_coil_type: Literal["Electric", "Gas", "HotWater"] | None = "Electric",
        supplemental_heating_coil_availability_schedule_name: str | None = ...,
        supplemental_heating_coil_capacity: float | Literal["Autosize"] | None = "Autosize",
        supplemental_heating_coil_maximum_outdoor_dry_bulb_temperature: float | None = 21,
        supplemental_gas_heating_coil_efficiency: float | None = 0.8,
        supplemental_gas_heating_coil_parasitic_electric_load: float | None = 0,
        dedicated_outdoor_air_system_name: str | None = ...,
        zone_cooling_design_supply_air_temperature_input_method: Literal[
            "SupplyAirTemperature", "TemperatureDifference"
        ]
        | None = "SupplyAirTemperature",
        zone_cooling_design_supply_air_temperature: float | None = 14,
        zone_cooling_design_supply_air_temperature_difference: float | None = 11.11,
        zone_heating_design_supply_air_temperature_input_method: Literal[
            "SupplyAirTemperature", "TemperatureDifference"
        ]
        | None = "SupplyAirTemperature",
        zone_heating_design_supply_air_temperature: float | None = 50,
        zone_heating_design_supply_air_temperature_difference: float | None = 30,
        design_specification_outdoor_air_object_name: str | None = ...,
        design_specification_zone_air_distribution_object_name: str | None = ...,
        baseboard_heating_type: Literal["Electric", "HotWater", "None"] | None = "None",
        baseboard_heating_availability_schedule_name: str | None = ...,
        baseboard_heating_capacity: float | Literal["Autosize"] | None = "Autosize",
        capacity_control_method: Literal["None", "SingleZoneVAV"] | None = "None",
    ) -> None:
        """Create a new ``HVACTemplate:Zone:PTHP`` and add it to the document.

        Packaged Terminal Heat Pump

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/hvac-template-objects/group-hvac-templates/#hvactemplatezonepthp
        """

class HVACTemplateSystemDualDuct:
    def __call__(
        self,
        name: str,
        /,
        *,
        system_availability_schedule_name: str | None = ...,
        system_configuration_type: Literal[
            "DualFanConstantVolume", "DualFanVariableVolume", "SingleFanConstantVolume", "SingleFanVariableVolume"
        ]
        | None = "SingleFanConstantVolume",
        main_supply_fan_maximum_flow_rate: float | Literal["Autosize"] | None = "Autosize",
        main_supply_fan_minimum_flow_fraction: float | None = 0.2,
        main_supply_fan_total_efficiency: float | None = 0.7,
        main_supply_fan_delta_pressure: float | None = 1000,
        main_supply_fan_motor_efficiency: float | None = 0.9,
        main_supply_fan_motor_in_air_stream_fraction: float | None = 1,
        main_supply_fan_part_load_power_coefficients: Literal[
            "ASHRAE90.1-2004AppendixG",
            "InletVaneDampers",
            "OutletDampers",
            "VariableSpeedMotor",
            "VariableSpeedMotorPressureReset",
        ]
        | None = "InletVaneDampers",
        cold_duct_supply_fan_maximum_flow_rate: float | Literal["Autosize"] | None = "Autosize",
        cold_duct_supply_fan_minimum_flow_fraction: float | None = 0.2,
        cold_duct_supply_fan_total_efficiency: float | None = 0.7,
        cold_duct_supply_fan_delta_pressure: float | None = 1000,
        cold_duct_supply_fan_motor_efficiency: float | None = 0.9,
        cold_duct_supply_fan_motor_in_air_stream_fraction: float | None = 1,
        cold_duct_supply_fan_part_load_power_coefficients: Literal[
            "ASHRAE90.1-2004AppendixG",
            "InletVaneDampers",
            "OutletDampers",
            "VariableSpeedMotor",
            "VariableSpeedMotorPressureReset",
        ]
        | None = "InletVaneDampers",
        cold_duct_supply_fan_placement: Literal["BlowThrough", "DrawThrough"] | None = "DrawThrough",
        hot_duct_supply_fan_maximum_flow_rate: float | Literal["Autosize"] | None = "Autosize",
        hot_duct_supply_fan_minimum_flow_fraction: float | None = 0.2,
        hot_duct_supply_fan_total_efficiency: float | None = 0.7,
        hot_duct_supply_fan_delta_pressure: float | None = 1000,
        hot_duct_supply_fan_motor_efficiency: float | None = 0.9,
        hot_duct_supply_fan_motor_in_air_stream_fraction: float | None = 1,
        hot_duct_supply_fan_part_load_power_coefficients: Literal[
            "ASHRAE90.1-2004AppendixG",
            "InletVaneDampers",
            "OutletDampers",
            "VariableSpeedMotor",
            "VariableSpeedMotorPressureReset",
        ]
        | None = "InletVaneDampers",
        hot_duct_supply_fan_placement: Literal["BlowThrough", "DrawThrough"] | None = "DrawThrough",
        cooling_coil_type: Literal["ChilledWater", "ChilledWaterDetailedFlatModel", "None"] | None = "ChilledWater",
        cooling_coil_availability_schedule_name: str | None = ...,
        cooling_coil_setpoint_control_type: Literal[
            "FixedSetpoint", "OutdoorAirTemperatureReset", "Scheduled", "Warmest"
        ]
        | None = "FixedSetpoint",
        cooling_coil_design_setpoint_temperature: float | None = 12.8,
        cooling_coil_setpoint_schedule_name: str | None = ...,
        cooling_coil_setpoint_at_outdoor_dry_bulb_low: float | None = 15.6,
        cooling_coil_reset_outdoor_dry_bulb_low: float | None = 15.6,
        cooling_coil_setpoint_at_outdoor_dry_bulb_high: float | None = 12.8,
        cooling_coil_reset_outdoor_dry_bulb_high: float | None = 23.3,
        heating_coil_type: Literal["Electric", "Gas", "HotWater", "None"] | None = "HotWater",
        heating_coil_availability_schedule_name: str | None = ...,
        heating_coil_setpoint_control_type: Literal[
            "Coldest", "FixedSetpoint", "OutdoorAirTemperatureReset", "Scheduled"
        ]
        | None = "FixedSetpoint",
        heating_coil_design_setpoint: float | None = 50,
        heating_coil_setpoint_schedule_name: str | None = ...,
        heating_coil_setpoint_at_outdoor_dry_bulb_low: float | None = 50,
        heating_coil_reset_outdoor_dry_bulb_low: float | None = 7.8,
        heating_coil_setpoint_at_outdoor_dry_bulb_high: float | None = 20,
        heating_coil_reset_outdoor_dry_bulb_high: float | None = 12.2,
        heating_coil_capacity: float | Literal["Autosize"] | None = "Autosize",
        gas_heating_coil_efficiency: float | None = 0.8,
        gas_heating_coil_parasitic_electric_load: float | None = 0,
        preheat_coil_type: Literal["Electric", "Gas", "HotWater", "None"] | None = "None",
        preheat_coil_availability_schedule_name: str | None = ...,
        preheat_coil_design_setpoint: float | None = 7.2,
        preheat_coil_setpoint_schedule_name: str | None = ...,
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
        cold_supply_plenum_name: str | None = ...,
        hot_supply_plenum_name: str | None = ...,
        return_plenum_name: str | None = ...,
        night_cycle_control: Literal["CycleOnAny", "CycleOnControlZone", "StayOff"] | None = "StayOff",
        night_cycle_control_zone_name: str | None = ...,
        heat_recovery_type: Literal["Enthalpy", "None", "Sensible"] | None = "None",
        sensible_heat_recovery_effectiveness: float | None = 0.7,
        latent_heat_recovery_effectiveness: float | None = 0.65,
        heat_recovery_heat_exchanger_type: Literal["Plate", "Rotary"] | None = "Plate",
        heat_recovery_frost_control_type: Literal[
            "ExhaustAirRecirculation", "ExhaustOnly", "MinimumExhaustTemperature", "None"
        ]
        | None = "None",
        dehumidification_control_type: Literal["CoolReheat", "None"] | None = "None",
        dehumidification_control_zone_name: str | None = ...,
        dehumidification_relative_humidity_setpoint: float | None = 60,
        dehumidification_relative_humidity_setpoint_schedule_name: str | None = ...,
        humidifier_type: Literal["ElectricSteam", "None"] | None = "None",
        humidifier_availability_schedule_name: str | None = ...,
        humidifier_rated_capacity: float | None = ...,
        humidifier_rated_electric_power: float | Literal["Autosize"] | None = "Autosize",
        humidifier_control_zone_name: str | None = ...,
        humidifier_relative_humidity_setpoint: float | None = 30,
        humidifier_relative_humidity_setpoint_schedule_name: str | None = ...,
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
        """Create a new ``HVACTemplate:System:DualDuct`` and add it to the document.

        Dual-duct constant volume or variable volume air loop

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/hvac-template-objects/group-hvac-templates/#hvactemplatesystemdualduct
        """

class ZoneHVACBaseboardRadiantConvectiveWaterDesign:
    def __call__(
        self,
        name: str,
        /,
        *,
        fraction_radiant: float,
        heating_design_capacity_method: Literal[
            "CapacityPerFloorArea", "FractionOfAutosizedHeatingCapacity", "HeatingDesignCapacity"
        ]
        | None = "HeatingDesignCapacity",
        heating_design_capacity_per_floor_area: float | None = ...,
        fraction_of_autosized_heating_design_capacity: float | None = 1,
        convergence_tolerance: float | None = 0.001,
        fraction_of_radiant_energy_incident_on_people: float | None = ...,
    ) -> None:
        """Create a new ``ZoneHVAC:Baseboard:RadiantConvective:Water:Design`` and add it to the document.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-radiative-convective-units/#zonehvacbaseboardradiantconvectivewaterdesign
        """

class ChillerElectric:
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
        design_condenser_fluid_flow_rate: float | Literal["Autosize"] | None = ...,
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
        chiller_flow_mode: Literal["ConstantFlow", "LeavingSetpointModulated", "NotModulated"] | None = "NotModulated",
        design_heat_recovery_water_flow_rate: float | Literal["Autosize"] | None = 0,
        heat_recovery_inlet_node_name: str | None = ...,
        heat_recovery_outlet_node_name: str | None = ...,
        sizing_factor: float | None = 1,
        basin_heater_capacity: float | None = 0,
        basin_heater_setpoint_temperature: float | None = 2,
        basin_heater_operating_schedule_name: str | None = ...,
        condenser_heat_recovery_relative_capacity_fraction: float | None = ...,
        heat_recovery_inlet_high_temperature_limit_schedule_name: str | None = ...,
        heat_recovery_leaving_temperature_setpoint_node_name: str | None = ...,
        end_use_subcategory: str | None = "General",
        thermosiphon_capacity_fraction_curve_name: str | None = ...,
        thermosiphon_minimum_temperature_difference: float | None = 0,
    ) -> None:
        """Create a new ``Chiller:Electric`` and add it to the document.

        This chiller model is the empirical model from the Building Loads and System Thermodynamics (BLAST) program. Chiller performance curves are generated by fitting catalog data to third order polynomial equations. Three sets of coefficients are required.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/energyplus-economics/cost-estimating/#chillerelectric
        """

class CoolingTowerVariableSpeedMerkel:
    def __call__(
        self,
        name: str,
        /,
        *,
        water_inlet_node_name: str,
        water_outlet_node_name: str,
        design_water_flow_rate: float | Literal["Autosize"],
        design_air_flow_rate: float | Literal["Autocalculate"],
        design_fan_power: float | Literal["Autocalculate"],
        fan_power_modifier_function_of_air_flow_rate_ratio_curve_name: str,
        u_factor_times_area_modifier_function_of_air_flow_ratio_curve_name: str,
        u_factor_times_area_modifier_function_of_wetbulb_temperature_difference_curve_name: str,
        u_factor_times_area_modifier_function_of_water_flow_ratio_curve_name: str,
        performance_input_method: Literal["NominalCapacity", "UFactorTimesAreaAndDesignWaterFlowRate"]
        | None = "NominalCapacity",
        heat_rejection_capacity_and_nominal_capacity_sizing_ratio: float | None = 1.25,
        nominal_capacity: float | Literal["Autosize"] | None = ...,
        free_convection_nominal_capacity: float | Literal["Autocalculate"] | None = ...,
        free_convection_nominal_capacity_sizing_factor: float | None = 0.1,
        design_water_flow_rate_per_unit_of_nominal_capacity: float | None = ...,
        design_air_flow_rate_per_unit_of_nominal_capacity: float | None = ...,
        minimum_air_flow_rate_ratio: float | None = 0.2,
        design_fan_power_per_unit_of_nominal_capacity: float | None = 0.0105,
        free_convection_regime_air_flow_rate: float | Literal["Autocalculate"] | None = 0,
        free_convection_regime_air_flow_rate_sizing_factor: float | None = 0.1,
        design_air_flow_rate_u_factor_times_area_value: float | Literal["Autosize"] | None = ...,
        free_convection_regime_u_factor_times_area_value: float | Literal["Autocalculate"] | None = 0,
        free_convection_u_factor_times_area_value_sizing_factor: float | None = 0.1,
        design_inlet_air_dry_bulb_temperature: float | None = 35,
        design_inlet_air_wet_bulb_temperature: float | None = 25.6,
        design_approach_temperature: float | Literal["Autosize"] | None = "Autosize",
        design_range_temperature: float | Literal["Autosize"] | None = "Autosize",
        basin_heater_capacity: float | None = 0,
        basin_heater_setpoint_temperature: float | None = 2,
        basin_heater_operating_schedule_name: str | None = ...,
        evaporation_loss_mode: Literal["LossFactor", "SaturatedExit"] | None = "SaturatedExit",
        evaporation_loss_factor: float | None = 0.2,
        drift_loss_percent: float | None = 0.008,
        blowdown_calculation_mode: Literal["ConcentrationRatio", "ScheduledRate"] | None = "ConcentrationRatio",
        blowdown_concentration_ratio: float | None = 3,
        blowdown_makeup_water_usage_schedule_name: str | None = ...,
        supply_water_storage_tank_name: str | None = ...,
        outdoor_air_inlet_node_name: str | None = ...,
        number_of_cells: int | None = 1,
        cell_control: Literal["MaximalCell", "MinimalCell"] | None = "MaximalCell",
        cell_minimum_water_flow_rate_fraction: float | None = 0.33,
        cell_maximum_water_flow_rate_fraction: float | None = 2.5,
        sizing_factor: float | None = 1,
        end_use_subcategory: str | None = "General",
    ) -> None:
        """Create a new ``CoolingTower:VariableSpeed:Merkel`` and add it to the document.

        This tower model is based on Merkel's theory, which is also the basis for the tower model in ASHRAE's HVAC1 Toolkit. The open wet cooling tower is modeled as a counter flow heat exchanger with a variable-speed fan drawing air through the tower (induced-draft configuration). For a multi-cell tower, the capacity and air/water flow rate inputs are for the entire tower.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-condenser-equipment/#coolingtowervariablespeedmerkel
        """

class AnyThermalStorageIceDetailed:
    def __call__(
        self,
        name: str,
        /,
        *,
        narrow_with_as_version_first: Never,
        capacity: float,
        inlet_node_name: str,
        outlet_node_name: str,
        discharging_curve_name: str,
        charging_curve_name: str,
        availability_schedule_name: str | None = ...,
        timestep_of_the_curve_data: float | None = ...,
        parasitic_electric_load_during_discharging: float | None = ...,
        parasitic_electric_load_during_charging: float | None = ...,
        tank_loss_coefficient: float | None = ...,
        freezing_temperature_of_storage_medium: float | None = 0,
        thaw_process_indicator: Literal["InsideMelt", "OutsideMelt"] | None = "OutsideMelt",
    ) -> None:
        """Create a new ``ThermalStorage:Ice:Detailed`` and add it to the document.

        This input syntax is intended to describe a thermal storage system that includes smaller containers filled with water that are placed in a larger tank or series of tanks. The model uses polynomial equations to describe the system performance.

        No call suits every release: narrow the document with ``as_version`` first.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-water-heaters/#thermalstorageicedetailed
        """

class RefrigerationCondenserEvaporativeCooled:
    def __call__(
        self,
        name: str,
        /,
        *,
        rated_effective_total_heat_rejection_rate: float,
        rated_fan_power: float,
        rated_subcooling_temperature_difference: float | None = 0,
        fan_speed_control_type: Literal["Fixed", "FixedLinear", "TwoSpeed", "VariableSpeed"] | None = "Fixed",
        minimum_fan_air_flow_ratio: float | None = 0.2,
        approach_temperature_constant_term: float | None = 6.63,
        approach_temperature_coefficient_2: float | None = 0.468,
        approach_temperature_coefficient_3: float | None = 17.93,
        approach_temperature_coefficient_4: float | None = -0.322,
        minimum_capacity_factor: float | None = 0.5,
        maximum_capacity_factor: float | None = 5,
        air_inlet_node_name: str | None = ...,
        rated_air_flow_rate: float | Literal["Autocalculate"] | None = "Autocalculate",
        basin_heater_capacity: float | None = 200,
        basin_heater_setpoint_temperature: float | None = 2,
        rated_water_pump_power: float | Literal["Autocalculate"] | None = 1000,
        evaporative_water_supply_tank_name: str | None = ...,
        evaporative_condenser_availability_schedule_name: str | None = ...,
        end_use_subcategory: str | None = "General",
        condenser_refrigerant_operating_charge_inventory: float | None = 0,
        condensate_receiver_refrigerant_inventory: float | None = 0,
        condensate_piping_refrigerant_inventory: float | None = 0,
    ) -> None:
        """Create a new ``Refrigeration:Condenser:EvaporativeCooled`` and add it to the document.

        Evaporative-cooled condenser for a refrigeration system (Refrigeration:System).

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-refrigeration/#refrigerationcondenserevaporativecooled
        """

class ParametricSetValueForRun:
    def __call__(
        self,
        name: str,
        /,
        *,
        values: Sequence[_g.ParametricSetValueForRunValuesItem | _g.ParametricSetValueForRunValuesGroup] = ...,
    ) -> None:
        """Create a new ``Parametric:SetValueForRun`` and add it to the document.

        Parametric objects allow a set of multiple simulations to be defined in a single idf file. The parametric preprocessor scans the idf for Parametric:* objects then creates and runs multiple idf files, one for each defined simulation. The core parametric object is Parametric:SetValueForRun which defines the name of a parameter and sets the parameter to different values depending on which run is being simulated.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/parametric-objects/#parametricsetvalueforrun
        """

class AnyOutputTableSummaryReports:
    def __call__(
        self,
        this_type_has_no_name_field: _g._PassFieldsAsKeywords = ...,
        /,
        *,
        reports: Sequence[
            _g.AnyOutputTableSummaryReportsReportsItem | _g.AnyOutputTableSummaryReportsReportsGroup
        ] = ...,
    ) -> None:
        """Create a new ``Output:Table:SummaryReports`` and add it to the document.

        This object allows the user to call report types that are predefined and will appear with the other tabular reports. These predefined reports are sensitive to the OutputControl:Table:Style object and appear in the same files as the tabular reports. The entries for this object is a list of the predefined reports that should appear in the tabular report output file.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/standard-output-reports/output-table-summaryreports/#outputtablesummaryreports
        """

class AnyOutputTableTimeBins:
    def __call__(
        self,
        this_type_has_no_name_field: _g._PassFieldsAsKeywords = ...,
        /,
        *,
        variable_name: str,
        key_value: str | None = "*",
        interval_start: float | None = ...,
        interval_size: float | None = ...,
        interval_count: int | None = ...,
        schedule_name: str | None = ...,
        variable_type: Literal["Energy", "Power", "Temperature", "VolumetricFlow"] | None = ...,
    ) -> None:
        """Create a new ``Output:Table:TimeBins`` and add it to the document.

        Produces a bin report in the table output file which shows the amount of time in hours that occurs in different bins for a single specific output variable or meter. Two different types of binning are reported: by month and by hour of the day.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/standard-output-reports/output-table-timebins/#outputtabletimebins
        """
