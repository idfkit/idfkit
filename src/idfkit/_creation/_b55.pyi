"""Creation signatures of generated classes (stub only).

DO NOT EDIT — regenerate with:
    python -m idfkit.codegen.generate_stubs
"""

from __future__ import annotations

from collections.abc import Sequence
from typing import Literal

from .. import _generated_types as _g

class FloorInterzone:
    def __call__(
        self,
        name: str,
        /,
        *,
        construction_name: str,
        zone_name: str,
        outside_boundary_condition_object: str,
        space_name: str | None = ...,
        azimuth_angle: float | None = ...,
        tilt_angle: float | None = 180,
        starting_x_coordinate: float | None = ...,
        starting_y_coordinate: float | None = ...,
        starting_z_coordinate: float | None = ...,
        length: float | None = ...,
        width: float | None = ...,
    ) -> None:
        """Create a new ``Floor:Interzone`` and add it to the document.

        Allows for simplified entry of floors using adjacent zone (interzone) heat transfer - adjacent surface should be a ceiling.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-thermal-zone-description-geometry/#floorinterzone
        """

class AnyZoneHVACPackagedTerminalHeatPump:
    def __call__(
        self,
        name: str,
        /,
        *,
        air_inlet_node_name: str,
        air_outlet_node_name: str,
        cooling_supply_air_flow_rate: float | Literal["Autosize"],
        heating_supply_air_flow_rate: float | Literal["Autosize"],
        cooling_outdoor_air_flow_rate: float | Literal["Autosize"],
        heating_outdoor_air_flow_rate: float | Literal["Autosize"],
        supply_air_fan_object_type: Literal["Fan:ConstantVolume", "Fan:OnOff", "Fan:SystemModel"],
        supply_air_fan_name: str,
        heating_coil_object_type: Literal["Coil:Heating:DX:SingleSpeed", "Coil:Heating:DX:VariableSpeed"],
        heating_coil_name: str,
        cooling_coil_object_type: Literal[
            "Coil:Cooling:DX:SingleSpeed",
            "Coil:Cooling:DX:VariableSpeed",
            "CoilSystem:Cooling:DX:HeatExchangerAssisted",
        ],
        cooling_coil_name: str,
        supplemental_heating_coil_object_type: Literal[
            "Coil:Heating:Electric", "Coil:Heating:Fuel", "Coil:Heating:Steam", "Coil:Heating:Water"
        ],
        supplemental_heating_coil_name: str,
        maximum_supply_air_temperature_from_supplemental_heater: float | Literal["Autosize"],
        availability_schedule_name: str | None = ...,
        outdoor_air_mixer_object_type: Literal["OutdoorAir:Mixer"] | None = ...,
        outdoor_air_mixer_name: str | None = ...,
        no_load_supply_air_flow_rate: float | Literal["Autosize"] | None = ...,
        no_load_outdoor_air_flow_rate: float | Literal["Autosize"] | None = ...,
        heating_convergence_tolerance: float | None = 0.001,
        cooling_convergence_tolerance: float | None = 0.001,
        maximum_outdoor_dry_bulb_temperature_for_supplemental_heater_operation: float | None = 21,
        fan_placement: Literal["BlowThrough", "DrawThrough"] | None = "DrawThrough",
        supply_air_fan_operating_mode_schedule_name: str | None = ...,
        availability_manager_list_name: str | None = ...,
        design_specification_zonehvac_sizing_object_name: str | None = ...,
        capacity_control_method: Literal["None", "SingleZoneVAV"] | None = "None",
        minimum_supply_air_temperature_in_cooling_mode: float | Literal["Autosize"] | None = "Autosize",
        maximum_supply_air_temperature_in_heating_mode: float | Literal["Autosize"] | None = "Autosize",
    ) -> None:
        """Create a new ``ZoneHVAC:PackagedTerminalHeatPump`` and add it to the document.

        Packaged terminal heat pump (PTHP). Forced-convection heating-cooling unit with supply fan, direct expansion (DX) cooling coil, DX heating coil (air-to-air heat pump), supplemental heating coil (gas, electric, hot water, or steam), and fixed-position outdoor air mixer.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-zone-forced-air-units/#zonehvacpackagedterminalheatpump
        """

class ZoneHVACLowTemperatureRadiantConstantFlow:
    def __call__(
        self,
        name: str,
        /,
        *,
        design_object: str,
        availability_schedule_name: str | None = ...,
        zone_name: str | None = ...,
        surface_name_or_radiant_surface_group_name: str | None = ...,
        hydronic_tubing_length: float | Literal["Autosize"] | None = "Autosize",
        rated_flow_rate: float | Literal["Autosize"] | None = ...,
        pump_flow_rate_schedule_name: str | None = ...,
        rated_pump_head: float | None = 179352,
        rated_power_consumption: float | None = ...,
        heating_water_inlet_node_name: str | None = ...,
        heating_water_outlet_node_name: str | None = ...,
        heating_high_water_temperature_schedule_name: str | None = ...,
        heating_low_water_temperature_schedule_name: str | None = ...,
        heating_high_control_temperature_schedule_name: str | None = ...,
        heating_low_control_temperature_schedule_name: str | None = ...,
        cooling_water_inlet_node_name: str | None = ...,
        cooling_water_outlet_node_name: str | None = ...,
        cooling_high_water_temperature_schedule_name: str | None = ...,
        cooling_low_water_temperature_schedule_name: str | None = ...,
        cooling_high_control_temperature_schedule_name: str | None = ...,
        cooling_low_control_temperature_schedule_name: str | None = ...,
        number_of_circuits: Literal["CalculateFromCircuitLength", "OnePerSurface"] | None = "OnePerSurface",
        circuit_length: float | None = 106.7,
    ) -> None:
        """Create a new ``ZoneHVAC:LowTemperatureRadiant:ConstantFlow`` and add it to the document.

        Low temperature hydronic radiant heating and/or cooling system embedded in a building surface (wall, ceiling, or floor). Controlled by varying the hot or chilled water temperature circulating through the unit.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-radiative-convective-units/#zonehvaclowtemperatureradiantconstantflow
        """

class AnyAirTerminalSingleDuctVAVHeatAndCoolNoReheat:
    def __call__(
        self,
        name: str,
        /,
        *,
        air_outlet_node_name: str,
        air_inlet_node_name: str,
        maximum_air_flow_rate: float | Literal["Autosize"],
        zone_minimum_air_flow_fraction: float,
        availability_schedule_name: str | None = ...,
    ) -> None:
        """Create a new ``AirTerminal:SingleDuct:VAV:HeatAndCool:NoReheat`` and add it to the document.

        Central air system terminal unit, single duct, variable volume for both cooling and heating, with no reheat coil.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-zone-hvac-air-loop-terminal-units/#airterminalsingleductvavheatandcoolnoreheat
        """

class AnyAirTerminalSingleDuctParallelPIUReheat:
    def __call__(
        self,
        name: str,
        /,
        *,
        maximum_primary_air_flow_rate: float | Literal["Autosize"],
        maximum_secondary_air_flow_rate: float | Literal["Autosize"],
        minimum_primary_air_flow_fraction: float | Literal["Autosize"],
        fan_on_flow_fraction: float | Literal["Autosize"],
        reheat_coil_object_type: Literal[
            "Coil:Heating:Electric", "Coil:Heating:Fuel", "Coil:Heating:Steam", "Coil:Heating:Water"
        ],
        reheat_coil_name: str,
        availability_schedule_name: str | None = ...,
        supply_air_inlet_node_name: str | None = ...,
        secondary_air_inlet_node_name: str | None = ...,
        outlet_node_name: str | None = ...,
        zone_mixer_name: str | None = ...,
        fan_name: str | None = ...,
        maximum_hot_water_or_steam_flow_rate: float | Literal["Autosize"] | None = ...,
        minimum_hot_water_or_steam_flow_rate: float | None = 0,
        convergence_tolerance: float | None = 0.001,
    ) -> None:
        """Create a new ``AirTerminal:SingleDuct:ParallelPIU:Reheat`` and add it to the document.

        Central air system terminal unit, single duct, variable volume, parallel powered induction unit (PIU), with reheat coil (hot water, electric, gas, or steam).

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-air-distribution-equipment/#airterminalsingleductparallelpiureheat
        """

class AnyCoilCoolingDXTwoSpeed:
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
        unit_internal_static_air_pressure: float | None = ...,
        low_speed_gross_rated_cooling_cop: float | None = 3,
        condenser_air_inlet_node_name: str | None = ...,
        condenser_type: Literal["AirCooled", "EvaporativelyCooled"] | None = "AirCooled",
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

class DehumidifierDesiccantSystem:
    def __call__(
        self,
        name: str,
        /,
        *,
        desiccant_heat_exchanger_object_type: Literal["HeatExchanger:Desiccant:BalancedFlow"],
        desiccant_heat_exchanger_name: str,
        sensor_node_name: str,
        regeneration_air_fan_object_type: Literal["Fan:ConstantVolume", "Fan:OnOff", "Fan:SystemModel"],
        regeneration_air_fan_name: str,
        availability_schedule_name: str | None = ...,
        regeneration_air_fan_placement: Literal["BlowThrough", "DrawThrough"] | None = "DrawThrough",
        regeneration_air_heater_object_type: Literal[
            "Coil:Heating:Electric", "Coil:Heating:Fuel", "Coil:Heating:Steam", "Coil:Heating:Water"
        ]
        | None = ...,
        regeneration_air_heater_name: str | None = ...,
        regeneration_inlet_air_setpoint_temperature: float | None = 46,
        companion_cooling_coil_object_type: Literal[
            "Coil:Cooling:DX:SingleSpeed",
            "Coil:Cooling:DX:TwoStageWithHumidityControlMode",
            "Coil:Cooling:DX:VariableSpeed",
        ]
        | None = ...,
        companion_cooling_coil_name: str | None = ...,
        companion_cooling_coil_upstream_of_dehumidifier_process_inlet: Literal["No", "Yes"] | None = "No",
        companion_coil_regeneration_air_heating: Literal["No", "Yes"] | None = "No",
        exhaust_fan_maximum_flow_rate: float | None = ...,
        exhaust_fan_maximum_power: float | None = ...,
        exhaust_fan_power_curve_name: str | None = ...,
    ) -> None:
        """Create a new ``Dehumidifier:Desiccant:System`` and add it to the document.

        This compound object models a desiccant heat exchanger, an optional heater, and associated fans. The process air stream is the air which is dehumidified. The regeneration air stream is the air which is heated to regenerate the desiccant. The desiccant heat exchanger transfers both sensible and latent energy between the process and regeneration air streams. The desiccant dehumidifier is typically used in an AirLoopHVAC:OutdoorAirSystem, but can also be specified in any AirLoopHVAC.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-humidifiers-and-dehumidifiers/#dehumidifierdesiccantsystem
        """

class AirLoopHVACUnitaryHeatCool:
    def __call__(
        self,
        name: str,
        /,
        *,
        unitary_system_air_inlet_node_name: str,
        unitary_system_air_outlet_node_name: str,
        cooling_supply_air_flow_rate: float | Literal["Autosize"],
        heating_supply_air_flow_rate: float | Literal["Autosize"],
        controlling_zone_or_thermostat_location: str,
        supply_fan_object_type: Literal["Fan:ConstantVolume", "Fan:OnOff"],
        supply_fan_name: str,
        heating_coil_object_type: Literal[
            "Coil:Heating:Electric", "Coil:Heating:Fuel", "Coil:Heating:Steam", "Coil:Heating:Water"
        ],
        heating_coil_name: str,
        cooling_coil_object_type: Literal[
            "Coil:Cooling:DX:SingleSpeed",
            "Coil:Cooling:DX:VariableSpeed",
            "CoilSystem:Cooling:DX:HeatExchangerAssisted",
        ],
        cooling_coil_name: str,
        availability_schedule_name: str | None = ...,
        supply_air_fan_operating_mode_schedule_name: str | None = ...,
        maximum_supply_air_temperature: float | Literal["Autosize"] | None = 80,
        no_load_supply_air_flow_rate: float | Literal["Autosize"] | None = ...,
        fan_placement: Literal["BlowThrough", "DrawThrough"] | None = "BlowThrough",
        dehumidification_control_type: Literal["CoolReheat", "Multimode", "None"] | None = "None",
        reheat_coil_object_type: Literal[
            "Coil:Heating:Desuperheater",
            "Coil:Heating:Electric",
            "Coil:Heating:Fuel",
            "Coil:Heating:Steam",
            "Coil:Heating:Water",
        ]
        | None = ...,
        reheat_coil_name: str | None = ...,
    ) -> None:
        """Create a new ``AirLoopHVAC:UnitaryHeatCool`` and add it to the document.

        Unitary system, heating and cooling with constant volume supply fan (continuous or cycling), direct expansion (DX) cooling coil, heating coil (gas, electric, hot water, or steam), and optional reheat coil for dehumidification control. Identical to AirLoopHVAC:Unitary:Furnace:HeatCool.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-unitary-equipment/#airloophvacunitaryheatcool
        """

class AnyAirLoopHVACUnitaryHeatPumpAirToAir:
    def __call__(
        self,
        name: str,
        /,
        *,
        air_inlet_node_name: str,
        air_outlet_node_name: str,
        cooling_supply_air_flow_rate: float | Literal["Autosize"],
        heating_supply_air_flow_rate: float | Literal["Autosize"],
        controlling_zone_or_thermostat_location: str,
        supply_air_fan_object_type: Literal["Fan:ConstantVolume", "Fan:OnOff"],
        supply_air_fan_name: str,
        heating_coil_object_type: Literal[
            "Coil:Heating:DX:SingleSpeed", "Coil:Heating:DX:VariableSpeed", "CoilSystem:IntegratedHeatPump:AirSource"
        ],
        heating_coil_name: str,
        cooling_coil_object_type: Literal[
            "Coil:Cooling:DX:SingleSpeed",
            "Coil:Cooling:DX:VariableSpeed",
            "CoilSystem:Cooling:DX:HeatExchangerAssisted",
            "CoilSystem:IntegratedHeatPump:AirSource",
        ],
        cooling_coil_name: str,
        supplemental_heating_coil_object_type: Literal[
            "Coil:Heating:Electric", "Coil:Heating:Fuel", "Coil:Heating:Steam", "Coil:Heating:Water"
        ],
        supplemental_heating_coil_name: str,
        maximum_supply_air_temperature_from_supplemental_heater: float | Literal["Autosize"],
        availability_schedule_name: str | None = ...,
        no_load_supply_air_flow_rate: float | Literal["Autosize"] | None = ...,
        maximum_outdoor_dry_bulb_temperature_for_supplemental_heater_operation: float | None = 21,
        fan_placement: Literal["BlowThrough", "DrawThrough"] | None = "BlowThrough",
        supply_air_fan_operating_mode_schedule_name: str | None = ...,
        dehumidification_control_type: Literal["CoolReheat", "Multimode", "None"] | None = "None",
    ) -> None:
        """Create a new ``AirLoopHVAC:UnitaryHeatPump:AirToAir`` and add it to the document.

        Unitary heat pump system, heating and cooling, single-speed with supply fan, direct expansion (DX) cooling coil, DX heating coil (air-to-air heat pump), and supplemental heating coil (gas, electric, hot water, or steam).

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-unitary-equipment/#airloophvacunitaryheatpumpairtoair
        """

class AirLoopHVACZoneMixer:
    def __call__(
        self,
        name: str,
        /,
        *,
        outlet_node_name: str,
        nodes: Sequence[_g.AirLoopHVACZoneMixerNodesItem | _g.AirLoopHVACZoneMixerNodesGroup] = ...,
    ) -> None:
        """Create a new ``AirLoopHVAC:ZoneMixer`` and add it to the document.

        Mix N inlet air streams into one (currently 500 per air loop, but extensible). Node names cannot be duplicated within a single zone mixer (AirLoopHVAC:ZoneMixer) list.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-air-path/#airloophvaczonemixer
        """

class AnyPlantEquipmentOperationSchemes:
    def __call__(
        self,
        name: str,
        /,
        *,
        control_scheme_1_object_type: Literal[
            "PlantEquipmentOperation:ComponentSetpoint",
            "PlantEquipmentOperation:CoolingLoad",
            "PlantEquipmentOperation:HeatingLoad",
            "PlantEquipmentOperation:ThermalEnergyStorage",
            "PlantEquipmentOperation:Uncontrolled",
            "PlantEquipmentOperation:UserDefined",
        ],
        control_scheme_1_name: str,
        control_scheme_1_schedule_name: str,
        control_scheme_2_object_type: Literal[
            "PlantEquipmentOperation:ComponentSetpoint",
            "PlantEquipmentOperation:CoolingLoad",
            "PlantEquipmentOperation:HeatingLoad",
            "PlantEquipmentOperation:ThermalEnergyStorage",
            "PlantEquipmentOperation:Uncontrolled",
            "PlantEquipmentOperation:UserDefined",
        ]
        | None = ...,
        control_scheme_2_name: str | None = ...,
        control_scheme_2_schedule_name: str | None = ...,
        control_scheme_3_object_type: Literal[
            "PlantEquipmentOperation:ComponentSetpoint",
            "PlantEquipmentOperation:CoolingLoad",
            "PlantEquipmentOperation:HeatingLoad",
            "PlantEquipmentOperation:ThermalEnergyStorage",
            "PlantEquipmentOperation:Uncontrolled",
            "PlantEquipmentOperation:UserDefined",
        ]
        | None = ...,
        control_scheme_3_name: str | None = ...,
        control_scheme_3_schedule_name: str | None = ...,
        control_scheme_4_object_type: Literal[
            "PlantEquipmentOperation:ComponentSetpoint",
            "PlantEquipmentOperation:CoolingLoad",
            "PlantEquipmentOperation:HeatingLoad",
            "PlantEquipmentOperation:ThermalEnergyStorage",
            "PlantEquipmentOperation:Uncontrolled",
            "PlantEquipmentOperation:UserDefined",
        ]
        | None = ...,
        control_scheme_4_name: str | None = ...,
        control_scheme_4_schedule_name: str | None = ...,
        control_scheme_5_object_type: Literal[
            "PlantEquipmentOperation:ComponentSetpoint",
            "PlantEquipmentOperation:CoolingLoad",
            "PlantEquipmentOperation:HeatingLoad",
            "PlantEquipmentOperation:ThermalEnergyStorage",
            "PlantEquipmentOperation:Uncontrolled",
            "PlantEquipmentOperation:UserDefined",
        ]
        | None = ...,
        control_scheme_5_name: str | None = ...,
        control_scheme_5_schedule_name: str | None = ...,
        control_scheme_6_object_type: Literal[
            "PlantEquipmentOperation:ComponentSetpoint",
            "PlantEquipmentOperation:CoolingLoad",
            "PlantEquipmentOperation:HeatingLoad",
            "PlantEquipmentOperation:ThermalEnergyStorage",
            "PlantEquipmentOperation:Uncontrolled",
            "PlantEquipmentOperation:UserDefined",
        ]
        | None = ...,
        control_scheme_6_name: str | None = ...,
        control_scheme_6_schedule_name: str | None = ...,
        control_scheme_7_object_type: Literal[
            "PlantEquipmentOperation:ComponentSetpoint",
            "PlantEquipmentOperation:CoolingLoad",
            "PlantEquipmentOperation:HeatingLoad",
            "PlantEquipmentOperation:ThermalEnergyStorage",
            "PlantEquipmentOperation:Uncontrolled",
            "PlantEquipmentOperation:UserDefined",
        ]
        | None = ...,
        control_scheme_7_name: str | None = ...,
        control_scheme_7_schedule_name: str | None = ...,
        control_scheme_8_object_type: Literal[
            "PlantEquipmentOperation:ComponentSetpoint",
            "PlantEquipmentOperation:CoolingLoad",
            "PlantEquipmentOperation:HeatingLoad",
            "PlantEquipmentOperation:ThermalEnergyStorage",
            "PlantEquipmentOperation:Uncontrolled",
            "PlantEquipmentOperation:UserDefined",
        ]
        | None = ...,
        control_scheme_8_name: str | None = ...,
        control_scheme_8_schedule_name: str | None = ...,
    ) -> None:
        """Create a new ``PlantEquipmentOperationSchemes`` and add it to the document.

        Operation schemes are listed in 'priority' order. Note that each scheme must address the entire load and/or condition ranges for the simulation. The actual one selected for use will be the first that is 'Scheduled' on. That is, if control scheme 1 is not 'on' and control scheme 2 is -- then control scheme 2 is selected. Only plant equipment should be listed on a Control Scheme for this item.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-plant-condenser-control/#plantequipmentoperationschemes
        """

class AnyLifeCycleCostRecurringCosts:
    def __call__(
        self,
        name: str,
        /,
        *,
        category: Literal[
            "Maintenance", "MajorOverhaul", "MinorOverhaul", "Operation", "OtherOperational", "Repair", "Replacement"
        ]
        | None = "Maintenance",
        cost: float | None = ...,
        start_of_costs: Literal["BasePeriod", "ServicePeriod"] | None = "ServicePeriod",
        years_from_start: int | None = ...,
        months_from_start: int | None = ...,
        repeat_period_years: int | None = 1,
        repeat_period_months: int | None = 0,
        annual_escalation_rate: float | None = ...,
    ) -> None:
        """Create a new ``LifeCycleCost:RecurringCosts`` and add it to the document.

        Recurring costs are costs that repeat over time on a regular schedule during the study period. If costs associated with equipment do repeat but not on a regular schedule, use LifeCycleCost:NonrecurringCost objects instead.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/energyplus-economics/lifecyclecost-recurringcosts/#lifecyclecostrecurringcosts
        """
