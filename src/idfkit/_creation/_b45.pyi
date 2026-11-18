"""Creation signatures of generated classes (stub only).

DO NOT EDIT — regenerate with:
    python -m idfkit.codegen.generate_stubs
"""

from __future__ import annotations

from typing import Literal

class AnyPerformancePrecisionTradeoffs:
    def __call__(self, /, *, use_coil_direct_solutions: Literal["No", "Yes"] | None = "No") -> None:
        """Create a new ``PerformancePrecisionTradeoffs`` and add it to the document.

        This object enables users to choose certain options that speed up EnergyPlus simulation, but may lead to small decreases in accuracy of results.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-simulation-parameters/#performanceprecisiontradeoffs
        """

class Roof:
    def __call__(
        self,
        name: str,
        /,
        *,
        construction_name: str,
        zone_name: str,
        space_name: str | None = ...,
        azimuth_angle: float | None = ...,
        tilt_angle: float | None = 0,
        starting_x_coordinate: float | None = ...,
        starting_y_coordinate: float | None = ...,
        starting_z_coordinate: float | None = ...,
        length: float | None = ...,
        width: float | None = ...,
    ) -> None:
        """Create a new ``Roof`` and add it to the document.

        Allows for simplified entry of roofs (exterior). View Factor to Ground is automatically calculated.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-thermal-zone-description-geometry/#roof
        """

class DoorInterzone:
    def __call__(
        self,
        name: str,
        /,
        *,
        construction_name: str,
        building_surface_name: str,
        outside_boundary_condition_object: str | None = ...,
        multiplier: float | None = 1,
        starting_x_coordinate: float | None = ...,
        starting_z_coordinate: float | None = ...,
        length: float | None = ...,
        height: float | None = ...,
    ) -> None:
        """Create a new ``Door:Interzone`` and add it to the document.

        Allows for simplified entry of interzone (opaque interior) doors (adjacent to other zones).

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-thermal-zone-description-geometry/#doorinterzone
        """

class AnyHVACTemplateZoneFanCoil:
    def __call__(
        self,
        /,
        *,
        zone_name: str,
        template_thermostat_name: str | None = ...,
        supply_air_maximum_flow_rate: float | Literal["Autosize"] | None = "Autosize",
        zone_heating_sizing_factor: float | None = ...,
        zone_cooling_sizing_factor: float | None = ...,
        outdoor_air_method: Literal["DetailedSpecification", "Flow/Area", "Flow/Person", "Flow/Zone", "Maximum", "Sum"]
        | None = "Flow/Person",
        outdoor_air_flow_rate_per_person: float | None = 0.00944,
        outdoor_air_flow_rate_per_zone_floor_area: float | None = 0,
        outdoor_air_flow_rate_per_zone: float | None = 0,
        system_availability_schedule_name: str | None = ...,
        supply_fan_total_efficiency: float | None = 0.7,
        supply_fan_delta_pressure: float | None = 75,
        supply_fan_motor_efficiency: float | None = 0.9,
        supply_fan_motor_in_air_stream_fraction: float | None = 1,
        cooling_coil_type: Literal["ChilledWater", "ChilledWaterDetailedFlatModel"] | None = "ChilledWater",
        cooling_coil_availability_schedule_name: str | None = ...,
        cooling_coil_design_setpoint: float | None = 14,
        heating_coil_type: Literal["HotWater"] | None = "HotWater",
        heating_coil_availability_schedule_name: str | None = ...,
        heating_coil_design_setpoint: float | None = 50,
        dedicated_outdoor_air_system_name: str | None = ...,
        zone_cooling_design_supply_air_temperature_input_method: Literal[
            "SupplyAirTemperature", "TemperatureDifference"
        ]
        | None = "SupplyAirTemperature",
        zone_cooling_design_supply_air_temperature_difference: float | None = 11.11,
        zone_heating_design_supply_air_temperature_input_method: Literal[
            "SupplyAirTemperature", "TemperatureDifference"
        ]
        | None = "SupplyAirTemperature",
        zone_heating_design_supply_air_temperature_difference: float | None = 30,
        design_specification_outdoor_air_object_name: str | None = ...,
        design_specification_zone_air_distribution_object_name: str | None = ...,
        capacity_control_method: Literal[
            "ConstantFanVariableFlow", "CyclingFan", "VariableFanConstantFlow", "VariableFanVariableFlow"
        ]
        | None = ...,
        low_speed_supply_air_flow_ratio: float | None = 0.33,
        medium_speed_supply_air_flow_ratio: float | None = 0.66,
        outdoor_air_schedule_name: str | None = ...,
        baseboard_heating_type: Literal["Electric", "HotWater", "None"] | None = "None",
        baseboard_heating_availability_schedule_name: str | None = ...,
        baseboard_heating_capacity: float | Literal["Autosize"] | None = "Autosize",
    ) -> None:
        """Create a new ``HVACTemplate:Zone:FanCoil`` and add it to the document.

        4 pipe fan coil unit with optional outdoor air.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/hvac-template-objects/group-hvac-templates/#hvactemplatezonefancoil
        """

class ZoneHVACPackagedTerminalAirConditioner:
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
        heating_coil_object_type: Literal[
            "Coil:Heating:Electric", "Coil:Heating:Fuel", "Coil:Heating:Steam", "Coil:Heating:Water"
        ],
        heating_coil_name: str,
        cooling_coil_object_type: Literal[
            "Coil:Cooling:DX",
            "Coil:Cooling:DX:SingleSpeed",
            "Coil:Cooling:DX:VariableSpeed",
            "CoilSystem:Cooling:DX:HeatExchangerAssisted",
        ],
        cooling_coil_name: str,
        availability_schedule_name: str | None = ...,
        outdoor_air_mixer_object_type: Literal["OutdoorAir:Mixer"] | None = ...,
        outdoor_air_mixer_name: str | None = ...,
        no_load_supply_air_flow_rate: float | Literal["Autosize"] | None = ...,
        no_load_supply_air_flow_rate_control_set_to_low_speed: Literal["No", "Yes"] | None = "Yes",
        no_load_outdoor_air_flow_rate: float | Literal["Autosize"] | None = ...,
        fan_placement: Literal["BlowThrough", "DrawThrough"] | None = "DrawThrough",
        supply_air_fan_operating_mode_schedule_name: str | None = ...,
        availability_manager_list_name: str | None = ...,
        design_specification_zonehvac_sizing_object_name: str | None = ...,
        capacity_control_method: Literal["None", "SingleZoneVAV"] | None = "None",
        minimum_supply_air_temperature_in_cooling_mode: float | Literal["Autosize"] | None = "Autosize",
        maximum_supply_air_temperature_in_heating_mode: float | Literal["Autosize"] | None = "Autosize",
    ) -> None:
        """Create a new ``ZoneHVAC:PackagedTerminalAirConditioner`` and add it to the document.

        Packaged terminal air conditioner (PTAC). Forced-convection heating-cooling unit with supply fan, direct expansion (DX) cooling coil, heating coil (gas, electric, hot water, or steam) and fixed-position outdoor air mixer.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-zone-forced-air-units/#zonehvacpackagedterminalairconditioner
        """

class ZoneHVACEquipmentConnections:
    def __call__(
        self,
        /,
        *,
        zone_name: str,
        zone_conditioning_equipment_list_name: str,
        zone_air_node_name: str,
        zone_air_inlet_node_or_nodelist_name: str | None = ...,
        zone_air_exhaust_node_or_nodelist_name: str | None = ...,
        zone_return_air_node_or_nodelist_name: str | None = ...,
        zone_return_air_node_1_flow_rate_fraction_schedule_name: str | None = ...,
        zone_return_air_node_1_flow_rate_basis_node_or_nodelist_name: str | None = ...,
    ) -> None:
        """Create a new ``ZoneHVAC:EquipmentConnections`` and add it to the document.

        Specifies the HVAC equipment connections for a zone. Node names are specified for the zone air node, air inlet nodes, air exhaust nodes, and the air return node. A zone equipment list is referenced which lists all HVAC equipment connected to the zone.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-zone-equipment/#zonehvacequipmentconnections
        """

class PlantEquipmentOperationCoolingLoad:
    def __call__(
        self,
        name: str,
        /,
        *,
        load_range_1_lower_limit: float,
        load_range_1_upper_limit: float,
        range_1_equipment_list_name: str | None = ...,
        load_range_2_lower_limit: float | None = ...,
        load_range_2_upper_limit: float | None = ...,
        range_2_equipment_list_name: str | None = ...,
        load_range_3_lower_limit: float | None = ...,
        load_range_3_upper_limit: float | None = ...,
        range_3_equipment_list_name: str | None = ...,
        load_range_4_lower_limit: float | None = ...,
        load_range_4_upper_limit: float | None = ...,
        range_4_equipment_list_name: str | None = ...,
        load_range_5_lower_limit: float | None = ...,
        load_range_5_upper_limit: float | None = ...,
        range_5_equipment_list_name: str | None = ...,
        load_range_6_lower_limit: float | None = ...,
        load_range_6_upper_limit: float | None = ...,
        range_6_equipment_list_name: str | None = ...,
        load_range_7_lower_limit: float | None = ...,
        load_range_7_upper_limit: float | None = ...,
        range_7_equipment_list_name: str | None = ...,
        load_range_8_lower_limit: float | None = ...,
        load_range_8_upper_limit: float | None = ...,
        range_8_equipment_list_name: str | None = ...,
        load_range_9_lower_limit: float | None = ...,
        load_range_9_upper_limit: float | None = ...,
        range_9_equipment_list_name: str | None = ...,
        load_range_10_lower_limit: float | None = ...,
        load_range_10_upper_limit: float | None = ...,
        range_10_equipment_list_name: str | None = ...,
    ) -> None:
        """Create a new ``PlantEquipmentOperation:CoolingLoad`` and add it to the document.

        Plant equipment operation scheme for cooling load range operation. Specifies one or more groups of equipment which are available to operate for successive cooling load ranges.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-plant-condenser-control/#plantequipmentoperationcoolingload
        """

class FaultModelTemperatureSensorOffsetCoilSupplyAir:
    def __call__(
        self,
        name: str,
        /,
        *,
        coil_object_type: Literal[
            "AirLoopHVAC:UnitarySystem",
            "Coil:Cooling:Water",
            "Coil:Cooling:Water:Detailedgeometry",
            "Coil:Heating:Desuperheater",
            "Coil:Heating:Electric",
            "Coil:Heating:Gas",
            "Coil:Heating:Steam",
            "Coil:Heating:Water",
            "CoilSystem:Cooling:DX",
            "CoilSystem:Heating:DX",
        ],
        coil_object_name: str,
        availability_schedule_name: str | None = ...,
        severity_schedule_name: str | None = ...,
        water_coil_controller_name: str | None = ...,
        reference_sensor_offset: float | None = 0,
    ) -> None:
        """Create a new ``FaultModel:TemperatureSensorOffset:CoilSupplyAir`` and add it to the document.

        This object describes fault of coil supply air temperature sensor offset

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-operational-faults/#faultmodeltemperaturesensoroffsetcoilsupplyair
        """

class FaultModelFoulingBoiler:
    def __call__(
        self,
        name: str,
        /,
        *,
        boiler_object_type: Literal["Boiler:HotWater"],
        boiler_object_name: str,
        availability_schedule_name: str | None = ...,
        severity_schedule_name: str | None = ...,
        fouling_factor: float | None = 1,
    ) -> None:
        """Create a new ``FaultModel:Fouling:Boiler`` and add it to the document.

        This object describes the fouling fault of boilers with water-based heat exchangers

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-operational-faults/#faultmodelfoulingboiler
        """
