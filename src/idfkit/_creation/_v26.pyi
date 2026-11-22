"""Creation signatures of generated classes (stub only).

DO NOT EDIT — regenerate with:
    python -m idfkit.codegen.generate_stubs
"""

from __future__ import annotations

from collections.abc import Sequence
from typing import Literal

from .. import _generated_types as _g

class SizingZone_v8_9_to_v22_1:
    def __call__(
        self,
        this_type_has_no_name_field: _g._PassFieldsAsKeywords = ...,
        /,
        *,
        zone_or_zonelist_name: str,
        zone_cooling_design_supply_air_humidity_ratio: float,
        zone_heating_design_supply_air_humidity_ratio: float,
        zone_cooling_design_supply_air_temperature_input_method: Literal[
            "SupplyAirTemperature", "TemperatureDifference"
        ]
        | None = "SupplyAirTemperature",
        zone_cooling_design_supply_air_temperature: float | None = ...,
        zone_cooling_design_supply_air_temperature_difference: float | None = ...,
        zone_heating_design_supply_air_temperature_input_method: Literal[
            "SupplyAirTemperature", "TemperatureDifference"
        ]
        | None = "SupplyAirTemperature",
        zone_heating_design_supply_air_temperature: float | None = ...,
        zone_heating_design_supply_air_temperature_difference: float | None = ...,
        design_specification_outdoor_air_object_name: str | None = ...,
        zone_heating_sizing_factor: float | None = ...,
        zone_cooling_sizing_factor: float | None = ...,
        cooling_design_air_flow_method: Literal["DesignDay", "DesignDayWithLimit", "Flow/Zone"] | None = "DesignDay",
        cooling_design_air_flow_rate: float | None = 0,
        cooling_minimum_air_flow_per_zone_floor_area: float | None = 0.000762,
        cooling_minimum_air_flow: float | None = 0,
        cooling_minimum_air_flow_fraction: float | None = 0.2,
        heating_design_air_flow_method: Literal["DesignDay", "DesignDayWithLimit", "Flow/Zone"] | None = "DesignDay",
        heating_design_air_flow_rate: float | None = 0,
        heating_maximum_air_flow_per_zone_floor_area: float | None = 0.002032,
        heating_maximum_air_flow: float | None = 0.1415762,
        heating_maximum_air_flow_fraction: float | None = 0.3,
        design_specification_zone_air_distribution_object_name: str | None = ...,
        account_for_dedicated_outdoor_air_system: Literal["No", "Yes"] | None = "No",
        dedicated_outdoor_air_system_control_strategy: Literal[
            "ColdSupplyAir", "NeutralDehumidifiedSupplyAir", "NeutralSupplyAir"
        ]
        | None = "NeutralSupplyAir",
        dedicated_outdoor_air_low_setpoint_temperature_for_design: float | Literal["Autosize"] | None = "Autosize",
        dedicated_outdoor_air_high_setpoint_temperature_for_design: float | Literal["Autosize"] | None = "Autosize",
        validate: bool = True,
    ) -> None:
        """Create a new ``Sizing:Zone`` and add it to the document.

        Specifies the data needed to perform a zone design air flow calculation. The calculation is done for every sizing period included in the input. The maximum cooling and heating load and cooling, heating, and ventilation air flows are then saved for system level and zone component design calculations.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v22.1/io-reference/overview/group-design-objects/#sizingzone
        """

class OtherEquipment_v9_3_to_v9_5:
    def __call__(
        self,
        name: str,
        /,
        *,
        zone_or_zonelist_name: str,
        schedule_name: str,
        fuel_type: Literal[
            "Coal",
            "Diesel",
            "DistrictCooling",
            "DistrictHeating",
            "Electricity",
            "FuelOilNo1",
            "FuelOilNo2",
            "Gasoline",
            "NaturalGas",
            "None",
            "OtherFuel1",
            "OtherFuel2",
            "Propane",
            "Steam",
        ]
        | None = "None",
        design_level_calculation_method: Literal[
            "EquipmentLevel", "Power/Area", "Power/Person", "Watts/Area", "Watts/Person"
        ]
        | None = "EquipmentLevel",
        design_level: float | None = ...,
        power_per_zone_floor_area: float | None = ...,
        power_per_person: float | None = ...,
        fraction_latent: float | None = 0,
        fraction_radiant: float | None = 0,
        fraction_lost: float | None = 0,
        carbon_dioxide_generation_rate: float | None = 0,
        end_use_subcategory: str | None = "General",
        validate: bool = True,
    ) -> None:
        """Create a new ``OtherEquipment`` and add it to the document.

        Sets internal gains or losses for 'other' equipment in the zone.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v9.5/io-reference/overview/group-internal-gains-people-lights-other/#otherequipment
        """

class WaterHeaterMixed_v9_3_to_v23_1:
    def __call__(
        self,
        name: str,
        /,
        *,
        setpoint_temperature_schedule_name: str,
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
        tank_volume: float | Literal["Autosize"] | None = 0,
        deadband_temperature_difference: float | None = 0,
        maximum_temperature_limit: float | None = ...,
        heater_control_type: Literal["Cycle", "Modulate"] | None = "Cycle",
        heater_maximum_capacity: float | Literal["Autosize"] | None = ...,
        heater_minimum_capacity: float | None = ...,
        heater_ignition_minimum_flow_rate: float | None = 0,
        heater_ignition_delay: float | None = 0,
        part_load_factor_curve_name: str | None = ...,
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
        ambient_temperature_schedule_name: str | None = ...,
        ambient_temperature_zone_name: str | None = ...,
        ambient_temperature_outdoor_air_node_name: str | None = ...,
        off_cycle_loss_coefficient_to_ambient_temperature: float | None = ...,
        off_cycle_loss_fraction_to_zone: float | None = 1,
        on_cycle_loss_coefficient_to_ambient_temperature: float | None = ...,
        on_cycle_loss_fraction_to_zone: float | None = 1,
        peak_use_flow_rate: float | None = ...,
        use_flow_rate_fraction_schedule_name: str | None = ...,
        cold_water_supply_temperature_schedule_name: str | None = ...,
        use_side_inlet_node_name: str | None = ...,
        use_side_outlet_node_name: str | None = ...,
        use_side_effectiveness: float | None = 1,
        source_side_inlet_node_name: str | None = ...,
        source_side_outlet_node_name: str | None = ...,
        source_side_effectiveness: float | None = 1,
        use_side_design_flow_rate: float | Literal["Autosize"] | None = "Autosize",
        source_side_design_flow_rate: float | Literal["Autosize"] | None = "Autosize",
        indirect_water_heating_recovery_time: float | None = 1.5,
        source_side_flow_control_mode: Literal[
            "IndirectHeatAlternateSetpoint", "IndirectHeatPrimarySetpoint", "StorageTank"
        ]
        | None = "IndirectHeatPrimarySetpoint",
        indirect_alternate_setpoint_temperature_schedule_name: str | None = ...,
        end_use_subcategory: str | None = "General",
        validate: bool = True,
    ) -> None:
        """Create a new ``WaterHeater:Mixed`` and add it to the document.

        Water heater with well-mixed, single-node water tank. May be used to model a tankless water heater (small tank volume), a hot water storage tank (zero heater capacity), or a heat pump water heater (see WaterHeater:HeatPump:PumpedCondenser.)

        EnergyPlus I/O Reference: https://docs.idfkit.com/v23.1/io-reference/overview/group-water-heaters/#waterheatermixed
        """

class ZoneHVACHybridUnitaryHVAC_v8_9_to_v9_2:
    def __call__(
        self,
        name: str,
        /,
        *,
        return_air_node_name: str,
        outdoor_air_node_name: str,
        supply_air_node_name: str,
        availability_schedule_name: str | None = ...,
        availability_manager_list_name: str | None = ...,
        minimum_supply_air_temperature_schedule_name: str | None = ...,
        maximum_supply_air_temperature_schedule_name: str | None = ...,
        minimum_supply_air_humidity_ratio_schedule_name: str | None = ...,
        maximum_supply_air_humidity_ratio_schedule_name: str | None = ...,
        method_to_choose_controlled_inputs_and_part_runtime_fraction: Literal["Automatic", "User Defined"]
        | None = "Automatic",
        relief_node_name: str | None = ...,
        system_maximum_supply_air_flow_rate: float | None = ...,
        external_static_pressure_at_system_maximum_supply_air_flow_rate: float | None = ...,
        scaling_factor: float | None = 1,
        number_of_operating_modes: float | None = 1,
        minimum_time_between_mode_change: float | None = 10,
        first_fuel_type: Literal[
            "Coal",
            "Diesel",
            "DistrictCooling",
            "DistrictHeating",
            "Electricity",
            "FuelOil#1",
            "FuelOil#2",
            "Gasoline",
            "NaturalGas",
            "None",
            "OtherFuel1",
            "OtherFuel2",
            "PropaneGas",
            "Steam",
        ]
        | None = "Electricity",
        second_fuel_type: Literal[
            "Coal",
            "Diesel",
            "DistrictCooling",
            "DistrictHeating",
            "Electricity",
            "FuelOil#1",
            "FuelOil#2",
            "Gasoline",
            "NaturalGas",
            "None",
            "OtherFuel1",
            "OtherFuel2",
            "PropaneGas",
            "Steam",
        ]
        | None = "None",
        third_fuel_type: Literal[
            "Coal",
            "Diesel",
            "DistrictCooling",
            "DistrictHeating",
            "Electricity",
            "FuelOil#1",
            "FuelOil#2",
            "Gasoline",
            "NaturalGas",
            "None",
            "OtherFuel1",
            "OtherFuel2",
            "PropaneGas",
            "Steam",
        ]
        | None = "None",
        objective_function_to_minimize: Literal["Electricity Use", "Second Fuel Use", "Third Fuel Use", "Water Use"]
        | None = "Electricity Use",
        design_specification_outdoor_air_object_name: str | None = ...,
        mode_0_name: str | None = ...,
        mode_0_supply_air_temperature_lookup_table_name: str | None = ...,
        mode_0_supply_air_humidity_ratio_lookup_table_name: str | None = ...,
        mode_0_system_electric_power_lookup_table_name: str | None = ...,
        mode_0_supply_fan_electric_power_lookup_table_name: str | None = ...,
        mode_0_external_static_pressure_lookup_table_name: str | None = ...,
        mode_0_system_second_fuel_consumption_lookup_table_name: str | None = ...,
        mode_0_system_third_fuel_consumption_lookup_table_name: str | None = ...,
        mode_0_system_water_use_lookup_table_name: str | None = ...,
        mode_0_outdoor_air_fraction: float | None = 0,
        mode_0_supply_air_mass_flow_rate_ratio: float | None = 0,
        modes: Sequence[_g.ZoneHVACHybridUnitaryHVACModesItem | _g.ZoneHVACHybridUnitaryHVACModesGroup] = ...,
        validate: bool = True,
    ) -> None:
        """Create a new ``ZoneHVAC:HybridUnitaryHVAC`` and add it to the document.

        Hybrid Unitary HVAC. A black box model for multi-mode packaged forced air equipment. Independent variables include outdoor air conditions and indoor air conditions. Controlled inputs include operating mode, supply air flow rate, and outdoor air faction. Emperical lookup tables are required to map supply air temperature supply air humidity, electricity use, fuel uses, water use, fan electricity use, and external static pressure as a function of each indpednent varaible and each controlled input. In each timestep the model will choose one or more combinations of settings for mode, supply air flow rate, outdoor air faction, and part runtime fraction so as to satisfy zone requests for sensible cooling, heating, ventilation, and/or dehumidification with the least resource consumption. Equipment in this class may consume electricity, water, and up to two additional fuel types.

        ``modes`` takes the extensible groups in order, one dict per group:

        ```python
        doc["ZoneHVAC:HybridUnitaryHVAC"].add(
            "ZoneHVAC HybridUnitaryHVAC 1",
            return_air_node_name="Return Air Node Name",
            outdoor_air_node_name="Outdoor Air Node Name",
            supply_air_node_name="Supply Air Node Name",
            modes=[
                {
                    "mode_minimum_outdoor_air_fraction": 0.1,
                    "mode_maximum_return_air_temperature": 0.0,
                    "mode_name": "Mode Name",
                    "mode_system_second_fuel_consumption_lookup_table_name": "Mode System Second Fuel Consumption Lookup Table 1",
                    "mode_supply_air_temperature_lookup_table_name": "Mode Supply Air Temperature Lookup Table 1",
                    "mode_maximum_return_air_relative_humidity": 100.0,
                    "mode_minimum_return_air_relative_humidity": 0.0,
                    "mode_supply_fan_electric_power_lookup_table_name": "Mode Supply Fan Electric Power Lookup Table 1",
                    "mode_maximum_supply_air_mass_flow_rate_ratio": 1.0,
                    "mode_minimum_return_air_temperature": 0.0,
                    "mode_minimum_supply_air_mass_flow_rate_ratio": 0.1,
                    "mode_maximum_outdoor_air_fraction": 1.0,
                    "mode_minimum_return_air_humidity_ratio": 0.0,
                    "mode_minimum_outdoor_air_temperature": 0.0,
                    "mode_external_static_pressure_lookup_table_name": "Mode External Static Pressure Lookup Table 1",
                    "mode_system_third_fuel_consumption_lookup_table_name": "Mode System Third Fuel Consumption Lookup Table 1",
                    "mode_maximum_outdoor_air_relative_humidity": 100.0,
                    "mode_minimum_outdoor_air_relative_humidity": 0.0,
                    "mode_maximum_outdoor_air_temperature": 0.0,
                    "mode_maximum_outdoor_air_humidity_ratio": 0.1,
                    "mode_system_water_use_lookup_table_name": "Mode System Water Use Lookup Table 1",
                    "mode_maximum_return_air_humidity_ratio": 0.1,
                    "mode_minimum_outdoor_air_humidity_ratio": 0.0,
                    "mode_supply_air_humidity_ratio_lookup_table_name": "Mode Supply Air Humidity Ratio Lookup Table 1",
                    "mode_system_electric_power_lookup_table_name": "Mode System Electric Power Lookup Table 1",
                },
                {
                    "mode_minimum_outdoor_air_fraction": 0.1,
                    "mode_maximum_return_air_temperature": 0.0,
                    "mode_name": "Mode Name",
                    "mode_system_second_fuel_consumption_lookup_table_name": "Mode System Second Fuel Consumption Lookup Table 2",
                    "mode_supply_air_temperature_lookup_table_name": "Mode Supply Air Temperature Lookup Table 2",
                    "mode_maximum_return_air_relative_humidity": 100.0,
                    "mode_minimum_return_air_relative_humidity": 0.0,
                    "mode_supply_fan_electric_power_lookup_table_name": "Mode Supply Fan Electric Power Lookup Table 2",
                    "mode_maximum_supply_air_mass_flow_rate_ratio": 1.0,
                    "mode_minimum_return_air_temperature": 0.0,
                    "mode_minimum_supply_air_mass_flow_rate_ratio": 0.1,
                    "mode_maximum_outdoor_air_fraction": 1.0,
                    "mode_minimum_return_air_humidity_ratio": 0.0,
                    "mode_minimum_outdoor_air_temperature": 0.0,
                    "mode_external_static_pressure_lookup_table_name": "Mode External Static Pressure Lookup Table 2",
                    "mode_system_third_fuel_consumption_lookup_table_name": "Mode System Third Fuel Consumption Lookup Table 2",
                    "mode_maximum_outdoor_air_relative_humidity": 100.0,
                    "mode_minimum_outdoor_air_relative_humidity": 0.0,
                    "mode_maximum_outdoor_air_temperature": 0.0,
                    "mode_maximum_outdoor_air_humidity_ratio": 0.1,
                    "mode_system_water_use_lookup_table_name": "Mode System Water Use Lookup Table 2",
                    "mode_maximum_return_air_humidity_ratio": 0.1,
                    "mode_minimum_outdoor_air_humidity_ratio": 0.0,
                    "mode_supply_air_humidity_ratio_lookup_table_name": "Mode Supply Air Humidity Ratio Lookup Table 2",
                    "mode_system_electric_power_lookup_table_name": "Mode System Electric Power Lookup Table 2",
                },
            ],
        )
        ```

        EnergyPlus I/O Reference: https://docs.idfkit.com/v9.2/io-reference/overview/group-zone-forced-air-units/#zonehvachybridunitaryhvac
        """
