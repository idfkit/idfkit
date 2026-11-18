"""Creation signatures of generated classes (stub only).

DO NOT EDIT — regenerate with:
    python -m idfkit.codegen.generate_stubs
"""

from __future__ import annotations

from collections.abc import Sequence
from typing import Literal

from .. import _generated_types as _g

class HotWaterEquipment:
    def __call__(
        self,
        name: str,
        /,
        *,
        zone_or_zonelist_or_space_or_spacelist_name: str,
        schedule_name: str,
        design_level_calculation_method: Literal[
            "", "EquipmentLevel", "Power/Area", "Power/Person", "Watts/Area", "Watts/Person"
        ]
        | None = "EquipmentLevel",
        design_level: float | None = ...,
        power_per_floor_area: float | None = ...,
        power_per_person: float | None = ...,
        fraction_latent: float | None = 0,
        fraction_radiant: float | None = 0,
        fraction_lost: float | None = 0,
        end_use_subcategory: str | None = "General",
    ) -> None:
        """Create a new ``HotWaterEquipment`` and add it to the document.

        Sets internal gains for hot water equipment in the zone. If a ZoneList, SpaceList, or a Zone comprised of more than one Space is specified then this definition applies to all applicable spaces, and each instance will be named with the Space Name plus this Object Name.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-internal-gains-people-lights-other/#hotwaterequipment
        """

class DaylightingDeviceTubular:
    def __call__(
        self,
        name: str,
        /,
        *,
        dome_name: str,
        diffuser_name: str,
        construction_name: str,
        diameter: float,
        total_length: float,
        effective_thermal_resistance: float | None = 0.28,
        transition_lengths: Sequence[
            _g.DaylightingDeviceTubularTransitionLengthsItem | _g.DaylightingDeviceTubularTransitionLengthsGroup
        ] = ...,
    ) -> None:
        """Create a new ``DaylightingDevice:Tubular`` and add it to the document.

        Defines a tubular daylighting device (TDD) consisting of three components: a dome, a pipe, and a diffuser. The dome and diffuser are defined separately using the FenestrationSurface:Detailed object.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-daylighting/#daylightingdevicetubular
        """

class HVACTemplateZoneIdealLoadsAirSystem:
    def __call__(
        self,
        this_type_has_no_name_field: _g._PassFieldsAsKeywords = ...,
        /,
        *,
        zone_name: str,
        template_thermostat_name: str | None = ...,
        system_availability_schedule_name: str | None = ...,
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
        dehumidification_setpoint: float | None = 60,
        humidification_control_type: Literal["", "ConstantSupplyHumidityRatio", "Humidistat", "None"] | None = "None",
        humidification_setpoint: float | None = 30,
        outdoor_air_method: Literal[
            "", "DetailedSpecification", "Flow/Area", "Flow/Person", "Flow/Zone", "Maximum", "None", "Sum"
        ]
        | None = "None",
        outdoor_air_flow_rate_per_person: float | None = 0.00944,
        outdoor_air_flow_rate_per_zone_floor_area: float | None = 0,
        outdoor_air_flow_rate_per_zone: float | None = 0,
        design_specification_outdoor_air_object_name: str | None = ...,
        demand_controlled_ventilation_type: Literal["", "CO2Setpoint", "None", "OccupancySchedule"] | None = "None",
        outdoor_air_economizer_type: Literal["", "DifferentialDryBulb", "DifferentialEnthalpy", "NoEconomizer"]
        | None = "NoEconomizer",
        heat_recovery_type: Literal["", "Enthalpy", "None", "Sensible"] | None = "None",
        sensible_heat_recovery_effectiveness: float | None = 0.7,
        latent_heat_recovery_effectiveness: float | None = 0.65,
    ) -> None:
        """Create a new ``HVACTemplate:Zone:IdealLoadsAirSystem`` and add it to the document.

        Zone with ideal air system that meets heating or cooling loads

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/hvac-template-objects/group-hvac-templates/#hvactemplatezoneidealloadsairsystem
        """

class AnyAirTerminalSingleDuctVAVHeatAndCoolReheat:
    def __call__(
        self,
        name: str,
        /,
        *,
        damper_air_outlet_node_name: str,
        air_inlet_node_name: str,
        maximum_air_flow_rate: float | Literal["Autosize"],
        zone_minimum_air_flow_fraction: float,
        reheat_coil_object_type: Literal[
            "Coil:Heating:Electric", "Coil:Heating:Fuel", "Coil:Heating:Steam", "Coil:Heating:Water"
        ],
        reheat_coil_name: str,
        air_outlet_node_name: str,
        availability_schedule_name: str | None = ...,
        maximum_hot_water_or_steam_flow_rate: float | Literal["Autosize"] | None = ...,
        minimum_hot_water_or_steam_flow_rate: float | None = 0,
        convergence_tolerance: float | None = 0.001,
        maximum_reheat_air_temperature: float | None = ...,
    ) -> None:
        """Create a new ``AirTerminal:SingleDuct:VAV:HeatAndCool:Reheat`` and add it to the document.

        Central air system terminal unit, single duct, variable volume for both cooling and heating, with reheat coil (hot water, electric, gas, or steam).

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-zone-hvac-air-loop-terminal-units/#airterminalsingleductvavheatandcoolreheat
        """

class AnyAirTerminalSingleDuctConstantVolumeCooledBeam:
    def __call__(
        self,
        name: str,
        /,
        *,
        cooled_beam_type: Literal["Active", "Passive"],
        supply_air_inlet_node_name: str,
        supply_air_outlet_node_name: str,
        chilled_water_inlet_node_name: str,
        chilled_water_outlet_node_name: str,
        availability_schedule_name: str | None = ...,
        supply_air_volumetric_flow_rate: float | Literal["", "Autosize"] | None = "Autosize",
        maximum_total_chilled_water_volumetric_flow_rate: float | Literal["", "Autosize"] | None = "Autosize",
        number_of_beams: int | Literal["", "Autosize"] | None = "Autosize",
        beam_length: float | Literal["", "Autosize"] | None = "Autosize",
        design_inlet_water_temperature: float | None = 15,
        design_outlet_water_temperature: float | None = 17,
        coil_surface_area_per_coil_length: float | None = 5.422,
        model_parameter_a: float | None = 15.3,
        model_parameter_n1: float | None = 0,
        model_parameter_n2: float | None = 0.84,
        model_parameter_n3: float | None = 0.12,
        model_parameter_a0: float | None = 0.171,
        model_parameter_k1: float | None = 0.0057,
        model_parameter_n: float | None = 0.4,
        coefficient_of_induction_kin: float | Literal["", "Autocalculate"] | None = "Autocalculate",
        leaving_pipe_inside_diameter: float | None = 0.0145,
    ) -> None:
        """Create a new ``AirTerminal:SingleDuct:ConstantVolume:CooledBeam`` and add it to the document.

        Central air system terminal unit, single duct, constant volume, with cooled beam (active or passive).

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-air-distribution-equipment/#airterminalsingleductconstantvolumecooledbeam
        """

class AnyCoilSystemIntegratedHeatPumpAirSource:
    def __call__(
        self,
        name: str,
        /,
        *,
        supply_hot_water_flow_sensor_node_name: str,
        space_cooling_coil_name: str,
        space_heating_coil_name: str | None = ...,
        dedicated_water_heating_coil_name: str | None = ...,
        scwh_coil_name: str | None = ...,
        scdwh_cooling_coil_name: str | None = ...,
        scdwh_water_heating_coil_name: str | None = ...,
        shdwh_heating_coil_name: str | None = ...,
        shdwh_water_heating_coil_name: str | None = ...,
        indoor_temperature_limit_for_scwh_mode: float | None = 20,
        ambient_temperature_limit_for_scwh_mode: float | None = 27,
        indoor_temperature_above_which_wh_has_higher_priority: float | None = 20,
        ambient_temperature_above_which_wh_has_higher_priority: float | None = 20,
        flag_to_indicate_load_control_in_scwh_mode: int | None = 0,
        minimum_speed_level_for_scwh_mode: int | None = 1,
        maximum_water_flow_volume_before_switching_from_scdwh_to_scwh_mode: float | None = 0,
        minimum_speed_level_for_scdwh_mode: int | None = 1,
        maximum_running_time_before_allowing_electric_resistance_heat_use_during_shdwh_mode: float | None = 360,
        minimum_speed_level_for_shdwh_mode: int | None = 1,
    ) -> None:
        """Create a new ``CoilSystem:IntegratedHeatPump:AirSource`` and add it to the document.

        This object is used for air-source integrated heat pump, a collection of its working modes.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-heating-and-cooling-coils/#coilsystemintegratedheatpumpairsource
        """

class ThermalStorageHotWaterStratified:
    def __call__(
        self,
        name: str,
        /,
        *,
        tank_volume: float,
        tank_height: float,
        ambient_temperature_indicator: Literal["Outdoors", "Schedule", "Zone"],
        tank_shape: Literal["", "HorizontalCylinder", "Other", "VerticalCylinder"] | None = "VerticalCylinder",
        tank_perimeter: float | None = ...,
        top_setpoint_temperature_schedule_name: str | None = ...,
        bottom_setpoint_temperature_schedule_name: str | None = ...,
        deadband_temperature_difference: float | None = 0.0001,
        top_temperature_sensor_height: float | None = ...,
        bottom_temperature_sensor_height: float | None = ...,
        maximum_temperature_limit: float | None = ...,
        nominal_heating_capacity: float | Literal["", "Autosize"] | None = "Autosize",
        ambient_temperature_schedule_name: str | None = ...,
        ambient_temperature_zone_name: str | None = ...,
        ambient_temperature_outdoor_air_node_name: str | None = ...,
        uniform_skin_loss_coefficient_per_unit_area_to_ambient_temperature: float | None = ...,
        use_side_inlet_node_name: str | None = ...,
        use_side_outlet_node_name: str | None = ...,
        use_side_flow_direction_schedule: str | None = ...,
        use_side_heat_transfer_effectiveness: float | None = 1,
        use_side_availability_schedule_name: str | None = ...,
        use_side_inlet_height: float | Literal["", "Autocalculate"] | None = "Autocalculate",
        use_side_outlet_height: float | None = 0,
        use_side_design_flow_rate: float | Literal["", "Autosize"] | None = "Autosize",
        source_side_inlet_node_name: str | None = ...,
        source_side_outlet_node_name: str | None = ...,
        source_side_flow_direction_schedule: str | None = ...,
        source_side_heat_transfer_effectiveness: float | None = 1,
        source_side_availability_schedule_name: str | None = ...,
        source_side_inlet_height: float | None = 0,
        source_side_outlet_height: float | Literal["", "Autocalculate"] | None = "Autocalculate",
        source_side_design_flow_rate: float | Literal["", "Autosize"] | None = "Autosize",
        tank_recovery_time: float | None = 4,
        inlet_mode: Literal["", "Fixed", "Seeking"] | None = "Fixed",
        number_of_nodes: int | None = 1,
        additional_destratification_conductivity: float | None = 0,
        node_1_additional_loss_coefficient: float | None = 0,
        node_2_additional_loss_coefficient: float | None = 0,
        node_3_additional_loss_coefficient: float | None = 0,
        node_4_additional_loss_coefficient: float | None = 0,
        node_5_additional_loss_coefficient: float | None = 0,
        node_6_additional_loss_coefficient: float | None = 0,
        node_7_additional_loss_coefficient: float | None = 0,
        node_8_additional_loss_coefficient: float | None = 0,
        node_9_additional_loss_coefficient: float | None = 0,
        node_10_additional_loss_coefficient: float | None = 0,
    ) -> None:
        """Create a new ``ThermalStorage:HotWater:Stratified`` and add it to the document.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-water-heaters/#thermalstoragehotwaterstratified
        """

class WaterUseEquipment:
    def __call__(
        self,
        name: str,
        /,
        *,
        peak_flow_rate: float,
        end_use_subcategory: str | None = "General",
        flow_rate_fraction_schedule_name: str | None = ...,
        target_temperature_schedule_name: str | None = ...,
        hot_water_supply_temperature_schedule_name: str | None = ...,
        cold_water_supply_temperature_schedule_name: str | None = ...,
        zone_name: str | None = ...,
        sensible_fraction_schedule_name: str | None = ...,
        latent_fraction_schedule_name: str | None = ...,
    ) -> None:
        """Create a new ``WaterUse:Equipment`` and add it to the document.

        A generalized object for simulating all water end uses. Hot and cold water uses are included, as well as controlled mixing of hot and cold water at the tap. The WaterUse:Equipment object can be used stand-alone, or coupled into a plant loop using the WaterUse:Connections object (see below). The WaterUse:Connections object allows water uses to be linked to WaterUse:Storage objects to store and draw reclaimed water. The object can also simulate drainwater heat recovery.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-water-systems/#wateruseequipment
        """
