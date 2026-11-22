"""Creation signatures of generated classes (stub only).

DO NOT EDIT — regenerate with:
    python -m idfkit.codegen.generate_stubs
"""

from __future__ import annotations

from collections.abc import Sequence
from typing import Literal

from .. import _generated_types as _g

class AnyRoomAirNodeAirflowNetworkInternalGains:
    def __call__(
        self,
        name: str = "",
        /,
        *,
        gains: Sequence[
            _g.AnyRoomAirNodeAirflowNetworkInternalGainsGainsItem
            | _g.AnyRoomAirNodeAirflowNetworkInternalGainsGainsGroup
        ] = ...,
        validate: bool = True,
    ) -> None:
        """Create a new ``RoomAir:Node:AirflowNetwork:InternalGains`` and add it to the document.

        define the internal gains that are associated with one particular RoomAir:Node

        ``gains`` takes the extensible groups in order, one dict per group:

        ```python
        doc["RoomAir:Node:AirflowNetwork:InternalGains"].add(
            "RoomAir Node AirflowNetwork InternalGains 1",
            gains=[
                {
                    "internal_gain_object_type": "AirTerminal:SingleDuct:UserDefined",
                    "internal_gain_object_name": "Internal Gain Object Name",
                    "fraction_of_gains_to_node": 0.0,
                },
                {
                    "internal_gain_object_type": "Coil:UserDefined",
                    "internal_gain_object_name": "Internal Gain Object Name",
                    "fraction_of_gains_to_node": 0.0,
                },
            ],
        )
        ```

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-room-air-models/#roomairnodeairflownetworkinternalgains
        """

class SurfaceContaminantSourceAndSinkGenericPressureDriven:
    def __call__(
        self,
        name: str,
        /,
        *,
        surface_name: str,
        generation_schedule_name: str,
        design_generation_rate_coefficient: float | None = ...,
        generation_exponent: float | None = ...,
        validate: bool = True,
    ) -> None:
        """Create a new ``SurfaceContaminantSourceAndSink:Generic:PressureDriven`` and add it to the document.

        Simulate generic contaminant source driven by the pressure difference across a surface.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-internal-gains-people-lights-other/#surfacecontaminantsourceandsinkgenericpressuredriven
        """

class ZoneInfiltrationFlowCoefficient:
    def __call__(
        self,
        name: str,
        /,
        *,
        zone_or_space_name: str,
        flow_coefficient: float,
        stack_coefficient: float,
        wind_coefficient: float,
        shelter_factor: float,
        schedule_name: str | None = ...,
        pressure_exponent: float | None = 0.67,
        validate: bool = True,
    ) -> None:
        """Create a new ``ZoneInfiltration:FlowCoefficient`` and add it to the document.

        Infiltration is specified as flow coefficient, schedule fraction, stack and wind coefficients, and is a function of temperature difference and wind speed: Infiltration=FSchedule * SQRT( (c * Cs*|(Tzone-Todb)|**n)**2 + (c* Cw*(s * WindSpd)**2n)**2 ) If a Zone comprised of more than one Space is specified then this definition applies to all applicable spaces, and each instance will be named with the Space Name plus this Object Name.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-airflow/#zoneinfiltrationflowcoefficient
        """

class AirflowNetworkIntraZoneLinkage:
    def __call__(
        self,
        name: str,
        /,
        *,
        node_1_name: str,
        node_2_name: str,
        component_name: str | None = ...,
        airflownetwork_multizone_surface_name: str | None = ...,
        validate: bool = True,
    ) -> None:
        """Create a new ``AirflowNetwork:IntraZone:Linkage`` and add it to the document.

        This object defines the connection between two nodes and a component used in the combination of RoomAir and AirflowNetwork model.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-airflow-network/#airflownetworkintrazonelinkage
        """

class HVACTemplateSystemDedicatedOutdoorAir:
    def __call__(
        self,
        name: str = "",
        /,
        *,
        system_availability_schedule_name: str | None = ...,
        air_outlet_type: Literal["DirectIntoZone"] | None = "DirectIntoZone",
        supply_fan_flow_rate: float | Literal["Autosize"] | None = "Autosize",
        supply_fan_total_efficiency: float | None = 0.7,
        supply_fan_delta_pressure: float | None = 1000,
        supply_fan_motor_efficiency: float | None = 0.9,
        supply_fan_motor_in_air_stream_fraction: float | None = 1,
        supply_fan_placement: Literal["BlowThrough", "DrawThrough"] | None = "DrawThrough",
        cooling_coil_type: Literal[
            "ChilledWater",
            "ChilledWaterDetailedFlatModel",
            "HeatExchangerAssistedChilledWater",
            "HeatExchangerAssistedDX",
            "None",
            "TwoSpeedDX",
            "TwoStageDX",
            "TwoStageHumidityControlDX",
        ]
        | None = "ChilledWater",
        cooling_coil_availability_schedule_name: str | None = ...,
        cooling_coil_setpoint_control_type: Literal["FixedSetpoint", "OutdoorAirTemperatureReset", "Scheduled"]
        | None = "FixedSetpoint",
        cooling_coil_design_setpoint: float | None = 12.8,
        cooling_coil_setpoint_schedule_name: str | None = ...,
        cooling_coil_setpoint_at_outdoor_dry_bulb_low: float | None = 15.6,
        cooling_coil_reset_outdoor_dry_bulb_low: float | None = 15.6,
        cooling_coil_setpoint_at_outdoor_dry_bulb_high: float | None = 12.8,
        cooling_coil_reset_outdoor_dry_bulb_high: float | None = 23.3,
        dx_cooling_coil_gross_rated_total_capacity: float | Literal["Autosize"] | None = "Autosize",
        dx_cooling_coil_gross_rated_sensible_heat_ratio: float | Literal["Autosize"] | None = "Autosize",
        dx_cooling_coil_gross_rated_cop: float | None = 3,
        heating_coil_type: Literal["Electric", "Gas", "HotWater", "None"] | None = "HotWater",
        heating_coil_availability_schedule_name: str | None = ...,
        heating_coil_setpoint_control_type: Literal["FixedSetpoint", "OutdoorAirTemperatureReset", "Scheduled"]
        | None = "FixedSetpoint",
        heating_coil_design_setpoint: float | None = 12.2,
        heating_coil_setpoint_schedule_name: str | None = ...,
        heating_coil_setpoint_at_outdoor_dry_bulb_low: float | None = 15,
        heating_coil_reset_outdoor_dry_bulb_low: float | None = 7.8,
        heating_coil_setpoint_at_outdoor_dry_bulb_high: float | None = 12.2,
        heating_coil_reset_outdoor_dry_bulb_high: float | None = 12.2,
        gas_heating_coil_efficiency: float | None = 0.8,
        gas_heating_coil_parasitic_electric_load: float | None = 0,
        heat_recovery_type: Literal["Enthalpy", "None", "Sensible"] | None = "None",
        heat_recovery_sensible_effectiveness: float | None = 0.7,
        heat_recovery_latent_effectiveness: float | None = 0.65,
        heat_recovery_heat_exchanger_type: Literal["Plate", "Rotary"] | None = "Plate",
        heat_recovery_frost_control_type: Literal[
            "ExhaustAirRecirculation", "ExhaustOnly", "MinimumExhaustTemperature", "None"
        ]
        | None = "None",
        dehumidification_control_type: Literal["CoolReheatDesuperheater", "CoolReheatHeatingCoil", "Multimode", "None"]
        | None = "None",
        dehumidification_setpoint: float | None = 0.00924,
        humidifier_type: Literal["ElectricSteam", "None"] | None = "None",
        humidifier_availability_schedule_name: str | None = ...,
        humidifier_rated_capacity: float | None = ...,
        humidifier_rated_electric_power: float | Literal["Autosize"] | None = "Autosize",
        humidifier_constant_setpoint: float | None = 0.003,
        dehumidification_setpoint_schedule_name: str | None = ...,
        humidifier_setpoint_schedule_name: str | None = ...,
        validate: bool = True,
    ) -> None:
        """Create a new ``HVACTemplate:System:DedicatedOutdoorAir`` and add it to the document.

        This object creates a dedicated outdoor air system that must be used with HVACTemplate:Zone:* objects for BaseboardHeat FanCoil PTAC PTHP WaterToAirHeatPump and VRF. Does not support HVACTemplate:Zone:VAV or other central multizone systems

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/hvac-template-objects/group-hvac-templates/#hvactemplatesystemdedicatedoutdoorair
        """

class ZoneControlThermostatOperativeTemperature:
    def __call__(
        self,
        this_type_has_no_name_field: _g._PassFieldsAsKeywords = ...,
        /,
        *,
        thermostat_name: str,
        radiative_fraction_input_mode: Literal["Constant", "Scheduled"],
        fixed_radiative_fraction: float | None = ...,
        radiative_fraction_schedule_name: str | None = ...,
        adaptive_comfort_model_type: Literal[
            "AdaptiveASH5580PercentUpperLine",
            "AdaptiveASH5590PercentUpperLine",
            "AdaptiveASH55CentralLine",
            "AdaptiveCEN15251CategoryIIIUpperLine",
            "AdaptiveCEN15251CategoryIIUpperLine",
            "AdaptiveCEN15251CategoryIUpperLine",
            "AdaptiveCEN15251CentralLine",
            "None",
        ]
        | None = "None",
        validate: bool = True,
    ) -> None:
        """Create a new ``ZoneControl:Thermostat:OperativeTemperature`` and add it to the document.

        This object can be used with the ZoneList option on a thermostat or with one of the zones on that list (but you won't be able to use the object list to pick only one of those zones. Thermostat names are <Zone Name> <global Thermostat name> internally.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-zone-controls-thermostats/#zonecontrolthermostatoperativetemperature
        """

class ZoneHVACEnergyRecoveryVentilatorController:
    def __call__(
        self,
        name: str,
        /,
        *,
        temperature_high_limit: float | None = ...,
        temperature_low_limit: float | None = ...,
        enthalpy_high_limit: float | None = ...,
        dewpoint_temperature_limit: float | None = ...,
        electronic_enthalpy_limit_curve_name: str | None = ...,
        exhaust_air_temperature_limit: Literal["ExhaustAirTemperatureLimit", "NoExhaustAirTemperatureLimit"]
        | None = "NoExhaustAirTemperatureLimit",
        exhaust_air_enthalpy_limit: Literal["ExhaustAirEnthalpyLimit", "NoExhaustAirEnthalpyLimit"]
        | None = "NoExhaustAirEnthalpyLimit",
        time_of_day_economizer_flow_control_schedule_name: str | None = ...,
        high_humidity_control_flag: Literal["No", "Yes"] | None = "No",
        humidistat_control_zone_name: str | None = ...,
        high_humidity_outdoor_air_flow_ratio: float | None = 1,
        control_high_indoor_humidity_based_on_outdoor_humidity_ratio: Literal["No", "Yes"] | None = "Yes",
        validate: bool = True,
    ) -> None:
        """Create a new ``ZoneHVAC:EnergyRecoveryVentilator:Controller`` and add it to the document.

        This controller is used exclusively by the ZoneHVAC:EnergyRecoveryVentilator object to allow economizer (free cooling) operation when possible.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-controllers/#zonehvacenergyrecoveryventilatorcontroller
        """

class CoilCoolingDXTwoStageWithHumidityControlMode:
    def __call__(
        self,
        name: str,
        /,
        *,
        air_inlet_node_name: str,
        air_outlet_node_name: str,
        normal_mode_stage_1_coil_performance_object_type: Literal["CoilPerformance:DX:Cooling"],
        normal_mode_stage_1_coil_performance_name: str,
        availability_schedule_name: str | None = ...,
        crankcase_heater_capacity: float | None = 0,
        crankcase_heater_capacity_function_of_temperature_curve_name: str | None = ...,
        maximum_outdoor_dry_bulb_temperature_for_crankcase_heater_operation: float | None = 10,
        number_of_capacity_stages: int | None = 1,
        number_of_enhanced_dehumidification_modes: int | None = 0,
        normal_mode_stage_1_2_coil_performance_object_type: Literal["CoilPerformance:DX:Cooling"] | None = ...,
        normal_mode_stage_1_2_coil_performance_name: str | None = ...,
        dehumidification_mode_1_stage_1_coil_performance_object_type: Literal["CoilPerformance:DX:Cooling"]
        | None = ...,
        dehumidification_mode_1_stage_1_coil_performance_name: str | None = ...,
        dehumidification_mode_1_stage_1_2_coil_performance_object_type: Literal["CoilPerformance:DX:Cooling"]
        | None = ...,
        dehumidification_mode_1_stage_1_2_coil_performance_name: str | None = ...,
        supply_water_storage_tank_name: str | None = ...,
        condensate_collection_water_storage_tank_name: str | None = ...,
        minimum_outdoor_dry_bulb_temperature_for_compressor_operation: float | None = -25,
        basin_heater_capacity: float | None = 0,
        basin_heater_setpoint_temperature: float | None = 2,
        basin_heater_operating_schedule_name: str | None = ...,
        validate: bool = True,
    ) -> None:
        """Create a new ``Coil:Cooling:DX:TwoStageWithHumidityControlMode`` and add it to the document.

        Direct expansion (DX) cooling coil and condensing unit (includes electric compressor and condenser fan), two-stage with humidity control mode (e.g. sub-cool or hot gas reheat). Optional inputs for moisture evaporation from wet coil when compressor cycles off with continuous fan operation. Requires two to four sets of performance data, see CoilPerformance:DX:Cooling. Stages are modeled as a face-split coil.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-heating-and-cooling-coils/#coilcoolingdxtwostagewithhumiditycontrolmode
        """

class PumpVariableSpeedCondensate:
    def __call__(
        self,
        name: str,
        /,
        *,
        inlet_node_name: str,
        outlet_node_name: str,
        design_steam_volume_flow_rate: float | Literal["Autosize"] | None = ...,
        design_pump_head: float | None = 179352,
        design_power_consumption: float | Literal["Autosize"] | None = ...,
        motor_efficiency: float | None = 0.9,
        fraction_of_motor_inefficiencies_to_fluid_stream: float | None = 0,
        coefficient_1_of_the_part_load_performance_curve: float | None = 0,
        coefficient_2_of_the_part_load_performance_curve: float | None = 1,
        coefficient_3_of_the_part_load_performance_curve: float | None = 0,
        coefficient_4_of_the_part_load_performance_curve: float | None = 0,
        pump_flow_rate_schedule_name: str | None = ...,
        zone_name: str | None = ...,
        skin_loss_radiative_fraction: float | None = ...,
        design_power_sizing_method: Literal["PowerPerFlow", "PowerPerFlowPerPressure"]
        | None = "PowerPerFlowPerPressure",
        design_electric_power_per_unit_flow_rate: float | None = 348701.1,
        design_shaft_power_per_unit_flow_rate_per_unit_head: float | None = 1.282051282,
        end_use_subcategory: str | None = "General",
        validate: bool = True,
    ) -> None:
        """Create a new ``Pump:VariableSpeed:Condensate`` and add it to the document.

        This pump model is described in the ASHRAE secondary HVAC toolkit. Variable Speed Condensate pump for Steam Systems

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-pumps/#pumpvariablespeedcondensate
        """

class CoolingTowerPerformanceCoolTools:
    def __call__(
        self,
        name: str,
        /,
        *,
        minimum_inlet_air_wet_bulb_temperature: float,
        maximum_inlet_air_wet_bulb_temperature: float,
        minimum_range_temperature: float,
        maximum_range_temperature: float,
        minimum_approach_temperature: float,
        maximum_approach_temperature: float,
        minimum_water_flow_rate_ratio: float,
        maximum_water_flow_rate_ratio: float,
        coefficient_1: float,
        coefficient_2: float,
        coefficient_3: float,
        coefficient_4: float,
        coefficient_5: float,
        coefficient_6: float,
        coefficient_7: float,
        coefficient_8: float,
        coefficient_9: float,
        coefficient_10: float,
        coefficient_11: float,
        coefficient_12: float,
        coefficient_13: float,
        coefficient_14: float,
        coefficient_15: float,
        coefficient_16: float,
        coefficient_17: float,
        coefficient_18: float,
        coefficient_19: float,
        coefficient_20: float,
        coefficient_21: float,
        coefficient_22: float,
        coefficient_23: float,
        coefficient_24: float,
        coefficient_25: float,
        coefficient_26: float,
        coefficient_27: float,
        coefficient_28: float,
        coefficient_29: float,
        coefficient_30: float,
        coefficient_31: float,
        coefficient_32: float,
        coefficient_33: float,
        coefficient_34: float,
        coefficient_35: float,
        validate: bool = True,
    ) -> None:
        """Create a new ``CoolingTowerPerformance:CoolTools`` and add it to the document.

        This object is used to define coefficients for the approach temperature correlation for a variable speed cooling tower when tower Model Type is specified as CoolToolsUserDefined in the object CoolingTower:VariableSpeed.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-condenser-equipment/#coolingtowerperformancecooltools
        """

class AnyCoilUserDefined:
    def __call__(
        self,
        name: str,
        /,
        *,
        model_setup_and_sizing_program_calling_manager_name: str,
        number_of_air_connections: int,
        air_connection_1_inlet_node_name: str,
        air_connection_1_outlet_node_name: str,
        overall_model_simulation_program_calling_manager_name: str | None = ...,
        air_connection_2_inlet_node_name: str | None = ...,
        air_connection_2_outlet_node_name: str | None = ...,
        plant_connection_is_used: Literal["No", "Yes"] | None = ...,
        plant_connection_inlet_node_name: str | None = ...,
        plant_connection_outlet_node_name: str | None = ...,
        supply_inlet_water_storage_tank_name: str | None = ...,
        collection_outlet_water_storage_tank_name: str | None = ...,
        ambient_zone_name: str | None = ...,
        validate: bool = True,
    ) -> None:
        """Create a new ``Coil:UserDefined`` and add it to the document.

        Defines a generic air system component for custom modeling using Energy Management System or External Interface

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-user-defined-hvac-and-plant-component/#coiluserdefined
        """
