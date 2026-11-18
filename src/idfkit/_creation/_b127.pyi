"""Creation signatures of generated classes (stub only).

DO NOT EDIT — regenerate with:
    python -m idfkit.codegen.generate_stubs
"""

from __future__ import annotations

from collections.abc import Sequence
from typing import Literal

from typing_extensions import Never

from .. import _generated_types as _g

class AirflowNetworkDistributionComponentOutdoorAirFlow:
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
        """Create a new ``AirflowNetwork:Distribution:Component:OutdoorAirFlow`` and add it to the document.

        This object includes the outdoor air flow rate set by the Controller:OutdoorAir object in the airflow network.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-airflow-network/#airflownetworkdistributioncomponentoutdoorairflow
        """

class AnyZoneHVACIdealLoadsAirSystem:
    def __call__(
        self,
        name: str,
        /,
        *,
        zone_supply_air_node_name: str,
        availability_schedule_name: str | None = ...,
        zone_exhaust_air_node_name: str | None = ...,
        system_inlet_air_node_name: str | None = ...,
        maximum_heating_supply_air_temperature: float | None = 50,
        minimum_cooling_supply_air_temperature: float | None = 13,
        maximum_heating_supply_air_humidity_ratio: float | None = 0.0156,
        minimum_cooling_supply_air_humidity_ratio: float | None = 0.0077,
        heating_limit: Literal["", "LimitCapacity", "LimitFlowRate", "LimitFlowRateAndCapacity", "NoLimit"]
        | None = "NoLimit",
        maximum_heating_air_flow_rate: float | Literal["Autosize"] | None = ...,
        maximum_sensible_heating_capacity: float | Literal["Autosize"] | None = ...,
        cooling_limit: Literal["", "LimitCapacity", "LimitFlowRate", "LimitFlowRateAndCapacity", "NoLimit"]
        | None = "NoLimit",
        maximum_cooling_air_flow_rate: float | Literal["Autosize"] | None = ...,
        maximum_total_cooling_capacity: float | Literal["Autosize"] | None = ...,
        heating_availability_schedule_name: str | None = ...,
        cooling_availability_schedule_name: str | None = ...,
        dehumidification_control_type: Literal[
            "", "ConstantSensibleHeatRatio", "ConstantSupplyHumidityRatio", "Humidistat", "None"
        ]
        | None = "ConstantSensibleHeatRatio",
        cooling_sensible_heat_ratio: float | None = 0.7,
        humidification_control_type: Literal["", "ConstantSupplyHumidityRatio", "Humidistat", "None"] | None = "None",
        design_specification_outdoor_air_object_name: str | None = ...,
        outdoor_air_inlet_node_name: str | None = ...,
        demand_controlled_ventilation_type: Literal["", "CO2Setpoint", "None", "OccupancySchedule"] | None = "None",
        outdoor_air_economizer_type: Literal["", "DifferentialDryBulb", "DifferentialEnthalpy", "NoEconomizer"]
        | None = "NoEconomizer",
        heat_recovery_type: Literal["", "Enthalpy", "None", "Sensible"] | None = "None",
        sensible_heat_recovery_effectiveness: float | None = 0.7,
        latent_heat_recovery_effectiveness: float | None = 0.65,
        design_specification_zonehvac_sizing_object_name: str | None = ...,
    ) -> None:
        """Create a new ``ZoneHVAC:IdealLoadsAirSystem`` and add it to the document.

        Ideal system used to calculate loads without modeling a full HVAC system. All that is required for the ideal system are zone controls, zone equipment configurations, and the ideal loads system component. This component can be thought of as an ideal unit that mixes zone air with the specified amount of outdoor air and then adds or removes heat and moisture at 100% efficiency in order to meet the specified controls. Energy use is reported as DistrictHeatingWater and DistrictCooling.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-zone-forced-air-units/#zonehvacidealloadsairsystem
        """

class AnyZoneHVACBaseboardRadiantConvectiveSteam:
    def __call__(
        self,
        name: str,
        /,
        *,
        narrow_with_as_version_first: Never,
        inlet_node_name: str,
        outlet_node_name: str,
        maximum_steam_flow_rate: float | Literal["Autosize"],
        availability_schedule_name: str | None = ...,
        heating_design_capacity: float | Literal["", "Autosize"] | None = "Autosize",
        degree_of_subcooling: float | None = 5,
        surface_fractions: Sequence[
            _g.ZoneHVACBaseboardRadiantConvectiveSteamSurfaceFractionsItem
            | _g.ZoneHVACBaseboardRadiantConvectiveSteamSurfaceFractionsGroup
        ] = ...,
    ) -> None:
        """Create a new ``ZoneHVAC:Baseboard:RadiantConvective:Steam`` and add it to the document.

        The number of surfaces can be expanded beyond 100, if necessary, by adding more groups to the end of the list.

        No call suits every release: narrow the document with ``as_version`` first.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-radiative-convective-units/#zonehvacbaseboardradiantconvectivesteam
        """

class CoilCoolingDXTwoSpeed:
    def __call__(
        self,
        name: str,
        /,
        *,
        high_speed_gross_rated_total_cooling_capacity: float | Literal["Autosize"],
        high_speed_rated_sensible_heat_ratio: float | Literal["Autosize"],
        high_speed_rated_air_flow_rate: float | Literal["Autosize"],
        air_inlet_node_name: str,
        air_outlet_node_name: str,
        total_cooling_capacity_function_of_temperature_curve_name: str,
        total_cooling_capacity_function_of_flow_fraction_curve_name: str,
        energy_input_ratio_function_of_temperature_curve_name: str,
        energy_input_ratio_function_of_flow_fraction_curve_name: str,
        part_load_fraction_correlation_curve_name: str,
        low_speed_gross_rated_total_cooling_capacity: float | Literal["Autosize"],
        low_speed_gross_rated_sensible_heat_ratio: float | Literal["Autosize"],
        low_speed_rated_air_flow_rate: float | Literal["Autosize"],
        low_speed_total_cooling_capacity_function_of_temperature_curve_name: str,
        low_speed_energy_input_ratio_function_of_temperature_curve_name: str,
        availability_schedule_name: str | None = ...,
        high_speed_gross_rated_cooling_cop: float | None = 3,
        high_speed_2017_rated_evaporator_fan_power_per_volume_flow_rate: float | None = 773.3,
        high_speed_2023_rated_evaporator_fan_power_per_volume_flow_rate: float | None = 934.4,
        unit_internal_static_air_pressure: float | None = ...,
        low_speed_gross_rated_cooling_cop: float | None = 3,
        low_speed_2017_rated_evaporator_fan_power_per_volume_flow_rate: float | None = 773.3,
        low_speed_2023_rated_evaporator_fan_power_per_volume_flow_rate: float | None = 934.4,
        condenser_air_inlet_node_name: str | None = ...,
        condenser_type: Literal["", "AirCooled", "EvaporativelyCooled"] | None = "AirCooled",
        minimum_outdoor_dry_bulb_temperature_for_compressor_operation: float | None = -25,
        high_speed_evaporative_condenser_effectiveness: float | None = 0.9,
        high_speed_evaporative_condenser_air_flow_rate: float | Literal["Autosize"] | None = ...,
        high_speed_evaporative_condenser_pump_rated_power_consumption: float | Literal["Autosize"] | None = ...,
        low_speed_evaporative_condenser_effectiveness: float | None = 0.9,
        low_speed_evaporative_condenser_air_flow_rate: float | Literal["Autosize"] | None = ...,
        low_speed_evaporative_condenser_pump_rated_power_consumption: float | Literal["Autosize"] | None = ...,
        supply_water_storage_tank_name: str | None = ...,
        condensate_collection_water_storage_tank_name: str | None = ...,
        basin_heater_capacity: float | None = 0,
        basin_heater_setpoint_temperature: float | None = 2,
        basin_heater_operating_schedule_name: str | None = ...,
        sensible_heat_ratio_function_of_temperature_curve_name: str | None = ...,
        sensible_heat_ratio_function_of_flow_fraction_curve_name: str | None = ...,
        low_speed_sensible_heat_ratio_function_of_temperature_curve_name: str | None = ...,
        low_speed_sensible_heat_ratio_function_of_flow_fraction_curve_name: str | None = ...,
        zone_name_for_condenser_placement: str | None = ...,
    ) -> None:
        """Create a new ``Coil:Cooling:DX:TwoSpeed`` and add it to the document.

        Direct expansion (DX) cooling coil and condensing unit (includes electric compressor and condenser fan), two-speed (or variable-speed). Requires two sets of performance data and will interpolate between speeds. Modeled as a single coil (multi-speed compressor or multiple compressors with row split or intertwined coil).

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-heating-and-cooling-coils/#coilcoolingdxtwospeed
        """

class AnyCoolingTowerVariableSpeed:
    def __call__(
        self,
        name: str,
        /,
        *,
        water_inlet_node_name: str,
        water_outlet_node_name: str,
        design_water_flow_rate: float | Literal["Autosize"],
        design_air_flow_rate: float | Literal["Autosize"],
        design_fan_power: float | Literal["Autosize"],
        model_type: Literal["", "CoolToolsCrossFlow", "CoolToolsUserDefined", "YorkCalc", "YorkCalcUserDefined"]
        | None = "YorkCalc",
        model_coefficient_name: str | None = ...,
        design_inlet_air_wet_bulb_temperature: float | None = 25.6,
        design_approach_temperature: float | None = 3.9,
        design_range_temperature: float | None = 5.6,
        fan_power_ratio_function_of_air_flow_rate_ratio_curve_name: str | None = ...,
        minimum_air_flow_rate_ratio: float | None = 0.2,
        fraction_of_tower_capacity_in_free_convection_regime: float | None = 0.125,
        basin_heater_capacity: float | None = 0,
        basin_heater_setpoint_temperature: float | None = 2,
        basin_heater_operating_schedule_name: str | None = ...,
        evaporation_loss_mode: Literal["LossFactor", "SaturatedExit"] | None = ...,
        evaporation_loss_factor: float | None = 0.2,
        drift_loss_percent: float | None = ...,
        blowdown_calculation_mode: Literal["ConcentrationRatio", "ScheduledRate"] | None = ...,
        blowdown_concentration_ratio: float | None = 3,
        blowdown_makeup_water_usage_schedule_name: str | None = ...,
        supply_water_storage_tank_name: str | None = ...,
        outdoor_air_inlet_node_name: str | None = ...,
        number_of_cells: int | None = 1,
        cell_control: Literal["", "MaximalCell", "MinimalCell"] | None = ...,
        cell_minimum_water_flow_rate_fraction: float | None = 0.33,
        cell_maximum_water_flow_rate_fraction: float | None = 2.5,
        sizing_factor: float | None = 1,
        end_use_subcategory: str | None = "General",
    ) -> None:
        """Create a new ``CoolingTower:VariableSpeed`` and add it to the document.

        This open wet tower model is based on purely empirical algorithms derived from manufacturer's performance data or field measurements. The user can select from two existing algorithms (CoolTools or YorkCalc), or they can enter their own correlation for approach temperature by using a variable speed tower model coefficient object. For a multi-cell tower, the capacity and air/water flow rate inputs are for the entire tower.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-condenser-equipment/#coolingtowervariablespeed
        """

class FaultModelThermostatOffset:
    def __call__(
        self,
        name: str,
        /,
        *,
        thermostat_name: str,
        availability_schedule_name: str | None = ...,
        severity_schedule_name: str | None = ...,
        reference_thermostat_offset: float | None = 2,
    ) -> None:
        """Create a new ``FaultModel:ThermostatOffset`` and add it to the document.

        This object describes fault of thermostat offset

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-operational-faults/#faultmodelthermostatoffset
        """

class AnyMatrixTwoDimension:
    def __call__(
        self,
        name: str,
        /,
        *,
        number_of_rows: int,
        number_of_columns: int,
        values: Sequence[_g.MatrixTwoDimensionValuesItem | _g.MatrixTwoDimensionValuesGroup] = ...,
    ) -> None:
        """Create a new ``Matrix:TwoDimension`` and add it to the document.

        matrix data in row-major order list each row keeping the columns in order number of values must equal N1 x N2

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-surface-construction-elements/#matrixtwodimension
        """
