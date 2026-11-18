"""Creation signatures of generated classes (stub only).

DO NOT EDIT — regenerate with:
    python -m idfkit.codegen.generate_stubs
"""

from __future__ import annotations

from collections.abc import Sequence
from typing import Literal

from .. import _generated_types as _g

class ScheduleWeekDaily:
    def __call__(
        self,
        name: str,
        /,
        *,
        sunday_schedule_day_name: str,
        monday_schedule_day_name: str,
        tuesday_schedule_day_name: str,
        wednesday_schedule_day_name: str,
        thursday_schedule_day_name: str,
        friday_schedule_day_name: str,
        saturday_schedule_day_name: str,
        holiday_schedule_day_name: str,
        summerdesignday_schedule_day_name: str,
        winterdesignday_schedule_day_name: str,
        customday1_schedule_day_name: str,
        customday2_schedule_day_name: str,
    ) -> None:
        """Create a new ``Schedule:Week:Daily`` and add it to the document.

        A Schedule:Week:Daily contains 12 Schedule:Day:Hourly objects, one for each day type.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-schedules/#scheduleweekdaily
        """

class WallAdiabatic:
    def __call__(
        self,
        name: str,
        /,
        *,
        construction_name: str,
        zone_name: str,
        space_name: str | None = ...,
        azimuth_angle: float | None = ...,
        tilt_angle: float | None = 90,
        starting_x_coordinate: float | None = ...,
        starting_y_coordinate: float | None = ...,
        starting_z_coordinate: float | None = ...,
        length: float | None = ...,
        height: float | None = ...,
    ) -> None:
        """Create a new ``Wall:Adiabatic`` and add it to the document.

        Allows for simplified entry of interior walls.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-thermal-zone-description-geometry/#walladiabatic
        """

class ShadingFinProjection:
    def __call__(
        self,
        name: str,
        /,
        *,
        window_or_door_name: str,
        left_extension_from_window_door: float | None = ...,
        left_distance_above_top_of_window: float | None = ...,
        left_distance_below_bottom_of_window: float | None = ...,
        left_tilt_angle_from_window_door: float | None = 90,
        left_depth_as_fraction_of_window_door_width: float | None = ...,
        right_extension_from_window_door: float | None = ...,
        right_distance_above_top_of_window: float | None = ...,
        right_distance_below_bottom_of_window: float | None = ...,
        right_tilt_angle_from_window_door: float | None = 90,
        right_depth_as_fraction_of_window_door_width: float | None = ...,
    ) -> None:
        """Create a new ``Shading:Fin:Projection`` and add it to the document.

        Fins are usually shading surfaces that are perpendicular to a window or door.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-thermal-zone-description-geometry/#shadingfinprojection
        """

class AirflowNetworkMultiZoneReferenceCrackConditions:
    def __call__(
        self,
        name: str,
        /,
        *,
        reference_temperature: float,
        reference_barometric_pressure: float | None = 101325,
        reference_humidity_ratio: float | None = 0,
    ) -> None:
        """Create a new ``AirflowNetwork:MultiZone:ReferenceCrackConditions`` and add it to the document.

        This object specifies the conditions under which the air mass flow coefficient was measured.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-airflow-network/#airflownetworkmultizonereferencecrackconditions
        """

class AnyHVACTemplateZonePTHP:
    def __call__(
        self,
        this_type_has_no_name_field: _g._PassFieldsAsKeywords = ...,
        /,
        *,
        zone_name: str,
        template_thermostat_name: str | None = ...,
        cooling_supply_air_flow_rate: float | Literal["", "Autosize"] | None = "Autosize",
        heating_supply_air_flow_rate: float | Literal["", "Autosize"] | None = "Autosize",
        no_load_supply_air_flow_rate: float | Literal["Autosize"] | None = ...,
        zone_heating_sizing_factor: float | None = ...,
        zone_cooling_sizing_factor: float | None = ...,
        outdoor_air_method: Literal[
            "", "DetailedSpecification", "Flow/Area", "Flow/Person", "Flow/Zone", "Maximum", "Sum"
        ]
        | None = "Flow/Person",
        outdoor_air_flow_rate_per_person: float | None = 0.00944,
        outdoor_air_flow_rate_per_zone_floor_area: float | None = 0,
        outdoor_air_flow_rate_per_zone: float | None = 0,
        system_availability_schedule_name: str | None = ...,
        supply_fan_operating_mode_schedule_name: str | None = ...,
        supply_fan_placement: Literal["", "BlowThrough", "DrawThrough"] | None = "DrawThrough",
        supply_fan_total_efficiency: float | None = 0.7,
        supply_fan_delta_pressure: float | None = 75,
        supply_fan_motor_efficiency: float | None = 0.9,
        cooling_coil_type: Literal["", "SingleSpeedDX"] | None = "SingleSpeedDX",
        cooling_coil_availability_schedule_name: str | None = ...,
        cooling_coil_gross_rated_total_capacity: float | Literal["", "Autosize"] | None = "Autosize",
        cooling_coil_gross_rated_sensible_heat_ratio: float | Literal["", "Autosize"] | None = "Autosize",
        cooling_coil_gross_rated_cop: float | None = 3,
        heat_pump_heating_coil_type: Literal["", "SingleSpeedDXHeatPump"] | None = "SingleSpeedDXHeatPump",
        heat_pump_heating_coil_availability_schedule_name: str | None = ...,
        heat_pump_heating_coil_gross_rated_capacity: float | Literal["", "Autosize"] | None = "Autosize",
        heat_pump_heating_coil_gross_rated_cop: float | None = 2.75,
        heat_pump_heating_minimum_outdoor_dry_bulb_temperature: float | None = -8,
        heat_pump_defrost_maximum_outdoor_dry_bulb_temperature: float | None = 5,
        heat_pump_defrost_strategy: Literal["", "Resistive", "ReverseCycle"] | None = "ReverseCycle",
        heat_pump_defrost_control: Literal["", "OnDemand", "Timed"] | None = "Timed",
        heat_pump_defrost_time_period_fraction: float | None = 0.058333,
        supplemental_heating_coil_type: Literal["", "Electric", "Gas", "HotWater"] | None = "Electric",
        supplemental_heating_coil_availability_schedule_name: str | None = ...,
        supplemental_heating_coil_capacity: float | Literal["", "Autosize"] | None = "Autosize",
        supplemental_heating_coil_maximum_outdoor_dry_bulb_temperature: float | None = 21,
        supplemental_gas_heating_coil_efficiency: float | None = 0.8,
        supplemental_gas_heating_coil_parasitic_electric_load: float | None = 0,
        dedicated_outdoor_air_system_name: str | None = ...,
        zone_cooling_design_supply_air_temperature_input_method: Literal[
            "", "SupplyAirTemperature", "TemperatureDifference"
        ]
        | None = "SupplyAirTemperature",
        zone_cooling_design_supply_air_temperature: float | None = 14,
        zone_cooling_design_supply_air_temperature_difference: float | None = 11.11,
        zone_heating_design_supply_air_temperature_input_method: Literal[
            "", "SupplyAirTemperature", "TemperatureDifference"
        ]
        | None = "SupplyAirTemperature",
        zone_heating_design_supply_air_temperature: float | None = 50,
        zone_heating_design_supply_air_temperature_difference: float | None = 30,
        design_specification_outdoor_air_object_name: str | None = ...,
        design_specification_zone_air_distribution_object_name: str | None = ...,
        baseboard_heating_type: Literal["", "Electric", "HotWater", "None"] | None = "None",
        baseboard_heating_availability_schedule_name: str | None = ...,
        baseboard_heating_capacity: float | Literal["", "Autosize"] | None = "Autosize",
    ) -> None:
        """Create a new ``HVACTemplate:Zone:PTHP`` and add it to the document.

        Packaged Terminal Heat Pump

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/hvac-template-objects/group-hvac-templates/#hvactemplatezonepthp
        """

class ThermostatSetpointDualSetpoint:
    def __call__(
        self,
        name: str,
        /,
        *,
        heating_setpoint_temperature_schedule_name: str | None = ...,
        cooling_setpoint_temperature_schedule_name: str | None = ...,
    ) -> None:
        """Create a new ``ThermostatSetpoint:DualSetpoint`` and add it to the document.

        Used for a heating and cooling thermostat with dual setpoints. The setpoints can be scheduled and varied throughout the simulation for both heating and cooling.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-zone-controls-thermostats/#thermostatsetpointdualsetpoint
        """

class AirTerminalSingleDuctConstantVolumeNoReheat:
    def __call__(
        self,
        name: str,
        /,
        *,
        air_inlet_node_name: str,
        air_outlet_node_name: str,
        maximum_air_flow_rate: float | Literal["Autosize"],
        availability_schedule_name: str | None = ...,
        design_specification_outdoor_air_object_name: str | None = ...,
        per_person_ventilation_rate_mode: Literal["", "CurrentOccupancy", "DesignOccupancy"]
        | None = "CurrentOccupancy",
    ) -> None:
        """Create a new ``AirTerminal:SingleDuct:ConstantVolume:NoReheat`` and add it to the document.

        Central air system terminal unit, single duct, constant volume, without reheat coil

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-air-distribution-equipment/#airterminalsingleductconstantvolumenoreheat
        """

class FanZoneExhaust:
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
        maximum_flow_rate: float | None = ...,
        end_use_subcategory: str | None = "General",
        flow_fraction_schedule_name: str | None = ...,
        system_availability_manager_coupling_mode: Literal["", "Coupled", "Decoupled"] | None = "Coupled",
        minimum_zone_temperature_limit_schedule_name: str | None = ...,
        balanced_exhaust_fraction_schedule_name: str | None = ...,
    ) -> None:
        """Create a new ``Fan:ZoneExhaust`` and add it to the document.

        Models a fan that exhausts air from a zone.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-fans/#fanzoneexhaust
        """

class UnitarySystemPerformanceMultispeed:
    def __call__(
        self,
        name: str,
        /,
        *,
        number_of_speeds_for_heating: int,
        number_of_speeds_for_cooling: int,
        single_mode_operation: Literal["", "No", "Yes"] | None = "No",
        no_load_supply_air_flow_rate_ratio: float | None = 1,
        flow_ratios: Sequence[
            _g.UnitarySystemPerformanceMultispeedFlowRatiosItem | _g.UnitarySystemPerformanceMultispeedFlowRatiosGroup
        ] = ...,
    ) -> None:
        """Create a new ``UnitarySystemPerformance:Multispeed`` and add it to the document.

        The UnitarySystemPerformance object is used to specify the air flow ratio at each operating speed. This object is primarily used for multispeed DX and water coils to allow operation at alternate flow rates different from those specified in the coil object.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-unitary-equipment/#unitarysystemperformancemultispeed
        """

class AnyChillerConstantCOP:
    def __call__(
        self,
        name: str,
        /,
        *,
        nominal_capacity: float | Literal["Autosize"],
        nominal_cop: float,
        chilled_water_inlet_node_name: str,
        chilled_water_outlet_node_name: str,
        design_chilled_water_flow_rate: float | Literal["Autosize"] | None = ...,
        design_condenser_water_flow_rate: float | Literal["Autosize"] | None = ...,
        condenser_inlet_node_name: str | None = ...,
        condenser_outlet_node_name: str | None = ...,
        condenser_type: Literal["", "AirCooled", "EvaporativelyCooled", "WaterCooled"] | None = "AirCooled",
        chiller_flow_mode: Literal["", "ConstantFlow", "LeavingSetpointModulated", "NotModulated"]
        | None = "NotModulated",
        sizing_factor: float | None = 1,
        basin_heater_capacity: float | None = 0,
        basin_heater_setpoint_temperature: float | None = 2,
        basin_heater_operating_schedule_name: str | None = ...,
    ) -> None:
        """Create a new ``Chiller:ConstantCOP`` and add it to the document.

        This constant COP chiller model provides a means of quickly specifying a Chiller where performance data is not available.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-plant-equipment/#chillerconstantcop
        """

class CondenserEquipmentList:
    def __call__(
        self,
        name: str,
        /,
        *,
        equipment: Sequence[_g.CondenserEquipmentListEquipmentItem | _g.CondenserEquipmentListEquipmentGroup] = ...,
    ) -> None:
        """Create a new ``CondenserEquipmentList`` and add it to the document.

        List condenser equipment in order of operating priority, 1st in list will be used 1st, etc Use only condenser equipment in this list. If no equipment object types and equipment names are specified, then the corresponding PlantEquipmentOperation:* object will assume all available condenser equipment for the loop should be OFF (not operate) within the specified lower/upper limit.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-plant-condenser-control/#condenserequipmentlist
        """
