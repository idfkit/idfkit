"""Creation signatures of generated classes (stub only).

DO NOT EDIT — regenerate with:
    python -m idfkit.codegen.generate_stubs
"""

from __future__ import annotations

from typing import Literal

class AnyZoneControlThermostatStagedDualSetpoint:
    def __call__(
        self,
        name: str,
        /,
        *,
        zone_or_zonelist_name: str,
        number_of_heating_stages: int,
        stage_1_heating_temperature_offset: float,
        number_of_cooling_stages: int,
        stage_1_cooling_temperature_offset: float,
        heating_temperature_setpoint_schedule_name: str | None = ...,
        heating_throttling_temperature_range: float | None = 1.1,
        stage_2_heating_temperature_offset: float | None = ...,
        stage_3_heating_temperature_offset: float | None = ...,
        stage_4_heating_temperature_offset: float | None = ...,
        cooling_temperature_setpoint_base_schedule_name: str | None = ...,
        cooling_throttling_temperature_range: float | None = 1.1,
        stage_2_cooling_temperature_offset: float | None = ...,
        stage_3_cooling_temperature_offset: float | None = ...,
        stage_4_cooling_temperature_offset: float | None = ...,
        validate: bool = True,
    ) -> None:
        """Create a new ``ZoneControl:Thermostat:StagedDualSetpoint`` and add it to the document.

        Define the Thermostat StagedDualSetpoint settings for a zone or list of zones. If you use a ZoneList in the Zone or ZoneList name field then this definition applies to all the zones in the ZoneList.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-zone-controls-thermostats/#zonecontrolthermostatstageddualsetpoint
        """

class FanComponentModel:
    def __call__(
        self,
        name: str,
        /,
        *,
        air_inlet_node_name: str,
        air_outlet_node_name: str,
        fan_wheel_diameter: float,
        fan_outlet_area: float,
        maximum_fan_static_efficiency: float,
        euler_number_at_maximum_fan_static_efficiency: float,
        maximum_dimensionless_fan_airflow: float,
        belt_maximum_torque: float | Literal["Autosize"],
        motor_maximum_speed: float,
        maximum_motor_output_power: float | Literal["Autosize"],
        maximum_vfd_output_power: float | Literal["Autosize"],
        fan_pressure_rise_curve_name: str,
        duct_static_pressure_reset_curve_name: str,
        normalized_fan_static_efficiency_curve_name_non_stall_region: str,
        normalized_fan_static_efficiency_curve_name_stall_region: str,
        normalized_dimensionless_airflow_curve_name_non_stall_region: str,
        normalized_dimensionless_airflow_curve_name_stall_region: str,
        availability_schedule_name: str | None = ...,
        maximum_flow_rate: float | Literal["Autosize"] | None = ...,
        minimum_flow_rate: float | Literal["Autosize"] | None = ...,
        fan_sizing_factor: float | None = 1,
        motor_fan_pulley_ratio: float | Literal["Autosize"] | None = 1,
        belt_sizing_factor: float | None = 1,
        belt_fractional_torque_transition: float | None = 0.167,
        motor_sizing_factor: float | None = 1,
        motor_in_airstream_fraction: float | None = 1,
        vfd_efficiency_type: Literal["Power", "Speed"] | None = ...,
        vfd_sizing_factor: float | None = 1,
        maximum_belt_efficiency_curve_name: str | None = ...,
        normalized_belt_efficiency_curve_name_region_1: str | None = ...,
        normalized_belt_efficiency_curve_name_region_2: str | None = ...,
        normalized_belt_efficiency_curve_name_region_3: str | None = ...,
        maximum_motor_efficiency_curve_name: str | None = ...,
        normalized_motor_efficiency_curve_name: str | None = ...,
        vfd_efficiency_curve_name: str | None = ...,
        end_use_subcategory: str | None = "General",
        validate: bool = True,
    ) -> None:
        """Create a new ``Fan:ComponentModel`` and add it to the document.

        A detailed fan type for constant-air-volume (CAV) and variable-air-volume (VAV) systems. It includes inputs that describe the air-distribution system as well as the fan, drive belt (if used), motor, and variable-frequency-drive (if used).

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-fans/#fancomponentmodel
        """

class HeatExchangerAirToAirSensibleAndLatent:
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
        sensible_effectiveness_of_heating_air_flow_curve_name: str | None = ...,
        latent_effectiveness_of_heating_air_flow_curve_name: str | None = ...,
        sensible_effectiveness_of_cooling_air_flow_curve_name: str | None = ...,
        latent_effectiveness_of_cooling_air_flow_curve_name: str | None = ...,
        validate: bool = True,
    ) -> None:
        """Create a new ``HeatExchanger:AirToAir:SensibleAndLatent`` and add it to the document.

        This object models an air-to-air heat exchanger using effectiveness relationships. The heat exchanger can transfer sensible energy, latent energy, or both between the supply (primary) and exhaust (secondary) air streams.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-heat-recovery/#heatexchangerairtoairsensibleandlatent
        """

class GeneratorMicroCHPNonNormalizedParameters:
    def __call__(
        self,
        name: str = "",
        /,
        *,
        maximum_electric_power: float | None = ...,
        minimum_electric_power: float | None = ...,
        minimum_cooling_water_flow_rate: float | None = ...,
        maximum_cooling_water_temperature: float | None = ...,
        electrical_efficiency_curve_name: str | None = ...,
        thermal_efficiency_curve_name: str | None = ...,
        cooling_water_flow_rate_mode: Literal["InternalControl", "PlantControl"] | None = ...,
        cooling_water_flow_rate_curve_name: str | None = ...,
        air_flow_rate_curve_name: str | None = ...,
        maximum_net_electrical_power_rate_of_change: float | None = ...,
        maximum_fuel_flow_rate_of_change: float | None = ...,
        heat_exchanger_u_factor_times_area_value: float | None = ...,
        skin_loss_u_factor_times_area_value: float | None = ...,
        skin_loss_radiative_fraction: float | None = ...,
        aggregated_thermal_mass_of_energy_conversion_portion_of_generator: float | None = ...,
        aggregated_thermal_mass_of_heat_recovery_portion_of_generator: float | None = ...,
        standby_power: float | None = ...,
        warm_up_mode: Literal["NominalEngineTemperature", "TimeDelay"] | None = ...,
        warm_up_fuel_flow_rate_coefficient: float | None = ...,
        nominal_engine_operating_temperature: float | None = ...,
        warm_up_power_coefficient: float | None = ...,
        warm_up_fuel_flow_rate_limit_ratio: float | None = ...,
        warm_up_delay_time: float | None = ...,
        cool_down_power: float | None = ...,
        cool_down_delay_time: float | None = ...,
        restart_mode: Literal["MandatoryCoolDown", "OptionalCoolDown"] | None = ...,
        validate: bool = True,
    ) -> None:
        """Create a new ``Generator:MicroCHP:NonNormalizedParameters`` and add it to the document.

        This object is referenced by a Generator:MicroCHP object and provides the non-normalized parameters for the MicroCHP generator model.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-electric-load-center-generator/#generatormicrochpnonnormalizedparameters
        """

class AnyPythonPluginSearchPaths:
    def __call__(
        self,
        name: str,
        /,
        *,
        add_current_working_directory_to_search_path: Literal["No", "Yes"] | None = "Yes",
        add_input_file_directory_to_search_path: Literal["No", "Yes"] | None = "Yes",
        validate: bool = True,
    ) -> None:
        """Create a new ``PythonPlugin:SearchPaths`` and add it to the document.

        Add directories to the search path for Python plugin modules The directory containing the EnergyPlus executable file is automatically added so that the Python interpreter can find the packaged up pyenergyplus Python package. By default, the current working directory and input file directory are also added to the search path. However, this object allows modifying this behavior. With this object, searching these directories can be disabled, and users can add supplemental search paths that point to libraries of plugin scripts.

        ``py_search_paths`` takes the extensible groups in order, one dict per group:

        ```python
        doc["PythonPlugin:SearchPaths"].add(
            "PythonPlugin SearchPaths 1",
            py_search_paths=[
                {"search_path": "Search Path"},
                {"search_path": "Search Path"},
            ],
        )
        ```

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-python-plugins/#pythonpluginsearchpaths
        """
