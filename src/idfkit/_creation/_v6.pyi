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
    ) -> None:
        """Create a new ``WindowMaterial:Glazing:EquivalentLayer`` and add it to the document.

        Glass material properties for Windows or Glass Doors Transmittance/Reflectance input method.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v9.1/io-reference/overview/group-surface-construction-elements/#windowmaterialglazingequivalentlayer
        """

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
    ) -> None:
        """Create a new ``ThermalStorage:Ice:Detailed`` and add it to the document.

        This input syntax is intended to describe a thermal storage system that includes smaller containers filled with water that are placed in a larger tank or series of tanks. The model uses polynomial equations to describe the system performance.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v25.1/io-reference/overview/group-water-heaters/#thermalstorageicedetailed
        """

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
    ) -> None:
        """Create a new ``ZoneHVAC:TerminalUnit:VariableRefrigerantFlow`` and add it to the document.

        Zone terminal unit with variable refrigerant flow (VRF) DX cooling and heating coils (air-to-air heat pump). The VRF terminal units are served by an AirConditioner:VariableRefrigerantFlow or AirConditioner:VariableRefrigerantFlow:FluidTemperatureControl:* system.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v9.2/io-reference/overview/group-zone-forced-air-units/#zonehvacterminalunitvariablerefrigerantflow
        """

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
    ) -> None:
        """Create a new ``AirLoopHVAC:UnitaryHeatCool:VAVChangeoverBypass`` and add it to the document.

        Unitary system, heating and cooling with constant volume supply fan (continuous or cycling), direct expansion (DX) cooling coil, heating coil (gas, electric, hot water, steam, or DX air-to-air heat pump) and bypass damper for variable volume flow to terminal units. Used with AirTerminal:SingleDuct:VAV:HeatAndCool:Reheat or AirTerminal:SingleDuct:VAV:HeatAndCool:NoReheat.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v9.1/io-reference/overview/group-unitary-equipment/#airloophvacunitaryheatcoolvavchangeoverbypass
        """

class AirflowNetworkDistributionComponentReliefAirFlow_v8_9:
    def __call__(
        self,
        name: str,
        /,
        *,
        air_mass_flow_coefficient_when_no_outdoor_air_flow_at_reference_conditions: float,
        air_mass_flow_exponent_when_no_outdoor_air_flow: float | None = 0.65,
        reference_crack_conditions: str | None = ...,
    ) -> None:
        """Create a new ``AirflowNetwork:Distribution:Component:ReliefAirFlow`` and add it to the document.

        This object allows variation of air flow rate to perform pressure.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v8.9/io-reference/overview/group-airflow-network/#airflownetworkdistributioncomponentreliefairflow
        """

class InternalMass_v8_9_to_v9_1:
    def __call__(self, name: str, /, *, construction_name: str, zone_name: str, surface_area: float) -> None:
        """Create a new ``InternalMass`` and add it to the document.

        Used to describe internal zone surface area that does not need to be part of geometric representation. This should be the total surface area exposed to the zone air.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v9.1/io-reference/overview/group-thermal-zone-description-geometry/#internalmass
        """

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
    ) -> None:
        """Create a new ``RoomAir:TemperaturePattern:SurfaceMapping`` and add it to the document.

        Defines a distribution pattern for the air temperatures adjacent to individual surfaces. This allows controlling the adjacent air temperature on a surface-by-surface basis rather than by height. This allows modeling different adjacent air temperatures on the opposite sides of the zone. Used in combination with RoomAir:TemperaturePattern:UserDefined.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v22.1/io-reference/overview/group-room-air-models/#roomairtemperaturepatternsurfacemapping
        """

class OutputSQLite_v8_9_to_v9_4:
    def __call__(self, /, *, option_type: Literal["Simple", "SimpleAndTabular"] | None = ...) -> None:
        """Create a new ``Output:SQLite`` and add it to the document.

        Output from EnergyPlus can be written to an SQLite format file.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v9.4/io-reference/input-for-output/#outputsqlite
        """

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
    ) -> None:
        """Create a new ``Output:SQLite`` and add it to the document.

        Output from EnergyPlus can be written to an SQLite format file.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v23.2/io-reference/input-for-output/#outputsqlite
        """

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
    ) -> None:
        """Create a new ``Coil:Cooling:WaterToAirHeatPump:EquationFit`` and add it to the document.

        Direct expansion (DX) cooling coil for water-to-air heat pump (includes electric compressor), single-speed, equation-fit model. Optional inputs for moisture evaporation from wet coil when compressor cycles off with continuous fan operation. Equation-fit model uses normalized curves to describe the heat pump performance.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v22.1/io-reference/overview/group-heating-and-cooling-coils/#coilcoolingwatertoairheatpumpequationfit
        """

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
    ) -> None:
        """Create a new ``AirflowNetwork:SimulationControl`` and add it to the document.

        This object defines the global parameters used in an Airflow Network simulation.

        A default shown is what EnergyPlus applies to a field left empty; only fields passed are stored.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v22.1/io-reference/overview/group-airflow-network/#airflownetworksimulationcontrol
        """

class ZonePropertyUserViewFactorsBySurfaceName_v9_4_to_v9_5:
    def __call__(
        self,
        /,
        *,
        zone_or_zonelist_name: str | None = ...,
        view_factors: list[_g.ZonePropertyUserViewFactorsBySurfaceNameViewFactorsItem] = ...,
    ) -> None:
        """Create a new ``ZoneProperty:UserViewFactors:BySurfaceName`` and add it to the document.

        View factors for Surface to Surface in a zone. (Number of Surfaces)**2 are expected. Any omitted surface pairs will be assumed to have a view factor of zero.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v9.5/io-reference/overview/group-advanced-surface-concepts/#zonepropertyuserviewfactorsbysurfacename
        """

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
    ) -> None:
        """Create a new ``InternalMass`` and add it to the document.

        Used to describe internal zone surface area that does not need to be part of geometric representation. This should be the total surface area exposed to the zone air. If you use a ZoneList in the Zone or ZoneList name field then this definition applies to all the zones in the ZoneList. Likewise for SpaceList.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.1/io-reference/overview/group-thermal-zone-description-geometry/#internalmass
        """
