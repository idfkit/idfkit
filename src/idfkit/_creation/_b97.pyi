"""Creation signatures of generated classes (stub only).

DO NOT EDIT — regenerate with:
    python -m idfkit.codegen.generate_stubs
"""

from __future__ import annotations

from collections.abc import Sequence
from typing import Literal

from typing_extensions import Never

from .. import _generated_types as _g

class SiteGroundTemperatureDeep:
    def __call__(
        self,
        this_type_has_no_name_field: _g._PassFieldsAsKeywords = ...,
        /,
        *,
        january_deep_ground_temperature: float | None = 16,
        february_deep_ground_temperature: float | None = 16,
        march_deep_ground_temperature: float | None = 16,
        april_deep_ground_temperature: float | None = 16,
        may_deep_ground_temperature: float | None = 16,
        june_deep_ground_temperature: float | None = 16,
        july_deep_ground_temperature: float | None = 16,
        august_deep_ground_temperature: float | None = 16,
        september_deep_ground_temperature: float | None = 16,
        october_deep_ground_temperature: float | None = 16,
        november_deep_ground_temperature: float | None = 16,
        december_deep_ground_temperature: float | None = 16,
        validate: bool = True,
    ) -> None:
        """Create a new ``Site:GroundTemperature:Deep`` and add it to the document.

        These temperatures are specifically for the ground heat exchangers that would use 'deep' (3-4 m depth) ground temperatures for their heat source. They are not used in other models.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-location-climate-weather-file-access/#sitegroundtemperaturedeep
        """

class RoomAirNodeAirflowNetworkAdjacentSurfaceList:
    def __call__(
        self,
        name: str = "",
        /,
        *,
        surfaces: Sequence[
            _g.RoomAirNodeAirflowNetworkAdjacentSurfaceListSurfacesItem
            | _g.RoomAirNodeAirflowNetworkAdjacentSurfaceListSurfacesGroup
        ] = ...,
        validate: bool = True,
    ) -> None:
        """Create a new ``RoomAir:Node:AirflowNetwork:AdjacentSurfaceList`` and add it to the document.

        ``surfaces`` takes the extensible groups in order, one dict per group:

        ```python
        doc["RoomAir:Node:AirflowNetwork:AdjacentSurfaceList"].add(
            "RoomAir Node AirflowNetwork AdjacentSurfaceList 1",
            surfaces=[
                {"surface_name": "Surface 1"},
                {"surface_name": "Surface 2"},
            ],
        )
        ```

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-room-air-models/#roomairnodeairflownetworkadjacentsurfacelist
        """

class AnyAirflowNetworkDistributionComponentOutdoorAirFlow:
    def __call__(
        self,
        name: str,
        /,
        *,
        narrow_with_as_version_first: Never,
        air_mass_flow_coefficient_when_no_outdoor_air_flow_at_reference_conditions: float,
        air_mass_flow_exponent_when_no_outdoor_air_flow: float | None = 0.65,
        reference_crack_conditions: str | None = ...,
        validate: bool = True,
    ) -> None:
        """Create a new ``AirflowNetwork:Distribution:Component:OutdoorAirFlow`` and add it to the document.

        This object includes the outdoor air flow rate set by the Controller:OutdoorAir object in the airflow network.

        No call suits every release: narrow the document with ``as_version`` first.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-airflow-network/#airflownetworkdistributioncomponentoutdoorairflow
        """

class HVACTemplateSystemUnitarySystem:
    def __call__(
        self,
        name: str,
        /,
        *,
        system_availability_schedule_name: str | None = ...,
        control_type: Literal["Load", "SetPoint"] | None = "Load",
        control_zone_or_thermostat_location_name: str | None = ...,
        cooling_supply_air_flow_rate: float | Literal["Autosize"] | None = "Autosize",
        heating_supply_air_flow_rate: float | Literal["Autosize"] | None = "Autosize",
        no_load_supply_air_flow_rate: float | Literal["Autosize"] | None = "Autosize",
        supply_fan_operating_mode_schedule_name: str | None = ...,
        supply_fan_placement: Literal["BlowThrough", "DrawThrough"] | None = "BlowThrough",
        supply_fan_total_efficiency: float | None = 0.7,
        supply_fan_delta_pressure: float | None = 600,
        supply_fan_motor_efficiency: float | None = 0.9,
        supply_fan_motor_in_air_stream_fraction: float | None = 1,
        cooling_coil_type: Literal[
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
        number_of_speeds_for_cooling: int | None = 1,
        cooling_coil_availability_schedule_name: str | None = ...,
        cooling_design_supply_air_temperature: float | None = 12.8,
        dx_cooling_coil_gross_rated_total_capacity: float | Literal["Autosize"] | None = "Autosize",
        dx_cooling_coil_gross_rated_sensible_heat_ratio: float | Literal["Autosize"] | None = "Autosize",
        dx_cooling_coil_gross_rated_cop: float | None = 3,
        heating_coil_type: Literal[
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
        number_of_speeds_or_stages_for_heating: int | None = 1,
        heating_coil_availability_schedule_name: str | None = ...,
        heating_design_supply_air_temperature: float | None = 50,
        heating_coil_gross_rated_capacity: float | Literal["Autosize"] | None = "Autosize",
        gas_heating_coil_efficiency: float | None = 0.8,
        gas_heating_coil_parasitic_electric_load: float | None = 0,
        heat_pump_heating_coil_gross_rated_cop: float | None = 2.75,
        heat_pump_heating_minimum_outdoor_dry_bulb_temperature: float | None = -8,
        heat_pump_defrost_maximum_outdoor_dry_bulb_temperature: float | None = 5,
        heat_pump_defrost_strategy: Literal["Resistive", "ReverseCycle"] | None = "ReverseCycle",
        heat_pump_defrost_control: Literal["OnDemand", "Timed"] | None = "Timed",
        heat_pump_defrost_time_period_fraction: float | None = 0.058333,
        supplemental_heating_or_reheat_coil_type: Literal["DesuperHeater", "Electric", "Gas", "HotWater", "None"]
        | None = "None",
        supplemental_heating_or_reheat_coil_availability_schedule_name: str | None = ...,
        supplemental_heating_or_reheat_coil_capacity: float | Literal["Autosize"] | None = "Autosize",
        supplemental_heating_or_reheat_coil_maximum_outdoor_dry_bulb_temperature: float | None = 21,
        supplemental_gas_heating_or_reheat_coil_efficiency: float | None = 0.8,
        supplemental_gas_heating_or_reheat_coil_parasitic_electric_load: float | None = 0,
        maximum_outdoor_air_flow_rate: float | Literal["Autosize"] | None = "Autosize",
        minimum_outdoor_air_flow_rate: float | Literal["Autosize"] | None = "Autosize",
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
        economizer_lockout: Literal["LockoutWithCompressor", "LockoutWithHeating", "NoLockout"] | None = "NoLockout",
        economizer_maximum_limit_dry_bulb_temperature: float | None = ...,
        economizer_maximum_limit_enthalpy: float | None = ...,
        economizer_maximum_limit_dewpoint_temperature: float | None = ...,
        economizer_minimum_limit_dry_bulb_temperature: float | None = ...,
        supply_plenum_name: str | None = ...,
        return_plenum_name: str | None = ...,
        heat_recovery_type: Literal["Enthalpy", "None", "Sensible"] | None = "None",
        sensible_heat_recovery_effectiveness: float | None = 0.7,
        latent_heat_recovery_effectiveness: float | None = 0.65,
        heat_recovery_heat_exchanger_type: Literal["Plate", "Rotary"] | None = "Plate",
        heat_recovery_frost_control_type: Literal[
            "ExhaustAirRecirculation", "ExhaustOnly", "MinimumExhaustTemperature", "None"
        ]
        | None = "None",
        dehumidification_control_type: Literal["CoolReheat", "Multimode", "None"] | None = "None",
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
        return_fan_delta_pressure: float | None = 300,
        return_fan_motor_efficiency: float | None = 0.9,
        return_fan_motor_in_air_stream_fraction: float | None = 1,
        validate: bool = True,
    ) -> None:
        """Create a new ``HVACTemplate:System:UnitarySystem`` and add it to the document.

        Unitary HVAC system with optional cooling and heating. Supports DX and chilled water, cooling, gas, electric, and hot water heating, air-to-air and water-to-air heat pumps.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/hvac-template-objects/group-hvac-templates/#hvactemplatesystemunitarysystem
        """

class AirTerminalSingleDuctConstantVolumeReheat:
    def __call__(
        self,
        name: str,
        /,
        *,
        air_outlet_node_name: str,
        air_inlet_node_name: str,
        maximum_air_flow_rate: float | Literal["Autosize"],
        reheat_coil_object_type: Literal[
            "Coil:Heating:Electric", "Coil:Heating:Fuel", "Coil:Heating:Steam", "Coil:Heating:Water"
        ],
        reheat_coil_name: str,
        availability_schedule_name: str | None = ...,
        maximum_hot_water_or_steam_flow_rate: float | Literal["Autosize"] | None = ...,
        minimum_hot_water_or_steam_flow_rate: float | None = 0,
        convergence_tolerance: float | None = 0.001,
        maximum_reheat_air_temperature: float | None = ...,
        validate: bool = True,
    ) -> None:
        """Create a new ``AirTerminal:SingleDuct:ConstantVolume:Reheat`` and add it to the document.

        Central air system terminal unit, single duct, constant volume, with reheat coil (hot water, electric, gas, or steam).

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-air-distribution-equipment/#airterminalsingleductconstantvolumereheat
        """

class FanOnOff:
    def __call__(
        self,
        name: str,
        /,
        *,
        pressure_rise: float,
        air_inlet_node_name: str,
        air_outlet_node_name: str,
        availability_schedule_name: str | None = ...,
        fan_total_efficiency: float | None = 0.6,
        maximum_flow_rate: float | Literal["Autosize"] | None = ...,
        motor_efficiency: float | None = 0.8,
        motor_in_airstream_fraction: float | None = 1,
        fan_power_ratio_function_of_speed_ratio_curve_name: str | None = ...,
        fan_efficiency_ratio_function_of_speed_ratio_curve_name: str | None = ...,
        end_use_subcategory: str | None = "General",
        validate: bool = True,
    ) -> None:
        """Create a new ``Fan:OnOff`` and add it to the document.

        Constant volume fan that is intended to cycle on and off based on cooling/heating load or other control signals. This fan can also operate continuously like Fan:ConstantVolume.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-fans/#fanonoff
        """

class CoilCoolingDXMultiSpeed:
    def __call__(
        self,
        name: str,
        /,
        *,
        air_inlet_node_name: str,
        air_outlet_node_name: str,
        fuel_type: Literal[
            "Diesel",
            "Electricity",
            "FuelOilNo1",
            "FuelOilNo2",
            "Gasoline",
            "NaturalGas",
            "OtherFuel1",
            "OtherFuel2",
            "Propane",
        ],
        number_of_speeds: int,
        speed_1_gross_rated_total_cooling_capacity: float | Literal["Autosize"],
        speed_1_gross_rated_sensible_heat_ratio: float | Literal["Autosize"],
        speed_1_rated_air_flow_rate: float | Literal["Autosize"],
        speed_1_total_cooling_capacity_function_of_temperature_curve_name: str,
        speed_1_total_cooling_capacity_function_of_flow_fraction_curve_name: str,
        speed_1_energy_input_ratio_function_of_temperature_curve_name: str,
        speed_1_energy_input_ratio_function_of_flow_fraction_curve_name: str,
        speed_1_part_load_fraction_correlation_curve_name: str,
        speed_2_gross_rated_total_cooling_capacity: float | Literal["Autosize"],
        speed_2_gross_rated_sensible_heat_ratio: float | Literal["Autosize"],
        speed_2_rated_air_flow_rate: float | Literal["Autosize"],
        speed_2_total_cooling_capacity_function_of_temperature_curve_name: str,
        speed_2_total_cooling_capacity_function_of_flow_fraction_curve_name: str,
        speed_2_energy_input_ratio_function_of_temperature_curve_name: str,
        speed_2_energy_input_ratio_function_of_flow_fraction_curve_name: str,
        speed_2_part_load_fraction_correlation_curve_name: str,
        availability_schedule_name: str | None = ...,
        condenser_air_inlet_node_name: str | None = ...,
        condenser_type: Literal["AirCooled", "EvaporativelyCooled"] | None = "AirCooled",
        minimum_outdoor_dry_bulb_temperature_for_compressor_operation: float | None = -25,
        supply_water_storage_tank_name: str | None = ...,
        condensate_collection_water_storage_tank_name: str | None = ...,
        apply_part_load_fraction_to_speeds_greater_than_1: Literal["No", "Yes"] | None = "No",
        apply_latent_degradation_to_speeds_greater_than_1: Literal["No", "Yes"] | None = "No",
        crankcase_heater_capacity: float | None = 0,
        crankcase_heater_capacity_function_of_temperature_curve_name: str | None = ...,
        maximum_outdoor_dry_bulb_temperature_for_crankcase_heater_operation: float | None = 10,
        basin_heater_capacity: float | None = 0,
        basin_heater_setpoint_temperature: float | None = 2,
        basin_heater_operating_schedule_name: str | None = ...,
        speed_1_gross_rated_cooling_cop: float | None = 3,
        speed_1_nominal_time_for_condensate_removal_to_begin: float | None = 0,
        speed_1_ratio_of_initial_moisture_evaporation_rate_and_steady_state_latent_capacity: float | None = 0,
        speed_1_maximum_cycling_rate: float | None = 0,
        speed_1_latent_capacity_time_constant: float | None = 0,
        speed_1_rated_waste_heat_fraction_of_power_input: float | None = 0.2,
        speed_1_waste_heat_function_of_temperature_curve_name: str | None = ...,
        speed_1_evaporative_condenser_effectiveness: float | None = 0.9,
        speed_1_evaporative_condenser_air_flow_rate: float | Literal["Autosize"] | None = ...,
        speed_1_rated_evaporative_condenser_pump_power_consumption: float | Literal["Autosize"] | None = ...,
        speed_2_gross_rated_cooling_cop: float | None = 3,
        speed_2_nominal_time_for_condensate_removal_to_begin: float | None = 0,
        speed_2_ratio_of_initial_moisture_evaporation_rate_and_steady_state_latent_capacity: float | None = 0,
        speed_2_maximum_cycling_rate: float | None = 0,
        speed_2_latent_capacity_time_constant: float | None = 0,
        speed_2_rated_waste_heat_fraction_of_power_input: float | None = 0.2,
        speed_2_waste_heat_function_of_temperature_curve_name: str | None = ...,
        speed_2_evaporative_condenser_effectiveness: float | None = 0.9,
        speed_2_evaporative_condenser_air_flow_rate: float | Literal["Autosize"] | None = ...,
        speed_2_rated_evaporative_condenser_pump_power_consumption: float | Literal["Autosize"] | None = ...,
        speed_3_gross_rated_total_cooling_capacity: float | Literal["Autosize"] | None = ...,
        speed_3_gross_rated_sensible_heat_ratio: float | Literal["Autosize"] | None = ...,
        speed_3_gross_rated_cooling_cop: float | None = 3,
        speed_3_rated_air_flow_rate: float | Literal["Autosize"] | None = ...,
        speed_3_total_cooling_capacity_function_of_temperature_curve_name: str | None = ...,
        speed_3_total_cooling_capacity_function_of_flow_fraction_curve_name: str | None = ...,
        speed_3_energy_input_ratio_function_of_temperature_curve_name: str | None = ...,
        speed_3_energy_input_ratio_function_of_flow_fraction_curve_name: str | None = ...,
        speed_3_part_load_fraction_correlation_curve_name: str | None = ...,
        speed_3_nominal_time_for_condensate_removal_to_begin: float | None = 0,
        speed_3_ratio_of_initial_moisture_evaporation_rate_and_steady_state_latent_capacity: float | None = 0,
        speed_3_maximum_cycling_rate: float | None = 0,
        speed_3_latent_capacity_time_constant: float | None = 0,
        speed_3_rated_waste_heat_fraction_of_power_input: float | None = 0.2,
        speed_3_waste_heat_function_of_temperature_curve_name: str | None = ...,
        speed_3_evaporative_condenser_effectiveness: float | None = 0.9,
        speed_3_evaporative_condenser_air_flow_rate: float | Literal["Autosize"] | None = ...,
        speed_3_rated_evaporative_condenser_pump_power_consumption: float | Literal["Autosize"] | None = ...,
        speed_4_gross_rated_total_cooling_capacity: float | Literal["Autosize"] | None = ...,
        speed_4_gross_rated_sensible_heat_ratio: float | Literal["Autosize"] | None = ...,
        speed_4_gross_rated_cooling_cop: float | None = 3,
        speed_4_rated_air_flow_rate: float | Literal["Autosize"] | None = ...,
        speed_4_total_cooling_capacity_function_of_temperature_curve_name: str | None = ...,
        speed_4_total_cooling_capacity_function_of_flow_fraction_curve_name: str | None = ...,
        speed_4_energy_input_ratio_function_of_temperature_curve_name: str | None = ...,
        speed_4_energy_input_ratio_function_of_flow_fraction_curve_name: str | None = ...,
        speed_4_part_load_fraction_correlation_curve_name: str | None = ...,
        speed_4_nominal_time_for_condensate_removal_to_begin: float | None = 0,
        speed_4_ratio_of_initial_moisture_evaporation_rate_and_steady_state_latent_capacity: float | None = 0,
        speed_4_maximum_cycling_rate: float | None = 0,
        speed_4_latent_capacity_time_constant: float | None = 0,
        speed_4_rated_waste_heat_fraction_of_power_input: float | None = 0.2,
        speed_4_waste_heat_function_of_temperature_curve_name: str | None = ...,
        speed_4_evaporative_condenser_effectiveness: float | None = 0.9,
        speed_4_evaporative_condenser_air_flow_rate: float | Literal["Autosize"] | None = ...,
        speed_4_rated_evaporative_condenser_pump_power_consumption: float | Literal["Autosize"] | None = ...,
        zone_name_for_condenser_placement: str | None = ...,
        validate: bool = True,
    ) -> None:
        """Create a new ``Coil:Cooling:DX:MultiSpeed`` and add it to the document.

        Direct expansion (DX) cooling coil and condensing unit (includes electric or engine-driven compressor and condenser fan), multi-speed (or variable-speed). Optional moisture evaporation from wet coil when compressor cycles off with continuous fan operation. Requires two to four sets of performance data and will interpolate between speeds. Modeled as a single coil (multi-speed compressor or multiple compressors with row split or intertwined coil).

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-heating-and-cooling-coils/#coilcoolingdxmultispeed
        """

class CoilCoolingDXVariableRefrigerantFlow:
    def __call__(
        self,
        name: str,
        /,
        *,
        gross_rated_total_cooling_capacity: float | Literal["Autosize"],
        gross_rated_sensible_heat_ratio: float | Literal["Autosize"],
        rated_air_flow_rate: float | Literal["Autosize"],
        cooling_capacity_ratio_modifier_function_of_temperature_curve_name: str,
        cooling_capacity_modifier_curve_function_of_flow_fraction_name: str,
        coil_air_inlet_node: str,
        coil_air_outlet_node: str,
        availability_schedule_name: str | None = ...,
        name_of_water_storage_tank_for_condensate_collection: str | None = ...,
        validate: bool = True,
    ) -> None:
        """Create a new ``Coil:Cooling:DX:VariableRefrigerantFlow`` and add it to the document.

        Variable refrigerant flow (VRF) direct expansion (DX) cooling coil. Used with ZoneHVAC:TerminalUnit:VariableRefrigerantFlow. Condensing unit is modeled separately, see AirConditioner:VariableRefrigerantFlow.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-heating-and-cooling-coils/#coilcoolingdxvariablerefrigerantflow
        """

class AirLoopHVACUnitaryHeatPumpWaterToAir:
    def __call__(
        self,
        name: str,
        /,
        *,
        air_inlet_node_name: str,
        air_outlet_node_name: str,
        supply_air_flow_rate: float | Literal["Autosize"],
        controlling_zone_or_thermostat_location: str,
        supply_air_fan_object_type: Literal["Fan:OnOff"],
        supply_air_fan_name: str,
        heating_coil_object_type: Literal[
            "Coil:Heating:WaterToAirHeatPump:EquationFit",
            "Coil:Heating:WaterToAirHeatPump:ParameterEstimation",
            "Coil:Heating:WaterToAirHeatPump:VariableSpeedEquationFit",
        ],
        heating_coil_name: str,
        cooling_coil_object_type: Literal[
            "Coil:Cooling:WaterToAirHeatPump:EquationFit",
            "Coil:Cooling:WaterToAirHeatPump:ParameterEstimation",
            "Coil:Cooling:WaterToAirHeatPump:VariableSpeedEquationFit",
        ],
        cooling_coil_name: str,
        supplemental_heating_coil_object_type: Literal[
            "Coil:Heating:Electric", "Coil:Heating:Fuel", "Coil:Heating:Steam", "Coil:Heating:Water"
        ],
        supplemental_heating_coil_name: str,
        maximum_supply_air_temperature_from_supplemental_heater: float | Literal["Autosize"],
        availability_schedule_name: str | None = ...,
        heating_convergence: float | None = 0.001,
        cooling_convergence: float | None = 0.001,
        maximum_outdoor_dry_bulb_temperature_for_supplemental_heater_operation: float | None = 21,
        outdoor_dry_bulb_temperature_sensor_node_name: str | None = ...,
        fan_placement: Literal["BlowThrough", "DrawThrough"] | None = "BlowThrough",
        supply_air_fan_operating_mode_schedule_name: str | None = ...,
        dehumidification_control_type: Literal["CoolReheat", "None"] | None = "None",
        heat_pump_coil_water_flow_mode: Literal["Constant", "ConstantOnDemand", "Cycling"] | None = "Cycling",
        dx_heating_coil_sizing_ratio: float | None = 1,
        validate: bool = True,
    ) -> None:
        """Create a new ``AirLoopHVAC:UnitaryHeatPump:WaterToAir`` and add it to the document.

        Unitary heat pump system, heating and cooling, single-speed with constant volume supply fan (continuous or cycling), direct expansion (DX) cooling coil, DX heating coil (water-to-air heat pump), and supplemental heating coil (gas, electric, hot water, or steam).

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-unitary-equipment/#airloophvacunitaryheatpumpwatertoair
        """

class AnyGroundHeatExchangerSurface:
    def __call__(
        self,
        name: str,
        /,
        *,
        construction_name: str,
        fluid_inlet_node_name: str,
        fluid_outlet_node_name: str,
        hydronic_tubing_inside_diameter: float | None = ...,
        number_of_tubing_circuits: int | None = ...,
        hydronic_tube_spacing: float | None = ...,
        surface_length: float | None = ...,
        surface_width: float | None = ...,
        lower_surface_environment: Literal["Exposed", "Ground"] | None = "Ground",
        validate: bool = True,
    ) -> None:
        """Create a new ``GroundHeatExchanger:Surface`` and add it to the document.

        A hydronic surface/panel consisting of a multi-layer construction with embedded rows of tubes. Typically used in hybrid geothermal systems and included in the condenser loop. This component may also be used as a simple solar collector. The bottom surface may be defined as ground-coupled or exposed to wind (eg. bridge deck).

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-condenser-equipment/#groundheatexchangersurface
        """

class GroundHeatExchangerSurface:
    def __call__(
        self,
        name: str,
        /,
        *,
        construction_name: str,
        fluid_inlet_node_name: str,
        fluid_outlet_node_name: str,
        hydronic_tubing_inside_diameter: float | None = ...,
        number_of_tubing_circuits: int | None = ...,
        hydronic_tube_spacing: float | None = ...,
        surface_length: float | None = ...,
        surface_width: float | None = ...,
        lower_surface_environment: Literal["Exposed", "Ground"] | None = "Ground",
        validate: bool = True,
    ) -> None:
        """Create a new ``GroundHeatExchanger:Surface`` and add it to the document.

        A hydronic surface/panel consisting of a multi-layer construction with embedded rows of tubes. Typically used in hybrid geothermal systems and included in the condenser loop. This component may also be used as a simple solar collector. The bottom surface may be defined as ground-coupled or exposed to wind (eg. bridge deck).

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-condenser-equipment/#groundheatexchangersurface
        """

class GroundHeatExchangerHorizontalTrench:
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
        trench_length_in_pipe_axial_direction: float | None = 50,
        number_of_trenches: int | None = 1,
        horizontal_spacing_between_pipes: float | None = 1,
        pipe_inner_diameter: float | None = 0.016,
        pipe_outer_diameter: float | None = 0.026,
        burial_depth: float | None = 1.5,
        soil_thermal_conductivity: float | None = 1.08,
        soil_density: float | None = 962,
        soil_specific_heat: float | None = 2576,
        pipe_thermal_conductivity: float | None = 0.3895,
        pipe_density: float | None = 641,
        pipe_specific_heat: float | None = 2405,
        soil_moisture_content_percent: float | None = 30,
        soil_moisture_content_percent_at_saturation: float | None = 50,
        evapotranspiration_ground_cover_parameter: float | None = 0.4,
        validate: bool = True,
    ) -> None:
        """Create a new ``GroundHeatExchanger:HorizontalTrench`` and add it to the document.

        This models a horizontal heat exchanger placed in a series of trenches The model uses the PipingSystem:Underground underlying algorithms, but provides a more usable input interface.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-condenser-equipment/#groundheatexchangerhorizontaltrench
        """

class ZoneHVACForcedAirUserDefined:
    def __call__(
        self,
        name: str,
        /,
        *,
        primary_air_inlet_node_name: str,
        primary_air_outlet_node_name: str,
        number_of_plant_loop_connections: int,
        overall_model_simulation_program_calling_manager_name: str | None = ...,
        model_setup_and_sizing_program_calling_manager_name: str | None = ...,
        secondary_air_inlet_node_name: str | None = ...,
        secondary_air_outlet_node_name: str | None = ...,
        plant_connection_1_inlet_node_name: str | None = ...,
        plant_connection_1_outlet_node_name: str | None = ...,
        plant_connection_2_inlet_node_name: str | None = ...,
        plant_connection_2_outlet_node_name: str | None = ...,
        plant_connection_3_inlet_node_name: str | None = ...,
        plant_connection_3_outlet_node_name: str | None = ...,
        supply_inlet_water_storage_tank_name: str | None = ...,
        collection_outlet_water_storage_tank_name: str | None = ...,
        ambient_zone_name: str | None = ...,
        validate: bool = True,
    ) -> None:
        """Create a new ``ZoneHVAC:ForcedAir:UserDefined`` and add it to the document.

        Defines a generic zone air unit for custom modeling using Energy Management System or External Interface

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-user-defined-hvac-and-plant-component/#zonehvacforcedairuserdefined
        """

class RefrigerationCondenserWaterCooled:
    def __call__(
        self,
        name: str,
        /,
        *,
        rated_condensing_temperature: float,
        rated_water_inlet_temperature: float,
        rated_effective_total_heat_rejection_rate: float | None = ...,
        rated_subcooling_temperature_difference: float | None = 0,
        water_inlet_node_name: str | None = ...,
        water_outlet_node_name: str | None = ...,
        water_cooled_loop_flow_type: Literal["ConstantFlow", "VariableFlow"] | None = "VariableFlow",
        water_outlet_temperature_schedule_name: str | None = ...,
        water_design_flow_rate: float | None = ...,
        water_maximum_flow_rate: float | None = ...,
        water_maximum_water_outlet_temperature: float | None = 55,
        water_minimum_water_inlet_temperature: float | None = 10,
        end_use_subcategory: str | None = "General",
        condenser_refrigerant_operating_charge_inventory: float | None = ...,
        condensate_receiver_refrigerant_inventory: float | None = ...,
        condensate_piping_refrigerant_inventory: float | None = ...,
        validate: bool = True,
    ) -> None:
        """Create a new ``Refrigeration:Condenser:WaterCooled`` and add it to the document.

        Water cooled condenser for a refrigeration system (Refrigeration:System).

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-refrigeration/#refrigerationcondenserwatercooled
        """

class UtilityCostChargeSimple:
    def __call__(
        self,
        this_type_has_no_name_field: _g._PassFieldsAsKeywords = ...,
        /,
        *,
        utility_cost_charge_simple_name: str,
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
        cost_per_unit_value_or_variable_name: float | str,
        season: Literal["Annual", "Fall", "Spring", "Summer", "Winter"] | None = ...,
        validate: bool = True,
    ) -> None:
        """Create a new ``UtilityCost:Charge:Simple`` and add it to the document.

        UtilityCost:Charge:Simple is one of the most often used objects for tariff calculation. It is used to compute energy and demand charges that are very simple. It may also be used for taxes, surcharges and any other charges that occur on a utility bill. Multiple UtilityCost:Charge:Simple objects may be defined for a single tariff and they will be added together.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/energyplus-economics/utilitycost-charge-simple/#utilitycostchargesimple
        """

class OutputTableMonthly:
    def __call__(
        self,
        name: str,
        /,
        *,
        digits_after_decimal: int | None = 2,
        variable_details: Sequence[
            _g.OutputTableMonthlyVariableDetailsItem | _g.OutputTableMonthlyVariableDetailsGroup
        ] = ...,
        validate: bool = True,
    ) -> None:
        """Create a new ``Output:Table:Monthly`` and add it to the document.

        Provides a generic method of setting up tables of monthly results. The report has multiple columns that are each defined using a repeated group of fields for any number of columns. A single Output:Table:Monthly object often produces multiple tables in the output. A table is produced for every instance of a particular output variable. For example, a table defined with zone variables will be produced once for every zone.

        ``variable_details`` takes the extensible groups in order, one dict per group:

        ```python
        doc["Output:Table:Monthly"].add(
            "Output Table Monthly 1",
            variable_details=[
                {
                    "variable_or_meter_name": "Variable or Meter Name",
                    "aggregation_type_for_variable_or_meter": "HoursNegative",
                },
                {
                    "variable_or_meter_name": "Variable or Meter Name",
                    "aggregation_type_for_variable_or_meter": "HoursNonNegative",
                },
            ],
        )
        ```

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/standard-output-reports/output-table-monthly/#outputtablemonthly
        """

class PythonPluginVariables:
    def __call__(
        self,
        name: str,
        /,
        *,
        global_py_vars: Sequence[
            _g.PythonPluginVariablesGlobalPyVarsItem | _g.PythonPluginVariablesGlobalPyVarsGroup
        ] = ...,
        validate: bool = True,
    ) -> None:
        """Create a new ``PythonPlugin:Variables`` and add it to the document.

        This object defines name identifiers for custom Python Plugin variable data that should be shared among all running Python Plugins.

        ``global_py_vars`` takes the extensible groups in order, one dict per group:

        ```python
        doc["PythonPlugin:Variables"].add(
            "PythonPlugin Variables 1",
            global_py_vars=[
                {"variable_name": "Variable Name"},
                {"variable_name": "Variable Name"},
            ],
        )
        ```

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-python-plugins/#pythonpluginvariables
        """
