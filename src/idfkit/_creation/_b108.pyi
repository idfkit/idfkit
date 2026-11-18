"""Creation signatures of generated classes (stub only).

DO NOT EDIT — regenerate with:
    python -m idfkit.codegen.generate_stubs
"""

from __future__ import annotations

from collections.abc import Sequence
from typing import Literal

from typing_extensions import Never

from .. import _generated_types as _g

class ShadingSite:
    def __call__(
        self,
        name: str,
        /,
        *,
        azimuth_angle: float | None = ...,
        tilt_angle: float | None = 90,
        starting_x_coordinate: float | None = ...,
        starting_y_coordinate: float | None = ...,
        starting_z_coordinate: float | None = ...,
        length: float | None = ...,
        height: float | None = ...,
    ) -> None:
        """Create a new ``Shading:Site`` and add it to the document.

        used for shading elements such as trees these items are fixed in space and would not move with relative geometry

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-thermal-zones-and-surfaces/#shadingsite
        """

class ZoneContaminantSourceAndSinkGenericDepositionRateSink:
    def __call__(
        self, name: str, /, *, zone_name: str, schedule_name: str, deposition_rate: float | None = ...
    ) -> None:
        """Create a new ``ZoneContaminantSourceAndSink:Generic:DepositionRateSink`` and add it to the document.

        Simulate generic contaminant source driven by the boundary layer diffusion controlled model.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-internal-gains-people-lights-other/#zonecontaminantsourceandsinkgenericdepositionratesink
        """

class AnyZoneRefrigerationDoorMixing:
    def __call__(
        self,
        name: str,
        /,
        *,
        narrow_with_as_version_first: Never,
        schedule_name: str,
        door_height: float | None = 3,
        door_area: float | None = 9,
        door_protection_type: Literal["AirCurtain", "None", "StripCurtain"] | None = "None",
    ) -> None:
        """Create a new ``ZoneRefrigerationDoorMixing`` and add it to the document.

        Refrigeration Door Mixing is used for an opening between two zones (or spaces) that are at the same elevation but have different air temperatures. In this case, the mixing air flow between the two zones is determined by the density difference between the two zones. This would typically be used between two zones in a refrigerated warehouse that are controlled at different temperatures. It could also be used to model a door to a walk-in refrigerated space if that space were modeled as a zone instead of using the object Refrigeration:WalkIn.

        No call suits every release: narrow the document with ``as_version`` first.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-airflow/#zonerefrigerationdoormixing
        """

class HVACTemplateZoneVRF:
    def __call__(
        self,
        /,
        *,
        zone_name: str,
        template_vrf_system_name: str,
        template_thermostat_name: str | None = ...,
        zone_heating_sizing_factor: float | None = ...,
        zone_cooling_sizing_factor: float | None = ...,
        rated_total_heating_capacity_sizing_ratio: float | None = 1,
        cooling_supply_air_flow_rate: float | Literal["Autosize"] | None = "Autosize",
        no_cooling_supply_air_flow_rate: float | Literal["Autosize"] | None = "Autosize",
        heating_supply_air_flow_rate: float | Literal["Autosize"] | None = "Autosize",
        no_heating_supply_air_flow_rate: float | Literal["Autosize"] | None = "Autosize",
        cooling_outdoor_air_flow_rate: float | Literal["Autosize"] | None = "Autosize",
        heating_outdoor_air_flow_rate: float | Literal["Autosize"] | None = "Autosize",
        no_load_outdoor_air_flow_rate: float | Literal["Autosize"] | None = "Autosize",
        outdoor_air_method: Literal["DetailedSpecification", "Flow/Area", "Flow/Person", "Flow/Zone", "Maximum", "Sum"]
        | None = "Flow/Person",
        outdoor_air_flow_rate_per_person: float | None = 0.00944,
        outdoor_air_flow_rate_per_zone_floor_area: float | None = 0,
        outdoor_air_flow_rate_per_zone: float | None = 0,
        design_specification_outdoor_air_object_name: str | None = ...,
        design_specification_zone_air_distribution_object_name: str | None = ...,
        system_availability_schedule_name: str | None = ...,
        supply_fan_operating_mode_schedule_name: str | None = ...,
        supply_air_fan_placement: Literal["BlowThrough", "DrawThrough"] | None = "BlowThrough",
        supply_fan_total_efficiency: float | None = 0.7,
        supply_fan_delta_pressure: float | None = 75,
        supply_fan_motor_efficiency: float | None = 0.9,
        cooling_coil_type: Literal["None", "VariableRefrigerantFlowDX"] | None = "VariableRefrigerantFlowDX",
        cooling_coil_availability_schedule_name: str | None = ...,
        cooling_coil_gross_rated_total_capacity: float | Literal["Autosize"] | None = "Autosize",
        cooling_coil_gross_rated_sensible_heat_ratio: float | Literal["Autosize"] | None = "Autosize",
        heat_pump_heating_coil_type: Literal["None", "VariableRefrigerantFlowDX"] | None = "VariableRefrigerantFlowDX",
        heat_pump_heating_coil_availability_schedule_name: str | None = ...,
        heat_pump_heating_coil_gross_rated_capacity: float | Literal["Autosize"] | None = "Autosize",
        zone_terminal_unit_on_parasitic_electric_energy_use: float | None = 0,
        zone_terminal_unit_off_parasitic_electric_energy_use: float | None = 0,
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
        baseboard_heating_type: Literal["Electric", "HotWater", "None"] | None = "None",
        baseboard_heating_availability_schedule_name: str | None = ...,
        baseboard_heating_capacity: float | Literal["Autosize"] | None = "Autosize",
    ) -> None:
        """Create a new ``HVACTemplate:Zone:VRF`` and add it to the document.

        Zone terminal unit with variable refrigerant flow (VRF) DX cooling and heating coils (air-to-air or water-to-air heat pump). The VRF terminal units are served by an HVACTemplate:System:VRF system.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/hvac-template-objects/group-hvac-templates/#hvactemplatezonevrf
        """

class AirTerminalSingleDuctSeriesPIUReheat:
    def __call__(
        self,
        name: str,
        /,
        *,
        maximum_air_flow_rate: float | Literal["Autosize"],
        maximum_primary_air_flow_rate: float | Literal["Autosize"],
        minimum_primary_air_flow_fraction: float | Literal["Autosize"],
        reheat_coil_object_type: Literal[
            "Coil:Heating:Electric", "Coil:Heating:Fuel", "Coil:Heating:Steam", "Coil:Heating:Water"
        ],
        reheat_coil_name: str,
        availability_schedule_name: str | None = ...,
        supply_air_inlet_node_name: str | None = ...,
        secondary_air_inlet_node_name: str | None = ...,
        outlet_node_name: str | None = ...,
        zone_mixer_name: str | None = ...,
        fan_name: str | None = ...,
        maximum_hot_water_or_steam_flow_rate: float | Literal["Autosize"] | None = ...,
        minimum_hot_water_or_steam_flow_rate: float | None = 0,
        convergence_tolerance: float | None = 0.001,
        fan_control_type: Literal["ConstantSpeed", "VariableSpeed"] | None = "ConstantSpeed",
        minimum_fan_turn_down_ratio: float | None = 0.3,
        heating_control_type: Literal["Modulated", "Staged"] | None = ...,
        design_heating_discharge_air_temperature: float | None = 32.1,
        high_limit_heating_discharge_air_temperature: float | None = 37.7,
    ) -> None:
        """Create a new ``AirTerminal:SingleDuct:SeriesPIU:Reheat`` and add it to the document.

        Central air system terminal unit, single duct, variable volume, series powered induction unit (PIU), with reheat coil (hot water, electric, gas, or steam).

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-zone-hvac-air-loop-terminal-units/#airterminalsingleductseriespiureheat
        """

class ChillerHeaterAbsorptionDirectFired:
    def __call__(
        self,
        name: str,
        /,
        *,
        chilled_water_inlet_node_name: str,
        chilled_water_outlet_node_name: str,
        condenser_inlet_node_name: str,
        hot_water_inlet_node_name: str,
        hot_water_outlet_node_name: str,
        nominal_cooling_capacity: float | Literal["Autosize"] | None = "Autosize",
        heating_to_cooling_capacity_ratio: float | None = 0.8,
        fuel_input_to_cooling_output_ratio: float | None = 0.97,
        fuel_input_to_heating_output_ratio: float | None = 1.25,
        electric_input_to_cooling_output_ratio: float | None = 0.01,
        electric_input_to_heating_output_ratio: float | None = 0,
        condenser_outlet_node_name: str | None = ...,
        minimum_part_load_ratio: float | None = 0.1,
        maximum_part_load_ratio: float | None = 1,
        optimum_part_load_ratio: float | None = 1,
        design_entering_condenser_water_temperature: float | None = 29,
        design_leaving_chilled_water_temperature: float | None = 7,
        design_chilled_water_flow_rate: float | Literal["Autosize"] | None = "Autosize",
        design_condenser_water_flow_rate: float | Literal["Autosize"] | None = "Autosize",
        design_hot_water_flow_rate: float | Literal["Autosize"] | None = "Autosize",
        cooling_capacity_function_of_temperature_curve_name: str | None = ...,
        fuel_input_to_cooling_output_ratio_function_of_temperature_curve_name: str | None = ...,
        fuel_input_to_cooling_output_ratio_function_of_part_load_ratio_curve_name: str | None = ...,
        electric_input_to_cooling_output_ratio_function_of_temperature_curve_name: str | None = ...,
        electric_input_to_cooling_output_ratio_function_of_part_load_ratio_curve_name: str | None = ...,
        heating_capacity_function_of_cooling_capacity_curve_name: str | None = ...,
        fuel_input_to_heat_output_ratio_during_heating_only_operation_curve_name: str | None = ...,
        temperature_curve_input_variable: Literal["EnteringCondenser", "LeavingCondenser"] | None = "EnteringCondenser",
        condenser_type: Literal["AirCooled", "WaterCooled"] | None = "WaterCooled",
        chilled_water_temperature_lower_limit: float | None = 2,
        fuel_higher_heating_value: float | None = 0,
        fuel_type: Literal[
            "Diesel", "FuelOilNo1", "FuelOilNo2", "Gasoline", "NaturalGas", "OtherFuel1", "OtherFuel2", "Propane"
        ]
        | None = "NaturalGas",
        sizing_factor: float | None = 1,
    ) -> None:
        """Create a new ``ChillerHeater:Absorption:DirectFired`` and add it to the document.

        Direct fired gas absorption chiller-heater using performance curves similar to DOE-2

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-plant-equipment/#chillerheaterabsorptiondirectfired
        """

class AnyGroundHeatExchangerSystem:
    def __call__(
        self,
        name: str,
        /,
        *,
        inlet_node_name: str,
        outlet_node_name: str,
        design_flow_rate: float,
        undisturbed_ground_temperature_model_type: Literal[
            "Site:GroundTemperature:Undisturbed:FiniteDifference",
            "Site:GroundTemperature:Undisturbed:KusudaAchenbach",
            "Site:GroundTemperature:Undisturbed:Xing",
        ],
        undisturbed_ground_temperature_model_name: str,
        ground_thermal_conductivity: float,
        ground_thermal_heat_capacity: float,
        ghe_vertical_responsefactors_object_name: str | None = ...,
        ghe_vertical_array_object_name: str | None = ...,
        vertical_well_locations: Sequence[
            _g.GroundHeatExchangerSystemVerticalWellLocationsItem
            | _g.GroundHeatExchangerSystemVerticalWellLocationsGroup
        ] = ...,
    ) -> None:
        """Create a new ``GroundHeatExchanger:System`` and add it to the document.

        Models vertical ground heat exchangers systems using the response factor approach developed by Eskilson. Response factors are calculated using a finite line source model assuming uniform heat flux at the borehole wall if UHFcalc is specified, or uniform borehole wall temperature if UBHWTcalc is specified.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-condenser-equipment/#groundheatexchangersystem
        """

class AvailabilityManagerDifferentialThermostat:
    def __call__(
        self,
        name: str,
        /,
        *,
        hot_node_name: str,
        cold_node_name: str,
        temperature_difference_on_limit: float,
        temperature_difference_off_limit: float | None = ...,
    ) -> None:
        """Create a new ``AvailabilityManager:DifferentialThermostat`` and add it to the document.

        Overrides fan/pump schedules depending on temperature difference between two nodes.

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-system-availability-managers/#availabilitymanagerdifferentialthermostat
        """

class FaultModelFoulingAirFilter:
    def __call__(
        self,
        name: str,
        /,
        *,
        fan_object_type: Literal["Fan:ConstantVolume", "Fan:OnOff", "Fan:VariableVolume"],
        fan_name: str,
        pressure_fraction_schedule_name: str,
        fan_curve_name: str,
        availability_schedule_name: str | None = ...,
    ) -> None:
        """Create a new ``FaultModel:Fouling:AirFilter`` and add it to the document.

        This object describes fault of dirty air filters

        EnergyPlus I/O Reference: https://docs.idfkit.com/v26.2/io-reference/overview/group-operational-faults/#faultmodelfoulingairfilter
        """
