"""Creation signatures of generated classes (stub only).

DO NOT EDIT — regenerate with:
    python -m idfkit.codegen.generate_stubs
"""

from __future__ import annotations

from collections.abc import Sequence
from typing import Literal

from typing_extensions import Never

from .. import _generated_types as _g

class ZoneAirHeatBalanceAlgorithm:
    def __call__(
        self,
        this_type_has_no_name_field: _g._PassFieldsAsKeywords = ...,
        /,
        *,
        algorithm: Literal["AnalyticalSolution", "EulerMethod", "ThirdOrderBackwardDifference"]
        | None = "ThirdOrderBackwardDifference",
        do_space_heat_balance_for_sizing: Literal["No", "Yes"] | None = "No",
        do_space_heat_balance_for_simulation: Literal["No", "Yes"] | None = "No",
        validate: bool = True,
    ) -> None:
        """Create a new ``ZoneAirHeatBalanceAlgorithm`` and add it to the document.

        Controls the zone/space air heat balance.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-simulation-parameters/#zoneairheatbalancealgorithm
        """

class SiteWeatherStation:
    def __call__(
        self,
        this_type_has_no_name_field: _g._PassFieldsAsKeywords = ...,
        /,
        *,
        wind_sensor_height_above_ground: float | None = 10,
        wind_speed_profile_exponent: float | None = 0.14,
        wind_speed_profile_boundary_layer_thickness: float | None = 270,
        air_temperature_sensor_height_above_ground: float | None = 1.5,
        validate: bool = True,
    ) -> None:
        """Create a new ``Site:WeatherStation`` and add it to the document.

        This object should only be used for non-standard weather data. Standard weather data such as TMY2, IWEC, and ASHRAE design day data are all measured at the default conditions and do not require this object.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-location-climate-weather-file-access/#siteweatherstation
        """

class SiteSolarAndVisibleSpectrum:
    def __call__(
        self,
        name: str,
        /,
        *,
        spectrum_data_method: Literal["Default", "UserDefined"] | None = "Default",
        solar_spectrum_data_object_name: str | None = ...,
        visible_spectrum_data_object_name: str | None = ...,
        validate: bool = True,
    ) -> None:
        """Create a new ``Site:SolarAndVisibleSpectrum`` and add it to the document.

        If this object is omitted, the default solar and visible spectrum data will be used.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-location-climate-weather-file-access/#sitesolarandvisiblespectrum
        """

class WindowThermalModelParams:
    def __call__(
        self,
        name: str,
        /,
        *,
        standard: Literal["EN673Declared", "EN673Design", "ISO15099"] | None = "ISO15099",
        thermal_model: Literal[
            "ConvectiveScalarModel_NoSDThickness",
            "ConvectiveScalarModel_withSDThickness",
            "ISO15099",
            "ScaledCavityWidth",
        ]
        | None = "ISO15099",
        sdscalar: float | None = 1,
        deflection_model: Literal["MeasuredDeflection", "NoDeflection", "TemperatureAndPressureInput"]
        | None = "NoDeflection",
        vacuum_pressure_limit: float | None = 13.238,
        initial_temperature: float | None = 25,
        initial_pressure: float | None = 101325,
        validate: bool = True,
    ) -> None:
        """Create a new ``WindowThermalModel:Params`` and add it to the document.

        object is used to select which thermal model should be used in tarcog simulations

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-surface-construction-elements/#windowthermalmodelparams
        """

class AnySurfacePropertyConvectionCoefficients:
    def __call__(
        self,
        this_type_has_no_name_field: _g._PassFieldsAsKeywords = ...,
        /,
        *,
        surface_name: str,
        convection_coefficient_1_location: Literal["Inside", "Outside"],
        convection_coefficient_1_type: Literal[
            "ASHRAEVerticalWall",
            "AdaptiveConvectionAlgorithm",
            "AlamdariHammondStableHorizontal",
            "AlamdariHammondUnstableHorizontal",
            "AlamdariHammondVerticalWall",
            "AwbiHattonHeatedFloor",
            "AwbiHattonHeatedWall",
            "BeausoleilMorrisonMixedAssistedWall",
            "BeausoleilMorrisonMixedOpposingWall",
            "BeausoleilMorrisonMixedStableCeiling",
            "BeausoleilMorrisonMixedStableFloor",
            "BeausoleilMorrisonMixedUnstableCeiling",
            "BeausoleilMorrisonMixedUnstableFloor",
            "ClearRoof",
            "DOE-2",
            "EmmelRoof",
            "EmmelVertical",
            "FisherPedersenCeilingDiffuserCeiling",
            "FisherPedersenCeilingDiffuserFloor",
            "FisherPedersenCeilingDiffuserWalls",
            "FohannoPolidoriVerticalWall",
            "GoldsteinNovoselacCeilingDiffuserFloor",
            "GoldsteinNovoselacCeilingDiffuserWalls",
            "GoldsteinNovoselacCeilingDiffuserWindow",
            "ISO15099Windows",
            "KaradagChilledCeiling",
            "KhalifaEq3WallAwayFromHeat",
            "KhalifaEq4CeilingAwayFromHeat",
            "KhalifaEq5WallNearHeat",
            "KhalifaEq6NonHeatedWalls",
            "KhalifaEq7Ceiling",
            "McAdams",
            "Mitchell",
            "MoWitt",
            "NusseltJurges",
            "Schedule",
            "Simple",
            "SimpleCombined",
            "TARP",
            "UserCurve",
            "Value",
            "WaltonStableHorizontalOrTilt",
            "WaltonUnstableHorizontalOrTilt",
        ],
        convection_coefficient_1: float | None = ...,
        convection_coefficient_1_schedule_name: str | None = ...,
        convection_coefficient_1_user_curve_name: str | None = ...,
        convection_coefficient_2_location: Literal["Inside", "Outside"] | None = ...,
        convection_coefficient_2_type: Literal[
            "ASHRAEVerticalWall",
            "AdaptiveConvectionAlgorithm",
            "AlamdariHammondStableHorizontal",
            "AlamdariHammondUnstableHorizontal",
            "AlamdariHammondVerticalWall",
            "AwbiHattonHeatedFloor",
            "AwbiHattonHeatedWall",
            "BeausoleilMorrisonMixedAssistedWall",
            "BeausoleilMorrisonMixedOpposingWall",
            "BeausoleilMorrisonMixedStableCeiling",
            "BeausoleilMorrisonMixedStableFloor",
            "BeausoleilMorrisonMixedUnstableCeiling",
            "BeausoleilMorrisonMixedUnstableFloor",
            "ClearRoof",
            "DOE-2",
            "EmmelRoof",
            "EmmelVertical",
            "FisherPedersenCeilingDiffuserCeiling",
            "FisherPedersenCeilingDiffuserFloor",
            "FisherPedersenCeilingDiffuserWalls",
            "FohannoPolidoriVerticalWall",
            "GoldsteinNovoselacCeilingDiffuserFloor",
            "GoldsteinNovoselacCeilingDiffuserWalls",
            "GoldsteinNovoselacCeilingDiffuserWindow",
            "ISO15099Windows",
            "KaradagChilledCeiling",
            "KhalifaEq3WallAwayFromHeat",
            "KhalifaEq4CeilingAwayFromHeat",
            "KhalifaEq5WallNearHeat",
            "KhalifaEq6NonHeatedWalls",
            "KhalifaEq7Ceiling",
            "McAdams",
            "Mitchell",
            "MoWitt",
            "NusseltJurges",
            "Schedule",
            "Simple",
            "SimpleCombined",
            "TARP",
            "UserCurve",
            "Value",
            "WaltonStableHorizontalOrTilt",
            "WaltonUnstableHorizontalOrTilt",
        ]
        | None = ...,
        convection_coefficient_2: float | None = 0.1,
        convection_coefficient_2_schedule_name: str | None = ...,
        convection_coefficient_2_user_curve_name: str | None = ...,
        validate: bool = True,
    ) -> None:
        """Create a new ``SurfaceProperty:ConvectionCoefficients`` and add it to the document.

        Allow user settable interior and/or exterior convection coefficients. Note that some other factors may limit the lower bounds for these values, such as for windows, the interior convection coefficient must be >.28, for trombe wall algorithm selection (zone), the interior convection coefficient must be >.1 for TARP interior convection, the lower limit is also .1 Minimum and maximum limits are set in HeatBalanceAlgorithm object. Defaults in HeatBalanceAlgorithm object are [.1,1000].

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-advanced-surface-concepts/#surfacepropertyconvectioncoefficients
        """

class AnyGasEquipment:
    def __call__(
        self,
        name: str,
        /,
        *,
        narrow_with_as_version_first: Never,
        schedule_name: str,
        design_level_calculation_method: Literal[
            "EquipmentLevel", "Power/Area", "Power/Person", "Watts/Area", "Watts/Person"
        ]
        | None = "EquipmentLevel",
        design_level: float | None = ...,
        power_per_person: float | None = ...,
        fraction_latent: float | None = 0,
        fraction_radiant: float | None = 0,
        fraction_lost: float | None = 0,
        carbon_dioxide_generation_rate: float | None = 0,
        end_use_subcategory: str | None = "General",
        validate: bool = True,
    ) -> None:
        """Create a new ``GasEquipment`` and add it to the document.

        Sets internal gains and contaminant rates for gas equipment in the zone. If a ZoneList, SpaceList, or a Zone comprised of more than one Space is specified then this definition applies to all applicable spaces, and each instance will be named with the Space Name plus this Object Name.

        No call suits every release: narrow the document with ``as_version`` first.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-internal-gains-people-lights-other/#gasequipment
        """

class AnyHVACTemplateZoneWaterToAirHeatPump:
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
        cooling_coil_type: Literal["Coil:Cooling:WaterToAirHeatPump:EquationFit"] | None = ...,
        cooling_coil_gross_rated_total_capacity: float | Literal["Autosize"] | None = "Autosize",
        cooling_coil_gross_rated_sensible_heat_ratio: float | Literal["Autosize"] | None = "Autosize",
        cooling_coil_gross_rated_cop: float | None = 3.5,
        heat_pump_heating_coil_type: Literal["Coil:Heating:WaterToAirHeatPump:EquationFit"] | None = ...,
        heat_pump_heating_coil_gross_rated_capacity: float | Literal["Autosize"] | None = "Autosize",
        heat_pump_heating_coil_gross_rated_cop: float | None = 4.2,
        supplemental_heating_coil_availability_schedule_name: str | None = ...,
        supplemental_heating_coil_capacity: float | Literal["Autosize"] | None = "Autosize",
        maximum_cycling_rate: float | None = 2.5,
        heat_pump_fan_delay_time: float | None = 60,
        dedicated_outdoor_air_system_name: str | None = ...,
        supplemental_heating_coil_type: Literal["Electric", "HotWater"] | None = "Electric",
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
        heat_pump_coil_water_flow_mode: Literal["Constant", "ConstantOnDemand", "Cycling"] | None = "Cycling",
        design_specification_outdoor_air_object_name: str | None = ...,
        design_specification_zone_air_distribution_object_name: str | None = ...,
        baseboard_heating_type: Literal["Electric", "HotWater", "None"] | None = "None",
        baseboard_heating_availability_schedule_name: str | None = ...,
        baseboard_heating_capacity: float | Literal["Autosize"] | None = "Autosize",
        validate: bool = True,
    ) -> None:
        """Create a new ``HVACTemplate:Zone:WaterToAirHeatPump`` and add it to the document.

        Water to Air Heat Pump to be used with HVACTemplate:Plant:MixedWaterLoop

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/hvac-template-objects/group-hvac-templates/#hvactemplatezonewatertoairheatpump
        """

class CoilHeatingDesuperheater:
    def __call__(
        self,
        name: str,
        /,
        *,
        air_inlet_node_name: str,
        air_outlet_node_name: str,
        heating_source_object_type: Literal[
            "Coil:Cooling:DX",
            "Coil:Cooling:DX:SingleSpeed",
            "Coil:Cooling:DX:TwoSpeed",
            "Coil:Cooling:DX:TwoStageWithHumidityControlMode",
            "Coil:Cooling:DX:VariableSpeed",
            "Refrigeration:CompressorRack",
            "Refrigeration:Condenser:AirCooled",
            "Refrigeration:Condenser:EvaporativeCooled",
            "Refrigeration:Condenser:WaterCooled",
        ],
        heating_source_name: str,
        availability_schedule_name: str | None = ...,
        heat_reclaim_recovery_efficiency: float | None = ...,
        temperature_setpoint_node_name: str | None = ...,
        on_cycle_parasitic_electric_load: float | None = ...,
        validate: bool = True,
    ) -> None:
        """Create a new ``Coil:Heating:Desuperheater`` and add it to the document.

        Desuperheater air heating coil. The heating energy provided by this coil is reclaimed from the superheated refrigerant gas leaving a compressor and does not impact the performance of the compressor. If the coil is located directly in an air loop branch or outdoor air equipment list, then it is controlled on leaving air temperature and the Temperature Setpoint Node Name must be specified. If the coil is contained within another component such as a unitary system, then the coil is controlled by the parent component and the setpoint node name is not entered.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-heating-and-cooling-coils/#coilheatingdesuperheater
        """

class OutdoorAirNodeList:
    def __call__(
        self,
        this_type_has_no_name_field: _g._PassFieldsAsKeywords = ...,
        /,
        *,
        nodes: Sequence[_g.OutdoorAirNodeListNodesItem | _g.OutdoorAirNodeListNodesGroup] = ...,
        validate: bool = True,
    ) -> None:
        """Create a new ``OutdoorAir:NodeList`` and add it to the document.

        This object sets the temperature and humidity conditions for an outdoor air node using the weather data values. to vary outdoor air node conditions with height above ground use OutdoorAir:Node instead of this object. This object may be used more than once. The same node name may not appear in both an OutdoorAir:Node object and an OutdoorAir:NodeList object.

        ``nodes`` takes the extensible groups in order, one dict per group:

        ```python
        doc["OutdoorAir:NodeList"].add(
            nodes=[
                {"node_or_nodelist_name": "Node or NodeList 1"},
                {"node_or_nodelist_name": "Node or NodeList 2"},
            ],
        )
        ```

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-air-distribution/#outdoorairnodelist
        """

class GroundHeatExchangerVerticalProperties:
    def __call__(
        self,
        name: str,
        /,
        *,
        depth_of_top_of_borehole: float,
        borehole_length: float,
        borehole_diameter: float,
        grout_thermal_conductivity: float,
        grout_thermal_heat_capacity: float,
        pipe_thermal_conductivity: float,
        pipe_thermal_heat_capacity: float,
        pipe_outer_diameter: float,
        pipe_thickness: float,
        u_tube_distance: float,
        validate: bool = True,
    ) -> None:
        """Create a new ``GroundHeatExchanger:Vertical:Properties`` and add it to the document.

        Properties for vertical ground heat exchanger systems

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-condenser-equipment/#groundheatexchangerverticalproperties
        """

class PlantEquipmentOperationUncontrolled:
    def __call__(self, name: str, /, *, equipment_list_name: str, validate: bool = True) -> None:
        """Create a new ``PlantEquipmentOperation:Uncontrolled`` and add it to the document.

        Plant equipment operation scheme for uncontrolled operation. Specifies a group of equipment that runs if the loop is active, unless turned off by the loop flow resolver to maintain continuity in the fluid loop.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-plant-condenser-control/#plantequipmentoperationuncontrolled
        """

class AnyEnergyManagementSystemMeteredOutputVariable:
    def __call__(
        self,
        name: str,
        /,
        *,
        ems_variable_name: str,
        update_frequency: Literal["SystemTimestep", "ZoneTimestep"],
        resource_type: Literal[
            "Coal",
            "CondensateWaterCollected",
            "Diesel",
            "DistrictCooling",
            "Electricity",
            "ElectricityProducedOnSite",
            "EnergyTransfer",
            "Gasoline",
            "MainsWaterSupply",
            "NaturalGas",
            "OnSiteWaterProduced",
            "OtherFuel1",
            "OtherFuel2",
            "Propane",
            "RainWaterCollected",
            "SolarAirHeating",
            "SolarWaterHeating",
            "WaterUse",
            "WellWaterDrawn",
        ],
        group_type: Literal["Building", "HVAC", "Plant", "System"],
        end_use_category: Literal[
            "Baseboard",
            "Boilers",
            "Chillers",
            "Cooling",
            "CoolingCoils",
            "ExteriorEquipment",
            "ExteriorLights",
            "Fans",
            "HeatRecovery",
            "HeatRecoveryForCooling",
            "HeatRecoveryForHeating",
            "HeatRejection",
            "Heating",
            "HeatingCoils",
            "Humidifier",
            "InteriorEquipment",
            "InteriorLights",
            "OnSiteGeneration",
            "Pumps",
            "Refrigeration",
            "WaterSystems",
        ],
        ems_program_or_subroutine_name: str | None = ...,
        end_use_subcategory: str | None = ...,
        units: str | None = ...,
        validate: bool = True,
    ) -> None:
        """Create a new ``EnergyManagementSystem:MeteredOutputVariable`` and add it to the document.

        This object sets up an EnergyPlus output variable from an Erl variable

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-energy-management-system-ems/#energymanagementsystemmeteredoutputvariable
        """

class RefrigerationWalkIn:
    def __call__(
        self,
        name: str,
        /,
        *,
        rated_coil_cooling_capacity: float,
        operating_temperature: float,
        rated_cooling_source_temperature: float,
        rated_total_heating_power: float,
        rated_total_lighting_power: float,
        defrost_schedule_name: str,
        insulated_floor_surface_area: float,
        availability_schedule_name: str | None = ...,
        heating_power_schedule_name: str | None = ...,
        rated_cooling_coil_fan_power: float | None = 375,
        rated_circulation_fan_power: float | None = 0,
        lighting_schedule_name: str | None = ...,
        defrost_type: Literal["Electric", "HotFluid", "None", "OffCycle"] | None = "Electric",
        defrost_control_type: Literal["TemperatureTermination", "TimeSchedule"] | None = "TimeSchedule",
        defrost_drip_down_schedule_name: str | None = ...,
        defrost_power: float | None = ...,
        temperature_termination_defrost_fraction_to_ice: float | None = ...,
        restocking_schedule_name: str | None = ...,
        average_refrigerant_charge_inventory: float | None = 0,
        insulated_floor_u_value: float | None = 0.3154,
        zone_data: Sequence[_g.RefrigerationWalkInZoneDataItem | _g.RefrigerationWalkInZoneDataGroup] = ...,
        validate: bool = True,
    ) -> None:
        """Create a new ``Refrigeration:WalkIn`` and add it to the document.

        Works in conjunction with a compressor rack, a refrigeration system, or a refrigeration secondary system to simulate the performance of a walk-in cooler. The walk-in cooler model uses information at rated conditions along with input descriptions for heat transfer surfaces facing multiple zones to determine performance.

        ``zone_data`` takes the extensible groups in order, one dict per group:

        ```python
        doc["Refrigeration:WalkIn"].add(
            "Refrigeration WalkIn 1",
            rated_coil_cooling_capacity=0.0,
            operating_temperature=0.0,
            rated_cooling_source_temperature=0.0,
            rated_total_heating_power=0.0,
            rated_total_lighting_power=0.0,
            defrost_schedule_name="Defrost Schedule 1",
            insulated_floor_surface_area=1.0,
            zone_data=[
                {
                    "zone_name": "Zone 1",
                    "total_insulated_surface_area_facing_zone": 1.0,
                    "insulated_surface_u_value_facing_zone": 0.3154,
                    "area_of_glass_reach_in_doors_facing_zone": 0.0,
                    "height_of_glass_reach_in_doors_facing_zone": 1.5,
                    "glass_reach_in_door_u_value_facing_zone": 1.136,
                    "glass_reach_in_door_opening_schedule_name_facing_zone": "Glass Reach In Door Opening Schedule Name Facing Zone 1",
                    "area_of_stocking_doors_facing_zone": 0.0,
                    "height_of_stocking_doors_facing_zone": 3.0,
                    "stocking_door_u_value_facing_zone": 0.3785,
                    "stocking_door_opening_schedule_name_facing_zone": "Stocking Door Opening Schedule Name Facing Zone 1",
                    "stocking_door_opening_protection_type_facing_zone": "AirCurtain",
                },
                {
                    "zone_name": "Zone 2",
                    "total_insulated_surface_area_facing_zone": 1.0,
                    "insulated_surface_u_value_facing_zone": 0.3154,
                    "area_of_glass_reach_in_doors_facing_zone": 0.0,
                    "height_of_glass_reach_in_doors_facing_zone": 1.5,
                    "glass_reach_in_door_u_value_facing_zone": 1.136,
                    "glass_reach_in_door_opening_schedule_name_facing_zone": "Glass Reach In Door Opening Schedule Name Facing Zone 2",
                    "area_of_stocking_doors_facing_zone": 0.0,
                    "height_of_stocking_doors_facing_zone": 3.0,
                    "stocking_door_u_value_facing_zone": 0.3785,
                    "stocking_door_opening_schedule_name_facing_zone": "Stocking Door Opening Schedule Name Facing Zone 2",
                    "stocking_door_opening_protection_type_facing_zone": "AirCurtain",
                },
            ],
        )
        ```

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-refrigeration/#refrigerationwalkin
        """
