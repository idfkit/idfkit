"""Creation signatures of generated classes (stub only).

DO NOT EDIT — regenerate with:
    python -m idfkit.codegen.generate_stubs
"""

from __future__ import annotations

from collections.abc import Sequence
from typing import Literal

from typing_extensions import Never

from .. import _generated_types as _g

class AnyConvergenceLimits:
    def __call__(
        self,
        this_type_has_no_name_field: _g._PassFieldsAsKeywords = ...,
        /,
        *,
        minimum_system_timestep: int | None = ...,
        maximum_hvac_iterations: int | None = 20,
        minimum_plant_iterations: int | None = 2,
        maximum_plant_iterations: int | None = 8,
    ) -> None:
        """Create a new ``ConvergenceLimits`` and add it to the document.

        Specifies limits on HVAC system simulation timesteps and iterations. This item is an advanced feature that should be used only with caution.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-simulation-parameters/#convergencelimits
        """

class SitePrecipitation:
    def __call__(
        self,
        this_type_has_no_name_field: _g._PassFieldsAsKeywords = ...,
        /,
        *,
        precipitation_model_type: Literal["ScheduleAndDesignLevel"] | None = ...,
        design_level_for_total_annual_precipitation: float | None = ...,
        precipitation_rates_schedule_name: str | None = ...,
        average_total_annual_precipitation: float | None = ...,
    ) -> None:
        """Create a new ``Site:Precipitation`` and add it to the document.

        Used to describe the amount of water precipitation at the building site. Precipitation includes both rain and the equivalent water content of snow.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-location-climate-weather-file-access/#siteprecipitation
        """

class AnyZoneCoolTowerShower:
    def __call__(
        self,
        name: str,
        /,
        *,
        narrow_with_as_version_first: Never,
        pump_flow_rate_schedule_name: str,
        maximum_water_flow_rate: float,
        effective_tower_height: float,
        airflow_outlet_area: float,
        maximum_air_flow_rate: float,
        minimum_indoor_temperature: float,
        rated_power_consumption: float,
        availability_schedule_name: str | None = ...,
        water_supply_storage_tank_name: str | None = ...,
        flow_control_type: Literal["WaterFlowSchedule", "WindDrivenFlow"] | None = "WindDrivenFlow",
        fraction_of_water_loss: float | None = ...,
        fraction_of_flow_schedule: float | None = ...,
    ) -> None:
        """Create a new ``ZoneCoolTower:Shower`` and add it to the document.

        A cooltower (sometimes referred to as a wind tower or a shower cooling tower) models passive downdraught evaporative cooling (PDEC) that is designed to capture the wind at the top of a tower and cool the outdoor air using water evaporation before delivering it to a zone (or space).

        No call suits every release: narrow the document with ``as_version`` first.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-airflow/#zonecooltowershower
        """

class AnyHVACTemplateSystemVRF:
    def __call__(
        self,
        name: str,
        /,
        *,
        system_availability_schedule_name: str | None = ...,
        gross_rated_total_cooling_capacity: float | Literal["Autosize"] | None = "Autosize",
        gross_rated_cooling_cop: float | None = 3.3,
        minimum_outdoor_temperature_in_cooling_mode: float | None = -6,
        maximum_outdoor_temperature_in_cooling_mode: float | None = 43,
        gross_rated_heating_capacity: float | Literal["Autosize"] | None = "Autosize",
        rated_heating_capacity_sizing_ratio: float | None = 1,
        gross_rated_heating_cop: float | None = 3.4,
        minimum_outdoor_temperature_in_heating_mode: float | None = -20,
        maximum_outdoor_temperature_in_heating_mode: float | None = 16,
        minimum_heat_pump_part_load_ratio: float | None = 0.15,
        zone_name_for_master_thermostat_location: str | None = ...,
        master_thermostat_priority_control_type: Literal[
            "LoadPriority", "MasterThermostatPriority", "Scheduled", "ThermostatOffsetPriority", "ZonePriority"
        ]
        | None = "MasterThermostatPriority",
        thermostat_priority_schedule_name: str | None = ...,
        heat_pump_waste_heat_recovery: Literal["No", "Yes"] | None = "No",
        equivalent_piping_length_used_for_piping_correction_factor_in_cooling_mode: float | None = 30,
        vertical_height_used_for_piping_correction_factor: float | None = 10,
        equivalent_piping_length_used_for_piping_correction_factor_in_heating_mode: float | None = 30,
        crankcase_heater_power_per_compressor: float | None = 33,
        number_of_compressors: int | None = 2,
        ratio_of_compressor_size_to_total_compressor_capacity: float | None = 0.5,
        maximum_outdoor_dry_bulb_temperature_for_crankcase_heater: float | None = 5,
        defrost_strategy: Literal["Resistive", "ReverseCycle"] | None = "Resistive",
        defrost_control: Literal["OnDemand", "Timed"] | None = "Timed",
        defrost_time_period_fraction: float | None = 0.058333,
        resistive_defrost_heater_capacity: float | Literal["Autosize"] | None = "Autosize",
        maximum_outdoor_dry_bulb_temperature_for_defrost_operation: float | None = 5,
        condenser_type: Literal["AirCooled", "EvaporativelyCooled", "WaterCooled"] | None = "AirCooled",
        water_condenser_volume_flow_rate: float | Literal["Autosize"] | None = "Autosize",
        evaporative_condenser_effectiveness: float | None = 0.9,
        evaporative_condenser_air_flow_rate: float | Literal["Autosize"] | None = "Autosize",
        evaporative_condenser_pump_rated_power_consumption: float | Literal["Autosize"] | None = 0,
        basin_heater_capacity: float | None = 0,
        basin_heater_setpoint_temperature: float | None = 2,
        basin_heater_operating_schedule_name: str | None = ...,
        fuel_type: Literal["Diesel", "Electricity", "Gasoline", "NaturalGas", "OtherFuel1", "OtherFuel2"]
        | None = "Electricity",
        minimum_outdoor_temperature_in_heat_recovery_mode: float | None = -15,
        maximum_outdoor_temperature_in_heat_recovery_mode: float | None = 45,
    ) -> None:
        """Create a new ``HVACTemplate:System:VRF`` and add it to the document.

        Variable refrigerant flow (VRF) heat pump condensing unit. Serves one or more VRF zone terminal units (HVACTemplate:Zone:VRF).

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/hvac-template-objects/group-hvac-templates/#hvactemplatesystemvrf
        """

class OutputControlSizingStyle:
    def __call__(
        self,
        this_type_has_no_name_field: _g._PassFieldsAsKeywords = ...,
        /,
        *,
        column_separator: Literal["Comma", "Fixed", "Tab"],
    ) -> None:
        """Create a new ``OutputControl:Sizing:Style`` and add it to the document.

        Default style for the Sizing output files is comma -- this works well for importing into spreadsheet programs such as Excel(tm) but not so well for word processing programs -- there tab may be a better choice. Fixed puts spaces between the 'columns'

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-design-objects/#outputcontrolsizingstyle
        """

class EvaporativeCoolerDirectCelDekPad:
    def __call__(
        self,
        name: str = "",
        /,
        *,
        recirculating_water_pump_power_consumption: float,
        air_inlet_node_name: str,
        air_outlet_node_name: str,
        availability_schedule_name: str | None = ...,
        direct_pad_area: float | Literal["Autosize"] | None = "Autosize",
        direct_pad_depth: float | Literal["Autosize"] | None = "Autosize",
        control_type: str | None = ...,
        water_supply_storage_tank_name: str | None = ...,
    ) -> None:
        """Create a new ``EvaporativeCooler:Direct:CelDekPad`` and add it to the document.

        Direct evaporative cooler with rigid media evaporative pad and recirculating water pump. This model has no controls other than its availability schedule.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-evaporative-coolers/#evaporativecoolerdirectceldekpad
        """

class HeatPumpWaterToWaterParameterEstimationHeating:
    def __call__(
        self,
        name: str,
        /,
        *,
        source_side_inlet_node_name: str,
        source_side_outlet_node_name: str,
        load_side_inlet_node_name: str,
        load_side_outlet_node_name: str,
        nominal_cop: float | None = ...,
        nominal_capacity: float | None = ...,
        minimum_part_load_ratio: float | None = ...,
        maximum_part_load_ratio: float | None = ...,
        optimum_part_load_ratio: float | None = ...,
        load_side_flow_rate: float | None = ...,
        source_side_flow_rate: float | None = ...,
        load_side_heat_transfer_coefficient: float | None = ...,
        source_side_heat_transfer_coefficient: float | None = ...,
        piston_displacement: float | None = ...,
        compressor_clearance_factor: float | None = ...,
        compressor_suction_and_discharge_pressure_drop: float | None = ...,
        superheating: float | None = ...,
        constant_part_of_electromechanical_power_losses: float | None = ...,
        loss_factor: float | None = ...,
        high_pressure_cut_off: float | None = 500000000,
        low_pressure_cut_off: float | None = 0,
    ) -> None:
        """Create a new ``HeatPump:WaterToWater:ParameterEstimation:Heating`` and add it to the document.

        OSU parameter estimation model

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-plant-equipment/#heatpumpwatertowaterparameterestimationheating
        """

class ElectricLoadCenterTransformer:
    def __call__(
        self,
        name: str,
        /,
        *,
        availability_schedule_name: str | None = ...,
        transformer_usage: Literal["LoadCenterPowerConditioning", "PowerInFromGrid", "PowerOutToGrid"]
        | None = "PowerInFromGrid",
        zone_name: str | None = ...,
        radiative_fraction: float | None = 0,
        rated_capacity: float | None = ...,
        phase: Literal[1, 3] | None = 3,
        conductor_material: Literal["Aluminum", "Copper"] | None = "Aluminum",
        full_load_temperature_rise: float | None = 150,
        fraction_of_eddy_current_losses: float | None = 0.1,
        performance_input_method: Literal["NominalEfficiency", "RatedLosses"] | None = "RatedLosses",
        rated_no_load_loss: float | None = ...,
        rated_load_loss: float | None = ...,
        nameplate_efficiency: float | None = 0.98,
        per_unit_load_for_nameplate_efficiency: float | None = 0.35,
        reference_temperature_for_nameplate_efficiency: float | None = 75,
        per_unit_load_for_maximum_efficiency: float | None = ...,
        consider_transformer_loss_for_utility_cost: Literal["No", "Yes"] | None = "Yes",
        meters: Sequence[
            _g.ElectricLoadCenterTransformerMetersItem | _g.ElectricLoadCenterTransformerMetersGroup
        ] = ...,
    ) -> None:
        """Create a new ``ElectricLoadCenter:Transformer`` and add it to the document.

        This object is used to model the energy losses of transformers when they are used to transfer electricity from the grid to a building (as distribution transformers) or transfer electricity from onsite generators to the grid.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-electric-load-center-generator/#electricloadcentertransformer
        """

class AnyOutputSQLite:
    def __call__(
        self,
        this_type_has_no_name_field: _g._PassFieldsAsKeywords = ...,
        /,
        *,
        option_type: Literal["Simple", "SimpleAndTabular"] | None = ...,
    ) -> None:
        """Create a new ``Output:SQLite`` and add it to the document.

        Output from EnergyPlus can be written to an SQLite format file.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/input-for-output/#outputsqlite
        """
