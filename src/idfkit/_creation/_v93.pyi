"""Creation signatures of generated classes (stub only).

DO NOT EDIT — regenerate with:
    python -m idfkit.codegen.generate_stubs
"""

from __future__ import annotations

from collections.abc import Sequence
from typing import Literal

from .. import _generated_types as _g
from .. import versioned as _vd

class OtherEquipment_v9_6_to_v23_1:
    def __call__(
        self,
        name: str,
        /,
        *,
        zone_or_zonelist_or_space_or_spacelist_name: str,
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
    ) -> None:
        """Create a new ``OtherEquipment`` and add it to the document.

        Sets internal gains or losses for 'other' equipment in the zone. If a ZoneList, SpaceList, or a Zone comprised of more than one Space is specified then this definition applies to all applicable spaces, and each instance will be named with the Space Name plus this Object Name.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v23.1/io-reference/overview/group-internal-gains-people-lights-other/#otherequipment
        """

class OtherEquipment_v23_2:
    def __call__(
        self,
        name: str,
        /,
        *,
        zone_or_zonelist_or_space_or_spacelist_name: str,
        schedule_name: str,
        fuel_type: Literal[
            "Coal",
            "Diesel",
            "DistrictCooling",
            "DistrictHeatingSteam",
            "DistrictHeatingWater",
            "Electricity",
            "FuelOilNo1",
            "FuelOilNo2",
            "Gasoline",
            "NaturalGas",
            "None",
            "OtherFuel1",
            "OtherFuel2",
            "Propane",
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
    ) -> None:
        """Create a new ``OtherEquipment`` and add it to the document.

        Sets internal gains or losses for 'other' equipment in the zone. If a ZoneList, SpaceList, or a Zone comprised of more than one Space is specified then this definition applies to all applicable spaces, and each instance will be named with the Space Name plus this Object Name.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v23.2/io-reference/overview/group-internal-gains-people-lights-other/#otherequipment
        """

class ZoneHVACHybridUnitaryHVAC_v9_4_to_v23_1:
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
        fan_heat_included_in_lookup_tables: Literal["No", "Yes"] | None = "No",
        fan_heat_gain_location: Literal["MixedAirStream", "SupplyAirStream"] | None = "SupplyAirStream",
        fan_heat_in_air_stream_fraction: float | None = 1,
        scaling_factor: float | None = 1,
        minimum_time_between_mode_change: float | None = 10,
        first_fuel_type: Literal[
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
        | None = "Electricity",
        second_fuel_type: Literal[
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
        third_fuel_type: Literal[
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
    ) -> None:
        """Create a new ``ZoneHVAC:HybridUnitaryHVAC`` and add it to the document.

        Hybrid Unitary HVAC. A black box model for multi-mode packaged forced air equipment. Independent variables include outdoor air conditions and indoor air conditions. Controlled inputs include operating mode, supply air flow rate, and outdoor air faction. Emperical lookup tables are required to map supply air temperature supply air humidity, electricity use, fuel uses, water use, fan electricity use, and external static pressure as a function of each indpednent varaible and each controlled input. In each timestep the model will choose one or more combinations of settings for mode, supply air flow rate, outdoor air faction, and part runtime fraction so as to satisfy zone requests for sensible cooling, heating, ventilation, and/or dehumidification with the least resource consumption. Equipment in this class may consume electricity, water, and up to two additional fuel types.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v23.1/io-reference/overview/group-zone-forced-air-units/#zonehvachybridunitaryhvac
        """

class SizingSystem_v8_9_to_v9_5:
    def __call__(
        self,
        /,
        *,
        airloop_name: str,
        preheat_design_temperature: float,
        preheat_design_humidity_ratio: float,
        precool_design_temperature: float,
        precool_design_humidity_ratio: float,
        central_cooling_design_supply_air_temperature: float,
        central_heating_design_supply_air_temperature: float,
        type_of_load_to_size_on: Literal["Sensible", "Total", "VentilationRequirement"] | None = "Sensible",
        design_outdoor_air_flow_rate: float | Literal["Autosize"] | None = "Autosize",
        central_heating_maximum_system_air_flow_ratio: float | Literal["Autosize"] | None = "Autosize",
        type_of_zone_sum_to_use: Literal["Coincident", "NonCoincident"] | None = "NonCoincident",
        central_cooling_design_supply_air_humidity_ratio: float | None = 0.008,
        central_heating_design_supply_air_humidity_ratio: float | None = 0.008,
        cooling_supply_air_flow_rate_method: Literal[
            "DesignDay",
            "Flow/System",
            "FlowPerCoolingCapacity",
            "FlowPerFloorArea",
            "FractionOfAutosizedCoolingAirflow",
        ]
        | None = "DesignDay",
        cooling_supply_air_flow_rate: float | None = 0,
        cooling_supply_air_flow_rate_per_floor_area: float | None = ...,
        cooling_fraction_of_autosized_cooling_supply_air_flow_rate: float | None = ...,
        cooling_supply_air_flow_rate_per_unit_cooling_capacity: float | None = ...,
        heating_supply_air_flow_rate_method: Literal[
            "DesignDay",
            "Flow/System",
            "FlowPerFloorArea",
            "FlowPerHeatingCapacity",
            "FractionOfAutosizedCoolingAirflow",
            "FractionOfAutosizedHeatingAirflow",
        ]
        | None = "DesignDay",
        heating_supply_air_flow_rate: float | None = 0,
        heating_supply_air_flow_rate_per_floor_area: float | None = ...,
        heating_fraction_of_autosized_heating_supply_air_flow_rate: float | None = ...,
        heating_fraction_of_autosized_cooling_supply_air_flow_rate: float | None = ...,
        heating_supply_air_flow_rate_per_unit_heating_capacity: float | None = ...,
        system_outdoor_air_method: Literal["VentilationRateProcedure", "ZoneSum"] | None = "ZoneSum",
        zone_maximum_outdoor_air_fraction: float | None = 1,
        cooling_design_capacity_method: Literal[
            "CapacityPerFloorArea", "CoolingDesignCapacity", "FractionOfAutosizedCoolingCapacity", "None"
        ]
        | None = "CoolingDesignCapacity",
        cooling_design_capacity: float | Literal["Autosize"] | None = "Autosize",
        cooling_design_capacity_per_floor_area: float | None = ...,
        fraction_of_autosized_cooling_design_capacity: float | None = ...,
        heating_design_capacity_method: Literal[
            "CapacityPerFloorArea", "FractionOfAutosizedHeatingCapacity", "HeatingDesignCapacity", "None"
        ]
        | None = "HeatingDesignCapacity",
        heating_design_capacity: float | Literal["Autosize"] | None = "Autosize",
        heating_design_capacity_per_floor_area: float | None = ...,
        fraction_of_autosized_heating_design_capacity: float | None = ...,
        central_cooling_capacity_control_method: Literal["Bypass", "OnOff", "VAV", "VT"] | None = "OnOff",
    ) -> None:
        """Create a new ``Sizing:System`` and add it to the document.

        Specifies the input needed to perform sizing calculations for a central forced air system. System design air flow, heating capacity, and cooling capacity will be calculated using this input data.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v9.5/io-reference/overview/group-design-objects/#sizingsystem
        """

class ElectricEquipment_v8_9_to_v9_5:
    def __call__(
        self,
        name: str,
        /,
        *,
        zone_or_zonelist_name: str,
        schedule_name: str,
        design_level_calculation_method: Literal["EquipmentLevel", "Watts/Area", "Watts/Person"]
        | None = "EquipmentLevel",
        design_level: float | None = ...,
        watts_per_zone_floor_area: float | None = ...,
        watts_per_person: float | None = ...,
        fraction_latent: float | None = 0,
        fraction_radiant: float | None = 0,
        fraction_lost: float | None = 0,
        end_use_subcategory: str | None = "General",
    ) -> None:
        """Create a new ``ElectricEquipment`` and add it to the document.

        Sets internal gains for electric equipment in the zone. If you use a ZoneList in the Zone or ZoneList name field then this definition applies to all the zones in the ZoneList.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v9.5/io-reference/overview/group-internal-gains-people-lights-other/#electricequipment
        """

class CoilCoolingDXVariableSpeed_v8_9_to_v22_1:
    def __call__(
        self,
        name: str,
        /,
        *,
        indoor_air_inlet_node_name: str,
        indoor_air_outlet_node_name: str,
        energy_part_load_fraction_curve_name: str,
        speed_1_reference_unit_gross_rated_total_cooling_capacity: float,
        speed_1_reference_unit_gross_rated_sensible_heat_ratio: float,
        speed_1_reference_unit_gross_rated_cooling_cop: float,
        speed_1_reference_unit_rated_air_flow_rate: float,
        speed_1_total_cooling_capacity_function_of_temperature_curve_name: str,
        speed_1_total_cooling_capacity_function_of_air_flow_fraction_curve_name: str,
        speed_1_energy_input_ratio_function_of_temperature_curve_name: str,
        speed_1_energy_input_ratio_function_of_air_flow_fraction_curve_name: str,
        number_of_speeds: float | None = 2,
        nominal_speed_level: float | None = 2,
        gross_rated_total_cooling_capacity_at_selected_nominal_speed_level: float
        | Literal["Autosize"]
        | None = "Autosize",
        rated_air_flow_rate_at_selected_nominal_speed_level: float | Literal["Autosize"] | None = "Autosize",
        nominal_time_for_condensate_to_begin_leaving_the_coil: float | None = 0,
        initial_moisture_evaporation_rate_divided_by_steady_state_ac_latent_capacity: float | None = 0,
        condenser_air_inlet_node_name: str | None = ...,
        condenser_type: Literal["AirCooled", "EvaporativelyCooled"] | None = "AirCooled",
        evaporative_condenser_pump_rated_power_consumption: float | Literal["Autosize"] | None = 0,
        crankcase_heater_capacity: float | None = 0,
        maximum_outdoor_dry_bulb_temperature_for_crankcase_heater_operation: float | None = 10,
        minimum_outdoor_dry_bulb_temperature_for_compressor_operation: float | None = -25,
        supply_water_storage_tank_name: str | None = ...,
        condensate_collection_water_storage_tank_name: str | None = ...,
        basin_heater_capacity: float | None = 0,
        basin_heater_setpoint_temperature: float | None = 2,
        basin_heater_operating_schedule_name: str | None = ...,
        speed_1_reference_unit_rated_condenser_air_flow_rate: float | None = ...,
        speed_1_reference_unit_rated_pad_effectiveness_of_evap_precooling: float | None = ...,
        speed_2_reference_unit_gross_rated_total_cooling_capacity: float | None = ...,
        speed_2_reference_unit_gross_rated_sensible_heat_ratio: float | None = ...,
        speed_2_reference_unit_gross_rated_cooling_cop: float | None = ...,
        speed_2_reference_unit_rated_air_flow_rate: float | None = ...,
        speed_2_reference_unit_rated_condenser_air_flow_rate: float | None = ...,
        speed_2_reference_unit_rated_pad_effectiveness_of_evap_precooling: float | None = ...,
        speed_2_total_cooling_capacity_function_of_temperature_curve_name: str | None = ...,
        speed_2_total_cooling_capacity_function_of_air_flow_fraction_curve_name: str | None = ...,
        speed_2_energy_input_ratio_function_of_temperature_curve_name: str | None = ...,
        speed_2_energy_input_ratio_function_of_air_flow_fraction_curve_name: str | None = ...,
        speed_3_reference_unit_gross_rated_total_cooling_capacity: float | None = ...,
        speed_3_reference_unit_gross_rated_sensible_heat_ratio: float | None = ...,
        speed_3_reference_unit_gross_rated_cooling_cop: float | None = ...,
        speed_3_reference_unit_rated_air_flow_rate: float | None = ...,
        speed_3_reference_unit_rated_condenser_air_flow_rate: float | None = ...,
        speed_3_reference_unit_rated_pad_effectiveness_of_evap_precooling: float | None = ...,
        speed_3_total_cooling_capacity_function_of_temperature_curve_name: str | None = ...,
        speed_3_total_cooling_capacity_function_of_air_flow_fraction_curve_name: str | None = ...,
        speed_3_energy_input_ratio_function_of_temperature_curve_name: str | None = ...,
        speed_3_energy_input_ratio_function_of_air_flow_fraction_curve_name: str | None = ...,
        speed_4_reference_unit_gross_rated_total_cooling_capacity: float | None = ...,
        speed_4_reference_unit_gross_rated_sensible_heat_ratio: float | None = ...,
        speed_4_reference_unit_gross_rated_cooling_cop: float | None = ...,
        speed_4_reference_unit_rated_air_flow_rate: float | None = ...,
        speed_4_reference_unit_rated_condenser_air_flow_rate: float | None = ...,
        speed_4_reference_unit_rated_pad_effectiveness_of_evap_precooling: float | None = ...,
        speed_4_total_cooling_capacity_function_of_temperature_curve_name: str | None = ...,
        speed_4_total_cooling_capacity_function_of_air_flow_fraction_curve_name: str | None = ...,
        speed_4_energy_input_ratio_function_of_temperature_curve_name: str | None = ...,
        speed_4_energy_input_ratio_function_of_air_flow_fraction_curve_name: str | None = ...,
        speed_5_reference_unit_gross_rated_total_cooling_capacity: float | None = ...,
        speed_5_reference_unit_gross_rated_sensible_heat_ratio: float | None = ...,
        speed_5_reference_unit_gross_rated_cooling_cop: float | None = ...,
        speed_5_reference_unit_rated_air_flow_rate: float | None = ...,
        speed_5_reference_unit_rated_condenser_air_flow_rate: float | None = ...,
        speed_5_reference_unit_rated_pad_effectiveness_of_evap_precooling: float | None = ...,
        speed_5_total_cooling_capacity_function_of_temperature_curve_name: str | None = ...,
        speed_5_total_cooling_capacity_function_of_air_flow_fraction_curve_name: str | None = ...,
        speed_5_energy_input_ratio_function_of_temperature_curve_name: str | None = ...,
        speed_5_energy_input_ratio_function_of_air_flow_fraction_curve_name: str | None = ...,
        speed_6_reference_unit_gross_rated_total_cooling_capacity: float | None = ...,
        speed_6_reference_unit_gross_rated_sensible_heat_ratio: float | None = ...,
        speed_6_reference_unit_gross_rated_cooling_cop: float | None = ...,
        speed_6_reference_unit_rated_air_flow_rate: float | None = ...,
        speed_6_reference_unit_condenser_air_flow_rate: float | None = ...,
        speed_6_reference_unit_rated_pad_effectiveness_of_evap_precooling: float | None = ...,
        speed_6_total_cooling_capacity_function_of_temperature_curve_name: str | None = ...,
        speed_6_total_cooling_capacity_function_of_air_flow_fraction_curve_name: str | None = ...,
        speed_6_energy_input_ratio_function_of_temperature_curve_name: str | None = ...,
        speed_6_energy_input_ratio_function_of_air_flow_fraction_curve_name: str | None = ...,
        speed_7_reference_unit_gross_rated_total_cooling_capacity: float | None = ...,
        speed_7_reference_unit_gross_rated_sensible_heat_ratio: float | None = ...,
        speed_7_reference_unit_gross_rated_cooling_cop: float | None = ...,
        speed_7_reference_unit_rated_air_flow_rate: float | None = ...,
        speed_7_reference_unit_condenser_flow_rate: float | None = ...,
        speed_7_reference_unit_rated_pad_effectiveness_of_evap_precooling: float | None = ...,
        speed_7_total_cooling_capacity_function_of_temperature_curve_name: str | None = ...,
        speed_7_total_cooling_capacity_function_of_air_flow_fraction_curve_name: str | None = ...,
        speed_7_energy_input_ratio_function_of_temperature_curve_name: str | None = ...,
        speed_7_energy_input_ratio_function_of_air_flow_fraction_curve_name: str | None = ...,
        speed_8_reference_unit_gross_rated_total_cooling_capacity: float | None = ...,
        speed_8_reference_unit_gross_rated_sensible_heat_ratio: float | None = ...,
        speed_8_reference_unit_gross_rated_cooling_cop: float | None = ...,
        speed_8_reference_unit_rated_air_flow_rate: float | None = ...,
        speed_8_reference_unit_condenser_air_flow_rate: float | None = ...,
        speed_8_reference_unit_rated_pad_effectiveness_of_evap_precooling: float | None = ...,
        speed_8_total_cooling_capacity_function_of_temperature_curve_name: str | None = ...,
        speed_8_total_cooling_capacity_function_of_air_flow_fraction_curve_name: str | None = ...,
        speed_8_energy_input_ratio_function_of_temperature_curve_name: str | None = ...,
        speed_8_energy_input_ratio_function_of_air_flow_fraction_curve_name: str | None = ...,
        speed_9_reference_unit_gross_rated_total_cooling_capacity: float | None = ...,
        speed_9_reference_unit_gross_rated_sensible_heat_ratio: float | None = ...,
        speed_9_reference_unit_gross_rated_cooling_cop: float | None = ...,
        speed_9_reference_unit_rated_air_flow_rate: float | None = ...,
        speed_9_reference_unit_condenser_air_flow_rate: float | None = ...,
        speed_9_reference_unit_rated_pad_effectiveness_of_evap_precooling: float | None = ...,
        speed_9_total_cooling_capacity_function_of_temperature_curve_name: str | None = ...,
        speed_9_total_cooling_capacity_function_of_air_flow_fraction_curve_name: str | None = ...,
        speed_9_energy_input_ratio_function_of_temperature_curve_name: str | None = ...,
        speed_9_energy_input_ratio_function_of_air_flow_fraction_curve_name: str | None = ...,
        speed_10_reference_unit_gross_rated_total_cooling_capacity: float | None = ...,
        speed_10_reference_unit_gross_rated_sensible_heat_ratio: float | None = ...,
        speed_10_reference_unit_gross_rated_cooling_cop: float | None = ...,
        speed_10_reference_unit_rated_air_flow_rate: float | None = ...,
        speed_10_reference_unit_condenser_air_flow_rate: float | None = ...,
        speed_10_reference_unit_rated_pad_effectiveness_of_evap_precooling: float | None = ...,
        speed_10_total_cooling_capacity_function_of_temperature_curve_name: str | None = ...,
        speed_10_total_cooling_capacity_function_of_air_flow_fraction_curve_name: str | None = ...,
        speed_10_energy_input_ratio_function_of_temperature_curve_name: str | None = ...,
        speed_10_energy_input_ratio_function_of_air_flow_fraction_curve_name: str | None = ...,
    ) -> None:
        """Create a new ``Coil:Cooling:DX:VariableSpeed`` and add it to the document.

        Direct expansion (DX) cooling coil and condensing unit (includes electric compressor and condenser fan), variable-speed. Optional inputs for moisture evaporation from wet coil when compressor cycles off with continuous fan operation. Requires two to ten sets of performance data and will interpolate between speeds. Modeled as a single coil with variable-speed compressor.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v22.1/io-reference/overview/group-heating-and-cooling-coils/#coilcoolingdxvariablespeed
        """

class RoomAirNodeAirflowNetworkInternalGains_v8_9_to_v9_4:
    def __call__(
        self,
        name: str = "",
        /,
        *,
        gains: Sequence[
            _vd.RoomAirNodeAirflowNetworkInternalGainsGainsItem_v8_9_to_v9_4
            | _vd.RoomAirNodeAirflowNetworkInternalGainsGainsGroup_v8_9_to_v9_4
        ] = ...,
    ) -> None:
        """Create a new ``RoomAir:Node:AirflowNetwork:InternalGains`` and add it to the document.

        define the internal gains that are associated with one particular RoomAir:Node

        EnergyPlus I/O Reference: https://docs.idfkit.com/v9.4/io-reference/overview/group-room-air-models/#roomairnodeairflownetworkinternalgains
        """
