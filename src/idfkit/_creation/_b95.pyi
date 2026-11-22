"""Creation signatures of generated classes (stub only).

DO NOT EDIT — regenerate with:
    python -m idfkit.codegen.generate_stubs
"""

from __future__ import annotations

from collections.abc import Sequence
from typing import Literal

from .. import _generated_types as _g

class Version:
    def __call__(
        self,
        this_type_has_no_name_field: _g._PassFieldsAsKeywords = ...,
        /,
        *,
        version_identifier: str | None = ...,
        validate: bool = True,
    ) -> None:
        """Create a new ``Version`` and add it to the document.

        Specifies the EnergyPlus version of the IDF file.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-simulation-parameters/#version
        """

class HVACSystemRootFindingAlgorithm:
    def __call__(
        self,
        this_type_has_no_name_field: _g._PassFieldsAsKeywords = ...,
        /,
        *,
        algorithm: Literal[
            "Alternation", "Bisection", "BisectionThenRegulaFalsi", "RegulaFalsi", "RegulaFalsiThenBisection"
        ]
        | None = "RegulaFalsi",
        number_of_iterations_before_algorithm_switch: int | None = 5,
        validate: bool = True,
    ) -> None:
        """Create a new ``HVACSystemRootFindingAlgorithm`` and add it to the document.

        Specifies a HVAC system solver algorithm to find a root

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-simulation-parameters/#hvacsystemrootfindingalgorithm
        """

class AnyRoomAirTemperaturePatternConstantGradient:
    def __call__(
        self,
        this_type_has_no_name_field: _g._PassFieldsAsKeywords = ...,
        /,
        *,
        room_air_temperature_pattern_constant_gradient_name: str,
        control_integer_for_pattern_control_schedule_name: int,
        thermostat_offset: float | None = ...,
        return_air_offset: float | None = ...,
        exhaust_air_offset: float | None = ...,
        temperature_gradient: float | None = ...,
        validate: bool = True,
    ) -> None:
        """Create a new ``RoomAir:TemperaturePattern:ConstantGradient`` and add it to the document.

        Used to model room air with a fixed temperature gradient in the vertical direction. Used in combination with RoomAir:TemperaturePattern:UserDefined.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-room-air-models/#roomairtemperaturepatternconstantgradient
        """

class AirTerminalSingleDuctVAVNoReheat:
    def __call__(
        self,
        name: str,
        /,
        *,
        air_outlet_node_name: str,
        air_inlet_node_name: str,
        maximum_air_flow_rate: float | Literal["Autosize"],
        availability_schedule_name: str | None = ...,
        zone_minimum_air_flow_input_method: Literal["Constant", "FixedFlowRate", "Scheduled"] | None = "Constant",
        constant_minimum_air_flow_fraction: float | Literal["Autosize"] | None = "Autosize",
        fixed_minimum_air_flow_rate: float | Literal["Autosize"] | None = "Autosize",
        minimum_air_flow_fraction_schedule_name: str | None = ...,
        design_specification_outdoor_air_object_name: str | None = ...,
        minimum_air_flow_turndown_schedule_name: str | None = ...,
        validate: bool = True,
    ) -> None:
        """Create a new ``AirTerminal:SingleDuct:VAV:NoReheat`` and add it to the document.

        Central air system terminal unit, single duct, variable volume, with no reheat coil.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-zone-hvac-air-loop-terminal-units/#airterminalsingleductvavnoreheat
        """

class AnyHeatExchangerAirToAirSensibleAndLatent:
    def __call__(
        self,
        name: str,
        /,
        *,
        nominal_supply_air_flow_rate: float | Literal["Autosize"],
        supply_air_inlet_node_name: str,
        supply_air_outlet_node_name: str,
        exhaust_air_inlet_node_name: str,
        exhaust_air_outlet_node_name: str,
        availability_schedule_name: str | None = ...,
        sensible_effectiveness_at_100_heating_air_flow: float | None = 0,
        latent_effectiveness_at_100_heating_air_flow: float | None = 0,
        sensible_effectiveness_at_100_cooling_air_flow: float | None = 0,
        latent_effectiveness_at_100_cooling_air_flow: float | None = 0,
        nominal_electric_power: float | None = 0,
        supply_air_outlet_temperature_control: Literal["No", "Yes"] | None = "No",
        heat_exchanger_type: Literal["Plate", "Rotary"] | None = "Plate",
        frost_control_type: Literal["ExhaustAirRecirculation", "ExhaustOnly", "MinimumExhaustTemperature", "None"]
        | None = "None",
        threshold_temperature: float | None = 1.7,
        initial_defrost_time_fraction: float | None = 0.083,
        rate_of_defrost_time_fraction_increase: float | None = 0.012,
        economizer_lockout: Literal["No", "Yes"] | None = "Yes",
        validate: bool = True,
    ) -> None:
        """Create a new ``HeatExchanger:AirToAir:SensibleAndLatent`` and add it to the document.

        This object models an air-to-air heat exchanger using effectiveness relationships. The heat exchanger can transfer sensible energy, latent energy, or both between the supply (primary) and exhaust (secondary) air streams.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-heat-recovery/#heatexchangerairtoairsensibleandlatent
        """

class AnyAirLoopHVACDedicatedOutdoorAirSystem:
    def __call__(
        self,
        name: str,
        /,
        *,
        airloophvac_mixer_name: str,
        airloophvac_splitter_name: str,
        preheat_design_temperature: float,
        preheat_design_humidity_ratio: float,
        precool_design_temperature: float,
        precool_design_humidity_ratio: float,
        number_of_airloophvac: int,
        airloophvac_outdoorairsystem_name: str | None = ...,
        availability_schedule_name: str | None = ...,
        airloophvacs: Sequence[
            _g.AirLoopHVACDedicatedOutdoorAirSystemAirloophvacsItem
            | _g.AirLoopHVACDedicatedOutdoorAirSystemAirloophvacsGroup
        ] = ...,
        validate: bool = True,
    ) -> None:
        """Create a new ``AirLoopHVAC:DedicatedOutdoorAirSystem`` and add it to the document.

        Defines a central forced air system to provide dedicated outdoor air to multiple AirLoopHVACs.

        ``airloophvacs`` takes the extensible groups in order, one dict per group:

        ```python
        doc["AirLoopHVAC:DedicatedOutdoorAirSystem"].add(
            "AirLoopHVAC DedicatedOutdoorAirSystem 1",
            airloophvac_mixer_name="AirLoopHVAC:Mixer 1",
            airloophvac_splitter_name="AirLoopHVAC:Splitter 1",
            preheat_design_temperature=0.0,
            preheat_design_humidity_ratio=0.0,
            precool_design_temperature=0.0,
            precool_design_humidity_ratio=0.0,
            number_of_airloophvac=0,
            airloophvacs=[
                {"airloophvac_name": "AirLoopHVAC 1"},
                {"airloophvac_name": "AirLoopHVAC 2"},
            ],
        )
        ```

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-air-path/#airloophvacdedicatedoutdoorairsystem
        """

class ChillerElectricEIR:
    def __call__(
        self,
        name: str,
        /,
        *,
        reference_capacity: float | Literal["Autosize"],
        reference_cop: float,
        cooling_capacity_function_of_temperature_curve_name: str,
        electric_input_to_cooling_output_ratio_function_of_temperature_curve_name: str,
        electric_input_to_cooling_output_ratio_function_of_part_load_ratio_curve_name: str,
        chilled_water_inlet_node_name: str,
        chilled_water_outlet_node_name: str,
        reference_leaving_chilled_water_temperature: float | None = 6.67,
        reference_entering_condenser_fluid_temperature: float | None = 29.4,
        reference_chilled_water_flow_rate: float | Literal["Autosize"] | None = ...,
        reference_condenser_fluid_flow_rate: float | Literal["Autosize"] | None = ...,
        minimum_part_load_ratio: float | None = 0.1,
        maximum_part_load_ratio: float | None = 1,
        optimum_part_load_ratio: float | None = 1,
        minimum_unloading_ratio: float | None = 0.2,
        condenser_inlet_node_name: str | None = ...,
        condenser_outlet_node_name: str | None = ...,
        condenser_type: Literal["AirCooled", "EvaporativelyCooled", "WaterCooled"] | None = "WaterCooled",
        condenser_fan_power_ratio: float | None = 0,
        fraction_of_compressor_electric_consumption_rejected_by_condenser: float | None = 1,
        leaving_chilled_water_lower_temperature_limit: float | None = 2,
        chiller_flow_mode: Literal["ConstantFlow", "LeavingSetpointModulated", "NotModulated"] | None = "NotModulated",
        design_heat_recovery_water_flow_rate: float | Literal["Autosize"] | None = 0,
        heat_recovery_inlet_node_name: str | None = ...,
        heat_recovery_outlet_node_name: str | None = ...,
        sizing_factor: float | None = 1,
        basin_heater_capacity: float | None = 0,
        basin_heater_setpoint_temperature: float | None = 2,
        basin_heater_operating_schedule_name: str | None = ...,
        condenser_heat_recovery_relative_capacity_fraction: float | None = ...,
        heat_recovery_inlet_high_temperature_limit_schedule_name: str | None = ...,
        heat_recovery_leaving_temperature_setpoint_node_name: str | None = ...,
        end_use_subcategory: str | None = "General",
        condenser_flow_control: Literal[
            "ConstantFlow", "ModulatedChillerPLR", "ModulatedDeltaTemperature", "ModulatedLoopPLR"
        ]
        | None = "ConstantFlow",
        condenser_loop_flow_rate_fraction_function_of_loop_part_load_ratio_curve_name: str | None = ...,
        temperature_difference_across_condenser_schedule_name: str | None = ...,
        condenser_minimum_flow_fraction: float | None = ...,
        thermosiphon_capacity_fraction_curve_name: str | None = ...,
        thermosiphon_minimum_temperature_difference: float | None = 0,
        validate: bool = True,
    ) -> None:
        """Create a new ``Chiller:Electric:EIR`` and add it to the document.

        This chiller model is the empirical model from the DOE-2 building Energy simulation program. Chiller performance at off-reference conditions is modeled using three polynomial equations. Three curves objects are required.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-plant-equipment/#chillerelectriceir
        """

class AnyDemandManagerExteriorLights:
    def __call__(
        self,
        name: str,
        /,
        *,
        limit_control: Literal["Fixed", "Off"],
        selection_control: Literal["All", "RotateMany", "RotateOne"],
        availability_schedule_name: str | None = ...,
        minimum_limit_duration: int | None = ...,
        maximum_limit_fraction: float | None = ...,
        limit_step_change: float | None = ...,
        rotation_duration: int | None = ...,
        lights: Sequence[_g.DemandManagerExteriorLightsLightsItem | _g.DemandManagerExteriorLightsLightsGroup] = ...,
        validate: bool = True,
    ) -> None:
        """Create a new ``DemandManager:ExteriorLights`` and add it to the document.

        used for demand limiting Exterior:Lights objects.

        ``lights`` takes the extensible groups in order, one dict per group:

        ```python
        doc["DemandManager:ExteriorLights"].add(
            "DemandManager ExteriorLights 1",
            limit_control="Fixed",
            selection_control="All",
            lights=[
                {"exterior_lights_name": "Exterior Lights 1"},
                {"exterior_lights_name": "Exterior Lights 2"},
            ],
        )
        ```

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-demand-limiting-controls/#demandmanagerexteriorlights
        """

class ElectricLoadCenterInverterFunctionOfPower:
    def __call__(
        self,
        name: str = "",
        /,
        *,
        availability_schedule_name: str | None = ...,
        zone_name: str | None = ...,
        radiative_fraction: float | None = ...,
        efficiency_function_of_power_curve_name: str | None = ...,
        rated_maximum_continuous_input_power: float | None = ...,
        minimum_efficiency: float | None = ...,
        maximum_efficiency: float | None = ...,
        minimum_power_output: float | None = ...,
        maximum_power_output: float | None = ...,
        ancillary_power_consumed_in_standby: float | None = ...,
        validate: bool = True,
    ) -> None:
        """Create a new ``ElectricLoadCenter:Inverter:FunctionOfPower`` and add it to the document.

        Electric power inverter to convert from direct current (DC) to alternating current (AC) in an electric load center that contains photovoltaic modules. This input object is for an inverter model where efficiency is a function of normalized power.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-electric-load-center-generator/#electricloadcenterinverterfunctionofpower
        """
