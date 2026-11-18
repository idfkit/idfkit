"""Creation signatures of generated classes (stub only).

DO NOT EDIT — regenerate with:
    python -m idfkit.codegen.generate_stubs
"""

from __future__ import annotations

from collections.abc import Sequence
from typing import Literal

from .. import _generated_types as _g

class MaterialPropertyHeatAndMoistureTransferRedistribution:
    def __call__(
        self,
        /,
        *,
        material_name: str,
        number_of_redistribution_points: int,
        moisture_content_1: float,
        liquid_transport_coefficient_1: float,
        moisture_content_2: float | None = ...,
        liquid_transport_coefficient_2: float | None = ...,
        moisture_content_3: float | None = ...,
        liquid_transport_coefficient_3: float | None = ...,
        moisture_content_4: float | None = ...,
        liquid_transport_coefficient_4: float | None = ...,
        moisture_content_5: float | None = ...,
        liquid_transport_coefficient_5: float | None = ...,
        moisture_content_6: float | None = ...,
        liquid_transport_coefficient_6: float | None = ...,
        moisture_content_7: float | None = ...,
        liquid_transport_coefficient_7: float | None = ...,
        moisture_content_8: float | None = ...,
        liquid_transport_coefficient_8: float | None = ...,
        moisture_content_9: float | None = ...,
        liquid_transport_coefficient_9: float | None = ...,
        moisture_content_10: float | None = ...,
        liquid_transport_coefficient_10: float | None = ...,
        moisture_content_11: float | None = ...,
        liquid_transport_coefficient_11: float | None = ...,
        moisture_content_12: float | None = ...,
        liquid_transport_coefficient_12: float | None = ...,
        moisture_content_13: float | None = ...,
        liquid_transport_coefficient_13: float | None = ...,
        moisture_content_14: float | None = ...,
        liquid_transport_coefficient_14: float | None = ...,
        moisture_content_15: float | None = ...,
        liquid_transport_coefficient_15: float | None = ...,
        moisture_content_16: float | None = ...,
        liquid_transport_coefficient_16: float | None = ...,
        moisture_content_17: float | None = ...,
        liquid_transport_coefficient_17: float | None = ...,
        moisture_content_18: float | None = ...,
        liquid_transport_coefficient_18: float | None = ...,
        moisture_content_19: float | None = ...,
        liquid_transport_coefficient_19: float | None = ...,
        moisture_content_20: float | None = ...,
        liquid_transport_coefficient_20: float | None = ...,
        moisture_content_21: float | None = ...,
        liquid_transport_coefficient_21: float | None = ...,
        moisture_content_22: float | None = ...,
        liquid_transport_coefficient_22: float | None = ...,
        moisture_content_23: float | None = ...,
        liquid_transport_coefficient_23: float | None = ...,
        moisture_content_24: float | None = ...,
        liquid_transport_coefficient_24: float | None = ...,
        moisture_content_25: float | None = ...,
        liquid_transport_coefficient_25: float | None = ...,
    ) -> None:
        """Create a new ``MaterialProperty:HeatAndMoistureTransfer:Redistribution`` and add it to the document.

        HeatBalanceAlgorithm = CombinedHeatAndMoistureFiniteElement solution algorithm only. Relationship between liquid transport coefficient and moisture content Has no effect with other HeatBalanceAlgorithm solution algorithms

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-surface-construction-elements/#materialpropertyheatandmoisturetransferredistribution
        """

class ShadingPropertyReflectance:
    def __call__(
        self,
        /,
        *,
        shading_surface_name: str,
        diffuse_solar_reflectance_of_unglazed_part_of_shading_surface: float | None = 0.2,
        diffuse_visible_reflectance_of_unglazed_part_of_shading_surface: float | None = 0.2,
        fraction_of_shading_surface_that_is_glazed: float | None = 0,
        glazing_construction_name: str | None = ...,
    ) -> None:
        """Create a new ``ShadingProperty:Reflectance`` and add it to the document.

        If this object is not defined for a shading surface the default values listed in following fields will be used in the solar reflection calculation.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-thermal-zone-description-geometry/#shadingpropertyreflectance
        """

class AnyHVACTemplatePlantBoiler:
    def __call__(
        self,
        name: str,
        /,
        *,
        boiler_type: Literal["CondensingHotWaterBoiler", "DistrictHotWater", "HotWaterBoiler"],
        capacity: float | Literal["Autosize"] | None = "Autosize",
        efficiency: float | None = 0.8,
        fuel_type: Literal["Coal", "Diesel", "Electricity", "Gasoline", "NaturalGas", "OtherFuel1", "OtherFuel2"]
        | None = ...,
        priority: str | None = ...,
        sizing_factor: float | None = 1,
        minimum_part_load_ratio: float | None = 0,
        maximum_part_load_ratio: float | None = 1.1,
        optimum_part_load_ratio: float | None = 1,
        water_outlet_upper_temperature_limit: float | None = 100,
        template_plant_loop_type: Literal["HotWater", "MixedWater"] | None = ...,
    ) -> None:
        """Create a new ``HVACTemplate:Plant:Boiler`` and add it to the document.

        This object adds a boiler to an HVACTemplate:Plant:HotWaterLoop or MixedWaterLoop.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/hvac-template-objects/group-hvac-templates/#hvactemplateplantboiler
        """

class AirLoopHVACZoneSplitter:
    def __call__(
        self,
        name: str,
        /,
        *,
        inlet_node_name: str,
        nodes: Sequence[_g.AirLoopHVACZoneSplitterNodesItem | _g.AirLoopHVACZoneSplitterNodesGroup] = ...,
    ) -> None:
        """Create a new ``AirLoopHVAC:ZoneSplitter`` and add it to the document.

        Split one air stream into N outlet streams (currently 500 per air loop, but extensible). Node names cannot be duplicated within a single zone splitter (AirLoopHVAC:ZoneSplitter) list.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-air-path/#airloophvaczonesplitter
        """

class AirLoopHVACSplitter:
    def __call__(
        self,
        name: str,
        /,
        *,
        inlet_node_name: str,
        nodes: Sequence[_g.AirLoopHVACSplitterNodesItem | _g.AirLoopHVACSplitterNodesGroup] = ...,
    ) -> None:
        """Create a new ``AirLoopHVAC:Splitter`` and add it to the document.

        Split one air stream from AirLoopHVAC:DedicatedOutdoorAirSystem outlet node into N outlet streams (currently 10 as default, but extensible). Node names should be Outdoor Air Stream Node Name in OutdoorAir:Mixer objects served by AirLoopHVAC objects listed in AirLoopHVAC:DedicatedOutdoorAirSystem.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-air-path/#airloophvacsplitter
        """

class DistrictHeatingSteam:
    def __call__(
        self,
        name: str,
        /,
        *,
        steam_inlet_node_name: str,
        steam_outlet_node_name: str,
        nominal_capacity: float | Literal["Autosize"] | None = ...,
        capacity_fraction_schedule_name: str | None = ...,
    ) -> None:
        """Create a new ``DistrictHeating:Steam`` and add it to the document.

        Centralized source of Steam, such as a district heating system.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-plant-equipment/#districtheatingsteam
        """

class CoolingTowerTwoSpeed:
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
        design_water_flow_rate: float | Literal["Autosize"] | None = ...,
        high_fan_speed_u_factor_times_area_value: float | Literal["Autosize"] | None = ...,
        low_fan_speed_air_flow_rate_sizing_factor: float | None = 0.5,
        low_fan_speed_fan_power_sizing_factor: float | None = 0.16,
        low_fan_speed_u_factor_times_area_value: float | Literal["Autocalculate"] | None = ...,
        low_fan_speed_u_factor_times_area_sizing_factor: float | None = 0.6,
        free_convection_regime_air_flow_rate: float | Literal["Autocalculate"] | None = 0,
        free_convection_regime_air_flow_rate_sizing_factor: float | None = 0.1,
        free_convection_regime_u_factor_times_area_value: float | Literal["Autocalculate"] | None = 0,
        free_convection_u_factor_times_area_value_sizing_factor: float | None = 0.1,
        performance_input_method: Literal["NominalCapacity", "UFactorTimesAreaAndDesignWaterFlowRate"]
        | None = "UFactorTimesAreaAndDesignWaterFlowRate",
        heat_rejection_capacity_and_nominal_capacity_sizing_ratio: float | None = 1.25,
        high_speed_nominal_capacity: float | None = ...,
        low_speed_nominal_capacity: float | Literal["Autocalculate"] | None = ...,
        low_speed_nominal_capacity_sizing_factor: float | None = 0.5,
        free_convection_nominal_capacity: float | Literal["Autocalculate"] | None = ...,
        free_convection_nominal_capacity_sizing_factor: float | None = 0.1,
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
        """Create a new ``CoolingTower:TwoSpeed`` and add it to the document.

        This tower model is based on Merkel's theory, which is also the basis for the tower model in ASHRAE's HVAC1 Toolkit. The open wet cooling tower is modeled as a counter flow heat exchanger with a two-speed fan drawing air through the tower (induced-draft configuration). For a multi-cell tower, the capacity and air/water flow rate inputs are for the entire tower.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-condenser-equipment/#coolingtowertwospeed
        """

class PlantEquipmentOperationChillerHeaterChangeover:
    def __call__(
        self,
        name: str,
        /,
        *,
        primary_cooling_plant_setpoint_temperature: float,
        primary_heating_plant_setpoint_at_outdoor_high_temperature: float,
        outdoor_high_temperature: float,
        primary_heating_plant_setpoint_at_outdoor_low_temperature: float,
        outdoor_low_temperature: float,
        secondary_distribution_cooling_plant_setpoint_temperature: float | None = ...,
        secondary_distribution_heating_plant_setpoint_temperature: float | None = ...,
        zone_load_polling_zonelist_name: str | None = ...,
        cooling_only_load_plant_equipment_operation_cooling_load_name: str | None = ...,
        heating_only_load_plant_equipment_operation_heating_load_name: str | None = ...,
        simultaneous_cooling_and_heating_plant_equipment_operation_cooling_load_name: str | None = ...,
        simultaneous_cooling_and_heating_plant_equipment_operation_heating_load_name: str | None = ...,
        dedicated_chilled_water_return_recovery_heat_pump_name: str | None = ...,
        dedicated_hot_water_return_recovery_heat_pump_name: str | None = ...,
        boiler_setpoint_temperature_offset: float | None = 0.5,
        primary_heating_plant_setpoint_at_backup_outdoor_low_temperature: float | None = ...,
        backup_outdoor_low_temperature: float | None = ...,
    ) -> None:
        """Create a new ``PlantEquipmentOperation:ChillerHeaterChangeover`` and add it to the document.

        Plant equipment operation object to control switchover between chiller and heater operation of chiller heater heat pump serving 2 plant loops. Poll zone loads and determine if plant should be in heating, cooling or simultaneous heating and cooling and dispatch equipment accordingly.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-plant-condenser-control/#plantequipmentoperationchillerheaterchangeover
        """

class LifeCycleCostRecurringCosts:
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
