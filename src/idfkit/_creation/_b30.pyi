"""Creation signatures of generated classes (stub only).

DO NOT EDIT — regenerate with:
    python -m idfkit.codegen.generate_stubs
"""

from __future__ import annotations

from typing import Literal

from .. import _generated_types as _g

class ConvergenceLimits:
    def __call__(
        self,
        /,
        *,
        minimum_system_timestep: int | None = ...,
        maximum_hvac_iterations: int | None = 20,
        minimum_plant_iterations: int | None = 2,
        maximum_plant_iterations: int | None = 8,
    ) -> None:
        """Create a new ``ConvergenceLimits`` and add it to the document.

        Specifies limits on HVAC system simulation timesteps and iterations. This item is an advanced feature that should be used only with caution.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-simulation-parameters/#convergencelimits
        """

class ComplianceBuilding:
    def __call__(self, /, *, building_rotation_for_appendix_g: float | None = 0) -> None:
        """Create a new ``Compliance:Building`` and add it to the document.

        Building level inputs related to compliance to building standards, building codes, and beyond energy code programs.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-compliance-objects/#compliancebuilding
        """

class ScheduleWeekRule:
    def __call__(
        self,
        name: str,
        /,
        *,
        schedule_year_rules_name: str,
        rule_priority_order: int,
        day_schedule_name: str,
        apply_sunday: Literal["", "No", "Yes"] | None = "No",
        apply_monday: Literal["", "No", "Yes"] | None = "No",
        apply_tuesday: Literal["", "No", "Yes"] | None = "No",
        apply_wednesday: Literal["", "No", "Yes"] | None = "No",
        apply_thursday: Literal["", "No", "Yes"] | None = "No",
        apply_friday: Literal["", "No", "Yes"] | None = "No",
        apply_saturday: Literal["", "No", "Yes"] | None = "No",
        date_ranges: list[_g.ScheduleWeekRuleDateRangesItem] = ...,
    ) -> None:
        """Create a new ``Schedule:Week:Rule`` and add it to the document.

        A Schedule:Week:Rule defines one override rule for a Schedule:Year:Rules. Rules are evaluated in ascending Rule Priority Order; the first matching rule wins. A rule matches a day if: (a) the day falls within the specified date ranges, AND (b) the corresponding Apply <DayOfWeek> field is Yes.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-schedules/#scheduleweekrule
        """

class AnyScheduleFile:
    def __call__(
        self,
        name: str,
        /,
        *,
        file_name: str,
        column_number: int,
        rows_to_skip_at_top: int,
        schedule_type_limits_name: str | None = ...,
        number_of_hours_of_data: float | None = 8760,
        column_separator: Literal["", "Comma", "Semicolon", "Tab"] | None = "Comma",
        interpolate_to_timestep: Literal["", "No", "Yes"] | None = "No",
        minutes_per_item: int | None = ...,
    ) -> None:
        """Create a new ``Schedule:File`` and add it to the document.

        A Schedule:File points to a text computer file that has 8760-8784 hours of data.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-schedules/#schedulefile
        """

class AnyConstructionAirBoundary:
    def __call__(
        self,
        name: str,
        /,
        *,
        air_exchange_method: Literal["", "None", "SimpleMixing"] | None = "None",
        simple_mixing_air_changes_per_hour: float | None = 0.5,
        simple_mixing_schedule_name: str | None = ...,
    ) -> None:
        """Create a new ``Construction:AirBoundary`` and add it to the document.

        Indicates an open boundary between two zones. It may be used for base surfaces and fenestration surfaces. The two adjacent zones are grouped together for solar, daylighting and radiant exchange. When this construction type is used, the Outside Boundary Condition of the surface (or the base surface of a fenestration surface) must be either Surface or Zone. A base surface with Construction:AirBoundary cannot hold any fenestration surfaces.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-surface-construction-elements/#constructionairboundary
        """

class Space:
    def __call__(
        self,
        name: str,
        /,
        *,
        zone_name: str,
        ceiling_height: float | Literal["", "Autocalculate"] | None = "Autocalculate",
        volume: float | Literal["", "Autocalculate"] | None = "Autocalculate",
        floor_area: float | Literal["", "Autocalculate"] | None = "Autocalculate",
        space_type: str | None = "General",
        construction_assignment_set_name: str | None = ...,
        tags: list[_g.SpaceTagsItem] = ...,
    ) -> None:
        """Create a new ``Space`` and add it to the document.

        Defines a space (room) in the building. All Spaces are part of a Zone. Every Zone contains one or more spaces. Space is an optional input. If a Zone has no Space(s) specified in input then a default Space named <Zone Name> will be created. If some surfaces in a Zone are assigned to a space and some are not, then a default Space named <Zone Name>-Remainder will be created. Input references to Space Names must have a matching Space object (default space names may not be referenced except in output variable keys).

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-thermal-zone-description-geometry/#space
        """

class GroundHeatTransferSlabMaterials:
    def __call__(
        self,
        /,
        *,
        nmat_number_of_materials: float,
        albedo_surface_albedo_no_snow: float | None = 0.16,
        albedo_surface_albedo_snow: float | None = 0.4,
        epslw_surface_emissivity_no_snow: float | None = 0.94,
        epslw_surface_emissivity_snow: float | None = 0.86,
        z0_surface_roughness_no_snow: float | None = 0.75,
        z0_surface_roughness_snow: float | None = 0.25,
        hin_indoor_hconv_downward_flow: float | None = 6.13,
        hin_indoor_hconv_upward: float | None = 9.26,
    ) -> None:
        """Create a new ``GroundHeatTransfer:Slab:Materials`` and add it to the document.

        Object gives an overall description of the slab ground heat transfer model.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-detailed-ground-heat-transfer/#groundheattransferslabmaterials
        """

class RoomAirNodeAirflowNetworkHVACEquipment:
    def __call__(
        self,
        name: str = "",
        /,
        *,
        equipment_fractions: list[_g.RoomAirNodeAirflowNetworkHVACEquipmentEquipmentFractionsItem] = ...,
    ) -> None:
        """Create a new ``RoomAir:Node:AirflowNetwork:HVACEquipment`` and add it to the document.

        define the zone equipment associated with one particular RoomAir:Node

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-room-air-models/#roomairnodeairflownetworkhvacequipment
        """

class Lights:
    def __call__(
        self,
        name: str,
        /,
        *,
        zone_or_zonelist_or_space_or_spacelist_name: str,
        schedule_name: str,
        design_level_calculation_method: Literal["", "LightingLevel", "Watts/Area", "Watts/Person"]
        | None = "LightingLevel",
        lighting_level: float | None = ...,
        watts_per_floor_area: float | None = ...,
        watts_per_person: float | None = ...,
        return_air_fraction: float | None = 0,
        fraction_radiant: float | None = 0,
        fraction_visible: float | None = 0,
        fraction_replaceable: float | None = 1,
        end_use_subcategory: str | None = "General",
        return_air_fraction_calculated_from_plenum_temperature: Literal["", "No", "Yes"] | None = "No",
        return_air_fraction_function_of_plenum_temperature_coefficient_1: float | None = 0,
        return_air_fraction_function_of_plenum_temperature_coefficient_2: float | None = 0,
        return_air_heat_gain_node_name: str | None = ...,
        exhaust_air_heat_gain_node_name: str | None = ...,
    ) -> None:
        """Create a new ``Lights`` and add it to the document.

        Sets internal gains for lights in the zone. If a ZoneList, SpaceList, or a Zone comprised of more than one Space is specified then this definition applies to all applicable spaces, and each instance will be named with the Space Name plus this Object Name.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/energyplus-economics/cost-estimating/#lights
        """

class AirflowNetworkMultiZoneSpecifiedFlowRate:
    def __call__(
        self,
        name: str,
        /,
        *,
        air_flow_value: float,
        air_flow_units: Literal["", "MassFlow", "VolumetricFlow"] | None = "MassFlow",
    ) -> None:
        """Create a new ``AirflowNetwork:MultiZone:SpecifiedFlowRate`` and add it to the document.

        This object is used to define specified flow through a linkage.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-airflow-network/#airflownetworkmultizonespecifiedflowrate
        """

class SizingZone:
    def __call__(
        self,
        /,
        *,
        zone_or_zonelist_name: str,
        zone_cooling_design_supply_air_humidity_ratio: float,
        zone_heating_design_supply_air_humidity_ratio: float,
        zone_cooling_design_supply_air_temperature_input_method: Literal[
            "", "SupplyAirTemperature", "TemperatureDifference"
        ]
        | None = "SupplyAirTemperature",
        zone_cooling_design_supply_air_temperature: float | None = ...,
        zone_cooling_design_supply_air_temperature_difference: float | None = ...,
        zone_heating_design_supply_air_temperature_input_method: Literal[
            "", "SupplyAirTemperature", "TemperatureDifference"
        ]
        | None = "SupplyAirTemperature",
        zone_heating_design_supply_air_temperature: float | None = ...,
        zone_heating_design_supply_air_temperature_difference: float | None = ...,
        design_specification_outdoor_air_object_name: str | None = ...,
        zone_heating_sizing_factor: float | None = ...,
        zone_cooling_sizing_factor: float | None = ...,
        cooling_design_air_flow_method: Literal["", "DesignDay", "DesignDayWithLimit", "Flow/Zone"]
        | None = "DesignDay",
        cooling_design_air_flow_rate: float | None = 0,
        cooling_minimum_air_flow_per_zone_floor_area: float | None = 0.000762,
        cooling_minimum_air_flow: float | None = 0,
        cooling_minimum_air_flow_fraction: float | None = 0.2,
        heating_design_air_flow_method: Literal["", "DesignDay", "DesignDayWithLimit", "Flow/Zone"]
        | None = "DesignDay",
        heating_design_air_flow_rate: float | None = 0,
        heating_maximum_air_flow_per_zone_floor_area: float | None = 0.002032,
        heating_maximum_air_flow: float | None = 0.1415762,
        heating_maximum_air_flow_fraction: float | None = 0.3,
        design_specification_zone_air_distribution_object_name: str | None = ...,
        account_for_dedicated_outdoor_air_system: Literal["", "No", "Yes"] | None = "No",
        dedicated_outdoor_air_system_control_strategy: Literal[
            "", "ColdSupplyAir", "NeutralDehumidifiedSupplyAir", "NeutralSupplyAir"
        ]
        | None = "NeutralSupplyAir",
        dedicated_outdoor_air_low_setpoint_temperature_for_design: float | Literal["", "Autosize"] | None = "Autosize",
        dedicated_outdoor_air_high_setpoint_temperature_for_design: float | Literal["", "Autosize"] | None = "Autosize",
        zone_load_sizing_method: Literal[
            "", "Latent Load", "Sensible And Latent Load", "Sensible Load", "Sensible Load Only No Latent Load"
        ]
        | None = "Sensible Load Only No Latent Load",
        zone_latent_cooling_design_supply_air_humidity_ratio_input_method: Literal[
            "", "HumidityRatioDifference", "SupplyAirHumidityRatio"
        ]
        | None = "HumidityRatioDifference",
        zone_dehumidification_design_supply_air_humidity_ratio: float | None = ...,
        zone_cooling_design_supply_air_humidity_ratio_difference: float | None = 0.005,
        zone_latent_heating_design_supply_air_humidity_ratio_input_method: Literal[
            "", "HumidityRatioDifference", "SupplyAirHumidityRatio"
        ]
        | None = "HumidityRatioDifference",
        zone_humidification_design_supply_air_humidity_ratio: float | None = ...,
        zone_humidification_design_supply_air_humidity_ratio_difference: float | None = 0.005,
        zone_humidistat_dehumidification_set_point_schedule_name: str | None = ...,
        zone_humidistat_humidification_set_point_schedule_name: str | None = ...,
        type_of_space_sum_to_use: Literal["", "Coincident", "NonCoincident"] | None = "Coincident",
        heating_coil_sizing_method: Literal[
            "", "CoolingCapacity", "GreaterOfHeatingOrCooling", "HeatingCapacity", "None"
        ]
        | None = "None",
        maximum_heating_capacity_to_cooling_load_sizing_ratio: float | None = 1,
    ) -> None:
        """Create a new ``Sizing:Zone`` and add it to the document.

        Specifies the data needed to perform a zone design air flow calculation. The calculation is done for every sizing period included in the input. The maximum cooling and heating load and cooling, heating, and ventilation air flows are then saved for system level and zone component design calculations.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-design-objects/#sizingzone
        """

class AnySizingPlant:
    def __call__(
        self,
        /,
        *,
        plant_or_condenser_loop_name: str,
        loop_type: Literal["Condenser", "Cooling", "Heating", "Steam"],
        design_loop_exit_temperature: float,
        loop_design_temperature_difference: float,
        sizing_option: Literal["", "Coincident", "NonCoincident"] | None = "NonCoincident",
        zone_timesteps_in_averaging_window: int | None = 1,
        coincident_sizing_factor_mode: Literal[
            "GlobalCoolingSizingFactor", "GlobalHeatingSizingFactor", "LoopComponentSizingFactor", "None"
        ]
        | None = ...,
    ) -> None:
        """Create a new ``Sizing:Plant`` and add it to the document.

        Specifies the input needed to autosize plant loop flow rates and equipment capacities. This information is initially used by components that use water for heating or cooling such as hot or chilled water coils to calculate their maximum water flow rates. These flow rates are then summed for use in calculating the Plant Loop flow rates.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-design-objects/#sizingplant
        """

class ZoneHVACOutdoorAirUnitEquipmentList:
    def __call__(
        self,
        name: str,
        /,
        *,
        component_1_object_type: Literal[
            "AirLoopHVAC:UnitarySystem",
            "Coil:Cooling:Water",
            "Coil:Cooling:Water:DetailedGeometry",
            "Coil:Heating:Electric",
            "Coil:Heating:Fuel",
            "Coil:Heating:Steam",
            "Coil:Heating:Water",
            "CoilSystem:Cooling:DX",
            "CoilSystem:Cooling:Water:HeatexchangerAssisted",
            "CoilSystem:Heating:DX",
            "Dehumidifier:Desiccant:NoFans",
            "HeatExchanger:AirToAir:FlatPlate",
            "HeatExchanger:AirToAir:SensibleAndLatent",
        ]
        | None = ...,
        component_1_name: str | None = ...,
        component_2_object_type: Literal[
            "AirLoopHVAC:UnitarySystem",
            "Coil:Cooling:Water",
            "Coil:Cooling:Water:DetailedGeometry",
            "Coil:Heating:Electric",
            "Coil:Heating:Fuel",
            "Coil:Heating:Steam",
            "Coil:Heating:Water",
            "CoilSystem:Cooling:DX",
            "CoilSystem:Cooling:Water:HeatexchangerAssisted",
            "CoilSystem:Heating:DX",
            "Dehumidifier:Desiccant:NoFans",
            "HeatExchanger:AirToAir:FlatPlate",
            "HeatExchanger:AirToAir:SensibleAndLatent",
        ]
        | None = ...,
        component_2_name: str | None = ...,
        component_3_object_type: Literal[
            "AirLoopHVAC:UnitarySystem",
            "Coil:Cooling:Water",
            "Coil:Cooling:Water:DetailedGeometry",
            "Coil:Heating:Electric",
            "Coil:Heating:Fuel",
            "Coil:Heating:Steam",
            "Coil:Heating:Water",
            "CoilSystem:Cooling:DX",
            "CoilSystem:Cooling:Water:HeatexchangerAssisted",
            "CoilSystem:Heating:DX",
            "Dehumidifier:Desiccant:NoFans",
            "HeatExchanger:AirToAir:FlatPlate",
            "HeatExchanger:AirToAir:SensibleAndLatent",
        ]
        | None = ...,
        component_3_name: str | None = ...,
        component_4_object_type: Literal[
            "AirLoopHVAC:UnitarySystem",
            "Coil:Cooling:Water",
            "Coil:Cooling:Water:DetailedGeometry",
            "Coil:Heating:Electric",
            "Coil:Heating:Fuel",
            "Coil:Heating:Steam",
            "Coil:Heating:Water",
            "CoilSystem:Cooling:DX",
            "CoilSystem:Cooling:Water:HeatexchangerAssisted",
            "CoilSystem:Heating:DX",
            "Dehumidifier:Desiccant:NoFans",
            "HeatExchanger:AirToAir:FlatPlate",
            "HeatExchanger:AirToAir:SensibleAndLatent",
        ]
        | None = ...,
        component_4_name: str | None = ...,
        component_5_object_type: Literal[
            "AirLoopHVAC:UnitarySystem",
            "Coil:Cooling:Water",
            "Coil:Cooling:Water:DetailedGeometry",
            "Coil:Heating:Electric",
            "Coil:Heating:Fuel",
            "Coil:Heating:Steam",
            "Coil:Heating:Water",
            "CoilSystem:Cooling:DX",
            "CoilSystem:Cooling:Water:HeatexchangerAssisted",
            "CoilSystem:Heating:DX",
            "Dehumidifier:Desiccant:NoFans",
            "HeatExchanger:AirToAir:FlatPlate",
            "HeatExchanger:AirToAir:SensibleAndLatent",
        ]
        | None = ...,
        component_5_name: str | None = ...,
        component_6_object_type: Literal[
            "AirLoopHVAC:UnitarySystem",
            "Coil:Cooling:Water",
            "Coil:Cooling:Water:DetailedGeometry",
            "Coil:Heating:Electric",
            "Coil:Heating:Fuel",
            "Coil:Heating:Steam",
            "Coil:Heating:Water",
            "CoilSystem:Cooling:DX",
            "CoilSystem:Cooling:Water:HeatexchangerAssisted",
            "CoilSystem:Heating:DX",
            "Dehumidifier:Desiccant:NoFans",
            "HeatExchanger:AirToAir:FlatPlate",
            "HeatExchanger:AirToAir:SensibleAndLatent",
        ]
        | None = ...,
        component_6_name: str | None = ...,
        component_7_object_type: Literal[
            "AirLoopHVAC:UnitarySystem",
            "Coil:Cooling:Water",
            "Coil:Cooling:Water:DetailedGeometry",
            "Coil:Heating:Electric",
            "Coil:Heating:Fuel",
            "Coil:Heating:Steam",
            "Coil:Heating:Water",
            "CoilSystem:Cooling:DX",
            "CoilSystem:Cooling:Water:HeatexchangerAssisted",
            "CoilSystem:Heating:DX",
            "Dehumidifier:Desiccant:NoFans",
            "HeatExchanger:AirToAir:FlatPlate",
            "HeatExchanger:AirToAir:SensibleAndLatent",
        ]
        | None = ...,
        component_7_name: str | None = ...,
        component_8_object_type: Literal[
            "AirLoopHVAC:UnitarySystem",
            "Coil:Cooling:Water",
            "Coil:Cooling:Water:DetailedGeometry",
            "Coil:Heating:Electric",
            "Coil:Heating:Fuel",
            "Coil:Heating:Steam",
            "Coil:Heating:Water",
            "CoilSystem:Cooling:DX",
            "CoilSystem:Cooling:Water:HeatexchangerAssisted",
            "CoilSystem:Heating:DX",
            "Dehumidifier:Desiccant:NoFans",
            "HeatExchanger:AirToAir:FlatPlate",
            "HeatExchanger:AirToAir:SensibleAndLatent",
        ]
        | None = ...,
        component_8_name: str | None = ...,
    ) -> None:
        """Create a new ``ZoneHVAC:OutdoorAirUnit:EquipmentList`` and add it to the document.

        Equipment list for components in a ZoneHVAC:OutdoorAirUnit. Components are simulated sequentially in the order given in the equipment list.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-zone-forced-air-units/#zonehvacoutdoorairunitequipmentlist
        """

class ZoneHVACBaseboardConvectiveElectric:
    def __call__(
        self,
        name: str,
        /,
        *,
        availability_schedule_name: str | None = ...,
        heating_design_capacity_method: Literal[
            "", "CapacityPerFloorArea", "FractionOfAutosizedHeatingCapacity", "HeatingDesignCapacity"
        ]
        | None = "HeatingDesignCapacity",
        heating_design_capacity: float | Literal["", "Autosize"] | None = "Autosize",
        heating_design_capacity_per_floor_area: float | None = ...,
        fraction_of_autosized_heating_design_capacity: float | None = 1,
        efficiency: float | None = 1,
    ) -> None:
        """Create a new ``ZoneHVAC:Baseboard:Convective:Electric`` and add it to the document.

        Electric baseboard heater, convection-only. Natural convection electric heating unit.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-radiative-convective-units/#zonehvacbaseboardconvectiveelectric
        """

class AnyCoilCoolingDXCurveFitSpeed:
    def __call__(
        self,
        name: str,
        /,
        *,
        gross_total_cooling_capacity_fraction: float,
        evaporator_air_flow_rate_fraction: float,
        condenser_air_flow_rate_fraction: float | None = ...,
        gross_sensible_heat_ratio: float | Literal["", "Autosize"] | None = "Autosize",
        gross_cooling_cop: float | None = 3,
        active_fraction_of_coil_face_area: float | None = 1,
        evaporative_condenser_pump_power_fraction: float | None = 1,
        evaporative_condenser_effectiveness: float | None = 0.9,
        total_cooling_capacity_modifier_function_of_temperature_curve_name: str | None = ...,
        total_cooling_capacity_modifier_function_of_air_flow_fraction_curve_name: str | None = ...,
        energy_input_ratio_modifier_function_of_temperature_curve_name: str | None = ...,
        energy_input_ratio_modifier_function_of_air_flow_fraction_curve_name: str | None = ...,
        part_load_fraction_correlation_curve_name: str | None = ...,
        rated_waste_heat_fraction_of_power_input: float | None = 0.2,
        waste_heat_modifier_function_of_temperature_curve_name: str | None = ...,
        sensible_heat_ratio_modifier_function_of_temperature_curve_name: str | None = ...,
        sensible_heat_ratio_modifier_function_of_flow_fraction_curve_name: str | None = ...,
    ) -> None:
        """Create a new ``Coil:Cooling:DX:CurveFit:Speed`` and add it to the document.

        DX cooling coil performance for a single speed within a single operating mode.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-coil-cooling-dx/#coilcoolingdxcurvefitspeed
        """

class CoilCoolingDXCurveFitSpeed:
    def __call__(
        self,
        name: str,
        /,
        *,
        gross_total_cooling_capacity_fraction: float,
        evaporator_air_flow_rate_fraction: float,
        condenser_air_flow_rate_fraction: float | None = ...,
        gross_sensible_heat_ratio: float | Literal["", "Autosize"] | None = "Autosize",
        gross_cooling_cop: float | None = 3,
        active_fraction_of_coil_face_area: float | None = 1,
        evaporative_condenser_pump_power_fraction: float | None = 1,
        evaporative_condenser_effectiveness: float | None = 0.9,
        total_cooling_capacity_modifier_function_of_temperature_curve_name: str | None = ...,
        total_cooling_capacity_modifier_function_of_air_flow_fraction_curve_name: str | None = ...,
        energy_input_ratio_modifier_function_of_temperature_curve_name: str | None = ...,
        energy_input_ratio_modifier_function_of_air_flow_fraction_curve_name: str | None = ...,
        part_load_fraction_correlation_curve_name: str | None = ...,
        rated_waste_heat_fraction_of_power_input: float | None = 0.2,
        waste_heat_modifier_function_of_temperature_curve_name: str | None = ...,
        sensible_heat_ratio_modifier_function_of_temperature_curve_name: str | None = ...,
        sensible_heat_ratio_modifier_function_of_flow_fraction_curve_name: str | None = ...,
    ) -> None:
        """Create a new ``Coil:Cooling:DX:CurveFit:Speed`` and add it to the document.

        DX cooling coil performance for a single speed within a single operating mode.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-coil-cooling-dx/#coilcoolingdxcurvefitspeed
        """

class CoilPerformanceDXCooling:
    def __call__(
        self,
        name: str,
        /,
        *,
        gross_rated_total_cooling_capacity: float | Literal["Autosize"],
        gross_rated_sensible_heat_ratio: float | Literal["Autosize"],
        rated_air_flow_rate: float | Literal["Autosize"],
        total_cooling_capacity_function_of_temperature_curve_name: str,
        total_cooling_capacity_function_of_flow_fraction_curve_name: str,
        energy_input_ratio_function_of_temperature_curve_name: str,
        energy_input_ratio_function_of_flow_fraction_curve_name: str,
        part_load_fraction_correlation_curve_name: str,
        gross_rated_cooling_cop: float | None = 3,
        fraction_of_air_flow_bypassed_around_coil: float | None = 0,
        nominal_time_for_condensate_removal_to_begin: float | None = 0,
        ratio_of_initial_moisture_evaporation_rate_and_steady_state_latent_capacity: float | None = 0,
        maximum_cycling_rate: float | None = 0,
        latent_capacity_time_constant: float | None = 0,
        condenser_air_inlet_node_name: str | None = ...,
        condenser_type: Literal["", "AirCooled", "EvaporativelyCooled"] | None = "AirCooled",
        evaporative_condenser_effectiveness: float | None = 0.9,
        evaporative_condenser_air_flow_rate: float | Literal["Autosize"] | None = ...,
        evaporative_condenser_pump_rated_power_consumption: float | Literal["", "Autosize"] | None = 0,
        sensible_heat_ratio_function_of_temperature_curve_name: str | None = ...,
        sensible_heat_ratio_function_of_flow_fraction_curve_name: str | None = ...,
    ) -> None:
        """Create a new ``CoilPerformance:DX:Cooling`` and add it to the document.

        Used to specify DX cooling coil performance for one mode of operation for a Coil:Cooling:DX:TwoStageWithHumidityControlMode object which may reference one to four CoilPerformance:DX:Cooling objects depending on the specified number of stages and dehumidification modes. In nearly all cases, the Rated Air Flow Rate will be the same for all performance objects associated with a given coil. If bypass is specified, the Rated Air Flow Rate includes both the bypassed flow and the flow through the active part of the coil.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-heating-and-cooling-coils/#coilperformancedxcooling
        """

class CoilHeatingSteam:
    def __call__(
        self,
        name: str,
        /,
        *,
        water_inlet_node_name: str,
        water_outlet_node_name: str,
        air_inlet_node_name: str,
        air_outlet_node_name: str,
        availability_schedule_name: str | None = ...,
        maximum_steam_flow_rate: float | Literal["Autosize"] | None = ...,
        degree_of_subcooling: float | None = ...,
        degree_of_loop_subcooling: float | None = 20,
        coil_control_type: Literal["TemperatureSetpointControl", "ZoneLoadControl"] | None = ...,
        temperature_setpoint_node_name: str | None = ...,
    ) -> None:
        """Create a new ``Coil:Heating:Steam`` and add it to the document.

        Steam heating coil. Condenses and sub-cools steam at loop pressure and discharges condensate through steam traps to low pressure condensate line.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-heating-and-cooling-coils/#coilheatingsteam
        """

class HumidifierSteamElectric:
    def __call__(
        self,
        name: str,
        /,
        *,
        availability_schedule_name: str | None = ...,
        rated_capacity: float | Literal["Autosize"] | None = ...,
        rated_power: float | Literal["Autosize"] | None = ...,
        rated_fan_power: float | None = ...,
        standby_power: float | None = ...,
        air_inlet_node_name: str | None = ...,
        air_outlet_node_name: str | None = ...,
        water_storage_tank_name: str | None = ...,
    ) -> None:
        """Create a new ``Humidifier:Steam:Electric`` and add it to the document.

        Electrically heated steam humidifier with fan.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-humidifiers-and-dehumidifiers/#humidifiersteamelectric
        """

class HeatExchangerDesiccantBalancedFlowPerformanceDataType1:
    def __call__(
        self,
        name: str,
        /,
        *,
        nominal_air_face_velocity: float | Literal["Autosize"],
        temperature_equation_coefficient_1: float,
        temperature_equation_coefficient_2: float,
        temperature_equation_coefficient_3: float,
        temperature_equation_coefficient_4: float,
        temperature_equation_coefficient_5: float,
        temperature_equation_coefficient_6: float,
        temperature_equation_coefficient_7: float,
        temperature_equation_coefficient_8: float,
        minimum_regeneration_inlet_air_humidity_ratio_for_temperature_equation: float,
        maximum_regeneration_inlet_air_humidity_ratio_for_temperature_equation: float,
        minimum_regeneration_inlet_air_temperature_for_temperature_equation: float,
        maximum_regeneration_inlet_air_temperature_for_temperature_equation: float,
        minimum_process_inlet_air_humidity_ratio_for_temperature_equation: float,
        maximum_process_inlet_air_humidity_ratio_for_temperature_equation: float,
        minimum_process_inlet_air_temperature_for_temperature_equation: float,
        maximum_process_inlet_air_temperature_for_temperature_equation: float,
        minimum_regeneration_air_velocity_for_temperature_equation: float,
        maximum_regeneration_air_velocity_for_temperature_equation: float,
        minimum_regeneration_outlet_air_temperature_for_temperature_equation: float,
        maximum_regeneration_outlet_air_temperature_for_temperature_equation: float,
        minimum_regeneration_inlet_air_relative_humidity_for_temperature_equation: float,
        maximum_regeneration_inlet_air_relative_humidity_for_temperature_equation: float,
        minimum_process_inlet_air_relative_humidity_for_temperature_equation: float,
        maximum_process_inlet_air_relative_humidity_for_temperature_equation: float,
        humidity_ratio_equation_coefficient_1: float,
        humidity_ratio_equation_coefficient_2: float,
        humidity_ratio_equation_coefficient_3: float,
        humidity_ratio_equation_coefficient_4: float,
        humidity_ratio_equation_coefficient_5: float,
        humidity_ratio_equation_coefficient_6: float,
        humidity_ratio_equation_coefficient_7: float,
        humidity_ratio_equation_coefficient_8: float,
        minimum_regeneration_inlet_air_humidity_ratio_for_humidity_ratio_equation: float,
        maximum_regeneration_inlet_air_humidity_ratio_for_humidity_ratio_equation: float,
        minimum_regeneration_inlet_air_temperature_for_humidity_ratio_equation: float,
        maximum_regeneration_inlet_air_temperature_for_humidity_ratio_equation: float,
        minimum_process_inlet_air_humidity_ratio_for_humidity_ratio_equation: float,
        maximum_process_inlet_air_humidity_ratio_for_humidity_ratio_equation: float,
        minimum_process_inlet_air_temperature_for_humidity_ratio_equation: float,
        maximum_process_inlet_air_temperature_for_humidity_ratio_equation: float,
        minimum_regeneration_air_velocity_for_humidity_ratio_equation: float,
        maximum_regeneration_air_velocity_for_humidity_ratio_equation: float,
        minimum_regeneration_outlet_air_humidity_ratio_for_humidity_ratio_equation: float,
        maximum_regeneration_outlet_air_humidity_ratio_for_humidity_ratio_equation: float,
        minimum_regeneration_inlet_air_relative_humidity_for_humidity_ratio_equation: float,
        maximum_regeneration_inlet_air_relative_humidity_for_humidity_ratio_equation: float,
        minimum_process_inlet_air_relative_humidity_for_humidity_ratio_equation: float,
        maximum_process_inlet_air_relative_humidity_for_humidity_ratio_equation: float,
        nominal_air_flow_rate: float | Literal["Autosize"] | None = ...,
        nominal_electric_power: float | None = 0,
    ) -> None:
        """Create a new ``HeatExchanger:Desiccant:BalancedFlow:PerformanceDataType1`` and add it to the document.

        RTO = B1 + B2*RWI + B3*RTI + B4*(RWI/RTI) + B5*PWI + B6*PTI + B7*(PWI/PTI) + B8*RFV RWO = C1 + C2*RWI + C3*RTI + C4*(RWI/RTI) + C5*PWI + C6*PTI + C7*(PWI/PTI) + C8*RFV where, RTO = Dry-bulb temperature of the regeneration outlet air (C) RWO = Humidity ratio of the regeneration outlet air (kgWater/kgDryAir) RWI = Humidity ratio of the regeneration inlet air (kgWater/kgDryAir) RTI = Dry-bulb temperature of the regeneration inlet air (C) PWI = Humidity ratio of the process inlet air (kgWater/kgDryAir) PTI = Dry-bulb temperature of the process inlet air (C) RFV = Regeneration Face Velocity (m/s)

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-heat-recovery/#heatexchangerdesiccantbalancedflowperformancedatatype1
        """

class OutdoorAirMixer:
    def __call__(
        self,
        name: str,
        /,
        *,
        mixed_air_node_name: str,
        outdoor_air_stream_node_name: str,
        relief_air_stream_node_name: str,
        return_air_stream_node_name: str,
    ) -> None:
        """Create a new ``OutdoorAir:Mixer`` and add it to the document.

        Outdoor air mixer. Node names cannot be duplicated within a single OutdoorAir:Mixer object or across all outdoor air mixers.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-air-distribution/#outdoorairmixer
        """

class SolarCollectorPerformanceFlatPlate:
    def __call__(
        self,
        name: str,
        /,
        *,
        gross_area: float,
        test_flow_rate: float,
        test_correlation_type: Literal["Average", "Inlet", "Outlet"],
        coefficient_1_of_efficiency_equation: float,
        coefficient_2_of_efficiency_equation: float,
        test_fluid: Literal["", "Water"] | None = "Water",
        coefficient_3_of_efficiency_equation: float | None = ...,
        coefficient_2_of_incident_angle_modifier: float | None = ...,
        coefficient_3_of_incident_angle_modifier: float | None = ...,
    ) -> None:
        """Create a new ``SolarCollectorPerformance:FlatPlate`` and add it to the document.

        Thermal and optical performance parameters for a single flat plate solar collector module. These parameters are based on the testing methodologies described in ASHRAE Standards 93 and 96 which are used Solar Rating and Certification Corporation (SRCC) Directory of SRCC Certified Solar Collector Ratings. See EnergyPlus DataSets file SolarCollectors.idf.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-solar-collectors/#solarcollectorperformanceflatplate
        """

class HeatPumpPlantLoopEIRHeating:
    def __call__(
        self,
        name: str,
        /,
        *,
        load_side_inlet_node_name: str,
        load_side_outlet_node_name: str,
        source_side_inlet_node_name: str,
        source_side_outlet_node_name: str,
        capacity_modifier_function_of_temperature_curve_name: str,
        electric_input_to_output_ratio_modifier_function_of_temperature_curve_name: str,
        electric_input_to_output_ratio_modifier_function_of_part_load_ratio_curve_name: str,
        condenser_type: Literal["", "AirSource", "WaterSource"] | None = "WaterSource",
        heat_recovery_inlet_node_name: str | None = ...,
        heat_recovery_outlet_node_name: str | None = ...,
        companion_heat_pump_name: str | None = ...,
        load_side_reference_flow_rate: float | Literal["", "Autosize"] | None = "Autosize",
        source_side_reference_flow_rate: float | Literal["", "Autosize"] | None = "Autosize",
        heat_recovery_reference_flow_rate: float | Literal["", "Autosize"] | None = "Autosize",
        reference_capacity: float | Literal["", "Autosize"] | None = "Autosize",
        reference_coefficient_of_performance: float | None = 3,
        sizing_factor: float | None = 1,
        heating_to_cooling_capacity_sizing_ratio: float | None = 1,
        heat_pump_sizing_method: Literal["", "CoolingCapacity", "GreaterOfHeatingOrCooling", "HeatingCapacity"]
        | None = "CoolingCapacity",
        control_type: Literal["", "Load", "Setpoint"] | None = "Load",
        flow_mode: Literal["", "ConstantFlow", "VariableSpeedPumping"] | None = "ConstantFlow",
        minimum_part_load_ratio: float | None = 0,
        minimum_source_inlet_temperature: float | None = -100,
        maximum_source_inlet_temperature: float | None = 100,
        minimum_supply_water_temperature_curve_name: str | None = ...,
        maximum_supply_water_temperature_curve_name: str | None = ...,
        dry_outdoor_correction_factor_curve_name: str | None = ...,
        maximum_outdoor_dry_bulb_temperature_for_defrost_operation: float | None = 10,
        heat_pump_defrost_control: Literal["None", "OnDemand", "Timed", "TimedEmpirical"] | None = ...,
        heat_pump_defrost_time_period_fraction: float | None = 0.058333,
        defrost_energy_input_ratio_function_of_temperature_curve_name: str | None = ...,
        timed_empirical_defrost_frequency_curve_name: str | None = ...,
        timed_empirical_defrost_heat_load_penalty_curve_name: str | None = ...,
        timed_empirical_defrost_heat_input_energy_fraction_curve_name: str | None = ...,
        minimum_heat_recovery_outlet_temperature: float | None = 4.5,
        heat_recovery_capacity_modifier_function_of_temperature_curve_name: str | None = ...,
        heat_recovery_electric_input_to_output_ratio_modifier_function_of_temperature_curve_name: str | None = ...,
    ) -> None:
        """Create a new ``HeatPump:PlantLoop:EIR:Heating`` and add it to the document.

        An EIR formulated water to water heat pump model, heating operation

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-plant-equipment/#heatpumpplantloopeirheating
        """

class AnyCoolingTowerSingleSpeed:
    def __call__(
        self,
        name: str,
        /,
        *,
        water_inlet_node_name: str,
        water_outlet_node_name: str,
        design_air_flow_rate: float | Literal["Autosize"],
        design_fan_power: float | Literal["Autosize"],
        design_water_flow_rate: float | Literal["Autosize"] | None = ...,
        design_u_factor_times_area_value: float | Literal["Autosize"] | None = ...,
        free_convection_u_factor_times_area_value_sizing_factor: float | None = 0.1,
        performance_input_method: Literal["", "NominalCapacity", "UFactorTimesAreaAndDesignWaterFlowRate"]
        | None = "UFactorTimesAreaAndDesignWaterFlowRate",
        heat_rejection_capacity_and_nominal_capacity_sizing_ratio: float | None = 1.25,
        nominal_capacity: float | None = ...,
        free_convection_capacity: float | Literal["Autocalculate"] | None = ...,
        free_convection_nominal_capacity_sizing_factor: float | None = 0.1,
        design_inlet_air_dry_bulb_temperature: float | None = 35,
        design_inlet_air_wet_bulb_temperature: float | None = 25.6,
        design_approach_temperature: float | Literal["", "Autosize"] | None = "Autosize",
        design_range_temperature: float | Literal["", "Autosize"] | None = "Autosize",
        basin_heater_capacity: float | None = 0,
        basin_heater_setpoint_temperature: float | None = 2,
        basin_heater_operating_schedule_name: str | None = ...,
        evaporation_loss_mode: Literal["LossFactor", "SaturatedExit"] | None = ...,
        evaporation_loss_factor: float | None = 0.2,
        drift_loss_percent: float | None = 0.008,
        blowdown_calculation_mode: Literal["ConcentrationRatio", "ScheduledRate"] | None = ...,
        blowdown_concentration_ratio: float | None = 3,
        blowdown_makeup_water_usage_schedule_name: str | None = ...,
        supply_water_storage_tank_name: str | None = ...,
        outdoor_air_inlet_node_name: str | None = ...,
        capacity_control: Literal["", "FanCycling", "FluidBypass"] | None = "FanCycling",
        number_of_cells: int | None = 1,
        cell_control: Literal["", "MaximalCell", "MinimalCell"] | None = ...,
        cell_minimum_water_flow_rate_fraction: float | None = 0.33,
        cell_maximum_water_flow_rate_fraction: float | None = 2.5,
        sizing_factor: float | None = 1,
        end_use_subcategory: str | None = "General",
    ) -> None:
        """Create a new ``CoolingTower:SingleSpeed`` and add it to the document.

        This tower model is based on Merkel's theory, which is also the basis for the tower model in ASHRAE's HVAC1 Toolkit. The open wet cooling tower is modeled as a counter flow heat exchanger with a single-speed fan drawing air through the tower (induced-draft configuration). Added fluid bypass as an additional capacity control. 8/2008. For a multi-cell tower, the capacity and air/water flow rate inputs are for the entire tower.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-condenser-equipment/#coolingtowersinglespeed
        """

class FluidCoolerSingleSpeed:
    def __call__(
        self,
        name: str,
        /,
        *,
        water_inlet_node_name: str,
        water_outlet_node_name: str,
        design_entering_water_temperature: float,
        design_entering_air_temperature: float,
        design_entering_air_wetbulb_temperature: float,
        design_water_flow_rate: float | Literal["Autosize"],
        design_air_flow_rate: float | Literal["Autosize"],
        design_air_flow_rate_fan_power: float | Literal["Autosize"],
        performance_input_method: Literal["", "NominalCapacity", "UFactorTimesAreaAndDesignWaterFlowRate"]
        | None = "NominalCapacity",
        design_air_flow_rate_u_factor_times_area_value: float | Literal["Autosize"] | None = ...,
        nominal_capacity: float | None = ...,
        outdoor_air_inlet_node_name: str | None = ...,
    ) -> None:
        """Create a new ``FluidCooler:SingleSpeed`` and add it to the document.

        The fluid cooler is modeled as a cross flow heat exchanger (both streams unmixed) with single-speed fans (induced draft configuration).

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-condenser-equipment/#fluidcoolersinglespeed
        """

class AnyGroundHeatExchangerResponseFactors:
    def __call__(
        self,
        name: str,
        /,
        *,
        ghe_vertical_properties_object_name: str,
        number_of_boreholes: int,
        g_function_reference_ratio: float | None = 0.0005,
        g_functions: list[_g.GroundHeatExchangerResponseFactorsGFunctionsItem] = ...,
    ) -> None:
        """Create a new ``GroundHeatExchanger:ResponseFactors`` and add it to the document.

        Response factor definitions from third-party tool, commonly referred to a 'g-functions'

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-condenser-equipment/#groundheatexchangerresponsefactors
        """

class GroundHeatExchangerResponseFactors:
    def __call__(
        self,
        name: str,
        /,
        *,
        ghe_vertical_properties_object_name: str,
        number_of_boreholes: int,
        g_function_reference_ratio: float | None = 0.0005,
        g_functions: list[_g.GroundHeatExchangerResponseFactorsGFunctionsItem] = ...,
    ) -> None:
        """Create a new ``GroundHeatExchanger:ResponseFactors`` and add it to the document.

        Response factor definitions from third-party tool, commonly referred to a 'g-functions'

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-condenser-equipment/#groundheatexchangerresponsefactors
        """

class PlantEquipmentList:
    def __call__(self, name: str, /, *, equipment: list[_g.PlantEquipmentListEquipmentItem] = ...) -> None:
        """Create a new ``PlantEquipmentList`` and add it to the document.

        List plant equipment in order of operating priority, 1st in list will be used 1st, etc Use only plant equipment in this list. If no equipment object types and equipment names are specified, then the corresponding PlantEquipmentOperation:* object will assume all available plant equipment for the loop should be OFF (not operate) within the specified lower/upper limit.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-plant-condenser-control/#plantequipmentlist
        """

class ExternalInterfaceFunctionalMockupUnitExportToActuator:
    def __call__(
        self,
        name: str,
        /,
        *,
        actuated_component_unique_name: str,
        actuated_component_type: str,
        actuated_component_control_type: str,
        fmu_variable_name: str,
        initial_value: float | None = ...,
    ) -> None:
        """Create a new ``ExternalInterface:FunctionalMockupUnitExport:To:Actuator`` and add it to the document.

        Hardware portion of EMS used to set up actuators in the model that are dynamically updated from the FMU.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-externalinterface/#externalinterfacefunctionalmockupunitexporttoactuator
        """

class AnyAirTerminalSingleDuctUserDefined:
    def __call__(
        self,
        name: str,
        /,
        *,
        primary_air_inlet_node_name: str,
        primary_air_outlet_node_name: str,
        number_of_plant_loop_connections: int,
        plant_connection_1_inlet_node_name: str,
        plant_connection_1_outlet_node_name: str,
        overall_model_simulation_program_calling_manager_name: str | None = ...,
        model_setup_and_sizing_program_calling_manager_name: str | None = ...,
        secondary_air_inlet_node_name: str | None = ...,
        secondary_air_outlet_node_name: str | None = ...,
        plant_connection_2_inlet_node_name: str | None = ...,
        plant_connection_2_outlet_node_name: str | None = ...,
        supply_inlet_water_storage_tank_name: str | None = ...,
        collection_outlet_water_storage_tank_name: str | None = ...,
        ambient_zone_name: str | None = ...,
    ) -> None:
        """Create a new ``AirTerminal:SingleDuct:UserDefined`` and add it to the document.

        Defines a generic single duct air terminal unit for custom modeling using Energy Management System or External Interface

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-user-defined-hvac-and-plant-component/#airterminalsingleductuserdefined
        """

class SetpointManagerSingleZoneHeating:
    def __call__(
        self,
        name: str,
        /,
        *,
        control_zone_name: str,
        zone_node_name: str,
        zone_inlet_node_name: str,
        setpoint_node_or_nodelist_name: str,
        control_variable: Literal["", "Temperature"] | None = "Temperature",
        minimum_supply_air_temperature: float | None = -99,
        maximum_supply_air_temperature: float | None = 99,
    ) -> None:
        """Create a new ``SetpointManager:SingleZone:Heating`` and add it to the document.

        This setpoint manager detects the control zone load to meet the current heating setpoint, zone inlet node flow rate, and zone node temperature, and calculates a setpoint temperature for the supply air that will satisfy the zone heating load for the control zone.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-setpoint-managers/#setpointmanagersinglezoneheating
        """

class SetpointManagerFollowSystemNodeTemperature:
    def __call__(
        self,
        name: str,
        /,
        *,
        setpoint_node_or_nodelist_name: str,
        control_variable: Literal["", "MaximumTemperature", "MinimumTemperature", "Temperature"] | None = "Temperature",
        reference_node_name: str | None = ...,
        reference_temperature_type: Literal["", "NodeDryBulb", "NodeWetBulb"] | None = "NodeDryBulb",
        offset_temperature_difference: float | None = ...,
        maximum_limit_setpoint_temperature: float | None = ...,
        minimum_limit_setpoint_temperature: float | None = ...,
    ) -> None:
        """Create a new ``SetpointManager:FollowSystemNodeTemperature`` and add it to the document.

        This setpoint manager is used to place a temperature setpoint on a system node that is derived from the current temperatures at a separate system node. The current value of the temperature at a reference node is obtained and used to generate setpoint on a second system node. If the reference node is also designated to be an outdoor air (intake) node, then this setpoint manager can be used to follow outdoor air conditions that are adjusted for altitude.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-setpoint-managers/#setpointmanagerfollowsystemnodetemperature
        """

class PhotovoltaicPerformanceSandia:
    def __call__(
        self,
        name: str,
        /,
        *,
        active_area: float | None = 1,
        number_of_cells_in_series: int | None = 1,
        number_of_cells_in_parallel: int | None = 1,
        short_circuit_current: float | None = ...,
        open_circuit_voltage: float | None = ...,
        current_at_maximum_power_point: float | None = ...,
        voltage_at_maximum_power_point: float | None = ...,
        sandia_database_parameter_aisc: float | None = ...,
        sandia_database_parameter_aimp: float | None = ...,
        sandia_database_parameter_c0: float | None = ...,
        sandia_database_parameter_c1: float | None = ...,
        sandia_database_parameter_bvoc0: float | None = ...,
        sandia_database_parameter_mbvoc: float | None = ...,
        sandia_database_parameter_bvmp0: float | None = ...,
        sandia_database_parameter_mbvmp: float | None = ...,
        diode_factor: float | None = ...,
        sandia_database_parameter_c2: float | None = ...,
        sandia_database_parameter_c3: float | None = ...,
        sandia_database_parameter_a0: float | None = ...,
        sandia_database_parameter_a1: float | None = ...,
        sandia_database_parameter_a2: float | None = ...,
        sandia_database_parameter_a3: float | None = ...,
        sandia_database_parameter_a4: float | None = ...,
        sandia_database_parameter_b0: float | None = ...,
        sandia_database_parameter_b1: float | None = ...,
        sandia_database_parameter_b2: float | None = ...,
        sandia_database_parameter_b3: float | None = ...,
        sandia_database_parameter_b4: float | None = ...,
        sandia_database_parameter_b5: float | None = ...,
        sandia_database_parameter_delta_tc_: float | None = ...,
        sandia_database_parameter_fd: float | None = ...,
        sandia_database_parameter_a: float | None = ...,
        sandia_database_parameter_b: float | None = ...,
        sandia_database_parameter_c4: float | None = ...,
        sandia_database_parameter_c5: float | None = ...,
        sandia_database_parameter_ix0: float | None = ...,
        sandia_database_parameter_ixx0: float | None = ...,
        sandia_database_parameter_c6: float | None = ...,
        sandia_database_parameter_c7: float | None = ...,
        sandia_database_parameter_delta_tc: float | None = ...,
    ) -> None:
        """Create a new ``PhotovoltaicPerformance:Sandia`` and add it to the document.

        Describes performance input data needed for specific makes and models of production PV panels using the empirical coefficients assembled by Sandia National Laboratory.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-electric-load-center-generator/#photovoltaicperformancesandia
        """

class CurveLinear:
    def __call__(
        self,
        name: str,
        /,
        *,
        coefficient1_constant: float,
        coefficient2_x: float,
        minimum_value_of_x: float,
        maximum_value_of_x: float,
        minimum_curve_output: float | None = ...,
        maximum_curve_output: float | None = ...,
        input_unit_type_for_x: Literal[
            "", "Dimensionless", "Distance", "MassFlow", "Power", "Pressure", "Temperature", "VolumetricFlow"
        ]
        | None = "Dimensionless",
        output_unit_type: Literal["", "Capacity", "Dimensionless", "Power", "Pressure", "Temperature"]
        | None = "Dimensionless",
    ) -> None:
        """Create a new ``Curve:Linear`` and add it to the document.

        Linear curve with one independent variable. Input for the linear curve consists of a curve name, the two coefficients, and the maximum and minimum valid independent variable values. Optional inputs for curve minimum and maximum may be used to limit the output of the performance curve. curve = C1 + C2*x

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-performance-curves/#curvelinear
        """
