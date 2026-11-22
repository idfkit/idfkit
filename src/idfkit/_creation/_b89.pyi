"""Creation signatures of generated classes (stub only).

DO NOT EDIT — regenerate with:
    python -m idfkit.codegen.generate_stubs
"""

from __future__ import annotations

from collections.abc import Sequence
from typing import Literal

from typing_extensions import Never

from .. import _generated_types as _g

class AnyScheduleYear:
    def __call__(
        self,
        name: str,
        /,
        *,
        narrow_with_as_version_first: Never,
        schedule_type_limits_name: str | None = ...,
        validate: bool = True,
    ) -> None:
        """Create a new ``Schedule:Year`` and add it to the document.

        A Schedule:Year contains from 1 to 52 week schedules

        ``schedule_weeks`` takes the extensible groups in order, one dict per group:

        ```python
        doc["Schedule:Year"].add(
            "Schedule Year 1",
            schedule_weeks=[
                {
                    "schedule_week_name": "Schedule:Week 1",
                    "start_month": 1,
                    "start_day": 1,
                    "end_month": 1,
                    "end_day": 1,
                },
                {
                    "schedule_week_name": "Schedule:Week 2",
                    "start_month": 1,
                    "start_day": 1,
                    "end_month": 1,
                    "end_day": 1,
                },
            ],
        )
        ```

        No call suits every release: narrow the document with ``as_version`` first.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-schedules/#scheduleyear
        """

class WindowMaterialDrapeEquivalentLayer:
    def __call__(
        self,
        name: str,
        /,
        *,
        front_side_drape_beam_diffuse_solar_transmittance: float,
        back_side_drape_beam_diffuse_solar_transmittance: float,
        front_side_drape_beam_diffuse_solar_reflectance: float,
        back_side_drape_beam_diffuse_solar_reflectance: float,
        drape_beam_beam_solar_transmittance_at_normal_incidence: float | None = 0,
        drape_beam_beam_visible_transmittance: float | None = ...,
        drape_beam_diffuse_visible_transmittance: float | None = ...,
        drape_beam_diffuse_visible_reflectance: float | None = ...,
        drape_material_infrared_transmittance: float | None = 0.05,
        front_side_drape_material_infrared_emissivity: float | None = 0.87,
        back_side_drape_material_infrared_emissivity: float | None = 0.87,
        width_of_pleated_fabric: float | None = 0,
        length_of_pleated_fabric: float | None = 0,
        validate: bool = True,
    ) -> None:
        """Create a new ``WindowMaterial:Drape:EquivalentLayer`` and add it to the document.

        Specifies the properties of equivalent layer drape fabric materials. Shades are considered to be perfect diffusers (all transmitted and reflected radiation is hemispherically-diffuse) independent of angle of incidence. unpleated drape fabric is treated as thin and flat layer.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-surface-construction-elements/#windowmaterialdrapeequivalentlayer
        """

class AirflowNetworkMultiZoneSurfaceCrack:
    def __call__(
        self,
        name: str,
        /,
        *,
        air_mass_flow_coefficient_at_reference_conditions: float,
        air_mass_flow_exponent: float | None = 0.65,
        reference_crack_conditions: str | None = ...,
        validate: bool = True,
    ) -> None:
        """Create a new ``AirflowNetwork:MultiZone:Surface:Crack`` and add it to the document.

        This object specifies the properties of airflow through a crack.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-airflow-network/#airflownetworkmultizonesurfacecrack
        """

class HVACTemplateZonePTAC:
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
        cooling_coil_type: Literal["SingleSpeedDX"] | None = "SingleSpeedDX",
        cooling_coil_availability_schedule_name: str | None = ...,
        cooling_coil_gross_rated_total_capacity: float | Literal["Autosize"] | None = "Autosize",
        cooling_coil_gross_rated_sensible_heat_ratio: float | Literal["Autosize"] | None = "Autosize",
        cooling_coil_gross_rated_cooling_cop: float | None = 3,
        heating_coil_type: Literal["Electric", "Gas", "HotWater"] | None = "Electric",
        heating_coil_availability_schedule_name: str | None = ...,
        heating_coil_capacity: float | Literal["Autosize"] | None = "Autosize",
        gas_heating_coil_efficiency: float | None = 0.8,
        gas_heating_coil_parasitic_electric_load: float | None = 0,
        dedicated_outdoor_air_system_name: str | None = ...,
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
        design_specification_outdoor_air_object_name: str | None = ...,
        design_specification_zone_air_distribution_object_name: str | None = ...,
        baseboard_heating_type: Literal["Electric", "HotWater", "None"] | None = "None",
        baseboard_heating_availability_schedule_name: str | None = ...,
        baseboard_heating_capacity: float | Literal["Autosize"] | None = "Autosize",
        capacity_control_method: Literal["None", "SingleZoneVAV"] | None = "None",
        validate: bool = True,
    ) -> None:
        """Create a new ``HVACTemplate:Zone:PTAC`` and add it to the document.

        Packaged Terminal Air Conditioner

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/hvac-template-objects/group-hvac-templates/#hvactemplatezoneptac
        """

class ZoneControlThermostatThermalComfort:
    def __call__(
        self,
        name: str,
        /,
        *,
        zone_or_zonelist_name: str,
        thermal_comfort_control_type_schedule_name: str,
        thermal_comfort_control_1_object_type: Literal[
            "ThermostatSetpoint:ThermalComfort:Fanger:DualSetpoint",
            "ThermostatSetpoint:ThermalComfort:Fanger:SingleCooling",
            "ThermostatSetpoint:ThermalComfort:Fanger:SingleHeating",
            "ThermostatSetpoint:ThermalComfort:Fanger:SingleHeatingOrCooling",
        ],
        thermal_comfort_control_1_name: str,
        averaging_method: Literal["ObjectAverage", "PeopleAverage", "SpecificObject"] | None = "PeopleAverage",
        specific_people_name: str | None = ...,
        minimum_dry_bulb_temperature_setpoint: float | None = 0,
        maximum_dry_bulb_temperature_setpoint: float | None = 50,
        thermal_comfort_control_2_object_type: Literal[
            "ThermostatSetpoint:ThermalComfort:Fanger:DualSetpoint",
            "ThermostatSetpoint:ThermalComfort:Fanger:SingleCooling",
            "ThermostatSetpoint:ThermalComfort:Fanger:SingleHeating",
            "ThermostatSetpoint:ThermalComfort:Fanger:SingleHeatingOrCooling",
        ]
        | None = ...,
        thermal_comfort_control_2_name: str | None = ...,
        thermal_comfort_control_3_object_type: Literal[
            "ThermostatSetpoint:ThermalComfort:Fanger:DualSetpoint",
            "ThermostatSetpoint:ThermalComfort:Fanger:SingleCooling",
            "ThermostatSetpoint:ThermalComfort:Fanger:SingleHeating",
            "ThermostatSetpoint:ThermalComfort:Fanger:SingleHeatingOrCooling",
        ]
        | None = ...,
        thermal_comfort_control_3_name: str | None = ...,
        thermal_comfort_control_4_object_type: Literal[
            "ThermostatSetpoint:ThermalComfort:Fanger:DualSetpoint",
            "ThermostatSetpoint:ThermalComfort:Fanger:SingleCooling",
            "ThermostatSetpoint:ThermalComfort:Fanger:SingleHeating",
            "ThermostatSetpoint:ThermalComfort:Fanger:SingleHeatingOrCooling",
        ]
        | None = ...,
        thermal_comfort_control_4_name: str | None = ...,
        validate: bool = True,
    ) -> None:
        """Create a new ``ZoneControl:Thermostat:ThermalComfort`` and add it to the document.

        If you use a ZoneList in the Zone or ZoneList name field then this definition applies to all the zones in the ZoneList.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-zone-controls-thermostats/#zonecontrolthermostatthermalcomfort
        """

class ThermostatSetpointSingleCooling:
    def __call__(
        self, name: str, /, *, setpoint_temperature_schedule_name: str | None = ..., validate: bool = True
    ) -> None:
        """Create a new ``ThermostatSetpoint:SingleCooling`` and add it to the document.

        Used for a cooling only thermostat. The setpoint can be scheduled and varied throughout the simulation but only cooling is allowed.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-zone-controls-thermostats/#thermostatsetpointsinglecooling
        """

class AnyAirLoopHVACUnitaryHeatPumpAirToAirMultiSpeed:
    def __call__(
        self,
        name: str,
        /,
        *,
        air_inlet_node_name: str,
        air_outlet_node_name: str,
        controlling_zone_or_thermostat_location: str,
        supply_air_fan_object_type: Literal["Fan:ConstantVolume", "Fan:OnOff"],
        supply_air_fan_name: str,
        supply_air_fan_placement: Literal["BlowThrough", "DrawThrough"],
        heating_coil_object_type: Literal[
            "Coil:Heating:DX:MultiSpeed",
            "Coil:Heating:Electric:MultiStage",
            "Coil:Heating:Gas:MultiStage",
            "Coil:Heating:Steam",
            "Coil:Heating:Water",
        ],
        heating_coil_name: str,
        cooling_coil_object_type: Literal["Coil:Cooling:DX:MultiSpeed"],
        cooling_coil_name: str,
        number_of_speeds_for_heating: int,
        number_of_speeds_for_cooling: int,
        heating_speed_1_supply_air_flow_rate: float | Literal["Autosize"],
        cooling_speed_1_supply_air_flow_rate: float | Literal["Autosize"],
        cooling_speed_2_supply_air_flow_rate: float | Literal["Autosize"],
        availability_schedule_name: str | None = ...,
        supply_air_fan_operating_mode_schedule_name: str | None = ...,
        supplemental_heating_coil_object_type: Literal[
            "Coil:Heating:Electric", "Coil:Heating:Fuel", "Coil:Heating:Steam", "Coil:Heating:Water"
        ]
        | None = ...,
        supplemental_heating_coil_name: str | None = ...,
        maximum_supply_air_temperature_from_supplemental_heater: float | Literal["Autosize"] | None = ...,
        maximum_outdoor_dry_bulb_temperature_for_supplemental_heater_operation: float | None = 21,
        auxiliary_on_cycle_electric_power: float | None = 0,
        auxiliary_off_cycle_electric_power: float | None = 0,
        design_heat_recovery_water_flow_rate: float | None = 0,
        maximum_temperature_for_heat_recovery: float | None = 80,
        heat_recovery_water_inlet_node_name: str | None = ...,
        heat_recovery_water_outlet_node_name: str | None = ...,
        no_load_supply_air_flow_rate: float | Literal["Autosize"] | None = ...,
        heating_speed_2_supply_air_flow_rate: float | Literal["Autosize"] | None = ...,
        heating_speed_3_supply_air_flow_rate: float | Literal["Autosize"] | None = ...,
        heating_speed_4_supply_air_flow_rate: float | Literal["Autosize"] | None = ...,
        cooling_speed_3_supply_air_flow_rate: float | Literal["Autosize"] | None = ...,
        cooling_speed_4_supply_air_flow_rate: float | Literal["Autosize"] | None = ...,
        validate: bool = True,
    ) -> None:
        """Create a new ``AirLoopHVAC:UnitaryHeatPump:AirToAir:MultiSpeed`` and add it to the document.

        Unitary system, heating and cooling, multi-speed with constant volume supply fan (continuous or cycling), direct expansion (DX) cooling coil, heating coil (DX air-to-air heat pump, gas, electric, hot water, or steam), and supplemental heating coil (gas, electric, hot water, or steam).

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-unitary-equipment/#airloophvacunitaryheatpumpairtoairmultispeed
        """

class FaultModelTemperatureSensorOffsetChillerSupplyWater:
    def __call__(
        self,
        name: str,
        /,
        *,
        chiller_object_type: Literal[
            "Chiller:Absorption",
            "Chiller:Absorption:Indirect",
            "Chiller:CombustionTurbine",
            "Chiller:ConstantCOP",
            "Chiller:Electric",
            "Chiller:Electric:EIR",
            "Chiller:Electric:ReformulatedEIR",
            "Chiller:EngineDriven",
        ],
        chiller_object_name: str,
        availability_schedule_name: str | None = ...,
        severity_schedule_name: str | None = ...,
        reference_sensor_offset: float | None = 0,
        validate: bool = True,
    ) -> None:
        """Create a new ``FaultModel:TemperatureSensorOffset:ChillerSupplyWater`` and add it to the document.

        This object describes fault of chiller supply water temperature sensor offset

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-operational-faults/#faultmodeltemperaturesensoroffsetchillersupplywater
        """

class AnyOutputTableMonthly:
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
