"""Creation signatures of generated classes (stub only).

DO NOT EDIT — regenerate with:
    python -m idfkit.codegen.generate_stubs
"""

from __future__ import annotations

from collections.abc import Sequence
from typing import Literal

from typing_extensions import Never

from .. import _generated_types as _g

class AnyMaterialPropertyHeatAndMoistureTransferDiffusion:
    def __call__(
        self,
        this_type_has_no_name_field: _g._PassFieldsAsKeywords = ...,
        /,
        *,
        material_name: str,
        number_of_data_pairs: int,
        relative_humidity_fraction_1: float,
        water_vapor_diffusion_resistance_factor_1: float,
        relative_humidity_fraction_2: float | None = ...,
        water_vapor_diffusion_resistance_factor_2: float | None = ...,
        relative_humidity_fraction_3: float | None = ...,
        water_vapor_diffusion_resistance_factor_3: float | None = ...,
        relative_humidity_fraction_4: float | None = ...,
        water_vapor_diffusion_resistance_factor_4: float | None = ...,
        relative_humidity_fraction_5: float | None = ...,
        water_vapor_diffusion_resistance_factor_5: float | None = ...,
        relative_humidity_fraction_6: float | None = ...,
        water_vapor_diffusion_resistance_factor_6: float | None = ...,
        relative_humidity_fraction_7: float | None = ...,
        water_vapor_diffusion_resistance_factor_7: float | None = ...,
        relative_humidity_fraction_8: float | None = ...,
        water_vapor_diffusion_resistance_factor_8: float | None = ...,
        relative_humidity_fraction_9: float | None = ...,
        water_vapor_diffusion_resistance_factor_9: float | None = ...,
        relative_humidity_fraction_10: float | None = ...,
        water_vapor_diffusion_resistance_factor_10: float | None = ...,
        relative_humidity_fraction_11: float | None = ...,
        water_vapor_diffusion_resistance_factor_11: float | None = ...,
        relative_humidity_fraction_12: float | None = ...,
        water_vapor_diffusion_resistance_factor_12: float | None = ...,
        relative_humidity_fraction_13: float | None = ...,
        water_vapor_diffusion_resistance_factor_13: float | None = ...,
        relative_humidity_fraction_14: float | None = ...,
        water_vapor_diffusion_resistance_factor_14: float | None = ...,
        relative_humidity_fraction_15: float | None = ...,
        water_vapor_diffusion_resistance_factor_15: float | None = ...,
        relative_humidity_fraction_16: float | None = ...,
        water_vapor_diffusion_resistance_factor_16: float | None = ...,
        relative_humidity_fraction_17: float | None = ...,
        water_vapor_diffusion_resistance_factor_17: float | None = ...,
        relative_humidity_fraction_18: float | None = ...,
        water_vapor_diffusion_resistance_factor_18: float | None = ...,
        relative_humidity_fraction_19: float | None = ...,
        water_vapor_diffusion_resistance_factor_19: float | None = ...,
        relative_humidity_fraction_20: float | None = ...,
        water_vapor_diffusion_resistance_factor_20: float | None = ...,
        relative_humidity_fraction_21: float | None = ...,
        water_vapor_diffusion_resistance_factor_21: float | None = ...,
        relative_humidity_fraction_22: float | None = ...,
        water_vapor_diffusion_resistance_factor_22: float | None = ...,
        relative_humidity_fraction_23: float | None = ...,
        water_vapor_diffusion_resistance_factor_23: float | None = ...,
        relative_humidity_fraction_24: float | None = ...,
        water_vapor_diffusion_resistance_factor_24: float | None = ...,
        relative_humidity_fraction_25: float | None = ...,
        water_vapor_diffusion_resistance_factor_25: float | None = ...,
        validate: bool = True,
    ) -> None:
        """Create a new ``MaterialProperty:HeatAndMoistureTransfer:Diffusion`` and add it to the document.

        HeatBalanceAlgorithm = CombinedHeatAndMoistureFiniteElement solution algorithm only. Relationship between water vapor diffusion and relative humidity fraction Has no effect with other HeatBalanceAlgorithm solution algorithms

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-surface-construction-elements/#materialpropertyheatandmoisturetransferdiffusion
        """

class WindowPropertyAirflowControl:
    def __call__(
        self,
        name: str,
        /,
        *,
        airflow_source: Literal["IndoorAir", "OutdoorAir"] | None = "IndoorAir",
        airflow_destination: Literal["IndoorAir", "OutdoorAir", "ReturnAir"] | None = "OutdoorAir",
        maximum_flow_rate: float | None = 0,
        airflow_control_type: Literal["AlwaysOff", "AlwaysOnAtMaximumFlow", "ScheduledOnly"]
        | None = "AlwaysOnAtMaximumFlow",
        airflow_is_scheduled: Literal["No", "Yes"] | None = "No",
        airflow_multiplier_schedule_name: str | None = ...,
        airflow_return_air_node_name: str | None = ...,
        validate: bool = True,
    ) -> None:
        """Create a new ``WindowProperty:AirflowControl`` and add it to the document.

        Used to control forced airflow through a gap between glass layers

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-thermal-zone-description-geometry/#windowpropertyairflowcontrol
        """

class ShadingOverhang:
    def __call__(
        self,
        name: str,
        /,
        *,
        window_or_door_name: str,
        height_above_window_or_door: float | None = ...,
        tilt_angle_from_window_door: float | None = 90,
        left_extension_from_window_door_width: float | None = ...,
        right_extension_from_window_door_width: float | None = ...,
        depth: float | None = ...,
        validate: bool = True,
    ) -> None:
        """Create a new ``Shading:Overhang`` and add it to the document.

        Overhangs are usually flat shading surfaces that reference a window or door.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-thermal-zone-description-geometry/#shadingoverhang
        """

class AnyZoneBaseboardOutdoorTemperatureControlled:
    def __call__(
        self,
        name: str,
        /,
        *,
        narrow_with_as_version_first: Never,
        schedule_name: str,
        capacity_at_low_temperature: float,
        low_temperature: float,
        capacity_at_high_temperature: float,
        high_temperature: float,
        fraction_radiant: float | None = 0,
        end_use_subcategory: str | None = "General",
        validate: bool = True,
    ) -> None:
        """Create a new ``ZoneBaseboard:OutdoorTemperatureControlled`` and add it to the document.

        Specifies outside temperature-controlled electric baseboard heating. If a ZoneList, SpaceList, or a Zone comprised of more than one Space is specified then this definition applies to all applicable spaces, and each instance will be named with the Space Name plus this Object Name.

        No call suits every release: narrow the document with ``as_version`` first.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-internal-gains-people-lights-other/#zonebaseboardoutdoortemperaturecontrolled
        """

class SetpointManagerScheduledDualSetpoint:
    def __call__(
        self,
        name: str,
        /,
        *,
        high_setpoint_schedule_name: str,
        low_setpoint_schedule_name: str,
        setpoint_node_or_nodelist_name: str,
        control_variable: Literal["Temperature"] | None = "Temperature",
        validate: bool = True,
    ) -> None:
        """Create a new ``SetpointManager:Scheduled:DualSetpoint`` and add it to the document.

        This setpoint manager places a high and low schedule value on one or more nodes.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-setpoint-managers/#setpointmanagerscheduleddualsetpoint
        """

class RefrigerationTranscriticalSystem:
    def __call__(
        self,
        name: str,
        /,
        *,
        system_type: Literal["SingleStage", "TwoStage"],
        medium_temperature_refrigerated_case_or_walkin_or_caseandwalkinlist_name: str,
        refrigeration_gas_cooler_name: str,
        high_pressure_compressor_or_compressorlist_name: str,
        refrigeration_system_working_fluid_type: str,
        low_temperature_refrigerated_case_or_walkin_or_caseandwalkinlist_name: str | None = ...,
        low_pressure_compressor_or_compressorlist_name: str | None = ...,
        receiver_pressure: float | None = 4000000,
        subcooler_effectiveness: float | None = 0.4,
        sum_ua_suction_piping_for_medium_temperature_loads: float | None = 0,
        medium_temperature_suction_piping_zone_name: str | None = ...,
        sum_ua_suction_piping_for_low_temperature_loads: float | None = 0,
        low_temperature_suction_piping_zone_name: str | None = ...,
        end_use_subcategory: str | None = "General",
        validate: bool = True,
    ) -> None:
        """Create a new ``Refrigeration:TranscriticalSystem`` and add it to the document.

        Detailed transcritical carbon dioxide (CO2) booster refrigeration systems used in supermarkets. The object allows for modeling either a single stage system with medium-temperature loads or a two stage system with both medium- and low-temperature loads.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-refrigeration/#refrigerationtranscriticalsystem
        """

class AnyRefrigerationSecondarySystem:
    def __call__(
        self,
        name: str,
        /,
        *,
        refrigerated_case_or_walkin_or_caseandwalkinlist_name: str,
        circulating_fluid_type: Literal["FluidAlwaysLiquid", "FluidPhaseChange"],
        circulating_fluid_name: str,
        evaporator_evaporating_temperature: float,
        evaporator_approach_temperature_difference: float,
        evaporator_capacity: float | None = ...,
        evaporator_flow_rate_for_secondary_fluid: float | None = ...,
        evaporator_range_temperature_difference: float | None = ...,
        number_of_pumps_in_loop: int | None = 1,
        total_pump_flow_rate: float | None = ...,
        total_pump_power: float | None = ...,
        total_pump_head: float | None = ...,
        phasechange_circulating_rate: float | None = 2.5,
        pump_drive_type: Literal["Constant", "Variable"] | None = "Constant",
        variable_speed_pump_cubic_curve_name: str | None = ...,
        pump_motor_heat_to_fluid: float | None = 0.85,
        sum_ua_distribution_piping: float | None = 0,
        distribution_piping_zone_name: str | None = ...,
        sum_ua_receiver_separator_shell: float | None = 0,
        receiver_separator_zone_name: str | None = ...,
        evaporator_refrigerant_inventory: float | None = 0,
        end_use_subcategory: str | None = "General",
        validate: bool = True,
    ) -> None:
        """Create a new ``Refrigeration:SecondarySystem`` and add it to the document.

        Works in conjunction with refrigerated cases and walkins to simulate the performance of a secondary loop supermarket refrigeration system. Heat from the refrigeration loads served by the secondary loop is absorbed by a primary refrigeration system (Refrigeration:System). The SecondarySystem object simulates a heat exchanger that is an evaporator, or refrigeration load, on the primary refrigeration system.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-refrigeration/#refrigerationsecondarysystem
        """

class DemandManagerLights:
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
        lights: Sequence[_g.DemandManagerLightsLightsItem | _g.DemandManagerLightsLightsGroup] = ...,
        validate: bool = True,
    ) -> None:
        """Create a new ``DemandManager:Lights`` and add it to the document.

        used for demand limiting Lights objects.

        ``lights`` takes the extensible groups in order, one dict per group:

        ```python
        doc["DemandManager:Lights"].add(
            "DemandManager Lights 1",
            limit_control="Fixed",
            selection_control="All",
            lights=[
                {"lights_name": "Lights 1"},
                {"lights_name": "Lights 2"},
            ],
        )
        ```

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-demand-limiting-controls/#demandmanagerlights
        """

class UtilityCostComputation:
    def __call__(
        self,
        name: str,
        /,
        *,
        tariff_name: str,
        compute_step_1: str | None = ...,
        compute_step_2: str | None = ...,
        compute_step_3: str | None = ...,
        compute_step_4: str | None = ...,
        compute_step_5: str | None = ...,
        compute_step_6: str | None = ...,
        compute_step_7: str | None = ...,
        compute_step_8: str | None = ...,
        compute_step_9: str | None = ...,
        compute_step_10: str | None = ...,
        compute_step_11: str | None = ...,
        compute_step_12: str | None = ...,
        compute_step_13: str | None = ...,
        compute_step_14: str | None = ...,
        compute_step_15: str | None = ...,
        compute_step_16: str | None = ...,
        compute_step_17: str | None = ...,
        compute_step_18: str | None = ...,
        compute_step_19: str | None = ...,
        compute_step_20: str | None = ...,
        compute_step_21: str | None = ...,
        compute_step_22: str | None = ...,
        compute_step_23: str | None = ...,
        compute_step_24: str | None = ...,
        compute_step_25: str | None = ...,
        compute_step_26: str | None = ...,
        compute_step_27: str | None = ...,
        compute_step_28: str | None = ...,
        compute_step_29: str | None = ...,
        compute_step_30: str | None = ...,
        validate: bool = True,
    ) -> None:
        """Create a new ``UtilityCost:Computation`` and add it to the document.

        The object lists a series of computations that are used to perform the utility bill calculation. The object is only used for complex tariffs that cannot be modeled any other way. For most utility tariffs, UtilityCost:Computation is unnecessary and should be avoided. If UtilityCost:Computation is used, it must contain references to all objects involved in the rate in the order that they should be computed.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/energyplus-economics/utilitycost-computation/#utilitycostcomputation
        """

class PythonPluginSearchPaths:
    def __call__(
        self,
        name: str,
        /,
        *,
        add_current_working_directory_to_search_path: Literal["No", "Yes"] | None = "Yes",
        add_input_file_directory_to_search_path: Literal["No", "Yes"] | None = "Yes",
        add_epin_environment_variable_to_search_path: Literal["No", "Yes"] | None = "Yes",
        py_search_paths: Sequence[
            _g.PythonPluginSearchPathsPySearchPathsItem | _g.PythonPluginSearchPathsPySearchPathsGroup
        ] = ...,
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
