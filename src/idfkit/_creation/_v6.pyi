"""Creation signatures of generated classes (stub only).

DO NOT EDIT — regenerate with:
    python -m idfkit.codegen.generate_stubs
"""

from __future__ import annotations

from typing import Literal

from .. import _generated_types as _g

class WindowMaterialGlazingEquivalentLayer_v8_9_to_v9_1:
    def __call__(
        self,
        name: str,
        /,
        *,
        front_side_beam_beam_solar_transmittance: float,
        back_side_beam_beam_solar_transmittance: float,
        front_side_beam_beam_solar_reflectance: float,
        back_side_beam_beam_solar_reflectance: float,
        optical_data_type: Literal["", "Spectral", "SpectralAverage"] | None = "SpectralAverage",
        window_glass_spectral_data_set_name: str | None = ...,
        front_side_beam_beam_visible_solar_transmittance: float | None = ...,
        back_side_beam_beam_visible_solar_transmittance: float | None = ...,
        front_side_beam_beam_visible_solar_reflectance: float | None = ...,
        back_side_beam_beam_visible_solar_reflectance: float | None = ...,
        front_side_beam_diffuse_solar_transmittance: float | None = 0,
        back_side_beam_diffuse_solar_transmittance: float | None = 0,
        front_side_beam_diffuse_solar_reflectance: float | None = 0,
        back_side_beam_diffuse_solar_reflectance: float | None = 0,
        front_side_beam_diffuse_visible_solar_transmittance: float | None = 0,
        back_side_beam_diffuse_visible_solar_transmittance: float | None = 0,
        front_side_beam_diffuse_visible_solar_reflectance: float | None = 0,
        back_side_beam_diffuse_visible_solar_reflectance: float | None = 0,
        diffuse_diffuse_solar_transmittance: float | Literal["", "Autocalculate"] | None = "Autocalculate",
        front_side_diffuse_diffuse_solar_reflectance: float | Literal["", "Autocalculate"] | None = "Autocalculate",
        back_side_diffuse_diffuse_solar_reflectance: float | Literal["", "Autocalculate"] | None = "Autocalculate",
        diffuse_diffuse_visible_solar_transmittance: float | Literal["", "Autocalculate"] | None = "Autocalculate",
        front_side_diffuse_diffuse_visible_solar_reflectance: float
        | Literal["", "Autocalculate"]
        | None = "Autocalculate",
        back_side_diffuse_diffuse_visible_solar_reflectance: float
        | Literal["", "Autocalculate"]
        | None = "Autocalculate",
        infrared_transmittance_applies_to_front_and_back_: float | None = 0,
        front_side_infrared_emissivity: float | None = 0.84,
        back_side_infrared_emissivity: float | None = 0.84,
        infrared_transmittance_applies_to_front_and_back: float | None = ...,
    ) -> None: ...

class ThermalStorageIceDetailed_v9_2_to_v25_1:
    def __call__(
        self,
        name: str,
        /,
        *,
        capacity: float,
        inlet_node_name: str,
        outlet_node_name: str,
        discharging_curve_variable_specifications: Literal[
            "FractionChargedLMTD", "FractionDischargedLMTD", "LMTDFractionCharged", "LMTDMassFlow"
        ],
        discharging_curve_name: str,
        charging_curve_variable_specifications: Literal[
            "FractionChargedLMTD", "FractionDischargedLMTD", "LMTDFractionCharged", "LMTDMassFlow"
        ],
        charging_curve_name: str,
        availability_schedule_name: str | None = ...,
        timestep_of_the_curve_data: float | None = ...,
        parasitic_electric_load_during_discharging: float | None = ...,
        parasitic_electric_load_during_charging: float | None = ...,
        tank_loss_coefficient: float | None = ...,
        freezing_temperature_of_storage_medium: float | None = 0,
        thaw_process_indicator: Literal["", "InsideMelt", "OutsideMelt"] | None = "OutsideMelt",
    ) -> None: ...

class ZoneHVACTerminalUnitVariableRefrigerantFlow_v9_2:
    def __call__(
        self,
        name: str = "",
        /,
        *,
        terminal_unit_air_inlet_node_name: str,
        terminal_unit_air_outlet_node_name: str,
        supply_air_fan_operating_mode_schedule_name: str,
        supply_air_fan_object_name: str,
        terminal_unit_availability_schedule: str | None = ...,
        cooling_supply_air_flow_rate: float | Literal["Autosize"] | None = ...,
        no_cooling_supply_air_flow_rate: float | Literal["Autosize"] | None = ...,
        heating_supply_air_flow_rate: float | Literal["Autosize"] | None = ...,
        no_heating_supply_air_flow_rate: float | Literal["Autosize"] | None = ...,
        cooling_outdoor_air_flow_rate: float | Literal["Autosize"] | None = ...,
        heating_outdoor_air_flow_rate: float | Literal["Autosize"] | None = ...,
        no_load_outdoor_air_flow_rate: float | Literal["Autosize"] | None = ...,
        supply_air_fan_placement: Literal["", "BlowThrough", "DrawThrough"] | None = "BlowThrough",
        supply_air_fan_object_type: Literal[
            "", "Fan:ConstantVolume", "Fan:OnOff", "Fan:SystemModel", "Fan:VariableVolume"
        ]
        | None = "Fan:ConstantVolume",
        outside_air_mixer_object_type: Literal["OutdoorAir:Mixer"] | None = ...,
        outside_air_mixer_object_name: str | None = ...,
        cooling_coil_object_type: Literal[
            "Coil:Cooling:DX:VariableRefrigerantFlow", "Coil:Cooling:DX:VariableRefrigerantFlow:FluidTemperatureControl"
        ]
        | None = ...,
        cooling_coil_object_name: str | None = ...,
        heating_coil_object_type: Literal[
            "Coil:Heating:DX:VariableRefrigerantFlow", "Coil:Heating:DX:VariableRefrigerantFlow:FluidTemperatureControl"
        ]
        | None = ...,
        heating_coil_object_name: str | None = ...,
        zone_terminal_unit_on_parasitic_electric_energy_use: float | None = 0,
        zone_terminal_unit_off_parasitic_electric_energy_use: float | None = 0,
        rated_heating_capacity_sizing_ratio: float | None = 1,
        availability_manager_list_name: str | None = ...,
        design_specification_zonehvac_sizing_object_name: str | None = ...,
        supplemental_heating_coil_object_type: Literal[
            "Coil:Heating:Electric", "Coil:Heating:Fuel", "Coil:Heating:Steam", "Coil:Heating:Water"
        ]
        | None = ...,
        supplemental_heating_coil_name: str | None = ...,
        maximum_supply_air_temperature_from_supplemental_heater: float | Literal["", "Autosize"] | None = "Autosize",
        maximum_outdoor_dry_bulb_temperature_for_supplemental_heater_operation: float | None = 21,
    ) -> None: ...

class AirLoopHVACUnitaryHeatCoolVAVChangeoverBypass_v8_9_to_v9_1:
    def __call__(
        self,
        name: str,
        /,
        *,
        cooling_supply_air_flow_rate: float | Literal["Autosize"],
        heating_supply_air_flow_rate: float | Literal["Autosize"],
        cooling_outdoor_air_flow_rate: float | Literal["Autosize"],
        heating_outdoor_air_flow_rate: float | Literal["Autosize"],
        air_inlet_node_name: str,
        bypass_duct_mixer_node_name: str,
        bypass_duct_splitter_node_name: str,
        air_outlet_node_name: str,
        outdoor_air_mixer_object_type: Literal["OutdoorAir:Mixer"],
        outdoor_air_mixer_name: str,
        supply_air_fan_object_type: Literal["Fan:ConstantVolume", "Fan:OnOff", "Fan:SystemModel"],
        supply_air_fan_name: str,
        supply_air_fan_placement: Literal["BlowThrough", "DrawThrough"],
        cooling_coil_object_type: Literal[
            "Coil:Cooling:DX:SingleSpeed",
            "Coil:Cooling:DX:TwoStageWithHumidityControlMode",
            "Coil:Cooling:DX:VariableSpeed",
            "CoilSystem:Cooling:DX:HeatExchangerAssisted",
        ],
        cooling_coil_name: str,
        heating_coil_object_type: Literal[
            "Coil:Heating:DX:SingleSpeed",
            "Coil:Heating:DX:VariableSpeed",
            "Coil:Heating:Electric",
            "Coil:Heating:Fuel",
            "Coil:Heating:Steam",
            "Coil:Heating:Water",
        ],
        heating_coil_name: str,
        availability_schedule_name: str | None = ...,
        no_load_supply_air_flow_rate: float | Literal["Autosize"] | None = ...,
        no_load_outdoor_air_flow_rate: float | Literal["Autosize"] | None = ...,
        outdoor_air_flow_rate_multiplier_schedule_name: str | None = ...,
        supply_air_fan_operating_mode_schedule_name: str | None = ...,
        priority_control_mode: Literal["", "CoolingPriority", "HeatingPriority", "ZonePriority"]
        | None = "ZonePriority",
        minimum_outlet_air_temperature_during_cooling_operation: float | None = 8,
        maximum_outlet_air_temperature_during_heating_operation: float | None = 50,
        dehumidification_control_type: Literal["", "CoolReheat", "Multimode", "None"] | None = "None",
    ) -> None: ...

class AirflowNetworkDistributionComponentReliefAirFlow_v8_9:
    def __call__(
        self,
        name: str,
        /,
        *,
        air_mass_flow_coefficient_when_no_outdoor_air_flow_at_reference_conditions: float,
        air_mass_flow_exponent_when_no_outdoor_air_flow: float | None = 0.65,
        reference_crack_conditions: str | None = ...,
    ) -> None: ...

class InternalMass_v8_9_to_v9_1:
    def __call__(self, name: str, /, *, construction_name: str, zone_name: str, surface_area: float) -> None: ...

class RoomAirTemperaturePatternSurfaceMapping_v8_9_to_v22_1:
    def __call__(
        self,
        name: str,
        /,
        *,
        control_integer_for_pattern_control_schedule_name: float,
        thermostat_offset: float | None = ...,
        return_air_offset: float | None = ...,
        exhaust_air_offset: float | None = ...,
        surface_deltas: list[_g.RoomAirTemperaturePatternSurfaceMappingSurfaceDeltasItem] = ...,
    ) -> None: ...

class OutputSQLite_v8_9_to_v9_4:
    def __call__(self, /, *, option_type: Literal["Simple", "SimpleAndTabular"] | None = ...) -> None: ...

class OutputSQLite_v9_5_to_v23_2:
    def __call__(
        self,
        /,
        *,
        option_type: Literal["Simple", "SimpleAndTabular"] | None = ...,
        unit_conversion_for_tabular_data: Literal[
            "", "InchPound", "JtoGJ", "JtoKWH", "JtoMJ", "None", "UseOutputControlTableStyle"
        ]
        | None = "UseOutputControlTableStyle",
    ) -> None: ...

class CoilCoolingWaterToAirHeatPumpEquationFit_v9_5_to_v22_1:
    def __call__(
        self,
        name: str,
        /,
        *,
        water_inlet_node_name: str,
        water_outlet_node_name: str,
        air_inlet_node_name: str,
        air_outlet_node_name: str,
        rated_air_flow_rate: float | Literal["Autosize"],
        rated_water_flow_rate: float | Literal["Autosize"],
        gross_rated_total_cooling_capacity: float | Literal["Autosize"],
        gross_rated_sensible_cooling_capacity: float | Literal["Autosize"],
        gross_rated_cooling_cop: float,
        total_cooling_capacity_curve_name: str,
        sensible_cooling_capacity_curve_name: str,
        cooling_power_consumption_curve_name: str,
        nominal_time_for_condensate_removal_to_begin: float | None = 0,
        ratio_of_initial_moisture_evaporation_rate_and_steady_state_latent_capacity: float | None = 0,
    ) -> None: ...

class AirflowNetworkSimulationControl_v9_5_to_v22_1:
    def __call__(
        self,
        name: str,
        /,
        *,
        airflownetwork_control: Literal[
            "",
            "MultizoneWithDistribution",
            "MultizoneWithDistributionOnlyDuringFanOperation",
            "MultizoneWithoutDistribution",
            "NoMultizoneOrDistribution",
        ]
        | None = "NoMultizoneOrDistribution",
        wind_pressure_coefficient_type: Literal["", "Input", "SurfaceAverageCalculation"]
        | None = "SurfaceAverageCalculation",
        height_selection_for_local_wind_pressure_calculation: Literal["", "ExternalNode", "OpeningHeight"]
        | None = "OpeningHeight",
        building_type: Literal["", "HighRise", "LowRise"] | None = "LowRise",
        maximum_number_of_iterations: float | None = 500,
        initialization_type: Literal["", "LinearInitializationMethod", "ZeroNodePressures"]
        | None = "ZeroNodePressures",
        relative_airflow_convergence_tolerance: float | None = 0.0001,
        absolute_airflow_convergence_tolerance: float | None = ...,
        convergence_acceleration_limit: float | None = -0.5,
        azimuth_angle_of_long_axis_of_building: float | None = 0,
        ratio_of_building_width_along_short_axis_to_width_along_long_axis: float | None = 1,
        height_dependence_of_external_node_temperature: Literal["", "No", "Yes"] | None = "No",
        solver: Literal["", "ConjugateGradient", "SkylineLU"] | None = "SkylineLU",
        allow_unsupported_zone_equipment: Literal["", "No", "Yes"] | None = "No",
    ) -> None: ...

class ZonePropertyUserViewFactorsBySurfaceName_v9_4_to_v9_5:
    def __call__(
        self,
        /,
        *,
        zone_or_zonelist_name: str | None = ...,
        view_factors: list[_g.ZonePropertyUserViewFactorsBySurfaceNameViewFactorsItem] = ...,
    ) -> None: ...

class InternalMass_v24_2_to_v26_1:
    def __call__(
        self,
        name: str,
        /,
        *,
        construction_name: str,
        surface_area: float,
        zone_or_zonelist_name: str | None = ...,
        space_or_spacelist_name: str | None = ...,
    ) -> None: ...
