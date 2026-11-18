"""Creation signatures of generated classes (stub only).

DO NOT EDIT — regenerate with:
    python -m idfkit.codegen.generate_stubs
"""

from __future__ import annotations

from collections.abc import Sequence
from typing import Literal

from .. import _generated_types as _g

class AvailabilityManagerOptimumStart_v8_9_to_v22_1:
    def __call__(
        self,
        name: str,
        /,
        *,
        applicability_schedule_name: str,
        fan_schedule_name: str,
        control_type: Literal["ControlZone", "MaximumofZoneList", "StayOff"] | None = "ControlZone",
        control_zone_name: str | None = ...,
        zone_list_name: str | None = ...,
        maximum_value_for_optimum_start_time: float | None = 6,
        control_algorithm: Literal[
            "AdaptiveASHRAE", "AdaptiveTemperatureGradient", "ConstantStartTime", "ConstantTemperatureGradient"
        ]
        | None = "AdaptiveASHRAE",
        constant_temperature_gradient_during_cooling: float | None = ...,
        constant_temperature_gradient_during_heating: float | None = ...,
        initial_temperature_gradient_during_cooling: float | None = ...,
        initial_temperature_gradient_during_heating: float | None = ...,
        constant_start_time: float | None = ...,
        number_of_previous_days: float | None = 2,
        validate: bool = True,
    ) -> None:
        """Create a new ``AvailabilityManager:OptimumStart`` and add it to the document.

        Determines the optimal start of HVAC systems before occupancy.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v22.1/io-reference/overview/group-system-availability-managers/#availabilitymanageroptimumstart
        """

class FloorGroundContact_v8_9_to_v9_5:
    def __call__(
        self,
        name: str,
        /,
        *,
        construction_name: str,
        zone_name: str,
        azimuth_angle: float | None = ...,
        tilt_angle: float | None = 180,
        starting_x_coordinate: float | None = ...,
        starting_y_coordinate: float | None = ...,
        starting_z_coordinate: float | None = ...,
        length: float | None = ...,
        width: float | None = ...,
        validate: bool = True,
    ) -> None:
        """Create a new ``Floor:GroundContact`` and add it to the document.

        Allows for simplified entry of exterior floors with ground contact. View Factors to Ground is automatically calculated.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v9.5/io-reference/overview/group-thermal-zone-description-geometry/#floorgroundcontact
        """

class PumpConstantSpeed_v8_9_to_v9_0:
    def __call__(
        self,
        name: str,
        /,
        *,
        inlet_node_name: str,
        outlet_node_name: str,
        design_flow_rate: float | Literal["Autosize"] | None = ...,
        design_pump_head: float | None = 179352,
        design_power_consumption: float | Literal["Autosize"] | None = ...,
        motor_efficiency: float | None = 0.9,
        fraction_of_motor_inefficiencies_to_fluid_stream: float | None = 0,
        pump_control_type: Literal["Continuous", "Intermittent"] | None = "Continuous",
        pump_flow_rate_schedule_name: str | None = ...,
        pump_curve_name: str | None = ...,
        impeller_diameter: float | None = ...,
        rotational_speed: float | None = ...,
        zone_name: str | None = ...,
        skin_loss_radiative_fraction: float | None = ...,
        design_power_sizing_method: Literal["PowerPerFlow", "PowerPerFlowPerPressure"]
        | None = "PowerPerFlowPerPressure",
        design_electric_power_per_unit_flow_rate: float | None = 348701.1,
        design_shaft_power_per_unit_flow_rate_per_unit_head: float | None = 1.282051282,
        validate: bool = True,
    ) -> None:
        """Create a new ``Pump:ConstantSpeed`` and add it to the document.

        This pump model is described in the ASHRAE secondary HVAC toolkit.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v9.0/io-reference/overview/group-pumps/#pumpconstantspeed
        """

class UtilityCostVariable_v8_9_to_v9_4:
    def __call__(
        self,
        name: str,
        /,
        *,
        tariff_name: str,
        variable_type: Literal["Currency", "Dimensionless", "Energy", "Power"] | None = "Dimensionless",
        january_value: float | None = ...,
        february_value: float | None = ...,
        march_value: float | None = ...,
        april_value: float | None = ...,
        may_value: float | None = ...,
        june_value: float | None = ...,
        july_value: float | None = ...,
        august_value: float | None = ...,
        september_value: float | None = ...,
        october_value: float | None = ...,
        november_value: float | None = ...,
        december_value: float | None = ...,
        validate: bool = True,
    ) -> None:
        """Create a new ``UtilityCost:Variable`` and add it to the document.

        Allows for the direct entry of monthly values into a utility tariff variable.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v9.4/io-reference/energyplus-economics/utilitycost-variable/#utilitycostvariable
        """

class DemandManagerThermostats_v8_9_to_v22_1:
    def __call__(
        self,
        name: str,
        /,
        *,
        reset_control: Literal["Fixed", "Off"],
        maximum_heating_setpoint_reset: float,
        maximum_cooling_setpoint_reset: float,
        selection_control: Literal["All", "RotateMany", "RotateOne"],
        availability_schedule_name: str | None = ...,
        minimum_reset_duration: float | None = ...,
        reset_step_change: float | None = ...,
        rotation_duration: float | None = ...,
        thermostats: Sequence[
            _g.DemandManagerThermostatsThermostatsItem | _g.DemandManagerThermostatsThermostatsGroup
        ] = ...,
        validate: bool = True,
    ) -> None:
        """Create a new ``DemandManager:Thermostats`` and add it to the document.

        used for demand limiting ZoneControl:Thermostat objects.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v22.1/io-reference/overview/group-demand-limiting-controls/#demandmanagerthermostats
        """

class CoilWaterHeatingAirToWaterHeatPumpWrapped_v23_2_to_v25_1:
    def __call__(
        self,
        name: str,
        /,
        *,
        rated_heating_capacity: float,
        evaporator_air_inlet_node_name: str,
        evaporator_air_outlet_node_name: str,
        rated_cop: float | None = 3.2,
        rated_sensible_heat_ratio: float | None = 0.85,
        rated_evaporator_inlet_air_dry_bulb_temperature: float | None = 19.7,
        rated_evaporator_inlet_air_wet_bulb_temperature: float | None = 13.5,
        rated_condenser_water_temperature: float | None = 57.5,
        rated_evaporator_air_flow_rate: float | Literal["Autocalculate"] | None = ...,
        evaporator_fan_power_included_in_rated_cop: Literal["No", "Yes"] | None = "Yes",
        crankcase_heater_capacity: float | None = 0,
        crankcase_heater_capacity_function_of_temperature_curve_name: str | None = ...,
        maximum_ambient_temperature_for_crankcase_heater_operation: float | None = 10,
        evaporator_air_temperature_type_for_curve_objects: Literal["DryBulbTemperature", "WetBulbTemperature"]
        | None = "WetBulbTemperature",
        heating_capacity_function_of_temperature_curve_name: str | None = ...,
        heating_capacity_function_of_air_flow_fraction_curve_name: str | None = ...,
        heating_cop_function_of_temperature_curve_name: str | None = ...,
        heating_cop_function_of_air_flow_fraction_curve_name: str | None = ...,
        part_load_fraction_correlation_curve_name: str | None = ...,
        validate: bool = True,
    ) -> None:
        """Create a new ``Coil:WaterHeating:AirToWaterHeatPump:Wrapped`` and add it to the document.

        Heat pump water heater (HPWH) heating coil, air-to-water direct-expansion (DX) system which includes a water heating coil, evaporator air coil, evaporator fan, electric compressor, and water pump. Part of a WaterHeater:HeatPump:WrappedCondenser system.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v25.1/io-reference/overview/group-heating-and-cooling-coils/#coilwaterheatingairtowaterheatpumpwrapped
        """
