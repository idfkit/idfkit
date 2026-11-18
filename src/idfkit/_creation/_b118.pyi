"""Creation signatures of generated classes (stub only).

DO NOT EDIT — regenerate with:
    python -m idfkit.codegen.generate_stubs
"""

from __future__ import annotations

from collections.abc import Sequence
from typing import Literal

from .. import _generated_types as _g

class ZoneControlContaminantController:
    def __call__(
        self,
        name: str,
        /,
        *,
        zone_name: str,
        carbon_dioxide_setpoint_schedule_name: str,
        carbon_dioxide_control_availability_schedule_name: str | None = ...,
        minimum_carbon_dioxide_concentration_schedule_name: str | None = ...,
        maximum_carbon_dioxide_concentration_schedule_name: str | None = ...,
        generic_contaminant_control_availability_schedule_name: str | None = ...,
        generic_contaminant_setpoint_schedule_name: str | None = ...,
    ) -> None:
        """Create a new ``ZoneControl:ContaminantController`` and add it to the document.

        Used to control a zone to a specified indoor level of CO2 or generic contaminants, or to specify minimum CO2 concentration schedule name for a zone.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-zone-controls-thermostats/#zonecontrolcontaminantcontroller
        """

class AnyZoneHVACLowTemperatureRadiantElectric:
    def __call__(
        self,
        name: str,
        /,
        *,
        heating_setpoint_temperature_schedule_name: str,
        availability_schedule_name: str | None = ...,
        zone_name: str | None = ...,
        surface_name_or_radiant_surface_group_name: str | None = ...,
        heating_design_capacity_method: Literal[
            "CapacityPerFloorArea", "FractionOfAutosizedHeatingCapacity", "HeatingDesignCapacity"
        ]
        | None = "HeatingDesignCapacity",
        heating_design_capacity: float | Literal["Autosize"] | None = "Autosize",
        heating_design_capacity_per_floor_area: float | None = ...,
        fraction_of_autosized_heating_design_capacity: float | None = 1,
        temperature_control_type: Literal[
            "MeanAirTemperature",
            "MeanRadiantTemperature",
            "OperativeTemperature",
            "OutdoorDryBulbTemperature",
            "OutdoorWetBulbTemperature",
        ]
        | None = "MeanAirTemperature",
        heating_throttling_range: float | None = 0,
    ) -> None:
        """Create a new ``ZoneHVAC:LowTemperatureRadiant:Electric`` and add it to the document.

        Electric resistance low temperature radiant system

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-radiative-convective-units/#zonehvaclowtemperatureradiantelectric
        """

class AnyAirTerminalSingleDuctVAVReheat:
    def __call__(
        self,
        name: str,
        /,
        *,
        damper_air_outlet_node_name: str,
        air_inlet_node_name: str,
        maximum_air_flow_rate: float | Literal["Autosize"],
        reheat_coil_object_type: Literal[
            "Coil:Heating:Electric", "Coil:Heating:Fuel", "Coil:Heating:Steam", "Coil:Heating:Water"
        ],
        reheat_coil_name: str,
        air_outlet_node_name: str,
        availability_schedule_name: str | None = ...,
        zone_minimum_air_flow_input_method: Literal["Constant", "FixedFlowRate", "Scheduled"] | None = "Constant",
        constant_minimum_air_flow_fraction: float | Literal["Autosize"] | None = "Autosize",
        fixed_minimum_air_flow_rate: float | Literal["Autosize"] | None = "Autosize",
        minimum_air_flow_fraction_schedule_name: str | None = ...,
        maximum_hot_water_or_steam_flow_rate: float | Literal["Autosize"] | None = ...,
        minimum_hot_water_or_steam_flow_rate: float | None = 0,
        convergence_tolerance: float | None = 0.001,
        damper_heating_action: Literal["Normal", "Reverse", "ReverseWithLimits"] | None = "ReverseWithLimits",
        maximum_flow_per_zone_floor_area_during_reheat: float | Literal["Autosize"] | None = "Autosize",
        maximum_flow_fraction_during_reheat: float | Literal["Autosize"] | None = "Autosize",
        maximum_reheat_air_temperature: float | None = ...,
        design_specification_outdoor_air_object_name: str | None = ...,
    ) -> None:
        """Create a new ``AirTerminal:SingleDuct:VAV:Reheat`` and add it to the document.

        Central air system terminal unit, single duct, variable volume, with reheat coil (hot water, electric, gas, or steam).

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-air-distribution-equipment/#airterminalsingleductvavreheat
        """

class FanVariableVolume:
    def __call__(
        self,
        name: str,
        /,
        *,
        pressure_rise: float,
        air_inlet_node_name: str,
        air_outlet_node_name: str,
        availability_schedule_name: str | None = ...,
        fan_total_efficiency: float | None = 0.7,
        maximum_flow_rate: float | Literal["Autosize"] | None = ...,
        fan_power_minimum_flow_rate_input_method: Literal["FixedFlowRate", "Fraction"] | None = "Fraction",
        fan_power_minimum_flow_fraction: float | None = 0.25,
        fan_power_minimum_air_flow_rate: float | None = ...,
        motor_efficiency: float | None = 0.9,
        motor_in_airstream_fraction: float | None = 1,
        fan_power_coefficient_1: float | None = ...,
        fan_power_coefficient_2: float | None = ...,
        fan_power_coefficient_3: float | None = ...,
        fan_power_coefficient_4: float | None = ...,
        fan_power_coefficient_5: float | None = ...,
        end_use_subcategory: str | None = "General",
    ) -> None:
        """Create a new ``Fan:VariableVolume`` and add it to the document.

        Variable air volume fan where the electric power input varies according to a performance curve as a function of flow fraction.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-fans/#fanvariablevolume
        """

class CoilHeatingGasMultiStage:
    def __call__(
        self,
        name: str,
        /,
        *,
        air_inlet_node_name: str,
        air_outlet_node_name: str,
        number_of_stages: int,
        stage_1_gas_burner_efficiency: float,
        stage_1_nominal_capacity: float | Literal["Autosize"],
        availability_schedule_name: str | None = ...,
        temperature_setpoint_node_name: str | None = ...,
        part_load_fraction_correlation_curve_name: str | None = ...,
        off_cycle_parasitic_gas_load: float | None = ...,
        stage_1_on_cycle_parasitic_electric_load: float | None = ...,
        stage_2_gas_burner_efficiency: float | None = ...,
        stage_2_nominal_capacity: float | Literal["Autosize"] | None = ...,
        stage_2_on_cycle_parasitic_electric_load: float | None = ...,
        stage_3_gas_burner_efficiency: float | None = ...,
        stage_3_nominal_capacity: float | Literal["Autosize"] | None = ...,
        stage_3_on_cycle_parasitic_electric_load: float | None = ...,
        stage_4_gas_burner_efficiency: float | None = ...,
        stage_4_nominal_capacity: float | Literal["Autosize"] | None = ...,
        stage_4_on_cycle_parasitic_electric_load: float | None = ...,
    ) -> None:
        """Create a new ``Coil:Heating:Gas:MultiStage`` and add it to the document.

        Gas heating coil, multi-stage. If the coil is located directly in an air loop branch or outdoor air equipment list, then it is controlled on leaving air temperature and the Temperature Setpoint Node Name must be specified. If the coil is contained within another component such as an air terminal unit, zone HVAC equipment, or unitary system, then the coil is controlled by the parent component and the setpoint node name is not entered.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-heating-and-cooling-coils/#coilheatinggasmultistage
        """

class ControllerWaterCoil:
    def __call__(
        self,
        name: str,
        /,
        *,
        control_variable: Literal["HumidityRatio", "Temperature", "TemperatureAndHumidityRatio"],
        actuator_variable: Literal["Flow"],
        sensor_node_name: str,
        actuator_node_name: str,
        action: Literal["Normal", "Reverse"] | None = ...,
        controller_convergence_tolerance: float | Literal["Autosize"] | None = "Autosize",
        maximum_actuated_flow: float | Literal["Autosize"] | None = ...,
        minimum_actuated_flow: float | None = ...,
    ) -> None:
        """Create a new ``Controller:WaterCoil`` and add it to the document.

        Controller for a water coil which is located directly in an air loop branch or outdoor air equipment list. Controls the coil water flow to meet the specified leaving air setpoint(s). Used with Coil:Heating:Water, Coil:Cooling:Water, Coil:Cooling:Water:DetailedGeometry, and CoilSystem:Cooling:Water:HeatexchangerAssisted.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-controllers/#controllerwatercoil
        """

class GroundHeatExchangerVerticalSizingRectangle:
    def __call__(
        self,
        name: str,
        /,
        *,
        sizingperiod_weatherfiledays_name: str,
        available_borehole_field_length: float,
        available_borehole_field_width: float,
        maximum_number_of_boreholes: float,
        design_flow_rate_per_borehole: float | None = 0.0005,
        minimum_borehole_spacing: float | None = 4,
        maximum_borehole_spacing: float | None = 6,
        minimum_borehole_vertical_length: float | None = 60,
        maximum_borehole_vertical_length: float | None = 135,
        minimum_exiting_fluid_temperature_for_sizing: float | None = 5,
        maximum_exiting_fluid_temperature_for_sizing: float | None = 35,
    ) -> None:
        """Create a new ``GroundHeatExchanger:Vertical:Sizing:Rectangle`` and add it to the document.

        Specifies parameters to be used for Ground Heat Exchanger borehole field design and sizing.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-condenser-equipment/#groundheatexchangerverticalsizingrectangle
        """

class GroundHeatExchangerPond:
    def __call__(
        self,
        name: str,
        /,
        *,
        fluid_inlet_node_name: str,
        fluid_outlet_node_name: str,
        pond_depth: float,
        pond_area: float,
        hydronic_tubing_inside_diameter: float,
        hydronic_tubing_outside_diameter: float,
        hydronic_tubing_thermal_conductivity: float,
        ground_thermal_conductivity: float,
        number_of_tubing_circuits: int,
        length_of_each_tubing_circuit: float,
    ) -> None:
        """Create a new ``GroundHeatExchanger:Pond`` and add it to the document.

        A model of a shallow pond with immersed pipe loops. Typically used in hybrid geothermal systems and included in the condenser loop. This component may also be used as a simple solar collector.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-condenser-equipment/#groundheatexchangerpond
        """

class AnyDemandManagerElectricEquipment:
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
        equipment: Sequence[
            _g.DemandManagerElectricEquipmentEquipmentItem | _g.DemandManagerElectricEquipmentEquipmentGroup
        ] = ...,
    ) -> None:
        """Create a new ``DemandManager:ElectricEquipment`` and add it to the document.

        used for demand limiting ElectricEquipment objects.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-demand-limiting-controls/#demandmanagerelectricequipment
        """

class CurveExponentialSkewNormal:
    def __call__(
        self,
        name: str,
        /,
        *,
        coefficient1_c1: float,
        coefficient2_c2: float,
        coefficient3_c3: float,
        coefficient4_c4: float,
        minimum_value_of_x: float,
        maximum_value_of_x: float,
        minimum_curve_output: float | None = ...,
        maximum_curve_output: float | None = ...,
        input_unit_type_for_x: Literal["Dimensionless"] | None = "Dimensionless",
        output_unit_type: Literal["Capacity", "Dimensionless", "Power", "Pressure", "Temperature"]
        | None = "Dimensionless",
    ) -> None:
        """Create a new ``Curve:ExponentialSkewNormal`` and add it to the document.

        Exponential-modified skew normal curve with one independent variable. Input consists of the curve name, the four coefficients, and the maximum and minimum valid independent variable values. Optional inputs for the curve minimum and maximum may be used to limit the output of the performance curve. curve = see Input Output Reference

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-performance-curves/#curveexponentialskewnormal
        """

class CurveExponentialDecay:
    def __call__(
        self,
        name: str,
        /,
        *,
        coefficient1_c1: float,
        coefficient2_c2: float,
        coefficient3_c3: float,
        minimum_value_of_x: float,
        maximum_value_of_x: float,
        minimum_curve_output: float | None = ...,
        maximum_curve_output: float | None = ...,
        input_unit_type_for_x: Literal["Dimensionless"] | None = "Dimensionless",
        output_unit_type: Literal["Capacity", "Dimensionless", "Power", "Pressure", "Temperature"]
        | None = "Dimensionless",
    ) -> None:
        """Create a new ``Curve:ExponentialDecay`` and add it to the document.

        Exponential decay curve with one independent variable. Input consists of the curve name, the three coefficients, and the maximum and minimum valid independent variable values. Optional inputs for the curve minimum and maximum may be used to limit the output of the performance curve. curve = C1+C2*exp(C3*x)

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-performance-curves/#curveexponentialdecay
        """

class FluidPropertiesGlycolConcentration:
    def __call__(
        self,
        name: str,
        /,
        *,
        glycol_type: Literal["EthyleneGlycol", "PropyleneGlycol", "UserDefinedGlycolType"],
        user_defined_glycol_name: str | None = ...,
        glycol_concentration: float | None = ...,
    ) -> None:
        """Create a new ``FluidProperties:GlycolConcentration`` and add it to the document.

        glycol and what concentration it is

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-fluid-properties/#fluidpropertiesglycolconcentration
        """
